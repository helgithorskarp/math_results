#!/usr/bin/env python3
"""SymPy reconstruction of all low-dimensional two-level collision walls."""

from __future__ import annotations

from collections import defaultdict
from hashlib import sha256
from json import dumps
from math import comb, factorial, gcd

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


# coefficient, B power, B shift, lambda, wall shift, slack power
Term = tuple[sp.Expr, int, sp.Expr, sp.Expr, sp.Expr, int]


def compact_terms(terms: list[Term]) -> list[Term]:
    coefficients = {}
    for coefficient, b_power, shift, lam, wall_shift, slack_power in terms:
        key = (b_power, shift, lam, wall_shift, slack_power)
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
            beta = sp.Rational(
                comb(b_power, moment)
                * factorial(moment)
                * factorial(slack_power),
                factorial(moment + slack_power + 1),
            )
            answer.append(
                (
                    sp.factor(coefficient * eta * beta),
                    b_power - moment,
                    shift + 2 * weight,
                    lam,
                    wall_shift + 2 * weight * (1 + lam),
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


def affine_rows(weights, variable):
    rows = defaultdict(lambda: defaultdict(list))
    for coefficient, b_power, shift, lam, wall_shift, degree in global_terms(
        weights, variable
    ):
        rows[(lam, wall_shift)][degree].append((coefficient, b_power, shift))
    return rows


def row_value(row, degree, boundary):
    return sp.factor(
        sum(
            (
                coefficient * (boundary + shift) ** b_power
                for coefficient, b_power, shift in row.get(degree, ())
            ),
            sp.Integer(0),
        )
    )


def collision_parameters(p: int, r: int):
    answer = set()
    for s in range(1, min(p, r - 1) + 1):
        for t in range(s + 1, r + 1):
            if gcd(s, t) != 1:
                continue
            if (s <= p - 1 and t <= r) or (s <= p and t <= r - 1):
                answer.add(sp.Rational(s, t))
    return sorted(answer)


def structural_groups(p: int, r: int, a):
    unit = defaultdict(list)
    moving = defaultdict(list)
    for k in range(p):
        for ell in range(r + 1):
            unit[sp.factor(2 * (k + a * ell))].append((k, ell))
    for i in range(p + 1):
        for j in range(r):
            moving[sp.factor(2 * i / a + 2 * j)].append((i, j))
    return unit, moving


def main() -> None:
    require(sp.__version__ == "1.13.3", "this derivation pins SymPy 1.13.3")
    variable = sp.symbols("t")
    counts = {}
    vanished = []
    degree_vectors_checked = 0

    for q in range(4, 8):
        cross_count = 0
        multirow_count = 0
        for p in range(1, q):
            r = q - p
            for a in collision_parameters(p, r):
                lam = (1 - a) / a
                rows = affine_rows((sp.Integer(1),) * p + (a,) * r, variable)
                unit_groups, moving_groups = structural_groups(p, r, a)
                for unit_wall, unit_indices in unit_groups.items():
                    unit_row = rows[(sp.Integer(0), unit_wall)]
                    for moving_offset, moving_indices in moving_groups.items():
                        boundary = sp.factor((unit_wall - moving_offset) / lam)
                        if boundary <= 0:
                            continue
                        cross_count += 1
                        if len(unit_indices) == len(moving_indices) == 1:
                            continue
                        multirow_count += 1
                        moving_row = rows[(lam, moving_offset)]
                        vector = [
                            sp.factor(
                                row_value(unit_row, degree, boundary)
                                + row_value(moving_row, degree, boundary)
                            )
                            for degree in range(q)
                        ]
                        degree_vectors_checked += q
                        if not any(vector):
                            vanished.append(
                                [
                                    q,
                                    p,
                                    r,
                                    str(a),
                                    str(unit_wall),
                                    str(boundary),
                                    unit_indices,
                                    moving_indices,
                                ]
                            )
        counts[str(q)] = {
            "positive_cross_walls_at_collision_parameters": cross_count,
            "multirow_walls": multirow_count,
        }

    require(not vanished, "a low-dimensional multirow wall vanished")
    q, a, i, ell = sp.symbols("q a i ell")
    margin = q * (1 + a) ** 2 - 4 * a * (i + ell)
    positive_form = q * (1 - a) ** 2 + 4 * a * (q - i - ell)
    require(sp.expand(margin - positive_form) == 0, "margin identity failed")

    s, t, k = sp.symbols("s t k", integer=True)
    require(
        sp.expand(t * (k + s) + s * (ell - t) - (t * k + s * ell)) == 0,
        "unit collision step failed",
    )
    require(
        sp.expand(t * (i + s) + s * (sp.Symbol("j") - t) - (t * i + s * sp.Symbol("j")))
        == 0,
        "moving collision step failed",
    )

    payload = {
        "status": "TWO_LEVEL_COLLISION_CLOSURE_DERIVED",
        "sympy_version": sp.__version__,
        "dimensions": [4, 7],
        "counts": counts,
        "multirow_walls_checked": sum(entry["multirow_walls"] for entry in counts.values()),
        "degree_coefficients_checked": degree_vectors_checked,
        "vanishing_multirow_walls": len(vanished),
        "collision_steps": {"unit_degree_step": "s", "moving_degree_step": "t"},
        "positive_margin_identity": "q*(1-a)**2 + 4*a*(q-i-ell)",
    }
    canonical = dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["certificate_sha256"] = sha256(canonical.encode()).hexdigest()
    print(dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
