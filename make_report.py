#!/usr/bin/env python3
"""
make_report.py - Turns resmon.py output into the tables for §6.7.

Reads samples.csv / host.csv / requests.csv from a run directory and emits
Markdown tables with Greek headers, ready to paste into the thesis:

  Πίνακας A  Χρήση πόρων ανά υποσύστημα (αδράνεια έναντι φόρτου)
  Πίνακας B  Επιβάρυνση ανά υποσύστημα (Δ = φόρτος - αδράνεια)
  Πίνακας C  Ανά υπηρεσία, αναλυτικά
  Πίνακας D  Ρυθμαπόδοση δικτύου και δίσκου ανά φάση
  Πίνακας E  Μετρικές κόμβου (φορτίο, μνήμη, swap, θερμοκρασία, throttling)
  Πίνακας F  Καθυστέρηση αιτημάτων ανά φάση και στόχο

Usage
-----
    python3 make_report.py --run ./run01 --idle-phase idle_pre \
        --out ./run01/report_6_7.md --plot

Statistics are median and p95 rather than mean: the distributions are
right-skewed and a single slow sample would otherwise dominate.
Only the standard library is required; matplotlib is optional (--plot).
"""

import argparse
import csv
import json
import statistics as st
from collections import defaultdict
from pathlib import Path

# Substring -> logical subsystem. First match wins, so order matters.
DEFAULT_GROUPS = [
    ("openmetadata-ingestion", "OpenMetadata (ingestion)"),
    ("openmetadata", "OpenMetadata"),
    ("elasticsearch", "Elasticsearch"),
    ("airflow", "Airflow"),
    ("kafka", "Kafka"),
    ("zookeeper", "Kafka"),
    ("postgres", "PostgreSQL"),
    ("mongo", "MongoDB"),
    ("goverflow", "Πράκτορες / FastAPI"),
    ("agent", "Πράκτορες / FastAPI"),
    ("api", "Πράκτορες / FastAPI"),
    ("ui", "Πράκτορες / FastAPI"),
]

GROUP_ORDER = [
    "Πράκτορες / FastAPI", "Kafka", "Airflow", "PostgreSQL",
    "MongoDB", "Elasticsearch", "OpenMetadata", "OpenMetadata (ingestion)", "Λοιπά",
]


def group_of(container, rules):
    name = container.lower()
    for needle, label in rules:
        if needle in name:
            return label
    return "Λοιπά"


def read_csv(path):
    p = Path(path)
    if not p.exists():
        return []
    with p.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def fnum(row, key, default=0.0):
    try:
        return float(row.get(key) or default)
    except (TypeError, ValueError):
        return default


def median(xs):
    return st.median(xs) if xs else 0.0


def p95(xs):
    if not xs:
        return 0.0
    if len(xs) == 1:
        return xs[0]
    s = sorted(xs)
    # nearest-rank, conservative for small n
    idx = min(len(s) - 1, max(0, int(round(0.95 * len(s))) - 1))
    return s[idx]


def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |",
           "| " + " | ".join("---" for _ in headers) + " |"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


def fmt(x, nd=1):
    return f"{x:.{nd}f}".replace(".", ",")  # Greek decimal comma


# --------------------------------------------------------------------------

def build(run_dir, idle_phase, group_rules, top_n):
    samples = read_csv(Path(run_dir) / "samples.csv")
    host = read_csv(Path(run_dir) / "host.csv")
    reqs = read_csv(Path(run_dir) / "requests.csv")

    if not samples:
        raise SystemExit(f"no samples.csv in {run_dir} - did resmon.py run?")

    phases = []
    for r in samples:
        if r["phase"] not in phases:
            phases.append(r["phase"])
    load_phases = [p for p in phases if p != idle_phase and not p.startswith("idle") and p != "done"]

    # ---- accumulate ------------------------------------------------------
    # (phase, group) -> lists ; (phase, container) -> lists
    g_cpu, g_mem = defaultdict(list), defaultdict(list)
    c_cpu, c_mem = defaultdict(list), defaultdict(list)
    # cumulative counters, for throughput: (phase, group) -> {metric: [values]}
    io = defaultdict(lambda: defaultdict(list))
    phase_ts = defaultdict(list)
    containers = {}

    for r in samples:
        ph, cont = r["phase"], r["container"]
        grp = group_of(cont, group_rules)
        containers[cont] = grp
        cpu = fnum(r, "cpu_pct_norm")
        mem = fnum(r, "mem_mb")
        g_cpu[(ph, grp)].append(cpu)
        g_mem[(ph, grp)].append(mem)
        c_cpu[(ph, cont)].append(cpu)
        c_mem[(ph, cont)].append(mem)
        for k in ("net_rx_mb", "net_tx_mb", "blk_read_mb", "blk_write_mb"):
            io[(ph, grp)][k].append(fnum(r, k))
        phase_ts[ph].append(fnum(r, "ts_unix"))

    groups = sorted({g for g in containers.values()},
                    key=lambda g: GROUP_ORDER.index(g) if g in GROUP_ORDER else 99)

    parts = []
    parts.append("<!-- Παραγόμενο από make_report.py. Οι τιμές CPU είναι ποσοστό "
                 "της συνολικής χωρητικότητας του κόμβου (4 πυρήνες = 100%). -->\n")

    # ---- Πίνακας A -------------------------------------------------------
    parts.append("### Πίνακας A — Χρήση πόρων ανά υποσύστημα\n")
    headers = ["Υποσύστημα"]
    for ph in [idle_phase] + load_phases:
        headers += [f"CPU% δ. ({ph})", f"CPU% p95 ({ph})", f"RAM MB δ. ({ph})"]
    rows = []
    for g in groups:
        row = [g]
        for ph in [idle_phase] + load_phases:
            row += [fmt(median(g_cpu[(ph, g)]), 2),
                    fmt(p95(g_cpu[(ph, g)]), 2),
                    fmt(median(g_mem[(ph, g)]), 0)]
        rows.append(row)
    total = ["**Σύνολο**"]
    for ph in [idle_phase] + load_phases:
        total += [fmt(sum(median(g_cpu[(ph, g)]) for g in groups), 2), "—",
                  fmt(sum(median(g_mem[(ph, g)]) for g in groups), 0)]
    rows.append(total)
    parts.append(md_table(headers, rows))
    parts.append("\nδ. = διάμεσος. Το p95 αποτυπώνει τις κορυφές φόρτου.\n")

    # ---- Πίνακας B -------------------------------------------------------
    parts.append("\n### Πίνακας B — Επιβάρυνση ανά υποσύστημα (Δ = φόρτος − αδράνεια)\n")
    rows = []
    for g in groups:
        base_cpu, base_mem = median(g_cpu[(idle_phase, g)]), median(g_mem[(idle_phase, g)])
        row = [g]
        for ph in load_phases:
            row += [fmt(median(g_cpu[(ph, g)]) - base_cpu, 2),
                    fmt(median(g_mem[(ph, g)]) - base_mem, 0)]
        rows.append(row)
    headers = ["Υποσύστημα"] + [h for ph in load_phases for h in (f"ΔCPU% ({ph})", f"ΔRAM MB ({ph})")]
    parts.append(md_table(headers, rows))
    parts.append("\nΘετικό Δ σημαίνει πρόσθετη κατανάλωση υπό φόρτο έναντι της "
                 "αδράνειας. Είναι το μέγεθος που τεκμηριώνει ποιο υποσύστημα "
                 "επιβαρύνεται πραγματικά από την agentic ενορχήστρωση.\n")

    # ---- Πίνακας C -------------------------------------------------------
    parts.append("\n### Πίνακας C — Ανά υπηρεσία (κορυφαίες κατά CPU υπό φόρτο)\n")
    ranked = sorted(
        containers,
        key=lambda c: max((median(c_cpu[(ph, c)]) for ph in load_phases), default=0.0),
        reverse=True,
    )[:top_n]
    headers = ["Container", "Υποσύστημα", f"CPU% δ. ({idle_phase})",
               "CPU% δ. (φόρτος)", "CPU% max", f"RAM MB ({idle_phase})",
               "RAM MB (φόρτος)", "RAM MB max"]
    rows = []
    for c in ranked:
        lcpu = [v for ph in load_phases for v in c_cpu[(ph, c)]]
        lmem = [v for ph in load_phases for v in c_mem[(ph, c)]]
        rows.append([
            c, containers[c],
            fmt(median(c_cpu[(idle_phase, c)]), 2),
            fmt(median(lcpu), 2),
            fmt(max(lcpu) if lcpu else 0.0, 2),
            fmt(median(c_mem[(idle_phase, c)]), 0),
            fmt(median(lmem), 0),
            fmt(max(lmem) if lmem else 0.0, 0),
        ])
    parts.append(md_table(headers, rows))

    # ---- Πίνακας D -------------------------------------------------------
    parts.append("\n### Πίνακας D — Ρυθμαπόδοση δικτύου και δίσκου ανά φάση\n")
    headers = ["Φάση", "Διάρκεια (s)", "Δίκτυο in (MB/s)", "Δίκτυο out (MB/s)",
               "Δίσκος read (MB/s)", "Δίσκος write (MB/s)"]
    rows = []
    for ph in [idle_phase] + load_phases:
        ts = phase_ts.get(ph, [])
        dur = (max(ts) - min(ts)) if len(ts) > 1 else 0.0
        vals = []
        for k in ("net_rx_mb", "net_tx_mb", "blk_read_mb", "blk_write_mb"):
            # counters are cumulative per container since start; sum the per-group spans
            delta = sum(max(io[(ph, g)][k]) - min(io[(ph, g)][k])
                        for g in groups if io[(ph, g)][k])
            vals.append(delta / dur if dur > 0 else 0.0)
        rows.append([ph, fmt(dur, 0)] + [fmt(v, 3) for v in vals])
    parts.append(md_table(headers, rows))
    parts.append("\nΤα NetIO/BlockIO του Docker είναι αθροιστικοί μετρητές από την "
                 "εκκίνηση του container· οι τιμές εδώ είναι διαφορές εντός φάσης "
                 "διαιρεμένες με τη διάρκειά της.\n")

    # ---- Πίνακας E -------------------------------------------------------
    if host:
        parts.append("\n### Πίνακας E — Μετρικές κόμβου\n")
        by_phase = defaultdict(list)
        for r in host:
            by_phase[r["phase"]].append(r)
        headers = ["Φάση", "load1 δ.", "load1 max", "Μνήμη σε χρήση MB (δ.)",
                   "Μνήμη max MB", "Swap MB (max)", "Θερμοκρασία °C (δ./max)",
                   "Throttling"]
        rows = []
        for ph in [idle_phase] + load_phases:
            rs = by_phase.get(ph, [])
            if not rs:
                continue
            l1 = [fnum(r, "load1") for r in rs]
            mu = [fnum(r, "mem_used_mb") for r in rs]
            sw = [fnum(r, "swap_used_mb") for r in rs]
            tp = [fnum(r, "cpu_temp_c") for r in rs if r.get("cpu_temp_c")]
            thr = any(str(r.get("throttle_now", "")) == "1" for r in rs)
            ever = any(str(r.get("throttle_ever", "")) == "1" for r in rs)
            label = "ναι (κατά τη μέτρηση)" if thr else ("είχε συμβεί" if ever else "όχι")
            rows.append([
                ph, fmt(median(l1), 2), fmt(max(l1), 2),
                fmt(median(mu), 0), fmt(max(mu), 0), fmt(max(sw) if sw else 0.0, 0),
                f"{fmt(median(tp), 1)} / {fmt(max(tp), 1)}" if tp else "—",
                label,
            ])
        parts.append(md_table(headers, rows))
        overhead = [fnum(r, "sampler_ms") for r in host]
        if overhead:
            parts.append(f"\nΕπιβάρυνση του ίδιου του δειγματολήπτη: διάμεσος "
                         f"{fmt(median(overhead), 0)} ms ανά δείγμα "
                         f"(μέγιστο {fmt(max(overhead), 0)} ms), σε διάστημα "
                         f"δειγματοληψίας που ορίζεται στο run_meta.json.\n")

    # ---- Πίνακας F -------------------------------------------------------
    if reqs:
        parts.append("\n### Πίνακας F — Καθυστέρηση αιτημάτων\n")
        by = defaultdict(list)
        for r in reqs:
            by[(r["phase"], r["target"])].append(r)
        headers = ["Φάση", "Στόχος", "n", "Επιτυχία", "Διάμεσος (s)",
                   "p95 (s)", "Ελάχ. (s)", "Μέγ. (s)"]
        rows = []
        for (ph, tgt), rs in sorted(by.items()):
            lat = [fnum(r, "latency_s") for r in rs]
            ok = sum(1 for r in rs if str(r.get("http_status")) == "200")
            rows.append([ph, tgt, len(rs), f"{ok}/{len(rs)}",
                         fmt(median(lat), 2), fmt(p95(lat), 2),
                         fmt(min(lat), 2), fmt(max(lat), 2)])
        parts.append(md_table(headers, rows))

    return "\n".join(parts), samples, host, groups, group_rules


def plot(run_dir, samples, host, group_rules, out_png):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("[plot] matplotlib not installed - skipping figure")
        return None

    t0 = min(fnum(r, "ts_unix") for r in samples)
    series = defaultdict(lambda: ([], []))
    for r in samples:
        g = group_of(r["container"], group_rules)
        x, y = series[g]
        x.append((fnum(r, "ts_unix") - t0) / 60.0)
        y.append(fnum(r, "cpu_pct_norm"))
    # samples for the same group at the same timestamp must be summed
    merged = {}
    for g, (xs, ys) in series.items():
        acc = defaultdict(float)
        for x, y in zip(xs, ys):
            acc[round(x, 4)] += y
        pts = sorted(acc.items())
        merged[g] = ([p[0] for p in pts], [p[1] for p in pts])

    fig, axes = plt.subplots(2, 1, figsize=(11, 7), sharex=True)
    for g, (xs, ys) in sorted(merged.items()):
        axes[0].plot(xs, ys, linewidth=1.1, label=g)
    axes[0].set_ylabel("CPU (% του κόμβου)")
    axes[0].legend(fontsize=7, ncol=3)
    axes[0].grid(alpha=0.3)

    if host:
        hx = [(fnum(r, "ts_unix") - t0) / 60.0 for r in host]
        axes[1].plot(hx, [fnum(r, "mem_used_mb") for r in host],
                     linewidth=1.2, label="Μνήμη σε χρήση (MB)")
        temps = [fnum(r, "cpu_temp_c") for r in host]
        if any(temps):
            ax2 = axes[1].twinx()
            ax2.plot(hx, temps, linewidth=1.0, linestyle="--", color="tab:red",
                     label="Θερμοκρασία (°C)")
            ax2.set_ylabel("°C")
        axes[1].set_ylabel("MB")
        axes[1].legend(fontsize=7, loc="upper left")
    axes[1].set_xlabel("Χρόνος (λεπτά από την έναρξη)")
    axes[1].grid(alpha=0.3)

    # phase bands
    bounds, cur, start = [], None, None
    for r in samples:
        ph, t = r["phase"], (fnum(r, "ts_unix") - t0) / 60.0
        if ph != cur:
            if cur is not None:
                bounds.append((cur, start, t))
            cur, start = ph, t
    if cur is not None:
        bounds.append((cur, start, (max(fnum(r, "ts_unix") for r in samples) - t0) / 60.0))
    for ax in axes:
        for i, (ph, a, b) in enumerate(bounds):
            if ph.startswith("idle"):
                ax.axvspan(a, b, alpha=0.07, color="grey")
            ax.axvline(a, color="grey", linewidth=0.5, alpha=0.5)
    for ph, a, b in bounds:
        axes[0].text(a, axes[0].get_ylim()[1] * 0.97, ph, fontsize=6,
                     rotation=90, va="top")

    fig.tight_layout()
    fig.savefig(out_png, dpi=200)
    print(f"[plot] {out_png}")
    return out_png


def main():
    ap = argparse.ArgumentParser(description="Build §6.7 tables from a resmon run")
    ap.add_argument("--run", default="./resmon_run")
    ap.add_argument("--idle-phase", default="idle_pre")
    ap.add_argument("--out", default=None)
    ap.add_argument("--top-n", type=int, default=12)
    ap.add_argument("--groups", default=None,
                    help="JSON file: {\"substring\": \"Label\", ...} overriding the defaults")
    ap.add_argument("--plot", action="store_true")
    args = ap.parse_args()

    rules = DEFAULT_GROUPS
    if args.groups:
        custom = json.loads(Path(args.groups).read_text(encoding="utf-8"))
        rules = list(custom.items()) + DEFAULT_GROUPS

    md, samples, host, _groups, rules = build(args.run, args.idle_phase, rules, args.top_n)
    out = Path(args.out) if args.out else Path(args.run) / "report_6_7.md"
    out.write_text(md, encoding="utf-8")
    print(f"[report] {out}")

    if args.plot:
        plot(args.run, samples, host, rules, Path(args.run) / "resources.png")


if __name__ == "__main__":
    main()