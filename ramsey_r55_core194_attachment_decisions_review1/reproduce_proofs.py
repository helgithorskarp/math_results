#!/usr/bin/env python3
"""Generate and fully replay the five claimed Core194 refutations serially."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import time
from pathlib import Path


CASES = ("a1_b3_c3", "a2_b2_c3", "a3_b1_c3", "a3_b2_c2", "a4_b0_c3")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def identity(path: Path) -> dict:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return {"bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def exact_status(text: str, expected: str) -> None:
    rows = [line for line in text.splitlines() if line.startswith("s ")]
    require(rows == [expected], "unexpected solver status transcript")


def main() -> None:
    if not __debug__:
        raise RuntimeError("run with assertions enabled (omit -O)")
    parser = argparse.ArgumentParser()
    parser.add_argument("--formula-work", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--kissat", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--solve-seconds", type=int, default=120)
    parser.add_argument("--replay-seconds", type=int, default=600)
    args = parser.parse_args()
    require(not args.out.exists(), "output directory must be new")
    require(args.solve_seconds > 0 and args.replay_seconds > 0, "positive time limits")
    args.out.mkdir(parents=True)
    version = subprocess.run([str(args.kissat), "--version"], text=True, capture_output=True, check=True).stdout.strip()
    require(version == "4.0.4", "unexpected Kissat version")
    start = time.monotonic()
    rows = []
    for case in CASES:
        cnf = args.formula_work / f"{case}.cnf"
        trace = args.out / f"{case}.drat"
        solve_log = args.out / f"{case}.solve.log"
        replay_log = args.out / f"{case}.replay.log"
        solve_start = time.monotonic()
        with solve_log.open("w") as output:
            solved = subprocess.run(
                [str(args.kissat), f"--time={args.solve_seconds}", str(cnf), str(trace)],
                stdout=output,
                stderr=subprocess.STDOUT,
                timeout=args.solve_seconds + 60,
            )
        exact_status(solve_log.read_text(), "s UNSATISFIABLE")
        require(solved.returncode == 20, "Kissat did not return UNSAT")
        solve_elapsed = round(time.monotonic() - solve_start, 6)
        replay_start = time.monotonic()
        with replay_log.open("w") as output:
            checked = subprocess.run(
                [str(args.drat_trim), str(cnf), str(trace), "-t", str(args.replay_seconds)],
                stdout=output,
                stderr=subprocess.STDOUT,
                timeout=args.replay_seconds + 60,
            )
        replay_text = replay_log.read_text()
        require(checked.returncode == 0 and "s VERIFIED" in replay_text, "full DRAT replay failed")
        match = re.search(r"(\d+) RAT lemmas in core", replay_text)
        require(match is not None, "missing RAT statistics")
        rows.append(
            {
                "id": case,
                "formula": identity(cnf),
                "proof": identity(trace),
                "solver_log": identity(solve_log),
                "replay_log": identity(replay_log),
                "rat_core_lemmas": int(match.group(1)),
                "solve_seconds": solve_elapsed,
                "replay_seconds": round(time.monotonic() - replay_start, 6),
            }
        )
        print(f"VERIFIED {case}", flush=True)
    report = {
        "status": "PASS",
        "execution": "serial; one solver or checker process at a time",
        "kissat_version": version,
        "kissat_binary": identity(args.kissat),
        "drat_trim_binary": identity(args.drat_trim),
        "cases": rows,
        "elapsed_seconds": round(time.monotonic() - start, 6),
    }
    (args.out / "proofs.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "cases": list(CASES)}, sort_keys=True))


if __name__ == "__main__":
    main()
