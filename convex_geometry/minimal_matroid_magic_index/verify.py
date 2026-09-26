#!/usr/bin/env python3
"""Finite exact checks for PROOF.md; Python standard library only.

Polynomials are tuples of Fraction coefficients in ascending degree.
This program is a consistency check, not a proof of all parameter values.
"""

from fractions import Fraction as F
from functools import cache
from hashlib import sha256
from itertools import product
from math import comb, factorial
import json


def require(condition, description):
    if not condition:
        raise AssertionError(description)


def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return tuple(p)


def add(p, q):
    out = [F(0)] * max(len(p), len(q))
    for i, a in enumerate(p):
        out[i] += a
    for i, a in enumerate(q):
        out[i] += a
    return trim(out)


def scale(p, a):
    return trim(tuple(a * b for b in p))


def mul(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return trim(out)


def evaluate(p, x):
    out = F(0)
    for a in reversed(p):
        out = out * x + a
    return out


@cache
def choose_poly(shift, degree):
    """The polynomial binom(x + shift, degree), including negative shifts."""
    require(degree >= 0, "negative binomial degree")
    p = (F(1),)
    for j in range(degree):
        p = mul(p, (F(shift - j), F(1)))
    return scale(p, F(1, factorial(degree)))


def residual(k, r):
    require(k >= 1 and r >= 1, "rank and corank must be positive")
    q = (F(0),)
    for j in range(k):
        q = add(q, scale(choose_poly(j, j), comb(r - 1 + j, j)))
    return q


def factored_ehrhart(k, n):
    r = n - k
    return scale(mul(choose_poly(r, r), residual(k, r)),
                 F(1, comb(n - 1, k - 1)))


def hstar_ehrhart(k, n):
    """Independent binomial-basis formula, Ferroni Theorem 3.1."""
    r, d = n - k, n - 1
    p = (F(0),)
    for j in range(min(k, r)):
        p = add(p, scale(choose_poly(d - j, d),
                         comb(k - 1, j) * comb(r - 1, j)))
    return p


def interpolation_residual(k, r):
    """Positive product decomposition (5), only in the normalized range."""
    require(1 <= k <= r, "interpolation positivity requires k <= r")
    q = (F(0),)
    for h in range(1, k + 1):
        term = (F(1),)
        for j in range(1, k + 1):
            if j != h:
                term = mul(term, (F(j), F(1)))
        weight = F(comb(r - 1, h - 1),
                   factorial(h - 1) * factorial(k - h))
        q = add(q, scale(term, weight))
    return q


def magic_coefficients(p, dilation):
    """Coefficients of (1-t)^d p(dilation*t/(1-t)); retain degree d."""
    d = len(p) - 1
    return tuple(sum(((-1) ** (i - j) * comb(d - j, i - j)
                      * p[j] * dilation ** j for j in range(i + 1)), F(0))
                 for i in range(d + 1))


def count_by_slices(k, r, m):
    return sum(comb(t + k - 1, k - 1) * comb(t + r - 1, r - 1)
               for t in range(m + 1))


def count_direct(k, n, m):
    """Enumerate integer coordinates in the original polytope inequalities."""
    return sum(1 for z in product(range(m + 1), repeat=n)
               if sum(z) == k * m and sum(z[k:]) <= m)


def main():
    # Hand-checkable polynomial and degree-elevation boundary cases.
    require(factored_ehrhart(1, 2) == (F(1), F(1)), "unit segment")
    require(residual(3, 3) == (F(10), F(12), F(3)), "Q_(3,3)")
    require(magic_coefficients((F(2), F(1)), F(1)) == (F(2), F(-1)),
            "different-degree sums do not preserve magic positivity")

    digest = sha256()
    cases = normalized = slice_checks = sign_checks = 0
    for n in range(2, 31):
        for k in range(1, n):
            r, d = n - k, n - 1
            p = factored_ehrhart(k, n)
            context = (k, n)
            require(len(p) == n, ("degree", context))
            require(p == hstar_ehrhart(k, n), ("hstar formula", context))
            require(p == factored_ehrhart(r, n), ("duality", context))
            require(evaluate(p, 0) == 1, ("constant term", context))
            require(evaluate(p, 1) == 1 + k * r, ("basis count", context))
            for m in range(n):
                require(evaluate(p, m) == count_by_slices(k, r, m),
                        ("slice count", context, m))
                slice_checks += 1

            if k <= r:
                q = residual(k, r)
                require(q == interpolation_residual(k, r),
                        ("positive interpolation", context))
                require(len(q) == k and q[-1] > 0, ("residual degree", context))
                for h in range(1, k + 1):
                    value = evaluate(q, -h)
                    require(value == (-1) ** (h - 1) * comb(r - 1, h - 1),
                            ("root sign certificate", context, h))
                    require((-1) ** (h - 1) * value > 0,
                            ("strict alternating signs", context, h))
                    sign_checks += 1
                normalized += 1

            threshold = max(k, r)
            require(evaluate(p, -threshold) == 0, ("sharp root", context))
            at = magic_coefficients(p, F(threshold))
            above = magic_coefficients(p, F(threshold) + F(1, 2))
            below = magic_coefficients(p, F(threshold) - F(1, 2))
            require(at[-1] == 0 and all(b > 0 for b in at[:-1]),
                    ("threshold positivity", context))
            require(all(b > 0 for b in above), ("strictly above", context))
            require(any(b < 0 for b in below), ("strictly below", context))
            if threshold > 1:
                require(any(b < 0 for b in magic_coefficients(p, F(threshold - 1))),
                        ("previous integer", context))
            record = [k, n, [str(a) for a in p], [str(a) for a in at]]
            digest.update((json.dumps(record, separators=(",", ":")) + "\n").encode())
            cases += 1

    lattice_checks = 0
    for n in range(2, 9):
        for k in range(1, n):
            p = factored_ehrhart(k, n)
            for m in range(4):
                require(count_direct(k, n, m) == evaluate(p, m),
                        ("direct lattice enumeration", k, n, m))
                lattice_checks += 1

    print(json.dumps({
        "all_checks_passed": True,
        "arithmetic": "Python integers and fractions.Fraction; no floating point",
        "parameter_range": "2 <= n <= 30; 1 <= k < n",
        "polynomial_cases": cases,
        "normalized_interpolation_cases": normalized,
        "alternating_sign_checks": sign_checks,
        "slice_count_checks": slice_checks,
        "direct_lattice_range": "2 <= n <= 8; 1 <= k < n; 0 <= m <= 3",
        "direct_lattice_checks": lattice_checks,
        "example_k3_n6_ehrhart_ascending": [str(a) for a in factored_ehrhart(3, 6)],
        "example_k3_n6_magic_at3_ascending": [str(a) for a in magic_coefficients(
            factored_ehrhart(3, 6), F(3))],
        "polynomial_and_threshold_records_sha256": digest.hexdigest(),
        "universal_claim_evidence": "The proof in PROOF.md, not this finite run",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
