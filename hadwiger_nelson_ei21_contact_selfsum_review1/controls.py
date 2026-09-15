#!/usr/bin/env python3
"""Independent controls for the EI21 contact/self-sum review."""

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
    values = [Q(value, 2) for value in range(-4, 5)]
    intervals = [(left, right) for left in values for right in values
                 if left <= right]
    for interval in intervals:
        enclosure = verify.isquare(interval)
        for value in (interval[0], interval[1], sum(interval) / 2):
            require(enclosure[0] <= value * value <= enclosure[1],
                    "square enclosure")
            cases += 1
    for left in intervals:
        for right in intervals:
            enclosure = verify.isub(left, right)
            for x in (left[0], left[1]):
                for y in (right[0], right[1]):
                    require(enclosure[0] <= x - y <= enclosure[1],
                            "difference enclosure")
                    cases += 1
    return cases


def brute_colourable(order, edges, colours):
    return any(all(word[left] != word[right] for left, right in edges)
               for word in itertools.product(range(colours), repeat=order))


def colouring_controls():
    pairs = list(itertools.combinations(range(5), 2))
    optional = [edge for edge in pairs if edge != (0, 1)]
    comparisons = 0
    for mask in range(1 << len(optional)):
        edges = [(0, 1)] + [edge for bit, edge in enumerate(optional)
                            if mask >> bit & 1]
        for colours in (2, 3):
            found, _, _ = verify.static_colour(5, edges, colours)
            require(found == brute_colourable(5, edges, colours),
                    "colouring search disagreement")
            comparisons += 1
    return comparisons


def graph_controls():
    complete4 = list(itertools.combinations(range(4), 2))
    cycle5 = [(i, (i + 1) % 5) for i in range(5)]
    path5 = [(i, i + 1) for i in range(4)]
    require(verify.vertex_connectivity(4, complete4)[0] == 3, "K4 connectivity")
    require(verify.vertex_connectivity(5, cycle5)[0] == 2, "C5 connectivity")
    require(verify.vertex_connectivity(5, path5)[0] == 1, "P5 connectivity")
    return 3


def certificate_controls():
    result = verify.verify(check_expected=False)
    geometry = json.loads(verify.GEOMETRY.read_text())
    certificate = json.loads(verify.SELFSUM.read_text())
    boxes, edges, _ = verify.source_review(geometry)
    review = verify.selfsum_review(boxes, edges, certificate)
    require(review["actual_chromatic_number"] == 4, "self-sum baseline")

    addresses = list(itertools.combinations_with_replacement(range(21), 2))
    sum_boxes = [(verify.iadd(boxes[a][0], boxes[b][0]),
                  verify.iadd(boxes[a][1], boxes[b][1])) for a, b in addresses]
    possible_equal = [(a, b) for a, b in itertools.combinations(range(231), 2)
                      if verify.overlaps(sum_boxes[a][0], sum_boxes[b][0])
                      and verify.overlaps(sum_boxes[a][1], sum_boxes[b][1])]
    clusters = verify.union_components(231, possible_equal)
    cluster_of = {address: cluster for cluster, members in enumerate(clusters)
                  for address in members}
    possible_edges = set()
    for left, right in itertools.combinations(range(231), 2):
        if cluster_of[left] == cluster_of[right]:
            continue
        dx = verify.isub(sum_boxes[left][0], sum_boxes[right][0])
        dy = verify.isub(sum_boxes[left][1], sum_boxes[right][1])
        distance = verify.iadd(verify.isquare(dx), verify.isquare(dy))
        if distance[0] <= 1 <= distance[1]:
            possible_edges.add(tuple(sorted((cluster_of[left], cluster_of[right]))))
    edge_list = sorted(possible_edges)
    word = certificate["four_colour_word"]
    bad_words = [word[:-1], word + "0", "x" + word[1:]]
    left, right = edge_list[0]
    improper = list(word)
    improper[right] = improper[left]
    bad_words.append("".join(improper))
    rejected = 0
    for bad in bad_words:
        if not verify.proper(bad, len(clusters), edge_list):
            rejected += 1
    require(rejected == len(bad_words), "bad word accepted")
    require(result["source"]["vertex_connectivity"] == 3, "baseline result")
    return rejected


if __name__ == "__main__":
    print(json.dumps({
        "status": "ALL_CONTROLS_PASSED",
        "interval_sample_checks": interval_controls(),
        "colouring_engine_comparisons": colouring_controls(),
        "graph_connectivity_controls": graph_controls(),
        "certificate_corruptions_rejected": certificate_controls(),
    }, indent=2, sort_keys=True))
