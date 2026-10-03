"""One child at a time, each with unchanged twenty-second guard."""
import hashlib
import json
import os
import resource
import subprocess
import time
from pathlib import Path

h = Path(__file__).resolve().parent
run = h / "character617-threshold-four-run"
run.mkdir(exist_ok=True)
checkpoint = run / "checkpoint.json"
env = os.environ.copy()
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "BLIS_NUM_THREADS"):
    env[key] = "1"
if any(run.glob("failure*.json")):
    raise SystemExit("Frozen incomplete batch; no retry")
index = len(list(run.glob("batch-*.json")))
while True:
    if any(Path("/scratch/research-team-sol61-six-20260929/state", key).exists() for key in ("PAUSED", "PAUSED.json", "HANDOVER.json")):
        raise SystemExit("Operations barrier: checkpoint retained")
    before = json.loads(checkpoint.read_text()) if checkpoint.exists() else None
    if before and before["complete"]:
        c = before
        break
    cmd = [str(h / "solver-env/bin/python"), str(h / "character617-threshold-four.py"),
           "--checkpoint", str(checkpoint), "--states-per-step", "1000"]
    record = {"agent": "six-vdw-3", "role": "researcher", "command": cmd, "guard_seconds": 20, "threads": 1,
              "batch": index, "start_processed": before["processed"] if before else 0}
    started = time.monotonic()
    try:
        p = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=20)
        record.update(exit_code=p.returncode, stdout=p.stdout, stderr=p.stderr,
                      status="COMPLETE_BATCH" if p.returncode == 0 else "INCOMPLETE_NO_EXCLUSION")
    except subprocess.TimeoutExpired:
        record["status"] = "TIMEOUT_INCOMPLETE_NO_EXCLUSION"
    record.update(seconds=time.monotonic()-started, peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                  input_sha256=hashlib.sha256(json.dumps(before, sort_keys=True).encode()).hexdigest())
    (run / f"batch-{index:04}.json").write_text(json.dumps(record, sort_keys=True, indent=2) + "\n")
    if record["status"] != "COMPLETE_BATCH":
        (run / f"failure-{index:04}.json").write_text(json.dumps(record, sort_keys=True, indent=2) + "\n")
        raise SystemExit("Preserved incomplete batch; no exclusion")
    c = json.loads(checkpoint.read_text())
    print(json.dumps({"batch": index, "processed": c["processed"], "states": len(c["states"]), "seconds": record["seconds"], "complete": c["complete"]}), flush=True)
    index += 1
print(json.dumps({"status": "COMPLETE_THRESHOLD_FOUR_QUEUE_PRIVATE_UNCHECKED", "batches": index,
                  "processed": c["processed"], "retained": c["retained_transitions"]}), flush=True)
