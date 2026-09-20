#!/usr/bin/env python3
"""Independent audit of the order-28 K4-free 7-chromatic Cayley graph.

This file imports no code or certificate from the submitted package.  It uses
an i-major vertex labelling, enumerates maximal independent sets with
Bron--Kerbosch on the complement, checks every four-class residual directly,
and separately runs an exact DSATUR colouring search.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, deque
from pathlib import Path


VERTICES = tuple((i, j) for i in range(7) for j in range(4))
INDEX = {vertex: i for i, vertex in enumerate(VERTICES)}
N = len(VERTICES)
ALL = (1 << N) - 1
IDENTITY = (0, 0)
GENERATORS = frozenset(
    {
        (2, 0),
        (5, 0),
        (3, 0),
        (4, 0),
        (0, 1),
        (0, 3),
        (1, 1),
        (1, 3),
        (3, 1),
        (3, 3),
        (1, 2),
        (6, 2),
    }
)

SEVEN_COLOURING = (
    ((0, 0), (1, 0), (5, 1), (3, 2), (5, 3)),
    ((2, 0), (3, 0), (0, 1), (1, 1)),
    ((4, 0), (5, 0), (2, 1), (0, 2), (2, 3)),
    ((6, 0), (4, 1), (6, 2), (4, 3)),
    ((6, 1), (1, 2), (2, 2), (6, 3)),
    ((3, 1), (4, 2), (5, 2), (3, 3)),
    ((0, 3), (1, 3)),
)


def multiply(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    i, j = x
    k, ell = y
    sign = -1 if j % 2 else 1
    return (i + sign * k) % 7, (j + ell) % 4


def inverse(x: tuple[int, int]) -> tuple[int, int]:
    i, j = x
    sign = -1 if j % 2 else 1
    return (-sign * i) % 7, (-j) % 4


def cayley_graph() -> tuple[tuple[int, ...], tuple[int, ...]]:
    edges = set()
    for x in VERTICES:
        for s in GENERATORS:
            y = multiply(x, s)
            u, v = sorted((INDEX[x], INDEX[y]))
            assert u != v
            edges.add((u, v))
    rows = [0] * N
    for u, v in edges:
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    encoded_edges = tuple((u << 8) | v for u, v in sorted(edges))
    return tuple(rows), encoded_edges


ADJ, ENCODED_EDGES = cayley_graph()


def edge_pairs() -> list[tuple[int, int]]:
    return [(code >> 8, code & 255) for code in ENCODED_EDGES]


def digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def is_independent(mask: int, adjacency: tuple[int, ...] = ADJ) -> bool:
    todo = mask
    while todo:
        bit = todo & -todo
        vertex = bit.bit_length() - 1
        if adjacency[vertex] & mask:
            return False
        todo ^= bit
    return True


def k4_count(adjacency: tuple[int, ...]) -> int:
    total = 0
    for a, b, c, d in itertools.combinations(range(len(adjacency)), 4):
        vertices = (a, b, c, d)
        if all((adjacency[u] >> v) & 1 for u, v in itertools.combinations(vertices, 2)):
            total += 1
    return total


def maximal_cliques(adjacency: tuple[int, ...]) -> list[int]:
    """Enumerate maximal cliques exactly with pivoted Bron--Kerbosch."""
    size = len(adjacency)
    all_vertices = (1 << size) - 1
    result: list[int] = []

    def visit(chosen: int, possible: int, excluded: int) -> None:
        if not possible and not excluded:
            result.append(chosen)
            return
        union = possible | excluded
        if union:
            pivot = max(
                (v for v in range(size) if (union >> v) & 1),
                key=lambda v: (possible & adjacency[v]).bit_count(),
            )
            candidates = possible & ~adjacency[pivot] & all_vertices
        else:
            candidates = possible
        while candidates:
            bit = candidates & -candidates
            vertex = bit.bit_length() - 1
            visit(
                chosen | bit,
                possible & adjacency[vertex],
                excluded & adjacency[vertex],
            )
            possible ^= bit
            excluded |= bit
            candidates ^= bit

    visit(0, all_vertices, 0)
    assert len(result) == len(set(result))
    return sorted(result)


def complement(adjacency: tuple[int, ...]) -> tuple[int, ...]:
    all_vertices = (1 << len(adjacency)) - 1
    return tuple(all_vertices & ~(row | (1 << v)) for v, row in enumerate(adjacency))


def induced_bipartite(mask: int, adjacency: tuple[int, ...] = ADJ) -> bool:
    colours: dict[int, int] = {}
    unseen = {v for v in range(len(adjacency)) if (mask >> v) & 1}
    while unseen:
        root = min(unseen)
        colours[root] = 0
        queue = deque([root])
        unseen.remove(root)
        while queue:
            u = queue.popleft()
            neighbors = adjacency[u] & mask
            while neighbors:
                bit = neighbors & -neighbors
                v = bit.bit_length() - 1
                neighbors ^= bit
                if v not in colours:
                    colours[v] = 1 - colours[u]
                    unseen.discard(v)
                    queue.append(v)
                elif colours[v] == colours[u]:
                    return False
    return True


def has_cycle(mask: int, length: int, adjacency: tuple[int, ...] = ADJ) -> bool:
    vertices = [v for v in range(len(adjacency)) if (mask >> v) & 1]
    for subset in itertools.combinations(vertices, length):
        start = min(subset)
        others = tuple(v for v in subset if v != start)
        for route in itertools.permutations(others):
            cycle = (start,) + route
            if cycle[1] > cycle[-1]:
                continue
            if all((adjacency[cycle[i]] >> cycle[(i + 1) % length]) & 1 for i in range(length)):
                return True
    return False


def odd_girth(mask: int) -> int | None:
    for length in (3, 5, 7):
        if has_cycle(mask, length):
            return length
    return None


def dsatur(adjacency: tuple[int, ...], k: int, active: int | None = None) -> dict[str, object]:
    """Exact k-colour decision with canonical colour introduction."""
    size = len(adjacency)
    active = (1 << size) - 1 if active is None else active
    vertices = [v for v in range(size) if (active >> v) & 1]
    if not vertices:
        return {"colourable": True, "nodes": 1, "colouring": []}
    colours = [-1] * size
    nodes = 0
    witness: list[int] | None = None

    first = max(vertices, key=lambda v: ((adjacency[v] & active).bit_count(), -v))
    colours[first] = 0

    def search(used: int, remaining: int) -> bool:
        nonlocal nodes, witness
        nodes += 1
        if not remaining:
            witness = colours.copy()
            return True

        best_vertex = -1
        best_key = (-1, -1, 0)
        best_forbidden = 0
        todo = remaining
        while todo:
            bit = todo & -todo
            v = bit.bit_length() - 1
            todo ^= bit
            forbidden = 0
            neighbors = adjacency[v] & active & ~remaining
            while neighbors:
                q = neighbors & -neighbors
                u = q.bit_length() - 1
                neighbors ^= q
                if colours[u] >= 0:
                    forbidden |= 1 << colours[u]
            key = (forbidden.bit_count(), (adjacency[v] & remaining).bit_count(), -v)
            if key > best_key:
                best_key = key
                best_vertex = v
                best_forbidden = forbidden

        next_remaining = remaining & ~(1 << best_vertex)
        # Any colouring can have its colour names permuted into first-use order,
        # so it suffices to try existing colours and at most one new colour.
        for colour in range(min(k, used + 1)):
            if (best_forbidden >> colour) & 1:
                continue
            colours[best_vertex] = colour
            feasible = True
            todo = next_remaining
            while todo:
                bit = todo & -todo
                v = bit.bit_length() - 1
                todo ^= bit
                forbidden = 0
                neighbors = adjacency[v] & active & ~next_remaining
                while neighbors:
                    q = neighbors & -neighbors
                    u = q.bit_length() - 1
                    neighbors ^= q
                    if colours[u] >= 0:
                        forbidden |= 1 << colours[u]
                if forbidden.bit_count() == k:
                    feasible = False
                    break
            if feasible and search(max(used, colour + 1), next_remaining):
                return True
            colours[best_vertex] = -1
        return False

    remaining = active & ~(1 << first)
    colourable = search(1, remaining)
    return {"colourable": colourable, "nodes": nodes, "colouring": witness}


def adjacency_from_edges(size: int, edges: list[tuple[int, int]]) -> tuple[int, ...]:
    rows = [0] * size
    for u, v in edges:
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    return tuple(rows)


def brute_k_colourable(adjacency: tuple[int, ...], k: int) -> bool:
    """Definition-level colouring oracle for tiny self-test graphs."""
    size = len(adjacency)
    for colours in itertools.product(range(k), repeat=size):
        if all(
            colours[u] != colours[v]
            for u in range(size)
            for v in range(u + 1, size)
            if (adjacency[u] >> v) & 1
        ):
            return True
    return False


def self_tests() -> dict[str, object]:
    c5 = adjacency_from_edges(5, [(i, (i + 1) % 5) for i in range(5)])
    k7 = adjacency_from_edges(7, list(itertools.combinations(range(7), 2)))
    k33 = adjacency_from_edges(6, [(i, j) for i in range(3) for j in range(3, 6)])
    k4_plus_isolate = adjacency_from_edges(5, list(itertools.combinations(range(4), 2)))
    assertions = {
        "C5_not_2_colourable": not dsatur(c5, 2)["colourable"],
        "C5_3_colourable": dsatur(c5, 3)["colourable"],
        "K7_not_6_colourable": not dsatur(k7, 6)["colourable"],
        "K7_7_colourable": dsatur(k7, 7)["colourable"],
        "K33_2_colourable": dsatur(k33, 2)["colourable"],
        "K4_control_detected": k4_count(k4_plus_isolate) == 1,
        "C5_K4_free": k4_count(c5) == 0,
    }
    assert all(assertions.values())

    compositions = [
        row
        for row in itertools.product(range(6), repeat=6)
        if sum(row) == 28
    ]
    assert compositions
    minimum_fives = min(row.count(5) for row in compositions)
    assert minimum_fives == 4

    # Positive control for the residual reduction: K_{5,5,5,5,4,4} is
    # six-colourable with alpha=5, and removing its four maximum parts leaves
    # the bipartite K_{4,4} induced by the final two colour classes.
    parts = [range(0, 5), range(5, 10), range(10, 15), range(15, 20), range(20, 24), range(24, 28)]
    control_edges = [
        (u, v)
        for i, left in enumerate(parts)
        for right in parts[i + 1 :]
        for u in left
        for v in right
    ]
    control = adjacency_from_edges(28, control_edges)
    residual = sum(1 << v for v in itertools.chain(parts[4], parts[5]))
    assert dsatur(control, 6)["colourable"]
    assert induced_bipartite(residual, control)

    # Exhaustively cross-check both independent engines on every labelled graph
    # with five vertices (2^10 edge sets), using only definition-level oracles.
    pairs = list(itertools.combinations(range(5), 2))
    dsatur_comparisons = 0
    bron_kerbosch_comparisons = 0
    for edge_mask in range(1 << len(pairs)):
        edges = [pair for i, pair in enumerate(pairs) if (edge_mask >> i) & 1]
        graph = adjacency_from_edges(5, edges)
        for k in (2, 3):
            assert bool(dsatur(graph, k)["colourable"]) == brute_k_colourable(graph, k)
            dsatur_comparisons += 1
        independent = maximal_cliques(complement(graph))
        computed_alpha = max(mask.bit_count() for mask in independent)
        brute_alpha = max(
            mask.bit_count() for mask in range(1 << 5) if is_independent(mask, graph)
        )
        assert computed_alpha == brute_alpha
        bron_kerbosch_comparisons += 1

    return {
        "solver_and_K4_tests": assertions,
        "six_class_size_compositions": len(compositions),
        "minimum_number_of_size_five_classes": minimum_fives,
        "positive_residual_control": "K_{5,5,5,5,4,4} leaves bipartite K_{4,4}",
        "all_labelled_five_vertex_graphs": 1024,
        "dsatur_vs_bruteforce_comparisons": dsatur_comparisons,
        "bron_kerbosch_vs_bruteforce_comparisons": bron_kerbosch_comparisons,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--emit",
        action="store_true",
        help="emit a freshly computed summary without comparing expected.json",
    )
    args = parser.parse_args()

    assert len(VERTICES) == len(set(VERTICES)) == 28
    assert INDEX[IDENTITY] == 0
    assert IDENTITY not in GENERATORS
    assert {inverse(s) for s in GENERATORS} == set(GENERATORS)
    assert all(multiply(IDENTITY, x) == multiply(x, IDENTITY) == x for x in VERTICES)
    assert all(multiply(x, inverse(x)) == multiply(inverse(x), x) == IDENTITY for x in VERTICES)
    assert all(
        multiply(multiply(x, y), z) == multiply(x, multiply(y, z))
        for x in VERTICES
        for y in VERTICES
        for z in VERTICES
    )

    edges = edge_pairs()
    assert len(edges) == 168
    assert all(row.bit_count() == 12 for row in ADJ)
    assert all(not ((ADJ[v] >> v) & 1) for v in range(N))
    assert k4_count(ADJ) == 0

    identity_neighbors = ADJ[0]
    neighborhood_edges = sum(
        1
        for u, v in edges
        if (identity_neighbors >> u) & 1 and (identity_neighbors >> v) & 1
    )
    neighborhood_triangles = sum(
        1
        for u, v, w in itertools.combinations(range(N), 3)
        if all((identity_neighbors >> q) & 1 for q in (u, v, w))
        and (ADJ[u] >> v) & 1
        and (ADJ[u] >> w) & 1
        and (ADJ[v] >> w) & 1
    )
    assert (neighborhood_edges, neighborhood_triangles) == (24, 0)

    named_colours = [[INDEX[x] for x in colour] for colour in SEVEN_COLOURING]
    assert sorted(itertools.chain.from_iterable(named_colours)) == list(range(N))
    assert all(is_independent(sum(1 << v for v in colour)) for colour in named_colours)

    complement_rows = complement(ADJ)
    maximal_independent = maximal_cliques(complement_rows)
    alpha = max(mask.bit_count() for mask in maximal_independent)
    maximum_independent = sorted(mask for mask in maximal_independent if mask.bit_count() == alpha)
    assert alpha == 5 and len(maximum_independent) == 56

    packing_count = 0
    residuals = set()
    for four in itertools.combinations(maximum_independent, 4):
        if any(x & y for x, y in itertools.combinations(four, 2)):
            continue
        packing_count += 1
        residuals.add(ALL ^ (four[0] | four[1] | four[2] | four[3]))
    assert packing_count == len(residuals) == 1820
    assert all(mask.bit_count() == 8 for mask in residuals)
    assert not any(induced_bipartite(mask) for mask in residuals)
    odd_girth_counts = Counter(odd_girth(mask) for mask in residuals)
    assert None not in odd_girth_counts

    six = dsatur(ADJ, 6)
    seven = dsatur(ADJ, 7)
    assert not six["colourable"] and seven["colourable"]

    deletion_nodes = []
    deletion_witness_hashes = []
    for deleted in range(N):
        result = dsatur(ADJ, 6, ALL ^ (1 << deleted))
        assert result["colourable"]
        colouring = result["colouring"]
        assert isinstance(colouring, list)
        assert all(
            colouring[u] != colouring[v]
            for u, v in edges
            if u != deleted and v != deleted
        )
        deletion_nodes.append(int(result["nodes"]))
        deletion_witness_hashes.append(digest(colouring))

    output = {
        "graph": {
            "vertices": N,
            "edges": len(edges),
            "degree": 12,
            "edge_sha256": digest(edges),
            "K4_count_exhaustive": 0,
            "identity_neighborhood_edges": neighborhood_edges,
            "identity_neighborhood_triangles": neighborhood_triangles,
        },
        "independence": {
            "alpha": alpha,
            "maximum_sets": len(maximum_independent),
            "maximum_set_sha256": digest(maximum_independent),
            "maximal_set_size_distribution": dict(
                (str(size), count)
                for size, count in sorted(
                    Counter(mask.bit_count() for mask in maximal_independent).items()
                )
            ),
        },
        "four_class_reduction": {
            "packings": packing_count,
            "distinct_residuals": len(residuals),
            "bipartite_residuals": 0,
            "odd_girth_distribution": {
                str(length): count for length, count in sorted(odd_girth_counts.items())
            },
            "residual_sha256": digest(sorted(residuals)),
        },
        "direct_colouring": {
            "six_colourable": False,
            "six_colour_search_nodes": six["nodes"],
            "seven_colourable": True,
            "seven_colour_search_nodes": seven["nodes"],
            "displayed_seven_colouring_valid": True,
        },
        "vertex_critical_crosscheck": {
            "all_28_deletions_six_colourable": True,
            "search_nodes_min": min(deletion_nodes),
            "search_nodes_max": max(deletion_nodes),
            "witnesses_sha256": digest(deletion_witness_hashes),
        },
        "self_tests": self_tests(),
    }
    if not args.emit:
        expected_path = Path(__file__).with_name("expected.json")
        expected = json.loads(expected_path.read_text(encoding="utf-8"))
        assert output == expected
        print("PASS: independent audit matches expected.json")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
