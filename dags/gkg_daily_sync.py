from datetime import datetime, timedelta, timezone
import logging
import csv
import zipfile
import io
import sys
import requests
import psycopg2
from psycopg2.extras import RealDictCursor
from pymongo import MongoClient

from urllib.parse import urlparse as _urlparse

from airflow import DAG, Dataset
from airflow.decorators import task
from airflow.utils.dates import days_ago

from kafka_callbacks import on_failure_callback

# Configuration
POSTGRES_CONN = "postgresql://stack_user:stack_password@100.95.246.75:5432/stack_db"
MONGO_CONN = "mongodb://admin:yourpassword@100.95.246.75:27017/"
MONGO_DB = "gkd_db"
MONGO_COLL = "last_24hours_gkd"
MONGO_STAGING = "last_24hours_gkd_staging"

# Lineage Datasets — Airflow postgres provider requires host:port/db/schema/table.
# Parsed from POSTGRES_CONN/MONGO_CONN (set from access_hosts.py tailscale config)
# so the URIs stay in sync with the actual connection strings automatically.
_pg = _urlparse(POSTGRES_CONN)
_mg = _urlparse(MONGO_CONN)
postgres_raw_data = Dataset(f"postgresql://{_pg.hostname}:{_pg.port or 5432}/{_pg.path.lstrip('/')}/public/raw_data")
mongo_gkd = Dataset(f"mongodb://{_mg.hostname}:{_mg.port or 27017}/{MONGO_DB}/{MONGO_COLL}")

BATCH_SIZE = 500  # documents flushed to MongoDB per insert_many
csv.field_size_limit(sys.maxsize)  # some GDELT fields exceed the 128 KB default

GKG_COLUMNS = [
    "GKGRECORDID", "DATE", "SourceCollectionIdentifier", "SourceCommonName",
    "DocumentIdentifier", "Counts", "V2Counts", "Themes", "V2Themes",
    "Locations", "V2Locations", "Persons", "V2Persons", "Organizations",
    "V2Organizations", "V2Tone", "Dates", "GCAM", "SharingImage",
    "RelatedImages", "SocialImageEmbeds", "SocialVideoEmbeds", "Quotations",
    "AllNames", "Amounts", "TranslationInfo", "Extras"
]

default_args = {
    "owner": "airflow",
    "retries": 20,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="gkd_daily_sync",
    schedule="0 0 * * *",
    start_date=days_ago(1),
    catchup=False,
    default_args=default_args,
    tags=["gdelt", "gkg", "mongodb", "daily"],
    description=(
        "Daily ETL: reads GKG file URLs for the past 24 h from PostgreSQL "
        "(stack_db.public.raw_data), downloads and parses each .zip from GDELT, "
        "streams records into MongoDB staging (gkd_db.last_24hours_gkd_staging) "
        "in batches of 500, then atomically renames staging → live collection."
    ),
    on_failure_callback=on_failure_callback,
) as dag:

    @task(inlets=[postgres_raw_data])
    def extract_from_postgres(data_interval_start: datetime = None):
        """Fetch GKG file URLs for the previous 24 hours."""
        window_end   = data_interval_start
        window_start = data_interval_start - timedelta(hours=24)

        logging.info("Querying PostgreSQL: %s → %s", window_start, window_end)

        conn = psycopg2.connect(POSTGRES_CONN, cursor_factory=RealDictCursor)
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT *
                    FROM public.raw_data
                    WHERE file_type = 'gkg'
                      AND file_timestamp >= %s
                      AND file_timestamp <  %s
                    ORDER BY file_timestamp
                    """,
                    (window_start, window_end),
                )
                rows = cur.fetchall()
            logging.info("PostgreSQL returned %d rows.", len(rows))
            return rows
        finally:
            conn.close()

    @task
    def stream_to_staging(rows):
        """
        Download, parse, and insert each GKG file one at a time directly into
        the staging collection. Never accumulates all documents in memory and
        never passes large data through XCom — only a small summary is returned.

        Each file's records are flushed to MongoDB in BATCH_SIZE chunks so
        memory usage is bounded to roughly one batch at a time.
        """
        if not rows:
            logging.warning("No rows — skipping.")
            return {"total_records": 0, "files_ok": 0, "failed_urls": []}

        client = MongoClient(MONGO_CONN)
        try:
            staging = client[MONGO_DB][MONGO_STAGING]
            staging.drop()  # clean up any leftover from a previous failed run

            total_inserted = 0
            failed_urls    = []
            ingested_at    = datetime.now(timezone.utc).isoformat()

            for row in rows:
                url = row.get("file_url")
                if not url:
                    continue

                try:
                    response = requests.get(url, timeout=60)
                    response.raise_for_status()

                    batch = []
                    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                        with z.open(z.namelist()[0]) as f:
                            raw = f.read()
                            try:
                                content = raw.decode("utf-8")
                            except UnicodeDecodeError:
                                content = raw.decode("latin-1")
                            reader = csv.DictReader(
                                content.splitlines(keepends=True),
                                fieldnames=GKG_COLUMNS,
                                delimiter="\t",
                            )
                            for record in reader:
                                record["_source_file_url"] = url
                                record["_ingested_at"]     = ingested_at
                                batch.append(record)
                                if len(batch) >= BATCH_SIZE:
                                    staging.insert_many(batch, ordered=False)
                                    total_inserted += len(batch)
                                    batch = []

                    if batch:
                        staging.insert_many(batch, ordered=False)
                        total_inserted += len(batch)

                    logging.info("OK %s — running total: %d", url, total_inserted)

                except Exception as exc:
                    logging.warning("FAILED %s — %s", url, exc)
                    failed_urls.append({"url": url, "error": str(exc)})

            logging.info(
                "Staging load complete: %d records, %d files ok, %d failed.",
                total_inserted, len(rows) - len(failed_urls), len(failed_urls),
            )
            return {
                "total_records": total_inserted,
                "files_ok":      len(rows) - len(failed_urls),
                "failed_urls":   failed_urls,
            }
        finally:
            client.close()

    @task(outlets=[mongo_gkd])
    def atomic_swap(summary):
        """
        Rename staging → live only after all data is safely written.
        The live collection is untouched until this point, so any crash in
        stream_to_staging leaves the previous day's data intact.
        """
        if summary.get("total_records", 0) == 0:
            logging.warning("No records in staging — skipping swap.")
            return

        client = MongoClient(MONGO_CONN)
        try:
            client[MONGO_DB][MONGO_STAGING].rename(MONGO_COLL, dropTarget=True)
            logging.info(
                "Atomic swap complete — %s now has %d documents.",
                MONGO_COLL, summary["total_records"],
            )
        finally:
            client.close()

    @task
    def report_summary(summary):
        """Log a human-readable run summary."""
        failed = summary.get("failed_urls", [])
        logging.info("=== GKD Daily Sync Summary ===")
        logging.info("  Records loaded : %d", summary.get("total_records", 0))
        logging.info("  Files OK       : %d", summary.get("files_ok", 0))
        logging.info("  Failed URLs    : %d", len(failed))
        for entry in failed:
            logging.warning("  FAILED %s — %s", entry["url"], entry["error"])
        if not failed:
            logging.info("All files ingested successfully.")

    # Pipeline
    rows    = extract_from_postgres()
    summary = stream_to_staging(rows)
    atomic_swap(summary)
    report_summary(summary)
