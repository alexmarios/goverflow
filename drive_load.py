#!/usr/bin/env python3
"""
drive_load.py - Reproducible load driver for the Goverflow §6.7 experiment.

Runs a scripted sequence of phases against the FastAPI layer while resmon.py
samples in the background. Writes the phase label to the marker file so every
resource sample is attributable to a known condition, and logs per-request
wall time so §6.7 can be correlated with §6.2/§6.3.

Typical run
-----------
    # terminal 1
    python3 resmon.py --out ./run01 --interval 5

    # terminal 2
    python3 drive_load.py --out ./run01 --base-url http://localhost:8010

Phases produced by the default plan:
    idle_pre        stack up, no traffic          (baseline)
    load_analyst    analytical requests
    load_governance governance write requests
    load_mixed      interleaved, concurrent
    idle_post       drain / return to baseline

Only the standard library is used; urllib does the HTTP.
"""

import argparse
import csv
import json
import time
import urllib.error
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

PHASE_FILE_DEFAULT = "/tmp/goverflow_phase"

# Keep these aligned with the prompts used in Tables 4-7 so the chapters agree.
PROMPTS = {
    "analyst": [
        "What are the top 5 GKG themes in the last 24 hours?",
        "What are the most frequently mentioned locations in the GKG dataset today?",
        "What is the average news tone for Germany in the last 24 hours?",
        "Which persons are most mentioned in GKG records today?",
    ],
    "governance": [
        "Show me a catalog snapshot for the stack_db schema in OpenMetadata.",
        "Are there any governance gaps in the raw_data table?",
        "Add a short description to the raw_data table of stack_db.",
        "What is the lineage of the raw_data table?",
    ],
    "ingestion": [
        "Show me the list of failed tasks from the last 24 hours.",
    ],
    "coder": [
        "Read the file dags/gdelt_masterfilelist_sync.py and tell me what it does.",
    ],
}

REQUEST_COLS = [
    "ts_iso", "ts_unix", "phase", "target", "prompt",
    "http_status", "latency_s", "response_chars", "error",
]


def set_phase(phase_file: str, label: str):
    Path(phase_file).write_text(label + "\n")
    print(f"[phase] {label}")


def post_chat(base_url: str, target: str, message: str, timeout: float):
    """POST /api/chat with the ChatRequest schema described in §5.4."""
    payload = json.dumps({
        "message": message,
        "target": target,
        "session_id": f"resmon-{uuid.uuid4().hex[:8]}",
        "history": [],
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return resp.status, round(time.time() - t0, 2), len(body), ""
    except urllib.error.HTTPError as exc:
        return exc.code, round(time.time() - t0, 2), 0, f"HTTPError {exc.reason}"
    except Exception as exc:  # timeout, connection refused, ...
        return 0, round(time.time() - t0, 2), 0, f"{type(exc).__name__}: {exc}"


def run_phase(writer, fh, base_url, phase_file, label, jobs, timeout,
              repeats=1, concurrency=1, settle=0.0):
    """jobs = list of (target, prompt). Repeated `repeats` times."""
    set_phase(phase_file, label)
    if settle:
        time.sleep(settle)

    work = [j for _ in range(repeats) for j in jobs]

    def one(job):
        target, prompt = job
        status, latency, nchars, err = post_chat(base_url, target, prompt, timeout)
        row = {
            "ts_iso": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "ts_unix": round(time.time(), 3),
            "phase": label,
            "target": target,
            "prompt": prompt,
            "http_status": status,
            "latency_s": latency,
            "response_chars": nchars,
            "error": err,
        }
        flag = "ok " if status == 200 else "ERR"
        print(f"  [{flag}] {latency:7.2f}s  {target:<11} {prompt[:58]}")
        return row

    if concurrency > 1:
        with ThreadPoolExecutor(max_workers=concurrency) as pool:
            rows = list(pool.map(one, work))
    else:
        rows = [one(j) for j in work]

    for r in rows:
        writer.writerow(r)
    fh.flush()


def main():
    ap = argparse.ArgumentParser(description="Goverflow load driver")
    ap.add_argument("--out", default="./resmon_run")
    ap.add_argument("--base-url", default="http://localhost:8010")
    ap.add_argument("--phase-file", default=PHASE_FILE_DEFAULT)
    ap.add_argument("--timeout", type=float, default=1200.0, help="per-request timeout (s)")
    ap.add_argument("--idle-seconds", type=float, default=180.0,
                    help="length of the idle baseline phases")
    ap.add_argument("--repeats", type=int, default=3,
                    help="repetitions per prompt (k in the thesis; k>=5 recommended)")
    args = ap.parse_args()

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    req_path = outdir / "requests.csv"
    is_new = not req_path.exists()

    with req_path.open("a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=REQUEST_COLS)
        if is_new:
            w.writeheader()

        print(f"[drive] baseline for {args.idle_seconds:.0f}s")
        set_phase(args.phase_file, "idle_pre")
        time.sleep(args.idle_seconds)

        run_phase(w, fh, args.base_url, args.phase_file, "load_analyst",
                  [("analyst", p) for p in PROMPTS["analyst"]],
                  args.timeout, repeats=args.repeats)

        run_phase(w, fh, args.base_url, args.phase_file, "load_governance",
                  [("governance", p) for p in PROMPTS["governance"]],
                  args.timeout, repeats=args.repeats)

        mixed = ([("orchestrator", p) for p in PROMPTS["analyst"][:2]] +
                 [("orchestrator", p) for p in PROMPTS["governance"][:2]] +
                 [("orchestrator", p) for p in PROMPTS["ingestion"]] +
                 [("orchestrator", p) for p in PROMPTS["coder"]])
        run_phase(w, fh, args.base_url, args.phase_file, "load_mixed",
                  mixed, args.timeout, repeats=args.repeats, concurrency=3)

        print(f"[drive] drain for {args.idle_seconds:.0f}s")
        set_phase(args.phase_file, "idle_post")
        time.sleep(args.idle_seconds)

        set_phase(args.phase_file, "done")

    print(f"[drive] finished -> {req_path}")


if __name__ == "__main__":
    main()