#!/usr/bin/env python3
"""Run one bounded SAT screen and preserve a model if found."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import pysat
from pysat.formula import CNF
from pysat.solvers import Solver


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("formula", type=Path)
    parser.add_argument("--solver", default="kissat404")
    parser.add_argument("--model", type=Path)
    args = parser.parse_args()

    formula = CNF(from_file=args.formula)
    start = time.monotonic()
    with Solver(name=args.solver, bootstrap_with=formula.clauses) as solver:
        satisfiable = solver.solve()
        model = solver.get_model() if satisfiable else None
    elapsed = time.monotonic() - start
    print(
        f"formula={args.formula} variables={formula.nv} clauses={len(formula.clauses)} "
        f"solver={args.solver} pysat={pysat.__version__} "
        f"result={'SAT' if satisfiable else 'UNSAT'} seconds={elapsed:.6f}",
        flush=True,
    )
    if satisfiable:
        if args.model is None:
            raise ValueError("--model is required when the formula is SAT")
        args.model.write_text(json.dumps({"model": model}, sort_keys=True) + "\n")
        print(f"wrote_model={args.model}", flush=True)


if __name__ == "__main__":
    main()
