#!/usr/bin/env python3
"""Exact symbolic derivation of a minimal three-level double-pole missing wall."""

from __future__ import annotations

from hashlib import sha256
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
        table[wall][slack_power] = sp.factor(table[wall][slack_power] + value)
    return {
        wall: {degree: value for degree, value in values.items() if value != 0}
        for wall, values in table.items()
    }


def find_row(table, wall):
    matches = [candidate for candidate in table if sp.factor(candidate - wall) == 0]
    require(len(matches) == 1, f"could not identify structural row {wall}")
    return table[matches[0]]


def main() -> None:
    require(sp.__version__ == "1.13.3", "this derivation pins SymPy 1.13.3")
    a, b, boundary, variable = sp.symbols("a b B t")
    polynomial = sp.Poly(
        a**10
        - 3 * a**9
        + 4 * a**8
        - 4 * a**7
        + 5 * a**6
        - 7 * a**5
        + 5 * a**4
        - 4 * a**3
        + 4 * a**2
        - 3 * a
        + 1,
        a,
        domain=sp.QQ,
    )
    left, right = sp.Rational(127, 200), sp.Rational(637, 1000)
    require(polynomial.eval(left) > 0, "wrong sign at left endpoint")
    require(polynomial.eval(right) < 0, "wrong sign at right endpoint")
    require(sp.count_roots(polynomial, left, right) == 1, "root is not isolated")

    beta = sp.factor(a * (1 - a**6) / (1 + a**7))
    resonant_boundary = sp.factor(2 * a * beta / (1 - a))
    table = hinge_table((sp.Integer(1), sp.Integer(1), a, a, b), boundary, variable)
    require(len(table) == 33, "unexpected structural-row count")

    unit = find_row(table, 2 * b)
    moving = find_row(table, (1 - a) * boundary / a)
    require(sorted(unit) == [3, 4], "unit row does not have exactly two jets")
    require(sorted(moving) == [3, 4], "moving row does not have exactly two jets")

    resonance = {boundary: 2 * a * b / (1 - a)}
    expected = {
        "unit3": 1 / (3 * a**2 * (a - 1) ** 3 * (b + 1)),
        "moving3": -a**5 / (3 * (a - 1) ** 3 * (a - b)),
        "unit4": -(8 * a * b + 7 * a - 6 * b - 5)
        / (24 * a**2 * b * (a - 1) ** 3 * (b + 1) ** 2),
        "moving4": a**5 * (5 * a**2 - 6 * a * b - 7 * a + 8 * b)
        / (24 * b * (a - 1) ** 3 * (a - b) ** 2),
    }
    actual = {
        "unit3": unit[3].subs(resonance),
        "moving3": moving[3].subs(resonance),
        "unit4": unit[4].subs(resonance),
        "moving4": moving[4].subs(resonance),
    }
    for name in expected:
        require(sp.factor(actual[name] - expected[name]) == 0, f"{name} mismatch")

    substitution = {boundary: resonant_boundary, b: beta}
    leading_sum = sp.factor(
        (unit[3] + moving[3]).subs(substitution, simultaneous=True)
    )
    next_sum = sp.factor(
        (unit[4] + moving[4]).subs(substitution, simultaneous=True)
    )
    require(leading_sum == 0, "leading coefficient did not cancel")
    expected_next = -(
        (a + 1)
        * (a**2 + 1)
        * (a**6 - a**5 + a**4 - a**3 + a**2 - a + 1) ** 2
        * polynomial.as_expr()
    ) / (
        24
        * a**9
        * (a - 1) ** 4
        * (a**2 - a + 1)
        * (a**2 + a + 1)
    )
    require(sp.factor(next_sum - expected_next) == 0, "next coefficient mismatch")

    ratio_difference = sp.factor(
        actual["unit4"] / actual["unit3"]
        - actual["moving4"] / actual["moving3"]
    )
    expected_ratio_difference = -(
        (a + 1) * (3 * a * b + 2 * a - 2 * b**2 - 3 * b)
    ) / (8 * b * (a - b) * (b + 1))
    require(
        sp.factor(ratio_difference - expected_ratio_difference) == 0,
        "two-jet ratio identity failed",
    )

    target = 2 * beta
    identical = []
    coprime = 0
    for wall, row in table.items():
        difference = sp.factor(
            wall.subs(substitution, simultaneous=True) - target
        )
        if difference == 0:
            identical.append((sp.sstr(wall), sorted(row)))
            continue
        numerator = sp.together(difference).as_numer_denom()[0]
        require(
            sp.gcd(polynomial, sp.Poly(numerator, a, domain=sp.QQ)).degree() == 0,
            f"unresolved extra collision at {wall}",
        )
        coprime += 1
    require(len(identical) == 2 and coprime == 31, "wall isolation failed")

    payload = {
        "status": "THREE_LEVEL_DOUBLE_POLE_MISSING_WALL_DERIVED",
        "sympy_version": sp.__version__,
        "active_dimension": 5,
        "weight_multiplicities": [2, 2, 1],
        "root_interval": ["127/200", "637/1000"],
        "defining_polynomial": sp.sstr(polynomial.as_expr()),
        "structural_rows": len(table),
        "rows_at_target_wall": len(identical),
        "other_rows_coprime_to_polynomial": coprime,
        "target_row_degrees": [3, 4],
        "cancelled_degrees": [3, 4],
        "minimal_active_dimension": 5,
    }
    canonical = dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["certificate_sha256"] = sha256(canonical.encode()).hexdigest()
    print(dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
