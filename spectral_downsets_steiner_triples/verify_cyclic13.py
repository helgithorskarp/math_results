"""Exact capped maximal-rank H for every common-cycle two-STS(13) input.

Regenerates all 22 translation orbits and all 231 possible cyclic systems.
Four systems, two disjoint pairs, and exactly one union remain. Fixed rational
entries are checked directly against the H definition and by two exact PSD
methods on affine fixed spaces. --full also checks the full 144-by-144 forms
by Schur elimination, independently of the written affine reduction.
CPython 3.11+, standard library only. Author: six-downset-2, researcher.
"""
import argparse
import copy
import json
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from pathlib import Path

from affine_psd import (affine_maps, affine_psd_rank, check_equivariance,
                        compression, invariant_partitions)
from certificates import (check_sts, complement_cube, cyclic_sts13, downset,
                          mask, steiner_certificate)
from verify import check_definition, exact_psd_rank, matrix_hash, relabel, rejects
from verify_three9 import gram_rank, upper, buffered_upper
from verify_two9 import polynomial_psd


def digest(value):
    return sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def cyclic_cohort():
    p = 13
    T = [tuple((x+b) % p for x in range(p)) for b in range(p)]
    remaining = {mask(t) for t in combinations(range(p), 3)}
    orbits = []
    while remaining:
        a = min(remaining)
        orbit = {relabel(a, g) for g in T}
        assert len(orbit) == p and orbit <= remaining
        remaining -= orbit
        orbits.append(tuple(sorted(orbit)))
    assert len(orbits) == 22
    systems = []
    for a, b in combinations(orbits, 2):
        blocks = tuple(sorted(a+b))
        try:
            check_sts(p, blocks)
        except ValueError:
            continue
        systems.append(blocks)
    systems.sort()
    assert len(systems) == 4 and len(set(systems)) == 4
    pairs = [(a, b) for a, b in combinations(systems, 2) if not set(a) & set(b)]
    assert len(pairs) == 2
    unions = {tuple(sorted(a+b)) for a, b in pairs}
    assert len(unions) == 1
    union = next(iter(unions))
    field = {mask((x, (x+d) % p, (x+4*d) % p))
             for x in range(p) for d in range(1, p)}
    assert len(field) == 52 and field == set(union)
    first = tuple(cyclic_sts13())
    assert first in systems
    second = tuple(sorted(field-set(first)))
    assert second in systems and not set(first) & set(second)
    check_sts(p, second)
    assert all({relabel(t, g) for t in union} == field for g in affine_maps(p))
    coverage = {'translation_triple_orbits': len(orbits),
                'candidate_systems': 231, 'cyclic_STSs': len(systems),
                'unordered_disjoint_pairs': len(pairs), 'distinct_unions': len(unions),
                'systems_sha256': digest(systems), 'union_sha256': digest(union)}
    return [list(first), list(second)], pairs, coverage


def decode(data, layers):
    D = downset(13, layers)
    assert (len(D), data['v'], data['N'], data['s']) == (144, 13, 144, 25)
    G = affine_maps(13)
    idx = {a: i for i, a in enumerate(D)}
    actions = [[idx[relabel(a, g)] for a in D] for g in G]
    remaining = {(i, j) for i in range(len(D)) for j in range(i, len(D))
                 if not D[i] & D[j]}
    supported_count = len(remaining)
    orbit_classes = []
    reps = []
    while remaining:
        i, j = min(remaining)
        images = {tuple(sorted((g[i], g[j]))) for g in actions}
        assert images <= remaining
        remaining -= images
        orbit_classes.append(sorted(images))
        reps.append([D[i], D[j]])
    assert (supported_count, len(reps)) == (6631, 54)
    assert len(data['orbit_numerators']) == len(reps)
    assert all(isinstance(x, int) for x in data['orbit_numerators'])
    den = data['denominator']
    assert isinstance(den, int) and den > 0
    Q = [[F(25 if i == j and i else 0) for j in range(144)] for i in range(144)]
    for orbit, numerator in zip(orbit_classes, data['orbit_numerators']):
        for i, j in orbit:
            Q[i][j] = Q[j][i] = F(numerator, den)
    assert digest(reps) == data['orbit_representatives_sha256']
    assert matrix_hash(Q) == data['centered_matrix_sha256']
    return D, Q, {'checked_affine_subgroup_order': len(G),
                  'supported_pairs': supported_count, 'supported_pair_orbits': len(reps),
                  'orbit_representatives_sha256': digest(reps)}


def projection(n, parts):
    Q = [[F(0) for _ in range(n)] for _ in range(n)]
    for part in parts:
        for i in part:
            for j in part:
                Q[i][j] = F(1, len(part))
    return Q


def certify(D, p, Q, parts, full=False):
    rank, ranks = affine_psd_rank(D, p, Q, parts)
    polynomials = {k: polynomial_psd(compression(Q, parts[k])) for k in ('T', 'H')}
    assert all(polynomials[k]['rank'] == ranks[k] for k in polynomials)
    if full:
        assert exact_psd_rank(Q) == rank
        print('full Schur verified', len(D), 'rank', rank, flush=True)
    return {'rank': rank, 'compressed_ranks': ranks, 'polynomials': polynomials}


def run(full=False):
    data = json.loads(Path(__file__).with_name('cyclic13_certificate.json').read_text())
    layers, cyclic_pairs, coverage = cyclic_cohort()
    D, Q, symmetry = decode(data, layers)
    check_definition(D, 25, Q, psd=False)
    assert all(x == 1 for x in Q[0])
    parts = invariant_partitions(D, 13)
    assert {k: len(a) for k, a in parts.items()} == {'T': 12, 'H': 15, 'G': 4}
    forms = {'centered': Q, 'centered_upper': upper(Q),
             'centered_gap72': buffered_upper(Q, F(72))}
    centered = {name: certify(D, 13, R, parts, full) for name, R in forms.items()}
    assert centered['centered']['rank'] == 130
    assert centered['centered_upper']['rank'] == centered['centered_gap72']['rank'] == 143
    stars = [[F(bool(a >> i & 1))-F(25, 144) for a in D] for i in range(13)]
    w = [F(j == 0)-F(1, 144) for j in range(144)]
    assert gram_rank(stars) == 13 and gram_rank(stars+[w]) == 14

    baselines = [steiner_certificate(13, pair) for pair in cyclic_pairs]
    assert all((Do, so) == (D, 25) for Do, so, _ in baselines)
    for _, _, baseline_Q in baselines:
        check_definition(D, 25, baseline_Q, psd=False)
        if full:
            assert exact_psd_rank(baseline_Q) == 95
            print('full ordinary decomposition verified rank95', flush=True)
    # A fixed decomposition has less symmetry than the centered certificate.
    # The complete two-decomposition average is affine-equivariant.
    Qo = [[sum((baseline_Q[i][j] for _, _, baseline_Q in baselines), F(0))/2
           for j in range(144)] for i in range(144)]
    check_definition(D, 25, Qo, psd=False)
    ordinary = certify(D, 13, Qo, parts, full)
    assert ordinary['rank'] == 107
    assert Qo[0][0] == F(6256, 3)
    trace = sum(Qo[i][i] for i in range(144))
    assert trace == F(16981, 3)
    assert sum(Qo[1][j]*w[j] for j in range(144)) == -182
    epsilon = F(72, 2)/trace
    assert epsilon == F(108, 16981) and 0 < epsilon < 1
    Qr = [[(1-epsilon)*Q[i][j]+epsilon*Qo[i][j] for j in range(144)]
          for i in range(144)]
    check_definition(D, 25, Qr, psd=False)
    repaired_forms = {'repaired': Qr, 'repaired_upper': upper(Qr),
                      'repaired_gap36': buffered_upper(Qr, F(36))}
    repaired = {name: certify(D, 13, R, parts, full) for name, R in repaired_forms.items()}
    assert repaired['repaired']['rank'] == 131
    assert repaired['repaired_upper']['rank'] == repaired['repaired_gap36']['rank'] == 143
    assert all(sum(Qr[i][j]*star[j] for j in range(144)) == 0
               for star in stars for i in range(144))

    baseline = []
    for p in (2, 3, 5):
        Db, sb, Qb = complement_cube(p)
        bp = invariant_partitions(Db, p)
        record = certify(Db, p, Qb, bp, full=True)
        assert check_definition(Db, sb, Qb) == record['rank'] == sb
        baseline.append({'p': p, 'N': len(Db), **record})

    # Both invariant restrictions are necessary: each misses one exact bad form.
    PT = projection(144, parts['T'])
    PG = projection(144, parts['G'])
    bad_T = [[-PT[i][j]+PG[i][j] for j in range(144)] for i in range(144)]
    assert exact_psd_rank(compression(bad_T, parts['H'])) == 0
    rejects(lambda: affine_psd_rank(D, 13, bad_T, parts))
    bad_H = [[PT[i][j]-F(i == j) for j in range(144)] for i in range(144)]
    assert exact_psd_rank(compression(bad_H, parts['T'])) == 0
    rejects(lambda: affine_psd_rank(D, 13, bad_H, parts))
    rejects(lambda: affine_maps(4))
    bad = copy.deepcopy(Q)
    bad[0][1] += 1
    bad[1][0] += 1
    rejects(lambda: check_definition(D, 25, bad, psd=False))
    rejects(lambda: check_equivariance(D, 13, bad))
    bad = copy.deepcopy(data)
    bad['orbit_numerators'][-1] += 1
    rejects(lambda: decode(bad, layers))
    rejects(lambda: check_sts(13, layers[1][:-1]))
    return {'arithmetic': 'fractions.Fraction and arbitrary-precision integers',
            'N': 144, 's': 25, 'v': 13, 'coverage': coverage, 'symmetry': symmetry,
            'fixed_space_dimensions': {k: len(a) for k, a in parts.items()},
            'centered_forms': centered, 'ordinary': ordinary,
            'ordinary_Q00': str(Qo[0][0]), 'ordinary_trace': str(trace),
            'ordinary_averaged_decompositions': len(baselines),
            'ordinary_matrix_sha256': matrix_hash(Qo),
            'epsilon': str(epsilon), 'repaired_forms': repaired,
            'centered_matrix_sha256': matrix_hash(Q),
            'repaired_matrix_sha256': matrix_hash(Qr),
            'kernel_star_rank': 13, 'centered_kernel_rank': 14,
            'cube_baselines': baseline, 'rejection_controls': 7}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--write-expected', action='store_true')
    parser.add_argument('--full', action='store_true')
    args = parser.parse_args()
    assert not (args.check and args.write_expected)
    result = run(args.full)
    expected = Path(__file__).with_name('cyclic13_expected.json')
    if args.check:
        assert result == json.loads(expected.read_text()), 'expected-output mismatch'
    if args.write_expected:
        expected.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, indent=2, sort_keys=True))
