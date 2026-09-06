#!/usr/bin/env python3
"""Independent positive-certificate audit for the Moser terminal connector.

The connector geometry is regenerated without importing either submitted
implementation.  Rational operations remain exact; only square roots are
enclosed, at a fixed 220-bit denominator.  The imported A159 extension fact
is checked separately in the full eight-element multiquadratic basis.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from itertools import combinations, product
from math import isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CONNECTOR = ROOT / "hadwiger_nelson_moser_terminal_connector"
GLUING = ROOT / "hadwiger_nelson_long_terminal_gluing"
POINTS159 = ROOT / "hadwiger_nelson_nonmono159_214_lowden2" / "points159.tsv"
ROOT_SCALE = 1 << 220


def floor_root(x: Fraction) -> Fraction:
    assert x >= 0
    n = x.numerator * ROOT_SCALE * ROOT_SCALE // x.denominator
    return Fraction(isqrt(n), ROOT_SCALE)


def ceil_root(x: Fraction) -> Fraction:
    lo = floor_root(x)
    if lo * lo == x:
        return lo
    return lo + Fraction(1, ROOT_SCALE)


class Interval:
    __slots__ = ("lo", "hi")

    def __init__(self, lo: Fraction | int, hi: Fraction | int | None = None):
        self.lo = Fraction(lo)
        self.hi = Fraction(lo if hi is None else hi)
        assert self.lo <= self.hi

    def __add__(self, other: "Interval") -> "Interval":
        return Interval(self.lo + other.lo, self.hi + other.hi)

    def __neg__(self) -> "Interval":
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other: "Interval") -> "Interval":
        return self + (-other)

    def __mul__(self, other: "Interval") -> "Interval":
        values = [a * b for a in (self.lo, self.hi) for b in (other.lo, other.hi)]
        return Interval(min(values), max(values))

    def __truediv__(self, other: "Interval") -> "Interval":
        assert not (other.lo <= 0 <= other.hi)
        values = [a / b for a in (self.lo, self.hi) for b in (other.lo, other.hi)]
        return Interval(min(values), max(values))

    def square(self) -> "Interval":
        values = [self.lo * self.lo, self.hi * self.hi]
        return Interval(0 if self.lo <= 0 <= self.hi else min(values), max(values))

    def sqrt(self) -> "Interval":
        assert self.lo >= 0
        return Interval(floor_root(self.lo), ceil_root(self.hi))

    def contains(self, value: Fraction | int) -> bool:
        return self.lo <= value <= self.hi


class ComplexBox:
    __slots__ = ("x", "y")

    def __init__(self, x: Interval, y: Interval):
        self.x, self.y = x, y

    def __add__(self, other: "ComplexBox") -> "ComplexBox":
        return ComplexBox(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "ComplexBox") -> "ComplexBox":
        return ComplexBox(self.x - other.x, self.y - other.y)

    def scale(self, scalar: Interval) -> "ComplexBox":
        return ComplexBox(self.x * scalar, self.y * scalar)

    def perpendicular(self) -> "ComplexBox":
        return ComplexBox(-self.y, self.x)

    def norm2(self) -> Interval:
        return self.x.square() + self.y.square()

    def multiply(self, other: "ComplexBox") -> "ComplexBox":
        return ComplexBox(
            self.x * other.x - self.y * other.y,
            self.x * other.y + self.y * other.x,
        )


def exact(value: int | Fraction) -> Interval:
    return Interval(value)


def generate_connector() -> tuple[list[ComplexBox], list[tuple[int, int, int]], dict]:
    sqrt3 = exact(3).sqrt()
    sqrt7 = exact(7).sqrt()
    sqrt11 = exact(11).sqrt()
    zero = ComplexBox(exact(0), exact(0))
    one = ComplexBox(exact(1), exact(0))
    v = ComplexBox(exact(Fraction(1, 2)), sqrt3 / exact(2))
    rho = ComplexBox(exact(Fraction(5, 6)), sqrt11 / exact(6))
    spindle = [zero, one, v, one + v, rho, rho.multiply(v), rho.multiply(one + v)]

    points = list(spindle)
    triangles: list[tuple[int, int, int]] = []
    absent = present = contact_checks = triangle_checks = 0
    lower = exact(8) - exact(2) * sqrt7
    upper = exact(8) + exact(2) * sqrt7

    for i, j in combinations(range(7), 2):
        chord = spindle[j] - spindle[i]
        chord2 = chord.norm2()
        assert chord2.lo > 0 and chord2.hi < 4
        multiplier = (exact(1) / chord2 - exact(Fraction(1, 4))).sqrt()
        midpoint = (spindle[i] + spindle[j]).scale(exact(Fraction(1, 2)))
        for sign in (-1, 1):
            a = midpoint + chord.perpendicular().scale(exact(sign) * multiplier)
            assert (a - spindle[i]).norm2().contains(1)
            assert (a - spindle[j]).norm2().contains(1)
            contact_checks += 2
            for anchor in spindle:
                delta = anchor - a
                radius2 = delta.norm2()
                if radius2.hi < lower.lo or radius2.lo > upper.hi:
                    absent += 1
                    continue
                assert radius2.lo > lower.hi and radius2.hi < upper.lo
                present += 1
                discriminant = exact(16) * radius2 - radius2.square() - exact(36)
                assert discriminant.lo > 0 and radius2.lo > 0
                along = (radius2 + exact(6)) / (exact(2) * radius2)
                across = discriminant.sqrt() / (exact(2) * radius2)
                for side in (-1, 1):
                    b = a + delta.scale(along) + delta.perpendicular().scale(exact(side) * across)
                    assert (b - a).norm2().contains(7)
                    assert (b - anchor).norm2().contains(1)
                    contact_checks += 1
                    edge = b - a
                    for orientation in (-1, 1):
                        c = a + edge.scale(exact(Fraction(1, 2))) + edge.perpendicular().scale(
                            exact(orientation) * sqrt3 / exact(2)
                        )
                        ids = (len(points), len(points) + 1, len(points) + 2)
                        points.extend((a, b, c))
                        triangles.append(ids)
                        for p, q in combinations((a, b, c), 2):
                            assert (p - q).norm2().contains(7)
                            triangle_checks += 1

    stats = {
        "spindle_pairs": 21,
        "double_contact_labels": 42,
        "second_anchor_cases": absent + present,
        "absent_cases": absent,
        "two_intersection_cases": present,
        "labelled_triangles": len(triangles),
        "labelled_points": len(points),
        "construction_contact_enclosures": contact_checks,
        "triangle_side_enclosures": triangle_checks,
    }
    return points, triangles, stats


def audit_common_colouring(points: list[ComplexBox], triangles: list[tuple[int, int, int]]) -> dict:
    certificate = json.loads((CONNECTOR / "certificate.json").read_text())
    text = certificate["labelled_colours"]
    assert len(text) == len(points) and set(text) <= set("0123")
    colours = [int(c) for c in text]
    same_nonunit = different_distinct = 0
    for i, j in combinations(range(len(points)), 2):
        difference = points[i] - points[j]
        if colours[i] == colours[j]:
            distance2 = difference.norm2()
            assert distance2.hi < 1 or distance2.lo > 1, ("same-colour unit ambiguity", i, j)
            same_nonunit += 1
        else:
            assert (
                difference.x.hi < 0
                or difference.x.lo > 0
                or difference.y.hi < 0
                or difference.y.lo > 0
            ), ("different-colour alias ambiguity", i, j)
            different_distinct += 1
    assert all(len({colours[i] for i in triangle}) > 1 for triangle in triangles)
    assert hashlib.sha256(json.dumps(certificate["colours"], separators=(",", ":")).encode()).hexdigest() == certificate["colours_sha256"]
    return {
        "same_colour_provably_nonunit_pairs": same_nonunit,
        "different_colour_provably_distinct_pairs": different_distinct,
        "all_pairs": same_nonunit + different_distinct,
        "nonmonochromatic_labelled_triangles": len(triangles),
        "labelled_colour_sha256": hashlib.sha256(text.encode()).hexdigest(),
    }


RADICALS = (3, 5, 11)


def field_add(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x + y for x, y in zip(a, b, strict=True))


def field_sub(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(x - y for x, y in zip(a, b, strict=True))


def field_mul(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * 8
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            factor = 1
            common = i & j
            for bit, radical in enumerate(RADICALS):
                if common & (1 << bit):
                    factor *= radical
            out[i ^ j] += factor * x * y
    return tuple(out)


def field_norm(point: tuple[tuple[int, ...], tuple[int, ...]]) -> tuple[int, ...]:
    return field_add(field_mul(point[0], point[0]), field_mul(point[1], point[1]))


def field_distance2(a, b) -> tuple[int, ...]:
    return field_norm((field_sub(a[0], b[0]), field_sub(a[1], b[1])))


def read_a159() -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    lines = POINTS159.read_text().splitlines()
    assert lines[0] == "# scale 12"
    points = []
    for line in lines[1:]:
        if not line.strip() or line.startswith("#"):
            continue
        values = tuple(map(int, line.split()))
        assert len(values) == 16
        points.append((values[:8], values[8:]))
    assert len(points) == len(set(points)) == 159
    return points


def audit_a159_extensions() -> dict:
    points = read_a159()
    unit = (144,) + (0,) * 7
    edges = [(i, j) for i, j in combinations(range(159), 2) if field_distance2(points[i], points[j]) == unit]
    assert len(edges) == 646
    terminals = (141, 142, 144)
    seven = (1008,) + (0,) * 7
    assert all(field_distance2(points[i], points[j]) == seven for i, j in combinations(terminals, 2))

    imported = json.loads((GLUING / "certificate.json").read_text())["159"]
    assert tuple(imported["terminals"]) == terminals
    rows = {row["pattern"]: row["colours"] for row in imported["extensions"]}
    assert set(rows) == {"001", "010", "011", "012"}
    canonical_checks = 0
    for pattern, colouring in rows.items():
        assert len(colouring) == 159 and set(colouring) <= set("0123")
        assert "".join(colouring[i] for i in terminals) == pattern
        assert all(colouring[i] != colouring[j] for i, j in edges)
        canonical_checks += len(edges)

    assignments = expanded_checks = 0
    for target in product("0123", repeat=3):
        if len(set(target)) == 1:
            continue
        palette = list(dict.fromkeys(target))
        pattern = "".join(str(palette.index(c)) for c in target)
        source = rows[pattern]
        palette += sorted(set("0123") - set(palette))
        colouring = "".join(palette[int(c)] for c in source)
        assert tuple(colouring[i] for i in terminals) == target
        assert all(colouring[i] != colouring[j] for i, j in edges)
        assignments += 1
        expanded_checks += len(edges)
    assert assignments == 60
    return {
        "vertices": len(points),
        "strict_unit_edges": len(edges),
        "full_pair_tests": len(points) * (len(points) - 1) // 2,
        "terminal_squared_distance": 7,
        "canonical_patterns": sorted(rows),
        "canonical_edge_checks": canonical_checks,
        "nonmonochromatic_assignments_extended": assignments,
        "expanded_edge_checks": expanded_checks,
        "coordinate_sha256": hashlib.sha256(POINTS159.read_bytes()).hexdigest(),
        "extension_certificate_sha256": hashlib.sha256((GLUING / "certificate.json").read_bytes()).hexdigest(),
    }


def controls() -> dict:
    two = exact(2).sqrt()
    assert two.lo * two.lo <= 2 <= two.hi * two.hi
    assert ceil_root(Fraction(9, 4)) == Fraction(3, 2)
    x = Interval(Fraction(-3, 5), Fraction(7, 11))
    y = Interval(Fraction(2, 7), Fraction(5, 3))
    values = [a * b for a in (x.lo, x.hi) for b in (y.lo, y.hi)]
    z = x * y
    assert z.lo == min(values) and z.hi == max(values)
    return {"exact_square_root_control": True, "irrational_root_enclosure_control": True, "signed_product_control": True}


def main() -> None:
    if not __debug__:
        raise RuntimeError("run with assertions enabled (omit -O)")
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    points, triangles, construction = generate_connector()
    result = {
        "status": "PASS",
        "verdict_scope": "fixed double/single-contact Moser terminal connector and stated private-interior A159 lifting",
        "arithmetic": "exact Fraction propagation with independently rounded 220-bit square-root enclosures",
        "connector": {**construction, **audit_common_colouring(points, triangles)},
        "a159_extension": audit_a159_extensions(),
        "controls": controls(),
        "native_solver_calls": 0,
        "negative_solver_claim_used": False,
        "target_graph_found": False,
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.write_text(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
