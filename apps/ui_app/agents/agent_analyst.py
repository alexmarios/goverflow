"""
Analyst Agent
-------------
GDELT GKG analytics agent — produces 3-hour news digests from
PostgreSQL (stack_db) and MongoDB (gkd_db.last_hour_gkd).
"""

import json
import os
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

import psycopg2
import psycopg2.extras
import psycopg2.pool
from pymongo import MongoClient
from dotenv import load_dotenv
from langchain.messages import HumanMessage, SystemMessage, ToolMessage
from langchain.tools import tool
from langchain_core.messages import BaseMessage

load_dotenv()

try:
    from agents.model_config import build_model, invoke_with_retry, serialize_lc_messages
    from access_hosts import AIRFLOW_URL as _AF_URL, OPENMETADATA_URL as _OM_URL, \
        MONGO_URI as _MG_URI, MONGO_DB as _MG_DB, MONGO_COLL as _MG_COLL
except ModuleNotFoundError:
    from model_config import build_model, invoke_with_retry, serialize_lc_messages
    from access_hosts import AIRFLOW_URL as _AF_URL, OPENMETADATA_URL as _OM_URL, \
        MONGO_URI as _MG_URI, MONGO_DB as _MG_DB, MONGO_COLL as _MG_COLL

# Populated after every run_agent() call so callers can retrieve the raw LangChain
# message chain (tool calls, tool results, final response) for debugging.
LAST_RUN_MESSAGES: list = []

# ── Connection constants ────────────────────────────────────────────────────────
# PostgreSQL uses stack_db (separate from airflow_db in access_hosts)
POSTGRES_CONN = "postgresql://stack_user:stack_password@100.95.246.75:5432/stack_db"
MONGO_CONN    = _MG_URI
MONGO_DB      = _MG_DB
MONGO_COLL    = _MG_COLL

# ── Knowledge docs ──────────────────────────────────────────────────────────────
_MEMORY_DIR = os.path.join(os.path.dirname(__file__), "memory", "knowledge")

def _load_doc(filename: str, stop_at: str = "") -> str:
    path = os.path.join(_MEMORY_DIR, filename)
    try:
        with open(path) as f:
            raw = f.read()
        if stop_at:
            cut = raw.find(stop_at)
            return raw[:cut].strip() if cut != -1 else raw.strip()
        return raw.strip()
    except FileNotFoundError as e:
        print(f"[analyst] knowledge doc not found: {e}")
        return ""

_MONGO_DOCS    = _load_doc("mongodb-context7.md", stop_at="## Atlas Administration API")
_POSTGRES_DOCS = _load_doc("postgressql-context7.md")

# ── GDELT field parsers ─────────────────────────────────────────────────────────

def _parse_semicolon_names(field: str) -> list[str]:
    """Parse V2Persons / V2Organizations / V2Locations (name,offset;name,offset;...)."""
    if not field:
        return []
    names = []
    for entry in field.split(";"):
        entry = entry.strip()
        if not entry:
            continue
        # V2 fields: "name,charoffset" — take the part before the last comma
        parts = entry.rsplit(",", 1)
        names.append(parts[0].strip())
    return names


def _parse_v2themes(field: str) -> list[str]:
    """Parse V2Themes (THEME,offset;THEME,offset;...)."""
    if not field:
        return []
    themes = []
    for entry in field.split(";"):
        entry = entry.strip()
        if not entry:
            continue
        parts = entry.rsplit(",", 1)
        themes.append(parts[0].strip())
    return themes


def _parse_tone(field: str) -> dict:
    """Parse V2Tone CSV: tone,pos,neg,polarity,ard,srd,wordcount."""
    if not field:
        return {}
    parts = field.split(",")
    keys = ["tone", "positive", "negative", "polarity", "activity_ref_density",
            "self_ref_density", "word_count"]
    try:
        return {k: float(v) for k, v in zip(keys, parts)}
    except (ValueError, TypeError):
        return {}


def _parse_counts(field: str) -> list[dict]:
    """Parse Counts field: TYPE#num#obj#loc;..."""
    if not field:
        return []
    results = []
    for entry in field.split(";"):
        entry = entry.strip()
        if not entry:
            continue
        parts = entry.split("#")
        if len(parts) >= 2:
            try:
                results.append({"type": parts[0], "count": int(parts[1]),
                                 "object": parts[2] if len(parts) > 2 else "",
                                 "location": parts[3] if len(parts) > 3 else ""})
            except (ValueError, IndexError):
                pass
    return results


# ── Connection singletons ────────────────────────────────────────────────────────
# MongoClient is thread-safe and manages its own connection pool internally —
# reusing one instance across all tool calls avoids the per-call handshake overhead.

_MONGO_CLIENT: MongoClient | None = None

def _mongo_coll():
    global _MONGO_CLIENT
    if _MONGO_CLIENT is None:
        _MONGO_CLIENT = MongoClient(MONGO_CONN, serverSelectionTimeoutMS=8000)
    return _MONGO_CLIENT[MONGO_DB][MONGO_COLL]

def _mongo_reset():
    global _MONGO_CLIENT, _GKG_CONTEXT
    _MONGO_CLIENT = None
    _GKG_CONTEXT  = None  # force re-fetch with new connection


_PG_POOL: psycopg2.pool.SimpleConnectionPool | None = None

def _pg_conn():
    global _PG_POOL
    if _PG_POOL is None:
        _PG_POOL = psycopg2.pool.SimpleConnectionPool(1, 4, POSTGRES_CONN, connect_timeout=10)
    return _PG_POOL.getconn()

def _pg_release(conn) -> None:
    if _PG_POOL:
        _PG_POOL.putconn(conn)


# ── Tools ───────────────────────────────────────────────────────────────────────

@tool
def postgres_query(sql: str) -> str:
    """Execute a read-only SQL query against stack_db and return results as JSON.
    Only SELECT statements are allowed."""
    sql_stripped = sql.strip().upper()
    if not sql_stripped.startswith("SELECT"):
        return json.dumps({"error": "Only SELECT queries are allowed."})
    conn = None
    try:
        conn = _pg_conn()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql)
            rows = cur.fetchmany(500)
        return json.dumps({"rows": [dict(r) for r in rows], "count": len(rows)}, default=str)
    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        if conn:
            _pg_release(conn)


@tool
def gkg_summary() -> str:
    """Return a high-level summary of the GKG collection: record count, time range,
    and top 10 news sources. Use this as the first call in any digest workflow."""
    try:
        coll = _mongo_coll()
        total = coll.count_documents({})
        # time range
        pipeline_range = [
            {"$group": {"_id": None,
                        "min_date": {"$min": "$DATE"},
                        "max_date": {"$max": "$DATE"}}}
        ]
        range_res = list(coll.aggregate(pipeline_range))
        date_range = range_res[0] if range_res else {}

        # top sources
        pipeline_src = [
            {"$group": {"_id": "$SourceCommonName", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        sources = [{"source": r["_id"], "articles": r["count"]}
                   for r in coll.aggregate(pipeline_src) if r["_id"]]

        return json.dumps({
            "total_records": total,
            "date_range": {"from": str(date_range.get("min_date", "")),
                           "to": str(date_range.get("max_date", ""))},
            "top_sources": sources
        })
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def gkg_top_themes(n: int = 20) -> str:
    """Return the top N themes from V2Themes across all GKG records (last 3h window)."""
    try:
        coll = _mongo_coll()
        pipeline = [
            {"$match": {"V2Themes": {"$exists": True, "$ne": ""}}},
            {"$project": {"themes_raw": {"$split": ["$V2Themes", ";"]}}},
            {"$unwind": "$themes_raw"},
            {"$match": {"themes_raw": {"$ne": ""}}},
            # strip char offset: "THEME,123" → "THEME"
            {"$project": {"theme": {"$arrayElemAt": [{"$split": ["$themes_raw", ","]}, 0]}}},
            {"$match": {"theme": {"$ne": ""}}},
            {"$group": {"_id": "$theme", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": n}
        ]
        results = [{"theme": r["_id"], "count": r["count"]}
                   for r in coll.aggregate(pipeline)]
        return json.dumps({"top_themes": results})
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def gkg_top_persons(n: int = 20) -> str:
    """Return the top N persons mentioned across all GKG records."""
    try:
        coll = _mongo_coll()
        pipeline = [
            {"$match": {"V2Persons": {"$exists": True, "$ne": ""}}},
            {"$project": {"persons_raw": {"$split": ["$V2Persons", ";"]}}},
            {"$unwind": "$persons_raw"},
            {"$match": {"persons_raw": {"$ne": ""}}},
            {"$project": {"person": {"$arrayElemAt": [{"$split": ["$persons_raw", ","]}, 0]}}},
            {"$match": {"person": {"$ne": ""}}},
            {"$group": {"_id": "$person", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": n}
        ]
        results = [{"person": r["_id"], "count": r["count"]}
                   for r in coll.aggregate(pipeline)]
        return json.dumps({"top_persons": results})
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def gkg_top_organizations(n: int = 20) -> str:
    """Return the top N organizations mentioned across all GKG records."""
    try:
        coll = _mongo_coll()
        pipeline = [
            {"$match": {"V2Organizations": {"$exists": True, "$ne": ""}}},
            {"$project": {"orgs_raw": {"$split": ["$V2Organizations", ";"]}}},
            {"$unwind": "$orgs_raw"},
            {"$match": {"orgs_raw": {"$ne": ""}}},
            {"$project": {"org": {"$arrayElemAt": [{"$split": ["$orgs_raw", ","]}, 0]}}},
            {"$match": {"org": {"$ne": ""}}},
            {"$group": {"_id": "$org", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": n}
        ]
        results = [{"organization": r["_id"], "count": r["count"]}
                   for r in coll.aggregate(pipeline)]
        return json.dumps({"top_organizations": results})
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def gkg_top_locations(n: int = 20) -> str:
    """Return the top N locations mentioned across all GKG records."""
    try:
        coll = _mongo_coll()
        pipeline = [
            {"$match": {"V2Locations": {"$exists": True, "$ne": ""}}},
            {"$project": {"locs_raw": {"$split": ["$V2Locations", ";"]}}},
            {"$unwind": "$locs_raw"},
            {"$match": {"locs_raw": {"$ne": ""}}},
            # V2Locations: "type#fullname#countrycode#adm1#lat#lon#offset"
            {"$project": {"location": {"$arrayElemAt": [{"$split": ["$locs_raw", "#"]}, 1]}}},
            {"$match": {"location": {"$ne": None, "$ne": ""}}},
            {"$group": {"_id": "$location", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": n}
        ]
        results = [{"location": r["_id"], "count": r["count"]}
                   for r in coll.aggregate(pipeline)]
        return json.dumps({"top_locations": results})
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def gkg_tone_analysis() -> str:
    """Return sentiment/tone statistics across all GKG records.
    Includes mean tone, positive/negative scores, polarity, and a
    distribution of articles by tone bucket (very negative / negative /
    neutral / positive / very positive)."""
    try:
        coll = _mongo_coll()
        pipeline = [
            {"$match": {"V2Tone": {"$exists": True, "$ne": ""}}},
            {"$project": {"tone_raw": {"$arrayElemAt": [{"$split": ["$V2Tone", ","]}, 0]},
                          "positive": {"$arrayElemAt": [{"$split": ["$V2Tone", ","]}, 1]},
                          "negative": {"$arrayElemAt": [{"$split": ["$V2Tone", ","]}, 2]}}},
            {"$project": {
                "tone": {"$toDouble": "$tone_raw"},
                "positive": {"$toDouble": "$positive"},
                "negative": {"$toDouble": "$negative"}
            }},
            {"$group": {
                "_id": None,
                "mean_tone": {"$avg": "$tone"},
                "mean_positive": {"$avg": "$positive"},
                "mean_negative": {"$avg": "$negative"},
                "min_tone": {"$min": "$tone"},
                "max_tone": {"$max": "$tone"},
                "very_negative": {"$sum": {"$cond": [{"$lte": ["$tone", -5]}, 1, 0]}},
                "negative": {"$sum": {"$cond": [{"$and": [{"$gt": ["$tone", -5]},
                                                           {"$lte": ["$tone", -1]}]}, 1, 0]}},
                "neutral": {"$sum": {"$cond": [{"$and": [{"$gt": ["$tone", -1]},
                                                          {"$lt": ["$tone", 1]}]}, 1, 0]}},
                "positive_bucket": {"$sum": {"$cond": [{"$and": [{"$gte": ["$tone", 1]},
                                                                   {"$lt": ["$tone", 5]}]}, 1, 0]}},
                "very_positive": {"$sum": {"$cond": [{"$gte": ["$tone", 5]}, 1, 0]}},
                "total": {"$sum": 1}
            }}
        ]
        res = list(coll.aggregate(pipeline))
        if not res:
            return json.dumps({"error": "No tone data found."})
        r = res[0]
        del r["_id"]
        return json.dumps({k: round(v, 3) if isinstance(v, float) else v
                           for k, v in r.items()})
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def gkg_counts_events(top_n: int = 15) -> str:
    """Return quantified event counts from the Counts field (e.g. KILL, ARREST, WOUND).
    Returns the top_n event types by total count, with representative articles."""
    try:
        coll = _mongo_coll()
        docs = coll.find(
            {"Counts": {"$exists": True, "$ne": ""}},
            {"Counts": 1, "SourceCommonName": 1, "DocumentIdentifier": 1}
        ).limit(2000)

        event_totals: Counter = Counter()
        samples: dict[str, list] = {}

        for doc in docs:
            for ev in _parse_counts(doc.get("Counts", "")):
                etype = ev["type"]
                event_totals[etype] += ev["count"]
                if etype not in samples:
                    samples[etype] = []
                if len(samples[etype]) < 3:
                    samples[etype].append({
                        "count": ev["count"],
                        "location": ev["location"],
                        "source": doc.get("SourceCommonName", ""),
                        "url": doc.get("DocumentIdentifier", "")
                    })

        top = [{"event_type": etype, "total_count": cnt,
                "sample_articles": samples.get(etype, [])}
               for etype, cnt in event_totals.most_common(top_n)]
        return json.dumps({"events": top})
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def gkg_search_theme(keyword: str) -> str:
    """Return up to 20 GKG records whose V2Themes contain keyword (case-insensitive).
    Shows source, headline-proxy URL, tone, and matched themes."""
    try:
        coll = _mongo_coll()
        regex = re.compile(keyword, re.IGNORECASE)
        docs = coll.find(
            {"V2Themes": {"$regex": regex}},
            {"SourceCommonName": 1, "DocumentIdentifier": 1,
             "V2Themes": 1, "V2Tone": 1, "DATE": 1}
        ).limit(20)

        results = []
        for doc in docs:
            themes = _parse_v2themes(doc.get("V2Themes", ""))
            matched = [t for t in themes if keyword.lower() in t.lower()]
            tone = _parse_tone(doc.get("V2Tone", ""))
            results.append({
                "date": str(doc.get("DATE", "")),
                "source": doc.get("SourceCommonName", ""),
                "url": doc.get("DocumentIdentifier", ""),
                "tone": round(tone.get("tone", 0), 2) if tone else None,
                "matched_themes": matched[:5]
            })
        return json.dumps({"keyword": keyword, "results": results, "count": len(results)})
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def gkg_quotations(n: int = 10) -> str:
    """Return up to n notable quotations extracted from GKG articles.
    The Quotations field contains structured quotes with speaker and verb."""
    try:
        coll = _mongo_coll()
        docs = coll.find(
            {"Quotations": {"$exists": True, "$ne": ""}},
            {"Quotations": 1, "SourceCommonName": 1, "DocumentIdentifier": 1, "DATE": 1}
        ).limit(n * 3)

        quotes = []
        for doc in docs:
            raw = doc.get("Quotations", "")
            # Quotations: verb#quote#speaker#offset;...
            for entry in raw.split(";"):
                parts = entry.split("#")
                if len(parts) >= 3 and parts[1].strip():
                    quotes.append({
                        "date": str(doc.get("DATE", "")),
                        "source": doc.get("SourceCommonName", ""),
                        "verb": parts[0].strip(),
                        "quote": parts[1].strip()[:300],
                        "speaker": parts[2].strip() if len(parts) > 2 else "",
                        "url": doc.get("DocumentIdentifier", "")
                    })
                if len(quotes) >= n:
                    break
            if len(quotes) >= n:
                break

        return json.dumps({"quotations": quotes[:n]})
    except Exception as e:
        return json.dumps({"error": str(e)})


# NRC EmoLex (c17) dimension labels — 10 primary emotions
_NRC_DIMS: dict[str, str] = {
    "c17.1":  "positive",
    "c17.2":  "negative",
    "c17.3":  "anger",
    "c17.4":  "trust",
    "c17.5":  "anticipation",
    "c17.6":  "disgust",
    "c17.7":  "fear",
    "c17.8":  "joy",
    "c17.9":  "sadness",
    "c17.10": "surprise",
}

# LIWC 2015 (c16) dimensions most useful for news analysis
_LIWC_DIMS: dict[str, str] = {
    "c16.26": "affect",
    "c16.27": "posemo",
    "c16.28": "negemo",
    "c16.29": "anxiety",
    "c16.30": "anger",
    "c16.31": "sadness",
    "c16.16": "social",
    "c16.33": "cogproc",
    "c16.37": "insight",
    "c16.40": "cause",
    "c16.46": "work",
    "c16.47": "achieve",
    "c16.52": "power",
    "c16.56": "risk",
    "c16.57": "focuspast",
    "c16.58": "focuspresent",
    "c16.59": "focusfuture",
}

_GCAM_WANTED = set(_NRC_DIMS) | set(_LIWC_DIMS)


def _parse_gcam(field: str) -> dict[str, int]:
    """Return {dimension_key: count} for dimensions in _GCAM_WANTED only."""
    if not field:
        return {}
    result: dict[str, int] = {}
    for pair in field.split(","):
        pair = pair.strip()
        if ":" not in pair:
            continue
        key, _, val = pair.partition(":")
        if key in _GCAM_WANTED:
            try:
                result[key] = int(val)
            except ValueError:
                pass
    return result


@tool
def gkg_gcam_emotions() -> str:
    """Aggregate NRC EmoLex (c17) and LIWC2015 (c16) emotion/psychological dimensions
    across all GKG records. Returns total raw word-match counts, article coverage
    (how many articles fired each dimension), and per-article averages normalized
    by word count. Use this to understand the dominant emotional register of the
    3-hour news window."""
    try:
        coll = _mongo_coll()
        docs = coll.find(
            {"GCAM": {"$exists": True, "$ne": ""}},
            {"GCAM": 1, "V2Tone": 1}
        )

        totals: dict[str, int] = {k: 0 for k in _GCAM_WANTED}
        coverage: dict[str, int] = {k: 0 for k in _GCAM_WANTED}
        total_words = 0
        doc_count = 0

        for doc in docs:
            gcam = _parse_gcam(doc.get("GCAM", ""))
            if not gcam:
                continue
            doc_count += 1
            # word count is the 7th field in V2Tone
            tone_parts = (doc.get("V2Tone") or "").split(",")
            try:
                wc = int(float(tone_parts[6])) if len(tone_parts) > 6 else 0
            except (ValueError, IndexError):
                wc = 0
            total_words += wc
            for key, cnt in gcam.items():
                totals[key] += cnt
                coverage[key] += 1

        if doc_count == 0:
            return json.dumps({"error": "No GCAM data found."})

        avg_words = total_words / doc_count if doc_count else 1

        def _build_section(dim_map: dict[str, str]) -> list[dict]:
            rows = []
            for key, label in dim_map.items():
                raw = totals[key]
                cov = coverage[key]
                rows.append({
                    "dimension": label,
                    "key": key,
                    "total_word_matches": raw,
                    "articles_with_matches": cov,
                    "pct_articles": round(100 * cov / doc_count, 1),
                    # per-1000-words normalisation for cross-article comparison
                    "per_1k_words": round(1000 * raw / total_words, 2) if total_words else 0,
                })
            return sorted(rows, key=lambda r: r["total_word_matches"], reverse=True)

        return json.dumps({
            "articles_analysed": doc_count,
            "avg_words_per_article": round(avg_words, 0),
            "nrc_emotions": _build_section(_NRC_DIMS),
            "liwc2015_dimensions": _build_section(_LIWC_DIMS),
        })
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def gkg_top_amounts(n: int = 20) -> str:
    """Return the top N numeric amounts mentioned across GKG articles.
    Mines the Amounts field for quantities like troop counts, casualties,
    dollar figures, and protest sizes. Essential for quantified crisis monitoring."""
    try:
        coll = _mongo_coll()
        pipeline = [
            {"$match": {"Amounts": {"$exists": True, "$ne": ""}}},
            {"$project": {"amounts_raw": {"$split": ["$Amounts", ";"]}}},
            {"$unwind": "$amounts_raw"},
            {"$match": {"amounts_raw": {"$ne": ""}}},
            # Amounts format: "value,object,offset" — first field is numeric value
            {"$project": {
                "amount_val": {"$arrayElemAt": [{"$split": ["$amounts_raw", ","]}, 0]},
                "parts": {"$split": ["$amounts_raw", ","]},
            }},
            {"$project": {
                "amount_num": {"$toDouble": "$amount_val"},
                # object is everything between first and last comma — join middle parts
                "parts": 1,
            }},
            {"$match": {"amount_num": {"$gt": 0}}},
            {"$group": {
                "_id": {"$arrayElemAt": ["$parts", 1]},
                "total": {"$sum": "$amount_num"},
                "max_single": {"$max": "$amount_num"},
                "mentions": {"$sum": 1},
            }},
            {"$match": {"_id": {"$ne": None, "$ne": ""}}},
            {"$sort": {"total": -1}},
            {"$limit": n},
        ]
        results = [
            {"object": r["_id"], "total": r["total"],
             "max_single": r["max_single"], "mentions": r["mentions"]}
            for r in coll.aggregate(pipeline)
        ]
        return json.dumps({"top_amounts": results})
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def gkg_all_names(n: int = 30) -> str:
    """Return the top N proper names from the AllNames field across GKG records.
    AllNames captures named events (Arab Spring, Orange Revolution), legislation
    (Iran Nuclear Deal), movements, wars, and proper nouns that V2Persons and
    V2Organizations miss. Use to surface 'what named events are driving the news?'"""
    try:
        coll = _mongo_coll()
        pipeline = [
            {"$match": {"AllNames": {"$exists": True, "$ne": ""}}},
            {"$project": {"names_raw": {"$split": ["$AllNames", ";"]}}},
            {"$unwind": "$names_raw"},
            {"$match": {"names_raw": {"$ne": ""}}},
            # AllNames format: "name,offset" — name is everything before the last comma
            {"$project": {"name": {
                "$reduce": {
                    "input": {"$slice": [{"$split": ["$names_raw", ","]}, 0,
                                         {"$subtract": [{"$size": {"$split": ["$names_raw", ","]}}, 1]}]},
                    "initialValue": "",
                    "in": {"$cond": [{"$eq": ["$$value", ""]}, "$$this",
                                     {"$concat": ["$$value", ",", "$$this"]}]}
                }
            }}},
            {"$match": {"name": {"$ne": ""}}},
            {"$group": {"_id": "$name", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": n},
        ]
        results = [{"name": r["_id"], "count": r["count"]} for r in coll.aggregate(pipeline)]
        return json.dumps({"top_names": results})
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def gkg_search_person(name: str) -> str:
    """Return up to 20 GKG records mentioning the given person (case-insensitive).
    Shows source, URL, date, tone, and co-occurring themes per article.
    Use for 'what is being said about [person X]?' queries."""
    try:
        coll = _mongo_coll()
        regex = re.compile(name, re.IGNORECASE)
        docs = coll.find(
            {"V2Persons": {"$regex": regex}},
            {"SourceCommonName": 1, "DocumentIdentifier": 1,
             "V2Persons": 1, "V2Themes": 1, "V2Tone": 1, "DATE": 1}
        ).limit(20)

        results = []
        for doc in docs:
            persons = _parse_semicolon_names(doc.get("V2Persons", ""))
            matched = [p for p in persons if name.lower() in p.lower()]
            themes = _parse_v2themes(doc.get("V2Themes", ""))[:5]
            tone = _parse_tone(doc.get("V2Tone", ""))
            results.append({
                "date": str(doc.get("DATE", "")),
                "source": doc.get("SourceCommonName", ""),
                "url": doc.get("DocumentIdentifier", ""),
                "tone": round(tone.get("tone", 0), 2) if tone else None,
                "matched_persons": matched[:3],
                "themes": themes,
            })
        return json.dumps({"person": name, "results": results, "count": len(results)})
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def gkg_search_location(name: str) -> str:
    """Return up to 20 GKG records mentioning the given location (case-insensitive).
    Shows source, URL, date, tone, key persons, and themes per article.
    Use full or partial place names, e.g. 'Ukraine', 'Gaza', 'Washington, DC'."""
    try:
        coll = _mongo_coll()
        regex = re.compile(name, re.IGNORECASE)
        docs = coll.find(
            {"V2Locations": {"$regex": regex}},
            {"SourceCommonName": 1, "DocumentIdentifier": 1,
             "V2Locations": 1, "V2Persons": 1, "V2Themes": 1, "V2Tone": 1, "DATE": 1}
        ).limit(20)

        results = []
        for doc in docs:
            # V2Locations: "type#fullname#countrycode#adm1#lat#lon#featureid#offset;..."
            matched_locs = []
            for entry in (doc.get("V2Locations") or "").split(";"):
                parts = entry.split("#")
                if len(parts) >= 2 and name.lower() in parts[1].lower():
                    matched_locs.append(parts[1])
            persons = _parse_semicolon_names(doc.get("V2Persons", ""))[:3]
            themes = _parse_v2themes(doc.get("V2Themes", ""))[:5]
            tone = _parse_tone(doc.get("V2Tone", ""))
            results.append({
                "date": str(doc.get("DATE", "")),
                "source": doc.get("SourceCommonName", ""),
                "url": doc.get("DocumentIdentifier", ""),
                "tone": round(tone.get("tone", 0), 2) if tone else None,
                "matched_locations": list(dict.fromkeys(matched_locs))[:3],
                "persons": persons,
                "themes": themes,
            })
        return json.dumps({"location": name, "results": results, "count": len(results)})
    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def gkg_theme_cooccurrence(theme: str, n: int = 10) -> str:
    """For a given theme keyword, find the top N other themes that co-occur in the
    same articles. Reveals the narrative frame around a topic — searching 'TERROR'
    might surface 'KILL,MILITARY,PROTEST' as dominant co-context. Scans up to 500
    matching articles for performance."""
    try:
        coll = _mongo_coll()
        regex = re.compile(theme, re.IGNORECASE)
        docs = coll.find(
            {"V2Themes": {"$regex": regex}},
            {"V2Themes": 1}
        ).limit(500)

        co_counter: Counter = Counter()
        matched_docs = 0
        for doc in docs:
            all_themes = _parse_v2themes(doc.get("V2Themes", ""))
            others = [t for t in all_themes if theme.lower() not in t.lower()]
            co_counter.update(set(others))
            matched_docs += 1

        top = [{"theme": t, "co_occurrences": c} for t, c in co_counter.most_common(n)]
        return json.dumps({
            "search_theme": theme,
            "articles_scanned": matched_docs,
            "top_cooccurring": top,
        })
    except Exception as e:
        return json.dumps({"error": str(e)})


# ── Tool registry ───────────────────────────────────────────────────────────────
tools = [
    postgres_query,
    gkg_summary,
    gkg_top_themes,
    gkg_top_persons,
    gkg_top_organizations,
    gkg_top_locations,
    gkg_tone_analysis,
    gkg_counts_events,
    gkg_search_theme,
    gkg_quotations,
    gkg_gcam_emotions,
    gkg_top_amounts,
    gkg_all_names,
    gkg_search_person,
    gkg_search_location,
    gkg_theme_cooccurrence,
]
tools_by_name = {t.name: t for t in tools}

model = build_model("analyst")
model_with_tools = model.bind_tools(tools)

# ── Data window context (lazy, cached) ──────────────────────────────────────────
# Fetched once per process from gkg_summary() so the LLM already knows the date
# range, record count, and top sources before the user asks anything — eliminating
# the mandatory first tool call in every session.

_GKG_CONTEXT: str | None = None

def _get_gkg_context() -> str:
    global _GKG_CONTEXT
    if _GKG_CONTEXT is not None:
        return _GKG_CONTEXT
    try:
        raw = json.loads(gkg_summary.invoke({}))
        if "error" in raw:
            print(f"[analyst] _get_gkg_context: gkg_summary returned error: {raw['error']}")
            return ""  # don't cache — retry next call
        dr    = raw.get("date_range", {})
        total = raw.get("total_records", 0)
        date_from = str(dr.get("from", "?"))
        date_to   = str(dr.get("to",   "?"))
        sources   = ", ".join(
            s["source"] for s in raw.get("top_sources", [])[:5] if s.get("source")
        )
        _GKG_CONTEXT = (
            f"**Current GKG data window:** {total:,} records covering {date_from} → {date_to}.\n"
            f"**Top 5 sources:** {sources}.\n"
            "You already have this summary — do NOT call gkg_summary() again unless you need "
            "a fresh count. Use this context to answer date/range questions directly."
        )
        print(f"[analyst] GKG context loaded: {total:,} records, {date_from} → {date_to}")
    except Exception as e:
        print(f"[analyst] _get_gkg_context failed: {e}")
        return ""  # don't cache — retry next call
    return _GKG_CONTEXT

SYSTEM_PROMPT = SystemMessage(content=f"""
You are the Analyst Agent in a multi-agent GDELT analytics system.

## Data sources
- MongoDB  : {MONGO_CONN}  →  {MONGO_DB}.{MONGO_COLL}   (last ~3h of GKG ingestion)
- PostgreSQL: {POSTGRES_CONN}  (stack_db — structured GDELT tables)
- Airflow  : {_AF_URL}
- OpenMetadata: {_OM_URL}

## GKG field reference
GKGRECORDID, DATE, SourceCollectionIdentifier, SourceCommonName, DocumentIdentifier,
Counts, V2Counts, Themes, V2Themes, Locations, V2Locations, Persons, V2Persons,
Organizations, V2Organizations, V2Tone, Dates, GCAM, SharingImage, RelatedImages,
SocialImageEmbeds, SocialVideoEmbeds, Quotations, AllNames, Amounts, TranslationInfo, Extras

V2Tone CSV order: tone, positive_score, negative_score, polarity,
                  activity_ref_density, self_ref_density, word_count

## Standard 3-hour digest workflow
When asked for a digest, news summary, or "what happened", call tools in this order:
1. gkg_summary()              — total records, time window, top sources
2. gkg_top_themes(20)         — dominant storylines
3. gkg_top_persons(15)        — key figures
4. gkg_top_organizations(15)  — key organisations
5. gkg_top_locations(15)      — geographic focus
6. gkg_tone_analysis()        — overall sentiment
7. gkg_counts_events(10)      — quantified violence / crisis events
8. gkg_gcam_emotions()        — NRC emotion profile + LIWC2015 psychological dimensions
9. gkg_quotations(8)          — notable direct quotes (if present)

Then synthesise into a structured digest:
  **3-Hour GDELT News Digest**
  • Headline themes and dominant narratives (with counts)
  • Key actors: persons + organisations
  • Geographic hotspots
  • Sentiment overview (V2Tone score + bucket distribution)
  • Emotion profile: dominant NRC emotions (fear/trust/joy/anger etc.) + LIWC dimensions
  • Quantified events (deaths, arrests, etc.)
  • 3–5 notable quotes
  • Suggested follow-up questions

## GCAM interpretation guide
- NRC per_1k_words > 20 = dominant emotion for that window
- LIWC "power" + "risk" spikes alongside high "negemo" → crisis framing
- High "cogproc" + "insight" → analytical/investigative coverage
- "focusfuture" > "focuspast" → forward-looking / speculative coverage

## General analytical rules
- Lead with concrete findings and numbers; save caveats for the end.
- Cross-reference themes with persons/locations to surface coherent stories.
- Flag anomalies: unusually low/high tone, sudden theme spikes, unfamiliar sources.
## New targeted tools (use instead of full digest when question is specific)
- gkg_search_person(name)       — articles mentioning a specific person + tone + themes
- gkg_search_location(name)     — articles from a specific place + persons + themes
- gkg_search_theme(keyword)     — articles matching a theme keyword
- gkg_theme_cooccurrence(theme) — what other themes appear alongside a given theme
- gkg_all_names(n)              — named events / legislation / movements (AllNames field)
- gkg_top_amounts(n)            — quantified numeric mentions (troops, $, casualties, etc.)

## General analytical rules
- Lead with concrete findings and numbers; save caveats for the end.
- Cross-reference themes with persons/locations to surface coherent stories.
- Flag anomalies: unusually low/high tone, sudden theme spikes, unfamiliar sources.
- For targeted questions (person/theme/event), call only the relevant tool(s) then
  postgres_query() if deeper structured data is needed.
- Only SELECT is allowed in postgres_query().
""")


import time as _time

def run_agent(request: str) -> str:
    import time as _t
    _start = _t.time()
    print(f"[analyst] run_agent START — {request[:80]!r}")
    messages: list[BaseMessage] = [SYSTEM_PROMPT]
    # Inject pre-loaded data window so the agent knows the date range without a tool call
    ctx = _get_gkg_context()
    if ctx:
        messages.append(SystemMessage(content=f"## Current data window\n\n{ctx}"))
    if _POSTGRES_DOCS:
        messages.append(SystemMessage(content=f"## PostgreSQL reference\n\n{_POSTGRES_DOCS}"))
    if _MONGO_DOCS:
        messages.append(SystemMessage(content=f"## MongoDB reference\n\n{_MONGO_DOCS}"))
    messages.append(HumanMessage(content=request))

    call_n = 0
    while True:
        call_n += 1
        print(f"[analyst] LLM call #{call_n} …")
        response = invoke_with_retry(model_with_tools, messages)
        print(f"[analyst] LLM call #{call_n} done in {_t.time()-_start:.1f}s")
        messages.append(response)
        if not response.tool_calls:
            print(f"[analyst] run_agent DONE in {_t.time()-_start:.1f}s ({call_n} LLM calls)")
            LAST_RUN_MESSAGES[:] = serialize_lc_messages(messages)
            return str(response.content)
        # Run all tool calls in parallel — digest fires 9 tools; sequential is wasteful
        _batch_t = _t.time()
        with ThreadPoolExecutor(max_workers=len(response.tool_calls)) as pool:
            futures = {
                pool.submit(tools_by_name[tc["name"]].invoke, tc["args"]): tc
                for tc in response.tool_calls
            }
            results: dict[str, str] = {}
            for future in as_completed(futures):
                tc = futures[future]
                try:
                    results[tc["id"]] = str(future.result())
                except Exception as exc:
                    results[tc["id"]] = json.dumps({"error": str(exc)})
                print(f"[analyst] tool_call: {tc['name']}  result: {results[tc['id']][:80]}")
        print(f"[analyst] tool batch ({len(response.tool_calls)} calls) in {_t.time()-_batch_t:.1f}s")
        # Append ToolMessages in original order so the LLM sees them correctly
        for tc in response.tool_calls:
            messages.append(ToolMessage(content=results[tc["id"]], tool_call_id=tc["id"]))


def run_agent_task(task: str, params: Optional[dict] = None, context: Optional[dict] = None) -> dict:
    params = params or {}
    context = context or {}
    prompt = (
        "You are executing an analyst subtask from the orchestrator.\n"
        f"Task: {task}\n"
        f"Params: {json.dumps(params, ensure_ascii=True)}\n"
        f"Context: {json.dumps(context, ensure_ascii=True)}\n"
        "Deliver concrete analytical findings. Use all available GKG tools to reach the "
        "strongest defensible conclusion. Start with gkg_summary() if this is a digest request."
    )
    result = run_agent(prompt)
    return {"status": "ok", "task": task, "result": result}


try:
    from agents.a2a_kafka_communication import kafka_worker as _kafka_worker, send_to_orchestrator as _send
except ModuleNotFoundError:
    from a2a_kafka_communication import kafka_worker as _kafka_worker, send_to_orchestrator as _send

def kafka_worker() -> None:
    _kafka_worker("analyst", run_agent_task)

def send_to_orchestrator(event_type: str, payload: dict) -> None:
    _send("analyst", event_type, payload)

if __name__ == "__main__":
    kafka_worker()
