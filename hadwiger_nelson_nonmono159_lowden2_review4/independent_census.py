#!/usr/bin/env python3
"""Independent exact census check for the Parts-159 low-denominator claim.

This implementation deliberately imports no submitted module.  It rebuilds
the equal-length segment orientations and every overlap-supported translation
using Python integers in Q(sqrt(3),sqrt(5),sqrt(11)).
"""

from __future__ import annotations

import hashlib
import json
import lzma
import math
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "hadwiger_nelson_nonmono159_lowden2"

EXPECTED_HASHES = {
    "CENSUS.txt": "f6edc359dccea27ba289d372ac4c60605e2d9463fd4d746a27872234d4385c1e",
    "colorings.txt.xz": "140b8a2fe8685e293ed0209a66bd276cd2cbb708eca08b6e8f340885ba4789a6",
    "enumerate_overlaps.cpp": "f0441fce4aebee3d8f45bf8aed0ff32441850f7b4ebfa30c578b6d45a69fbd0e",
    "overlap_transforms.txt.xz": "9cbc97fcd0f2c9df37c2949466c11f99ef3327930bc8957edcec734a566ce338",
    "points.tsv": "4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02",
    "verify_colorings.cpp": "c2ab826d4ebd3aaffc5f62ee645d70e78e326bb9fcbc0b3f5e35124c17e103c4",
}

Field = tuple[int, ...]
Point = tuple[Field, Field]
Vector = tuple[Field, Field]
Orientation = tuple[bool, int, Field, Field]

ZERO: Field = (0,) * 8
RADICANDS = (3, 5, 11)


def add(a: Field, b: Field) -> Field:
    return tuple(x + y for x, y in zip(a, b))


def sub(a: Field, b: Field) -> Field:
    return tuple(x - y for x, y in zip(a, b))


def neg(a: Field) -> Field:
    return tuple(-x for x in a)


def mul(a: Field, b: Field) -> Field:
    result = [0] * 8
    for i, ai in enumerate(a):
        if not ai:
            continue
        for j, bj in enumerate(b):
            if not bj:
                continue
            coefficient = ai * bj
            common_bits = i & j
            for bit, radicand in enumerate(RADICANDS):
                if common_bits & (1 << bit):
                    coefficient *= radicand
            result[i ^ j] += coefficient
    return tuple(result)


def squared_norm(vector: Vector) -> Field:
    return add(mul(vector[0], vector[0]), mul(vector[1], vector[1]))


def parse_field(encoded: str) -> Field:
    result = tuple(map(int, encoded.split(",")))
    assert len(result) == 8
    return result


def read_points() -> list[Point]:
    points = []
    for line in (TARGET / "points.tsv").read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        values = tuple(map(int, line.split()))
        assert len(values) == 16
        points.append((values[:8], values[8:]))
    assert len(points) == 159 and len(set(points)) == 159
    return points


def directed_vectors(points: list[Point]) -> dict[Field, set[Vector]]:
    by_distance: dict[Field, set[Vector]] = defaultdict(set)
    for i, point in enumerate(points):
        for earlier in points[:i]:
            vector = (sub(point[0], earlier[0]), sub(point[1], earlier[1]))
            by_distance[squared_norm(vector)].add(vector)
            by_distance[squared_norm(vector)].add((neg(vector[0]), neg(vector[1])))
    return by_distance


def reduced_orientation(
    reflected: bool, numerator_c: Field, numerator_s: Field, distance: Field
) -> Orientation:
    assert all(value == 0 for i, value in enumerate(distance) if i not in (0, 5))
    denominator = distance[0] * distance[0] - 33 * distance[5] * distance[5]
    conjugate = (distance[0], 0, 0, 0, 0, -distance[5], 0, 0)
    c = mul(numerator_c, conjugate)
    s = mul(numerator_s, conjugate)
    divisor = abs(denominator)
    for value in c + s:
        divisor = math.gcd(divisor, abs(value))
    assert divisor > 0
    denominator //= divisor
    c = tuple(value // divisor for value in c)
    s = tuple(value // divisor for value in s)
    if denominator < 0:
        denominator = -denominator
        c, s = neg(c), neg(s)
    assert add(mul(c, c), mul(s, s)) == (denominator * denominator,) + (0,) * 7
    return reflected, denominator, c, s


def enumerate_orientations(vectors: dict[Field, set[Vector]]) -> set[Orientation]:
    result: set[Orientation] = set()
    for distance, vector_set in vectors.items():
        for a in vector_set:
            for b in vector_set:
                rotation_c = add(mul(a[0], b[0]), mul(a[1], b[1]))
                rotation_s = sub(mul(b[0], a[1]), mul(b[1], a[0]))
                result.add(reduced_orientation(False, rotation_c, rotation_s, distance))
                reflection_c = sub(mul(a[0], b[0]), mul(a[1], b[1]))
                reflection_s = add(mul(a[0], b[1]), mul(a[1], b[0]))
                result.add(reduced_orientation(True, reflection_c, reflection_s, distance))
    return result


def transformed_numerator(orientation: Orientation, point: Point) -> Point:
    reflected, _, c, s = orientation
    cx, sy = mul(c, point[0]), mul(s, point[1])
    sx, cy = mul(s, point[0]), mul(c, point[1])
    if reflected:
        return add(cx, sy), sub(sx, cy)
    return sub(cx, sy), add(sx, cy)


def expected_placements(
    points: list[Point], orientations: list[Orientation]
) -> dict[tuple[object, ...], int]:
    result: dict[tuple[object, ...], int] = {}
    for orientation in orientations:
        reflected, denominator, c, s = orientation
        image = [transformed_numerator(orientation, point) for point in points]
        differences = Counter(
            (
                sub(tuple(denominator * x for x in left[0]), right[0]),
                sub(tuple(denominator * y for y in left[1]), right[1]),
            )
            for left in points
            for right in image
        )
        for (tx, ty), multiplicity in differences.items():
            if multiplicity >= 2:
                key = (reflected, denominator, c, s, tx, ty)
                assert key not in result
                result[key] = multiplicity
    return result


def archived_placements() -> tuple[bytes, dict[tuple[object, ...], int]]:
    raw = lzma.decompress((TARGET / "overlap_transforms.txt.xz").read_bytes())
    result: dict[tuple[object, ...], int] = {}
    placement_lines = 0
    for line in raw.decode().splitlines():
        if not line.startswith("placement="):
            continue
        placement_lines += 1
        row = dict(item.split("=", 1) for item in line.split(";"))
        key = (
            bool(int(row["reflected"])),
            int(row["denominator"]),
            parse_field(row["c"]),
            parse_field(row["s"]),
            parse_field(row["tx"]),
            parse_field(row["ty"]),
        )
        assert key not in result
        result[key] = int(row["placement"])
    assert placement_lines == len(result)
    return raw, result


def main() -> None:
    for name, expected in EXPECTED_HASHES.items():
        assert hashlib.sha256((TARGET / name).read_bytes()).hexdigest() == expected

    points = read_points()
    vectors = directed_vectors(points)
    assert sum(map(len, vectors.values())) == 3612
    orientations = enumerate_orientations(vectors)
    rotation_count = sum(not orientation[0] for orientation in orientations)
    reflection_count = sum(orientation[0] for orientation in orientations)
    assert (rotation_count, reflection_count) == (1874, 1830)

    selected = sorted(orientation for orientation in orientations if orientation[1] <= 2)
    assert len(selected) == 12
    expected = expected_placements(points, selected)
    raw, archived = archived_placements()
    assert archived == expected

    histogram = Counter(expected.values())
    certificates = sum(count * multiplicity * (multiplicity - 1) // 2
                       for multiplicity, count in histogram.items())
    assert len(expected) == 32990
    assert certificates == 2797044
    assert min(histogram) == 2 and max(histogram) == 159

    census = (TARGET / "CENSUS.txt").read_text()
    assert "placements_with_at_least_two_overlaps=32990\n" in census
    assert "selected_orientations=12\n" in census
    assert "pair_certificates=2797044\n" in census
    for multiplicity, count in sorted(histogram.items()):
        assert f"overlap_{multiplicity}={count}\n" in census

    histogram_encoding = json.dumps(sorted(histogram.items()), separators=(",", ":")).encode()
    output = {
        "all_checks": True,
        "pair_certificates": certificates,
        "placements": len(expected),
        "selected_denominators": dict(sorted(Counter(o[1] for o in selected).items())),
        "selected_orientations": len(selected),
        "transform_stream_sha256": hashlib.sha256(raw).hexdigest(),
        "unfiltered_reflections": reflection_count,
        "unfiltered_rotations": rotation_count,
        "vector_count": sum(map(len, vectors.values())),
        "histogram_sha256": hashlib.sha256(histogram_encoding).hexdigest(),
    }
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
