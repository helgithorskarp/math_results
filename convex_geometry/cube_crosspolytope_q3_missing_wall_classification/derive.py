#!/usr/bin/env python3
"""Exact symbolic derivation for the q=3 missing-wall classification."""

from __future__ import annotations

from hashlib import sha256
from itertools import product
from json import dumps

import sympy as sp


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def wall(weights, supplier, tail, boundary):
    weight = weights[supplier]
    return (
        boundary * (1 / weight - 1)
        + 2 * sum((weights[index] for index in tail), sp.Integer(0)) / weight
    )


def jump(weights, supplier, tail):
    weight = weights[supplier]
    denominator = sp.prod(weights)
    for index, entry in enumerate(weights):
        if index != supplier and index not in tail:
            denominator *= weight - entry
    for index in tail:
        denominator *= weight + weights[index]
    return sp.factor((-1) ** len(tail) * weight**4 / denominator)


def strip_degenerate(expression, variables, factors):
    polynomial = sp.Poly(expression, *variables, domain=sp.QQ)
    if polynomial.is_zero:
        return sp.Integer(0)
    for factor in factors:
        divisor = sp.Poly(factor, *variables, domain=sp.QQ)
        while True:
            quotient, remainder = sp.div(polynomial, divisor)
            if not remainder.is_zero:
                break
            polynomial = quotient
    return sp.factor(polynomial.as_expr())


def multiply_intervals(first, second):
    products = (
        first[0] * second[0], first[0] * second[1],
        first[1] * second[0], first[1] * second[1],
    )
    return min(products), max(products)


def polynomial_interval(expression, variable, interval):
    polynomial = sp.Poly(expression, variable, domain=sp.QQ)
    answer = (sp.Rational(0), sp.Rational(0))
    for coefficient in polynomial.all_coeffs():
        answer = multiply_intervals(answer, interval)
        answer = (answer[0] + coefficient, answer[1] + coefficient)
    return answer


def rational_sign_at_root(expression, variable, root):
    numerator, denominator = sp.together(expression).as_numer_denom()
    direct_value = sp.factor(expression.subs(variable, root))
    if direct_value.is_positive is True:
        return 1
    if direct_value.is_negative is True:
        return -1
    if direct_value.is_zero is True:
        return 0
    for digits in (12, 20, 30, 40, 60, 80):
        approximation = sp.Rational(str(sp.N(root, digits)))
        error = sp.Rational(1, 10 ** (digits - 4))
        interval = (approximation - error, approximation + error)
        require(root > interval[0] and root < interval[1],
                "failed to enclose an exact algebraic root")
        numerator_interval = polynomial_interval(numerator, variable, interval)
        denominator_interval = polynomial_interval(denominator, variable, interval)
        numerator_sign = 1 if numerator_interval[0] > 0 else (-1 if numerator_interval[1] < 0 else 0)
        denominator_sign = 1 if denominator_interval[0] > 0 else (-1 if denominator_interval[1] < 0 else 0)
        if numerator_sign and denominator_sign:
            return numerator_sign * denominator_sign
    raise RuntimeError(f"could not determine algebraic sign of {expression}")


def main() -> None:
    require(sp.__version__ == "1.13.3", "this certificate pins SymPy 1.13.3")

    # Two suppliers x>y and a third weight z.  Divide all three weights and B
    # by x, writing r=y/x, u=z/x and beta=B/x.
    r, u = sp.symbols("r u")
    pair_weights = (sp.Integer(1), r, u)

    def pair_jump(supplier, tail):
        return jump(pair_weights, supplier, tail)

    pair_rows = []
    for bits in product((0, 1), repeat=4):
        e, f, g, h = bits
        first_tail = tuple(index for bit, index in ((e, 1), (f, 2)) if bit)
        second_tail = tuple(index for bit, index in ((g, 0), (h, 2)) if bit)
        cancellation = sp.factor(
            sp.together(pair_jump(0, first_tail) + pair_jump(1, second_tail))
            .as_numer_denom()[0]
        )
        beta = sp.factor(
            2 * ((g + h * u) - r * (e * r + f * u)) / (r - 1)
        )
        pair_rows.append({
            "bits": "".join(map(str, bits)),
            "cancellation_numerator": str(cancellation),
            "beta": str(beta),
        })

    pair_table_bytes = dumps(pair_rows, sort_keys=True, separators=(",", ":")).encode()

    denominator = r**5 + r**4 - r + 1
    normal_forms = {
        "0100": (
            r * (r**2 - r + 1) / ((1 - r) * (r**2 + 1)),
            2 * r**2 * (r**2 - r + 1) / ((1 - r) ** 2 * (r**2 + 1)),
        ),
        "1000": (
            r * (r**4 + r**3 - r + 1) / denominator,
            2 * r**2 / (1 - r),
        ),
        "1001": (
            r * (r**2 + 1) * (r**2 + r - 1) / denominator,
            2 * r * (r + 1) * (1 - r**3 - r**4) / denominator,
        ),
        "1100": (
            r * (r**2 + 1) * (1 - r - r**2) / denominator,
            2 * r**2 * (1 - r) * (r**3 + 2 * r**2 + 2 * r + 2) / denominator,
        ),
    }
    for bits, (u_formula, beta_formula) in normal_forms.items():
        e, f, g, h = map(int, bits)
        first_tail = tuple(index for bit, index in ((e, 1), (f, 2)) if bit)
        second_tail = tuple(index for bit, index in ((g, 0), (h, 2)) if bit)
        cancellation = sp.factor(
            pair_jump(0, first_tail) + pair_jump(1, second_tail)
        )
        collision = sp.factor(
            wall(pair_weights, 0, first_tail, beta_formula)
            - wall(pair_weights, 1, second_tail, beta_formula)
        )
        require(sp.factor(cancellation.subs(u, u_formula)) == 0,
                f"pair cancellation failed for {bits}")
        require(sp.factor(collision.subs(u, u_formula)) == 0,
                f"pair collision failed for {bits}")

    pair_exception_polynomials = {
        "0100:third_tail_y": (
            r**7 - 2 * r**6 + 4 * r**5 - 6 * r**4
            + 7 * r**3 - 5 * r**2 + 3 * r - 1
        ),
        "0100:weight_equality_u_1": 2 * r**3 - 2 * r**2 + 2 * r - 1,
        "0100:third_tail_xy": r**3 + r - 1,
        "1001:third_tail_empty": (
            r**10 + 2 * r**9 + r**8 - 3 * r**6 - r**5
            + 3 * r**4 + r**3 + 3 * r**2 - 2 * r - 1
        ),
    }
    pair_exception_intervals = {
        "0100:third_tail_y": (sp.Rational(614437, 10**6), sp.Rational(614438, 10**6)),
        "0100:weight_equality_u_1": (sp.Rational(647798, 10**6), sp.Rational(647799, 10**6)),
        "0100:third_tail_xy": (sp.Rational(682327, 10**6), sp.Rational(682328, 10**6)),
        "1001:third_tail_empty": (sp.Rational(736190, 10**6), sp.Rational(736191, 10**6)),
    }
    pair_exceptions = []
    for name, polynomial in pair_exception_polynomials.items():
        poly = sp.Poly(polynomial, r, domain=sp.QQ)
        low, high = pair_exception_intervals[name]
        require(poly.count_roots(0, 1) == 1, f"{name} is not unique in (0,1)")
        require(poly.count_roots(low, high) == 1, f"{name} isolation failed")
        root = next(root for root in poly.real_roots() if 0 < root < 1)
        pair_exceptions.append({
            "event": name,
            "polynomial": str(polynomial),
            "isolating_interval": [str(low), str(high)],
            "approximation": str(sp.N(root, 16)),
        })

    # Triple collisions.  Normalize and order the distinct weights as 1>a>b>0.
    a, b = sp.symbols("a b")
    weights = (sp.Integer(1), a, b)
    tails = {
        0: ((), (1,), (2,), (1, 2)),
        1: ((), (0,), (2,), (0, 2)),
        2: ((), (0,), (1,), (0, 1)),
    }
    triple_rows = []
    candidates = []
    degeneracies = (a, b, a - 1, b - 1, a - b)
    variables = (b, a)
    for indices in product(range(4), repeat=3):
        chosen = tuple(tails[index][indices[index]] for index in range(3))
        target = wall(weights, 0, chosen[0], sp.Integer(0))
        boundary_01 = sp.factor(
            (target - wall(weights, 1, chosen[1], sp.Integer(0))) / (1 / a - 1)
        )
        boundary_02 = sp.factor(
            (target - wall(weights, 2, chosen[2], sp.Integer(0))) / (1 / b - 1)
        )
        collision = strip_degenerate(
            sp.together(boundary_01 - boundary_02).as_numer_denom()[0],
            variables,
            degeneracies,
        )
        cancellation = strip_degenerate(
            sp.together(sum(jump(weights, index, chosen[index]) for index in range(3)))
            .as_numer_denom()[0],
            variables,
            degeneracies,
        )
        row = {
            "pattern": "".join(map(str, indices)),
            "collision": str(collision),
            "cancellation": str(cancellation),
        }
        if collision == 0 or cancellation == 0:
            row["eliminant"] = "degenerate"
            triple_rows.append(row)
            continue
        if not collision.free_symbols or not cancellation.free_symbols:
            row["eliminant"] = "constant"
            triple_rows.append(row)
            continue
        chain = sp.subresultants(collision, cancellation, b)
        constants = [entry for entry in chain if sp.degree(entry, b) == 0]
        linears = [entry for entry in chain if sp.degree(entry, b) == 1]
        if not constants or not linears:
            # In the only such nonconstant cases collision is +/-2(a+1),
            # hence nonzero throughout 0<a<1.
            require(sp.Poly(collision, a).count_roots(0, 1) == 0,
                    f"unresolved triangular case {indices}")
            row["eliminant"] = str(collision)
            triple_rows.append(row)
            continue
        eliminant = strip_degenerate(constants[-1], variables, degeneracies)
        linear = linears[-1]
        linear_poly = sp.Poly(linear, b)
        linear_constant = linear_poly.coeff_monomial(1)
        linear_coefficient = linear_poly.coeff_monomial(b)
        exceptional_specialization = sp.gcd(
            sp.Poly(eliminant, a),
            sp.gcd(sp.Poly(linear_constant, a), sp.Poly(linear_coefficient, a)),
        )
        exceptional_expression = strip_degenerate(
            exceptional_specialization.as_expr(), variables, degeneracies
        )
        if exceptional_expression.free_symbols:
            require(sp.Poly(exceptional_expression, a).count_roots(0, 1) == 0,
                    f"unresolved vanishing linear subresultant for {indices}")
        b_formula = sp.factor(-linear_constant / linear_coefficient)
        collision_sub = sp.factor(
            sp.together(collision.subs(b, b_formula)).as_numer_denom()[0]
        )
        cancellation_sub = sp.factor(
            sp.together(cancellation.subs(b, b_formula)).as_numer_denom()[0]
        )
        common = sp.gcd(
            sp.Poly(eliminant, a),
            sp.gcd(sp.Poly(collision_sub, a), sp.Poly(cancellation_sub, a)),
        )
        common_expression = strip_degenerate(common.as_expr(), variables, degeneracies)
        row["eliminant"] = str(common_expression)
        triple_rows.append(row)
        if not common_expression.free_symbols:
            continue
        for root in sp.Poly(common_expression, a).real_roots():
            if not (root > 0 and root < 1):
                continue
            b_value = sp.factor(b_formula.subs(a, root))
            positive_b = rational_sign_at_root(b_formula, a, root) > 0
            ordered = rational_sign_at_root(a - b_formula, a, root) > 0
            if not (positive_b and ordered):
                continue
            boundary_formula = sp.factor(boundary_01.subs(b, b_formula))
            boundary_value = sp.factor(boundary_formula.subs(a, root))
            boundary_positive = rational_sign_at_root(boundary_formula, a, root) > 0
            minimal_polynomial = sp.Poly(sp.minpoly(root, a), a, domain=sp.QQ)
            root_factor = next(
                factor
                for factor, _multiplicity in sp.factor_list(common_expression)[1]
                if sp.gcd(sp.Poly(factor, a, domain=sp.QQ), minimal_polynomial).degree() > 0
            )
            primitive = sp.Poly(root_factor, a, domain=sp.QQ).primitive()[1]
            if primitive.LC() < 0:
                primitive = -primitive
            require(sp.rem(sp.Poly(collision_sub, a), primitive).is_zero,
                    f"collision factor mismatch for {indices}")
            require(sp.rem(sp.Poly(cancellation_sub, a), primitive).is_zero,
                    f"cancellation factor mismatch for {indices}")
            candidates.append({
                "pattern": "".join(map(str, indices)),
                "eliminant": str(primitive.as_expr()),
                "b_formula": str(b_formula),
                "a_approximation": str(sp.N(root, 16)),
                "b_approximation": str(sp.N(b_value, 16)),
                "B_approximation": str(sp.N(boundary_value, 16)),
                "B_sign": "positive" if boundary_positive else "negative",
            })

    triple_table_bytes = dumps(triple_rows, sort_keys=True, separators=(",", ":")).encode()
    expected_patterns = [("120", "positive"), ("310", "positive"), ("312", "negative")]
    require([(entry["pattern"], entry["B_sign"]) for entry in candidates] == expected_patterns,
            "unexpected sorted triple orbit census")

    triple_intervals = {
        "120": (sp.Rational(715885, 10**6), sp.Rational(715887, 10**6)),
        "310": (sp.Rational(867093, 10**6), sp.Rational(867094, 10**6)),
        "312": (sp.Rational(792818, 10**6), sp.Rational(792820, 10**6)),
    }
    for entry in candidates:
        polynomial = sp.Poly(sp.sympify(entry["eliminant"]), a, domain=sp.QQ)
        low, high = triple_intervals[entry["pattern"]]
        require(polynomial.count_roots(0, 1) == 1,
                f"nonunique unit root for {entry['pattern']}")
        require(polynomial.count_roots(low, high) == 1,
                f"failed root isolation for {entry['pattern']}")
        entry["a_isolating_interval"] = [str(low), str(high)]

    result = {
        "status": "Q3_MISSING_WALL_CLASSIFICATION_DERIVED",
        "computer_algebra": "SymPy 1.13.3 over QQ with lexicographic subresultants",
        "pair_label_patterns_checked": len(pair_rows),
        "pair_factor_table_sha256": sha256(pair_table_bytes).hexdigest(),
        "two_label_normal_forms": [
            {"bits": bits, "u": str(sp.factor(values[0])), "beta": str(sp.factor(values[1]))}
            for bits, values in normal_forms.items()
        ],
        "pair_third_supplier_exceptions": pair_exceptions,
        "triple_tail_patterns_checked": len(triple_rows),
        "triple_elimination_table_sha256": sha256(triple_table_bytes).hexdigest(),
        "sorted_triple_common_zero_orbits": candidates,
        "positive_boundary_triple_orbits": 2,
        "scope": (
            "Together with PROOF.md, the exact elimination classifies every "
            "missing positive candidate wall for three distinct active weights."
        ),
    }
    print(dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
