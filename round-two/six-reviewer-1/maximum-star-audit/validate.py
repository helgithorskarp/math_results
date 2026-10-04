"""Serial bounded normal/optimized/cold positives and semantic adverse controls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import sys
import tempfile
import time


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--receipt")
    args = p.parse_args()
    root = Path(__file__).resolve().parent
    expected = json.loads((root/"EXPECTED.json").read_text())
    env = {**os.environ, **{n: "1" for n in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "BLIS_NUM_THREADS"]}}
    env.pop("PYTHONPATH", None)
    results = []
    damages = {"coordinates.py": ["smaller_star", "omit_complements", "empty_metric", "naive_cap", "raw_saturation", "simple_unit_boundary"],
               "frobenius.py": ["drop_empty_square", "wrong_star_sign", "unordered_half", "floor_sqrt", "underpay_radius", "omit_coverage"]}
    with tempfile.TemporaryDirectory(prefix="maximum-star-review-") as tmp:
        cold = Path(tmp)/"source"
        cold.mkdir()
        for name in ["arithmetic.py", "coordinates.py", "frobenius.py", "EXPECTED.json"]:
            shutil.copyfile(root/name, cold/name)
        for location, directory in [("local", root), ("cold-source-only", cold)]:
            for program in ["coordinates.py", "frobenius.py"]:
                records = []
                for optimized in [False, True]:
                    record = Path(tmp)/(location+"-"+program+("-O" if optimized else "")+".json")
                    command = [sys.executable, "-B"]+(["-O"] if optimized else [])+[str(directory/program), "--record", str(record)]
                    start = time.monotonic()
                    run = subprocess.run(command, cwd=directory, env=env, capture_output=True, text=True, timeout=45)
                    if run.returncode:
                        raise ValueError("positive failure "+program+" "+run.stderr)
                    summary = json.loads(run.stdout)
                    data = record.read_bytes()
                    if summary != expected[program] or len(data) != summary["record_bytes"] or hashlib.sha256(data).hexdigest() != summary["record_sha256"]:
                        raise ValueError("entire record/summary mismatch "+program)
                    records.append(data)
                    results.append({"program": program, "location": location, "optimized": optimized,
                                    "kind": "positive", "seconds": round(time.monotonic()-start, 6),
                                    "record_bytes": len(data), "record_sha256": hashlib.sha256(data).hexdigest()})
                if records[0] != records[1]:
                    raise ValueError("whole normal/optimized records differ")
        for program, cases in damages.items():
            for case in cases:
                for optimized in [False, True]:
                    command = [sys.executable, "-B"]+(["-O"] if optimized else [])+[str(root/program), "--damage", case]
                    start = time.monotonic()
                    run = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True, timeout=45)
                    if not run.returncode or "ValueError:" not in run.stderr or "AssertionError" in run.stderr:
                        raise ValueError("semantic damage did not explicitly reject "+program+" "+case)
                    results.append({"program": program, "optimized": optimized, "kind": "semantic-rejection",
                                    "damage": case, "seconds": round(time.monotonic()-start, 6),
                                    "final_error": run.stderr.splitlines()[-1]})
    receipt = {"agent": "six-reviewer-1", "role": "independent mathematical reviewer",
               "python_version": sys.version.split()[0], "standard_library_only": True,
               "serial_child_count": 1, "native_threads": 1, "fixed_child_timeout_seconds": 45,
               "positive_children": sum(r["kind"] == "positive" for r in results),
               "semantic_rejections": sum(r["kind"] == "semantic-rejection" for r in results),
               "total_child_seconds": round(sum(r["seconds"] for r in results), 6),
               "max_child_seconds": max(r["seconds"] for r in results),
               "cumulative_child_peak_RSS_KiB": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
               "children": results, "records": {n: {k: v for k, v in s.items() if k in ["record_bytes", "record_sha256"]} for n, s in expected.items()}}
    if args.receipt:
        Path(args.receipt).write_text(json.dumps(receipt, indent=2)+"\n")
    print(json.dumps({k: v for k, v in receipt.items() if k not in ["children", "records"]}, sort_keys=True))


if __name__ == "__main__":
    main()
