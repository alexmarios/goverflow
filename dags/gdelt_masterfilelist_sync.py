from airflow import DAG, Dataset
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

import os
import shutil

import requests

from kafka_callbacks import on_failure_callback

GDELT_URL = "http://data.gdeltproject.org/gdeltv2/masterfilelist.txt"
# Canonical path for masterfilelist - must match gdelt_masterfilelist_to_postgres DAG
# This path works within the Airflow container environment
MASTERFILE_DIR = "/opt/airflow/dags/data/raw"
LOCAL_PATH = os.path.join(MASTERFILE_DIR, "masterfilelist.txt")
_CHUNK = 1 * 1024 * 1024   # 1 MB
_MAX_RETRIES = 10

gdelt_masterfile = Dataset(f"file://{LOCAL_PATH}")


def download_masterfilelist():
    os.makedirs(os.path.dirname(LOCAL_PATH), exist_ok=True)
    tmp_path = LOCAL_PATH + ".tmp"

    success = False
    downloaded = 0
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            with requests.get(GDELT_URL, stream=True, timeout=(10, 120)) as resp:
                resp.raise_for_status()
                expected = int(resp.headers.get("Content-Length", 0))
                downloaded = 0
                with open(tmp_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=_CHUNK):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)

            if expected and downloaded < expected:
                raise ValueError(
                    f"Incomplete download: got {downloaded:,} of {expected:,} bytes"
                )
            success = True
            break  # success — exit retry loop
        except Exception as exc:
            # Only unlink if the file actually exists to avoid secondary errors
            if os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass
            if attempt == _MAX_RETRIES:
                raise
            print(f"Attempt {attempt}/{_MAX_RETRIES} failed ({exc}), retrying…")

    if success:
        # Robust check before moving to ensure the file is present
        if os.path.exists(tmp_path):
            shutil.move(tmp_path, LOCAL_PATH)
            print(f"Downloaded masterfilelist.txt → {LOCAL_PATH} ({downloaded:,} bytes)")
        else:
            raise FileNotFoundError(f"Temporary file {tmp_path} disappeared before move.")
    else:
        raise RuntimeError("Failed to download masterfilelist after maximum retries.")


with DAG(
    dag_id="gdelt_masterfilelist_sync",
    start_date=days_ago(1),
    schedule=timedelta(minutes=15),
    catchup=False,
    tags=["gdelt", "ingestion", "download"],
    description=(
        "Downloads the GDELT v2 masterfilelist.txt every 15 minutes from "
        "data.gdeltproject.org. Atomic write (tmp → final) with up to 10 retries. "
        "Emits a Dataset event that triggers gdelt_masterfilelist_to_postgres."
    ),
    on_failure_callback=on_failure_callback,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
    },
) as dag:
    PythonOperator(
        task_id="download_masterfilelist",
        python_callable=download_masterfilelist,
        outlets=[gdelt_masterfile],
    )
