#!/usr/bin/env python3
"""Independent exact audit for the full-prime-fiber classification.

No target code or certificate is imported.  A root sum is tested by the exact
field trace of its squared norm, expressed through Ramanujan sums; this is a
different representation from reduction modulo cyclotomic polynomials.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter, defaultdict
from functools import cache
from math import gcd


def prime_factors(n):
    factors = []
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            factors.append(divisor)
            while n % divisor == 0:
                n //= divisor
        divisor += 1
    if n > 1:
        factors.append(n)
    return factors


@cache
def phi(n):
    value = n
    for prime in prime_factors(n):
        value -= value // prime
    return value


@cache
def mobius(n):
    sign = 1
    for prime in prime_factors(n):
        if n % (prime * prime) == 0:
            return 0
        sign = -sign
    return sign


@cache
def ramanujan(n, exponent):
    """Sum of zeta_n^(a*exponent) over units a modulo n."""
    common = gcd(n, exponent)
    quotient = n // common
    return mobius(quotient) * phi(n) // phi(quotient)


def trace_squared_norm(n, exponents):
    """Trace_Q(zeta_n)/Q of |sum zeta_n^e|^2, an exact integer."""
    exponents = tuple(exponent % n for exponent in exponents)
    value = sum(ramanujan(n, left - right)
                for left in exponents for right in exponents)
    if value < 0:
        raise AssertionError("a trace of conjugate squared magnitudes is negative")
    return value


def root_sum_zero(n, exponents):
    return trace_squared_norm(n, tuple(exponents)) == 0


def spectral_pair(n, p, points, frequencies):
    if len(points) != len(set(points)) or len(frequencies) != len(set(frequencies)):
        return False
    if len(points) != len(frequencies):
        return False
    modulus = n * p
    for (b, u), (c, v) in itertools.combinations(frequencies, 2):
        exponents = (p * a * (b - c) + n * j * (u - v) for a, j in points)
        if not root_sum_zero(modulus, exponents):
            return False
    return True


def cyclic_pair(n, points, frequencies):
    if len(points) != len(set(points)) or len(frequencies) != len(set(frequencies)):
        return False
    if len(points) != len(frequencies):
        return False
    return all(root_sum_zero(n, ((left - right) * point for point in points))
               for left, right in itertools.combinations(frequencies, 2))


@cache
def frequency_subsets(modulus, size):
    """All translated-normalized frequency sets; deliberately exhaustive."""
    return tuple((0, *tail)
                 for tail in itertools.combinations(range(1, modulus), size - 1))


def normalized_spectra(n, p, points):
    """Enumerate every spectrum translated to contain zero, with no clique search."""
    modulus, size = n * p, len(points)
    encoded = tuple((p * a + n * j) % modulus for a, j in points)
    zero_differences = {
        difference for difference in range(1, modulus)
        if root_sum_zero(modulus, (difference * point for point in encoded))
    }
    return [frequencies for frequencies in frequency_subsets(modulus, size)
            if all((left - right) % modulus in zero_differences
                   for left, right in itertools.combinations(frequencies, 2))]


def cyclic_spectra(n, points):
    if len(points) > n:
        return []
    zero_differences = {
        difference for difference in range(1, n)
        if root_sum_zero(n, (difference * point for point in points))
    }
    return [frequencies for frequencies in frequency_subsets(n, len(points))
            if all((left - right) % n in zero_differences
                   for left, right in itertools.combinations(frequencies, 2))]


def valuation_two(value):
    if value <= 0:
        raise ValueError("valuation representative must be positive")
    return (value & -value).bit_length() - 1


def normal_form(n, p, points):
    fiber = {(0, level) for level in range(p)}
    if len(points) != 2 * p or not fiber <= set(points):
        return None
    residual = set(points) - fiber
    if n % 2 or Counter(level for _, level in residual) != Counter(range(p)):
        return None
    valuations = {valuation_two(a) for a, _ in residual}
    if len(valuations) != 1:
        return None
    value = next(iter(valuations))
    return value if value < valuation_two(n) else None


def canonical_spectrum(n, p, valuation):
    step = n // (2 ** (valuation + 1))
    return [(first, level) for first in (0, step) for level in range(p)]


def complement(n, valuation):
    modulus = 2 ** (valuation + 1)
    return [(x, 0) for x in range(n) if x % modulus < modulus // 2]


def tiles(n, p, points, translations):
    sums = Counter(((a + x) % n, (j + y) % p)
                   for a, j in points for x, y in translations)
    return len(sums) == n * p and set(sums.values()) == {1}


def audit_small_full_fibers():
    cases = ((2, 3), (3, 2), (3, 5), (4, 3), (5, 2))
    rows, digest = [], hashlib.sha256()
    for n, p in cases:
        base_spectral_sets = sum(
            bool(cyclic_spectra(n, base))
            for base in itertools.combinations(range(n), p)
        )
        if base_spectral_sets:
            raise AssertionError("chosen census case violates the base hypothesis")

        fiber = tuple((0, level) for level in range(p))
        residual_universe = tuple((a, level) for a in range(1, n)
                                  for level in range(p))
        candidate_count = spectral_count = spectrum_count = selection_count = 0
        for residual in itertools.combinations(residual_universe, p):
            candidate_count += 1
            points = fiber + residual
            spectra = normalized_spectra(n, p, points)
            valuation = normal_form(n, p, points)
            if bool(spectra) != (valuation is not None):
                raise AssertionError("classification disagrees with exhaustive spectra")
            if not spectra:
                continue

            spectral_count += 1
            spectrum_count += len(spectra)
            if len({level for _, level in residual}) != p:
                raise AssertionError("positive residual is not a level graph")
            if not spectral_pair(n, p, points, canonical_spectrum(n, p, valuation)):
                raise AssertionError("displayed spectrum fails")
            if not tiles(n, p, points, complement(n, valuation)):
                raise AssertionError("displayed complement fails")

            for encoded_spectrum in spectra:
                frequencies = [(value % n, value % p) for value in encoded_spectrum]
                levels = defaultdict(list)
                for first, level in frequencies:
                    levels[level].append(first)
                if sorted(map(len, levels.values())) != [2] * p:
                    raise AssertionError("a spectrum does not have two points per level")
                for chosen in itertools.product(*(levels[level] for level in range(p))):
                    gamma = list(zip(chosen, range(p)))
                    if not spectral_pair(n, p, residual, gamma):
                        raise AssertionError("a deletion selection is not a spectrum")
                    selection_count += 1
            digest.update(repr((n, p, residual, valuation, len(spectra))).encode())

        rows.append({
            "n": n,
            "p": p,
            "candidate_sets": candidate_count,
            "spectral_sets": spectral_count,
            "normalized_spectra": spectrum_count,
            "all_spectrum_deletion_selections": selection_count,
            "base_spectral_sets_of_size_p": base_spectral_sets,
        })
    return rows, digest.hexdigest()


def audit_graph_dichotomy():
    tested = accepted = 0
    profiles = Counter()
    for n, p in ((2, 3), (3, 2), (4, 3)):
        universe = tuple(itertools.product(range(n), range(p)))
        for first_coordinates in itertools.product(range(n), repeat=p):
            gamma = list(zip(first_coordinates, range(p)))
            for points in itertools.combinations(universe, p):
                tested += 1
                if not spectral_pair(n, p, points, gamma):
                    continue
                accepted += 1
                level_count = len({level for _, level in points})
                if level_count not in (1, p):
                    raise AssertionError("graph-spectrum dichotomy fails")
                profiles[f"{n},{p}:levels={level_count}"] += 1
                if level_count == 1:
                    projected_points = [a for a, _ in points]
                    if not cyclic_pair(n, projected_points, list(first_coordinates)):
                        raise AssertionError("one-level projection is not spectral")

    noncoprime_points = [(0, 0), (1, 0), (1, 1)]
    noncoprime_frequencies = [(j, j) for j in range(3)]
    if not spectral_pair(3, 3, noncoprime_points, noncoprime_frequencies):
        raise AssertionError("claimed noncoprime control is not spectral")
    return {
        "candidate_pairs": tested,
        "spectral_pairs": accepted,
        "profile_counts": dict(sorted(profiles.items())),
        "noncoprime_counterexample_profile": [2, 1, 0],
    }


def audit_binary_congruence_and_halves():
    congruences = half_partitions = 0
    for n in range(2, 97, 2):
        exponent = valuation_two(n)
        for delta in range(1, n):
            for a in range(1, n):
                if delta * a % n != n // 2:
                    continue
                congruences += 1
                if valuation_two(delta) >= exponent:
                    raise AssertionError("delta valuation is outside the asserted range")
                if valuation_two(a) != exponent - 1 - valuation_two(delta):
                    raise AssertionError("binary valuation formula fails")
        for valuation in range(exponent):
            first_half = {x for x in range(n)
                          if x % (2 ** (valuation + 1)) < 2 ** valuation}
            for a in range(1, n):
                if valuation_two(a) != valuation:
                    continue
                half_partitions += 1
                second_half = {(x + a) % n for x in first_half}
                if first_half & second_half or first_half | second_half != set(range(n)):
                    raise AssertionError("binary half-translate partition fails")
    return {"congruence_solutions": congruences,
            "half_translate_partitions": half_partitions,
            "maximum_n": 96}


def audit_fixtures_and_controls():
    fixtures = []
    for n, p, valuation, offsets in (
        (8, 3, 0, [1, 3, 7]),
        (8, 3, 1, [2, 6, 2]),
        (12, 5, 0, [1, 5, 7, 11, 3]),
        (12, 5, 1, [2, 6, 10, 2, 6]),
        (210, 11, 0, list(range(1, 22, 2))),
    ):
        points = ([(0, level) for level in range(p)]
                  + list(zip(offsets, range(p))))
        spectrum = canonical_spectrum(n, p, valuation)
        translations = complement(n, valuation)
        if normal_form(n, p, points) != valuation:
            raise AssertionError("fixture does not have its asserted normal form")
        if not spectral_pair(n, p, points, spectrum):
            raise AssertionError("fixture spectrum fails")
        if not tiles(n, p, points, translations):
            raise AssertionError("fixture tiling fails")
        fixtures.append({"n": n, "p": p, "valuation": valuation,
                         "complement_size": len(translations)})

    mixed = ([(0, level) for level in range(3)]
             + [(1, 0), (2, 1), (3, 2)])
    repeated_level = ([(0, level) for level in range(3)]
                      + [(1, 0), (1, 1), (3, 1)])
    if normalized_spectra(4, 3, mixed):
        raise AssertionError("mixed-valuation control is unexpectedly spectral")
    if normalized_spectra(4, 3, repeated_level):
        raise AssertionError("repeated-level control is unexpectedly spectral")

    upper = ([(0, level) for level in range(5)]
             + [(4, level) for level in range(5)])
    if spectral_pair(12, 5, upper, canonical_spectrum(12, 5, 2)):
        raise AssertionError("upper-bound valuation has the proposed spectrum")

    return {
        "fixtures": fixtures,
        "rejected_controls": [
            "mixed valuations",
            "repeated residual level",
            "valuation equal to v2(n)",
            "noncoprime graph-spectrum dichotomy",
        ],
    }


def main():
    if not root_sum_zero(3, (0, 1, 2)):
        raise AssertionError("third-root control")
    if not root_sum_zero(8, (0, 4)):
        raise AssertionError("antipodal control")
    if root_sum_zero(5, (0, 1, 2)):
        raise AssertionError("nonzero root-sum control")

    censuses, digest = audit_small_full_fibers()
    report = {
        "schema": "independent-full-prime-fiber-review-v1",
        "root_zero_method": "Ramanujan-sum trace of squared norm",
        "reads_target_code_or_certificate": False,
        "small_full_fiber_censuses": censuses,
        "positive_case_digest_sha256": digest,
        "graph_spectrum_dichotomy": audit_graph_dichotomy(),
        "binary_arithmetic": audit_binary_congruence_and_halves(),
        "fixtures_and_controls": audit_fixtures_and_controls(),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
