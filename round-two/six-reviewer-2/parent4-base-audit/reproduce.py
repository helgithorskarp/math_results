"""Rebuild the ENTIRE independent record; serial fixed-guard stages."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from grid import need

ROOT = Path(__file__).resolve().parent


def assemble(controls, stages):
    need(len(stages) == 4 and stages[-1]["retained"] == [],
         "all screens complete and final frontier empty")
    need(all(s["complete"] and s["threshold"] == 1117 for s in stages),
         "stronger threshold throughout, not just at the terminal screen")
    return {"agent": "six-reviewer-2", "role": "independent mathematical reviewer",
            "scope": "literal P, at most one class per every unused original divisor2520>=8; outside parent4",
            "controls": controls, "threshold": 1117, "stages": stages,
            "stronger_hole_minimum": 2, "minimum_claimed_sharp": False,
            "two_tail_capacity": {"per_hole": "2 r16 + r32 >= 4",
                                  "minimum_productive_classes": 2}}


def run(scratch, optimized=False):
    scratch = Path(scratch).resolve()
    need(scratch != ROOT and ROOT not in scratch.parents,
         "generated outputs belong outside the public source directory")
    scratch.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
                 "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "BLIS_NUM_THREADS"):
        env[name] = "1"
    base = [sys.executable, "-B"] + (["-O"] if optimized else [])

    def child(args):
        p = subprocess.run(base + args, cwd=ROOT, env=env, capture_output=True,
                           text=True, timeout=45)
        need(p.returncode == 0, "incomplete or failed run: " + p.stderr)
        return p.stdout

    controls = json.loads(child(["controls.py"]))
    stages = []
    for i in range(1, 5):
        out = scratch / ("stage" + str(i) + ".json")
        args = ["stage.py", "--stage", str(i), "--out", str(out),
                "--records", str(scratch / ("canonical" + str(i) + ".bin"))]
        if i > 1:
            args += ["--previous", str(scratch / ("stage" + str(i - 1) + ".json"))]
        child(args)
        stages.append(json.loads(out.read_text()))
    result = assemble(controls, stages)
    raw = (json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n").encode()
    need(raw == (ROOT / "EXPECTED.json").read_bytes(), "entire independent record mismatch")
    (scratch / "REPRODUCED.json").write_bytes(raw)
    return {"complete": True, "entire_record_sha256": hashlib.sha256(raw).hexdigest(),
            "raw_branch_records": sum(s["raw_input_count"] for s in stages),
            "original_resource_marginals": sum(s["marginal_entries"] for s in stages),
            "phase_intersections": sum(s["phase_intersections"] for s in stages),
            "BASE_holes_outside_parent4_at_least": 2,
            "productive_TAIL_classes_at_least": 2, "sharpness_claimed": False}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--scratch", required=True)
    p.add_argument("--optimized", action="store_true")
    a = p.parse_args()
    print(json.dumps(run(a.scratch, a.optimized), sort_keys=True))
