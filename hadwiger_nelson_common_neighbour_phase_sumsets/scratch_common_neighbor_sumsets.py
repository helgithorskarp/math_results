#!/usr/bin/env python3
"""Exact search of four-owner common-neighbour direction sumsets.

For a unit-direction set D, choose four centres C subset D around the common
neighbour 0 and form X={0} union C union (C+D).  All coincidences and every
unit pair are decided exactly in Q(sqrt(3),sqrt(11)).  Deterministic DSATUR
tests three and four colours.  Exploratory UNSAT outcomes require a separate
certificate before they can support a claim.
"""

from __future__ import annotations

import argparse
from itertools import combinations
import json
import time

from scratch_four_circle_moser_layers import Q, cadd, cmul, csub, dsatur, norm2


def direction_pool(mode):
    zero, one = Q(), Q([1])
    s3, s11 = Q([0, 1]), Q([0, 0, 1])
    omega = (one / 2, s3 / 2)
    rho = (Q([5]) / 6, s11 / 6)
    ii = (zero, one)
    rho_inverse = (rho[0], -rho[1])
    phases = [(one, zero), rho]
    if mode in ("four", "six"):
        phases += [ii, cmul(ii, rho)]
    if mode == "six":
        phases += [rho_inverse, cmul(ii, rho_inverse)]
    rotations = [(one, zero)]
    for _ in range(5):
        rotations.append(cmul(rotations[-1], omega))
    directions = []
    phase_orbit = []
    seen = set()
    for phase_index, phase in enumerate(phases):
        for step, rotation in enumerate(rotations):
            value = cmul(phase, rotation)
            if value not in seen:
                seen.add(value)
                directions.append(value)
                phase_orbit.append((phase_index, step))
    return directions, phase_orbit


def graph_for_centres(centres, directions):
    zero = (Q(), Q())
    points, addresses, index = [], [], {}

    def add(point, address):
        if point not in index:
            index[point] = len(points)
            points.append(point)
            addresses.append([])
        addresses[index[point]].append(address)

    add(zero, ["common"])
    for owner, centre in enumerate(centres):
        add(centre, ["centre", owner])
        for direction_index, direction in enumerate(directions):
            add(cadd(centre, direction), ["rim", owner, direction_index])
    edges = []
    adjacency = [set() for _ in points]
    unit = Q([1])
    for a in range(len(points)):
        for b in range(a + 1, len(points)):
            if norm2(csub(points[a], points[b])) == unit:
                edges.append((a, b))
                adjacency[a].add(b)
                adjacency[b].add(a)
    return points, addresses, edges, adjacency


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("two", "four", "six"), default="two")
    parser.add_argument("--node-limit", type=int, default=2_000_000)
    parser.add_argument("--maximum-cases", type=int, default=0)
    args = parser.parse_args()
    directions, phase_orbit = direction_pool(args.mode)
    natural = tuple(phase_orbit.index(value) for value in ((0, 0), (0, 1), (1, 0), (1, 1)))
    cases = [natural] + [case for case in combinations(range(len(directions)), 4) if case != natural]
    if args.maximum_cases:
        cases = cases[:args.maximum_cases]
    summary = {"cases": 0, "colour4": 0, "noncolour4": 0, "colour3": 0, "noncolour3": 0,
               "unknown": 0, "maximum_vertices": 0, "maximum_edges": 0, "first_noncolour4": None,
               "densest": None}
    started = time.monotonic()
    for case_index, case in enumerate(cases):
        points, addresses, edges, adjacency = graph_for_centres([directions[i] for i in case], directions)
        summary["cases"] += 1
        summary["maximum_vertices"] = max(summary["maximum_vertices"], len(points))
        if len(edges) > summary["maximum_edges"]:
            summary["maximum_edges"] = len(edges)
            summary["densest"] = {"case": case, "vertices": len(points), "edges": len(edges)}
        try:
            four, nodes4 = dsatur(adjacency, 4, args.node_limit)
        except RuntimeError:
            summary["unknown"] += 1
            continue
        if four is None:
            summary["noncolour4"] += 1
            row = {"case_index": case_index, "case": case, "labels": [phase_orbit[i] for i in case],
                   "vertices": len(points), "edges": len(edges), "nodes4": nodes4,
                   "status": "NONCOLOUR4_PROVISIONAL"}
            print(json.dumps(row, sort_keys=True), flush=True)
            summary["first_noncolour4"] = row
            break
        summary["colour4"] += 1
        if not all(four[a] != four[b] for a, b in edges):
            raise ValueError("invalid four-colouring")
        try:
            three, nodes3 = dsatur(adjacency, 3, args.node_limit)
        except RuntimeError:
            summary["unknown"] += 1
            continue
        if three is None:
            summary["noncolour3"] += 1
        else:
            summary["colour3"] += 1
            if not all(three[a] != three[b] for a, b in edges):
                raise ValueError("invalid three-colouring")
        if case_index == 0:
            print(json.dumps({"natural_case": case, "labels": [phase_orbit[i] for i in case],
                              "vertices": len(points), "edges": len(edges),
                              "colour3": three is not None, "nodes3": nodes3,
                              "colour4": True, "nodes4": nodes4}, sort_keys=True), flush=True)
        if (case_index + 1) % 100 == 0:
            print(json.dumps({"progress": case_index + 1, "elapsed": round(time.monotonic() - started, 2),
                              "noncolour3": summary["noncolour3"], "unknown": summary["unknown"]}, sort_keys=True), flush=True)
    summary["seconds"] = round(time.monotonic() - started, 3)
    summary["mode"] = args.mode
    summary["directions"] = len(directions)
    print(json.dumps(summary, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()

