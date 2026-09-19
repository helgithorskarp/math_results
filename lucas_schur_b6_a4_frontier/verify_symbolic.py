#!/usr/bin/env python3
"""Exact affine-cell certificate for the canonical Lucas (4,6) ray.

The certificate proves the two ordinary Schur-layer inequalities that make
the alternating Lucas image Schur-positive.  It uses exact restricted-
partition quasipolynomials and rational Bernstein coefficients only.
"""

from __future__ import annotations

import argparse
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
W_BETA_TWELFTHS = (12, 5, 8, 9, 8, 5)
EXPECTED_CERTIFICATE_SHA256 = "83bca8bd00e22bcbce864fec0631fc605a9971b448de643b0d0b2929947ee43c"

j, t, x, z = sp.symbols("j t x z")


def t_common(n: sp.Expr) -> sp.Expr:
    return n**4 / sp.Integer(2160) + sp.Rational(7, 540) * n**3 + n**2 / sp.Integer(8)


def t_residue_polynomial(n: sp.Expr, residue: int) -> sp.Expr:
    return (
        t_common(n)
        + sp.Rational(T_ALPHA_NUMERATORS[residue % 3], 540) * n
        + sp.Rational(T_BETA_NUMERATORS[residue], 2160)
    )


def w_common(n: sp.Expr) -> sp.Expr:
    return n**2 / sp.Integer(12) + n / sp.Integer(2)


def w_residue_polynomial(n: sp.Expr, residue: int) -> sp.Expr:
    return w_common(n) + sp.Rational(W_BETA_TWELFTHS[residue], 12)


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


def W(n: int) -> int:
    """Partitions of n using parts 1,2,3."""
    if n < 0:
        return 0
    value = Fraction(n**2, 12) + Fraction(n, 2) + Fraction(W_BETA_TWELFTHS[n % 6], 12)
    assert value.denominator == 1
    return value.numerator


def P(n: int) -> int:
    """Partitions of n using parts 2,3,4,5,6."""
    if n < 0:
        return 0
    if n % 2 == 0:
        return T(n // 2) + T(n // 2 - 4)
    half = (n - 1) // 2
    return T(half - 1) + T(half - 2)


def Q(n: int) -> int:
    """Partitions of n using parts 2,3,4."""
    if n < 0:
        return 0
    return W(n // 2) if n % 2 == 0 else W((n - 3) // 2)


def gaussian_layer(k: int, i: int) -> int:
    """[q^i](1-q)({2k+6 choose 6}_q-{3k+4 choose 4}_q), i<=6k."""
    return (
        P(i)
        - sum(P(i - 2 * k - nu) for nu in range(1, 7))
        + sum(
            P(i - 4 * k - mu - nu)
            for mu in range(1, 7)
            for nu in range(mu + 1, 7)
        )
        - Q(i)
        + sum(Q(i - 3 * k - nu) for nu in range(1, 5))
    )


def remainder_layer(k: int, r: int) -> int:
    """Ordinary Schur layer of the aligned ten-step remainder."""
    return gaussian_layer(k, r + 5) - gaussian_layer(k - 10, r - 55)


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


def residue_series(qvar: sp.Symbol, period: int, degree: int, polynomial) -> sp.Expr:
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
    t_series = residue_series(qvar, 30, 4, t_residue_polynomial)
    assert sp.cancel(t_series * (1 - qvar) * (1 - qvar**2) * (1 - qvar**3) ** 2 * (1 - qvar**5) - 1) == 0
    w_series = residue_series(qvar, 6, 2, w_residue_polynomial)
    assert sp.cancel(w_series * (1 - qvar) * (1 - qvar**2) * (1 - qvar**3) - 1) == 0


# (kind, coefficient, (coefficient_of_j, coefficient_of_t, constant))
Term = tuple[str, int, tuple[int, int, int]]


def p_terms(r_parity: int, k_residue: int, coefficient: int, k_multiplier: int, shift: int) -> list[Term]:
    """Expand P(2j+r_parity-k_multiplier*k-shift), k=2t+rho."""
    constant = r_parity - k_multiplier * k_residue - shift
    if constant % 2 == 0:
        half = constant // 2
        return [
            ("T", coefficient, (1, -k_multiplier, half)),
            ("T", coefficient, (1, -k_multiplier, half - 4)),
        ]
    half = (constant - 1) // 2
    return [
        ("T", coefficient, (1, -k_multiplier, half - 1)),
        ("T", coefficient, (1, -k_multiplier, half - 2)),
    ]


def q_terms(r_parity: int, k_residue: int, coefficient: int, k_multiplier: int, shift: int) -> list[Term]:
    """Expand Q(2j+r_parity-k_multiplier*k-shift) through W."""
    constant = r_parity - k_multiplier * k_residue - shift
    if constant % 2 == 0:
        return [("W", coefficient, (1, -k_multiplier, constant // 2))]
    return [("W", coefficient, (1, -k_multiplier, (constant - 3) // 2))]


def k_terms(r_parity: int, k_residue: int) -> list[Term]:
    """Translate remainder_layer(k,r), r=2j+r_parity."""
    i_parity = r_parity + 5
    result = p_terms(i_parity, k_residue, 1, 0, 0)
    result += p_terms(i_parity, k_residue, -1, 0, 60)
    for nu in range(1, 7):
        result += p_terms(i_parity, k_residue, -1, 2, nu)
        result += p_terms(i_parity, k_residue, 1, 2, nu + 40)
    for mu in range(1, 7):
        for nu in range(mu + 1, 7):
            result += p_terms(i_parity, k_residue, 1, 4, mu + nu)
            result += p_terms(i_parity, k_residue, -1, 4, mu + nu + 20)
    result += q_terms(i_parity, k_residue, -1, 0, 0)
    result += q_terms(i_parity, k_residue, 1, 0, 60)
    for nu in range(1, 5):
        result += q_terms(i_parity, k_residue, 1, 3, nu)
        result += q_terms(i_parity, k_residue, -1, 3, nu + 30)
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


def domain_end(k_residue: int) -> tuple[int, int]:
    """Exclusive pair bound: 0 <= j < 3k-2."""
    return (6, -2) if k_residue == 0 else (6, 1)


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
    w_beta_min = sp.Rational(min(W_BETA_TWELFTHS), 12)
    w_beta_max = sp.Rational(max(W_BETA_TWELFTHS), 12)

    for residue in (0, 1):
        for quantity in ("A", "C"):
            terms = quantity_terms(residue, quantity)
            end = domain_end(residue)
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
                assert coefficients_nonnegative(gap - 1, x), ("unstable cell", residue, quantity, left, right)
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
                        bound = w_common(arg_expr) + (w_beta_min if coefficient > 0 else w_beta_max)
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
                        "negative Bernstein coefficient", residue, quantity, left, right, index, coefficient
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
        coefficient * (T if kind == "T" else W)(pair + argument[1] * parameter + argument[2])
        for kind, coefficient, argument in terms
    )


def verify_term_translation(max_k: int = 200) -> None:
    for k in range(13, max_k + 1):
        residue = k % 2
        parameter = (k - residue) // 2
        for quantity in ("A", "C"):
            terms = quantity_terms(residue, quantity)
            pair_count = domain_end(residue)[0] * parameter + domain_end(residue)[1]
            for pair in range(pair_count):
                expected = remainder_layer(k, 2 * pair)
                if quantity == "C":
                    expected = 2 * expected - remainder_layer(k, 2 * pair + 1)
                assert evaluate_terms(terms, parameter, pair) == expected, (
                    "term translation", k, quantity, pair
                )


def verify_finite_bases() -> None:
    for k in range(13, 2 * T_START):
        residue = k % 2
        parameter = (k - residue) // 2
        pair_count = domain_end(residue)[0] * parameter + domain_end(residue)[1]
        for quantity in ("A", "C"):
            for pair in range(pair_count):
                current = remainder_layer(k, 2 * pair)
                if quantity == "C":
                    current = 2 * current - remainder_layer(k, 2 * pair + 1)
                assert current >= 0, ("finite sign", k, quantity, pair, current)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--show-certificate", action="store_true")
    args = parser.parse_args()
    assert sp.__version__ == "1.14.0", sp.__version__
    verify_quasipolynomials()
    verify_term_translation()
    verify_finite_bases()
    records = certificate_records()
    canonical = json.dumps(records, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    if EXPECTED_CERTIFICATE_SHA256:
        assert digest == EXPECTED_CERTIFICATE_SHA256, digest
    if args.show_certificate:
        print(json.dumps(records, indent=2, sort_keys=True))
    exact_cells = sum("exact_values" in record for record in records)
    bernstein_count = sum(len(record.get("bernstein_QQ[x]", [])) for record in records)
    print("exact QQ affine-cell/Bernstein certificate passed")
    print("T and W quasipolynomial generating-function identities verified exactly")
    print(f"finite recurrence parameters verified for 13 <= k < {2 * T_START}")
    print(f"affine cells: {len(records)}; exact cells: {exact_cells}; Bernstein polynomials: {bernstein_count}")
    print(f"certificate SHA-256: {digest}")


if __name__ == "__main__":
    main()
