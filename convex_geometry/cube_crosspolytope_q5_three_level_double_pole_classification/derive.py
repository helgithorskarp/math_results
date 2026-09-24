#!/usr/bin/env python3
"""Exact symbolic classification of isolated double-pole walls for (1,1,a,a,b)."""

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


def rational_sign_at_root(expression, defining, left, right) -> int:
    numerator, denominator = sp.together(expression).as_numer_denom()
    midpoint = (left + right) / 2
    for value, name in ((numerator, "numerator"), (denominator, "denominator")):
        polynomial = sp.Poly(value, defining.gens[0], domain=sp.QQ)
        require(
            sp.count_roots(polynomial, left, right) == 0,
            f"{name} has a zero in a defining root interval",
        )
        require(polynomial.eval(midpoint) != 0, f"{name} vanishes at midpoint")
    return int(sp.sign(numerator.subs(defining.gens[0], midpoint))) * int(
        sp.sign(denominator.subs(defining.gens[0], midpoint))
    )


def bisect(polynomial, left, right, steps=90):
    left_sign = sp.sign(polynomial.eval(left))
    require(left_sign * sp.sign(polynomial.eval(right)) < 0, "root is not bracketed")
    for _ in range(steps):
        midpoint = (left + right) / 2
        midpoint_sign = sp.sign(polynomial.eval(midpoint))
        if midpoint_sign == 0:
            return midpoint
        if midpoint_sign == left_sign:
            left = midpoint
        else:
            right = midpoint
    return (left + right) / 2


def remove_endpoint_roots(polynomial):
    """Remove all factors a and a-1 before an open-unit-interval count."""
    variable = polynomial.gens[0]
    answer = polynomial
    for factor in (sp.Poly(variable, variable), sp.Poly(variable - 1, variable)):
        while answer.degree() > 0:
            quotient, remainder = sp.div(answer, factor)
            if not remainder.is_zero:
                break
            answer = quotient
    return answer


def main() -> None:
    require(sp.__version__ == "1.13.3", "this derivation pins SymPy 1.13.3")
    a, b, boundary, variable = sp.symbols("a b B t")

    p1 = sp.Poly(
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
    p4 = sp.Poly(
        4 * a**15
        + 8 * a**14
        + 4 * a**13
        + 6 * a**9
        - 2 * a**8
        - 2 * a**7
        + 6 * a**6
        - a**2
        + 2 * a
        - 1,
        a,
        domain=sp.QQ,
    )
    p5 = sp.Poly(
        a**12
        + a**11
        + a**10
        + a**9
        + a**8
        + a**7
        - 2 * a**6
        + a**5
        + a**4
        + a**3
        + a**2
        + a
        + 1,
        a,
        domain=sp.QQ,
    )

    d1 = a**6 - a**5 + a**4 - a**3 + a**2 - a + 1
    n1 = -a * (a - 1) * (a**2 - a + 1) * (a**2 + a + 1)
    d2 = a**8 + a**7 + 2 * a - 2
    n2 = a * (a**7 + a**6 + 2 * a - 2)
    d3 = a**9 + 2 * a**8 + a**7 + a**2 - 2 * a + 1
    n3 = a * (a**2 + 1) * (a**2 + a - 1) * (a**4 + a**3 - a + 1)
    d4 = 2 * a**8 + 2 * a**7 - a + 1
    n4 = a * (2 * a**7 + 2 * a**6 + a - 1)
    phi1, phi2, phi3, phi4 = n1 / d1, n2 / d2, -n3 / d3, n4 / d4

    table = hinge_table((sp.Integer(1), sp.Integer(1), a, a, b), boundary, variable)
    require(len(table) == 33, "unexpected structural-row count")

    shortlist = {
        (0, 1, 0, 0),
        (1, 0, 0, 0),
        (1, 1, 0, 1),
        (2, 0, 0, 1),
        (2, 0, 1, 1),
        (2, 1, 0, 0),
        (2, 1, 1, 0),
        (2, 1, 2, 0),
    }
    expected_branches = {
        (0, 1, 0, 0): [phi1],
        (1, 0, 0, 0): [phi2],
        (1, 1, 0, 1): [-phi2],
        (2, 0, 0, 1): [2 * a, n3 / d3],
        (2, 0, 1, 1): [phi4, 2 * a - 1],
        (2, 1, 0, 0): [-2 * a, phi3],
        (2, 1, 1, 0): [-phi4, 1 - 2 * a],
        (2, 1, 2, 0): [phi1, 2 - 2 * a],
    }
    expected_polynomial = {
        (0, 1, 0, 0): p1,
        (1, 0, 0, 0): p2,
        (1, 1, 0, 1): p2,
        (2, 0, 0, 1): p3,
        (2, 0, 1, 1): p4,
        (2, 1, 0, 0): p3,
        (2, 1, 1, 0): p4,
        (2, 1, 2, 0): p5,
    }
    nondegenerate_branch = {
        (0, 1, 0, 0): phi1,
        (1, 0, 0, 0): phi2,
        (1, 1, 0, 1): -phi2,
        (2, 0, 0, 1): n3 / d3,
        (2, 0, 1, 1): phi4,
        (2, 1, 0, 0): phi3,
        (2, 1, 1, 0): -phi4,
        (2, 1, 2, 0): phi1,
    }

    examined = 0
    computed_shortlist = set()
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
                    leading_numerator = sp.factor(
                        sp.together(leading).as_numer_denom()[0]
                    )
                    parity_allows = (ell + h + g) % 2 == 1
                    pattern = (ell, h, i, g)
                    if parity_allows and pattern in shortlist:
                        computed_shortlist.add(pattern)
                        branches = sp.solve(leading_numerator, b)
                        expected = expected_branches[pattern]
                        require(len(branches) == len(expected), f"branch count at {pattern}")
                        require(
                            all(
                                any(sp.factor(x - y) == 0 for y in branches)
                                for x in expected
                            ),
                            f"leading branches at {pattern}",
                        )
                        ratio_difference = sp.factor(
                            (unit[4] / unit[3] - moving[4] / moving[3]).subs(
                                boundary, resonant_boundary
                            )
                        )
                        reduced = sp.factor(
                            sp.together(
                                ratio_difference.subs(
                                    b, nondegenerate_branch[pattern]
                                )
                            )
                        )
                        reduced_numerator = sp.Poly(
                            reduced.as_numer_denom()[0], a, domain=sp.QQ
                        )
                        quotient, remainder = sp.div(
                            reduced_numerator, expected_polynomial[pattern]
                        )
                        require(remainder.is_zero, f"ratio polynomial at {pattern}")
                        require(
                            sp.count_roots(remove_endpoint_roots(quotient), 0, 1)
                            == 0,
                            f"unaccounted ratio root at {pattern}",
                        )
                    elif parity_allows:
                        # Section 2 of PROOF.md gives the elementary B<=0 exclusion.
                        pass
    require(examined == 36, "did not inspect every pair")
    require(computed_shortlist == shortlist, "shortlist mismatch")

    intervals = {
        "I": (p1, sp.Rational(127, 200), sp.Rational(637, 1000), phi1, (0, 1, 0, 0)),
        "II": (p2, sp.Rational(27, 40), sp.Rational(677, 1000), phi2, (1, 0, 0, 0)),
        "III": (p3, sp.Rational(64, 125), sp.Rational(513, 1000), phi3, (2, 1, 0, 0)),
    }
    root_counts = {
        "P1": int(sp.count_roots(p1, 0, 1)),
        "P2": int(sp.count_roots(p2, 0, 1)),
        "P3": int(sp.count_roots(p3, 0, 1)),
        "P4": int(sp.count_roots(p4, 0, 1)),
        "P5": int(sp.count_roots(p5, 0, 1)),
    }
    require(root_counts == {"P1": 1, "P2": 2, "P3": 1, "P4": 1, "P5": 0}, "root census")
    require(
        sp.count_roots(p2, sp.Rational(9, 10), sp.Rational(901, 1000)) == 1,
        "second P2 root interval",
    )
    require(
        sp.count_roots(p4, sp.Rational(71, 125), sp.Rational(569, 1000)) == 1,
        "P4 root interval",
    )

    # Exact sign certificates at every possible nondegenerate root.
    for name, polynomial, left, right, beta, pattern in (
        ("I", p1, sp.Rational(127, 200), sp.Rational(637, 1000), phi1, (0, 1, 0, 0)),
        ("II", p2, sp.Rational(27, 40), sp.Rational(677, 1000), phi2, (1, 0, 0, 0)),
        ("II-bad", p2, sp.Rational(9, 10), sp.Rational(901, 1000), phi2, (1, 0, 0, 0)),
        ("III", p3, sp.Rational(64, 125), sp.Rational(513, 1000), phi3, (2, 1, 0, 0)),
        ("P4", p4, sp.Rational(71, 125), sp.Rational(569, 1000), phi4, (2, 0, 1, 1)),
    ):
        require(sp.count_roots(polynomial, left, right) == 1, f"isolation {name}")
        ell, h, i, g = pattern
        resonant_boundary = sp.factor(
            2 * (a * (ell * a + h * beta) - (i + g * beta)) / (1 - a)
        )
        signs = (
            rational_sign_at_root(beta, polynomial, left, right),
            rational_sign_at_root(a - beta, polynomial, left, right),
            rational_sign_at_root(resonant_boundary, polynomial, left, right),
        )
        expected_signs = {
            "I": (1, 1, 1),
            "II": (1, 1, 1),
            "II-bad": (1, -1, 1),
            "III": (1, 1, 1),
            "P4": (-1, 1, 1),
        }
        require(signs == expected_signs[name], f"admissibility signs {name}: {signs}")

    # The sign-reflected branches are disposed of without numerical inference.
    require(
        rational_sign_at_root(-phi2, p2, sp.Rational(27, 40), sp.Rational(677, 1000)) < 0
        and rational_sign_at_root(-phi2, p2, sp.Rational(9, 10), sp.Rational(901, 1000)) < 0,
        "reflected P2 branches",
    )
    require(
        rational_sign_at_root(n3 / d3, p3, sp.Rational(64, 125), sp.Rational(513, 1000)) < 0,
        "reflected P3 branch",
    )
    reflected_p4_boundary = sp.factor(
        2 * (2 * a**2 + a * (-phi4) - 1) / (1 - a)
    )
    require(
        rational_sign_at_root(-phi4, p4, sp.Rational(71, 125), sp.Rational(569, 1000)) > 0
        and rational_sign_at_root(
            reflected_p4_boundary,
            p4,
            sp.Rational(71, 125),
            sp.Rational(569, 1000),
        )
        < 0,
        "reflected P4 branch",
    )

    physical = []
    for name, (polynomial, left, right, beta, pattern) in intervals.items():
        alpha_approx = bisect(polynomial, left, right)
        beta_approx = sp.factor(beta).subs(a, alpha_approx)
        ell, h, i, g = pattern
        boundary_expression = sp.factor(
            2 * (a * (ell * a + h * beta) - (i + g * beta)) / (1 - a)
        )
        boundary_approx = boundary_expression.subs(a, alpha_approx)

        unit = find_row(table, 2 * (ell * a + h * b))
        moving = find_row(
            table, (1 - a) * boundary / a + 2 * (i + g * b) / a
        )
        substitution = {boundary: boundary_expression, b: beta}
        require(
            sp.factor((unit[3] + moving[3]).subs(substitution, simultaneous=True))
            == 0,
            f"degree-three cancellation in family {name}",
        )
        next_sum = sp.factor(
            (unit[4] + moving[4]).subs(substitution, simultaneous=True)
        )
        next_numerator = sp.Poly(
            sp.together(next_sum).as_numer_denom()[0], a, domain=sp.QQ
        )
        require(
            sp.rem(next_numerator, polynomial).is_zero,
            f"degree-four cancellation in family {name}",
        )

        target = sp.factor(2 * (ell * a + h * beta))
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
                sp.gcd(polynomial, sp.Poly(numerator, a, domain=sp.QQ)).degree()
                == 0,
                f"unresolved extra collision in family {name} at {wall}",
            )
            coprime += 1
        require(len(identical) == 2 and coprime == 31, f"wall isolation {name}")
        physical.append(
            {
                "family": name,
                "pattern": list(pattern),
                "root_interval": [str(left), str(right)],
                "alpha_approx": f"{float(alpha_approx):.15f}",
                "beta_approx": f"{float(beta_approx):.15f}",
                "B_approx": f"{float(boundary_approx):.15f}",
                "rows_at_wall": len(identical),
                "other_rows_coprime": coprime,
            }
        )

    payload = {
        "status": "Q5_THREE_LEVEL_DOUBLE_POLE_CLASSIFICATION_DERIVED",
        "sympy_version": sp.__version__,
        "pair_patterns_examined": examined,
        "sign_and_boundary_feasible_patterns": len(shortlist),
        "nondegenerate_eliminants": 5,
        "root_counts_in_unit_interval": root_counts,
        "physical_families": physical,
        "physical_family_count": len(physical),
        "structural_rows": len(table),
    }
    canonical = dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["certificate_sha256"] = sha256(canonical.encode()).hexdigest()
    print(dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
