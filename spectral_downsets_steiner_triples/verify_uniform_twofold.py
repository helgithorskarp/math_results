"""Exact finite validation accompanying the uniform written incidence proof.

At primes 13,19,31: both centered and uniformly maximal forms by exact affine
compression, rational/integer Schur and integer characteristic-polynomial
checks. At16: all four full integer Schur checks,
with no symmetry reduction. At13 also checks the ordinary and repaired forms
in full. All inputs are regenerated; no fixed weight fixture is needed.
CPython3.11+, standard library only. Author: six-downset-2, researcher.
"""
import argparse
import json
import sys
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path

from affine_psd import check_equivariance, compression, invariant_partitions
from integer_psd import integer_psd_rank
from twofold_identities import run as identities
from uniform_twofold import (binary_field16, centered_certificate, design_data,
                             gap, maximal_certificate, nonbijective_fixture, prime_decomposition,
                             repaired_certificate, weights)
from verify import check_definition, exact_psd_rank, matrix_hash, rejects
from verify_three9 import buffered_upper, gram_rank
from verify_two9 import polynomial_psd


def digest(value):
    return sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def incidence_check(v, blocks):
    pairs, completion, outside = design_data(v, blocks)
    P = [[int(a >> x & 1) for a in pairs] for x in range(v)]
    C = [[int(completion[a] >> x & 1) for a in pairs] for x in range(v)]
    B = [[int(a >> x & 1) for a in blocks] for x in range(v)]
    H = [[outside[a].get(x, 0) for a in blocks] for x in range(v)]
    assert all(sum(row) == v-1 for matrix in (P, C, B, H) for row in matrix)
    assert all(sum(H[x][j] for x in range(v)) == 3 for j in range(len(blocks)))
    for x in range(v):
        for y in range(v):
            dot = lambda A, Z: sum(a*b for a, b in zip(A[x], Z[y]))
            assert dot(P, P) == (v-2)*int(x == y)+1
            E = dot(C, C)-dot(P, P)
            assert dot(B, B) == (v-3)*int(x == y)+2
            assert dot(P, C) == dot(C, P) == 2*int(x != y)
            assert dot(B, H) == dot(H, B) == 3*int(x != y)+E
    for block in blocks:
        contained = [p for p in pairs if p & block == p]
        assert len(contained) == 3
        for x in range(v):
            assert sum(int(p >> x & 1) for p in contained) == 2*int(block >> x & 1)
            assert sum(int(completion[p] >> x & 1) for p in contained) == (
                int(block >> x & 1)+outside[block].get(x, 0))
    for p in pairs:
        containing = [a for a in blocks if a & p == p]
        assert len(containing) == 2
        for x in range(v):
            assert sum(int(a >> x & 1) for a in containing) == (
                2*int(p >> x & 1)+int(completion[p] >> x & 1))
    return {'pair_completion_permutation': len(set(completion.values())) == len(pairs),
            'incidence_identities_checked': 10,
            'outside_completion_multiplicities': sorted({n for row in H for n in row})}


def compressed_certification(Q, p, parts):
    small = {name: compression(Q, part) for name, part in parts.items()}
    ranks = {name: exact_psd_rank(form) for name, form in small.items()}
    assert all(integer_psd_rank(form) == ranks[name] for name, form in small.items())
    polynomial_hashes = {}
    for name in ('T', 'H'):
        polynomial = polynomial_psd(small[name])
        assert polynomial['rank'] == ranks[name]
        polynomial_hashes[name] = digest(polynomial)
    rank = ranks['T']+(p-1)*(ranks['H']-ranks['G'])
    return {'rank': rank, 'compressed_ranks': ranks,
            'integer_polynomial_sha256': polynomial_hashes}


def run():
    result = {'agent': 'six-downset-2', 'role': 'researcher',
              'arithmetic': 'Fraction, integer Schur, integer coefficient comparison',
              'identities': identities(), 'primes': []}
    for p in (13, 19, 31):
        D0, roots, blocks, systems = prime_decomposition(p)
        D, s, Qc = centered_certificate(p, blocks)
        assert D == D0
        check_definition(D, s, Qc, psd=False)
        check_equivariance(D, p, Qc)
        parts = invariant_partitions(D, p)
        lower = compressed_certification(Qc, p, parts)
        buffered = compressed_certification(buffered_upper(Qc, gap(p)), p, parts)
        n = len(D)
        assert lower['rank'] == n-p-1 and buffered['rank'] == n-1
        record = {'v': p, 'roots': roots, 'N': n, 's': s,
                  'weights': {k: str(x) for k, x in weights(p).items()},
                  'gap': str(gap(p)), 'lower': lower, 'buffered_upper': buffered,
                  'fixed_dimensions': {k: len(a) for k, a in parts.items()},
                  'centered_matrix_sha256': matrix_hash(Qc),
                  **incidence_check(p, blocks)}
        Dm, sm, Qm, eta = maximal_certificate(p, blocks, (D, s, Qc))
        assert (Dm, sm) == (D, s)
        check_definition(D, s, Qm, psd=False)
        check_equivariance(D, p, Qm)
        maximal_lower = compressed_certification(Qm, p, parts)
        maximal_upper = compressed_certification(buffered_upper(Qm, gap(p)/2), p, parts)
        assert maximal_lower['rank'] == n-p and maximal_upper['rank'] == n-1
        record['uniform_maximal'] = {'eta': str(eta), 'lower': maximal_lower,
                                     'buffered_upper': maximal_upper,
                                     'gap': str(gap(p)/2), 'Q00': str(Qm[0][0]),
                                     'matrix_sha256': matrix_hash(Qm)}
        Dr, sr, Qr, Qo, epsilon, trace = repaired_certificate(p, systems, (D, s, Qc))
        assert (Dr, sr) == (D, s)
        check_definition(D, s, Qo, psd=False)
        check_definition(D, s, Qr, psd=False)
        w = [F(j == 0)-F(1, n) for j in range(n)]
        singleton = D.index(1)
        assert sum(Qo[singleton][j]*w[j] for j in range(n)) == n-s*p-1 != 0
        stars = [[F(bool(a >> x & 1))-F(s, n) for a in D] for x in range(p)]
        assert gram_rank(stars+[w]) == p+1
        if p == 13:
            # Full independent lower and cap checks also reproduce the useful
            # ordinary two-system baseline, without the affine bridge.
            assert integer_psd_rank(Qo) == n-4*p+3
            assert integer_psd_rank(Qr) == n-p
            assert integer_psd_rank(buffered_upper(Qr, gap(p)/2)) == n-1
        record['repair'] = {'epsilon': str(epsilon), 'ordinary_trace': str(trace),
                            'ordinary_Q00': str(Qo[0][0]),
                            'singleton_Qow': n-s*p-1,
                            'rank_by_kernel_intersection': n-p,
                            'gap_by_trace_bound': str(gap(p)/2),
                            'matrix_sha256': matrix_hash(Qr),
                            'full_checked': p == 13}
        result['primes'].append(record)
        print('validated prime', p, 'N', n, file=sys.stderr, flush=True)
    roots, blocks = binary_field16()
    D, s, Qc = centered_certificate(16, blocks)
    check_definition(D, s, Qc, psd=False)
    rank = integer_psd_rank(Qc)
    upper_rank = integer_psd_rank(buffered_upper(Qc, gap(16)))
    assert (len(D), s, rank, upper_rank) == (217, 31, 200, 216)
    result['binary16'] = {'v': 16, 'N': len(D), 's': s, 'roots': roots,
                          'field_modulus': 'X^4+X+1 over F2',
                          'full_lower_rank': rank, 'full_buffered_upper_rank': upper_rank,
                          'gap': str(gap(16)), 'matrix_sha256': matrix_hash(Qc),
                          **incidence_check(16, blocks)}
    Dm, sm, Qm, eta = maximal_certificate(16, blocks, (D, s, Qc))
    assert (Dm, sm) == (D, s)
    check_definition(D, s, Qm, psd=False)
    assert integer_psd_rank(Qm) == 201
    assert integer_psd_rank(buffered_upper(Qm, gap(16)/2)) == 216
    result['binary16']['uniform_maximal'] = {
        'eta': str(eta), 'full_lower_rank': 201, 'full_buffered_upper_rank': 216,
        'gap': str(gap(16)/2), 'Q00': str(Qm[0][0]), 'matrix_sha256': matrix_hash(Qm)}
    result['nonbijective'] = []
    for v in (13, 15):
        blocks, perm = nonbijective_fixture(v)
        D, s, Qc = centered_certificate(v, blocks)
        check_definition(D, s, Qc, psd=False)
        n = len(D)
        assert integer_psd_rank(Qc) == n-v-1
        assert integer_psd_rank(buffered_upper(Qc, gap(v))) == n-1
        _, _, Qm, eta = maximal_certificate(v, blocks, (D, s, Qc))
        check_definition(D, s, Qm, psd=False)
        assert integer_psd_rank(Qm) == n-v
        assert integer_psd_rank(buffered_upper(Qm, gap(v)/2)) == n-1
        pairs, completion, _ = design_data(v, blocks)
        result['nonbijective'].append({
            'v': v, 'N': n, 's': s, 'fixture_permutation': perm,
            'distinct_completion_pairs': len(set(completion.values())),
            'total_pairs': len(pairs), 'centered_rank': n-v-1,
            'maximal_rank': n-v, 'buffered_upper_rank': n-1,
            'centered_gap': str(gap(v)), 'maximal_gap': str(gap(v)/2),
            'eta': str(eta), 'centered_sha256': matrix_hash(Qc),
            'maximal_sha256': matrix_hash(Qm), **incidence_check(v, blocks)})
        print('validated nonbijective', v, 'N', n, file=sys.stderr, flush=True)
    # Malformed mathematical inputs and a corrupted supported entry must fail.
    _, _, blocks, _ = prime_decomposition(13)
    rejects(lambda: centered_certificate(13, blocks[:-1]))
    rejects(lambda: centered_certificate(13, blocks+[blocks[0]]))
    rejects(lambda: weights(12))
    D, s, Qc = centered_certificate(13, blocks)
    Qc[0][1] += 1
    rejects(lambda: check_definition(D, s, Qc, psd=False))
    rejects(lambda: integer_psd_rank([[F(0), F(1)], [F(1), F(0)]]))
    result['rejection_controls'] = 5
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--write-expected', action='store_true')
    args = parser.parse_args()
    assert not (args.check and args.write_expected)
    result = run()
    expected = Path(__file__).with_name('uniform_twofold_expected.json')
    if args.check:
        assert result == json.loads(expected.read_text()), 'expected output mismatch'
    if args.write_expected:
        expected.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps(result, indent=2, sort_keys=True))
