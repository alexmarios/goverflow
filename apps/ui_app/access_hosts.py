# Central host/URL configuration.
#
# Switch ACCESS_MODE to change all service endpoints at once:
#   "local"     — services running on this machine
#   "tailscale" — services running on the Raspberry Pi via Tailscale VPN
#
# To find your Pi's Tailscale IP: run `tailscale ip -4` on the Pi.

ACCESS_MODE = "tailscale"  # <-- change this: "local" | "tailscale"

_HOSTS = {
    "local": {
        "airflow":       "http://127.0.0.1:8080",
        "openmetadata":  "http://localhost:8585",
        "kafka_broker":  "localhost:29092",
        "kafka_ui":      "http://localhost:8081",
        "editor_agent":  "http://localhost:8001",
        "postgres":      "postgresql://stack_user:stack_password@localhost:5432/airflow_db",
        "mongo":         "mongodb://admin:yourpassword@localhost:27017",
        "mongo_db":      "gkd_db",
        "mongo_coll":    "last_24hours_gkd",
        "dags_dir":      "/opt/airflow/dags",
        "remote_user":   "",
        "remote_host":   "",
    },
    "tailscale": {
        "airflow":       "http://100.95.246.75:8080",
        "openmetadata":  "http://100.95.246.75:8585",
        "kafka_broker":  "100.95.246.75:29092",
        "kafka_ui":      "http://100.95.246.75:8081",
        "editor_agent":  "http://100.95.246.75:8001",
        "postgres":      "postgresql://stack_user:stack_password@100.95.246.75:5432/airflow_db",
        "mongo":         "mongodb://admin:yourpassword@100.95.246.75:27017",
        "mongo_db":      "gkd_db",
        "mongo_coll":    "last_24hours_gkd",
        "dags_dir":      "/home/alexpi/goverflow/dags",
        "remote_user":   "alexpi",
        "remote_host":   "100.95.246.75",
    },
}

_cfg = _HOSTS[ACCESS_MODE]

AIRFLOW_URL      = _cfg["airflow"]
OPENMETADATA_URL = _cfg["openmetadata"]
KAFKA_BROKER     = _cfg["kafka_broker"]
KAFKA_UI_URL     = _cfg["kafka_ui"]
EDITOR_AGENT_URL = _cfg["editor_agent"]
POSTGRES_DSN     = _cfg["postgres"]
MONGO_URI        = _cfg["mongo"]
MONGO_DB         = _cfg["mongo_db"]
MONGO_COLL       = _cfg["mongo_coll"]
DAGS_DIR         = _cfg["dags_dir"]
REMOTE_USER      = _cfg["remote_user"]
REMOTE_HOST      = _cfg["remote_host"]

# Keep .env in sync with the active ACCESS_MODE so other tools (Airflow, etc.)
# that read .env directly always point at the same hosts.
import pathlib
from dotenv import set_key

_ENV_FILE = pathlib.Path(__file__).parent / ".env"

_ENV_SYNC = {
    "AIRFLOW_API_URL":    AIRFLOW_URL,
    "OPENMETADATA_HOST":  OPENMETADATA_URL,
    "POSTGRES_DSN":       POSTGRES_DSN,
    "MONGO_URI":          MONGO_URI,
}

for _key, _val in _ENV_SYNC.items():
    set_key(str(_ENV_FILE), _key, _val)


def setup_ssh_key_auth() -> None:
    """Copy your local SSH public key to the remote host so SCP/SSH work without a password."""
    if not REMOTE_USER or not REMOTE_HOST:
        print("[access_hosts] No remote host configured — nothing to do.")
        return
    import subprocess
    import pathlib

    # Pick the best available key; prefer ed25519 over rsa.
    ssh_dir = pathlib.Path.home() / ".ssh"
    key_candidates = ["id_ed25519", "id_rsa", "id_ecdsa"]
    pub_key = next((str(ssh_dir / f"{k}.pub") for k in key_candidates if (ssh_dir / f"{k}.pub").exists()), None)

    target = f"{REMOTE_USER}@{REMOTE_HOST}"
    cmd = ["ssh-copy-id"]
    if pub_key:
        cmd += ["-i", pub_key]
        print(f"[access_hosts] Using key: {pub_key}")
    cmd.append(target)
    print(f"[access_hosts] Running ssh-copy-id {target} ...")
    result = subprocess.run(cmd, text=True)
    if result.returncode == 0:
        print(f"[access_hosts] SSH key auth set up successfully for {target}.")
    else:
        print(f"[access_hosts] ssh-copy-id failed (exit {result.returncode}). "
              "Make sure the remote host is reachable and you know the password for this one-time setup.")


if __name__ == "__main__":
    setup_ssh_key_auth()
