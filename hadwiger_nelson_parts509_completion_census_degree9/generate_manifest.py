#!/usr/bin/env python3
"""Generate an exact manifest of all numerically discovered unit-circle centers.

The numerical clustering is only a candidate generator.  Every emitted center
and neighbor set is recomputed in Q(sqrt(3),sqrt(5),sqrt(11)) exactly.  An
independent exhaustive triple count supplies the completeness certificate.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
PARTS = HERE.parent / "hadwiger_nelson_parts509_criticality"
PRIMES = (3, 5, 11)


def load_parts():
    path = PARTS / "parts509.py"
    spec = importlib.util.spec_from_file_location("parts509_manifest", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def f_neg(a):
    return tuple(-x for x in a)


def f_scale(a, scalar):
    return tuple(scalar * x for x in a)


def f_conjugate(a, sign_mask):
    return tuple(
        -coefficient if (basis_mask & sign_mask).bit_count() % 2 else coefficient
        for basis_mask, coefficient in enumerate(a)
    )


def f_inverse(parts, a):
    if a == parts.ZERO:
        raise ZeroDivisionError
    product = parts.ONE
    for sign_mask in range(1, 8):
        product = parts.f_mul(product, f_conjugate(a, sign_mask))
    norm = parts.f_mul(a, product)
    if any(norm[index] for index in range(1, 8)) or norm[0] == 0:
        raise ArithmeticError(f"failed to compute field norm: {norm}")
    return f_scale(product, 1 / norm[0])


def f_div(parts, a, b):
    return parts.f_mul(a, f_inverse(parts, b))


def real_value(x):
    return sum(
        float(coefficient)
        * math.sqrt(math.prod(PRIMES[bit] for bit in range(3) if mask & (1 << bit)))
        for mask, coefficient in enumerate(x)
    )


def candidate_clusters(points):
    clusters = defaultdict(set)
    for i, (x1, y1) in enumerate(points):
        for j in range(i + 1, len(points)):
            x2, y2 = points[j]
            dx, dy = x2 - x1, y2 - y1
            d2 = dx * dx + dy * dy
            if d2 > 4.0 + 1e-11:
                continue
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            if abs(d2 - 4.0) < 1e-11:
                centers = [(mx, my)]
            else:
                h = math.sqrt(max(0.0, 1.0 - d2 / 4.0))
                d = math.sqrt(d2)
                px, py = -dy / d, dx / d
                centers = [(mx + h * px, my + h * py), (mx - h * px, my - h * py)]
            for qx, qy in centers:
                clusters[(round(qx, 9), round(qy, 9))].update((i, j))
    return [key for key, vertices in clusters.items() if len(vertices) >= 3]


def exact_center(parts, points, triple):
    p0, p1, p2 = (points[index] for index in triple)
    ax = parts.f_sub(p1[0], p0[0])
    ay = parts.f_sub(p1[1], p0[1])
    bx = parts.f_sub(p2[0], p0[0])
    by = parts.f_sub(p2[1], p0[1])
    r1 = parts.f_sub(parts.f_add(parts.f_sq(p1[0]), parts.f_sq(p1[1])),
                     parts.f_add(parts.f_sq(p0[0]), parts.f_sq(p0[1])))
    r2 = parts.f_sub(parts.f_add(parts.f_sq(p2[0]), parts.f_sq(p2[1])),
                     parts.f_add(parts.f_sq(p0[0]), parts.f_sq(p0[1])))
    determinant = parts.f_sub(parts.f_mul(ax, by), parts.f_mul(ay, bx))
    denominator = f_scale(determinant, Fraction(2))
    qx = f_div(parts, parts.f_sub(parts.f_mul(r1, by), parts.f_mul(ay, r2)), denominator)
    qy = f_div(parts, parts.f_sub(parts.f_mul(ax, r2), parts.f_mul(r1, bx)), denominator)
    return qx, qy


def serialize_field(value):
    return [str(coefficient) for coefficient in value]


def serialize_point(point):
    return [serialize_field(point[0]), serialize_field(point[1])]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--points-output", type=Path)
    args = parser.parse_args()
    parts = load_parts()
    points = parts.parse_points(PARTS / "parts509.vtx")
    if args.points_output is not None:
        with args.points_output.open("w") as output:
            output.write("# basis=1,sqrt3,sqrt5,sqrt15,sqrt11,sqrt33,sqrt55,sqrt165 scale=96\n")
            for point in points:
                scaled = [coefficient * 96 for coordinate in point for coefficient in coordinate]
                if any(value.denominator != 1 for value in scaled):
                    raise ValueError("coordinate denominator does not divide 96")
                output.write(" ".join(str(value.numerator) for value in scaled) + "\n")
    floats = [(real_value(x), real_value(y)) for x, y in points]
    clusters = candidate_clusters(floats)
    exact_candidates = {}
    for number, (qx_float, qy_float) in enumerate(clusters, 1):
        approximate_neighbors = [
            index
            for index, (x, y) in enumerate(floats)
            if abs((x - qx_float) ** 2 + (y - qy_float) ** 2 - 1.0) < 1e-6
        ]
        if len(approximate_neighbors) < 3:
            raise ValueError("cluster lost its third approximate neighbor")
        center = exact_center(parts, points, approximate_neighbors[:3])
        exact_neighbors = tuple(
            index
            for index, point in enumerate(points)
            if parts.squared_distance(center, point) == parts.ONE
        )
        if len(exact_neighbors) < 3:
            raise ValueError(f"spurious numerical center {number}: {center}")
        exact_candidates[center] = exact_neighbors
        if number % 100 == 0:
            print(f"processed={number}/{len(clusters)}", file=sys.stderr)
    if len(exact_candidates) != len(clusters):
        raise ValueError(
            f"numerical clustering duplicated exact centers: {len(clusters)} -> {len(exact_candidates)}"
        )
    point_indices = {point: index for index, point in enumerate(points)}
    rows = []
    for center, neighbors in exact_candidates.items():
        rows.append(
            {
                "center": serialize_point(center),
                "degree": len(neighbors),
                "existing_vertex": point_indices.get(center),
                "neighbors": list(neighbors),
            }
        )
    rows.sort(
        key=lambda row: (
            -row["degree"],
            row["existing_vertex"] is None,
            -1 if row["existing_vertex"] is None else row["existing_vertex"],
            row["center"],
        )
    )
    histogram = defaultdict(int)
    external_histogram = defaultdict(int)
    triple_count = 0
    for row in rows:
        histogram[row["degree"]] += 1
        if row["existing_vertex"] is None:
            external_histogram[row["degree"]] += 1
        triple_count += math.comb(row["degree"], 3)
    document = {
        "schema": "parts509-unit-circle-centers-v1",
        "basis_radicands": [1, 3, 5, 15, 11, 33, 55, 165],
        "base_vertex_count": len(points),
        "center_count": len(rows),
        "unit_circle_triple_count": triple_count,
        "degree_histogram": {str(k): histogram[k] for k in sorted(histogram)},
        "external_degree_histogram": {
            str(k): external_histogram[k] for k in sorted(external_histogram)
        },
        "centers": rows,
    }
    args.output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: document[key] for key in document if key != "centers"}, indent=2))


if __name__ == "__main__":
    main()
