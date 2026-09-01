#!/usr/bin/env python3
"""Exact SAT encoding for the size-at-most-29 LD-code question in Q_7.

The family-excess theorem in the accompanying README makes the fixed
normalization lossless: zero is an isolated codeword, e_0 is its orphan, and
all other unit vectors and all weight-two words containing coordinate zero
are non-codewords.  Generated CNF and proof files are restricted to /scratch.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import pathlib
import time

from pysat.card import CardEnc, EncType
from pysat.formula import CNF
from pysat.pb import PBEnc
from pysat.solvers import Solver

from local_graphs import local_graph_assumptions, local_graph_representatives


DIMENSION = 7
VERTEX_COUNT = 1 << DIMENSION
NEIGHBORS = tuple(
    tuple(vertex ^ (1 << coordinate) for coordinate in range(DIMENSION))
    for vertex in range(VERTEX_COUNT)
)
BALLS = tuple(
    frozenset({vertex, *NEIGHBORS[vertex]})
    for vertex in range(VERTEX_COUNT)
)


def swap_coordinates(vertex: int, first: int, second: int) -> int:
    """Apply a coordinate transposition to a cube vertex."""
    if ((vertex >> first) & 1) == ((vertex >> second) & 1):
        return vertex
    return vertex ^ (1 << first) ^ (1 << second)


def add_lex_constraint(cnf: CNF, first: int, second: int) -> None:
    """Require the code incidence vector x to satisfy x <=lex swap(x)."""
    prefix: int | None = None
    moved = [
        vertex
        for vertex in range(VERTEX_COUNT)
        if swap_coordinates(vertex, first, second) != vertex
    ]
    for index, vertex in enumerate(moved):
        image = swap_coordinates(vertex, first, second)
        left, right = vertex + 1, image + 1
        if prefix is None:
            cnf.append([-left, right])
        else:
            cnf.append([-prefix, -left, right])
        if index == len(moved) - 1:
            continue
        next_prefix = cnf.nv + 1
        if prefix is None:
            cnf.append([-next_prefix, -left, right])
            cnf.append([-next_prefix, left, -right])
            cnf.append([left, right, next_prefix])
            cnf.append([-left, -right, next_prefix])
        else:
            cnf.append([-next_prefix, prefix])
            cnf.append([-next_prefix, -left, right])
            cnf.append([-next_prefix, left, -right])
            cnf.append([-prefix, left, right, next_prefix])
            cnf.append([-prefix, -left, -right, next_prefix])
        prefix = next_prefix


def add_stabilizer_lex_constraints(cnf: CNF) -> None:
    """Break adjacent-swap symmetries among coordinates 1,...,6."""
    for first in range(1, DIMENSION - 1):
        add_lex_constraint(cnf, first, first + 1)


def add_nonisolated_variables(cnf: CNF) -> list[int]:
    """Return indicators for selected vertices with a selected neighbor."""
    result: list[int] = []
    for vertex in range(VERTEX_COUNT):
        indicator = cnf.nv + 1
        result.append(indicator)
        selected = vertex + 1
        neighbor_lits = [neighbor + 1 for neighbor in NEIGHBORS[vertex]]
        cnf.append([-indicator, selected])
        cnf.append([-indicator, *neighbor_lits])
        for neighbor in neighbor_lits:
            cnf.append([-selected, -neighbor, indicator])
    return result


def add_singleton_variables(cnf: CNF) -> list[int]:
    """Return indicators for vertices whose identifying set has size one."""
    result: list[int] = []
    for vertex in range(VERTEX_COUNT):
        indicator = cnf.nv + 1
        result.append(indicator)
        ball = [word + 1 for word in sorted(BALLS[vertex])]
        cnf.append([-indicator, *ball])
        for first, second in itertools.combinations(ball, 2):
            cnf.append([-indicator, -first, -second])
        for selected in ball:
            others = [word for word in ball if word != selected]
            cnf.append([-selected, *others, indicator])
    return result


def add_pair_indicators(cnf: CNF, distance: int) -> list[int]:
    """Return conjunction indicators for selected pairs at one distance."""
    result: list[int] = []
    for first, second in itertools.combinations(range(VERTEX_COUNT), 2):
        if (first ^ second).bit_count() != distance:
            continue
        indicator = cnf.nv + 1
        result.append(indicator)
        left, right = first + 1, second + 1
        cnf.append([-indicator, left])
        cnf.append([-indicator, right])
        cnf.append([indicator, -left, -right])
    return result


def build(
    *,
    lex: bool,
    structural: bool,
    pair_bounds: bool,
    dynamic_pair_bound: bool,
) -> CNF:
    """Build a lossless exact-cardinality-29 encoding."""
    cnf = CNF()

    for vertex in range(VERTEX_COUNT):
        cnf.append([word + 1 for word in sorted(BALLS[vertex])])

    # Domination makes separation automatic at distances other than two.
    for first, second in itertools.combinations(range(VERTEX_COUNT), 2):
        if (first ^ second).bit_count() != 2:
            continue
        witnesses = sorted(BALLS[first] ^ BALLS[second])
        cnf.append(
            [first + 1, second + 1, *(word + 1 for word in witnesses)]
        )

    cardinality = CardEnc.equals(
        lits=list(range(1, VERTEX_COUNT + 1)),
        bound=29,
        top_id=cnf.nv,
        encoding=EncType.totalizer,
    )
    cnf.extend(cardinality.clauses)

    # Zero is an isolated codeword and e_0 is an orphan with signature {0}.
    cnf.append([1])
    for coordinate in range(DIMENSION):
        cnf.append([-((1 << coordinate) + 1)])
    for coordinate in range(1, DIMENSION):
        cnf.append([-((1 | (1 << coordinate)) + 1)])

    if lex:
        add_stabilizer_lex_constraints(cnf)
    if not structural:
        return cnf

    nonisolated = add_nonisolated_variables(cnf)
    singleton = add_singleton_variables(cnf)
    edges = add_pair_indicators(cnf, 1)
    distance_two_pairs = add_pair_indicators(cnf, 2) if pair_bounds else []

    cnf.extend(
        CardEnc.atmost(
            lits=nonisolated,
            bound=17,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend(
        CardEnc.atleast(
            lits=singleton,
            bound=41,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    # If b codewords are nonisolated and p signatures are singleton, then
    # p+b <= 58 because at most 29 singleton signatures are on non-codewords.
    cnf.extend(
        CardEnc.atmost(
            lits=[*nonisolated, *singleton],
            bound=58,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend(
        CardEnc.atmost(
            lits=edges,
            bound=33,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    if pair_bounds:
        cnf.extend(
            CardEnc.atleast(
                lits=distance_two_pairs,
                bound=24,
                top_id=cnf.nv,
                encoding=EncType.totalizer,
            ).clauses
        )
    if pair_bounds and dynamic_pair_bound:
        # A_2 >= 2p-58 is equivalent to A_2+2(128-p) >= 198.
        dynamic = PBEnc.atleast(
            lits=[*distance_two_pairs, *(-literal for literal in singleton)],
            weights=[*[1] * len(distance_two_pairs), *[2] * len(singleton)],
            bound=198,
            top_id=cnf.nv,
        )
        cnf.extend(dynamic.clauses)
    return cnf


def dimacs_bytes(cnf: CNF) -> bytes:
    lines = [f"p cnf {cnf.nv} {len(cnf.clauses)}"]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in cnf.clauses)
    return ("\n".join(lines) + "\n").encode("ascii")


def scratch_path(raw: str) -> pathlib.Path:
    path = pathlib.Path(raw).resolve()
    if not path.is_relative_to("/scratch"):
        raise ValueError("solver artifacts must stay under /scratch")
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--no-lex", action="store_true")
    parser.add_argument("--no-structural", action="store_true")
    parser.add_argument("--no-pair-bounds", action="store_true")
    parser.add_argument("--no-dynamic-pair-bound", action="store_true")
    parser.add_argument(
        "--local-graph-index",
        type=int,
        help="fix one of the canonical local graphs numbered from zero",
    )
    parser.add_argument("--build-only", action="store_true")
    parser.add_argument("--write-cnf", metavar="SCRATCH_PATH")
    args = parser.parse_args()

    started = time.monotonic()
    cnf = build(
        lex=not args.no_lex and args.local_graph_index is None,
        structural=not args.no_structural,
        pair_bounds=not args.no_pair_bounds,
        dynamic_pair_bound=not args.no_dynamic_pair_bound,
    )
    if args.local_graph_index is not None:
        representatives = local_graph_representatives()
        if not 0 <= args.local_graph_index < len(representatives):
            raise ValueError(
                f"local graph index must be in 0..{len(representatives)-1}"
            )
        local_mask = representatives[args.local_graph_index]
        cnf.extend(
            [[literal] for literal in local_graph_assumptions(local_mask)]
        )
        print(
            f"local_graph={args.local_graph_index}/{len(representatives)} "
            f"edges={local_mask.bit_count()} mask={local_mask}",
            flush=True,
        )
    payload = dimacs_bytes(cnf)
    print(
        f"variables={cnf.nv} clauses={len(cnf.clauses)} "
        f"sha256={hashlib.sha256(payload).hexdigest()}",
        flush=True,
    )
    if args.write_cnf:
        scratch_path(args.write_cnf).write_bytes(payload)
    print(f"built_seconds={time.monotonic() - started:.3f}", flush=True)
    if args.build_only:
        return

    solve_started = time.monotonic()
    with Solver(
        name=args.solver,
        bootstrap_with=cnf.clauses,
    ) as solver:
        satisfiable = solver.solve()
        model = solver.get_model() if satisfiable else None
    print(
        f"{args.solver}={'SAT' if satisfiable else 'UNSAT'} "
        f"solve_seconds={time.monotonic() - solve_started:.3f}",
        flush=True,
    )
    if model is not None:
        positive = {literal for literal in model if literal > 0}
        code = [v for v in range(VERTEX_COUNT) if v + 1 in positive]
        print("code:", " ".join(f"{vertex:07b}" for vertex in code))


if __name__ == "__main__":
    main()
