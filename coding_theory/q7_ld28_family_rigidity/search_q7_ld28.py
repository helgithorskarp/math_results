#!/usr/bin/env python3
"""Exact SAT search for a 28-word locating-dominating code in Q_7.

The four branches normalize a codeword of minimum induced degree.  Unlike the
earlier baseline formulation, branch ``r`` also states the resulting global
fact that every selected vertex has at least ``r`` selected cube neighbours.
Solver inputs and proof logs, when requested, must be written under /scratch.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import pathlib
import time

from pysat.card import CardEnc, EncType
from pysat.formula import CNF
from pysat.solvers import Solver


DIMENSION = 7
VERTEX_COUNT = 1 << DIMENSION
NEIGHBORS = tuple(
    tuple(vertex ^ (1 << coordinate) for coordinate in range(DIMENSION))
    for vertex in range(VERTEX_COUNT)
)
CLOSED_NEIGHBORHOODS = tuple(
    frozenset({vertex, *NEIGHBORS[vertex]}) for vertex in range(VERTEX_COUNT)
)


def add_minimum_degree_constraints(cnf: CNF, minimum_degree: int) -> None:
    """Require every selected vertex to have selected degree at least r."""
    if minimum_degree == 0:
        return
    clause_size = DIMENSION - minimum_degree + 1
    for vertex in range(VERTEX_COUNT):
        for subset in itertools.combinations(NEIGHBORS[vertex], clause_size):
            # x_v -> sum_{u in N(v)} x_u >= minimum_degree.
            cnf.append([-(vertex + 1), *(neighbor + 1 for neighbor in subset)])


def swap_coordinates(vertex: int, first: int, second: int) -> int:
    """Apply one coordinate transposition to a cube vertex."""
    first_bit = (vertex >> first) & 1
    second_bit = (vertex >> second) & 1
    if first_bit == second_bit:
        return vertex
    return vertex ^ (1 << first) ^ (1 << second)


def add_lex_constraint(cnf: CNF, first: int, second: int) -> None:
    """Require x <=lex g(x) for a coordinate transposition g."""
    prefix: int | None = None
    moved_positions = [
        vertex
        for vertex in range(VERTEX_COUNT)
        if swap_coordinates(vertex, first, second) != vertex
    ]
    for index, vertex in enumerate(moved_positions):
        image = swap_coordinates(vertex, first, second)
        left = vertex + 1
        right = image + 1

        # If the earlier entries agree, forbid the first difference 1 > 0.
        if prefix is None:
            cnf.append([-left, right])
        else:
            cnf.append([-prefix, -left, right])

        if index == len(moved_positions) - 1:
            continue
        next_prefix = cnf.nv + 1
        if prefix is None:
            # next_prefix <-> (left <-> right).
            cnf.append([-next_prefix, -left, right])
            cnf.append([-next_prefix, left, -right])
            cnf.append([left, right, next_prefix])
            cnf.append([-left, -right, next_prefix])
        else:
            # next_prefix <-> prefix and (left <-> right).
            cnf.append([-next_prefix, prefix])
            cnf.append([-next_prefix, -left, right])
            cnf.append([-next_prefix, left, -right])
            cnf.append([-prefix, left, right, next_prefix])
            cnf.append([-prefix, -left, -right, next_prefix])
        prefix = next_prefix


def add_stabilizer_generator_lex_constraints(cnf: CNF, branch: int) -> None:
    """Break adjacent-swap symmetries stabilizing the normalized origin."""
    blocks = (range(branch), range(branch, DIMENSION))
    for block in blocks:
        coordinates = list(block)
        for first, second in zip(coordinates, coordinates[1:], strict=False):
            add_lex_constraint(cnf, first, second)


def add_redundant_edge_bounds(
    cnf: CNF, branch: int, *, isolated_bound: bool
) -> None:
    """Expose the exact global induced-edge bounds to the SAT solver."""
    edge_variables: list[int] = []
    for first in range(VERTEX_COUNT):
        for second in NEIGHBORS[first]:
            if first >= second:
                continue
            edge = cnf.nv + 1
            edge_variables.append(edge)
            left = first + 1
            right = second + 1
            # edge <-> x_first and x_second.
            cnf.append([-edge, left])
            cnf.append([-edge, right])
            cnf.append([edge, -left, -right])
    assert len(edge_variables) == DIMENSION * VERTEX_COUNT // 2 == 448

    # Every one of the 100 non-codewords needs a code neighbour, so the
    # code/non-code boundary 7*28 - 2e is at least 100: e <= 48.  With at
    # least 22 isolated codewords, all edges lie on at most six vertices; the
    # cube edge-isoperimetric bound e(S) <= |S|log_2(|S|)/2 improves this to 7.
    upper = CardEnc.atmost(
        lits=edge_variables,
        bound=7 if isolated_bound else 48,
        top_id=cnf.nv,
        encoding=EncType.totalizer,
    )
    cnf.extend(upper.clauses)

    # Minimum code degree r gives 2e >= 28r.
    if branch:
        lower = CardEnc.atleast(
            lits=edge_variables,
            bound=14 * branch,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        )
        cnf.extend(lower.clauses)


def add_isolated_codeword_bound(cnf: CNF) -> list[int]:
    """Require the family-count consequence: at least 22 isolated codewords."""
    nonisolated_variables: list[int] = []
    for vertex in range(VERTEX_COUNT):
        nonisolated = cnf.nv + 1
        nonisolated_variables.append(nonisolated)
        selected = vertex + 1
        neighbors = [neighbor + 1 for neighbor in NEIGHBORS[vertex]]
        # nonisolated <-> selected and some selected cube neighbour.
        cnf.append([-nonisolated, selected])
        cnf.append([-nonisolated, *neighbors])
        for neighbor in neighbors:
            cnf.append([-selected, -neighbor, nonisolated])
    upper = CardEnc.atmost(
        lits=nonisolated_variables,
        bound=6,
        top_id=cnf.nv,
        encoding=EncType.totalizer,
    )
    cnf.extend(upper.clauses)
    return nonisolated_variables


def add_singleton_signature_bound(cnf: CNF) -> list[int]:
    """Require at least 50 vertices with a singleton identifying set."""
    singleton_variables: list[int] = []
    for vertex in range(VERTEX_COUNT):
        singleton = cnf.nv + 1
        singleton_variables.append(singleton)
        neighborhood = [
            word + 1 for word in sorted(CLOSED_NEIGHBORHOODS[vertex])
        ]
        # singleton -> exactly one selected word in N[vertex].
        cnf.append([-singleton, *neighborhood])
        for first, second in itertools.combinations(neighborhood, 2):
            cnf.append([-singleton, -first, -second])
        # Every possible exactly-one pattern implies singleton.
        for selected in neighborhood:
            others = [word for word in neighborhood if word != selected]
            cnf.append([-selected, *others, singleton])
    lower = CardEnc.atleast(
        lits=singleton_variables,
        bound=50,
        top_id=cnf.nv,
        encoding=EncType.totalizer,
    )
    cnf.extend(lower.clauses)
    upper = CardEnc.atmost(
        lits=singleton_variables,
        bound=56,
        top_id=cnf.nv,
        encoding=EncType.totalizer,
    )
    cnf.extend(upper.clauses)
    return singleton_variables


def add_distance_two_pair_bound(cnf: CNF) -> None:
    """Require at least 44 selected pairs at Hamming distance two."""
    pair_variables: list[int] = []
    for first in range(VERTEX_COUNT):
        for second in range(first + 1, VERTEX_COUNT):
            if (first ^ second).bit_count() != 2:
                continue
            pair = cnf.nv + 1
            pair_variables.append(pair)
            left = first + 1
            right = second + 1
            cnf.append([-pair, left])
            cnf.append([-pair, right])
            cnf.append([pair, -left, -right])
    assert len(pair_variables) == 1344
    lower = CardEnc.atleast(
        lits=pair_variables,
        bound=44,
        top_id=cnf.nv,
        encoding=EncType.totalizer,
    )
    cnf.extend(lower.clauses)


def build(
    branch: int,
    *,
    all_pair_clauses: bool,
    lex_generators: bool,
    edge_bounds: bool,
    isolated_bound: bool,
    singleton_bound: bool,
    distance_two_bound: bool,
) -> CNF:
    """Build one lossless minimum-degree branch at exact cardinality 28."""
    cnf = CNF()

    # Domination.
    for vertex in range(VERTEX_COUNT):
        cnf.append(
            [word + 1 for word in sorted(CLOSED_NEIGHBORHOODS[vertex])]
        )

    # If two non-codewords have equal nonempty signatures, their closed
    # neighborhoods intersect, hence their distance is at most two.  Adjacent
    # non-codewords have intersection {u,v}, which contains no codeword.
    # Therefore only distance-two pairs need explicit separation clauses.
    for first in range(VERTEX_COUNT):
        for second in range(first + 1, VERTEX_COUNT):
            if not all_pair_clauses and (first ^ second).bit_count() != 2:
                continue
            witnesses = sorted(
                CLOSED_NEIGHBORHOODS[first]
                ^ CLOSED_NEIGHBORHOODS[second]
            )
            cnf.append(
                [first + 1, second + 1, *(word + 1 for word in witnesses)]
            )

    cardinality = CardEnc.equals(
        lits=list(range(1, VERTEX_COUNT + 1)),
        bound=28,
        top_id=cnf.nv,
        encoding=EncType.totalizer,
    )
    cnf.extend(cardinality.clauses)

    # Translate a minimum-induced-degree codeword to zero.  The incidence
    # bound gives delta(Q_7[C]) <= floor(8 - 128/28) = 3.  Coordinate
    # permutations make its exact neighbour set {e_0,...,e_{branch-1}}.
    cnf.append([1])
    for coordinate in range(DIMENSION):
        variable = (1 << coordinate) + 1
        cnf.append([variable if coordinate < branch else -variable])

    # Since zero was chosen to have minimum induced degree, every codeword has
    # induced degree at least the branch value.
    add_minimum_degree_constraints(cnf, branch)
    if lex_generators:
        add_stabilizer_generator_lex_constraints(cnf, branch)
    if edge_bounds:
        add_redundant_edge_bounds(
            cnf, branch, isolated_bound=isolated_bound
        )
    nonisolated_variables: list[int] | None = None
    singleton_variables: list[int] | None = None
    if isolated_bound:
        if branch != 0:
            raise ValueError("the isolated-codeword reduction leaves only branch 0")
        nonisolated_variables = add_isolated_codeword_bound(cnf)
    if singleton_bound:
        if branch != 0:
            raise ValueError("the family-count reduction leaves only branch 0")
        singleton_variables = add_singleton_signature_bound(cnf)
    if nonisolated_variables is not None and singleton_variables is not None:
        # If b codewords are non-isolated, at most 28-b codewords themselves
        # have singleton signatures, in addition to at most 28 singleton
        # signatures on non-codewords.  Thus p+b <= 56.
        joint = CardEnc.atmost(
            lits=[*nonisolated_variables, *singleton_variables],
            bound=56,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        )
        cnf.extend(joint.clauses)
    if distance_two_bound:
        add_distance_two_pair_bound(cnf)
    return cnf


def dimacs_bytes(cnf: CNF) -> bytes:
    lines = [f"p cnf {cnf.nv} {len(cnf.clauses)}"]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in cnf.clauses)
    return ("\n".join(lines) + "\n").encode("ascii")


def scratch_path(raw_path: str) -> pathlib.Path:
    path = pathlib.Path(raw_path).resolve()
    if not path.is_relative_to("/scratch"):
        raise ValueError("generated solver artifacts must stay under /scratch")
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("branch", type=int, choices=range(4))
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument(
        "--all-pair-clauses",
        action="store_true",
        help="also emit pair clauses entailed by domination",
    )
    parser.add_argument(
        "--lex-generators",
        action="store_true",
        help="break adjacent-coordinate symmetries stabilizing the branch",
    )
    parser.add_argument(
        "--edge-bounds",
        action="store_true",
        help="add redundant induced-edge cardinality bounds",
    )
    parser.add_argument(
        "--isolated-bound",
        action="store_true",
        help="use the proved lower bound of 22 isolated codewords",
    )
    parser.add_argument(
        "--singleton-bound",
        action="store_true",
        help="use the proved lower bound of 50 singleton signatures",
    )
    parser.add_argument(
        "--distance-two-bound",
        action="store_true",
        help="use the proved lower bound of 44 distance-two code pairs",
    )
    parser.add_argument("--write-cnf", metavar="SCRATCH_PATH")
    parser.add_argument("--proof", metavar="SCRATCH_PATH")
    args = parser.parse_args()

    started = time.monotonic()
    cnf = build(
        args.branch,
        all_pair_clauses=args.all_pair_clauses,
        lex_generators=args.lex_generators,
        edge_bounds=args.edge_bounds,
        isolated_bound=args.isolated_bound,
        singleton_bound=args.singleton_bound,
        distance_two_bound=args.distance_two_bound,
    )
    payload = dimacs_bytes(cnf)
    digest = hashlib.sha256(payload).hexdigest()
    print(
        f"branch {args.branch}: {cnf.nv} variables, {len(cnf.clauses)} clauses, "
        f"sha256 {digest}",
        flush=True,
    )
    if args.write_cnf:
        scratch_path(args.write_cnf).write_bytes(payload)
    print(f"built in {time.monotonic() - started:.3f}s", flush=True)

    solve_started = time.monotonic()
    with Solver(
        name=args.solver,
        bootstrap_with=cnf.clauses,
        with_proof=bool(args.proof),
    ) as solver:
        satisfiable = solver.solve()
        model = solver.get_model() if satisfiable else None
        proof = solver.get_proof() if args.proof and not satisfiable else None
    print(
        f"{args.solver}: {'SAT' if satisfiable else 'UNSAT'} "
        f"in {time.monotonic() - solve_started:.3f}s",
        flush=True,
    )

    if model is not None:
        positive = {literal for literal in model if literal > 0}
        code = [
            vertex
            for vertex in range(VERTEX_COUNT)
            if vertex + 1 in positive
        ]
        print("code:", " ".join(f"{vertex:07b}" for vertex in code))
    if args.proof and proof is not None:
        proof_path = scratch_path(args.proof)
        proof_path.write_text("\n".join(proof) + "\n", encoding="ascii")
        print(
            f"proof lines: {len(proof)}; sha256 "
            f"{hashlib.sha256(proof_path.read_bytes()).hexdigest()}"
        )


if __name__ == "__main__":
    main()
