#!/usr/bin/env python3
"""Algebraic incidence controls for an ordinary cycle-saturation proof.

This producer uses tight pair capacities and omitted-T words. Neither
the equality frames nor the necessary cores are full-host constructions.
"""
from collections import Counter
from itertools import combinations, product
import json


def record():
    pairs = tuple(combinations(range(4), 2))
    cycle = {(0, 1), (1, 2), (2, 3), (0, 3)}
    profiles = []
    for q in range(4):
        h = [3] * 4
        h[q] = 2
        margins = [x + 3 for x in h]
        caps = [h[i] + h[j] - (4 if (i, j) in cycle else 3)
                for i, j in pairs]
        counts = [0] * 16
        for (i, j), cap in zip(pairs, caps):
            counts[(1 << i) | (1 << j)] = cap
        for i in range(4):
            counts[1 << i] = margins[i] - sum(
                cap for pair, cap in zip(pairs, caps) if i in pair)
        if min(counts) < 0 or sum(counts) != 12:
            raise ValueError("degree-nine equality margins failed")
        profiles.append({"h": h, "blue_margins": margins,
                         "pair_caps": caps, "blue_word_counts": counts,
                         "outside_red_block": [6, 2, 2, 1]})
    classes = {"X_repeat": [], "Y_repeat": [], "cross_repeat": []}
    for omitted in product(range(3), repeat=4):
        if sorted(Counter(omitted).values()) != [1, 1, 2]:
            continue
        repeated = next(t for t in range(3) if omitted.count(t) == 2)
        positions = [i for i, t in enumerate(omitted) if t == repeated]
        name = ("X_repeat" if positions == [0, 1] else
                "Y_repeat" if positions == [2, 3] else "cross_repeat")
        word = sum((7 ^ (1 << t)) << (3 * i)
                   for i, t in enumerate(omitted))
        classes[name].append(word)
    return {
        "cycle_profiles": profiles,
        "row_costs_by_blue_rank": [1, 0, 0, 1, 3],
        "leaf_core_words": {k: sorted(v) for k, v in sorted(classes.items())},
        "leaf_core_counts": {k: len(v) for k, v in sorted(classes.items())},
        "leaf_X_special_ordinary_red_sets": [[5, 7], [4, 6]],
        "leaf_X_special_ordinary_red_overlap": 0,
        "caseII_full_T_degree_splits": [[5, 4, 5], [4, 5, 6]],
    }


if __name__ == "__main__":
    print(json.dumps(record(), indent=2, sort_keys=True))
