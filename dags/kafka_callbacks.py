"""
Shared Airflow failure callback — publishes an event to Kafka topic "airflow-events".
The orchestrator agent (agent_orchestrator.py) listens on that topic and acts.

Broker address comes from the KAFKA_BROKER env var (set it in your docker-compose).
Default: host.docker.internal:29092  (reaches the host machine from inside Docker).
"""

import json
import os
import logging

log = logging.getLogger(__name__)

KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "goverflow-kafka-1:9092")
KAFKA_TOPIC = "airflow-events"


def on_failure_callback(context: dict) -> None:
    """
    Wire this to on_failure_callback on any DAG or task.
    Publishes a JSON event so the orchestrator agent can react immediately.
    Failures are silently logged if Kafka is unavailable — Airflow is never affected.
    """
    try:
        from kafka import KafkaProducer

        event = {
            "dag_id":         context["dag"].dag_id,
            "dag_run_id":     context["run_id"],
            "task_id":        context["task_instance"].task_id,
            "try_number":     context["task_instance"].try_number,
            "state":          "failed",
            "execution_date": str(context.get("execution_date", "")),
        }

        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            # fail fast — don't block Airflow if Kafka is slow
            request_timeout_ms=5000,
            retries=1,
        )
        producer.send(KAFKA_TOPIC, value=event)
        producer.flush(timeout=5)
        producer.close()

        log.info("[kafka_callback] Event sent: %s", event)

    except Exception as e:
        # Never let a callback failure hide the real DAG failure
        log.warning("[kafka_callback] Could not send Kafka event: %s", e)
