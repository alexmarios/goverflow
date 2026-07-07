"""
model_config.py — Central model configuration for all agents
=============================================================
Edit this file to change which model each agent uses without touching
any agent code.

Each agent entry supports these keys:
  model           — model identifier (e.g. "qwen3.5:397b-cloud", "gpt-4o", "claude-sonnet-4-6")
  model_provider  — LangChain provider name: "ollama" | "openai" | "anthropic" | "google_genai" | ...
  base_url        — (optional) custom endpoint, required for self-hosted/Ollama
  temperature     — 0.0 = deterministic, 1.0 = creative
  profile         — (optional) provider-specific flags, e.g. {"structured_output": True}
  api_key_env     — name of the environment variable that holds the API key

Usage in agent files (already wired up):
  from model_config import build_model
  model = build_model("analyst")
"""

import os
import time
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

# ── Per-agent model configuration ─────────────────────────────────────────────
# Edit the values here. Keys must match the names used in build_model() calls.

AGENT_MODELS: dict = {

    # ── Analyst ────────────────────────────────────────────────────────────────
    # Handles GDELT data queries across Postgres, MongoDB, Neo4j, Elasticsearch.
    # Needs strong reasoning and tool-calling; structured_output required.
    "analyst": {
        "model":          "deepseek-v4-flash:cloud",
        "model_provider": "ollama",
        "base_url":       "https://ollama.com",
        "temperature":    0.0,
        "profile":        {"structured_output": True},
        "api_key_env":    "OLLAMA_API_KEY",
    },

    # ── Governance ─────────────────────────────────────────────────────────────
    # Enforces data quality, classifies assets, maintains lineage in OpenMetadata.
    # Deterministic output is critical — classifications must be stable.
    "governance": {
        "model":          "nemotron-3-super:cloud",
        "model_provider": "ollama",
        "base_url":       "https://ollama.com",
        "temperature":    0.0,
        "profile":        {"structured_output": True},
        "api_key_env":    "OLLAMA_API_KEY",
    },

    # ── Ingestion ──────────────────────────────────────────────────────────────
    # Monitors GDELT feed health, triggers Airflow DAGs, handles backfill.
    # Low temperature for reliable infrastructure decisions.
    "ingestion": {
        "model":          "gemma4:31b-cloud",
        "model_provider": "ollama",
        "base_url":       "https://ollama.com",
        "temperature":    0.0,
        "profile":        {"structured_output": True},
        "api_key_env":    "OLLAMA_API_KEY",
    },

    # ── Coder ──────────────────────────────────────────────────────────────────
    # Creates and edits Python source files and Airflow DAGs.
    # Deterministic output ensures consistent, reviewable code changes.
    "coder": {
        "model":          "qwen3-coder-next",
        "model_provider": "ollama",
        "base_url":       "https://ollama.com",
        "temperature":    0.0,
        "profile":        {"structured_output": True},
        "api_key_env":    "OLLAMA_API_KEY",
    },

    # ── Orchestrator ───────────────────────────────────────────────────────────
    # Master coordinator: classifies intent, decomposes plans, synthesises
    # results. Uses an LLM for future free-form planning and synthesis steps.
    "orchestrator": {
        "model":          "deepseek-v4-pro:cloud",
        "model_provider": "ollama",
        "base_url":       "https://ollama.com",
        "temperature":    0.0,
        "profile":        {"structured_output": True},
        "api_key_env":    "OLLAMA_API_KEY",
    },

}


# ── Builder ────────────────────────────────────────────────────────────────────

def build_model(agent_name: str):
    """Instantiate and return an LLM for the given agent name.

    Reads AGENT_MODELS[agent_name], resolves the API key from the environment,
    and calls LangChain's init_chat_model() with all configured parameters.

    Raises KeyError if agent_name is not in AGENT_MODELS.
    """
    if agent_name not in AGENT_MODELS:
        raise KeyError(
            f"No model config for '{agent_name}'. "
            f"Available agents: {list(AGENT_MODELS)}"
        )

    cfg = AGENT_MODELS[agent_name]
    api_key = os.getenv(cfg.get("api_key_env", ""), "")

    kwargs: dict = {
        "model_provider": cfg["model_provider"],
        "temperature":    cfg["temperature"],
    }
    if "base_url" in cfg:
        kwargs["base_url"] = cfg["base_url"]
    if "profile" in cfg:
        kwargs["profile"] = cfg["profile"]
    # Only add client_kwargs when an API key is actually configured.
    # Ollama uses a Bearer token; OpenAI/Anthropic providers handle auth
    # through their own environment variables (OPENAI_API_KEY, etc.) and
    # do not need a manual Authorization header.
    if api_key and cfg["model_provider"] == "ollama":
        kwargs["client_kwargs"] = {
            "headers": {"Authorization": f"Bearer {api_key}"}
        }

    return init_chat_model(cfg["model"], **kwargs)


def serialize_lc_messages(messages: list) -> list[dict]:
    """Serialize a LangChain message list to plain dicts for JSON transport.

    All message types are included: system, human, ai, tool.
    System message content is truncated to 800 chars to keep the payload
    reasonable (they contain full reference docs).
    """
    out = []
    for msg in messages:
        t = getattr(msg, "type", "unknown")
        item: dict = {"type": t}
        content = getattr(msg, "content", "")
        if not isinstance(content, str):
            content = str(content)
        # Truncate system messages — they can be tens of kilobytes of docs
        if t == "system" and len(content) > 800:
            item["content"] = content[:800] + f"\n… [{len(content) - 800} chars truncated]"
        else:
            item["content"] = content
        tcs = getattr(msg, "tool_calls", None)
        if tcs:
            item["tool_calls"] = [
                {"name": tc.get("name", ""), "args": tc.get("args", {})}
                for tc in tcs
            ]
        tc_id = getattr(msg, "tool_call_id", None)
        if tc_id:
            item["tool_call_id"] = tc_id
        name = getattr(msg, "name", None)
        if name:
            item["name"] = name
        out.append(item)
    return out


def invoke_with_retry(model, messages, max_attempts: int = 4, base_delay: float = 2.0):
    """Invoke an LLM with exponential backoff on 503 / overload errors.

    Delays: 2s, 4s, 8s before giving up on the 4th attempt.
    All other exceptions are re-raised immediately.
    """
    _RETRYABLE = ("503", "overload", "rate limit", "too many requests", "529")
    for attempt in range(max_attempts):
        try:
            return model.invoke(messages)
        except Exception as exc:
            msg = str(exc).lower()
            if any(tok in msg for tok in _RETRYABLE) and attempt < max_attempts - 1:
                delay = base_delay * (2 ** attempt)
                print(f"[model_config] LLM overload (attempt {attempt+1}/{max_attempts}) "
                      f"— retrying in {delay:.0f}s …  error={exc!r}")
                time.sleep(delay)
            else:
                raise
