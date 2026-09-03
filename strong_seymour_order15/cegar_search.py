#!/usr/bin/env python3
"""Counterexample-guided SAT search for order-15 strong Seymour vertices.

The persistent clauses forbid explicit complete directed matchings.  Every
such clause is valid in any tournament with no strong Seymour vertex.  If the
accumulated CNF is UNSAT, it is therefore an independently checkable finite
exclusion.  All generated files must be written below /scratch.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver


N = 15


def arc(pool: IDPool, i: int, j: int) -> int:
    """Literal asserting i -> j; the edge variable means low -> high."""
    if i == j:
        raise ValueError("loops are not tournament arcs")
    variable = pool.id(("edge", min(i, j), max(i, j)))
    return variable if i < j else -variable


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_case(case: str) -> tuple[int, int]:
    degree_text, size_text = case.split("-")
    return int(degree_text[1:]), int(size_text[1:])


def at_least(
    cnf: CNF, pool: IDPool, literals: list[int], bound: int
) -> None:
    cnf.extend(
        CardEnc.atleast(
            literals, bound=bound, vpool=pool, encoding=EncType.totalizer
        ).clauses
    )


def at_most(cnf: CNF, pool: IDPool, literals: list[int], bound: int) -> None:
    cnf.extend(
        CardEnc.atmost(
            literals, bound=bound, vpool=pool, encoding=EncType.totalizer
        ).clauses
    )


def exactly(cnf: CNF, pool: IDPool, literals: list[int], bound: int) -> None:
    at_least(cnf, pool, literals, bound)
    at_most(cnf, pool, literals, bound)


def add_normalized_obstruction(
    cnf: CNF,
    pool: IDPool,
    root: int,
    left: list[int],
    right: list[int],
    available_heads: list[int],
    require_internal_outneighbor: bool,
) -> None:
    """Fix an inclusion-minimal Hall witness at a normalized root."""
    if len(right) != len(left) - 1:
        raise ValueError("a minimal witness has one fewer Hall neighbor")
    for tail in left:
        if arc(pool, root, tail) not in cnf.clauses:
            # The caller normally fixes these arcs separately.  Requiring them
            # again makes this helper safe for the secondary normalization.
            cnf.append([arc(pool, root, tail)])
    for head in available_heads:
        incoming = [arc(pool, tail, head) for tail in left]
        if head in right:
            # Inclusion-minimality makes every Hall neighbor have at least two
            # preimages.  This is useful but not needed for deficiency alone.
            at_least(cnf, pool, incoming, 2)
        else:
            for literal in incoming:
                cnf.append([-literal])
    if require_internal_outneighbor:
        for tail in left:
            cnf.append(
                [arc(pool, tail, other) for other in left if other != tail]
            )


def build_base(
    case: str,
    mode: str,
    secondary_size: int | None,
    secondary_degree_region: str | None,
) -> tuple[CNF, IDPool]:
    root_degree, root_size = parse_case(case)
    valid_sizes = {6: range(3, 6), 7: range(1, 7)}
    if root_degree not in valid_sizes or root_size not in valid_sizes[root_degree]:
        raise ValueError("cases are d6-s3..5 and d7-s1..6")
    if mode not in {"all", "regular", "nonregular"}:
        raise ValueError(mode)
    if mode == "regular" and (root_degree != 7 or root_size < 3):
        raise ValueError("regular cases are d7-s3..6")
    if secondary_size is not None and not (
        mode == "nonregular"
        and root_degree == 7
        and root_size == 1
        and secondary_size in range(3, 7)
    ):
        raise ValueError("secondary normalization is only d7-s1, sizes 3..6")
    if secondary_degree_region is not None and not (
        secondary_size == 6
        and secondary_degree_region in {"witness", "neighbors"}
    ):
        raise ValueError("secondary degree region requires secondary size six")

    pool = IDPool()
    cnf = CNF()
    degrees = [
        [arc(pool, x, y) for y in range(N) if y != x] for x in range(N)
    ]
    for degree_literals in degrees:
        at_least(cnf, pool, degree_literals, 6)
        if mode == "regular":
            exactly(cnf, pool, degree_literals, 7)

    root = 0
    exactly(cnf, pool, degrees[root], root_degree)
    for y in range(1, N):
        cnf.append([arc(pool, root, y) if y <= root_degree else arc(pool, y, root)])
    root_left = list(range(1, root_size + 1))
    root_right = list(range(root_degree + 1, root_degree + root_size))
    root_heads = list(range(root_degree + 1, N))
    add_normalized_obstruction(
        cnf,
        pool,
        root,
        root_left,
        root_right,
        root_heads,
        require_internal_outneighbor=root_degree == 6 or mode == "regular",
    )

    if mode == "nonregular" and root_degree == 7:
        if root_size == 1:
            exactly(cnf, pool, degrees[1], 6)
        elif root_size == 2:
            cnf.append([arc(pool, 1, 2)])
            exactly(cnf, pool, degrees[2], 6)
        else:
            representatives = [1]
            if root_size < root_degree:
                representatives.append(root_size + 1)
            representatives.append(root_degree + 1)
            if root_degree + root_size <= N - 1:
                representatives.append(root_degree + root_size)
            # At least one representative has degree exactly six.  Since the
            # global lower bound is already present, it suffices to forbid all
            # representatives from simultaneously having degree >=7.
            threshold_literals: list[int] = []
            for index, vertex in enumerate(representatives):
                indicator = pool.id(("representative-degree-at-least-seven", index))
                threshold_literals.append(indicator)
                clauses = CardEnc.atleast(
                    degrees[vertex],
                    bound=7,
                    vpool=pool,
                    encoding=EncType.totalizer,
                ).clauses
                cnf.extend([[-indicator, *clause] for clause in clauses])
                clauses = CardEnc.atmost(
                    degrees[vertex],
                    bound=6,
                    vpool=pool,
                    encoding=EncType.totalizer,
                ).clauses
                cnf.extend([[indicator, *clause] for clause in clauses])
            cnf.append([-indicator for indicator in threshold_literals])

    if secondary_size is not None:
        secondary_root = 1
        secondary_left = list(range(2, 2 + secondary_size))
        secondary_right = list(range(8, 8 + secondary_size - 1))
        add_normalized_obstruction(
            cnf,
            pool,
            secondary_root,
            secondary_left,
            secondary_right,
            [0, *range(8, N)],
            require_internal_outneighbor=True,
        )
        if secondary_size == 6:
            cnf.append([arc(pool, 13, 14)])
            if secondary_degree_region == "witness":
                exactly(cnf, pool, degrees[2], 6)
            elif secondary_degree_region == "neighbors":
                exactly(cnf, pool, degrees[8], 6)
            else:
                # The split form is preferred for proof production.  Without
                # it, encode the valid disjunction using two exact indicators.
                indicators: list[int] = []
                for vertex in (2, 8):
                    indicator = pool.id(("secondary-degree-six", vertex))
                    indicators.append(indicator)
                    clauses = CardEnc.atmost(
                        degrees[vertex],
                        bound=6,
                        vpool=pool,
                        encoding=EncType.totalizer,
                    ).clauses
                    cnf.extend([[-indicator, *clause] for clause in clauses])
                cnf.append(indicators)

    return cnf, pool


def decode_tournament(pool: IDPool, model: list[int]) -> list[list[bool]]:
    positive = {literal for literal in model if literal > 0}
    matrix = [[False] * N for _ in range(N)]
    for i in range(N):
        for j in range(i + 1, N):
            if abs(arc(pool, i, j)) in positive:
                matrix[i][j] = True
            else:
                matrix[j][i] = True
    return matrix


def perfect_matchings(
    matrix: list[list[bool]], root: int, limit: int
) -> list[list[tuple[int, int]]]:
    left = [vertex for vertex in range(N) if matrix[root][vertex]]
    right = [vertex for vertex in range(N) if matrix[vertex][root]]
    if len(left) > len(right):
        return []
    choices = {
        tail: [head for head in right if matrix[tail][head]] for tail in left
    }
    ordered_left = sorted(left, key=lambda tail: (len(choices[tail]), tail))
    results: list[list[tuple[int, int]]] = []

    def visit(position: int, used: set[int], pairs: list[tuple[int, int]]) -> None:
        if limit and len(results) >= limit:
            return
        if position == len(ordered_left):
            results.append(pairs[:])
            return
        tail = ordered_left[position]
        for head in choices[tail]:
            if head in used:
                continue
            used.add(head)
            pairs.append((tail, head))
            visit(position + 1, used, pairs)
            pairs.pop()
            used.remove(head)

    visit(0, set(), [])
    return results


def forbid_matching_clause(
    pool: IDPool,
    matrix: list[list[bool]],
    root: int,
    matching: list[tuple[int, int]],
) -> list[int]:
    event = [
        arc(pool, root, vertex) if matrix[root][vertex] else arc(pool, vertex, root)
        for vertex in range(N)
        if vertex != root
    ]
    event.extend(arc(pool, tail, head) for tail, head in matching)
    # Deduplicate literals: a matching head's orientation to the root is
    # already present in the exact-neighborhood part of the event.
    return [-literal for literal in dict.fromkeys(event)]


def validate_output(path: Path | None) -> None:
    if path is None:
        return
    if not path.is_absolute() or path.parts[:2] != ("/", "scratch"):
        raise SystemExit("every output must be an absolute path below /scratch")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "case",
        choices=[
            *[f"d6-s{size}" for size in range(3, 6)],
            *[f"d7-s{size}" for size in range(1, 7)],
        ],
    )
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--mode", choices=("all", "regular", "nonregular"), default="all"
    )
    parser.add_argument("--secondary-size", type=int)
    parser.add_argument(
        "--secondary-degree-region", choices=("witness", "neighbors")
    )
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--matchings-per-vertex", type=int, default=64)
    parser.add_argument("--max-iterations", type=int, default=0)
    parser.add_argument("--witness-output", type=Path)
    args = parser.parse_args()
    validate_output(args.output)
    validate_output(args.witness_output)

    cnf, pool = build_base(
        args.case,
        args.mode,
        args.secondary_size,
        args.secondary_degree_region,
    )
    seen_clauses: set[tuple[int, ...]] = set()
    added = 0
    iteration = 0
    with Solver(name=args.solver, bootstrap_with=cnf.clauses) as solver:
        while solver.solve():
            iteration += 1
            matrix = decode_tournament(pool, solver.get_model())
            new_clauses: list[list[int]] = []
            strong_vertices: list[int] = []
            for root in range(N):
                matchings = perfect_matchings(
                    matrix, root, args.matchings_per_vertex
                )
                if matchings:
                    strong_vertices.append(root)
                for matching in matchings:
                    clause = forbid_matching_clause(pool, matrix, root, matching)
                    key = tuple(clause)
                    if key not in seen_clauses:
                        seen_clauses.add(key)
                        new_clauses.append(clause)
            if not strong_vertices:
                if args.witness_output is not None:
                    args.witness_output.write_text(
                        json.dumps(matrix, indent=2) + "\n"
                    )
                print(
                    json.dumps(
                        {
                            "status": "COUNTEREXAMPLE",
                            "iteration": iteration,
                            "degrees": [sum(row) for row in matrix],
                        },
                        sort_keys=True,
                    )
                )
                raise SystemExit(10)
            if not new_clauses:
                raise RuntimeError("strong vertices found but no new clauses generated")
            for clause in new_clauses:
                solver.add_clause(clause)
                cnf.append(clause)
            added += len(new_clauses)
            if iteration <= 10 or iteration % 100 == 0:
                print(
                    json.dumps(
                        {
                            "iteration": iteration,
                            "strong_vertices": strong_vertices,
                            "new_clauses": len(new_clauses),
                            "total_matching_clauses": added,
                        },
                        sort_keys=True,
                    ),
                    flush=True,
                )
            if args.max_iterations and iteration >= args.max_iterations:
                print(json.dumps({"status": "INCOMPLETE", "iteration": iteration}))
                raise SystemExit(2)

    cnf.to_file(args.output)
    print(
        json.dumps(
            {
                "status": "UNSAT",
                "case": args.case,
                "mode": args.mode,
                "secondary_size": args.secondary_size,
                "secondary_degree_region": args.secondary_degree_region,
                "iterations": iteration,
                "variables": pool.top,
                "clauses": len(cnf.clauses),
                "matching_clauses": added,
                "sha256": sha256(args.output),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
