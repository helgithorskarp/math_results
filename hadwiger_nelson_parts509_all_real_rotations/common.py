#!/usr/bin/env python3
"""Exact common routines for the all-real Parts-509 rotation closure."""

from __future__ import annotations

import base64
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CRITICALITY = ROOT / "hadwiger_nelson_parts509_criticality"
ROTATIONS = ROOT / "hadwiger_nelson_parts509_rotation_scan"
POINTS = CRITICALITY / "parts509.vtx"
GRAPH_CERTIFICATE = CRITICALITY / "certificate.json"
ROTATION_CERTIFICATE = ROTATIONS / "rotation_certificate.json"
CRITICALITY_CERTIFICATE = ROTATIONS / "criticality_certificate.json"
L_SIZE = 374
N = 509
FORMAT = "parts509-all-real-rotations-v1"

sys.path.insert(0, str(CRITICALITY))
from parts509 import (  # noqa: E402
    ONE,
    ZERO,
    FieldElement,
    Point,
    build_edges,
    f_add,
    f_mul,
    f_sq,
    f_sub,
    parse_points,
)


def f_neg(x: FieldElement) -> FieldElement:
    return tuple(-a for a in x)


def f_scale(x: FieldElement, scalar: Fraction) -> FieldElement:
    return tuple(scalar * a for a in x)


@lru_cache(maxsize=None)
def f_inv(y: FieldElement) -> FieldElement:
    """Invert in Q(sqrt(3),sqrt(5),sqrt(11)) by rational elimination."""
    if y == ZERO:
        raise ZeroDivisionError
    columns = []
    for j in range(8):
        basis = tuple(Fraction(int(i == j)) for i in range(8))
        columns.append(f_mul(y, basis))
    rows = [
        [columns[column][row] for column in range(8)]
        + [Fraction(int(row == 0))]
        for row in range(8)
    ]
    for column in range(8):
        pivot = next(row for row in range(column, 8) if rows[row][column])
        rows[column], rows[pivot] = rows[pivot], rows[column]
        scale = rows[column][column]
        rows[column] = [entry / scale for entry in rows[column]]
        for row in range(8):
            if row == column or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [
                a - scale * b for a, b in zip(rows[row], rows[column])
            ]
    answer = tuple(rows[row][-1] for row in range(8))
    if f_mul(answer, y) != ONE:
        raise AssertionError("field inversion failed")
    return answer


def f_div(x: FieldElement, y: FieldElement) -> FieldElement:
    return f_mul(x, f_inv(y))


_BASIS_RADICANDS = (1, 3, 5, 15, 11, 33, 55, 165)


def _sqrt_bounds(radix: int, bits: int) -> tuple[Fraction, Fraction]:
    """Dyadic bounds containing sqrt(radix), computed with integers only."""
    scaled_square = radix << (2 * bits)
    floor = math.isqrt(scaled_square)
    lower = Fraction(floor, 1 << bits)
    if floor * floor == scaled_square:
        return lower, lower
    return lower, Fraction(floor + 1, 1 << bits)


def f_sign(x: FieldElement) -> int:
    """Rigorous sign in the fixed real embedding, via refining dyadic bounds."""
    if x == ZERO:
        return 0
    bits = 24
    while bits <= 1536:
        lower = Fraction(0)
        upper = Fraction(0)
        for coefficient, radix in zip(x, _BASIS_RADICANDS):
            if not coefficient:
                continue
            lo, hi = _sqrt_bounds(radix, bits)
            if coefficient > 0:
                lower += coefficient * lo
                upper += coefficient * hi
            else:
                lower += coefficient * hi
                upper += coefficient * lo
        if lower > 0:
            return 1
        if upper < 0:
            return -1
        bits *= 2
    raise ArithmeticError("failed to separate a nonzero field element")


def norm2(point: Point) -> FieldElement:
    return f_add(f_sq(point[0]), f_sq(point[1]))


def dot_data(p: Point, q: Point) -> tuple[FieldElement, FieldElement]:
    # p dot R(c,s)q = A*c + B*s.
    return (
        f_add(f_mul(p[0], q[0]), f_mul(p[1], q[1])),
        f_sub(f_mul(p[1], q[0]), f_mul(p[0], q[1])),
    )


LineKey = tuple[FieldElement, FieldElement, FieldElement]
Edge = tuple[int, int]


def normalized_line(points: list[Point], radii: list[FieldElement], u: int, v: int) -> LineKey:
    """Return the projective K-line A*c+B*s=C, normalized by A then B."""
    a, b = dot_data(points[u], points[v])
    rhs = f_scale(f_sub(f_add(radii[u], radii[v]), ONE), Fraction(1, 2))
    lead = a if a != ZERO else b
    if lead == ZERO:
        raise ValueError("rotation-invariant pair has no event line")
    return f_div(a, lead), f_div(b, lead), f_div(rhs, lead)


def enumerate_line_classes(points: list[Point]):
    """Enumerate all admissible non-invariant cross-pair event lines exactly."""
    if len(points) != N:
        raise ValueError(f"expected {N} points")
    radii = [norm2(point) for point in points]
    line_edges: dict[LineKey, list[Edge]] = defaultdict(list)
    line_discriminants: dict[LineKey, FieldElement] = {}
    invariant: list[Edge] = []
    sign_cache: dict[tuple[FieldElement, FieldElement], int] = {}
    admissible_pairs = 0
    tangent_pairs = 0
    for u in range(L_SIZE):
        for v in range(L_SIZE, N):
            if points[u] == (ZERO, ZERO):
                if radii[v] == ONE:
                    invariant.append((u, v))
                continue
            rr = f_mul(radii[u], radii[v])
            if rr == ZERO:
                raise ValueError("unexpected zero-radius S point")
            rhs = f_scale(f_sub(f_add(radii[u], radii[v]), ONE), Fraction(1, 2))
            discriminant = f_sub(rr, f_sq(rhs))
            radius_key = radii[u], radii[v]
            if radius_key not in sign_cache:
                sign_cache[radius_key] = f_sign(discriminant)
            sign = sign_cache[radius_key]
            if sign < 0:
                continue
            admissible_pairs += 1
            tangent_pairs += int(sign == 0)
            key = normalized_line(points, radii, u, v)
            line_edges[key].append((u, v))
            previous = line_discriminants.setdefault(key, discriminant)
            # Square membership is invariant under changing the equation scale.
            # Equality is not expected because distinct pairs can scale the line.
            if f_sign(previous) != sign:
                raise AssertionError("one line received incompatible intersections")
    stats = {
        "vertices_labeled": N,
        "L_vertices": L_SIZE,
        "S_vertices": N - L_SIZE,
        "cross_radius_pair_classes": len(sign_cache),
        "admissible_radius_pair_classes": sum(sign >= 0 for sign in sign_cache.values()),
        "admissible_cross_pairs": admissible_pairs,
        "tangent_cross_pairs": tangent_pairs,
        "invariant_cross_edges": len(invariant),
        "line_classes": len(line_edges),
    }
    return (
        {key: sorted(edges) for key, edges in line_edges.items()},
        line_discriminants,
        sorted(invariant),
        stats,
        radii,
    )


def encode_fraction(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def encode_line(key: LineKey) -> list[list[str]]:
    return [[encode_fraction(value) for value in element] for element in key]


def line_digest(keys) -> str:
    digest = hashlib.sha256()
    for key in sorted(keys):
        digest.update(json.dumps(encode_line(key), separators=(",", ":")).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def internal_edges(points: list[Point]) -> list[Edge]:
    return [
        edge
        for edge in build_edges(points)
        if edge[1] < L_SIZE or edge[0] >= L_SIZE
    ]


def pack_coloring(colors: list[int]) -> str:
    if len(colors) != N or any(color not in range(4) for color in colors):
        raise ValueError("bad four-colouring")
    raw = bytearray((N + 3) // 4)
    for index, color in enumerate(colors):
        raw[index // 4] |= color << (2 * (index % 4))
    return base64.b64encode(raw).decode("ascii")


def unpack_coloring(packed: str) -> list[int]:
    raw = base64.b64decode(packed, validate=True)
    if len(raw) != (N + 3) // 4 or raw[-1] >> 2:
        raise ValueError("bad packed four-colouring")
    return [(raw[i // 4] >> (2 * (i % 4))) & 3 for i in range(N)]


def coloring_ok(colors: list[int], edges: list[Edge]) -> bool:
    return all(colors[u] != colors[v] for u, v in edges)


def edge_size_histogram(classes: dict[LineKey, list[Edge]]) -> dict[str, int]:
    return {
        str(size): count
        for size, count in sorted(Counter(map(len, classes.values())).items())
    }
