"""Sequential reproducible audit of the two-red free-involution extension.
Author: six-books-2, role researcher. Python standard library only.
Generated records and logs are private validation data, not proof premises.
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
    expected = json.loads((HERE / "two_red_expected.json").read_text())
    env = dict(os.environ)
    for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                 "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
        env[name] = "1"
    start = time.monotonic()
    measurements = []

    def run(label, arguments):
        before = time.monotonic()
        result = subprocess.run([sys.executable, "-O", str(HERE / (label + ".py")),
                                 *[str(x) for x in arguments]], env=env,
                                capture_output=True, text=True, timeout=120)
        (scratch / (label + ".stdout")).write_text(result.stdout)
        (scratch / (label + ".stderr")).write_text(result.stderr)
        measurements.append({"step": label, "returncode": result.returncode,
                             "wall_seconds": time.monotonic() - before})
        require(result.returncode == 0, label + " failed: " + result.stderr[-2000:])
        return json.loads(result.stdout)

    records = scratch / "two_red_survivors.json"
    fast = run("two_red_census", ["--records", records])
    fast.pop("wall_seconds")
    require(fast == {k: v for k, v in expected.items() if k != "controls"},
            "every fast census diagnostic must agree")
    separate = run("two_red_independent", ["--compare-records", records])
    for key in ("complete", "all_survivor_flag_entries_match", "analytic_forms_match",
                "literal_page_cost_tables", "Boolean_flag_constraint_search"):
        require(separate[key] is True, "separate audit: " + key)
    for key in ("cases", "raw_patterns", "color_survivors", "inside_flag_survivors",
                "full_matching_sign_enumeration"):
        require(separate[key] == expected[key], "separate diagnostic: " + key)
    controls = run("two_red_controls", [])
    controls.pop("wall_seconds")
    require(controls == expected["controls"], "all exact controls must agree")
    summary = {"agent": "six-books-2", "role": "researcher", "complete": True,
               "validation_not_theorem_premise": True,
               "raw_patterns": expected["raw_patterns"],
               "necessary_color_survivors": expected["color_survivors"],
               "inside_flag_survivors": expected["inside_flag_survivors"],
               "all_survivor_flag_entries_match": True, "analytic_forms": 3,
               "vector_controls": controls["vector_controls"],
               "literal_controls": controls["literal_controls"],
               "threads": 1, "full_matching_sign_enumeration": False,
               "wall_seconds": time.monotonic() - start,
               "peak_child_rss_kib_linux": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
               "measurements": measurements}
    (scratch / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
