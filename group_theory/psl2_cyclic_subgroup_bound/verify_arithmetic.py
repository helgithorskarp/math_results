#!/usr/bin/env python3
"""Finite audit of the arithmetic in the PSL(2,q) cyclic-subgroup bound.

This script is a falsification check, not a proof of the universal theorem.
It checks every prime power q <= LIMIT, recomputes omega(|PSL(2,q)|) from
the prime divisors of q, q-1, and q+1, verifies the odd/even identities in
the README, and checks the q^2+1 comparison outside q=4,5.
"""

from __future__ import annotations

from math import gcd


LIMIT = 1_000_000


def smallest_prime_factors(limit: int) -> list[int]:
    spf = list(range(limit + 1))
    for p in range(2, int(limit**0.5) + 1):
        if spf[p] != p:
            continue
        for n in range(p * p, limit + 1, p):
            if spf[n] == n:
                spf[n] = p
    return spf


def distinct_prime_factors(n: int, spf: list[int]) -> set[int]:
    factors: set[int] = set()
    while n > 1:
        p = spf[n]
        factors.add(p)
        while n % p == 0:
            n //= p
    return factors


def main() -> None:
    spf = smallest_prime_factors(LIMIT + 1)
    primes = [p for p in range(2, LIMIT + 1) if spf[p] == p]
    rows: dict[int, tuple[int, int]] = {}

    for characteristic in primes:
        q = characteristic
        while q <= LIMIT:
            if q >= 4:
                fq = distinct_prime_factors(q, spf)
                fm = distinct_prime_factors(q - 1, spf)
                fp = distinct_prime_factors(q + 1, spf)
                order_primes = fq | fm | fp
                t = len(order_primes)

                # Cross-check that the union really is the support of
                # q(q^2-1)/gcd(2,q-1); division cannot delete a prime.
                assert gcd(characteristic, (q - 1) * (q + 1)) == 1
                if q % 2:
                    assert t == len(fm) + len(fp)
                else:
                    assert t == 1 + len(fm) + len(fp)

                torus_lower_bound = q * q + 1
                target = 1 << (t + 2)
                rows[q] = (t, torus_lower_bound - target)
                if q not in (4, 5):
                    assert torus_lower_bound >= target, (q, t)

            if q > LIMIT // characteristic:
                break
            q *= characteristic

    q_min, (_, margin_min) = min(
        ((q, data) for q, data in rows.items() if q >= 7),
        key=lambda item: item[1][1],
    )

    assert rows[4][0] == rows[5][0] == 3
    assert 32 == 1 << (rows[4][0] + 2) == 1 << (rows[5][0] + 2)

    print(f"prime_power_limit={LIMIT}")
    print(f"prime_powers_checked={len(rows)}")
    print(f"smallest_q_ge_7_margin={margin_min} at_q={q_min}")
    print("exceptional_q=4,5 exact_cyc=32 threshold=32")


if __name__ == "__main__":
    main()
