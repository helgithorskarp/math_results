#!/usr/bin/env python3
"""Search mixed exact Moser-phase direction sumsets for a 5-colour signal.

For phase cosets S in <rho,eta>/U, let D be their sixfold U-orbits and build
X={0} union D union (D+D).  Here rho=(5+i*sqrt(11))/6, eta=exp(pi*i/6),
and U=<exp(pi*i/3)>.  Hence every searched point has an exact realization in
Q(sqrt(3),sqrt(11),i).  Floating point only discovers coincidences and unit
edges in this screening program.  A non-4-colourable hit is provisional until
the same phase set is rebuilt by the exact arithmetic checker.
"""

from __future__ import annotations

import argparse
from itertools import combinations
import json
import math
import time

from scratch_four_circle_moser_layers import dsatur


def phase(label, rho, eta):
    k, e = label
    return rho**k * eta**e


def support(labels):
    omega = complex(0.5, math.sqrt(3) / 2)
    rho = complex(5 / 6, math.sqrt(11) / 6)
    eta = complex(math.sqrt(3) / 2, 0.5)
    directions = []
    for label in labels:
        p = phase(label, rho, eta)
        directions.extend(p * omega**j for j in range(6))
    lookup, points = {}, []

    def add(z):
        key = (round(z.real * 10**9), round(z.imag * 10**9))
        if key not in lookup:
            lookup[key] = len(points)
            points.append(z)

    add(0j)
    for z in directions:
        add(z)
    for a in directions:
        for b in directions:
            add(a + b)
    adjacency = [set() for _ in points]
    edges = []
    minimum_nonedge_error = 1.0
    for a in range(len(points)):
        for b in range(a + 1, len(points)):
            error = abs(abs(points[a] - points[b]) - 1)
            if error < 2e-7:
                adjacency[a].add(b)
                adjacency[b].add(a)
                edges.append((a, b))
            else:
                minimum_nonedge_error = min(minimum_nonedge_error, error)
    return points, edges, adjacency, minimum_nonedge_error


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-exponent", type=int, default=5)
    parser.add_argument("--phase-count", type=int, choices=(3, 4, 5), default=4)
    parser.add_argument("--node-limit", type=int, default=5_000_000)
    args = parser.parse_args()
    origin = (0, 0)
    available = [(k, e) for k in range(-args.maximum_exponent, args.maximum_exponent + 1)
                 for e in range(2) if (k, e) != origin]
    cases = combinations(available, args.phase_count - 1)
    summary = {"cases": 0, "colour4": 0, "noncolour4": 0, "unknown": 0,
               "over508": 0, "maximum_vertices": 0, "maximum_edges": 0,
               "densest": None, "minimum_nonedge_error": 1.0,
               "first_noncolour4": None}
    started = time.monotonic()
    for case_index, tail in enumerate(cases):
        labels = (origin,) + tail
        points, edges, adjacency, separation = support(labels)
        summary["cases"] += 1
        summary["maximum_vertices"] = max(summary["maximum_vertices"], len(points))
        summary["minimum_nonedge_error"] = min(summary["minimum_nonedge_error"], separation)
        if len(edges) > summary["maximum_edges"]:
            summary["maximum_edges"] = len(edges)
            summary["densest"] = {"labels": labels, "vertices": len(points), "edges": len(edges)}
        if len(points) > 508:
            summary["over508"] += 1
            continue
        try:
            colouring, nodes = dsatur(adjacency, 4, args.node_limit)
        except RuntimeError:
            summary["unknown"] += 1
            continue
        if colouring is None:
            summary["noncolour4"] += 1
            row = {"status": "NONCOLOUR4_PROVISIONAL", "case_index": case_index,
                   "labels": labels, "vertices": len(points), "edges": len(edges),
                   "nodes4": nodes, "minimum_nonedge_error": separation}
            summary["first_noncolour4"] = row
            print(json.dumps(row, sort_keys=True), flush=True)
            break
        if not all(colouring[a] != colouring[b] for a, b in edges):
            raise ValueError("invalid four-colouring")
        summary["colour4"] += 1
        if (case_index + 1) % 100 == 0:
            print(json.dumps({"progress": case_index + 1,
                              "elapsed": round(time.monotonic() - started, 2),
                              "maximum_edges": summary["maximum_edges"],
                              "unknown": summary["unknown"]}, sort_keys=True), flush=True)
    summary["seconds"] = round(time.monotonic() - started, 3)
    summary["phase_count"] = args.phase_count
    summary["maximum_exponent"] = args.maximum_exponent
    print(json.dumps(summary, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()

