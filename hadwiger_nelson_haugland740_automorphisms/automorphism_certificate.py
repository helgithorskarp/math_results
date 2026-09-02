#!/usr/bin/env python3
"""Build and verify a compact automorphism/CNF-symmetry certificate for Haugland G1."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict, deque
from pathlib import Path


N = 740
M = 3985
COLOURS = 4
TRIANGLE = (0, 13, 42)
ENDPOINTS = (0, 5)
ANCHOR = 1
LEX_PREFIX = 64


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_edge_bytes(edges: list[tuple[int, int]]) -> bytes:
    return "".join(f"{u} {v}\n" for u, v in sorted(edges)).encode()


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    """Return left after right."""
    return tuple(left[right[v]] for v in range(len(left)))


def permutation_order(permutation: tuple[int, ...]) -> int:
    identity = tuple(range(len(permutation)))
    power = identity
    for order in range(1, len(permutation) + 1):
        power = compose(permutation, power)
        if power == identity:
            return order
    raise AssertionError("permutation order exceeds its degree")


def refine_colours(
    adjacency: list[set[int]], colours: list[int]
) -> tuple[list[int], int]:
    """Run deterministic one-dimensional colour refinement to stability."""
    rounds = 0
    while True:
        signatures = [
            (
                colours[v],
                tuple(sorted(Counter(colours[w] for w in adjacency[v]).items())),
            )
            for v in range(len(adjacency))
        ]
        labels = {signature: i for i, signature in enumerate(sorted(set(signatures)))}
        new_colours = [labels[signature] for signature in signatures]
        if new_colours == colours:
            return colours, rounds
        colours = new_colours
        rounds += 1


def cells(colours: list[int]) -> list[list[int]]:
    result: dict[int, list[int]] = defaultdict(list)
    for vertex, colour in enumerate(colours):
        result[colour].append(vertex)
    return [result[colour] for colour in sorted(result)]


def variable(vertex: int, colour: int) -> int:
    return COLOURS * vertex + colour + 1


def base_cnf(edges: list[tuple[int, int]]) -> list[tuple[int, ...]]:
    clauses: list[tuple[int, ...]] = []
    for vertex in range(N):
        clauses.append(tuple(variable(vertex, colour) for colour in range(COLOURS)))
        for colour in range(COLOURS):
            for other in range(colour + 1, COLOURS):
                clauses.append((-variable(vertex, colour), -variable(vertex, other)))
    for u, v in edges:
        for colour in range(COLOURS):
            clauses.append((-variable(u, colour), -variable(v, colour)))
    for colour, vertex in enumerate(TRIANGLE):
        clauses.append((variable(vertex, colour),))
    clauses.append((variable(ENDPOINTS[1], 0),))
    return clauses


def root_assignments(clauses: list[tuple[int, ...]]) -> dict[int, bool]:
    values: dict[int, bool] = {}
    changed = True
    while changed:
        changed = False
        for clause in clauses:
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
                raise AssertionError("root unit propagation found a contradiction")
            if len(undecided) == 1:
                literal = undecided[0]
                atom, wanted = abs(literal), literal > 0
                if atom in values and values[atom] != wanted:
                    raise AssertionError("inconsistent root unit propagation")
                if atom not in values:
                    values[atom] = wanted
                    changed = True
    return values


def variable_symmetry(
    permutation: tuple[int, ...], swap_colours_1_2: bool
) -> dict[int, int]:
    colour_map = (0, 2, 1, 3) if swap_colours_1_2 else (0, 1, 2, 3)
    return {
        variable(vertex, colour): variable(permutation[vertex], colour_map[colour])
        for vertex in range(N)
        for colour in range(COLOURS)
    }


def image_clause(clause: tuple[int, ...], symmetry: dict[int, int]) -> frozenset[int]:
    return frozenset(
        symmetry[abs(literal)] if literal > 0 else -symmetry[abs(literal)]
        for literal in clause
    )


def add_lex_leader(
    clauses: list[tuple[int, ...]],
    symmetry: dict[int, int],
    fixed: dict[int, bool],
    next_variable: int,
) -> int:
    pairs = [
        (atom, symmetry[atom])
        for atom in range(1, COLOURS * N + 1)
        if atom != symmetry[atom]
        and atom not in fixed
        and symmetry[atom] not in fixed
    ][:LEX_PREFIX]
    if len(pairs) != LEX_PREFIX:
        raise AssertionError("too few moved, root-unfixed atoms")
    first_gate = next_variable
    for i, (left, right) in enumerate(pairs):
        gate = None if i == 0 else first_gate + i - 1
        prefix = () if gate is None else (-gate,)
        clauses.append(prefix + (-left, right))
        if i + 1 < len(pairs):
            next_gate = first_gate + i
            clauses.append(prefix + (left, right, next_gate))
            clauses.append(prefix + (-left, -right, next_gate))
            if gate is not None:
                clauses.append((-next_gate, gate))
            clauses.append((-next_gate, -left, right))
            clauses.append((-next_gate, left, -right))
    return first_gate + LEX_PREFIX - 1


def symmetry_cnf(
    edges: list[tuple[int, int]], group: list[tuple[int, ...]]
) -> tuple[list[tuple[int, ...]], int]:
    clauses = base_cnf(edges)
    fixed = root_assignments(clauses)
    identity = tuple(range(N))
    next_variable = COLOURS * N + 1
    for permutation in group:
        if permutation == identity:
            continue
        swap = (permutation[TRIANGLE[1]], permutation[TRIANGLE[2]]) == (
            TRIANGLE[2],
            TRIANGLE[1],
        )
        symmetry = variable_symmetry(permutation, swap)
        next_variable = add_lex_leader(clauses, symmetry, fixed, next_variable)
    return clauses, next_variable - 1


def dimacs_bytes(clauses: list[tuple[int, ...]], variables: int) -> bytes:
    lines = [f"p cnf {variables} {len(clauses)}\n"]
    lines.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(lines).encode()


def load_graph(path: Path) -> tuple[dict, list[tuple[int, int]], list[set[int]]]:
    payload = json.loads(path.read_text())
    if payload["graph_counts"]["G1"] != [N, M]:
        raise AssertionError("unexpected G1 counts")
    edges = [tuple(sorted(map(int, edge))) for edge in payload["G1_edges"]]
    if len(edges) != M or len(set(edges)) != M:
        raise AssertionError("invalid or duplicate G1 edges")
    if any(not (0 <= u < v < N) for u, v in edges):
        raise AssertionError("invalid edge endpoint")
    edges.sort()
    adjacency = [set() for _ in range(N)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    return payload, edges, adjacency


def discover_group(edges: list[tuple[int, int]]) -> list[tuple[int, ...]]:
    """Use pynauty only to discover candidate permutations for the certificate."""
    import pynauty  # Optional build-time dependency; verifier never imports it.

    adjacency = {v: [] for v in range(N)}
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    graph = pynauty.Graph(N, directed=False, adjacency_dict=adjacency)
    generators, size1, size2, _, _ = pynauty.autgrp(graph)
    expected = int(size1 * (10**size2))
    identity = tuple(range(N))
    group = {identity}
    queue = deque([identity])
    while queue:
        current = queue.popleft()
        for generator_list in generators:
            candidate = compose(tuple(generator_list), current)
            if candidate not in group:
                group.add(candidate)
                queue.append(candidate)
    if len(group) != expected:
        raise AssertionError("failed to enumerate discovered group")
    return sorted(group)


def build(graph_path: Path, certificate_path: Path) -> None:
    graph_bytes = graph_path.read_bytes()
    _, edges, _ = load_graph(graph_path)
    group = discover_group(edges)
    clauses, variables = symmetry_cnf(edges, group)
    cnf_bytes = dimacs_bytes(clauses, variables)
    certificate = {
        "graph_sha256": sha256_bytes(graph_bytes),
        "canonical_G1_edges_sha256": sha256_bytes(canonical_edge_bytes(edges)),
        "automorphisms": [list(permutation) for permutation in group],
        "colour_refinement_anchor": ANCHOR,
        "lex_prefix": LEX_PREFIX,
        "symmetry_cnf_variables": variables,
        "symmetry_cnf_clauses": len(clauses),
        "symmetry_cnf_sha256": sha256_bytes(cnf_bytes),
    }
    certificate_path.write_text(json.dumps(certificate, separators=(",", ":")) + "\n")
    print(
        f"built=true automorphisms={len(group)} cnf_variables={variables} "
        f"cnf_clauses={len(clauses)} cnf_sha256={sha256_bytes(cnf_bytes)}"
    )


def verify(graph_path: Path, certificate_path: Path, cnf_path: Path | None) -> None:
    graph_bytes = graph_path.read_bytes()
    certificate = json.loads(certificate_path.read_text())
    _, edges, adjacency = load_graph(graph_path)
    if sha256_bytes(graph_bytes) != certificate["graph_sha256"]:
        raise AssertionError("graph hash mismatch")
    edge_hash = sha256_bytes(canonical_edge_bytes(edges))
    if edge_hash != certificate["canonical_G1_edges_sha256"]:
        raise AssertionError("edge hash mismatch")
    edge_set = set(edges)

    group = [tuple(map(int, row)) for row in certificate["automorphisms"]]
    group_set = set(group)
    identity = tuple(range(N))
    if len(group) != 12 or len(group_set) != 12 or identity not in group_set:
        raise AssertionError("certificate must contain 12 distinct permutations")
    for permutation in group:
        if sorted(permutation) != list(range(N)):
            raise AssertionError("row is not a permutation")
        image_edges = {
            tuple(sorted((permutation[u], permutation[v]))) for u, v in edges
        }
        if image_edges != edge_set:
            raise AssertionError("row is not a graph automorphism")
    for left in group:
        for right in group:
            if compose(left, right) not in group_set:
                raise AssertionError("permutations are not closed under composition")

    order_histogram = Counter(permutation_order(row) for row in group)
    if order_histogram != Counter({1: 1, 2: 3, 3: 2, 6: 6}):
        raise AssertionError(f"unexpected element orders: {order_histogram}")
    if not all(compose(a, b) == compose(b, a) for a in group for b in group):
        raise AssertionError("certificate group is not abelian")

    stable, base_rounds = refine_colours(adjacency, [0] * N)
    stable_cells = cells(stable)
    size_histogram = Counter(map(len, stable_cells))
    if len(stable_cells) != 66 or size_histogram != Counter({12: 60, 2: 4, 6: 2}):
        raise AssertionError("unexpected stable colour-refinement partition")
    anchor_cell = next(cell for cell in stable_cells if ANCHOR in cell)
    if len(anchor_cell) != 12:
        raise AssertionError("anchor stable cell does not have size 12")
    if {permutation[ANCHOR] for permutation in group} != set(anchor_cell):
        raise AssertionError("certified group does not fill the anchor cell")
    group_orbits: list[list[int]] = []
    seen: set[int] = set()
    for vertex in range(N):
        if vertex not in seen:
            orbit = sorted({permutation[vertex] for permutation in group})
            group_orbits.append(orbit)
            seen.update(orbit)
    if sorted(group_orbits) != sorted(stable_cells):
        raise AssertionError("colour-refinement cells do not equal group orbits")
    individualized = list(stable)
    individualized[ANCHOR] = max(stable) + 1
    discrete, individual_rounds = refine_colours(adjacency, individualized)
    if len(set(discrete)) != N:
        raise AssertionError("individualized refinement is not discrete")

    clauses = base_cnf(edges)
    if len(clauses) != 21124:
        raise AssertionError("unexpected base CNF clause count")
    clause_set = {frozenset(clause) for clause in clauses}
    if len(clause_set) != len(clauses):
        raise AssertionError("duplicate base clauses")
    fixed = root_assignments(clauses)
    boolean_group: list[tuple[int, ...]] = []
    for permutation in group:
        endpoint_image = {permutation[v] for v in ENDPOINTS}
        if endpoint_image != set(ENDPOINTS):
            raise AssertionError("endpoint pair is not invariant")
        pair_image = (permutation[TRIANGLE[1]], permutation[TRIANGLE[2]])
        if pair_image == (TRIANGLE[1], TRIANGLE[2]):
            swap = False
        elif pair_image == (TRIANGLE[2], TRIANGLE[1]):
            swap = True
        else:
            raise AssertionError("pinned neighbour pair is not invariant")
        symmetry = variable_symmetry(permutation, swap)
        if any(image_clause(clause, symmetry) not in clause_set for clause in clauses):
            raise AssertionError("base colouring CNF is not invariant")
        if any(
            symmetry[atom] not in fixed or fixed[symmetry[atom]] != value
            for atom, value in fixed.items()
        ):
            raise AssertionError("root assignments are not symmetry-invariant")
        boolean_group.append(
            tuple(symmetry[atom] for atom in range(1, COLOURS * N + 1))
        )
    boolean_group_set = set(boolean_group)
    if len(boolean_group_set) != len(group):
        raise AssertionError("Boolean symmetry action is not faithful")
    for left in boolean_group:
        for right in boolean_group:
            composite = tuple(
                left[right[atom - 1] - 1]
                for atom in range(1, COLOURS * N + 1)
            )
            if composite not in boolean_group_set:
                raise AssertionError("Boolean symmetries are not closed under composition")

    if certificate["lex_prefix"] != LEX_PREFIX:
        raise AssertionError("lex-prefix mismatch")
    symmetry_clauses, variables = symmetry_cnf(edges, group)
    cnf_bytes = dimacs_bytes(symmetry_clauses, variables)
    cnf_hash = sha256_bytes(cnf_bytes)
    if variables != certificate["symmetry_cnf_variables"]:
        raise AssertionError("CNF variable count mismatch")
    if len(symmetry_clauses) != certificate["symmetry_cnf_clauses"]:
        raise AssertionError("CNF clause count mismatch")
    if cnf_hash != certificate["symmetry_cnf_sha256"]:
        raise AssertionError("CNF hash mismatch")
    if cnf_path is not None:
        cnf_path.write_bytes(cnf_bytes)

    print(
        "all_checks=true "
        f"vertices={N} edges={M} automorphism_group_order={len(group)} "
        f"group_isomorphic_to=C6xC2 base_refinement_cells={len(stable_cells)} "
        f"vertex_orbits={len(group_orbits)} "
        f"base_refinement_rounds={base_rounds} anchor_cell_size={len(anchor_cell)} "
        f"individualized_cells={len(set(discrete))} "
        f"individualized_rounds={individual_rounds} "
        f"cnf_variables={variables} cnf_clauses={len(symmetry_clauses)} "
        f"cnf_sha256={cnf_hash}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("graph", type=Path)
    build_parser.add_argument("certificate", type=Path)
    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("graph", type=Path)
    verify_parser.add_argument("certificate", type=Path)
    verify_parser.add_argument("--cnf-out", type=Path)
    args = parser.parse_args()
    if args.command == "build":
        build(args.graph, args.certificate)
    else:
        verify(args.graph, args.certificate, args.cnf_out)


if __name__ == "__main__":
    main()
