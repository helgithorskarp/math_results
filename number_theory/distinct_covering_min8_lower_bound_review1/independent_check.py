"""Independent exact audit of the minimum-eight LCM lower bound.

No target module is imported. Symmetry uses pairwise p-adic agreement,
and capacity is counted in literal congruence classes over the full period.
Python >= 3.10, standard library only; see README.md for the proof boundary.
"""
import argparse
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import permutations, product
import json
from math import gcd
from pathlib import Path
from time import monotonic
import resource


SPECIAL = {
    5040: (8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 24, 28, 30, 35, 36),
    7560: (8, 9, 10, 12, 14, 15, 18, 20, 21, 24, 27, 28),
    7920: (8, 9, 10, 11, 12, 15, 16),
    9240: (8, 10, 11, 12, 14, 15),
    9360: (8, 9, 10, 12, 13, 15),
}
CLAIMED_UPPER = {
    2520: 2474, 3360: 3156, 3600: 3361, 3960: 3739,
    4320: 4159, 4680: 4275, 5040: 5039, 5760: 5323,
    6480: 6077, 6720: 6496, 7200: 7079, 7560: 7559,
    7920: 7908, 8400: 8326, 8640: 8531, 9240: 8831, 9360: 9237,
}


def literal_divisors(n):
    return tuple(m for m in range(1, n + 1) if n % m == 0)


@lru_cache(None)
def prime_power_factors(n):
    """Return the maximal prime powers in n by simple trial division."""
    powers = []
    for p in range(2, n + 1):
        if n % p:
            continue
        q = 1
        while n % p == 0:
            n //= p
            q *= p
        powers.append(q)
        if n == 1:
            break
    return tuple(powers)


def agreement_signature(m, a, previous):
    return tuple(gcd(a - b, q)
                 for n, b in previous
                 for q in prime_power_factors(gcd(m, n)))


def orbit_representatives(m, previous):
    """One residue per stabilizer orbit, using capped p-adic agreements."""
    signatures = set()
    for a in range(m):
        signature = agreement_signature(m, a, previous)
        if signature not in signatures:
            signatures.add(signature)
            yield a


def literal_masks(period, moduli):
    """Build each class by evaluating x % m for every point in the period."""
    masks = {}
    for m in moduli:
        if period % m:
            raise ValueError('Every modulus must divide the period.')
        rows = [0] * m
        for x in range(period):
            rows[x % m] |= 1 << x
        masks[m] = tuple(rows)
    return masks


def literal_capacity(period, uncovered, remaining, masks):
    total = period - uncovered.bit_count()
    for m in remaining:
        largest = 0
        for row in masks[m]:
            largest = max(largest, (uncovered & row).bit_count())
            # A class contains exactly period/m points, so this is maximal.
            if largest == period // m:
                break
        total += largest
    return total


def search(period, anchors, minimum=8, pruning=False):
    moduli = tuple(m for m in literal_divisors(period) if m >= minimum)
    if not anchors or len(set(anchors)) != len(anchors):
        raise ValueError('Anchors must be nonempty and distinct.')
    if any(m not in moduli for m in anchors):
        raise ValueError('Every anchor must be an eligible modulus.')
    masks = literal_masks(period, moduli)
    remaining = [tuple(m for m in moduli if m not in anchors[:depth])
                 for depth in range(len(anchors) + 1)]
    nodes = [0] * (len(anchors) + 1)
    terminal_histogram = Counter()
    cuts = leaves = 0
    digest = sha256()

    def record(tag, previous, capacity):
        terminal_histogram[capacity] += 1
        event = [tag, [a for _, a in previous], capacity]
        digest.update((json.dumps(event, separators=(',', ':')) + '\n').encode())

    def walk(depth, uncovered, previous):
        nonlocal cuts, leaves
        nodes[depth] += 1
        if pruning and depth >= 2:
            capacity = literal_capacity(period, uncovered, remaining[depth], masks)
            if capacity < period:
                cuts += 1
                record('cut', previous, capacity)
                return
        if depth == len(anchors):
            capacity = literal_capacity(period, uncovered, remaining[depth], masks)
            leaves += 1
            record('leaf', previous, capacity)
            return
        m = anchors[depth]
        for a in orbit_representatives(m, previous):
            walk(depth + 1, uncovered & ~masks[m][a], previous + ((m, a),))

    walk(0, (1 << period) - 1, ())
    if not terminal_histogram:
        raise RuntimeError('No complete proof events.')
    upper = max(terminal_histogram)
    return {'L': period, 'anchors': list(anchors), 'upper': upper,
            'excluded': upper < period, 'nodes': nodes, 'cuts': cuts,
            'leaves': leaves, 'terminal_capacity_histogram': dict(sorted(terminal_histogram.items())),
            'independent_event_sha256': digest.hexdigest()}


def tree_automorphisms(p, depth):
    """Enumerate the entire small group, independently of orbit signatures."""
    if depth == 0:
        return [(0,)]
    subgroups = tree_automorphisms(p, depth - 1)
    answer = []
    for root in permutations(range(p)):
        for children in product(subgroups, repeat=p):
            answer.append(tuple(root[x % p] + p * children[x % p][x // p]
                                for x in range(p ** depth)))
    return answer


def controls():
    group_checks = 0
    for p, depth, prior_moduli in [(2, 3, (2, 4)), (2, 3, (4, 8)), (3, 2, (3, 9))]:
        group = tree_automorphisms(p, depth)
        m = p ** depth
        for values in product(*(range(n) for n in prior_moduli)):
            previous = tuple(zip(prior_moduli, values))
            stabilizer = [f for f in group if all(f[a] % n == a for n, a in previous)]
            signatures = {}
            for a in range(m):
                signatures.setdefault(agreement_signature(m, a, previous), set()).add(a)
            signature_orbits = {frozenset(s) for s in signatures.values()}
            actual_orbits = {frozenset(f[a] % m for f in stabilizer) for a in range(m)}
            if signature_orbits != actual_orbits:
                raise RuntimeError('Agreement signature does not match the full stabilizer.')
            group_checks += 1
    # A constructive positive control prevents interpreting every run as UNSAT.
    cover = [(2, 0), (3, 0), (4, 1), (6, 1), (12, 11)]
    if not all(any(x % m == a for m, a in cover) for x in range(12)):
        raise RuntimeError('Positive covering fixture is invalid.')
    positive = search(12, (2, 3, 4), minimum=2)
    if positive['excluded']:
        raise RuntimeError('A genuine covering was excluded.')
    # Boundary controls: all uncovered and no uncovered points.
    masks = literal_masks(12, (2, 3, 4, 6, 12))
    if literal_capacity(12, 0, tuple(masks), masks) != 12:
        raise RuntimeError('Empty uncovered set is mishandled.')
    if literal_capacity(12, (1 << 12) - 1, (12,), masks) != 1:
        raise RuntimeError('Single-point classes are mishandled.')
    return {'full_stabilizer_checks': group_checks, 'positive_period12': True,
            'empty_uncovered_and_singleton_controls': True}


def prove():
    candidates = []
    equality = []
    for period in range(8, 10080, 8):
        density_capacity = sum(period // m for m in literal_divisors(period) if m >= 8)
        if density_capacity >= period:
            candidates.append(period)
        if density_capacity == period:
            equality.append(period)
    if candidates != list(CLAIMED_UPPER):
        raise RuntimeError('The independently scanned candidate set differs from the claim.')
    results = []
    for period in candidates:
        anchors = SPECIAL.get(period, tuple(m for m in (8, 9, 10, 12, 15) if period % m == 0))
        result = search(period, anchors, pruning=period in (5040, 7560))
        if not result['excluded'] or result['upper'] != CLAIMED_UPPER[period]:
            raise RuntimeError('The claimed exclusion or upper bound was not reproduced: ' + str(result))
        if period in (5040, 7560) and result['leaves']:
            raise RuntimeError('An uncut leaf remains in a pruned case.')
        print(f'L={period} upper={result["upper"]} nodes={sum(result["nodes"])} cuts={result["cuts"]} leaves={result["leaves"]}', flush=True)
        results.append(result)
    return {'agent': 'six-reviewer-1', 'role': 'independent reviewer',
            'claim': 'L_min(8) >= 10080, minimum exactly eight',
            'multiples_checked': len(range(8, 10080, 8)),
            'density_exclusions': len(range(8, 10080, 8)) - len(candidates),
            'density_equality_cases': equality, 'cases': results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', type=Path)
    parser.add_argument('--check', type=Path)
    parser.add_argument('--controls-only', action='store_true')
    args = parser.parse_args()
    start = monotonic()
    checked_controls = controls()
    print(json.dumps(checked_controls, sort_keys=True), flush=True)
    if args.controls_only:
        return
    result = prove()
    result['controls'] = checked_controls
    if args.check is not None and result != json.loads(args.check.read_text()):
        raise RuntimeError('Independent manifest mismatch.')
    if args.write is not None:
        args.write.write_text(json.dumps(result, indent=2) + '\n')
    print('INDEPENDENT AUDIT PASSED: all 1259 LCMs below 10080 excluded.', flush=True)
    print(f'Elapsed seconds: {monotonic() - start:.3f}', flush=True)
    print(f'Peak RSS (Linux KiB): {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}', flush=True)


if __name__ == '__main__':
    main()
