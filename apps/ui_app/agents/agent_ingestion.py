"""
Airflow Ingestion Agent
-----------------------
This module implements an autonomous agent that watches Apache Airflow for DAG
failures and attempts to resolve them without human intervention.

Full tech stack
~~~~~~~~~~~~~~~
* **LangChain** (``init_chat_model``, ``@tool``, ``bind_tools``)
  Provides the agentic loop scaffolding. ``init_chat_model`` creates an LLM
  instance backed by any provider; ``@tool`` turns ordinary Python functions
  into callable tools the model can invoke; ``bind_tools`` wires those tool
  schemas into the model so its responses can include structured ``tool_calls``
  payloads.

* **Ollama** (provider)
  Serves the LLM locally or on a private cloud endpoint. Here we use
  ``qwen3.5:397b-cloud``, a large reasoning model that is deterministic enough
  for infrastructure decisions when ``temperature=0.0``.

* **kafka-python** (``KafkaConsumer``, ``KafkaProducer``)
  Consumes Airflow failure events from the ``airflow-events`` Kafka topic in
  real time. This is the *preferred* event source because latency is
  milliseconds rather than the 60-second polling interval.

* **Apache Airflow REST API v1** (``/api/v1/...``)
  Used for: listing DAGs, fetching failed dag runs, reading task instance logs,
  and triggering new dag runs — all over HTTP with basic auth.

* **threading + queue.Queue**
  Two producer threads (Kafka listener, polling loop) push failure events onto a
  shared queue. A single consumer thread (the event processor) pops events one
  at a time and runs the LLM agent. This decouples event *detection* from event
  *processing* so a slow LLM call never blocks incoming events.

* **JSON file memory** (``memory/ingestion_memory.json``)
  Persists the set of already-handled ``dag_run_id`` values to disk. When the
  process restarts it reloads this set and skips any failures it already acted
  on, preventing duplicate retries.

Failure-detection sources
~~~~~~~~~~~~~~~~~~~~~~~~~
1. **Kafka** (real-time, preferred)
   Airflow can publish a JSON message to the ``airflow-events`` topic from an
   ``on_failure_callback`` on each DAG or globally via ``airflow.cfg``.
   Expected message format::

       {"dag_id": "...", "dag_run_id": "...", "task_id": "...", "try_number": 1}

2. **Polling loop** (fallback, every 60 s)
   Queries the Airflow REST API for recently failed dag runs. Catches failures
   that were never published to Kafka — e.g. when Kafka is down or the DAG
   author forgot to add the callback.

Agent decision logic
~~~~~~~~~~~~~~~~~~~~
1. Read the task log (``get_task_log``).
2. If the error is *transient* (network timeout, HTTP 5xx, resource not ready):
   call ``retry_dag``.
3. If the error is *deterministic* (SyntaxError, ImportError, wrong path):
   read the DAG file (``read_dag_file``), patch it (``patch_dag_file``), then
   retry.
4. Reply with a short human-readable summary of what was done and why.

To wire Airflow → Kafka add this callback to your DAGs or airflow.cfg:

    from kafka import KafkaProducer
    from access_hosts import KAFKA_BROKER as BROKER
    def on_fail(context):
        producer = KafkaProducer(
            bootstrap_servers=BROKER,
            value_serializer=lambda v: json.dumps(v).encode(),
        )
        producer.send("airflow-events", {
            "dag_id":     context["dag"].dag_id,
            "dag_run_id": context["run_id"],
            "task_id":    context["task_instance"].task_id,
            "try_number": context["task_instance"].try_number,
        })
        producer.flush()
"""

import os
import json
import queue
import threading
import time
import glob
from typing import Optional
from dotenv import load_dotenv

import requests
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

# LangChain entry points:
#   init_chat_model  — unified factory that builds a chat model from any
#                      provider (Ollama, OpenAI, Anthropic, …) via a single API.
#   HumanMessage     — wraps plain user text in the chat message format.
#   SystemMessage    — wraps the system / persona prompt.
#   ToolMessage      — wraps a tool's return value so the model sees it as
#                      coming from the tool rather than from the user.
#   BaseMessage      — the common type for all message variants (used for
#                      the messages list type hint).
#   tool             — decorator that registers a Python function as an
#                      LLM-callable tool.
from langchain.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.messages import BaseMessage
from langchain.tools import tool

# Load environment variables from .env (e.g. OLLAMA_API_KEY) before anything
# tries to read os.getenv(…).
load_dotenv()

try:
    from agents.model_config import build_model, serialize_lc_messages
except ModuleNotFoundError:
    from model_config import build_model, serialize_lc_messages

LAST_RUN_MESSAGES: list = []

# ── Knowledge docs ─────────────────────────────────────────────────────────────
# Airflow reference: DAG Python API + REST API sections.
# CLI sections are omitted — the agent calls the REST API, not the CLI.

_AIRFLOW_DOCS: str = ""
_AIRFLOW_DOCS_PATH = os.path.join(os.path.dirname(__file__), "memory", "knowledge", "airflow-context7.md")
try:
    with open(_AIRFLOW_DOCS_PATH) as _f:
        _raw = _f.read()
    _cut = _raw.find("## CLI - DAG Commands")
    _AIRFLOW_DOCS = (_raw[:_cut].strip() if _cut != -1 else _raw).strip()
    del _raw, _cut
except FileNotFoundError as e:
    print(f"[ingestion] knowledge doc not found: {e}")

_GDELT_DOCS: str = ""
_GDELT_DOCS_PATH = os.path.join(os.path.dirname(__file__), "memory", "knowledge", "gdelt-manual.md")
try:
    with open(_GDELT_DOCS_PATH) as _f:
        _GDELT_DOCS = _f.read().strip()
except FileNotFoundError as e:
    print(f"[ingestion] knowledge doc not found: {e}")

# ── Config ────────────────────────────────────────────────────────────────────

from access_hosts import AIRFLOW_URL, KAFKA_BROKER as BROKER, DAGS_DIR, REMOTE_USER, REMOTE_HOST

AUTH = ("admin", "admin")

# The Kafka topic that Airflow (or a custom callback) publishes failure events
# to. All agents that consume these events must agree on this name.
KAFKA_TOPIC = "airflow-events"

# Consumer group ID. Kafka uses this to track which messages each logical
# consumer group has already read (the "committed offset"). If you restart this
# agent with the same group ID, Kafka picks up where it left off instead of
# replaying old messages. Changing the group ID resets the offset.
KAFKA_GROUP = "ingestion-group"

# Absolute path to the directory where Airflow looks for DAG definition files.
# The agent writes patched .py files here so Airflow's DAG processor picks up
# the fix automatically on the next scan cycle (typically within 30 seconds).
# Value is controlled by ACCESS_MODE in access_hosts.py.


# How often (in seconds) the polling fallback wakes up to scan Airflow for
# failures that were never published to Kafka.
POLL_INTERVAL = 60  # seconds between polling cycles

# Path to the JSON file that stores the set of already-handled dag_run_ids.
# Using __file__ as the anchor means the path is relative to this module's
# location regardless of the working directory at launch.
MEMORY_PATH = os.path.join(os.path.dirname(__file__), "memory", "ingestion_memory.json")

# Shared queue: the threading handoff point between producers and the consumer.
#
# Producer threads (kafka_listener, polling_loop) call event_queue.put(event).
# The consumer thread (process_events) calls event_queue.get() to receive them.
#
# queue.Queue is thread-safe by design — no locks needed in the application
# code. Each item is a dict with keys: dag_id, dag_run_id, task_id, try_number.
event_queue: queue.Queue = queue.Queue()


# ── Deduplication helpers ─────────────────────────────────────────────────────

def _load_handled() -> set[str]:
    """
    Load the set of already-handled dag_run_ids from disk.

    This is the restart-safety mechanism. Without it, every time the agent
    process restarts it would re-process every known failure and trigger
    unwanted duplicate runs. The JSON file acts as a simple persistent set.

    Returns an empty set when the file doesn't exist (first run).
    """
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH) as f:
            return set(json.load(f).get("handled", []))
    return set()


def _save_handled(h: set[str]) -> None:
    """
    Persist the current handled set back to disk.

    Called immediately *after* adding a new run_id to the in-memory set and
    *before* invoking the agent. This order is deliberate: if the agent crashes
    mid-execution the run_id is already on disk, so the next restart will skip
    it and not trigger a second retry of the same failure.
    """
    # Create the memory/ subdirectory on first use; exist_ok avoids a race
    # condition if two threads somehow call this simultaneously.
    os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)
    with open(MEMORY_PATH, "w") as f:
        json.dump({"handled": list(h)}, f, indent=2)


# Module-level set loaded once at import time.
#
# Loading at import (not inside a function) means the set is shared by all
# threads in this process without needing a lock — Python's GIL ensures that
# set.add() and the `in` membership test are individually atomic for built-in
# types. The single consumer thread is the only writer, so there are no
# concurrent modifications to worry about.
handled: set[str] = _load_handled()


# ── Airflow REST API helpers ───────────────────────────────────────────────────

def _airflow_get(path: str, params: Optional[dict] = None):
    """
    Thin wrapper around requests.get for the Airflow REST API.

    Prepends AIRFLOW_URL + /api/v1 and injects basic auth so every caller
    gets consistent behavior without repeating boilerplate. Returns the raw
    requests.Response so callers can inspect .ok and .json() themselves.
    """
    return requests.get(f"{AIRFLOW_URL}/api/v1{path}", auth=AUTH, params=params)


def _dag_file_path(dag_id: str) -> Optional[str]:
    """
    Find the Python file for a dag_id inside DAGS_DIR.

    Uses a substring-match strategy: if the dag_id string appears anywhere in
    the filename the file is considered a match. This tolerates common naming
    patterns like ``dag_gdelt_backfill.py`` or ``gdelt_backfill_dag.py`` for a
    dag_id of ``gdelt_backfill``.

    Returns None when no match is found so callers can return a friendly error
    message rather than raising a FileNotFoundError.
    """
    # glob returns absolute paths; basename strips the directory so the
    # substring match only runs against the filename itself.
    for f in glob.glob(os.path.join(DAGS_DIR, "*.py")):
        if dag_id in os.path.basename(f):
            return f
    return None


# ── LangChain Tools ───────────────────────────────────────────────────────────
#
# The @tool decorator (from langchain.tools) turns each function below into a
# LangChain Tool object. It does three things automatically:
#
#   1. Extracts the function name as the tool name the model uses in tool_calls.
#   2. Uses the docstring as the human-readable description that appears in the
#      JSON schema sent to the model — write docstrings as instructions to the
#      LLM, not to human developers.
#   3. Generates a JSON Schema from the type-annotated parameters so the model
#      knows exactly what arguments to supply.
#
# Tools must have a docstring; without one LangChain raises a validation error.

@tool
def list_failed_tasks() -> str:
    """
    Return all recently failed DAG runs (last 25 per DAG) with their failed task instances.
    Use this to get a broad picture of what is broken right now.
    """
    # Fetch every known DAG in this Airflow instance (up to 100).
    # Then, for each DAG, walk its most recent failed runs and collect the
    # individual task instances that are in the "failed" state.
    dags_resp = _airflow_get("/dags", {"limit": 100})
    if not dags_resp.ok:
        return f"Could not list DAGs: {dags_resp.status_code}"

    results = []
    for dag in dags_resp.json().get("dags", []):
        dag_id = dag["dag_id"]

        # Limit to the 10 most recent failed runs per DAG. This cap keeps the
        # LLM's context window manageable — 10 runs is enough to spot a pattern
        # without flooding the prompt with hundreds of old failures.
        runs_resp = _airflow_get(
            f"/dags/{dag_id}/dagRuns",
            {"limit": 10, "order_by": "-execution_date", "state": "failed"},
        )
        if not runs_resp.ok:
            continue
        for run in runs_resp.json().get("dag_runs", []):
            run_id = run["dag_run_id"]
            # Fetch only the task instances that failed within this run.
            tasks_resp = _airflow_get(
                f"/dags/{dag_id}/dagRuns/{run_id}/taskInstances",
                {"state": "failed"},
            )
            for t in tasks_resp.json().get("task_instances", []):
                results.append(
                    f"dag={dag_id} run={run_id} task={t['task_id']} try={t.get('try_number', 1)}"
                )
    return "\n".join(results) if results else "No failed tasks found."


@tool
def get_task_log(dag_id: str, dag_run_id: str, task_id: str, try_number: int) -> str:
    """
    Fetch the last 30 lines of a task's execution log.
    Always call this before deciding whether to retry or fix the code.
    """
    url = (
        f"{AIRFLOW_URL}/api/v1/dags/{dag_id}/dagRuns/{dag_run_id}"
        f"/taskInstances/{task_id}/logs/{try_number}"
    )

    # The Airflow log endpoint can return either a JSON envelope {"content": "…"}
    # or a raw text file. Sending "Accept: text/plain" forces the raw format,
    # which is far easier to parse and much more compact in the LLM prompt.
    resp = requests.get(url, auth=AUTH, headers={"Accept": "text/plain"})
    if not resp.ok:
        return f"Log unavailable ({resp.status_code})"

    # Return only the *last* 30 lines. The first portion of any Airflow task log
    # is almost always startup boilerplate (Airflow version banner, DAG imports,
    # environment variable dumps) that adds noise without diagnostic value. The
    # actual error traceback and failure message appear near the end.
    lines = resp.text.strip().splitlines()
    return "\n".join(lines[-30:])


@tool
def retry_dag(dag_id: str) -> str:
    """
    Trigger a new run of the DAG. Use this for transient failures
    (network errors, timeouts, temporary resource issues).
    """
    # POST to the dagRuns endpoint with an empty ``conf`` dict. Airflow treats
    # this as a new *manual* dag run triggered immediately — equivalent to
    # clicking "Trigger DAG" in the Airflow UI. The empty conf means no
    # run-time parameters are overridden; the DAG uses its own defaults.
    url = f"{AIRFLOW_URL}/api/v1/dags/{dag_id}/dagRuns"
    resp = requests.post(url, auth=AUTH, json={"conf": {}})
    if resp.ok:
        run = resp.json()
        return f"Triggered: dag={dag_id} run_id={run['dag_run_id']} state={run['state']}"
    return f"Trigger failed ({resp.status_code}): {resp.text}"


@tool
def list_dag_files() -> str:
    """List all DAG Python files available in the DAGs directory."""
    # Try local first (works when running on the same machine as Airflow).
    # glob.glob never raises OSError — it just returns [] for missing dirs.
    local_files = glob.glob(os.path.join(DAGS_DIR, "*.py"))
    if local_files:
        return "\n".join(os.path.basename(f) for f in local_files)
    # Local dir absent — fall back to SSH.
    if REMOTE_USER and REMOTE_HOST:
        import subprocess
        r = subprocess.run(
            ["ssh", f"{REMOTE_USER}@{REMOTE_HOST}",
             f"ls '{DAGS_DIR}'/*.py 2>/dev/null || echo __EMPTY__"],
            capture_output=True, text=True, timeout=15,
        )
        if r.returncode == 0 and "__EMPTY__" not in r.stdout and r.stdout.strip():
            return "\n".join(os.path.basename(p) for p in r.stdout.strip().splitlines())
    return "No DAG files found."


@tool
def read_dag_file(dag_id: str) -> str:
    """
    Read the full source code of a DAG file.
    Use this before patching — you need to understand the current code first.
    """
    path = _dag_file_path(dag_id)
    if path:
        try:
            with open(path) as f:
                return f.read()
        except OSError as e:
            print(f"[ingestion] failed to read DAG file {path}: {e}")
    # Local path not found or unreadable — try SSH to the Pi.
    if REMOTE_USER and REMOTE_HOST:
        import subprocess
        remote_path = f"{DAGS_DIR}/*{dag_id}*.py"
        r = subprocess.run(
            ["ssh", f"{REMOTE_USER}@{REMOTE_HOST}",
             f"cat $(ls {remote_path} 2>/dev/null | head -1) 2>/dev/null || echo __NOT_FOUND__"],
            capture_output=True, text=True, timeout=15,
        )
        if r.returncode == 0 and "__NOT_FOUND__" not in r.stdout:
            return r.stdout
    return f"No file found for dag_id '{dag_id}' in {DAGS_DIR}"


@tool
def patch_dag_file(dag_id: str, new_content: str) -> str:
    """
    Overwrite a DAG file with corrected source code.
    Only use this when the log clearly shows a code bug (syntax error, wrong path,
    missing import, broken logic). Always read the file first, make minimal changes,
    and preserve the overall structure. After patching, call retry_dag.
    """
    import subprocess, tempfile, pathlib

    path = _dag_file_path(dag_id)
    remote_path = f"{DAGS_DIR}/{dag_id}.py"

    # ── Remote Pi path (DAGS_DIR not locally accessible) ──────────────────────
    if (not path or not os.path.exists(path or "")) and REMOTE_USER and REMOTE_HOST:
        # Write to a temp file then SCP to the Pi
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
            tmp.write(new_content)
            tmp_path = tmp.name
        try:
            # Backup on remote first
            subprocess.run(
                ["ssh", f"{REMOTE_USER}@{REMOTE_HOST}",
                 f"cp {remote_path} {remote_path}.bak 2>/dev/null; true"],
                timeout=15,
            )
            scp = subprocess.run(
                ["scp", tmp_path, f"{REMOTE_USER}@{REMOTE_HOST}:{remote_path}"],
                capture_output=True, text=True, timeout=30,
            )
        finally:
            pathlib.Path(tmp_path).unlink(missing_ok=True)
        if scp.returncode == 0:
            return f"Patched {dag_id}.py via SCP (remote backup saved as .bak)"
        return f"SCP failed: {scp.stderr.strip()} — hint: ssh-copy-id {REMOTE_USER}@{REMOTE_HOST}"

    if not path:
        return f"No file found for dag_id '{dag_id}' in {DAGS_DIR}"

    backup = path + ".bak"
    try:
        with open(path) as f:
            original = f.read()
        with open(backup, "w") as f:
            f.write(original)
        with open(path, "w") as f:
            f.write(new_content)
        return f"Patched {os.path.basename(path)} (backup saved to {os.path.basename(backup)})"

    except PermissionError as e:
        print(f"[ingestion] permission denied writing {path}, retrying with sudo: {e}")
        result = subprocess.run(
            ["sudo", "tee", path],
            input=new_content.encode(),
            capture_output=True,
        )
        if result.returncode == 0:
            subprocess.run(["sudo", "tee", backup], input=original.encode(), capture_output=True)
            return f"Patched {os.path.basename(path)} via sudo (backup saved)"
        return f"Permission error — could not patch {os.path.basename(path)}: {result.stderr.decode()}"


# ── LangChain Agent ───────────────────────────────────────────────────────────

# Collect all tool objects into a list for registration with the model.
# tools_by_name provides O(1) lookup when the model emits a tool_call with a
# specific tool name — used in the agentic loop below.
tools = [list_failed_tasks, get_task_log, retry_dag, list_dag_files, read_dag_file, patch_dag_file]
tools_by_name = {t.name: t for t in tools}

# Build the chat model using LangChain's provider-agnostic factory.
#
# init_chat_model(model, model_provider=…, …) abstracts away provider-specific
# SDK differences. Swapping providers (e.g. from Ollama to OpenAI) only
# requires changing these two arguments.
#
# Model choice — "qwen3.5:397b-cloud":
#   Qwen 3.5 at 397B parameters is a large reasoning model with strong code
#   understanding. The "-cloud" suffix indicates a cloud-hosted Ollama endpoint
#   rather than a locally-running instance.
#
# temperature=0.0:
#   Forces the model to always pick the highest-probability token, making its
#   decisions fully deterministic (no randomness). This is critical for
#   infrastructure operations: you want the model to make the *same* decision
#   every time it sees the same error, not a probabilistic one.
#
# max_retries=10:
#   LangChain will automatically retry failed API calls (rate limits, transient
#   network errors) up to 10 times with exponential back-off before giving up.
model = build_model("ingestion")

# bind_tools() injects the JSON schemas of all registered tools into every
# request the model receives. This enables the model to emit structured
# ``tool_calls`` in its response (instead of plain text) when it wants to
# invoke a tool. Without bind_tools the model has no knowledge that tools
# exist and will never produce a tool_call.
model_with_tools = model.bind_tools(tools)

# The system prompt is injected at the start of every conversation as the first
# message. It acts as the LLM's decision framework / operating manual:
#
#   - Defines the agent's role and goal.
#   - Establishes concrete decision rules (retry vs. fix).
#   - Specifies the exact workflow steps the agent must follow.
#   - Sets guardrails (minimal changes, preserve structure).
#
# Keeping this outside the functions means it is built once and reused across
# all agent calls, saving construction overhead.
SYSTEM_PROMPT = SystemMessage(content=f"""
## Service endpoints (from access_hosts.py)
- Airflow API : {AIRFLOW_URL}
- DAGs path   : {DAGS_DIR} (on Raspberry Pi — read_dag_file/patch_dag_file use SSH/SCP automatically)
- Kafka broker: {BROKER}

You are an autonomous Airflow ingestion agent. Your job is to keep the GDELT data
pipeline healthy — detect failures, fix them, and proactively prevent recurrence.

Decision rules:
- RETRY if the error is transient: network timeout, HTTP 5xx, temporary file lock,
  resource not available yet, connection refused.
- FIX CODE if the error is deterministic: SyntaxError, ImportError, FileNotFoundError
  (wrong hardcoded path), AttributeError, NameError, logic bugs, wrong URL.
- REFACTOR if the same DAG has failed more than twice with similar errors — fix the
  root cause properly rather than applying a patch.

Workflow:
1. Call get_task_log to read the failure details.
2. Based on the error, decide: retry, fix, or refactor.
3. If retry: call retry_dag directly.
4. If fix or refactor: call read_dag_file, analyse the code thoroughly, apply a
   complete and robust fix (not just the minimum change), call patch_dag_file with
   the corrected full file content, then call retry_dag.
5. After fixing, scan the rest of the DAG file for similar latent bugs and fix those
   too in the same patch — do not leave known problems behind.
6. Respond with a structured summary: what failed, root cause, what was changed, result.

Act immediately and decisively. Do not ask for permission before retrying or patching.
Preserve DAG identity (dag_id, schedule, owners) and task structure; everything else
can be improved. Leave the pipeline in a better state than you found it.
""")


# ── Agentic loop helpers ──────────────────────────────────────────────────────

def run_agent(event: dict) -> str:
    """
    Per-failure entry point for events sourced from the Kafka topic or the
    polling loop.

    The ``event`` dict seeds the first HumanMessage with exactly the failure
    context the model needs: which DAG failed, which run, which task, and which
    attempt number. This gives the model enough information to call
    ``get_task_log`` immediately without having to ask a clarifying question.

    Returns the model's final plain-text decision summary.
    """
    dag_id = event["dag_id"]
    dag_run_id = event["dag_run_id"]
    task_id = event.get("task_id", "unknown")
    try_number = event.get("try_number", 1)

    print(f"\n[ingestion] Handling failure: dag={dag_id} task={task_id} run={dag_run_id}")

    messages: list[BaseMessage] = [SYSTEM_PROMPT]
    if _AIRFLOW_DOCS:
        messages.append(SystemMessage(content=f"## Airflow reference\n\n{_AIRFLOW_DOCS}"))
    if _GDELT_DOCS:
        messages.append(SystemMessage(content=f"## GDELT GKG reference\n\n{_GDELT_DOCS}"))
    messages.append(HumanMessage(
        content=(
            f"DAG '{dag_id}' failed.\n"
            f"Run ID: {dag_run_id}\n"
            f"Failed task: {task_id} (try #{try_number})\n\n"
            f"Investigate and fix it."
        )
    ))

    # ── Agentic loop ──────────────────────────────────────────────────────────
    # This is the core ReAct (Reason + Act) pattern:
    #
    #   1. Call model_with_tools.invoke(messages) — the model sees the full
    #      conversation history and decides what to do next.
    #   2. Append the model's response to messages (so the next call has context).
    #   3. If the response contains tool_calls: execute each tool, wrap the
    #      result in a ToolMessage, and append it to messages, then loop back
    #      to step 1.
    #   4. If the response has NO tool_calls: the model has finished reasoning
    #      and produced its final answer as plain text. Break out of the loop.
    #
    # The loop naturally terminates when the model is satisfied — no fixed
    # iteration limit is needed, though in practice 3–6 iterations are typical.
    while True:
        response = model_with_tools.invoke(messages)
        messages.append(response)

        if response.tool_calls:
            # Execute every tool the model requested in this round.
            # A single response can request multiple tools simultaneously.
            for tc in response.tool_calls:
                print(f"[ingestion] tool_call: {tc['name']}({tc['args']})")
                result = tools_by_name[tc["name"]].invoke(tc["args"])
                print(f"[ingestion] tool_result: {str(result)[:300]}")
                # ToolMessage must carry the tool_call_id so the model can
                # correlate this result with the request it made.
                messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))
        else:
            # No more tool calls — the agent has reached a final decision.
            # response.content is the human-readable summary of what was done.
            print(f"[ingestion] decision: {response.content}")
            return str(response.content)


def _run_llm_agent(prompt: str) -> str:
    """
    Run the full agentic loop for an arbitrary free-text prompt.

    Identical in structure to run_agent() but accepts any prompt string instead
    of a structured event dict. Used by run_agent_task() and run_agent_chat()
    for operator-initiated queries that aren't tied to a specific failure event.

    Returns the model's final plain-text response.
    """
    messages: list[BaseMessage] = [SYSTEM_PROMPT]
    if _AIRFLOW_DOCS:
        messages.append(SystemMessage(content=f"## Airflow reference\n\n{_AIRFLOW_DOCS}"))
    if _GDELT_DOCS:
        messages.append(SystemMessage(content=f"## GDELT GKG reference\n\n{_GDELT_DOCS}"))
    messages.append(HumanMessage(content=prompt))
    _t0 = time.time()
    _iter = 0
    print(f"[ingestion] _run_llm_agent START — {prompt[:120]!r}")
    while True:
        _iter += 1
        _llm_t = time.time()
        print(f"[ingestion] LLM call #{_iter} …")
        response = model_with_tools.invoke(messages)
        print(f"[ingestion] LLM call #{_iter} done in {time.time()-_llm_t:.1f}s")
        messages.append(response)
        if response.tool_calls:
            for tc in response.tool_calls:
                _tool_t = time.time()
                print(f"[ingestion] tool_call: {tc['name']}({tc['args']})")
                result = tools_by_name[tc["name"]].invoke(tc["args"])
                print(f"[ingestion] tool_result ({tc['name']}): {str(result)[:300]}  [{time.time()-_tool_t:.1f}s]")
                messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))
        else:
            print(f"[ingestion] _run_llm_agent DONE in {time.time()-_t0:.1f}s ({_iter} LLM calls)")
            LAST_RUN_MESSAGES[:] = serialize_lc_messages(messages)
            return str(response.content)


# ── Programmatic / orchestrator API ──────────────────────────────────────────

def run_agent_task(task: str, params: Optional[dict] = None, context: Optional[dict] = None) -> dict:
    """
    Programmatic API for orchestrator calls.
    Supports high-level ingestion tasks and returns structured output.

    Supported task names and their behaviour:

    ``check_feed_health``
        Returns static configuration metadata about the agent (broker, topic,
        group, poll interval). No LLM or network call needed — purely
        informational so the orchestrator can confirm the agent is correctly
        configured before sending work.

    ``check_failed_dags``
        Runs the full LLM agentic loop with an optional custom prompt. The
        model will call list_failed_tasks, read logs, and decide whether to
        retry or patch each failure. Returns the model's summary.

    ``ingest_latest`` / ``backfill``
        Both branches trigger a new Airflow dag run via retry_dag (no LLM
        needed — it is a direct imperative action). Requires ``dag_id`` in
        params. Returns a success/error dict based on whether Airflow accepted
        the trigger.
    """
    params = params or {}

    if task == "check_feed_health":
        # Pure config echo — no external calls needed. Lets the orchestrator
        # verify the agent is alive and knows its configuration.
        return {
            "status": "ok",
            "message": f"Ingestion listener configured for topic '{KAFKA_TOPIC}' on '{BROKER}'.",
            "details": {
                "broker": BROKER,
                "topic": KAFKA_TOPIC,
                "group": KAFKA_GROUP,
                "poll_interval_s": POLL_INTERVAL,
            },
        }

    if task == "check_failed_dags":
        # Run the LLM agent to discover failures and decide whether to retry
        # or fix. The operator can supply a custom prompt via params["message"]
        # to narrow the scope (e.g. "only check gdelt DAGs").
        prompt = params.get("message") or "List all failed DAGs, read their logs, and fix or retry them."
        answer = _run_llm_agent(prompt)
        return {"status": "ok", "message": answer}

    if task in {"ingest_latest", "backfill"}:
        # Both are direct Airflow trigger actions. They differ in *which* DAG
        # they are meant to run (latest fetch vs. historical backfill), but
        # the mechanism is identical: call retry_dag with the right dag_id.
        dag_id = params.get("dag_id")
        if not dag_id:
            return {
                "status": "error",
                "message": "Missing required parameter: dag_id",
                "task": task,
            }
        trigger_result = retry_dag.invoke({"dag_id": dag_id})
        return {
            "status": "ok" if str(trigger_result).startswith("Triggered:") else "error",
            "message": str(trigger_result),
            "task": task,
            "params": params,
        }

    # Free-form chat message routed through A2A or directly from the UI.
    if task == "chat":
        prompt = params.get("message", "")
        answer = _run_llm_agent(prompt)
        return {"status": "ok", "result": answer}

    return {
        "status": "error",
        "message": f"Unsupported ingestion task: {task}",
    }


def run_agent_chat(request: str) -> str:
    """
    Conversational entry point for UI or orchestrator free-text use.

    Routes incoming requests based on keyword matching in the lowercased text:

    * DAG/failure-analysis keywords (``dag``, ``fail``, ``fix``, ``retry``,
      ``check``, ``investigate``, ``log``) → full LLM agentic loop. The model
      reads logs, reasons about the root cause, and decides what action to take.

    * ``backfill`` → direct call to run_agent_task("backfill", …).

    * ``ingest`` / ``latest`` → direct call to run_agent_task("ingest_latest", …).

    * Anything else → health-check echo via run_agent_task("check_feed_health").

    The two-tier routing keeps simple operational commands fast (no LLM round
    trip) while still allowing complex analytical queries to use the full agent.
    """
    lower = request.lower()
    _t0 = time.time()
    if any(k in lower for k in ("dag", "fail", "failure", "fix", "retry", "check", "investigate", "log")):
        print(f"[ingestion] run_agent_chat → LLM path for: {request[:80]!r}")
        result = _run_llm_agent(request)
        print(f"[ingestion] run_agent_chat DONE in {time.time()-_t0:.1f}s")
        return result
    if "backfill" in lower:
        print("[ingestion] run_agent_chat → backfill path")
        return str(run_agent_task("backfill", {"dag_id": "gdelt_backfill"}))
    if "ingest" in lower or "latest" in lower:
        print("[ingestion] run_agent_chat → ingest_latest path")
        return str(run_agent_task("ingest_latest", {"dag_id": "gdelt_ingest_latest"}))
    print("[ingestion] run_agent_chat → check_feed_health path")
    return str(run_agent_task("check_feed_health", {}))


# ── Event processor ───────────────────────────────────────────────────────────

def process_events() -> None:
    """
    Consume failure events from the shared queue and run the LLM agent for
    each unique failure.

    This function runs on the *main thread* and loops forever. It is the single
    consumer of event_queue; both producer threads (kafka_listener and
    polling_loop) feed into it.

    Deduplication order matters:
        1. handled.add(run_id)   — mark as handled in memory.
        2. _save_handled(handled) — persist to disk immediately.
        3. run_agent(event)      — invoke the LLM.

    Steps 1 and 2 happen *before* step 3. If the agent crashes or the process
    is killed mid-run_agent call, the run_id is already on disk. On the next
    restart the event will be skipped rather than retried — a deliberate
    conservative choice to avoid flooding Airflow with duplicate runs.

    queue.Queue.task_done() signals to any code calling event_queue.join() that
    this item has been fully processed. It is called at the end of every
    iteration (including the skip path) to keep the queue's internal counter
    accurate.
    """
    while True:
        event = event_queue.get()
        run_id = event.get("dag_run_id", "")

        # Skip runs already handled in this session or a previous one.
        if run_id in handled:
            print(f"[ingestion] Skipping already-handled run: {run_id}")
            event_queue.task_done()
            continue

        # Mark as handled BEFORE invoking the agent (crash-safety pattern).
        handled.add(run_id)
        _save_handled(handled)

        try:
            run_agent(event)
        except Exception as e:
            print(f"[ingestion] Agent error: {e}")

        # Signal that this queue item is fully processed.
        event_queue.task_done()


# ── Kafka listener ────────────────────────────────────────────────────────────

def kafka_listener() -> None:
    """
    Listen for Airflow failure events on the Kafka topic.
    Airflow should publish JSON messages to this topic via on_failure_callback.

    Example callback to add to your DAG:
        from kafka import KafkaProducer
        from access_hosts import KAFKA_BROKER as BROKER
        def on_fail(context):
            producer = KafkaProducer(bootstrap_servers=BROKER,
                                     value_serializer=lambda v: json.dumps(v).encode())
            producer.send("airflow-events", {
                "dag_id": context["dag"].dag_id,
                "dag_run_id": context["run_id"],
                "task_id": context["task_instance"].task_id,
                "try_number": context["task_instance"].try_number,
            })
            producer.flush()

    Reconnect loop design
    ~~~~~~~~~~~~~~~~~~~~~
    The outer ``while True`` loop recreates the KafkaConsumer from scratch on
    each iteration. This handles broker restarts cleanly: when the broker
    disappears the inner ``for msg in consumer`` loop raises an exception,
    which is caught, and after a back-off the outer loop reconnects. A
    long-lived consumer object that tries to reconnect internally is harder
    to reason about and sometimes gets stuck; starting fresh is simpler.

    ``auto_offset_reset="latest"``
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    When the consumer group has no committed offset (first run, or the offset
    expired), start reading from the *newest* available message rather than
    replaying the entire topic history. This is the right choice for an
    operational agent: we only care about *new* failures that occur while the
    agent is running, not failures from days ago that have likely already been
    addressed manually.

    ``NoBrokersAvailable`` back-off
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    A 30-second sleep prevents a tight CPU-burning retry loop if Kafka hasn't
    started yet (common during container stack bringup). Other exceptions use a
    shorter 10-second sleep because they might be transient network blips.
    """
    while True:
        try:
            # Reconnect from scratch on each outer loop iteration to handle
            # broker restarts cleanly. The consumer is recreated with the same
            # group_id so Kafka picks up from the last committed offset.
            consumer = KafkaConsumer(
                KAFKA_TOPIC,
                bootstrap_servers=BROKER,
                group_id=KAFKA_GROUP,
                # Only read messages published *after* this consumer first
                # connected (or after the last committed offset if the group
                # has been here before).
                auto_offset_reset="latest",
                # Deserialize message values from UTF-8 JSON bytes into dicts.
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            )
            print(f"[kafka] Listening on topic '{KAFKA_TOPIC}'...")
            for msg in consumer:
                event = msg.value
                # Accept messages that explicitly signal failure OR that carry
                # a dag_id field (some producers omit the state field and rely
                # on the topic name to convey the failure semantics).
                if event.get("state") == "failed" or "dag_id" in event:
                    print(f"[kafka] Event received: {event}")
                    event_queue.put(event)

        except NoBrokersAvailable:
            # Kafka may not be running yet (e.g. still starting up); use a
            # longer 30-second backoff to avoid a tight, CPU-burning retry loop.
            print("[kafka] Broker not available, retrying in 30s...")
            time.sleep(30)
        except Exception as e:
            # All other errors (network blips, deserialization failures, etc.)
            # use a shorter 10-second backoff since they may be transient.
            print(f"[kafka] Error: {e}, retrying in 10s...")
            time.sleep(10)


# ── Polling fallback ──────────────────────────────────────────────────────────

def polling_loop() -> None:
    """
    Fallback: poll Airflow every POLL_INTERVAL seconds for failed runs.
    Catches failures that were not published to Kafka.

    This function exists because the Kafka path requires DAG authors to add an
    ``on_failure_callback``. Not every DAG will have one, and Kafka itself can
    be temporarily unavailable. The polling loop ensures no failure goes
    unnoticed regardless of whether Kafka is working.

    Design choices:
    ~~~~~~~~~~~~~~~
    * **limit=5 per DAG** — keeps each polling cycle fast. Checking 5 recent
      runs per DAG across 50 DAGs is 50 API calls; bumping the limit to 25
      would make cycles noticeably slower with diminishing returns (older
      failures are likely already handled or stale).

    * **Only the first failed task instance** — the agent reads the full task
      list itself via ``list_failed_tasks`` once it starts investigating. Sending
      only the first task in the event keeps the event payload small and avoids
      pre-computing information the agent will re-fetch anyway.

    * **``if run_id in handled``** — filters out failures already in the
      deduplication set *before* enqueuing, saving unnecessary queue traffic for
      runs the processor would skip anyway.
    """
    print(f"[polling] Starting, interval={POLL_INTERVAL}s")
    while True:
        time.sleep(POLL_INTERVAL)
        try:
            dags_resp = _airflow_get("/dags", {"limit": 100})
            if not dags_resp.ok:
                continue
            for dag in dags_resp.json().get("dags", []):
                dag_id = dag["dag_id"]

                # Limit to the 5 most recent failed runs per DAG to keep each
                # polling cycle fast (avoids a large number of API calls when
                # there are many DAGs with long failure histories).
                runs_resp = _airflow_get(
                    f"/dags/{dag_id}/dagRuns",
                    {"limit": 5, "order_by": "-execution_date", "state": "failed"},
                )
                if not runs_resp.ok:
                    continue
                for run in runs_resp.json().get("dag_runs", []):
                    run_id = run["dag_run_id"]
                    if run_id in handled:
                        # Already processed in a previous polling cycle or via
                        # Kafka; skip without enqueuing.
                        continue

                    # Fetch the failed task instances for this run so the event
                    # can include an initial task_id for the agent to look at.
                    tasks_resp = _airflow_get(
                        f"/dags/{dag_id}/dagRuns/{run_id}/taskInstances",
                        {"state": "failed"},
                    )
                    tasks = tasks_resp.json().get("task_instances", [])
                    if tasks:
                        # Take only the *first* failed task. The agent will call
                        # list_failed_tasks itself to see the full picture; this
                        # is just enough context to seed the conversation.
                        t = tasks[0]
                        event = {
                            "dag_id": dag_id,
                            "dag_run_id": run_id,
                            "task_id": t["task_id"],
                            "try_number": t.get("try_number", 1),
                        }
                        print(f"[polling] Detected failure: {event}")
                        event_queue.put(event)
        except Exception as e:
            print(f"[polling] Error: {e}")


try:
    from agents.a2a_kafka_communication import kafka_worker as _kafka_worker, send_to_orchestrator as _send
except ModuleNotFoundError:
    from a2a_kafka_communication import kafka_worker as _kafka_worker, send_to_orchestrator as _send

def send_to_orchestrator(event_type: str, payload: dict) -> None:
    _send("ingestion", event_type, payload)

def kafka_worker() -> None:
    _kafka_worker("ingestion", run_agent_task)


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    """
    Three-thread architecture
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    When this module is run directly (not imported), three concurrent execution
    paths are started:

    Thread 1 — kafka_listener (daemon)
        Blocks on the Kafka consumer and pushes failure events onto
        event_queue. Marked as a daemon thread so it is automatically killed
        when the main thread exits (no cleanup needed for a Kafka consumer).

    Thread 2 — polling_loop (daemon)
        Sleeps for POLL_INTERVAL seconds, then scans Airflow for failures and
        pushes any new ones onto event_queue. Also a daemon thread.

    Main thread — process_events()
        Runs forever, popping events from event_queue one at a time and
        invoking the LLM agent for each. Running this on the main thread means
        KeyboardInterrupt (Ctrl-C) lands here and gracefully stops the process,
        which in turn kills both daemon threads.

    The queue is the only shared state between the three paths (beyond the
    ``handled`` set which is only written by process_events and only read by
    kafka_listener / polling_loop for the ``in handled`` check).
    """
    print("[ingestion] Starting Airflow Ingestion Agent")
    print(f"[ingestion] DAGs dir: {DAGS_DIR}")
    print(f"[ingestion] Kafka broker: {BROKER} | topic: {KAFKA_TOPIC}")

    # Kafka listener — real-time Airflow failure events (daemon: killed with main thread)
    threading.Thread(target=kafka_listener, daemon=True, name="kafka").start()

    # Kafka worker — orchestrator task requests on agent.ingestion.inbox (daemon)
    threading.Thread(target=kafka_worker, daemon=True, name="kafka-worker").start()

    # Polling loop — fallback (daemon: killed with main thread)
    threading.Thread(target=polling_loop, daemon=True, name="polling").start()

    # Event processor — runs agent for each failure (main thread, blocks forever)
    process_events()
