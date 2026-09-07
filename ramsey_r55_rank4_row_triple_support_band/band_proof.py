#!/usr/bin/env python3
"""Solve and externally check the single support-at-most-eight formula."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import time

from joint_completion import file_sha256


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--checker", type=Path, required=True)
    parser.add_argument("--proof", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--seconds", type=int, default=600)
    parser.add_argument("--keep-proof", action="store_true")
    args = parser.parse_args()

    metadata = json.loads(args.metadata.read_text())
    expected_hash = metadata["formula"]["sha256"]
    if file_sha256(args.cnf) != expected_hash:
        raise RuntimeError("formula hash mismatch")
    command = [str(args.solver), "-q", "--unsat"]
    if "kissat" in args.solver.name.lower():
        command.append(f"--time={args.seconds}")
    else:
        command += ["-t", str(args.seconds)]
    command += [str(args.cnf), str(args.proof)]
    started = time.monotonic()
    solved = subprocess.run(command, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, text=True, check=False,
                            timeout=args.seconds + 60)
    solver_seconds = time.monotonic() - started
    result = {
        "schema": "rank4-row-triple-support-band-single-proof-v1",
        "cnf_sha256": expected_hash,
        "cnf_bytes": args.cnf.stat().st_size,
        "variables": metadata["formula"]["variables"],
        "clauses": metadata["formula"]["clauses"],
        "solver": subprocess.run([str(args.solver), "--version"],
                                 capture_output=True, text=True,
                                 check=True).stdout.strip(),
        "solver_sha256": file_sha256(args.solver),
        "solver_seconds": solver_seconds,
        "proof_format": "binary-drat",
        "checker_sha256": file_sha256(args.checker),
    }
    if (solved.returncode == 20 and "s UNSATISFIABLE" in solved.stdout
            and args.proof.is_file() and args.proof.stat().st_size):
        checked_at = time.monotonic()
        checked = subprocess.run([str(args.checker), str(args.cnf), str(args.proof)],
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 text=True, check=False,
                                 timeout=2 * args.seconds + 120)
        result["checker_seconds"] = time.monotonic() - checked_at
        if checked.returncode == 0 and "s VERIFIED" in checked.stdout:
            result.update({
                "status": "UNSAT_PROOF_VERIFIED",
                "proof_bytes": args.proof.stat().st_size,
                "proof_sha256": file_sha256(args.proof),
            })
        else:
            result.update({
                "status": "PROOF_REJECTED",
                "checker_output_tail": checked.stdout[-1000:],
            })
    else:
        result.update({
            "status": "UNKNOWN_OR_MISSING_PROOF",
            "solver_exit": solved.returncode,
            "solver_output_tail": solved.stdout[-1000:],
        })
    args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))
    if not args.keep_proof:
        args.proof.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
