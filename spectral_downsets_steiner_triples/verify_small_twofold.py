"""Exact new-order validation and separate reproduction of old 9-point inputs.

Every full lower form and buffered upper form is checked by integer Schur
congruence. One full input also uses rational Schur on all four forms.
This validates examples; infinite scope rests on the written incidence proof.
CPython3.11+, assertions enabled, standard library. six-downset-2, researcher.
"""
import argparse
import json
import sys
from fractions import Fraction as F
from pathlib import Path

from integer_psd import integer_psd_rank
from small_twofold import fixtures
from twofold_small_identities import run as identities
from uniform_twofold import centered_certificate, design_data, gap, maximal_certificate, weights
from verify import check_definition, exact_psd_rank, matrix_hash, rejects
from verify_three9 import buffered_upper
from verify_two9 import decode
from verify_uniform_twofold import incidence_check


def run():
    out = {'agent': 'six-downset-2', 'role': 'researcher',
           'identities': identities(), 'inputs': [], 'old9_reproduction': []}
    old = json.loads(Path(__file__).with_name('two9_certificates.json').read_text())
    for index, case in enumerate(old['cases']):
        D, Q = decode(old['first_blocks'], case)
        check_definition(D, 17, Q, psd=False)
        upper = [[F(70*int(i == j))-Q[i][j] for j in range(70)] for i in range(70)]
        assert integer_psd_rank(Q) == case['expected_rank_Q'] == 60
        assert integer_psd_rank(upper) == case['expected_rank_upper'] == 69
        out['old9_reproduction'].append({'case_index': index, 'rank': 60,
                                        'upper_rank': 69, 'matrix_sha256': matrix_hash(Q)})
    for name, v, blocks, generation in fixtures():
        D, s, Qc = centered_certificate(v, blocks)
        Dm, sm, Qm, eta = maximal_certificate(v, blocks, (D, s, Qc))
        assert (Dm, sm) == (D, s)
        check_definition(D, s, Qc, psd=False)
        check_definition(D, s, Qm, psd=False)
        n = len(D)
        forms = {'centered': Qc, 'centered_buffer': buffered_upper(Qc, gap(v)),
                 'maximal': Qm, 'maximal_buffer': buffered_upper(Qm, gap(v)/2)}
        ranks = {key: integer_psd_rank(matrix) for key, matrix in forms.items()}
        assert ranks == {'centered': n-v-1, 'centered_buffer': n-1,
                         'maximal': n-v, 'maximal_buffer': n-1}
        if name == 'two_STS9_case_0':
            assert {key: exact_psd_rank(matrix) for key, matrix in forms.items()} == ranks
        pairs, completing, _ = design_data(v, blocks)
        assert len(set(completing.values())) < len(pairs)
        out['inputs'].append({'name': name, 'v': v, 'N': n, 's': s,
                              'blocks': blocks, 'generation': generation,
                              'weights': {key: str(value) for key, value in weights(v).items()},
                              'ranks': ranks, 'centered_gap': str(gap(v)),
                              'maximal_gap': str(gap(v)/2), 'eta': str(eta),
                              'Q00': str(Qm[0][0]),
                              'centered_sha256': matrix_hash(Qc),
                              'maximal_sha256': matrix_hash(Qm),
                              'distinct_completion_pairs': len(set(completing.values())),
                              'total_pairs': len(pairs),
                              'rational_Schur_also_checked': name == 'two_STS9_case_0',
                              'no_two_STS_decomposition': v % 2 == 0,
                              **incidence_check(v, blocks)})
        print('validated', name, 'N', n, 'ranks', ranks, file=sys.stderr, flush=True)
    # Controls expose the malformed-design boundary and the completion term.
    rejects(lambda: weights(8))
    rejects(lambda: gap(8))
    rejects(lambda: centered_certificate(v, blocks[:-1]))
    rejects(lambda: centered_certificate(v, blocks+[blocks[0]]))
    damaged = [row[:] for row in Qc]
    counts = {}
    for pair in completing.values():
        counts[pair] = counts.get(pair, 0)+1
    for i, a in enumerate(D):
        if a.bit_count() != 1:
            continue
        for j, b in enumerate(D):
            if b.bit_count() == 1 and a != b:
                damaged[i][j] -= weights(v)['t']*(counts.get(a | b, 0)-1)
    rejects(lambda: check_definition(D, s, damaged, psd=False))
    rejects(lambda: integer_psd_rank([[F(0), F(1)], [F(1), F(0)]]))
    out['rejection_controls'] = 6
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--write-expected', action='store_true')
    args = parser.parse_args()
    assert not (args.check and args.write_expected)
    out = run()
    expected = Path(__file__).with_name('small_twofold_expected.json')
    if args.check:
        assert out == json.loads(expected.read_text()), 'expected output mismatch'
    if args.write_expected:
        expected.write_text(json.dumps(out, indent=2, sort_keys=True)+'\n')
    print(json.dumps(out, indent=2, sort_keys=True))
