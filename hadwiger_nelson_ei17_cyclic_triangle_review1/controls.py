#!/usr/bin/env python3
"""Definition-level controls for the independent cyclic EI17 review."""

from __future__ import annotations

import json
from functools import lru_cache
from itertools import product

import verify as V


def require(condition, message):
    if not condition:
        raise ValueError(message)


def independent_partition_count(edges):
    """Count four independent-set partitions, not sequential colour words."""
    vertex_count = 17
    adjacency = [0]*vertex_count
    for a, b in edges:
        adjacency[a] |= 1 << b
        adjacency[b] |= 1 << a
    independent = []
    for mask in range(1 << vertex_count):
        left = mask
        okay = True
        while left:
            bit = left & -left
            vertex = bit.bit_length()-1
            left -= bit
            if adjacency[vertex] & left:
                okay = False
                break
        if okay:
            independent.append(mask)
    by_minimum = [[] for _ in range(vertex_count)]
    for mask in independent:
        if mask:
            by_minimum[(mask & -mask).bit_length()-1].append(mask)

    @lru_cache(None)
    def count(remaining, blocks):
        if not remaining:
            return int(blocks == 0)
        if blocks == 0 or remaining.bit_count() < blocks:
            return 0
        minimum = (remaining & -remaining).bit_length()-1
        return sum(count(remaining ^ block, blocks-1)
                   for block in by_minimum[minimum]
                   if block & remaining == block)

    partitions = count((1 << vertex_count)-1, 4)
    return len(independent), partitions, count.cache_info().misses


def brute_domain_solution(domains, neighbours):
    return next((word for word in product(range(4), repeat=len(domains))
                 if all(domains[v] & (1 << word[v]) for v in range(len(domains)))
                 and all(word[v] != word[w] for v in range(len(domains))
                         for w in neighbours[v] if v < w)), None)


def domain_solver_controls():
    graphs = [
        [{1}, {0, 2}, {1, 3}, {2}],
        [{1, 3}, {0, 2}, {1, 3}, {0, 2}],
        [{1, 2, 3}, {0, 2, 3}, {0, 1, 3}, {0, 1, 2}],
    ]
    masks = (1, 2, 4, 8, 3, 5, 9, 6, 10, 12, 15)
    cases = 0
    for neighbours in graphs:
        for domains in product(masks, repeat=4):
            expected = brute_domain_solution(domains, neighbours)
            actual = V.solve_domains(domains, neighbours)
            require((actual is None) == (expected is None),
                    "domain solver existence mismatch")
            if actual is not None:
                require(all(domains[v] & (1 << actual[v]) for v in range(4)),
                        "domain solver mask violation")
                require(all(actual[v] != actual[w] for v in range(4)
                            for w in neighbours[v] if v < w),
                        "domain solver edge violation")
            cases += 1
    return cases


def interval_controls():
    cases = 0
    intervals = [V.Interval(V.Q(a), V.Q(b))
                 for a in range(-3, 4) for b in range(a, 4)]
    for left in intervals:
        square_values = [left.lo*left.lo, left.hi*left.hi]
        if left.contains(0):
            square_values.append(V.Q(0))
        square = left.square()
        require(square == V.Interval(min(square_values), max(square_values)),
                "square endpoint control")
        cases += 1
        for right in intervals:
            products = [x*y for x in (left.lo, left.hi)
                        for y in (right.lo, right.hi)]
            require(left*right == V.Interval(min(products), max(products)),
                    "product endpoint control")
            cases += 1
    sqrt3 = V.sqrt_integer_interval(3)
    require(sqrt3.lo*sqrt3.lo < 3 < sqrt3.hi*sqrt3.hi,
            "sqrt(3) strict bracket")
    return cases + 1


def structural_controls():
    path = [{1}, {0, 2}, {1}]
    triangle = [{1, 2}, {0, 2}, {0, 1}]
    require(V.component_count(path) == 1
            and V.component_count(path, frozenset({1})) == 2,
            "path articulation")
    require(V.component_count(path, omitted_edge=(0, 1)) == 2,
            "path bridge")
    require(V.component_count(triangle, frozenset({1})) == 1,
            "triangle false articulation")
    return 3


def pin_controls():
    rejected = 0
    for path, expected in V.PINS.items():
        require(V.digest(path) == expected, "baseline pin mismatch")
        data = bytearray(path.read_bytes())
        data[len(data)//2] ^= 1
        require(__import__("hashlib").sha256(data).hexdigest() != expected,
                "one-byte corruption missed")
        rejected += 1
    return rejected


if __name__ == "__main__":
    edges = sorted(tuple(edge) for edge in
                   json.loads((V.SOURCE / "seed_edges.json").read_text()))
    independent_sets, partitions, states = independent_partition_count(edges)
    require((independent_sets, partitions) == (1181, 85088),
            "independent-set partition census")
    print(json.dumps({
        "status": "CONTROLS PASSED",
        "independent_sets": independent_sets,
        "four_independent_set_partitions": partitions,
        "partition_dynamic_states": states,
        "domain_solver_bruteforce_cases": domain_solver_controls(),
        "interval_endpoint_cases": interval_controls(),
        "structural_cases": structural_controls(),
        "one_byte_pin_corruptions_detected": pin_controls(),
    }, indent=2, sort_keys=True))
