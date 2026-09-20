#!/usr/bin/env python3
"""Exact audit of deletion-capacity localization around lexicographic L_13."""

from __future__ import annotations

from itertools import combinations
import json


POINTS = tuple(range(1, 10))
ALL4 = tuple(frozenset(x) for x in combinations(POINTS, 4))
L13 = ALL4[:13]
L13_SET = frozenset(L13)
REMAINING = tuple(x for x in ALL4 if x not in L13_SET)
SWAPS = ((1, 2), (3, 4), (6, 7), (8, 9))


def avoiding(family, point):
    return sum(point not in block for block in family)


BASE_AVOID = tuple(avoiding(L13, point) for point in POINTS)
CAPACITY = tuple(11 - x for x in BASE_AVOID)


def respects_capacity(extra):
    """Necessary condition for L13 union extra to remain Non-FC."""
    return all(
        sum(point not in block for block in extra) <= CAPACITY[point - 1]
        for point in POINTS
    )


def edge(block):
    assert {8, 9} <= block
    answer = tuple(sorted(block - {8, 9}))
    assert len(answer) == 2
    return answer


def edge_name(e):
    return "".join(map(str, e))


def family_name(family):
    return ",".join(sorted(edge_name(edge(block)) for block in family))


def compose(p, q):
    """Return p after q, with permutations represented by image tuples."""
    return tuple(p[q[i] - 1] for i in range(9))


def subgroup():
    identity = tuple(POINTS)
    generators = []
    for a, b in SWAPS:
        p = list(identity)
        p[a - 1], p[b - 1] = p[b - 1], p[a - 1]
        generators.append(tuple(p))
    group = {identity}
    frontier = [identity]
    while frontier:
        p = frontier.pop()
        for g in generators:
            q = compose(p, g)
            if q not in group:
                group.add(q)
                frontier.append(q)
    return tuple(sorted(group))


GROUP = subgroup()


def act_block(p, block):
    return frozenset(p[i - 1] for i in block)


def act_family(p, family):
    return frozenset(act_block(p, block) for block in family)


def canonical(family):
    encodings = []
    for p in GROUP:
        transformed = act_family(p, family)
        encodings.append(tuple(sorted(tuple(sorted(block)) for block in transformed)))
    return min(encodings)


def candidates(size):
    if size == 0:
        return (tuple(),)
    # Capacity zero at 8 and 9 forces all possible candidates into HARD.
    hard = tuple(block for block in REMAINING if {8, 9} <= block)
    return tuple(extra for extra in combinations(hard, size) if respects_capacity(extra))


def orbit_sizes(families):
    buckets = {}
    for family in families:
        key = canonical(family)
        buckets[key] = buckets.get(key, 0) + 1
    return sorted(buckets.values(), reverse=True)


def main():
    expected_edges = {
        (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9),
        (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (5, 6), (5, 7),
    }
    assert {tuple(sorted(block - {1, 2})) for block in L13} == expected_edges
    assert tuple(sum(point in block for block in L13) for point in POINTS) == (
        13, 13, 6, 6, 4, 3, 3, 2, 2
    )
    assert BASE_AVOID == (0, 0, 7, 7, 9, 10, 10, 11, 11)
    assert CAPACITY == (11, 11, 4, 4, 2, 1, 1, 0, 0)
    assert len(REMAINING) == 113

    hard = tuple(block for block in REMAINING if {8, 9} <= block)
    assert len(hard) == 21
    assert sum(not ({8, 9} <= block) for block in REMAINING) == 92
    assert all(not respects_capacity((block,)) for block in REMAINING if block not in hard)

    by_size = {m: candidates(m) for m in range(1, 5)}
    assert {m: len(v) for m, v in by_size.items()} == {1: 21, 2: 45, 3: 9, 4: 0}
    assert len(GROUP) == 16

    expected_triples = {
        "16,57,67", "17,56,67", "26,57,67", "27,56,67",
        "36,57,67", "37,56,67", "46,57,67", "47,56,67",
        "56,57,67",
    }
    observed_triples = {family_name(family) for family in by_size[3]}
    assert observed_triples == expected_triples

    orbits = {m: orbit_sizes(by_size[m]) for m in range(1, 4)}
    assert {m: len(v) for m, v in orbits.items()} == {1: 9, 2: 16, 3: 3}
    assert orbits[3] == [4, 4, 1]

    triple_representatives = sorted(
        family_name(tuple(frozenset(block) for block in key))
        for key in {canonical(family) for family in by_size[3]}
    )

    report = {
        "base_avoid": BASE_AVOID,
        "capacity": CAPACITY,
        "remaining_blocks": len(REMAINING),
        "one_block_immediately_excluded": 92,
        "candidate_counts": {str(m): len(by_size[m]) for m in range(1, 5)},
        "subgroup_order": len(GROUP),
        "orbit_counts": {str(m): len(orbits[m]) for m in range(1, 4)},
        "triple_orbit_sizes": orbits[3],
        "triple_representatives": triple_representatives,
        "status": "PASS",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
