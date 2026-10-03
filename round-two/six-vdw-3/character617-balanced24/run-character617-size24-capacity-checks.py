"""Disjoint1024-prefix full-column-product checks; unchanged checker/guards."""
import collections
import hashlib
import json
import os
import resource
import subprocess
import time
from pathlib import Path

h = Path(__file__).resolve().parent
work = h / "character617-size24-capacity-checks"
work.mkdir(exist_ok=True)
if (work/"failed.json").exists() or (work/"run.json").exists():
    raise SystemExit("Preserve existing failure or complete run")
env = os.environ.copy()
for name in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS","BLIS_NUM_THREADS"):
    env[name] = "1"
started = time.monotonic()
children = []
for mode in ("normal","optimized"):
    d = work / mode
    d.mkdir(exist_ok=True)
    for start in range(0,76735,1024):
        stop = min(start+1024,76735)
        dest = d/f"range-{start:05}.json"
        if dest.exists():
            continue
        if any(Path("/scratch/research-team-sol61-six-20260929/state",k).exists() for k in ("PAUSED","PAUSED.json","HANDOVER.json")):
            raise SystemExit("Operations barrier")
        command = [str(h/"solver-env/bin/python")]
        if mode == "optimized":command.append("-O")
        command += [str(h/"check-character617-size24-capacity.py"),"--input",str(h/"character617-size24-capacity.json"),
                    "--domain",str(h/"character617-threshold-four.json"),"--output",str(dest),"--start",str(start),"--stop",str(stop)]
        s = time.monotonic()
        record = {"mode":mode,"start":start,"stop":stop,"guard_seconds":20,"threads":1,"command":command}
        try:
            p = subprocess.run(command,env=env,capture_output=True,text=True,timeout=20)
            record.update(exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr,status="COMPLETE" if p.returncode==0 else "INCOMPLETE_NO_EXCLUSION")
        except subprocess.TimeoutExpired:record["status"]="TIMEOUT_INCOMPLETE_NO_EXCLUSION"
        record.update(seconds=time.monotonic()-s,peak_child_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss)
        children.append(record)
        (work/"execution.json").write_text(json.dumps(children,indent=2)+"\n")
        if record["status"] != "COMPLETE":
            (work/"failed.json").write_text(json.dumps(record,indent=2)+"\n")
            raise SystemExit("Incomplete range preserved; no retry")
    records, hist = [], collections.Counter()
    fields = ("remaining_five_sets","remaining_labeled_cores","labeled_fourteen_column_packs")
    totals = dict.fromkeys(fields,0)
    cursor = 0
    for path in sorted(d.glob('range-*.json')):
        part = json.loads(path.read_text())
        if part["start"] != cursor or part["status"] != "COMPLETE_PRIVATE_ROW_CAPACITY_RANGE_CHECKED":raise ValueError("Whole exact partition")
        cursor = part["stop"]
        if hashlib.sha256(json.dumps(part["records"],sort_keys=True,separators=(",",":")).encode()).hexdigest() != part["records_sha256"]:raise ValueError("Whole transcript hash")
        records.extend(part["records"])
        hist.update({(c,b,s):n for c,b,s,n in part["histogram"]})
        for key in fields:totals[key] += part[key]
    if cursor != 76735:raise ValueError("All five-sets covered")
    full = {"agent":"six-vdw-3","role":"researcher","checked_five_sets":cursor,**totals,
            "records":records,"histogram":[[c,b,s,n] for (c,b,s),n in sorted(hist.items())],
            "status":"COMPLETE_PRIVATE_ROW_CAPACITY_AUTHOR_CHECKED"}
    producer = json.loads((h/"character617-size24-capacity.json").read_text())
    if full["histogram"] != producer["histogram"] or totals["remaining_five_sets"] != producer["remaining_five_sets"] or totals["remaining_labeled_cores"] != producer["remaining_labeled_cores"]:raise ValueError("Whole producer totals")
    (d/"checked.json").write_text(json.dumps(full,sort_keys=True)+"\n")
    print(json.dumps({k:v for k,v in full.items() if k not in ("records","histogram")}),flush=True)
if (work/"normal/checked.json").read_bytes() != (work/"optimized/checked.json").read_bytes():raise ValueError("Whole mode transcript mismatch")
record = {"agent":"six-vdw-3","role":"researcher","children":len(children),"whole_pairs":1,"guard_seconds":20,"threads":1,
          "seconds":time.monotonic()-started,"maximum_child_seconds":max(r["seconds"] for r in children),
          "peak_child_rss_kib":resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
          "status":"COMPLETE_PRIVATE_ROW_CAPACITY_AUTHOR_CHECKED"}
(work/"run.json").write_text(json.dumps(record,indent=2)+"\n")
print(json.dumps(record))
