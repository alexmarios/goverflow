"""
Simple Multi-Agent Chat UI
==========================

Runs a small FastAPI server that serves a single-page chat interface.
The UI allows selecting one agent (or all agents) and sending a message.
"""

from __future__ import annotations

import asyncio
import concurrent.futures
import json as _json
import threading
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any, Literal

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel, Field

from agents.agent_analyst import run_agent as analyst_run_agent
from agents.agent_analyst import LAST_RUN_MESSAGES as _analyst_lc
from agents.agent_analyst import kafka_worker as _analyst_kafka_worker
from agents.agent_coder import run_agent_chat as coder_run_chat
from agents.agent_coder import LAST_RUN_MESSAGES as _coder_lc
from agents.agent_coder import kafka_worker as _coder_kafka_worker
from agents.agent_governance import run_agent as governance_run_agent
from agents.agent_governance import LAST_RUN_MESSAGES as _governance_lc
from agents.agent_governance import kafka_worker as _governance_kafka_worker
from agents.agent_ingestion import run_agent_chat as ingestion_run_chat
from agents.agent_ingestion import LAST_RUN_MESSAGES as _ingestion_lc
from agents.agent_ingestion import kafka_worker as _ingestion_kafka_worker
from agents.agent_orchestrator import run_orchestrator_agent_with_trace
from agents.a2a_kafka_communication import dispatch_and_wait as _a2a_dispatch
from agents.model_config import build_model, invoke_with_retry as _model_invoke_with_retry


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """Start each specialist agent's A2A Kafka consumer as a daemon thread.

    This makes every agent listen on its agent.{name}.inbox topic so the
    Orchestrator can dispatch tasks over Kafka rather than direct function calls.
    Daemon threads die automatically when the uvicorn process exits.
    """
    workers = [
        ("analyst",    _analyst_kafka_worker),
        ("governance", _governance_kafka_worker),
        ("coder",      _coder_kafka_worker),
        ("ingestion",  _ingestion_kafka_worker),
    ]
    for name, fn in workers:
        t = threading.Thread(target=fn, daemon=True, name=f"a2a-{name}")
        t.start()
        print(f"[startup] A2A Kafka worker started: {name} → agent.{name}.inbox")
    yield


app = FastAPI(title="Multi-Agent Chat", lifespan=lifespan)
AGENT_TIMEOUT_SECONDS = 1200

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, description="User message for the selected agent")
    target: Literal["orchestrator", "analyst", "governance", "ingestion", "coder", "all"] = "orchestrator"
    session_id: str | None = None
    history: list[dict] | None = None  # [{role, agent, text}, ...] — last N turns from the UI


class DagApplyRequest(BaseModel):
    suggestions: str = Field(min_length=1, description="Suggestions text from a previous /api/dag-check call")


def _run_with_timeout(fn, *args, timeout_s: int = AGENT_TIMEOUT_SECONDS):
    """Run a blocking agent call with a hard timeout."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        fut = pool.submit(fn, *args)
        try:
            return fut.result(timeout=timeout_s)
        except concurrent.futures.TimeoutError:
            return f"Timed out after {timeout_s}s."
        except Exception as exc:
            return f"Failed: {exc}"


def _build_context(history: list[dict] | None, message: str) -> str:
    """Prepend the last ≤10 chat turns to the current message so agents have conversation context."""
    if not history:
        return message
    lines: list[str] = []
    for m in history[-10:]:
        role = m.get("role", "user")
        agent = m.get("agent", "")
        text = (m.get("text") or "")[:600].strip()
        if not text:
            continue
        if role == "user":
            lines.append(f"User: {text}")
        else:
            lines.append(f"{agent.capitalize()}: {text}")
    if not lines:
        return message
    return "Conversation so far:\n" + "\n".join(lines) + "\n\n---\n\nCurrent request: " + message


def _run_target(target: str, message: str, session_id: str | None, history: list[dict] | None = None) -> dict[str, Any]:
    results: list[dict[str, str]] = []
    traces: list[dict[str, Any]] = []
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    message_with_ctx = _build_context(history, message)

    def _trace_pair(agent: str, request_text: str, response_text: str, raw_lc: list | None = None) -> None:
        traces.append({
            "event": "chat_request",
            "from": "user", "to": agent,
            "timestamp": ts,
            "message": {"text": request_text},
        })
        resp_entry: dict[str, Any] = {
            "event": "chat_response",
            "from": agent, "to": "user",
            "timestamp": ts,
            "message": {"text": response_text},
        }
        if raw_lc:
            resp_entry["raw_lc"] = raw_lc
        traces.append(resp_entry)

    if target in ("orchestrator", "all"):
        orchestrator_result = _run_with_timeout(run_orchestrator_agent_with_trace, message, session_id)
        if isinstance(orchestrator_result, dict):
            resp_text = str(orchestrator_result.get("response", ""))
            results.append({"agent": "orchestrator", "text": resp_text})
            trace_items = orchestrator_result.get("trace", [])
            if isinstance(trace_items, list):
                traces.extend(trace_items)
            _trace_pair("orchestrator", message, resp_text)
        else:
            resp_text = str(orchestrator_result)
            results.append({"agent": "orchestrator", "text": resp_text})
            _trace_pair("orchestrator", message, resp_text)

    if target in ("analyst", "all"):
        a2a = _a2a_dispatch("analyst", "chat", {"message": message_with_ctx}, timeout_ms=AGENT_TIMEOUT_SECONDS * 1000)
        analyst_text = str(a2a.get("result", a2a) if a2a else _run_with_timeout(analyst_run_agent, message_with_ctx))
        results.append({"agent": "analyst", "text": analyst_text})
        _trace_pair("analyst", message, analyst_text, raw_lc=list(_analyst_lc))

    if target in ("governance", "all"):
        a2a = _a2a_dispatch("governance", "chat", {"message": message_with_ctx}, timeout_ms=AGENT_TIMEOUT_SECONDS * 1000)
        governance_text = str(a2a.get("result", a2a) if a2a else _run_with_timeout(governance_run_agent, message_with_ctx))
        results.append({"agent": "governance", "text": governance_text})
        _trace_pair("governance", message, governance_text, raw_lc=list(_governance_lc))

    if target in ("ingestion", "all"):
        a2a = _a2a_dispatch("ingestion", "chat", {"message": message_with_ctx}, timeout_ms=AGENT_TIMEOUT_SECONDS * 1000)
        ingestion_result = str(a2a.get("result", a2a) if a2a else _run_with_timeout(ingestion_run_chat, message_with_ctx))
        results.append({"agent": "ingestion", "text": ingestion_result})
        _trace_pair("ingestion", message, ingestion_result, raw_lc=list(_ingestion_lc))

    if target in ("coder", "all"):
        a2a = _a2a_dispatch("coder", "chat", {"message": message_with_ctx}, timeout_ms=AGENT_TIMEOUT_SECONDS * 1000)
        coder_result = str(a2a.get("result", a2a) if a2a else _run_with_timeout(coder_run_chat, message_with_ctx))
        results.append({"agent": "coder", "text": coder_result})
        _trace_pair("coder", message, coder_result, raw_lc=list(_coder_lc))

    return {"responses": results, "traces": traces}


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Multi-Agent Console</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', system-ui, sans-serif;
      background: #080d1a;
      color: #e2e8f0;
      height: 100vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    /* Header */
    .hdr {
      background: #0f172a;
      border-bottom: 1px solid #1e293b;
      padding: 10px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
    }
    .hdr-left { display: flex; align-items: center; gap: 12px; }
    .hdr h1 { font-size: 16px; font-weight: 700; letter-spacing: -0.02em; }
    .hdr-sub { font-size: 12px; color: #475569; }
    .hdr-pills { display: flex; gap: 6px; }
    .pill {
      font-size: 11px; font-weight: 600; padding: 3px 10px;
      border-radius: 20px; letter-spacing: 0.03em;
    }
    .sidebar-toggle-btn {
      background: none; border: 1px solid #1e293b; color: #64748b;
      border-radius: 6px; padding: 5px 9px; cursor: pointer;
      font-size: 15px; line-height: 1; flex-shrink: 0;
    }
    .sidebar-toggle-btn:hover { background: #1e293b; color: #94a3b8; }

    /* App row */
    .app-row {
      display: flex;
      flex: 1;
      overflow: hidden;
    }

    /* Sessions sidebar */
    .sidebar {
      width: 220px;
      min-width: 220px;
      background: #0a1020;
      border-right: 1px solid #1e293b;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      transition: width 0.2s ease, min-width 0.2s ease;
      flex-shrink: 0;
    }
    .sidebar.collapsed { width: 0; min-width: 0; }
    .sidebar-hdr {
      padding: 10px 12px;
      border-bottom: 1px solid #1e293b;
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-shrink: 0;
    }
    .sidebar-title {
      font-size: 11px; font-weight: 700;
      color: #334155; text-transform: uppercase; letter-spacing: 0.06em;
      white-space: nowrap;
    }
    .new-chat-btn {
      background: #1d4ed8; color: #fff; border: none;
      border-radius: 6px; padding: 4px 10px;
      font-size: 12px; font-weight: 600; cursor: pointer;
      white-space: nowrap; flex-shrink: 0;
    }
    .new-chat-btn:hover { background: #1e40af; }
    .sessions-list { flex: 1; overflow-y: auto; padding: 6px; }
    .session-item {
      padding: 8px 10px; border-radius: 6px; cursor: pointer;
      border: 1px solid transparent; margin-bottom: 3px;
      transition: background 0.1s; position: relative;
    }
    .session-item:hover { background: #1e293b44; }
    .session-item.active { background: #1e3a8a22; border-color: #1e40af44; }
    .session-title {
      font-size: 12px; color: #94a3b8;
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
      font-weight: 500; padding-right: 18px;
    }
    .session-item.active .session-title { color: #93c5fd; }
    .session-date { font-size: 10px; color: #334155; margin-top: 2px; }
    .session-delete {
      position: absolute; right: 6px; top: 50%; transform: translateY(-50%);
      background: none; border: none; color: #334155;
      cursor: pointer; font-size: 15px; padding: 1px 3px;
      opacity: 0; transition: opacity 0.1s; line-height: 1;
    }
    .session-item:hover .session-delete { opacity: 1; }
    .session-delete:hover { color: #f87171; }
    .sessions-empty { font-size: 12px; color: #334155; padding: 16px 10px; text-align: center; }

    /* Layout */
    .main {
      display: grid;
      grid-template-columns: 1.45fr 1fr;
      flex: 1;
      overflow: hidden;
    }

    /* Chat panel */
    .chat-panel {
      display: flex;
      flex-direction: column;
      border-right: 1px solid #1e293b;
      overflow: hidden;
    }
    .chat-scroll {
      flex: 1;
      overflow-y: auto;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      scroll-behavior: smooth;
    }

    /* Bubbles */
    .bwrap { display: flex; flex-direction: column; }
    .bwrap.user { align-items: flex-end; }
    .bwrap.bot  { align-items: flex-start; }
    .bmeta { font-size: 11px; color: #475569; margin-bottom: 3px; padding: 0 4px; }
    .bubble {
      max-width: 90%;
      padding: 10px 14px;
      border-radius: 14px;
      font-size: 14px;
      line-height: 1.6;
    }
    .bubble.user {
      background: #1d4ed8;
      color: #dbeafe;
      border-bottom-right-radius: 4px;
    }
    .bubble.bot {
      background: #0f172a;
      border: 1px solid #1e293b;
      border-bottom-left-radius: 4px;
    }
    .bheader {
      display: flex; align-items: center; gap: 7px;
      margin-bottom: 8px; padding-bottom: 7px;
      border-bottom: 1px solid #1e293b;
    }
    .bdot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
    .bname { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; }

    /* Content inside bubble */
    pre.txt { white-space: pre-wrap; font-family: inherit; font-size: 14px; margin: 0; }
    .tbl-wrap { overflow-x: auto; margin: 6px 0; }
    table { border-collapse: collapse; width: 100%; font-size: 13px; }
    th, td { border: 1px solid #1e293b; padding: 6px 10px; text-align: left; }
    th { background: #1e293b; }

    /* Markdown elements rendered inside bot bubbles */
    .bubble h1,.bubble h2,.bubble h3,.bubble h4 {
      color: #e2e8f0; font-weight: 700; margin: 10px 0 4px;
      border-bottom: 1px solid #1e293b; padding-bottom: 3px;
    }
    .bubble h1 { font-size: 17px; }
    .bubble h2 { font-size: 15px; }
    .bubble h3 { font-size: 14px; }
    .bubble h4 { font-size: 13px; color: #94a3b8; }
    .bubble p  { margin: 4px 0; }
    .bubble ul, .bubble ol { margin: 4px 0 4px 18px; padding: 0; }
    .bubble li { margin: 2px 0; }
    .bubble strong { color: #f1f5f9; font-weight: 700; }
    .bubble em { color: #cbd5e1; font-style: italic; }
    .bubble code { background: #1e293b; border-radius: 4px; padding: 1px 5px; font-size: 13px; font-family: monospace; color: #7dd3fc; }
    .bubble pre.code-block { background: #1e293b; border-radius: 6px; padding: 10px 12px; overflow-x: auto; margin: 6px 0; }
    .bubble pre.code-block code { background: none; padding: 0; color: #7dd3fc; font-size: 13px; }
    .bubble blockquote { border-left: 3px solid #334155; margin: 6px 0; padding: 4px 10px; color: #94a3b8; }
    .bubble hr { border: none; border-top: 1px solid #1e293b; margin: 8px 0; }

    /* Input bar */
    .input-bar {
      padding: 10px 14px;
      border-top: 1px solid #1e293b;
      background: #0f172a;
      display: flex;
      align-items: center;
      gap: 8px;
      flex-shrink: 0;
    }
    .input-bar select {
      background: #080d1a; color: #e2e8f0;
      border: 1px solid #1e293b; border-radius: 8px;
      padding: 9px 10px; font-size: 13px; cursor: pointer;
    }
    .input-bar textarea {
      flex: 1;
      background: #080d1a; color: #e2e8f0;
      border: 1px solid #1e293b; border-radius: 8px;
      padding: 9px 14px; font-size: 14px;
      resize: none; overflow-y: auto;
      min-height: 38px; max-height: 160px;
      line-height: 1.5; font-family: inherit;
    }
    .input-bar textarea:focus { outline: none; border-color: #2563eb; }
    .send-btn {
      background: #2563eb; color: #fff; border: none;
      border-radius: 8px; padding: 9px 20px;
      font-size: 14px; font-weight: 600; cursor: pointer;
    }
    .send-btn:hover:not(:disabled) { background: #1d4ed8; }
    .send-btn:disabled { opacity: 0.4; cursor: not-allowed; }
    .status-txt { font-size: 12px; color: #334155; white-space: nowrap; flex-shrink: 0; }

    /* Sequence panel */
    .seq-panel {
      display: flex;
      flex-direction: column;
      overflow: hidden;
      background: #080d1a;
    }
    .seq-hdr {
      padding: 10px 16px;
      border-bottom: 1px solid #1e293b;
      font-size: 11px; font-weight: 700;
      color: #334155; text-transform: uppercase; letter-spacing: 0.06em;
      flex-shrink: 0;
    }
    /* Agent node graph */
    .graph-section {
      padding: 10px 10px 8px;
      border-bottom: 1px solid #1e293b;
      flex-shrink: 0;
    }
    #agent-graph { width: 100%; height: auto; display: block; }
    .bg-edge { stroke: #1a2a45; stroke-width: 1; }

    /* Flow log */
    .flow-hdr {
      padding: 6px 12px;
      border-bottom: 1px solid #1e293b;
      font-size: 10px; font-weight: 700;
      color: #334155; text-transform: uppercase; letter-spacing: 0.06em;
      flex-shrink: 0; display: flex; align-items: center; gap: 6px;
    }
    .flow-scroll { flex: 1; overflow-y: auto; min-height: 0; padding: 6px; }
    .flow-card {
      padding: 8px 10px; border-radius: 6px;
      border: 1px solid #141f35; background: #090e1c;
      margin-bottom: 5px; cursor: pointer;
      transition: background 0.1s, border-color 0.1s;
    }
    .flow-card:hover { background: #0d1428; border-color: #2a3d5a; }
    .flow-card.sel { background: #0d1e3a; border-color: #1e40af55; }
    .flow-route {
      display: flex; align-items: center; gap: 5px; margin-bottom: 4px;
    }
    .flow-badge {
      font-size: 9px; font-weight: 700; text-transform: uppercase;
      letter-spacing: 0.05em; padding: 2px 5px; border-radius: 3px;
      white-space: nowrap; flex-shrink: 0;
    }
    .flow-line { flex: 1; height: 1px; }
    .flow-head { font-size: 9px; line-height: 1; flex-shrink: 0; }
    .flow-etype { font-size: 10px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

    /* Thinking dots — shown while agent is processing */
    .thinking-dots { display: flex; gap: 4px; align-items: center; height: 16px; }
    .thinking-dots span {
      width: 6px; height: 6px; border-radius: 50%; background: #334155;
      animation: dotBounce 1.2s infinite ease-in-out;
    }
    .thinking-dots span:nth-child(2) { animation-delay: 0.2s; }
    .thinking-dots span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes dotBounce {
      0%, 80%, 100% { transform: scale(0.8); background: #334155; }
      40% { transform: scale(1.2); background: #64748b; }
    }

    /* Streaming cursor — blinks at end of in-progress response */
    .stream-cursor {
      display: inline-block; width: 2px; height: 13px;
      background: #475569; margin-left: 2px;
      vertical-align: text-bottom;
      animation: blink 0.8s step-end infinite;
    }

    /* Empty state */
    .seq-empty {
      display: flex; flex-direction: column;
      align-items: center; justify-content: center;
      height: 120px; gap: 6px;
      color: #1e293b; font-size: 13px;
    }

    /* Payload panel */
    .payload {
      border-top: 1px solid #1e293b;
      background: #0a1020;
      flex-shrink: 0;
      display: flex;
      flex-direction: column;
      max-height: 340px;
    }
    .payload-hdr {
      display: flex; align-items: center;
      justify-content: space-between;
      padding: 8px 14px;
      border-bottom: 1px solid #1e293b;
      flex-shrink: 0;
    }
    .payload-title { font-size: 12px; display: flex; align-items: center; gap: 4px; }
    .payload-close {
      background: none; border: none;
      color: #334155; cursor: pointer; font-size: 18px;
      line-height: 1; padding: 0;
    }
    .payload-close:hover { color: #94a3b8; }
    .payload-body { overflow-y: auto; flex: 1; padding: 10px 14px; }
    .payload-body pre {
      font-size: 12px; color: #7dd3fc;
      white-space: pre-wrap;
      font-family: 'Fira Code', 'Cascadia Code', 'Consolas', monospace;
      margin: 0;
    }
    /* JSON tree */
    .json-tree { font-family: 'Fira Code','Cascadia Code','Consolas',monospace; font-size: 12px; line-height: 1.8; }
    .json-toggle { cursor: pointer; color: #475569; user-select: none; padding: 0 4px; font-size: 10px; }
    .json-toggle:hover { color: #94a3b8; }
    .json-indent { margin-left: 18px; border-left: 1px solid #1e293b; padding-left: 4px; }
    .json-key    { color: #93c5fd; }
    .json-str    { color: #86efac; }
    .json-num    { color: #fcd34d; }
    .json-bool   { color: #f9a8d4; }
    .json-null   { color: #64748b; font-style: italic; }
    .json-punc   { color: #475569; }
    .payload-raw-btn {
      background: none; border: 1px solid #1e293b; color: #475569;
      border-radius: 4px; padding: 2px 7px; font-size: 10px; cursor: pointer;
    }
    .payload-raw-btn:hover { color: #94a3b8; border-color: #334155; }
    /* Flow card */
    .flow-ts  { font-size: 9px; color: #1e293b; margin-left: auto; flex-shrink: 0; padding-left: 4px; }
    .flow-msg { font-size: 11px; color: #3d5068; overflow: hidden; margin-top: 3px;
                display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }
    .flow-json-pill { font-size: 9px; color: #334155; border: 1px solid #1e293b;
                      border-radius: 3px; padding: 1px 4px; font-family: monospace;
                      margin-left: 4px; flex-shrink: 0; }

    /* Auto session tab */
    .auto-tab {
      margin: 8px 6px 2px;
      padding: 9px 10px;
      border-radius: 7px;
      border: 1px solid #1e3a8a44;
      background: #0d1f3c;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      flex-shrink: 0;
      transition: background 0.1s;
    }
    .auto-tab:hover { background: #0f2545; }
    .auto-tab.active { border-color: #2563eb55; background: #0f2545; }
    .auto-tab.state-critical { border-color: #dc262666; background: #1f0d0d; animation: pulseTab 1.4s infinite; }
    @keyframes pulseTab { 0%,100% { border-color:#dc262666; } 50% { border-color:#dc2626bb; } }
    .auto-dot {
      width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0;
      transition: background 0.3s;
    }
    .auto-dot.idle     { background: #1e3a8a; }
    .auto-dot.checking { background: #2563eb; animation: blink 1s infinite; }
    .auto-dot.critical { background: #dc2626; animation: blink 0.7s infinite; }
    @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.25} }
    .auto-info { flex: 1; min-width: 0; }
    .auto-title { font-size: 12px; font-weight: 700; color: #93c5fd; white-space: nowrap; }
    .auto-sub   { font-size: 10px; color: #334155; margin-top: 1px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .auto-tab.state-critical .auto-sub { color: #f87171; }
    .auto-badge {
      background: #dc2626; color: #fff; border-radius: 10px;
      padding: 1px 5px; font-size: 10px; font-weight: 700; flex-shrink: 0;
    }
    .auto-run-btn {
      background: none; border: 1px solid #1e3a8a55; color: #3b82f6;
      border-radius: 4px; padding: 2px 6px; cursor: pointer;
      font-size: 11px; line-height: 1.4; flex-shrink: 0;
    }
    .auto-run-btn:hover { background: #1e3a8a33; }
    .auto-run-btn:disabled { opacity: 0.3; cursor: not-allowed; }
    .sidebar-divider { height: 1px; background: #1e293b; margin: 4px 6px 2px; }

    /* DAG Upgrade monitor tab */
    .dag-tab {
      margin: 2px 6px 8px;
      padding: 9px 10px;
      border-radius: 7px;
      border: 1px solid #06532244;
      background: #041a10;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      flex-shrink: 0;
      transition: background 0.1s;
    }
    .dag-tab:hover { background: #072a1a; }
    .dag-tab.active { border-color: #05966955; background: #072a1a; }
    .dag-tab.state-pending { border-color: #d9770066; background: #1a1200; animation: pulseTab 1.4s infinite; }
    .dag-dot.idle     { background: #065f46; }
    .dag-dot.checking { background: #10b981; animation: blink 1s infinite; }
    .dag-dot.pending  { background: #d97706; animation: blink 1s infinite; }
    .dag-dot.applying { background: #0891b2; animation: blink 0.7s infinite; }

    /* DAG suggestion action bar */
    .dag-action-bar {
      background: #041a10;
      border-bottom: 1px solid #065f46;
      padding: 9px 14px;
      display: flex;
      align-items: center;
      gap: 8px;
      flex-shrink: 0;
    }
    .dag-action-text { font-size: 12px; color: #6ee7b7; flex: 1; }
    .dag-apply-btn {
      background: #059669; color: #fff; border: none;
      border-radius: 6px; padding: 5px 14px;
      font-size: 12px; font-weight: 600; cursor: pointer; white-space: nowrap;
    }
    .dag-apply-btn:hover:not(:disabled) { background: #047857; }
    .dag-apply-btn:disabled { opacity: 0.4; cursor: not-allowed; }
    .dag-skip-btn {
      background: none; border: 1px solid #1e293b; color: #475569;
      border-radius: 6px; padding: 5px 10px;
      font-size: 12px; cursor: pointer; white-space: nowrap;
    }
    .dag-skip-btn:hover { background: #1e293b22; color: #94a3b8; }

    /* Critical banner */
    .critical-banner {
      background: #150505;
      border-bottom: 1px solid #7f1d1d;
      padding: 9px 14px;
      display: flex;
      align-items: center;
      gap: 8px;
      flex-shrink: 0;
      animation: pulseTab 1.4s infinite;
    }
    .critical-banner-icon { font-size: 15px; flex-shrink: 0; }
    .critical-banner-text { font-size: 12px; color: #fca5a5; flex: 1; }
    .critical-skip-btn {
      background: none; border: 1px solid #7f1d1d; color: #f87171;
      border-radius: 6px; padding: 5px 10px;
      font-size: 12px; cursor: pointer; white-space: nowrap; flex-shrink: 0;
    }
    .critical-skip-btn:hover { background: #7f1d1d33; color: #fca5a5; }

    @media (max-width: 860px) {
      .main { grid-template-columns: 1fr; grid-template-rows: 1fr 1fr; }
      .chat-panel { border-right: none; border-bottom: 1px solid #1e293b; }
      .hdr-pills { display: none; }
      .sidebar { display: none; }
    }
  </style>
</head>
<body>

<div class="hdr">
  <div class="hdr-left">
    <button class="sidebar-toggle-btn" id="sidebar-toggle" title="Toggle sessions panel">☰</button>
    <h1>Multi-Agent Console</h1>
    <span class="hdr-sub">GDELT Analytics &nbsp;·&nbsp; Orchestrator ▸ Analyst · Governance · Ingestion</span>
  </div>
  <div class="hdr-pills">
    <span class="pill" style="background:#1e3a8a22;color:#93c5fd;border:1px solid #1e40af44">Orchestrator</span>
    <span class="pill" style="background:#14532d22;color:#86efac;border:1px solid #16653444">Analyst</span>
    <span class="pill" style="background:#7c2d1222;color:#fdba74;border:1px solid #92400e44">Governance</span>
    <span class="pill" style="background:#3b076422;color:#c4b5fd;border:1px solid #4c1d9544">Ingestion</span>
    <span class="pill" style="background:#16434922;color:#67e8f9;border:1px solid #0e737744">Coder</span>
  </div>
</div>

<div class="app-row">

  <!-- Sessions sidebar -->
  <div class="sidebar" id="sidebar">
    <div class="sidebar-hdr">
      <span class="sidebar-title">Sessions</span>
      <button class="new-chat-btn" id="new-chat">+ New</button>
    </div>
    <!-- Auto monitor tab — always pinned at top -->
    <div class="auto-tab" id="auto-session-tab">
      <div class="auto-dot idle" id="auto-dot"></div>
      <div class="auto-info">
        <div class="auto-title">Auto Monitor</div>
        <div class="auto-sub" id="auto-sub">Starting…</div>
      </div>
      <span class="auto-badge" id="auto-badge" style="display:none">0</span>
      <button class="auto-run-btn" id="auto-run-btn" title="Run check now">▶</button>
    </div>
    <!-- DAG Upgrade monitor tab — pinned below Auto Monitor -->
    <div class="dag-tab" id="dag-session-tab">
      <div class="auto-dot dag-dot idle" id="dag-dot"></div>
      <div class="auto-info">
        <div class="auto-title" style="color:#6ee7b7">DAG Upgrade</div>
        <div class="auto-sub" id="dag-sub">Starting…</div>
      </div>
      <span class="auto-badge" id="dag-badge" style="display:none">0</span>
      <button class="auto-run-btn" id="dag-run-btn" title="Audit DAGs now">▶</button>
    </div>
    <div class="sidebar-divider"></div>
    <div class="sessions-list" id="sessions-list">
      <div class="sessions-empty">No saved sessions</div>
    </div>
  </div>

  <div class="main">

    <!-- Chat panel -->
    <div class="chat-panel">
      <div class="chat-scroll" id="chat"></div>
      <!-- Critical banner — shown only when auto monitor needs user input -->
      <div class="critical-banner" id="critical-banner" style="display:none">
        <span class="critical-banner-icon">⚠</span>
        <span class="critical-banner-text">Agent is awaiting your decision — review the message above and type your response below.</span>
        <button class="critical-skip-btn" id="critical-skip-btn">Skip</button>
      </div>
      <!-- DAG suggestion action bar — shown when coder has pending DAG improvements -->
      <div class="dag-action-bar" id="dag-action-bar" style="display:none">
        <span style="font-size:15px;flex-shrink:0">🔧</span>
        <span class="dag-action-text">Coder agent found DAG improvements — review above and apply?</span>
        <button class="dag-apply-btn" id="dag-apply-btn">Apply Changes</button>
        <button class="dag-skip-btn" id="dag-skip-btn">Skip</button>
      </div>
      <div class="input-bar">
        <select id="target">
          <option value="orchestrator">Orchestrator</option>
          <option value="analyst">Analyst</option>
          <option value="governance">Governance</option>
          <option value="ingestion">Ingestion</option>
          <option value="coder">Coder</option>
          <option value="all">All agents</option>
        </select>
        <textarea id="message" rows="1" placeholder="Ask a question or request an action…"></textarea>
        <button class="send-btn" id="send">Send</button>
        <span class="status-txt" id="status">Ready</span>
      </div>
    </div>

    <!-- Flow panel -->
    <div class="seq-panel">
      <div class="seq-hdr">Agent Flow</div>

      <!-- Node graph -->
      <div class="graph-section">
        <svg id="agent-graph" viewBox="0 0 272 155" xmlns="http://www.w3.org/2000/svg">
          <!-- Static background edges — trimmed to circle boundary (r=11) -->
          <line class="bg-edge" x1="41"  y1="68" x2="99"  y2="68"/>
          <line class="bg-edge" x1="120" y1="63" x2="202" y2="19"/>
          <line class="bg-edge" x1="121" y1="66" x2="201" y2="52"/>
          <line class="bg-edge" x1="121" y1="70" x2="201" y2="84"/>
          <line class="bg-edge" x1="120" y1="73" x2="202" y2="117"/>
          <!-- Active edges (updated by JS) -->
          <g id="active-edges"></g>
          <!-- Nodes (updated by JS) -->
          <g id="graph-nodes"></g>
        </svg>
      </div>

      <!-- Flow event log -->
      <div class="flow-hdr">
        <span>Message Flow</span>
        <span id="flow-count" style="font-weight:400;text-transform:none;letter-spacing:0;color:#334155"></span>
      </div>
      <div class="flow-scroll" id="seq-scroll">
        <div id="seq-events">
          <div class="seq-empty">
            <span>No messages yet</span>
            <span style="font-size:12px">Send a message to see agent flow</span>
          </div>
        </div>
      </div>

      <!-- Payload inspector (unchanged) -->
      <div class="payload" id="payload" style="display:none">
        <div class="payload-hdr">
          <div class="payload-title" id="payload-title">Message</div>
          <button class="payload-raw-btn" id="payload-lc-btn" title="Show LangChain message chain" style="display:none">LangChain</button>
          <button class="payload-raw-btn" id="payload-raw-btn" title="Toggle raw JSON">Raw</button>
          <button class="payload-close" id="payload-close" title="Close">×</button>
        </div>
        <div class="payload-body">
          <div id="payload-pre"></div>
        </div>
      </div>
    </div>

  </div>
</div>

<script>
  const AGENT_COL = { user:0, orchestrator:1, analyst:2, governance:3, ingestion:4, coder:5 };
  const AGENT_COLOR = {
    user:'#475569', orchestrator:'#2563eb',
    analyst:'#16a34a', governance:'#ea580c', ingestion:'#7c3aed', coder:'#0891b2'
  };
  const AGENT_TEXT = {
    user:'#94a3b8', orchestrator:'#93c5fd',
    analyst:'#86efac', governance:'#fdba74', ingestion:'#c4b5fd', coder:'#67e8f9'
  };

  const STORAGE_KEY = 'mags_sessions';
  const SIDEBAR_KEY = 'mags_sidebar';
  const AUTO_SESSION_ID = 'auto-session';
  const AUTO_MSGS_KEY   = 'mags_auto_msgs';
  const DAG_SESSION_ID  = 'dag-monitor-session';
  const DAG_MSGS_KEY    = 'mags_dag_msgs';
  const DAG_PENDING_KEY = 'mags_dag_pending';

  // Lock/unlock the agent selector when entering special sessions
  function _setAgentLock(value) {
    const sel = document.getElementById('target');
    if (!sel) return;
    if (value) {
      sel.value = value;
      sel.disabled = true;
      sel.title = 'Agent is fixed for this session';
    } else {
      sel.disabled = false;
      sel.title = '';
    }
  }

  // Fixed check slots: 00:30, 02:30, 04:30 … 22:30  (every even hour at :30)
  function msUntilNextFixedCheck() {
    const now = new Date();
    const totalMs = (now.getHours() * 3600 + now.getMinutes() * 60 + now.getSeconds()) * 1000 + now.getMilliseconds();
    const slots = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22].map(h => (h * 60 + 30) * 60 * 1000);
    for (const slotMs of slots) {
      if (slotMs > totalMs) return slotMs - totalMs;
    }
    return 24 * 3600 * 1000 - totalMs + slots[0]; // wrap to next day 00:30
  }

  // ── Auto Monitor state ──
  let autoState = 'idle'; // 'idle' | 'checking' | 'critical'
  let autoTimer = null;
  let autoCountdownTimer = null;
  let autoNextCheckAt = 0;
  let autoUnread = 0;

  // ── DAG Upgrade Monitor state ──
  let dagState = 'idle'; // 'idle' | 'checking' | 'pending' | 'applying'
  let dagTimer = null;
  let dagCountdownTimer = null;
  let dagNextCheckAt = 0;
  let dagUnread = 0;
  let dagLastSuggestions = localStorage.getItem(DAG_PENDING_KEY) || '';

  function loadAutoMsgs() {
    try { return JSON.parse(localStorage.getItem(AUTO_MSGS_KEY) || '[]'); } catch { return []; }
  }
  function saveAutoMsgs(msgs) { localStorage.setItem(AUTO_MSGS_KEY, JSON.stringify(msgs.slice(-300))); }

  function scheduleNextAutoCheck(delayMs) {
    clearTimeout(autoTimer);
    autoNextCheckAt = Date.now() + delayMs;
    updateAutoTab();
    autoTimer = setTimeout(runAutoCheck, delayMs);
  }

  function updateAutoTab() {
    const tab  = document.getElementById('auto-session-tab');
    const dot  = document.getElementById('auto-dot');
    const sub  = document.getElementById('auto-sub');
    const badge = document.getElementById('auto-badge');
    const runBtn = document.getElementById('auto-run-btn');
    if (!tab) return;

    tab.classList.toggle('active', currentSessionId === AUTO_SESSION_ID);
    tab.classList.toggle('state-critical', autoState === 'critical');

    dot.className = 'auto-dot ' + autoState;

    if (autoState === 'checking') {
      sub.textContent = 'Checking now…';
    } else if (autoState === 'critical') {
      sub.textContent = 'Awaiting your decision';
    } else {
      const rem = Math.max(0, autoNextCheckAt - Date.now());
      const nextDt = new Date(autoNextCheckAt);
      const hh = nextDt.getHours().toString().padStart(2, '0');
      const mm = nextDt.getMinutes().toString().padStart(2, '0');
      const remMin = Math.floor(rem / 60000);
      const remS   = Math.floor((rem % 60000) / 1000);
      sub.textContent = remMin >= 60
        ? 'Next: ' + hh + ':' + mm + ' (in ' + Math.floor(remMin / 60) + 'h ' + (remMin % 60) + 'm)'
        : 'Next: ' + hh + ':' + mm + ' (' + remMin + 'm ' + (remS < 10 ? '0' : '') + remS + 's)';
    }

    if (autoUnread > 0 && currentSessionId !== AUTO_SESSION_ID) {
      badge.style.display = '';
      badge.textContent = autoUnread > 9 ? '9+' : autoUnread;
    } else {
      badge.style.display = 'none';
      if (currentSessionId === AUTO_SESSION_ID) autoUnread = 0;
    }

    if (runBtn) runBtn.disabled = autoState !== 'idle';
  }

  async function runAutoCheck() {
    if (autoState !== 'idle') return;  // already running or in critical state
    autoState = 'checking';
    updateAutoTab();
    try {
      const ctrl = new AbortController();
      const tid  = setTimeout(() => ctrl.abort(), 420000);  // 7 min — 4 agents in parallel
      const resp = await fetch('/api/auto-check', { signal: ctrl.signal });
      clearTimeout(tid);
      const data = await resp.json();
      const critical = !!data.critical;
      const now  = Date.now();

      // Split the combined message into per-agent sections and show each as its own bubble.
      // Sections are separated by "### <Title> (<Agent>)\n" headings written by the backend.
      const sectionMap = {
        'Pipeline Status (Ingestion)': 'ingestion',
        'Governance & Metadata':       'governance',
        'Data Quality (Analyst)':      'analyst',
        'DAG Code Health (Coder)':     'coder',
        'Orchestrator Summary':        'orchestrator',
      };
      const fullMsg = (data.message || '').trim();
      const msgs = loadAutoMsgs();

      // Always store the full combined message for history replay
      msgs.push({ role: 'bot', agent: 'orchestrator', text: fullMsg, time: now, _autoReport: true });
      saveAutoMsgs(msgs);

      if (currentSessionId === AUTO_SESSION_ID) {
        // Show a slim header bubble from orchestrator
        const ts = fullMsg.match(/System Health Report — ([^\n]+)/)?.[1] || new Date(now).toLocaleTimeString();
        addBotBubble('orchestrator', `## System Health Report — ${ts}`, false);

        // Show one bubble per agent section
        for (const [title, agent] of Object.entries(sectionMap)) {
          const esc = title.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
          const re = new RegExp(`###\\s*${esc}\\n([\\s\\S]*?)(?=\\n###|$)`);
          const match = fullMsg.match(re);
          if (match) {
            const body = match[1].trim();
            if (body) addBotBubble(agent, body, false);
          }
        }
        renderSequence(data.traces || []);
      } else {
        autoUnread++;
      }

      if (critical) {
        autoState = 'critical';
        switchSession(AUTO_SESSION_ID);
        document.getElementById('critical-banner').style.display = 'flex';
      } else {
        autoState = 'idle';
      }
    } catch (err) {
      if (err && err.name === 'AbortError') {
        console.warn('[auto-check] request timed out, rescheduling');
      } else {
        const txt = 'Auto-check failed: ' + String(err);
        const msgs = loadAutoMsgs();
        msgs.push({ role: 'bot', agent: 'system', text: txt, time: Date.now() });
        saveAutoMsgs(msgs);
        if (currentSessionId === AUTO_SESSION_ID) addBotBubble('system', txt, false);
        else autoUnread++;
      }
      autoState = 'idle';
    } finally {
      if (autoState === 'idle') scheduleNextAutoCheck(msUntilNextFixedCheck());
      updateAutoTab();
    }
  }

  function initAutoMonitor() {
    // Countdown refresh every 1 s so the display ticks smoothly
    autoCountdownTimer = setInterval(() => {
      if (autoState === 'idle') updateAutoTab();
    }, 1000);
    document.getElementById('auto-session-tab').addEventListener('click', () => switchSession(AUTO_SESSION_ID));
    document.getElementById('auto-run-btn').addEventListener('click', e => {
      e.stopPropagation();
      if (autoState === 'idle') runAutoCheck();
    });
    document.getElementById('critical-skip-btn').addEventListener('click', () => {
      autoState = 'idle';
      document.getElementById('critical-banner').style.display = 'none';
      scheduleNextAutoCheck(msUntilNextFixedCheck());
      updateAutoTab();
    });
    scheduleNextAutoCheck(msUntilNextFixedCheck());
  }

  // ── DAG Upgrade Monitor ────────────────────────────────────────────────────
  function loadDagMsgs() {
    try { return JSON.parse(localStorage.getItem(DAG_MSGS_KEY) || '[]'); } catch { return []; }
  }
  function saveDagMsgs(msgs) { localStorage.setItem(DAG_MSGS_KEY, JSON.stringify(msgs.slice(-300))); }

  function scheduleNextDagCheck(delayMs) {
    clearTimeout(dagTimer);
    dagNextCheckAt = Date.now() + delayMs;
    updateDagTab();
    dagTimer = setTimeout(runDagCheck, delayMs);
  }

  function updateDagTab() {
    const tab    = document.getElementById('dag-session-tab');
    const dot    = document.getElementById('dag-dot');
    const sub    = document.getElementById('dag-sub');
    const badge  = document.getElementById('dag-badge');
    const runBtn = document.getElementById('dag-run-btn');
    if (!tab) return;

    tab.classList.toggle('active', currentSessionId === DAG_SESSION_ID);
    tab.classList.toggle('state-pending', dagState === 'pending');

    dot.className = 'auto-dot dag-dot ' + dagState;

    if (dagState === 'checking') {
      sub.textContent = 'Auditing DAGs…';
    } else if (dagState === 'pending') {
      sub.textContent = 'Suggestions ready — awaiting your decision';
    } else if (dagState === 'applying') {
      sub.textContent = 'Applying changes…';
    } else {
      const rem    = Math.max(0, dagNextCheckAt - Date.now());
      const nextDt = new Date(dagNextCheckAt);
      const hh     = nextDt.getHours().toString().padStart(2, '0');
      const mm     = nextDt.getMinutes().toString().padStart(2, '0');
      const remH   = Math.floor(rem / 3600000);
      const remMin = Math.floor((rem % 3600000) / 60000);
      const remS   = Math.floor((rem % 60000) / 1000);
      sub.textContent = remH >= 1
        ? 'Next: ' + hh + ':' + mm + ' (in ' + remH + 'h ' + remMin + 'm)'
        : 'Next: ' + hh + ':' + mm + ' (' + remMin + 'm ' + (remS < 10 ? '0' : '') + remS + 's)';
    }

    if (dagUnread > 0 && currentSessionId !== DAG_SESSION_ID) {
      badge.style.display = '';
      badge.textContent = dagUnread > 9 ? '9+' : dagUnread;
    } else {
      badge.style.display = 'none';
      if (currentSessionId === DAG_SESSION_ID) dagUnread = 0;
    }

    if (runBtn) runBtn.disabled = dagState !== 'idle';
  }

  async function runDagCheck() {
    if (dagState !== 'idle') return;
    dagState = 'checking';
    updateDagTab();
    try {
      const ctrl = new AbortController();
      const tid  = setTimeout(() => ctrl.abort(), 600000);
      const resp = await fetch('/api/dag-check', { signal: ctrl.signal });
      clearTimeout(tid);
      const data = await resp.json();
      const msg           = (data.message || 'DAG audit complete.').trim();
      const hasSuggestions = !!data.has_suggestions;

      const msgs = loadDagMsgs();
      msgs.push({ role: 'bot', agent: 'coder', text: msg, time: Date.now() });
      saveDagMsgs(msgs);

      if (currentSessionId === DAG_SESSION_ID) {
        addBotBubble('coder', msg, false);
        renderSequence(data.traces || []);
      } else {
        dagUnread++;
      }

      if (hasSuggestions) {
        dagState = 'pending';
        dagLastSuggestions = msg;
        localStorage.setItem(DAG_PENDING_KEY, msg);
        // Auto-switch to DAG session so user sees the suggestions
        switchSession(DAG_SESSION_ID);
        document.getElementById('dag-action-bar').style.display = 'flex';
      } else {
        dagState = 'idle';
        scheduleNextDagCheck(24 * 3600 * 1000);
      }
    } catch (err) {
      if (err && err.name === 'AbortError') {
        console.warn('[dag-check] timed out, rescheduling');
      } else {
        const txt = 'DAG audit failed: ' + String(err);
        const msgs = loadDagMsgs();
        msgs.push({ role: 'bot', agent: 'system', text: txt, time: Date.now() });
        saveDagMsgs(msgs);
        if (currentSessionId === DAG_SESSION_ID) addBotBubble('system', txt, false);
        else dagUnread++;
      }
      dagState = 'idle';
      scheduleNextDagCheck(24 * 3600 * 1000);
    } finally {
      updateDagTab();
    }
  }

  async function runDagApply() {
    if (dagState !== 'pending') return;
    dagState = 'applying';
    document.getElementById('dag-action-bar').style.display = 'none';
    document.getElementById('dag-apply-btn').disabled = true;
    updateDagTab();

    const approvalMsg = 'Apply the suggested DAG improvements.';
    addUserBubble(approvalMsg);

    try {
      const ctrl = new AbortController();
      const tid  = setTimeout(() => ctrl.abort(), 600000);
      const resp = await fetch('/api/dag-apply', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ suggestions: dagLastSuggestions }),
        signal: ctrl.signal,
      });
      clearTimeout(tid);
      const data = await resp.json();
      const msg  = (data.message || 'Changes applied.').trim();
      const msgs = loadDagMsgs();
      msgs.push({ role: 'bot', agent: 'coder', text: msg, time: Date.now() });
      saveDagMsgs(msgs);
      addBotBubble('coder', msg, false);
      renderSequence(data.traces || []);
    } catch (err) {
      const txt = 'Apply failed: ' + String(err);
      const msgs = loadDagMsgs();
      msgs.push({ role: 'bot', agent: 'system', text: txt, time: Date.now() });
      saveDagMsgs(msgs);
      addBotBubble('system', txt, false);
    } finally {
      dagLastSuggestions = '';
      localStorage.removeItem(DAG_PENDING_KEY);
      dagState = 'idle';
      scheduleNextDagCheck(24 * 3600 * 1000);
      updateDagTab();
    }
  }

  function initDagMonitor() {
    // Restore pending state from localStorage (survives page refresh)
    if (dagLastSuggestions) {
      dagState = 'pending';
    }

    dagCountdownTimer = setInterval(() => {
      if (dagState === 'idle') updateDagTab();
    }, 1000);

    document.getElementById('dag-session-tab').addEventListener('click', () => switchSession(DAG_SESSION_ID));
    document.getElementById('dag-run-btn').addEventListener('click', e => {
      e.stopPropagation();
      if (dagState === 'idle') runDagCheck();
    });
    document.getElementById('dag-apply-btn').addEventListener('click', runDagApply);
    document.getElementById('dag-skip-btn').addEventListener('click', () => {
      dagState = 'idle';
      dagLastSuggestions = '';
      localStorage.removeItem(DAG_PENDING_KEY);
      document.getElementById('dag-action-bar').style.display = 'none';
      scheduleNextDagCheck(24 * 3600 * 1000);
      updateDagTab();
    });

    // Schedule first check 24 h from now (▶ button allows running immediately)
    scheduleNextDagCheck(24 * 3600 * 1000);

    // If we restored a pending state, show action bar immediately if on DAG session
    updateDagTab();
  }

  // ── Session persistence (localStorage) ──
  function genId() {
    return typeof crypto !== 'undefined' && crypto.randomUUID
      ? crypto.randomUUID()
      : Date.now().toString(36) + '-' + Math.random().toString(36).slice(2);
  }
  function loadSessions() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); } catch { return []; }
  }
  function saveSessions(s) { localStorage.setItem(STORAGE_KEY, JSON.stringify(s)); }

  function createSession() {
    const sessions = loadSessions();
    const s = { id: genId(), title: 'New Chat', messages: [], traces: [], created: Date.now(), lastActive: Date.now() };
    sessions.unshift(s);
    saveSessions(sessions);
    return s;
  }
  function getSession(id) { return loadSessions().find(s => s.id === id) || null; }

  function deleteSession(id) { saveSessions(loadSessions().filter(s => s.id !== id)); }

  function pushMessage(sessionId, msg) {
    const sessions = loadSessions();
    const s = sessions.find(s => s.id === sessionId);
    if (!s) return;
    s.messages.push(msg);
    s.lastActive = Date.now();
    if (s.title === 'New Chat') {
      const first = s.messages.find(m => m.role === 'user');
      if (first) s.title = first.text.slice(0, 40) + (first.text.length > 40 ? '…' : '');
    }
    saveSessions(sessions);
  }

  function saveTraces(sessionId, traces) {
    const sessions = loadSessions();
    const s = sessions.find(s => s.id === sessionId);
    if (!s) return;
    s.traces = traces;
    saveSessions(sessions);
  }

  function formatTime(ts) {
    const d = new Date(ts || Date.now());
    return d.getHours().toString().padStart(2,'0') + ':' + d.getMinutes().toString().padStart(2,'0');
  }

  function formatDate(ts) {
    const diffMin = Math.floor((Date.now() - ts) / 60000);
    if (diffMin < 1) return 'just now';
    if (diffMin < 60) return diffMin + 'm ago';
    const diffH = Math.floor(diffMin / 60);
    if (diffH < 24) return diffH + 'h ago';
    const diffD = Math.floor(diffH / 24);
    if (diffD < 7) return diffD + 'd ago';
    return new Date(ts).toLocaleDateString();
  }

  // ── State ──
  let currentSessionId = null;
  let chatEl, statusEl, seqEl, payloadEl, payloadTitleEl, payloadPreEl;
  let liveActiveNodes = new Set();  // agents currently processing (drives graph pulses)
  let liveActiveEdges = [];         // edges currently active

  // ── Sidebar toggle ──
  function isSidebarOpen() { return localStorage.getItem(SIDEBAR_KEY) !== 'closed'; }

  function applySidebarState() {
    const open = isSidebarOpen();
    document.getElementById('sidebar').classList.toggle('collapsed', !open);
    document.getElementById('sidebar-toggle').title = open ? 'Hide sessions panel' : 'Show sessions panel';
  }

  function toggleSidebar() {
    localStorage.setItem(SIDEBAR_KEY, isSidebarOpen() ? 'closed' : 'open');
    applySidebarState();
  }

  // ── Render sessions list ──
  function renderSessions() {
    const list = document.getElementById('sessions-list');
    const sessions = loadSessions();
    list.innerHTML = '';
    if (!sessions.length) {
      list.innerHTML = '<div class="sessions-empty">No saved sessions</div>';
      return;
    }
    sessions.forEach(s => {
      const item = document.createElement('div');
      item.className = 'session-item' + (s.id === currentSessionId ? ' active' : '');

      const title = document.createElement('div');
      title.className = 'session-title';
      title.textContent = s.title;

      const date = document.createElement('div');
      date.className = 'session-date';
      date.textContent = formatDate(s.lastActive);

      const del = document.createElement('button');
      del.className = 'session-delete';
      del.textContent = '×';
      del.title = 'Delete session';
      del.addEventListener('click', e => {
        e.stopPropagation();
        deleteSession(s.id);
        if (s.id === currentSessionId) startNewSession();
        else renderSessions();
      });

      item.appendChild(title);
      item.appendChild(date);
      item.appendChild(del);
      item.addEventListener('click', () => switchSession(s.id));
      list.appendChild(item);
    });
  }

  // ── Session switching ──
  function startNewSession() {
    const s = createSession();
    currentSessionId = s.id;
    chatEl.innerHTML = '';
    renderSequence([]);
    renderSessions();
    setStatus('Ready');
  }

  function switchSession(id) {
    if (id === currentSessionId) return;

    // Auto session: load from dedicated storage
    if (id === AUTO_SESSION_ID) {
      currentSessionId = AUTO_SESSION_ID;
      chatEl.innerHTML = '';
      const _autoSectionMap = {
        'Pipeline Status (Ingestion)': 'ingestion',
        'Governance & Metadata':       'governance',
        'Data Quality (Analyst)':      'analyst',
        'DAG Code Health (Coder)':     'coder',
        'Orchestrator Summary':        'orchestrator',
      };
      loadAutoMsgs().forEach(m => {
        if (m.role === 'user') { addUserBubble(m.text, false, m.time); return; }
        if (m._autoReport) {
          // Re-split stored auto-report into per-agent bubbles
          const ts2 = m.text.match(/System Health Report — ([^\n]+)/)?.[1] || new Date(m.time).toLocaleTimeString();
          addBotBubble('orchestrator', `## System Health Report — ${ts2}`, false, m.time);
          for (const [title, agent] of Object.entries(_autoSectionMap)) {
            const esc2 = title.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
            const re2 = new RegExp(`###\\s*${esc2}\\n([\\s\\S]*?)(?=\\n###|$)`);
            const match2 = m.text.match(re2);
            if (match2) { const body2 = match2[1].trim(); if (body2) addBotBubble(agent, body2, false, m.time); }
          }
        } else {
          addBotBubble(m.agent || 'orchestrator', m.text, false, m.time);
        }
      });
      chatEl.scrollTop = chatEl.scrollHeight;
      autoUnread = 0;
      document.getElementById('critical-banner').style.display = autoState === 'critical' ? 'flex' : 'none';
      document.getElementById('dag-action-bar').style.display = 'none';
      _setAgentLock('orchestrator');
      updateAutoTab();
      updateDagTab();
      renderSessions();
      setStatus('Auto Monitor');
      return;
    }

    // DAG Upgrade Monitor session
    if (id === DAG_SESSION_ID) {
      currentSessionId = DAG_SESSION_ID;
      chatEl.innerHTML = '';
      loadDagMsgs().forEach(m => {
        if (m.role === 'user') addUserBubble(m.text, false, m.time);
        else addBotBubble(m.agent || 'coder', m.text, false, m.time);
      });
      chatEl.scrollTop = chatEl.scrollHeight;
      dagUnread = 0;
      document.getElementById('critical-banner').style.display = 'none';
      document.getElementById('dag-action-bar').style.display = dagState === 'pending' ? 'flex' : 'none';
      _setAgentLock('coder');
      updateAutoTab();
      updateDagTab();
      renderSessions();
      setStatus('DAG Upgrade Monitor');
      return;
    }

    // Hide both banners and unlock agent selector for regular sessions
    document.getElementById('critical-banner').style.display = 'none';
    document.getElementById('dag-action-bar').style.display = 'none';
    _setAgentLock(null);

    const s = getSession(id);
    if (!s) return;
    currentSessionId = id;
    chatEl.innerHTML = '';
    s.messages.forEach(m => {
      if (m.role === 'user') addUserBubble(m.text, false, m.time);
      else addBotBubble(m.agent, m.text, false, m.time);
    });
    chatEl.scrollTop = chatEl.scrollHeight;
    renderSequence(s.traces || []);
    renderSessions();
    updateAutoTab();
    setStatus('Ready');
  }

  // ── Init ──
  function init() {
    chatEl         = document.getElementById('chat');
    statusEl       = document.getElementById('status');
    seqEl          = document.getElementById('seq-events');
    payloadEl      = document.getElementById('payload');
    payloadTitleEl = document.getElementById('payload-title');
    payloadPreEl   = document.getElementById('payload-pre');

    document.getElementById('send').addEventListener('click', submit);
    const msgEl = document.getElementById('message');
    msgEl.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); submit(); } });
    msgEl.addEventListener('input', () => { msgEl.style.height = 'auto'; msgEl.style.height = msgEl.scrollHeight + 'px'; });
    document.getElementById('payload-close').addEventListener('click', () => {
      payloadEl.style.display = 'none';
      document.querySelectorAll('.flow-card.sel').forEach(el => el.classList.remove('sel'));
    });
    document.getElementById('payload-raw-btn').addEventListener('click', () => {
      _payloadRawMode = !_payloadRawMode;
      _payloadLcMode  = false;
      _renderPayloadContent(_payloadRawMode, false);
    });
    document.getElementById('payload-lc-btn').addEventListener('click', () => {
      _payloadLcMode  = !_payloadLcMode;
      _payloadRawMode = false;
      _renderPayloadContent(false, _payloadLcMode);
    });
    document.getElementById('sidebar-toggle').addEventListener('click', toggleSidebar);
    document.getElementById('new-chat').addEventListener('click', startNewSession);

    applySidebarState();
    initAutoMonitor();
    initDagMonitor();
    refreshGraphNodes(new Set());

    const sessions = loadSessions();
    if (sessions.length) {
      currentSessionId = sessions[0].id;
      sessions[0].messages.forEach(m => {
        if (m.role === 'user') addUserBubble(m.text, false, m.time);
        else addBotBubble(m.agent, m.text, false, m.time);
      });
      if (sessions[0].messages.length) chatEl.scrollTop = chatEl.scrollHeight;
    } else {
      currentSessionId = createSession().id;
    }
    renderSessions();
  }

  function setStatus(text, err) {
    statusEl.textContent = text;
    statusEl.style.color = err ? '#fca5a5' : '#334155';
  }

  /* ── Text/table rendering ── */
  function norm(t) { return String(t).replace(/\\n/g, '\n').replace(/\\t/g, '\t'); }
  function isPipe(l) { const t = l.trim(); return t.startsWith('|') && t.endsWith('|'); }
  function isSep(l)  { return /^\|[\s:\-|]+\|$/.test(l.trim()); }
  function splitRow(l) { return l.trim().slice(1,-1).split('|').map(c => c.trim()); }

  function buildTable(lines) {
    const wrap = document.createElement('div'); wrap.className = 'tbl-wrap';
    const tbl = document.createElement('table');
    const thead = document.createElement('thead'); const tbody = document.createElement('tbody');
    const hr = document.createElement('tr');
    splitRow(lines[0]).forEach(c => { const th = document.createElement('th'); th.textContent = c; hr.appendChild(th); });
    thead.appendChild(hr);
    for (let i = 2; i < lines.length; i++) {
      const tr = document.createElement('tr');
      splitRow(lines[i]).forEach(c => { const td = document.createElement('td'); td.textContent = c; tr.appendChild(td); });
      tbody.appendChild(tr);
    }
    tbl.appendChild(thead); tbl.appendChild(tbody); wrap.appendChild(tbl);
    return wrap;
  }

  function escHtml(s) {
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }
  function inlineMd(s) {
    return escHtml(s)
      .replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>')
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*([^*\n]+?)\*/g, '<em>$1</em>')
      .replace(/`([^`\n]+)`/g, '<code>$1</code>');
  }

  function renderContent(container, rawText) {
    const lines = norm(rawText).split('\n');
    let i = 0;
    let paraLines = [];

    function flushPara() {
      if (!paraLines.length) return;
      const p = document.createElement('p');
      p.innerHTML = inlineMd(paraLines.join(' '));
      container.appendChild(p);
      paraLines = [];
    }

    while (i < lines.length) {
      const cur = lines[i] || '';
      const nxt = lines[i+1] || '';

      // ── Markdown table ──
      if (isPipe(cur) && isSep(nxt)) {
        flushPara();
        const rows = [cur, nxt]; i += 2;
        while (i < lines.length && isPipe(lines[i])) { rows.push(lines[i]); i++; }
        container.appendChild(buildTable(rows));
        continue;
      }

      // ── Fenced code block ──
      if (cur.startsWith('```')) {
        flushPara();
        const codeLines = []; i++;
        while (i < lines.length && !lines[i].startsWith('```')) { codeLines.push(lines[i]); i++; }
        i++;
        const pre = document.createElement('pre'); pre.className = 'code-block';
        const code = document.createElement('code'); code.textContent = codeLines.join('\n');
        pre.appendChild(code); container.appendChild(pre);
        continue;
      }

      // ── Heading ──
      const hm = cur.match(/^(#{1,4})\s+(.+)$/);
      if (hm) {
        flushPara();
        const h = document.createElement('h' + hm[1].length);
        h.innerHTML = inlineMd(hm[2]);
        container.appendChild(h); i++;
        continue;
      }

      // ── Horizontal rule ──
      if (/^[-*_]{3,}$/.test(cur.trim())) {
        flushPara();
        container.appendChild(document.createElement('hr')); i++;
        continue;
      }

      // ── Blockquote ──
      if (cur.startsWith('> ')) {
        flushPara();
        const bq = document.createElement('blockquote');
        while (i < lines.length && lines[i].startsWith('> ')) {
          const p = document.createElement('p'); p.innerHTML = inlineMd(lines[i].slice(2));
          bq.appendChild(p); i++;
        }
        container.appendChild(bq);
        continue;
      }

      // ── Bullet list ──
      if (/^[-*+]\s+/.test(cur)) {
        flushPara();
        const ul = document.createElement('ul');
        while (i < lines.length && /^[-*+]\s+/.test(lines[i])) {
          const li = document.createElement('li'); li.innerHTML = inlineMd(lines[i].replace(/^[-*+]\s+/, ''));
          ul.appendChild(li); i++;
        }
        container.appendChild(ul);
        continue;
      }

      // ── Numbered list ──
      if (/^\d+\.\s+/.test(cur)) {
        flushPara();
        const ol = document.createElement('ol');
        while (i < lines.length && /^\d+\.\s+/.test(lines[i])) {
          const li = document.createElement('li'); li.innerHTML = inlineMd(lines[i].replace(/^\d+\.\s+/, ''));
          ol.appendChild(li); i++;
        }
        container.appendChild(ol);
        continue;
      }

      // ── Empty line — flush paragraph ──
      if (!cur.trim()) {
        flushPara(); i++;
        continue;
      }

      // ── Regular text line — accumulate into paragraph ──
      paraLines.push(cur); i++;
    }
    flushPara();
  }

  /* ── Chat bubbles ── */
  function addUserBubble(text, save = true, ts = null) {
    const t = ts || Date.now();
    const wrap = document.createElement('div'); wrap.className = 'bwrap user';
    const meta = document.createElement('div'); meta.className = 'bmeta';
    meta.textContent = 'You · ' + formatTime(t);
    const bub  = document.createElement('div'); bub.className  = 'bubble user'; bub.textContent = text;
    wrap.appendChild(meta); wrap.appendChild(bub);
    chatEl.appendChild(wrap); chatEl.scrollTop = chatEl.scrollHeight;
    if (save) {
      if (currentSessionId === AUTO_SESSION_ID) {
        const msgs = loadAutoMsgs(); msgs.push({ role: 'user', text, time: Date.now() }); saveAutoMsgs(msgs);
      } else if (currentSessionId === DAG_SESSION_ID) {
        const msgs = loadDagMsgs(); msgs.push({ role: 'user', text, time: Date.now() }); saveDagMsgs(msgs);
      } else if (currentSessionId) {
        pushMessage(currentSessionId, { role: 'user', text, time: Date.now() }); renderSessions();
      }
    }
  }

  function addBotBubble(agent, text, save = true, ts = null) {
    const t = ts || Date.now();
    const col  = AGENT_COLOR[agent] || '#475569';
    const tcol = AGENT_TEXT[agent]  || '#94a3b8';
    const wrap = document.createElement('div'); wrap.className = 'bwrap bot';
    const meta = document.createElement('div'); meta.className = 'bmeta';
    meta.textContent = agent.charAt(0).toUpperCase() + agent.slice(1) + ' · ' + formatTime(t);
    meta.style.color = tcol;
    const bub = document.createElement('div'); bub.className = 'bubble bot';
    const hdr = document.createElement('div'); hdr.className = 'bheader';
    hdr.innerHTML = '<span class="bdot" style="background:' + col + '"></span>' +
                    '<span class="bname" style="color:' + tcol + '">' + agent + '</span>';
    const body = document.createElement('div');
    renderContent(body, text);
    bub.appendChild(hdr); bub.appendChild(body);
    wrap.appendChild(meta); wrap.appendChild(bub);
    chatEl.appendChild(wrap); chatEl.scrollTop = chatEl.scrollHeight;
    if (save) {
      if (currentSessionId === AUTO_SESSION_ID) {
        const msgs = loadAutoMsgs(); msgs.push({ role: 'bot', agent, text, time: Date.now() }); saveAutoMsgs(msgs);
      } else if (currentSessionId === DAG_SESSION_ID) {
        const msgs = loadDagMsgs(); msgs.push({ role: 'bot', agent, text, time: Date.now() }); saveDagMsgs(msgs);
      } else if (currentSessionId) {
        pushMessage(currentSessionId, { role: 'bot', agent, text, time: Date.now() });
      }
    }
  }

  /* ── Agent node graph + flow stack ── */
  const NS = 'http://www.w3.org/2000/svg';
  const NODE_R = 11; // circle radius — must match the offsets used in SVG bg-edges above
  const GRAPH_NODES = {
    user:         { x: 30,  y: 68,  label: 'User' },
    orchestrator: { x: 110, y: 68,  label: 'Orch' },
    analyst:      { x: 212, y: 14,  label: 'Analyst' },
    governance:   { x: 212, y: 50,  label: 'Gov' },
    ingestion:    { x: 212, y: 86,  label: 'Ingest' },
    coder:        { x: 212, y: 122, label: 'Coder' },
  };

  function svgEl(tag, attrs) {
    const el = document.createElementNS(NS, tag);
    Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, v));
    return el;
  }

  // Returns edge endpoints trimmed to the circle boundary on each side.
  function edgePoints(p1, p2) {
    const dx = p2.x - p1.x, dy = p2.y - p1.y;
    const len = Math.sqrt(dx*dx + dy*dy) || 1;
    const ux = dx/len, uy = dy/len;
    return { x1: p1.x + NODE_R*ux, y1: p1.y + NODE_R*uy,
             x2: p2.x - NODE_R*ux, y2: p2.y - NODE_R*uy };
  }

  function refreshGraphNodes(activeSet) {
    const g = document.getElementById('graph-nodes');
    if (!g) return;
    g.innerHTML = '';
    Object.entries(GRAPH_NODES).forEach(([name, pos]) => {
      const active = activeSet.has(name);
      const c = AGENT_COLOR[name] || '#475569';
      const t = AGENT_TEXT[name]  || '#94a3b8';
      if (active) {
        // Pulsing ring via SMIL animation
        const ring = svgEl('circle', { cx: pos.x, cy: pos.y, r: NODE_R + 3,
          fill: 'none', stroke: c, 'stroke-width': '1' });
        const ar = svgEl('animate', { attributeName: 'r',
          values: `${NODE_R + 3};${NODE_R + 9};${NODE_R + 3}`,
          dur: '1.5s', repeatCount: 'indefinite' });
        const ao = svgEl('animate', { attributeName: 'opacity',
          values: '0.7;0;0.7', dur: '1.5s', repeatCount: 'indefinite' });
        ring.appendChild(ar); ring.appendChild(ao);
        g.appendChild(ring);
      }
      g.appendChild(svgEl('circle', { cx: pos.x, cy: pos.y, r: NODE_R,
        fill: active ? c + '30' : '#0d1428',
        stroke: active ? c : '#1e293b',
        'stroke-width': active ? '1.5' : '1' }));
      const letter = svgEl('text', { x: pos.x, y: pos.y + 4,
        'text-anchor': 'middle', 'font-size': '9', 'font-weight': '700',
        fill: active ? t : '#334155' });
      letter.textContent = pos.label[0];
      g.appendChild(letter);
      const lbl = svgEl('text', { x: pos.x, y: pos.y + NODE_R + 12,
        'text-anchor': 'middle', 'font-size': '7.5',
        fill: active ? t + 'cc' : '#1e293b' });
      lbl.textContent = pos.label;
      g.appendChild(lbl);
    });
  }

  function refreshActiveEdges(connections) {
    const g = document.getElementById('active-edges');
    if (!g) return;
    g.innerHTML = '';
    connections.forEach(({ from, to, color, live }) => {
      const pf = GRAPH_NODES[from] || GRAPH_NODES.orchestrator;
      const pt = GRAPH_NODES[to]   || GRAPH_NODES.analyst;
      const ep = edgePoints(pf, pt);
      const line = svgEl('line', { x1: ep.x1, y1: ep.y1, x2: ep.x2, y2: ep.y2,
        stroke: color, 'stroke-width': live ? '2' : '1.5', 'stroke-opacity': '0.75' });
      if (live) {
        const ao = svgEl('animate', { attributeName: 'stroke-opacity',
          values: '0.9;0.2;0.9', dur: '1s', repeatCount: 'indefinite' });
        line.appendChild(ao);
      }
      g.appendChild(line);
    });
  }

  function setLiveNode(agent, active) {
    if (active) {
      liveActiveNodes.add(agent);
      const from = (agent === 'orchestrator' || agent === 'user') ? 'user' : 'orchestrator';
      if (!liveActiveEdges.find(e => e.to === agent)) {
        liveActiveEdges.push({ from, to: agent, color: AGENT_COLOR[from] || '#64748b', live: true });
      }
    } else {
      liveActiveNodes.delete(agent);
      liveActiveEdges = liveActiveEdges.filter(e => e.to !== agent);
    }
    refreshGraphNodes(liveActiveNodes);
    refreshActiveEdges(liveActiveEdges);
  }

  function clearAllLiveNodes() {
    liveActiveNodes.clear();
    liveActiveEdges = [];
    refreshGraphNodes(new Set());
    refreshActiveEdges([]);
  }

  /* ── JSON tree renderer ── */
  function buildJsonTree(val, depth) {
    depth = depth || 0;
    const wrap = document.createElement('span');
    if (val === null) {
      wrap.innerHTML = '<span class="json-null">null</span>';
    } else if (typeof val === 'boolean') {
      wrap.innerHTML = '<span class="json-bool">' + val + '</span>';
    } else if (typeof val === 'number') {
      wrap.innerHTML = '<span class="json-num">' + val + '</span>';
    } else if (typeof val === 'string') {
      const safe = escHtml(val);
      wrap.innerHTML = '<span class="json-str">"' + safe + '"</span>';
    } else if (Array.isArray(val)) {
      if (!val.length) { wrap.innerHTML = '<span class="json-punc">[]</span>'; return wrap; }
      const tog = document.createElement('span'); tog.className = 'json-toggle'; tog.textContent = '▾';
      const lbl = document.createElement('span'); lbl.style.color = '#64748b'; lbl.textContent = ' [' + val.length + ']';
      const body = document.createElement('div'); body.className = 'json-indent';
      val.forEach((v, idx) => {
        const row = document.createElement('div');
        const idxSpan = document.createElement('span'); idxSpan.className = 'json-key'; idxSpan.textContent = idx + ': ';
        row.appendChild(idxSpan); row.appendChild(buildJsonTree(v, depth + 1));
        if (idx < val.length - 1) { const c = document.createElement('span'); c.className = 'json-punc'; c.textContent = ','; row.appendChild(c); }
        body.appendChild(row);
      });
      tog.addEventListener('click', () => { const c = body.style.display === 'none'; body.style.display = c ? '' : 'none'; tog.textContent = c ? '▾' : '▸'; });
      wrap.appendChild(tog); wrap.appendChild(lbl); wrap.appendChild(body);
    } else if (typeof val === 'object') {
      const keys = Object.keys(val);
      if (!keys.length) { wrap.innerHTML = '<span class="json-punc">{}</span>'; return wrap; }
      const tog = document.createElement('span'); tog.className = 'json-toggle'; tog.textContent = '▾';
      const lbl = document.createElement('span'); lbl.style.color = '#64748b'; lbl.textContent = ' {' + keys.length + '}';
      const body = document.createElement('div'); body.className = 'json-indent';
      keys.forEach((k, idx) => {
        const row = document.createElement('div');
        const kSpan = document.createElement('span'); kSpan.className = 'json-key'; kSpan.textContent = '"' + k + '": ';
        row.appendChild(kSpan); row.appendChild(buildJsonTree(val[k], depth + 1));
        if (idx < keys.length - 1) { const c = document.createElement('span'); c.className = 'json-punc'; c.textContent = ','; row.appendChild(c); }
        body.appendChild(row);
      });
      tog.addEventListener('click', () => { const c = body.style.display === 'none'; body.style.display = c ? '' : 'none'; tog.textContent = c ? '▾' : '▸'; });
      wrap.appendChild(tog); wrap.appendChild(lbl); wrap.appendChild(body);
    }
    return wrap;
  }

  function renderSequence(traces) {
    seqEl.innerHTML = '';
    const activeEdgesG = document.getElementById('active-edges');
    const graphNodesG  = document.getElementById('graph-nodes');

    if (!Array.isArray(traces) || !traces.length) {
      seqEl.innerHTML = '<div class="seq-empty"><span>No agent messages</span><span style="font-size:12px">Send a message to see agent flow</span></div>';
      payloadEl.style.display = 'none';
      if (activeEdgesG) activeEdgesG.innerHTML = '';
      refreshGraphNodes(new Set());
      const fc = document.getElementById('flow-count'); if (fc) fc.textContent = '';
      return;
    }

    const activeSet = new Set();
    const connections = [];
    traces.forEach(item => {
      const from = ((item.from || 'orchestrator') + '').toLowerCase().replace(/[^a-z]/g, '');
      const to   = ((item.to   || 'analyst')      + '').toLowerCase().replace(/[^a-z]/g, '');
      activeSet.add(from); activeSet.add(to);
      connections.push({ from, to, color: AGENT_COLOR[from] || '#64748b' });
    });
    refreshActiveEdges(connections);
    refreshGraphNodes(activeSet);

    const fc = document.getElementById('flow-count');
    if (fc) fc.textContent = '· ' + traces.length + ' event' + (traces.length !== 1 ? 's' : '');

    traces.forEach(item => {
      const from    = ((item.from || 'orchestrator') + '').toLowerCase().replace(/[^a-z]/g, '');
      const to      = ((item.to   || 'analyst')      + '').toLowerCase().replace(/[^a-z]/g, '');
      const color   = AGENT_COLOR[from] || '#64748b';
      const toColor = AGENT_COLOR[to]   || '#64748b';
      const fromTxt = AGENT_TEXT[from]  || '#94a3b8';
      const toTxt   = AGENT_TEXT[to]    || '#94a3b8';
      const evtType = item.event || 'message';
      let rawContent = '';
      let isJson = false;
      if (item.message) {
        if (item.message.payload && item.message.payload.task) rawContent = item.message.payload.task;
        else if (typeof item.message.text === 'string') rawContent = item.message.text;
        else rawContent = JSON.stringify(item.message);
      }
      // Detect if content is JSON
      if (rawContent.trim().startsWith('{') || rawContent.trim().startsWith('[')) {
        try { JSON.parse(rawContent); isJson = true; } catch {}
      }
      const preview = rawContent.slice(0, 140);
      const ts = item.timestamp ? item.timestamp.slice(11, 16) : '';

      const card = document.createElement('div'); card.className = 'flow-card';

      // Route: [FROM] ──▶ [TO]  ·ts
      const route = document.createElement('div'); route.className = 'flow-route';
      const fb = document.createElement('span'); fb.className = 'flow-badge';
      fb.style.cssText = 'background:' + color + '22;color:' + fromTxt + ';border:1px solid ' + color + '44';
      fb.textContent = from;
      const ln = document.createElement('div'); ln.className = 'flow-line';
      ln.style.background = color + '55';
      const hd = document.createElement('span'); hd.className = 'flow-head';
      hd.style.color = toColor; hd.textContent = '▶';
      const tb = document.createElement('span'); tb.className = 'flow-badge';
      tb.style.cssText = 'background:' + toColor + '22;color:' + toTxt + ';border:1px solid ' + toColor + '44';
      tb.textContent = to;
      if (ts) { const tsEl = document.createElement('span'); tsEl.className = 'flow-ts'; tsEl.textContent = ts; route.append(fb, ln, hd, tb, tsEl); }
      else route.append(fb, ln, hd, tb);

      const etRow = document.createElement('div'); etRow.style.cssText = 'display:flex;align-items:center;gap:4px;';
      const et = document.createElement('span'); et.className = 'flow-etype';
      et.style.color = color + 'cc'; et.textContent = evtType;
      etRow.appendChild(et);
      if (isJson) { const jp = document.createElement('span'); jp.className = 'flow-json-pill'; jp.textContent = '{ }'; etRow.appendChild(jp); }

      card.appendChild(route); card.appendChild(etRow);
      if (preview) {
        const pm = document.createElement('div'); pm.className = 'flow-msg';
        pm.textContent = preview; card.appendChild(pm);
      }

      card.addEventListener('click', () => {
        document.querySelectorAll('.flow-card.sel').forEach(el => el.classList.remove('sel'));
        card.classList.add('sel');
        showPayload(item, from, to, evtType);
      });
      seqEl.appendChild(card);
    });
  }

  let _payloadRawMode = false;
  let _payloadLcMode  = false;
  let _payloadCurrent = null;

  function _renderPayloadContent(rawMode, lcMode) {
    payloadPreEl.innerHTML = '';
    if (!_payloadCurrent) return;

    const lcBtn  = document.getElementById('payload-lc-btn');
    const rawBtn = document.getElementById('payload-raw-btn');
    const rawLc  = _payloadCurrent.raw_lc || null;

    // ── LangChain message chain view ─────────────────────────────────
    if (lcMode && rawLc) {
      if (lcBtn) { lcBtn.textContent = 'Response'; lcBtn.style.display = ''; }
      if (rawBtn) rawBtn.style.display = 'none';
      rawLc.forEach((msg, idx) => {
        const block = document.createElement('div');
        block.style.cssText = 'margin-bottom:10px;border-bottom:1px solid #1e293b;padding-bottom:8px;';
        // Header row
        const typeColors = { human: '#3b82f6', ai: '#10b981', tool: '#f59e0b' };
        const hdr = document.createElement('div');
        hdr.style.cssText = 'display:flex;align-items:center;gap:8px;margin-bottom:4px;';
        const badge = document.createElement('span');
        badge.style.cssText = `font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;` +
          `padding:2px 6px;border-radius:3px;background:${(typeColors[msg.type]||'#475569')}22;` +
          `color:${typeColors[msg.type]||'#64748b'};border:1px solid ${(typeColors[msg.type]||'#475569')}44;`;
        badge.textContent = msg.type;
        hdr.appendChild(badge);
        if (msg.name) {
          const nameSpan = document.createElement('span');
          nameSpan.style.cssText = 'font-size:11px;color:#f59e0b;font-family:monospace;';
          nameSpan.textContent = msg.name;
          hdr.appendChild(nameSpan);
        }
        if (msg.tool_call_id) {
          const tcid = document.createElement('span');
          tcid.style.cssText = 'font-size:9px;color:#334155;font-family:monospace;';
          tcid.textContent = 'id:' + msg.tool_call_id.slice(-8);
          hdr.appendChild(tcid);
        }
        block.appendChild(hdr);
        // Tool calls list (on AI messages)
        if (msg.tool_calls && msg.tool_calls.length) {
          msg.tool_calls.forEach(tc => {
            const tcDiv = document.createElement('div');
            tcDiv.style.cssText = 'background:#1e293b;border-radius:4px;padding:5px 8px;margin:3px 0;font-family:monospace;font-size:11px;';
            const fnSpan = document.createElement('span');
            fnSpan.style.color = '#10b981'; fnSpan.textContent = tc.name + '(';
            const argsSpan = document.createElement('span');
            argsSpan.style.color = '#94a3b8'; argsSpan.textContent = JSON.stringify(tc.args);
            const closeSpan = document.createElement('span');
            closeSpan.style.color = '#10b981'; closeSpan.textContent = ')';
            tcDiv.appendChild(fnSpan); tcDiv.appendChild(argsSpan); tcDiv.appendChild(closeSpan);
            block.appendChild(tcDiv);
          });
        }
        // Content
        if (msg.content) {
          // Try JSON tree first, else markdown
          let parsed = null;
          const trimmed = msg.content.trim();
          if (trimmed.startsWith('{') || trimmed.startsWith('[')) {
            try { parsed = JSON.parse(trimmed); } catch {}
          }
          if (parsed !== null) {
            const tree = document.createElement('div'); tree.className = 'json-tree';
            tree.appendChild(buildJsonTree(parsed, 0)); block.appendChild(tree);
          } else if (msg.type === 'ai') {
            renderContent(block, msg.content);
          } else {
            const pre = document.createElement('pre');
            pre.style.cssText = 'font-size:11px;color:#94a3b8;white-space:pre-wrap;';
            pre.textContent = msg.content; block.appendChild(pre);
          }
        }
        payloadPreEl.appendChild(block);
      });
      return;
    }

    // ── Normal message view ──────────────────────────────────────────
    if (lcBtn) { lcBtn.textContent = 'LangChain'; lcBtn.style.display = rawLc ? '' : 'none'; }

    const msg = _payloadCurrent.message || {};
    let textContent = '';
    if (typeof msg.text === 'string') textContent = msg.text;
    else if (msg.payload) textContent = JSON.stringify(msg.payload, null, 2);
    else textContent = JSON.stringify(msg, null, 2);

    let parsed = null;
    const trimmed = textContent.trim();
    if (trimmed.startsWith('{') || trimmed.startsWith('[')) {
      try { parsed = JSON.parse(trimmed); } catch {}
    }

    if (rawMode || parsed === null) {
      if (!rawMode && typeof msg.text === 'string') {
        renderContent(payloadPreEl, msg.text);
      } else {
        const pre = document.createElement('pre'); pre.textContent = textContent;
        payloadPreEl.appendChild(pre);
      }
    } else {
      const tree = document.createElement('div'); tree.className = 'json-tree';
      tree.appendChild(buildJsonTree(parsed, 0));
      payloadPreEl.appendChild(tree);
    }
    if (rawBtn) { rawBtn.textContent = (rawMode || parsed === null) ? 'Tree' : 'Raw'; rawBtn.style.display = parsed !== null ? '' : 'none'; }
  }

  function showPayload(item, from, to, evtType) {
    _payloadCurrent = item;
    _payloadRawMode = false;
    _payloadLcMode  = false;
    payloadEl.style.display = 'flex';
    const fc = AGENT_TEXT[from] || '#94a3b8';
    const tc = AGENT_TEXT[to]   || '#94a3b8';
    payloadTitleEl.innerHTML =
      '<span style="color:' + fc + '">' + from + '</span>' +
      '<span style="color:#334155"> → </span>' +
      '<span style="color:' + tc + '">' + to + '</span>' +
      '<span style="color:#1e293b"> &nbsp;·&nbsp; </span>' +
      '<span style="color:#475569">' + evtType + '</span>';
    _renderPayloadContent(false, false);
  }

  /* ── Streaming bubble helpers ── */
  function createThinkingBubble(agent) {
    const col  = AGENT_COLOR[agent] || '#475569';
    const tcol = AGENT_TEXT[agent]  || '#94a3b8';
    const wrap = document.createElement('div'); wrap.className = 'bwrap bot';
    const bub  = document.createElement('div'); bub.className = 'bubble bot';
    const hdr  = document.createElement('div'); hdr.className = 'bheader';
    hdr.innerHTML = '<span class="bdot" style="background:' + col + '"></span>' +
                    '<span class="bname" style="color:' + tcol + '">' + agent + '</span>';
    const dots = document.createElement('div'); dots.className = 'thinking-dots';
    dots.innerHTML = '<span></span><span></span><span></span>';
    bub.appendChild(hdr); bub.appendChild(dots);
    wrap.appendChild(bub);
    chatEl.appendChild(wrap); chatEl.scrollTop = chatEl.scrollHeight;
    return wrap;
  }

  function createStreamingBubble(agent) {
    const col  = AGENT_COLOR[agent] || '#475569';
    const tcol = AGENT_TEXT[agent]  || '#94a3b8';
    const t    = Date.now();
    const wrap = document.createElement('div'); wrap.className = 'bwrap bot';
    const meta = document.createElement('div'); meta.className = 'bmeta';
    meta.textContent = agent.charAt(0).toUpperCase() + agent.slice(1) + ' · ' + formatTime(t);
    meta.style.color = tcol;
    const bub  = document.createElement('div'); bub.className = 'bubble bot';
    const hdr  = document.createElement('div'); hdr.className = 'bheader';
    hdr.innerHTML = '<span class="bdot" style="background:' + col + '"></span>' +
                    '<span class="bname" style="color:' + tcol + '">' + agent + '</span>' +
                    '<span class="stream-cursor"></span>';
    const body = document.createElement('div');
    const pre  = document.createElement('pre'); pre.className = 'txt';
    body.appendChild(pre);
    bub.appendChild(hdr); bub.appendChild(body);
    wrap.appendChild(meta); wrap.appendChild(bub);
    chatEl.appendChild(wrap); chatEl.scrollTop = chatEl.scrollHeight;
    return { wrap, bub, hdr, body, pre };
  }

  function updateStreamingBubble(bubble, text) {
    if (!bubble) return;
    bubble.pre.textContent = text;
    chatEl.scrollTop = chatEl.scrollHeight;
  }

  function finalizeStreamingBubble(bubble, agent, text) {
    if (!bubble) return;
    const cursor = bubble.hdr.querySelector('.stream-cursor');
    if (cursor) cursor.remove();
    bubble.body.innerHTML = '';
    renderContent(bubble.body, text);
    chatEl.scrollTop = chatEl.scrollHeight;
  }

  /* ── Submit ── */
  // Save a bot message to a specific session without rendering it in the UI.
  function saveResponseToSession(sessionId, agent, text) {
    if (sessionId === AUTO_SESSION_ID) {
      const msgs = loadAutoMsgs();
      msgs.push({ role: 'bot', agent, text, time: Date.now() });
      saveAutoMsgs(msgs);
      autoUnread++;
      updateAutoTab();
    } else {
      pushMessage(sessionId, { role: 'bot', agent, text, time: Date.now() });
      renderSessions();
    }
  }

  async function submit() {
    const input     = document.getElementById('message');
    const targetSel = document.getElementById('target');
    const sendBtn   = document.getElementById('send');
    const msg = input.value.trim();
    if (!msg) return;

    const sendSessionId = currentSessionId;
    const sendTarget    = targetSel.value;

    addUserBubble(msg);
    input.value = ''; input.style.height = 'auto';
    sendBtn.disabled = true;
    setStatus('Connecting…');

    const ctrl = new AbortController();
    const tid  = setTimeout(() => ctrl.abort(), 600000);

    let history = [];
    if (sendSessionId !== AUTO_SESSION_ID && sendSessionId !== DAG_SESSION_ID) {
      const s = getSession(sendSessionId);
      if (s) history = s.messages.slice(-10);
    }

    const thinkingBubbles = {};  // agent → wrap element
    const streamBubbles   = {};  // agent → { wrap, bub, hdr, body, pre }
    const streamTexts     = {};  // agent → accumulated text

    try {
      const resp = await fetch('/api/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg, target: sendTarget, session_id: sendSessionId, history }),
        signal: ctrl.signal,
      });
      clearTimeout(tid);
      if (!resp.ok) throw new Error('HTTP ' + resp.status);

      const reader  = resp.body.getReader();
      const decoder = new TextDecoder();
      let   buf     = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buf += decoder.decode(value, { stream: true });
        const lines = buf.split('\n');
        buf = lines.pop();

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue;
          let ev;
          try { ev = JSON.parse(line.slice(6)); } catch { continue; }
          const viewing = currentSessionId === sendSessionId;

          if (ev.type === 'thinking') {
            setStatus(ev.agent + ' is thinking…');
            setLiveNode(ev.agent, true);
            if (viewing) thinkingBubbles[ev.agent] = createThinkingBubble(ev.agent);
          }
          else if (ev.type === 'start_response') {
            if (thinkingBubbles[ev.agent]) {
              thinkingBubbles[ev.agent].remove();
              delete thinkingBubbles[ev.agent];
            }
            streamTexts[ev.agent] = '';
            if (viewing) streamBubbles[ev.agent] = createStreamingBubble(ev.agent);
          }
          else if (ev.type === 'token') {
            streamTexts[ev.agent] = (streamTexts[ev.agent] || '') + ev.text;
            if (viewing && streamBubbles[ev.agent])
              updateStreamingBubble(streamBubbles[ev.agent], streamTexts[ev.agent]);
          }
          else if (ev.type === 'end_response') {
            const text = streamTexts[ev.agent] || '';
            if (viewing && streamBubbles[ev.agent])
              finalizeStreamingBubble(streamBubbles[ev.agent], ev.agent, text);
            // Persist to the originating session regardless of where user is now
            if (sendSessionId === AUTO_SESSION_ID) {
              const msgs = loadAutoMsgs();
              msgs.push({ role: 'bot', agent: ev.agent, text, time: Date.now() });
              saveAutoMsgs(msgs);
              if (!viewing) { autoUnread++; updateAutoTab(); }
            } else if (sendSessionId === DAG_SESSION_ID) {
              const msgs = loadDagMsgs();
              msgs.push({ role: 'bot', agent: ev.agent, text, time: Date.now() });
              saveDagMsgs(msgs);
              if (!viewing) { dagUnread++; updateDagTab(); }
            } else if (sendSessionId) {
              pushMessage(sendSessionId, { role: 'bot', agent: ev.agent, text, time: Date.now() });
              if (!viewing) renderSessions();
            }
            setLiveNode(ev.agent, false);
          }
          else if (ev.type === 'traces') {
            const traceList = ev.traces || [];
            if (sendSessionId && sendSessionId !== AUTO_SESSION_ID && sendSessionId !== DAG_SESSION_ID) {
              saveTraces(sendSessionId, traceList);
            }
            if (viewing) renderSequence(traceList);
          }
          else if (ev.type === 'done') {
            const n = Object.keys(streamTexts).length;
            setStatus(n + ' agent' + (n !== 1 ? 's' : '') + ' responded');
            clearAllLiveNodes();
          }
          else if (ev.type === 'error') {
            const errText = ev.message || 'Agent error';
            if (viewing) addBotBubble('system', errText);
            else saveResponseToSession(sendSessionId, 'system', errText);
            setStatus('Error', true);
            clearAllLiveNodes();
          }
        }
      }
    } catch (err) {
      clearAllLiveNodes();
      Object.values(thinkingBubbles).forEach(b => { if (b && b.parentNode) b.remove(); });
      if (err && err.name === 'AbortError') {
        setStatus('Request is taking longer than expected…', true);
      } else {
        const errText = 'Request failed: ' + String(err);
        if (currentSessionId === sendSessionId) addBotBubble('system', errText);
        else saveResponseToSession(sendSessionId, 'system', errText);
        setStatus('Failed', true);
      }
    } finally {
      sendBtn.disabled = false;
      if (sendSessionId === AUTO_SESSION_ID && autoState === 'critical') {
        autoState = 'idle';
        document.getElementById('critical-banner').style.display = 'none';
        scheduleNextAutoCheck(msUntilNextFixedCheck());
        updateAutoTab();
      }
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
</script>
</body>
</html>
"""


AUTO_SESSION_ID = "auto-session"


@app.get("/api/auto-check")
def api_auto_check() -> dict[str, Any]:
    """
    Fan-out health check: all four specialized agents answer in parallel,
    results are assembled into a single report.
    """
    import time as _time
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    deadline = _time.monotonic() + 120  # narrow prompts — 2 min should be plenty

    _step1_t = _time.time()
    print(f"[auto-check] START — fan-out to all 4 agents  ts={ts}")

    # Prompts are intentionally narrow — each agent must finish in 2-3 tool calls.
    # Deep analysis belongs in regular chat; this is a critical-issues-only pulse check.
    _ing_prompt = (
        "CRITICAL CHECK ONLY — make at most 2 tool calls, then answer.\n"
        "Call 1: list DAG runs from the last 24 hours and find any with state=failed.\n"
        "Call 2 (only if needed): get details on the first failed run.\n"
        "Report: number of DAGs active, number of failures in last 24 h, names of failed DAGs if any.\n"
        "End with one word: OK or CRITICAL."
    )
    _gov_prompt = (
        "CRITICAL CHECK ONLY — make exactly 2 tool calls, then answer.\n"
        "Call 1: openmetadata_api GET /api/v1/tables params={\"limit\": 0} — get total table count.\n"
        "Call 2: openmetadata_api GET /api/v1/dataQuality/testCases params={\"limit\": 0} — get total test case count.\n"
        "Report: total tables in catalog, total test cases defined, and whether any quality alerts are visible.\n"
        "End with one word: OK or CRITICAL."
    )
    _analyst_prompt = (
        "CRITICAL CHECK ONLY — make at most 2 tool calls, then answer.\n"
        "Call 1: run a single SQL query: SELECT table_name, pg_total_relation_size(table_name::text) AS bytes "
        "FROM information_schema.tables WHERE table_schema='public' ORDER BY bytes DESC LIMIT 10.\n"
        "Call 2 (only if needed): check one MongoDB collection document count.\n"
        "Report: the top tables by size, flag any that appear unexpectedly empty (0 rows / 0 bytes).\n"
        "End with one word: OK or CRITICAL."
    )
    _coder_prompt = (
        "CRITICAL CHECK ONLY — make exactly 1 tool call, then answer.\n"
        "Call 1: list_directory on the DAGs directory.\n"
        "From the filenames alone, report how many DAG files exist. "
        "Do NOT read individual files — this is a count-only check.\n"
        "Report: number of DAG files found. Flag if the count is 0 (no DAGs deployed).\n"
        "End with one word: OK or CRITICAL."
    )

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        ing_fut = pool.submit(ingestion_run_chat, _ing_prompt)
        gov_fut  = pool.submit(lambda: governance_run_agent(_gov_prompt, max_iters=6))
        ana_fut  = pool.submit(lambda: analyst_run_agent(_analyst_prompt))
        cod_fut  = pool.submit(lambda: str(coder_run_chat(_coder_prompt)))

        def _collect(fut, name, fallback):
            try:
                return str(fut.result(timeout=max(10, deadline - _time.monotonic())))
            except Exception as _e:
                print(f"[auto-check] {name} TIMEOUT/ERROR: {_e}")
                return fallback

        ing_report = _collect(ing_fut,  "ingestion",  "Ingestion agent did not respond in time.")
        gov_report = _collect(gov_fut,  "governance", "Governance agent did not respond in time.")
        ana_report = _collect(ana_fut,  "analyst",    "Analyst agent did not respond in time.")
        cod_report = _collect(cod_fut,  "coder",      "Coder agent did not respond in time.")

    print(f"[auto-check] all agents done in {_time.time()-_step1_t:.1f}s")

    # ── Strip raw JSON blobs from governance output ───────────────────────────
    def _strip_json_blobs(text: str) -> str:
        import re as _re
        lines = text.splitlines()
        clean: list[str] = []
        in_json = 0
        for line in lines:
            stripped = line.strip()
            in_json += stripped.count("{") + stripped.count("[")
            in_json -= stripped.count("}") + stripped.count("]")
            in_json = max(in_json, 0)
            if _re.match(r'^[\{\}\[\],]', stripped) or _re.match(r'^"[^"]+"\s*:', stripped):
                continue
            if in_json > 0:
                continue
            clean.append(line)
        result = "\n".join(clean).strip()
        return result if len(result) >= 30 else "(Governance agent returned unreadable data — check logs)"

    gov_report = _strip_json_blobs(gov_report)

    critical = any(
        "CRITICAL" in r for r in (ing_report, gov_report, ana_report, cod_report)
    )

    # ── Step 2: orchestrator LLM synthesizes all four reports ─────────────────
    # Plain LLM call — no tools bound — so it cannot make extra API calls and
    # will return in one shot regardless of what the agents reported.
    _synth_t = _time.time()
    _synth_prompt = f"""You are the system orchestrator. Four specialized agents just completed a health check of the data platform. Their raw reports are below. Write a comprehensive, well-structured executive summary for the operator.

Your summary must:
- Open with a one-line overall status (OK / WARNING / CRITICAL) and the key reason
- Have a clearly labelled section for each agent (Pipeline, Governance, Data Quality, Code Health)
- Under each section: explain what was checked, what was found, and what (if anything) needs attention — be specific, include names, counts, and timestamps where the agents provided them
- Close with a "Next Steps" section listing any recommended actions in priority order (only if issues were found)
- Use markdown formatting (## headings, bullet points, bold for critical items)
- Be thorough: the operator reads this report as their daily briefing, so depth is valued

Raw agent reports
-----------------
### INGESTION AGENT
{ing_report}

### GOVERNANCE AGENT
{gov_report}

### ANALYST AGENT
{ana_report}

### CODER AGENT
{cod_report}
"""
    try:
        from langchain.messages import HumanMessage as _HM, SystemMessage as _SM
        _synth_model = build_model("orchestrator")
        _synth_resp = _model_invoke_with_retry(
            _synth_model,
            [_SM(content="You are the data platform orchestrator. Synthesize agent reports into an executive summary."),
             _HM(content=_synth_prompt)],
        )
        orch_summary = str(_synth_resp.content).strip()
        print(f"[auto-check] orchestrator synthesis done in {_time.time()-_synth_t:.1f}s")
    except Exception as _e:
        orch_summary = ""
        print(f"[auto-check] orchestrator synthesis FAILED: {_e}")

    # Build per-agent sections (shown as individual bubbles in the UI)
    # and the orchestrator summary (shown as its own bubble at the end).
    message = "\n\n".join([
        f"## System Health Report — {ts}",
        f"### Pipeline Status (Ingestion)\n{ing_report}",
        f"### Governance & Metadata\n{gov_report}",
        f"### Data Quality (Analyst)\n{ana_report}",
        f"### DAG Code Health (Coder)\n{cod_report}",
        f"### Orchestrator Summary\n{orch_summary}" if orch_summary else "",
    ]).rstrip("\n\n")
    if critical:
        message = "[CRITICAL] " + message

    print(f"[auto-check] TOTAL: {_time.time()-_step1_t:.1f}s  critical={critical}")

    traces = [
        {"event": "auto_check", "from": "user",        "to": "orchestrator",
         "timestamp": ts, "message": {"text": "Scheduled health check"}},
        {"event": "auto_check", "from": "orchestrator", "to": "ingestion",
         "timestamp": ts, "message": {"text": "DAG run status"}},
        {"event": "auto_check", "from": "ingestion",   "to": "orchestrator",
         "timestamp": ts, "message": {"text": ing_report[:200]}},
        {"event": "auto_check", "from": "orchestrator", "to": "governance",
         "timestamp": ts, "message": {"text": "Catalog & quality status"}},
        {"event": "auto_check", "from": "governance",  "to": "orchestrator",
         "timestamp": ts, "message": {"text": gov_report[:200]}},
        {"event": "auto_check", "from": "orchestrator", "to": "analyst",
         "timestamp": ts, "message": {"text": "Data anomaly check"}},
        {"event": "auto_check", "from": "analyst",     "to": "orchestrator",
         "timestamp": ts, "message": {"text": ana_report[:200]}},
        {"event": "auto_check", "from": "orchestrator", "to": "coder",
         "timestamp": ts, "message": {"text": "DAG code health check"}},
        {"event": "auto_check", "from": "coder",       "to": "orchestrator",
         "timestamp": ts, "message": {"text": cod_report[:200]}},
        {"event": "auto_check", "from": "orchestrator", "to": "user",
         "timestamp": ts, "message": {"text": orch_summary[:200] if orch_summary else "Summary compiled"}},
    ]

    return {
        "message": message,
        "critical": message.strip().startswith("[CRITICAL]"),
        "traces": traces,
    }


@app.get("/api/dag-check")
def api_dag_check() -> dict[str, Any]:
    """
    Read-only DAG audit: coder agent inspects all DAGs and reports improvement
    suggestions without applying any changes.
    """
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    prompt = (
        "You are performing a READ-ONLY DAG audit. DO NOT use write_file or patch_file.\n\n"
        "Steps:\n"
        "1. Use search_files or list_directory to find all .py files in the DAGs directory.\n"
        "2. Use read_file to read each DAG file.\n"
        "3. For each DAG identify concrete improvements, such as:\n"
        "   - Missing catchup=False\n"
        "   - Missing retries / retry_delay_seconds\n"
        "   - No email_on_failure alert\n"
        "   - Hardcoded credentials or connection strings\n"
        "   - Missing tags for better Airflow UI organisation\n"
        "   - Overly broad schedule intervals that waste resources\n"
        "   - Any other Airflow best-practice issues\n"
        "4. Return a structured report:\n"
        "   - Brief summary of overall DAG health\n"
        "   - For each DAG with issues: filename, current value, and the exact change to make\n"
        "   - If no improvements are needed, say so clearly\n\n"
        "IMPORTANT: This is analysis only. Do NOT modify any file."
    )
    try:
        result_str = str(_run_with_timeout(coder_run_chat, prompt))
        has_suggestions = any(
            kw in result_str.lower()
            for kw in ["suggest", "improvement", "missing", "should add", "recommend",
                       "consider", "fix", "change", "update", "add retries", "catchup"]
        )
        traces = [
            {"event": "dag_audit", "from": "user", "to": "coder",
             "timestamp": ts, "message": {"text": "DAG audit request (read-only)"}},
            {"event": "dag_audit", "from": "coder", "to": "user",
             "timestamp": ts, "message": {"text": result_str[:200]}},
        ]
        return {"message": result_str, "has_suggestions": has_suggestions, "traces": traces}
    except Exception as exc:
        return {"message": f"DAG check failed: {exc}", "has_suggestions": False, "traces": []}


@app.post("/api/dag-apply")
def api_dag_apply(payload: DagApplyRequest) -> dict[str, Any]:
    """
    Apply DAG improvements previously suggested by /api/dag-check.
    The coder agent reads each file, patches it, and verifies syntax.
    """
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    prompt = (
        "Apply the following DAG improvements. For every change:\n"
        "1. Read the current file with read_file first.\n"
        "2. Use patch_file to apply the change surgically.\n"
        "3. Confirm the syntax check passed.\n\n"
        f"Improvements to implement:\n{payload.suggestions}\n\n"
        "After all changes are done, provide a concise summary: which files were modified, "
        "backup locations, and syntax check results for each."
    )
    try:
        result_str = str(_run_with_timeout(coder_run_chat, prompt))
        traces = [
            {"event": "dag_apply", "from": "user", "to": "coder",
             "timestamp": ts, "message": {"text": "Apply DAG improvements (user approved)"}},
            {"event": "dag_apply", "from": "coder", "to": "user",
             "timestamp": ts, "message": {"text": result_str[:200]}},
        ]
        return {"message": result_str, "traces": traces}
    except Exception as exc:
        return {"message": f"DAG apply failed: {exc}", "traces": []}


@app.post("/api/chat/stream")
async def api_chat_stream(payload: ChatRequest) -> StreamingResponse:
    """SSE streaming version of /api/chat.
    Emits: thinking → start_response → token* → end_response → traces → done
    """
    async def generate():
        target = payload.target
        agent_list = (
            ["orchestrator", "analyst", "governance", "ingestion", "coder"]
            if target == "all"
            else [target]
        )
        # Emit thinking events immediately so the UI has something to show
        for name in agent_list:
            yield f"data: {_json.dumps({'type': 'thinking', 'agent': name})}\n\n"

        try:
            result = await asyncio.to_thread(
                _run_target, target, payload.message, payload.session_id, payload.history
            )
        except Exception as exc:
            yield f"data: {_json.dumps({'type': 'error', 'message': str(exc)})}\n\n"
            yield f"data: {_json.dumps({'type': 'done'})}\n\n"
            return

        # Adaptive chunk size: target ~1.5 s total stream time across all responses
        total_chars = sum(len(r.get("text") or "") for r in result.get("responses", []))
        chunk = max(6, total_chars // 150) if total_chars else 6

        for resp in result.get("responses", []):
            name = resp["agent"]
            text = resp.get("text") or ""
            yield f"data: {_json.dumps({'type': 'start_response', 'agent': name})}\n\n"
            for i in range(0, len(text), chunk):
                yield f"data: {_json.dumps({'type': 'token', 'agent': name, 'text': text[i:i + chunk]})}\n\n"
                await asyncio.sleep(0.010)
            yield f"data: {_json.dumps({'type': 'end_response', 'agent': name})}\n\n"

        yield f"data: {_json.dumps({'type': 'traces', 'traces': result.get('traces', [])})}\n\n"
        yield f"data: {_json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no", "Connection": "keep-alive"},
    )


@app.post("/api/chat")
def api_chat(payload: ChatRequest) -> dict[str, Any]:
    try:
        return _run_target(payload.target, payload.message, payload.session_id, payload.history)
    except Exception as exc:  # Keep API stable for UI even if one agent fails unexpectedly
        return {"error": f"Agent call failed: {exc}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8010, reload=False)