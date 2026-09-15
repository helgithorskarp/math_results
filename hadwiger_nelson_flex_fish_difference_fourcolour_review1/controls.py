#!/usr/bin/env python3
"""Independent controls for the difference-body review checker."""

from __future__ import annotations

import itertools
import json
from fractions import Fraction as Q

import verify


def require(condition, message):
    if not condition:
        raise ValueError(message)


def interval_controls():
    cases = 0
    values = [Q(i, 2) for i in range(-4, 5)]
    intervals = [(left, right) for left in values for right in values
                 if left <= right]
    for left in intervals:
        square = verify.isquare(left)
        samples = [left[0], left[1], (left[0] + left[1]) / 2]
        for value in samples:
            require(square[0] <= value * value <= square[1], "square enclosure")
            cases += 1
    for left in intervals:
        for right in intervals:
            difference = verify.isub(left, right)
            for x in (left[0], left[1]):
                for y in (right[0], right[1]):
                    require(difference[0] <= x - y <= difference[1],
                            "difference enclosure")
                    cases += 1
    return cases


def brute_colourable(order, edges, colours):
    return any(all(word[a] != word[b] for a, b in edges)
               for word in itertools.product(range(colours), repeat=order))


def colouring_controls():
    # All 512 labelled five-vertex graphs containing the normalizing edge.
    pairs = list(itertools.combinations(range(5), 2))
    optional = [edge for edge in pairs if edge != (0, 1)]
    for mask in range(1 << len(optional)):
        edges = [(0, 1)] + [edge for bit, edge in enumerate(optional)
                            if mask >> bit & 1]
        for colours in (2, 3):
            found, _ = verify.k_colourable(5, edges, colours)
            require(found == brute_colourable(5, edges, colours),
                    "colouring search disagreement")
    return (1 << len(optional)) * 2


def certificate_controls():
    result = verify.verify(check_expected=False)
    target = json.loads(verify.CERTIFICATE.read_text())
    graph = verify.conservative_graph(
        json.loads(verify.GEOMETRY.read_text()))
    edges = graph["edges"]
    word = target["four_colour_word"]
    rejected = 0
    corruptions = [word[:-1], word + "0", "x" + word[1:]]
    left, right = edges[0]
    improper = list(word)
    improper[right] = improper[left]
    corruptions.append("".join(improper))
    for candidate in corruptions:
        try:
            verify.check_word(candidate, len(graph["clusters"]), edges)
        except ValueError:
            rejected += 1
    require(rejected == len(corruptions), "word corruption accepted")
    require(result["actual_chromatic_number"] == 4, "baseline failed")
    return rejected


if __name__ == "__main__":
    print(json.dumps({
        "status": "ALL_CONTROLS_PASSED",
        "interval_sample_checks": interval_controls(),
        "colouring_engine_comparisons": colouring_controls(),
        "certificate_corruptions_rejected": certificate_controls(),
    }, indent=2, sort_keys=True))
