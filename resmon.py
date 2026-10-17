#!/usr/bin/env python3
"""
resmon.py - Resource sampler for the Goverflow stack on Raspberry Pi 5.

Samples, at a fixed interval:
  * per-container CPU / memory / net IO / block IO  (docker stats)
  * host load, memory, swap, SoC temperature, throttling flags

Every sample is tagged with the current experiment *phase*, read from a
plain-text marker file. Change the phase by writing to that file:

    echo "load_analyst" > /tmp/goverflow_phase

Usage
-----
    python3 resmon.py --out ./run01 --interval 5
    python3 resmon.py --out ./run01 --interval 5 --duration 900

Stop with Ctrl-C; both CSV files are flushed on every sample, so an
interrupted run is still usable.

No third-party dependencies. Only the docker CLI must be on PATH.
"""

import argparse
import csv
import json
import os
import re
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PHASE_FILE_DEFAULT = "/tmp/goverflow_phase"

# --------------------------------------------------------------------------
# unit parsing
# --------------------------------------------------------------------------

# docker uses binary units for memory (MiB/GiB) and decimal for IO (MB/GB)
_UNITS = {
    "b": 1,
    "kb": 10**3, "mb": 10**6, "gb": 10**9, "tb": 10**12,
    "kib": 2**10, "mib": 2**20, "gib": 2**30, "tib": 2**40,
}
_SIZE_RE = re.compile(r"^\s*([0-9]*\.?[0-9]+)\s*([a-zA-Z]*)\s*$")


def to_mb(token: str) -> float:
    """'1.234GiB' -> MB (decimal megabytes). Returns 0.0 on '--' or garbage."""
    if not token or token.strip() in ("--", "-", "N/A"):
        return 0.0
    m = _SIZE_RE.match(token)
    if not m:
        return 0.0
    value, unit = float(m.group(1)), m.group(2).lower()
    return value * _UNITS.get(unit or "b", 1) / 10**6


def split_pair(token: str):
    """'1.2GiB / 15.6GiB' -> ('1.2GiB', '15.6GiB')"""
    if not token or "/" not in token:
        return token or "", ""
    a, b = token.split("/", 1)
    return a.strip(), b.strip()


def to_pct(token: str) -> float:
    try:
        return float(str(token).replace("%", "").strip())
    except (ValueError, AttributeError):
        return 0.0


# --------------------------------------------------------------------------
# collectors
# --------------------------------------------------------------------------

def docker_stats(timeout=30):
    """One non-streaming snapshot of all running containers."""
    try:
        out = subprocess.run(
            ["docker", "stats", "--no-stream", "--format", "{{json .}}"],
            capture_output=True, text=True, timeout=timeout, check=True,
        ).stdout
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as exc:
        print(f"[warn] docker stats failed: {exc}", file=sys.stderr)
        return []

    rows = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def read_host():
    """Host-level metrics. Raspberry Pi specifics degrade gracefully elsewhere."""
    h = {}

    try:
        l1, l5, l15 = Path("/proc/loadavg").read_text().split()[:3]
        h["load1"], h["load5"], h["load15"] = float(l1), float(l5), float(l15)
    except (OSError, ValueError):
        h["load1"] = h["load5"] = h["load15"] = 0.0

    mem = {}
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            key, _, rest = line.partition(":")
            parts = rest.split()
            if parts:
                mem[key] = float(parts[0]) / 1000.0  # kB -> MB
    except OSError:
        pass

    h["mem_total_mb"] = round(mem.get("MemTotal", 0.0), 1)
    h["mem_available_mb"] = round(mem.get("MemAvailable", 0.0), 1)
    h["mem_used_mb"] = round(h["mem_total_mb"] - h["mem_available_mb"], 1)
    h["swap_total_mb"] = round(mem.get("SwapTotal", 0.0), 1)
    h["swap_used_mb"] = round(mem.get("SwapTotal", 0.0) - mem.get("SwapFree", 0.0), 1)

    # SoC temperature: sysfs first (no extra binary needed)
    h["cpu_temp_c"] = ""
    for zone in sorted(Path("/sys/class/thermal").glob("thermal_zone*")):
        try:
            if "cpu" in (zone / "type").read_text().lower() or zone.name.endswith("zone0"):
                h["cpu_temp_c"] = round(int((zone / "temp").read_text().strip()) / 1000.0, 1)
                break
        except (OSError, ValueError):
            continue

    # Raspberry Pi throttling flags. Bits 0-3 = happening now, 16-19 = has happened.
    h["throttled_hex"], h["throttle_now"], h["throttle_ever"] = "", "", ""
    try:
        out = subprocess.run(["vcgencmd", "get_throttled"],
                             capture_output=True, text=True, timeout=5).stdout.strip()
        m = re.search(r"0x([0-9a-fA-F]+)", out)
        if m:
            bits = int(m.group(1), 16)
            h["throttled_hex"] = f"0x{bits:x}"
            h["throttle_now"] = int(bool(bits & 0xF))
            h["throttle_ever"] = int(bool(bits & 0xF0000))
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        pass

    return h


# --------------------------------------------------------------------------
# main loop
# --------------------------------------------------------------------------

SAMPLE_COLS = [
    "ts_iso", "ts_unix", "phase", "container",
    "cpu_pct", "cpu_pct_norm", "mem_mb", "mem_limit_mb", "mem_pct",
    "net_rx_mb", "net_tx_mb", "blk_read_mb", "blk_write_mb", "pids",
]

HOST_COLS = [
    "ts_iso", "ts_unix", "phase",
    "load1", "load5", "load15",
    "mem_total_mb", "mem_available_mb", "mem_used_mb",
    "swap_total_mb", "swap_used_mb",
    "cpu_temp_c", "throttled_hex", "throttle_now", "throttle_ever",
    "sampler_ms",
]

_stop = False


def _handle_signal(signum, frame):
    global _stop
    _stop = True


def main():
    ap = argparse.ArgumentParser(description="Goverflow resource sampler")
    ap.add_argument("--out", default="./resmon_run", help="output directory")
    ap.add_argument("--interval", type=float, default=5.0, help="seconds between samples")
    ap.add_argument("--duration", type=float, default=0.0, help="stop after N seconds (0 = until Ctrl-C)")
    ap.add_argument("--phase-file", default=PHASE_FILE_DEFAULT)
    ap.add_argument("--phase", default="idle", help="initial phase label")
    args = ap.parse_args()

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    samples_path = outdir / "samples.csv"
    host_path = outdir / "host.csv"

    ncpu = os.cpu_count() or 1
    Path(args.phase_file).write_text(args.phase + "\n")

    # Provenance: written once so the run is self-describing in the thesis appendix.
    meta = {
        "started_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "interval_s": args.interval,
        "ncpu": ncpu,
        "uname": " ".join(os.uname()),
        "phase_file": args.phase_file,
        "note_cpu_pct": "docker stats CPUPerc is relative to ONE core; cpu_pct_norm = cpu_pct / ncpu",
    }
    for cmd, key in (
        (["docker", "--version"], "docker"),
        (["docker", "compose", "version", "--short"], "docker_compose"),
    ):
        try:
            meta[key] = subprocess.run(cmd, capture_output=True, text=True, timeout=10).stdout.strip()
        except (subprocess.SubprocessError, FileNotFoundError):
            meta[key] = "unavailable"
    (outdir / "run_meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False))

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    new_samples = not samples_path.exists()
    new_host = not host_path.exists()

    print(f"[resmon] ncpu={ncpu} interval={args.interval}s -> {outdir}")
    print(f"[resmon] set the phase with:  echo \"<label>\" > {args.phase_file}")

    started = time.time()
    with samples_path.open("a", newline="", encoding="utf-8") as sf, \
         host_path.open("a", newline="", encoding="utf-8") as hf:

        sw = csv.DictWriter(sf, fieldnames=SAMPLE_COLS)
        hw = csv.DictWriter(hf, fieldnames=HOST_COLS)
        if new_samples:
            sw.writeheader()
        if new_host:
            hw.writeheader()

        while not _stop:
            t0 = time.time()
            try:
                phase = Path(args.phase_file).read_text().strip() or "unlabelled"
            except OSError:
                phase = "unlabelled"

            ts = datetime.now(timezone.utc)
            ts_iso = ts.isoformat(timespec="seconds")
            ts_unix = round(ts.timestamp(), 3)

            for row in docker_stats():
                mem_used, mem_limit = split_pair(row.get("MemUsage", ""))
                net_rx, net_tx = split_pair(row.get("NetIO", ""))
                blk_r, blk_w = split_pair(row.get("BlockIO", ""))
                cpu = to_pct(row.get("CPUPerc", "0"))
                sw.writerow({
                    "ts_iso": ts_iso,
                    "ts_unix": ts_unix,
                    "phase": phase,
                    "container": row.get("Name", row.get("Container", "?")),
                    "cpu_pct": round(cpu, 2),
                    "cpu_pct_norm": round(cpu / ncpu, 2),
                    "mem_mb": round(to_mb(mem_used), 1),
                    "mem_limit_mb": round(to_mb(mem_limit), 1),
                    "mem_pct": round(to_pct(row.get("MemPerc", "0")), 2),
                    "net_rx_mb": round(to_mb(net_rx), 3),
                    "net_tx_mb": round(to_mb(net_tx), 3),
                    "blk_read_mb": round(to_mb(blk_r), 3),
                    "blk_write_mb": round(to_mb(blk_w), 3),
                    "pids": row.get("PIDs", ""),
                })

            host = read_host()
            host.update({
                "ts_iso": ts_iso,
                "ts_unix": ts_unix,
                "phase": phase,
                "sampler_ms": round((time.time() - t0) * 1000, 1),
            })
            hw.writerow(host)

            sf.flush()
            hf.flush()

            if args.duration and (time.time() - started) >= args.duration:
                break

            time.sleep(max(0.0, args.interval - (time.time() - t0)))

    print(f"\n[resmon] stopped. {samples_path}  {host_path}")


if __name__ == "__main__":
    main()