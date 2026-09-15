#!/usr/bin/env python3
"""Exact geometry for the complete nonunit-D-edge lens closure of G15.

The scalar field is Q(sqrt(3),sqrt(11)), represented in the ordered basis
1,sqrt(3),sqrt(11),sqrt(33).  No floating-point predicates are used.
"""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEPENDENCY = HERE.parent / "hadwiger_nelson_parts509_g14_g15_embedding" / "embedding_certificate.json"
DEPENDENCY_SHA256 = "993121f93b552350a5c5270af3dc052c82c505a86fe7083bc3eb87163271bd8f"

Q = Fraction
RADICAND = (1, 3, 11, 33)
ZERO = (Q(0),) * 4
ONE = (Q(1), Q(0), Q(0), Q(0))
ONE_THIRD = (Q(1, 3), Q(0), Q(0), Q(0))
FOUR = (Q(4), Q(0), Q(0), Q(0))
SQRT11 = (Q(0), Q(0), Q(1), Q(0))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def sub(a, b):
    return add(a, neg(b))


def scale(a, q):
    return tuple(Q(q) * x for x in a)


def mul(a, b):
    out = [Q(0)] * 4
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i ^ j] += x * y * RADICAND[i & j]
    return tuple(out)


def point_add(p, q):
    return add(p[0], q[0]), add(p[1], q[1])


def point_sub(p, q):
    return sub(p[0], q[0]), sub(p[1], q[1])


def point_scale(p, q):
    return scale(p[0], q), scale(p[1], q)


def squared_distance(p, q):
    dx, dy = point_sub(p, q)
    return add(mul(dx, dx), mul(dy, dy))


def parse_source_point(row):
    a, b, c, d = map(Q, row)
    return (a, b, Q(0), Q(0)), (c, d, Q(0), Q(0))


def load_source():
    if hashlib.sha256(DEPENDENCY.read_bytes()).hexdigest() != DEPENDENCY_SHA256:
        raise ValueError("G15 dependency hash mismatch")
    obj = json.loads(DEPENDENCY.read_text())
    rows = obj["g15"]["coordinates"]
    if len(rows) != 15:
        raise ValueError("expected fifteen G15 points")
    return [parse_source_point(row) for row in rows]


def generate_formal_points():
    source = load_source()
    unit, third, four = [], [], []
    for i in range(len(source)):
        for j in range(i + 1, len(source)):
            d2 = squared_distance(source[i], source[j])
            if d2 == ONE:
                unit.append((i, j))
            elif d2 == ONE_THIRD:
                third.append((i, j))
            elif d2 == FOUR:
                four.append((i, j))

    formal = [(p, f"S{i}") for i, p in enumerate(source)]
    for i, j in third:
        difference = point_sub(source[j], source[i])
        midpoint = point_scale(point_add(source[i], source[j]), Q(1, 2))
        # The two intersections of the unit circles have displacement
        # +/- i*(q-p)*sqrt(11)/2 from the midpoint because |q-p|^2=1/3.
        offset = (
            scale(mul(difference[1], SQRT11), Q(-1, 2)),
            scale(mul(difference[0], SQRT11), Q(1, 2)),
        )
        formal.append((point_add(midpoint, offset), f"L13:{i}:{j}:+"))
        formal.append((point_sub(midpoint, offset), f"L13:{i}:{j}:-"))
    for i, j in four:
        # Distance two gives the unique tangent unit-circle intersection.
        formal.append((point_scale(point_add(source[i], source[j]), Q(1, 2)), f"L4:{i}:{j}"))
    return formal, unit, third, four


def physical_support():
    formal, unit, third, four = generate_formal_points()
    index = {}
    points = []
    owners = []
    for point, label in formal:
        if point not in index:
            index[point] = len(points)
            points.append(point)
            owners.append([])
        owners[index[point]].append(label)
    return points, owners, unit, third, four


def complete_edges(points):
    return [
        (i, j)
        for i in range(len(points))
        for j in range(i + 1, len(points))
        if squared_distance(points[i], points[j]) == ONE
    ]


def fraction_text(x):
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def point_stream(points):
    rows = [[[fraction_text(x) for x in coordinate] for coordinate in point] for point in points]
    return json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()


def edge_stream(edges):
    return json.dumps([list(edge) for edge in edges], separators=(",", ":")).encode()


def sha256(data):
    return hashlib.sha256(data).hexdigest()
