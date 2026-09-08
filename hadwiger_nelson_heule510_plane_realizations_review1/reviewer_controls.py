#!/usr/bin/env python3
"""Small exact controls for the reviewer implementation."""

from fractions import Fraction as F
from itertools import product
import json

import independent_audit as audit


def main():
    checks = 0
    for square in (-3, 33):
        field = audit.Quadratic(square)
        values = [(F(a, d), F(b, d)) for a, b, d in product(range(-2, 3), range(-2, 3), (1, 2))]
        for x in values:
            for y in values:
                expected = (x[0] * y[0] + square * x[1] * y[1],
                            x[0] * y[1] + x[1] * y[0])
                audit.require(field.mul(x, y) == expected, "quadratic multiplication control")
                audit.require(field.sub(field.add(x, y), y) == x, "quadratic addition control")
                if y != audit.QZERO:
                    audit.require(field.mul(field.mul(x, y), field.inv(y)) == x,
                                  "quadratic inverse control")
                checks += 1

    # Exact row-space membership and nonmembership.
    field = audit.Quadratic(-3)
    rows = [
        [audit.QONE, (F(0), F(1)), audit.QZERO],
        [audit.QZERO, audit.QONE, audit.QONE],
    ]
    basis, pivots = field.rref(rows, 3)
    audit.require(len(basis) == 2, "exact RREF rank control")
    for row in rows:
        audit.require(field.reduce(row, basis, pivots) == (audit.QZERO,) * 3,
                      "exact RREF membership control")
    audit.require(field.reduce([audit.QZERO, audit.QZERO, audit.QONE], basis, pivots)
                  != (audit.QZERO,) * 3, "exact RREF nonmembership control")

    # Finite-field extension operations are checked against their defining law.
    modular = audit.ModularQuadratic(audit.ORIENTATION_PRIME)
    p = audit.ORIENTATION_PRIME
    modular_cases = 0
    for a, b, c, d in product(range(-2, 3), repeat=4):
        x = (a % p, b % p)
        y = (c % p, d % p)
        expected = ((a * c - 3 * b * d) % p, (a * d + b * c) % p)
        audit.require(modular.mul(x, y) == expected, "modular extension multiplication")
        if y != (0, 0):
            audit.require(modular.mul(modular.mul(x, y), modular.inv(y)) == x,
                          "modular extension inverse")
        modular_cases += 1

    zero = ((F(0),) * 8, (F(0),) * 8)
    one = ((F(1),) + (F(0),) * 7, (F(0),) * 8)
    mixed = ((F(0), F(1), F(1)) + (F(0),) * 5, (F(0),) * 8)
    audit.require(audit.norm2(zero, one) == ((1, F(1)),), "rational unit control")
    audit.require(audit.norm2(zero, mixed) == ((1, F(8)), (15, F(2))),
                  "multiquadratic cross-term control")
    audit.require(audit.canonical_direction((F(0), F(-2), F(1))) == (F(0), F(2), F(-1)),
                  "direction sign control")

    print(json.dumps({
        "exact_quadratic_cases": checks,
        "modular_quadratic_cases": modular_cases,
        "rref_controls": 4,
        "radical_norm_controls": 2,
        "direction_controls": 1,
        "status": "REVIEWER_CONTROLS_PASSED",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
