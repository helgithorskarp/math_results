"""Separate full-period capacity arithmetic and first-appearance normalization.

This is an audit by the same researcher, not an independent reviewer verdict.
The reference capacity scans actual congruence classes modulo the entire L;
it uses neither the quotient gcd formula nor bit-sliced counters.
"""
from functools import lru_cache
from itertools import product
from math import prod
from pathlib import Path
import argparse
import json
import random
from time import monotonic
import cover_bound as fast


def prime_powers(m):
    """Independent trial division, returning (prime, maximal prime power)."""
    result = []
    for p in range(2, m + 1):
        if m % p:
            continue
        power = 1
        while m % p == 0:
            power *= p
            m //= p
        result.append((p, power))
        if m == 1:
            break
    return result


def normalize(previous):
    """Relabel the ORIGINAL children by first appearance and reconstruct CRT."""
    names, answer = {}, []
    for modulus, residue in previous:
        coordinates = []
        for p, maximal in prime_powers(modulus):
            power, encoded = 1, 0
            while power < maximal:
                original_prefix = residue % power
                key = p, power, original_prefix
                digit = residue // power % p
                labels = names.setdefault(key, {})
                if digit not in labels:
                    labels[digit] = len(labels)
                encoded += labels[digit] * power
                power *= p
            coordinates.append((maximal, encoded))
        reconstructed = next(a for a in range(modulus)
                             if all(a % q == b for q, b in coordinates))
        answer.append((modulus, reconstructed))
    return tuple(answer)


def reference_options(modulus, previous):
    for a in range(modulus):
        extended = previous + ((modulus, a),)
        if normalize(extended) == extended:
            yield a


@lru_cache(None)
def literal_classes(L, m):
    # A different mask builder, testing x % m directly.
    out = [0] * m
    for x in range(L):
        out[x % m] |= 1 << x
    return tuple(out)


def reference_bound(L, Q, U, remaining):
    # Lift the actual uncovered residues to the full period, rather than use
    # gcd(Q,m), lcm(Q,m), grouped weights, or a projected occupancy formula.
    lifted = 0
    for offset in range(0, L, Q):
        lifted |= U << offset
    result = L - lifted.bit_count()
    for m in remaining:
        best = 0
        # Each literal class has L/m points, so reaching that size is maximal.
        for mask in literal_classes(L, m):
            best = max(best, (lifted & mask).bit_count())
            if best == L // m:
                break
        result += best
    return result


def controls():
    counts = []
    for moduli in [(2, 3, 4), (3, 4, 5, 6, 10), (8, 9, 12), (8, 10, 12, 15)]:
        brute = {normalize(tuple(zip(moduli, a)))
                 for a in product(*(range(m) for m in moduli))}
        generated = set()
        def visit(i, seen, previous):
            if i == len(moduli):
                generated.add(previous)
                return
            m = moduli[i]
            for a, nxt in fast.canonical_options(m, seen):
                visit(i + 1, nxt, previous + ((m, a),))
        visit(0, {}, ())
        if brute != generated:
            raise RuntimeError('A symmetry orbit is missing or duplicated.')
        counts.append({'moduli': list(moduli), 'literal_tuples': prod(moduli),
                       'canonical_tuples': len(generated)})
    fibres, rng = 0, random.Random(20260929)
    for Q in range(1, 13):
        for U in range(1 << Q):
            for g in fast.divisors(Q):
                counts_by_phase = [0] * g
                for x in range(Q):
                    if U >> x & 1:
                        counts_by_phase[x % g] += 1
                if fast.maximum_fibre(U, Q, g) != max(counts_by_phase):
                    raise RuntimeError('The fibre maximum is incorrect.')
                fibres += 1
    projection_cases = 0
    for L in [12, 24, 60, 72, 120, 360]:
        for Q in fast.divisors(L):
            for _ in range(3):
                U = rng.getrandbits(Q)
                remaining = fast.divisors(L)
                formula = L - L // Q * U.bit_count() + sum(
                    L // fast.lcm(Q, m) * fast.maximum_fibre(U, Q, fast.gcd(Q, m))
                    for m in remaining)
                if formula != reference_bound(L, Q, U, remaining):
                    raise RuntimeError('Quotient capacity differs from literal coverage.')
                projection_cases += 1
    # Positive control: the classical distinct covering of period 12 exists.
    witness = [(2, 0), (3, 0), (4, 1), (6, 1), (12, 11)]
    if not all(any(x % m == a for m, a in witness) for x in range(12)):
        raise RuntimeError('Known witness failed.')
    positive = fast.search_case(12, [2, 3, 4], minimum=2)
    if positive['excludes']:
        raise RuntimeError('The bound incorrectly excludes a known cover.')
    # Independent divisibility scan checks every candidate, including equality.
    literal_candidates = []
    for L in range(8, 10080, 8):
        literal_divisors = [m for m in range(1, L + 1) if L % m == 0]
        if literal_divisors != fast.divisors(L):
            raise RuntimeError('A divisor was omitted or added.')
        if sum(L // m for m in literal_divisors if m >= 8) >= L:
            literal_candidates.append(L)
    if literal_candidates != fast.candidates():
        raise RuntimeError('The candidate sieve omitted an LCM.')
    return {'symmetry_controls': counts, 'fibre_cases': fibres,
            'literal_projection_cases': projection_cases,
            'positive_cover_checked': True, 'candidate_list_checked': True}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--full', action='store_true')
    p.add_argument('--expected', type=Path, default=Path(__file__).with_name('expected.json'))
    args = p.parse_args()
    start = monotonic()
    print(json.dumps(controls(), indent=2), flush=True)
    if args.full:
        actual = fast.prove(reference_bound, reference_options)
        if actual != json.loads(args.expected.read_text()):
            raise RuntimeError('Reference proof events differ from the production run.')
        print('FULL AUDIT PASSED: literal capacity, separate normalization, identical proof events.', flush=True)
    print(f'Elapsed seconds: {monotonic() - start:.3f}', flush=True)


if __name__ == '__main__':
    main()
