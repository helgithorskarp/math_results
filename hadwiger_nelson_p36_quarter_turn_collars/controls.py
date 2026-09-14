#!/usr/bin/env python3
"""Alternate interface construction and corruption controls."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import verify


HERE = Path(__file__).resolve().parent
Vec = tuple[int, int, int, int]


class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def join(self, x: int, y: int) -> None:
        x, y = self.find(x), self.find(y)
        if x != y:
            self.parent[x] = y


def interface_graph(c: Vec, patch_points: list[Vec], units: tuple[Vec, ...],
                    adjacent, opposite, internal):
    count = len(patch_points)
    relative_adjacent = verify.minus(c, verify.quarter(c))
    relative_opposite = verify.plus(c, c)
    adjacent_collisions = adjacent.get(relative_adjacent, ())
    adjacent_edges = [pair for displacement in units
                      for pair in adjacent.get(
                          verify.plus(relative_adjacent, displacement), ())]
    opposite_collisions = opposite.get(relative_opposite, ())
    opposite_edges = [pair for displacement in units
                      for pair in opposite.get(
                          verify.plus(relative_opposite, displacement), ())]

    uf = UnionFind(4 * count)

    def formal(layer: int, point: int) -> int:
        return layer * count + point

    formal_edges = []
    for layer in range(4):
        for i, j in adjacent_collisions:
            uf.join(formal(layer, i), formal((layer + 1) % 4, j))
        for i, j in adjacent_edges:
            formal_edges.append((formal(layer, i), formal((layer + 1) % 4, j)))
        for i, j in internal:
            formal_edges.append((formal(layer, i), formal(layer, j)))
    for layer in range(2):
        for i, j in opposite_collisions:
            uf.join(formal(layer, i), formal(layer + 2, j))
        for i, j in opposite_edges:
            formal_edges.append((formal(layer, i), formal(layer + 2, j)))

    root_coordinate = {}
    for layer in range(4):
        for index, point in enumerate(patch_points):
            image = verify.plus(c, verify.quarter_power(
                verify.minus(point, c), layer))
            root = uf.find(formal(layer, index))
            if root in root_coordinate:
                verify.require(root_coordinate[root] == image,
                               "interface collision joins unequal points")
            else:
                root_coordinate[root] = image
    verify.require(len(set(root_coordinate.values())) == len(root_coordinate),
                   "interface construction missed a collision")
    physical = sorted(root_coordinate.values())
    where = {point: index for index, point in enumerate(physical)}
    root_index = {root: where[point] for root, point in root_coordinate.items()}
    edges = set()
    for x, y in formal_edges:
        x, y = root_index[uf.find(x)], root_index[uf.find(y)]
        verify.require(x != y, "unit edge collapsed in interface construction")
        edges.add((x, y) if x < y else (y, x))
    return physical, edges


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    labels, patch_points = verify.make_patch()
    units = verify.exact_unit_vectors()
    count = len(patch_points)
    adjacent = defaultdict(list)
    opposite = defaultdict(list)
    for i, p in enumerate(patch_points):
        for j, q in enumerate(patch_points):
            adjacent[verify.minus(p, verify.quarter(q))].append((i, j))
            opposite[verify.plus(p, q)].append((i, j))
    verify.require(len(adjacent) == count * count,
                   "adjacent anchor offsets are not injective")
    verify.require(set(map(len, adjacent.values())) == {1},
                   "an adjacent interface has multiple collisions")
    internal = []
    for i, p in enumerate(patch_points):
        for j in range(i + 1, count):
            if verify.squared_norm(verify.minus(p, patch_points[j])) == (16, 0):
                internal.append((i, j))
    verify.require(len(internal) == 342, "alternate P36 edge count changed")

    centers = [verify.center(p, q) for p in patch_points for q in patch_points]
    representatives = sorted({verify.canonical(c) for c in centers})
    stream = hashlib.sha256()
    for c in representatives:
        direct_points, direct_edges, _, _, _ = verify.physical_graph(
            c, patch_points, units)
        interface_points, interface_edges = interface_graph(
            c, patch_points, units, adjacent, opposite, internal)
        verify.require(interface_points == direct_points,
                       "interface/direct physical point mismatch")
        verify.require(interface_edges == direct_edges,
                       "interface/direct edge mismatch")
        stream.update(json.dumps(
            [list(c), len(direct_points), len(direct_edges)],
            separators=(",", ":")).encode())
        stream.update(b"\n")

    # Positive words, rather than the producer search, are the certificate.
    result = verify.verify(HERE / "colourings.json")
    payload = json.loads((HERE / "colourings.json").read_text())
    row = payload["certificates"][0]
    c = tuple(row["center"])
    points, edges, _, _, _ = verify.physical_graph(c, patch_points, units)
    bad = list(row["word"])
    x, y = next(iter(edges))
    bad[x] = bad[y]
    rejected_monochromatic_word = False
    try:
        verify.check_word("".join(bad), len(points), edges)
    except ValueError:
        rejected_monochromatic_word = True
    verify.require(rejected_monochromatic_word,
                   "monochromatic certificate corruption was accepted")

    output = {
        "status": "PASS",
        "direct_interface_orbits_compared": len(representatives),
        "adjacent_offset_buckets": len(adjacent),
        "opposite_sum_buckets": len(opposite),
        "interface_count_stream_sha256": stream.hexdigest(),
        "rejected_monochromatic_word": rejected_monochromatic_word,
        "verified_graph_stream_sha256": result["graph_stream_sha256"],
        "verified_colour_cover_sha256": result["colour_cover_sha256"],
    }
    if args.check_expected:
        expected = json.loads((HERE / "EXPECTED_CONTROLS.json").read_text())
        verify.require(output == expected,
                       "control output differs from EXPECTED_CONTROLS.json")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
