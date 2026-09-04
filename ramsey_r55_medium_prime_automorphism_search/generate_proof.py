#!/usr/bin/env python3
"""Generate a Glucose RUP proof for one medium-prime formula."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import pysat
from pysat.formula import CNF
from pysat.solvers import Solver


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("formula", type=Path)
    parser.add_argument("proof", type=Path)
    args = parser.parse_args()

    formula = CNF(from_file=args.formula)
    with Solver(
        name="glucose42", bootstrap_with=formula.clauses, with_proof=True
    ) as solver:
        satisfiable = solver.solve()
        proof = solver.get_proof() if not satisfiable else None
    if satisfiable or proof is None:
        raise AssertionError("expected UNSAT formula with a proof trace")
    args.proof.write_text("\n".join(proof) + "\n")
    additions = sum(not line.startswith("d ") for line in proof)
    print(
        f"formula={args.formula} proof={args.proof} solver=glucose42 "
        f"pysat={pysat.__version__} lines={len(proof)} additions={additions} "
        f"deletions={len(proof) - additions} bytes={args.proof.stat().st_size} "
        f"sha256={hashlib.sha256(args.proof.read_bytes()).hexdigest()}",
        flush=True,
    )


if __name__ == "__main__":
    main()
