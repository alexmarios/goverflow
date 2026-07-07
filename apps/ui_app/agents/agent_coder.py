"""
Coder Agent
-----------
Autonomous file-editing agent for Python source files and Airflow DAGs.

Responsibilities:
  - Create and update .py files in allowed project directories
  - Always backs up every file before overwriting it (microsecond timestamp, auto-pruned)
  - Validates Python syntax after every write or patch
  - DAG files: AST-checks for catchup=False after every write
  - Works autonomously: reads, plans, edits, checks, reports

Allowed directories (configurable via CODER_ALLOWED_DIRS env var, colon-separated):
  local project root (resolved at runtime)
  DAGS_DIR and its parent directory (from access_hosts)

Configurable env vars:
  CODER_MAX_FILE_SIZE_MB   — max content size per write/patch (default 5 MB)
  CODER_BACKUP_KEEP_LAST_N — backups to retain per file (default 10)
  CODER_MAX_ITERS          — LLM iteration cap per run (default 20)
  CODER_ALLOWED_DIRS       — colon-separated allowed paths
"""

from __future__ import annotations

import ast
import json
import logging
import os
import shutil
import subprocess
import time
from dataclasses import dataclass, field as dc_field
from datetime import datetime
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from access_hosts import DAGS_DIR as _DAGS_DIR, REMOTE_USER as _REMOTE_USER, REMOTE_HOST as _REMOTE_HOST
from langchain.messages import HumanMessage, SystemMessage, ToolMessage
from langchain.tools import tool
from langchain_core.messages import BaseMessage

load_dotenv()

logger = logging.getLogger(__name__)

# ── Knowledge docs ─────────────────────────────────────────────────────────────
_AIRFLOW_DOCS: str = ""
_AIRFLOW_DOCS_PATH = os.path.join(os.path.dirname(__file__), "memory", "knowledge", "airflow-context7.md")
try:
    with open(_AIRFLOW_DOCS_PATH) as _f:
        _AIRFLOW_DOCS = _f.read().strip()
except FileNotFoundError as e:
    print(f"[coder] knowledge doc not found: {e}")

_GDELT_DOCS: str = ""
_GDELT_DOCS_PATH = os.path.join(os.path.dirname(__file__), "memory", "knowledge", "gdelt-manual.md")
try:
    with open(_GDELT_DOCS_PATH) as _f:
        _GDELT_DOCS = _f.read().strip()
except FileNotFoundError as e:
    print(f"[coder] knowledge doc not found: {e}")

try:
    from agents.model_config import build_model, serialize_lc_messages
except ModuleNotFoundError:
    from model_config import build_model, serialize_lc_messages

LAST_RUN_MESSAGES: list = []


# ── Configurable limits ────────────────────────────────────────────────────────

MAX_FILE_SIZE_MB: float = float(os.getenv("CODER_MAX_FILE_SIZE_MB", "5"))
MAX_FILE_SIZE_BYTES: int = int(MAX_FILE_SIZE_MB * 1024 * 1024)
BACKUP_KEEP_LAST_N: int = int(os.getenv("CODER_BACKUP_KEEP_LAST_N", "10"))
MAX_ITERS_DEFAULT: int = int(os.getenv("CODER_MAX_ITERS", "20"))
# Compact message history after this many LLM calls to avoid context overflow
COMPACT_AFTER_ITERS: int = 8
COMPACT_KEEP_TAIL: int = 6


# ── Structured result type ─────────────────────────────────────────────────────

@dataclass
class TaskResult:
    """Standardised result returned by every run_agent* entry point."""
    status: str         # "ok" | "max_iters" | "error"
    result: str         # final LLM response text
    duration_s: float
    iterations: int
    touched_paths: list[str] = dc_field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "result": self.result,
            "duration_s": self.duration_s,
            "iterations": self.iterations,
            "touched_paths": self.touched_paths,
        }


# ── Allowed directories ────────────────────────────────────────────────────────

def _default_allowed() -> list[Path]:
    env = os.getenv("CODER_ALLOWED_DIRS", "")
    if env:
        return [Path(p.strip()) for p in env.split(":") if p.strip()]
    return [
        Path(__file__).resolve().parent.parent,  # local project root (agents/, main.py, etc.)
        Path(_DAGS_DIR),                         # Pi DAGs dir — remote writes go via SCP
    ]

ALLOWED_DIRS: list[Path] = _default_allowed()
BACKUP_SUBDIR = "__backups__"

# SSH/SCP flags used for every remote call.
# StrictHostKeyChecking=no is required inside Docker (no persistent known_hosts).
_SSH_OPTS = [
    "-o", "StrictHostKeyChecking=no",
    "-o", "UserKnownHostsFile=/dev/null",
    "-o", "BatchMode=yes",
    "-o", "ConnectTimeout=10",
]


def _resolve(path: str) -> Path:
    return Path(path).expanduser().resolve()


def _is_remote(path: Path) -> bool:
    """True only when the path matches the remote-user pattern AND is not locally accessible.
    Handles the Docker case where the DAGs directory is bind-mounted at the same path."""
    if not bool(_REMOTE_HOST) or f"/home/{_REMOTE_USER}" not in str(path):
        return False
    # Walk up the tree — if any ancestor exists locally the path is mounted, not remote.
    p = Path(path)
    for _ in range(6):
        if p.exists():
            return False
        p = p.parent
    return True


def _is_allowed(path: Path) -> bool:
    """Check resolved and unresolved paths — macOS rewrites /home/<user> to
    /System/Volumes/Data/home/<user>, so the resolved form may not match the
    entry in ALLOWED_DIRS. Both are checked; write_file handles the actual
    remote-write failure gracefully via OSError."""
    for d in ALLOWED_DIRS:
        try:
            if path.resolve().is_relative_to(d.resolve()):
                return True
        except Exception as e:
            print(f"[coder] path resolve check failed: {e}")
        try:
            if path.is_relative_to(d):
                return True
        except Exception as e:
            print(f"[coder] path relative check failed: {e}")
    return False


def _validate_pattern(pattern: str) -> bool:
    """Reject glob patterns that contain path separators or .. traversal."""
    return "/" not in pattern and os.sep not in pattern and ".." not in pattern


def _backup(path: Path) -> str:
    """Copy a file to __backups__ with microsecond-resolution timestamp; prune old copies."""
    backup_dir = path.parent / BACKUP_SUBDIR
    backup_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    dest = backup_dir / f"{path.name}.{ts}.bak"
    shutil.copy2(path, dest)
    if BACKUP_KEEP_LAST_N > 0:
        existing = sorted(backup_dir.glob(f"{path.name}.*.bak"))
        for old in existing[:-BACKUP_KEEP_LAST_N]:
            try:
                old.unlink()
            except Exception as e:
                print(f"[coder] failed to delete old backup {old}: {e}")
    return str(dest)


# ── Airflow DAG safety ─────────────────────────────────────────────────────────

def _check_dag_catchup(path: Path) -> list[str]:
    """Walk the AST and return warnings for DAG() calls missing or having catchup=True."""
    warnings: list[str] = []
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError as e:
        print(f"[coder] SyntaxError parsing DAG {path}: {e}")
        return []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = ""
        if isinstance(node.func, ast.Name):
            fn = node.func.id
        elif isinstance(node.func, ast.Attribute):
            fn = node.func.attr
        if fn != "DAG":
            continue
        kw_names = {kw.arg for kw in node.keywords}
        if "catchup" not in kw_names:
            warnings.append(
                f"line {node.lineno}: DAG() missing catchup=False — "
                "omitting it enables historical backfill runs"
            )
        else:
            for kw in node.keywords:
                if (kw.arg == "catchup"
                        and isinstance(kw.value, ast.Constant)
                        and kw.value.value is True):
                    warnings.append(
                        f"line {node.lineno}: DAG() has catchup=True — change to False"
                    )
    return warnings


# ── LLM helpers ────────────────────────────────────────────────────────────────

def _invoke_with_retry(mdl, messages: list[BaseMessage], max_attempts: int = 3):
    """Call mdl.invoke() with exponential backoff on transient failures."""
    for attempt in range(max_attempts):
        try:
            return mdl.invoke(messages)
        except Exception as exc:
            if attempt == max_attempts - 1:
                raise
            wait = 2 ** attempt
            logger.warning(
                f"[coder] LLM invoke failed (attempt {attempt + 1}/{max_attempts}): "
                f"{exc}; retrying in {wait}s"
            )
            time.sleep(wait)


def _maybe_compact(messages: list[BaseMessage], iteration: int) -> list[BaseMessage]:
    """After COMPACT_AFTER_ITERS, trim middle messages to stay within context limits.

    Keeps: SystemMessage(s) + original HumanMessage + last COMPACT_KEEP_TAIL messages.
    This avoids splitting an AIMessage from its ToolMessage responses because the
    tail always ends at a complete exchange boundary.
    """
    if iteration < COMPACT_AFTER_ITERS:
        return messages
    system_msgs = [m for m in messages if isinstance(m, SystemMessage)]
    non_system = [m for m in messages if not isinstance(m, SystemMessage)]
    if len(non_system) <= COMPACT_KEEP_TAIL:
        return messages
    tail = non_system[-COMPACT_KEEP_TAIL:]
    compacted: list[BaseMessage] = list(system_msgs)
    first_human = next((m for m in non_system if isinstance(m, HumanMessage)), None)
    if first_human is not None and not any(m is first_human for m in tail):
        compacted.append(first_human)
    compacted.extend(tail)
    logger.debug(
        f"[coder] compacted {len(messages)} → {len(compacted)} messages at iteration {iteration}"
    )
    return compacted


# ── Tools ──────────────────────────────────────────────────────────────────────

@tool
def read_file(path: str) -> str:
    """
    Read the full content of a file.
    Always read the current state of a file before editing it.
    Args:
        path: absolute path to the file
    """
    p = _resolve(path)
    if not _is_allowed(p):
        return json.dumps({"error": f"Path not in allowed directories: {p}"})
    if _is_remote(p):
        if not _REMOTE_USER or not _REMOTE_HOST:
            return json.dumps({"error": "Remote path but REMOTE_USER/REMOTE_HOST not configured."})
        _r = subprocess.run(
            ["ssh"] + _SSH_OPTS + [f"{_REMOTE_USER}@{_REMOTE_HOST}", f"cat '{path}' 2>/dev/null || echo __NOT_FOUND__"],
            capture_output=True, text=True, timeout=15,
        )
        if _r.returncode != 0 or "__NOT_FOUND__" in _r.stdout:
            return json.dumps({"path": path, "content": None, "note": "File not found on remote host."})
        content = _r.stdout
        return json.dumps({"path": path, "content": content, "lines": content.count("\n") + 1})
    if not p.exists():
        return json.dumps({"error": f"File not found: {p}"})
    try:
        content = p.read_text(encoding="utf-8")
        return json.dumps({"path": str(p), "content": content, "lines": content.count("\n") + 1})
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def write_file(path: str, content: str) -> str:
    """
    Write content to a file. Creates the file if it does not exist.
    Existing files are automatically backed up before overwriting.
    Python files are syntax-checked; DAG files are also checked for catchup=False.
    Use patch_file for targeted edits to existing files — it is faster and safer.
    Args:
        path:    absolute path to the file
        content: full file content to write
    """
    p = _resolve(path)
    if not _is_allowed(p):
        return json.dumps({"error": f"Path not in allowed directories: {p}"})
    size = len(content.encode("utf-8"))
    if size > MAX_FILE_SIZE_BYTES:
        return json.dumps({
            "error": (
                f"Content size {size / 1024 / 1024:.1f} MB exceeds "
                f"limit {MAX_FILE_SIZE_MB} MB"
            )
        })
    if _is_remote(p):
        # Path lives on the Pi — deploy via SCP using a temp file; never touch dag_staging.
        if not _REMOTE_USER or not _REMOTE_HOST:
            return json.dumps({"error": "Remote path but REMOTE_USER/REMOTE_HOST not configured."})
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w", suffix=p.suffix, delete=False, encoding="utf-8") as _tmp:
            _tmp.write(content)
            _tmp_path = _tmp.name
        try:
            _scp = subprocess.run(
                ["scp"] + _SSH_OPTS + [_tmp_path, f"{_REMOTE_USER}@{_REMOTE_HOST}:{path}"],
                capture_output=True, text=True, timeout=30,
            )
        finally:
            Path(_tmp_path).unlink(missing_ok=True)
        if _scp.returncode == 0:
            return json.dumps({"status": "deployed_via_scp", "remote_path": path})
        return json.dumps({
            "status": "error",
            "message": f"SCP failed — file NOT saved anywhere. Fix SSH auth first.",
            "scp_error": _scp.stderr.strip(),
            "hint": f"Run: ssh-copy-id {_REMOTE_USER}@{_REMOTE_HOST}",
        })
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        backup_path = _backup(p) if p.exists() else None
        p.write_text(content, encoding="utf-8")
    except OSError as _oe:
        return json.dumps({"error": f"Cannot write {p}: {_oe}"})
    result: dict = {"status": "written", "path": str(p)}
    if backup_path:
        result["backup"] = backup_path
    if p.suffix == ".py":
        check = subprocess.run(
            ["python3", "-m", "py_compile", str(p)],
            capture_output=True, text=True,
        )
        if check.returncode == 0:
            result["syntax"] = "ok"
            if "dags" in str(p).lower():
                dag_warn = _check_dag_catchup(p)
                if dag_warn:
                    result["dag_warnings"] = dag_warn
        else:
            result["syntax"] = "error"
            result["syntax_detail"] = check.stderr.strip()
    return json.dumps(result)


@tool
def patch_file(path: str, old_str: str, new_str: str) -> str:
    """
    Apply a targeted string replacement in a file without a full rewrite.
    Prefer this over write_file for edits to existing files — fewer tokens,
    cleaner diffs, lower risk of accidental data loss.
    old_str must appear EXACTLY ONCE in the file; include 2-3 lines of
    surrounding context to make it unique if needed.
    The file is backed up before modification. If the patch introduces a
    syntax error in a .py file, the original is automatically restored.
    Args:
        path:    absolute path to the file
        old_str: exact string to replace (must be unique in the file)
        new_str: replacement string
    """
    import tempfile
    p = _resolve(path)
    if not _is_allowed(p):
        return json.dumps({"error": f"Path not in allowed directories: {p}"})

    if _is_remote(p):
        # Remote file: fetch via SSH, apply patch in memory, deploy via SCP.
        if not _REMOTE_USER or not _REMOTE_HOST:
            return json.dumps({"error": "Remote path but REMOTE_USER/REMOTE_HOST not configured."})
        _r = subprocess.run(
            ["ssh"] + _SSH_OPTS + [f"{_REMOTE_USER}@{_REMOTE_HOST}", f"cat '{path}'"],
            capture_output=True, text=True, timeout=15,
        )
        if _r.returncode != 0:
            return json.dumps({"error": f"SSH read failed: {_r.stderr.strip()}"})
        content = _r.stdout
        count = content.count(old_str)
        if count == 0:
            return json.dumps({"error": "old_str not found in remote file — check exact whitespace"})
        if count > 1:
            return json.dumps({"error": f"old_str appears {count} times — add more context lines"})
        new_content = content.replace(old_str, new_str, 1)
        # Syntax-check locally before deploying
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as _tmp:
            _tmp.write(new_content)
            _tmp_path = _tmp.name
        try:
            _chk = subprocess.run(["python3", "-m", "py_compile", _tmp_path], capture_output=True, text=True)
            if _chk.returncode != 0:
                return json.dumps({"error": "Syntax error in patched content — NOT deployed.", "detail": _chk.stderr.strip()})
            # Backup on remote then deploy
            subprocess.run(["ssh"] + _SSH_OPTS + [f"{_REMOTE_USER}@{_REMOTE_HOST}", f"cp '{path}' '{path}.bak' 2>/dev/null; true"], timeout=10)
            _scp = subprocess.run(
                ["scp"] + _SSH_OPTS + [_tmp_path, f"{_REMOTE_USER}@{_REMOTE_HOST}:{path}"],
                capture_output=True, text=True, timeout=30,
            )
        finally:
            Path(_tmp_path).unlink(missing_ok=True)
        if _scp.returncode == 0:
            return json.dumps({"status": "deployed_via_scp", "remote_path": path, "syntax": "ok"})
        return json.dumps({
            "status": "error",
            "message": "SCP failed — file NOT saved anywhere. Fix SSH auth first.",
            "scp_error": _scp.stderr.strip(),
            "hint": f"Run: ssh-copy-id {_REMOTE_USER}@{_REMOTE_HOST}",
        })

    if not p.exists():
        return json.dumps({"error": f"File not found: {p}"})
    try:
        content = p.read_text(encoding="utf-8")
    except Exception as e:
        return json.dumps({"error": str(e)})
    count = content.count(old_str)
    if count == 0:
        return json.dumps({"error": "old_str not found — check exact whitespace and indentation"})
    if count > 1:
        return json.dumps({
            "error": (
                f"old_str appears {count} times — extend it with more surrounding "
                "lines to make it unique"
            )
        })
    new_content = content.replace(old_str, new_str, 1)
    new_size = len(new_content.encode("utf-8"))
    if new_size > MAX_FILE_SIZE_BYTES:
        return json.dumps({"error": f"Patched content {new_size / 1024 / 1024:.1f} MB exceeds limit"})
    try:
        backup_path = _backup(p)
        p.write_text(new_content, encoding="utf-8")
    except OSError as _oe:
        return json.dumps({"error": f"Cannot write {p}: {_oe}"})
    result: dict = {"status": "patched", "path": str(p), "backup": backup_path}
    if p.suffix == ".py":
        check = subprocess.run(
            ["python3", "-m", "py_compile", str(p)],
            capture_output=True, text=True,
        )
        if check.returncode == 0:
            result["syntax"] = "ok"
            if "dags" in str(p).lower():
                dag_warn = _check_dag_catchup(p)
                if dag_warn:
                    result["dag_warnings"] = dag_warn
        else:
            result["syntax"] = "error"
            result["syntax_detail"] = check.stderr.strip()
            shutil.copy2(backup_path, p)
            result["status"] = "reverted"
            result["note"] = "Syntax error after patch — original file restored from backup"
    return json.dumps(result)


@tool
def list_directory(path: str, pattern: str = "*") -> str:
    """
    List files and subdirectories inside a directory.
    Args:
        path:    absolute path to the directory
        pattern: glob pattern with no path separators (default "*")
    """
    p = _resolve(path)
    if not _is_allowed(p):
        return json.dumps({"error": f"Path not in allowed directories: {p}"})
    if _is_remote(p):
        if not _REMOTE_USER or not _REMOTE_HOST:
            return json.dumps({"error": "Remote path but REMOTE_USER/REMOTE_HOST not configured."})
        if not _validate_pattern(pattern):
            return json.dumps({"error": "Pattern must not contain path separators or '..'"})
        _name_filter = f"-name '{pattern}'" if pattern != "*" else ""
        _r = subprocess.run(
            ["ssh"] + _SSH_OPTS + [f"{_REMOTE_USER}@{_REMOTE_HOST}",
             f"find '{path}' -maxdepth 1 -mindepth 1 {_name_filter} -printf '%f\\t%y\\t%s\\n' 2>/dev/null"],
            capture_output=True, text=True, timeout=15,
        )
        if _r.returncode != 0 and not _r.stdout:
            return json.dumps({"error": f"SSH listing failed: {_r.stderr.strip()}"})
        entries = []
        for _line in _r.stdout.splitlines():
            _parts = _line.strip().split("\t")
            if not _parts or not _parts[0] or _parts[0] == BACKUP_SUBDIR:
                continue
            entries.append({
                "name": _parts[0],
                "type": "dir" if len(_parts) > 1 and _parts[1] == "d" else "file",
                "size": int(_parts[2]) if len(_parts) > 2 and _parts[2].isdigit() else None,
            })
        entries.sort(key=lambda e: e["name"])
        return json.dumps({"path": str(p), "entries": entries, "count": len(entries)})
    if not p.is_dir():
        return json.dumps({"error": f"Not a directory: {p}"})
    if not _validate_pattern(pattern):
        return json.dumps({"error": "Pattern must not contain path separators or '..'"})
    try:
        entries = [
            {
                "name": item.name,
                "type": "dir" if item.is_dir() else "file",
                "size": item.stat().st_size if item.is_file() else None,
            }
            for item in sorted(p.glob(pattern))
        ]
        return json.dumps({"path": str(p), "entries": entries, "count": len(entries)})
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def search_files(directory: str, pattern: str) -> str:
    """
    Recursively find files matching a glob pattern inside a directory.
    Returns up to 100 matches; 'truncated' is true when more exist.
    Example: search_files(_DAGS_DIR, "*.py")
    Args:
        directory: absolute path to start searching from
        pattern:   glob pattern with no path separators, e.g. "*.py" or "gdelt_*.py"
    """
    d = _resolve(directory)
    if not _is_allowed(d):
        return json.dumps({"error": f"Path not in allowed directories: {d}"})
    if _is_remote(d):
        if not _REMOTE_USER or not _REMOTE_HOST:
            return json.dumps({"error": "Remote path but REMOTE_USER/REMOTE_HOST not configured."})
        if not _validate_pattern(pattern):
            return json.dumps({"error": "Pattern must not contain path separators or '..'"})
        _r = subprocess.run(
            ["ssh"] + _SSH_OPTS + [f"{_REMOTE_USER}@{_REMOTE_HOST}",
             f"find '{directory}' -name '{pattern}' -type f 2>/dev/null | grep -v '{BACKUP_SUBDIR}' | head -100"],
            capture_output=True, text=True, timeout=30,
        )
        if _r.returncode != 0 and not _r.stdout:
            return json.dumps({"error": f"SSH search failed: {_r.stderr.strip()}"})
        matches = [m for m in _r.stdout.splitlines() if m.strip()]
        return json.dumps({
            "directory": str(d), "pattern": pattern,
            "matches": matches, "count": len(matches), "truncated": len(matches) >= 100,
        })
    if not _validate_pattern(pattern):
        return json.dumps({"error": "Pattern must not contain path separators or '..'"})
    try:
        all_matches = [str(p) for p in d.rglob(pattern) if BACKUP_SUBDIR not in p.parts]
        truncated = len(all_matches) > 100
        return json.dumps({
            "directory": str(d),
            "pattern": pattern,
            "matches": all_matches[:100],
            "count": len(all_matches[:100]),
            "truncated": truncated,
        })
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def run_syntax_check(path: str) -> str:
    """
    Check Python syntax of a .py file without running it.
    Returns "ok" or the error message.
    Args:
        path: absolute path to the Python file
    """
    p = _resolve(path)
    if not _is_allowed(p):
        return json.dumps({"error": f"Path not in allowed directories: {p}"})
    if not p.exists():
        return json.dumps({"error": f"File not found: {p}"})
    check = subprocess.run(
        ["python3", "-m", "py_compile", str(p)],
        capture_output=True, text=True,
    )
    if check.returncode == 0:
        return json.dumps({"path": str(p), "syntax": "ok"})
    return json.dumps({"path": str(p), "syntax": "error", "detail": check.stderr.strip()})


@tool
def create_directory(path: str) -> str:
    """
    Create a directory (and any missing parents).
    Args:
        path: absolute path to create
    """
    p = _resolve(path)
    if not _is_allowed(p):
        return json.dumps({"error": f"Path not in allowed directories: {p}"})
    try:
        p.mkdir(parents=True, exist_ok=True)
        return json.dumps({"status": "created", "path": str(p)})
    except Exception as e:
        return json.dumps({"error": str(e)})


tools = [
    read_file, write_file, patch_file,
    list_directory, search_files,
    run_syntax_check, create_directory,
]
tools_by_name = {t.name: t for t in tools}

# ── Lazy model initialization — build_model() is deferred until first use so
# tests can monkeypatch build_model before any agent call is made. ────────────

_model_with_tools = None


def _get_model():
    global _model_with_tools
    if _model_with_tools is None:
        _m = build_model("coder")
        _model_with_tools = _m.bind_tools(tools)
    return _model_with_tools


_dags_dir    = str(_DAGS_DIR)
_dags_parent = str(Path(_DAGS_DIR).parent)
_proj_root   = str(Path(__file__).resolve().parent.parent)

SYSTEM_PROMPT = SystemMessage(content=f"""
You are the Coder Agent in a multi-agent data analytics system.

## Scope
Create and edit Python source files: Airflow DAGs, agent modules, configuration files,
and utility scripts. You work within approved project directories only.

## Allowed directories
- {_proj_root}   (agent modules, config — files exist locally)
- {_dags_dir}    (Airflow DAG files — lives on the remote Raspberry Pi)
- {_dags_parent} (Docker configs — lives on the remote Raspberry Pi)

## Remote DAG files — IMPORTANT
The DAGs directory `{_dags_dir}` is on a remote Raspberry Pi.
- **Always use the real DAGs path** (`{_dags_dir}/filename.py`) for all tool calls.
- `read_file` fetches the file from the Pi via SSH — you will get the real content.
- `patch_file` reads from the Pi, applies the change, syntax-checks locally, then SCPs back.
- `write_file` syntax-checks locally then SCPs to the Pi.
- There is NO local staging directory. If a tool returns `"status": "error"`, report it
  to the user — do not fall back to writing anywhere else.
- A successful deploy shows `"status": "deployed_via_scp"` in the tool result.

## Workflow — always follow this order
1. **Read first**: use read_file or list_directory to understand the current state
   before writing anything. Never write blindly.
2. **Plan**: think about what changes are needed and why.
3. **Edit surgically**: prefer patch_file for targeted changes to existing files.
   Use write_file only when creating new files or doing a complete rewrite.
4. **Verify**: use run_syntax_check on every .py file you write or patch.
5. **Report**: summarise what was changed, the backup location, and the syntax result.
   Include the list of files touched.

## patch_file vs write_file
- Use **patch_file** when editing an existing file — it is faster, uses fewer tokens,
  and produces a cleaner diff. Supply 2-3 lines of surrounding context in old_str
  to ensure uniqueness.
- Use **write_file** only when creating a new file or when changes are so extensive
  that a full rewrite is cleaner than a series of patches.

## Code quality rules
- Preserve existing imports, class structure, and public API unless explicitly asked.
- Match the file's existing style (indentation, docstrings, naming conventions).
- For Airflow DAGs: always set `catchup=False` unless explicitly required.
- Never delete files — rewrite or leave them intact.
- Never write credentials or secrets into source files.

## Autonomy
Act immediately on clear requests. Do not ask for confirmation unless the change is
irreversible and ambiguous. Always report the backup path so changes can be rolled back.
""")


# ── Agent loop ─────────────────────────────────────────────────────────────────

# Tools that produce a "path" in their result and count as file touches
_TOUCH_TOOLS = frozenset(("write_file", "patch_file", "read_file"))


def run_agent(request: str, max_iters: int = MAX_ITERS_DEFAULT) -> TaskResult:
    """Run the coder agent for a free-text request and return a TaskResult."""
    messages: list[BaseMessage] = [SYSTEM_PROMPT]
    if _AIRFLOW_DOCS:
        messages.append(SystemMessage(content=f"## Airflow reference\n\n{_AIRFLOW_DOCS}"))
    if _GDELT_DOCS:
        messages.append(SystemMessage(content=f"## GDELT GKG reference\n\n{_GDELT_DOCS}"))
    messages.append(HumanMessage(content=request))
    t0 = time.time()
    iteration = 0
    touched: list[str] = []
    first_line = next((ln.strip() for ln in request.splitlines() if ln.strip()), request[:80])
    logger.info(f"[coder] run_agent START — {first_line!r}")

    while True:
        iteration += 1
        if iteration > max_iters:
            last = str(messages[-1].content) if messages else ""
            logger.warning(f"[coder] max_iters={max_iters} reached after {time.time()-t0:.1f}s")
            return TaskResult(
                status="max_iters",
                result=last,
                duration_s=round(time.time() - t0, 2),
                iterations=iteration - 1,
                touched_paths=touched,
            )

        messages = _maybe_compact(messages, iteration)

        llm_t = time.time()
        logger.debug(f"[coder] LLM call #{iteration} …")
        response = _invoke_with_retry(_get_model(), messages)
        logger.info(f"[coder] LLM call #{iteration} done in {time.time()-llm_t:.1f}s")
        messages.append(response)

        if response.tool_calls:
            for tc in response.tool_calls:
                tool_t = time.time()
                logger.debug(f"[coder] tool_call: {tc['name']}({json.dumps(tc['args'])[:120]})")
                result = tools_by_name[tc["name"]].invoke(tc["args"])
                logger.info(
                    f"[coder] tool_result ({tc['name']}): "
                    f"{str(result)[:200]}  [{time.time()-tool_t:.1f}s]"
                )
                # Track which files were touched for the lineage record
                if tc["name"] in _TOUCH_TOOLS:
                    try:
                        p = json.loads(result).get("path")
                        if p and p not in touched:
                            touched.append(p)
                    except Exception as e:
                        print(f"[coder] failed to parse tool result for path tracking: {e}")
                messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))
        else:
            duration = round(time.time() - t0, 2)
            logger.info(
                f"[coder] run_agent DONE in {duration}s "
                f"({iteration} LLM calls, {len(touched)} file(s) touched)"
            )
            LAST_RUN_MESSAGES[:] = serialize_lc_messages(messages)
            return TaskResult(
                status="ok",
                result=str(response.content),
                duration_s=duration,
                iterations=iteration,
                touched_paths=touched,
            )


def run_agent_task(task: str, params: Optional[dict] = None, context: Optional[dict] = None) -> dict:
    """Orchestrator-compatible task API. Returns a plain dict."""
    params = params or {}
    context = context or {}
    prompt = (
        f"You are executing a coding subtask from the orchestrator.\n"
        f"Task: {task}\n"
        f"Params: {json.dumps(params, ensure_ascii=True)}\n"
        f"Context: {json.dumps(context, ensure_ascii=True)}\n"
        "Complete the task, verify syntax, and report what was done. "
        "Include the list of files you touched."
    )
    tr = run_agent(prompt)
    return {
        "status": tr.status,
        "task": task,
        "result": tr.result,
        "duration_s": tr.duration_s,
        "iterations": tr.iterations,
        "touched_paths": tr.touched_paths,
    }


def run_agent_chat(request: str) -> str:
    """Conversational entry point used by main.py direct-target calls."""
    logger.info("[coder] run_agent_chat start")
    tr = run_agent(request)
    logger.info(f"[coder] run_agent_chat DONE in {tr.duration_s}s")
    return tr.result


try:
    from agents.a2a_kafka_communication import kafka_worker as _kafka_worker, send_to_orchestrator as _send
except ModuleNotFoundError:
    from a2a_kafka_communication import kafka_worker as _kafka_worker, send_to_orchestrator as _send

def kafka_worker() -> None:
    _kafka_worker("coder", run_agent_task)

def send_to_orchestrator(event_type: str, payload: dict) -> None:
    _send("coder", event_type, payload)

if __name__ == "__main__":
    kafka_worker()
