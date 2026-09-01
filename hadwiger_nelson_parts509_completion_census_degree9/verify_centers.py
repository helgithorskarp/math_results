#!/usr/bin/env python3
"""Solver-free exact verifier for the Parts-509 unit-circle center census."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path


BASIS = 8
PRIMES = (3, 5, 11)
RADICANDS = (1, 3, 5, 15, 11, 33, 55, 165)
SCALE = 96
ZERO = (Fraction(0),) * BASIS
ONE = (Fraction(1),) + (Fraction(0),) * (BASIS - 1)


def field_add(left, right):
    return tuple(a + b for a, b in zip(left, right, strict=True))


def field_subtract(left, right):
    return tuple(a - b for a, b in zip(left, right, strict=True))


def field_multiply(left, right):
    result = [Fraction(0)] * BASIS
    for i, a in enumerate(left):
        if not a:
            continue
        for j, b in enumerate(right):
            if not b:
                continue
            shared = i & j
            factor = 1
            for bit, prime in enumerate(PRIMES):
                if shared & (1 << bit):
                    factor *= prime
            result[i ^ j] += a * b * factor
    return tuple(result)


def squared_distance(left, right):
    dx = field_subtract(left[0], right[0])
    dy = field_subtract(left[1], right[1])
    return field_add(field_multiply(dx, dx), field_multiply(dy, dy))


def parse_field(row):
    if len(row) != BASIS:
        raise ValueError("field element does not have eight coefficients")
    return tuple(Fraction(value) for value in row)


def parse_center(row):
    if len(row) != 2:
        raise ValueError("point does not have two coordinates")
    return parse_field(row[0]), parse_field(row[1])


def read_points(path):
    points = []
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        if not line or line.startswith("#"):
            continue
        values = [int(value) for value in line.split()]
        if len(values) != 2 * BASIS:
            raise ValueError(f"point line {line_number} does not have 16 integers")
        coordinates = []
        for offset in (0, BASIS):
            coordinates.append(tuple(Fraction(value, SCALE) for value in values[offset : offset + BASIS]))
        points.append(tuple(coordinates))
    if len(points) != 509 or len(set(points)) != 509:
        raise ValueError("point manifest must contain 509 distinct points")
    return points


def check_source_bridge(points, source_directory):
    module_path = source_directory / "parts509.py"
    coordinate_path = source_directory / "parts509.vtx"
    spec = importlib.util.spec_from_file_location("parts509_source_bridge", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {module_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    parsed = module.parse_points(coordinate_path)
    if parsed != points:
        raise ValueError("integer point manifest differs from the parsed Parts coordinate source")


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("points", type=Path)
    parser.add_argument("centers", type=Path)
    parser.add_argument(
        "--source-directory",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "hadwiger_nelson_parts509_criticality",
    )
    args = parser.parse_args()
    points = read_points(args.points)
    check_source_bridge(points, args.source_directory)
    document = json.loads(args.centers.read_text())
    if document.get("schema") != "parts509-unit-circle-centers-v1":
        raise ValueError("unexpected center-manifest schema")
    if document.get("basis_radicands") != list(RADICANDS):
        raise ValueError("unexpected field basis")
    if document.get("base_vertex_count") != len(points):
        raise ValueError("wrong base-vertex count")
    rows = document.get("centers")
    if not isinstance(rows, list) or len(rows) != document.get("center_count"):
        raise ValueError("wrong center count")
    point_indices = {point: index for index, point in enumerate(points)}
    centers = []
    degree_histogram = Counter()
    external_histogram = Counter()
    unit_triples_accounted_for = 0
    incidence_checks = 0
    for row_number, row in enumerate(rows):
        center = parse_center(row["center"])
        if center in centers:
            raise ValueError(f"duplicate center in row {row_number}")
        centers.append(center)
        exact_neighbors = [
            vertex
            for vertex, point in enumerate(points)
            if squared_distance(center, point) == ONE
        ]
        incidence_checks += len(points)
        if exact_neighbors != row.get("neighbors"):
            raise ValueError(f"neighbor list mismatch in row {row_number}")
        degree = len(exact_neighbors)
        if degree != row.get("degree") or degree < 3:
            raise ValueError(f"degree mismatch in row {row_number}")
        existing_vertex = point_indices.get(center)
        if existing_vertex != row.get("existing_vertex"):
            raise ValueError(f"existing-vertex marker mismatch in row {row_number}")
        degree_histogram[degree] += 1
        if existing_vertex is None:
            external_histogram[degree] += 1
        unit_triples_accounted_for += math.comb(degree, 3)
    if len(set(centers)) != len(centers):
        raise ValueError("center manifest is not duplicate-free")
    if {point_indices[center] for center in centers if center in point_indices} != set(range(509)):
        raise ValueError("the manifest does not contain every Parts vertex as a center")
    expected_histogram = {str(key): degree_histogram[key] for key in sorted(degree_histogram)}
    expected_external = {str(key): external_histogram[key] for key in sorted(external_histogram)}
    if expected_histogram != document.get("degree_histogram"):
        raise ValueError("degree histogram mismatch")
    if expected_external != document.get("external_degree_histogram"):
        raise ValueError("external degree histogram mismatch")
    if unit_triples_accounted_for != document.get("unit_circle_triple_count"):
        raise ValueError("unit-circle triple accounting mismatch")
    external_maximum = max(external_histogram)
    if external_maximum != 10 or external_histogram[10] != 4:
        raise ValueError("unexpected external maximum degree or multiplicity")
    summary = {
        "all_checks": True,
        "parts_vertices": len(points),
        "centers_with_at_least_three_neighbors": len(centers),
        "existing_vertex_centers": len(points),
        "external_centers": len(centers) - len(points),
        "external_maximum_unit_neighbors": external_maximum,
        "external_maximizers": external_histogram[external_maximum],
        "external_degree_9_centers": external_histogram[9],
        "exact_incidence_checks": incidence_checks,
        "unit_circle_triples_accounted_for": unit_triples_accounted_for,
        "points_sha256": file_sha256(args.points),
        "centers_sha256": file_sha256(args.centers),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
