# goverflow

A self-hosted data platform built on a Raspberry Pi, developed as an MSc thesis project (University of Peloponnese). It ingests GDELT (Global Database of Events, Language, and Tone) — specifically the GKG (Global Knowledge Graph) subset — processes and catalogues the data, and exposes a multi-agent AI chat interface that can query, govern, and autonomously extend the pipeline.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Services](#services)
  - [Dockerfile.airflow](#dockerfileairflow)
  - [ui_app Dockerfile](#ui_app-dockerfile)
- [Multi-Agent System](#multi-agent-system)
  - [Chat UI & API](#chat-ui--api)
  - [Orchestrator](#orchestrator)
    - [SubTask TypedDict](#subtask-typeddict)
    - [Orchestrator memory system](#orchestrator-memory-system)
    - [Utility functions](#utility-functions)
  - [Analyst](#analyst)
  - [Governance](#governance)
  - [Ingestion](#ingestion)
  - [Coder](#coder)
  - [Agent-to-Agent Communication](#agent-to-agent-communication-a2a)
    - [Complete Kafka topology](#complete-kafka-topology)
  - [Model Configuration](#model-configuration)
  - [Shared Agent Infrastructure](#shared-agent-infrastructure)
- [Airflow DAGs](#airflow-dags)
- [Data Sources](#data-sources)
  - [GDELT domain knowledge](#gdelt-domain-knowledge-baked-into-agents)
- [Network & Connectivity](#network--connectivity)
- [Getting Started](#getting-started)
- [Project Layout](#project-layout)

---

## Architecture Overview

```
                        ┌─────────────────────────────────────────────────┐
                        │               Docker Compose Stack              │
                        │                                                 │
  ┌──────────────┐      │  ┌────────────┐      ┌────────────────────────┐ │
  │   GDELT      │──────▶  │  Airflow   │      │     OpenMetadata       │ │
  │  (external)  │      │  │ :8080      │─────▶│  (catalog + lineage)   │ │
  └──────────────┘      │  └─────┬──────┘      │     :8585              │ │
                        │        │ schedules    └───────────────────────┘ │
                        │        │                        │               │
                        │   ┌─────▼──────┐       ┌────────▼───────┐       │
                        │   │ PostgreSQL │       │ Elasticsearch  │       │
                        │   │   :5432    │       │    :9200       │       │
                        │   └────────────┘       └────────────────┘       │
                        │                                                 │
                        │  ┌────────────┐      ┌────────────────────────┐ │
                        │  │  MongoDB   │      │        Kafka           │ │
                        │  │  :27017    │      │  :9092 / :29092        │ │
                        │  └────────────┘      └────────────────────────┘ │
                        │                                                 │
                        │  ┌───────────────────────────────────────────┐  │
                        │  │         Multi-Agent UI  :8010             │  │
                        │  │  Orchestrator → Analyst / Governance /    │  │
                        │  │               Ingestion / Coder           │  │
                        │  └───────────────────────────────────────────┘  │
                        └─────────────────────────────────────────────────┘
```

All services run in a single Docker Compose network (`stack_net`). The Raspberry Pi is accessed remotely over **Tailscale VPN** (`100.95.246.75`).

---

## Services

| Service | Port | Image / Build | Description |
|---|---|---|---|
| PostgreSQL | 5432 | `postgres:15` | Stores Airflow metadata and OpenMetadata catalog data across `airflow_db` and `openmetadata_db`. `stack_db` (GDELT event tables) must be created separately — it is not in `init-db.sql`. |
| MongoDB | 27017 | `mongo:7` | Stores processed GDELT GKG records (`gkd_db`), agent memory, and document collections |
| Kafka | 9092 / 29092 | `confluentinc/cp-kafka:7.7.1` | KRaft-mode (no ZooKeeper) broker for event streaming and agent-to-agent messaging |
| Elasticsearch | 9200 | `docker.elastic.co/elasticsearch:7.17.24` | Full-text search index backing OpenMetadata's discovery UI |
| OpenMetadata | 8585 | `openmetadata/server:1.12.5` | Data catalog, lineage tracking, data quality tests, and asset classification |
| Airflow Webserver | 8080 | custom (`Dockerfile.airflow`) | DAG management UI with OpenMetadata lineage backend installed |
| Airflow Scheduler | — | custom (`Dockerfile.airflow`) | DAG scheduling and task execution |
| Multi-Agent UI | 8010 | custom (`apps/ui_app/Dockerfile`) | FastAPI chat interface backed by five LangChain agents |

> **Redis** is defined in `docker-compose.yml` but commented out. It is not used by the current stack.

Airflow is configured with the **OpenMetadata Lineage Backend** (`AIRFLOW__LINEAGE__BACKEND: OpenMetadataLineageBackend`) so every DAG run automatically registers lineage edges in the catalog without any per-DAG annotation.

### Dockerfile.airflow

The custom Airflow image extends `apache/airflow:2.9.0-python3.10` with:

| Package | Version | Purpose |
|---|---|---|
| `openmetadata-ingestion` | 1.12.5 | OpenMetadata lineage backend provider |
| `openmetadata-managed-apis` | 1.12.5 | OpenMetadata managed pipeline APIs |
| `presidio-analyzer` | 2.2.33 | PII detection (used by Governance agent checks) |
| `presidio-anonymizer` | 2.2.33 | PII anonymisation |
| `pymongo` | latest | MongoDB driver for DAG tasks |
| `psycopg2-binary` | latest | PostgreSQL driver for DAG tasks |
| `tabulate` | 0.9.0 | Pinned to resolve conflict with openmetadata packages |
| `sqlparse` | 0.5.3 | Pinned (force-reinstalled last to override transitive deps) |
| `protobuf` | 6.30.2 | Pinned (force-reinstalled last to override transitive deps) |

The three pinned packages are installed last with `--force-reinstall` because openmetadata-ingestion pulls in conflicting transitive versions.

### ui_app Dockerfile

Built from `python:3.11-slim`. Installs `openssh-client` so the Coder agent can SCP DAG files to the Pi. After pip installing requirements, applies a one-line security patch to LangGraph's checkpoint serializer:

```dockerfile
RUN sed -i 's/LC_REVIVER = Reviver()/LC_REVIVER = Reviver(allowed_objects="core")/' \
    /usr/local/lib/python3.11/site-packages/langgraph/checkpoint/serde/jsonplus.py
```

This restricts object deserialization to the `"core"` allowlist, preventing arbitrary Python object instantiation through the checkpoint store. Source code is not copied into the image — it is bind-mounted at runtime so `--reload` works during development.

---

## Multi-Agent System

`apps/ui_app/` is a **FastAPI** application that serves a self-contained single-page chat interface. Users select a target agent (or `all` / `orchestrator`) and send a message. Each request is dispatched to one or more LangChain agent loops that call tools, read data, and return a streamed response.

All agents run at **temperature 0.0** and are served through the **Ollama cloud endpoint**. Models are centrally registered in `agents/model_config.py` — swap any model there without touching agent code.

| Agent | File | Model | Role |
|---|---|---|---|
| Orchestrator | `agent_orchestrator.py` | `deepseek-v4-pro:cloud` | Master coordinator — decomposes, dispatches, synthesises |
| Analyst | `agent_analyst.py` | `deepseek-v4-flash:cloud` | GDELT analytics from PostgreSQL + MongoDB |
| Governance | `agent_governance.py` | `nemotron-3-super:cloud` | Data quality, asset classification, lineage (OpenMetadata) |
| Ingestion | `agent_ingestion.py` | `gemma4:31b-cloud` | Airflow DAG failure watchdog — detect, classify, retry/patch |
| Coder | `agent_coder.py` | `qwen3-coder-next` | Autonomous file-editing and DAG patching with safety checks |

Agent communication goes entirely through **Kafka A2A** (`agents/a2a_kafka_communication.py`) — there are no direct in-process calls in the normal request path.

### Chat UI & API

**File:** `main.py`

#### Lifespan

FastAPI's `lifespan` is an `asynccontextmanager` that runs code **once at server startup** (before the first request) and **once at shutdown** (after the last request). Everything before `yield` is startup; everything after `yield` is teardown.

```python
@asynccontextmanager
async def lifespan(_app: FastAPI):
    # --- startup: runs once when uvicorn is ready ---
    for name, fn in workers:
        threading.Thread(target=fn, daemon=True, name=f"a2a-{name}").start()
    yield
    # --- shutdown: runs when the process is stopping ---
    # (daemon threads die automatically with the process — nothing to clean up)

app = FastAPI(lifespan=lifespan)
```

This is the modern replacement for the deprecated `@app.on_event("startup")` decorator. The advantage is that startup and teardown logic live in the same function, making it obvious what gets set up and what needs to be cleaned up.

In this project, lifespan is used to start the four A2A Kafka consumer threads — one per specialist agent — so they are listening on their inbox topics before the first chat request arrives. All four threads are `daemon=True`, which means Python will not wait for them to finish when the process exits; they die automatically with uvicorn.

#### FastAPI endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Serves the full single-page chat UI as inline HTML |
| `POST` | `/api/chat` | Synchronous JSON chat — returns all agent responses in one payload |
| `POST` | `/api/chat/stream` | SSE streaming — emits `thinking → start_response → token* → end_response → traces → done` events so the UI can render incrementally |
| `GET` | `/api/auto-check` | Fan-out health check: all four specialist agents answer narrow diagnostics in parallel and return a single report with OK / CRITICAL status |
| `GET` | `/api/dag-check` | Read-only DAG audit: Coder agent inspects all `.py` DAG files and returns improvement suggestions without writing anything |
| `POST` | `/api/dag-apply` | Apply improvements from a previous `/api/dag-check` call — Coder patches, backs up, and syntax-checks each file |

#### Request model

```python
class ChatRequest(BaseModel):
    message: str                    # user input
    target: Literal[                # which agent(s) to invoke
        "orchestrator", "analyst", "governance",
        "ingestion", "coder", "all"
    ] = "orchestrator"
    session_id: str | None = None   # ties multiple turns into one session
    history: list[dict] | None = None  # last N turns [{role, agent, text}]
```

#### Conversation context

`_build_context()` prepends the last 10 chat turns (each capped at 600 chars) to every agent call so agents have full conversation continuity without re-sending the entire history to the LLM. Format:

```
Conversation so far:
User: <previous message>
Analyst: <previous response>
...
---
Current request: <new message>
```

#### Hard timeout

Every agent call runs inside a `ThreadPoolExecutor(max_workers=1)` with `AGENT_TIMEOUT_SECONDS = 1200` (20 minutes). If the agent hangs, the thread is abandoned and a timeout message is returned — the FastAPI event loop is never blocked.

#### Trace log

Every request produces a `traces` list emitted alongside responses. Each entry records the direction (`from`, `to`), event type (`chat_request` / `chat_response`), timestamp, and, for specialist agents, the full serialized LangChain message chain (`raw_lc`) including tool calls and tool results. The UI renders these in a right-hand sequence panel with an interactive JSON tree viewer.

#### Single-page UI features

- Dark-themed chat interface with markdown rendering inside bot bubbles (headings, tables, code blocks, blockquotes)
- Left sidebar with persistent session list (stored in `localStorage`) and a **New Chat** button
- Agent selector dropdown (`orchestrator` / `analyst` / `governance` / `ingestion` / `coder` / `all`)
- Live SSE streaming with animated thinking dots and a blinking cursor while the agent is working
- Right-hand sequence diagram panel showing the agent graph (SVG) and a scrollable flow log of every tool call / response
- Clickable flow cards open a JSON payload inspector with a collapsible tree view and raw mode
- **Auto-check tab** in the sidebar: runs `/api/auto-check` on demand and pulses red when CRITICAL issues are detected
- **DAG upgrade tab**: runs `/api/dag-check` and surfaces a one-click "Apply" button that posts suggestions to `/api/dag-apply`

---

### Orchestrator

**File:** `agents/agent_orchestrator.py`  
**Model:** `deepseek-v4-pro:cloud` via Ollama (temperature 0.0)  
**Knowledge:** GDELT domain knowledge baked directly into the system prompt (CAMEO event codes, Goldstein scale, QuadClass, FIPS country codes, polystore mapping) — not loaded from files. This allows it to translate raw GDELT identifiers into human-readable answers without LLM hallucination.

The master coordinator. Its internal architecture mirrors the LangGraph state-machine pattern — `TypedDict` state dicts passed through node functions — implemented in plain Python so it runs on a Raspberry Pi without heavy ML dependencies.

#### State machine

```
idle → understand → plan → dispatch → synthesise → respond
```

| State | Action |
|---|---|
| `understand` | Classifies the user's intent; identifies which specialist agents are relevant |
| `plan` | Decomposes the request into `SubTask` TypedDicts — one per specialist agent, each with a focused prompt |
| `dispatch` | Fans tasks out to specialist agents; runs independent tasks concurrently via threads |
| `synthesise` | Merges each agent's raw response into a single coherent, structured answer |
| `respond` | Streams the final answer back to the chat UI along with a trace log |

Key implementation details:
- `OrchestratorAgent` is a `@dataclass` — auto-generated `__init__`, easy to extend.
- `SubTask` and `OrchestratorState` are `TypedDict` — dict literals with statically known keys, trivially JSON-serialisable.
- `fcntl` file locking protects concurrent writes to shared memory files from multiple agents.

#### SubTask TypedDict

One `SubTask` is created per specialist agent per user request. It is created in the `PLAN` state and mutated through `DISPATCH → WAIT → SYNTHESIZE`.

| Field | Type | Description |
|---|---|---|
| `subtask_id` | `str` | Stable identifier used in `depends_on` chains (e.g. `"gov-1"`, `"ana-1"`) |
| `target_agent` | `Literal[...]` | Which agent executes this task: `"analyst"` / `"governance"` / `"ingestion"` / `"coder"` |
| `task` | `str` | Named operation forwarded to `run_agent_task()` (e.g. `"count_events"`, `"chat"`) |
| `params` | `dict` | Parameters passed verbatim to the agent |
| `depends_on` | `list[str]` | `subtask_id`s that must complete before this task can be dispatched; `[]` means immediately eligible |
| `timeout_ms` | `int` | Max wait time in ms; heavy tasks get 120 000, orchestrator default is 220 000 |
| `fallback` | `str \| None` | Human-readable fallback description for the synthesiser's caveat text |
| `status` | `Literal[...]` | `"pending"` → `"dispatched"` → `"completed"` \| `"failed"` |
| `result` | `dict \| None` | Agent response dict on success |
| `error` | `str \| None` | Error message on failure |
| `dispatch_time` | `str \| None` | ISO 8601 timestamp at moment of dispatch |
| `completion_time` | `str \| None` | ISO 8601 timestamp when result/error is received |
| `retries` | `int` | Dispatch retry count (max 3) |

#### Orchestrator memory system

The Orchestrator maintains two file-backed memory layers. All shared files are protected by `fcntl.flock` to prevent corruption from concurrent agent writes.

**Private memory** — only the Orchestrator reads and writes:

| File | Content |
|---|---|
| `memory/private/conversations/{session_id}.json` | Full chat history per session: `turn_id`, `timestamp`, `role`, `message`, `plan`, `agent_results`, `metadata` (latency, agents used) |
| `memory/private/conversations/index.json` | Index of all sessions: `session_id`, `created_at`, `last_updated`, summary. Used to find relevant past sessions. |
| `memory/private/strategies/decomposition_cache.json` | Learned decomposition patterns keyed by normalised intent signature. Each entry has a subtask template, success count, and average latency. Checked before planning — if a matching pattern exists it is reused. |
| `memory/private/agents/capability_registry.json` | Per-agent: `status` (healthy/degraded/offline), last heartbeat, capabilities, avg response time, error rate. Updated from heartbeat messages and actual interaction results. |
| `memory/private/user/user_context.json` | Accumulated user knowledge: frequent regions, topics, preferred output format, session count. Used to personalise responses. |

**Shared memory** — all agents read and write:

| File | Content |
|---|---|
| `memory/shared/schema_registry.json` | Current state of all data stores: tables, collections, indexes, field types, row counts. Written by Ingestion; read by Orchestrator and Analyst. |
| `memory/shared/data_freshness.json` | Latest ingestion timestamp per GDELT data type (export, mentions, gkg). Always checked before planning. |
| `memory/shared/quality_alerts.json` | Active data quality issues from Governance. Each alert has `alert_id`, `severity`, `scope`, `description`, `created_at`. |
| `memory/shared/result_cache/{query_hash}.json` | Cached Analyst query results with TTL (default 60 min). Hash is computed from query params with `compute_query_hash()`. |

The `decomposition_cache` means repeated or similar questions get faster, cheaper answers — the Orchestrator skips the planning LLM call and reuses a known-good subtask template.

#### Utility functions

| Function | Signature | Purpose |
|---|---|---|
| `get_current_time()` | `→ str` | Current UTC time as ISO 8601 with `Z` suffix |
| `generate_uuid()` | `→ str` | New UUID4 string — used for `session_id`, `turn_id`, `correlation_id`, `message_id` |
| `compute_query_hash(params)` | `dict → str` | SHA-256 of a JSON-serialised params dict (sorted keys) — used as result cache filenames |
| `create_a2a_message(from_agent, to_agent, msg_type, ...)` | `→ dict` | Builds a well-formed A2A envelope with all required fields |

---

### Analyst

**File:** `agents/agent_analyst.py`  
**Model:** `deepseek-v4-flash:cloud` via Ollama (temperature 0.0)  
**Knowledge docs:** `gdelt-manual.md`, `mongodb-context7.md`, `postgressql-context7.md` — injected at startup. Also receives GDELT domain knowledge (CAMEO codes, Goldstein scale, etc.) baked into its system prompt, same as the Orchestrator.

Produces structured analytics from GDELT data stored in **PostgreSQL** (`stack_db`) and **MongoDB** (`gkd_db`). Specialises in news digests, event frequency counts, tone analysis, and cross-source correlation.

Uses a `ThreadPoolExecutor` to parallelise multi-source queries and reduce response time on the Raspberry Pi's limited CPU.

A PostgreSQL connection pool (`psycopg2.pool`) is shared across calls. The pool is reset automatically if a connection goes stale.

#### Tools available to the model

| Tool | Description |
|---|---|
| `postgres_query(sql)` | Executes a read-only SQL query on `stack_db`; returns results as a markdown table |
| `gkg_summary()` | High-level summary of GKG records from the last 24 h (MongoDB) |
| `gkg_top_themes(n)` | Top N GDELT GKG themes by frequency |
| `gkg_top_persons(n)` | Top N named persons mentioned across all GKG records |
| `gkg_top_organizations(n)` | Top N named organisations |
| `gkg_top_locations(n)` | Top N locations with event counts |
| `gkg_tone_analysis()` | Aggregate tone statistics (avg, min, max, polarity, activity ref density) |
| `gkg_counts_events(top_n)` | Top event count types from the COUNTS field |
| `gkg_search_theme(keyword)` | Filter GKG records containing a specific theme |
| `gkg_quotations(n)` | Top N quoted passages extracted from source articles |
| `gkg_gcam_emotions()` | GCAM emotion dimension aggregation (valence, arousal, etc.) |
| `gkg_top_amounts(n)` | Top N numeric amounts found in AMOUNTS field |
| `gkg_all_names(n)` | Combined top persons + organisations |
| `gkg_search_person(name)` | Full records mentioning a specific person |
| `gkg_search_location(name)` | Full records mentioning a specific location |

Parsers for GKG's semicolon-separated fields (`V2THEMES`, `COUNTS`, `AMOUNTS`, `GCAM`, `TONE`) are implemented locally — no external GKG parsing library is used.

---

### Governance

**File:** `agents/agent_governance.py`  
**Model:** `nemotron-3-super:cloud` via Ollama (temperature 0.0)

Enforces data quality, maintains metadata, classifies assets by risk and sensitivity, and traces data lineage. Deterministic output (temperature 0.0) is critical — classification labels must be stable across calls.

Connects to: **OpenMetadata REST API**, **PostgreSQL** (read-only), **MongoDB** (read-only), **Airflow REST API**.  
Knowledge docs injected at startup: `gdelt-manual.md`, `openmetadata-context7.md`, `mongodb-context7.md`, `postgressql-context7.md`.

Persistent state is stored in `agents/memory/governance_memory.json` with three keys:
- `classifications` — asset → risk/sensitivity labels
- `lineage` — directed edges (source → destination)
- `incidents` — governance policy violations

#### Tools available to the model

| Tool | Description |
|---|---|
| `catalog_snapshot(service, database)` | Returns the full known-assets snapshot from `catalog_manifest.json` (written every 30 min by Airflow); optionally filtered by service or database |
| `openmetadata_api(method, path, params, body)` | General-purpose OpenMetadata REST client — GET/PUT/POST/PATCH; used for table tagging, lineage edges, quality test registration |
| `postgres_query(sql, limit)` | Read-only PostgreSQL query for schema introspection (`information_schema`) and data profiling |
| `mongodb_query(database, collection, pipeline, limit)` | MongoDB aggregation pipeline; read-only |
| `dag_reader(action, filename)` | Parses a DAG `.py` file with Python `ast` (no import/execution) to extract task graph, operators, Dataset URIs, and dependency edges for lineage |
| `airflow_api(method, path, params, body)` | Airflow REST API client — used read-only for DAG metadata and run history |

---

### Ingestion

**File:** `agents/agent_ingestion.py`  
**Model:** `gemma4:31b-cloud` via Ollama (temperature 0.0)  
**Knowledge docs:** `airflow-context7.md` — injected at startup so the agent understands Airflow operator types, task lifecycle, and log formats without needing exploratory LLM calls.

Autonomous watchdog for Airflow DAG failures. Two failure-detection threads run concurrently, pushing events onto a shared `queue.Queue`. A single consumer thread pops events and runs the LLM agent — decoupling event detection from (potentially slow) LLM processing.

#### Failure-detection sources

| Source | Mechanism | Latency |
|---|---|---|
| Kafka topic `airflow-events` | `KafkaConsumer` listening in real time | Milliseconds |
| Airflow REST API | Polling loop every 60 s | Up to 60 s |

The Kafka source is preferred. The polling loop is a fallback for failures never published to Kafka (e.g. Kafka is down, or the DAG author didn't add the callback).

#### Decision logic per failure

1. Call `get_task_log` — read the last 10 log lines via Airflow REST API.
2. **Transient error** (network timeout, HTTP 5xx, resource not ready) → call `retry_dag`.
3. **Deterministic error** (SyntaxError, ImportError, wrong path) → call `read_dag_file`, then `patch_dag_file` to fix the source, then `retry_dag`.
4. Report a human-readable summary of what was done and why.

Already-handled `dag_run_id` values are persisted to `agents/memory/ingestion_memory.json`. On restart, this set is reloaded and duplicate retries are skipped.

#### Tools available to the model

| Tool | Description |
|---|---|
| `list_failed_tasks()` | Lists all DAG runs in `failed` state from the Airflow REST API |
| `get_task_log(dag_id, dag_run_id, task_id, try_number)` | Fetches the last 10 lines of a specific task's log |
| `retry_dag(dag_id)` | Triggers a new DAG run via Airflow REST API |
| `list_dag_files()` | Lists all `.py` files in the DAGs directory |
| `read_dag_file(dag_id)` | Reads the full source of a DAG file |
| `patch_dag_file(dag_id, new_content)` | Overwrites a DAG file with new content after a syntax check |

#### Wiring Airflow → Kafka

Add an `on_failure_callback` to your DAGs (already implemented in `dags/kafka_callbacks.py`):

```python
from kafka import KafkaProducer
from access_hosts import KAFKA_BROKER

def on_fail(context):
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode(),
    )
    producer.send("airflow-events", {
        "dag_id":     context["dag"].dag_id,
        "dag_run_id": context["run_id"],
        "task_id":    context["task_instance"].task_id,
        "try_number": context["task_instance"].try_number,
    })
    producer.flush()
```

---

### Coder

**File:** `agents/agent_coder.py`  
**Model:** `qwen3-coder-next` via Ollama (temperature 0.0)  
**Knowledge docs:** `airflow-context7.md`, `gdelt-manual.md` — injected at startup so the agent understands the DAG patterns and GDELT data structures it is editing.

Autonomous file-editing agent for Python source files and Airflow DAGs. Designed for safe, auditable edits with no possibility of silent corruption.

#### Safety guarantees on every write

1. **Backup** — microsecond-timestamped copy created before any overwrite, auto-pruned to the last `CODER_BACKUP_KEEP_LAST_N` (default 10) backups per file.
2. **Syntax check** — `ast.parse()` run after every `write_file` or `patch_file`. Write is rejected if the AST parse fails.
3. **`catchup=False` guard** — AST walk run after every DAG write to confirm the DAG won't backfill historical runs unexpectedly.
4. **Context compaction** — after `COMPACT_AFTER_ITERS` (default 8) LLM iterations, the message history is compacted to the last `COMPACT_KEEP_TAIL` (6) messages to avoid context overflow on long editing sessions.

#### Configurable limits

| Env var | Default | Description |
|---|---|---|
| `CODER_MAX_FILE_SIZE_MB` | 5 | Maximum content size per write |
| `CODER_BACKUP_KEEP_LAST_N` | 10 | Backups retained per file |
| `CODER_MAX_ITERS` | 20 | LLM iteration cap per run |
| `CODER_ALLOWED_DIRS` | (see below) | Colon-separated list of directories the agent may write to |

#### Allowed write directories (default)

- `apps/ui_app/` — local project root
- `/home/alexpi/goverflow/dags/` — Airflow DAGs directory. Writes to this path are sent over **SCP/SSH** to the remote Pi, so the Docker container can modify live DAGs without a volume mount.

#### Tools available to the model

| Tool | Description |
|---|---|
| `read_file(path)` | Read any file within allowed directories |
| `write_file(path, content)` | Full file overwrite — backs up first, then checks syntax |
| `patch_file(path, old_str, new_str)` | Surgical string replacement — backs up, replaces, checks syntax |
| `list_directory(path, pattern)` | List files matching a glob pattern |
| `search_files(directory, pattern)` | Recursive glob search |
| `run_syntax_check(path)` | Explicit `ast.parse()` check on any file |
| `create_directory(path)` | Create a new directory within allowed paths |

---

### Agent-to-Agent Communication (A2A)

**File:** `agents/a2a_kafka_communication.py`

All agent communication — whether triggered by the Orchestrator or directly by a user selecting a specific agent in the UI — goes through Kafka A2A. There are no direct in-process function calls in the normal request path.

#### Startup

When uvicorn starts, `main.py`'s `lifespan()` launches four daemon threads — one per specialist agent — each running `kafka_worker()`. These threads open a `KafkaConsumer` on their inbox topic and wait for work before the first request arrives.

```
uvicorn starts → lifespan()
  analyst    kafka_worker thread → KafkaConsumer on agent.analyst.inbox
  governance kafka_worker thread → KafkaConsumer on agent.governance.inbox
  coder      kafka_worker thread → KafkaConsumer on agent.coder.inbox
  ingestion  kafka_worker thread → KafkaConsumer on agent.ingestion.inbox
```

#### `dispatch_and_wait()` — the shared request-reply function

**File:** `agents/a2a_kafka_communication.py`

Every caller — `main.py` for direct user messages and `agent_orchestrator._call_agent()` for orchestrated tasks — uses the same function:

```python
dispatch_and_wait(target, task, params, context, timeout_ms)
```

Internal steps:
1. Generate a `correlation_id` (UUID).
2. Open a `KafkaConsumer` on `agent.orchestrator.inbox` with a unique `group_id` (`orch-reply-{correlation_id}`) **before** publishing — prevents missing a fast response.
3. Publish a `task_request` envelope to `agent.{target}.inbox`.
4. Poll the reply consumer until a `task_response` with the matching `correlation_id` arrives, or `timeout_ms` elapses.
5. Return the `payload` dict from the response, or `None` on timeout/error.

The caller falls back to a direct `run_agent_task()` call if `None` is returned (broker down or timeout).

#### Path 1 — user sends message directly to an agent

User selects **analyst** (or governance / coder / ingestion) in the UI dropdown:

```
POST /api/chat  { target: "analyst", message: "..." }
  → main.py _run_target()
  → dispatch_and_wait("analyst", "chat", {"message": "..."})
      → publishes task_request to agent.analyst.inbox
      → analyst kafka_worker calls run_agent_task("chat", {"message": "..."})
      → run_agent_task builds a prompt and runs the full LLM loop
      → publishes task_response to agent.orchestrator.inbox
  → dispatch_and_wait returns the payload
  → response sent to UI
  fallback: if broker unreachable → analyst_run_agent(message) direct call
```

The `task="chat"` convention tells every agent's `run_agent_task()` to treat `params["message"]` as a free-form user prompt and run its full LLM agent loop.

#### Path 2 — user sends message to the Orchestrator

User selects **orchestrator** in the UI dropdown:

```
POST /api/chat  { target: "orchestrator", message: "..." }
  → main.py _run_target()
  → run_orchestrator_agent_with_trace(message)
      → Orchestrator._plan()  — decomposes into SubTasks
      → Orchestrator._dispatch() → _dispatch_subtask() → _call_agent()
          → dispatch_and_wait("analyst", task, params)
              → publishes task_request to agent.analyst.inbox
              → analyst kafka_worker responds
          → dispatch_and_wait("governance", task, params)
              → publishes task_request to agent.governance.inbox
              → governance kafka_worker responds
      → Orchestrator._synthesize() — merges all responses
  → response sent to UI
```

`_call_agent()` in the orchestrator delegates directly to `dispatch_and_wait()`, keeping the Kafka request-reply logic in one place.

#### Message types

**`task_request`** — caller → specialist agent

```json
{
  "message_id":     "a1b2c3d4-...",
  "correlation_id": "req-xyz",
  "from_agent":     "orchestrator",
  "to_agent":       "analyst",
  "type":           "task_request",
  "reply_topic":    "agent.orchestrator.inbox",
  "payload": {
    "task":    "chat",
    "params":  { "message": "What are the top GDELT themes today?" },
    "context": { "session_id": "abc123" }
  }
}
```

**`task_response`** — specialist agent → caller

```json
{
  "message_id":     "b2c3d4e5-...",
  "correlation_id": "req-xyz",
  "from_agent":     "analyst",
  "to_agent":       "orchestrator",
  "type":           "task_response",
  "payload": {
    "status": "ok",
    "task":   "chat",
    "result": "Top themes in the last 3 hours: ..."
  }
}
```

**`agent_notification`** — specialist agent → Orchestrator (proactive, not in response to a task)

```json
{
  "message_id": "f9e8d7c6-...",
  "from_agent": "coder",
  "to_agent":   "orchestrator",
  "type":       "agent_notification",
  "event_type": "dag_fixed",
  "payload":    { "dag_id": "gdelt_masterfilelist_sync", "patch": "added retry=3" }
}
```

#### Consumer loop (`kafka_worker`)

Each agent's `kafka_worker(agent_name, run_task_fn)` in `a2a_kafka_communication.py` runs a persistent `KafkaConsumer` loop:

1. Receive a `task_request` envelope from `agent.{name}.inbox`.
2. Call `run_task_fn(task, params, context)` — `run_agent_task()` in each agent module.
3. Publish a `task_response` envelope to the `reply_topic` from the request.

Reconnect behaviour:
- `NoBrokersAvailable` → wait 30 s then reconnect
- Any other exception → wait 10 s then reconnect

The loop never exits — agents self-heal if the broker restarts.

#### `send_to_orchestrator()` — proactive agent notifications

Any agent can call `send_to_orchestrator(from_agent, event_type, payload)` at any point during its run to proactively notify the Orchestrator — not just in response to a task. Examples: anomaly detected, DAG fixed, quality test failed. One-shot producer: creates, sends, flushes, closes. Failures are logged and swallowed so a notification failure never crashes the agent.

#### Heartbeat monitoring

The Orchestrator's system prompt instructs it to monitor `agent.heartbeat`. Each agent is expected to publish a heartbeat every 30 seconds. Missing 4 consecutive heartbeats (2 minutes) triggers the agent-offline detection path. This is defined in `KAFKA_CONFIG`:

```python
KAFKA_CONFIG = {
    "heartbeat_interval_s": 30,
    "heartbeat_timeout_s": 120,   # 4 missed beats
}
```

`agent.events` is a system-wide event bus. Agents publish to it when significant state changes occur — new data loaded, schema changes detected, quality alerts raised — so any interested agent can react without direct coupling.

#### Complete Kafka topology

| Topic | Producer | Consumer | Purpose |
|---|---|---|---|
| `agent.analyst.inbox` | `dispatch_and_wait()` | Analyst `kafka_worker` | Task requests to Analyst |
| `agent.governance.inbox` | `dispatch_and_wait()` | Governance `kafka_worker` | Task requests to Governance |
| `agent.coder.inbox` | `dispatch_and_wait()` | Coder `kafka_worker` | Task requests to Coder |
| `agent.ingestion.inbox` | `dispatch_and_wait()` | Ingestion `kafka_worker` | Task requests to Ingestion |
| `agent.orchestrator.inbox` | All `kafka_worker` threads | `dispatch_and_wait()` reply consumer | Task responses + proactive notifications |
| `agent.heartbeat` | All agents (every 30 s) | Orchestrator | Health monitoring |
| `agent.events` | Any agent | Any interested agent | System-wide event bus |
| `airflow-events` | DAG `on_failure_callback` | Ingestion agent | Real-time DAG failure alerts |

---

### Model Configuration

**File:** `agents/model_config.py`

Central registry for all agent models. Edit this file to swap a model without touching any agent code.

```python
AGENT_MODELS = {
    "analyst":      { "model": "deepseek-v4-flash:cloud", "temperature": 0.0 },
    "governance":   { "model": "nemotron-3-super:cloud",  "temperature": 0.0 },
    "ingestion":    { "model": "gemma4:31b-cloud",        "temperature": 0.0 },
    "coder":        { "model": "qwen3-coder-next",        "temperature": 0.0 },
    "orchestrator": { "model": "deepseek-v4-pro:cloud",   "temperature": 0.0 },
}
```

All models with a `:cloud` suffix are served through the **Ollama cloud endpoint** (`https://ollama.com`) and authenticated via `Authorization: Bearer <OLLAMA_API_KEY>`. The exception is `qwen3-coder-next` (Coder agent) — no `:cloud` suffix, meaning it resolves to a locally-running Ollama instance on the Pi. Switching any agent to `openai`, `anthropic`, or `google_genai` only requires changing `model_provider` in its entry — no agent code changes needed.

**`build_model(agent_name)`** — resolves the config, reads the API key from the environment, and calls LangChain's `init_chat_model()`. Raises `KeyError` for unknown agent names.

**`invoke_with_retry(model, messages, max_attempts=4, base_delay=2.0)`** — exponential-backoff wrapper (delays: 2 s, 4 s, 8 s) that retries on 503 / overload / rate-limit responses. All other exceptions are re-raised immediately.

**`serialize_lc_messages(messages)`** — converts a LangChain message list to plain dicts for JSON transport. System message content is truncated to 800 chars to keep trace payloads reasonable.

---

### Shared Agent Infrastructure

#### Knowledge documents

Every agent's system prompt is augmented at startup with reference documentation loaded from `agents/memory/knowledge/`:

| File | Used by |
|---|---|
| `airflow-context7.md` | Coder, Ingestion, Governance |
| `gdelt-manual.md` | Analyst, Coder, Governance |
| `openmetadata-context7.md` | Governance |
| `mongodb-context7.md` | Governance, Analyst |
| `postgressql-context7.md` | Governance, Analyst |

This eliminates LLM calls for catalog and schema discovery — agents start with full context.

#### Airflow API client

The Airflow REST API v1 client is **not a standalone file** — each agent that needs it defines its own `airflow_api()` tool function locally (e.g. `agent_governance.py:999`, `agent_ingestion.py`). Common operations used across agents:

| Operation | HTTP call | Used by |
|---|---|---|
| Fetch task log (last 10 lines) | `GET /api/v1/dags/{id}/dagRuns/{run}/taskInstances/{task}/logs/{n}` | Ingestion, Governance |
| List DAG runs by state | `GET /api/v1/dags/{id}/dagRuns?state=failed` | Ingestion |
| Trigger new DAG run | `POST /api/v1/dags/{id}/dagRuns` | Ingestion |
| List all DAGs | `GET /api/v1/dags` | Governance |

All Airflow API calls use HTTP Basic Auth with the `AIRFLOW_USER` / `AIRFLOW_PASSWORD` environment variables.

#### Catalog manifest

`agents/memory/catalog_manifest.json` is a full snapshot of all known assets — OpenMetadata services and tables, PostgreSQL schemas and columns with row counts, MongoDB collections with field samples. It is written every 30 minutes by the `catalog_manifest_refresh` Airflow DAG and injected into Governance and Analyst agent sessions. This means agents never need to spend LLM calls on "what tables exist?" discovery.

#### Persistent memory files

| File | Owner | Content |
|---|---|---|
| `memory/governance_memory.json` | Governance | Asset classifications, lineage edges, incidents |
| `memory/ingestion_memory.json` | Ingestion | Set of already-handled `dag_run_id` values |
| `memory/agent_memory.json` | All agents | Shared cross-agent memory (optional) |

---

## Airflow DAGs

| DAG | Schedule | Trigger | Description |
|---|---|---|---|
| `gdelt_masterfilelist_sync` | Every 15 min | Time | Downloads the GDELT v2 master file list from `data.gdeltproject.org` in 1 MB streaming chunks, up to 10 retries with resumption from a `.tmp` file |
| `gdelt_masterfilelist_to_postgres` | Dataset-triggered | `file://masterfilelist.txt` | Parses the master file list and loads new GDELT event records into PostgreSQL `stack_db` |
| `gdelt_masterfilelist_validate` | Dataset-triggered | upstream DAG | Validates loaded records: row counts, null checks, schema assertions |
| `gkd_hourly_sync` | Hourly | Time | Downloads GKG `.zip` files from GDELT (URLs sourced from PostgreSQL), parses 27-column TSV, and loads records into MongoDB `gkd_db` via atomic staging rename |
| `catalog_manifest_refresh` | Every 30 min | Time | Pulls the full asset catalog from OpenMetadata + PostgreSQL + MongoDB in parallel (using `ThreadPoolExecutor`) and writes `catalog_manifest.json`; three catalog sources: OpenMetadata REST API, PostgreSQL `information_schema`, MongoDB collection stats |
| `kafka_callbacks` | — | — | Shared `on_failure_callback` used by all DAGs to publish failure events to the `airflow-events` Kafka topic; imported as a module, not a standalone DAG |
| UUID-named DAGs | Various | Various | Dynamically generated DAGs created by the Coder agent; JSON configs stored in `dag_generated_configs/` |

**Dataset-based scheduling** — `gdelt_masterfilelist_sync` declares `gdelt_masterfile = Dataset("file://masterfilelist.txt")` as an outlet. Downstream DAGs declare it as an inlet and are triggered automatically when the sync completes successfully. This replaces fragile time-based chaining.

**Lineage backend** — Airflow is globally configured to publish lineage edges to OpenMetadata on every task completion, so the catalog always reflects the current pipeline topology without any manual annotation.

---

## Data Sources

### GDELT v2 (Global Database of Events, Language, and Tone)

Open global event dataset updated every 15 minutes by the GDELT Project.

- **Master file list** (`masterfilelist.txt`) — index of all published GDELT export files (CSV + ZIP). Downloaded every 15 min and diffed to find new files.
- **GKG (Global Knowledge Graph)** — enriched event records with:
  - `V2THEMES` — GDELT ontology themes (e.g. `TAX_FNCACT_PRESIDENT`, `CRISISLEX_CRISISLEXREC`)
  - `V2PERSONS` — named persons with offsets
  - `V2ORGANIZATIONS` — named organisations
  - `V2LOCATIONS` — geolocated places
  - `TONE` — six tone scores: tone, positive score, negative score, polarity, activity reference density, self/group reference density
  - `COUNTS` — numeric amounts extracted from text
  - `QUOTATIONS` — direct quotes from source articles
  - `GCAM` — Google Content Analysis Metadata (100+ emotion/sentiment dimensions)
  - `AMOUNTS` — numeric values with context strings

Data is downloaded in streaming 1 MB chunks to handle large files on the Pi's limited RAM.

#### GDELT domain knowledge baked into agents

The Orchestrator and Analyst system prompts include the following domain reference so agents can translate raw GDELT identifiers into human-readable answers without LLM hallucination:

**CAMEO event codes** (most common):

| Code | Meaning | Code | Meaning |
|---|---|---|---|
| 01 | Make public statement | 10 | Demand |
| 02 | Appeal | 11 | Disapprove |
| 03 | Express intent to cooperate | 12 | Reject |
| 04 | Consult | 13 | Threaten |
| 05 | Diplomatic cooperation | 14 | Protest |
| 06 | Material cooperation | 15 | Exhibit force posture |
| 07 | Provide aid | 17 | Coerce |
| 08 | Yield | 18 | Assault |
| 09 | Investigate | 19 | Fight |
| 20 | Use unconventional mass violence | | |

**Goldstein scale**: −10 (most conflictual, e.g. military attack) to +10 (most cooperative, e.g. major agreement). Examples: −5 = threaten, 0 = neutral, +5 = diplomatic cooperation.

**Country codes**: GDELT uses **FIPS 10-4**, not ISO 3166. Notable differences: Turkey = `TU` (not `TR`), Germany = `GM` (not `DE`), Japan = `JA` (not `JP`), Switzerland = `SZ` (not `CH`). Agents translate user-provided country names to FIPS before querying.

**QuadClass**: 1 = verbal cooperation, 2 = material cooperation, 3 = verbal conflict, 4 = material conflict.

**Polystore mapping**:

| Store | Data | Query type |
|---|---|---|
| PostgreSQL | Events, Mentions tables | Structured queries, time-series |
| MongoDB | GKG documents, GCAM arrays, theme lists | Semi-structured, aggregations |
| Neo4j | Entity relationship graphs (person↔org↔location↔event) | Graph traversal |
| Elasticsearch | Themes, persons, organisations | Full-text search |

> Neo4j and Elasticsearch are referenced in the Orchestrator system prompt as part of the intended polystore. Neo4j is not currently running in the Docker Compose stack but is designed for future graph analytics.

### GKG data in MongoDB (`gkd_db`)

"GKD" in the codebase (DAG id `gkd_daily_sync`, collection `last_24hours_gkd`) refers to **GDELT GKG Data** — it is not a separate data source. The `gkd_daily_sync` DAG reads GKG file URLs from PostgreSQL (populated by `gdelt_masterfilelist_to_postgres`), downloads each `.zip` from GDELT, parses the 27-column TSV, and streams records to MongoDB in batches of 500.

An atomic staging rename (`last_24hours_gkd_staging` → `last_24hours_gkd`) ensures the live collection is never partially updated — any crash leaves the previous run's data intact.

- `last_24hours_gkd` — live collection, rolling 24-hour window of GKG records
- `last_24hours_gkd_staging` — transient, dropped and rebuilt on each run

**Kafka is not part of this data pipeline.** See below for how Kafka is actually used.

### How Kafka is used

Kafka has two roles in this project — neither involves ingesting external data:

**1. DAG failure alerts (`airflow-events` topic)**

Every DAG registers `on_failure_callback` from `dags/kafka_callbacks.py`. When any task fails, the callback publishes a JSON event to Kafka within 5 seconds:

```json
{
  "dag_id": "gdelt_masterfilelist_sync",
  "dag_run_id": "scheduled__2026-05-23T00:00:00+00:00",
  "task_id": "download_masterfilelist",
  "try_number": 2,
  "state": "failed",
  "execution_date": "2026-05-23 00:00:00+00:00"
}
```

The Ingestion agent's `KafkaConsumer` thread receives this in real time and triggers autonomous recovery (read log → classify error → retry or patch DAG). If Kafka is unavailable the callback logs a warning and does nothing — Airflow's own failure handling is never affected.

**2. Agent-to-agent messaging (`agent.*.inbox` topics)**

The Orchestrator dispatches tasks to specialist agents and receives results back via Kafka, so agents can run in separate processes or containers:

| Topic | Direction |
|---|---|
| `agent.analyst.inbox` | Orchestrator → Analyst |
| `agent.governance.inbox` | Orchestrator → Governance |
| `agent.ingestion.inbox` | Orchestrator → Ingestion |
| `agent.coder.inbox` | Orchestrator → Coder |
| `agent.orchestrator.inbox` | Any agent → Orchestrator (results + proactive notifications) |

---

## Network & Connectivity

All services are deployed on a **Raspberry Pi** accessed over **Tailscale VPN**.

`apps/ui_app/access_hosts.py` is the single source of truth for all service URLs. Switching between local development and the remote Pi:

```python
ACCESS_MODE = "tailscale"  # "local" | "tailscale"
```

On import, `access_hosts.py` automatically writes the active URLs back into `apps/ui_app/.env` via `python-dotenv`'s `set_key`, so all tools that read `.env` directly (Airflow container, shell scripts) always point at the same hosts as the Python code.

#### Kafka listener configuration

Kafka is configured with two listeners:

| Listener | Address | Used by |
|---|---|---|
| `INTERNAL` | `kafka:9092` | Services inside Docker Compose network |
| `EXTERNAL` | `100.95.246.75:29092` | Agents running outside Docker (development mode) |

#### SSH key setup (one-time)

The Coder agent writes DAG files to the remote Pi via SCP over SSH. Set up passwordless SSH access once:

```bash
python apps/ui_app/access_hosts.py
```

This runs `ssh-copy-id` to install your public key on the Pi. Prefers `id_ed25519` over `id_rsa`.

---

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Tailscale (if deploying to a remote Pi)
- An Ollama account with API key (for cloud model access)
- Python 3.13 + uv (for local development without Docker)

### 1. Configure environment variables

**Root `.env`** — used by Airflow and Compose services:

```bash
DB_USER=stack_user
DB_PASSWORD=stack_password
MONGO_USER=admin
MONGO_PASSWORD=yourpassword
AIRFLOW_ADMIN_USER=admin
AIRFLOW_ADMIN_PASSWORD=admin
AIRFLOW__CORE__FERNET_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
```

**`apps/ui_app/.env`** — used by the multi-agent UI container:

```bash
OLLAMA_API_KEY=<your-ollama-api-key>
OPENMETADATA_HOST=http://<host>:8585
OPENMETADATA_TOKEN=<openmetadata-ingestion-bot-jwt>
POSTGRES_DSN=postgresql://stack_user:stack_password@<host>:5432/airflow_db
AIRFLOW_API_URL=http://<host>:8080
AIRFLOW_USER=admin
AIRFLOW_PASSWORD=admin
AIRFLOW_DAGS_PATH=/home/alexpi/goverflow/dags
MONGO_URI=mongodb://admin:yourpassword@<host>:27017
```

To obtain the `OPENMETADATA_TOKEN`: OpenMetadata UI → Settings → Bots → Ingestion Bot → copy JWT token.

### 2. Create `stack_db` (one-time)

`init-db.sql` only creates `openmetadata_db` and `airflow_db`. The GDELT events database must be created manually:

```bash
docker compose exec postgres psql -U stack_user -c "CREATE DATABASE stack_db;"
```

### 3. Start the stack

```bash
# First run: airflow-init migrates the DB and creates the admin user before
# the webserver and scheduler start (depends on service_completed_successfully)
docker compose up -d
```

Check all services are healthy:

```bash
docker compose ps
```

On first boot Elasticsearch takes ~60 s to become ready; OpenMetadata waits for it automatically.

### 4. Access the interfaces

| Interface | URL |
|---|---|
| Multi-Agent Chat | `http://<host>:8010` |
| Airflow | `http://<host>:8080` |
| OpenMetadata | `http://<host>:8585` |

### 5. Development — UI app without Docker

```bash
# Switch to local mode so agents hit localhost services
# Edit apps/ui_app/access_hosts.py: ACCESS_MODE = "local"

source .venv/bin/activate
cd apps/ui_app
uvicorn main:app --host 0.0.0.0 --port 8010 --reload
```

The `--reload` flag is powered by `watchfiles` (listed in `requirements.txt`) — file changes trigger a hot reload without restarting the server.

### 6. VS Code

The workspace is pre-configured in `.vscode/settings.json`:

```json
{
  "python.defaultInterpreterPath": "/home/alexpi/goverflow/.venv/bin/python",
  "python.analysis.extraPaths": ["apps/ui_app"]
}
```

The `.venv` was created with `uv` using Python 3.13 (from Anaconda). The `apps/ui_app` extra path ensures imports like `from agents.agent_analyst import …` resolve correctly in the IDE without installing the package.

---

## Project Layout

```
goverflow/
├── apps/
│   └── ui_app/                        # Multi-agent FastAPI app
│       ├── agents/
│       │   ├── agent_analyst.py            # GDELT GKG analytics (Postgres + MongoDB)
│       │   ├── agent_coder.py              # Autonomous file-editing + DAG patching
│       │   ├── agent_governance.py         # Data governance + OpenMetadata integration
│       │   ├── agent_ingestion.py          # Airflow failure watchdog (Kafka + polling)
│       │   ├── agent_orchestrator.py       # Master coordinator (state machine)
│       │   ├── a2a_kafka_communication.py  # Inter-agent Kafka messaging
│       │   ├── model_config.py             # Central LLM registry (all agent models)
│       │   └── memory/
│       │       ├── knowledge/              # Reference docs injected into system prompts
│       │       │   ├── airflow-context7.md
│       │       │   ├── gdelt-manual.md
│       │       │   ├── mongodb-context7.md
│       │       │   ├── openmetadata-context7.md
│       │       │   └── postgressql-context7.md
│       │       ├── private/                # Orchestrator-only memory
│       │       │   ├── conversations/      # Per-session chat history + index.json
│       │       │   ├── strategies/         # decomposition_cache.json
│       │       │   ├── agents/             # capability_registry.json
│       │       │   └── user/               # user_context.json
│       │       ├── shared/                 # All-agent shared memory (fcntl-locked)
│       │       │   ├── schema_registry.json
│       │       │   ├── data_freshness.json
│       │       │   ├── quality_alerts.json
│       │       │   └── result_cache/       # {query_hash}.json per cached query
│       │       ├── catalog_manifest.json   # Live catalog snapshot (30-min Airflow refresh)
│       │       ├── governance_memory.json  # Classifications, lineage edges, incidents
│       │       └── ingestion_memory.json   # Handled dag_run_ids (dedup store)
│       ├── access_hosts.py            # Single source of truth for all service URLs
│       ├── airflow_api.py             # Airflow REST API v1 client helpers
│       ├── main.py                    # FastAPI entrypoint — endpoints + chat UI HTML
│       ├── dag_staging/               # Temp dir for DAG content before SCP to Pi
│       ├── Dockerfile                 # python:3.11-slim + requirements + uvicorn
│       └── requirements.txt           # Python dependencies
│
├── dags/                              # Airflow DAGs (bind-mounted into all Airflow containers)
│   ├── catalog_manifest_refresh.py        # 30-min catalog snapshot DAG
│   ├── gdelt_masterfilelist_sync.py       # 15-min GDELT master file download
│   ├── gdelt_masterfilelist_to_postgres.py # Dataset-triggered: parse + load
│   ├── gdelt_masterfilelist_validate.py    # Dataset-triggered: quality checks
│   ├── gkd_hourly_sync.py                 # Hourly GKD Kafka → MongoDB
│   ├── kafka_callbacks.py                 # Shared on_failure_callback → Kafka
│   ├── data/raw/                          # Downloaded GDELT master file list
│   └── <uuid>.py                          # Dynamically generated DAGs (Coder agent)
│
├── dag_generated_configs/             # JSON configs for Coder-generated DAGs
├── logs/airflow/                      # Airflow scheduler + task logs (bind-mounted)
├── docker-compose.yml                 # Full stack definition
├── Dockerfile.airflow                 # Custom Airflow image with OpenMetadata provider
├── init-db.sql                        # PostgreSQL init: creates airflow_db + openmetadata_db (stack_db created manually)
├── ty.toml                            # ty (Python type checker) configuration
└── .venv/                             # Project venv (Python 3.13, created with uv)
```
# goverflow
