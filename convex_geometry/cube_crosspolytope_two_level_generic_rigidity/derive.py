#!/usr/bin/env python3
"""Exact symbolic audit of arbitrary-q two-level resonance rigidity."""

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
    return table


def find_row(table, wall):
    matches = [candidate for candidate in table if sp.factor(candidate - wall) == 0]
    require(len(matches) == 1, f"could not identify structural row {wall}")
    return table[matches[0]]


def candidates(q: int):
    answer = []
    for p in range(1, q):
        r = q - p
        for m in range(2, min(p, r) + 1):
            k, j = p - m, r - m
            for ell in range(r + 1):
                for i in range(p + 1):
                    # The resonance boundary is positive somewhere in (0,1)
                    # exactly when its numerator is positive at a=1.
                    if ell + k - j - i > 0:
                        answer.append((p, r, m, k, ell, i, j))
    return answer


def closed_ratios(p, r, m, ell, i, a, boundary):
    q = p + r
    d = q - m
    k, j = p - m, r - m
    unit_shift = boundary + 2 * k + 2 * a * ell
    moving_shift = boundary + 2 * i + 2 * a * j
    unit_bracket = (
        m
        + r
        - ell
        - (r - ell) * a / (1 - a)
        + sp.Rational(3, 2) * k
        + ell * (1 + 2 * a) / (1 + a)
    )
    moving_bracket = (
        a * (p - i + m)
        + a * (p - i) / (1 - a)
        + i * a * (a + 2) / (1 + a)
        + sp.Rational(3, 2) * a * j
    )
    common = sp.Rational(m - 1, d + 1)
    return (
        sp.factor(common * unit_bracket / unit_shift),
        sp.factor(common * moving_bracket / moving_shift),
    )


def main() -> None:
    require(sp.__version__ == "1.13.3", "this derivation pins SymPy 1.13.3")
    a, boundary, variable = sp.symbols("a B t", positive=True)

    counts = {}
    row_ratio_checks = 0
    difference_checks = 0
    parity_relevant = 0
    examples = []
    for q in (4, 5, 6):
        entries = candidates(q)
        counts[str(q)] = len(entries)
        parity_relevant += sum((r - ell) % 2 for p, r, m, k, ell, i, j in entries)
        for p in range(1, q):
            r = q - p
            local = [entry for entry in entries if entry[0] == p]
            if not local:
                continue
            table = hinge_table((sp.Integer(1),) * p + (a,) * r, boundary, variable)
            for _, _, m, k, ell, i, j in local:
                unit_wall = sp.factor(2 * (k + a * ell))
                moving_wall = sp.factor((1 - a) * boundary / a + 2 * i / a + 2 * j)
                resonance_boundary = sp.factor(
                    2 * (a * k + a**2 * ell - i - a * j) / (1 - a)
                )
                degree = q - m
                unit = find_row(table, unit_wall)
                moving = find_row(table, moving_wall)
                actual_unit = sp.factor(
                    unit[degree + 1].subs(boundary, resonance_boundary)
                    / unit[degree].subs(boundary, resonance_boundary)
                )
                actual_moving = sp.factor(
                    moving[degree + 1].subs(boundary, resonance_boundary)
                    / moving[degree].subs(boundary, resonance_boundary)
                )
                expected_unit, expected_moving = closed_ratios(
                    p, r, m, ell, i, a, resonance_boundary
                )
                require(
                    sp.factor(actual_unit - expected_unit) == 0,
                    "unit-row ratio mismatch",
                )
                require(
                    sp.factor(actual_moving - expected_moving) == 0,
                    "moving-row ratio mismatch",
                )
                row_ratio_checks += 2

                x = k - i + a * (ell - j)
                expected_difference = -(
                    (m - 1) * (q * (1 + a) ** 2 - 4 * a * (i + ell))
                ) / (4 * x * (q - m + 1) * (1 + a))
                actual_difference = sp.factor(actual_unit - actual_moving)
                require(
                    sp.factor(actual_difference - expected_difference) == 0,
                    "resonance-ratio difference mismatch",
                )
                difference_checks += 1
                if (r - ell) % 2 and len(examples) < 8:
                    examples.append(
                        {
                            "parameters": [p, r, m, ell, i],
                            "difference": sp.sstr(actual_difference),
                        }
                    )

    q, i, ell = sp.symbols("q i ell", integer=True, nonnegative=True)
    margin = q * (1 + a) ** 2 - 4 * a * (i + ell)
    positive_form = q * (1 - a) ** 2 + 4 * a * (q - i - ell)
    require(sp.expand(margin - positive_form) == 0, "positive-margin identity failed")

    payload = {
        "status": "TWO_LEVEL_GENERIC_RIGIDITY_DERIVED",
        "sympy_version": sp.__version__,
        "dimensions": [4, 5, 6],
        "higher_multiplicity_candidate_counts": counts,
        "row_ratio_checks": row_ratio_checks,
        "difference_checks": difference_checks,
        "parity_relevant_checks": parity_relevant,
        "ratio_difference": "-(m - 1)*(q*(a + 1)**2 - 4*a*(ell + i))/(4*X*(a + 1)*(q - m + 1))",
        "positive_margin_identity": "q*(a - 1)**2 + 4*a*(q - ell - i)",
        "sample_parity_relevant_differences": examples,
    }
    canonical = dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["certificate_sha256"] = sha256(canonical.encode()).hexdigest()
    print(dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
