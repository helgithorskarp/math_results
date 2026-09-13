#!/usr/bin/env python3
"""Geometry-first closure around the four common-neighbour Moser centres.

This is a candidate generator, not a certificate.  Starting from the exact
two-phase support X={0} union C union (C+D), add every intersection of an
owner unit circle with a unit circle about a current point.  Thus every new
point is physically realized when generated.  Floating point is used only to
deduplicate and discover the finite graph; a positive candidate must later be
rebuilt from its construction DAG and certified exactly.
"""

from __future__ import annotations

import argparse
import cmath
import json
import math
import time

from scratch_four_circle_moser_layers import dsatur


def key(z, scale=10**10):
    return round(z.real * scale), round(z.imag * scale)


def intersections(a, b):
    delta = b - a
    distance = abs(delta)
    if distance < 1e-12 or distance > 2 + 1e-10:
        return []
    midpoint = (a + b) / 2
    height2 = max(0.0, 1 - distance * distance / 4)
    offset = (delta / distance) * 1j * math.sqrt(height2)
    if abs(offset) < 1e-12:
        return [midpoint]
    return [midpoint + offset, midpoint - offset]


def initial_geometry():
    omega = cmath.exp(1j * math.pi / 3)
    rho = (5 + 1j * math.sqrt(11)) / 6
    rotations = [omega**k for k in range(6)]
    directions = rotations + [rho * value for value in rotations]
    centres = [1 + 0j, omega, rho, rho * omega]
    points, sources, lookup = [], [], {}

    def add(z, source):
        k = key(z)
        if k not in lookup:
            lookup[k] = len(points)
            points.append(z)
            sources.append([])
        sources[lookup[k]].append(source)
        return lookup[k]

    add(0j, ["common"])
    for owner, centre in enumerate(centres):
        add(centre, ["centre", owner])
        for direction_index, direction in enumerate(directions):
            add(centre + direction, ["rim", owner, direction_index])
    return centres, points, sources, lookup, add


def graph(points):
    adjacency = [set() for _ in points]
    edges = []
    near_misses = []
    for a in range(len(points)):
        for b in range(a + 1, len(points)):
            error = abs(abs(points[a] - points[b]) - 1)
            if error < 2e-8:
                edges.append((a, b))
                adjacency[a].add(b)
                adjacency[b].add(a)
            elif error < 2e-6:
                near_misses.append((error, a, b))
    return edges, adjacency, sorted(near_misses)[:10]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", type=int, default=1)
    parser.add_argument("--node-limit", type=int, default=20_000_000)
    args = parser.parse_args()
    centres, points, sources, lookup, add = initial_geometry()
    depth_sizes = [len(points)]
    for depth in range(args.depth):
        old_points = list(points)
        for owner, centre in enumerate(centres):
            for q_index, q in enumerate(old_points):
                for branch, z in enumerate(intersections(centre, q)):
                    add(z, ["intersection", depth + 1, owner, q_index, branch])
        depth_sizes.append(len(points))
        if len(points) > 2000:
            break
    started = time.monotonic()
    edges, adjacency, near_misses = graph(points)
    row = {
        "depth_sizes": depth_sizes,
        "vertices": len(points),
        "edges": len(edges),
        "maximum_degree": max(map(len, adjacency)),
        "multi_source_vertices": sum(len(value) > 1 for value in sources),
        "near_misses": near_misses,
    }
    try:
        four, nodes4 = dsatur(adjacency, 4, args.node_limit)
    except RuntimeError:
        four, nodes4 = "unknown", args.node_limit
    row["nodes4"] = nodes4
    if four == "unknown":
        row["colour4"] = "unknown"
    elif four is None:
        row["colour4"] = False
        row["status"] = "NONCOLOUR4_PROVISIONAL"
    else:
        if not all(four[a] != four[b] for a, b in edges):
            raise ValueError("invalid four-colouring")
        row["colour4"] = True
        row["colour_word"] = "".join(str(value) for value in four)
    row["colour_seconds"] = round(time.monotonic() - started, 3)
    print(json.dumps(row, sort_keys=True))


if __name__ == "__main__":
    main()

