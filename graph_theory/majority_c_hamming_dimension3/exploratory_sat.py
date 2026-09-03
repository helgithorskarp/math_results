#!/usr/bin/env python3
"""Optional exact SAT cross-checks used during discovery of the theorem.

Requires python-sat.  Solver verdicts are not used by the proof in README.md.
"""

from __future__ import annotations

import argparse
import itertools
import json

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver


Vertex = tuple[int, ...]


def vertices(n: int, dimension: int) -> list[Vertex]:
    return list(itertools.product(range(n), repeat=dimension))


def neighbor_indices(v: Vertex, n: int, index: dict[Vertex, int]) -> list[int]:
    out = []
    for coordinate, old in enumerate(v):
        for new in range(n):
            if new == old:
                continue
            w = list(v)
            w[coordinate] = new
            out.append(index[tuple(w)])
    return out


def conditional_majority_clauses(
    cnf: CNF,
    guard: int,
    neighbor_literals: list[int],
    threshold: int,
) -> None:
    false_subset_size = len(neighbor_literals) - threshold + 1
    for subset in itertools.combinations(neighbor_literals, false_subset_size):
        cnf.append([-guard, *subset])


def coloring_cnf(n: int, dimension: int, colors: int) -> tuple[CNF, list[Vertex]]:
    vs = vertices(n, dimension)
    index = {v: i for i, v in enumerate(vs)}

    def variable(i: int, color: int) -> int:
        return 1 + i * colors + color

    cnf = CNF()
    for i in range(len(vs)):
        cnf.append([variable(i, color) for color in range(colors)])
        for first, second in itertools.combinations(range(colors), 2):
            cnf.append([-variable(i, first), -variable(i, second)])
    for color in range(colors):
        cnf.append([variable(i, color) for i in range(len(vs))])

    # Canonical first-use order removes only permutations of color names.
    cnf.append([variable(0, 0)])
    for color in range(1, colors):
        for i in range(len(vs)):
            cnf.append(
                [-variable(i, color)]
                + [variable(j, color - 1) for j in range(i)]
            )

    degree = dimension * (n - 1)
    threshold = (degree + 1) // 2
    for i, v in enumerate(vs):
        neighbors = neighbor_indices(v, n, index)
        for color in range(colors):
            conditional_majority_clauses(
                cnf,
                variable(i, color),
                [variable(j, color) for j in neighbors],
                threshold,
            )
    return cnf, vs


def minimum_class_cnf(n: int, dimension: int, size: int) -> tuple[CNF, list[Vertex]]:
    vs = vertices(n, dimension)
    index = {v: i for i, v in enumerate(vs)}
    degree = dimension * (n - 1)
    threshold = (degree + 1) // 2
    cnf = CNF()
    cnf.append([1])  # The origin is in the set, by vertex transitivity.
    for i, v in enumerate(vs):
        conditional_majority_clauses(
            cnf,
            i + 1,
            [j + 1 for j in neighbor_indices(v, n, index)],
            threshold,
        )
    pool = IDPool(start_from=len(vs) + 1)
    cnf.extend(
        CardEnc.atmost(
            lits=list(range(1, len(vs) + 1)),
            bound=size,
            vpool=pool,
            encoding=EncType.seqcounter,
        )
    )
    return cnf, vs


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="mode", required=True)
    coloring = subparsers.add_parser("coloring")
    coloring.add_argument("--n", type=int, required=True)
    coloring.add_argument("--dimension", type=int, default=3)
    coloring.add_argument("--colors", type=int, required=True)
    minimum = subparsers.add_parser("minimum-class")
    minimum.add_argument("--n", type=int, required=True)
    minimum.add_argument("--dimension", type=int, default=3)
    minimum.add_argument("--size", type=int, required=True)
    parser.add_argument("--solver", default="cadical195")
    args = parser.parse_args()

    if args.mode == "coloring":
        cnf, vs = coloring_cnf(args.n, args.dimension, args.colors)
    else:
        cnf, vs = minimum_class_cnf(args.n, args.dimension, args.size)

    with Solver(name=args.solver, bootstrap_with=cnf) as solver:
        sat = solver.solve()
        model = solver.get_model() if sat else None

    result: dict[str, object] = {
        "mode": args.mode,
        "n": args.n,
        "dimension": args.dimension,
        "solver": args.solver,
        "variables": cnf.nv,
        "clauses": len(cnf.clauses),
        "status": "SAT" if sat else "UNSAT",
    }
    if model is not None:
        positive = {literal for literal in model if literal > 0}
        if args.mode == "minimum-class":
            result["set"] = [
                list(v) for i, v in enumerate(vs) if i + 1 in positive
            ]
        else:
            classes: list[list[list[int]]] = [[] for _ in range(args.colors)]
            for i, v in enumerate(vs):
                hits = [
                    color
                    for color in range(args.colors)
                    if 1 + i * args.colors + color in positive
                ]
                assert len(hits) == 1
                classes[hits[0]].append(list(v))
            result["classes"] = classes
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
