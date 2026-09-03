#!/usr/bin/env python3
"""Exact arithmetic audit for the Suzuki cyclic-subgroup formula and bound."""

from __future__ import annotations

import argparse
from math import prod


def factor(n: int) -> dict[int, int]:
    """Factor a positive integer by deterministic trial division."""
    if n < 1:
        raise ValueError("factorization input must be positive")
    out: dict[int, int] = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p = 3 if p == 2 else p + 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def tau(n: int) -> int:
    """Return the number of positive divisors of n."""
    return prod(exponent + 1 for exponent in factor(n).values())


def omega(n: int) -> int:
    """Return the number of distinct prime divisors of n."""
    return len(factor(n))


def divisors(n: int) -> list[int]:
    """Return all positive divisors of n in increasing order."""
    values = [1]
    for prime, exponent in factor(n).items():
        values = [
            divisor * prime**power
            for divisor in values
            for power in range(exponent + 1)
        ]
    return sorted(values)


def audit_exponent(e: int) -> tuple[int, int, int, int]:
    """Audit one odd Suzuki field exponent."""
    if e < 3 or e % 2 == 0:
        raise ValueError("e must be odd and at least 3")

    q = 2**e
    r = 2 ** ((e + 1) // 2)
    t_minus = q - r + 1
    t_plus = q + r + 1
    odd_part = (q - 1) * (q * q + 1)
    group_order = q * q * odd_part

    assert t_minus * t_plus == q * q + 1

    n_zero = group_order // (2 * (q - 1))
    n_minus = group_order // (4 * t_minus)
    n_plus = group_order // (4 * t_plus)
    assert n_zero + n_minus + n_plus == q**4

    # Independently check that the four Suzuki partition types account for
    # every nonidentity element exactly once.
    partition_nonidentity = (
        (q * q + 1) * (q * q - 1)
        + n_zero * (q - 2)
        + n_minus * (t_minus - 1)
        + n_plus * (t_plus - 1)
    )
    assert partition_nonidentity == group_order - 1

    cyclic_formula = (
        1
        + (q * q + 1) * ((q - 1) + (q * q - q) // 2)
        + n_zero * (tau(q - 1) - 1)
        + n_minus * (tau(t_minus) - 1)
        + n_plus * (tau(t_plus) - 1)
    )
    assert cyclic_formula > q**4

    max_threshold = 0
    for index in divisors(e):
        distinct_primes = omega(group_order * index)
        threshold = 2 ** (distinct_primes + 2)
        assert q**4 + 1 >= threshold
        assert cyclic_formula >= threshold
        max_threshold = max(max_threshold, threshold)

    if e >= 7:
        assert q >= 8 * e
        assert q**4 > 8 * e * odd_part
    elif e == 3:
        assert factor(odd_part) == {5: 1, 7: 1, 13: 1}
    elif e == 5:
        assert factor(odd_part) == {5: 2, 31: 1, 41: 1}

    return q, cyclic_formula, q**4 + 1, max_threshold


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-exponent", type=int, default=19)
    args = parser.parse_args()
    if args.max_exponent < 3:
        parser.error("--max-exponent must be at least 3")
    return args


def main() -> None:
    args = parse_args()
    print("e q exact_cyc torus_lower_bound max_almost_simple_threshold")
    checked = 0
    for e in range(3, args.max_exponent + 1, 2):
        q, exact_cyc, lower_bound, threshold = audit_exponent(e)
        print(e, q, exact_cyc, lower_bound, threshold)
        checked += 1
    print(f"checked_exponents={checked}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
