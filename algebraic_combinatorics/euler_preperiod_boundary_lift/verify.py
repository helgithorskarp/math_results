#!/usr/bin/env python3
"""Definition-level audit of the Euler boundary-lift valuation theorem."""

from __future__ import annotations

import argparse
import json
import math


def primes_through(limit: int) -> list[int]:
    sieve = [True] * (limit + 1)
    if limit >= 0:
        sieve[0] = False
    if limit >= 1:
        sieve[1] = False
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            for multiple in range(p * p, limit + 1, p):
                sieve[multiple] = False
    return [p for p in range(3, limit + 1, 2) if sieve[p]]


def valuation(value: int, prime: int) -> int:
    if value == 0:
        raise ValueError("valuation of zero is not finite")
    result = 0
    while value % prime == 0:
        value //= prime
        result += 1
    return result


def euler_up_down_through(limit: int) -> list[int]:
    """Return A_0,...,A_limit using the Entringer triangle."""
    row = [1]
    values = [1]
    for n in range(1, limit + 1):
        new_row = [0] * (n + 1)
        for k in range(1, n + 1):
            new_row[k] = new_row[k - 1] + row[n - k]
        row = new_row
        values.append(row[n])
    if values[:10] != [1, 1, 1, 2, 5, 16, 61, 272, 1385, 7936]:
        raise RuntimeError("Entringer normalization check failed")
    return values


def wieferich_order(prime: int) -> int:
    return valuation((1 << (prime - 1)) - 1, prime)


def second_fermat_quotient_mod_p(prime: int) -> int:
    residue = pow(2, prime - 1, prime**3)
    if (residue - 1) % (prime * prime):
        raise RuntimeError(f"{prime} is not base-two Wieferich")
    return ((residue - 1) // (prime * prime)) % prime


def run(max_index: int) -> dict[str, object]:
    if max_index < 1091:
        raise ValueError("max-index must be at least 1091 for the spot check")
    values = euler_up_down_through(max_index)
    primes = primes_through(max_index + 1)

    instances = 0
    quotient_divisible = 0
    maximum_q = 0
    wieferich_in_range: list[int] = []
    for p in primes:
        w_p = wieferich_order(p)
        if w_p >= 2:
            wieferich_in_range.append(p)
        q = 1
        while q * (p - 1) - 1 <= max_index:
            index = q * (p - 1) - 1
            observed = valuation(values[index], p)
            predicted = w_p - 1
            if observed != predicted:
                raise RuntimeError(
                    f"valuation mismatch p={p} q={q}: "
                    f"observed={observed} predicted={predicted}"
                )
            instances += 1
            quotient_divisible += int(q % p == 0)
            maximum_q = max(maximum_q, q)
            q += 1

    spot_checks = []
    for p in (1093, 3511):
        w_p = wieferich_order(p)
        if w_p != 2:
            raise RuntimeError(f"unexpected Wieferich order for {p}: {w_p}")
        spot_checks.append(
            {
                "p": p,
                "second_fermat_quotient_mod_p": second_fermat_quotient_mod_p(p),
                "w_p": w_p,
            }
        )

    direct_1093 = valuation(values[1091], 1093)
    if direct_1093 != 1:
        raise RuntimeError(f"unexpected v_1093(A_1091): {direct_1093}")

    return {
        "direct_entringer_audit": {
            "max_index": max_index,
            "maximum_q": maximum_q,
            "odd_primes": len(primes),
            "quotient_divisible_by_p_instances": quotient_divisible,
            "valuation_instances": instances,
            "wieferich_primes_in_range": wieferich_in_range,
        },
        "spot_checks": spot_checks,
        "v_1093_A_1091": direct_1093,
        "status": "PASS",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-index", type=int, default=1200)
    args = parser.parse_args()
    print(json.dumps(run(args.max_index), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
