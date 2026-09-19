#!/usr/bin/env python3
"""Independent edge-by-edge check of the low-slack Q4 census.

This implementation uses unordered endpoint pairs and assigns the 32 global
Q4 edges one at a time.  It does not import the facet-gluing verifier.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations
import json


DIM = 4
MAX_COST = 10  # twice the Q4 slack cutoff five
VERTICES = tuple(range(1 << DIM))
EDGES = tuple(
    sorted(
        (vertex, vertex ^ (1 << coordinate))
        for vertex in VERTICES
        for coordinate in range(DIM)
        if vertex < (vertex ^ (1 << coordinate))
    )
)
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
FACET_VERTEX_SETS = tuple(
    frozenset(vertex for vertex in VERTICES if ((vertex >> coordinate) & 1) == bit)
    for coordinate in range(DIM)
    for bit in (0, 1)
)
FACET_EDGES = tuple(
    tuple(index for index, edge in enumerate(EDGES) if set(edge) <= vertices)
    for vertices in FACET_VERTEX_SETS
)
EDGE_FACETS = tuple(
    tuple(facet for facet, edges in enumerate(FACET_EDGES) if edge in edges)
    for edge in range(len(EDGES))
)
SQUARES = tuple(
    tuple(
        EDGE_INDEX[tuple(sorted(edge))]
        for edge in (
            (base, base ^ (1 << first)),
            (base, base ^ (1 << second)),
            (base ^ (1 << first), base ^ (1 << first) ^ (1 << second)),
            (base ^ (1 << second), base ^ (1 << first) ^ (1 << second)),
        )
    )
    for first in range(DIM)
    for second in range(first + 1, DIM)
    for base in VERTICES
    if not (base >> first) & 1 and not (base >> second) & 1
)
FACET_SQUARES = tuple(
    tuple(square for square in SQUARES if all(edge in edges for edge in square))
    for edges in map(frozenset, FACET_EDGES)
)


def local_cost(mask: int, facet: int) -> int:
    missing = []
    inactive_incidences = 0
    for square in FACET_SQUARES[facet]:
        chosen = [edge for edge in square if (mask >> edge) & 1]
        if len(chosen) == 4:
            raise ValueError("completed square")
        if len(chosen) == 3:
            missing.append(next(edge for edge in square if edge not in chosen))
        else:
            inactive_incidences += len(chosen)
    return 2 * inactive_incidences + 4 * (len(missing) - len(set(missing))) - len(missing)


def candidates(facet: int) -> tuple[tuple[int, int], ...]:
    edges = FACET_EDGES[facet]
    result = []
    for local_mask in range(1 << len(edges)):
        mask = sum(
            ((local_mask >> position) & 1) << edge
            for position, edge in enumerate(edges)
        )
        try:
            cost = local_cost(mask, facet)
        except ValueError:
            continue
        if cost <= MAX_COST:
            result.append((mask, cost))
    return tuple(result)


def direct_slack(mask: int) -> int:
    witnesses = []
    for square in SQUARES:
        chosen = [edge for edge in square if (mask >> edge) & 1]
        if len(chosen) == 4:
            raise AssertionError("enumerated pattern is not square-free")
        if len(chosen) == 3:
            witnesses.append(next(edge for edge in square if edge not in chosen))
    multiplicities = Counter(witnesses)
    pairs = sum(count * (count - 1) // 2 for count in multiplicities.values())
    return 6 * mask.bit_count() - 7 * len(witnesses) + 2 * pairs


def normalized_graph_hash(masks: set[int]) -> str:
    rows = []
    for mask in masks:
        rows.append(tuple(edge for index, edge in enumerate(EDGES) if (mask >> index) & 1))
    canonical = json.dumps(sorted(rows), separators=(",", ":"))
    return sha256(canonical.encode("ascii")).hexdigest()


def census() -> tuple[set[int], int, int]:
    initial = tuple(candidates(facet) for facet in range(len(FACET_EDGES)))
    complete: set[int] = set()
    nodes = 0
    pruned = 0

    def visit(depth: int, values: int, states: tuple[tuple[tuple[int, int], ...], ...]) -> None:
        nonlocal nodes, pruned
        nodes += 1
        if sum(min(cost for _, cost in facet_states) for facet_states in states) > MAX_COST:
            pruned += 1
            return
        if depth == len(EDGES):
            complete.add(values)
            return
        edge = depth
        for bit in (0, 1):
            next_states = list(states)
            possible = True
            for facet in EDGE_FACETS[edge]:
                filtered = tuple(
                    state
                    for state in next_states[facet]
                    if ((state[0] >> edge) & 1) == bit
                )
                if not filtered:
                    possible = False
                    break
                next_states[facet] = filtered
            if possible:
                visit(
                    depth + 1,
                    values | (bit << edge),
                    tuple(next_states),
                )

    visit(0, 0, initial)
    return complete, nodes, pruned


def independent_check() -> dict[str, object]:
    if len(EDGES) != 32 or len(SQUARES) != 24:
        raise AssertionError("incorrect Q4 structure")
    if set(map(len, FACET_EDGES)) != {12} or set(map(len, FACET_SQUARES)) != {6}:
        raise AssertionError("incorrect Q3 facet structure")
    if set(map(len, EDGE_FACETS)) != {3}:
        raise AssertionError("each Q4 edge must lie in three Q3 facets")

    patterns, nodes, pruned = census()
    spectrum = Counter((mask.bit_count(), direct_slack(mask)) for mask in patterns)
    expected = {(0, 0): 1, (17, 3): 64, (19, 5): 192}
    if spectrum != expected:
        raise AssertionError("independent low-slack spectrum mismatch")
    graph_hash = normalized_graph_hash(patterns)
    expected_hash = "e9e897e7ac97b4fce847acbb395615d3cc1e409dea2ef57148273fd1a1bd1c72"
    if graph_hash != expected_hash:
        raise AssertionError("entry-level graph set differs from the production census")
    deficits = sorted(
        17 * slack - 3 * edges
        for (edges, slack), count in spectrum.items()
        for _ in range(count)
        if edges and 17 * slack - 3 * edges > 0
    )
    if deficits[0] != 28 or len(deficits) != 192:
        raise AssertionError("defect-28 classification mismatch")
    return {
        "representation": "unordered endpoint pairs",
        "algorithm": "global edge branching with local-state lower bounds",
        "edge_branch_nodes": nodes,
        "edge_branch_pruned": pruned,
        "q4_low_slack_patterns": len(patterns),
        "q4_low_slack_spectrum_E_S_count": [
            [edge_count, slack, count]
            for (edge_count, slack), count in sorted(spectrum.items())
        ],
        "q4_least_positive_deficit": deficits[0],
        "normalized_graph_set_sha256": graph_hash,
    }


def main() -> None:
    print(json.dumps(independent_check(), sort_keys=True, indent=2))
    print("status=PASS")


if __name__ == "__main__":
    main()
