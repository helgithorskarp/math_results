#!/usr/bin/env python3
"""Exact audit for the regular-residue Euler up/down lift theorem.

The universal theorem is proved in THEOREM.md.  This script computes Euler
up/down numbers from the Entringer triangle, independently of Bernoulli and
tangent formulas, and checks a finite adversarial sample modulo p^6.
"""

from __future__ import annotations

import json
from math import comb, isqrt


VALUATION_CAP = 6
BASE_Q_VALUES = (0, 1, 2, 3, 5, 8)


def primes_up_to(limit: int) -> list[int]:
    if limit < 3:
        return []
    result: list[int] = []
    for candidate in range(3, limit + 1, 2):
        if all(candidate % divisor for divisor in range(3, isqrt(candidate) + 1, 2)):
            result.append(candidate)
    return result


def valuation(value: int, prime: int) -> int:
    """Return v_prime(value) for a nonzero integer."""
    if value == 0:
        raise ValueError("valuation(0) is not finite")
    answer = 0
    while value % prime == 0:
        answer += 1
        value //= prime
    return answer


def valuation_from_residue(residue: int, prime: int, cap: int) -> int:
    """Recover a valuation below cap from a residue modulo prime**cap."""
    if not 0 <= residue < prime**cap:
        raise ValueError("residue outside its declared modulus")
    if residue == 0:
        return cap
    return valuation(residue, prime)


def order_of_two(prime: int) -> int:
    value = 1
    for order in range(1, prime):
        value = (2 * value) % prime
        if value == 1:
            return order
    raise AssertionError("Fermat bound failed")


def bernoulli_mod_prime(prime: int) -> list[int]:
    """Return B_0,...,B_(p-3) in F_p via the defining recurrence."""
    values = [0] * (prime - 2)
    values[0] = 1
    for n in range(1, prime - 2):
        total = sum(comb(n + 1, k) * values[k] for k in range(n)) % prime
        values[n] = (-total * pow(n + 1, -1, prime)) % prime
    return values


def entringer_targets_mod(targets: set[int], modulus: int) -> dict[int, int]:
    """Compute selected A_n modulo modulus by the Entringer triangle.

    If the preceding row is e(n-1,0),...,e(n-1,n-1), then the next row
    starts at zero and its remaining entries are cumulative sums of the
    preceding row in reverse order.  The last entry is A_n.
    """
    if not targets:
        return {}
    if min(targets) < 0:
        raise ValueError("negative Euler index")
    row = [1]
    result: dict[int, int] = {}
    if 0 in targets:
        result[0] = 1 % modulus
    for n in range(1, max(targets) + 1):
        running = 0
        next_row = [0]
        for entry in reversed(row):
            running = (running + entry) % modulus
            next_row.append(running)
        row = next_row
        if n in targets:
            result[n] = row[-1]
    if result.keys() != targets:
        raise AssertionError("not every requested Euler number was produced")
    return result


def predicted_valuation(prime: int, residue_index: int, m: int) -> int:
    order = order_of_two(prime)
    if residue_index % order:
        return 0
    wieferich_order = valuation(pow(2, prime - 1) - 1, prime)
    return wieferich_order + valuation(m, prime) if m % prime == 0 else wieferich_order


def audit_small_primes(limit: int = 97) -> tuple[dict[str, int], list[dict[str, object]]]:
    counts = {
        "formula_cases": 0,
        "zero_valuation_cases": 0,
        "order_only_cases": 0,
        "p_divides_m_cases": 0,
        "p_squared_divides_m_cases": 0,
    }
    nonempty_order_profiles: list[dict[str, object]] = []

    for prime in primes_up_to(limit):
        bernoulli = bernoulli_mod_prime(prime)
        order = order_of_two(prime)
        wieferich_order = valuation(pow(2, prime - 1) - 1, prime)
        cases: set[tuple[int, int]] = set()

        for j in range(2, prime - 2, 2):
            if bernoulli[j] != 0:
                cases.update((j, q) for q in BASE_Q_VALUES)

        order_residues = [
            j
            for j in range(2, prime - 2, 2)
            if bernoulli[j] != 0 and j % order == 0
        ]
        # q=j gives m=jp and explicitly exercises the v_p(m) correction.
        cases.update((j, j) for j in order_residues)

        # At p=17,j=8, q=j(p+1) gives m=jp^2 and exercises v_p(m)=2.
        if prime == 17:
            cases.add((8, 8 * (prime + 1)))

        targets = {j + q * (prime - 1) - 1 for j, q in cases}
        values = entringer_targets_mod(targets, prime**VALUATION_CAP)

        for j, q in sorted(cases):
            m = j + q * (prime - 1)
            actual = valuation_from_residue(values[m - 1], prime, VALUATION_CAP)
            predicted = predicted_valuation(prime, j, m)
            if predicted >= VALUATION_CAP:
                raise AssertionError("audit cap is too small")
            if actual != predicted:
                raise AssertionError((prime, j, q, m, actual, predicted))
            counts["formula_cases"] += 1
            if predicted == 0:
                counts["zero_valuation_cases"] += 1
            else:
                counts["order_only_cases"] += 1
            m_valuation = valuation(m, prime) if m % prime == 0 else 0
            if m_valuation >= 1:
                counts["p_divides_m_cases"] += 1
            if m_valuation >= 2:
                counts["p_squared_divides_m_cases"] += 1

        if order_residues:
            nonempty_order_profiles.append(
                {
                    "prime": prime,
                    "ord_p_2": order,
                    "w_p": wieferich_order,
                    "regular_order_residues": order_residues,
                }
            )

    return counts, nonempty_order_profiles


def audit_wieferich_prime() -> dict[str, object]:
    prime = 1093
    bernoulli = bernoulli_mod_prime(prime)
    order = order_of_two(prime)
    wieferich_order = valuation(pow(2, prime - 1) - 1, prime)
    residues = [
        j
        for j in range(2, prime - 2, 2)
        if bernoulli[j] != 0 and j % order == 0
    ]
    if residues != [364, 728] or wieferich_order != 2:
        raise AssertionError("unexpected 1093 control data")

    cases = [(j, q) for j in residues for q in (0, 1)]
    boundary_index = prime - 2
    targets = {j + q * (prime - 1) - 1 for j, q in cases} | {boundary_index}
    values = entringer_targets_mod(targets, prime**VALUATION_CAP)
    valuations: dict[str, int] = {}
    for j, q in cases:
        m = j + q * (prime - 1)
        actual = valuation_from_residue(values[m - 1], prime, VALUATION_CAP)
        predicted = predicted_valuation(prime, j, m)
        if actual != predicted:
            raise AssertionError((prime, j, q, actual, predicted))
        valuations[f"j={j},q={q}"] = actual

    boundary_valuation = valuation_from_residue(
        values[boundary_index], prime, VALUATION_CAP
    )
    if boundary_valuation != wieferich_order - 1:
        raise AssertionError("boundary theorem control failed")
    return {
        "prime": prime,
        "ord_p_2": order,
        "w_p": wieferich_order,
        "regular_order_residues": residues,
        "interior_valuations": valuations,
        "boundary_v_p_A_p_minus_2": boundary_valuation,
    }


def audit_irregular_boundary() -> dict[str, int]:
    prime = 37
    j = 32
    bernoulli = bernoulli_mod_prime(prime)
    if bernoulli[j] != 0:
        raise AssertionError("(37,32) should be an irregular pair")
    value = entringer_targets_mod({j - 1}, prime**4)[j - 1]
    actual = valuation_from_residue(value, prime, 4)
    cyclotomic = valuation(pow(2, j) - 1, prime) if (pow(2, j) - 1) % prime == 0 else 0
    if actual != 1 or cyclotomic != 0:
        raise AssertionError("irregular sharpness control failed")
    return {
        "prime": prime,
        "j": j,
        "v_p_A_j_minus_1": actual,
        "v_p_2_to_j_minus_1": cyclotomic,
    }


def run_audit() -> dict[str, object]:
    counts, profiles = audit_small_primes()
    wieferich = audit_wieferich_prime()
    counts["formula_cases"] += len(wieferich["interior_valuations"])
    counts["order_only_cases"] += len(wieferich["interior_valuations"])
    return {
        "status": "PASS",
        "method": "Entringer triangle modulo p^6; Bernoulli residues from their defining recurrence",
        "small_prime_limit": 97,
        "valuation_cap": VALUATION_CAP,
        "counts": counts,
        "nonempty_regular_order_profiles_through_97": profiles,
        "wieferich_control": wieferich,
        "excluded_irregular_control": audit_irregular_boundary(),
    }


if __name__ == "__main__":
    print(json.dumps(run_audit(), indent=2, sort_keys=True))
