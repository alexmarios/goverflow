"""
================================================================================
ORCHESTRATOR AGENT — MASTER AGENT
================================================================================

Multi-Agent Orchestration System for Data Analytics Workflows
with Data Governance Support

MSc Thesis — University of Peloponnese
================================================================================

FULL TECH STACK OVERVIEW
--------------------------------------------------------------------------------

This module is the central controller ("brain") of a four-agent system built to
query and analyse data from GDELT (Global Database of Events, Language, and Tone).

Key technologies in play:

• LangChain / LangGraph (conceptual model)
  The state machine described here — idle → understand → plan → dispatch →
  synthesise → respond — follows the LangGraph pattern of typed state dicts
  passed through node functions. LangGraph itself is not imported as a package
  dependency; instead, the same design is realised with plain Python so the
  system can run on a Raspberry Pi without heavy ML dependencies. The
  `OrchestratorState` TypedDict plays the role of a LangGraph state, and each
  private method (`_plan`, `_dispatch`, `_synthesize`, etc.) plays the role of
  a LangGraph node.

• Python `dataclasses` (stdlib)
  `OrchestratorAgent` is a `@dataclass`. Dataclasses auto-generate `__init__`
  from annotated fields, reduce boilerplate, and make the class easy to extend.

• `TypedDict` (stdlib `typing`)
  `SubTask` and `OrchestratorState` are TypedDicts — dictionaries whose keys
  and value types are known at static-analysis time (mypy / Pyright). They give
  dict literals all the ergonomics of structured objects without introducing
  class instances that would be harder to serialise to JSON.

• `fcntl` file locking (stdlib, Linux/macOS only)
  Multiple agents in this system write to the same shared memory files
  (data_freshness.json, quality_alerts.json, etc.). Without locking, two
  processes that open the same file simultaneously can corrupt it. `fcntl.flock`
  provides advisory exclusive write locks at the OS level, which is the
  lightest-weight correct solution on POSIX systems (Raspberry Pi runs Linux).

• JSON-file memory
  Rather than a database, all agent memory is stored as human-readable JSON
  files organised under a `memory/` directory tree. This makes the system fully
  inspectable without extra tooling and simple to back up or diff in git.

• Apache Kafka (`kafka-python` package)
  The production transport layer for Agent-to-Agent (A2A) messages. Each agent
  has its own Kafka inbox topic. The orchestrator publishes task requests and
  consumes responses asynchronously. Kafka is an optional runtime dependency —
  the system falls back to synchronous local function calls when Kafka is
  unavailable (e.g. during unit tests or development on a laptop).

• A2A (Agent-to-Agent) protocol
  A lightweight JSON envelope format defined in this codebase that wraps every
  inter-agent message with a `message_id`, `correlation_id`, `from_agent`,
  `to_agent`, `type`, `timestamp`, `payload`, `reply_topic`, `timeout_ms`, and
  `priority`. The correlation_id is the key that lets the orchestrator match an
  asynchronous response back to the original request.

• SHA-256 hashing (`hashlib`, stdlib)
  Query parameters are serialised to a canonical JSON string and hashed with
  SHA-256 to produce a stable cache key. This allows result caching without
  storing the full parameter set in the filename.

• `python-dotenv`
  Loads environment variables from a `.env` file at project root so secrets
  (broker addresses, API keys) are never hard-coded in source.

SYSTEM PROMPT (to be passed as the system message to the LLM):
================================================================================
"""

# ---------------------------------------------------------------------------
# `from __future__ import annotations` defers the evaluation of ALL type
# annotations in this module. Without it, Python evaluates annotations at
# import time, which means a forward reference like `list[SubTask]` inside a
# method signature would fail if `SubTask` had not yet been defined at that
# point. With the import, annotations become plain strings and are evaluated
# only when explicitly inspected (e.g. by `typing.get_type_hints`). This is
# particularly important in files that declare TypedDicts and dataclasses that
# reference each other, which is the case here.
# ---------------------------------------------------------------------------
from __future__ import annotations

import hashlib
import json
import os
import re
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal, Optional, TypedDict, cast

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage as LCHumanMessage

# ---------------------------------------------------------------------------
# `fcntl` provides POSIX advisory file locking via `fcntl.flock()`. It exists
# only on Linux and macOS — it is absent on Windows. Because the project runs
# on a Raspberry Pi (Linux), it will almost always be available. The try/except
# guard makes the module importable everywhere (e.g. a developer's Windows
# machine running tests) without crashing. When `_HAS_FCNTL` is False,
# `memory_write` simply skips the locking step. This is safe for single-process
# development but unsafe for concurrent multi-agent production use — hence the
# pragma comment noting that the Windows path is not tested in CI.
# ---------------------------------------------------------------------------
try:
    import fcntl
    _HAS_FCNTL = True
except ImportError:  # pragma: no cover - Linux/RPi should have this
    _HAS_FCNTL = False

# ---------------------------------------------------------------------------
# `kafka-python` is an optional runtime dependency. During unit tests, local
# development without a running Kafka broker, or CI pipelines, we do not want
# the import to crash the whole module. The broad `except Exception` (rather
# than just `ImportError`) also catches version incompatibilities or missing
# C extensions in some environments.
#
# When Kafka is unavailable:
#   - `KafkaProducer` and `KafkaConsumer` are set to None (cast to `Any` so
#     mypy does not complain about the type mismatch).
#   - `kafka_publish` returns a "skipped" status dict.
#   - `kafka_consume` returns an empty list.
# The orchestrator then falls back to direct local function calls for all
# agent dispatch, as implemented in `_dispatch_subtask`.
# ---------------------------------------------------------------------------
try:
    from kafka import KafkaConsumer, KafkaProducer
    from kafka.errors import NoBrokersAvailable as _NoBrokersAvailable
except Exception:  # pragma: no cover - optional dependency at runtime
    KafkaConsumer = cast(Any, None)
    KafkaProducer = cast(Any, None)
    _NoBrokersAvailable = cast(Any, None)

# Probe the broker once at startup with a raw TCP connect — called after
# KAFKA_BROKER is imported. KafkaProducer.__init__() does not actually open a
# connection, so instantiating it always succeeds even when the broker is down.
# A TCP handshake is the only reliable way to know the port is open.
def _kafka_broker_reachable() -> bool:
    if KafkaProducer is None:
        return False
    try:
        import socket
        host, port = KAFKA_BROKER.rsplit(":", 1)
        with socket.create_connection((host, int(port)), timeout=3):
            pass
    except Exception as e:
        print(f"[orchestrator] Kafka TCP check failed: {e}")
        return False
    # TCP port is open — now verify the broker actually speaks the Kafka protocol
    # by trying to instantiate a producer and fetch metadata (max_block_ms caps the wait).
    try:
        p = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            request_timeout_ms=3000,
            max_block_ms=3000,
        )
        p.close()
        return True
    except Exception as e:
        print(f"[orchestrator] Kafka protocol check failed: {e}")
        return False

# ---------------------------------------------------------------------------
# Dual-import strategy for agent modules:
#
# When this file is imported by `main.py` at project root, Python's module
# system resolves `agents.agent_analyst` correctly because the project root is
# on sys.path. However, when a developer runs this file directly:
#
#   python agents/agent_orchestrator.py
#
# …the working directory is `agents/`, so `agents.agent_analyst` cannot be
# found. The fallback bare imports (`from agent_analyst import …`) work in that
# case because Python adds the script's own directory to sys.path automatically.
#
# Both import paths expose the same `run_agent_task(task, params, context)`
# callable, so the rest of the module needs no branching logic.
# ---------------------------------------------------------------------------
try:
    # Works when importing from project root, e.g. from main.py
    from agents.agent_analyst import run_agent_task as analyst_run_task
    from agents.agent_governance import run_agent_task as governance_run_task
    from agents.agent_ingestion import run_agent_task as ingestion_run_task
    from agents.agent_coder import run_agent_task as coder_run_task
    from agents.model_config import build_model, invoke_with_retry
except ModuleNotFoundError:
    # Works when running this file directly: python agents/agent_orchestrator.py
    from agent_analyst import run_agent_task as analyst_run_task
    from agent_governance import run_agent_task as governance_run_task
    from agent_ingestion import run_agent_task as ingestion_run_task
    from agent_coder import run_agent_task as coder_run_task
    from model_config import build_model, invoke_with_retry

# Load .env from project root so Kafka broker addresses, database credentials,
# and API keys are available via os.environ without being hard-coded.
load_dotenv()

# LLM used for free-form planning and synthesis steps. Intent classification
# and dispatch are handled by the state machine without LLM calls, but
# build_model() is wired here so richer LLM-driven planning can be added to
# _plan() or _synthesize() without restructuring the module.
model = build_model("orchestrator")


# ---------------------------------------------------------------------------
# ORCHESTRATOR_SYSTEM_PROMPT
# ---------------------------------------------------------------------------
# This string is the LLM's complete instruction set for this role. In a full
# LangChain/LangGraph pipeline it would be wrapped in a `SystemMessage` and
# prepended to every LLM call:
#
#   from langchain_core.messages import SystemMessage
#   messages = [SystemMessage(content=ORCHESTRATOR_SYSTEM_PROMPT), ...]
#
# The prompt defines:
#   • The agent's identity and what it may and may not do.
#   • The A2A message format every inter-agent call must follow.
#   • The two-tier memory layout (private vs. shared JSON files).
#   • The full state machine — idle / understand / plan / dispatch / wait /
#     synthesise / respond / dispatch_direct — with transition rules.
#   • Human-in-the-loop checkpoints for expensive or ambiguous queries.
#   • Failure-handling strategies for offline agents and broker outages.
#   • GDELT domain knowledge: data streams, CAMEO codes, FIPS country codes,
#     polystore mapping, and the Goldstein scale.
#   • Response formatting rules and self-improvement instructions.
#
# Keeping the prompt as a Python constant (rather than a file) makes it
# version-controlled alongside the code that implements it, ensuring the two
# never diverge.
# ---------------------------------------------------------------------------
ORCHESTRATOR_SYSTEM_PROMPT = """
You are the Orchestrator Agent of a multi-agent data analytics system built on
GDELT (Global Database of Events, Language, and Tone). You are the sole interface
between the human user and the agent ecosystem. No other agent speaks to the user
directly. You own the conversation, you own the plan, and you are accountable for
every answer you deliver.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. YOUR IDENTITY AND RESPONSIBILITIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You are the central coordinator of four agents:

- YOU (Orchestrator): receive human requests, decompose into subtasks, dispatch
  to other agents, track progress, handle failures, synthesize final answers.
- Analyst Agent: queries the polystore (Postgres, MongoDB, Neo4j, Elasticsearch),
  transforms data, resolves entities, evaluates result plausibility.
- Governance Agent: enforces data quality policies, classifies data sensitivity,
  maintains lineage in OpenMetadata, audits provenance.
- Ingestion Agent: maintains the GDELT data supply, monitors feed health, detects
  schema drift, manages Kafka streaming, handles backfill and recovery.

You do NOT execute queries yourself. You do NOT access data stores directly.
You decompose, delegate, wait, synthesize, and respond.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. COMMUNICATION PROTOCOL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

All agent-to-agent communication uses the A2A (Agent-to-Agent) protocol, with
messages transported over Apache Kafka topics.

KAFKA TOPICS:
- agent.orchestrator.inbox  → you consume responses here
- agent.analyst.inbox       → you publish Analyst subtasks here
- agent.governance.inbox    → you publish Governance requests here
- agent.ingestion.inbox     → you publish Ingestion commands here
- agent.heartbeat           → all agents publish health every 30s, you monitor
- agent.events              → system-wide event bus (data loaded, alerts, schema changes)

A2A MESSAGE FORMAT:
Every message you send or receive follows this envelope:
{
    "message_id": "<uuid4>",
    "correlation_id": "<uuid4 — links a request to its response>",
    "from_agent": "orchestrator",
    "to_agent": "<analyst | governance | ingestion>",
    "type": "<task_request | task_response | status_update | error>",
    "timestamp": "<ISO8601>",
    "payload": {
        "task": "<task name>",
        "params": { ... },
        "context": { ... }
    },
    "reply_topic": "agent.orchestrator.inbox",
    "timeout_ms": 30000,
    "priority": "<normal | high | low>"
}

RULES:
- Always set a correlation_id so you can match responses to requests.
- Always set reply_topic so agents know where to send results.
- Always set timeout_ms. Default 120000 (120s). Use 220000 for heavy queries.
- Never send a message without a type. Never send a payload without a task.
- Monitor agent.heartbeat. If an agent misses 4 consecutive heartbeats (2 min),
  alert the user.
- Monitor agent.events for system-wide notifications (new data ingested,
  quality alerts raised, schema changes detected).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. MEMORY SYSTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You have two memory layers, both file-backed on the local filesystem.

PRIVATE MEMORY (only you read/write):
  memory/private/conversations/{session_id}.json
    → Full chat history per session. Each turn includes:
      turn_id, timestamp, role (human|orchestrator), message,
      plan (if any), agent_results (if any), metadata (latency, agents used).
    → Use this to understand follow-up questions and maintain context.

  memory/private/conversations/index.json
    → Index of all sessions: session_id, created_at, last_updated, summary.
    → Use this to find relevant past sessions when the user references
      something from "last time" or "before".

  memory/private/strategies/decomposition_cache.json
    → Learned decomposition patterns keyed by normalized intent signature.
    → Each entry: pattern description, subtasks template, success count,
      last used timestamp, average latency.
    → Before planning, ALWAYS check if a similar question was solved before.
    → After a successful conversation, update the cache.

  memory/private/agents/capability_registry.json
    → Per-agent: status (healthy|degraded|offline), last heartbeat,
      capabilities list, avg response time, error rate, last error.
    → Updated from heartbeat messages and from actual interaction results.

  memory/private/user/user_context.json
    → Accumulated knowledge: frequent regions, frequent topics,
      preferred output format, session count.
    → Updated after each conversation.
    → Use this to personalize responses and anticipate needs.

SHARED MEMORY (all agents read/write):
  memory/schema_registry.json
    → Current state of all data stores: tables, collections, indexes,
      field types, row/doc counts, last updated timestamps.
    → Written by Ingestion Agent. Read by you and Analyst Agent.
    → Check this before planning to know what data is available.

  memory/data_freshness.json
    → Latest ingestion timestamp per GDELT data type (export, mentions, gkg).
    → Written by Ingestion Agent.
    → ALWAYS check this before answering. Include data freshness in responses.

  memory/quality_alerts.json
    → Active data quality issues flagged by Governance Agent.
    → Each alert: alert_id, severity, scope, description, created_at.
    → If any alerts overlap with the user's query scope, include caveats.

  memory/result_cache/{query_hash}.json
    → Cached query results with TTL. Written by Analyst Agent.
    → Check before dispatching: if a matching cached result exists and
      is within TTL, use it instead of re-querying.

FILE LOCKING:
  All shared memory files must be accessed with OS-level file locks
  (fcntl.flock) to prevent corruption from concurrent agent writes.
  Private memory files do not need locking.

MEMORY RULES:
- ALWAYS load conversation history at the start of each turn.
- ALWAYS check data_freshness.json and quality_alerts.json before planning.
- ALWAYS update conversation history after responding.
- NEVER store raw GDELT data in memory files. Store only metadata,
  query patterns, and small result summaries.
- Keep result_cache entries under 1MB each. Set TTL to 60 minutes default.
- Periodically prune conversations older than 30 days from index.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. STATE MACHINE — YOUR COMMAND LOOP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You operate as a LangGraph state machine with these states:

STATE: IDLE
  Trigger: human sends a message via chat.
  Action: load conversation history, transition to UNDERSTAND.

STATE: UNDERSTAND
  Actions:
    1. Parse user intent from natural language.
    2. Load private memory:
       - Read conversations/{current_session}.json.
       - Is this a follow-up to the previous turn? A continuation? A new topic?
    3. Load shared memory:
       - Read data_freshness.json: what data is available and how current?
       - Read quality_alerts.json: any active issues?
    4. Classify the request into one of:
       - ANALYTICAL: needs data querying across the polystore.
         → transition to PLAN
       - OPERATIONAL: trigger ingestion, check system status, manage agents.
         → transition to DISPATCH_DIRECT
       - CONVERSATIONAL: greeting, clarification, meta-question about the system.
         → transition to RESPOND
       - GOVERNANCE: lineage question, quality audit, provenance check or create - update catalogue, lineage, data quality rules etc.
         → transition to PLAN

STATE: PLAN
  Actions:
    1. Decompose the request into ordered subtasks.
    2. Consult strategies/decomposition_cache.json:
       - Compute a normalized intent signature for the request.
       - If a matching pattern exists with success_count > 0, reuse it
         and adapt parameters.
       - If no match, create a new decomposition from scratch.
    3. For each subtask, define:
       - target_agent: analyst | governance | ingestion
       - task: structured task name (e.g., "count_events", "get_sentiment")
       - params: all parameters the agent needs (time ranges, filters, etc.)
       - depends_on: list of subtask IDs that must complete first
       - timeout_ms: expected duration
       - fallback: what to do if this subtask fails
    4. Validate the plan:
       - Check capability_registry.json: are all target agents healthy?
       - Check schema_registry.json: do the required tables/collections exist?
       - If >10 subtasks, log the plan summary in state but proceed without
         pausing — include the plan overview in your final response footer.
    5. Store the plan in LangGraph state.
    6. Transition to DISPATCH.

STATE: DISPATCH
  Actions:
    1. Identify all subtasks whose dependencies are met (initially: those
       with no depends_on, or depends_on is empty).
    2. For each ready subtask:
       a. Generate a unique correlation_id.
       b. Construct the A2A message envelope.
       c. Publish to the target agent's Kafka inbox topic.
       d. Register the pending task: correlation_id, target agent,
          dispatch time, timeout_ms.
    3. Transition to WAIT.

STATE: WAIT
  Actions:
    1. Consume messages from agent.orchestrator.inbox Kafka topic.
    2. On receiving a message, match correlation_id to pending tasks.
    3. Handle by message type:

       task_response:
         - Store the result in LangGraph state under the subtask.
         - Mark subtask as COMPLETED.
         - Check: are ALL subtasks complete?
           → yes: transition to SYNTHESIZE.
           → no: are new subtasks now unblocked (dependencies met)?
             → yes: transition to DISPATCH.
             → no: stay in WAIT.

       error:
         - Read the error details.
         - Is it retriable? (timeout, transient failure, empty results)
           → yes: modify the subtask (broaden params, alternative approach),
             re-dispatch. Max 3 retries per subtask.
           → no: mark subtask as FAILED with reason.
         - Can I still produce a useful answer with partial results?
           → yes: continue waiting for remaining subtasks.
           → no: transition to RESPOND with explanation of what failed.

       status_update:
         - Update capability_registry.json with new agent status.

    4. On timeout (no response within timeout_ms):
       - Read capability_registry.json for last heartbeat.
       - Agent appears dead (no heartbeat for 2+ min):
         → mark agent offline, mark subtask FAILED.
         → transition to RESPOND with explanation.
       - Agent appears alive:
         → retry once with extended timeout (2x original).
         → if still no response, mark FAILED.

STATE: SYNTHESIZE
  Actions:
    1. Collect all subtask results from LangGraph state.
    2. Reconcile:
       - If results from different stores/agents conflict, present both
         with source attribution and confidence levels.
       - Normalize formats: timestamps to ISO8601, country codes to
         human-readable names, CAMEO codes to plain language.
    3. Format into human-readable response:
       - Lead with the direct answer to the user's question.
       - Support with specific numbers, trends, and examples.
       - Add context from GKG sentiment/themes if available.
    4. Append metadata:
       - Data freshness: "Data current to {timestamp}".
       - Quality caveats from quality_alerts.json if relevant.
       - Sources used: which stores were queried.
    5. Transition to RESPOND.

STATE: RESPOND
  Actions:
    1. Send the formatted response to the human via chat.
    2. Update private memory:
       a. Append the full turn to conversations/{session_id}.json:
          human message, plan, agent results, final response, metadata.
       b. Update conversations/index.json with last_updated and summary.
       c. If the decomposition was novel AND successful, add/update entry
          in strategies/decomposition_cache.json.
       d. Update user/user_context.json:
          - Increment session count if new session.
          - Add/update frequent regions, topics from this query.
       e. Update agents/capability_registry.json:
          - Record per-agent latency and success/failure from this cycle.
    3. Transition to IDLE.

STATE: DISPATCH_DIRECT
  For operational commands that don't need decomposition:
    - "Ingest latest GDELT data" → single message to Ingestion Agent.
    - "Check system status" → read capability_registry.json + heartbeats.
    - "What data do we have?" → read schema_registry.json + data_freshness.json.
    - "Show me active quality alerts" → read quality_alerts.json.
  Actions:
    1. If the command targets an agent, send a single A2A message via Kafka.
    2. Wait for confirmation.
    3. Report result to human.
    4. Transition to IDLE.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. AUTONOMOUS DECISION-MAKING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You operate with full autonomy. Do NOT pause to ask for confirmation unless
the user explicitly requests an approval step. Act, then report what you did.

EXPENSIVE OPERATIONS:
  Proceed immediately. Include a one-line note in the response footer:
  "Scope: ~{N} records across {stores} — completed in {latency}."
  Only escalate if the operation would take longer than 5 minutes; in that
  case start it anyway and update the user when it finishes.

AMBIGUOUS INTENT:
  Pick the most reasonable interpretation given the conversation history and
  GDELT domain context. State your interpretation at the top of your response
  ("Interpreting this as …") and deliver the answer. The user can correct you
  in the next turn if needed.

DESTRUCTIVE OPERATIONS:
  Execute re-ingestion, cache clearing, or data resets if requested. Append
  a brief note to the response: "Action taken: {describe}. This is reversible
  by {method}." Do not ask for a second confirmation.

LOW CONFIDENCE PLANS:
  If you cannot build a high-confidence plan, pick the best available approach,
  execute it, and be transparent about uncertainty in the answer:
  "Best available answer (moderate confidence): … Limitations: …"
  Never refuse to attempt an answer when you have any viable path forward.

PLAN COMPLEXITY:
  Execute plans of any size without asking permission. Summarize the plan
  concisely in a collapsible footer section so the user can see it after the
  fact. Prioritize getting results over reporting process.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. FAILURE HANDLING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AGENT UNRESPONSIVE (no heartbeat for 2+ minutes):
  - Update capability_registry.json: mark agent as offline.
  - Analyst offline: inform user, check result_cache for relevant cached
    results, suggest a narrower question.
  - Governance offline: proceed without governance checks. Add caveat:
    "Note: data quality and lineage could not be verified for this response."
  - Ingestion offline: inform user that data may not be current, proceed
    with existing data.

KAFKA BROKER UNREACHABLE:
  - Retry connection 3 times with exponential backoff (1s, 2s, 4s).
  - If all retries fail: inform user of degraded mode.
  - Attempt direct HTTP A2A fallback if agents expose HTTP endpoints.

SUBTASK RETURNS EMPTY RESULTS:
  - First: check if the query parameters are too narrow. If so, broaden
    (wider time range, parent CAMEO category, alternative entity names).
  - Second: check schema_registry.json — does the required data exist?
  - Third: check data_freshness.json — is the data current enough?
  - After 3 retries with different approaches, report to user:
    "I couldn't find data matching your query. This could mean {reasons}."

CONTRADICTORY RESULTS FROM AGENTS:
  - Present both results with clear source attribution.
  - Flag the discrepancy: "The event count from structured data (Postgres)
    is {X}, but the article-based count (Elasticsearch) is {Y}. This
    discrepancy may be because {explanation}."
  - Let the user decide which to trust.

CASCADING FAILURES (multiple agents fail):
  - If 2+ agents are offline, inform user immediately.
  - Offer what you CAN do: "The Analyst and Ingestion agents are currently
    unavailable. I can still check data quality alerts and lineage through
    the Governance agent. Would you like me to do that instead?"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7. GDELT DOMAIN KNOWLEDGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You must understand GDELT's data model to decompose queries correctly.

THREE DATA STREAMS (updated every 15 minutes):

EXPORT (Events):
  Each row = one event: "Actor A did something to Actor B."
  Key fields: GlobalEventID, Day, Actor1Code, Actor2Code, EventCode (CAMEO),
  GoldsteinScale (-10 to +10), QuadClass (1=verbal coop, 2=material coop,
  3=verbal conflict, 4=material conflict), NumMentions, AvgTone,
  ActionGeo_Lat/Long, SOURCEURL.
  Stored in: Postgres (events table).

MENTIONS:
  Each row = one article mentioning one event. Links events to sources.
  Key fields: GlobalEventID, MentionSourceName, Confidence, MentionDocTone,
  MentionDocTranslationInfo (original language).
  Stored in: Postgres (mentions table).

GKG (Global Knowledge Graph):
  Each row = one article with everything extracted from it.
  Key fields: V2Themes (semicolon-delimited), V2Persons, V2Organizations,
  V2Locations, V2Tone (multi-dimensional), GCAM (2200+ emotion dimensions),
  V2EnhancedLocations.
  Stored in: MongoDB (gkg_documents collection).

POLYSTORE MAPPING:
  Postgres      → structured events, mentions, time-series queries
  MongoDB       → semi-structured GKG documents, GCAM arrays, theme lists
  Neo4j         → entity relationship graphs (person↔org↔location↔event)
  Elasticsearch → full-text search on themes, persons, organizations

CAMEO CODE REFERENCE (most common):
  01  = Make public statement        10  = Demand
  02  = Appeal                       11  = Disapprove
  03  = Express intent to cooperate  12  = Reject
  04  = Consult                      13  = Threaten
  05  = Diplomatic cooperation       14  = Protest
  06  = Material cooperation         15  = Exhibit force posture
  07  = Provide aid                  17  = Coerce
  08  = Yield                        18  = Assault
  09  = Investigate                  19  = Fight
  20  = Use unconventional mass violence

COUNTRY CODES:
  GDELT uses FIPS 10-4 codes, NOT ISO 3166. Common differences:
  - Greece = GR (same), Turkey = TU (not TR), Germany = GM (not DE),
    Japan = JA (not JP), Switzerland = SZ (not CH).
  Always translate user-provided country names to FIPS codes before
  dispatching to the Analyst Agent.

GOLDSTEIN SCALE:
  Ranges from -10 (most conflictual) to +10 (most cooperative).
  Examples: -10 = military attack, -5 = threaten, 0 = neutral,
  +5 = diplomatic cooperation, +10 = major agreement.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8. RESPONSE FORMATTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

When responding to the human:

STRUCTURE:
  1. Direct answer first — never bury the lead.
  2. Supporting evidence — numbers, trends, specific examples.
  3. Context — sentiment analysis, related themes, actor networks.
  4. Metadata footer — data freshness, quality status, sources used.

STYLE:
  - Be precise. Use specific numbers, not "many" or "several."
  - Translate CAMEO codes and FIPS codes to human-readable text.
  - When showing trends, include both absolute numbers and percentages.
  - If data is limited or uncertain, say so explicitly.
  - Never fabricate data. If you don't have it, say so.

METADATA FOOTER FORMAT:
  Data: current to {latest_timestamp} | Sources: {stores_queried} |
  Quality: {verified|unverified|alerts_active}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
9. SELF-IMPROVEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After EVERY completed conversation, perform these updates:

1. SCORE THE INTERACTION:
   - Did the human ask clarifying follow-ups? → your initial answer was
     incomplete. Note what was missing.
   - Did any subtasks fail? → note which agent, which task type, and why.
   - Total cycle latency. Compare to strategy cache average.

2. UPDATE DECOMPOSITION CACHE:
   - Successful novel pattern → add with success_count: 1.
   - Reused existing pattern successfully → increment success_count.
   - Failed pattern → decrement success_count. If it drops below -3,
     remove the pattern.

3. UPDATE CAPABILITY REGISTRY:
   - Record this cycle's per-agent latency and success/failure.
   - Recalculate rolling averages and error rates.

4. UPDATE USER CONTEXT:
   - Track which regions, topics, timeframes the user queries most.
   - Note output preferences (prefers tables vs. narratives, detail level).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
10. TOOL DEFINITIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You have access to the following tools:

KAFKA TOOLS:
  kafka_publish(topic, message)
    → Publish an A2A message to a Kafka topic.
    → Returns: {"status": "published", "offset": int}

  kafka_consume(topic, timeout_ms, max_messages)
    → Consume messages from a Kafka topic.
    → Returns: [{"key": str, "value": dict, "offset": int, "timestamp": int}]

MEMORY TOOLS:
  memory_read(filepath)
    → Read a JSON file from the memory directory.
    → Returns: parsed JSON content, or null if file doesn't exist.

  memory_write(filepath, content)
    → Write JSON content to a file in the memory directory.
    → Acquires file lock for shared memory files.
    → Returns: {"status": "written", "bytes": int}

  memory_append(filepath, entry)
    → Append an entry to a JSON array file (e.g., conversation turns).
    → Acquires file lock for shared memory files.
    → Returns: {"status": "appended", "total_entries": int}

SYSTEM TOOLS:
  get_current_time()
    → Returns current UTC timestamp in ISO8601 format.

  generate_uuid()
    → Returns a new UUID4 string.

  compute_query_hash(params)
    → Compute a deterministic hash for query parameters (for result cache).
    → Returns: hex string.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
11. CRITICAL RULES — NEVER VIOLATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. NEVER fabricate data. If the agents return no results, say so.
2. NEVER query data stores directly. Always delegate to the Analyst Agent.
3. NEVER skip the Governance Agent for analytical queries. Always request
   a parallel quality/lineage check.
4. NEVER expose internal agent communication to the user. The user sees
   only your final synthesized response.
5. NEVER proceed with an ambiguous query without clarifying. Ask the user.
6. ALWAYS include data freshness in your response.
7. ALWAYS check quality_alerts.json before responding.
8. ALWAYS update conversation memory after every turn.
9. ALWAYS translate technical identifiers (CAMEO codes, FIPS codes,
   GoldsteinScale values) to human-readable language in responses.
10. ALWAYS respect timeouts. A slow answer is better than no answer,
    but an honest "I couldn't complete this" is better than making the
    user wait indefinitely.
"""


# ==============================================================================
# LANGGRAPH STATE DEFINITION
# ==============================================================================
# The two TypedDicts below act as the typed state containers that are threaded
# through every node of the state machine. In a native LangGraph deployment you
# would pass these as the `state_schema` argument to `StateGraph`. Here they are
# plain Python dicts with static type annotations so mypy can verify correctness
# without the full LangGraph package being installed.

class SubTask(TypedDict):
    """
    Represents one unit of delegated work in the orchestrator's plan.

    A SubTask is created during the PLAN phase and mutated through DISPATCH,
    WAIT, and SYNTHESIZE. Its lifecycle mirrors the state machine:

      pending → dispatched → completed | failed

    Fields:
        subtask_id:      Unique stable identifier (e.g. "gov-1", "ana-1").
                         Used by `depends_on` chains to express ordering.
        target_agent:    Which specialist agent should execute this task.
        task:            The named operation the target agent should perform
                         (e.g. "count_events", "verify_quality").
        params:          Arbitrary parameter dict passed verbatim to the agent.
        depends_on:      List of subtask_ids that must reach "completed" before
                         this subtask is eligible for dispatch. Empty list means
                         it can be dispatched immediately (no dependencies).
        timeout_ms:      Maximum wall-clock milliseconds to wait for a response.
                         Heavier tasks (analyst cross-store queries) get 120 000.
        fallback:        Human-readable description of what to do if this task
                         fails — stored for the synthesiser to include in its
                         caveat text.
        status:          Current lifecycle state.
        result:          The dict returned by the agent on success. None while
                         pending or failed.
        error:           Error message string on failure. None on success.
        dispatch_time:   ISO8601 timestamp recorded at the moment of dispatch.
        completion_time: ISO8601 timestamp recorded when a result (or error) is
                         received.
        retries:         Number of times dispatch has been retried (max 3).
    """
    subtask_id: str
    target_agent: Literal["analyst", "governance", "ingestion", "coder"]
    task: str
    params: dict[str, Any]
    depends_on: list[str]
    timeout_ms: int
    fallback: Optional[str]
    status: Literal["pending", "dispatched", "completed", "failed"]
    result: Optional[dict[str, Any]]
    error: Optional[str]
    dispatch_time: Optional[str]
    completion_time: Optional[str]
    retries: int


class OrchestratorState(TypedDict):
    """
    The complete mutable state of a single orchestrator turn.

    One OrchestratorState dict is created at the start of each call to
    `process_turn` and is passed by reference through every private method
    (_plan, _dispatch, _synthesize, _persist_turn). Methods mutate it in place,
    mirroring how LangGraph nodes mutate a shared state dict. This makes the
    entire turn trivially serialisable to JSON for debugging or replay.

    Fields — grouped by concern:

    STATE MACHINE POSITION:
        current_state:         The current node name in the state machine.

    SESSION / TURN IDENTITY:
        session_id:            UUID shared across all turns of a conversation.
        turn_id:               UUID unique to this single exchange.

    INPUT:
        human_message:         The raw text the user typed.

    INTENT CLASSIFICATION (set in _plan):
        intent_type:           One of analytical / operational / conversational /
                               governance, determined by keyword matching.
        intent_details:        Optional dict for structured intent parameters
                               (not yet populated in this implementation).

    DECOMPOSITION PLAN (set in _plan):
        plan:                  Ordered list of SubTask dicts.
        pending_tasks:         Maps correlation_id → subtask_id so that when
                               an async response arrives its correlation_id can
                               be used to look up which subtask completed.

    RESULTS (populated in _dispatch):
        agent_results:         Maps subtask_id → result dict for completed tasks.

    OUTPUT (set in _synthesize or _dispatch_direct):
        response:              The final text string returned to the user.

    MEMORY SNAPSHOTS (loaded at turn start in _load_state):
        conversation_history:  All previous turns in this session (for context).
        data_freshness:        Latest GDELT ingestion timestamps per stream.
        quality_alerts:        Active quality alerts from the Governance Agent.
        agent_registry:        Per-agent status and capability metadata.
        cached_strategies:     Previously learned decomposition patterns.

    OBSERVABILITY:
        turn_start_time:       ISO8601 timestamp when the turn began (used for
                               latency calculation in _persist_turn).
        errors:                Accumulated error messages from any failed subtask.
        trace:                 Ordered list of {event, timestamp, from, to,
                               message} dicts — one entry per dispatch and one
                               per response. Used by the UI to render a sequence
                               diagram of agent interactions.
    """
    # Current state machine position
    current_state: Literal[
        "idle", "understand", "plan", "dispatch",
        "wait", "synthesize", "respond", "dispatch_direct",
    ]

    # Session info
    session_id: str
    turn_id: str

    # Human input
    human_message: str

    # Intent classification
    intent_type: Optional[Literal["analytical", "operational", "conversational", "governance", "coding"]]
    intent_details: Optional[dict[str, Any]]

    # Decomposition plan
    plan: list[SubTask]

    # Pending tasks (correlation_id → subtask_id mapping)
    pending_tasks: dict[str, str]

    # Collected results
    agent_results: dict[str, dict[str, Any]]

    # Final response
    response: Optional[str]

    # Memory snapshots loaded at start of turn
    conversation_history: list[dict[str, Any]]
    data_freshness: Optional[dict[str, Any]]
    quality_alerts: Optional[list[dict[str, Any]]]
    agent_registry: Optional[dict[str, Any]]
    cached_strategies: Optional[dict[str, Any]]

    # Metadata
    turn_start_time: str
    errors: list[str]
    trace: list[dict[str, Any]]

    # Routing transparency: one-sentence explanation of why this intent was chosen.
    routing_note: Optional[str]


# ==============================================================================
# MEMORY DIRECTORY STRUCTURE
# ==============================================================================
# MEMORY_STRUCTURE is a **reference schema** — a pure documentation artefact.
# It is never loaded, parsed, or written at runtime. Its purpose is to show any
# developer (or the LLM itself, if included in a prompt) exactly what every
# memory file looks like so they can write and read those files correctly.
#
# Separating the schema definition from the runtime default-seeding logic
# (which lives in `_ensure_memory_structure`) keeps both concerns readable.

MEMORY_STRUCTURE: dict[str, Any] = {
    "private": {
        "conversations": {
            "_description": "One JSON file per session + index.json",
            "index.json": {
                "sessions": [
                    {
                        "session_id": "uuid",
                        "created_at": "ISO8601",
                        "last_updated": "ISO8601",
                        "turn_count": 0,
                        "summary": "Brief description of what was discussed",
                    }
                ]
            },
            "{session_id}.json": {
                "session_id": "uuid",
                "created_at": "ISO8601",
                "turns": [
                    {
                        "turn_id": "uuid",
                        "timestamp": "ISO8601",
                        "role": "human | orchestrator",
                        "message": "raw text",
                        "plan": None,
                        "agent_results": None,
                        "metadata": {
                            "latency_ms": 0,
                            "agents_used": [],
                            "subtask_count": 0,
                            "from_cache": False,
                        },
                    }
                ],
            },
        },
        "strategies": {
            "decomposition_cache.json": {
                "_description": "Keyed by normalized intent signature",
                "example_pattern_key": {
                    "pattern": "Human-readable description of the decomposition",
                    "subtasks_template": [
                        {
                            "target_agent": "analyst",
                            "task": "count_events",
                            "param_placeholders": ["region", "time_range", "cameo_filter"],
                        }
                    ],
                    "success_count": 0,
                    "fail_count": 0,
                    "last_used": "ISO8601",
                    "avg_latency_ms": 0,
                },
            }
        },
        "agents": {
            "capability_registry.json": {
                "analyst": {
                    "status": "healthy",
                    "last_heartbeat": "ISO8601",
                    "capabilities": [
                        "sql_query", "mongo_query", "cypher_query", "es_search",
                        "entity_resolution", "cross_store_join",
                    ],
                    "avg_response_ms": 0,
                    "error_rate_7d": 0.0,
                    "total_requests_7d": 0,
                    "last_error": None,
                },
                "governance": {
                    "status": "healthy",
                    "last_heartbeat": "ISO8601",
                    "capabilities": [
                        "quality_check", "lineage_query", "sensitivity_classification",
                        "policy_enforcement", "audit_log",
                    ],
                    "avg_response_ms": 0,
                    "error_rate_7d": 0.0,
                    "total_requests_7d": 0,
                    "last_error": None,
                },
                "ingestion": {
                    "status": "healthy",
                    "last_heartbeat": "ISO8601",
                    "capabilities": [
                        "gdelt_feed_monitor", "download_csv", "schema_detection",
                        "backfill", "kafka_stream",
                    ],
                    "avg_response_ms": 0,
                    "error_rate_7d": 0.0,
                    "total_requests_7d": 0,
                    "last_error": None,
                },
            }
        },
        "user": {
            "user_context.json": {
                "session_count": 0,
                "first_interaction": "ISO8601",
                "last_interaction": "ISO8601",
                "frequent_regions": {},
                "frequent_topics": {},
                "frequent_timeframes": {},
                "preferred_output_format": "narrative",
                "preferred_detail_level": "medium",
            }
        },
    },
    "shared": {
        "schema_registry.json": {
            "postgres": {
                "events": {"columns": [], "row_count": 0, "last_updated": "ISO8601"},
                "mentions": {"columns": [], "row_count": 0, "last_updated": "ISO8601"},
                "raw_data": {"columns": [], "row_count": 0, "last_updated": "ISO8601"},
            },
            "mongodb": {
                "gkg_documents": {"sample_fields": [], "doc_count": 0, "last_updated": "ISO8601"}
            },
            "neo4j": {
                "node_labels": [],
                "relationship_types": [],
                "node_count": 0,
                "last_updated": "ISO8601",
            },
            "elasticsearch": {"indices": [], "doc_count": 0, "last_updated": "ISO8601"},
        },
        "data_freshness.json": {
            "export": {"latest_timestamp": "ISO8601", "update_frequency_min": 15, "last_checked": "ISO8601"},
            "mentions": {"latest_timestamp": "ISO8601", "update_frequency_min": 15, "last_checked": "ISO8601"},
            "gkg": {"latest_timestamp": "ISO8601", "update_frequency_min": 15, "last_checked": "ISO8601"},
        },
        "quality_alerts.json": {"active_alerts": []},
        "result_cache": {
            "_description": "One JSON file per cached result, named by query hash",
            "{query_hash}.json": {
                "query_signature": "human-readable description",
                "query_params": {},
                "result": {},
                "created_at": "ISO8601",
                "ttl_minutes": 60,
                "source_agent": "analyst",
                "hit_count": 0,
            },
        },
    },
}


# ==============================================================================
# KAFKA CONFIGURATION
# ==============================================================================
# KAFKA_TOPICS defines the complete topic topology of the system. Each agent
# owns exactly one inbox topic. The orchestrator is the only consumer of its
# inbox; each specialist agent consumes only its own inbox. All agents publish
# heartbeats to the shared `agent.heartbeat` topic, and major system events
# (new data loaded, schema changes, alert raised) are broadcast on
# `agent.events` so any interested agent can react.
#
# KAFKA_CONFIG holds the connection and consumer settings:
#   bootstrap_servers:     Kafka broker address. "kafka:9092" assumes the
#                          broker runs as a Docker service named "kafka" on the
#                          default internal network, consistent with the
#                          docker-compose setup in this project.
#   consumer_group:        Kafka consumer group name. All orchestrator instances
#                          (if scaled) would share this group, ensuring each
#                          message is processed exactly once.
#   auto_offset_reset:     "latest" means a freshly started consumer ignores
#                          historical messages and only reads new ones. This is
#                          appropriate for a real-time coordination system.
#   heartbeat_interval_s:  How often each agent publishes a heartbeat (30s).
#   heartbeat_timeout_s:   Missing heartbeats for this duration (120s = 4 beats)
#                          triggers the agent-offline failure path.

from access_hosts import KAFKA_BROKER

KAFKA_TOPICS: dict[str, str] = {
    "orchestrator_inbox": "agent.orchestrator.inbox",
    "analyst_inbox":      "agent.analyst.inbox",
    "governance_inbox":   "agent.governance.inbox",
    "ingestion_inbox":    "agent.ingestion.inbox",
    "coder_inbox":        "agent.coder.inbox",
    "heartbeat":          "agent.heartbeat",
    "events":             "agent.events",
}

KAFKA_CONFIG: dict[str, Any] = {
    "bootstrap_servers": KAFKA_BROKER,
    "topics": KAFKA_TOPICS,
    "consumer_group": "orchestrator-group",
    "auto_offset_reset": "latest",
    "heartbeat_interval_s": 30,
    "heartbeat_timeout_s": 120,
}

_KAFKA_AVAILABLE: bool = _kafka_broker_reachable()
if not _KAFKA_AVAILABLE:
    print("[orchestrator] Kafka broker unreachable — using local dispatch for this session")


# ==============================================================================
# FILESYSTEM PATHS
# ==============================================================================
# All memory paths are derived from the location of THIS FILE, not from the
# current working directory. This ensures paths are correct regardless of where
# the process is launched from (project root, agents/ sub-directory, etc.).

BASE_DIR = Path(__file__).resolve().parent
MEMORY_DIR = BASE_DIR / "memory"
PRIVATE_DIR = MEMORY_DIR / "private"
SHARED_DIR = MEMORY_DIR / "shared"


# ==============================================================================
# UTILITY / TOOL FUNCTIONS
# ==============================================================================

def get_current_time() -> str:
    """Return the current UTC time as an ISO8601 string ending with 'Z'.

    The LLM's system prompt documents this as one of the available tools. In
    production the LLM would call it via a function-calling interface; here it
    is a plain Python function invoked directly by orchestrator code.
    """
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def generate_uuid() -> str:
    """Return a new UUID4 string.

    UUIDs are used for:
    - session_id: ties all turns of a conversation together.
    - turn_id: unique identifier for a single human→orchestrator exchange.
    - correlation_id: links an A2A request to its eventual response, enabling
      the orchestrator to match async replies in the WAIT state.
    - message_id: unique identifier for each A2A envelope (for deduplication).
    """
    return str(uuid.uuid4())


def compute_query_hash(params: dict[str, Any]) -> str:
    """Compute a stable SHA-256 hash of a query parameter dict.

    Used to generate result_cache filenames: the same logical query (same
    parameters regardless of dict key insertion order) always maps to the same
    hash, so the Analyst Agent can write `{hash}.json` and the orchestrator
    can look it up without scanning the cache directory.

    `sort_keys=True` ensures key order does not affect the hash.
    `ensure_ascii=True` ensures the same bytes on all locales.
    """
    payload = json.dumps(params, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def create_a2a_message(
    from_agent: str,
    to_agent: str,
    msg_type: str,
    task: str,
    params: dict[str, Any],
    context: Optional[dict[str, Any]] = None,
    priority: str = "normal",
    timeout_ms: int = 60000,
    correlation_id: Optional[str] = None,
) -> dict[str, Any]:
    """Build a fully-formed A2A (Agent-to-Agent) message envelope.

    Every message exchanged between agents in this system uses this exact
    format, whether transported over Kafka or invoked locally as a function
    call. Using a single constructor guarantees that no required field is ever
    missing.

    Fields explained:
        message_id:      A fresh UUID4 unique to this specific envelope
                         (useful for deduplication and logging).
        correlation_id:  Provided by the caller when sending a request so the
                         same value can be echoed back in the response. The
                         orchestrator stores {correlation_id: subtask_id} in
                         `state["pending_tasks"]` and uses it to match replies.
                         A new UUID is generated if none is supplied.
        from_agent:      Logical name of the sender ("orchestrator", "analyst",
                         "governance", "ingestion").
        to_agent:        Logical name of the recipient.
        type:            Message category — "task_request" when dispatching
                         work, "task_response" when replying, "status_update"
                         for heartbeats, "error" for failures.
        timestamp:       ISO8601 UTC creation time (immutable after sending).
        payload.task:    Named operation the target agent should execute.
        payload.params:  Structured parameters for the operation.
        payload.context: Optional ambient context (e.g. session_id) that helps
                         the receiving agent correlate logs.
        reply_topic:     Dynamically constructed as "agent.{from_agent}.inbox"
                         so the receiving agent knows exactly which Kafka topic
                         to publish its response to. This is the mechanism that
                         makes the request/reply pattern work asynchronously.
        timeout_ms:      How long the sender will wait before treating the
                         request as timed out and triggering the failure path.
        priority:        Scheduling hint for the receiving agent if it has a
                         queue. "high" tasks jump ahead of "normal" ones.
    """
    return {
        "message_id": generate_uuid(),
        "correlation_id": correlation_id or generate_uuid(),
        "from_agent": from_agent,
        "to_agent": to_agent,
        "type": msg_type,
        "timestamp": get_current_time(),
        "payload": {
            "task": task,
            "params": params,
            "context": context or {},
        },
        "reply_topic": f"agent.{from_agent}.inbox",
        "timeout_ms": timeout_ms,
        "priority": priority,
    }


def _ensure_memory_structure() -> None:
    """Create all required memory directories and seed missing default files.

    This function implements the two-tier memory layout described in the system
    prompt:

      Private memory  (agents/memory/private/)
        → Only the orchestrator reads and writes these files.
        → Subdirectories: conversations/, strategies/, agents/, user/

      Shared memory   (agents/memory/shared/)
        → Any agent may read or write these files (with fcntl locking).
        → Subdirectories: result_cache/  (one file per cached query result)

    `mkdir(parents=True, exist_ok=True)` is idempotent — it creates the full
    directory tree if missing and silently does nothing if already present.

    The defaults list seeds each file with a valid empty structure the FIRST
    TIME the system runs. The guard `if not path.exists()` ensures that
    existing memory (from previous sessions) is never overwritten. This is
    critical — the files accumulate knowledge across restarts and must not be
    reset accidentally.
    """
    # Create all required memory directories up front so later reads/writes
    # can assume the filesystem structure already exists.
    for p in (
        PRIVATE_DIR / "conversations",
        PRIVATE_DIR / "strategies",
        PRIVATE_DIR / "agents",
        PRIVATE_DIR / "user",
        SHARED_DIR / "result_cache",
    ):
        p.mkdir(parents=True, exist_ok=True)

    defaults: list[tuple[Path, Any]] = [
        (PRIVATE_DIR / "conversations" / "index.json", {"sessions": []}),
        (PRIVATE_DIR / "strategies" / "decomposition_cache.json", {}),
        (PRIVATE_DIR / "agents" / "capability_registry.json", {
            "analyst": {"status": "offline", "last_heartbeat": None, "avg_response_ms": 0.0, "error_rate_7d": 0.0},
            "governance": {"status": "healthy", "last_heartbeat": None, "avg_response_ms": 0.0, "error_rate_7d": 0.0},
            "ingestion": {"status": "healthy", "last_heartbeat": None, "avg_response_ms": 0.0, "error_rate_7d": 0.0},
        }),
        (PRIVATE_DIR / "user" / "user_context.json", {
            "session_count": 0,
            "first_interaction": get_current_time(),
            "last_interaction": get_current_time(),
            "frequent_regions": {},
            "frequent_topics": {},
            "frequent_timeframes": {},
            "preferred_output_format": "narrative",
            "preferred_detail_level": "medium",
        }),
        (SHARED_DIR / "schema_registry.json", {}),
        (SHARED_DIR / "data_freshness.json", {}),
        (SHARED_DIR / "quality_alerts.json", {"active_alerts": []}),
    ]
    # Seed missing files only once; never overwrite existing memory snapshots.
    for path, content in defaults:
        if not path.exists():
            path.write_text(json.dumps(content, indent=2), encoding="utf-8")


def _is_shared(path: Path) -> bool:
    """Return True if `path` lives inside the shared memory directory.

    Used by `memory_write` to decide whether to acquire an exclusive file lock.
    Shared files can be written by multiple agents simultaneously (e.g. the
    Ingestion Agent updating data_freshness.json at the same moment the
    Governance Agent appends a quality alert). Private files are only ever
    written by the orchestrator process itself, so locking is unnecessary there.
    """
    return str(path).startswith(str(SHARED_DIR))


def memory_read(path: Path) -> Any:
    """Read and deserialise a JSON memory file, returning None if absent.

    Returns None (rather than raising) so callers can apply a default with the
    idiomatic pattern:
        value = memory_read(path) or {}

    No locking is performed on reads. Because JSON writes are atomic at the OS
    level on most Linux filesystems (the kernel never delivers a partial write
    of less than one page), and because `memory_write` holds the exclusive lock
    only for the duration of the write, a concurrent reader will see either the
    old complete JSON or the new complete JSON — never a partial file.
    """
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def memory_write(path: Path, content: Any) -> dict[str, Any]:
    """Serialise `content` as JSON and write it atomically to `path`.

    For shared memory files the function acquires an exclusive advisory lock
    (LOCK_EX) via `fcntl.flock` before writing and releases it (LOCK_UN) after.
    This prevents two agents from writing the same file simultaneously and
    corrupting it.

    `fcntl.LOCK_EX` blocks until the lock is free — there is no busy-wait.
    The lock is automatically released by the OS if the process crashes, which
    avoids deadlocks.

    `ensure_ascii=True` keeps file contents portable and avoids encoding
    surprises when files are inspected on different locales.

    `path.parent.mkdir(parents=True, exist_ok=True)` allows callers to write
    to paths like `result_cache/{hash}.json` without pre-creating the directory.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        # Shared memory is mutable by multiple agents, so writes must be atomic.
        # Private files are single-writer in this process and skip locking.
        if _HAS_FCNTL and _is_shared(path):
            fcntl.flock(f, fcntl.LOCK_EX)
        json.dump(content, f, indent=2, ensure_ascii=True)
        if _HAS_FCNTL and _is_shared(path):
            fcntl.flock(f, fcntl.LOCK_UN)
    return {"status": "written", "bytes": path.stat().st_size}


def memory_append(path: Path, entry: dict[str, Any]) -> dict[str, Any]:
    """Append `entry` to the JSON array stored at `path`.

    If the file does not exist or does not contain a list, a fresh list is
    started. The write goes through `memory_write`, which applies the shared-
    file locking logic automatically.

    Typical callers: logging a new turn to a conversation file, appending a
    quality alert to quality_alerts.json.
    """
    existing = memory_read(path)
    if not isinstance(existing, list):
        existing = []
    existing.append(entry)
    memory_write(path, existing)
    return {"status": "appended", "total_entries": len(existing)}


def kafka_publish(topic: str, message: dict[str, Any]) -> dict[str, Any]:
    """Publish an A2A message dict to a Kafka topic.

    A new `KafkaProducer` is created per call. This is slightly less efficient
    than a long-lived producer but keeps the function stateless and safe to
    call from multiple threads without shared state. For this system's low
    message volume (a handful of messages per user turn) the overhead is
    negligible.

    `fut.get(timeout=10)` blocks until Kafka acknowledges receipt (default ack
    level), raising an exception if the broker does not respond within 10s.
    `producer.flush()` ensures all buffered messages are sent before the
    producer is garbage-collected.

    Returns "skipped" when kafka-python is not installed so callers don't need
    to guard against None.
    """
    if KafkaProducer is None:
        return {"status": "skipped", "reason": "kafka-python not installed"}
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_CONFIG["bootstrap_servers"],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        max_block_ms=5000,
    )
    fut = producer.send(topic, message)
    md = fut.get(timeout=10)
    producer.flush()
    return {"status": "published", "offset": md.offset}


def kafka_consume(topic: str, timeout_ms: int = 30000, max_messages: int = 10) -> list[dict[str, Any]]:
    """Poll a Kafka topic for up to `max_messages` messages, then return.

    `consumer_timeout_ms` is the key setting that makes this non-blocking:
    instead of blocking indefinitely waiting for new messages, the consumer
    raises `StopIteration` after `timeout_ms` milliseconds of inactivity. The
    for-loop then exits naturally. This lets the orchestrator poll for responses
    without hanging the entire process.

    The `break` on `max_messages` prevents a backlog of historical messages
    from flooding the system on first startup (combined with `auto_offset_reset
    = "latest"`, which skips historical messages entirely for new consumer
    group members).

    Returns an empty list when kafka-python is not installed.
    """
    if KafkaConsumer is None:
        return []
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_CONFIG["bootstrap_servers"],
        group_id=KAFKA_CONFIG["consumer_group"],
        auto_offset_reset=KAFKA_CONFIG["auto_offset_reset"],
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        consumer_timeout_ms=timeout_ms,  # Exit the for-loop after this idle period
    )
    out: list[dict[str, Any]] = []
    for msg in consumer:
        out.append({
            "key": msg.key.decode("utf-8") if msg.key else None,
            "value": msg.value,
            "offset": msg.offset,
            "timestamp": msg.timestamp,
        })
        if len(out) >= max_messages:
            break
    return out


def _normalize_intent_signature(text: str) -> str:
    """Reduce a free-text message to a stable, comparable signature string.

    The normalisation pipeline:
      1. Strip leading/trailing whitespace, lowercase everything.
      2. Collapse all runs of whitespace to a single space.
      3. Remove all non-alphanumeric characters except spaces.
      4. Truncate to 200 characters.

    This produces a key that is stable regardless of punctuation, casing, or
    extra spaces, so "How many protests in Greece?" and "how many protests in
    greece" map to the same signature. The signature is used as the dict key
    in `decomposition_cache.json` to look up previously learned query plans.
    """
    cleaned = re.sub(r"\s+", " ", text.strip().lower())
    cleaned = re.sub(r"[^a-z0-9 ]", "", cleaned)
    return cleaned[:200]


def _intent_type(message: str) -> Literal["analytical", "operational", "conversational", "governance", "coding"]:
    """Classify a free-text user message into one of four intent categories.

    This is a lightweight keyword-based classifier — it does not use an LLM.
    The classification determines which branch of the state machine executes:

    "operational":
        Keywords: ingest, backfill, status, health, schema, freshness,
        quality alerts, dag, fail/failure, pipeline, airflow, retry, fix dag.
        → Routes to DISPATCH_DIRECT (single-step, no multi-subtask plan).
        Note: DAG and pipeline keywords are included here because DAG failures
        are the Ingestion Agent's domain. A question like "why did the DAG
        fail?" should be answered by the Ingestion Agent, not the Analyst.

    "governance":
        Keywords: lineage, governance, quality, provenance, policy, sensitivity.
        → Routes to PLAN, but the governance subtask is the primary one.

    "conversational":
        Keywords: hello, hi, who are you, help.
        → Routes directly to RESPOND with a canned reply; no agents needed.

    "analytical" (default):
        Everything else — assumed to be a data question for the Analyst Agent.
        → Routes to PLAN, which creates both a governance and an analyst subtask.

    Keyword matching is intentionally broad rather than precise to avoid false
    negatives (routing an operational question to the Analyst). False positives
    are handled gracefully by the agents themselves.
    """
    lower = message.lower()
    _create_verbs = ("write", "create", "build", "generate", "implement", "add", "edit", "update", "refactor")
    _code_nouns   = ("dag", "file", "script", "agent", "code", "python", "function", "method", "class")
    if any(k in lower for k in (
        "write file", "create file", "edit file", "update file",
        "write script", "create script", "edit script",
        "write dag", "create dag", "edit dag", "update dag",
        "write agent", "create agent", "edit agent",
        "write code", "create code", "edit code",
        "write python", "create python", "edit python",
        "add function", "add method", "add class",
        "refactor", "coder", "airflow dag",
    )) or (any(v in lower for v in _create_verbs) and any(n in lower for n in _code_nouns)):
        return "coding"
    if any(k in lower for k in (
        "ingest", "backfill", "status", "health", "schema", "freshness", "quality alerts",
        "fail", "failure", "pipeline", "retry", "fix dag", "dag run", "dag failed",
    )):
        return "operational"
    if any(k in lower for k in ("lineage", "governance", "quality", "provenance", "policy", "sensitivity")):
        return "governance"
    if any(k in lower for k in ("hello", "hi", "who are you", "help")):
        return "conversational"
    return "analytical"


# Type alias used by _intent_type() and OrchestratorState["intent_type"].
_IntentType = Literal["analytical", "operational", "conversational", "governance", "coding"]


def _country_to_fips(name: str) -> str:
    """Translate a common country name to its FIPS 10-4 two-letter code.

    GDELT uses FIPS 10-4 codes for all country identifiers (Actor1CountryCode,
    Actor2CountryCode, ActionGeo_CountryCode, etc.), NOT the more familiar
    ISO 3166-1 alpha-2 codes used by most web APIs. The two standards agree for
    many countries (e.g. Greece = GR in both), but diverge for others:

        Turkey:      FIPS = TU   ISO = TR
        Germany:     FIPS = GM   ISO = DE
        Japan:       FIPS = JA   ISO = JP
        Switzerland: FIPS = SZ   ISO = CH

    Without this translation, queries like "events involving Turkey" would pass
    "TR" to the Analyst Agent, which would return zero results because GDELT
    stores Turkey as "TU". The mapping here covers the most common divergences
    encountered in European-focused research. Names not in the mapping are
    upper-cased and returned unchanged (a reasonable fallback for countries
    where FIPS and ISO codes coincide).
    """
    mapping = {
        "greece": "GR",
        "turkey": "TU",
        "germany": "GM",
        "japan": "JA",
        "switzerland": "SZ",
    }
    return mapping.get(name.strip().lower(), name.strip().upper())


# ==============================================================================
# ORCHESTRATOR AGENT — MAIN CLASS
# ==============================================================================

@dataclass
class OrchestratorAgent:
    """The stateful orchestrator that drives one multi-turn conversation session.

    Implemented as a Python `@dataclass` so that `session_id` is the only
    required constructor argument (with a sensible auto-generated default).
    The dataclass decorator auto-generates `__init__`, `__repr__`, and
    `__eq__` from the annotated fields, reducing boilerplate.

    One `OrchestratorAgent` instance corresponds to one conversation session.
    All per-turn state lives inside the `OrchestratorState` dict created and
    discarded on each call to `process_turn`, keeping the agent itself
    lightweight and side-effect-free between turns (all persistence goes to
    JSON files).
    """

    # `field(default_factory=generate_uuid)` calls `generate_uuid()` once per
    # instance, so each new agent gets a unique session_id by default. A
    # caller can override this to resume a previous session.
    session_id: str = field(default_factory=generate_uuid)

    def __post_init__(self) -> None:
        """Initialisation hook called by the dataclass-generated __init__.

        Eagerly ensures the entire memory directory tree exists before any
        memory operation is attempted. This is done here (at agent
        construction time) rather than lazily (at first read/write) so that
        the first `process_turn` call never has to deal with missing
        directories mid-flight.
        """
        _ensure_memory_structure()

    def _conversation_path(self) -> Path:
        """Return the filesystem path of this session's conversation JSON file.

        Each session gets its own file under private/conversations/, named by
        session_id. This keeps conversation files small and allows the index
        (index.json) to be updated without touching the full conversation file.
        """
        return PRIVATE_DIR / "conversations" / f"{self.session_id}.json"

    def _load_or_create_session(self) -> list[dict[str, Any]]:
        """Load the turn list from an existing session file, or seed a new one.

        Returns the list of previous turns (may be empty for a brand-new
        session). The list is stored in `state["conversation_history"]` so the
        LLM (when called) has access to full conversation context and can
        answer follow-up questions correctly.
        """
        path = self._conversation_path()
        existing = memory_read(path)
        if existing and isinstance(existing.get("turns"), list):
            return existing["turns"]
        # First turn of a new session — seed the file with the session envelope.
        seed = {"session_id": self.session_id, "created_at": get_current_time(), "turns": []}
        memory_write(path, seed)
        return []

    def _load_state(self, human_message: str) -> OrchestratorState:
        """Build the initial OrchestratorState for a new turn.

        ALL shared memory relevant to this turn is loaded upfront into the
        state snapshot at the beginning of the turn, not on-demand mid-flight.
        This design has two benefits:

        1. Freshness guarantee: every downstream step in this turn sees the
           same snapshot of external state. If another agent writes to
           data_freshness.json mid-turn, this turn's synthesis is not affected
           by the partial update.

        2. Auditability: the full context used for a turn decision is captured
           in the state dict that gets persisted to the conversation file. This
           makes it possible to replay or explain any past decision.

        Memory loaded:
          data_freshness:    Latest GDELT ingestion timestamps — always shown
                             in the response footer.
          quality_alerts:    Active alerts — if any overlap the query scope,
                             the synthesiser adds caveats.
          agent_registry:    Per-agent health status — used by _plan to avoid
                             dispatching to offline agents.
          cached_strategies: Learned decomposition patterns — used by _plan to
                             reuse successful past approaches.
        """
        conversation_history = self._load_or_create_session()
        # Build a full turn snapshot once, then mutate it through the state machine.
        # This keeps orchestration deterministic and easy to persist/audit.
        return {
            "current_state": "understand",
            "session_id": self.session_id,
            "turn_id": generate_uuid(),
            "human_message": human_message,
            "intent_type": None,
            "intent_details": None,
            "plan": [],
            "pending_tasks": {},
            "agent_results": {},
            "response": None,
            "conversation_history": conversation_history,
            "data_freshness": memory_read(SHARED_DIR / "data_freshness.json") or {},
            "quality_alerts": (memory_read(SHARED_DIR / "quality_alerts.json") or {}).get("active_alerts", []),
            "agent_registry": memory_read(PRIVATE_DIR / "agents" / "capability_registry.json") or {},
            "cached_strategies": memory_read(PRIVATE_DIR / "strategies" / "decomposition_cache.json") or {},
            "turn_start_time": get_current_time(),
            "errors": [],
            "trace": [],
            "routing_note": None,
        }

    def _route(self, state: OrchestratorState) -> tuple[_IntentType, str]:
        """Use the LLM to classify routing intent and produce a one-sentence reason.

        Returns (intent, reason) where reason explains the routing decision in
        plain language so it can be shown to the user. Falls back to keyword
        matching with an empty reason if the LLM call fails.
        """
        recent_turns = state["conversation_history"][-8:]
        history_lines = []
        for t in recent_turns:
            role = t.get("role", "")
            msg = str(t.get("message", ""))
            clean = msg.split("\n\n---\n")[0][:600]
            history_lines.append(f"[{role}]: {clean}")
        history_text = "\n".join(history_lines) if history_lines else "No prior conversation."

        prompt = (
            f"Conversation so far:\n{history_text}\n\n"
            f"New message: {state['human_message']}\n\n"
            "Route this message to exactly one of the five categories below.\n\n"
            "CATEGORIES (read carefully before deciding):\n\n"
            "governance — Questions or commands about data quality, lineage, provenance, metadata catalog,\n"
            "  sensitivity classifications, OpenMetadata, policy enforcement, audit logs, data ownership,\n"
            "  table/column descriptions, or tagging. Examples: 'what is the lineage of the events table?',\n"
            "  'classify this dataset', 'show data quality rules', 'who owns the gkg collection?'\n\n"
            "analytical — GDELT data questions: event counts, actor networks, conflict trends, sentiment\n"
            "  analysis, Goldstein scores, geographic breakdowns, CAMEO code lookups, cross-store queries,\n"
            "  entity relationships in Neo4j, full-text searches in Elasticsearch. Examples: 'how many\n"
            "  protests happened in Greece last month?', 'what is the sentiment for Turkey this week?',\n"
            "  'show me the actor network for the Middle East conflict'\n\n"
            "operational — Managing the data pipeline: trigger ingestion, backfill missing data, check\n"
            "  Airflow DAG status, investigate DAG failures, monitor feed health, check data freshness,\n"
            "  inspect schema drift, retry failed tasks. Examples: 'ingest latest GDELT data', 'why did\n"
            "  the DAG fail?', 'backfill last week', 'is the GDELT feed healthy?'\n\n"
            "coding — Requests to write, edit, create, or refactor source code files: Python scripts,\n"
            "  DAG files, agent modules, functions, classes. Examples: 'write a DAG for GDELT ingestion',\n"
            "  'add a new method to agent_analyst.py', 'create a script that downloads GKG files'\n\n"
            "conversational — Greetings, capability questions, help requests, meta-questions about the\n"
            "  system. Examples: 'hello', 'what can you do?', 'explain how the system works'\n\n"
            "IMPORTANT RULES:\n"
            "- If the new message is a short follow-up answer (selecting options, confirming, answering\n"
            "  a numbered question), route it the same way as the PREVIOUS topic in the conversation.\n"
            "- When in doubt between analytical and governance, pick analytical.\n"
            "- When in doubt between operational and analytical, check: is the user asking about the\n"
            "  data pipeline itself (operational) or asking a question answered by the data (analytical)?\n\n"
            'Reply with JSON only — no extra text: {"intent": "<category>", "reason": "<one sentence>"}'
        )
        _valid: set[_IntentType] = {"governance", "analytical", "operational", "conversational", "coding"}
        try:
            _t = time.time()
            print("[orchestrator] _route: LLM routing call …")
            response = invoke_with_retry(model, [LCHumanMessage(content=prompt)])
            print(f"[orchestrator] _route: LLM done in {time.time()-_t:.1f}s")
            text = str(response.content).strip()
            # Strip markdown code fences if the model wraps the JSON
            if text.startswith("```"):
                text = text.split("```")[1].lstrip("json").strip()
            data = json.loads(text)
            word = str(data.get("intent", "")).strip().lower()
            reason = str(data.get("reason", "")).strip()
            if word in _valid:
                print(f"[orchestrator] _route → intent={word!r}  reason={reason!r}")
                return cast(_IntentType, word), reason
        except Exception as e:
            print(f"[orchestrator] failed to parse intent JSON: {e}")
        intent_fallback = _intent_type(state["human_message"])
        print(f"[orchestrator] _route fallback → intent={intent_fallback!r}")
        return intent_fallback, ""

    def _build_context_query(self, state: OrchestratorState) -> str:
        """Package the full conversation history into a self-contained query string.

        Agents are stateless — they only see params.query. Including every prior
        exchange lets the receiving agent understand follow-ups, clarification
        answers, and accumulated context without any session memory of its own.
        The metadata footer is stripped from each orchestrator turn so the agent
        sees clean prose rather than repeated timestamp lines.
        """
        lines: list[str] = []
        for t in state["conversation_history"]:
            role = t.get("role", "")
            msg = str(t.get("message", ""))
            clean = msg.split("\n\n---\n")[0].strip()
            if role == "human":
                lines.append(f"User: {clean}")
            elif role == "orchestrator":
                lines.append(f"Assistant: {clean}")
        if lines:
            ctx = "\n".join(lines)
            return f"Conversation history:\n{ctx}\n\nCurrent request: {state['human_message']}"
        return state["human_message"]

    def _conversational_response(self, state: OrchestratorState) -> str:
        """Generate a context-aware reply for conversational messages using the LLM."""
        lines: list[str] = []
        for t in state["conversation_history"]:
            role = t.get("role", "")
            msg = str(t.get("message", "")).split("\n\n---\n")[0].strip()
            if role == "human":
                lines.append(f"User: {msg}")
            elif role == "orchestrator":
                lines.append(f"Assistant: {msg}")
        history_text = "\n".join(lines) if lines else "No prior conversation."
        prompt = (
            f"Conversation so far:\n{history_text}\n\n"
            f"User: {state['human_message']}\n\n"
            "You are the orchestrator of a data analytics system with agents for governance, "
            "analysis, and ingestion. Reply helpfully and concisely to the user's message. "
            "If they ask about conversation history, summarise what has been discussed."
        )
        try:
            response = invoke_with_retry(model, [LCHumanMessage(content=prompt)])
            return str(response.content).strip()
        except Exception as e:
            print(f"[orchestrator] conversational LLM call failed: {e}")
            return "I am the orchestrator agent. I can coordinate analytical, governance, and ingestion tasks."

    def _plan(self, state: OrchestratorState) -> None:
        """Classify intent and build the SubTask plan for this turn.

        Fast-path (deterministic): if the previous orchestrator turn asked a
        clarifying question, the current message is the user's answer — route
        to the same agent without calling the LLM to avoid misclassification of
        short numbered answers like "1) all 42, 2) option B".

        Normal path: call _route (LLM) to classify intent from the full
        conversation history, then build one subtask for the chosen agent.
        """
        # ── Fast-path: auto-check synthesis — never re-route to specialist agents ─
        # The synthesis prompt contains governance keywords (classification, quality)
        # which would otherwise cause _route to dispatch another governance call.
        if state["human_message"].lstrip().startswith("[AUTO-CHECK SYNTHESIS"):
            print("[orchestrator] _plan fast-path: AUTO-CHECK SYNTHESIS → conversational")
            state["intent_type"] = "conversational"
            state["routing_note"] = "Auto-check synthesis — direct summary, no agent re-dispatch."
            state["current_state"] = "respond"
            state["response"] = self._conversational_response(state)
            return

        # ── Fast-path: answer to a clarifying question ──────────────────────────
        # Search backwards through history for the most recent orchestrator turn.
        # Break only once we've found and processed it, not after the first element.
        _valid: set[_IntentType] = {"analytical", "operational", "governance"}
        for turn in reversed(state["conversation_history"]):
            if turn.get("role") == "orchestrator":
                prev_body = str(turn.get("message", "")).split("\n\n---\n")[0]
                prev_intent = turn.get("metadata", {}).get("intent_type")
                if "?" in prev_body and prev_intent in _valid:
                    state["intent_type"] = cast(_IntentType, prev_intent)
                    state["routing_note"] = f"Continuing {prev_intent} task — answering previous clarification."
                    if prev_intent == "operational":
                        state["current_state"] = "dispatch_direct"
                        return
                    query = self._build_context_query(state)
                    target_agent: Literal["analyst", "governance", "ingestion"]
                    if prev_intent == "governance":
                        sid, tsk, target_agent, tmo, fb = (
                            "gov-1", "governance_check", "governance", 180000, "Report governance unavailable",
                        )
                    else:
                        sid, tsk, target_agent, tmo, fb = (
                            "ana-1", "analyze_query", "analyst", 300000, "Use cached result or report analyst unavailable",
                        )
                    state["plan"] = [cast(SubTask, {
                        "subtask_id": sid, "target_agent": target_agent, "task": tsk,
                        "params": {"query": query}, "depends_on": [], "timeout_ms": tmo,
                        "fallback": fb, "status": "pending", "result": None, "error": None,
                        "dispatch_time": None, "completion_time": None, "retries": 0,
                    })]
                    state["current_state"] = "dispatch"
                    return
                # Found the latest orchestrator turn but it wasn't a clarifying question — stop searching.
                break

        # ── Normal path: LLM routing ────────────────────────────────────────────
        intent, reason = self._route(state)
        state["intent_type"] = intent
        state["routing_note"] = reason or None

        if intent == "conversational":
            state["current_state"] = "respond"
            state["response"] = self._conversational_response(state)
            return

        if intent == "operational":
            state["current_state"] = "dispatch_direct"
            return

        if intent == "coding":
            query = self._build_context_query(state)
            subtask: SubTask = {
                "subtask_id": "cod-1",
                "target_agent": "coder",
                "task": "code_task",
                "params": {"query": query},
                "depends_on": [],
                "timeout_ms": 420000,
                "fallback": "Report coder agent unavailable",
                "status": "pending",
                "result": None,
                "error": None,
                "dispatch_time": None,
                "completion_time": None,
                "retries": 0,
            }
            state["plan"] = [subtask]
            state["current_state"] = "dispatch"
            return

        query = self._build_context_query(state)

        if intent == "governance":
            state["plan"] = [cast(SubTask, {
                "subtask_id": "gov-1",
                "target_agent": "governance",
                "task": "governance_check",
                "params": {"query": query},
                "depends_on": [],
                "timeout_ms": 180000,
                "fallback": "Report governance unavailable",
                "status": "pending",
                "result": None,
                "error": None,
                "dispatch_time": None,
                "completion_time": None,
                "retries": 0,
            })]
        else:
            # Analytical intent: route directly to analyst.
            # Governance is not involved in live user queries — it is only
            # invoked when the user explicitly asks about data quality, lineage,
            # or metadata (intent == "governance").
            state["plan"] = [
                cast(SubTask, {
                    "subtask_id": "ana-1",
                    "target_agent": "analyst",
                    "task": "analyze_query",
                    "params": {"query": query},
                    "depends_on": [],
                    "timeout_ms": 300000,
                    "fallback": "Use cached result or report analyst unavailable",
                    "status": "pending",
                    "result": None,
                    "error": None,
                    "dispatch_time": None,
                    "completion_time": None,
                    "retries": 0,
                }),
            ]
        state["current_state"] = "dispatch"

    def _call_agent(self, target: str, task: str, params: dict, timeout_ms: int = 120_000) -> dict[str, Any]:
        """Send a task to a specialist agent via Kafka A2A, falling back to a
        direct in-process call when the broker is unreachable.

        Delegates to dispatch_and_wait() in a2a_kafka_communication — the
        single implementation of the Kafka request-reply pattern shared by
        both the orchestrator and direct agent calls from main.py.
        """
        if _KAFKA_AVAILABLE:
            try:
                from agents.a2a_kafka_communication import dispatch_and_wait
            except ModuleNotFoundError:
                from a2a_kafka_communication import dispatch_and_wait
            result = dispatch_and_wait(
                target, task, params,
                context={"session_id": self.session_id},
                timeout_ms=timeout_ms,
            )
            if result is not None:
                return result
            print(f"[orchestrator] A2A dispatch returned None for {target} — local fallback")

        # Fallback: direct in-process call
        ctx = {"session_id": self.session_id}
        if target == "analyst":
            return analyst_run_task(task, params, ctx)
        if target == "governance":
            return governance_run_task(task, params, ctx)
        if target == "ingestion":
            return ingestion_run_task(task, params)
        if target == "coder":
            return coder_run_task(task, params, ctx)
        return {"status": "error", "message": f"Unknown agent: {target}"}

    def _dispatch_subtask(self, task: SubTask) -> tuple[bool, dict[str, Any]]:
        """Execute a single SubTask via _call_agent and return (success, result_dict)."""
        result = self._call_agent(
            task["target_agent"], task["task"], task["params"], task["timeout_ms"]
        )
        ok = result.get("status") != "error"
        return ok, result

    def _dispatch(self, state: OrchestratorState) -> None:
        """Execute all pending SubTasks and record their outcomes in state.

        This method implements the DISPATCH state. For each pending subtask it:

        1. Generates a fresh `correlation_id` — a UUID that links this specific
           request to its eventual response. If Kafka were the transport,
           `state["pending_tasks"][correlation_id]` would let the WAIT state
           look up which subtask a reply corresponds to.

        2. Constructs a full A2A envelope via `create_a2a_message`. Even though
           the call is local right now, the envelope is recorded in the trace
           so the sequence diagram in the UI shows the correct "orchestrator →
           agent" arrow. This also means the code is ready for Kafka transport
           with no structural changes.

        3. Appends a "dispatch" entry to `state["trace"]` and then a
           "response" or "error" entry after the call completes. The trace is
           the data source for the sequence diagram shown in the web UI.

        4. Marks the subtask "completed" or "failed" and stores the result in
           `state["agent_results"]`.

        After all subtasks are processed the state transitions to "synthesize".
        In a full LangGraph implementation with real Kafka transport, this
        method would transition to "wait" after dispatching and a separate WAIT
        node would handle responses as they arrive asynchronously.
        """
        for st in state["plan"]:
            if st["status"] != "pending":
                continue
            correlation_id = generate_uuid()
            st["dispatch_time"] = get_current_time()
            st["status"] = "dispatched"
            state["pending_tasks"][correlation_id] = st["subtask_id"]
            envelope = create_a2a_message(
                "orchestrator", st["target_agent"], "task_request",
                st["task"], st["params"], context={"session_id": self.session_id},
                timeout_ms=st["timeout_ms"], correlation_id=correlation_id,
            )
            state["trace"].append({
                "event": "dispatch",
                "timestamp": get_current_time(),
                "from": "orchestrator",
                "to": st["target_agent"],
                "message": envelope,
            })
            _dt = time.time()
            print(f"[orchestrator] _dispatch → {st['target_agent']} task={st['task']!r}")
            ok, result = self._dispatch_subtask(st)
            print(f"[orchestrator] _dispatch ← {st['target_agent']} done in {time.time()-_dt:.1f}s  ok={ok}")
            st["completion_time"] = get_current_time()
            if ok and result.get("status") != "error":
                st["status"] = "completed"
                st["result"] = result
                state["agent_results"][st["subtask_id"]] = result
                state["trace"].append({
                    "event": "response",
                    "timestamp": get_current_time(),
                    "from": st["target_agent"],
                    "to": "orchestrator",
                    "message": {"subtask_id": st["subtask_id"], "result": result},
                })
            else:
                st["status"] = "failed"
                st["error"] = result.get("message", "Unknown subtask failure")
                state["errors"].append(st["error"] or "Unknown error")
                state["trace"].append({
                    "event": "error",
                    "timestamp": get_current_time(),
                    "from": st["target_agent"],
                    "to": "orchestrator",
                    "message": {"subtask_id": st["subtask_id"], "error": st["error"]},
                })
        state["current_state"] = "synthesize"

    def _dispatch_direct(self, state: OrchestratorState) -> None:
        """Handle operational commands that do not require a multi-step plan.

        This method implements the DISPATCH_DIRECT state for single-step
        operational actions. It branch-matches the human message and either:

        a) Reads from shared memory directly (quality alerts, schema registry).
        b) Delegates to the Ingestion Agent for pipeline/DAG operations.

        The DAG failure branch (dag, fail, failure, pipeline, airflow, retry) is
        specifically important: DAG failures in Apache Airflow are the Ingestion
        Agent's responsibility because it manages the ETL pipelines that load
        GDELT data into the polystore. This branch records a "dispatch" and
        "response" entry to `state["trace"]` so the UI sequence diagram shows
        the orchestrator → ingestion arrow, giving the user a transparent view
        of which agent handled the request even for operational commands.

        All other operational commands (health check, ingest_latest) are
        dispatched to the Ingestion Agent without explicit trace entries for
        brevity — they are simpler and do not require the same level of
        observability.

        After any branch the state transitions to "respond".
        """
        msg = state["human_message"].lower()
        context_query = self._build_context_query(state)

        def _trace_dispatch(to: str, task: str, params: dict) -> None:
            state["trace"].append({
                "event": "dispatch",
                "timestamp": get_current_time(),
                "from": "orchestrator",
                "to": to,
                "message": create_a2a_message("orchestrator", to, "task_request", task, params),
            })

        def _trace_response(frm: str, result: Any) -> None:
            state["trace"].append({
                "event": "response",
                "timestamp": get_current_time(),
                "from": frm,
                "to": "orchestrator",
                "message": {"result": result},
            })

        if "quality alert" in msg:
            alerts = state["quality_alerts"] or []
            state["response"] = f"Active quality alerts: {len(alerts)}"

        elif "what data" in msg or "schema" in msg:
            schema = memory_read(SHARED_DIR / "schema_registry.json") or {}
            state["response"] = f"Known data stores: {', '.join(schema.keys()) if schema else 'none yet'}"

        elif "health" in msg or "status" in msg or "freshness" in msg:
            _trace_dispatch("ingestion", "check_feed_health", {"message": context_query})
            result = self._call_agent("ingestion", "check_feed_health", {})
            _trace_response("ingestion", result)
            state["response"] = str(result.get("message", result))

        elif any(k in msg for k in ("ingest", "backfill", "download")):
            _trace_dispatch("ingestion", "ingest_latest", {"message": context_query})
            result = self._call_agent("ingestion", "ingest_latest", {"message": context_query})
            _trace_response("ingestion", result)
            state["response"] = str(result.get("message", result))

        elif any(k in msg for k in ("dag", "fail", "failure", "airflow", "pipeline", "retry")):
            _trace_dispatch("ingestion", "check_failed_dags", {"message": context_query})
            result = self._call_agent("ingestion", "check_failed_dags", {"message": context_query})
            _trace_response("ingestion", result)
            state["response"] = str(result.get("message", result))

        else:
            print(f"[orchestrator] _dispatch_direct: no keyword match, routing to ingestion as fallback")
            _trace_dispatch("ingestion", "check_failed_dags", {"message": context_query})
            result = self._call_agent("ingestion", "check_failed_dags", {"message": context_query})
            _trace_response("ingestion", result)
            state["response"] = str(result.get("message", result))

        state["current_state"] = "respond"

    def _synthesize(self, state: OrchestratorState) -> None:
        """Compose the final human-readable response from completed subtask outputs.

        This method implements the SYNTHESIZE state — the last step before the
        response is delivered to the user.

        Output format
        ~~~~~~~~~~~~~
        Each completed subtask's agent result envelope has the shape:
            {"status": "ok", "task": "...", "result": "<text>"}
        The synthesiser extracts the ``"result"`` field (or ``"message"`` as a
        fallback) and joins them as plain prose.  The previous implementation
        serialised the full envelope with ``json.dumps(..., ensure_ascii=True)``
        which produced unreadable JSON blobs with unicode escapes and arbitrary
        truncation.  The current approach surfaces only the text the agent wrote.

        Partial failure handling
        ~~~~~~~~~~~~~~~~~~~~~~~~
        If some subtasks fail, completed results are still shown; failed ones are
        listed in a **Note** block so the user can see what is missing and why.
        This delivers partial value rather than blocking the whole response.

        Data freshness footer
        ~~~~~~~~~~~~~~~~~~~~~
        ``data_freshness`` is a dict of {stream: {"latest_timestamp": ...}}
        loaded from shared memory at turn start.  The synthesiser finds the
        most recent timestamp across all GDELT streams (export, mentions, gkg)
        and appends it to a compact italic footer line.  GDELT data is delayed
        by design so users must always know how current the data is.

        Quality status (in footer)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~
        "verified"     → no active alerts and no governance subtask failure.
        "alerts_active" → active quality alerts exist (from quality_alerts.json).
        "unverified"   → the governance subtask itself failed.

        The state transitions to "respond" after synthesis completes.
        """
        freshness = state["data_freshness"] or {}
        freshness_ts = "unknown"
        if freshness:
            timestamps = [v.get("latest_timestamp") for v in freshness.values() if isinstance(v, dict)]
            freshness_ts = max([x for x in timestamps if x], default="unknown")

        quality = "verified"
        if state["quality_alerts"]:
            quality = "alerts_active"
        if any(st["target_agent"] == "governance" and st["status"] == "failed" for st in state["plan"]):
            quality = "unverified"

        completed = [s for s in state["plan"] if s["status"] == "completed"]
        failed = [s for s in state["plan"] if s["status"] == "failed"]

        # Extract the human-readable text from each agent result envelope.
        # Agent results have the shape {"status": "ok", "task": "...", "result": "<text>"}.
        # We surface "result" (or "message" as fallback) — never the raw dict.
        sections: list[str] = []
        for st in completed:
            result_data = st.get("result") or {}
            agent_text = (
                result_data.get("result")
                or result_data.get("message")
                or str(result_data)
            )
            sections.append(str(agent_text).strip())

        response = "\n\n".join(s for s in sections if s)

        if failed:
            failure_lines = ["**Note:** The following subtasks could not complete:"]
            for f in failed:
                failure_lines.append(f"- **{f['target_agent']}**: {f['error']}")
            response = (response + "\n\n" + "\n".join(failure_lines)).strip()

        sources = ", ".join(sorted({s["target_agent"] for s in completed})) or "none"
        response += f"\n\n---\n*Data current to {freshness_ts} · Quality: {quality} · Sources: {sources}*"

        state["response"] = response
        state["current_state"] = "respond"

    def _persist_turn(self, state: OrchestratorState) -> None:
        """Write the completed turn to persistent memory.

        Two separate writes are performed:

        1. Per-session conversation file (private/conversations/{session_id}.json)
           Two turn records are appended: one for the human message and one for
           the orchestrator response. Recording them as separate turn objects
           (with role "human" and "orchestrator" respectively) matches the
           common AI chat memory format and makes it straightforward to replay
           the conversation or fine-tune a model on it later.

           The orchestrator turn includes:
             - plan: the full SubTask list (for post-hoc analysis of planning
               quality and for the decomposition_cache learning loop).
             - agent_results: all raw agent outputs (for debugging).
             - metadata.latency_ms: end-to-end wall-clock latency for this turn,
               measured from `turn_start_time` (set at the very beginning of
               `_load_state`) to now. This is compared against
               `strategies/decomposition_cache.json` avg_latency_ms values to
               evaluate whether a plan was efficient.

        2. Global session index (private/conversations/index.json)
           A lightweight index of all sessions. Each entry stores only the
           session_id, creation time, last-updated time, turn count, and a
           120-character summary (the latest human message). This lets the
           orchestrator quickly find a relevant past session by summary text
           without reading every conversation file.

           If the session already has an index entry, it is updated in place.
           If not, a new entry is appended. This is an O(n) scan over sessions,
           which is acceptable for the expected number of sessions (hundreds,
           not millions).
        """
        conv_path = self._conversation_path()
        conv = cast(dict[str, Any], memory_read(conv_path) or {"session_id": self.session_id, "created_at": get_current_time(), "turns": []})
        if not isinstance(conv.get("turns"), list):
            conv["turns"] = []
        # Turn-level latency is captured here so downstream strategy learning
        # can evaluate decomposition quality over time.
        latency_ms = int((datetime.now(timezone.utc) - datetime.fromisoformat(state["turn_start_time"].replace("Z", "+00:00"))).total_seconds() * 1000)
        conv["turns"].append({
            "turn_id": state["turn_id"],
            "timestamp": get_current_time(),
            "role": "human",
            "message": state["human_message"],
            "plan": None,
            "agent_results": None,
            "metadata": {},
        })
        conv["turns"].append({
            "turn_id": generate_uuid(),
            "timestamp": get_current_time(),
            "role": "orchestrator",
            "message": state["response"],
            "plan": state["plan"],
            "agent_results": state["agent_results"],
            "metadata": {
                "latency_ms": latency_ms,
                "agents_used": sorted({s["target_agent"] for s in state["plan"]}),
                "subtask_count": len(state["plan"]),
                "intent_type": state.get("intent_type"),
                "from_cache": False,
            },
        })
        memory_write(conv_path, conv)

        index_path = PRIVATE_DIR / "conversations" / "index.json"
        idx = cast(dict[str, Any], memory_read(index_path) or {"sessions": []})
        if not isinstance(idx.get("sessions"), list):
            idx["sessions"] = []
        # Keep a light global index for quick session lookup without opening
        # every conversation file.
        found = False
        for s in idx.get("sessions", []):
            if s.get("session_id") == self.session_id:
                s["last_updated"] = get_current_time()
                s["turn_count"] = int(s.get("turn_count", 0)) + 1
                s["summary"] = state["human_message"][:120]
                found = True
                break
        if not found:
            idx.setdefault("sessions", []).append({
                "session_id": self.session_id,
                "created_at": get_current_time(),
                "last_updated": get_current_time(),
                "turn_count": 1,
                "summary": state["human_message"][:120],
            })
        memory_write(index_path, idx)

    def process_turn(self, human_message: str) -> str:
        """Drive one full turn of the state machine and return the response text.

        This is the primary interface for `main.py` and any other caller that
        only needs the final text response (not the agent trace).

        State machine execution order:
          1. _load_state     → create the OrchestratorState snapshot.
          2. _plan           → classify intent, build SubTask list, set next state.
          3. _dispatch       → if state is "dispatch": run all pending subtasks.
             _dispatch_direct → if state is "dispatch_direct": run single-step op.
          4. _synthesize     → if state is "synthesize": merge results into response.
          5. _persist_turn   → write the completed turn to JSON memory files.
          6. Return response string.

        The conditional checks on `state["current_state"]` after each method call
        implement the state transition logic. Each node sets the next state before
        returning, and the driver reads it to decide which node to call next. This
        mirrors the LangGraph execution model where a graph router reads
        `state["current_state"]` to select the next node.

        The fallback return "I could not complete the request." handles the
        (theoretically unreachable) case where the state never reached "respond".
        """
        # Minimal explicit state-machine driver:
        # understand/plan -> dispatch -> synthesize -> respond -> persist.
        state = self._load_state(human_message)
        self._plan(state)

        if state["current_state"] == "dispatch":
            self._dispatch(state)
        elif state["current_state"] == "dispatch_direct":
            self._dispatch_direct(state)

        if state["current_state"] == "synthesize":
            self._synthesize(state)

        if state["current_state"] == "respond":
            self._persist_turn(state)
            return self._attach_routing_note(state)

        self._persist_turn(state)
        return "I could not complete the request."

    def _attach_routing_note(self, state: OrchestratorState) -> str:
        """Append the routing explanation to the response so the user can see it."""
        response = state["response"] or "I could not produce a response."
        note = state.get("routing_note")
        intent = state.get("intent_type") or "unknown"
        if note:
            response += f"\n\n> *Routed to **{intent}** — {note}*"
        else:
            response += f"\n\n> *Routed to **{intent}***"
        return response

    def process_turn_with_trace(self, human_message: str) -> dict[str, Any]:
        """Like `process_turn`, but also returns the agent interaction trace.

        Returns a dict with two keys:
            "response": str — the final answer text.
            "trace":    list — ordered list of dispatch/response/error events.

        The trace is used by the web UI to render a sequence diagram showing
        which agents were contacted, in what order, and what they returned.
        It is also useful for debugging plan decisions and agent failures.

        This variant always calls `_persist_turn` regardless of final state
        (unlike `process_turn`, which calls it in two separate branches) to
        ensure the turn is always saved even if the state machine ended early.
        """
        _t0 = time.time()
        print(f"[orchestrator] process_turn_with_trace START — {human_message[:100]!r}")
        state = self._load_state(human_message)

        _tp = time.time()
        print("[orchestrator] _plan …")
        self._plan(state)
        print(f"[orchestrator] _plan done in {time.time()-_tp:.1f}s  next_state={state['current_state']!r}")

        if state["current_state"] == "dispatch":
            _td = time.time()
            print("[orchestrator] _dispatch …")
            self._dispatch(state)
            print(f"[orchestrator] _dispatch done in {time.time()-_td:.1f}s")
        elif state["current_state"] == "dispatch_direct":
            _td = time.time()
            print("[orchestrator] _dispatch_direct …")
            self._dispatch_direct(state)
            print(f"[orchestrator] _dispatch_direct done in {time.time()-_td:.1f}s")

        if state["current_state"] == "synthesize":
            _ts = time.time()
            print("[orchestrator] _synthesize …")
            self._synthesize(state)
            print(f"[orchestrator] _synthesize done in {time.time()-_ts:.1f}s")

        self._persist_turn(state)
        print(f"[orchestrator] process_turn_with_trace DONE — total {time.time()-_t0:.1f}s")
        return {"response": self._attach_routing_note(state), "trace": state["trace"]}


# ==============================================================================
# PUBLIC API
# ==============================================================================

def run_orchestrator_agent(request: str, session_id: Optional[str] = None) -> str:
    """Public entry point for a single-turn orchestrator call (no trace).

    Called by `main.py` and any other module that needs to send a request to
    the orchestrator and receive a plain text response. If `session_id` is
    provided, the call is treated as a continuation of an existing conversation
    (the session's history is loaded from memory). If omitted, a new session
    UUID is generated.

    This is the simplest public interface — one string in, one string out.
    """
    orchestrator = OrchestratorAgent(session_id=session_id or generate_uuid())
    return orchestrator.process_turn(request)


def run_orchestrator_agent_with_trace(request: str, session_id: Optional[str] = None) -> dict[str, Any]:
    """Public entry point for a single-turn orchestrator call that includes trace.

    Returns {"response": str, "trace": list}. Used by the web UI (FastAPI
    endpoint or Gradio interface in main.py) when the frontend needs to render
    the agent sequence diagram alongside the text response.

    The `session_id` argument follows the same semantics as
    `run_orchestrator_agent`.
    """
    orchestrator = OrchestratorAgent(session_id=session_id or generate_uuid())
    return orchestrator.process_turn_with_trace(request)


def orchestrator_inbox_listener() -> None:
    """Listen for messages sent by agents to the orchestrator inbox.

    Follows the same consumer pattern as kafka_consumer.py.
    Runs as a daemon thread so the orchestrator can receive proactive
    notifications (e.g. "dag fixed", "alert raised") from any agent
    without waiting for the next user request.

    task_response messages (replies to dispatched tasks) are handled by
    the per-dispatch reply consumer in _dispatch — this listener skips them
    so they are not consumed twice.
    """
    if KafkaConsumer is None:
        print("[orchestrator] kafka-python not available — inbox listener not started")
        return

    topic = KAFKA_TOPICS["orchestrator_inbox"]
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_CONFIG["bootstrap_servers"],
        group_id="orchestrator-inbox-group",
        auto_offset_reset="latest",
        enable_auto_commit=True,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    )
    print(f"[orchestrator] Inbox listener on '{topic}'... Ctrl+C to stop.")
    try:
        for msg in consumer:
            message = msg.value
            # task_response messages are consumed by the per-dispatch reply
            # consumer in _dispatch; skip them here to avoid double processing.
            if message.get("type") == "task_response":
                continue
            from_agent  = message.get("from_agent", "unknown")
            event_type  = message.get("event_type", message.get("type", "?"))
            payload_str = str(message.get("payload", ""))[:200]
            print(f"[orchestrator] ← {from_agent} | {event_type} | {payload_str}")
    except KeyboardInterrupt:
        print("\n[orchestrator] Inbox listener stopped.")
    finally:
        consumer.close()


# ==============================================================================
# EXAMPLE A2A TASK MESSAGES
# ==============================================================================
# The three EXAMPLE_* dicts below are reference templates — they are never
# called or parsed at runtime. Their purpose is to document the correct A2A
# payload format for each specialist agent's most common task types so that:
#
#   a) A developer implementing a new agent can copy the format exactly.
#   b) The LLM can be shown these examples in a few-shot prompt to teach it
#      how to construct valid task payloads.
#   c) Integration tests can use these as fixture inputs.
#
# Each dict key is the task name; the value is the complete payload dict that
# would appear in an A2A message's `payload` field.

EXAMPLE_ANALYST_TASKS: dict[str, Any] = {
    "count_events": {
        "task": "count_events",
        "params": {
            "store": "postgres",
            "table": "events",
            "filters": {
                "cameo_prefix": "14",                            # CAMEO 14 = Protest
                "countries": ["GR", "TU", "HU", "PL", "RO", "BG"],  # FIPS codes, not ISO
                "time_range": {
                    "start": "2026-03-21T00:00:00Z",
                    "end": "2026-04-20T23:59:59Z",
                },
            },
            "group_by": ["Actor1CountryCode"],
            "order_by": "count DESC",
        },
    },
    "get_sentiment_trend": {
        "task": "get_sentiment_trend",
        "params": {
            "store": "mongodb",
            "collection": "gkg_documents",
            "filters": {
                "countries": ["HU"],
                "time_range": {
                    "start": "2026-03-21T00:00:00Z",
                    "end": "2026-04-20T23:59:59Z",
                },
            },
            "gcam_dimensions": ["c12.1", "c12.3", "v10.1"],  # GCAM emotion dimensions
            "aggregation": "daily_average",
        },
    },
    "query_entity_network": {
        "task": "query_entity_network",
        "params": {
            "store": "neo4j",
            "seed_entities": ["HUNGARY", "ORBAN"],
            "relationship_types": ["MENTIONED_WITH", "ACTS_ON"],
            "max_depth": 2,
            "limit": 50,
        },
    },
    "search_themes": {
        "task": "search_themes",
        "params": {
            "store": "elasticsearch",
            "query": "PROTEST AND ECONOMIC_HARDSHIP",
            "time_range": {
                "start": "2026-03-21T00:00:00Z",
                "end": "2026-04-20T23:59:59Z",
            },
            "size": 100,
        },
    },
}

EXAMPLE_GOVERNANCE_TASKS: dict[str, Any] = {
    "verify_quality": {
        "task": "verify_quality",
        "params": {
            "scope": {
                "data_types": ["export", "gkg"],
                "time_range": {
                    "start": "2026-03-21T00:00:00Z",
                    "end": "2026-04-20T23:59:59Z",
                },
            },
            "checks": ["completeness", "freshness", "confidence_distribution"],
        },
    },
    "trace_lineage": {
        "task": "trace_lineage",
        "params": {
            "entity": "events.protest_count_hungary_2026q1",
            "direction": "upstream",   # "upstream" = where did this data come from?
            "depth": 3,
        },
    },
}

EXAMPLE_INGESTION_TASKS: dict[str, Any] = {
    "ingest_latest": {
        "task": "ingest_latest",
        "params": {
            "data_types": ["export", "mentions", "gkg"],
            "count": 10,  # Number of latest GDELT 15-min files to fetch
        },
    },
    "check_feed_health": {
        "task": "check_feed_health",
        "params": {},  # No parameters needed — the agent reads its own state
    },
    "backfill": {
        "task": "backfill",
        "params": {
            "time_range": {
                "start": "2026-04-15T00:00:00Z",
                "end": "2026-04-17T23:59:59Z",
            },
            "data_types": ["gkg"],  # Backfill only GKG; events were already loaded
        },
    },
}


# ==============================================================================
# CLI ENTRY POINT
# ==============================================================================

def run_cli() -> None:
    """Simple REPL loop for testing the orchestrator directly from a terminal.

    Usage:
        python agents/agent_orchestrator.py

    This starts a Read-Eval-Print Loop (REPL) that:
      1. Prompts for user input with "You: ".
      2. Passes the input to `orchestrator.process_turn(user_input)`.
      3. Prints the response and the wall-clock latency.
      4. Repeats until the user presses Ctrl+C or sends EOF (Ctrl+D).

    A single `OrchestratorAgent` instance is shared across all turns in the
    loop so that `session_id` stays constant and conversation history
    accumulates correctly (follow-up questions work as expected).

    The latency measurement here is coarser than the one in `_persist_turn`
    because it includes Python input() blocking time. The per-turn latency
    stored in memory (from `_persist_turn`) is the accurate processing latency.

    This function is only executed when the script is run directly, not when
    it is imported as a module (see the `if __name__ == "__main__":` guard).
    """
    print("[orchestrator] Master agent started. Type a request (Ctrl+C to exit).")
    # Start the inbox listener as a background daemon thread so the orchestrator
    # can receive proactive notifications from agents while waiting for user input.
    import threading as _threading
    _threading.Thread(target=orchestrator_inbox_listener, daemon=True, name="inbox").start()
    session_id = generate_uuid()
    orchestrator = OrchestratorAgent(session_id=session_id)
    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n[orchestrator] Session ended.")
            break
        if not user_input:
            continue
        started = time.time()
        result = orchestrator.process_turn(user_input)
        elapsed = int((time.time() - started) * 1000)
        print(f"\nOrchestrator: {result}\n")
        print(f"[orchestrator] latency={elapsed}ms | session={session_id}\n")


if __name__ == "__main__":
    run_cli()
