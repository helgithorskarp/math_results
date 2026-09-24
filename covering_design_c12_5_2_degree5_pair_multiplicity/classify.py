#!/usr/bin/env python3
"""Enumerate the local incidence types, using only the standard library."""

from itertools import combinations, permutations

EDGES = tuple(combinations(range(5), 2))
EDGE_PERMUTATIONS = tuple(
    tuple(EDGES.index(tuple(sorted((p[u], p[v])))) for u, v in EDGES)
    for p in permutations(range(5))
)


def canonical(edge_counts):
    """The least vector in the full S_5 orbit, with no heuristic pruning."""
    return min(tuple(edge_counts[j] for j in perm)
               for perm in EDGE_PERMUTATIONS)


def labelled_vectors():
    """All ten-entry vectors of sum nine and vertex degrees at most four."""
    result = []

    def visit(index, remaining, degrees, counts):
        if remaining < 0 or sum(4 - d for d in degrees) < 2 * remaining:
            return
        if index == len(EDGES):
            if remaining == 0:
                result.append(tuple(counts))
            return
        u, v = EDGES[index]
        for count in range(min(4 - degrees[u], 4 - degrees[v], remaining) + 1):
            degrees[u] += count
            degrees[v] += count
            visit(index + 1, remaining - count, degrees, counts + [count])
            degrees[u] -= count
            degrees[v] -= count

    visit(0, 9, [0] * 5, [])
    return tuple(sorted(result))


def incidence(edge_counts):
    """Return eleven column masks and five four-set row masks.

    A column of weight one is a singleton incidence. A column of weight
    two is an edge; repeated edges give different underlying points.
    """
    degrees = [sum(edge_counts[e] for e, (u, v) in enumerate(EDGES)
                   if i in (u, v)) for i in range(5)]
    columns = tuple(
        [1 << i for i in range(5) for _ in range(4 - degrees[i])]
        + [(1 << u) | (1 << v) for e, (u, v) in enumerate(EDGES)
           for _ in range(edge_counts[e])]
    )
    rows = tuple(sum(1 << j for j, column in enumerate(columns) if column >> i & 1)
                 for i in range(5))
    return columns, rows


def types():
    vectors = labelled_vectors()
    counts = {}
    for vector in vectors:
        key = canonical(vector)
        counts[key] = counts.get(key, 0) + 1
    return vectors, tuple((key, counts[key]) for key in sorted(counts))
