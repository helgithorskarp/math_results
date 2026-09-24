#!/usr/bin/env python3
"""Symbolic derivation for the q=5 two-level missing-wall classification."""

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


def serialized_table(table):
    return [
        {
            "wall": sp.sstr(wall),
            "hinges": {
                str(degree): sp.sstr(sp.factor(value))
                for degree, value in sorted(table[wall].items())
            },
        }
        for wall in sorted(table, key=sp.sstr)
    ]


def candidates(q: int):
    answer = []
    for p in range(1, q):
        r = q - p
        for m in range(1, min(p, r) + 1):
            k, j = p - m, r - m
            for ell in range(r + 1):
                for i in range(p + 1):
                    # There is some 0<a<1 with B>0 iff this endpoint is positive.
                    if ell + k - j - i > 0:
                        answer.append((p, r, m, k, ell, i, j))
    return answer


def lowest_formula(p, r, m, ell, i, a):
    """Closed coefficient of H_(q-m) at a cross-family resonance."""
    q = p + r
    k, j = p - m, r - m
    x = k - i + a * (ell - j)
    common = (
        2 ** (m - 1)
        * x ** (m - 1)
        / (sp.factorial(m - 1) * sp.factorial(q - m) * (1 - a) ** (m - 1))
    )
    unit = (
        sp.binomial(p, m)
        * sp.binomial(r, ell)
        * (-1) ** (p - m + ell)
        / (
            2 ** (p - m)
            * a**r
            * (1 - a) ** (r - ell)
            * (1 + a) ** ell
        )
    )
    moving = (
        sp.binomial(p, i)
        * sp.binomial(r, m)
        * (-1) ** (q - m)
        * a ** (2 * p - 1)
        / (
            2 ** (r - m)
            * (1 - a) ** (p - i)
            * (1 + a) ** i
        )
    )
    return sp.factor(common * (unit + moving))


def primitive_positive(expression, variable):
    polynomial = sp.Poly(expression, variable, domain=sp.QQ)
    polynomial = sp.Poly(polynomial.clear_denoms()[1], variable, domain=sp.ZZ)
    _, polynomial = polynomial.primitive()
    if polynomial.LC() < 0:
        polynomial = -polynomial
    return polynomial


def internal_collisions(p: int, r: int):
    answer = []
    constant = [(k, ell) for k in range(p) for ell in range(r + 1)]
    for index, first in enumerate(constant):
        for second in constant[index + 1 :]:
            k1, ell1 = first
            k2, ell2 = second
            if ell1 == ell2:
                continue
            value = sp.Rational(k2 - k1, ell1 - ell2)
            if 0 < value < 1:
                answer.append(("constant", value, first, second))
    moving = [(i, j) for i in range(p + 1) for j in range(r)]
    for index, first in enumerate(moving):
        for second in moving[index + 1 :]:
            i1, j1 = first
            i2, j2 = second
            if j1 == j2:
                continue
            value = sp.Rational(i2 - i1, j1 - j2)
            if 0 < value < 1:
                answer.append(("moving", value, first, second))
    return answer


def main() -> None:
    require(sp.__version__ == "1.13.3", "this derivation pins SymPy 1.13.3")
    a, boundary, variable = sp.symbols("a B t", positive=True)
    lam = (1 - a) / a

    # Check the arbitrary-q coefficient formula against exact principal parts
    # in every positive resonance type for q=3,4,5.
    tables = {}
    formula_checks = 0
    for q in (3, 4, 5):
        for p in range(1, q):
            r = q - p
            table = hinge_table((sp.Integer(1),) * p + (a,) * r, boundary, variable)
            tables[(p, r)] = table
            for pp, rr, m, k, ell, i, j in candidates(q):
                if (pp, rr) != (p, r):
                    continue
                constant_wall = sp.factor(2 * (k + a * ell))
                moving_wall = sp.factor(lam * boundary + 2 * i / a + 2 * j)
                resonance_boundary = sp.factor(
                    a * (constant_wall - 2 * i / a - 2 * j) / (1 - a)
                )
                degree = q - m
                actual = sp.factor(
                    (
                        find_row(table, constant_wall).get(degree, 0)
                        + find_row(table, moving_wall).get(degree, 0)
                    ).subs(boundary, resonance_boundary)
                )
                expected = lowest_formula(p, r, m, ell, i, a)
                require(sp.factor(actual - expected) == 0, "closed coefficient mismatch")
                formula_checks += 1
    require(formula_checks == 42, "wrong number of formula checks")

    q5_candidates = candidates(5)
    parity_candidates = [entry for entry in q5_candidates if (entry[1] - entry[4]) % 2]
    require(len(q5_candidates) == 26, "wrong q=5 candidate count")
    require(len(parity_candidates) == 9, "wrong q=5 parity count")

    orbit_polynomials = {
        (4, 1, 0, 0): 2 * a**8 + a**3 - 3 * a**2 + 3 * a - 1,
        (4, 1, 0, 1): 8 * a**8 - a**3 + a**2 + a - 1,
        (4, 1, 0, 2): 12 * a**8 + a**3 + a**2 - a - 1,
        (3, 2, 1, 0): 2 * a**8 + 2 * a**7 - 3 * a**2 + 6 * a - 3,
        (3, 2, 1, 1): 2 * a**7 + a - 1,
        (2, 3, 2, 0): a**8 + 2 * a**7 + a**6 + 4 * a - 4,
    }
    intervals = {
        (4, 1, 0, 0): (sp.Rational(630979443162, 10**12), sp.Rational(630979443163, 10**12)),
        (4, 1, 0, 1): (sp.Rational(636690912035, 10**12), sp.Rational(636690912036, 10**12)),
        (4, 1, 0, 2): (sp.Rational(716658280303, 10**12), sp.Rational(716658280304, 10**12)),
        (3, 2, 1, 0): (sp.Rational(697890411717, 10**12), sp.Rational(697890411718, 10**12)),
        (3, 2, 1, 1): (sp.Rational(745071972941, 10**12), sp.Rational(745071972942, 10**12)),
        (2, 3, 2, 0): (sp.Rational(795592019016, 10**12), sp.Rational(795592019017, 10**12)),
    }

    orbits = []
    for entry in parity_candidates:
        p, r, m, k, ell, i, j = entry
        table = tables[(p, r)]
        constant_wall = sp.factor(2 * (k + a * ell))
        moving_wall = sp.factor(lam * boundary + 2 * i / a + 2 * j)
        resonance_boundary = sp.factor(
            a * (constant_wall - 2 * i / a - 2 * j) / (1 - a)
        )
        degree = 5 - m
        vectors = []
        for hinge_degree in range(degree, 5):
            aggregate = sp.factor(
                (
                    find_row(table, constant_wall).get(hinge_degree, 0)
                    + find_row(table, moving_wall).get(hinge_degree, 0)
                ).subs(boundary, resonance_boundary)
            )
            vectors.append(primitive_positive(sp.together(aggregate).as_numer_denom()[0], a))

        if m == 1:
            key = (p, r, ell, i)
            expected = sp.Poly(orbit_polynomials[key], a, domain=sp.ZZ)
            require(vectors == [expected], f"wrong orbit polynomial for {key}")
            require(expected.is_irreducible, f"reducible orbit polynomial for {key}")
            low, high = intervals[key]
            require(expected.count_roots(0, 1) == 1, f"nonunique root for {key}")
            require(expected.count_roots(low, high) == 1, f"root isolation failed for {key}")
            require(ell * low**2 + (k - j) * low - i > 0, f"root outside B>0 domain for {key}")
            root = next(root for root in expected.real_roots() if 0 < root < 1)
            orbits.append(
                {
                    "weights": f"1^{p} a^{r}",
                    "indices": [k, ell, i, j],
                    "minimal_polynomial": sp.sstr(expected.as_expr()),
                    "a_isolating_interval": [str(low), str(high)],
                    "a_approximation": str(sp.N(root, 18)),
                    "B_formula": sp.sstr(resonance_boundary),
                    "B_approximation": str(sp.N(resonance_boundary.subs(a, root), 18)),
                    "wall_formula": sp.sstr(constant_wall),
                    "wall_approximation": str(sp.N(constant_wall.subs(a, root), 18)),
                }
            )

    obstruction_expected = {
        (3, 2, 1, 0): (
            a**8 + a**7 - 3 * a**2 + 6 * a - 3,
            10 * a**10 + 4 * a**9 - 22 * a**8 - 16 * a**7 - 45 * a**4 + 90 * a**3 - 12 * a**2 - 66 * a + 33,
            908446872528,
        ),
        (3, 2, 1, 1): (
            a**7 + a - 1,
            10 * a**9 - 2 * a**8 - 16 * a**7 + 15 * a**3 - 15 * a**2 - 11 * a + 11,
            55973,
        ),
        (2, 3, 2, 0): (
            a**8 + 2 * a**7 + a**6 + 2 * a - 2,
            11 * a**10 + 18 * a**9 - 12 * a**8 - 34 * a**7 - 15 * a**6 + 32 * a**3 - 36 * a**2 - 16 * a + 20,
            1429061632,
        ),
    }
    obstruction_resultants = {}
    for p, r, m, k, ell, i, j in parity_candidates:
        if m == 1:
            continue
        table = tables[(p, r)]
        constant_wall = 2 * (k + a * ell)
        moving_wall = lam * boundary + 2 * i / a + 2 * j
        resonance_boundary = sp.factor(
            a * (constant_wall - 2 * i / a - 2 * j) / (1 - a)
        )
        polys = []
        for degree in (3, 4):
            aggregate = sp.factor(
                (
                    find_row(table, constant_wall).get(degree, 0)
                    + find_row(table, moving_wall).get(degree, 0)
                ).subs(boundary, resonance_boundary)
            )
            polys.append(primitive_positive(sp.together(aggregate).as_numer_denom()[0], a))
        key = (p, r, ell, i)
        expected_first, expected_second, expected_resultant = obstruction_expected[key]
        require(polys[0] == sp.Poly(expected_first, a), f"wrong first obstruction {key}")
        require(polys[1] == sp.Poly(expected_second, a), f"wrong second obstruction {key}")
        result = abs(int(sp.resultant(polys[0], polys[1])))
        require(result == expected_resultant, f"wrong resultant {key}")
        require(sp.gcd(polys[0], polys[1]).degree() == 0, f"common obstruction root {key}")
        obstruction_resultants[f"{p}{r}_{ell}{i}"] = result

    expected_internal = {
        (4, 1): [],
        (3, 2): [
            ("constant", sp.Rational(1, 2), (0, 2), (1, 0)),
            ("constant", sp.Rational(1, 2), (1, 2), (2, 0)),
        ],
        (2, 3): [
            ("constant", sp.Rational(1, 2), (0, 2), (1, 0)),
            ("constant", sp.Rational(1, 3), (0, 3), (1, 0)),
            ("constant", sp.Rational(1, 2), (0, 3), (1, 1)),
            ("moving", sp.Rational(1, 2), (0, 2), (1, 0)),
            ("moving", sp.Rational(1, 2), (1, 2), (2, 0)),
        ],
        (1, 4): [
            ("moving", sp.Rational(1, 2), (0, 2), (1, 0)),
            ("moving", sp.Rational(1, 3), (0, 3), (1, 0)),
            ("moving", sp.Rational(1, 2), (0, 3), (1, 1)),
        ],
    }
    for key, expected in expected_internal.items():
        observed = internal_collisions(*key)
        require(observed == expected, f"wrong internal collisions for {key}")
        p, r = key
        for family, _, first, second in observed:
            if family == "constant":
                require(r + first[0] != r + second[0], "equal internal lowest degrees")
            else:
                require(p + first[1] != p + second[1], "equal internal lowest degrees")

    special_cases = {
        (3, 2): [sp.Rational(1, 2)],
        (2, 3): [sp.Rational(1, 3), sp.Rational(1, 2)],
        (1, 4): [sp.Rational(1, 3), sp.Rational(1, 2)],
    }
    cross_checks = 0
    for (p, r), values in special_cases.items():
        for value in values:
            weights = (sp.Integer(1),) * p + (value,) * r
            local_lam = (1 - value) / value
            constant_walls = {2 * (k + value * ell) for k in range(p) for ell in range(r + 1)}
            offsets = {2 * i / value + 2 * j for i in range(p + 1) for j in range(r)}
            boundaries = sorted(
                {(wall - offset) / local_lam for wall in constant_walls for offset in offsets if wall > 0 and wall > offset}
            )
            for resonance_boundary in boundaries:
                table = hinge_table(weights, resonance_boundary, variable)
                require(
                    all(vector for wall, vector in table.items() if wall > 0),
                    f"special internal collision disappeared at {(p, r, value, resonance_boundary)}",
                )
                cross_checks += 1
    require(cross_checks == 25, "wrong special cross-resonance audit count")

    diagonal = tables[(5, 0)] if (5, 0) in tables else hinge_table((sp.Integer(1),) * 5, boundary, variable)
    expected_diagonal_walls = {sp.Integer(0), sp.Integer(2), sp.Integer(4), sp.Integer(6), sp.Integer(8)}
    require(set(diagonal) == expected_diagonal_walls, "wrong diagonal walls")
    require(all(diagonal[wall] for wall in expected_diagonal_walls if wall > 0), "empty diagonal wall")

    q5_serialized = {}
    for p in range(1, 5):
        r = 5 - p
        q5_serialized[f"{p}{r}"] = serialized_table(tables[(p, r)])
    q5_serialized["50"] = serialized_table(diagonal)

    result = {
        "status": "Q5_TWO_LEVEL_MISSING_WALLS_DERIVED",
        "computer_algebra": "SymPy 1.13.3 over QQ(a,B)",
        "arbitrary_q_lowest_coefficient_checks": formula_checks,
        "q5_equal_multiplicity_positive_candidates": len(q5_candidates),
        "q5_parity_compatible_candidates": len(parity_candidates),
        "q5_higher_multiplicity_obstructions": len(obstruction_resultants),
        "obstruction_resultants": obstruction_resultants,
        "special_internal_pair_collisions": sum(map(len, expected_internal.values())),
        "special_cross_resonance_checks": cross_checks,
        "structural_wall_rows": {key: len(rows) for key, rows in q5_serialized.items()},
        "hinge_table_sha256": {
            key: sha256(dumps(rows, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            for key, rows in q5_serialized.items()
        },
        "missing_wall_orbits": orbits,
        "new_missing_wall_orbits": len(orbits),
        "scope": "All positive candidate walls with five active weights taking at most two distinct values, plus an arbitrary-q lowest-coefficient obstruction.",
    }
    require(len(orbits) == 6, "wrong orbit count")
    print(dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
