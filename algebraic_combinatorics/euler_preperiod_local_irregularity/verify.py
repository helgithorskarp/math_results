#!/usr/bin/env python3
"""Exact audit of the local irregularity classification.

The universal theorem is proved in THEOREM.md.  This checker independently
constructs Euler up/down residues from their differential recurrence,
Bernoulli residues from their defining recurrence, and selected Euler rows
from the Entringer triangle.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math


def odd_primes_through(bound: int) -> list[int]:
    if bound < 3:
        return []
    sieve = bytearray(b"\x01") * (bound + 1)
    sieve[:2] = b"\x00\x00"
    for q in range(2, math.isqrt(bound) + 1):
        if sieve[q]:
            count = (bound - q * q) // q + 1
            sieve[q * q : bound + 1 : q] = b"\x00" * count
    return [q for q in range(3, bound + 1, 2) if sieve[q]]


def zigzag_mod_ode(p: int, max_index: int | None = None) -> list[int]:
    """A_n mod p from y'=(y^2+1)/2, y=sec+tan."""
    if p % 2 == 0 or p < 3:
        raise ValueError("p must be an odd integer at least 3")
    if max_index is None:
        max_index = p - 1
    if max_index < 0:
        raise ValueError("max_index must be nonnegative")
    values = [1]
    binomial_row = [1]
    inv_two = (p + 1) // 2
    for n in range(max_index):
        convolution = sum(
            coefficient * values[k] * values[n - k]
            for k, coefficient in enumerate(binomial_row)
        ) % p
        if n == 0:
            convolution = (convolution + 1) % p
        values.append(convolution * inv_two % p)
        binomial_row = [1] + [
            (binomial_row[k - 1] + binomial_row[k]) % p
            for k in range(1, len(binomial_row))
        ] + [1]
    return values


def zigzag_mod_entringer(p: int, max_index: int) -> list[int]:
    """Independent Entringer-triangle construction of A_n mod p."""
    if max_index < 0:
        raise ValueError("max_index must be nonnegative")
    row = [1]
    values = [1]
    for n in range(1, max_index + 1):
        next_row = [0] * (n + 1)
        for k in range(1, n + 1):
            next_row[k] = (next_row[k - 1] + row[n - k]) % p
        row = next_row
        values.append(row[n])
    return values


def bernoulli_mod(p: int) -> list[int]:
    """B_0,...,B_(p-3) mod p from the defining binomial recurrence."""
    values = [1]
    binomial_row = [1, 1]  # C(1,k); advance to C(n+1,k) in the loop.
    for n in range(1, p - 2):
        binomial_row = [1] + [
            (binomial_row[k - 1] + binomial_row[k]) % p
            for k in range(1, len(binomial_row))
        ] + [1]
        subtotal = sum(binomial_row[k] * values[k] for k in range(n)) % p
        values.append(-subtotal * pow(n + 1, -1, p) % p)
    return values


def order_of_two(p: int) -> int:
    value = 1
    for order in range(1, p):
        value = 2 * value % p
        if value == 1:
            return order
    raise AssertionError("Fermat order not found")


def positive_residue(index: int, p: int) -> int:
    if index < 1:
        raise ValueError("index must be positive")
    return 1 + (index - 1) % (p - 1)


def irregular_data(
    p: int, zigzag: list[int], bernoulli: list[int]
) -> tuple[set[int], set[int], set[int], int, bool]:
    order = order_of_two(p)
    e_set = {j for j in range(2, p - 2, 2) if zigzag[j] == 0}
    b_set = {j for j in range(2, p - 2, 2) if bernoulli[j] == 0}
    o_set = {j for j in range(2, p - 2, 2) if j % order == 0}
    wieferich = pow(2, p - 1, p * p) == 1
    return e_set, b_set, o_set, order, wieferich


def predicted_triple_starts(
    p: int, zigzag: list[int], bernoulli: list[int]
) -> set[int]:
    if p == 3:
        return set()
    e_set, b_set, o_set, _, wieferich = irregular_data(
        p, zigzag, bernoulli
    )
    t_set = b_set | o_set
    starts: set[int] = set()

    for u in range(2, p - 4, 2):
        if u in e_set and u + 2 in e_set and u + 2 in t_set:
            starts.add(u)

    if p - 3 in e_set and wieferich and p % 4 == 1:
        starts.add(p - 3)

    for u in range(3, p - 5, 2):
        j = u + 1
        if j in e_set and j in t_set and j + 2 in t_set:
            starts.add(u)

    if p - 4 >= 3 and p - 3 in e_set and p - 3 in b_set and wieferich:
        starts.add(p - 4)

    return starts


def actual_triple_starts(p: int, zigzag: list[int]) -> set[int]:
    return {
        u
        for u in range(1, p)
        if all(zigzag[positive_residue(u + offset, p)] == 0 for offset in range(3))
    }


def consecutive_pair_starts(p: int, zigzag: list[int]) -> list[int]:
    return [
        u
        for u in range(1, p)
        if zigzag[u] == 0 and zigzag[positive_residue(u + 1, p)] == 0
    ]


def verify(bound: int = 1200) -> dict[str, object]:
    primes = odd_primes_through(bound)
    tangent_checks = 0
    cyclic_start_checks = 0
    boundary_checks = 0
    mixed_safe: list[int] = []
    triple_primes: dict[str, list[int]] = {}
    cache: dict[int, tuple[list[int], list[int]]] = {}

    for p in primes:
        zigzag = zigzag_mod_ode(p)
        bernoulli = bernoulli_mod(p)
        cache[p] = (zigzag, bernoulli)

        if p >= 5:
            for j in range(2, p - 2, 2):
                predicted_tangent_zero = bernoulli[j] == 0 or pow(2, j, p) == 1
                assert (zigzag[j - 1] == 0) == predicted_tangent_zero
                tangent_checks += 1
            assert (zigzag[p - 2] == 0) == (pow(2, p - 1, p * p) == 1)
            assert (zigzag[p - 1] == 0) == (p % 4 == 1)
            boundary_checks += 2

        actual = actual_triple_starts(p, zigzag)
        predicted = predicted_triple_starts(p, zigzag, bernoulli)
        assert actual == predicted
        cyclic_start_checks += p - 1
        if actual:
            triple_primes[str(p)] = sorted(actual)

        if p >= 5:
            e_set, b_set, _, _, _ = irregular_data(p, zigzag, bernoulli)
            if e_set and b_set and not actual:
                mixed_safe.append(p)

    independent_primes = [p for p in (3, 5, 7, 43, 67, 433, 1093) if p <= bound]
    shift_checks = 0
    for p in independent_primes:
        ode = zigzag_mod_ode(p, 2 * p - 2)
        entringer = zigzag_mod_entringer(p, 2 * p - 2)
        assert ode == entringer
        epsilon = -1 % p if p % 4 == 3 else 1
        for n in range(1, p):
            assert ode[n + p - 1] == epsilon * ode[n] % p
            shift_checks += 1

    strict_p = 67
    if strict_p <= bound:
        zigzag, bernoulli = cache[strict_p]
        e_set, b_set, _, order, wieferich = irregular_data(
            strict_p, zigzag, bernoulli
        )
        strict_example: dict[str, object] = {
            "p": strict_p,
            "e_irregular_indices": sorted(e_set),
            "b_irregular_indices": sorted(b_set),
            "order_of_two": order,
            "wieferich": wieferich,
            "triple_starts": sorted(actual_triple_starts(strict_p, zigzag)),
        }
    else:
        strict_example = {}

    pair_examples: dict[str, list[int]] = {}
    for p in (43, 433, 1093):
        if p <= bound:
            pair_examples[str(p)] = consecutive_pair_starts(p, cache[p][0])

    record: dict[str, object] = {
        "bound": bound,
        "odd_prime_count": len(primes),
        "tangent_identity_checks": tangent_checks,
        "boundary_identity_checks": boundary_checks,
        "cyclic_start_checks": cyclic_start_checks,
        "shift_checks": shift_checks,
        "independent_entringer_primes": independent_primes,
        "mixed_irregular_safe_primes": mixed_safe,
        "triple_residue_primes": triple_primes,
        "strict_example": strict_example,
        "consecutive_pair_examples": pair_examples,
        "arithmetic": "Python exact integers and finite-field inverses",
    }
    payload = json.dumps(record, sort_keys=True, separators=(",", ":"))
    record["record_sha256"] = hashlib.sha256(payload.encode()).hexdigest()
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bound", type=int, default=1200)
    args = parser.parse_args()
    if args.bound < 3:
        raise SystemExit("--bound must be at least 3")
    print(json.dumps(verify(args.bound), sort_keys=True, separators=(",", ":")))
    print("VERIFIED local irregularity classification")


if __name__ == "__main__":
    main()
