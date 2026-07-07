from airflow import DAG, Dataset
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

import os

from kafka_callbacks import on_failure_callback

MASTERFILE_DIR = "/opt/airflow/dags/data/raw"
LOCAL_PATH = os.path.join(MASTERFILE_DIR, "masterfilelist.txt")

gdelt_masterfile = Dataset(f"file://{LOCAL_PATH}")


def validate_masterfilelist():
    """Validate that the masterfilelist.txt exists and is non-empty."""
    if not os.path.exists(LOCAL_PATH):
        raise FileNotFoundError(f"Masterfilelist not found at {LOCAL_PATH}")
    
    file_size = os.path.getsize(LOCAL_PATH)
    if file_size == 0:
        raise ValueError(f"Masterfilelist is empty at {LOCAL_PATH}")
    
    with open(LOCAL_PATH, "r") as f:
        line_count = sum(1 for _ in f)
    
    print(f"Validation passed: {LOCAL_PATH} ({file_size:,} bytes, {line_count:,} lines)")
    return {"file_size": file_size, "line_count": line_count}


with DAG(
    dag_id="gdelt_masterfilelist_validate",
    start_date=days_ago(1),
    schedule=timedelta(minutes=30),
    catchup=False,
    tags=["gdelt", "validation", "quality"],
    description="Validates that the GDELT masterfilelist.txt has been downloaded and is non-empty.",
    on_failure_callback=on_failure_callback,
) as dag:
    PythonOperator(
        task_id="validate_masterfilelist",
        python_callable=validate_masterfilelist,
        inlets=[gdelt_masterfile],
    )
