#!/usr/bin/env python3
"""Audit finite instances of the irregularity obstructions in README.md.

This uses only exact arithmetic modulo each prime.  It is supplementary to
the proof: finite verification cannot establish the quantified theorem.
"""

from __future__ import annotations

import argparse


def primes_up_to(bound: int) -> list[int]:
    sieve = bytearray(b"\x01") * (bound + 1)
    if bound >= 0:
        sieve[0] = 0
    if bound >= 1:
        sieve[1] = 0
    for q in range(2, int(bound**0.5) + 1):
        if sieve[q]:
            sieve[q * q : bound + 1 : q] = b"\x00" * (
                (bound - q * q) // q + 1
            )
    return [p for p in range(3, bound + 1, 2) if sieve[p]]


def up_down_mod(p: int, last_index: int) -> list[int]:
    """Return A_0,...,A_last_index modulo p via Entringer's triangle."""
    previous = [1]
    values = [1]
    for n in range(1, last_index + 1):
        row = [0] * (n + 1)
        running = 0
        for j in range(1, n + 1):
            running = (running + previous[n - j]) % p
            row[j] = running
        values.append(row[n])
        previous = row
    return values


def bernoulli_mod(p: int) -> list[int]:
    """Return B_0,...,B_(p-3) in F_p (all denominators are invertible)."""
    last = p - 3
    bernoulli = [0] * (last + 1)
    bernoulli[0] = 1
    # Sum_{j=0}^m binom(m+1,j) B_j = 0 for m >= 1.
    for m in range(1, last + 1):
        binomial = 1
        total = 0
        for j in range(m):
            total = (total + binomial * bernoulli[j]) % p
            binomial = binomial * (m + 1 - j) * pow(j + 1, -1, p) % p
        bernoulli[m] = -total * pow(m + 1, -1, p) % p
    return bernoulli


def audit_prime(p: int) -> tuple[bool, bool, int]:
    values = up_down_mod(p, 2 * (p - 1) + 2)
    sign = 1 if p % 4 == 1 else -1

    for n in range(1, p + 2):
        assert values[n + p - 1] == sign * values[n] % p
    expected_boundary = 0 if p % 4 == 1 else p - 2
    assert values[p - 1] == expected_boundary

    e_irregular = {
        ell for ell in range(2, p - 2, 2) if values[ell] == 0
    }
    bernoulli = bernoulli_mod(p)
    b_irregular = {
        ell for ell in range(2, p - 2, 2) if bernoulli[ell] == 0
    }

    triples = 0
    for n in range(1, p):
        if values[n] or values[n + 1] or values[n + 2]:
            continue
        triples += 1
        r_parity = (n + 3) % 2
        if r_parity == 0:  # odd--even--odd
            ell = (n + 1) % (p - 1)
            assert ell in e_irregular
            assert b_irregular
        else:  # even--odd--even
            ell = n % (p - 1)
            if ell <= p - 5:
                assert ell in e_irregular and ell + 2 in e_irregular
            else:
                assert ell == p - 3 and ell in e_irregular and p % 4 == 1

    return not e_irregular, not b_irregular, triples


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bound", type=int, default=200)
    parser.add_argument("--wieferich-demo", action="store_true")
    args = parser.parse_args()
    if args.bound < 3:
        parser.error("--bound must be at least 3")

    count = e_regular = b_regular = triple_count = 0
    for p in primes_up_to(args.bound):
        is_e_regular, is_b_regular, triples = audit_prime(p)
        count += 1
        e_regular += is_e_regular
        b_regular += is_b_regular
        triple_count += triples

    print(f"audited {count} odd primes p <= {args.bound}")
    print(f"E-regular: {e_regular}; B-regular: {b_regular}")
    print(f"three-term zero classes found: {triple_count}")

    if args.wieferich_demo:
        p = 1093
        values = up_down_mod(p, 1093)
        residues = [(n, values[n]) for n in range(1091, 1094)]
        assert residues == [(1091, 0), (1092, 0), (1093, 1)]
        assert pow(2, p - 1, p * p) == 1
        print(f"p={p} Wieferich demo: {residues}")


if __name__ == "__main__":
    main()
