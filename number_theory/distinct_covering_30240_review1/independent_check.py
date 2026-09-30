#!/usr/bin/env python3
"""six-reviewer-1: CRT tensor audit and complete two-phase neighborhood.

No author's module, solver, or search implementation is imported. The
explicit cover is copied untrusted input; all required arithmetic is checked.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def prime_power_axes(n):
    axes, p = [], 2
    while p*p <= n:
        power = 1
        while n % p == 0:
            n //= p
            power *= p
        if power > 1:
            axes.append(power)
        p += 1
    if n > 1:
        axes.append(n)
    return tuple(axes)


def validate(data):
    require(type(data) is dict and data.get('format_version') == 1, 'invalid format')
    rows = data['congruences']
    require(type(rows) is list and 1 <= len(rows) < 256, 'invalid class list')
    require(all(type(row) is list and len(row) == 2 and
                all(type(v) is int for v in row) and row[1] >= 2 and
                0 <= row[0] < row[1] for row in rows), 'invalid integer class')
    require(len({m for a, m in rows}) == len(rows), 'repeated modulus')
    period = 1
    for a, m in rows:
        period = period//gcd(period, m)*m
    require(type(data['lcm']) is int and data['lcm'] == period, 'incorrect actual LCM')
    require(period <= 100000, 'outside the explicit resource boundary')
    return rows, period


def tensor_membership(data):
    """One bit per class; intersect independent prime-coordinate masks."""
    rows, L = validate(data)
    axes = prime_power_axes(L)
    weights = tuple((L//q)*pow(L//q, -1, q) for q in axes)
    all_classes = (1 << len(rows))-1
    masks = []
    for q in axes:
        projections = tuple((gcd(q, m), a % gcd(q, m)) for a, m in rows)
        masks.append(tuple(sum(1 << i for i, (d, a) in enumerate(projections)
                               if r % d == a) for r in range(q)))
    membership, seen = [None]*L, set()
    for coordinates in product(*(range(q) for q in axes)):
        bits = all_classes
        for tables, r in zip(masks, coordinates):
            bits &= tables[r]
        x = sum(r*e for r, e in zip(coordinates, weights)) % L
        require(x not in seen and all(x % q == r for q, r in zip(axes, coordinates)),
                'CRT tuple reconstruction failed')
        seen.add(x)
        membership[x] = bits
    require(len(seen) == L and all(b is not None for b in membership),
            'incomplete Cartesian enumeration')
    return rows, L, axes, membership


def partition_points(membership, classes):
    private, doubles = [[] for _ in range(classes)], {}
    for x, bits in enumerate(membership):
        if bits.bit_count() == 1:
            private[bits.bit_length()-1].append(x)
        elif bits.bit_count() == 2:
            doubles.setdefault(bits, []).append(x)
    return private, doubles


def single_residue(points, modulus):
    require(points, 'private points required')
    residue = points[0] % modulus
    return residue if all(x % modulus == residue for x in points) else None


def two_phase_neighborhood(rows, membership):
    """Every changed pair has at most one candidate, forced by privates."""
    private, doubles = partition_points(membership, len(rows))
    require(all(private), 'this neighborhood theorem requires irredundance')
    require(all(membership), 'this neighborhood theorem requires coverage')
    statistics, alternatives = Counter(), []
    for i, j in combinations(range(len(rows)), 2):
        ai, mi = rows[i]
        aj, mj = rows[j]
        # If i changes, its private points must all be covered by the new j;
        # the converse holds for j. Thus both new phases are forced.
        bi, bj = single_residue(private[j], mi), single_residue(private[i], mj)
        if bi is None or bj is None:
            statistics['private_residue_mismatch'] += 1
            continue
        require(bi != ai and bj != aj, 'a private point was originally shared')
        residual = private[i]+private[j]+doubles.get((1 << i)|(1 << j), [])
        if any(x % mi != bi and x % mj != bj for x in residual):
            statistics['forced_candidate_leaves_holes'] += 1
            continue
        statistics['alternate_cover'] += 1
        alternatives.append([[mi, ai, bi], [mj, aj, bj]])
    pairs = len(rows)*(len(rows)-1)//2
    require(sum(statistics.values()) == pairs, 'incomplete pair audit')
    return {'pairs': pairs, 'pair_outcomes': dict(sorted(statistics.items())),
            'single_phase_alternatives': 0,
            'two_phase_alternatives': len(alternatives),
            'alternatives_as_modulus_old_new': alternatives}


def main_audit(data, raw_hash):
    rows, L, axes, membership = tensor_membership(data)
    require(min(m for a, m in rows) == 8, 'minimum is not exactly eight')
    require(all(membership), 'uncovered point in the full period')
    private, _ = partition_points(membership, len(rows))
    require(all(private), 'a class is redundant')
    multiplicity = bytes(bits.bit_count() for bits in membership)
    histogram = dict(sorted(Counter(multiplicity).items()))
    require(sum(histogram.values()) == L, 'wrong multiplicity total')
    require(sum(k*v for k, v in histogram.items()) == sum(L//m for a, m in rows),
            'total incidence identity fails')
    result = {
        'agent': 'six-reviewer-1', 'role': 'independent mathematical reviewer',
        'input_cover_sha256': raw_hash, 'classes': len(rows), 'lcm': L,
        'minimum_modulus': 8, 'prime_power_CRT_axes': list(axes),
        'Cartesian_tuples_checked': L, 'uncovered': 0,
        'coverage_multiplicities': {str(k): v for k, v in histogram.items()},
        'multiplicity_bytes_sha256': sha256(multiplicity).hexdigest(),
        'total_incidences': sum(k*v for k, v in histogram.items()),
        'membership_patterns': len(set(membership)),
        'private_points_by_modulus': [[m, len(P)] for (a, m), P in zip(rows, private)],
        'minimum_private_points': min(map(len, private)),
        'phase_neighborhood': two_phase_neighborhood(rows, membership),
    }
    return result


def literal_membership(rows, L):
    """Controls only: deliberately different definition-level algorithm."""
    return [sum(1 << i for i, (a, m) in enumerate(rows) if x % m == a)
            for x in range(L)]


def controls(original):
    configurations = points = 0
    for moduli in ((2, 3, 4), (3, 5), (4, 9), (2, 3, 4, 6)):
        L = 1
        for m in moduli:
            L = L//gcd(L, m)*m
        for residues in product(*(range(m) for m in moduli)):
            data = {'format_version': 1, 'lcm': L,
                    'congruences': [list(pair) for pair in zip(residues, moduli)]}
            rows, period, axes, membership = tensor_membership(data)
            require(membership == literal_membership(rows, L), 'small CRT mismatch')
            configurations += 1
            points += L
    # All independent phase choices for every pair in twelve genuine covers.
    fixture = ((0, 2), (0, 3), (1, 4), (1, 6), (11, 12))
    pair_controls = literal_choices = 0
    for unit, shift in product((1, 5, 7, 11), (0, 1, 3)):
        rows = [[(unit*a+shift) % m, m] for a, m in fixture]
        membership = literal_membership(rows, 12)
        private, _ = partition_points(membership, len(rows))
        require(all(membership) and all(private), 'bad irredundant fixture')
        optimized = two_phase_neighborhood(rows, membership)
        actual = []
        for i, j in combinations(range(len(rows)), 2):
            ai, mi = rows[i]
            aj, mj = rows[j]
            for bi, bj in product(range(mi), range(mj)):
                if bi == ai or bj == aj:
                    continue
                changed = [row[:] for row in rows]
                changed[i][0], changed[j][0] = bi, bj
                if all(literal_membership(changed, 12)):
                    actual.append([[mi, ai, bi], [mj, aj, bj]])
                literal_choices += 1
            pair_controls += 1
        require(actual == optimized['alternatives_as_modulus_old_new'],
                'two-phase candidate lemma failed complete literal comparison')
    rejected = 0
    corruptions = []
    for action in ('duplicate', 'wrong_period', 'invalid_phase', 'boolean_phase'):
        data = json.loads(json.dumps(original))
        if action == 'duplicate':
            data['congruences'].append(data['congruences'][0][:])
        elif action == 'wrong_period':
            data['lcm'] += 1
        elif action == 'invalid_phase':
            data['congruences'][0][0] = data['congruences'][0][1]
        else:
            data['congruences'][0][0] = True
        corruptions.append(data)
    for data in corruptions:
        try:
            validate(data)
        except ValueError:
            rejected += 1
        else:
            raise RuntimeError('invalid cover metadata accepted')
    essential_changed = json.loads(json.dumps(original))
    essential_changed['congruences'][0][0] = (essential_changed['congruences'][0][0]+1) % 8
    try:
        main_audit(essential_changed, 'control')
    except ValueError:
        rejected += 1
    else:
        raise RuntimeError('changed essential class accepted')
    return {'complete_small_CRT_configurations': configurations,
            'literal_small_point_checks': points,
            'complete_small_pair_controls': pair_controls,
            'literal_small_phase_choices': literal_choices,
            'corrupted_inputs_rejected': rejected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cover', type=Path, default=HERE/'cover.json')
    parser.add_argument('--author-expected', type=Path,
                        help='optional JSON comparison; target code is never imported')
    args = parser.parse_args()
    raw = args.cover.read_bytes()
    data = json.loads(raw)
    result = main_audit(data, sha256(raw).hexdigest())
    result['controls'] = controls(data)
    if args.author_expected is not None:
        expected = json.loads(args.author_expected.read_text())
        for key in ('minimum_modulus', 'lcm', 'classes', 'uncovered',
                    'coverage_multiplicities', 'multiplicity_bytes_sha256',
                    'private_points_by_modulus'):
            require(result[key] == expected[key], 'target manifest differs: '+key)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
