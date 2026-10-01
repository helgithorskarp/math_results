#!/usr/bin/env python3
"""Exact ten-point multiple-pair cap; standard library only.

Checks rational positivity and literal full forced completion, not floating
discovery. The all-real sufficiency/completeness bridge is PROOF.md.
Actual author six-downset-3, role researcher. No external data needed.
"""
import argparse
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
import json
from math import comb
from pathlib import Path

from arithmetic import determinant, matrix_hash, positive
from blocks import blocks
from matrices import construct, parameters, rational, require, scaled_integer_matrix


def sparse_columns(a):
    return [[(i, a[i][j]) for i in range(len(a)) if a[i][j]] for j in range(len(a))]


def apply(columns, v):
    out = [0]*len(columns)
    for j, x in v.items():
        for i, y in columns[j]:
            out[i] += x*y
    return out


def finite_incidence_controls():
    """Finite controls support, but do not prove, the generic counting proof."""
    records, dimensions = [], []
    choose = lambda n, k: comb(n, k) if 0 <= k <= n else 0
    for n in range(7, 12):
        pairs = [a for a in range(1 << n) if a.bit_count() == 2]
        for r in range(3, (n-1)//2+1):
            layer = [a for a in range(1 << n) if a.bit_count() == r]
            inclusion = [sum(int(a & b == a) << j for j, b in enumerate(layer)) for a in pairs]
            point_columns = [sum(int(bool(b & (1 << i))) << j for j, b in enumerate(layer)) for i in range(n)]
            for a in pairs:
                for b in layer:
                    require(int(not a & b) == 1-(a & b).bit_count()+int(a & b == a),
                            'Disjoint2/r identity')
            q, beta, gamma = choose(n-4, r-2), choose(n-4, r-3), choose(n-4, r-4)
            for i, a in enumerate(pairs):
                for j, b in enumerate(pairs):
                    require((inclusion[i] & inclusion[j]).bit_count() ==
                            q*int(i == j)+beta*(a & b).bit_count()+gamma,
                            'Full inclusion Gram identity')
                for point in range(n):
                    require((inclusion[i] & point_columns[point]).bit_count() ==
                            choose(n-3, r-3)+choose(n-3, r-2)*int(bool(a & (1 << point))),
                            'Forward point-incidence lift')
            for b in layer:
                contained = [a for a in pairs if a & b == a]
                for point in range(n):
                    require(sum(bool(a & (1 << point)) for a in contained) ==
                            (r-1)*int(bool(b & (1 << point))), 'Transpose point-incidence lift')
            p = [int(i == 0)-int(i == n-1) for i in range(n)]
            fpair = {a: sum(p[i] for i in range(n) if a >> i & 1) for a in pairs}
            flayer = {a: sum(p[i] for i in range(n) if a >> i & 1) for a in layer}
            require(all(sum(flayer[b] for b in layer if not a & b) ==
                        -comb(n-3, r-1)*fpair[a] for a in pairs), 'Point-standard forward action')
            require(all(sum(fpair[a] for a in pairs if not a & b) ==
                        -(n-r-1)*flayer[b] for b in layer), 'Point-standard transpose action')
            require((n-2)*comb(n-3, r-1) == (n-r-1)*comb(n-2, r-1),
                    'Symmetric standard bilinear coefficient')
            records.append({'n': n, 'r': r, 'q': q, 'disjoint_entries': len(pairs)*len(layer),
                            'Gram_entries': len(pairs)**2, 'forward_point_entries': n*len(pairs),
                            'transpose_point_entries': n*len(layer)})
        possible = list(range(3, (n-1)//2+1))
        for mask in range(1 << len(possible)):
            selected = [r for j, r in enumerate(possible) if mask >> j & 1]
            z = {k: k for k in range(2, n//2+1)}
            _, meta = blocks(n, z, 1, {r: 1 for r in selected})
            literal_middle = sum(2 <= a.bit_count() <= n-2 for a in range(1 << n))
            require(sum(meta['dimensions'].values()) == literal_middle, 'Complete dimension sum')
            dimensions.append({'n': n, 'selected': selected, 'middle_dimension': literal_middle})
    return {'incidence_cases': records, 'all_selected_subsets_dimension_cases': dimensions,
            'generic_validity_uses_counting_proof_not_extrapolation': True}


def literal_checks(n, L, small, meta, c):
    N, s = meta['N'], meta['s']
    members = [a for a in range(1 << n) if a.bit_count() <= n-2]
    index = {a: i for i, a in enumerate(members)}
    middle = [a for a in members if a.bit_count() >= 2]
    m = len(middle); ti = {a: i for i, a in enumerate(middle)}
    H = [[L[index[a]][index[b]] for b in middle] for a in middle]
    Hnum, D = scaled_integer_matrix(H)
    full_num = [[rational(x)*D for x in row] for row in L]
    require(all(x.denominator == 1 for row in full_num for x in row), 'Common full integer scale')
    full_num = [[int(x) for x in row] for row in full_num]
    Hcols = sparse_columns(Hnum)
    R = [[int(bool(a >> i & 1)) for a in middle] for i in range(n)]
    t = [a.bit_count()-1 for a in middle]
    def q_action(v):
        total = sum(v.values())
        return [x-D*total for x in apply(Hcols, v)]
    def g_action(v):
        rv = [sum(row[j]*x for j, x in v.items()) for row in R]
        tv = sum(t[j]*x for j, x in v.items())
        return [v.get(j, 0)+sum(R[i][j]*rv[i] for i in range(n))+t[j]*tv for j in range(m)]
    qt = q_action({i: x for i, x in enumerate(t)})
    qr = [q_action({j: x for j, x in enumerate(row) if x}) for row in R]
    expected = [row[:] for row in full_num]
    expected[0][0] = D+sum(t[j]*qt[j] for j in range(m))
    for i in range(n):
        p = index[1 << i]
        expected[0][p] = expected[p][0] = D-sum(R[i][j]*qt[j] for j in range(m))
        for h in range(n):
            expected[p][index[1 << h]] = D+sum(R[i][j]*qr[h][j] for j in range(m))
        for j, a in enumerate(middle):
            expected[p][index[a]] = expected[index[a]][p] = D-qr[i][j]
    for j, a in enumerate(middle):
        expected[0][index[a]] = expected[index[a]][0] = D+qt[j]
    require(expected == full_num, 'All full entries disagree with independent SQS completion')
    require(len(members) == N and m == N-n-1, 'Literal family dimension')
    require(all(sum(row) == N*D for row in full_num), 'Full row normalization')
    require(all(full_num[i][j] == full_num[j][i] for i in range(N) for j in range(N)), 'Full symmetry')
    require(all(full_num[i][i] == s*D for i in range(1, N)), 'Nonempty diagonal')
    require(all(full_num[i][j] == 0 for i, a in enumerate(members)
                for j, b in enumerate(members) if i != j and a & b), 'Intersecting support')
    star_sizes = []
    for point in range(n):
        star = [j for j, a in enumerate(members) if a >> point & 1]
        star_sizes.append(len(star))
        require(all(sum(row[j] for j in star) == s*D for row in full_num), 'Full star equation')
    require(star_sizes == [s]*n, 'Literal point-star sizes')
    groups = [[ti[a] for a in middle if a.bit_count() == k] for k in meta['layers']]
    constants = [{j: 1 for j in group} for group in groups]
    standard = [{j: int(bool(middle[j] & 1))-int(bool(middle[j] & (1 << (n-1)))) for j in group}
                for group in groups]
    standard = [{j: x for j, x in v.items() if x} for v in standard]
    for name, vectors, q, g, norm in [('constant', constants, small['Q0'], meta['G0'], 1),
                                    ('standard', standard, small['Q1'], meta['G1'], 2)]:
        for j, v in enumerate(vectors):
            qv, gv = q_action(v), g_action(v)
            for i, w in enumerate(vectors):
                require(sum(x*qv[h] for h, x in w.items()) == D*norm*q[i][j], name+' literal Q block')
                require(sum(x*gv[h] for h, x in w.items()) == norm*g[i][j], name+' literal Gram block')
    histogram = {}
    full = (1 << n)-1
    z, epsilon, delta = parameters(n, c['z'], c['epsilon'], c['delta'])
    for i, a in enumerate(middle):
        for j, b in enumerate(middle):
            ka, kb = a.bit_count(), b.bit_count()
            if i == j:
                value = F(s)
            elif a & b:
                value = F(0)
            elif a | b == full:
                value = s-z[ka]
            elif ka == kb == 2:
                value = epsilon
            elif min(ka, kb) == 2 and max(ka, kb) in delta:
                value = delta[max(ka, kb)]
            else:
                value = F(0)
            require(Hnum[i][j] == value*D, 'Literal middle architecture coefficient')
            if i < j and value:
                pair = tuple(sorted((ka, kb)))
                histogram[pair] = histogram.get(pair, 0)+1
    return {'common_integer_denominator': D, 'full_forced_completion_entries': N*N,
            'row_equations': N, 'star_equations': N*n, 'point_star_sizes': star_sizes,
            'literal_constant_standard_Q_and_Gram_entries': 4*(n-3)**2,
            'nonzero_unordered_middle_orbits': [{'sizes': list(pair), 'pairs': count}
                                                for pair, count in sorted(histogram.items())]}, full_num


def verify(c, controls=True):
    require(c['agent'] == 'six-downset-3' and c['role'] == 'researcher', 'Actual author metadata')
    require(type(c['n']) is int and c['n'] == 10, 'Finite certificate is n10')
    require(type(c['N']) is int and c['N'] == 1013, 'Finite cap scale')
    require(type(c['s']) is int and c['s'] == 502, 'Finite star size')
    z, epsilon, delta = parameters(c['n'], c['z'], c['epsilon'], c['delta'])
    require(set(delta) == {3, 4}, 'Finite certificate has selected sizes3,4')
    small, meta = blocks(c['n'], c['z'], c['epsilon'], c['delta'])
    positives = {name: positive(a) for name, a in small.items()}
    require(all(0 < z[k] < 2*c['s'] for k in range(3, c['n']//2+1)), 'Strict residual scalar tests')
    require(sum(meta['dimensions'].values()) == 1002, 'Complete finite middle dimension')
    require(c['expected_slack_ranks'] == {'lower': 1003, 'upper': 1012}, 'Maximal finite ranks')
    result = {'agent': 'six-downset-3', 'role': 'researcher', 'n': 10, 'N': 1013, 's': 502,
              'parameters': {'z': c['z'], 'epsilon': c['epsilon'], 'delta': c['delta']},
              'six_PD_blocks': positives, 'scalar_tests': {str(k): [str(z[k]), str(2*c['s']-z[k])]
                                                          for k in range(3, 6)},
              'complete_middle_dimensions': meta['dimensions'],
              'coupled_layers': meta['coupled_layers'], 'coupled_norms': meta['coupled_norms'],
              'certified_slack_ranks_by_complete_reduction': c['expected_slack_ranks'],
              'trust_boundary': 'Exact rational small-block PD and literal full completion; ordinary real averaging, invariant-subspace completeness and finite congruence proof are unformalized. Author-checked, independently unreviewed.',
              'dense_full_slack_eliminations_completed': 0}
    if controls:
        members, L = construct(c['n'], c['z'], c['epsilon'], c['delta'])
        result['L_sha256'] = matrix_hash(L)
        result['literal_full_checks'], _ = literal_checks(c['n'], L, small, meta, c)
        result['finite_controls'] = finite_incidence_controls()
        result['negative_controls'] = negative_controls(c)
    return result


def negative_controls(c):
    cases = []
    def add(name, change):
        damaged = deepcopy(c); change(damaged); cases.append((name, damaged))
    add('float_coefficient', lambda d: d['delta'].__setitem__('4', .24))
    add('boolean_coefficient', lambda d: d.__setitem__('epsilon', True))
    add('decimal_string', lambda d: d['delta'].__setitem__('4', '0.24'))
    add('zero_denominator', lambda d: d['z'].__setitem__('2', '1/0'))
    add('wrong_order', lambda d: d.__setitem__('n', 9))
    add('wrong_cap_scale', lambda d: d.__setitem__('N', 1012))
    add('wrong_star_size', lambda d: d.__setitem__('s', 501))
    add('missing_orbit', lambda d: d['delta'].pop('4'))
    add('central_layer_alias', lambda d: d['delta'].__setitem__('5', '1'))
    add('duplicate_integer_key', lambda d: d['z'].__setitem__(2, '1'))
    add('negative_residual_parameter', lambda d: d['z'].__setitem__('5', '-1'))
    add('excessive_two_four_weight', lambda d: d['delta'].__setitem__('4', '100'))
    rejected = []
    for name, damaged in cases:
        try:
            verify(damaged, controls=False)
        except (ValueError, KeyError, TypeError, ZeroDivisionError):
            rejected.append(name)
        else:
            raise ValueError('Damaged finite certificate accepted: '+name)
    require(determinant([[0, 1], [1, 0]]) == -1, 'Bareiss pivot control')
    require(determinant([[1, 2], [2, 4]]) == 0, 'Bareiss singular control')
    require(determinant([[3, 1], [1, 2]]) == 5, 'Bareiss PD control')
    return rejected


CERT = json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = verify(CERT)
    result['certificate_sha256'] = sha256(Path(__file__).with_name('CERTIFICATE.json').read_bytes()).hexdigest()
    output = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(output)
    else:
        print(output, end='')


if __name__ == '__main__':
    main()
