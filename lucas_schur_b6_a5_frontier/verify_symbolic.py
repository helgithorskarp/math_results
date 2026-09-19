#!/usr/bin/env python3
"""Exact affine-cell certificate for the canonical Lucas (5,6) ray."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from fractions import Fraction

import sympy as sp


T_START = 60
T_ALPHA_NUMERATORS = (279, 239, 259)
T_BETA_NUMERATORS = (
    2160, 905, 928, 2025, 608, 1225, 2160, 473, 1360, 1593,
    1040, 1225, 1728, 905, 928, 2025, 1040, 793, 2160, 473,
    1360, 2025, 608, 1225, 1728, 905, 1360, 1593, 1040, 793,
)
U_DELTA_NUMERATORS = (
    360, 163, 248, 243, 136, 275, 288, 163, 248, 171,
    280, 203, 288, 163, 176, 315, 208, 203, 288, 91,
    320, 243, 208, 203, 216, 235, 248, 243, 208, 131,
)
EXPECTED_CERTIFICATE_SHA256 = "304a65abfeacfc29317c2cc4cdc8a9cc99d4c28c3d5bc8a777bff027348f88f5"

j, t, x, z = sp.symbols("j t x z")


def t_common(n: sp.Expr) -> sp.Expr:
    return n**4 / sp.Integer(2160) + sp.Rational(7, 540) * n**3 + n**2 / sp.Integer(8)


def t_residue_polynomial(n: sp.Expr, residue: int) -> sp.Expr:
    return (
        t_common(n)
        + sp.Rational(T_ALPHA_NUMERATORS[residue % 3], 540) * n
        + sp.Rational(T_BETA_NUMERATORS[residue], 2160)
    )


def u_common(n: sp.Expr) -> sp.Expr:
    return n**3 / sp.Integer(180) + sp.Rational(11, 120) * n**2 + sp.Rational(9, 20) * n


def u_residue_polynomial(n: sp.Expr, residue: int) -> sp.Expr:
    return u_common(n) + sp.Rational(U_DELTA_NUMERATORS[residue], 360)


def T(n: int) -> int:
    """Partitions of n using parts 1,2,3,3,5."""
    if n < 0:
        return 0
    value = (
        Fraction(n**4, 2160)
        + Fraction(7 * n**3, 540)
        + Fraction(n**2, 8)
        + Fraction(T_ALPHA_NUMERATORS[n % 3] * n, 540)
        + Fraction(T_BETA_NUMERATORS[n % 30], 2160)
    )
    assert value.denominator == 1
    return value.numerator


def U(n: int) -> int:
    """Partitions of n using parts 1,2,3,5."""
    if n < 0:
        return 0
    value = (
        Fraction(n**3, 180)
        + Fraction(11 * n**2, 120)
        + Fraction(9 * n, 20)
        + Fraction(U_DELTA_NUMERATORS[n % 30], 360)
    )
    assert value.denominator == 1
    return value.numerator


def P6(n: int) -> int:
    """Partitions of n using parts 2,3,4,5,6."""
    if n < 0:
        return 0
    if n % 2 == 0:
        return T(n // 2) + T(n // 2 - 4)
    half = (n - 1) // 2
    return T(half - 1) + T(half - 2)


def P5(n: int) -> int:
    """Partitions of n using parts 2,3,4,5."""
    if n < 0:
        return 0
    if n % 2 == 0:
        return U(n // 2) + U(n // 2 - 4)
    half = (n - 1) // 2
    return U(half - 1) + U(half - 2)


def gaussian_layer(k: int, i: int) -> int:
    """[q^i](1-q)({5k+6 choose 6}_q-{6k+5 choose 5}_q), i<=15k."""
    return (
        P6(i)
        - sum(P6(i - 5 * k - nu) for nu in range(1, 7))
        + sum(
            P6(i - 10 * k - mu - nu)
            for mu in range(1, 7)
            for nu in range(mu + 1, 7)
        )
        - P5(i)
        + sum(P5(i - 6 * k - nu) for nu in range(1, 6))
        - sum(
            P5(i - 12 * k - mu - nu)
            for mu in range(1, 6)
            for nu in range(mu + 1, 6)
        )
    )


def remainder_layer(k: int, r: int) -> int:
    """Ordinary Schur layer of the aligned two-step remainder."""
    return gaussian_layer(k, r + 6) - gaussian_layer(k - 2, r - 24)


def power_sum(power: int, y: sp.Expr) -> sp.Expr:
    if power == 0:
        return 1 / (1 - y)
    if power == 1:
        return y / (1 - y) ** 2
    if power == 2:
        return y * (1 + y) / (1 - y) ** 3
    if power == 3:
        return y * (1 + 4 * y + y**2) / (1 - y) ** 4
    if power == 4:
        return y * (1 + 11 * y + 11 * y**2 + y**3) / (1 - y) ** 5
    raise ValueError(power)


def residue_series(qvar: sp.Symbol, period: int, polynomial) -> sp.Expr:
    m = sp.symbols("m", integer=True, nonnegative=True)
    y = qvar**period
    result = 0
    for residue in range(period):
        expression = sp.Poly(sp.expand(polynomial(period * m + residue, residue)), m, domain=sp.QQ)
        result += qvar**residue * sum(
            coefficient * power_sum(power[0], y)
            for power, coefficient in expression.terms()
        )
    return result


def verify_quasipolynomials() -> None:
    qvar = sp.symbols("qvar")
    t_series = residue_series(qvar, 30, t_residue_polynomial)
    assert sp.cancel(t_series * (1 - qvar) * (1 - qvar**2) * (1 - qvar**3) ** 2 * (1 - qvar**5) - 1) == 0
    u_series = residue_series(qvar, 30, u_residue_polynomial)
    assert sp.cancel(u_series * (1 - qvar) * (1 - qvar**2) * (1 - qvar**3) * (1 - qvar**5) - 1) == 0


# (kind, coefficient, (coefficient_of_j, coefficient_of_t, constant))
Term = tuple[str, int, tuple[int, int, int]]


def restricted_terms(
    kind: str,
    r_parity: int,
    k_residue: int,
    coefficient: int,
    k_multiplier: int,
    shift: int,
) -> list[Term]:
    """Expand P6/P5(2j+r-k_multiplier*k-shift) through T/U."""
    constant = r_parity - k_multiplier * k_residue - shift
    if constant % 2 == 0:
        half = constant // 2
        return [
            (kind, coefficient, (1, -k_multiplier, half)),
            (kind, coefficient, (1, -k_multiplier, half - 4)),
        ]
    half = (constant - 1) // 2
    return [
        (kind, coefficient, (1, -k_multiplier, half - 1)),
        (kind, coefficient, (1, -k_multiplier, half - 2)),
    ]


def k_terms(r_parity: int, k_residue: int) -> list[Term]:
    """Translate remainder_layer(k,r), r=2j+r_parity."""
    i_parity = r_parity + 6
    result = restricted_terms("T", i_parity, k_residue, 1, 0, 0)
    result += restricted_terms("T", i_parity, k_residue, -1, 0, 30)
    for nu in range(1, 7):
        result += restricted_terms("T", i_parity, k_residue, -1, 5, nu)
        result += restricted_terms("T", i_parity, k_residue, 1, 5, nu + 20)
    for mu in range(1, 7):
        for nu in range(mu + 1, 7):
            result += restricted_terms("T", i_parity, k_residue, 1, 10, mu + nu)
            result += restricted_terms("T", i_parity, k_residue, -1, 10, mu + nu + 10)

    result += restricted_terms("U", i_parity, k_residue, -1, 0, 0)
    result += restricted_terms("U", i_parity, k_residue, 1, 0, 30)
    for nu in range(1, 6):
        result += restricted_terms("U", i_parity, k_residue, 1, 6, nu)
        result += restricted_terms("U", i_parity, k_residue, -1, 6, nu + 18)
    for mu in range(1, 6):
        for nu in range(mu + 1, 6):
            result += restricted_terms("U", i_parity, k_residue, -1, 12, mu + nu)
            result += restricted_terms("U", i_parity, k_residue, 1, 12, mu + nu + 6)
    return result


def consolidate(terms: list[Term]) -> list[Term]:
    coefficients: dict[tuple[str, tuple[int, int, int]], int] = defaultdict(int)
    for kind, coefficient, argument in terms:
        coefficients[(kind, argument)] += coefficient
    return sorted(
        (kind, coefficient, argument)
        for (kind, argument), coefficient in coefficients.items()
        if coefficient
    )


def quantity_terms(k_residue: int, quantity: str) -> list[Term]:
    even = k_terms(0, k_residue)
    if quantity == "A":
        return consolidate(even)
    odd = k_terms(1, k_residue)
    return consolidate(
        [(kind, 2 * coefficient, argument) for kind, coefficient, argument in even]
        + [(kind, -coefficient, argument) for kind, coefficient, argument in odd]
    )


def domain_end(k_residue: int, quantity: str) -> tuple[int, int]:
    """Exclusive j bound, including the unpaired even-k A endpoint."""
    if k_residue == 0:
        return (15, -2 if quantity == "A" else -3)
    return (15, 5)


def coefficients_nonnegative(expression: sp.Expr, variable: sp.Symbol) -> bool:
    polynomial = sp.Poly(sp.expand(expression), variable, domain=sp.QQ)
    return all(coefficient >= 0 for _, coefficient in polynomial.terms())


def affine_string(slope: int, constant: int) -> str:
    return str(sp.expand(slope * t + constant))


def certificate_records() -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    alpha_min = sp.Rational(min(T_ALPHA_NUMERATORS), 540)
    alpha_max = sp.Rational(max(T_ALPHA_NUMERATORS), 540)
    beta_min = sp.Rational(min(T_BETA_NUMERATORS), 2160)
    beta_max = sp.Rational(max(T_BETA_NUMERATORS), 2160)
    delta_min = sp.Rational(min(U_DELTA_NUMERATORS), 360)
    delta_max = sp.Rational(max(U_DELTA_NUMERATORS), 360)

    for residue in (0, 1):
        for quantity in ("A", "C"):
            terms = quantity_terms(residue, quantity)
            end = domain_end(residue, quantity)
            candidates = {(0, 0), end} | {(-arg[1], -arg[2]) for _, _, arg in terms}
            boundaries: set[tuple[int, int]] = set()
            for bound in candidates:
                lower_test = bound[0] * (T_START + x) + bound[1]
                end_test = (end[0] - bound[0]) * (T_START + x) + end[1] - bound[1]
                if coefficients_nonnegative(lower_test, x) and coefficients_nonnegative(end_test, x):
                    boundaries.add(bound)
            ordered = sorted(boundaries, key=lambda b: (b[0] * T_START + b[1], b[0], b[1]))
            assert ordered[0] == (0, 0) and ordered[-1] == end

            for left, right in zip(ordered, ordered[1:]):
                gap = (right[0] - left[0]) * (T_START + x) + right[1] - left[1]
                assert coefficients_nonnegative(gap - 1, x), (
                    "unstable cell", residue, quantity, left, right
                )
                lower = left[0] * t + left[1]
                upper = right[0] * t + right[1] - 1
                active: list[Term] = []
                for kind, coefficient, argument in terms:
                    threshold = -argument[1] * t - argument[2]
                    if coefficients_nonnegative((lower - threshold).subs(t, T_START + x), x):
                        active.append((kind, coefficient, argument))

                if left[0] == 0 and right[0] == 0:
                    assert all(argument[1] == 0 for _, _, argument in active)
                    k = 2 * T_START + residue
                    values = []
                    for pair in range(left[1], right[1]):
                        current = remainder_layer(k, 2 * pair)
                        if quantity == "C":
                            current = 2 * current - remainder_layer(k, 2 * pair + 1)
                        assert current >= 0
                        values.append(current)
                    records.append({
                        "k_mod_2": residue,
                        "quantity": quantity,
                        "lower": affine_string(*left),
                        "upper": affine_string(right[0], right[1] - 1),
                        "active_terms": len(active),
                        "exact_values": values,
                    })
                    continue

                polynomial = sp.Integer(0)
                for kind, coefficient, argument in active:
                    arg_expr = j + argument[1] * t + argument[2]
                    if kind == "T":
                        if coefficient > 0:
                            bound = t_common(arg_expr) + alpha_min * arg_expr + beta_min
                        else:
                            bound = t_common(arg_expr) + alpha_max * arg_expr + beta_max
                    else:
                        bound = u_common(arg_expr) + (delta_min if coefficient > 0 else delta_max)
                    polynomial += coefficient * bound

                width = upper - lower
                assert coefficients_nonnegative(width.subs(t, T_START + x), x)
                on_unit = sp.expand(polynomial).subs(j, lower + width * z).subs(t, T_START + x)
                power = sp.Poly(sp.expand(on_unit), z, domain=sp.QQ.frac_field(x))
                assert power.degree() <= 4
                power_coeffs = [power.coeff_monomial(z**degree) for degree in range(5)]
                bernstein: list[str] = []
                for index in range(5):
                    coefficient = sp.cancel(sum(
                        power_coeffs[degree] * sp.binomial(index, degree) / sp.binomial(4, degree)
                        for degree in range(index + 1)
                    ))
                    coefficient_poly = sp.Poly(coefficient, x, domain=sp.QQ)
                    assert coefficients_nonnegative(coefficient_poly.as_expr(), x), (
                        "negative Bernstein coefficient",
                        residue,
                        quantity,
                        left,
                        right,
                        index,
                        coefficient,
                    )
                    bernstein.append(str(coefficient_poly.as_expr()))
                records.append({
                    "k_mod_2": residue,
                    "quantity": quantity,
                    "lower": affine_string(*left),
                    "upper": affine_string(right[0], right[1] - 1),
                    "active_terms": len(active),
                    "bernstein_QQ[x]": bernstein,
                })
    return records


def evaluate_terms(terms: list[Term], parameter: int, pair: int) -> int:
    return sum(
        coefficient * (T if kind == "T" else U)(
            pair + argument[1] * parameter + argument[2]
        )
        for kind, coefficient, argument in terms
    )


def verify_term_translation(max_k: int = 200) -> None:
    for k in range(3, max_k + 1):
        residue = k % 2
        parameter = (k - residue) // 2
        for quantity in ("A", "C"):
            terms = quantity_terms(residue, quantity)
            end = domain_end(residue, quantity)
            for pair in range(end[0] * parameter + end[1]):
                expected = remainder_layer(k, 2 * pair)
                if quantity == "C":
                    expected = 2 * expected - remainder_layer(k, 2 * pair + 1)
                assert evaluate_terms(terms, parameter, pair) == expected, (
                    "term translation", k, quantity, pair
                )


def verify_finite_bases() -> None:
    for k in range(3, 2 * T_START):
        residue = k % 2
        parameter = (k - residue) // 2
        for quantity in ("A", "C"):
            end = domain_end(residue, quantity)
            for pair in range(end[0] * parameter + end[1]):
                current = remainder_layer(k, 2 * pair)
                if quantity == "C":
                    current = 2 * current - remainder_layer(k, 2 * pair + 1)
                assert current >= 0, ("finite sign", k, quantity, pair, current)


def main() -> None:
    assert sp.__version__ == "1.14.0", sp.__version__
    verify_quasipolynomials()
    verify_term_translation()
    verify_finite_bases()
    records = certificate_records()
    canonical = json.dumps(records, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    if EXPECTED_CERTIFICATE_SHA256:
        assert digest == EXPECTED_CERTIFICATE_SHA256, digest
    exact_cells = sum("exact_values" in record for record in records)
    bernstein_count = sum(len(record.get("bernstein_QQ[x]", [])) for record in records)
    print("exact QQ affine-cell/Bernstein certificate passed")
    print("T and U quasipolynomial generating-function identities verified exactly")
    print(f"finite recurrence parameters verified for 3 <= k < {2 * T_START}")
    print(
        f"affine cells: {len(records)}; exact cells: {exact_cells}; "
        f"Bernstein polynomials: {bernstein_count}"
    )
    print(f"certificate SHA-256: {digest}")


if __name__ == "__main__":
    main()
