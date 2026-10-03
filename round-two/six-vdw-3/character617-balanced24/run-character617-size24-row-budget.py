"""Resumable disjoint64-core producer/literal-checker stages, guards20s."""
import argparse
import collections
import hashlib
import json
import os
import resource
import subprocess
import time
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--last-range", type=int, default=3400)
args = ap.parse_args()
h = Path(__file__).resolve().parent
work = h/"character617-size24-row-budget-checks"
work.mkdir(exist_ok=True)
if (work/"failed.json").exists() or (work/"run.json").exists():
    raise SystemExit("Preserve complete run or first failure; no retry")
env = os.environ.copy()
for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
             "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "BLIS_NUM_THREADS"):
    env[name] = "1"
children = json.loads((work/"execution.json").read_text()) if (work/"execution.json").exists() else []
for name in ("producer", "normal", "optimized"):
    (work/name).mkdir(exist_ok=True)
for start in range(0, 3400, 64):
    if start >= args.last_range:
        break
    stop = min(start+64, 3400)
    for mode in ("producer", "normal", "optimized"):
        dest = work/mode/f"range-{start:04}.json"
        if dest.exists():
            continue
        if any(Path("/scratch/research-team-sol61-six-20260929/state", name).exists()
               for name in ("PAUSED", "PAUSED.json", "HANDOVER.json")):
            raise SystemExit("Operations barrier")
        command = [str(h/"solver-env/bin/python")]
        if mode == "optimized":
            command.append("-O")
        if mode == "producer":
            command += [str(h/"character617-size24-row-budget.py"),
                        "--domain", str(h/"character617-size24-capacity.json"),
                        "--start", str(start), "--stop", str(stop)]
        else:
            command += [str(h/"check-character617-size24-row-budget.py"),
                        "--domain", str(h/"character617-size24-capacity-checks/normal/checked.json"),
                        "--input", str(work/"producer"/f"range-{start:04}.json")]
        command += ["--output", str(dest)]
        begin = time.monotonic()
        record = {"mode": mode, "start": start, "stop": stop,
                  "guard_seconds": 20, "threads": 1, "command": command}
        try:
            p = subprocess.run(command, env=env, capture_output=True, text=True, timeout=20)
            record.update(exit_code=p.returncode, stdout=p.stdout, stderr=p.stderr,
                          status="COMPLETE" if p.returncode == 0 else "INCOMPLETE_NO_EXCLUSION")
        except subprocess.TimeoutExpired:
            record["status"] = "TIMEOUT_INCOMPLETE_NO_EXCLUSION"
        record.update(seconds=time.monotonic()-begin,
                      peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        children.append(record)
        (work/"execution.json").write_text(json.dumps(children, indent=2)+"\n")
        if record["status"] != "COMPLETE":
            (work/"failed.json").write_text(json.dumps(record, indent=2)+"\n")
            raise SystemExit("First incomplete stage frozen; no retry or exclusion")
    if any((work/"producer"/f"range-{start:04}.json").read_bytes()
           != (work/mode/f"range-{start:04}.json").read_bytes()
           for mode in ("normal", "optimized")):
        raise ValueError("Whole mathematical mode transcript differs")
    print(json.dumps({"range": [start, stop], "status": "COMPLETE_THREE_WHOLE_TRANSCRIPTS_EQUAL"}), flush=True)
if args.last_range < 3400:
    raise SystemExit(0)
records = []
cursor = 0
for p in sorted((work/"normal").glob("range-*.json")):
    d = json.loads(p.read_text())
    if d["start"] != cursor or d["status"] != "COMPLETE_PRIVATE_ROW_BUDGET_RANGE":
        raise ValueError("Whole gapless verified partition")
    cursor = d["stop"]
    records.extend(d["records"])
if cursor != 3400:
    raise ValueError("All3400 cores completed")
full = {"schema": "private-character617-size24-row-budget-complete-v1",
        "agent": "six-vdw-3", "role": "researcher", "checked_cores": 3400,
        "records": records,
        "records_sha256": hashlib.sha256(json.dumps(records, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "surviving_cores": sum(r["row_choices"] > 0 for r in records),
        "row_choices": sum(r["row_choices"] for r in records),
        "cohorts": [[c, s, sum(1 for r in records if len(r["C"]) == c and len(r["B0"]) == s),
                     sum(1 for r in records if len(r["C"]) == c and len(r["B0"]) == s and r["row_choices"]),
                     sum(r["row_choices"] for r in records if len(r["C"]) == c and len(r["B0"]) == s)]
                    for c, s in sorted({(len(r["C"]), len(r["B0"])) for r in records})],
        "status": "COMPLETE_PRIVATE_ROW_BUDGET_AUTHOR_CHECKED"}
(work/"checked.json").write_text(json.dumps(full, sort_keys=True)+"\n")
run = {"agent": "six-vdw-3", "role": "researcher", "children": len(children),
       "whole_pairs": 108, "guard_seconds": 20, "threads": 1,
       "seconds": sum(r["seconds"] for r in children),
       "maximum_child_seconds": max(r["seconds"] for r in children),
       "peak_child_rss_kib": max(r["peak_child_rss_kib"] for r in children),
       "status": "COMPLETE_PRIVATE_ROW_BUDGET_AUTHOR_CHECKED"}
(work/"run.json").write_text(json.dumps(run, indent=2)+"\n")
print(json.dumps({k: v for k, v in full.items() if k != "records"}))
print(json.dumps(run))
