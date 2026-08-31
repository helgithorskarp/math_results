#!/usr/bin/env python3
"""SAT search used to discover additional small locating-dominating codes."""

from __future__ import annotations

import argparse
import hashlib
import time

from pysat.card import CardEnc, EncType
from pysat.formula import CNF
from pysat.solvers import Solver


DIMENSION = 7
VERTEX_COUNT = 1 << DIMENSION
NEIGHBORHOODS = tuple(
    frozenset(
        {vertex, *(vertex ^ (1 << coordinate) for coordinate in range(DIMENSION))}
    )
    for vertex in range(VERTEX_COUNT)
)


def build(bound: int, zero_degree: int | None) -> CNF:
    """Encode a locating-dominating code of size at most ``bound``."""
    cnf = CNF()
    for vertex in range(VERTEX_COUNT):
        cnf.append([word + 1 for word in sorted(NEIGHBORHOODS[vertex])])
    for first in range(VERTEX_COUNT):
        for second in range(first + 1, VERTEX_COUNT):
            witnesses = sorted(NEIGHBORHOODS[first] ^ NEIGHBORHOODS[second])
            cnf.append(
                [first + 1, second + 1, *(word + 1 for word in witnesses)]
            )

    # Location-domination is monotone under adding codewords, so at-most K
    # decides whether a code of any size at most K exists.
    cardinality = CardEnc.atmost(
        lits=list(range(1, VERTEX_COUNT + 1)),
        bound=bound,
        top_id=cnf.nv,
        encoding=EncType.totalizer,
    )
    cnf.extend(cardinality.clauses)

    # Every nonempty code can be translated to contain zero.
    cnf.append([1])
    if zero_degree is not None:
        # Coordinate permutations make the neighborhood pattern canonical.
        for coordinate in range(DIMENSION):
            variable = (1 << coordinate) + 1
            cnf.append([variable if coordinate < zero_degree else -variable])
    return cnf


def dimacs_bytes(cnf: CNF) -> bytes:
    lines = [f"p cnf {cnf.nv} {len(cnf.clauses)}"]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in cnf.clauses)
    return ("\n".join(lines) + "\n").encode("ascii")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bound", type=int)
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--zero-degree", type=int, choices=range(DIMENSION + 1))
    parser.add_argument(
        "--write-cnf",
        metavar="SCRATCH_PATH",
        help="optionally write DIMACS; use a path under /scratch",
    )
    args = parser.parse_args()

    started = time.monotonic()
    cnf = build(args.bound, args.zero_degree)
    payload = dimacs_bytes(cnf)
    print(
        f"Q7 size <= {args.bound}: {cnf.nv} variables, "
        f"{len(cnf.clauses)} clauses, "
        f"sha256 {hashlib.sha256(payload).hexdigest()}",
        flush=True,
    )
    if args.write_cnf:
        with open(args.write_cnf, "wb") as output:
            output.write(payload)
    print(f"built in {time.monotonic() - started:.3f}s", flush=True)

    solve_started = time.monotonic()
    with Solver(name=args.solver, bootstrap_with=cnf.clauses) as solver:
        satisfiable = solver.solve()
        model = solver.get_model() if satisfiable else None
    print(
        f"{args.solver}: {'SAT' if satisfiable else 'UNSAT'} "
        f"in {time.monotonic() - solve_started:.3f}s"
    )
    if model is not None:
        positive = {literal for literal in model if literal > 0}
        code = [
            vertex
            for vertex in range(VERTEX_COUNT)
            if vertex + 1 in positive
        ]
        print(" ".join(f"{vertex:07b}" for vertex in code))


if __name__ == "__main__":
    main()
