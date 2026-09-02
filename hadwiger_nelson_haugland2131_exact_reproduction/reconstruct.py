#!/usr/bin/env python3
"""Exact reconstruction of Haugland's 2026 heptagonal 5-chromatic graph.

Exploratory version.  Exact decisions use Q(zeta_84), extended by sqrt(5)
only for the final rotation.  Floating point is used solely to propose
candidate unit pairs; every retained edge is checked in the exact field.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import time
from pathlib import Path
from typing import Any, Iterable

import sympy as sp
from sympy.polys.domains import QQ


Point = tuple[Any, Any]
FloatPoint = tuple[float, float]
PairElement = tuple[Any, Any]  # a + b sqrt(5), with a,b in Q(zeta_84)
ExtendedPoint = tuple[PairElement, PairElement]


def parse_paths(tex: str) -> list[list[int]]:
    appendix = tex.split("Appendix A:", 1)[1]
    rows = re.findall(r"(?m)^\s*((?:\d+\s*&\s*){4,5}\d+)\s*\\\\", appendix)
    paths = [[int(x) for x in re.findall(r"\d+", row)] for row in rows]
    if len(paths) != 231 or {len(path) for path in paths} != {5, 6}:
        raise ValueError("Appendix A path table was not parsed as expected")
    return paths


class Cyclotomic84:
    def __init__(self) -> None:
        symbolic_zeta = sp.exp(sp.I * sp.pi / 42)
        self.field = QQ.algebraic_field(symbolic_zeta)
        self.zeta = self.field.from_sympy(symbolic_zeta)
        self.zero = self.field.zero
        self.one = self.field.one
        self.i = self.zeta**21
        self.sqrt3 = (self.zeta**14 - self.zeta**-14) / self.i
        assert self.sqrt3 * self.sqrt3 == 3 * self.one

    def unit_vectors(self) -> list[Point]:
        z, i, one = self.zeta, self.i, self.one
        alpha = one / ((z**12 - z**-12) / (2 * i))
        beta = one / ((z**24 - z**-24) / (2 * i))
        base_x = self.sqrt3 * (alpha + beta) / 4
        base_y = (alpha - beta) / 4

        vectors: list[Point] = []
        for j in range(42):
            rotation = z ** (2 * j)
            cosine = (rotation + rotation**-1) / 2
            sine = (rotation - rotation**-1) / (2 * i)
            vectors.append((cosine, sine))
            vectors.append(
                (base_x * cosine - base_y * sine, base_x * sine + base_y * cosine)
            )
        assert len(vectors) == 84
        assert all(x * x + y * y == one for x, y in vectors)
        assert all(
            vectors[j + 42][0] == -vectors[j][0]
            and vectors[j + 42][1] == -vectors[j][1]
            for j in range(42)
        )
        return vectors

    @staticmethod
    def float_vectors() -> list[FloatPoint]:
        alpha = 1 / math.sin(2 * math.pi / 7)
        beta = 1 / math.sin(4 * math.pi / 7)
        base_x = math.sqrt(3) * (alpha + beta) / 4
        base_y = (alpha - beta) / 4
        vectors: list[FloatPoint] = []
        for j in range(42):
            angle = math.pi * j / 21
            c, s = math.cos(angle), math.sin(angle)
            vectors.append((c, s))
            vectors.append((base_x * c - base_y * s, base_x * s + base_y * c))
        return vectors


def insert_point(
    exact: Point,
    approximate: FloatPoint,
    index: dict[Point, int],
    points: list[Point],
    floats: list[FloatPoint],
) -> int:
    if exact in index:
        old = index[exact]
        if math.dist(approximate, floats[old]) > 1e-8:
            raise AssertionError("inconsistent floating rendering of exact point")
        return old
    new = len(points)
    index[exact] = new
    points.append(exact)
    floats.append(approximate)
    return new


def build_g1(
    paths: Iterable[list[int]], exact_vectors: list[Point], float_vectors: list[FloatPoint],
    field: Cyclotomic84,
) -> tuple[list[Point], list[FloatPoint]]:
    points: list[Point] = []
    floats: list[FloatPoint] = []
    index: dict[Point, int] = {}
    origin = (field.zero, field.zero)
    target = (field.zero, field.sqrt3)
    insert_point(origin, (0.0, 0.0), index, points, floats)
    for path in paths:
        exact = origin
        approximate = (0.0, 0.0)
        for step in path:
            ux, uy = exact_vectors[step]
            fx, fy = float_vectors[step]
            exact = (exact[0] + ux, exact[1] + uy)
            approximate = (approximate[0] + fx, approximate[1] + fy)
            insert_point(exact, approximate, index, points, floats)
        if exact != target:
            raise AssertionError(f"path does not end exactly at B: {path}")
    return points, floats


def unit_edges(points: list[Point], floats: list[FloatPoint], one: Any) -> list[tuple[int, int]]:
    candidates: list[tuple[int, int]] = []
    for u, (x, y) in enumerate(floats):
        for v in range(u + 1, len(floats)):
            dx, dy = x - floats[v][0], y - floats[v][1]
            if abs(dx * dx + dy * dy - 1.0) < 1e-8:
                candidates.append((u, v))
    edges: list[tuple[int, int]] = []
    for u, v in candidates:
        dx = points[u][0] - points[v][0]
        dy = points[u][1] - points[v][1]
        if dx * dx + dy * dy == one:
            edges.append((u, v))
    if len(edges) != len(candidates):
        raise AssertionError(
            f"{len(candidates) - len(edges)} floating candidates failed exact verification"
        )
    return edges


def build_g2(
    g1: list[Point], g1_float: list[FloatPoint], field: Cyclotomic84,
) -> tuple[list[Point], list[FloatPoint]]:
    points: list[Point] = []
    floats: list[FloatPoint] = []
    index: dict[Point, int] = {}
    r = field.sqrt3
    for copy in (1, 2):
        for (x, y), (fx, fy) in zip(g1, g1_float, strict=True):
            if copy == 1:
                exact = ((x + r * y) / 2 - field.one, (-r * x + y) / 2)
                approximate = (
                    (fx + math.sqrt(3) * fy) / 2 - 1,
                    (-math.sqrt(3) * fx + fy) / 2,
                )
            else:
                exact = ((x - r * y) / 2 + field.one, (r * x + y) / 2)
                approximate = (
                    (fx - math.sqrt(3) * fy) / 2 + 1,
                    (math.sqrt(3) * fx + fy) / 2,
                )
            insert_point(exact, approximate, index, points, floats)
    return points, floats


def promote(x: Any, zero: Any) -> PairElement:
    return x, zero


def pair_square(x: PairElement) -> PairElement:
    a, b = x
    return a * a + 5 * b * b, 2 * a * b


def pair_add(x: PairElement, y: PairElement) -> PairElement:
    return x[0] + y[0], x[1] + y[1]


def pair_sub(x: PairElement, y: PairElement) -> PairElement:
    return x[0] - y[0], x[1] - y[1]


def insert_extended(
    exact: ExtendedPoint,
    approximate: FloatPoint,
    index: dict[ExtendedPoint, int],
    points: list[ExtendedPoint],
    floats: list[FloatPoint],
) -> int:
    if exact in index:
        old = index[exact]
        if math.dist(approximate, floats[old]) > 1e-8:
            raise AssertionError("inconsistent floating rendering of exact extended point")
        return old
    new = len(points)
    index[exact] = new
    points.append(exact)
    floats.append(approximate)
    return new


def build_g3(
    g2: list[Point], g2_float: list[FloatPoint], field: Cyclotomic84,
) -> tuple[list[ExtendedPoint], list[FloatPoint]]:
    points: list[ExtendedPoint] = []
    floats: list[FloatPoint] = []
    index: dict[ExtendedPoint, int] = {}
    zero, one, sqrt3 = field.zero, field.one, field.sqrt3
    for copy in (0, 1):
        for (x, y), (fx, fy) in zip(g2, g2_float, strict=True):
            if copy == 0:
                exact = (promote(x, zero), promote(y, zero))
                approximate = (fx, fy)
            else:
                # sqrt(15) = sqrt(3) sqrt(5).
                exact_x = ((7 * (x + one)) / 8 - one, -(sqrt3 * y) / 8)
                exact_y = (7 * y / 8, sqrt3 * (x + one) / 8)
                exact = (exact_x, exact_y)
                approximate = (
                    (7 * (fx + 1) - math.sqrt(15) * fy) / 8 - 1,
                    (math.sqrt(15) * (fx + 1) + 7 * fy) / 8,
                )
            insert_extended(exact, approximate, index, points, floats)
    return points, floats


def extended_unit_edges(
    points: list[ExtendedPoint], floats: list[FloatPoint], zero: Any, one: Any
) -> list[tuple[int, int]]:
    candidates: list[tuple[int, int]] = []
    for u, (x, y) in enumerate(floats):
        for v in range(u + 1, len(floats)):
            dx, dy = x - floats[v][0], y - floats[v][1]
            if abs(dx * dx + dy * dy - 1.0) < 1e-8:
                candidates.append((u, v))
    edges: list[tuple[int, int]] = []
    for u, v in candidates:
        dx = pair_sub(points[u][0], points[v][0])
        dy = pair_sub(points[u][1], points[v][1])
        norm = pair_add(pair_square(dx), pair_square(dy))
        if norm == (one, zero):
            edges.append((u, v))
    if len(edges) != len(candidates):
        raise AssertionError(
            f"{len(candidates) - len(edges)} floating candidates failed exact verification"
        )
    return edges


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    start = time.monotonic()
    if args.source.suffix.lower() == ".json":
        paths = json.loads(args.source.read_text())["paths"]
    else:
        paths = parse_paths(args.source.read_text())
    field = Cyclotomic84()
    vectors = field.unit_vectors()
    float_vectors = field.float_vectors()
    print(f"paths={len(paths)} exact_unit_vectors={len(vectors)}")

    g1, f1 = build_g1(paths, vectors, float_vectors, field)
    e1 = unit_edges(g1, f1, field.one)
    endpoint_a = g1.index((field.zero, field.zero))
    endpoint_b = g1.index((field.zero, field.sqrt3))
    print(
        f"G1_vertices={len(g1)} G1_edges={len(e1)} "
        f"endpoints=({endpoint_a},{endpoint_b})"
    )

    g2, f2 = build_g2(g1, f1, field)
    e2 = unit_edges(g2, f2, field.one)
    print(f"G2_vertices={len(g2)} G2_edges={len(e2)}")

    g3, f3 = build_g3(g2, f2, field)
    e3 = extended_unit_edges(g3, f3, field.zero, field.one)
    print(f"G3_vertices={len(g3)} G3_edges={len(e3)}")

    if (len(g1), len(e1), len(g2), len(e2), len(g3), len(e3)) != (
        740,
        3985,
        1066,
        6264,
        2131,
        12530,
    ):
        raise AssertionError("reconstructed graph counts do not match the paper")

    payload = {
        "source": "Haugland, arXiv:2608.04542v2, Appendix A",
        "paths": paths,
        "graph_counts": {
            "G1": [len(g1), len(e1)],
            "G2": [len(g2), len(e2)],
            "G3": [len(g3), len(e3)],
        },
        "G1_endpoints": [endpoint_a, endpoint_b],
        "G1_edges": e1,
        "G3_edges": e3,
    }
    args.output.write_text(json.dumps(payload, separators=(",", ":")) + "\n")
    print(f"output={args.output} seconds={time.monotonic() - start:.3f}")


if __name__ == "__main__":
    main()
