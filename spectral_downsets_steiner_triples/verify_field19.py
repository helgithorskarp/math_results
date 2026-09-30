"""Exact capped maximal-rank H for one specified affine field design at19.

Regenerates the literal field block set, its contained cyclic decompositions,
the affine action and all supported pair orbits. Fixed rational weights are
checked by full definition equations and two exact compressed PSD methods.
--full additionally checks all seven 305-by-305 forms by integer Schur
elimination, independently of the prime-affine representation bridge.
Standard library only. Author: six-downset-2, researcher.
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
from certificates import check_sts, downset, mask, steiner_certificate
from integer_psd import integer_psd_rank
from verify import check_definition, exact_psd_rank, matrix_hash, relabel, rejects
from verify_three9 import gram_rank, upper, buffered_upper
from verify_two9 import polynomial_psd


def digest(value):
    return sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def field_design():
    p, rho = 19, 8
    assert (rho*rho-rho+1) % p == 0
    U = {mask((x, (x+d) % p, (x+rho*d) % p))
         for x in range(p) for d in range(1, p)}
    other_root = {mask((x, (x+d) % p, (x+12*d) % p))
                  for x in range(p) for d in range(1, p)}
    assert U == other_root and len(U) == 114
    assert all(sum(t & a == a for t in U) == 2
               for a in (mask(s) for s in combinations(range(p), 2)))
    T = [tuple((x+b) % p for x in range(p)) for b in range(p)]
    remaining = set(U)
    orbits = []
    while remaining:
        a = min(remaining)
        orbit = {relabel(a, g) for g in T}
        assert len(orbit) == p and orbit <= remaining
        remaining -= orbit
        orbits.append(tuple(sorted(orbit)))
    assert len(orbits) == 6
    systems = []
    for inds in combinations(range(6), 3):
        blocks = tuple(sorted(t for i in inds for t in orbits[i]))
        try:
            check_sts(p, blocks)
        except ValueError:
            continue
        systems.append(blocks)
    assert len(systems) == len(set(systems)) == 8
    pairs = [(a, b) for a, b in combinations(systems, 2) if not set(a) & set(b)]
    assert len(pairs) == 4 and all(set(a+b) == U for a, b in pairs)
    pair_keys = {tuple(sorted(pair)) for pair in pairs}
    for g in affine_maps(p):
        assert {relabel(t, g) for t in U} == U
        for pair in pairs:
            image = tuple(sorted(tuple(sorted(relabel(t, g) for t in system))
                                 for system in pair))
            assert image in pair_keys
    coverage = {'field_blocks': len(U), 'pair_multiplicity': 2,
                'translation_triple_orbits_within_U': len(orbits),
                'contained_cyclic_system_candidates': 20,
                'contained_cyclic_STSs': len(systems),
                'unordered_contained_cyclic_decompositions': len(pairs),
                'systems_sha256': digest(systems),
                'union_sha256': digest(sorted(U))}
    return [list(a) for a in pairs[0]], pairs, coverage


def decode(data, layers):
    D = downset(19, layers)
    assert (len(D), data['v'], data['N'], data['s']) == (305, 19, 305, 37)
    G = affine_maps(19)
    idx = {a: i for i, a in enumerate(D)}
    actions = [[idx[relabel(a, g)] for a in D] for g in G]
    remaining = {(i, j) for i in range(305) for j in range(i, 305) if not D[i] & D[j]}
    supported = len(remaining)
    orbit_classes, reps = [], []
    while remaining:
        i, j = min(remaining)
        images = {tuple(sorted((g[i], g[j]))) for g in actions}
        assert images <= remaining
        remaining -= images
        orbit_classes.append(sorted(images))
        reps.append([D[i], D[j]])
    assert (supported, len(reps)) == (34220, 115)
    assert digest(reps) == data['orbit_representatives_sha256']
    den = data['denominator']
    assert isinstance(den, int) and den > 0
    assert len(data['orbit_numerators']) == len(reps)
    assert all(isinstance(x, int) for x in data['orbit_numerators'])
    Q = [[F(37 if i == j and i else 0) for j in range(305)] for i in range(305)]
    for orbit, numerator in zip(orbit_classes, data['orbit_numerators']):
        for i, j in orbit:
            Q[i][j] = Q[j][i] = F(numerator, den)
    assert matrix_hash(Q) == data['centered_matrix_sha256']
    return D, Q, {'checked_affine_subgroup_order': len(G),
                  'supported_pairs': supported, 'supported_pair_orbits': len(reps),
                  'orbit_representatives_sha256': digest(reps)}


def certify(D, Q, parts, full=False):
    rank, ranks = affine_psd_rank(D, 19, Q, parts)
    polynomials = {k: polynomial_psd(compression(Q, parts[k])) for k in ('T', 'H')}
    assert all(polynomials[k]['rank'] == ranks[k] for k in polynomials)
    if full:
        assert integer_psd_rank(Q) == rank
        print('full integer Schur verified', len(D), 'rank', rank, flush=True)
    return {'rank': rank, 'compressed_ranks': ranks, 'polynomials': polynomials}


def run(full=False):
    data = json.loads(Path(__file__).with_name('field19_certificate.json').read_text())
    layers, pairs, coverage = field_design()
    D, Q, symmetry = decode(data, layers)
    check_definition(D, 37, Q, psd=False)
    assert all(x == 1 for x in Q[0])
    parts = invariant_partitions(D, 19)
    assert {k: len(a) for k, a in parts.items()} == {'T': 17, 'H': 20, 'G': 4}
    assert data['centered_gap'] == 132
    forms = {'centered': Q, 'centered_upper': upper(Q),
             'centered_gap132': buffered_upper(Q, F(132))}
    centered = {name: certify(D, R, parts, full) for name, R in forms.items()}
    assert centered['centered']['rank'] == 285
    assert centered['centered_upper']['rank'] == centered['centered_gap132']['rank'] == 304
    stars = [[F(bool(a >> i & 1))-F(37, 305) for a in D] for i in range(19)]
    w = [F(j == 0)-F(1, 305) for j in range(305)]
    assert gram_rank(stars) == 19 and gram_rank(stars+[w]) == 20

    Qo = [[F(0) for _ in D] for _ in D]
    for pair in pairs:
        Do, so, input_Q = steiner_certificate(19, pair)
        assert (Do, so) == (D, 37)
        check_definition(D, 37, input_Q, psd=False)
        for i in range(305):
            for j in range(305):
                Qo[i][j] += input_Q[i][j]/4
    check_definition(D, 37, Qo, psd=False)
    ordinary = certify(D, Qo, parts, full)
    assert ordinary['rank'] == 250 and Qo[0][0] == F(15525, 2)
    trace = sum(Qo[i][i] for i in range(305))
    assert trace == F(38021, 2)
    assert sum(Qo[1][j]*w[j] for j in range(305)) == -399
    epsilon = F(66)/trace
    assert epsilon == F(132, 38021) and 0 < epsilon < 1
    Qr = [[(1-epsilon)*Q[i][j]+epsilon*Qo[i][j] for j in range(305)]
          for i in range(305)]
    check_definition(D, 37, Qr, psd=False)
    repaired_forms = {'repaired': Qr, 'repaired_upper': upper(Qr),
                      'repaired_gap66': buffered_upper(Qr, F(66))}
    repaired = {name: certify(D, R, parts, full) for name, R in repaired_forms.items()}
    assert repaired['repaired']['rank'] == 286
    assert repaired['repaired_upper']['rank'] == repaired['repaired_gap66']['rank'] == 304
    assert all(sum(Qr[i][j]*star[j] for j in range(305)) == 0
               for star in stars for i in range(305))

    # Validate the full integer checker against the separate rational checker
    # on the actual compressed forms, including singular and indefinite inputs.
    for forms_group in (forms, {'ordinary': Qo}, repaired_forms):
        for R in forms_group.values():
            for part in parts.values():
                B = compression(R, part)
                assert integer_psd_rank(B) == exact_psd_rank(B)
    rejects(lambda: integer_psd_rank([[0, 1], [1, 0]]))
    rejects(lambda: integer_psd_rank([[1, 2], [2, 1]]))
    bad = copy.deepcopy(Q)
    bad[0][1] += 1
    bad[1][0] += 1
    rejects(lambda: check_definition(D, 37, bad, psd=False))
    rejects(lambda: check_equivariance(D, 19, bad))
    bad_data = copy.deepcopy(data)
    bad_data['orbit_numerators'][-1] += 1
    rejects(lambda: decode(bad_data, layers))
    rejects(lambda: check_sts(19, layers[1][:-1]))
    return {'arithmetic': 'fractions.Fraction and arbitrary-precision integers',
            'v': 19, 'N': 305, 's': 37, 'coverage': coverage, 'symmetry': symmetry,
            'fixed_space_dimensions': {k: len(a) for k, a in parts.items()},
            'centered_forms': centered, 'ordinary': ordinary,
            'ordinary_Q00': str(Qo[0][0]), 'ordinary_trace': str(trace),
            'ordinary_averaged_decompositions': len(pairs),
            'ordinary_matrix_sha256': matrix_hash(Qo), 'epsilon': str(epsilon),
            'repaired_forms': repaired, 'centered_matrix_sha256': matrix_hash(Q),
            'repaired_matrix_sha256': matrix_hash(Qr),
            'kernel_star_rank': 19, 'centered_kernel_rank': 20,
            'integer_checker_compressed_crosschecks': 21, 'rejection_controls': 6}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--write-expected', action='store_true')
    parser.add_argument('--full', action='store_true')
    args = parser.parse_args()
    assert not (args.check and args.write_expected)
    result = run(args.full)
    expected = Path(__file__).with_name('field19_expected.json')
    if args.check:
        assert result == json.loads(expected.read_text()), 'expected-output mismatch'
    if args.write_expected:
        expected.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, indent=2, sort_keys=True))
