#!/usr/bin/env python3
"""Generate and independently DRAT-check proofs for the review binary CNFs."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import time


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path: Path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cnf-dir", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--cadical", required=True, type=Path)
    parser.add_argument("--drat-trim", required=True, type=Path)
    parser.add_argument("--seconds", type=int, default=900)
    args = parser.parse_args()
    require(args.seconds > 0, "positive timeout")
    args.out.mkdir(parents=True, exist_ok=True)
    cadical = args.cadical.resolve()
    checker = args.drat_trim.resolve()
    require(cadical.is_file() and checker.is_file(), "solver/checker binaries exist")
    results = []
    for stem in ("host_completeness_binary", "parent_binary"):
        cnf = (args.cnf_dir / f"{stem}.cnf").resolve()
        proof = (args.out / f"{stem}.drat").resolve()
        solver_log = args.out / f"{stem}.solver.log"
        checker_log = args.out / f"{stem}.checker.log"
        require(cnf.is_file(), f"CNF exists: {stem}")
        start = time.monotonic()
        solve_command = [str(cadical), "-t", str(args.seconds), str(cnf), str(proof)]
        with solver_log.open("w") as stream:
            solved = subprocess.run(solve_command, stdout=stream,
                                    stderr=subprocess.STDOUT,
                                    timeout=args.seconds + 20)
        require(solved.returncode == 20, f"{stem}: solver returned UNSAT")
        check_command = [str(checker), str(cnf), str(proof),
                         "-t", str(args.seconds)]
        with checker_log.open("w") as stream:
            checked = subprocess.run(check_command, stdout=stream,
                                     stderr=subprocess.STDOUT,
                                     timeout=args.seconds + 20)
        text = checker_log.read_text()
        require(checked.returncode == 0 and "s VERIFIED" in text,
                f"{stem}: DRAT proof verified")
        item = {
            "name": stem,
            "cnf_sha256": digest(cnf),
            "cnf_bytes": cnf.stat().st_size,
            "drat_sha256": digest(proof),
            "drat_bytes": proof.stat().st_size,
            "solver_exit": solved.returncode,
            "checker_exit": checked.returncode,
            "checker_reported_verified": True,
            "solver_binary_sha256": digest(cadical),
            "checker_binary_sha256": digest(checker),
            "elapsed_seconds": time.monotonic() - start,
        }
        results.append(item)
        (args.out / "binary_proof_checks.json").write_text(
            json.dumps(results, indent=2) + "\n")
        print(json.dumps(item), flush=True)


if __name__ == "__main__":
    main()
