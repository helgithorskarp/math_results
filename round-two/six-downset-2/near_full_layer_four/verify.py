"""Exact n17 support threshold, centered seed, and full cap repair checks.

Author six-downset-2, researcher. All inputs are compact rational data;
neither a floating search nor a solver status is part of this proof.
"""
import argparse
import copy
from fractions import Fraction as Q
import hashlib
import json
from math import comb, isqrt
from pathlib import Path

from exact import both
from model import affine, blocks, choose, original, parameters, require, trade
from shared import (arithmetic_audit, decoded, digest, projection_gram,
                    rational_strings, rejected)

ROOT = Path(__file__).resolve().parent


def basis_audit():
    meta, recover = affine(17)
    require(meta['affine_rank'] == 29 and len(meta['pairs']) == 71
            and len(meta['free_pairs']) == 42, 'Full real-affine dimensions')
    require(meta['free_pairs'] == [(a, b) for a in range(3, 16)
            for b in range(a, 16) if a+b <= 17], 'Full middle free-coordinate census')
    for index in range(-1, 42):
        values = [Q(0)]*42
        if index >= 0:
            values[index] = Q(1)
        beta = decoded(17, meta, recover, values)
        require(all(beta[a][b] == v for (a, b), v in zip(meta['free_pairs'], values)),
                'Every specified free coordinate retained')
    return {'supported_coordinates': 71, 'affine_rank': 29,
            'free_middle_coordinates': 42, 'independent_decoder_basis_checks': 43,
            'original_moment_equations_per_check': 30}


def seed_fixture(doc):
    require((doc['n'], doc['r'], doc['N'], doc['s']) == (17, 15, 131054, 65519),
            'Fixed seventeen-point seed domain')
    require(doc['largest_active_layer'] == 4 and doc['common_denominator'] == 10**6,
            'Seed support and denominator declarations')
    require(doc['repair_endpoint'] == '1/27720'
            and doc['seed_projected_lower_floor'] == '1/2'
            and doc['seed_upper_floor'] == '1/4' and doc['repair_upper_floor'] == '1/8',
            'Seed and repair floor conventions')
    meta, recover = affine(17)
    require(doc['free_pairs'] == [list(p) for p in meta['free_pairs']],
            'Complete seed free-pair census')
    values = rational_strings(doc['free_values'])
    require(all(10**6 % v.denominator == 0 for v in values), 'Seed common denominator')
    for (a, b), v in zip(meta['free_pairs'], values):
        require(a+b == 17 or a <= 4 or v == 0, 'Forbidden seed noncomplement coupling')
    noncomp = [(a, b) for (a, b), v in zip(meta['free_pairs'], values) if a+b < 17 and v]
    require(len(noncomp) == 20 and max(a for a, b in noncomp) == 4,
            'Attained active layer four and twenty middle noncomplement orbits')
    return meta, decoded(17, meta, recover, values)


def seed_checks(doc):
    meta, beta = seed_fixture(doc)
    n, N, s = 17, meta['N'], meta['s']
    endpoint = Q(doc['repair_endpoint'])
    require(endpoint == Q(1, 4*(n-2)*(n-3)*(2*n-1)), 'Exact credited repair parameter')
    rows = [sum(trade(n, a, b)*choose(n-a, b) for b in range(1, 16))
            for a in range(1, 16)]
    require(rows == [1680, -105]+[0]*13, 'Actual trade row sums')
    require(sum(comb(n, a)*v for a, v in enumerate(rows, 1)) == 14280,
            'Actual empty diagonal update')
    require(all(sum(trade(n, a, b)*choose(n-a-1, b-1) for b in range(1, 16)) == 0
                for a in range(1, 16)), 'Trade preserves each excluding-point star')
    records = []
    for t in (Q(0), endpoint):
        order_total, rank_total, details = 0, 0, []
        for j, aa, g, K, U in blocks(n, beta, t):
            d = len(aa)
            require(g == [comb(n-2*j, a-j) for a in aa] and all(v > 0 for v in g),
                    'Complete-sector positive Gram metric')
            if j == 0:
                require(all(sum(v*aa[k] for k, v in enumerate(row)) == 0 for row in K),
                        'Degree-zero cardinality kernel')
            if j == 1 or j == 0 and not t:
                require(all(sum(row) == 0 for row in K), 'Point/center block kernel')
            expected = d-(2 if j == 0 and not t else 1 if j in (0, 1) else 0)
            lower = [[g[i]*v for v in row] for i, row in enumerate(K)]
            both(lower, expected)
            if not t:
                P = projection_gram(g, aa, j)
                both([[lower[i][k]-Q(1, 2)*P[i][k] for k in range(d)] for i in range(d)])
            floor = Q(1, 4) if not t else Q(1, 8)
            upper = [[g[i]*(v-floor*int(i == k)) for k, v in enumerate(row)]
                     for i, row in enumerate(U)]
            both(upper, d)
            multiplicity = comb(n, j)-(comb(n, j-1) if j else 0)
            order_total += multiplicity*d
            rank_total += multiplicity*expected
            details.append({'j': j, 'layers': aa, 'multiplicity': multiplicity,
                'lower_rank': expected, 'upper_gap_rank': d,
                'lower_sha256': digest(lower), 'upper_gap_sha256': digest(upper)})
        require(len(details) == 9 and order_total == N-1, 'Every original sector covered')
        require(rank_total+1 == N-n-(not t), 'Full lower rank at seed/endpoint')
        records.append({'t': str(t), 'full_lower_rank': rank_total+1,
            'full_upper_rank': N-1, 'upper_nonzero_floor': str(floor),
            'actual_empty_L_diagonal': str(1+14280*t),
            'actual_empty_M_loop': str(Q(1+14280*t-s, N-s)),
            'actual_empty_L_singleton_entry': str(1-1680*t),
            'actual_empty_L_two_set_entry': str(1+105*t), 'sectors': details})
    return {'n': n, 'r': 15, 'N': N, 's': s,
            'nonzero_middle_noncomplement_orbits': 20, 'attained_active_layer': 4,
            'seed_projected_lower_floor': '1/2', 'parameters': records,
            'real_interval_bridge': 'Convexity and the explicitly checked common star kernels'}


def constant_forms(n, beta):
    """Direct original layer-vector quadratic forms, not a PSD extrapolation."""
    r, N, s = parameters(n)
    g = [comb(n, a) for a in range(1, r+1)]
    scales = [isqrt(v) for v in g]
    K = [[Q(s*int(a == b)-comb(n, b))
          +beta[a][b]*choose(n-a, b) for b in range(1, r+1)] for a in range(1, r+1)]
    U = [[Q((N-s)*int(a == b))-beta[a][b]*choose(n-a, b)
          for b in range(1, r+1)] for a in range(1, r+1)]
    forms = [[[Q(g[i]*v, s*scales[i]*scales[k]) for k, v in enumerate(row)]
              for i, row in enumerate(A)] for A in (K, U)]
    for A in forms:
        require(all(A[i][k] == A[k][i] for i in range(r) for k in range(r)),
                'Direct rational constant-form symmetry')
    return scales, forms


def dual_checks(doc):
    require(doc['n'] == 17 and doc['largest_active_layer'] == 3
            and doc['degrees'] == [0] and doc['matrix_roles'] == [[0, 'lower'], [0, 'upper']],
            'Fixed degree-zero two-sided obstruction domain')
    require(doc['grid_denominator'] == 10**12 and doc['recovery_equation_rank'] == 18,
            'Recorded recovery metadata')
    meta, recover = affine(17)
    pairs = [p for p in meta['free_pairs'] if sum(p) == 17 or p[0] <= 3]
    require(len(pairs) == 17 and doc['allowed_free_pairs'] == [list(p) for p in pairs],
            'All seventeen real permitted middle coordinates')
    Y = [[rational_strings(row) for row in matrix] for matrix in doc['Y']]
    require(len(Y) == 2 and all(len(A) == 15 and all(len(row) == 15 for row in A) for A in Y),
            'Dual matrix dimensions')
    floor = Q(doc['positive_definite_floor'])
    require(floor == Q(1, 200000000), 'Exact dual positive floor')
    for A in Y:
        both(A, 15)
        both([[v-floor*int(i == k) for k, v in enumerate(row)]
              for i, row in enumerate(A)], 15)
    require(sum(Y[j][i][i] for j in range(2) for i in range(15)) == 1, 'Combined dual trace')
    base_values = [Q(meta['s']) if sum(p) == 17 else Q(0) for p in meta['free_pairs']]
    base_beta = decoded(17, meta, recover, base_values)
    scales, base = constant_forms(17, base_beta)
    require(doc['scales'] == [scales, scales], 'Direct dual metric scales')
    _, aa, g, K, U = blocks(17, base_beta)[0]
    require(base == [[[Q(g[i]*v, meta['s']*scales[i]*scales[k]) for k, v in enumerate(row)]
                       for i, row in enumerate(A)] for A in (K, U)],
            'Direct original form versus harmonic degree-zero decoder')
    def pairing(forms):
        return sum(Y[j][i][k]*forms[j][i][k] for j in range(2)
                   for i in range(15) for k in range(15))
    coefficients = []
    for pair in pairs:
        values = list(base_values)
        values[meta['free_pairs'].index(pair)] += 1
        _, changed = constant_forms(17, decoded(17, meta, recover, values))
        coefficient = pairing(changed)-pairing(base)
        require(coefficient == 0, 'Exact coefficient of an arbitrary real face coordinate')
        coefficients.append(str(coefficient))
    constant = pairing(base)
    require(constant == Q(doc['dual_constant']) and constant < Q(-1, 10000),
            'Strict negative two-sided dual constant')
    return {'orders': [15, 15], 'roles': ['lower degree0', 'upper degree0'],
        'permitted_noncomplement_orbits': 11, 'permitted_complement_orbits': 6,
        'zero_coefficients': coefficients, 'constant': str(constant),
        'constant_below': '-1/10000', 'positive_definite_floor': str(floor),
        'Y_sha256': [digest(A) for A in Y],
        'base_form_sha256': [digest(A) for A in base]}


def literal_checks(n, F, C, L):
    _, N, s = parameters(n)
    require(len(L) == N and all(sum(row) == N for row in L), 'Original full row sums')
    require(all(sum(row) == 0 for row in C), 'Original centering')
    for i, A in enumerate([0]+F):
        for k, B in enumerate([0]+F):
            require(L[i][k] == L[k][i], 'Original symmetry')
            if A & B:
                require(L[i][k] == s*int(i == k), 'Original intersecting support')
    for point in range(n):
        x = [int(bool(A & (1 << point))) for A in F]
        require(sum(x) == s and all(sum(v*x[k] for k, v in enumerate(row)) == 0 for row in C),
                'Every original star size/kernel')


def literal_control():
    meta, recover = affine(7)
    require(meta['free_pairs'] == [(3, 3), (3, 4)], 'Seven-point literal control coordinates')
    beta = decoded(7, meta, recover, [Q(1, 7), Q(55)])
    F, C, L = original(7, beta)
    literal_checks(7, F, C, L)
    _, aa, g, K, U = blocks(7, beta)[0]
    N = meta['N']
    for i, A in enumerate(F):
        a = A.bit_count()
        for k, b in enumerate(aa):
            actual = sum(v for v, B in zip(C[i], F) if B.bit_count() == b)
            require(actual == K[aa.index(a)][k], 'Literal constant-vector lower action')
            actual_upper = N*int(a == b)-comb(7, b)-actual
            require(actual_upper == U[aa.index(a)][k], 'Literal constant-vector upper action')
    scales, direct = constant_forms(7, beta)
    require(direct == [[[Q(g[i]*v, meta['s']*scales[i]*scales[k]) for k, v in enumerate(row)]
                       for i, row in enumerate(A)] for A in (K, U)],
            'Literal action versus direct negative-proof forms')
    return {'n': 7, 'original_order': N, 'full_L_sha256': digest(L),
        'action_rows': 2*len(F)*len(aa), 'star_kernels': 7,
        'original_empty_M_loop': str(Q(1-meta['s'], N-meta['s'])),
        'affine_control_only_PSD_not_claimed': True}


def controls(seed, dual):
    cases = []
    bad = copy.deepcopy(seed)
    bad['free_values'].pop()
    require(rejected(lambda: seed_fixture(bad)), 'Omitted seed coordinate control')
    cases.append('omitted seed coordinate')
    bad = copy.deepcopy(seed)
    bad['free_values'][0] = 0.5
    require(rejected(lambda: seed_fixture(bad)), 'Float seed coordinate control')
    cases.append('floating seed coordinate')
    bad = copy.deepcopy(seed)
    index = bad['free_pairs'].index([5, 5])
    bad['free_values'][index] = '1'
    require(rejected(lambda: seed_fixture(bad)), 'Forbidden middle support control')
    cases.append('forbidden size5 noncomplement coupling')
    bad = copy.deepcopy(seed)
    bad['free_values'][0] = '1000000000'
    require(rejected(lambda: seed_checks(bad)), 'False lower PSD certificate control')
    cases.append('damaged lower seed')
    bad = copy.deepcopy(dual)
    bad['Y'][0][0][0] = '-1'
    require(rejected(lambda: dual_checks(bad)), 'Negative dual PSD control')
    cases.append('negative dual diagonal')
    bad = copy.deepcopy(dual)
    bad['Y'][0][0][1] = bad['Y'][0][1][0] = str(Q(bad['Y'][0][0][1])+Q(1, 1000))
    require(rejected(lambda: dual_checks(bad)), 'False cancellation/PSD control')
    cases.append('changed dual offdiagonal')
    bad = copy.deepcopy(dual)
    bad['allowed_free_pairs'].pop()
    require(rejected(lambda: dual_checks(bad)), 'Incomplete face census control')
    cases.append('omitted permitted complement coordinate')
    bad = copy.deepcopy(dual)
    bad['dual_constant'] = '-1'
    require(rejected(lambda: dual_checks(bad)), 'False dual constant control')
    cases.append('false declared dual constant')
    bad = copy.deepcopy(dual)
    bad['scales'][0][0] += 1
    require(rejected(lambda: dual_checks(bad)), 'Wrong physical metric control')
    cases.append('changed constant-sector metric scale')
    meta, recover = affine(7)
    F, C, L = original(7, recover([Q(1, 7), Q(55)]))
    L[0][0] += 1
    require(rejected(lambda: literal_checks(7, F, C, L)), 'Original empty-loop control')
    cases.append('changed original empty loop')
    require(rejected(lambda: original(17, seed_fixture(seed)[1])), 'Large literal allocation guard')
    cases.append('forbidden full-order literal allocation')
    return cases


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    seed = json.loads((ROOT/'seed.json').read_text())
    dual = json.loads((ROOT/'dual.json').read_text())
    result = {'agent': 'six-downset-2', 'role': 'researcher',
        'claim': 'Least active noncomplement layer is exactly4 for real centered capped H on D(17,15)',
        'proof_status': 'Exact rational certificates; ordinary bridges unformalized; independent review unclaimed',
        'full_affine_basis': basis_audit(), 'seed_and_repair': seed_checks(seed),
        'dual': dual_checks(dual), 'literal_control': literal_control(),
        'arithmetic_audit': arithmetic_audit(), 'rejected_controls': controls(seed, dual),
        'seed_sha256': hashlib.sha256((ROOT/'seed.json').read_bytes()).hexdigest(),
        'dual_sha256': hashlib.sha256((ROOT/'dual.json').read_bytes()).hexdigest(),
        'no_literal_n17_matrix': True, 'arithmetic': 'CPython integers and fractions.Fraction'}
    body = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.check:
        require(body == args.check.read_text(), 'Entire frozen expected record mismatch')
    if args.output:
        args.output.write_text(body)
    print(json.dumps({'ok': True, 'result_sha256': hashlib.sha256(body.encode()).hexdigest(),
        'n': 17, 'least_active_layer': 4, 'complete_seed_endpoint_blocks': 18,
        'dual_orders': [15, 15], 'literal_order': 120,
        'controls': len(result['rejected_controls'])}, sort_keys=True))


if __name__ == '__main__':
    main()
