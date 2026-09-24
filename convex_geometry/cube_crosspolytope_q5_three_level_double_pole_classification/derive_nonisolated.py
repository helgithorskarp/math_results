#!/usr/bin/env python3
"""SymPy derivation excluding every non-isolated double-pole cancellation."""

from __future__ import annotations

import argparse
from functools import reduce
from hashlib import sha256
from json import dumps
from math import gcd

import sympy as sp

from derive import find_row, hinge_table, require


def primitive_coefficients(polynomial: sp.Poly) -> list[int]:
    descending = polynomial.all_coeffs()
    common_denominator = sp.ilcm(*[int(value.q) for value in descending])
    integers = [int(value * common_denominator) for value in descending]
    common_numerator = reduce(gcd, (abs(value) for value in integers if value), 0)
    integers = [value // common_numerator for value in integers]
    if integers[0] < 0:
        integers = [-value for value in integers]
    return list(reversed(integers))


def polynomial_from_coefficients(coefficients, variable) -> sp.Poly:
    return sp.Poly(
        sum(value * variable**index for index, value in enumerate(coefficients)),
        variable,
        domain=sp.QQ,
    )


def open_root_count(polynomial: sp.Poly) -> int:
    count = int(sp.count_roots(polynomial, 0, 1))
    count -= int(polynomial.eval(0) == 0)
    count -= int(polynomial.eval(1) == 0)
    return count


def build_certificate():
    require(sp.__version__ == "1.13.3", "this derivation pins SymPy 1.13.3")
    a, b, boundary, variable = sp.symbols("a b B t")
    table = hinge_table((sp.Integer(1), sp.Integer(1), a, a, b), boundary, variable)
    require(len(table) == 33, "unexpected structural-row count")

    rows = []
    for k in range(2):
        for ell in range(3):
            for h in range(2):
                wall = 2 * (k + a * ell + b * h)
                rows.append((f"U({k},{ell},{h})", wall, find_row(table, wall)))
    for i in range(3):
        for j in range(2):
            for g in range(2):
                wall = (1 - a) * boundary / a + 2 * (i + a * j + b * g) / a
                rows.append((f"A({i},{j},{g})", wall, find_row(table, wall)))
    for i in range(3):
        for ell in range(3):
            wall = (1 - b) * boundary / b + 2 * (i + a * ell) / b
            rows.append((f"b({i},{ell})", wall, find_row(table, wall)))
    require(len(rows) == 33, "row-label count")

    d1 = a**6 - a**5 + a**4 - a**3 + a**2 - a + 1
    n1 = -a * (a - 1) * (a**2 - a + 1) * (a**2 + a + 1)
    d2 = a**8 + a**7 + 2 * a - 2
    n2 = a * (a**7 + a**6 + 2 * a - 2)
    d3 = a**9 + 2 * a**8 + a**7 + a**2 - 2 * a + 1
    n3 = a * (a**2 + 1) * (a**2 + a - 1) * (a**4 + a**3 - a + 1)
    d4 = 2 * a**8 + 2 * a**7 - a + 1
    n4 = a * (2 * a**7 + 2 * a**6 + a - 1)

    branches = [
        ("B01", (0, 1, 0, 0), n1 / d1),
        ("B10", (1, 0, 0, 0), n2 / d2),
        ("B11", (1, 1, 0, 1), -n2 / d2),
        ("B20", (2, 0, 0, 1), n3 / d3),
        ("B201", (2, 0, 1, 1), n4 / d4),
        ("B21", (2, 1, 0, 0), -n3 / d3),
        ("B211", (2, 1, 1, 0), -n4 / d4),
        ("B212", (2, 1, 2, 0), n1 / d1),
    ]

    branch_records = []
    for name, pattern, beta in branches:
        ell, h, i, g = pattern
        resonant_boundary = sp.factor(
            2 * (a * (ell * a + h * beta) - (i + g * beta)) / (1 - a)
        )
        target = sp.factor(2 * (ell * a + h * beta))
        substitutions = {b: beta, boundary: resonant_boundary}

        differences = {}
        coefficients = {}
        generic_rows = []
        factor_map = {}
        for label, wall, row in rows:
            difference = sp.factor(
                wall.subs(substitutions, simultaneous=True) - target
            )
            differences[label] = difference
            coefficients[label] = sp.factor(
                row.get(4, 0).subs(substitutions, simultaneous=True)
            )
            if difference == 0:
                generic_rows.append(label)
                continue
            numerator = sp.Poly(
                sp.together(difference).as_numer_denom()[0], a, domain=sp.QQ
            )
            for factor, _multiplicity in sp.factor_list(numerator.as_expr())[1]:
                polynomial = sp.Poly(factor, a, domain=sp.QQ)
                if open_root_count(polynomial) == 0:
                    continue
                key = tuple(primitive_coefficients(polynomial))
                factor_map[key] = polynomial_from_coefficients(key, a)

        intended = sorted([f"U(0,{ell},{h})", f"A({i},0,{g})"])
        require(sorted(generic_rows) == intended, f"generic collision on {name}")

        factors = []
        ordered_factors = sorted(
            factor_map.values(),
            key=lambda value: (value.degree(), primitive_coefficients(value)),
        )
        for polynomial in ordered_factors:
            colliding = []
            for label, difference in differences.items():
                if difference == 0:
                    colliding.append(label)
                    continue
                numerator = sp.Poly(
                    sp.together(difference).as_numer_denom()[0],
                    a,
                    domain=sp.QQ,
                )
                if sp.rem(numerator, polynomial).is_zero:
                    colliding.append(label)
            aggregate = sp.cancel(sum(coefficients[label] for label in colliding))
            aggregate_numerator = sp.Poly(
                sp.together(aggregate).as_numer_denom()[0], a, domain=sp.QQ
            )
            common = sp.gcd(polynomial, aggregate_numerator)
            require(common.degree() == 0, f"non-isolated cancellation on {name}")
            factors.append(
                {
                    "polynomial": primitive_coefficients(polynomial),
                    "degree": polynomial.degree(),
                    "open_unit_roots": open_root_count(polynomial),
                    "colliding_rows": sorted(colliding),
                    "aggregate_numerator_degree": aggregate_numerator.degree(),
                    "aggregate_gcd_degree": common.degree(),
                }
            )

        # Every possible collision root in (0,1) occurs on a recorded factor.
        for label, difference in differences.items():
            if difference == 0:
                continue
            residual = sp.Poly(
                sp.together(difference).as_numer_denom()[0], a, domain=sp.QQ
            )
            for polynomial in ordered_factors:
                while residual.degree() >= polynomial.degree():
                    quotient, remainder = sp.div(residual, polynomial)
                    if not remainder.is_zero:
                        break
                    residual = quotient
            require(
                open_root_count(residual) == 0,
                f"uncovered collision factor on {name}, row {label}",
            )

        branch_records.append(
            {
                "name": name,
                "pattern": list(pattern),
                "generic_rows": sorted(generic_rows),
                "other_rows": 31,
                "collision_factor_count": len(factors),
                "collision_root_count": sum(
                    item["open_unit_roots"] for item in factors
                ),
                "factors": factors,
            }
        )

    certificate = {
        "format": "q5-double-pole-nonisolated-collision-certificate-v1",
        "coefficient_order": "ascending",
        "parameter_interval": "0<a<1",
        "structural_rows": 33,
        "branches": branch_records,
    }
    return certificate


def summary(certificate):
    canonical = dumps(certificate, sort_keys=True, separators=(",", ":"))
    counts = {
        record["name"]: {
            "collision_factors": record["collision_factor_count"],
            "open_unit_roots": record["collision_root_count"],
        }
        for record in certificate["branches"]
    }
    factors = [
        factor
        for record in certificate["branches"]
        for factor in record["factors"]
    ]
    return {
        "status": "Q5_NONISOLATED_DOUBLE_POLE_WALLS_EXCLUDED",
        "sympy_version": sp.__version__,
        "structural_rows": certificate["structural_rows"],
        "leading_branches": len(certificate["branches"]),
        "row_differences_checked": 31 * len(certificate["branches"]),
        "branch_counts": counts,
        "collision_factors": len(factors),
        "open_unit_collision_roots": sum(
            factor["open_unit_roots"] for factor in factors
        ),
        "maximum_factor_degree": max(factor["degree"] for factor in factors),
        "aggregate_cancellation_factors": sum(
            factor["aggregate_gcd_degree"] > 0 for factor in factors
        ),
        "certificate_sha256": sha256(canonical.encode()).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", action="store_true")
    arguments = parser.parse_args()
    certificate = build_certificate()
    payload = certificate if arguments.certificate else summary(certificate)
    print(dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
