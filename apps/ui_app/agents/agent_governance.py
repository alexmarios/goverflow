"""
Data Governance Agent
---------------------
Enforces data quality, maintains metadata, classifies assets by risk and
sensitivity, traces data lineage across the pipeline, and advises the team
on data standards and governance policies.

Full tech stack
~~~~~~~~~~~~~~~
- LangChain ``init_chat_model`` — instantiates the LLM (Qwen 3.5 via Ollama)
  and ``@tool`` — decorates plain Python functions so LangChain can bind them
  to the model's tool-call interface (JSON-Schema introspection + dispatch).

- OpenMetadata REST API — open-source metadata catalog used as the system of
  record for table/column metadata, data classifications, data quality tests,
  lineage graphs, and governance incidents.  Every call is authenticated with
  an HTTP ``Authorization: Bearer <JWT>`` header whose value comes from the
  ``OPENMETADATA_TOKEN`` environment variable.

- Airflow REST API — Apache Airflow exposes a stable REST API
  (``/api/v1/dags``, ``/api/v1/datasets``, ``/api/v1/dagRuns``, etc.) that
  the governance agent uses in read-only mode to inspect DAG metadata and
  task-run history.  Authentication is HTTP Basic (username/password).

- psycopg2 — mature CPython adapter for PostgreSQL.  Used here to open
  short-lived, read-only connections for schema introspection
  (``information_schema``) and data profiling.

- pymongo — official Python driver for MongoDB.  Used to inspect collections,
  sample documents, and run read-only aggregation pipelines without issuing
  any write commands.

- Python ``ast`` module — part of the standard library.  Parses Python source
  code into an Abstract Syntax Tree (AST) so the agent can extract DAG
  structure (IDs, tasks, operators, Dataset URIs, dependency edges) without
  ever importing or executing the DAG file, avoiding Airflow side effects.

- JSON file memory (``memory/governance_memory.json``) — a lightweight
  persistence layer that survives process restarts.  Stores three governance
  artefacts: asset classifications, lineage edges, and incidents.

Connects to: OpenMetadata, PostgreSQL (read-only), MongoDB (read-only),
             Airflow REST API, Airflow DAG files.
Local docs:  memory/knowledge/gdelt-manual.md, memory/knowledge/openmetadata-context7.md,
             memory/knowledge/mongodb-context7.md, memory/knowledge/postgressql-context7.md.
"""

import ast
import datetime
import glob
import json
import os
import time
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

import requests
from dotenv import load_dotenv
from langchain.messages import HumanMessage, SystemMessage, ToolMessage
from langchain.tools import tool
from langchain_core.messages import BaseMessage

# psycopg2 and pymongo are imported at module level (not inside the tool
# functions) because a linter / import-checker in the project enforces that
# all third-party imports appear at the top of the file rather than inside
# function bodies.  Previously they were lazy imports inside the tool
# functions; moving them here makes the dependency requirements explicit and
# ensures any missing-package errors surface at startup, not at call time.
import psycopg2
import psycopg2.extras
import pymongo

# Load .env file so all os.getenv() calls below can resolve environment
# variables even when the agent is launched directly (not via a shell that
# already has them set).
load_dotenv()

try:
    from agents.model_config import build_model, serialize_lc_messages
except ModuleNotFoundError:
    from model_config import build_model, serialize_lc_messages

LAST_RUN_MESSAGES: list = []

# ── Config ─────────────────────────────────────────────────────────────────────
#
# Each variable is read from the environment with a safe default that points
# to the local Docker Compose stack used in development.
#
# OPENMETADATA_HOST  — base URL of the OpenMetadata server.  OpenMetadata is
#   an open-source metadata management and data discovery platform.  All REST
#   calls are rooted here (e.g. http://localhost:8585/api/v1/tables).
#
# OPENMETADATA_TOKEN — a long-lived JWT (JSON Web Token) issued by OpenMetadata
#   under Settings → Bots → Ingestion Bot.  It is placed in every request's
#   ``Authorization: Bearer <token>`` header.
#
# POSTGRES_DSN — libpq-style connection string in the format
#   ``postgresql://<user>:<password>@<host>:<port>/<database>``.
#   psycopg2 parses this natively so no individual host/user/port variables
#   are needed.
#
# MONGO_URI — MongoDB connection URI (``mongodb://<host>:<port>``).  MongoDB
#   stores processed GDELT events, GKG records, and enriched graph adjacency
#   documents.  The governance agent inspects it (read-only) to profile
#   collections, detect schema drift, and register lineage.
#
# AIRFLOW_DAGS_PATH — filesystem path to the Airflow DAGs directory.  The
#   governance agent reads ``.py`` files from this path and analyses them with
#   the Python ``ast`` module to extract task dependency graphs and Dataset
#   URIs for lineage tracking — without executing any DAG code.
#
# AIRFLOW_API_URL / AIRFLOW_USER / AIRFLOW_PASSWORD — Airflow's REST API
#   endpoint and Basic-auth credentials.  The governance agent queries these
#   for DAG metadata and run history.
#
# QUERY_LOG_PATH — optional path to a query log file.  If set, could be used
#   for lineage inference from observed SQL queries (not yet implemented).

from access_hosts import AIRFLOW_URL as _AF_URL, OPENMETADATA_URL as _OM_URL, POSTGRES_DSN as _PG_DSN, MONGO_URI as _MG_URI, DAGS_DIR as _DAGS_DIR, REMOTE_USER as _REMOTE_USER, REMOTE_HOST as _REMOTE_HOST

OPENMETADATA_HOST  = os.getenv("OPENMETADATA_HOST", _OM_URL)
OPENMETADATA_TOKEN = os.getenv("OPENMETADATA_TOKEN", "")
POSTGRES_DSN       = os.getenv("POSTGRES_DSN", _PG_DSN)
MONGO_URI          = os.getenv("MONGO_URI", _MG_URI)
AIRFLOW_DAGS_PATH  = os.getenv("AIRFLOW_DAGS_PATH", _DAGS_DIR)
AIRFLOW_API_URL    = os.getenv("AIRFLOW_API_URL", _AF_URL)
AIRFLOW_USER       = os.getenv("AIRFLOW_USER", "admin")
AIRFLOW_PASSWORD   = os.getenv("AIRFLOW_PASSWORD", "admin")
QUERY_LOG_PATH     = os.getenv("QUERY_LOG_PATH", "")

# Path to the JSON file that persists governance state between process restarts.
# Placed inside the ``agents/memory/`` subdirectory alongside the agent module.
MEMORY_PATH = os.path.join(os.path.dirname(__file__), "memory", "governance_memory.json")

# Catalog manifest written by the catalog_manifest_refresh Airflow DAG every 30 min.
# The DAG runs in the Airflow container and writes to /opt/airflow/dags/catalog_manifest.json
# which maps to the same host directory as AIRFLOW_DAGS_PATH in this container.
CATALOG_MANIFEST_PATH = os.path.join(os.path.dirname(__file__), "memory", "catalog_manifest.json")

# ── Authentication helpers ──────────────────────────────────────────────────────
#
# The two systems this agent writes to use different authentication schemes:
#
# _OM_HEADERS (dict) — OpenMetadata uses stateless Bearer JWT authentication.
#   Every HTTP request carries a full ``Authorization: Bearer <token>`` header.
#   The Content-Type is ``application/json`` for most methods, but PATCH
#   requires ``application/json-patch+json`` (see _om_request for details).
#
# _AF_AUTH (tuple) — Airflow uses HTTP Basic authentication.  The requests
#   library accepts ``auth=(username, password)`` and encodes it as
#   ``Authorization: Basic base64(<user>:<password>)`` automatically.  A
#   plain tuple is used rather than a dict because that is the requests API
#   convention for Basic auth.

_OM_HEADERS = {
    "Authorization": f"Bearer {OPENMETADATA_TOKEN}",
    "Content-Type": "application/json",
}
_AF_AUTH = (AIRFLOW_USER, AIRFLOW_PASSWORD)

# _CONTEXT_WINDOW — maximum number of messages (excluding the system prompt)
# kept in the active conversation history before the oldest messages are
# silently dropped.  LLMs have a finite context window (token budget), and a
# long governance session can accumulate hundreds of turns.  Keeping only the
# most recent 100 messages prevents context-overflow errors and keeps inference
# costs predictable.  The system prompt is always preserved as messages[0]
# regardless of this limit.
_CONTEXT_WINDOW = 100

# Warn early if the token is absent so the operator sees the error before the
# first API call returns HTTP 401.
if not OPENMETADATA_TOKEN:
    warnings.warn("OPENMETADATA_TOKEN is not set — all OpenMetadata API calls will return HTTP 401.")


# ── Memory ─────────────────────────────────────────────────────────────────────
#
# The memory file contains three keys:
#
#   "classifications" (dict[fqn → {level, timestamp}]) — maps a fully-qualified
#     asset name (e.g. "local_postgres.public.gdelt_events.actor1Name") to its
#     assigned risk/sensitivity level (L0 Public / L1 Internal / L2 Sensitive /
#     L3 PII) and the date it was classified.  Allows the agent to skip
#     re-classifying assets that were already reviewed in a previous session.
#
#   "lineage_edges" (list[{from, to, source, timestamp}]) — each element
#     records one directed data-flow relationship registered in OpenMetadata's
#     lineage graph.  Lets the agent avoid creating duplicate edges across
#     sessions.
#
#   "incidents" (list[{asset, finding, timestamp}]) — append-only log of every
#     write action the agent has made to OpenMetadata (tag updates, quality
#     test creations, description changes, etc.).  Provides an audit trail and
#     is surfaced in the system prompt so the agent can refer to past decisions.

def load_memory() -> dict:
    """Restore prior governance state from disk; return an empty slate on first run."""
    _empty = {"classifications": {}, "lineage_edges": [], "incidents": []}
    try:
        with open(MEMORY_PATH) as f:
            return json.load(f)
    except FileNotFoundError:
        return _empty
    except json.JSONDecodeError as e:
        print(f"[governance] memory file corrupt (resetting): {e}")
        return _empty


def save_memory(mem: dict) -> None:
    """Persist the in-memory governance state to disk atomically (overwrite)."""
    # Create the ``memory/`` subdirectory on first run if it does not yet exist.
    os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)
    with open(MEMORY_PATH, "w") as f:
        json.dump(mem, f, indent=2)


def _memory_summary(mem: dict) -> str:
    """
    Build a compact text block summarising prior governance actions.

    This string is injected into the system prompt at the start of each session
    (see ``run_governance_session``), giving the model persistent memory across
    process restarts.  Without this injection, the model would have no knowledge
    of assets it classified or incidents it opened in previous sessions, because
    LLMs are stateless between invocations.

    The summaries are intentionally capped to avoid bloating the context window:
    - At most 10 classified assets are shown (the most recently added).
    - At most 5 incidents are shown (the most recent by list position).
    """
    parts = []
    if mem["classifications"]:
        # Cap at 10 to keep the prompt size bounded
        parts.append(
            f"Previously classified assets ({len(mem['classifications'])}):\n" +
            "\n".join(f"  {fqn}: {v['level']}" for fqn, v in list(mem["classifications"].items())[-10:])
        )
    if mem["lineage_edges"]:
        parts.append(f"Lineage edges registered: {len(mem['lineage_edges'])}")
    if mem["incidents"]:
        # Cap at 5 most recent incidents to avoid bloating the context window
        parts.append(
            f"Prior incidents ({len(mem['incidents'])}):\n" +
            "\n".join(f"  [{i['timestamp'][:10]}] {i['asset']}: {i['finding'][:80]}"
                      for i in mem["incidents"][-5:])
        )
    return "\n\n".join(parts) if parts else "No prior governance actions recorded."


# ── Internal helpers ───────────────────────────────────────────────────────────

# Paths that returned HTTP 404 in this process run — never retry them.
# Only GET paths are cached (write methods shouldn't be skipped on future turns).
_OM_404_CACHE: set[str] = set()

# ── OpenMetadata API reference ─────────────────────────────────────────────────
# Loaded once at module startup from the companion documentation file.
# Only the REST API section is kept (Python SDK and CLI sections are omitted —
# the agent uses raw HTTP via _om_request, not the SDK).
# Injected as a SystemMessage so the agent has concrete endpoint paths,
# request body formats, and response shapes without making any network calls.

_OM_API_DOCS_PATH = os.path.join(os.path.dirname(__file__), "memory", "knowledge", "openmetadata-context7.md")
_OM_API_DOCS: str = ""

try:
    with open(_OM_API_DOCS_PATH) as _f:
        _raw_docs = _f.read()
    # Keep only the REST API section; stop before the Python SDK section
    # to avoid injecting irrelevant SDK/CLI content into the context window.
    _sdk_marker = "## Python SDK"
    _cut = _raw_docs.find(_sdk_marker)
    _OM_API_DOCS = (_raw_docs[:_cut].strip() if _cut != -1 else _raw_docs).strip()
    del _raw_docs, _cut, _sdk_marker
except FileNotFoundError as e:
    print(f"[governance] knowledge doc not found: {e}")

# GDELT GKG codebook — loaded from the local markdown copy so the agent has
# authoritative field semantics without making any external network calls.
_GDELT_DOCS_PATH = os.path.join(os.path.dirname(__file__), "memory", "knowledge", "gdelt-manual.md")
_GDELT_DOCS: str = ""
try:
    with open(_GDELT_DOCS_PATH) as _f:
        _GDELT_DOCS = _f.read().strip()
except FileNotFoundError as e:
    print(f"[governance] knowledge doc not found: {e}")

# MongoDB and PostgreSQL reference docs — injected so the agent can construct
# correct queries without trial-and-error against live databases.
_MONGO_DOCS_PATH = os.path.join(os.path.dirname(__file__), "memory", "knowledge", "mongodb-context7.md")
_MONGO_DOCS: str = ""
try:
    with open(_MONGO_DOCS_PATH) as _f:
        _MONGO_DOCS = _f.read().strip()
except FileNotFoundError as e:
    print(f"[governance] knowledge doc not found: {e}")

_PG_DOCS_PATH = os.path.join(os.path.dirname(__file__), "memory", "knowledge", "postgressql-context7.md")
_PG_DOCS: str = ""
try:
    with open(_PG_DOCS_PATH) as _f:
        _PG_DOCS = _f.read().strip()
except FileNotFoundError as e:
    print(f"[governance] knowledge doc not found: {e}")

# ── Live catalog context ───────────────────────────────────────────────────────
# Cached once per process: which PostgreSQL database postgres_query is connected
# to, which databases are registered in OpenMetadata, and which database services
# are available.  Injected as a SystemMessage at the start of every agent run so
# the model never has to guess database names or service FQNs.

_CATALOG_CONTEXT: str | None = None


def _get_catalog_context() -> str:
    """
    Query the live environment once per process to build catalog context.

    Calls:
      - SELECT current_database() via psycopg2 — finds the connected PG database.
      - GET /api/v1/databases       — lists databases registered in OpenMetadata.
      - GET /api/v1/services/databaseServices — lists database service FQNs.

    The result is cached at module level (_CATALOG_CONTEXT) so subsequent
    run_agent() calls within the same process pay zero network overhead.
    On any failure the function still returns a partial result so the agent
    can operate with whatever information is available.
    """
    global _CATALOG_CONTEXT
    if _CATALOG_CONTEXT is not None:
        return _CATALOG_CONTEXT

    parts: list[str] = []

    # 1. Find the connected PostgreSQL database name
    try:
        conn = psycopg2.connect(POSTGRES_DSN)
        conn.set_session(readonly=True, autocommit=True)
        with conn.cursor() as cur:
            cur.execute("SELECT current_database()")
            pg_db = cur.fetchone()[0]
        conn.close()
        parts.append(f"postgres_query is connected to PostgreSQL database: **{pg_db}**")
        parts.append(
            f"Use postgres_query ONLY for queries inside **{pg_db}** "
            "(information_schema, pg_catalog, and tables in this database)."
        )
    except Exception as e:
        parts.append(f"postgres_query connection info unavailable: {e}")

    # 2. Enumerate databases registered in OpenMetadata
    try:
        om_resp = _om_request("GET", "/api/v1/databases", params={"limit": 50})
        dbs = om_resp.get("data", [])
        if dbs:
            db_lines = [
                f"  - {d.get('fullyQualifiedName', d.get('name', '?'))} "
                f"(service: {d.get('service', {}).get('fullyQualifiedName', '?')})"
                for d in dbs
            ]
            parts.append("Databases registered in OpenMetadata:\n" + "\n".join(db_lines))
        else:
            parts.append("OpenMetadata returned no registered databases (catalog may be empty).")
    except Exception as e:
        parts.append(f"OpenMetadata database list unavailable: {e}")

    # 3. Enumerate database services in OpenMetadata
    try:
        svc_resp = _om_request("GET", "/api/v1/services/databaseServices", params={"limit": 50})
        svcs = svc_resp.get("data", [])
        if svcs:
            svc_lines = [
                f"  - {s.get('fullyQualifiedName', s.get('name', '?'))} "
                f"[{s.get('serviceType', '?')}]"
                for s in svcs
            ]
            parts.append("Database services in OpenMetadata:\n" + "\n".join(svc_lines))
    except Exception as e:
        parts.append(f"OpenMetadata service list unavailable: {e}")

    _CATALOG_CONTEXT = "\n\n".join(parts)
    return _CATALOG_CONTEXT


def _om_request(method: str, path: str, params: Optional[dict] = None, body: Optional[dict | list] = None) -> dict:
    """
    Send an authenticated HTTP request to the OpenMetadata REST API.

    PATCH and RFC 6902 JSON Patch
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    OpenMetadata's PATCH endpoints follow RFC 6902 (JSON Patch), which is a
    different wire format than a standard JSON body.  A JSON Patch payload is a
    *list* of operation objects, e.g.:
        [{"op": "replace", "path": "/description", "value": "New description"}]
    The standard JSON media type ``application/json`` is not accepted by these
    endpoints — the server expects ``application/json-patch+json``.  This
    function detects PATCH requests and swaps the Content-Type header
    accordingly; all other methods keep the default ``application/json``.

    Error handling
    ~~~~~~~~~~~~~~
    - HTTP errors are returned as ``{"error": ..., "detail": ...}`` dicts so the
      LLM receives a structured error it can reason about and report to the user.
    - Some OM endpoints return 204 No Content (empty body) or malformed HTML
      error pages; the ``try/except`` around ``resp.json()`` handles those by
      returning the raw text truncated to 2 000 characters.
    """
    url = f"{OPENMETADATA_HOST}{path}"
    m = method.upper()
    # Skip GET calls to endpoints confirmed as 404 in this process run
    if m == "GET" and path in _OM_404_CACHE:
        return {"error": "HTTP 404", "detail": "endpoint not available in this OpenMetadata installation (cached)"}
    # PATCH sends a JSON Patch list (RFC 6902) which requires a different Content-Type than regular JSON
    headers = dict(_OM_HEADERS)
    if m == "PATCH":
        headers["Content-Type"] = "application/json-patch+json"
    resp = requests.request(m, url, headers=headers, params=params, json=body, timeout=30)
    if not resp.ok:
        if m == "GET" and resp.status_code == 404:
            _OM_404_CACHE.add(path)
            print(f"[governance] 404 cached for GET {path} — will skip on future calls")
        return {"error": f"HTTP {resp.status_code}", "detail": resp.text[:500]}
    # Some OM endpoints return 204 No Content or HTML error pages that cannot be parsed as JSON
    try:
        return resp.json()
    except Exception as e:
        print(f"[governance] failed to parse response as JSON: {e}")
        return {"text": resp.text[:2000]}


def _af_request(method: str, path: str, params: Optional[dict] = None, body: Optional[dict] = None) -> dict:
    """
    Send an authenticated HTTP request to the Airflow REST API.

    This mirrors ``_om_request`` in structure but uses HTTP Basic authentication
    (the ``_AF_AUTH`` tuple) instead of the Bearer JWT used by OpenMetadata.
    Airflow does not require a special Content-Type for any of its endpoints, so
    the default ``application/json`` (set automatically by requests when
    ``json=body`` is passed) is always correct.

    Error handling follows the same pattern as ``_om_request``: HTTP errors
    become structured dicts and non-JSON responses are returned as ``{"text":
    ...}`` to keep the agent's tool result parsing uniform.
    """
    # Airflow uses HTTP Basic auth (admin/admin), not the Bearer JWT used by OpenMetadata
    url = f"{AIRFLOW_API_URL}{path}"
    resp = requests.request(method.upper(), url, auth=_AF_AUTH, params=params, json=body, timeout=30)
    if not resp.ok:
        return {"error": f"HTTP {resp.status_code}", "detail": resp.text[:500]}
    try:
        return resp.json()
    except Exception as e:
        print(f"[governance] failed to parse response as JSON: {e}")
        return {"text": resp.text[:2000]}


def _parse_dag_ast(source: str, filename: str) -> str:
    """
    Statically analyse a DAG Python source file and return structured lineage
    and dependency information as a JSON string.

    Why AST analysis instead of importing the module?
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Airflow DAG files execute code at module scope (the DAG object is created,
    tasks are instantiated, and the task graph is wired up as the module is
    imported).  Importing a DAG file in this agent process would trigger all of
    those side effects — potentially connecting to databases, calling external
    APIs, or scheduling runs.  Python's built-in ``ast`` module parses source
    code into an Abstract Syntax Tree *without* executing any of it, making the
    analysis completely safe.

    How ``ast.walk`` works
    ~~~~~~~~~~~~~~~~~~~~~~
    ``ast.walk(tree)`` performs a depth-first traversal of every node in the
    AST, yielding each one.  This lets a single loop inspect all function calls,
    binary operators, and expressions in the file regardless of how deeply
    nested they are in conditionals, loops, or function definitions.

    What is extracted
    ~~~~~~~~~~~~~~~~~
    - DAG IDs and schedule intervals — from ``DAG(dag_id=..., schedule=...)``
      constructor calls.
    - Task IDs and operator types — from any ``*Operator(task_id=...)``
      constructor call (PythonOperator, BashOperator, PostgresOperator, etc.).
    - Dataset URIs — from ``Dataset(uri=...)`` constructor calls introduced in
      Airflow 2.4's dataset-aware scheduling feature.
    - Dependency edges — from ``>>`` expressions (Python's right-shift operator
      used by Airflow to express task dependency, e.g. ``extract >> transform``).
      ``ast.unparse`` converts both sides back to readable strings.

    All of this is done purely through string matching on the AST; no imports,
    no eval, no subprocess calls.
    """
    result: dict = {
        "file": filename,
        "dags": [],
        "tasks": [],
        "dependencies": [],
        "datasets": [],
        "schedule": None,
        "operators": [],
    }

    # Bail early and surface the error rather than crashing the agent on malformed files
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return json.dumps({"error": f"SyntaxError in {filename}: {e}"})

    # ast.walk yields every node in the AST via depth-first traversal.
    # Each node is checked for the patterns we care about (Call, Expr/BinOp).
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            # Resolve both plain names (DAG(...)) and attribute calls (models.DAG(...))
            func_name = ""
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                func_name = node.func.attr

            # Capture dag_id and schedule from DAG() constructor calls.
            # dag_id may appear as the first positional argument or as the
            # explicit keyword argument ``dag_id``; the keyword form takes
            # precedence when both are present.
            if func_name == "DAG":
                dag_id = None
                schedule = None
                # First positional arg may be dag_id; keyword form takes precedence
                for i, arg in enumerate(node.args):
                    if i == 0 and isinstance(arg, ast.Constant):
                        dag_id = arg.value
                for kw in node.keywords:
                    if kw.arg == "dag_id" and isinstance(kw.value, ast.Constant):
                        dag_id = kw.value.value
                    if kw.arg in ("schedule", "schedule_interval"):
                        # Constant schedules (cron strings, timedelta literals) are
                        # extracted directly; complex expressions are unparsed to a
                        # readable string representation.
                        schedule = (
                            kw.value.value
                            if isinstance(kw.value, ast.Constant)
                            else ast.unparse(kw.value)
                        )
                if dag_id:
                    result["dags"].append(dag_id)
                if schedule:
                    result["schedule"] = schedule

            # Capture task_id and operator type from any *Operator() constructor
            # calls.  The name check covers all standard Airflow operators as well
            # as custom ones that follow the *Operator naming convention.
            if func_name.endswith("Operator") or func_name in (
                "PythonOperator", "BashOperator", "PostgresOperator",
                "EmptyOperator", "DummyOperator",
            ):
                task_id = None
                for kw in node.keywords:
                    if kw.arg == "task_id" and isinstance(kw.value, ast.Constant):
                        task_id = kw.value.value
                if task_id:
                    result["tasks"].append({"task_id": task_id, "operator": func_name})
                    if func_name not in result["operators"]:
                        result["operators"].append(func_name)

            # Capture Dataset URIs for Airflow 2.4+ dataset-aware scheduling.
            # Dataset(uri="...") declares a logical data asset that Airflow uses
            # to express cross-DAG dependencies and inlet/outlet lineage.
            if func_name == "Dataset":
                uri = None
                if node.args and isinstance(node.args[0], ast.Constant):
                    uri = node.args[0].value
                for kw in node.keywords:
                    if kw.arg == "uri" and isinstance(kw.value, ast.Constant):
                        uri = kw.value.value
                if uri and uri not in result["datasets"]:
                    result["datasets"].append(uri)

        # Detect >> dependency arrows (task_a >> task_b).
        # In Python's AST, ``a >> b`` is represented as an ``ast.BinOp`` node
        # whose ``op`` field is ``ast.RShift``.  Airflow overloads the right-shift
        # operator on task objects to declare dependencies.
        # ``ast.unparse`` converts both operands back to readable Python source.
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.BinOp):
            if isinstance(node.value.op, ast.RShift):
                left = ast.unparse(node.value.left)
                right = ast.unparse(node.value.right)
                result["dependencies"].append(f"{left} >> {right}")

    return json.dumps(result, indent=2)


# ── LangChain tools ────────────────────────────────────────────────────────────

def _fetch_all_pages(path: str, params: Optional[dict] = None, max_pages: int = 20) -> list:
    """Paginate through an OpenMetadata list endpoint and return all items."""
    params = dict(params or {})
    params.setdefault("limit", 100)
    items: list = []
    after: Optional[str] = None
    for _ in range(max_pages):
        if after:
            params["after"] = after
        resp = _om_request("GET", path, params=params)
        batch = resp.get("data", [])
        items.extend(batch)
        paging = resp.get("paging", {})
        after = paging.get("after")
        if not after or len(batch) < params["limit"]:
            break
    return items


def _compact_catalog_string() -> str:
    """
    Read the catalog manifest written by the catalog_manifest_refresh DAG and
    return a compact (~2k char) catalog summary for injection as a SystemMessage.

    Returns an empty string if the manifest doesn't exist yet (first run before
    the DAG has executed), so the caller can skip the injection silently.
    """
    try:
        with open(CATALOG_MANIFEST_PATH) as f:
            manifest = json.load(f)
    except FileNotFoundError:
        return ""
    except Exception as exc:
        print(f"[governance] catalog manifest unreadable: {exc}")
        return ""

    refreshed = manifest.get("refreshed_at", "")[:16].replace("T", " ")
    lines = [f"## Known assets (refreshed {refreshed} UTC)\n"]

    # ── OpenMetadata registered tables ────────────────────────────────────────
    om = manifest.get("openmetadata", {})
    om_tables = om.get("tables", [])
    service_tables: dict[str, list[dict]] = {}
    for tbl in om_tables:
        svc = (tbl.get("fqn") or "").split(".")[0] or "?"
        service_tables.setdefault(svc, []).append(tbl)

    for svc in om.get("services", []):
        svc_fqn  = svc.get("fqn", "?")
        svc_type = svc.get("type", "")
        lines.append(f"OpenMetadata service: {svc_fqn} [{svc_type}]")
        for tbl in service_tables.get(svc_fqn, []):
            tags    = tbl.get("tags") or []
            tag_str = f" [tags: {', '.join(tags)}]" if tags else ""
            lines.append(f"  {tbl['fqn']} ({tbl.get('col_count', 0)} cols){tag_str}")
        lines.append("")

    # ── PostgreSQL direct ─────────────────────────────────────────────────────
    for pg_db in manifest.get("postgres", []):
        db_name = pg_db.get("database", "?")
        tables  = pg_db.get("tables", [])
        lines.append(f"PostgreSQL database: {db_name} ({len(tables)} tables)")
        for t in tables:
            rc  = t.get("row_count")
            rc_str = f", ~{rc:,} rows" if rc is not None else ""
            cols = ", ".join(c["name"] for c in (t.get("columns") or [])[:8])
            lines.append(f"  {t['schema']}.{t['table']} ({t.get('col_count',0)} cols{rc_str})")
            if cols:
                lines.append(f"    cols: {cols}{'…' if len(t.get('columns') or []) > 8 else ''}")
        lines.append("")

    # ── MongoDB direct ────────────────────────────────────────────────────────
    for mg_db in manifest.get("mongo", []):
        db_name = mg_db.get("database", "?")
        lines.append(f"MongoDB database: {db_name}")
        for col in mg_db.get("collections", []):
            dc     = col.get("doc_count")
            dc_str = f" ({dc:,} docs)" if dc is not None else ""
            fields = ", ".join((col.get("sample_fields") or [])[:6])
            lines.append(f"  {col['name']}{dc_str}")
            if fields:
                lines.append(f"    fields: {fields}")
        lines.append("")

    # ── Governance gaps ───────────────────────────────────────────────────────
    gap_tables = [t for t in om_tables if t.get("gaps")]
    if gap_tables:
        lines.append("OpenMetadata governance gaps:")
        for t in gap_tables:
            lines.append(f"  {t['fqn']}: {', '.join(t['gaps'])}")

    result = "\n".join(lines)
    if len(result) > 3000:
        result = result[:2950] + "\n… (truncated — use catalog_snapshot for full detail)"
    return result


@tool
def catalog_snapshot(service: Optional[str] = None, database: Optional[str] = None) -> str:
    """
    Return a single structured snapshot of the OpenMetadata catalog.

    Fetches — in parallel — databases, tables (with columns, tags, owner,
    description), data-quality test-case counts, lineage edge counts, and
    glossary terms, then assembles them into a compact governance schema.

    Each table entry includes a ``governance_gaps`` list so the agent can
    immediately see which assets need attention without additional API calls.

    service:  optional filter — only tables whose FQN starts with this service name
    database: optional filter — only tables in this database (partial match)

    Returns JSON with keys:
      services        — list of database services
      databases       — list of registered databases with their service
      tables          — list of tables, each with:
                          fqn, schema, description, owner, tags,
                          column_count, columns (name+type+description+tags),
                          quality_tests, lineage_edges, governance_gaps
      glossary_terms  — list of active glossary terms (name + description)
      summary         — aggregate governance health counts
    """
    def _fetch_services():
        return _om_request("GET", "/api/v1/services/databaseServices", params={"limit": 100}).get("data", [])

    def _fetch_databases():
        return _fetch_all_pages("/api/v1/databases", {"fields": "service"})

    def _fetch_tables():
        params: dict = {"fields": "columns,tags,owner,description", "limit": 100}
        if service:
            params["service"] = service
        if database:
            params["database"] = database
        return _fetch_all_pages("/api/v1/tables", params)

    def _fetch_test_cases():
        raw = _fetch_all_pages("/api/v1/dataQuality/testCases", {"fields": "testDefinition,entityLink"})
        counts: dict[str, int] = {}
        for tc in raw:
            link = tc.get("entityLink", "")
            # entityLink format: <#E::table::fqn::column> or <#E::table::fqn>
            parts = link.strip("<>").split("::")
            if len(parts) >= 3:
                table_fqn = parts[2]
                counts[table_fqn] = counts.get(table_fqn, 0) + 1
        return counts

    def _fetch_glossary():
        terms = _fetch_all_pages("/api/v1/glossaryTerms", {"fields": "description,tags", "status": "Approved"})
        return [{"name": t.get("name"), "description": (t.get("description") or "")[:120]} for t in terms]

    # Run all fetches in parallel
    with ThreadPoolExecutor(max_workers=5) as pool:
        f_svcs   = pool.submit(_fetch_services)
        f_dbs    = pool.submit(_fetch_databases)
        f_tables = pool.submit(_fetch_tables)
        f_tests  = pool.submit(_fetch_test_cases)
        f_gloss  = pool.submit(_fetch_glossary)
        services_raw  = f_svcs.result()
        databases_raw = f_dbs.result()
        tables_raw    = f_tables.result()
        test_counts   = f_tests.result()
        glossary      = f_gloss.result()

    services = [
        {"name": s.get("fullyQualifiedName", s.get("name")), "type": s.get("serviceType")}
        for s in services_raw
    ]

    databases = [
        {
            "fqn": d.get("fullyQualifiedName"),
            "service": d.get("service", {}).get("fullyQualifiedName"),
        }
        for d in databases_raw
    ]

    tables: list[dict] = []
    gap_counts = {"no_owner": 0, "no_description": 0, "no_tags": 0, "no_quality_tests": 0}

    for t in tables_raw:
        fqn = t.get("fullyQualifiedName", "")
        owner_name = (
            (t.get("owner") or {}).get("displayName")
            or (t.get("owner") or {}).get("name")
        )
        description = (t.get("description") or "").strip()
        tags = [tg.get("tagFQN") for tg in (t.get("tags") or []) if tg.get("tagFQN")]
        q_count = test_counts.get(fqn, 0)

        columns = []
        for col in t.get("columns") or []:
            col_tags = [tg.get("tagFQN") for tg in (col.get("tags") or []) if tg.get("tagFQN")]
            columns.append({
                "name": col.get("name"),
                "type": col.get("dataType"),
                "description": (col.get("description") or "").strip() or None,
                "tags": col_tags or None,
            })

        gaps: list[str] = []
        if not owner_name:
            gaps.append("no_owner"); gap_counts["no_owner"] += 1
        if not description:
            gaps.append("no_description"); gap_counts["no_description"] += 1
        if not tags:
            gaps.append("no_tags"); gap_counts["no_tags"] += 1
        if q_count == 0:
            gaps.append("no_quality_tests"); gap_counts["no_quality_tests"] += 1

        tables.append({
            "fqn": fqn,
            "schema": t.get("databaseSchema", {}).get("fullyQualifiedName"),
            "description": description or None,
            "owner": owner_name,
            "tags": tags or None,
            "column_count": len(columns),
            "columns": columns,
            "quality_tests": q_count,
            "governance_gaps": gaps or None,
        })

    summary = {
        "total_services": len(services),
        "total_databases": len(databases),
        "total_tables": len(tables),
        "total_glossary_terms": len(glossary),
        "tables_with_gaps": sum(1 for t in tables if t["governance_gaps"]),
        **gap_counts,
    }

    result = {
        "services": services,
        "databases": databases,
        "tables": tables,
        "glossary_terms": glossary,
        "summary": summary,
    }
    # Cap at 12 000 chars — the snapshot can be large; the agent can drill down
    # with openmetadata_api if it needs a specific table's full detail.
    return json.dumps(result, indent=2, default=str)[:12000]


@tool
def openmetadata_api(method: str, path: str, params: Optional[dict] = None, body: Optional[dict | list] = None) -> str:
    """
    Call the OpenMetadata REST API (auth via OPENMETADATA_TOKEN).
    method: GET | POST | PUT | PATCH | DELETE
    path:   e.g. /api/v1/tables, /api/v1/tags, /api/v1/lineage
    params: query-string dict for GET requests
    body:   dict for POST/PUT; list of JSON-Patch ops for PATCH
    """
    result = _om_request(method, path, params, body)
    return json.dumps(result, indent=2)[:4000]


@tool
def postgres_query(sql: str, limit: int = 100) -> str:
    """
    Execute a read-only SQL query against PostgreSQL (connection from POSTGRES_DSN).
    sql:   SELECT or introspection query (information_schema, pg_catalog)
    limit: max rows returned (default 100)
    Forbidden: INSERT, UPDATE, DELETE, DROP, TRUNCATE, ALTER, CREATE.
    """
    normalized = sql.strip().upper()
    for forbidden in ("INSERT", "UPDATE", "DELETE", "DROP", "TRUNCATE", "ALTER", "CREATE"):
        if normalized.startswith(forbidden):
            return f"Error: {forbidden} statements are not allowed (read-only access)."

    try:
        conn = psycopg2.connect(POSTGRES_DSN)
        conn.set_session(readonly=True, autocommit=True)
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql)
            rows = cur.fetchmany(limit)
        conn.close()
        return json.dumps([dict(r) for r in rows], indent=2, default=str)[:4000]
    except Exception as e:
        return f"Query error: {e}"


@tool
def mongodb_query(
    action: str,
    database: Optional[str] = None,
    collection: Optional[str] = None,
    filter: Optional[dict] = None,
    pipeline: Optional[list] = None,
    limit: int = 20,
) -> str:
    """
    Query MongoDB read-only (connection from MONGO_URI).
    action:     list_databases | list_collections | find | aggregate | count
    database:   required for all except list_databases
    collection: required for find, aggregate, count
    filter:     MongoDB query dict (optional)
    pipeline:   list of aggregation stage dicts (aggregate only)
    limit:      max documents returned (default 20, max 200)
    """
    limit = min(limit, 200)
    try:
        client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

        if action == "list_databases":
            return json.dumps(client.list_database_names())

        if not database:
            return "Error: 'database' is required for this action."
        db = client[database]

        if action == "list_collections":
            return json.dumps(db.list_collection_names())

        if not collection:
            return "Error: 'collection' is required for find, aggregate, and count."
        col = db[collection]

        if action == "find":
            docs = list(col.find(filter or {}, limit=limit))
            return json.dumps(docs, indent=2, default=str)[:4000]

        if action == "aggregate":
            if not pipeline:
                return "Error: 'pipeline' is required for aggregate."
            return json.dumps(list(col.aggregate(pipeline))[:limit], indent=2, default=str)[:4000]

        if action == "count":
            return json.dumps({"count": col.count_documents(filter or {})})

        return f"Error: unknown action '{action}'. Use: list_databases | list_collections | find | aggregate | count"
    except Exception as e:
        return f"MongoDB error: {e}"


@tool
def dag_reader(action: str, filename: Optional[str] = None) -> str:
    """
    Access Airflow DAG files from AIRFLOW_DAGS_PATH without importing or executing them.
    action:   list | read | parse
    filename: DAG filename (required for read/parse; partial name match supported)
    parse returns JSON with dag IDs, tasks, operators, dataset URIs, dependencies.
    """
    _is_remote_dags = bool(_REMOTE_HOST) and not os.path.isdir(AIRFLOW_DAGS_PATH)

    if _is_remote_dags:
        import subprocess
        # DAGs directory lives on the Raspberry Pi — use SSH to access files.
        if action == "list":
            r = subprocess.run(
                ["ssh", f"{_REMOTE_USER}@{_REMOTE_HOST}", f"ls {AIRFLOW_DAGS_PATH}/*.py 2>/dev/null || echo NO_FILES"],
                capture_output=True, text=True, timeout=15,
            )
            if r.returncode != 0:
                return f"SSH error listing DAGs: {r.stderr.strip()}"
            names = [os.path.basename(p) for p in r.stdout.strip().splitlines() if p != "NO_FILES"]
            return "\n".join(names) if names else "No DAG files found."

        if not filename:
            return "Error: 'filename' is required for 'read' and 'parse'."
        remote_path = f"{AIRFLOW_DAGS_PATH}/{filename}"
        r = subprocess.run(
            ["ssh", f"{_REMOTE_USER}@{_REMOTE_HOST}", f"cat '{remote_path}' 2>/dev/null || echo __NOT_FOUND__"],
            capture_output=True, text=True, timeout=15,
        )
        source = r.stdout
        if "__NOT_FOUND__" in source or r.returncode != 0:
            return f"Error: '{filename}' not found on remote host at {remote_path}"
        if action == "read":
            return source[:6000]
        if action == "parse":
            return _parse_dag_ast(source, filename)
        return f"Error: unknown action '{action}'. Use: list | read | parse"

    if not os.path.isdir(AIRFLOW_DAGS_PATH):
        return f"Error: AIRFLOW_DAGS_PATH '{AIRFLOW_DAGS_PATH}' is not a valid directory."

    if action == "list":
        files = sorted(glob.glob(os.path.join(AIRFLOW_DAGS_PATH, "*.py")))
        return "\n".join(os.path.basename(f) for f in files) if files else "No DAG files found."

    if not filename:
        return "Error: 'filename' is required for 'read' and 'parse'."

    filepath = os.path.join(AIRFLOW_DAGS_PATH, filename)
    if not os.path.isfile(filepath):
        matches = glob.glob(os.path.join(AIRFLOW_DAGS_PATH, f"*{filename}*"))
        if not matches:
            return f"Error: '{filename}' not found in {AIRFLOW_DAGS_PATH}"
        filepath = matches[0]

    with open(filepath) as f:
        source = f.read()

    if action == "read":
        return source[:6000]
    if action == "parse":
        return _parse_dag_ast(source, os.path.basename(filepath))

    return f"Error: unknown action '{action}'. Use: list | read | parse"


@tool
def airflow_api(method: str, path: str, params: Optional[dict] = None, body: Optional[dict] = None) -> str:
    """
    Call the Airflow REST API read-only (auth from AIRFLOW_USER/AIRFLOW_PASSWORD).
    method: GET (POST blocked for dagRuns — triggering is the ingestion agent's job)
    path:   e.g. /api/v1/dags, /api/v1/dags/{id}/tasks, /api/v1/datasets
    params: query-string dict (optional)
    body:   JSON body (optional)
    """
    if "dagRuns" in path and method.upper() == "POST":
        return "Error: triggering DAG runs is not a governance action. Use the ingestion agent."
    result = _af_request(method, path, params, body)
    return json.dumps(result, indent=2)[:4000]



# ── Agent setup ────────────────────────────────────────────────────────────────
#
# The tool list controls which functions the model can invoke.  ``tools_by_name``
# is a fast lookup dict used during the agentic loop to dispatch tool calls by
# name without iterating the full list.

tools = [
    catalog_snapshot,
    openmetadata_api,
    postgres_query,
    mongodb_query,
    dag_reader,
    airflow_api,
]
tools_by_name = {t.name: t for t in tools}

# ``init_chat_model`` is LangChain's unified model factory.  It returns a
# LangChain chat model object regardless of the underlying provider, allowing
# the rest of the code to stay provider-agnostic.  Here it targets a locally
# hosted Qwen 3.5 397B model served through the Ollama API.
#
# temperature=0.0 is critical for a governance agent: deterministic outputs
# ensure that the same schema produces the same classification every time, and
# prevents the model from "improvising" metadata or quality rules.
#
# ``structured_output: True`` instructs the Ollama provider to use JSON-mode
# for tool-call responses, ensuring tool arguments are always valid JSON.
#
# ``bind_tools(tools)`` attaches the JSON-Schema descriptions of all @tool
# functions to every model call, so the model always knows what tools are
# available and what arguments they expect.
model = build_model("governance")
model_with_tools = model.bind_tools(tools)

# ── System prompt ──────────────────────────────────────────────────────────────
#
# The SystemMessage is the agent's constitution.  It is always placed as the
# first message in every conversation (messages[0]) and is never dropped by the
# sliding context window.  It defines:
#   - The agent's identity and mandate within the multi-agent system.
#   - The four core governance responsibilities (schema management, data
#     profiling, GDELT domain knowledge, policy classification).
#   - Risk classification levels: L0 Public, L1 Internal, L2 Sensitive, L3 PII.
#   - Tool usage policy: which tool to use for which purpose, and critical
#     constraints (read-only Postgres, no DAG triggering, etc.).
#   - Behaviour rules: when to ask for confirmation, how to format findings,
#     how to handle tool failures.
#   - Output format: [ASSET] → [FINDING] → [RECOMMENDATION] → [ACTION REQUIRED].

SYSTEM_PROMPT = SystemMessage(content=f"""
# ── Service endpoints (from access_hosts.py) ────────────────
- OpenMetadata : {OPENMETADATA_HOST}
- PostgreSQL   : {POSTGRES_DSN}
- MongoDB      : {MONGO_URI}
- Airflow      : {AIRFLOW_API_URL}
- DAGs path    : {AIRFLOW_DAGS_PATH} (remote Pi — dag_reader handles SSH automatically)

# ── Identity ────────────────────────────────────────────────
You are a Data Governance Agent operating within a multi-agent analytics system
built on the GDELT Project dataset. Your role is to enforce data quality, maintain
metadata, classify assets by risk and sensitivity, and advise the team on data
standards and governance policies.

## Core responsibilities

1. Schema & metadata management
   - Connect to OpenMetadata to read, register, and update table/column metadata
     for both PostgreSQL and MongoDB data stores.
   - Ensure every data asset has an owner, description, tags, and data classification.
   - Flag assets that lack documentation or lineage information.

2. Data profiling & quality
   - Read table schemas and sample data from PostgreSQL (GDELT event tables,
     GKG tables, mention tables) and MongoDB (processed events, GKG records,
     graph adjacency documents).
   - Detect schema drift, missing values, null rates, and type mismatches.
   - Raise data quality incidents in OpenMetadata when thresholds are breached.

3. GDELT domain knowledge
   - The GDELT GKG Codebook v2.1 is injected into your context at session start
     as a "GDELT GKG reference" block. Use it as the authoritative reference for
     all GKG field semantics, tone scores, GCAM dimensions, location types,
     count types, and theme codes.
   - When a column name or value pattern matches a GDELT field, cross-reference the
     codebook block before making governance decisions or writing metadata descriptions.

4. Policy & classification
   - Apply risk classification (L0 Public / L1 Internal / L2 Sensitive / L3 PII)
     to all assets based on content analysis and codebook context.
   - Recommend masking, access control, or retention policies where appropriate.
   - Identify fields that may carry indirect PII (actor names, geographic identifiers,
     source URLs) and flag them for review.

5. Autonomous governance
   - Act on governance decisions without waiting for confirmation. Apply the most
     appropriate policy given available context, then report what you did and why.
   - When schema ambiguity exists, apply the most conservative classification
     (higher sensitivity level) and document the assumption in OpenMetadata.
     Note it in your response so the user can override if needed.
   - Default environment is prod unless the user's message or session history
     clearly indicates otherwise. State the assumption in your response.
   - When a request is underspecified, pick the broadest safe interpretation and
     execute it: inspect the full schema, apply the policy to all flagged columns,
     open a data quality incident (not just a warning) when thresholds are breached.
   - For multi-step governance workflows, execute all steps and present a
     structured audit trail of what was done, not a plan requiring approval.

## Tools available

catalog_snapshot  — ALWAYS call this first. Returns a single structured snapshot of
                    the entire OpenMetadata catalog: services, databases, tables with
                    columns/tags/owner/description, quality-test counts, glossary terms,
                    and a governance_gaps list per table. Use it to orient yourself before
                    making targeted openmetadata_api calls. Optional filters: service, database.
openmetadata_api  — full CRUD access to the OpenMetadata REST API
postgres_query    — read-only SQL against the connected PostgreSQL database
mongodb_query     — read-only queries against MongoDB (find, aggregate, count, list)
dag_reader        — list, read, or AST-parse Airflow DAG files
airflow_api       — read-only Airflow REST API (DAG runs blocked)

## OpenMetadata API knowledge

An "OpenMetadata API reference" block is injected at the start of each session.
It contains concrete endpoint paths, request body formats, response shapes, and
pagination patterns for all major OM entity types (tables, lineage, test cases,
glossary terms, search). Use it to construct correct API calls before falling
back to trial-and-error with openmetadata_api.

## PostgreSQL connection constraint

- postgres_query connects to exactly ONE database (the one configured in POSTGRES_DSN).
  PostgreSQL does NOT support cross-database queries.
- NEVER write SQL that references another database by three-part prefix:
      SELECT * FROM other_db.public.some_table        -- WILL FAIL
      SELECT 1 FROM other_db.schema.table LIMIT 1     -- WILL FAIL
  These always raise "cross-database references are not implemented".
- To inspect a table in a database you are NOT currently connected to, use
  openmetadata_api with a direct FQN lookup:
      GET /api/v1/tables/name/{{service}}.{{database}}.{{schema}}.{{table}}
- Use SELECT current_database() to confirm which database postgres_query is
  connected to before querying schema objects.
- A "Live catalog context" block is injected at the start of each session.
  It tells you which database postgres_query is connected to and which databases
  and services are registered in OpenMetadata. Use it to plan your queries.

## Registering tables in OpenMetadata (POST /api/v1/tables)

ALWAYS check existence before creating. Use:
  GET /api/v1/tables/name/<service>.<database>.<schema>.<table>
If it returns a table object (has "id"), the table exists — do NOT POST again.

POST body shape (EXACTLY this — no other fields):
{{
  "name": "<simple_table_name>",
  "databaseSchema": "<service>.<database>.<schema>",
  "columns": [
    {{"name": "id",        "dataType": "INT"}},
    {{"name": "username",  "dataType": "VARCHAR",   "dataLength": 255}},
    {{"name": "created",   "dataType": "TIMESTAMP"}},
    {{"name": "active",    "dataType": "BOOLEAN"}}
  ]
}}

CRITICAL RULES — violating any of these causes HTTP 400 "Unrecognized field":
- "databaseSchema" goes in the REQUEST BODY as a fully-qualified-name string (service.db.schema).
  NEVER send it as a query parameter.
- NEVER include "database" or "schema" as separate body fields. They do NOT exist in POST.
- "name" must be just the table name (e.g. "ab_permission"), NEVER a dotted FQN.
- Every column MUST have "name" and "dataType". All other column fields are optional.

PostgreSQL data_type → OpenMetadata dataType mapping (required — OM rejects raw PG types):
  integer            → INT
  bigint             → BIGINT
  smallint           → INT
  character varying  → VARCHAR  (also add "dataLength": <n> if known)
  varchar            → VARCHAR
  text               → TEXT
  boolean            → BOOLEAN
  numeric            → NUMERIC  (add "precision" and "scale" if known)
  double precision   → DOUBLE
  real               → FLOAT
  timestamp without time zone → TIMESTAMP
  timestamp with time zone    → TIMESTAMP
  date               → DATE
  time               → TIME
  json               → JSON
  jsonb              → JSON
  uuid               → UUID
  bytea              → BYTES
  ARRAY              → ARRAY
  USER-DEFINED       → STRUCT

For existing tables with missing columns, use PATCH — NOT another POST:
  PATCH /api/v1/tables/<table_id>
  Content-Type: application/json-patch+json
  Body: [{{"op": "add", "path": "/columns/-", "value": {{"name": "col", "dataType": "INT"}}}}]

Example full workflow:
  1. GET /api/v1/tables/name/Raw_Data_Postgres.airflow_db.public.ab_permission
     → if 200 with id, table exists → PATCH to add missing cols; skip POST
     → if 404, proceed to step 2
  2. POST /api/v1/tables
     body: {{"name": "ab_permission", "databaseSchema": "Raw_Data_Postgres.airflow_db.public",
             "columns": [{{"name": "id", "dataType": "INT"}}, {{"name": "name", "dataType": "VARCHAR", "dataLength": 256}}]}}

## MongoDB / NoSQL service FQN convention

OpenMetadata's MongoDB connector always injects a synthetic schema layer named "default".
Collection FQNs are always: <service>.<database>.default.<collection>
NEVER construct a MongoDB table FQN as <service>.<database>.<collection> — that path
will 404. Before any MongoDB FQN lookup, resolve the schema with:
  GET /api/v1/databaseSchemas?database=<db_fqn>
to confirm the actual schema name (almost always "default").

## Existence check protocol

A 404 on GET /api/v1/tables/name/<fqn> proves only that *that exact FQN* is not
registered. A wrong FQN gives a 404 even if the table exists under the correct FQN.
Do NOT treat a 404 from a guessed FQN as proof the table is absent.

Before issuing POST /api/v1/tables:
1. Resolve the correct schema FQN: GET /api/v1/databaseSchemas?database=<db_fqn>
2. Search: GET /api/v1/search/query?q=<table_name>&index=table_search_index
3. Only POST if (1) resolves a schema AND (2) returns no hit for the table name.
If a 409 is returned on POST, the table already exists — switch to PATCH.

## JSON Patch atomicity

PATCH bodies are atomic — if ANY operation fails, NONE are applied.
Before sending a multi-op PATCH that references other entities (tags, owners, glossary terms),
verify each referenced FQN/id exists:
  GET /api/v1/tags/name/<tagFQN>
  GET /api/v1/users/name/<username>
  GET /api/v1/glossaryTerms/name/<termFQN>
If you cannot verify a reference, split the PATCH into separate calls — one bad op
cannot then roll back the others.

## Updating table owners (PATCH /api/v1/tables/<id>)

OpenMetadata 1.12.5 uses the **plural /owners** path with a full EntityReference array.
Wrong: {{"op":"add","path":"/owner","value":"<uuid>"}}
Right:
[{{"op": "add", "path": "/owners", "value": [
  {{"id": "<user_uuid>", "type": "user"}}
]}}]

"type" must be present ("user" or "team"). Omitting it or using /owner (singular) causes HTTP 500.
Get the user uuid first: GET /api/v1/users/name/<username>

## Creating data quality test cases (POST /api/v1/dataQuality/testCases)

Path: /api/v1/dataQuality/testCases   (NOT /api/v1/testCases)

Body:
{{
  "name": "<test_name>",
  "description": "...",
  "testDefinition": "columnValuesToBeNotNull",
  "entityLink": "<#E::table::<table_fqn>::columns::<col_name>>",
  "parameterValues": [{{"name": "...", "value": "..."}}]
}}

Field names — common mistakes:
- "testDefinition"  NOT "definition" or "testDefinitionFQN"
- "entityLink"      NOT "entityFQN" or "tableLink"
- Column-level:  <#E::table::<table_fqn>::columns::<column_name>>
- Table-level:   <#E::table::<table_fqn>>

List available test definitions: GET /api/v1/dataQuality/testDefinitions?limit=50

## Learn from recent tool results — do not guess field names

Before constructing a POST or PATCH body for a new entity, scan the current context
for a recent GET response of the same entity type. The GET response shape is the
authoritative template for POST/PUT body field names — they match exactly.
If a prior tool result already shows a working example, copy its field names.

When a response returns HTTP 400 with "Unrecognized field X" or "param Y must not be null":
- Fix ONLY the field named in the error message.
- Do not rename other fields or restructure the body.
- Do not retry with the same body — that will produce the same error.

## Known unavailable endpoints (do NOT call these — they return HTTP 404 in this installation)

- GET /api/v1/dataQuality            (use /api/v1/dataQuality/testCases instead)
- GET /api/v1/dataQuality/tests      (not available)
- GET /api/v1/dataQuality/testResults (not available)
- GET /api/v1/alerts                 (not available)
- GET /api/v1/incidents              (not available)
- GET /api/v1/dataQuality/incidents  (not available)
- GET /api/v1/server                 (not available)
- GET /api/v1/services               (not available — use /api/v1/services/databaseServices
                                      or /api/v1/services/pipelineServices etc.)
- GET /api/v1/services/connections   (not available)
- GET /api/v1/tables with fields=classifications (invalid — use fields=tags)
- GET /api/v1/tables with fields=columns.name or fields=columns.description
  (invalid sub-field syntax — use fields=columns to get the full columns array)

## Known unavailable search indexes (do NOT use these — they return HTTP 500)

- dag_search_index          → use index=pipeline_search_index
- mongo_collection_search_index → use index=table_search_index
- mongo                     → use index=table_search_index

## Airflow pipeline lineage

Airflow DAGs are registered in OpenMetadata as Pipeline entities, not as tables.

Finding a pipeline:
  GET /api/v1/pipelines                          — list all pipelines
  GET /api/v1/pipelines/name/<service>.<dag_id>  — fetch by FQN
  GET /api/v1/search/query?q=<dag_name>&index=pipeline_search_index  — search

Registering pipeline → table lineage:
  POST /api/v1/lineage
  body={{
    "edge": {{
      "fromEntity": {{"id": "<pipeline_id>", "type": "pipeline"}},
      "toEntity":   {{"id": "<table_id>",    "type": "table"}},
      "lineageDetails": {{"description": "<how the DAG writes to the table>"}}
    }}
  }}

Pipeline FQN format: <pipelineServiceName>.<dag_id>
To find the pipeline service name: GET /api/v1/services/pipelineServices

## Batch tool calls — CRITICAL for performance

When you need to perform the same write operation on multiple assets (e.g. creating
glossary terms for 20 columns, or tagging 10 tables), issue ALL tool calls in a
SINGLE response batch rather than one per response. The tool executor runs them in
parallel, so 10 simultaneous POSTs take the same time as 1.

Example — correct (batch):
  Response contains tool_calls: [POST glossaryTerm col1, POST glossaryTerm col2, ...]

Example — wrong (sequential):
  Response 1: POST glossaryTerm col1 → wait → Response 2: POST glossaryTerm col2 ...

## Tool loop prevention — CRITICAL

- If you already called a tool with certain arguments and received a result, do NOT call
  it again with the same arguments. The result will be identical. Use it and move on.
- If a search query returns results that do not match what you need, do NOT retry the
  same search. Switch strategy: use a direct FQN lookup instead —
  GET /api/v1/tables/name/{{service}}.{{database}}.{{schema}}.{{table}}.
- Every repeated identical tool call wastes time and brings you closer to the iteration
  limit without making progress. When stuck, summarise what you found and stop.

## Behaviour rules

- Be precise and technical. Your audience is data engineers and data governance leads.
- Always cite the codebook (section and field name) when making domain assertions.
- Never invent metadata. If you cannot determine a field's meaning from the codebook
  or schema context, apply the most conservative classification and flag it for review.
- When presenting findings, structure output as:
      [ASSET] → [FINDING] → [ACTION TAKEN] → [OUTCOME]
- Log every governance action you take as a comment in OpenMetadata.
- If a tool call fails, retry ONCE with different parameters. If it fails again, do NOT
  retry. Move on and include the failure in the audit trail.
- Do not expose connection strings, tokens, or credentials in your responses.
- Never trigger DAG runs — that is the ingestion agent's responsibility.
  Use airflow_api only for read operations (GET) and dataset URI inspection.
- Proactively surface governance issues you notice while completing a task,
  even if they were not explicitly requested. Create incidents and recommendations
  without being asked.

## Tone & format

Concise, precise, professional. Use tables for multi-column findings.
Use bullet points only for short lists. Prefer structured prose for explanations.
No filler, no over-explanation of obvious steps.

""")


# ── Internal write-log helper ──────────────────────────────────────────────────

def _log_om_write(mem: dict, tc) -> None:
    """
    Append a governance write action to in-memory state when the agent calls
    ``openmetadata_api`` with a mutating HTTP method.

    Why only POST/PUT/PATCH/DELETE?
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    GET requests are read operations — they retrieve information but do not
    change the state of any data asset.  Recording GET calls as governance
    incidents would create noise that drowns out the meaningful audit trail of
    actual changes.  Only write operations (POST to create, PUT to replace,
    PATCH to partially update, DELETE to remove) are governance-relevant and
    worth persisting.

    Why not call save_memory here?
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    In a single agent turn, the model may issue multiple tool calls in the same
    response (e.g. look up a user UUID with GET, then PATCH a table with the
    UUID, then POST a quality test).  Calling ``save_memory`` after each
    individual write would cause multiple redundant disk writes per turn.
    Instead, ``_log_om_write`` only mutates the in-memory dict; ``save_memory``
    is called once after the full tool batch completes (see the tool-call loops
    in ``run_governance_session`` and ``run_agent``).

    Lineage edges vs incidents
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    Lineage writes (paths containing ``/lineage``) are stored in the
    ``lineage_edges`` list with from/to FQN fields extracted from the edge
    body.  All other writes are stored in the ``incidents`` list as a generic
    audit log entry with the method, path, and timestamp.
    """
    # Only record write operations; GET reads are not governance actions worth persisting
    method = tc["args"].get("method", "").upper()
    if method not in ("POST", "PUT", "PATCH", "DELETE"):
        return
    path = tc["args"].get("path", "")
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    if "/lineage" in path:
        # Extract source and target FQNs from the lineage edge body
        body = tc["args"].get("body") or {}
        edge = {
            "from": body.get("edge", {}).get("fromEntity", {}).get("fqn", "?"),
            "to":   body.get("edge", {}).get("toEntity", {}).get("fqn", "?"),
            "source": "openmetadata_api",
            "timestamp": ts,
        }
        mem["lineage_edges"].append(edge)
    else:
        # Record any other write (tag update, quality test, description change, etc.) as an incident
        mem["incidents"].append({
            "asset": path,
            "finding": f"{method} {path}",
            "timestamp": ts,
        })


# ── Interactive session ────────────────────────────────────────────────────────

def run_governance_session() -> None:
    """
    Run an interactive multi-turn governance REPL (Read-Eval-Print Loop).

    Session lifecycle
    ~~~~~~~~~~~~~~~~~
    1. ``load_memory()`` restores prior classification decisions, lineage edges,
       and incidents from disk so the agent has continuity across restarts.
    2. If memory is non-empty, ``_memory_summary()`` is appended to the system
       prompt so the model is aware of past decisions before the first user
       message.  When memory is empty (first ever run), no summary is injected
       to avoid adding empty noise to the prompt.
    3. The main ``while True`` loop reads one user message per iteration.
    4. The inner ``while True`` loop (the agentic loop) repeatedly invokes the
       model until it produces a plain text response (no more tool calls):
         - If the model returns tool calls, each is dispatched to its handler,
           and the result is appended as a ToolMessage.
         - After all tool calls in a batch are processed, ``save_memory`` is
           called once to persist any write actions logged by ``_log_om_write``.
         - When the model returns a plain text response, it is printed and the
           inner loop exits, returning to the user prompt.

    Sliding context window
    ~~~~~~~~~~~~~~~~~~~~~~
    The sliding window (``_CONTEXT_WINDOW = 100``) keeps the conversation list
    from growing unboundedly.  Before each model invocation, if the message
    list exceeds ``_CONTEXT_WINDOW + 1`` entries, the oldest messages (after
    the system prompt) are silently dropped.  The system prompt (messages[0])
    is always preserved so the agent never loses its identity or tool policies.
    """
    # Load prior session state so the agent remembers past decisions
    mem = load_memory()

    print("[governance] Data Governance Agent started.")
    print(f"[governance] OpenMetadata : {OPENMETADATA_HOST}")
    print(f"[governance] Airflow      : {AIRFLOW_API_URL}")
    print(f"[governance] DAGs path    : {AIRFLOW_DAGS_PATH}")
    print(f"[governance] Memory       : {len(mem['incidents'])} incidents, "
          f"{len(mem['lineage_edges'])} lineage edges, "
          f"{len(mem['classifications'])} classified assets")
    print("[governance] Type your governance request. Ctrl+C to exit.\n")

    # Inject memory only when there is something to recall — avoids adding empty noise to the prompt.
    # ``any([...])`` is used instead of ``bool(mem)`` because the top-level dict always has
    # all three keys; we need to check whether any of the collections are non-empty.
    has_memory = any([mem["classifications"], mem["lineage_edges"], mem["incidents"]])
    system_content = str(SYSTEM_PROMPT.content)
    if has_memory:
        system_content += f"\n\n## Memory from previous runs\n\n{_memory_summary(mem)}"
    session_prompt = SystemMessage(content=system_content)
    catalog_ctx = _get_catalog_context()
    catalog_msg = SystemMessage(content=f"## Live catalog context\n\n{catalog_ctx}")
    messages: list[BaseMessage] = [session_prompt, catalog_msg]
    _compact = _compact_catalog_string()
    if _compact:
        messages.append(SystemMessage(content=_compact))
    if _OM_API_DOCS:
        messages.append(SystemMessage(content=f"## OpenMetadata API reference\n\n{_OM_API_DOCS}"))
    if _GDELT_DOCS:
        messages.append(SystemMessage(content=f"## GDELT GKG reference\n\n{_GDELT_DOCS}"))
    if _MONGO_DOCS:
        messages.append(SystemMessage(content=f"## MongoDB reference\n\n{_MONGO_DOCS}"))
    if _PG_DOCS:
        messages.append(SystemMessage(content=f"## PostgreSQL reference\n\n{_PG_DOCS}"))

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n[governance] Session ended.")
            break

        if not user_input:
            continue

        messages.append(HumanMessage(content=user_input))

        # Inner agentic loop: the model keeps calling tools until it produces
        # a plain text response with no further tool calls.
        while True:
            # Keep system prompt + last _CONTEXT_WINDOW messages to prevent context overflow.
            # Slice: messages[0] is always the system prompt; messages[-_CONTEXT_WINDOW:]
            # are the most recent turns.
            if len(messages) > _CONTEXT_WINDOW + 1:
                messages = [messages[0]] + messages[-_CONTEXT_WINDOW:]
            response = model_with_tools.invoke(messages)
            messages.append(response)

            if response.tool_calls:
                # Run all tool calls in this batch concurrently — the model has
                # already committed to which tools to call before seeing any results,
                # so the calls are independent and safe to parallelise.
                _batch_t = time.time()
                with ThreadPoolExecutor(max_workers=len(response.tool_calls)) as pool:
                    futures = {
                        pool.submit(tools_by_name[tc["name"]].invoke, tc["args"]): tc
                        for tc in response.tool_calls
                    }
                    raw_results: dict[str, str] = {}
                    for future in as_completed(futures):
                        tc = futures[future]
                        try:
                            raw_results[tc["id"]] = str(future.result())
                        except Exception as exc:
                            raw_results[tc["id"]] = f"Tool error: {exc}"
                print(f"[governance] tool batch done in {time.time()-_batch_t:.1f}s")
                # Append ToolMessages in original order so the LLM sees them correctly.
                for tc in response.tool_calls:
                    result = raw_results[tc["id"]]
                    print(f"[governance] tool_call  : {tc['name']}({json.dumps(tc['args'])[:200]})")
                    print(f"[governance] tool_result: {result[:300].replace(chr(10), ' ')}")
                    messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))
                    if tc["name"] == "openmetadata_api":
                        _log_om_write(mem, tc)
                # Persist after every tool batch so no governance actions are lost on crash
                save_memory(mem)
            else:
                # No tool calls: the model has produced its final response for this turn.
                print(f"\nAgent: {response.content}\n")
                break


def run_agent(request: str, max_iters: int = 100) -> str:
    """
    Run the governance agent for a single programmatic request and return the
    final response as a plain string.

    This is the single-turn API used by the orchestrator and other agents to
    invoke governance capabilities without starting an interactive REPL.  It
    runs the same agentic loop as ``run_governance_session`` — the model can
    still issue multiple rounds of tool calls before producing its final
    answer — but the function returns that answer as a string rather than
    printing it.

    Memory is loaded at the start so that programmatic callers also benefit
    from prior governance state (e.g. already-classified assets are not
    re-classified on every orchestrator call).  Write actions are logged and
    persisted after each tool batch, exactly as in the interactive session.

    Args:
        request: the governance task description as a plain-text string.

    Returns:
        The agent's final response string.
    """
    # Load memory so programmatic callers also benefit from prior governance state
    mem = load_memory()
    # Inject memory summary into the system prompt (same as run_governance_session).
    # Without this the agent would be blind to prior classifications and incidents
    # when invoked programmatically by the orchestrator.
    has_memory = any([mem["classifications"], mem["lineage_edges"], mem["incidents"]])
    system_content = str(SYSTEM_PROMPT.content)
    if has_memory:
        system_content += f"\n\n## Memory from previous runs\n\n{_memory_summary(mem)}"
    session_prompt = SystemMessage(content=system_content)
    catalog_ctx = _get_catalog_context()
    catalog_msg = SystemMessage(content=f"## Live catalog context\n\n{catalog_ctx}")
    messages: list[BaseMessage] = [session_prompt, catalog_msg]
    _compact = _compact_catalog_string()
    if _compact:
        messages.append(SystemMessage(content=_compact))
    if _OM_API_DOCS:
        messages.append(SystemMessage(content=f"## OpenMetadata API reference\n\n{_OM_API_DOCS}"))
    if _GDELT_DOCS:
        messages.append(SystemMessage(content=f"## GDELT GKG reference\n\n{_GDELT_DOCS}"))
    if _MONGO_DOCS:
        messages.append(SystemMessage(content=f"## MongoDB reference\n\n{_MONGO_DOCS}"))
    if _PG_DOCS:
        messages.append(SystemMessage(content=f"## PostgreSQL reference\n\n{_PG_DOCS}"))
    messages.append(HumanMessage(content=request))

    _t0 = time.time()
    _iter = 0
    # Per-run cache: identical (tool_name, args) pairs return the cached result instantly
    # instead of making a redundant LLM+tool round-trip.  Key = "tool:sorted_args_json".
    _call_cache: dict[str, str] = {}
    first_line = next((ln.strip() for ln in request.splitlines() if ln.strip()), request[:80])
    print(f"[governance] run_agent START — {first_line!r}")
    while True:
        # Apply the same sliding window as the interactive session to prevent context overflow
        if len(messages) > _CONTEXT_WINDOW + 1:
            messages = [messages[0]] + messages[-_CONTEXT_WINDOW:]
        _iter += 1
        if _iter > max_iters:
            # Walk backwards to find the last clean AI text response (not a ToolMessage).
            # messages[-1] is often a ToolMessage when the limit is hit, which would
            # return raw tool output (e.g. a full file) as the agent's reply.
            for msg in reversed(messages):
                if hasattr(msg, "tool_calls") and not msg.tool_calls and msg.content:
                    print(f"[governance] max_iters={max_iters} reached — returning last AI response")
                    return str(msg.content)
            print(f"[governance] max_iters={max_iters} reached — no clean AI response found")
            return (
                f"Reached the iteration limit ({max_iters}) before completing the task. "
                "Please try again with a more specific request."
            )
        _llm_t = time.time()
        print(f"[governance] LLM call #{_iter} …")
        response = model_with_tools.invoke(messages)
        print(f"[governance] LLM call #{_iter} done in {time.time()-_llm_t:.1f}s")
        messages.append(response)

        if response.tool_calls:
            # Separate cached hits from calls that need to run.
            cached_results: dict[str, str] = {}
            to_run: list[tuple] = []  # (tc, call_key)
            for tc in response.tool_calls:
                call_key = f"{tc['name']}:{json.dumps(tc['args'], sort_keys=True)}"
                if call_key in _call_cache:
                    print(f"[governance] DUPLICATE skipped: {tc['name']} — returning cached result")
                    # Do NOT echo the full tool output — the model already has it in context
                    # and echoing a large blob (e.g. a DAG file) causes the model to output
                    # the raw content verbatim instead of synthesising a response.
                    cached_results[tc["id"]] = (
                        f"[duplicate call skipped — {tc['name']} with these arguments was already called "
                        f"and the result is already in your context. Do not output raw tool results; "
                        f"use what you already know to answer the user.]"
                    )
                else:
                    to_run.append((tc, call_key))

            # Run non-cached tools concurrently.
            fresh_results: dict[str, tuple[str, str]] = {}  # id -> (result, call_key)
            if to_run:
                _batch_t = time.time()
                with ThreadPoolExecutor(max_workers=len(to_run)) as pool:
                    futures = {
                        pool.submit(tools_by_name[tc["name"]].invoke, tc["args"]): (tc, call_key)
                        for tc, call_key in to_run
                    }
                    for future in as_completed(futures):
                        tc, call_key = futures[future]
                        try:
                            result = str(future.result())
                        except Exception as exc:
                            result = f"Tool error: {exc}"
                        fresh_results[tc["id"]] = (result, call_key)
                print(f"[governance] tool batch ({len(to_run)} calls) done in {time.time()-_batch_t:.1f}s")

            # Append ToolMessages in original order so the LLM sees them correctly.
            for tc in response.tool_calls:
                if tc["id"] in cached_results:
                    messages.append(ToolMessage(content=cached_results[tc["id"]], tool_call_id=tc["id"]))
                else:
                    result, call_key = fresh_results[tc["id"]]
                    _call_cache[call_key] = result
                    print(f"[governance] tool_call: {tc['name']}({json.dumps(tc['args'])[:120]})")
                    print(f"[governance] tool_result ({tc['name']}): {result[:200]}")
                    messages.append(ToolMessage(content=result, tool_call_id=tc["id"]))
                    if tc["name"] == "openmetadata_api":
                        _log_om_write(mem, tc)
            # Persist after every tool batch so no governance actions are lost on crash
            save_memory(mem)
        else:
            # No more tool calls — return the final text response to the caller
            print(f"[governance] run_agent DONE in {time.time()-_t0:.1f}s ({_iter} LLM calls) — {str(response.content)[:200]!r}")
            LAST_RUN_MESSAGES[:] = serialize_lc_messages(messages)
            return str(response.content)


def run_agent_task(task: str, params: Optional[dict] = None, context: Optional[dict] = None) -> dict:
    """
    Programmatic API for orchestrator calls using a structured task/params pattern.

    The orchestrator dispatches governance work as named tasks (e.g.
    ``"classify_table"``, ``"register_lineage"``, ``"run_quality_check"``)
    with typed parameters and optional context from other agents.  This function
    converts that structured input into a single natural-language prompt and
    delegates to ``run_agent``, which runs the full agentic loop.

    The task/params/context dispatch pattern lets the orchestrator call the
    governance agent in a uniform way without knowing the internal prompt
    structure.  The resulting dict ``{"status": "ok", "task": ..., "result": ...}``
    gives the orchestrator a structured envelope it can inspect or log.

    Args:
        task:    short description of the governance task to execute
                 (e.g. "classify all tables in the gdelt schema").
        params:  structured parameters relevant to the task
                 (e.g. {"schema": "gdelt", "level": "L2"}).
        context: additional context from other agents or the orchestrator
                 (e.g. {"triggered_by": "ingestion_agent", "run_id": "..."}).

    Returns:
        A dict with keys: status ("ok"), task (echo), result (agent response string).
    """
    params = params or {}
    context = context or {}
    # Build a structured prompt that gives the model all the information it
    # needs to execute the task autonomously without further clarification.
    prompt = (
        "You are executing a governance subtask from the orchestrator.\n"
        f"Task: {task}\n"
        f"Params: {json.dumps(params, ensure_ascii=True)}\n"
        f"Context: {json.dumps(context, ensure_ascii=True)}\n"
        "Return a concise governance result with findings and caveats."
    )
    result = run_agent(prompt)
    return {"status": "ok", "task": task, "result": result}


# ── Main ───────────────────────────────────────────────────────────────────────
#
# When run directly (``python agent_governance.py``), start the interactive REPL.
# When imported as a module (by the orchestrator or other agents), only the
# ``run_agent`` and ``run_agent_task`` functions are used.

try:
    from agents.a2a_kafka_communication import kafka_worker as _kafka_worker, send_to_orchestrator as _send
except ModuleNotFoundError:
    from a2a_kafka_communication import kafka_worker as _kafka_worker, send_to_orchestrator as _send

def kafka_worker() -> None:
    _kafka_worker("governance", run_agent_task)

def send_to_orchestrator(event_type: str, payload: dict) -> None:
    _send("governance", event_type, payload)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "worker":
        kafka_worker()
    else:
        run_governance_session()
