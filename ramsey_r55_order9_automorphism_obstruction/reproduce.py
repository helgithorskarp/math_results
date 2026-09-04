#!/usr/bin/env python3
"""Regenerate both formulas and certificates, then independently replay them.

All bulky generated files stay in the required external --work directory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command, log=None):
    if log is None:
        return subprocess.run(command, check=True, cwd=HERE)
    with log.open("w") as out:
        return subprocess.run(command, stdout=out, stderr=subprocess.STDOUT, cwd=HERE)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--kissat", default=os.environ.get("KISSAT", "kissat"))
    parser.add_argument("--drat-trim", default=os.environ.get("DRAT_TRIM", "drat-trim"))
    parser.add_argument("--cxx", default=os.environ.get("CXX", "g++"))
    parser.add_argument("--seconds", type=int, default=300,
                        help="per-solver limit; a timeout is a failed reproduction")
    args = parser.parse_args()
    work = args.work.resolve()
    if work == HERE.parent or HERE.parent in work.parents:
        raise ValueError("put generated files outside the repository")
    if args.seconds <= 0:
        raise ValueError("seconds must be positive")
    work.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((HERE / "result.json").read_text())
    for relative, digest in manifest["source_dependencies"].items():
        if sha(HERE / relative) != digest:
            raise RuntimeError(f"source dependency mismatch: {relative}")
    run([sys.executable, str(HERE / "audit_symmetry.py")])
    verifier = work / "verify_formula"
    run([args.cxx, "-O3", "-std=c++20", "-Wall", "-Wextra", "-Wpedantic",
         str(HERE / "verify_formula.cpp"), "-o", str(verifier)])
    observed = []
    for index, expected in enumerate(manifest["cases"]):
        started = time.monotonic()
        formula = work / f"case{index}.cnf"
        run([sys.executable, str(HERE / "generate_formula.py"),
             "--case", str(index), str(formula)])
        if sha(formula) != expected["cnf_sha256"]:
            raise RuntimeError("formula hash mismatch")
        run([str(verifier), str(index), str(formula)])
        proof = work / f"case{index}.drat"
        answer = run([args.kissat, f"--time={args.seconds}", "--quiet",
                      str(formula), str(proof)], work / f"case{index}.solver.log")
        if answer.returncode != 20:
            raise RuntimeError(f"case {index}: solver exit {answer.returncode}; not certified")
        replay_log = work / f"case{index}.replay.log"
        replay = run([args.drat_trim, str(formula), str(proof)], replay_log)
        verified = "s VERIFIED" in replay_log.read_text().splitlines()
        if replay.returncode != 0 or not verified:
            raise RuntimeError(f"case {index}: proof replay failed")
        record = {"case": expected["cycle_counts"], "cnf_sha256": sha(formula),
                  "proof_sha256": sha(proof), "proof_bytes": proof.stat().st_size,
                  "matches_reference_proof": sha(proof) == expected["reference_proof_sha256"],
                  "independently_replayed": True,
                  "elapsed_seconds": round(time.monotonic() - started, 3)}
        observed.append(record)
        (work / "replay.json").write_text(json.dumps(observed, indent=2) + "\n")
        print(f"PASS case={index} UNSAT certificate_replay=VERIFIED "
              f"reference_proof_match={record['matches_reference_proof']}", flush=True)
    print("PASS both residual order-nine cases independently certified")


if __name__ == "__main__":
    main()
