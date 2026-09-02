#!/usr/bin/env python3
"""Build colouring CNFs and a directly checkable 5-colouring witness."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pysat.formula import CNF
from pysat.solvers import Solver

import reconstruct


LEX_PAIR_COUNT = 64
COLOUR_INVOLUTION = (0, 2, 1, 3)


def variable(vertex: int, colour: int, colours: int) -> int:
    return colours * vertex + colour + 1


def find_triangle(
    n: int, edges: list[tuple[int, int]], anchor: int | None = None
) -> tuple[int, int, int]:
    adjacency = [set() for _ in range(n)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    anchors = range(n) if anchor is None else (anchor,)
    candidates: list[tuple[int, int, int, int]] = []
    for u in anchors:
        for v in sorted(adjacency[u]):
            for w in sorted(adjacency[u] & adjacency[v]):
                if v < w:
                    candidates.append(
                        (len(adjacency[v]) + len(adjacency[w]), -v, -w, u)
                    )
    if candidates:
        _, minus_v, minus_w, u = max(candidates)
        return u, -minus_v, -minus_w
    raise RuntimeError("graph has no triangle")


def colouring_cnf(
    n: int,
    edges: list[tuple[int, int]],
    colours: int,
    pin_triangle: bool,
    exactly_one: bool = True,
    triangle_anchor: int | None = None,
) -> tuple[CNF, tuple[int, int, int] | None]:
    cnf = CNF()
    for vertex in range(n):
        cnf.append([variable(vertex, colour, colours) for colour in range(colours)])
        if exactly_one:
            for colour in range(colours):
                for other in range(colour + 1, colours):
                    cnf.append(
                        [
                            -variable(vertex, colour, colours),
                            -variable(vertex, other, colours),
                        ]
                    )
    for u, v in edges:
        for colour in range(colours):
            cnf.append(
                [-variable(u, colour, colours), -variable(v, colour, colours)]
            )
    triangle = find_triangle(n, edges, triangle_anchor) if pin_triangle else None
    if triangle is not None:
        for colour, vertex in enumerate(triangle):
            cnf.append([variable(vertex, colour, colours)])
    return cnf, triangle


def decode_colouring(model: list[int], n: int, colours: int) -> list[int]:
    positive = {literal for literal in model if literal > 0}
    answer: list[int] = []
    for vertex in range(n):
        selected = [
            colour
            for colour in range(colours)
            if variable(vertex, colour, colours) in positive
        ]
        if len(selected) != 1:
            raise AssertionError(f"vertex {vertex} has selected colours {selected}")
        answer.append(selected[0])
    return answer


def check_colouring(colouring: list[int], edges: list[tuple[int, int]], colours: int) -> None:
    if not all(0 <= value < colours for value in colouring):
        raise AssertionError("colour outside range")
    for u, v in edges:
        if colouring[u] == colouring[v]:
            raise AssertionError(f"monochromatic edge {(u, v)}")


def halfturn_vertex_permutation(points, sqrt3) -> list[int]:
    index = {point: vertex for vertex, point in enumerate(points)}
    permutation = [index[(-x, sqrt3 - y)] for x, y in points]
    if any(permutation[permutation[v]] != v for v in range(len(points))):
        raise AssertionError("half-turn map is not an involution")
    return permutation


def variable_involution(
    vertex_permutation: list[int], colours: int = 4
) -> dict[int, int]:
    if colours != len(COLOUR_INVOLUTION):
        raise ValueError("the checked colour involution is defined only for four colours")
    return {
        variable(vertex, colour, colours): variable(
            vertex_permutation[vertex], COLOUR_INVOLUTION[colour], colours
        )
        for vertex in range(len(vertex_permutation))
        for colour in range(colours)
    }


def check_cnf_involution(cnf: CNF, involution: dict[int, int]) -> None:
    clauses = {frozenset(clause) for clause in cnf.clauses}
    if len(clauses) != len(cnf.clauses):
        raise AssertionError("base CNF contains duplicate clauses")
    for clause in clauses:
        image = frozenset(
            involution[abs(literal)] if literal > 0 else -involution[abs(literal)]
            for literal in clause
        )
        if image not in clauses:
            raise AssertionError(f"CNF involution fails on clause {sorted(clause)}")


def root_assignments(cnf: CNF) -> dict[int, bool]:
    """Return the deterministic fixed point of plain root unit propagation."""
    values: dict[int, bool] = {}
    changed = True
    while changed:
        changed = False
        for clause in cnf.clauses:
            undecided: list[int] = []
            satisfied = False
            for literal in clause:
                atom = abs(literal)
                if atom in values:
                    if values[atom] == (literal > 0):
                        satisfied = True
                        break
                else:
                    undecided.append(literal)
            if satisfied:
                continue
            if not undecided:
                raise AssertionError("base CNF contradicts itself under root propagation")
            if len(undecided) == 1:
                literal = undecided[0]
                atom, wanted = abs(literal), literal > 0
                if atom in values and values[atom] != wanted:
                    raise AssertionError("inconsistent root unit assignments")
                if atom not in values:
                    values[atom] = wanted
                    changed = True
    return values


def add_prefix_lex_leader(
    cnf: CNF, involution: dict[int, int], pair_count: int = LEX_PAIR_COUNT
) -> list[tuple[int, int]]:
    """Orient a prefix of Boolean transpositions under an involutive symmetry."""
    original_variables = cnf.nv
    fixed = root_assignments(cnf)
    pairs = [
        (atom, involution[atom])
        for atom in range(1, original_variables + 1)
        if atom < involution[atom]
        and atom not in fixed
        and involution[atom] not in fixed
    ][:pair_count]
    if len(pairs) != pair_count:
        raise AssertionError("too few unfixed variable pairs for the lex leader")

    # e_i (i >= 1) says that pairs before i were equal.  e_0 is true
    # implicitly.  If a prefix is equal, the next pair may not be (1,0),
    # and equality forces the next prefix flag.  Once a pair is (0,1), the
    # remaining flags may be false and the rest of the assignment is free.
    for i, (left, right) in enumerate(pairs):
        gate = None if i == 0 else original_variables + i
        prefix = [] if gate is None else [-gate]
        cnf.append(prefix + [-left, right])
        if i + 1 < len(pairs):
            next_gate = original_variables + i + 1
            cnf.append(prefix + [left, right, next_gate])
            cnf.append(prefix + [-left, -right, next_gate])
    return pairs


def endpoint_forcing_cnf(
    payload: dict, g1_points, sqrt3
) -> tuple[CNF, tuple[int, int, int], list[tuple[int, int]]]:
    edges = [tuple(edge) for edge in payload["G1_edges"]]
    n = payload["graph_counts"]["G1"][0]
    endpoint_a, endpoint_b = payload["G1_endpoints"]
    cnf, triangle = colouring_cnf(
        n,
        edges,
        4,
        True,
        exactly_one=True,
        triangle_anchor=endpoint_a,
    )
    assert triangle is not None
    cnf.append([variable(endpoint_b, 0, 4)])
    permutation = halfturn_vertex_permutation(g1_points, sqrt3)
    involution = variable_involution(permutation)
    check_cnf_involution(cnf, involution)
    pairs = add_prefix_lex_leader(cnf, involution)
    return cnf, triangle, pairs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=Path)
    parser.add_argument("cnf4", type=Path)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.graph.read_text())
    field = reconstruct.Cyclotomic84()
    g1_points, _ = reconstruct.build_g1(
        payload["paths"], field.unit_vectors(), field.float_vectors(), field
    )
    endpoint_a, endpoint_b = payload["G1_endpoints"]
    cnf4, triangle, lex_pairs = endpoint_forcing_cnf(
        payload, g1_points, field.sqrt3
    )
    if triangle is None or triangle[0] != endpoint_a:
        raise AssertionError("canonical triangle must start at endpoint A")
    cnf4.to_file(args.cnf4)
    print(
        f"G1_equal_endpoint_four_colour_cnf variables={cnf4.nv} "
        f"clauses={len(cnf4.clauses)} triangle={triangle} "
        f"endpoints=({endpoint_a},{endpoint_b}) lex_pairs={len(lex_pairs)}"
    )

    edges = [tuple(edge) for edge in payload["G3_edges"]]
    n = payload["graph_counts"]["G3"][0]
    cnf5, _ = colouring_cnf(n, edges, 5, False)
    with Solver(name="cadical195", bootstrap_with=cnf5.clauses) as solver:
        if not solver.solve():
            raise AssertionError("unexpectedly failed to find a 5-colouring")
        colouring = decode_colouring(solver.get_model(), n, 5)
    check_colouring(colouring, edges, 5)
    certificate = {
        "vertices": n,
        "edges": len(edges),
        "G1_four_colour_triangle_pin": triangle,
        "G1_forced_different_endpoints": [endpoint_a, endpoint_b],
        "G1_halfturn_colour_involution": list(COLOUR_INVOLUTION),
        "G1_prefix_lex_pairs": len(lex_pairs),
        "five_colouring": colouring,
    }
    args.certificate.write_text(json.dumps(certificate, separators=(",", ":")) + "\n")
    print(f"five_colouring_verified=true certificate={args.certificate}")


if __name__ == "__main__":
    main()
