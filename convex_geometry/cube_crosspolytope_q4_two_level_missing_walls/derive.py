#!/usr/bin/env python3
"""Exact symbolic derivation of the q=4 two-level missing-wall theorem."""

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
        require(
            set(actual_vector) == set(expected_vector),
            f"{name}: wrong hinge degrees at {wall}",
        )
        for degree, expected_value in expected_vector.items():
            require(
                sp.factor(actual_vector[degree] - expected_value) == 0,
                f"{name}: wrong coefficient at {wall}, degree {degree}",
            )


def find_row(table, wall):
    matches = [candidate for candidate in table if sp.factor(candidate - wall) == 0]
    require(len(matches) == 1, f"could not identify structural row {wall}")
    return table[matches[0]]


def serialized_table(table):
    rows = []
    for wall in sorted(table, key=sp.sstr):
        rows.append(
            {
                "wall": sp.sstr(wall),
                "hinges": {
                    str(degree): sp.sstr(sp.factor(value))
                    for degree, value in sorted(table[wall].items())
                },
            }
        )
    return rows


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

    tables = {
        (3, 1): hinge_table((sp.Integer(1),) * 3 + (a,), boundary, variable),
        (2, 2): hinge_table((sp.Integer(1),) * 2 + (a,) * 2, boundary, variable),
        (1, 3): hinge_table((sp.Integer(1),) + (a,) * 3, boundary, variable),
        (4, 0): hinge_table((sp.Integer(1),) * 4, boundary, variable),
    }

    expected_31 = {
        sp.Integer(0): {
            1: -boundary**2 / (2 * a * (a - 1)),
            2: -boundary * (5 * a - 4) / (2 * a * (a - 1) ** 2),
            3: -(15 * a**2 - 24 * a + 10) / (6 * a * (a - 1) ** 3),
        },
        2 * a: {
            1: -(boundary + 2 * a) ** 2 / (2 * a * (a + 1)),
            2: -(boundary + 2 * a) * (5 * a + 4) / (2 * a * (a + 1) ** 2),
            3: -(15 * a**2 + 24 * a + 10) / (6 * a * (a + 1) ** 3),
        },
        sp.Integer(2): {
            2: 3 * (boundary + 2) / (4 * a * (a - 1)),
            3: (11 * a - 9) / (8 * a * (a - 1) ** 2),
        },
        2 * (a + 1): {
            2: 3 * (boundary + 2 * a + 2) / (4 * a * (a + 1)),
            3: (11 * a + 9) / (8 * a * (a + 1) ** 2),
        },
        sp.Integer(4): {3: -1 / (8 * a * (a - 1))},
        2 * (a + 2): {3: -1 / (8 * a * (a + 1))},
        sp.factor(lam * boundary): {3: a**5 / (6 * (a - 1) ** 3)},
        sp.factor(lam * boundary + 2 / a): {
            3: -a**5 / (2 * (a - 1) ** 2 * (a + 1))
        },
        sp.factor(lam * boundary + 4 / a): {
            3: a**5 / (2 * (a - 1) * (a + 1) ** 2)
        },
        sp.factor(lam * boundary + 6 / a): {3: -a**5 / (6 * (a + 1) ** 3)},
    }
    expected_22 = {
        sp.Integer(0): {
            2: boundary / (2 * a**2 * (a - 1) ** 2),
            3: (3 * a - 2) / (3 * a**2 * (a - 1) ** 3),
        },
        2 * a: {
            2: (boundary + 2 * a) / (a**2 * (a - 1) * (a + 1)),
            3: 2 * (3 * a**2 - 2) / (3 * a**2 * (a - 1) ** 2 * (a + 1) ** 2),
        },
        4 * a: {
            2: (boundary + 4 * a) / (2 * a**2 * (a + 1) ** 2),
            3: (3 * a + 2) / (3 * a**2 * (a + 1) ** 3),
        },
        sp.Integer(2): {3: -1 / (6 * a**2 * (a - 1) ** 2)},
        2 * (a + 1): {3: -1 / (3 * a**2 * (a - 1) * (a + 1))},
        2 * (2 * a + 1): {3: -1 / (6 * a**2 * (a + 1) ** 2)},
        sp.factor(lam * boundary): {
            2: boundary * a**2 / (2 * (a - 1) ** 2),
            3: a**3 * (2 * a - 3) / (3 * (a - 1) ** 3),
        },
        sp.factor(lam * boundary + 2): {3: -a**3 / (6 * (a - 1) ** 2)},
        sp.factor(lam * boundary + 2 / a): {
            2: -a**2 * (boundary + 2) / ((a - 1) * (a + 1)),
            3: -2 * a**3 * (2 * a**2 - 3) / (3 * (a - 1) ** 2 * (a + 1) ** 2),
        },
        sp.factor(lam * boundary + 2 + 2 / a): {
            3: a**3 / (3 * (a - 1) * (a + 1))
        },
        sp.factor(lam * boundary + 4 / a): {
            2: a**2 * (boundary + 4) / (2 * (a + 1) ** 2),
            3: a**3 * (2 * a + 3) / (3 * (a + 1) ** 3),
        },
        sp.factor(lam * boundary + 2 + 4 / a): {3: -a**3 / (6 * (a + 1) ** 2)},
    }
    expected_13 = {
        sp.Integer(0): {3: -1 / (6 * a**3 * (a - 1) ** 3)},
        2 * a: {3: -1 / (2 * a**3 * (a - 1) ** 2 * (a + 1))},
        4 * a: {3: -1 / (2 * a**3 * (a - 1) * (a + 1) ** 2)},
        6 * a: {3: -1 / (6 * a**3 * (a + 1) ** 3)},
        sp.factor(lam * boundary): {
            1: boundary**2 / (2 * a * (a - 1)),
            2: boundary * (4 * a - 5) / (2 * (a - 1) ** 2),
            3: a * (10 * a**2 - 24 * a + 15) / (6 * (a - 1) ** 3),
        },
        sp.factor(lam * boundary + 2): {
            2: -3 * (boundary + 2 * a) / (4 * (a - 1)),
            3: -a * (9 * a - 11) / (8 * (a - 1) ** 2),
        },
        sp.factor(lam * boundary + 4): {3: a / (8 * (a - 1))},
        sp.factor(lam * boundary + 2 / a): {
            1: -(boundary + 2) ** 2 / (2 * a * (a + 1)),
            2: -(boundary + 2) * (4 * a + 5) / (2 * (a + 1) ** 2),
            3: -a * (10 * a**2 + 24 * a + 15) / (6 * (a + 1) ** 3),
        },
        sp.factor(lam * boundary + 2 + 2 / a): {
            2: 3 * (boundary + 2 * a + 2) / (4 * (a + 1)),
            3: a * (9 * a + 11) / (8 * (a + 1) ** 2),
        },
        sp.factor(lam * boundary + 4 + 2 / a): {3: -a / (8 * (a + 1))},
    }
    expected_40 = {
        sp.Integer(0): {
            0: boundary**3 / 6,
            1: 2 * boundary**2,
            2: 5 * boundary,
            3: sp.Rational(10, 3),
        },
        sp.Integer(2): {
            1: -(boundary + 2) ** 2,
            2: -9 * (boundary + 2) / 2,
            3: sp.Rational(-49, 12),
        },
        sp.Integer(4): {
            2: 3 * (boundary + 4) / 4,
            3: sp.Rational(5, 4),
        },
        sp.Integer(6): {3: sp.Rational(-1, 12)},
    }
    expected_tables = {(3, 1): expected_31, (2, 2): expected_22, (1, 3): expected_13, (4, 0): expected_40}
    for key, expected in expected_tables.items():
        check_table(tables[key], expected, str(key))

    candidates = []
    for p, r in ((3, 1), (2, 2), (1, 3)):
        table = tables[(p, r)]
        for k in range(p):
            for ell in range(r + 1):
                for i in range(p + 1):
                    for j in range(r):
                        # Equal lowest hinge degree and existence of B>0 for some 0<a<1.
                        if r + k != p + j or ell + k - j - i <= 0:
                            continue
                        constant_wall = sp.factor(2 * (k + a * ell))
                        moving_wall = sp.factor(lam * boundary + 2 * i / a + 2 * j)
                        resonance_boundary = sp.factor(
                            a * (constant_wall - 2 * i / a - 2 * j) / (1 - a)
                        )
                        degree = r + k
                        aggregate = sp.factor(
                            (
                                find_row(table, constant_wall).get(degree, 0)
                                + find_row(table, moving_wall).get(degree, 0)
                            ).subs(boundary, resonance_boundary)
                        )
                        candidates.append(
                            {
                                "stratum": f"1^{p}a^{r}",
                                "indices": [k, ell, i, j],
                                "wall": sp.sstr(constant_wall),
                                "B": sp.sstr(resonance_boundary),
                                "lowest_degree": degree,
                                "aggregate": sp.sstr(aggregate),
                            }
                        )

    expected_indices = {
        (3, 1): {(2, 0, 0, 0), (2, 0, 1, 0), (2, 1, 0, 0), (2, 1, 1, 0), (2, 1, 2, 0)},
        (2, 2): {(0, 1, 0, 0), (0, 2, 0, 0), (0, 2, 1, 0), (1, 1, 0, 1), (1, 2, 0, 1), (1, 2, 1, 1)},
        (1, 3): {(0, 3, 0, 2)},
    }
    for p, r in expected_indices:
        observed = {
            tuple(entry["indices"])
            for entry in candidates
            if entry["stratum"] == f"1^{p}a^{r}"
        }
        require(observed == expected_indices[(p, r)], f"wrong candidate set for {(p, r)}")

    p1 = 4 * a**6 - 3 * a**2 + 6 * a - 3
    p2 = a**6 + a**5 + 2 * a - 2
    p3 = 2 * a**2 - 1
    polynomials = [sp.Poly(poly, a, domain=sp.QQ) for poly in (p1, p2, p3)]
    intervals = [
        (sp.Rational(663190523, 10**9), sp.Rational(165797631, 250000000)),
        (sp.Rational(766427599, 10**9), sp.Rational(1916069, 2500000)),
        (sp.Rational(707106781, 10**9), sp.Rational(353553391, 500000000)),
    ]
    roots = []
    for polynomial, (low, high) in zip(polynomials, intervals):
        require(polynomial.count_roots(0, 1) == 1, f"nonunique root of {polynomial}")
        require(polynomial.count_roots(low, high) == 1, f"root isolation failed for {polynomial}")
        roots.append(next(root for root in polynomial.real_roots() if 0 < root < 1))

    no_root_polynomials = (
        2 * a**4 + a**2 + 1,
        4 * a**7 + 4 * a**6 - 3 * a**3 + 9 * a**2 - 9 * a + 3,
        4 * a**6 + a**2 - 2 * a + 1,
        4 * a**6 - a**2 + 1,
        a**7 + 2 * a**6 + a**5 + a**2 - 2 * a + 1,
        2 * a**6 + 2 * a**5 - a + 1,
        3 * a**7 + 9 * a**6 + 9 * a**5 + 3 * a**4 - 4 * a + 4,
    )
    for polynomial in no_root_polynomials:
        require(sp.Poly(polynomial, a).count_roots(0, 1) == 0, f"unexpected root of {polynomial}")

    table22 = tables[(2, 2)]
    resonance_boundary = 2 * a**2 / (1 - a)
    degree3_obstruction = sp.factor(
        (
            find_row(table22, 2 * a).get(3, 0)
            + find_row(table22, lam * boundary).get(3, 0)
        ).subs(boundary, resonance_boundary)
    )
    obstruction_numerator = sp.factor(sp.together(degree3_obstruction).as_numer_denom()[0])
    expected_obstruction = 2 * a**8 + a**7 - 4 * a**6 - 3 * a**5 + 6 * a**3 - 6 * a**2 - 4 * a + 4
    require(obstruction_numerator == expected_obstruction, "wrong degree-three obstruction")
    require(sp.gcd(sp.Poly(p2, a), sp.Poly(expected_obstruction, a)).degree() == 0, "obstruction shares exceptional root")
    require(sp.resultant(p2, expected_obstruction, a) == 896, "wrong obstruction resultant")

    collision_audit = {
        (3, 1): internal_collisions(3, 1),
        (2, 2): internal_collisions(2, 2),
        (1, 3): internal_collisions(1, 3),
    }
    require(collision_audit[(3, 1)] == [], "unexpected internal collision in 111a")
    require(collision_audit[(2, 2)] == [("constant", sp.Rational(1, 2), (0, 2), (1, 0))], "wrong 11aa collision audit")
    require(collision_audit[(1, 3)] == [("moving", sp.Rational(1, 2), (0, 2), (1, 0))], "wrong 1aaa collision audit")

    # At the only constant internal collision, adding the moving row at B=2
    # still leaves a positive quadratic coefficient at wall 2.
    specialized = hinge_table((sp.Integer(1), sp.Integer(1), sp.Rational(1, 2), sp.Rational(1, 2)), sp.Integer(2), variable)
    require(specialized[sp.Integer(2)][2] > 0, "special collision cancels unexpectedly")

    serialized = {f"{p}{r}": serialized_table(table) for (p, r), table in tables.items()}
    result = {
        "status": "Q4_TWO_LEVEL_MISSING_WALLS_DERIVED",
        "computer_algebra": "SymPy 1.13.3 over QQ(a,B)",
        "structural_wall_rows": {key: len(rows) for key, rows in serialized.items()},
        "hinge_table_sha256": {
            key: sha256(dumps(rows, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            for key, rows in serialized.items()
        },
        "residual_multiplicity_rule": "r+k=p+j",
        "positive_equal_multiplicity_cross_resonances": len(candidates),
        "cross_resonance_data": candidates,
        "special_internal_collisions": {
            f"{p}{r}": [
                {
                    "family": family,
                    "a": str(value),
                    "rows": [list(first), list(second)],
                }
                for family, value, first, second in entries
            ]
            for (p, r), entries in collision_audit.items()
        },
        "obstruction_resultant": 896,
        "missing_wall_orbits": [
            {
                "weights": "(1,1,1,a1)",
                "minimal_polynomial": sp.sstr(p1),
                "a_isolating_interval": list(map(str, intervals[0])),
                "a_approximation": str(sp.N(roots[0], 18)),
                "B_formula": "4*a1/(1-a1)",
                "B_approximation": str(sp.N(4 * roots[0] / (1 - roots[0]), 18)),
                "wall": "4",
            },
            {
                "weights": "(1,1,1,1/sqrt(2))",
                "minimal_polynomial": sp.sstr(p3),
                "a_isolating_interval": list(map(str, intervals[2])),
                "a_approximation": str(sp.N(roots[2], 18)),
                "B": "2*sqrt(2)",
                "wall": "4",
            },
            {
                "weights": "(1,1,a2,a2)",
                "minimal_polynomial": sp.sstr(p2),
                "a_isolating_interval": list(map(str, intervals[1])),
                "a_approximation": str(sp.N(roots[1], 18)),
                "B_formula": "2*a2^2/(1-a2)",
                "B_approximation": str(sp.N(2 * roots[1] ** 2 / (1 - roots[1]), 18)),
                "wall": "2*(1+a2)",
            },
        ],
        "new_missing_wall_orbits": 3,
        "scope": "All positive candidate walls with four active weights taking at most two distinct values.",
    }
    print(dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
