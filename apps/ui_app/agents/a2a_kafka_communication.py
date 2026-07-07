"""
A2A Kafka Communication
-----------------------
Central module for all agent-to-agent Kafka messaging.

Every agent imports from here instead of duplicating producer/consumer code.

Usage
-----
In a specialist agent module:

    from a2a_kafka_communication import kafka_worker, send_to_orchestrator

    # Run as a standalone Kafka worker process:
    if __name__ == "__main__":
        kafka_worker("analyst", run_agent_task)

    # Proactively notify the orchestrator from anywhere in the agent:
    send_to_orchestrator("analyst", "anomaly_detected", {"table": "gdelt_events"})

Topics
------
    agent.{name}.inbox          — orchestrator → agent (task requests)
    agent.orchestrator.inbox    — agent → orchestrator (responses + notifications)
"""

import json
import time
import uuid
from typing import Any, Callable


# ── Request-reply: orchestrator → agent → orchestrator ────────────────────────

def dispatch_and_wait(
    target: str,
    task: str,
    params: dict[str, Any],
    context: dict[str, Any] | None = None,
    timeout_ms: int = 120_000,
) -> dict[str, Any] | None:
    """Publish a task_request to agent.{target}.inbox and block until the
    task_response with a matching correlation_id arrives on
    agent.orchestrator.inbox.

    The reply consumer is opened BEFORE the message is published so a fast
    agent response is never missed. Each call uses a unique consumer group
    (orch-reply-{correlation_id}) so concurrent dispatches never steal each
    other's replies.

    Returns the response payload dict on success, or None on timeout/error so
    the caller can fall back to a direct in-process function call.

    Args:
        target:     Agent name: "analyst" | "governance" | "coder" | "ingestion"
        task:       Short task description forwarded to run_agent_task().
        params:     Task parameters (e.g. {"message": user_message}).
        context:    Optional call context (e.g. {"session_id": "abc"}).
        timeout_ms: How long to wait for the response, in milliseconds.
    """
    try:
        from kafka import KafkaConsumer, KafkaProducer
        from access_hosts import KAFKA_BROKER
    except ImportError as exc:
        print(f"[a2a] kafka-python not available: {exc}")
        return None

    correlation_id = str(uuid.uuid4())
    inbox_topic    = f"agent.{target}.inbox"
    reply_topic    = "agent.orchestrator.inbox"

    envelope = {
        "message_id":     str(uuid.uuid4()),
        "correlation_id": correlation_id,
        "from_agent":     "orchestrator",
        "to_agent":       target,
        "type":           "task_request",
        "reply_topic":    reply_topic,
        "payload": {
            "task":    task,
            "params":  params or {},
            "context": context or {},
        },
    }

    try:
        # Open reply consumer FIRST to avoid missing a fast response.
        reply_consumer = KafkaConsumer(
            reply_topic,
            bootstrap_servers=KAFKA_BROKER,
            group_id=f"orch-reply-{correlation_id}",
            auto_offset_reset="latest",
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            consumer_timeout_ms=timeout_ms,
        )

        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        producer.send(inbox_topic, value=envelope)
        producer.flush()
        producer.close()
        print(f"[a2a] → {inbox_topic} (corr={correlation_id[:8]})")

        for msg in reply_consumer:
            val = msg.value
            if (val.get("correlation_id") == correlation_id
                    and val.get("type") == "task_response"):
                reply_consumer.close()
                print(f"[a2a] ← {target} response received")
                return val.get("payload", {})

        reply_consumer.close()
        print(f"[a2a] timeout waiting for {target} ({timeout_ms}ms)")
        return None

    except Exception as exc:
        print(f"[a2a] dispatch_and_wait error for {target}: {exc}")
        return None


# ── Producer: agent → orchestrator ────────────────────────────────────────────

def send_to_orchestrator(from_agent: str, event_type: str, payload: dict[str, Any]) -> None:
    """Publish a notification to the orchestrator's Kafka inbox.

    Call this from anywhere inside an agent to proactively inform the
    orchestrator — e.g. after fixing a DAG, raising a quality alert, or
    completing a significant analysis.

    Args:
        from_agent:  Name of the sending agent ("analyst", "coder", …)
        event_type:  Short label for the event ("dag_fixed", "alert_raised", …)
        payload:     Arbitrary dict with event details.
    """
    try:
        from kafka import KafkaProducer
        from access_hosts import KAFKA_BROKER

        message = {
            "message_id":  str(uuid.uuid4()),
            "from_agent":  from_agent,
            "to_agent":    "orchestrator",
            "type":        "agent_notification",
            "event_type":  event_type,
            "payload":     payload,
        }
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        producer.send("agent.orchestrator.inbox", value=message)
        producer.flush()
        producer.close()
        print(f"[{from_agent}] → orchestrator: {event_type}")
    except Exception as exc:
        print(f"[{from_agent}] send_to_orchestrator failed: {exc}")


# ── Consumer: orchestrator → agent ────────────────────────────────────────────

def kafka_worker(agent_name: str, run_task_fn: Callable) -> None:
    """Listen on agent.{agent_name}.inbox for A2A task requests.

    Deserializes each incoming envelope, calls run_task_fn, and publishes
    the result back to the reply_topic specified in the envelope (typically
    agent.orchestrator.inbox).

    Reconnects automatically if the broker drops — same backoff pattern as
    kafka_consumer.py:
        NoBrokersAvailable  → wait 30 s
        Any other exception → wait 10 s

    Args:
        agent_name:   Logical name of this agent ("analyst", "coder", …)
        run_task_fn:  Callable with signature:
                          run_task_fn(task, params, context) -> dict
                      The function must accept all three positional arguments.
    """
    try:
        from kafka import KafkaConsumer, KafkaProducer
        from kafka.errors import NoBrokersAvailable
        from access_hosts import KAFKA_BROKER
    except ImportError as exc:
        print(f"[{agent_name}] kafka-python not available — worker not started ({exc})")
        return

    inbox_topic = f"agent.{agent_name}.inbox"
    group_id    = f"{agent_name}-worker-group"

    while True:
        try:
            consumer = KafkaConsumer(
                inbox_topic,
                bootstrap_servers=KAFKA_BROKER,
                group_id=group_id,
                auto_offset_reset="latest",
                enable_auto_commit=True,
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            )
            print(f"[{agent_name}] Kafka worker listening on '{inbox_topic}'...")

            for msg in consumer:
                envelope = msg.value
                if envelope.get("type") != "task_request":
                    continue

                payload        = envelope.get("payload", {})
                task           = payload.get("task", "")
                params         = payload.get("params", {})
                context        = payload.get("context", {})
                reply_topic    = envelope.get("reply_topic", "agent.orchestrator.inbox")
                correlation_id = envelope.get("correlation_id")

                print(f"[{agent_name}] Task received: {task!r} (corr={correlation_id})")
                try:
                    result = run_task_fn(task, params, context)
                except Exception as exc:
                    result = {"status": "error", "task": task, "result": str(exc)}

                response = {
                    "message_id":    str(uuid.uuid4()),
                    "correlation_id": correlation_id,
                    "from_agent":    agent_name,
                    "to_agent":      envelope.get("from_agent", "orchestrator"),
                    "type":          "task_response",
                    "payload":       result,
                }
                producer = KafkaProducer(
                    bootstrap_servers=KAFKA_BROKER,
                    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                )
                producer.send(reply_topic, response)
                producer.flush()
                producer.close()
                print(f"[{agent_name}] Response sent to '{reply_topic}'")

        except NoBrokersAvailable:
            print(f"[{agent_name}] Broker not available, retrying in 30s...")
            time.sleep(30)
        except Exception as exc:
            print(f"[{agent_name}] Kafka error: {exc}, retrying in 10s...")
            time.sleep(10)
