#!/usr/bin/env python3
"""Exact interval certificate for the aligned EI17 pivot-cloud colouring."""

from __future__ import annotations

from itertools import combinations
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
SEED = HERE.parent / "hadwiger_nelson_ei17_common_pair"
sys.path.insert(0, str(SEED))

from intervals import squared_distance  # noqa: E402
from seed import certify as certify_seed  # noqa: E402


SEED_COLOUR_WORD = "00110231213003232"


def require(test, message):
    if not test:
        raise ValueError(message)


def boxes_disjoint(left, right):
    return left.hi < right.lo or right.hi < left.lo


def certify():
    points, seed_report = certify_seed()
    seed_edges = [tuple(edge) for edge in json.loads((SEED / "seed_edges.json").read_text())]
    colours = tuple(map(int, SEED_COLOUR_WORD))
    require(len(colours) == 17 and set(colours) == set(range(4)), "seed colour word")
    require(all(colours[u] != colours[v] for u, v in seed_edges), "proper seed colouring")

    # The formal label (i,a) denotes p_i-p_a.  All (a,a) labels are the
    # shared origin; further exact coincidences are allowed.
    labels = [(i, a) for i in range(17) for a in range(17)]
    difference_boxes = {
        (i, a): (points[i][0] - points[a][0], points[i][1] - points[a][1])
        for i, a in labels
    }
    difference_colours = {(i, a): colours[i] ^ colours[a] for i, a in labels}
    require(len({difference_colours[(a, a)] for a in range(17)}) == 1,
            "shared origin colour")

    different_colour_separation_checks = 0
    same_colour_unit_exclusion_checks = 0
    for left, right in combinations(labels, 2):
        left_box, right_box = difference_boxes[left], difference_boxes[right]
        if difference_colours[left] != difference_colours[right]:
            require(boxes_disjoint(left_box[0], right_box[0]) or
                    boxes_disjoint(left_box[1], right_box[1]),
                    f"different-colour labels may coincide: {left}, {right}")
            different_colour_separation_checks += 1
        else:
            distance = squared_distance(left_box, right_box)
            require(not distance.contains(1),
                    f"same-colour labels may be at unit distance: {left}, {right}")
            same_colour_unit_exclusion_checks += 1

    return {
        "claim": "every aligned pivot subcloud is four-colourable",
        "seed_exact_unique_root": seed_report["exact_unique_root"],
        "seed_colour_word": SEED_COLOUR_WORD,
        "formal_difference_labels": len(labels),
        "maximum_distinct_support_points": 273,
        "different_colour_separation_checks": different_colour_separation_checks,
        "same_colour_unit_exclusion_checks": same_colour_unit_exclusion_checks,
        "colour_rule": "colour(p_i-p_a)=colour(p_i) XOR colour(p_a)",
        "arithmetic": "exact rational outward intervals with denominator 2^100",
    }


if __name__ == "__main__":
    print(json.dumps(certify(), indent=2, sort_keys=True))
