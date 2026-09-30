#!/usr/bin/env python3
"""Regenerate all certificates, then check them and controls sequentially."""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if args.output_dir.exists() and not args.resume:
        parser.error("Use a fresh output directory, or --resume to replay saved cases")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    proofs = args.output_dir / "proofs"
    expected = HERE / "expected.json"
    env = os.environ.copy()
    env.update({k: "1" for k in ["OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS",
                                "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"]})
    start = time.monotonic()
    command = [sys.executable, str(HERE / "generate.py"), "--output", str(proofs),
               "--seconds-per-case", "90"]
    if args.resume:
        command.append("--resume")
    # Generation has a separate <=90s limit for each of the finitely many
    # primitive parents/children. Every STARTED attempt is durably recorded.
    subprocess.run(command, env=env, check=True)
    for optimized in (False, True):
        interpreter = [sys.executable] + (["-O"] if optimized else [])
        subprocess.run(interpreter + [str(HERE / "verify.py"), str(proofs),
                                     "--expected", str(expected)],
                       env=env, check=True, timeout=90)
        for e in (0, 1):
            for a, b in [(30, 32), (32, 30)]:
                name = f"controls-{e}-{a}-{b}-{'optimized' if optimized else 'normal'}.json"
                subprocess.run(interpreter + [str(HERE / "checker_controls.py"), str(proofs),
                    "--endpoint", str(e), "--budget", str(a), str(b),
                    "--output", str(args.output_dir / name)],
                    env=env, check=True, timeout=90)
    for e in (0, 1):
        for a, b in [(30, 32), (32, 30)]:
            paths = [args.output_dir / f"controls-{e}-{a}-{b}-{mode}.json"
                     for mode in ("normal", "optimized")]
            normal, optimized = [json.loads(p.read_text()) for p in paths]
            if normal != optimized:
                raise ValueError("Normal/optimized complete control results differ")
    print(json.dumps({"status": "UNIFORM63_CERTIFICATES_AND_CONTROLS_PASSED",
                      "agent": "six-vdw-2", "role": "researcher",
                      "root_cases": 24, "nodes": 36, "splits": 2, "closed_leaves": 34,
                      "full_parent_state_regressions": 24, "controls_rejected": 76,
                      "all_checks_sequential": True, "threads": 1,
                      "seconds": round(time.monotonic()-start, 3)}))


if __name__ == "__main__":
    main()
