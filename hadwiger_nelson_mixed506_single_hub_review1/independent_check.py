#!/usr/bin/env python3
"""Independent exact audit of the mixed506 single-hub center catalogs.

This reviewer-owned checker imports no reviewed module.  It parses the pinned
Parts coordinates directly, verifies every generated center against every
component point, and independently exhausts every point triple using the
circumradius identity in Z[sqrt(33)].
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE_PINS = {
    159: "4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02",
    214: "97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f",
}
CATALOG_PINS = {
    "B": "98cb10340a4f234616022f680e7c86e988031c46a2f7486f419276e9795f2154",
    "V": "d9286e087f5d29b4f8115c66cf1440f2e2f6c6db26ed3bd84361332d65ed062a",
}
EXPECTED = {
    "B": {
        "vertices": 292,
        "scale": 72,
        "centers": 1173,
        "external": {3: 440, 4: 225, 5: 114, 6: 59, 7: 29, 8: 5, 9: 5, 10: 4},
        "all_triples": 4106980,
        "short_triples": 2680610,
        "unit_triples": 49302,
    },
    "V": {
        "vertices": 214,
        "scale": 12,
        "centers": 748,
        "external": {3: 256, 4: 130, 5: 88, 6: 36, 7: 12, 8: 4, 10: 8},
        "all_triples": 1610564,
        "short_triples": 950868,
        "unit_triples": 32792,
    },
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_source(order: int) -> list[tuple[int, int, int, int]]:
    path = ROOT / "hadwiger_nelson_nonmono159_214_lowden2" / f"points{order}.tsv"
    require(sha256(path) == SOURCE_PINS[order], "source-coordinate hash")
    points = []
    for line in path.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        values = tuple(map(int, line.split()))
        require(len(values) == 16, "coordinate width")
        require(all(values[index] == 0 for index in range(16)
                    if index not in (0, 5, 9, 12)), "coordinate subfield")
        points.append(tuple(values[index] for index in (0, 5, 9, 12)))
    require(len(points) == len(set(points)) == order, "source point count")
    return points


def components() -> dict[str, list[tuple[int, int, int, int]]]:
    A = read_source(159)
    V = read_source(214)
    scaled_A = [tuple(6 * value for value in point) for point in A]
    transformed_A = []
    for a, b, c, d in A:
        # Numerators at scale 72 after multiplication by (5+i*sqrt(11))/6.
        transformed_A.append((5 * a - 11 * d, 5 * b - c,
                              5 * c + 11 * b, 5 * d + a))
    B = list(dict.fromkeys(scaled_A + transformed_A))
    require(len(B) == 292, "inner-union cardinality")
    return {"B": B, "V": V}


def norm_coefficients(values: tuple[Fraction, Fraction, Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    a, b, c, d = values
    return a * a + 33 * b * b + 3 * c * c + 11 * d * d, 2 * (a * b + c * d)


def center_neighbors(center: tuple[Fraction, Fraction, Fraction, Fraction],
                     points: list[tuple[int, int, int, int]], scale: int) -> list[int]:
    result = []
    for index, point in enumerate(points):
        delta = tuple(Fraction(value, scale) - coordinate
                      for value, coordinate in zip(point, center))
        if norm_coefficients(delta) == (1, 0):
            result.append(index)
    return result


def mul_r(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return x[0] * y[0] + 33 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def add_r(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return x[0] + y[0], x[1] + y[1]


def sub_r(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return x[0] - y[0], x[1] - y[1]


def scale_r(x: tuple[int, int], factor: int) -> tuple[int, int]:
    return factor * x[0], factor * x[1]


def positive_r(x: tuple[int, int]) -> bool:
    a, b = x
    if b == 0:
        return a > 0
    if a >= 0 and b >= 0:
        return True
    if a <= 0 and b <= 0:
        return False
    if a > 0:
        return a * a > 33 * b * b
    return 33 * b * b > a * a


def squared_distance(p: tuple[int, int, int, int],
                     q: tuple[int, int, int, int]) -> tuple[int, int]:
    a, b, c, d = (x - y for x, y in zip(p, q))
    return a * a + 33 * b * b + 3 * c * c + 11 * d * d, 2 * (a * b + c * d)


def audit_component(name: str, points: list[tuple[int, int, int, int]],
                    catalog_path: Path) -> None:
    expected = EXPECTED[name]
    scale = expected["scale"]
    require(len(points) == expected["vertices"], "component size")
    require(sha256(catalog_path) == CATALOG_PINS[name], "catalog hash")
    rows = json.loads(catalog_path.read_text())
    require(len(rows) == expected["centers"], "catalog center count")

    actual_points = {tuple(Fraction(value, scale) for value in point) for point in points}
    centers = set()
    external_histogram = Counter()
    catalog_triples: set[tuple[int, int, int]] = set()
    for row in rows:
        center = tuple(Fraction(value) for value in row["point"])
        require(center not in centers, "duplicate center")
        centers.add(center)
        neighbors = center_neighbors(center, points, scale)
        require(neighbors == row["neighbors"] and len(neighbors) >= 3,
                "complete center-neighbor list")
        internal = center in actual_points
        require(internal == row["internal"], "internal-center flag")
        if not internal:
            external_histogram[len(neighbors)] += 1
        for triple in combinations(neighbors, 3):
            require(triple not in catalog_triples, "triple assigned to two centers")
            catalog_triples.add(triple)
    require(dict(sorted(external_histogram.items())) == expected["external"],
            "external degree histogram")
    require(len(catalog_triples) == expected["unit_triples"], "catalog triple multiplicity")

    order = len(points)
    distances = [[None] * order for _ in range(order)]
    for i, j in combinations(range(order), 2):
        distances[i][j] = distances[j][i] = squared_distance(points[i], points[j])
    short = 0
    unit = 0
    seen_unit: set[tuple[int, int, int]] = set()
    four = (4 * scale * scale, 0)
    for i, j, k in combinations(range(order), 3):
        A, B, C = distances[i][j], distances[i][k], distances[j][k]
        if any(positive_r(sub_r(side, four)) for side in (A, B, C)):
            continue
        short += 1
        AB = mul_r(A, B)
        heron = sub_r(scale_r(AB, 4), mul_r(sub_r(add_r(A, B), C), sub_r(add_r(A, B), C)))
        if mul_r(AB, C) != scale_r(heron, scale * scale):
            continue
        require(positive_r(heron), "degenerate unit-circumradius triple")
        triple = (i, j, k)
        require(triple in catalog_triples, "uncataloged unit-circle triple")
        seen_unit.add(triple)
        unit += 1
    require(comb(order, 3) == expected["all_triples"], "all-triple count")
    require(short == expected["short_triples"], "short-triple count")
    require(unit == expected["unit_triples"] and seen_unit == catalog_triples,
            "complete unit-circle triple census")
    print(f"PASS {name}: vertices={order} centers={len(rows)} external={sum(external_histogram.values())} "
          f"max_external_degree={max(external_histogram)} all_triples={comb(order,3)} "
          f"unit_triples={unit} catalog_sha256={CATALOG_PINS[name]}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog-dir", type=Path, required=True)
    args = parser.parse_args()
    parts = components()
    print("PASS pinned sources: A=159 V=214 B=292 exact points in Q(i*sqrt(3),i*sqrt(11))")
    for name in ("B", "V"):
        audit_component(name, parts[name], args.catalog_dir.resolve() / f"centers_{name}.json")
    require(881 * 214 + 534 * 292 == 344462, "labeled anchor-family count")
    print("PASS hub frontier: external_centers=881+534 max_degree=10 sharp_centers=4+8 anchor_families=344462")
    print("PASS: independently verified the finite center census supporting the mixed506 single-hub theorem")
    print("SCOPE: the universal center/intersection and quadratic-rotation arguments are re-derived mathematics; hub-free and quadratic families remain open")


if __name__ == "__main__":
    main()
