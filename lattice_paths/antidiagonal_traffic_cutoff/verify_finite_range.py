#!/usr/bin/env python3
"""Exact finite bridge for the antidiagonal traffic cutoff theorem.

The mathematical proof shows that for fixed n the maximum occurs at the first
allowed k (positive and congruent to n modulo 2) for which

    F_n(k) = n^2 - 5n - 2 - (7n+1)k - 2nk^2

is nonpositive.  This program checks R_n(k) < 1 for that candidate for every
496 <= n <= 9999.  All comparisons are over Python integers.
"""

from __future__ import annotations

from decimal import Decimal, getcontext
from math import comb

START = 496
STOP = 10_000  # exclusive
CHECKPOINTS = frozenset({496, 497, 999, 1000, 9998, 9999})


def central_binomial(n: int) -> int:
    """Return C(n, floor(n/2)); used only for initialization/checks."""
    return comb(n, n // 2)


def critical_k(n: int) -> int:
    """First allowed k at which the adjacent ratio is nonincreasing."""
    k = 1 if n % 2 else 2
    while n * n - 5 * n - 2 - (7 * n + 1) * k - 2 * n * k * k > 0:
        k += 2
    return k


def offset_ratio(n: int, k: int) -> tuple[int, int]:
    """Return p,q with C(n,(n-k)/2)/C(n,floor(n/2)) = p/q."""
    if n % 2:
        m = n // 2
        steps = (k - 1) // 2
        denominator_shift = 1
    else:
        m = n // 2
        steps = k // 2
        denominator_shift = 0

    numerator = 1
    denominator = 1
    for j in range(1, steps + 1):
        numerator *= m - j + 1
        denominator *= m + j + denominator_shift
    return numerator, denominator


def traffic_ratio_parts(
    n: int,
    k: int,
    central_n: int,
    central_n_minus_2: int,
    central_2n_minus_2: int,
) -> tuple[int, int]:
    """Return numerator and denominator of the unreduced exact R_n(k)."""
    p1, q1 = offset_ratio(n, k)
    p2, q2 = offset_ratio(n - 2, k)
    numerator = (
        2 * n * (k + 1) * central_n * central_n_minus_2 * p1 * p2
    )
    denominator = (n + k) * central_2n_minus_2 * q1 * q2
    return numerator, denominator


def main() -> None:
    # b2 and b1 are C(n-2,floor((n-2)/2)) and
    # C(n-1,floor((n-1)/2)) at the start of each iteration.
    b2 = central_binomial(START - 2)
    b1 = central_binomial(START - 1)
    denominator_central = comb(2 * START - 2, START - 1)

    worst_numerator = 0
    worst_denominator = 1
    worst_n = 0
    worst_k = 0

    for n in range(START, STOP):
        # C(2m+2,m+1)=2*C(2m+1,m), while
        # C(2m+1,m)=(2m+1)/(m+1)*C(2m,m).
        if n % 2 == 0:
            bn = 2 * b1
        else:
            bn = n * b1 // ((n + 1) // 2)

        if n in CHECKPOINTS:
            assert bn == central_binomial(n)
            assert b2 == central_binomial(n - 2)
            assert denominator_central == comb(2 * n - 2, n - 1)

        k = critical_k(n)
        numerator, denominator = traffic_ratio_parts(
            n, k, bn, b2, denominator_central
        )
        if numerator >= denominator:
            raise AssertionError(f"R >= 1 at n={n}, k={k}")

        if numerator * worst_denominator > worst_numerator * denominator:
            worst_numerator = numerator
            worst_denominator = denominator
            worst_n = n
            worst_k = k

        b2, b1 = b1, bn
        if n + 1 < STOP:
            # C(2n,n) / C(2n-2,n-1) = (2n)(2n-1)/n^2.
            denominator_central = (
                denominator_central * (2 * n) * (2 * n - 1) // (n * n)
            )

    # Confirm sharpness immediately below the claimed cutoff.
    boundary_n = START - 1
    boundary_k = critical_k(boundary_n)
    boundary_numerator, boundary_denominator = traffic_ratio_parts(
        boundary_n,
        boundary_k,
        central_binomial(boundary_n),
        central_binomial(boundary_n - 2),
        comb(2 * boundary_n - 2, boundary_n - 1),
    )
    assert boundary_numerator > boundary_denominator

    getcontext().prec = 30
    worst_decimal = Decimal(worst_numerator) / Decimal(worst_denominator)
    boundary_decimal = Decimal(boundary_numerator) / Decimal(boundary_denominator)
    print(f"PASS checked={STOP - START} range={START}..{STOP - 1}")
    print(f"worst n={worst_n} k={worst_k} R={worst_decimal}")
    print(f"boundary n={boundary_n} k={boundary_k} R={boundary_decimal} > 1")


if __name__ == "__main__":
    main()
