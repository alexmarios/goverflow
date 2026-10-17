#!/usr/bin/env python3
"""
preflight.py — Καταγραφή περιβάλλοντος και απογραφή δεδομένων.

Παράγει τα δεδομένα για δύο πίνακες της ΔΕ που σήμερα λείπουν εντελώς:
  §4.1 Περιβάλλον Εκτέλεσης       (σχόλιο 8 του επιβλέποντα)
  §4.6 Προδιαγραφή Δεδομένων      (σχόλιο 9)

Ελέγχει επίσης τις αναντιστοιχίες που εντοπίστηκαν στο κείμενο:
  - πόσοι πίνακες υπάρχουν όντως στη stack_db (υπάρχει πίνακας γεγονότων;)
  - ποιο είναι το πραγματικό όνομα της βάσης MongoDB (gkg_db ή gkd_db)
  - πόσες ροές Airflow είναι εγγεγραμμένες και ποιες
  - αν το gdelt_gkg_ingest υπάρχει ακόμη
  - ποιος λογαριασμός έγραψε τελευταίος στον κατάλογο OpenMetadata

Χωρίς εξαρτήσεις πέρα από το docker CLI. Τρέξ' το στον κόμβο εκτέλεσης.

Χρήση
-----
    python3 preflight.py                      # όλα
    python3 preflight.py --section env        # μόνο περιβάλλον
    python3 preflight.py --section data       # μόνο δεδομένα
    python3 preflight.py --section dags       # μόνο ροές
    python3 preflight.py --md > preflight.md  # έξοδος σε markdown
"""

import argparse
import json
import re
import subprocess
import sys

# --- ΠΡΟΣΑΡΜΟΣΕ ΕΔΩ αν διαφέρουν τα ονόματα υπηρεσιών/χρηστών ---------------
PG_SVC = "postgres"
PG_USER = "postgres"
PG_DBS = ["stack_db", "airflow_db", "openmetadata_db"]
MONGO_SVC = "mongodb"
AIRFLOW_SVC = "airflow-scheduler"
DAGS_DIR = "dags"

EXPECTED_DAGS = [
    "gdelt_masterfilelist_sync",
    "gdelt_masterfilelist_to_postgres",
    "gdelt_masterfilelist_validate",
    "gkg_daily_sync",
]
# ---------------------------------------------------------------------------

MD = False


def sh(cmd, timeout=60):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True,
                           text=True, timeout=timeout)
        return r.stdout.strip()
    except Exception as e:
        return f"(σφάλμα: {e})"


def head(title):
    print(f"\n{'## ' if MD else ''}{title}")
    if not MD:
        print("=" * len(title))


def kv(k, v):
    v = (v or "(κενό)").strip()
    if MD:
        print(f"| {k} | {v} |")
    else:
        print(f"  {k:<34} {v}")


def table_start(a, b):
    if MD:
        print(f"\n| {a} | {b} |")
        print("|---|---|")


def note(msg):
    print(f"\n{'> ' if MD else '  !! '}{msg}")


# ------------------------------------------------------------------- ενότητες

def section_env():
    head("§4.1 Περιβάλλον Εκτέλεσης")
    table_start("Παράμετρος", "Τιμή")

    model = sh("cat /proc/device-tree/model 2>/dev/null | tr -d '\\0'")
    kv("Μοντέλο συσκευής", model or "(μη Raspberry Pi ή μη διαθέσιμο)")

    lscpu = sh("lscpu")
    def g(pat):
        m = re.search(pat + r":\s*(.+)", lscpu)
        return m.group(1).strip() if m else ""
    kv("Επεξεργαστής", g("Model name") or g("Vendor ID"))
    kv("Αρχιτεκτονική", g("Architecture"))
    kv("Λογικοί πυρήνες", sh("nproc"))
    kv("Μέγιστη συχνότητα", g("CPU max MHz"))

    mem = sh("free -h --si | awk '/^Mem:/{print $2}'")
    kv("Μνήμη RAM", mem)
    swap = sh("free -h --si | awk '/^Swap:/{print $2}'")
    kv("Swap", swap)

    kv("Ρίζα συστήματος αρχείων", sh("df -h / | awk 'NR==2{print $2\" σύνολο, \"$4\" ελεύθερα\"}'"))
    kv("Τύπος αποθηκευτικού μέσου",
       sh("lsblk -dno NAME,SIZE,ROTA,TRAN 2>/dev/null | head -3 | tr '\\n' '; '"))

    kv("Λειτουργικό σύστημα",
       sh("grep PRETTY_NAME /etc/os-release | cut -d'\"' -f2"))
    kv("Πυρήνας", sh("uname -sr"))

    kv("Docker Engine", sh("docker --version"))
    kv("Docker Compose", sh("docker compose version"))
    kv("Ενεργά containers", sh("docker ps -q | wc -l"))

    temp = sh("vcgencmd measure_temp") or sh("cat /sys/class/thermal/thermal_zone0/temp")
    kv("Θερμοκρασία", temp)
    thr = sh("vcgencmd get_throttled")
    kv("Κατάσταση throttling", thr)
    if thr and "0x0" not in thr:
        note("Ο επεξεργαστής έχει υποστεί θερμική υποβάθμιση. Άφησε το σύστημα "
             "να κρυώσει πριν από μετρήσεις καθυστέρησης.")

    if not MD:
        print("\n  Ενεργά containers:")
        for line in sh('docker ps --format "{{.Names}}\t{{.Image}}"').splitlines():
            print(f"    {line}")

    note("Θυμήσου να δηλώσεις στη ΔΕ ότι τα γλωσσικά μοντέλα εκτελούνται "
         "ΑΠΟΜΑΚΡΥΣΜΕΝΑ. Ο περιορισμός πόρων αφορά το επίπεδο δεδομένων και "
         "ενορχήστρωσης, όχι την εξαγωγή συμπερασμάτων.")


def section_dags():
    head("Απογραφή Ροών Airflow")

    raw = sh(f"docker compose exec -T {AIRFLOW_SVC} airflow dags list -o json", 120)
    found = []
    try:
        for d in json.loads(raw):
            found.append(d.get("dag_id", ""))
    except Exception:
        raw2 = sh(f"docker compose exec -T {AIRFLOW_SVC} airflow dags list", 120)
        found = [l.split()[0] for l in raw2.splitlines()[2:]
                 if l.strip() and not l.startswith("=")]

    prod = [d for d in found if not d.startswith(("om_", "OpenMetadata"))]
    print(f"  Σύνολο εγγεγραμμένων ροών: {len(found)}")
    print(f"  Εκτός των ροών μεταδεδομένων του OpenMetadata: {len(prod)}\n")
    for d in sorted(prod):
        mark = "  " if d in EXPECTED_DAGS else "? "
        print(f"    {mark}{d}")

    missing = [d for d in EXPECTED_DAGS if d not in found]
    extra = [d for d in prod if d not in EXPECTED_DAGS]
    if missing:
        note(f"Αναμενόμενες ροές που ΔΕΝ βρέθηκαν: {', '.join(missing)}")
    if extra:
        note(f"Ροές εκτός της αναμενόμενης λίστας: {', '.join(extra)}. "
             f"Αν κάποια από αυτές φορτώνει δεδομένα, η §4.5 πρέπει να την "
             f"περιλάβει.")

    if "gdelt_gkg_ingest" in found:
        note("Το gdelt_gkg_ingest είναι ΑΚΟΜΗ εγγεγραμμένο. Είναι διπλότυπο του "
             "gkg_daily_sync και πρέπει να αφαιρεθεί πριν από τα πειράματα "
             "(δες Ε3): γράφει στην ίδια συλλογή και μπορεί να παραπλανήσει "
             "τον Coder ως προς το ποιο αρχείο να διορθώσει.")

    print("\n  Χρονοπρογραμματισμός και κατάσταση παύσης:")
    for d in EXPECTED_DAGS:
        det = sh(f"docker compose exec -T {AIRFLOW_SVC} "
                 f"airflow dags details {d} -o json", 60)
        sched = paused = "?"
        try:
            j = json.loads(det)
            j = j[0] if isinstance(j, list) else j
            sched = str(j.get("timetable_summary") or j.get("schedule_interval") or "?")
            paused = str(j.get("is_paused", "?"))
        except Exception:
            pass
        print(f"    {d:<38} schedule={sched:<22} paused={paused}")

    note("Πριν από κάθε πείραμα, ΟΛΕΣ οι ροές πρέπει να είναι σε παύση. Το "
         "gdelt_masterfilelist_sync τρέχει ανά 15′ και πυροδοτεί μέσω Dataset "
         "το gdelt_masterfilelist_to_postgres — αν μείνει ενεργό, μολύνει κάθε "
         "μέτρηση πόρων και καθυστέρησης.")

    print("\n  Έλεγχος watermark (σχόλιο Ε5):")
    for f in ["gdelt_masterfilelist_to_postgres.py", "gkg_daily_sync.py"]:
        hits = sh(f"grep -c 'watermark\\|last_processed\\|checkpoint' "
                  f"{DAGS_DIR}/{f} 2>/dev/null")
        print(f"    {f:<40} αναφορές watermark: {hits or 0}")

    print("\n  Έλεγχος του validate DAG (σχόλιο Ε4):")
    v = sh(f"grep -n 'catalog_manifest\\|quality\\|expectation\\|assert\\|check' "
           f"{DAGS_DIR}/gdelt_masterfilelist_validate.py 2>/dev/null | head -12")
    print(v or "    (δεν βρέθηκαν σχετικές αναφορές — άνοιξε το αρχείο χειροκίνητα)")
    if "catalog_manifest" in v:
        note("Το validate ανανεώνει το catalog_manifest.json. Η §4.5 απλώς το "
             "παρέλειπε· η §4.9 είναι σωστή.")
    elif any(w in v for w in ("quality", "expectation", "assert")):
        note("Το validate εκτελεί ελέγχους ποιότητας. ΑΝΗΚΕΙ ΣΤΟ ΣΚΕΛΟΣ B0 του "
             "ΕΕ2 — η συνεισφορά του Governance πρέπει να μετρηθεί πάνω από "
             "αυτόν, όχι πάνω από το μηδέν.")


def section_data():
    head("§4.6 Προδιαγραφή Συνόλου Δεδομένων")

    print("\n  PostgreSQL — πίνακες ανά βάση:")
    for db in PG_DBS:
        out = sh(f'docker compose exec -T {PG_SVC} psql -U {PG_USER} -d {db} -t -A -F"|" '
                 f'-c "SELECT schemaname, relname, n_live_tup '
                 f'FROM pg_stat_user_tables ORDER BY n_live_tup DESC;"', 60)
        rows = [l for l in out.splitlines() if "|" in l]
        print(f"\n    {db}  ({len(rows)} πίνακες)")
        for l in rows[:25]:
            p = l.split("|")
            print(f"      {p[0]}.{p[1]:<32} {p[2]:>12} εγγραφές")

        if db == "stack_db":
            names = [l.split("|")[1].lower() for l in rows]
            has_events = any("event" in n for n in names)
            has_mentions = any("mention" in n for n in names)
            if not has_events:
                note("ΔΕΝ βρέθηκε πίνακας γεγονότων στη stack_db. Το §6.3 όμως "
                     "εκτελεί ερωτήματα τύπου «How many events were recorded in "
                     "Greece». Δες Ε7: είτε λείπει ροή από τη λίστα, είτε το §6.3 "
                     "πρέπει να ξαναγραφεί ώστε να αντιστοιχεί στα δεδομένα που "
                     "όντως υπάρχουν.")
            if not has_mentions:
                note("ΔΕΝ βρέθηκε πίνακας mentions, αν και αναφέρεται στον πίνακα "
                     "δρομολόγησης του §6.2. Διόρθωσε τα ερωτήματα του ΕΕ0.")

    print("\n  PostgreSQL — μεγέθη:")
    out = sh(f'docker compose exec -T {PG_SVC} psql -U {PG_USER} -d postgres -t -A -F"|" '
             f'-c "SELECT datname, pg_size_pretty(pg_database_size(datname)) '
             f'FROM pg_database WHERE datistemplate = false;"', 60)
    for l in out.splitlines():
        if "|" in l:
            a, b = l.split("|")[:2]
            print(f"    {a:<28} {b}")

    print("\n  MongoDB — βάσεις και συλλογές:")
    dbs = sh(f"""docker compose exec -T {MONGO_SVC} mongosh --quiet --eval '
        db.adminCommand({{listDatabases:1}}).databases.forEach(function(d){{
          if (["admin","config","local"].indexOf(d.name) === -1) {{
            print(d.name + " | " + (d.sizeOnDisk/1048576).toFixed(1) + " MB");
          }}
        }});' """, 60)
    print(f"    {dbs or '(καμία)'}")

    for name in ("gkg_db", "gkd_db"):
        cols = sh(f"""docker compose exec -T {MONGO_SVC} mongosh {name} --quiet --eval '
            db.getCollectionNames().forEach(function(c){{
              print("  " + c + " | " + db[c].countDocuments() + " έγγραφα");
            }});' """, 90)
        if cols and "έγγραφα" in cols:
            print(f"\n    {name}:")
            print(cols)

    if "gkd_db" in dbs and "gkg_db" not in dbs:
        note("Η βάση MongoDB ονομάζεται gkd_db, αλλά το κείμενο της ΔΕ γράφει "
             "gkg_db σε τρία σημεία (§5.2.2 ×2, §5.6.4). Δες Ε2 — αποφάσισε "
             "ΤΩΡΑ, γιατί το όνομα μπαίνει στα FQN του OpenMetadata και άρα "
             "στο gold.json και σε κάθε στιγμιότυπο του ΕΕ2.")
    elif "gkg_db" in dbs and "gkd_db" in dbs:
        note("Υπάρχουν ΚΑΙ ΟΙ ΔΥΟ βάσεις (gkg_db και gkd_db). Η μετονομασία "
             "έγινε μερικώς. Επαλήθευσε ποια χρησιμοποιείται και διάγραψε την "
             "άλλη πριν από τα πειράματα.")

    print("\n  Χρήση δίσκου ανά volume:")
    print(sh("docker system df -v 2>/dev/null | sed -n '/VOLUME NAME/,/^$/p' | head -20"))


def section_catalog():
    head("Έλεγχος Καταλόγου OpenMetadata")

    import os
    url = os.environ.get("OM_URL", "http://localhost:8585")
    token = os.environ.get("OM_TOKEN", "")
    if not token:
        note("Δεν ορίστηκε OM_TOKEN — παραλείπεται. "
             'export OM_TOKEN="<bearer>" και ξανατρέξε.')
        return

    auth = f'-H "Authorization: Bearer {token}"'
    out = sh(f'curl -s {auth} "{url}/api/v1/tables?limit=100&fields=owners,tags"', 90)
    try:
        data = json.loads(out)
    except Exception:
        note("Η κλήση στο OpenMetadata απέτυχε. Έλεγξε URL και token.")
        return

    tables = data.get("data", [])
    print(f"  Καταγεγραμμένοι πίνακες: {len(tables)}")
    by_db = {}
    for t in tables:
        fqn = t.get("fullyQualifiedName", "")
        parts = fqn.split(".")
        db = parts[1] if len(parts) > 1 else "?"
        by_db[db] = by_db.get(db, 0) + 1
    for db, n in sorted(by_db.items(), key=lambda x: -x[1]):
        print(f"    {db:<28} {n}")

    if by_db.get("airflow_db", 0) > by_db.get("stack_db", 0):
        note(f"Ο κατάλογος περιέχει {by_db.get('airflow_db')} πίνακες της "
             f"airflow_db έναντι {by_db.get('stack_db', 0)} της stack_db. Δες Ε9: "
             f"οι πίνακες της airflow_db είναι εσωτερικά μεταδεδομένα της "
             f"πλατφόρμας και ΔΕΝ αποτελούν αντικείμενο διακυβέρνησης. "
             f"Μη τους μετράς ως εξοικονομημένη ανθρώπινη εργασία.")

    bots = sh(f'curl -s {auth} "{url}/api/v1/bots?limit=50"', 60)
    if "goverflow" in bots.lower():
        print("\n  Βρέθηκε αποκλειστικός λογαριασμός για τον πράκτορα.")
    else:
        note("ΔΕΝ βρέθηκε αποκλειστικό bot για τον Governance. Δες Ε8: χωρίς "
             "αυτό, το πεδίο changedBy δείχνει ingestion-bot και δεν ξεχωρίζει "
             "τις εγγραφές του πράκτορα από εκείνες των connectors — που είναι "
             "ακριβώς η σύγκριση B0/B1 του ΕΕ2.")


def main():
    global MD
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--section", choices=["env", "dags", "data", "catalog", "all"],
                    default="all")
    ap.add_argument("--md", action="store_true",
                    help="Έξοδος σε markdown για αντιγραφή στη ΔΕ")
    a = ap.parse_args()
    MD = a.md

    if not sh("docker ps -q"):
        print("ΣΦΑΛΜΑ: το docker δεν αποκρίνεται.", file=sys.stderr)
        sys.exit(1)

    if a.section in ("env", "all"):
        section_env()
    if a.section in ("dags", "all"):
        section_dags()
    if a.section in ("data", "all"):
        section_data()
    if a.section in ("catalog", "all"):
        section_catalog()

    print("\n" + ("---" if MD else "=" * 60))
    print("Συμπλήρωσε τα κενά των πινάκων §4.1 και §4.6 με τα παραπάνω, "
          "και λύσε κάθε προειδοποίηση πριν ξεκινήσεις τα πειράματα.")


if __name__ == "__main__":
    main()