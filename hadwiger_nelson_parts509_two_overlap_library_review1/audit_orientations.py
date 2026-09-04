#!/usr/bin/env python3
"""Rebuild every overlap-forced orientation with Python arbitrary integers."""

from __future__ import annotations

from collections import defaultdict
from math import gcd
from pathlib import Path
import sys


RADICANDS = (1, 3, 5, 15, 11, 33, 55, 165)
ZERO = (0,) * 8
Field = tuple[int, ...]
Point = tuple[Field, Field]
Vector = tuple[Field, Field]


def add(a: Field, b: Field) -> Field:
    return tuple(x + y for x, y in zip(a, b))


def sub(a: Field, b: Field) -> Field:
    return tuple(x - y for x, y in zip(a, b))


def neg(a: Field) -> Field:
    return tuple(-x for x in a)


def mul(a: Field, b: Field) -> Field:
    out = [0] * 8
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    out[i ^ j] += x * y * RADICANDS[i & j]
    return tuple(out)


def norm(v: Vector) -> Field:
    return add(mul(v[0], v[0]), mul(v[1], v[1]))


def vectors_by_distance(points: list[Point]) -> dict[Field, set[Vector]]:
    result: dict[Field, set[Vector]] = defaultdict(set)
    for i, p in enumerate(points):
        for q in points[:i]:
            vector = (sub(p[0], q[0]), sub(p[1], q[1]))
            distance = norm(vector)
            result[distance].add(vector)
            result[distance].add((neg(vector[0]), neg(vector[1])))
    return result


def make_orientation(reflected: bool, numerator_c: Field,
                     numerator_s: Field, distance: Field) -> tuple:
    if any(distance[i] for i in range(8) if i not in (0, 5)):
        raise ValueError("shared squared distance escaped Q(sqrt(33))")
    d0, d5 = distance[0], distance[5]
    denominator = d0 * d0 - 33 * d5 * d5
    if denominator == 0:
        raise ValueError("zero algebraic norm in orientation denominator")
    conjugate = (d0, 0, 0, 0, 0, -d5, 0, 0)
    c, s = mul(numerator_c, conjugate), mul(numerator_s, conjugate)
    divisor = abs(denominator)
    for value in c + s:
        divisor = gcd(divisor, abs(value))
    denominator //= divisor
    c = tuple(value // divisor for value in c)
    s = tuple(value // divisor for value in s)
    if denominator < 0:
        denominator, c, s = -denominator, neg(c), neg(s)
    return reflected, denominator, c, s


def orientation_from_pair(a: Vector, b: Vector, reflected: bool) -> tuple:
    distance = norm(a)
    if distance != norm(b) or distance == ZERO:
        raise ValueError("overlap segments have unequal or zero length")
    if reflected:
        numerator_c = sub(mul(a[0], b[0]), mul(a[1], b[1]))
        numerator_s = add(mul(a[0], b[1]), mul(a[1], b[0]))
    else:
        numerator_c = add(mul(a[0], b[0]), mul(a[1], b[1]))
        numerator_s = sub(mul(b[0], a[1]), mul(b[1], a[0]))
    return make_orientation(reflected, numerator_c, numerator_s, distance)


def read_points(path: Path) -> tuple[list[Point], list[Point]]:
    values = []
    for line in path.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        row = tuple(map(int, line.split()))
        if len(row) != 16:
            raise ValueError("malformed point row")
        values.append((row[:8], row[8:]))
    if len(values) != 509 or len(set(values)) != 509:
        raise ValueError("unexpected point census")
    return values[:374], [values[0]] + values[374:]


def main() -> None:
    if len(sys.argv) != 3:
        raise ValueError("usage: audit_orientations.py POINTS.tsv RESIDUAL_SEEDS.tsv")
    large, small = read_points(Path(sys.argv[1]))
    left_vectors = vectors_by_distance(large)
    small_vectors = vectors_by_distance(small)
    orientations = set()
    for distance in left_vectors.keys() & small_vectors.keys():
        for a in left_vectors[distance]:
            for b in small_vectors[distance]:
                orientations.add(orientation_from_pair(a, b, False))
                orientations.add(orientation_from_pair(a, b, True))
    ordered = sorted(orientations)
    rotations = sum(not item[0] for item in ordered)
    if (sum(map(len, left_vectors.values())), sum(map(len, small_vectors.values()))) != (11650, 1666):
        raise ValueError("directed vector census mismatch")
    if len(ordered) != 2840 or rotations != 1420:
        raise ValueError("orientation census mismatch")

    seeds = [tuple(map(int, line.split())) for line in Path(sys.argv[2]).read_text().splitlines()
             if line and not line.startswith("#")]
    for orientation_index, first, second in seeds:
        p0, q0 = divmod(first, 136)
        p1, q1 = divmod(second, 136)
        if p0 == p1 or q0 == q1:
            raise ValueError("degenerate overlap pair")
        a = (sub(large[p1][0], large[p0][0]), sub(large[p1][1], large[p0][1]))
        b = (sub(small[q1][0], small[q0][0]), sub(small[q1][1], small[q0][1]))
        derived = orientation_from_pair(a, b, orientation_index >= 1420)
        if not 0 <= orientation_index < len(ordered) or derived != ordered[orientation_index]:
            raise ValueError("residual seed does not induce its stated orientation")

    print("left_directed_vectors=11650 small_directed_vectors=1666")
    print("rotations=1420 reflections=1420")
    print(f"residual_seed_orientation_matches={len(seeds)}/{len(seeds)}")
    print("python_arbitrary_integer_orientation_reconstruction=true")


if __name__ == "__main__":
    main()
