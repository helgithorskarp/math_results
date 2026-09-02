#!/usr/bin/env python3
"""Exact scan of K-rational relative rotations of the Parts-509 L/S gadgets.

K is Q(sqrt(3), sqrt(5), sqrt(11)).  The script enumerates every rotation
matrix with entries in K at which a noncentral cross-pair between the fixed
374-point L gadget and rotated 135-point S gadget is at unit distance.  Away
from these finitely many events the strict graph has only the rotation-
invariant central cross edges.

SAT is used only to discover positive 4-colouring witnesses.  The output
certificate contains those witnesses; verify_certificate.py replays them.
Solver inputs and outputs are intentionally not written by this program.
"""

from __future__ import annotations

import argparse
import base64
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Sequence

import sympy
from pysat.solvers import Solver


HERE = Path(__file__).resolve().parent
CRITICALITY = HERE.parent / "hadwiger_nelson_parts509_criticality"
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
    to_field,
)


FORMAT = "parts509-k-rational-rotation-scan-v1"
L_SIZE = 374
N = 509
PRIMES = (3, 5, 11)
RADICALS = tuple(sympy.sqrt(p) for p in PRIMES)
ALGEBRAIC_FIELD = sympy.QQ.algebraic_field(*RADICALS)


def f_neg(x: FieldElement) -> FieldElement:
    return tuple(-a for a in x)


def f_scale(x: FieldElement, q: Fraction) -> FieldElement:
    return tuple(q * a for a in x)


@lru_cache(maxsize=None)
def f_inv(y: FieldElement) -> FieldElement:
    """Invert a field element by exact Gaussian elimination (cached)."""
    if y == ZERO:
        raise ZeroDivisionError
    # Column j is y times basis element sqrt(product(PRIMES bits of j)).
    columns = []
    for j in range(8):
        basis = tuple(Fraction(int(i == j)) for i in range(8))
        columns.append(f_mul(y, basis))
    rows = [
        [columns[col][row] for col in range(8)] + [Fraction(int(row == 0))]
        for row in range(8)
    ]
    for col in range(8):
        pivot = next(row for row in range(col, 8) if rows[row][col])
        rows[col], rows[pivot] = rows[pivot], rows[col]
        scale = rows[col][col]
        rows[col] = [entry / scale for entry in rows[col]]
        for row in range(8):
            if row == col or not rows[row][col]:
                continue
            scale = rows[row][col]
            rows[row] = [a - scale * b for a, b in zip(rows[row], rows[col])]
    answer = tuple(rows[row][-1] for row in range(8))
    assert f_mul(answer, y) == ONE
    return answer


def f_div(x: FieldElement, y: FieldElement) -> FieldElement:
    return f_mul(x, f_inv(y))


def f_to_sympy(x: FieldElement) -> sympy.Expr:
    result = sympy.Integer(0)
    for mask, coefficient in enumerate(x):
        term = sympy.Rational(coefficient.numerator, coefficient.denominator)
        for bit, radical in enumerate(RADICALS):
            if mask & (1 << bit):
                term *= radical
        result += term
    return sympy.expand(result)


def sympy_to_f(x: sympy.Expr) -> FieldElement:
    """Convert an element already known to lie in K to the squarefree basis."""
    return to_field(x)


def f_sign(x: FieldElement) -> int:
    if x == ZERO:
        return 0
    value = sympy.N(f_to_sympy(x), 80)
    if value > 0:
        return 1
    if value < 0:
        return -1
    raise ArithmeticError(f"failed to separate sign of {x}")


def sqrt_in_k(x: FieldElement) -> FieldElement | None:
    """Return the nonnegative square root in K, or None if it is not in K."""

    sign = f_sign(x)
    if sign < 0:
        return None
    if sign == 0:
        return ZERO
    try:
        root_anp = ALGEBRAIC_FIELD.from_sympy(sympy.sqrt(f_to_sympy(x)))
    except sympy.polys.polyerrors.CoercionFailed:
        return None
    root = sympy_to_f(ALGEBRAIC_FIELD.to_sympy(root_anp))
    if f_sq(root) != x:
        raise AssertionError("SymPy field-membership conversion returned a false square root")
    if f_sign(root) < 0:
        root = f_neg(root)
    return root


def norm2(p: Point) -> FieldElement:
    return f_add(f_sq(p[0]), f_sq(p[1]))


def dot_data(p: Point, q: Point) -> tuple[FieldElement, FieldElement]:
    # p dot R(c,s)q = A*c + B*s.
    a = f_add(f_mul(p[0], q[0]), f_mul(p[1], q[1]))
    b = f_sub(f_mul(p[1], q[0]), f_mul(p[0], q[1]))
    return a, b


def rotate(q: Point, rotation: tuple[FieldElement, FieldElement]) -> Point:
    c, s = rotation
    return (
        f_sub(f_mul(c, q[0]), f_mul(s, q[1])),
        f_add(f_mul(s, q[0]), f_mul(c, q[1])),
    )


def cross_unit_events(
    points: Sequence[Point],
) -> tuple[
    dict[tuple[FieldElement, FieldElement], set[tuple[int, int]]],
    list[tuple[int, int]],
    dict[str, int],
]:
    """Enumerate all K-rational rotations carrying a noncentral cross unit edge."""

    radius = [norm2(point) for point in points]
    root_cache: dict[tuple[FieldElement, FieldElement], FieldElement | None] = {}
    events: dict[tuple[FieldElement, FieldElement], set[tuple[int, int]]] = defaultdict(set)
    invariant: list[tuple[int, int]] = []
    admissible_pairs = k_pairs = tangent_pairs = 0

    for u in range(L_SIZE):
        for v in range(L_SIZE, N):
            if points[u] == (ZERO, ZERO):
                if radius[v] == ONE:
                    invariant.append((u, v))
                continue
            rp2, rq2 = radius[u], radius[v]
            c_rhs = f_scale(f_sub(f_add(rp2, rq2), ONE), Fraction(1, 2))
            rr = f_mul(rp2, rq2)
            discriminant = f_sub(rr, f_sq(c_rhs))
            if f_sign(discriminant) < 0:
                continue
            admissible_pairs += 1
            key = (rp2, rq2)
            if key not in root_cache:
                root_cache[key] = sqrt_in_k(discriminant)
            root = root_cache[key]
            if root is None:
                continue
            k_pairs += 1
            if root == ZERO:
                tangent_pairs += 1
            a, b = dot_data(points[u], points[v])
            for sign in (1,) if root == ZERO else (1, -1):
                signed_root = f_scale(root, Fraction(sign))
                c = f_div(f_sub(f_mul(c_rhs, a), f_mul(b, signed_root)), rr)
                s = f_div(f_add(f_mul(c_rhs, b), f_mul(a, signed_root)), rr)
                rotation = (c, s)
                assert f_add(f_sq(c), f_sq(s)) == ONE
                assert f_add(f_mul(a, c), f_mul(b, s)) == c_rhs
                assert f_add(
                    f_sq(f_sub(points[u][0], rotate(points[v], rotation)[0])),
                    f_sq(f_sub(points[u][1], rotate(points[v], rotation)[1])),
                ) == ONE
                events[rotation].add((u, v))

        if u and u % 50 == 0:
            print(
                f"enumerated cross events through L vertex {u}/{L_SIZE - 1}: "
                f"{len(events)} rotations",
                flush=True,
            )

    stats = {
        "radius_pair_classes": len(root_cache),
        "admissible_cross_pairs": admissible_pairs,
        "k_rational_cross_pairs": k_pairs,
        "tangent_cross_pairs": tangent_pairs,
        "invariant_cross_edges": len(invariant),
        "event_rotations": len(events),
    }
    return dict(events), sorted(invariant), stats


def coloring_clauses(n: int, edges: Iterable[tuple[int, int]]) -> list[list[int]]:
    clauses = [[4 * vertex + color + 1 for color in range(4)] for vertex in range(n)]
    clauses.extend(
        [-4 * u - color - 1, -4 * v - color - 1]
        for u, v in edges
        for color in range(4)
    )
    # The fixed L triangle survives every relative rotation.
    clauses.extend([[4 * vertex + color + 1] for color, vertex in enumerate((0, 149, 152))])
    return clauses


def decode_model(model: Sequence[int], n: int) -> list[int]:
    positive = set(literal for literal in model if literal > 0)
    coloring = []
    for vertex in range(n):
        colors = [color for color in range(4) if 4 * vertex + color + 1 in positive]
        if not colors:
            raise AssertionError(f"SAT model gives vertex {vertex} no colour")
        coloring.append(colors[0])
    return coloring


def pack_coloring(colors: Sequence[int]) -> str:
    data = bytearray((len(colors) + 3) // 4)
    for index, color in enumerate(colors):
        data[index // 4] |= color << (2 * (index % 4))
    return base64.b64encode(data).decode("ascii")


def encode_fraction(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def encode_field(value: FieldElement) -> list[str]:
    return [encode_fraction(coefficient) for coefficient in value]


def scan(points_path: Path, output_path: Path) -> None:
    points = parse_points(points_path)
    if len(points) != N:
        raise ValueError(f"expected {N} points, got {len(points)}")
    all_edges = build_edges(points)
    l_edges = [(u, v) for u, v in all_edges if v < L_SIZE]
    s_edges = [(u, v) for u, v in all_edges if u >= L_SIZE]
    events, invariant, stats = cross_unit_events(points)
    base_edges = l_edges + s_edges + invariant

    records = []
    uncolorable = []
    cross_histogram: Counter[int] = Counter()
    for index, (rotation, event_edges) in enumerate(sorted(events.items())):
        edges = base_edges + sorted(event_edges)
        cross_histogram[len(invariant) + len(event_edges)] += 1
        with Solver(name="cadical195", bootstrap_with=coloring_clauses(N, edges)) as solver:
            satisfiable = solver.solve()
            coloring = decode_model(solver.get_model(), N) if satisfiable else None
        record = {
            "cos": encode_field(rotation[0]),
            "sin": encode_field(rotation[1]),
            "event_cross_edges": [list(edge) for edge in sorted(event_edges)],
            "distinct_points": len(set(points[:L_SIZE]) | {rotate(p, rotation) for p in points[L_SIZE:]}),
            "four_coloring": pack_coloring(coloring) if coloring is not None else None,
        }
        records.append(record)
        if not satisfiable:
            uncolorable.append(index)
        if (index + 1) % 100 == 0:
            print(f"tested {index + 1}/{len(events)} event rotations", flush=True)

    with Solver(name="cadical195", bootstrap_with=coloring_clauses(N, base_edges)) as solver:
        if not solver.solve():
            raise AssertionError("rotation-generic baseline unexpectedly not 4-colourable")
        generic_coloring = decode_model(solver.get_model(), N)

    certificate = {
        "format": FORMAT,
        "scope": "relative rotations with cos(theta), sin(theta) in Q(sqrt(3),sqrt(5),sqrt(11))",
        "point_source": str(points_path.name),
        "counts": {
            "vertices_labeled": N,
            "L_vertices": L_SIZE,
            "S_vertices": N - L_SIZE,
            "L_edges": len(l_edges),
            "S_edges": len(s_edges),
            **stats,
            "cross_edge_histogram": dict(sorted(cross_histogram.items())),
            "uncolorable_event_indices": uncolorable,
        },
        "invariant_cross_edges": [list(edge) for edge in invariant],
        "generic_four_coloring": pack_coloring(generic_coloring),
        "events": records,
    }
    output_path.write_text(json.dumps(certificate, separators=(",", ":")) + "\n")
    print(json.dumps(certificate["counts"], indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "points",
        nargs="?",
        type=Path,
        default=CRITICALITY / "parts509.vtx",
    )
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    scan(args.points, args.output)


if __name__ == "__main__":
    main()
