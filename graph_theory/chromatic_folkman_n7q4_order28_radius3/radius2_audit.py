#!/usr/bin/env python3
"""Solver-independent completeness audit for the radius-two frontier."""

from collections import Counter
from itertools import combinations
from pathlib import Path

import verify


EDGE_BITS = {edge: 1 << index for index, edge in enumerate(verify.PAIRS)}
BASE_MASK = sum(EDGE_BITS[edge] for edge in verify.BASE_EDGES)


def adjacency_from_edge_mask(edge_mask):
    adjacency = [0] * verify.N
    for index, (u, v) in enumerate(verify.PAIRS):
        if (edge_mask >> index) & 1:
            adjacency[u] |= 1 << v
            adjacency[v] |= 1 << u
    return adjacency


def can_add_without_k4(adjacency, edge):
    """Test an absent edge, assuming the current graph is K4-free."""
    u, v = edge
    common = adjacency[u] & adjacency[v]
    remaining = common
    while remaining:
        bit = remaining & -remaining
        w = bit.bit_length() - 1
        if adjacency[w] & common:
            return False
        remaining -= bit
    return True


def feasible_candidate_masks(fixed_mask, candidates):
    adjacency = adjacency_from_edge_mask(fixed_mask)
    feasible = set()

    def recurse(index, selected):
        if index == len(candidates):
            feasible.add(selected)
            return

        recurse(index + 1, selected)
        edge = candidates[index]
        if can_add_without_k4(adjacency, edge):
            u, v = edge
            adjacency[u] |= 1 << v
            adjacency[v] |= 1 << u
            recurse(index + 1, selected | (1 << index))
            adjacency[u] &= ~(1 << v)
            adjacency[v] &= ~(1 << u)

    recurse(0, 0)
    return feasible


def monochromatic_edge_mask(code):
    return sum(
        EDGE_BITS[edge]
        for edge in verify.PAIRS
        if code[edge[0]] == code[edge[1]]
    )


def main():
    verify.validate_graph()
    codes = verify.parse_colourings(Path(__file__).with_name("colourings.txt"))
    seed_masks = tuple(monochromatic_edge_mask(code) for code in codes[:6])
    assert all(not (BASE_MASK & mask) for mask in seed_masks)

    raw_maximal_count = 0
    distinct_maximal = set()
    candidate_distribution = Counter()

    # Any graph missing at most two inherited edges is represented: nominate
    # two inherited edges for deletion, then permit either nominated edge to
    # be added back.  Edges that already create a K4 when added individually
    # cannot occur in any K4-free extension, by monotonicity.
    for deleted in combinations(verify.BASE_EDGES, 2):
        fixed_mask = BASE_MASK
        for edge in deleted:
            fixed_mask &= ~EDGE_BITS[edge]
        fixed_adjacency = adjacency_from_edge_mask(fixed_mask)
        candidates = tuple(
            edge
            for edge in verify.PAIRS
            if not (fixed_mask & EDGE_BITS[edge])
            and can_add_without_k4(fixed_adjacency, edge)
        )
        candidate_distribution[len(candidates)] += 1
        feasible = feasible_candidate_masks(fixed_mask, candidates)
        maximal = tuple(
            selected
            for selected in feasible
            if all(
                (selected | (1 << index)) not in feasible
                for index in range(len(candidates))
                if not ((selected >> index) & 1)
            )
        )
        raw_maximal_count += len(maximal)
        for selected in maximal:
            graph_mask = fixed_mask
            for index, edge in enumerate(candidates):
                if (selected >> index) & 1:
                    graph_mask |= EDGE_BITS[edge]
            distinct_maximal.add(graph_mask)

    assert len(candidate_distribution) > 0
    assert max(candidate_distribution) == 10
    assert raw_maximal_count == 30211
    assert len(distinct_maximal) == 4416
    edge_distribution = Counter(mask.bit_count() for mask in distinct_maximal)
    assert edge_distribution == Counter(
        {156: 9, 157: 384, 158: 1757, 159: 1795, 160: 459, 161: 11, 162: 1}
    )

    uncovered = set(distinct_maximal)
    new_coverage = []
    for monochromatic in seed_masks:
        covered = {graph for graph in uncovered if not (graph & monochromatic)}
        new_coverage.append(len(covered))
        uncovered -= covered
    assert new_coverage == [3163, 948, 234, 59, 9, 3]
    assert not uncovered

    print("nominated_deletion_pairs=12090")
    print(f"candidate_count_distribution={dict(sorted(candidate_distribution.items()))}")
    print(f"raw_maximal_completions={raw_maximal_count}")
    print(f"distinct_maximal_completions={len(distinct_maximal)}")
    print(f"edge_count_distribution={dict(sorted(edge_distribution.items()))}")
    print("six_partition_new_coverage=3163,948,234,59,9,3")
    print("uncovered=0")


if __name__ == "__main__":
    main()
