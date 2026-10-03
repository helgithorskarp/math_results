"""Optional local campaign gate; external reproduction needs no campaign state."""
from pathlib import Path
from datetime import datetime, timezone
import json
import os


def check_operations():
    location = os.environ.get("DISCOVERY_OPERATIONS_MONITOR")
    if not location:
        return
    monitor = Path(location)
    if any((monitor / name).exists() for name in ("PAUSED", "PAUSED.json", "HANDOVER")):
        raise RuntimeError("operations barrier; no mathematical conclusion")
    handover = monitor / "HANDOVER.json"
    if handover.exists() and json.loads(handover.read_bytes()).get("phase") != "completed":
        raise RuntimeError("incomplete handover; no mathematical conclusion")
    budget = json.loads((monitor / "health.json").read_bytes())["credit_budget"]
    age = (datetime.now(timezone.utc) - datetime.fromisoformat(budget["checked_at"])).total_seconds()
    if budget["status"] != "authorized" or not 0 <= age < 180:
        raise RuntimeError("unauthorized or stale operations health; no mathematical conclusion")
