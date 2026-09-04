#!/usr/bin/env python3
"""Solver-free verifier for the six-bridge Parts augmentation closure."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
from pathlib import Path


BASIS = 8
PRIMES = (3, 5, 11)
SCALE = 96
BASE_SIZE = 509
TOTAL_SIZE = 515
EXPECTED_POINTS_SHA256 = "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50"
EXPECTED_BASE_EDGE_SHA256 = "5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c"
EXPECTED_BASE_CERTIFICATE_SHA256 = "d354f9629c41639168b80fc1aa6feb6e4187dd37dee7efcb83b4ef6ebe68d16c"
EXPECTED_EDGE_SHA256 = "f665c9a30ed9e8691a0c2ffceb32bbe47e369ae74491b1aa2bba9e44496df20d"
BRIDGE_COORDINATES = [
    [[0, 0, 0, 0, 0, 0, 0, 0], [0, -16, 0, 0, 48, 0, 0, 0]],
    [[0, 0, 0, 0, 0, 0, 0, 0], [0, 16, 0, 0, 48, 0, 0, 0]],
    [[24, 0, 0, 0, 0, 24, 0, 0], [0, -8, 0, 0, -24, 0, 0, 0]],
    [[-24, 0, 0, 0, 0, -24, 0, 0], [0, -8, 0, 0, -24, 0, 0, 0]],
    [[-24, 0, 0, 0, 0, 24, 0, 0], [0, 8, 0, 0, -24, 0, 0, 0]],
    [[24, 0, 0, 0, 0, -24, 0, 0], [0, 8, 0, 0, -24, 0, 0, 0]],
]
BRIDGE_NEIGHBORS = [
    [40, 51, 151, 168, 217, 220, 475],
    [149, 170, 262, 273, 298, 303, 429],
    [154, 157, 265, 266, 299, 300, 431],
    [162, 165, 269, 270, 301, 302, 433],
    [43, 44, 152, 159, 218, 477],
    [47, 48, 160, 167, 219, 479],
]

Field = tuple[int, ...]
Point = tuple[Field, Field]
Edge = tuple[int, int]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def field_multiply(left: Field, right: Field) -> Field:
    result = [0] * BASIS
    for i, a in enumerate(left):
        if not a:
            continue
        for j, b in enumerate(right):
            if not b:
                continue
            factor = 1
            for bit, prime in enumerate(PRIMES):
                if (i & j) & (1 << bit):
                    factor *= prime
            result[i ^ j] += factor * a * b
    return tuple(result)


def squared_distance(left: Point, right: Point) -> Field:
    dx = tuple(a - b for a, b in zip(left[0], right[0], strict=True))
    dy = tuple(a - b for a, b in zip(left[1], right[1], strict=True))
    xx = field_multiply(dx, dx)
    yy = field_multiply(dy, dy)
    return tuple(a + b for a, b in zip(xx, yy, strict=True))


def read_points(path: Path) -> list[Point]:
    if sha256(path) != EXPECTED_POINTS_SHA256:
        raise ValueError("unexpected points.tsv SHA-256")
    points = []
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        values = tuple(map(int, line.split()))
        if len(values) != 2 * BASIS:
            raise ValueError("point row does not have 16 coefficients")
        points.append((values[:BASIS], values[BASIS:]))
    if len(points) != BASE_SIZE or len(set(points)) != BASE_SIZE:
        raise AssertionError("expected 509 distinct Parts points")
    return points


def build_edges(points: list[Point]) -> list[Edge]:
    unit = (SCALE * SCALE,) + (0,) * (BASIS - 1)
    return [
        (i, j)
        for i in range(len(points))
        for j in range(i + 1, len(points))
        if squared_distance(points[i], points[j]) == unit
    ]


def edge_digest(edges: list[Edge]) -> str:
    return hashlib.sha256("".join(f"{u} {v}\n" for u, v in edges).encode("ascii")).hexdigest()


def unpack_colors(payload: bytes, count: int) -> list[int]:
    expected_bytes = (count + 3) // 4
    if len(payload) != expected_bytes:
        raise ValueError("packed coloring has the wrong byte length")
    colors = [(payload[index // 4] >> (2 * (index % 4))) & 3 for index in range(count)]
    if count % 4 and payload[-1] >> (2 * (count % 4)):
        raise ValueError("nonzero padding bits in packed coloring")
    return colors


def check_coloring(colors: dict[int, int], edges: list[Edge]) -> int:
    checks = 0
    for u, v in edges:
        if u in colors and v in colors:
            if colors[u] == colors[v]:
                raise AssertionError(f"monochromatic edge {(u, v)}")
            checks += 1
    return checks


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?", type=Path, default=Path(__file__).with_name("certificate.json"))
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    root = here.parent
    points_path = root / "hadwiger_nelson_parts509_completion_census_degree9" / "points.tsv"
    criticality_path = root / "hadwiger_nelson_parts509_criticality" / "certificate.json"
    if sha256(criticality_path) != EXPECTED_BASE_CERTIFICATE_SHA256:
        raise ValueError("unexpected Parts criticality certificate SHA-256")
    criticality = json.loads(criticality_path.read_text(encoding="utf-8"))
    if criticality["edge_sha256"] != EXPECTED_BASE_EDGE_SHA256:
        raise ValueError("Parts criticality edge digest mismatch")

    certificate = json.loads(args.certificate.read_text(encoding="utf-8"))
    expected_metadata = {
        "format": "parts509-six-bridge-augmentation-minimum-v1",
        "scale": SCALE,
        "basis_radicands": [1, 3, 5, 15, 11, 33, 55, 165],
        "base_vertices": BASE_SIZE,
        "bridge_vertices": 6,
        "vertices": TOTAL_SIZE,
        "edges": 2482,
        "edge_sha256": EXPECTED_EDGE_SHA256,
        "bridge_coordinates_scaled96": BRIDGE_COORDINATES,
        "bridge_neighbors": BRIDGE_NEIGHBORS,
        "bridge_degrees": [7, 7, 7, 7, 6, 6],
        "bridge_internal_edges": [],
        "coloring_rows": BASE_SIZE,
        "coloring_row_length": TOTAL_SIZE - 1,
        "minimum_non_four_colorable_order": BASE_SIZE,
        "augmentation_subsets_closed": 64,
    }
    if any(certificate.get(key) != value for key, value in expected_metadata.items()):
        raise AssertionError("certificate metadata mismatch")

    points = read_points(points_path)
    bridges = [tuple(tuple(coordinate) for coordinate in point) for point in BRIDGE_COORDINATES]
    points.extend(bridges)
    if len(points) != TOTAL_SIZE or len(set(points)) != TOTAL_SIZE:
        raise AssertionError("bridge augmentation point census mismatch")
    edges = build_edges(points)
    digest = edge_digest(edges)
    if len(edges) != 2482 or digest != EXPECTED_EDGE_SHA256:
        raise AssertionError("bridge augmentation edge census mismatch")
    base_edges = [(u, v) for u, v in edges if v < BASE_SIZE]
    if len(base_edges) != 2442 or edge_digest(base_edges) != EXPECTED_BASE_EDGE_SHA256:
        raise AssertionError("base induced graph mismatch")
    adjacency = [[] for _ in points]
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    if [adjacency[BASE_SIZE + index] for index in range(6)] != BRIDGE_NEIGHBORS:
        raise AssertionError("bridge-neighbor lists mismatch")
    if any(neighbor >= BASE_SIZE for row in BRIDGE_NEIGHBORS for neighbor in row):
        raise AssertionError("unexpected bridge-internal edge")

    row_length = TOTAL_SIZE - 1
    row_bytes = (row_length + 3) // 4
    payload = base64.b64decode(certificate["base_deletion_colorings_base64"], validate=True)
    if len(payload) != BASE_SIZE * row_bytes:
        raise AssertionError("deletion-coloring payload length mismatch")
    coloring_checks = 0
    for deleted in range(BASE_SIZE):
        row = payload[deleted * row_bytes : (deleted + 1) * row_bytes]
        packed_colors = unpack_colors(row, row_length)
        active = [vertex for vertex in range(TOTAL_SIZE) if vertex != deleted]
        coloring_checks += check_coloring(dict(zip(active, packed_colors, strict=True)), edges)

    # If an induced non-4-colourable subgraph omitted a Parts vertex v, it
    # would be a subgraph of the explicitly coloured graph (P union B)-v.
    # Hence it contains all 509 Parts vertices. Conversely those vertices
    # induce the certified non-4-colourable Parts graph. Restricting any row
    # to any subset of the six bridges proves the same statement for all 64
    # augmentation subsets.
    summary = {
        "all_checks": True,
        "vertices": len(points),
        "edges": len(edges),
        "base_edges": len(base_edges),
        "bridge_edges_to_base": len(edges) - len(base_edges),
        "bridge_degrees": [len(adjacency[BASE_SIZE + index]) for index in range(6)],
        "bridge_internal_edges": 0,
        "base_deletion_colorings": BASE_SIZE,
        "coloring_edge_checks": coloring_checks,
        "augmentation_subsets_closed": 64,
        "minimum_non_four_colorable_order": BASE_SIZE,
        "edge_sha256": digest,
    }
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
