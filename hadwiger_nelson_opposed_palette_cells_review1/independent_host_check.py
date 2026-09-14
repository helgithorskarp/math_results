#!/usr/bin/env python3
"""Independent exact audit of the auxiliary H421 attachment gate.

This script reconstructs the 21-point heptagonal motif and its 421-point
difference support from the published formulas.  It imports neither the
target host gate nor the sibling geometry implementation.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
from itertools import combinations
import json
from math import lcm
from pathlib import Path


HERE = Path(__file__).resolve().parent

# Phi_42(t) = t^12+t^11-t^9-t^8+t^6-t^4-t^3+t+1.
MODULUS = (1, 1, 0, -1, -1, 0, 1, 0, -1, -1, 0, 1, 1)
ZERO = (Q(0),) * 12
ONE = (Q(1),) + ZERO[1:]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def neg(value):
    return tuple(-x for x in value)


def sub(left, right):
    return add(left, neg(right))


def scale(value, scalar):
    scalar = Q(scalar)
    return tuple(scalar * x for x in value)


def reduce_polynomial(coefficients):
    coefficients = list(coefficients)
    if len(coefficients) < 12:
        coefficients.extend([Q(0)] * (12 - len(coefficients)))
    for degree in range(len(coefficients) - 1, 11, -1):
        leading = coefficients[degree]
        if leading:
            for offset in range(12):
                coefficients[degree - 12 + offset] -= leading * MODULUS[offset]
    return tuple(coefficients[:12])


def multiply(left, right):
    raw = [Q(0)] * 23
    for i, a in enumerate(left):
        if not a:
            continue
        for j, b in enumerate(right):
            if b:
                raw[i + j] += a * b
    return reduce_polynomial(raw)


def power(exponent):
    # The defining root is exp(pi*i/21), hence has order 42.
    return reduce_polynomial([Q(0)] * (exponent % 42) + [Q(1)])


POWERS = tuple(power(exponent) for exponent in range(42))


def conjugate(value):
    answer = ZERO
    for exponent, coefficient in enumerate(value):
        answer = add(answer, scale(POWERS[-exponent % 42], coefficient))
    return answer


def squared_modulus(value):
    return multiply(value, conjugate(value))


def inverse(value):
    columns = [multiply(value, POWERS[j]) for j in range(12)]
    matrix = [
        [columns[column][row] for column in range(12)] + [Q(row == 0)]
        for row in range(12)
    ]
    for column in range(12):
        pivot = next(row for row in range(column, 12)
                     if matrix[row][column])
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        divisor = matrix[column][column]
        matrix[column] = [entry / divisor for entry in matrix[column]]
        for row in range(12):
            if row == column or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [a - factor * b
                           for a, b in zip(matrix[row], matrix[column])]
    answer = tuple(row[-1] for row in matrix)
    require(multiply(value, answer) == ONE, "cyclotomic inverse failure")
    return answer


def motif():
    p = inverse(sub(POWERS[24], POWERS[-24 % 42]))
    q = neg(multiply(POWERS[-7 % 42],
                     inverse(sub(POWERS[6], POWERS[-6 % 42]))))
    r = neg(multiply(POWERS[7],
                     inverse(sub(POWERS[12], POWERS[-12 % 42]))))
    return [multiply(seed, POWERS[6 * turn % 42])
            for seed in (p, q, r) for turn in range(7)]


def integerize(points):
    denominator = lcm(*(entry.denominator for point in points for entry in point))
    rows = [tuple(int(denominator * entry) for entry in point)
            for point in points]
    return rows, denominator


def compact_hash(value):
    payload = json.dumps(value, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def audit():
    seed = motif()
    require(len(seed) == 21 and len(set(seed)) == 21, "motif identity failure")
    points = sorted({sub(left, right) for left in seed for right in seed})
    require(len(points) == 421, "difference support is not H421")
    rows, denominator = integerize(points)
    require(denominator == 7, "unexpected H421 common denominator")

    distance_one = scale(ONE, denominator * denominator)
    distance_three = scale(ONE, 3 * denominator * denominator)
    unit_edges = []
    sqrt3_pairs = []
    for a, b in combinations(range(len(rows)), 2):
        distance = squared_modulus(sub(rows[b], rows[a]))
        if distance == distance_one:
            unit_edges.append((a, b))
        if distance == distance_three:
            sqrt3_pairs.append((a, b))
    require(len(unit_edges) == 1848, "unexpected strict H421 unit graph")
    require(len(sqrt3_pairs) == 126, "unexpected H421 sqrt(3)-pair count")

    # alpha = 2*t^7-1 is i*sqrt(3).  The roots are represented after scaling
    # every support point by six, avoiding division in the membership lookup.
    alpha = sub(scale(POWERS[7], 2), ONE)
    require(multiply(alpha, alpha) == scale(ONE, -3), "sqrt(-3) identity")
    scaled_rows = [scale(point, 6) for point in rows]
    position = {point: index for index, point in enumerate(scaled_rows)}
    records = []
    for a, b in sqrt3_pairs:
        roots = []
        for sign in (-1, 1):
            root = add(scale(add(rows[a], rows[b]), 3),
                       scale(multiply(alpha, sub(rows[b], rows[a])), sign))
            require(root in position, "a unit-circle root is absent from H421")
            require(squared_modulus(sub(root, scaled_rows[a]))
                    == scale(ONE, (6 * denominator) ** 2),
                    "first root distance is not one")
            require(squared_modulus(sub(root, scaled_rows[b]))
                    == scale(ONE, (6 * denominator) ** 2),
                    "second root distance is not one")
            roots.append(position[root])
        require(roots[0] != roots[1], "the two circle roots coincide")
        records.append([a, b, *roots])

    return {
        "status": "INDEPENDENT_H421_GATE_PASSED",
        "motif_points": len(seed),
        "support_points": len(rows),
        "support_unit_edges": len(unit_edges),
        "all_support_pair_checks": len(rows) * (len(rows) - 1) // 2,
        "sqrt3_pairs": len(sqrt3_pairs),
        "circle_roots_checked": 2 * len(sqrt3_pairs),
        "unit_root_equalities_checked": 4 * len(sqrt3_pairs),
        "new_circle_roots": 0,
        "root_index_table_sha256": compact_hash(records),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = audit()
    if args.check_expected:
        expected = json.loads((HERE / "HOST_EXPECTED.json").read_text())
        require(result == expected, "result differs from HOST_EXPECTED.json")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
