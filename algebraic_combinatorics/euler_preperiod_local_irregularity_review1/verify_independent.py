#!/usr/bin/env python3
"""Independent exact audit of the local Euler-zero classification.

This checker deliberately avoids the target's differential recurrence and
Bernoulli recurrence.  Euler up/down residues are recovered from

    sec(z) cos(z) = 1,       tan(z) cos(z) = sin(z),

and exact Bernoulli numbers are produced by the Akiyama--Tanigawa transform.
All checks use explicit failures, rather than Python ``assert`` statements,
so they remain active under ``python -O``.
"""

from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction


BOUND = 1093


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def odd_primes_through(bound: int) -> list[int]:
    sieve = bytearray(b"\x01") * (bound + 1)
    if bound >= 0:
        sieve[0] = 0
    if bound >= 1:
        sieve[1] = 0
    for q in range(2, math.isqrt(bound) + 1):
        if sieve[q]:
            sieve[q * q : bound + 1 : q] = b"\x00" * (
                (bound - q * q) // q + 1
            )
    return [p for p in range(3, bound + 1, 2) if sieve[p]]


def zigzag_mod_trig(modulus: int, max_index: int) -> list[int]:
    """Compute A_n modulo ``modulus`` from two reciprocal trig identities.

    Even coefficients are obtained from sec(z)cos(z)=1 and odd coefficients
    from tan(z)cos(z)=sin(z), all in exponential-generating-function form.
    This is structurally separate from the target's ODE and Entringer routes.
    """
    require(modulus >= 2, "modulus must be at least two")
    require(max_index >= 0, "max_index must be nonnegative")
    values = [1]
    binomial_row = [1]
    for n in range(1, max_index + 1):
        binomial_row = [1] + [
            (binomial_row[k - 1] + binomial_row[k]) % modulus
            for k in range(1, n)
        ] + [1]
        known_part = 0
        sign = -1
        for k in range(2, n + 1, 2):
            known_part += sign * binomial_row[k] * values[n - k]
            sign = -sign
        right_side = 0 if n % 2 == 0 else (-1) ** ((n - 1) // 2)
        values.append((right_side - known_part) % modulus)
    return values


def bernoulli_exact(max_index: int) -> list[Fraction]:
    """Akiyama--Tanigawa transform (with B_1=+1/2; even terms standard)."""
    work = [Fraction(0)] * (max_index + 1)
    values: list[Fraction] = []
    for m in range(max_index + 1):
        work[m] = Fraction(1, m + 1)
        for j in range(m, 0, -1):
            work[j - 1] = j * (work[j - 1] - work[j])
        values.append(work[0])
    return values


def order_of_two(p: int) -> int:
    value = 1
    for order in range(1, p):
        value = 2 * value % p
        if value == 1:
            return order
    raise RuntimeError(f"no multiplicative order found for p={p}")


def rho(index: int, p: int) -> int:
    require(index >= 1, "positive-residue reduction requires a positive index")
    return 1 + (index - 1) % (p - 1)


def irregular_sets(
    p: int, zigzag: list[int], bernoulli: list[Fraction]
) -> tuple[set[int], set[int], set[int], bool]:
    order = order_of_two(p)
    even_indices = range(2, p - 2, 2)
    e_set = {j for j in even_indices if zigzag[j] % p == 0}
    b_set = {
        j for j in range(2, p - 2, 2) if bernoulli[j].numerator % p == 0
    }
    o_set = {j for j in range(2, p - 2, 2) if j % order == 0}
    wieferich = pow(2, p - 1, p * p) == 1
    return e_set, b_set, o_set, wieferich


def actual_run_starts(p: int, zigzag: list[int], length: int) -> set[int]:
    return {
        u
        for u in range(1, p)
        if all(zigzag[rho(u + t, p)] % p == 0 for t in range(length))
    }


def predicted_triples(
    p: int, e_set: set[int], b_set: set[int], o_set: set[int], wieferich: bool
) -> set[int]:
    if p == 3:
        return set()
    t_set = b_set | o_set
    starts: set[int] = set()
    for u in range(2, p - 4, 2):
        if u in e_set and u + 2 in e_set and u + 2 in t_set:
            starts.add(u)
    if p % 4 == 1 and p - 3 in e_set and wieferich:
        starts.add(p - 3)
    for u in range(3, p - 5, 2):
        j = u + 1
        if j in e_set and j in t_set and j + 2 in t_set:
            starts.add(u)
    if p - 3 in e_set and p - 3 in b_set and wieferich:
        starts.add(p - 4)
    return starts


def predicted_pairs(
    p: int, e_set: set[int], b_set: set[int], o_set: set[int], wieferich: bool
) -> set[int]:
    """Four-class pair theorem proved in REVIEW.md."""
    if p == 3:
        return set()
    t_set = b_set | o_set
    starts: set[int] = set()
    for u in range(2, p - 4, 2):
        if u in e_set and u + 2 in t_set:
            starts.add(u)
    if p - 3 in e_set and wieferich:
        starts.add(p - 3)
    for u in range(3, p - 3, 2):
        j = u + 1
        if j in e_set and j in t_set:
            starts.add(u)
    if p % 4 == 1 and wieferich:
        starts.add(p - 2)
    return starts


def verify() -> dict[str, object]:
    primes = odd_primes_through(BOUND)
    bernoulli = bernoulli_exact(BOUND - 3)
    require(
        zigzag_mod_trig(1_000_000_007, 6) == [1, 1, 1, 2, 5, 16, 61],
        "reciprocal-trigonometric construction failed its defining prefix",
    )
    require(
        bernoulli[2] == Fraction(1, 6)
        and bernoulli[4] == Fraction(-1, 30)
        and bernoulli[6] == Fraction(1, 42),
        "Akiyama-Tanigawa construction failed its defining prefix",
    )
    triple_checks = 0
    pair_checks = 0
    tangent_checks = 0
    endpoint_checks = 0
    triple_primes: dict[str, list[int]] = {}
    pair_examples: dict[str, list[int]] = {}
    cyclic_boundaries: dict[str, dict[str, list[int]]] = {}
    cache: dict[int, list[int]] = {}

    for p in primes:
        # Working modulo p^2 independently tests both the classification and
        # the first two endpoint-valuation levels.
        zigzag_lift = zigzag_mod_trig(p * p, p - 1)
        zigzag = [value % p for value in zigzag_lift]
        cache[p] = zigzag
        if p == 3:
            e_set: set[int] = set()
            b_set: set[int] = set()
            o_set: set[int] = set()
            wieferich = False
        else:
            e_set, b_set, o_set, wieferich = irregular_sets(
                p, zigzag, bernoulli
            )
            t_set = b_set | o_set
            for j in range(2, p - 2, 2):
                require(
                    (zigzag[j - 1] == 0) == (j in t_set),
                    f"interior tangent predicate failed at p={p}, j={j}",
                )
                tangent_checks += 1
            require(
                (zigzag_lift[p - 2] % p == 0)
                == (pow(2, p - 1, p * p) == 1),
                f"first endpoint valuation level failed at p={p}",
            )
            require(
                (zigzag_lift[p - 2] % (p * p) == 0)
                == (pow(2, p - 1, p**3) == 1),
                f"second endpoint valuation level failed at p={p}",
            )
            require(
                (zigzag[p - 1] == 0) == (p % 4 == 1),
                f"secant endpoint predicate failed at p={p}",
            )
            endpoint_checks += 3

        actual_triples = actual_run_starts(p, zigzag, 3)
        classified_triples = predicted_triples(
            p, e_set, b_set, o_set, wieferich
        )
        require(
            actual_triples == classified_triples,
            f"triple classification failed at p={p}",
        )
        triple_checks += p - 1
        if actual_triples:
            triple_primes[str(p)] = sorted(actual_triples)

        actual_pairs = actual_run_starts(p, zigzag, 2)
        classified_pairs = predicted_pairs(p, e_set, b_set, o_set, wieferich)
        require(
            actual_pairs == classified_pairs,
            f"pair classification failed at p={p}",
        )
        pair_overlap_triples = {
            u for u in actual_pairs if rho(u + 1, p) in actual_pairs
        }
        require(
            actual_triples == pair_overlap_triples,
            f"pair-overlap completeness failed at p={p}",
        )
        pair_checks += p - 1
        if p in (43, 433, 1093):
            pair_examples[str(p)] = sorted(actual_pairs)

        if p in (3, 5, 7, 67, 1093):
            starts = [u for u in range(max(1, p - 4), p)]
            cyclic_boundaries[str(p)] = {
                str(u): [
                    int(zigzag[rho(u + t, p)] == 0) for t in range(3)
                ]
                for u in starts
            }

    # A second period is computed only for selected adversarial primes.  The
    # shift follows here from the reciprocal trig construction, not the
    # target's frequency-expansion implementation.
    shift_checks = 0
    for p in (3, 5, 7, 43, 67, 1093):
        extended = zigzag_mod_trig(p, 2 * p - 2)
        epsilon = 1 if p % 4 == 1 else p - 1
        for n in range(1, p):
            require(
                extended[n + p - 1] == epsilon * extended[n] % p,
                f"frequency shift failed at p={p}, n={n}",
            )
            shift_checks += 1

    e67, b67, o67, w67 = irregular_sets(67, cache[67], bernoulli)
    require(e67 == {26}, "unexpected E_67")
    require(b67 == {58}, "unexpected B_67")
    require(o67 == set(), "unexpected O_67")
    require(not w67, "67 unexpectedly Wieferich")

    record: dict[str, object] = {
        "bound": BOUND,
        "odd_prime_count": len(primes),
        "arithmetic": "exact Fraction and modular integer arithmetic",
        "euler_method": "sec*cos=1 and tan*cos=sin",
        "bernoulli_method": "Akiyama-Tanigawa exact transform",
        "tangent_predicate_checks": tangent_checks,
        "endpoint_lift_checks": endpoint_checks,
        "triple_start_checks": triple_checks,
        "pair_start_checks": pair_checks,
        "shift_checks": shift_checks,
        "triple_residue_primes": triple_primes,
        "pair_examples": pair_examples,
        "strict_example_67": {
            "E": sorted(e67),
            "B": sorted(b67),
            "O": sorted(o67),
            "wieferich": w67,
        },
        "cyclic_boundary_zero_bits": cyclic_boundaries,
    }
    payload = json.dumps(record, sort_keys=True, separators=(",", ":"))
    record["record_sha256"] = hashlib.sha256(payload.encode()).hexdigest()
    return record


def main() -> None:
    print(json.dumps(verify(), sort_keys=True, separators=(",", ":")))
    print("VERIFIED independent triple audit and pair refinement")


if __name__ == "__main__":
    main()
