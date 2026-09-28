"""Budgeted SAT probe for six-color Schur colorings.

Requires python-sat 1.9.dev15. UNKNOWN means only the conflict budget was hit.
"""

from __future__ import annotations

import argparse
import time

from pysat.solvers import Solver


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=537)
    parser.add_argument("--colors", type=int, default=6)
    parser.add_argument("--symmetry", action="store_true",
                        help="require equal colors at i and N+1-i")
    parser.add_argument("--conflicts", type=int, default=100000)
    args = parser.parse_args()
    n, k = args.n, args.colors
    if n < 1 or k < 1 or args.conflicts < 1:
        parser.error("n, colors, and conflicts must be positive")

    def representative(i: int) -> int:
        return min(i, n + 1 - i) if args.symmetry else i

    def variable(i: int, color: int) -> int:
        return (representative(i) - 1) * k + color + 1

    clauses: list[list[int]] = []
    for i in sorted({representative(j) for j in range(1, n + 1)}):
        clauses.append([variable(i, c) for c in range(k)])
        for c in range(k):
            for d in range(c):
                clauses.append([-variable(i, c), -variable(i, d)])

    # Every x <= y with x+y <= N is encoded, including x=y.
    for x in range(1, n + 1):
        for y in range(x, n - x + 1):
            z = x + y
            for c in range(k):
                clauses.append(sorted(set((-variable(x, c), -variable(y, c),
                                           -variable(z, c)))))

    start = time.monotonic()
    with Solver(name="cadical195", bootstrap_with=clauses) as solver:
        solver.conf_budget(args.conflicts)
        result = solver.solve_limited(expect_interrupt=True)
        elapsed = time.monotonic() - start
        print(f"n={n} colors={k} symmetry={args.symmetry} clauses={len(clauses)} "
              f"conflict_budget={args.conflicts} result="
              f"{'SAT' if result is True else 'UNSAT' if result is False else 'UNKNOWN'} "
              f"seconds={elapsed:.2f} stats={solver.accum_stats()}")
        if result is not True:
            return
        model = set(solver.get_model())
        coloring = []
        for i in range(1, n + 1):
            choices = [c for c in range(k) if variable(i, c) in model]
            if len(choices) != 1:
                raise RuntimeError(f"bad decoding at {i}")
            coloring.append(choices[0])
        for x in range(1, n + 1):
            for y in range(x, n - x + 1):
                if coloring[x - 1] == coloring[y - 1] == coloring[x + y - 1]:
                    raise RuntimeError(f"invalid witness at {(x, y, x + y)}")
        print("verified_coloring=" + "".join(str(c + 1) for c in coloring))


if __name__ == "__main__":
    main()
