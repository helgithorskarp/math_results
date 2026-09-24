#!/usr/bin/env python3
"""SymPy derivation for the complementary ordering 0<a<b<1."""

from __future__ import annotations

import argparse
from hashlib import sha256
from json import dumps

import sympy as sp

from derive import find_row, hinge_table, rational_sign_at_root, require
from derive_nonisolated import (
    open_root_count,
    polynomial_from_coefficients,
    primitive_coefficients,
)


def branches_and_eliminants(a):
    d2 = a**8 + a**7 + 2 * a - 2
    d3 = a**9 + 2 * a**8 + a**7 + a**2 - 2 * a + 1
    d4 = 2 * a**8 + 2 * a**7 - a + 1
    s6 = sum(a**index for index in range(7))
    p2 = sp.Poly(
        a**15
        + 2 * a**14
        + a**13
        + 6 * a**9
        + 2 * a**8
        - 2 * a**7
        - 6 * a**6
        + 4 * a**2
        - 8 * a
        + 4,
        a,
        domain=sp.QQ,
    )
    p3 = sp.Poly(
        a**15
        + 4 * a**14
        + 5 * a**13
        - 4 * a**11
        + a**9
        - a**8
        + a**7
        - a**6
        + 4 * a**4
        - 5 * a**2
        + 4 * a
        - 1,
        a,
        domain=sp.QQ,
    )
    return [
        (
            "C1100",
            (1, 1, 0, 0),
            -a * (a**7 + a**6 - 2 * a + 2) / d2,
            sp.Poly(
                a**15
                + 2 * a**14
                + a**13
                - 6 * a**9
                - 6 * a**8
                - 6 * a**7
                - 6 * a**6
                - 4 * a**2
                + 8 * a
                - 4,
                a,
                domain=sp.QQ,
            ),
            "no_open_unit_root",
        ),
        (
            "C1101",
            (1, 1, 0, 1),
            -a * (a**7 + a**6 + 2 * a - 2) / d2,
            p2,
            "beta_negative",
        ),
        (
            "C1110",
            (1, 1, 1, 0),
            -a * (a**2 + 1) * (a**4 - a**2 + 1) / ((a - 1) * s6),
            sp.Poly(
                a**10
                - 2 * a**8
                - a**7
                + 2 * a**6
                + 2 * a**5
                + 2 * a**4
                - a**3
                - 2 * a**2
                + 1,
                a,
                domain=sp.QQ,
            ),
            "no_open_unit_root",
        ),
        (
            "C2000",
            (2, 0, 0, 0),
            a * (a**8 + 2 * a**7 + a**6 + a**2 - 2 * a + 1) / d3,
            sp.Poly(
                a**17
                + 4 * a**16
                + 6 * a**15
                + 4 * a**14
                + a**13
                + 3 * a**11
                - a**10
                - 2 * a**9
                - 2 * a**8
                - a**7
                + 3 * a**6
                + a**4
                - 4 * a**3
                + 6 * a**2
                - 4 * a
                + 1,
                a,
                domain=sp.QQ,
            ),
            "no_open_unit_root",
        ),
        (
            "C2001",
            (2, 0, 0, 1),
            a
            * (a**2 + 1)
            * (a**2 + a - 1)
            * (a**4 + a**3 - a + 1)
            / d3,
            p3,
            "beta_negative",
        ),
        (
            "C2010",
            (2, 0, 1, 0),
            a * (2 * a**7 + 2 * a**6 - a + 1) / d4,
            sp.Poly(
                4 * a**15
                + 8 * a**14
                + 4 * a**13
                - 6 * a**9
                + 6 * a**8
                - 6 * a**7
                + 6 * a**6
                + a**2
                - 2 * a
                + 1,
                a,
                domain=sp.QQ,
            ),
            "no_open_unit_root",
        ),
    ]


def structural_rows(table, a, b, boundary):
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
    return rows


def numerator_polynomial(expression, variable):
    numerator = sp.together(sp.cancel(expression)).as_numer_denom()[0]
    return sp.Poly(numerator, variable, domain=sp.QQ)


def candidate_pattern_audit(table, a, b, boundary):
    candidates = {
        (1, 1, 0, 0),
        (1, 1, 0, 1),
        (1, 1, 1, 0),
        (2, 0, 0, 0),
        (2, 0, 0, 1),
        (2, 0, 1, 0),
    }
    computed = set()
    nondegenerate = {
        pattern: beta for _name, pattern, beta, _eliminant, _obstruction in branches_and_eliminants(a)
    }
    expected_solutions = {
        (1, 1, 0, 0): [-a, nondegenerate[(1, 1, 0, 0)]],
        (1, 1, 0, 1): [nondegenerate[(1, 1, 0, 1)]],
        (1, 1, 1, 0): [1 - a, nondegenerate[(1, 1, 1, 0)]],
        (2, 0, 0, 0): [nondegenerate[(2, 0, 0, 0)]],
        (2, 0, 0, 1): [2 * a, nondegenerate[(2, 0, 0, 1)]],
        (2, 0, 1, 0): [nondegenerate[(2, 0, 1, 0)]],
    }
    examined = 0
    for ell in range(3):
        for h in range(2):
            unit = find_row(table, 2 * (ell * a + h * b))
            for i in range(3):
                for g in range(2):
                    examined += 1
                    moving = find_row(
                        table, (1 - a) * boundary / a + 2 * (i + g * b) / a
                    )
                    resonant_boundary = sp.factor(
                        2 * (a * (ell * a + h * b) - (i + g * b)) / (1 - a)
                    )
                    leading = sp.factor(
                        (unit[3] + moving[3]).subs(boundary, resonant_boundary)
                    )
                    # In 0<a<b<1 the a-supplier sign is always negative, so
                    # opposite signs require ell+h even.  The elementary B>0
                    # inequalities leave precisely the six listed patterns.
                    if ell + h == 0:
                        potentially_positive = False
                    elif (ell, h) in ((1, 1), (2, 0)):
                        potentially_positive = i <= 1 and not (i == 1 and g == 1)
                    else:
                        potentially_positive = False
                    if (ell + h) % 2 == 0 and potentially_positive:
                        pattern = (ell, h, i, g)
                        computed.add(pattern)
                        require(leading != 0, f"identically zero pair at {pattern}")
                        leading_numerator = sp.factor(
                            sp.together(leading).as_numer_denom()[0]
                        )
                        solutions = [sp.factor(value) for value in sp.solve(leading_numerator, b)]
                        expected = expected_solutions[pattern]
                        require(len(solutions) == len(expected), f"leading branch count at {pattern}")
                        require(
                            all(
                                any(sp.factor(value - candidate) == 0 for candidate in solutions)
                                for value in expected
                            ),
                            f"leading branches at {pattern}",
                        )
                        if pattern == (2, 0, 1, 0):
                            require(
                                sp.factor(leading_numerator.subs(a, sp.Rational(1, 2))) == 0,
                                "missing vertical leading branch",
                            )
    require(examined == 36 and computed == candidates, "candidate-pattern census")
    # Every additional algebraic branch is outside the parameter domain.
    for pattern, discarded, expected_boundary in (
        ((1, 1, 1, 0), 1 - a, -2),
        ((2, 0, 0, 1), 2 * a, -4 * a),
    ):
        ell, h, i, g = pattern
        resonant = sp.factor(
            2 * (a * (ell * a + h * discarded) - (i + g * discarded)) / (1 - a)
        )
        require(sp.factor(resonant - expected_boundary) == 0, f"discarded branch {pattern}")
    vertical_boundary = sp.factor(
        (2 * (2 * a**2 - 1) / (1 - a)).subs(a, sp.Rational(1, 2))
    )
    require(vertical_boundary == -2, "vertical branch boundary")
    return candidates


def build_certificate():
    require(sp.__version__ == "1.13.3", "this derivation pins SymPy 1.13.3")
    a, b, boundary, variable = sp.symbols("a b B t")
    table = hinge_table((sp.Integer(1), sp.Integer(1), a, a, b), boundary, variable)
    require(len(table) == 33, "unexpected structural-row count")
    candidates = candidate_pattern_audit(table, a, b, boundary)
    rows = structural_rows(table, a, b, boundary)

    # The only equal unit-supplier walls in the complementary domain occur at
    # b=2a.  B>0 then leaves the three rows recorded below.  Their H3 sum has
    # no root even on the larger interval 0<a<1.
    triple_beta = 2 * a
    triple_boundary = 4 * a**2 / (1 - a)
    triple_substitution = {b: triple_beta, boundary: triple_boundary}
    triple_target = 4 * a
    triple_rows = []
    for label, wall, row in rows:
        if sp.factor(wall.subs(triple_substitution, simultaneous=True) - triple_target) == 0:
            triple_rows.append((label, row))
    require(
        sorted(label for label, _row in triple_rows)
        == ["A(0,0,0)", "U(0,0,1)", "U(0,2,0)"],
        "exceptional triple census",
    )
    triple_h3 = sp.cancel(
        sum(row.get(3, 0) for _label, row in triple_rows).subs(
            triple_substitution, simultaneous=True
        )
    )
    triple_polynomial = numerator_polynomial(triple_h3, a)
    require(open_root_count(triple_polynomial) == 0, "exceptional triple H3 root")

    intervals = {
        "C1101": [
            (sp.Rational(27, 40), sp.Rational(677, 1000)),
            (sp.Rational(9, 10), sp.Rational(901, 1000)),
        ],
        "C2001": [(sp.Rational(64, 125), sp.Rational(513, 1000))],
    }

    branch_records = []
    for name, pattern, beta, eliminant, obstruction in branches_and_eliminants(a):
        require(pattern in candidates, f"uncertified branch pattern {name}")
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
            difference = sp.cancel(wall.subs(substitutions, simultaneous=True) - target)
            differences[label] = difference
            coefficients[label] = {
                degree: sp.cancel(value.subs(substitutions, simultaneous=True))
                for degree, value in row.items()
            }
            if difference == 0:
                generic_rows.append(label)
                continue
            numerator = numerator_polynomial(difference, a)
            for factor, _multiplicity in sp.factor_list(numerator.as_expr())[1]:
                polynomial = sp.Poly(factor, a, domain=sp.QQ)
                if open_root_count(polynomial) == 0:
                    continue
                key = tuple(primitive_coefficients(polynomial))
                factor_map[key] = polynomial_from_coefficients(key, a)

        intended = sorted([f"U(0,{ell},{h})", f"A({i},0,{g})"])
        require(sorted(generic_rows) == intended, f"generic rows on {name}")
        generic_h3 = sp.cancel(
            sum(coefficients[label].get(3, 0) for label in generic_rows)
        )
        require(generic_h3 == 0, f"generic H3 cancellation on {name}")
        generic_h4 = sp.cancel(
            sum(coefficients[label].get(4, 0) for label in generic_rows)
        )
        generic_numerator = numerator_polynomial(generic_h4, a)
        quotient, remainder = sp.div(generic_numerator, eliminant)
        require(remainder.is_zero, f"generic eliminant on {name}")
        beta_denominator = sp.Poly(sp.cancel(beta).as_numer_denom()[1], a, domain=sp.QQ)
        for factor, _multiplicity in sp.factor_list(quotient.as_expr())[1]:
            polynomial = sp.Poly(factor, a, domain=sp.QQ)
            if open_root_count(polynomial):
                require(
                    sp.gcd(polynomial, beta_denominator).degree() > 0,
                    f"unrecorded generic H4 root on {name}",
                )
        eliminant_roots = open_root_count(eliminant)
        if obstruction == "no_open_unit_root":
            require(eliminant_roots == 0, f"unexpected eliminant root on {name}")
        else:
            require(eliminant_roots == len(intervals[name]), f"root count on {name}")
            for left, right in intervals[name]:
                require(sp.count_roots(eliminant, left, right) == 1, f"root interval {name}")
                require(
                    rational_sign_at_root(beta, eliminant, left, right) < 0,
                    f"beta obstruction on {name}",
                )

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
                numerator = numerator_polynomial(difference, a)
                if sp.rem(numerator, polynomial).is_zero:
                    colliding.append(label)
            jet_data = {}
            both_cancel = True
            for degree in (3, 4):
                aggregate = sp.cancel(
                    sum(coefficients[label].get(degree, 0) for label in colliding)
                )
                aggregate_numerator = numerator_polynomial(aggregate, a)
                common = sp.gcd(polynomial, aggregate_numerator)
                gcd_degree = common.degree()
                both_cancel &= gcd_degree > 0
                jet_data[f"H{degree}_numerator_degree"] = (
                    -1 if aggregate_numerator.is_zero else aggregate_numerator.degree()
                )
                jet_data[f"H{degree}_gcd_degree"] = gcd_degree
            require(not both_cancel, f"complementary missing wall on {name}")
            factors.append(
                {
                    "polynomial": primitive_coefficients(polynomial),
                    "degree": polynomial.degree(),
                    "open_unit_roots": open_root_count(polynomial),
                    "colliding_rows": sorted(colliding),
                    **jet_data,
                }
            )

        for label, difference in differences.items():
            if difference == 0:
                continue
            residual = numerator_polynomial(difference, a)
            for polynomial in ordered_factors:
                while residual.degree() >= polynomial.degree():
                    quotient, remainder = sp.div(residual, polynomial)
                    if not remainder.is_zero:
                        break
                    residual = quotient
            require(
                open_root_count(residual) == 0,
                f"uncovered collision on {name}, row {label}",
            )

        branch_records.append(
            {
                "name": name,
                "pattern": list(pattern),
                "generic_rows": sorted(generic_rows),
                "generic_eliminant": primitive_coefficients(eliminant),
                "generic_eliminant_roots": eliminant_roots,
                "generic_root_obstruction": obstruction,
                "other_rows": 31,
                "collision_factor_count": len(factors),
                "collision_root_count": sum(
                    item["open_unit_roots"] for item in factors
                ),
                "factors": factors,
            }
        )

    return {
        "format": "q5-complementary-double-pole-exclusion-v1",
        "coefficient_order": "ascending",
        "parameter_domain": "0<a<b<1 and B>0",
        "structural_rows": 33,
        "pair_patterns_examined": 36,
        "candidate_patterns": len(candidates),
        "exceptional_triple": {
            "condition": "b=2a",
            "rows": sorted(label for label, _row in triple_rows),
            "H3_numerator": primitive_coefficients(triple_polynomial),
            "open_unit_roots": open_root_count(triple_polynomial),
        },
        "branches": branch_records,
    }


def summary(certificate):
    canonical = dumps(certificate, sort_keys=True, separators=(",", ":"))
    factors = [
        factor for branch in certificate["branches"] for factor in branch["factors"]
    ]
    return {
        "status": "Q5_COMPLEMENTARY_DOUBLE_POLE_WALLS_EXCLUDED",
        "sympy_version": sp.__version__,
        "structural_rows": certificate["structural_rows"],
        "pair_patterns_examined": certificate["pair_patterns_examined"],
        "candidate_patterns": certificate["candidate_patterns"],
        "leading_branches": len(certificate["branches"]),
        "generic_eliminant_roots": sum(
            branch["generic_eliminant_roots"] for branch in certificate["branches"]
        ),
        "exceptional_triple_H3_roots": certificate["exceptional_triple"][
            "open_unit_roots"
        ],
        "branch_counts": {
            branch["name"]: {
                "collision_factors": branch["collision_factor_count"],
                "open_unit_roots": branch["collision_root_count"],
            }
            for branch in certificate["branches"]
        },
        "row_differences_checked": 31 * len(certificate["branches"]),
        "collision_factors": len(factors),
        "open_unit_collision_roots": sum(
            factor["open_unit_roots"] for factor in factors
        ),
        "aggregate_H4_cancellation_factors": sum(
            factor["H4_gcd_degree"] > 0 for factor in factors
        ),
        "factors_canceling_both_jets": sum(
            factor["H3_gcd_degree"] > 0 and factor["H4_gcd_degree"] > 0
            for factor in factors
        ),
        "maximum_factor_degree": max(factor["degree"] for factor in factors),
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
