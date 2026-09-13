#!/usr/bin/env python3
"""Sweep depth-two physical circle closures over all two-phase quartets.

Candidate-generation numerics only.  Every generated point is an intersection
of two specified unit circles, so realizability is built into the search.
Any non-4-colourable output is provisional pending reconstruction and exact
certification.  Positive colourings are checked directly.
"""

from __future__ import annotations

import argparse
import cmath
from itertools import combinations
import json
import math
import time

from scratch_four_circle_moser_layers import dsatur


def key(z, scale=10**9):
    return round(z.real * scale), round(z.imag * scale)


def intersections(a, b):
    delta = b - a
    distance = abs(delta)
    if distance < 1e-11 or distance > 2 + 1e-9:
        return []
    midpoint = (a + b) / 2
    height2 = max(0.0, 1 - distance * distance / 4)
    offset = delta / distance * 1j * math.sqrt(height2)
    return [midpoint] if abs(offset) < 1e-11 else [midpoint + offset, midpoint - offset]


def support(centres, directions, depth):
    points, lookup = [], {}

    def add(z):
        k = key(z)
        if k not in lookup:
            lookup[k] = len(points)
            points.append(z)

    add(0j)
    for centre in centres:
        add(centre)
        for direction in directions:
            add(centre + direction)
    sizes = [len(points)]
    for _ in range(depth):
        old_points = list(points)
        for centre in centres:
            for q in old_points:
                for z in intersections(centre, q):
                    add(z)
        sizes.append(len(points))
    adjacency = [set() for _ in points]
    edge_count = 0
    minimum_nonedge_error = 1.0
    for a in range(len(points)):
        for b in range(a + 1, len(points)):
            error = abs(abs(points[a] - points[b]) - 1)
            if error < 2e-7:
                adjacency[a].add(b)
                adjacency[b].add(a)
                edge_count += 1
            else:
                minimum_nonedge_error = min(minimum_nonedge_error, error)
    return points, adjacency, sizes, edge_count, minimum_nonedge_error


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", type=int, default=2)
    parser.add_argument("--node-limit", type=int, default=5_000_000)
    args = parser.parse_args()
    omega = cmath.exp(1j * math.pi / 3)
    rho = (5 + 1j * math.sqrt(11)) / 6
    directions = [omega**k for k in range(6)] + [rho * omega**k for k in range(6)]
    natural = (0, 1, 6, 7)
    cases = [natural] + [case for case in combinations(range(12), 4) if case != natural]
    summary = {"cases": 0, "colour4": 0, "noncolour4": 0, "unknown": 0,
               "over508": 0, "maximum_vertices": 0, "maximum_edges": 0,
               "minimum_nonedge_error": 1.0, "first_noncolour4": None}
    started = time.monotonic()
    for case_index, case in enumerate(cases):
        points, adjacency, sizes, edge_count, separation = support(
            [directions[i] for i in case], directions, args.depth
        )
        summary["cases"] += 1
        summary["maximum_vertices"] = max(summary["maximum_vertices"], len(points))
        summary["maximum_edges"] = max(summary["maximum_edges"], edge_count)
        summary["minimum_nonedge_error"] = min(summary["minimum_nonedge_error"], separation)
        if len(points) > 508:
            summary["over508"] += 1
        try:
            colouring, nodes = dsatur(adjacency, 4, args.node_limit)
        except RuntimeError:
            summary["unknown"] += 1
            continue
        if colouring is None:
            summary["noncolour4"] += 1
            row = {"status": "NONCOLOUR4_PROVISIONAL", "case_index": case_index,
                   "case": case, "sizes": sizes, "vertices": len(points),
                   "edges": edge_count, "nodes4": nodes}
            summary["first_noncolour4"] = row
            print(json.dumps(row, sort_keys=True), flush=True)
            break
        if any(colouring[v] == colouring[w] for v in range(len(points)) for w in adjacency[v]):
            raise ValueError("invalid four-colouring")
        summary["colour4"] += 1
        if (case_index + 1) % 50 == 0:
            print(json.dumps({"progress": case_index + 1,
                              "elapsed": round(time.monotonic() - started, 2),
                              "maximum_vertices": summary["maximum_vertices"],
                              "unknown": summary["unknown"]}, sort_keys=True), flush=True)
    summary["seconds"] = round(time.monotonic() - started, 3)
    summary["depth"] = args.depth
    print(json.dumps(summary, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()

