"""Entire checked row domain in fixed <=20000-choice serial batches."""
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
ap.add_argument("--pilot-only", action="store_true")
args = ap.parse_args()
h = Path(__file__).resolve().parent
work = h/"character617-size24-row-completion-checks"
work.mkdir(exist_ok=True)
if (work/"failed.json").exists() or (work/"run.json").exists():
    raise SystemExit("Preserve completed run or first failure")
domain = json.loads((h/"character617-size24-row-budget-checks/checked.json").read_text())
first = [i for i, r in enumerate(domain["records"]) if len(r["B0"]) >= 7]
batches = [first]
batch, number = [], 0
remaining = sorted((i for i in range(3400) if i not in set(first)),
                   key=lambda i: (-len(domain["records"][i]["B0"]), -len(domain["records"][i]["C"]), i))
for i in remaining:
    count = domain["records"][i]["row_choices"]
    if batch and (number+count > 20000 or len(batch) >= 512):
        batches.append(batch)
        batch, number = [], 0
    batch.append(i)
    number += count
if batch:
    batches.append(batch)
flat = [i for b in batches for i in b]
if sorted(flat) != list(range(3400)) or any(sum(domain["records"][i]["row_choices"] for i in b) > 20000 for b in batches):
    raise ValueError("Entire disjoint complete prechosen batching")
(work/"plan.json").write_text(json.dumps({"core_count": 3400, "batches": batches,
                                         "maximum_rows_per_batch": 20000, "guard_seconds": 20}, indent=2)+"\n")
env = os.environ.copy()
for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS",
             "VECLIB_MAXIMUM_THREADS", "BLIS_NUM_THREADS"):
    env[name] = "1"
children = json.loads((work/"execution.json").read_text()) if (work/"execution.json").exists() else []
for name in ("producer", "normal", "optimized"):
    (work/name).mkdir(exist_ok=True)
for ordinal, indices in enumerate(batches):
    if args.pilot_only and ordinal:
        break
    selection = work/f"selection-{ordinal:03}.json"
    if selection.exists() and json.loads(selection.read_text()) != indices:
        raise ValueError("Preserve original selection")
    selection.write_text(json.dumps(indices)+"\n")
    for mode in ("producer", "normal", "optimized"):
        dest = work/mode/f"batch-{ordinal:03}.json"
        if dest.exists():
            continue
        if any(Path("/scratch/research-team-sol61-six-20260929/state", name).exists()
               for name in ("PAUSED", "PAUSED.json", "HANDOVER.json")):
            raise SystemExit("Operations barrier")
        command = [str(h/"solver-env/bin/python")]
        if mode == "optimized":
            command.append("-O")
        script = "character617-size24-row-completion.py" if mode == "producer" else "check-character617-size24-row-completion.py"
        command += [str(h/script), "--domain", str(h/"character617-size24-row-budget-checks/checked.json"),
                    "--selection", str(selection), "--output", str(dest)]
        if mode != "producer":
            command += ["--input", str(work/"producer"/f"batch-{ordinal:03}.json")]
        begin = time.monotonic()
        record = {"mode": mode, "batch": ordinal, "cores": len(indices),
                  "row_choices": sum(domain["records"][i]["row_choices"] for i in indices),
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
            raise SystemExit("First incomplete batch preserved; no identical retry")
    if any((work/"producer"/f"batch-{ordinal:03}.json").read_bytes()
           != (work/mode/f"batch-{ordinal:03}.json").read_bytes() for mode in ("normal", "optimized")):
        raise ValueError("Whole mathematical mode transcripts differ")
    part = json.loads((work/"normal"/f"batch-{ordinal:03}.json").read_text())
    print(json.dumps({"batch": ordinal, "cores": len(indices), "row_choices": part["row_choices"],
                      "remaining": part["remaining_row_choices"], "minimum": min((r["conditional_minimum"] for r in part["records"] if r["conditional_minimum"] is not None), default=None)}), flush=True)
if args.pilot_only:
    raise SystemExit(0)
seen, summaries, residual, histogram = set(), [], [], collections.Counter()
for ordinal in range(len(batches)):
    part = json.loads((work/"normal"/f"batch-{ordinal:03}.json").read_text())
    for r in part["records"]:
        index = r["core_index"]
        if index in seen:
            raise ValueError("Duplicate core between batches")
        seen.add(index)
        summaries.append({k: v for k, v in r.items() if k != "answers"})
        histogram.update(dict(r["missing_histogram"]))
        for row in r["answers"]:
            if row[5] <= 20:
                residual.append({"core_index": index, "A0": r["A0"], "B0": r["B0"], "C": r["C"],
                                 "additional_rows": row[:5], "relaxed_minimum": row[5]})
if sorted(seen) != list(range(3400)) or sum(r["row_choices"] for r in summaries) != domain["row_choices"]:
    raise ValueError("Entire checked core and row coefficient domain")
summaries.sort(key=lambda r: r["core_index"])
residual.sort(key=lambda r: (r["core_index"], r["additional_rows"]))
full = {"schema": "private-character617-size24-row-completion-complete-v1",
        "agent": "six-vdw-3", "role": "researcher", "cores": 3400,
        "row_choices": domain["row_choices"], "records": summaries,
        "records_sha256": hashlib.sha256(json.dumps(summaries, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "remaining_row_choices": len(residual), "residual": residual,
        "residual_sha256": hashlib.sha256(json.dumps(residual, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "global_conditional_minimum": min(histogram), "missing_histogram": sorted(histogram.items()),
        "cohorts": [[c, s, sum(r["row_choices"] for r in summaries if len(r["C"]) == c and len(r["B0"]) == s),
                     sum(r["remaining_row_choices"] for r in summaries if len(r["C"]) == c and len(r["B0"]) == s),
                     min((r["conditional_minimum"] for r in summaries if len(r["C"]) == c and len(r["B0"]) == s and r["conditional_minimum"] is not None), default=None)]
                    for c, s in sorted({(len(r["C"]), len(r["B0"])) for r in summaries})],
        "status": "COMPLETE_PRIVATE_RELAXED_ROW_COMPLETION_AUTHOR_CHECKED"}
(work/"checked.json").write_text(json.dumps(full, sort_keys=True)+"\n")
run = {"agent": "six-vdw-3", "role": "researcher", "children": len(children),
       "whole_pairs": 2*len(batches), "guard_seconds": 20, "threads": 1,
       "seconds": sum(r["seconds"] for r in children),
       "maximum_child_seconds": max(r["seconds"] for r in children),
       "peak_child_rss_kib": max(r["peak_child_rss_kib"] for r in children),
       "status": "COMPLETE_PRIVATE_RELAXED_ROW_COMPLETION_AUTHOR_CHECKED"}
(work/"run.json").write_text(json.dumps(run, indent=2)+"\n")
print(json.dumps({k: v for k, v in full.items() if k not in ("records", "residual", "missing_histogram")}))
print(json.dumps(run))
