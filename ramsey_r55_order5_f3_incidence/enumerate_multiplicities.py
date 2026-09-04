#!/usr/bin/env python3
"""Exhaust all 6,435 multisets of eight three-bit incidence columns.

Bit 0 represents x, bit 1 y, bit 2 z. Fixed edge order is xy, xz, yz.
This audits the necessary conditions in PROOF.md, not 43-vertex graphs.
"""
from itertools import combinations, combinations_with_replacement, permutations, product
from math import factorial
import json

PAIRS = tuple(combinations(range(3), 2))


def bit(value, position):
    return (value >> position) & 1


def canonical(columns, edges):
    """Quotient only fixed permutations, column permutations, and color reversal."""
    images = []
    for p in permutations(range(3)):
        cols = tuple(sorted(sum(bit(v, p[i]) << i for i in range(3))
                            for v in columns))
        es = tuple(edges[PAIRS.index(tuple(sorted((p[i], p[j]))))]
                   for i, j in PAIRS)
        images.append((cols, es))
        images.append((tuple(sorted(v ^ 7 for v in cols)),
                       tuple(1 - e for e in es)))
    return min(images)


def main():
    counts = {"column_multisets": 0, "balanced_multisets": 0,
              "pair_cap_multisets": 0, "before_mixed_cap": 0,
              "surviving_labeled_fixed_multisets": 0,
              "surviving_fully_labeled_matrices": 0}
    before_triangle, before_mixed, survivors = set(), set(), set()
    for columns in combinations_with_replacement(range(8), 8):
        counts["column_multisets"] += 1
        if any(sum(bit(v, i) for v in columns) != 4 for i in range(3)):
            continue
        counts["balanced_multisets"] += 1
        if any(sum(bit(v, i) * bit(v, j) for v in columns) > 2
               for i, j in PAIRS):
            continue
        counts["pair_cap_multisets"] += 1
        for edges in product(range(2), repeat=3):
            key = canonical(columns, edges)
            before_triangle.add(key)
            if len(set(edges)) == 1 and (7 if edges[0] else 0) in columns:
                continue
            before_mixed.add(key)
            counts["before_mixed_cap"] += 1
            if any(columns.count((c << i) | (c << j) |
                                 ((1 - c) << (3 - i - j))) >= 2
                   for (i, j), c in zip(PAIRS, edges)):
                continue
            survivors.add(key)
            counts["surviving_labeled_fixed_multisets"] += 1
            labels = factorial(8)
            for value in range(8):
                labels //= factorial(columns.count(value))
            counts["surviving_fully_labeled_matrices"] += labels
    counts["classes_before_triangle_cap"] = len(before_triangle)
    counts["classes_before_mixed_cap"] = len(before_mixed)
    counts["surviving_equivalence_classes"] = len(survivors)
    representatives = []
    for h in (0, 1):
        multiplicities = (1, 1, 1, 1, h, 2 - h, 2 - h, h)
        columns = tuple(v for v, count in enumerate(multiplicities)
                        for _ in range(count))
        assert canonical(columns, (1, 0, 0)) in survivors
        representatives.append({"h": h, "columns": columns,
                                "multiplicities": multiplicities,
                                "fixed_edges": (1, 0, 0),
                                "fixed_red_degrees": (21, 21, 20)})
    assert len(survivors) == len(representatives) == 2
    print(json.dumps({"format": "r55-order5-f3-incidence-v1",
                      "counts": counts, "representatives": representatives},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
