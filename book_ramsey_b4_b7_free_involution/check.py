"""Sequential exact validation of the free-involution analytic lemma.
Author: six-books-2, role researcher. No external mathematical inputs.
Generated files go only to the explicitly supplied scratch directory.
"""
import argparse
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scratch", type=Path, required=True)
    args = parser.parse_args()
    scratch = args.scratch.resolve()
    require(scratch != HERE and HERE not in scratch.parents,
            "scratch must be outside the contribution directory")
    scratch.mkdir(parents=True, exist_ok=True)
    expected = json.loads((HERE / "expected.json").read_text())
    env = dict(os.environ)
    for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                 "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
        env[name] = "1"
    start = time.monotonic()
    measurements = []

    def run(label, command):
        before = time.monotonic()
        result = subprocess.run([str(x) for x in command], env=env,
                                capture_output=True, text=True, timeout=120)
        (scratch / (label + ".stdout")).write_text(result.stdout)
        (scratch / (label + ".stderr")).write_text(result.stderr)
        measurements.append({"step": label, "returncode": result.returncode,
                             "wall_seconds": time.monotonic() - before})
        require(result.returncode == 0, label + " failed: " + result.stderr[-2000:])
        return result.stdout

    for name in ("census", "formula_controls"):
        run("build_" + name, ["g++", "-std=c++17", "-O2", "-Wall", "-Wextra",
                              "-Wpedantic", HERE / (name + ".cpp"),
                              "-o", scratch / name])
    census = [json.loads(line) for line in
              run("census", [scratch / "census", "6", scratch / "survivors.jsonl"]).splitlines()]
    require(census == expected["census_cases"], "all census case fields differ")
    formula = json.loads(run("formula_controls", [scratch / "formula_controls"]))
    require(formula == expected["formula_controls"], "formula controls differ")
    matrix = json.loads(run("matrix_controls", [sys.executable, "-O", HERE / "matrix_controls.py"]))
    matrix.pop("wall_seconds")
    require(matrix == expected["matrix_controls"], "matrix controls differ")
    separate_lines = run("independent_census", [sys.executable, "-O", HERE / "independent_census.py",
                                               "--reference", scratch / "survivors.jsonl"]).splitlines()
    separate = json.loads(separate_lines[-1])
    require(separate["complete"] and separate["full_survivor_flag_sets_match"],
            "independent entrywise census did not complete")
    require(separate["analytic_shapes"] == expected["analytic_shapes"], "analytic shape count")
    require(not separate["full_signing_enumeration"], "scope mismatch")
    for key, value in expected["census_totals"].items():
        require(separate[key] == value, "independent census total: " + key)
    summary = {"agent": "six-books-2", "role": "researcher", "complete": True,
               "validation_not_theorem_premise": True,
               "census_totals": expected["census_totals"],
               "all_survivor_flag_entries_match": True,
               "analytic_shapes": 2, "threads": 1,
               "wall_seconds": time.monotonic() - start,
               "peak_child_rss_kib_linux": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
               "measurements": measurements, "full_order22_enumeration": False}
    (scratch / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
