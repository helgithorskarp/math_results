#!/usr/bin/env python3
"""Exact symbolic derivation for the repeated-weight q=3 classification."""

from __future__ import annotations

from hashlib import sha256
from itertools import product
from json import dumps
from math import comb, factorial

import sympy as sp


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def principal_parts(weights, variable):
    size = len(weights)
    transform = 1 / (
        (1 - variable) ** size
        * sp.prod(weights)
        * sp.prod(1 - weight + weight * variable for weight in weights)
    )
    answer = []
    for target in dict.fromkeys(weights):
        multiplicity = weights.count(target)
        lam = sp.factor((1 - target) / target)
        regularized = sp.cancel((variable + lam) ** multiplicity * transform)
        for order in range(1, multiplicity + 1):
            coefficient = sp.factor(
                sp.diff(regularized, variable, multiplicity - order).subs(
                    variable, -lam
                )
                / factorial(multiplicity - order)
            )
            answer.append((lam, order, coefficient))
    return answer


# coefficient*(B+shift)^b_power*(s-lambda*B-wall_shift)_+^slack_power
Term = tuple[sp.Expr, int, sp.Expr, sp.Expr, sp.Expr, int]


def compact_terms(terms: list[Term]) -> list[Term]:
    coefficients = {}
    for coefficient, b_power, shift, lam, wall_shift, slack_power in terms:
        key = (
            b_power,
            sp.factor(shift),
            sp.factor(lam),
            sp.factor(wall_shift),
            slack_power,
        )
        coefficients[key] = sp.factor(coefficients.get(key, 0) + coefficient)
    return [
        (coefficient, *key)
        for key, coefficient in coefficients.items()
        if coefficient != 0
    ]


def baseline_terms(weights, variable) -> list[Term]:
    size = len(weights)
    return [
        (
            sp.factor(
                coefficient / (factorial(order - 1) * factorial(size - order))
            ),
            order - 1,
            sp.Integer(0),
            lam,
            sp.Integer(0),
            size - order,
        )
        for lam, order, coefficient in principal_parts(weights, variable)
    ]


def tail_replace(terms: list[Term], weight) -> list[Term]:
    answer = []
    for coefficient, b_power, shift, lam, wall_shift, slack_power in terms:
        for moment in range(b_power + 1):
            eta = sp.factor(
                weight**moment / (1 + weight + lam * weight) ** (moment + 1)
                - 1 / (weight * (1 + lam) ** (moment + 1))
            )
            beta_factor = sp.Rational(
                comb(b_power, moment)
                * factorial(moment)
                * factorial(slack_power),
                factorial(moment + slack_power + 1),
            )
            answer.append(
                (
                    sp.factor(coefficient * eta * beta_factor),
                    b_power - moment,
                    shift + 2 * weight,
                    lam,
                    sp.factor(wall_shift + 2 * weight * (1 + lam)),
                    slack_power + moment + 1,
                )
            )
    return compact_terms(answer)


def global_terms(weights, variable) -> list[Term]:
    size = len(weights)
    answer = []
    for mask in range((1 << size) - 1):
        remaining = tuple(
            weights[index] for index in range(size) if not ((mask >> index) & 1)
        )
        terms = baseline_terms(remaining, variable)
        for index, weight in enumerate(weights):
            if (mask >> index) & 1:
                terms = tail_replace(terms, weight)
        answer.extend(terms)
    return compact_terms(answer)


def hinge_table(weights, boundary, variable):
    table = {}
    for coefficient, b_power, shift, lam, wall_shift, slack_power in global_terms(
        weights, variable
    ):
        wall = sp.factor(lam * boundary + wall_shift)
        value = sp.factor(coefficient * (boundary + shift) ** b_power)
        table.setdefault(wall, {}).setdefault(slack_power, 0)
        table[wall][slack_power] = sp.factor(
            table[wall][slack_power] + value
        )
    return {
        wall: {degree: value for degree, value in values.items() if value != 0}
        for wall, values in table.items()
    }


def check_table(actual, expected, name):
    require(len(actual) == len(expected), f"{name}: wrong wall count")
    for wall, expected_vector in expected.items():
        matches = [candidate for candidate in actual if sp.factor(candidate - wall) == 0]
        require(len(matches) == 1, f"{name}: wall match failed at {wall}")
        actual_vector = actual[matches[0]]
        require(set(actual_vector) == set(expected_vector),
                f"{name}: wrong hinge degrees at {wall}")
        for degree, expected_value in expected_vector.items():
            require(sp.factor(actual_vector[degree] - expected_value) == 0,
                    f"{name}: wrong coefficient at {wall}, degree {degree}")


def serialized_table(table):
    rows = []
    for wall in sorted(table, key=sp.sstr):
        rows.append({
            "wall": sp.sstr(wall),
            "hinges": {
                str(degree): sp.sstr(sp.factor(value))
                for degree, value in sorted(table[wall].items())
            },
        })
    return rows


def main() -> None:
    require(sp.__version__ == "1.13.3", "this derivation pins SymPy 1.13.3")
    a, boundary, variable = sp.symbols("a B t", positive=True)
    lam = (1 - a) / a

    table_11a = hinge_table((sp.Integer(1), sp.Integer(1), a), boundary, variable)
    expected_11a = {
        sp.Integer(0): {
            1: -boundary / (a * (a - 1)),
            2: -(4 * a - 3) / (2 * a * (a - 1) ** 2),
        },
        2 * a: {
            1: -(boundary + 2 * a) / (a * (a + 1)),
            2: -(4 * a + 3) / (2 * a * (a + 1) ** 2),
        },
        sp.Integer(2): {2: 1 / (2 * a * (a - 1))},
        2 * (a + 1): {2: 1 / (2 * a * (a + 1))},
        sp.factor(lam * boundary): {2: a**3 / (2 * (a - 1) ** 2)},
        sp.factor(lam * boundary + 2 / a): {
            2: -a**3 / ((a - 1) * (a + 1))
        },
        sp.factor(lam * boundary + 4 / a): {2: a**3 / (2 * (a + 1) ** 2)},
    }
    check_table(table_11a, expected_11a, "(1,1,a)")

    table_1aa = hinge_table((sp.Integer(1), a, a), boundary, variable)
    expected_1aa = {
        sp.Integer(0): {2: 1 / (2 * a**2 * (a - 1) ** 2)},
        2 * a: {2: 1 / (a**2 * (a - 1) * (a + 1))},
        4 * a: {2: 1 / (2 * a**2 * (a + 1) ** 2)},
        sp.factor(lam * boundary): {
            1: boundary / (a - 1),
            2: a * (3 * a - 4) / (2 * (a - 1) ** 2),
        },
        sp.factor(lam * boundary + 2): {2: -a / (2 * (a - 1))},
        sp.factor(lam * boundary + 2 / a): {
            1: -(boundary + 2) / (a + 1),
            2: -a * (3 * a + 4) / (2 * (a + 1) ** 2),
        },
        sp.factor(lam * boundary + 2 + 2 / a): {2: a / (2 * (a + 1))},
    }
    check_table(table_1aa, expected_1aa, "(1,a,a)")

    table_111 = hinge_table((sp.Integer(1),) * 3, boundary, variable)
    expected_111 = {
        sp.Integer(0): {0: boundary**2 / 2, 1: 3 * boundary, 2: sp.Integer(3)},
        sp.Integer(2): {1: -3 * (boundary + 2) / 2, 2: sp.Rational(-21, 8)},
        sp.Integer(4): {2: sp.Rational(3, 8)},
    }
    check_table(table_111, expected_111, "(1,1,1)")

    exceptional_polynomial = a**4 + a - 1
    exceptional_boundary = 2 * a / (1 - a)
    aggregate = sp.factor(
        expected_11a[sp.Integer(2)][2]
        + expected_11a[sp.factor(lam * boundary)][2]
    )
    aggregate_at_resonance = sp.factor(aggregate.subs(boundary, exceptional_boundary))
    require(
        aggregate_at_resonance
        == exceptional_polynomial / (2 * a * (a - 1) ** 2),
        "exceptional cancellation factor mismatch",
    )

    resonance_parameters = {
        "11a": (
            2 * a / lam,
            2 / lam,
            2 * (1 + a) / lam,
            (2 * (1 + a) - 2 / a) / lam,
        ),
        "1aa": (
            2 * a / lam,
            4 * a / lam,
            (4 * a - 2) / lam,
            (4 * a - 2 / a) / lam,
        ),
    }
    separation_checks = 0
    for name, parameters in resonance_parameters.items():
        for first_index in range(len(parameters)):
            for second_index in range(first_index + 1, len(parameters)):
                numerator = sp.factor(
                    sp.together(parameters[first_index] - parameters[second_index])
                    .as_numer_denom()[0]
                )
                polynomial_difference = sp.Poly(numerator, a, domain=sp.QQ)
                for boundary_factor in (sp.Poly(a, a), sp.Poly(a - 1, a)):
                    while sp.rem(polynomial_difference, boundary_factor).is_zero:
                        polynomial_difference = sp.quo(
                            polynomial_difference, boundary_factor
                        )
                require(
                    polynomial_difference.count_roots(0, 1) == 0,
                    f"simultaneous interior resonance in {name}",
                )
                separation_checks += 1

    polynomial = sp.Poly(exceptional_polynomial, a, domain=sp.QQ)
    low = sp.Rational(724491959, 10**9)
    high = sp.Rational(724491960, 10**9)
    require(polynomial.count_roots(0, 1) == 1, "exceptional root is not unique")
    require(polynomial.count_roots(low, high) == 1, "root isolation failed")
    root = next(root for root in polynomial.real_roots() if 0 < root < 1)

    rows_11a = serialized_table(table_11a)
    rows_1aa = serialized_table(table_1aa)
    rows_111 = serialized_table(table_111)
    result = {
        "status": "Q3_REPEATED_WEIGHT_CLASSIFICATION_DERIVED",
        "computer_algebra": "SymPy 1.13.3 over QQ(a,B)",
        "repeated_weight_strata": ["(1,1,a)", "(1,a,a)", "(1,1,1)"],
        "structural_wall_rows": [len(rows_11a), len(rows_1aa), len(rows_111)],
        "hinge_table_sha256": {
            "11a": sha256(dumps(rows_11a, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
            "1aa": sha256(dumps(rows_1aa, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
            "111": sha256(dumps(rows_111, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        },
        "positive_cross_resonance_types": {"11a": 4, "1aa": 4},
        "resonance_parameter_separation_checks": separation_checks,
        "new_missing_wall_orbits": 1,
        "exceptional_orbit": {
            "weights": "(1,1,a) up to permutation",
            "minimal_polynomial": sp.sstr(exceptional_polynomial),
            "a_isolating_interval": [str(low), str(high)],
            "a_approximation": str(sp.N(root, 18)),
            "B_formula": sp.sstr(exceptional_boundary),
            "B_approximation": str(sp.N(exceptional_boundary.subs(a, root), 18)),
            "wall": "2",
            "aggregate_quadratic_factor": sp.sstr(aggregate_at_resonance),
        },
        "scope": (
            "Together with the distinct-weight classification, this gives all "
            "positive missing candidate walls for three active weights."
        ),
    }
    print(dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
