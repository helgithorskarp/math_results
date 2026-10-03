"""Fresh disjoint independent checks, fixed twenty seconds per child."""
import json
import os
import resource
import subprocess
import time
from pathlib import Path

h = Path(__file__).resolve().parent
output = h / "character617-threshold-four-checks"
output.mkdir(exist_ok=True)
if (output / "failed.json").exists() or (output / "run.json").exists():
    raise SystemExit("Preserve prior complete or failed run")
env = os.environ.copy()
for key in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "BLIS_NUM_THREADS"):
    env[key] = "1"
children = []
begun = time.monotonic()
source = h / "character617-threshold-four.json"
data = json.loads(source.read_text())
for mode in ("normal", "optimized"):
    pieces = output / mode
    pieces.mkdir(exist_ok=True)
    jobs = [("tuples", s, min(s+16, 308)) for s in range(1, 308, 16)]
    jobs += [("states", s, min(s+3000, data["states"])) for s in range(0, data["states"], 3000)]
    jobs += [("merge", 0, 0)]
    for kind, start, stop in jobs:
        if any(Path("/scratch/research-team-sol61-six-20260929/state", k).exists() for k in ("PAUSED", "PAUSED.json", "HANDOVER.json")):
            raise SystemExit("Operations barrier: preserve partial checks")
        dest = pieces / (f"{kind}-{start:05}.json" if kind != "merge" else "checked.json")
        if dest.exists():
            continue
        command = [str(h / "solver-env/bin/python")]
        if mode == "optimized":
            command.append("-O")
        command += [str(h / "check-character617-threshold-four.py"), "--input", str(source), "--output", str(dest),
                    "--mode", kind, "--start", str(start), "--stop", str(stop)]
        if kind == "merge":
            command += ["--pieces", str(pieces)]
        s = time.monotonic()
        record = {"mode": mode, "kind": kind, "start": start, "stop": stop, "command": command, "guard_seconds": 20, "threads": 1}
        try:
            p = subprocess.run(command, env=env, capture_output=True, text=True, timeout=20)
            record.update(exit_code=p.returncode, stdout=p.stdout, stderr=p.stderr,
                          status="COMPLETE" if p.returncode == 0 else "INCOMPLETE_NO_EXCLUSION")
        except subprocess.TimeoutExpired:
            record["status"] = "TIMEOUT_INCOMPLETE_NO_EXCLUSION"
        record.update(seconds=time.monotonic()-s, peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        children.append(record)
        (output / "execution.json").write_text(json.dumps(children, indent=2)+"\n")
        if record["status"] != "COMPLETE":
            (output / "failed.json").write_text(json.dumps(record, indent=2)+"\n")
            raise SystemExit("Incomplete independent check; no retry")
    print(json.dumps({"mode": mode, "complete": True, "record": json.loads((pieces/"checked.json").read_text())}), flush=True)
if (output/"normal/checked.json").read_bytes() != (output/"optimized/checked.json").read_bytes():
    raise ValueError("Whole independent modes differ")
record = {"agent": "six-vdw-3", "role": "researcher", "children": len(children), "whole_pairs": 1,
          "status": "COMPLETE_PRIVATE_THRESHOLD_FOUR_AUTHOR_CHECKED", "seconds": time.monotonic()-begun,
          "maximum_child_seconds": max(r["seconds"] for r in children), "peak_child_rss_kib": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
(output/"run.json").write_text(json.dumps(record, indent=2)+"\n")
print(json.dumps(record))
