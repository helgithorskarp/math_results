"""Exact computer-assisted proof that L_min(8) >= 10080.

Python >= 3.10, standard library only. See proof.md for completeness.
No published covering-system exclusion, solver, or floating point is used.
"""
from collections import defaultdict
from functools import lru_cache
from hashlib import sha256
from math import gcd, isqrt, lcm
import argparse
import json
from pathlib import Path
from time import monotonic


def divisors(n):
    result = set()
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            result.update((d, n // d))
    return sorted(result)


@lru_cache(None)
def factor_levels(m):
    result = []
    p, n = 2, m
    while p * p <= n:
        if n % p == 0:
            levels, power = [], 1
            while n % p == 0:
                levels.append(power)
                power *= p
                n //= p
            result.append((p, tuple(levels)))
        p += 1
    if n > 1:
        result.append((n, (1,)))
    return tuple(result)


@lru_cache(None)
def class_masks(period, modulus):
    if period % modulus:
        raise ValueError('The modulus must divide the period.')
    return tuple(sum(1 << x for x in range(a, period, modulus))
                 for a in range(modulus))


def maximum_fibre(uncovered, period, modulus):
    """Maximum population in one residue modulo modulus; exact integers."""
    if modulus * modulus <= period:
        return max((uncovered & mask).bit_count()
                   for mask in class_masks(period, modulus))
    low = (1 << modulus) - 1
    counters = []
    for shift in range(0, period, modulus):
        carry = (uncovered >> shift) & low
        level = 0
        while carry:
            if level == len(counters):
                counters.append(carry)
                break
            counters[level], carry = counters[level] ^ carry, counters[level] & carry
            level += 1
    possible, result = low, 0
    for level in reversed(range(len(counters))):
        intersection = possible & counters[level]
        if intersection:
            possible = intersection
            result |= 1 << level
    return result


def canonical_options(modulus, seen):
    """Name children 0,1,... at each prime-digit prefix on first appearance."""
    for residue in range(modulus):
        updates, valid = {}, True
        for p, levels in factor_levels(modulus):
            for power in levels:
                key = p, power, residue % power
                child = residue // power % p
                count = seen.get(key, 0)
                if child >= min(p, count + 1):
                    valid = False
                    break
                updates[key] = max(count, child + 1)
            if not valid:
                break
        if valid:
            next_seen = seen.copy()
            next_seen.update(updates)
            yield residue, next_seen


def search_case(L, anchors, minimum=8, prune=False,
                reference_bound=None, reference_options=None):
    """Exhaust every canonical anchor branch, or prune by a proved upper bound.

    There is no timeout or incomplete-success return. An interrupted process
    produces no completed result. Callbacks enable the separate arithmetic and
    canonicalization implementations in audit.py.
    """
    anchors = tuple(anchors)
    if not anchors or len(anchors) != len(set(anchors)):
        raise ValueError('Need a nonempty tuple of distinct anchors.')
    if any(m < minimum or L % m for m in anchors):
        raise ValueError('Every anchor must be an eligible divisor of L.')
    Q = lcm(*anchors)
    moduli = [m for m in divisors(L) if m >= minimum]
    remaining_by_depth, weights_by_depth = [], []
    for depth in range(len(anchors) + 1):
        remaining = [m for m in moduli if m not in anchors[:depth]]
        remaining_by_depth.append(remaining)
        weights = defaultdict(int)
        for m in remaining:
            weights[gcd(m, Q)] += L // lcm(m, Q)
        weights_by_depth.append(sorted(weights.items()))
    nodes = [0] * (len(anchors) + 1)
    pruned, leaves, upper = 0, 0, -1
    digest = sha256()

    def score(U, depth):
        if reference_bound is not None:
            return reference_bound(L, Q, U, remaining_by_depth[depth])
        return L - L // Q * U.bit_count() + sum(
            w * maximum_fibre(U, Q, g) for g, w in weights_by_depth[depth])

    def record(tag, residues, value):
        digest.update((json.dumps([tag, residues, value], separators=(',', ':'))
                       + '\n').encode('ascii'))

    def visit(depth, U, seen, residues):
        nonlocal pruned, leaves, upper
        nodes[depth] += 1
        if prune and depth >= 2:
            value = score(U, depth)
            if value < L:
                pruned += 1
                upper = max(upper, value)
                record('cut', residues, value)
                return
        if depth == len(anchors):
            leaves += 1
            value = score(U, depth)
            upper = max(upper, value)
            record('leaf', residues, value)
            return
        m = anchors[depth]
        if reference_options is None:
            choices = canonical_options(m, seen)
        else:
            previous = tuple(zip(anchors[:depth], residues))
            choices = ((a, None) for a in reference_options(m, previous))
        for a, next_seen in choices:
            visit(depth + 1, U & ~class_masks(Q, m)[a], next_seen, residues + (a,))

    visit(0, (1 << Q) - 1, {}, ())
    if upper < 0:
        raise RuntimeError('No terminal proof event was reached.')
    return {'L': L, 'anchors': list(anchors), 'Q': Q, 'upper': upper,
            'excludes': upper < L, 'nodes': nodes, 'pruned': pruned,
            'leaves': leaves, 'proof_events_sha256': digest.hexdigest()}


SPECIAL = {
    5040: ([8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 24, 28, 30, 35, 36], True),
    7560: ([8, 9, 10, 12, 14, 15, 18, 20, 21, 24, 27, 28], True),
    7920: ([8, 9, 10, 11, 12, 15, 16], False),
    9240: ([8, 10, 11, 12, 14, 15], False),
    9360: ([8, 9, 10, 12, 13, 15], False),
}


def anchors_for(L):
    return SPECIAL.get(L, ([m for m in [8, 9, 10, 12, 15] if L % m == 0], False))


def candidates():
    """All multiples of 8 below 10080 surviving the elementary union bound."""
    return [L for L in range(8, 10080, 8)
            if sum(L // d for d in divisors(L) if d >= 8) >= L]


def prove(reference_bound=None, reference_options=None):
    results = []
    for L in candidates():
        anchors, prune = anchors_for(L)
        result = search_case(L, anchors, prune=prune,
                             reference_bound=reference_bound,
                             reference_options=reference_options)
        if not result['excludes']:
            raise RuntimeError(f'No exclusion established at L={L}: {result}')
        print(f'L={L} upper={result["upper"]} nodes={sum(result["nodes"])}', flush=True)
        results.append(result)
    return {'agent': 'six-covering-2', 'role': 'researcher',
            'claim': 'L_min(8) >= 10080, minimum exactly eight',
            'multiples_checked': 1259, 'union_bound_exclusions': 1259 - len(results),
            'candidates': results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', type=Path)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    start = monotonic()
    result = prove()
    if args.check is not None:
        expected = json.loads(args.check.read_text())
        if result != expected:
            raise RuntimeError('The complete result differs from expected.json.')
    if args.write is not None:
        args.write.write_text(json.dumps(result, indent=2) + '\n')
    print('PROVED L_min(8) >= 10080; all 17 candidate LCMs excluded.', flush=True)
    print(f'Elapsed seconds: {monotonic() - start:.3f}', flush=True)


if __name__ == '__main__':
    main()
