"""
Catalog Manifest Refresh DAG
-----------------------------
Runs every 30 minutes. Pulls catalog data from three sources in parallel:
  1. OpenMetadata REST API — registered services, databases, OM-managed tables
  2. PostgreSQL (direct) — all schemas/tables/columns/row-counts per database
  3. MongoDB (direct)   — all collections with doc-counts and sample field names

Writes a JSON manifest to the governance agent's memory directory so the agent
gets a full known-assets snapshot injected at session start without spending
LLM calls on catalog discovery.
"""

import datetime
import json
import os
from concurrent.futures import ThreadPoolExecutor

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

MANIFEST_PATH = "/home/alexpi/goverflow/apps/ui_app/agents/memory/catalog_manifest.json"

OM_HOST  = os.getenv("OPENMETADATA_HOST", "http://openmetadata-server:8585")
OM_TOKEN = os.getenv("OPENMETADATA_TOKEN", os.getenv("AIRFLOW__LINEAGE__JWT_TOKEN", ""))
DB_USER  = os.getenv("DB_USER", "stack_user")
DB_PASS  = os.getenv("DB_PASSWORD", "")
MONGO_URI = os.getenv("MONGO_URI", f"mongodb://admin:{os.getenv('MONGO_PASSWORD','')}@mongodb:27017")

PG_BASE_DSN  = f"postgresql://{DB_USER}:{DB_PASS}@postgres:5432"
# Databases to skip when auto-discovering (Postgres internals)
PG_SKIP_DBS  = {"template0", "template1"}


def refresh_catalog_manifest() -> None:
    import psycopg2
    import psycopg2.extras
    import pymongo
    import requests

    om_headers = {
        "Authorization": f"Bearer {OM_TOKEN}",
        "Content-Type": "application/json",
    }

    # ── OpenMetadata helpers ───────────────────────────────────────────────────

    def _om_get(path: str, params: dict | None = None) -> dict:
        try:
            r = requests.get(f"{OM_HOST}{path}", headers=om_headers, params=params, timeout=30)
            return r.json() if r.ok else {}
        except Exception as exc:
            print(f"[manifest] OM GET {path} failed: {exc}")
            return {}

    def _fetch_pages(path: str, params: dict | None = None, max_pages: int = 20) -> list:
        params = dict(params or {})
        params.setdefault("limit", 100)
        items: list = []
        after = None
        for _ in range(max_pages):
            if after:
                params["after"] = after
            resp = _om_get(path, params)
            batch = resp.get("data", [])
            items.extend(batch)
            after = resp.get("paging", {}).get("after")
            if not after or len(batch) < params["limit"]:
                break
        return items

    def _fetch_om_services() -> list:
        return _om_get("/api/v1/services/databaseServices", {"limit": 50}).get("data", [])

    def _fetch_om_databases() -> list:
        return _fetch_pages("/api/v1/databases", {"fields": "service"})

    def _fetch_om_tables() -> list:
        return _fetch_pages("/api/v1/tables", {"fields": "columns,tags,owner,description", "limit": 100})

    def _fetch_om_test_counts() -> dict:
        raw = _fetch_pages("/api/v1/dataQuality/testCases", {"fields": "entityLink"})
        counts: dict[str, int] = {}
        for tc in raw:
            parts = tc.get("entityLink", "").strip("<>").split("::")
            if len(parts) >= 3:
                counts[parts[2]] = counts.get(parts[2], 0) + 1
        return counts

    # ── PostgreSQL direct extraction ───────────────────────────────────────────

    def _fetch_pg_database(db_name: str) -> dict | None:
        dsn = f"{PG_BASE_DSN}/{db_name}"
        try:
            conn = psycopg2.connect(dsn)
            conn.set_session(readonly=True, autocommit=True)
            tables = []
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                # All user tables with column counts
                cur.execute("""
                    SELECT
                        t.table_schema,
                        t.table_name,
                        COUNT(c.column_name) AS col_count
                    FROM information_schema.tables t
                    JOIN information_schema.columns c
                      ON c.table_schema = t.table_schema
                     AND c.table_name  = t.table_name
                    WHERE t.table_schema NOT IN ('pg_catalog','information_schema','pg_toast')
                      AND t.table_type = 'BASE TABLE'
                    GROUP BY t.table_schema, t.table_name
                    ORDER BY t.table_schema, t.table_name
                """)
                table_rows = cur.fetchall()

                for row in table_rows:
                    schema     = row["table_schema"]
                    table_name = row["table_name"]
                    col_count  = row["col_count"]

                    # Column names and types
                    cur.execute("""
                        SELECT column_name, data_type
                        FROM information_schema.columns
                        WHERE table_schema = %s AND table_name = %s
                        ORDER BY ordinal_position
                    """, (schema, table_name))
                    columns = [{"name": r["column_name"], "type": r["data_type"]} for r in cur.fetchall()]

                    # Approximate row count from pg_stat (fast, no seq-scan)
                    cur.execute("""
                        SELECT reltuples::bigint AS row_count
                        FROM pg_class
                        WHERE relname = %s
                          AND relnamespace = (SELECT oid FROM pg_namespace WHERE nspname = %s)
                    """, (table_name, schema))
                    rc_row = cur.fetchone()
                    row_count = rc_row["row_count"] if rc_row else None

                    tables.append({
                        "schema":    schema,
                        "table":     table_name,
                        "col_count": col_count,
                        "row_count": row_count,
                        "columns":   columns,
                    })
            conn.close()
            print(f"[manifest] PG {db_name}: {len(tables)} tables")
            return {"database": db_name, "tables": tables}
        except Exception as exc:
            print(f"[manifest] PG {db_name} failed: {exc}")
            return None

    # ── MongoDB direct extraction ──────────────────────────────────────────────

    def _fetch_mongo() -> list:
        catalog = []
        try:
            client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            for db_name in client.list_database_names():
                if db_name in ("admin", "local", "config"):
                    continue
                db = client[db_name]
                collections = []
                for col_name in db.list_collection_names():
                    col = db[col_name]
                    try:
                        doc_count = col.estimated_document_count()
                    except Exception:
                        doc_count = None
                    # Sample one document to discover field names
                    sample = col.find_one({}, projection={"_id": 0})
                    fields = list(sample.keys())[:30] if sample else []
                    collections.append({
                        "name":          col_name,
                        "doc_count":     doc_count,
                        "sample_fields": fields,
                    })
                catalog.append({"database": db_name, "collections": collections})
            client.close()
            print(f"[manifest] Mongo: {sum(len(d['collections']) for d in catalog)} collections")
        except Exception as exc:
            print(f"[manifest] MongoDB failed: {exc}")
        return catalog

    # ── Discover all PostgreSQL databases dynamically ──────────────────────────

    pg_databases: list[str] = []
    try:
        conn = psycopg2.connect(f"{PG_BASE_DSN}/postgres")
        conn.set_session(readonly=True, autocommit=True)
        with conn.cursor() as cur:
            cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false ORDER BY datname")
            pg_databases = [r[0] for r in cur.fetchall() if r[0] not in PG_SKIP_DBS]
        conn.close()
        print(f"[manifest] discovered PG databases: {pg_databases}")
    except Exception as exc:
        print(f"[manifest] PG database discovery failed: {exc}")

    # ── Run all fetches in parallel ────────────────────────────────────────────

    with ThreadPoolExecutor(max_workers=4 + len(pg_databases)) as pool:
        f_svcs   = pool.submit(_fetch_om_services)
        f_dbs    = pool.submit(_fetch_om_databases)
        f_tables = pool.submit(_fetch_om_tables)
        f_tests  = pool.submit(_fetch_om_test_counts)
        f_mongo  = pool.submit(_fetch_mongo)
        f_pg     = {db: pool.submit(_fetch_pg_database, db) for db in pg_databases}

        services_raw  = f_svcs.result()
        databases_raw = f_dbs.result()
        om_tables_raw = f_tables.result()
        test_counts   = f_tests.result()
        mongo_catalog = f_mongo.result()
        pg_catalog    = [r for db in pg_databases if (r := f_pg[db].result()) is not None]

    # ── Build OM table entries ─────────────────────────────────────────────────

    om_tables = []
    for t in om_tables_raw:
        fqn      = t.get("fullyQualifiedName", "")
        tags     = [tg.get("tagFQN") for tg in (t.get("tags") or []) if tg.get("tagFQN")]
        owner    = (t.get("owner") or {}).get("displayName") or (t.get("owner") or {}).get("name")
        has_desc = bool((t.get("description") or "").strip())
        q_count  = test_counts.get(fqn, 0)
        columns  = [
            {"name": c.get("name"), "type": c.get("dataType")}
            for c in (t.get("columns") or [])
        ]

        gaps: list[str] = []
        if not owner:    gaps.append("no_owner")
        if not has_desc: gaps.append("no_description")
        if not tags:     gaps.append("no_tags")
        if q_count == 0: gaps.append("no_quality_tests")

        om_tables.append({
            "fqn":       fqn,
            "schema":    (t.get("databaseSchema") or {}).get("fullyQualifiedName", ""),
            "col_count": len(columns),
            "columns":   columns,
            "tags":      tags or None,
            "gaps":      gaps or None,
        })

    # ── Write manifest ─────────────────────────────────────────────────────────

    manifest = {
        "refreshed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "openmetadata": {
            "services": [
                {"fqn": s.get("fullyQualifiedName", s.get("name")), "type": s.get("serviceType")}
                for s in services_raw
            ],
            "databases": [
                {
                    "fqn":     d.get("fullyQualifiedName"),
                    "service": (d.get("service") or {}).get("fullyQualifiedName"),
                }
                for d in databases_raw
            ],
            "tables": om_tables,
        },
        "postgres": pg_catalog,
        "mongo":    mongo_catalog,
    }

    os.makedirs(os.path.dirname(MANIFEST_PATH), exist_ok=True)
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)

    n_om  = len(om_tables)
    n_pg  = sum(len(d["tables"]) for d in pg_catalog)
    n_mg  = sum(len(d["collections"]) for d in mongo_catalog)
    print(f"[manifest] done — OM:{n_om} tables | PG:{n_pg} tables | Mongo:{n_mg} collections → {MANIFEST_PATH}")


with DAG(
    dag_id="catalog_manifest_refresh",
    start_date=days_ago(1),
    schedule=timedelta(minutes=30),
    catchup=False,
    max_active_runs=1,
    tags=["governance", "catalog"],
) as dag:
    PythonOperator(
        task_id="refresh_catalog_manifest",
        python_callable=refresh_catalog_manifest,
    )
