#!/usr/bin/env python3
"""Exhaustively sanity-check the sequential-counter bridge on small inputs.

This does not replace inspection of the cardinality encoding.  It guards the
specific API convention used by ``build_hitting_decision.py``: the generated
CNF must be extendible exactly when at least ``bound`` input literals are true.
"""

from __future__ import annotations

from itertools import product

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver


def main() -> None:
    cases = 0
    for size in range(1, 9):
        inputs = list(range(1, size + 1))
        for bound in range(0, size + 1):
            encoding = CardEnc.atleast(
                lits=inputs,
                bound=bound,
                top_id=size,
                encoding=EncType.seqcounter,
            )
            with Solver(bootstrap_with=encoding.clauses) as solver:
                for values in product((False, True), repeat=size):
                    assumptions = [
                        variable if value else -variable
                        for variable, value in zip(inputs, values)
                    ]
                    observed = solver.solve(assumptions=assumptions)
                    expected = sum(values) >= bound
                    assert observed == expected, (size, bound, values)
                    cases += 1
    print(f"sizes=1..8 assignments_checked={cases}")
    print("cardinality_api_check=true")


if __name__ == "__main__":
    main()
