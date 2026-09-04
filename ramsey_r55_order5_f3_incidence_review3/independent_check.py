#!/usr/bin/env python3
"""Independent exhaustive audit of the residual order-five incidence lemma.

No code or data from the reviewed artifact is imported.  The first audit keeps
all fixed vertices and moving cycles labeled instead of fixing a row or using
multiset canonicalization.  The second rebuilds the stated 13-vertex local
scope check with a direct edge-color predicate.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product


UNIVERSE = (1 << 8) - 1
ROWS = tuple(sum(1 << i for i in subset) for subset in combinations(range(8), 4))
PAIRS = ((0, 1), (0, 2), (1, 2))
EXPECTED_COLUMNS = {
    (0, 1, 2, 3, 5, 5, 6, 6): 0,
    (0, 1, 2, 3, 4, 5, 6, 7): 1,
}


def cardinality(mask: int) -> int:
    return mask.bit_count()


def normal_columns(rows: tuple[int, int, int], edges: tuple[int, int, int]):
    # Make the minority fixed-edge color red.  Complementing swaps every row.
    if sum(edges) == 2:
        rows = tuple(UNIVERSE ^ row for row in rows)
        edges = tuple(1 - edge for edge in edges)
    assert sum(edges) == 1
    x, y = PAIRS[edges.index(1)]
    z = 3 - x - y
    columns = []
    for moving_cycle in range(8):
        columns.append(sum(((rows[vertex] >> moving_cycle) & 1) << bit
                           for bit, vertex in enumerate((x, y, z))))
    return tuple(sorted(columns))


def enumerate_labeled_incidence():
    tested = 0
    pair_cap_rows = 0
    survivors = Counter()
    monochromatic_survivors = 0
    for rows in product(ROWS, repeat=3):
        if any(cardinality(rows[i] & rows[j]) > 2 or
               cardinality((UNIVERSE ^ rows[i]) & (UNIVERSE ^ rows[j])) > 2
               for i, j in PAIRS):
            tested += 8
            continue
        pair_cap_rows += 1
        for edges in product((0, 1), repeat=3):
            tested += 1
            if len(set(edges)) == 1:
                color = edges[0]
                neighborhoods = rows if color else tuple(UNIVERSE ^ row for row in rows)
                if neighborhoods[0] & neighborhoods[1] & neighborhoods[2]:
                    continue
            failed = False
            for (i, j), color in zip(PAIRS, edges, strict=True):
                k = 3 - i - j
                same_i = rows[i] if color else UNIVERSE ^ rows[i]
                same_j = rows[j] if color else UNIVERSE ^ rows[j]
                opposite_k = UNIVERSE ^ rows[k] if color else rows[k]
                if cardinality(same_i & same_j & opposite_k) > 1:
                    failed = True
                    break
            if failed:
                continue
            if len(set(edges)) == 1:
                monochromatic_survivors += 1
                continue
            columns = normal_columns(rows, edges)
            assert columns in EXPECTED_COLUMNS, (rows, edges, columns)
            survivors[EXPECTED_COLUMNS[columns]] += 1
    assert tested == len(ROWS) ** 3 * 8 == 2_744_000
    assert monochromatic_survivors == 0
    assert survivors == {0: 60_480, 1: 241_920}
    return tested, pair_cap_rows, survivors


def red_edge(u, v, left_column, right_column, left_step, right_step, word):
    if u > v:
        u, v = v, u
    if v < 3:
        return (u, v) == (0, 1)
    if u < 3:
        column = left_column if v < 8 else right_column
        return bool(column & (1 << u))
    if v < 8:
        distance = (v - u) % 5
        return distance in (left_step, 5 - left_step)
    if u >= 8:
        distance = (v - u) % 5
        return distance in (right_step, 5 - right_step)
    left_index, right_index = u - 3, v - 8
    return bool(word & (1 << ((right_index - left_index) % 5)))


FIVES = tuple(combinations(range(13), 5))


def acceptable(*parameters):
    for vertices in FIVES:
        colors = {red_edge(u, v, *parameters)
                  for u, v in combinations(vertices, 2)}
        if len(colors) == 1:
            return False
    return True


def audit_local_pairs():
    templates = 0
    colorings = 0
    domain_histogram = Counter()
    for columns in EXPECTED_COLUMNS:
        for left, right in combinations(range(8), 2):
            for left_step, right_step in product((1, 2), repeat=2):
                templates += 1
                allowed = 0
                for word in range(32):
                    colorings += 1
                    allowed += acceptable(columns[left], columns[right],
                                          left_step, right_step, word)
                assert allowed > 0
                domain_histogram[allowed] += 1
    assert templates == 224 and colorings == 7168
    assert min(domain_histogram) == 6 and max(domain_histogram) == 32
    return templates, colorings, domain_histogram


def main():
    tested, pair_rows, survivors = enumerate_labeled_incidence()
    print(f"labeled_tests={tested} pair_cap_row_triples={pair_rows} "
          f"survivors={sum(survivors.values())} h0={survivors[0]} h1={survivors[1]}")
    templates, colorings, histogram = audit_local_pairs()
    rendered = ",".join(f"{size}:{count}" for size, count in sorted(histogram.items()))
    print(f"local_templates={templates} local_colorings={colorings} "
          f"five_sets_each={len(FIVES)} allowed_word_histogram={rendered}")
    print("edge_orbits=183 fixed_incidence_orbits=24 internal_orbits=16 "
          "cross_cycle_orbits=140 fixed_pair_orbits=3")
    print("independent_order5_incidence_check=true")


if __name__ == "__main__":
    main()
