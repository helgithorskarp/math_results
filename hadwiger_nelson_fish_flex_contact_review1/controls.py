#!/usr/bin/env python3
"""Definition-level controls for the independent fish review."""

from __future__ import annotations

import json
import tempfile
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path

from verify import (GEOMETRY, RELATION, components, idifference, iscale,
                    isquare, static_colour, verify)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def brute_three_colourable(n, edges):
    return any(all(word[a] != word[b] for a, b in edges)
               for word in product(range(3), repeat=n))


def solver_three_colourable(n, edges):
    # The production solver has a fixed 23-vertex interface.  Pad with a
    # forced chain so isolated production vertices do not affect existence.
    padded = list(edges)
    for vertex in range(n, 23):
        padded.append((0, vertex))
    return static_colour(padded, 3)[0]


def graph_controls():
    # All 512 labelled five-vertex graphs containing the normalizing edge.
    pairs = [pair for pair in combinations(range(5), 2) if pair != (0, 1)]
    cases = 0
    for mask in range(1 << len(pairs)):
        edges = [(0, 1)] + [pair for bit, pair in enumerate(pairs)
                            if mask & (1 << bit)]
        require(brute_three_colourable(5, edges)
                == solver_three_colourable(5, edges),
                f"colour control {mask}")
        cases += 1
    return cases


def interval_controls():
    cases = 0
    for lo in range(-4, 5):
        for hi in range(lo, 5):
            interval = (Q(lo), Q(hi))
            square = isquare(interval)
            actual = [Q(x*x) for x in range(lo, hi + 1)]
            require(square[0] <= min(actual) and max(actual) <= square[1],
                    "square enclosure")
            for scalar in range(-4, 5):
                scaled = iscale(Q(scalar), interval)
                values = [Q(scalar*x) for x in range(lo, hi + 1)]
                require(scaled == (min(values), max(values)), "scale enclosure")
                cases += 1
    require(idifference((Q(-2), Q(3)), (Q(5), Q(7))) == (Q(-9), Q(-2)),
            "difference enclosure")
    return cases + 1


def cut_controls():
    path = [{1}, {0, 2}, {1}]
    triangle = [{1, 2}, {0, 2}, {0, 1}]
    require(components(path) == 1 and components(path, frozenset({1})) == 2,
            "path cut")
    require(components(triangle, frozenset({1})) == 1, "triangle cut")
    return 2


def corruption_controls():
    geometry = json.loads(GEOMETRY.read_text())
    relation = json.loads(RELATION.read_text())
    mutations = []
    bad = json.loads(json.dumps(geometry))
    bad["midpoint_numerators"][2][0] += 1
    mutations.append((bad, relation))
    bad = json.loads(json.dumps(geometry))
    bad["inverse_numerators"][0][0] += 1
    mutations.append((bad, relation))
    bad_relation = json.loads(json.dumps(relation))
    bad_relation["words"][0] = "0" + bad_relation["words"][0][1:]
    mutations.append((geometry, bad_relation))
    rejected = 0
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        for index, (gdata, rdata) in enumerate(mutations):
            gp, rp = root / f"g{index}.json", root / f"r{index}.json"
            gp.write_text(json.dumps(gdata))
            rp.write_text(json.dumps(rdata))
            try:
                verify(gp, rp)
            except ValueError:
                rejected += 1
    require(rejected == len(mutations), "corruption accepted")
    return rejected


if __name__ == "__main__":
    print(json.dumps({
        "status": "CONTROLS PASSED",
        "five_vertex_graphs_compared_with_bruteforce": graph_controls(),
        "interval_cases": interval_controls(),
        "cut_cases": cut_controls(),
        "certificate_corruptions_rejected": corruption_controls(),
    }, indent=2, sort_keys=True))
