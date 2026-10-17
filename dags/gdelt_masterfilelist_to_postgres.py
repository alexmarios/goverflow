from airflow import DAG, Dataset
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.exceptions import AirflowException

import os
import re
from urllib.parse import urlparse as _urlparse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from datetime import timedelta

from kafka_callbacks import on_failure_callback

# Canonical path for masterfilelist - used consistently across all GDELT DAGs
# This path works within the Airflow container environment
MASTERFILE_DIR = "/opt/airflow/dags/data/raw"
LOCAL_PATH = os.path.join(MASTERFILE_DIR, "masterfilelist.txt")

DB_NAME = "stack_db"
DB_CONFIG = {
    "host":     os.environ.get("DB_HOST", "postgres"),
    "port":     int(os.environ.get("DB_PORT", 5432)),
    "dbname":   DB_NAME,
    "user":     os.environ.get("DB_USER", "airflow"),
    "password": os.environ.get("DB_PASSWORD", "airflow"),
}

# Dataset URI must match the actual file path for proper lineage tracking
gdelt_masterfile = Dataset(f"file://{LOCAL_PATH}")

# Downstream Dataset URI — Airflow postgres provider requires host:port/db/schema/table.
# Host is read from POSTGRES_DSN env var (written by access_hosts.py) so it stays
# consistent with gkg_daily_sync.py which parses its own POSTGRES_CONN.
_pg_dsn = _urlparse(os.environ.get("POSTGRES_DSN", f"postgresql://stack_user:stack_password@100.95.246.75:5432/{DB_NAME}"))
postgres_raw_data = Dataset(f"postgresql://{_pg_dsn.hostname}:{_pg_dsn.port or 5432}/{DB_NAME}/public/raw_data")


def ensure_db():
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            dbname="postgres",
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
            if not cur.fetchone():
                cur.execute(f"CREATE DATABASE {DB_NAME}")
                print(f"Database '{DB_NAME}' created.")
            else:
                print(f"Database '{DB_NAME}' already exists.")
    except psycopg2.Error as e:
        raise AirflowException(f"Database setup failed: {e}")
    finally:
        if conn:
            conn.close()


def ensure_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS raw_data (
                id              SERIAL PRIMARY KEY,
                file_size_bytes BIGINT,
                md5_hash        TEXT,
                file_url        TEXT UNIQUE,
                file_type       TEXT,
                file_timestamp  TIMESTAMP,
                ingested_at     TIMESTAMP DEFAULT NOW()
            );
        """)
    conn.commit()


def get_watermark(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT MAX(file_timestamp) FROM raw_data;")
        result = cur.fetchone()[0]
    return result


def extract_file_type(url: str) -> str:
    if ".export."   in url: return "export"
    if ".mentions." in url: return "mentions"
    if ".gkg."      in url: return "gkg"
    return "unknown"


def extract_file_timestamp(url: str):
    from datetime import datetime
    match = re.search(r"/(\d{14})\.", url)
    if match:
        return datetime.strptime(match.group(1), "%Y%m%d%H%M%S")
    return None


def load_to_postgres():
    conn = None
    try:
        ensure_db()

        conn = psycopg2.connect(**DB_CONFIG)
        ensure_table(conn)
        watermark = get_watermark(conn)

        if watermark:
            print(f"Watermark: {watermark} — skipping rows with file_timestamp <= watermark.")
        else:
            print("No watermark found — full load.")

        rows = []
        skipped = 0
        parse_errors = 0
        
        # Ensure directory exists before checking for file
        os.makedirs(MASTERFILE_DIR, exist_ok=True)
        
        # Check if file exists before attempting to read
        if not os.path.exists(LOCAL_PATH):
            raise AirflowException(
                f"Masterfile not found at path: {LOCAL_PATH}. "
                f"Ensure gdelt_masterfilelist_sync DAG has run successfully and wrote to this location."
            )
        
        with open(LOCAL_PATH, "r", errors="ignore") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                parts = re.split(r"\s+", line, maxsplit=2)
                if len(parts) != 3:
                    parse_errors += 1
                    if parse_errors <= 5:  # Log first 5 errors only
                        print(f"Warning: Skipping malformed line {line_num}: {line[:80]}")
                    continue
                size_bytes, md5, url = parts
                
                # PostgreSQL does not support NUL characters in TEXT/VARCHAR fields.
                # Sanitize all components of the row.
                md5 = md5.replace('\x00', '')
                url = url.replace('\x00', '')
                
                file_ts = extract_file_timestamp(url)

                if watermark and file_ts and file_ts <= watermark:
                    skipped += 1
                    continue

                rows.append((
                    int(size_bytes),
                    md5,
                    url,
                    extract_file_type(url),
                    file_ts,
                ))

        print(f"Skipped {skipped} rows (already ingested). Parse errors: {parse_errors}. Processing {len(rows)} new rows.")

        # Batch insert for efficiency - use executemany instead of row-by-row
        inserted = 0
        if rows:
            with conn.cursor() as cur:
                # We use a more robust insertion method to avoid NUL character issues 
                # even if some slipped through, although replace('\x00', '') should handle it.
                cur.executemany("""
                    INSERT INTO raw_data (file_size_bytes, md5_hash, file_url, file_type, file_timestamp)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (file_url) DO NOTHING;
                """, rows)
                inserted = cur.rowcount

        conn.commit()
        print(f"Inserted {inserted} new rows into raw_data.")
        
    except FileNotFoundError as e:
        raise AirflowException(f"File not found: {e}")
    except psycopg2.Error as e:
        raise AirflowException(f"Database error: {e}")
    except Exception as e:
        raise AirflowException(f"Unexpected error during load: {e}")
    finally:
        if conn:
            conn.close()


with DAG(
    dag_id="gdelt_masterfilelist_to_postgres",
    schedule=[gdelt_masterfile],
    start_date=days_ago(1),
    catchup=False,
    tags=["gdelt", "postgres", "ingestion"],
    description=(
        "Triggered by gdelt_masterfilelist_sync. Parses the GDELT masterfilelist.txt "
        "and inserts new file metadata rows (URL, type, timestamp, MD5) into "
        "stack_db.public.raw_data using a watermark to skip already-ingested entries."
    ),
    on_failure_callback=on_failure_callback,
    default_args={
        "execution_timeout": timedelta(minutes=15),
        "retries": 2,
        "retry_delay": timedelta(minutes=2),
    },
) as dag:
    PythonOperator(
        task_id="load_to_postgres",
        python_callable=load_to_postgres,
        outlets=[postgres_raw_data],
    )
