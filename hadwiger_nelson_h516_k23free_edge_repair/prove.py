#!/usr/bin/env python3
"""Generate a fresh DRAT proof for the frozen four-colouring CNF."""
import argparse
import hashlib
import json
import pathlib
import shutil
import time

from pysat.formula import CNF
from pysat.solvers import Glucose42

D = pathlib.Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", type=pathlib.Path, required=True)
    args = ap.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    cnf = D / "four_colour.cnf"
    start = time.monotonic()
    with Glucose42(bootstrap_with=CNF(from_file=str(cnf)).clauses,
                   with_proof=True) as solver:
        solver.conf_budget(5_000_000)
        answer = solver.solve_limited(expect_interrupt=True)
        elapsed = time.monotonic() - start
        solver.prfile.flush()
        solver.prfile.seek(0)
        name = "four_colour.drat" if answer is False else "four_colour.partial.drat"
        target = args.work / name
        with target.open("wb") as handle:
            shutil.copyfileobj(solver.prfile, handle)
        receipt = {
            "answer": "UNSAT" if answer is False else "SAT" if answer else "UNKNOWN",
            "seconds": elapsed,
            "statistics": solver.accum_stats(),
            "proof_file": name,
            "proof_bytes": target.stat().st_size,
            "proof_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            "proof_verified": False,
        }
    (args.work / "solve.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
