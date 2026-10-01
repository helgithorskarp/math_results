#!/usr/bin/env python3
"""Exact standard-library checker; optional independent full-slack elimination.

six-downset-3, researcher. General real completeness is proved in PROOF.md.
"""
import argparse
from fractions import Fraction as Q
from itertools import product
from math import comb, gcd, lcm
from pathlib import Path
import json

from arithmetic import psd_rank, matrix_hash
from blocks import blocks, inverse
from matrices import construct, parameters, rational, require

def reference_lift(n, z, epsilon, delta, members):
    """Construct every full entry from middle Q and the forced-star lift.

    Does not call the production closed-entry formulas or their completion.
    """
    N, s, full = len(members), 2**(n-1)-n, (1 << n)-1
    middle = [a for a in members if a.bit_count() >= 2]
    core = []
    for a in middle:
        row = []
        for b in middle:
            value = Q(s-1) if a == b else Q(-1)
            if b == (full ^ a):
                value += s-z[a.bit_count()]
            elif not a & b and a.bit_count() == b.bit_count() == 2:
                value += epsilon
            elif not a & b and {a.bit_count(), b.bit_count()} == {2, 3}:
                value += delta
            row.append(value)
        core.append(row)
    incidence = [[j for j, a in enumerate(middle) if a >> i & 1] for i in range(n)]
    rq = [[sum(core[j][k] for j in incidence[i]) for k in range(len(middle))]
          for i in range(n)]
    index = {a: i for i, a in enumerate(members)}
    L = [[Q(0) for _ in members] for _ in members]
    for i, a in enumerate(middle):
        for j, b in enumerate(middle):
            L[index[a]][index[b]] = core[i][j]+1
        for point in range(n):
            L[index[1 << point]][index[a]] = L[index[a]][index[1 << point]] = 1-rq[point][i]
    for i in range(n):
        for j in range(n):
            L[index[1 << i]][index[1 << j]] = 1+sum(rq[i][k] for k in incidence[j])
    for i in range(1, N):
        L[0][i] = L[i][0] = N-sum(L[i][1:])
    L[0][0] = N-sum(L[0][1:])
    return L, middle, core


def literal_block_checks(n, middle, core, g0, g1, expected):
    layers = list(range(2, n-1)); d = len(layers)
    sizes = [layers.index(a.bit_count()) for a in middle]
    signs = [int(bool(a & 1))-int(bool(a & 2)) for a in middle]
    literal0 = [[Q(0) for _ in layers] for _ in layers]
    literal1 = [[Q(0) for _ in layers] for _ in layers]
    for i, a in enumerate(middle):
        for j, b in enumerate(middle):
            literal0[sizes[i]][sizes[j]] += core[i][j]
            literal1[sizes[i]][sizes[j]] += signs[i]*signs[j]*core[i][j]
    require(literal0 == expected['Q0'], 'constant Q block differs')
    require(literal1 == [[2*x for x in row] for row in expected['Q1']], 'standard Q block differs')
    images0, images1 = [], []
    for k in layers:
        group = [i for i, a in enumerate(middle) if a.bit_count() == k]
        images0.append([sum(middle[i].bit_count()-1 for i in group)]
                       +[-sum(int(bool(middle[i] >> point & 1)) for i in group) for point in range(n)]
                       +[int(i in group) for i in range(len(middle))])
        images1.append([sum((k-1)*signs[i] for i in group)]
                       +[-sum(signs[i] for i in group if middle[i] >> point & 1) for point in range(n)]
                       +[signs[i] if i in group else 0 for i in range(len(middle))])
    gram = lambda vectors: [[sum(x*y for x, y in zip(a, b)) for b in vectors] for a in vectors]
    require(gram(images0) == g0, 'constant Gram block differs')
    require(gram(images1) == [[2*x for x in row] for row in g1], 'standard Gram block differs')
    return 4*d*d


def check_definition(n, members, L):
    N, s = len(members), 2**(n-1)-n
    require(N == 2**n-n-1 and members[0] == 0, 'complete canonical vertex set')
    for i, a in enumerate(members):
        require(sum(L[i]) == N, 'row normalization')
        require(a == 0 or L[i][i] == s, 'nonempty diagonal')
        for j, b in enumerate(members):
            require(L[i][j] == L[j][i], 'symmetry')
            require(i == j or not a & b or L[i][j] == 0, 'intersecting support')
        for point in range(n):
            require(sum(L[i][j] for j, b in enumerate(members) if b >> point & 1) == s, 'forced star equation')
    star_gram = [[sum(int(bool(a >> i & 1) and bool(a >> j & 1)) for a in members)-Q(s*s, N)
                  for j in range(n)] for i in range(n)]
    require(psd_rank(star_gram) == n, 'centered stars independent')



def incidence_controls():
    records = []
    for n in range(7, 12):
        pairs = [a for a in range(1 << n) if a.bit_count() == 2]
        triples = [a for a in range(1 << n) if a.bit_count() == 3]
        U = [[int(a & b == a) for a in pairs] for b in triples]
        for i, a in enumerate(pairs):
            for j, c in enumerate(pairs):
                require(sum(row[i]*row[j] for row in U) == (n-4)*int(i == j)+(a & c).bit_count(), 'U Gram')
            for t, b in enumerate(triples):
                require(int(not a & b) == 1-(a & b).bit_count()+U[t][i], 'D23 identity')
            for point in range(n):
                require(sum(U[t][i] for t, b in enumerate(triples) if b >> point & 1) == 1+(n-3)*int(bool(a >> point & 1)), 'R3 U')
        sizes = [comb(n, k) for k in range(2, n-1)]
        w2, z3 = comb(n, 2)-n, comb(n, 3)-comb(n, 2)
        remaining = sum(comb(n, k)-n for k in range(4, n-3))
        m = 2**n-2*n-2
        dimensions = [n-3, (n-1)*(n-3), 4*w2, 2*z3, remaining]
        require(sum(dimensions) == m and z3 > 0 and w2 > 0, 'complete dimensions')
        f = [int(a in (3, 12))-int(a in (5, 10)) for a in pairs]
        require(all(sum(f[i] for i, a in enumerate(pairs) if a >> point & 1) == 0 for point in range(n)), 'f in W2')
        uf = [sum(row[i]*f[i] for i in range(len(f))) for row in U]
        require(all(sum(uf[t] for t, b in enumerate(triples) if b >> point & 1) == 0 for point in range(n)), 'Uf in W3')
        require(sum(x*x for x in uf) == (n-4)*sum(x*x for x in f), 'lift norm')
        full = (1 << n)-1
        vectors = [dict((a, f[i]) for i, a in enumerate(pairs) if f[i]),
                   dict((b, uf[t]) for t, b in enumerate(triples) if uf[t])]
        vectors += [{full ^ b: v for b, v in vectors[1].items()},
                    {full ^ a: v for a, v in vectors[0].items()}]
        z, e, d = parameters(n, {k: str(Q(3*k+1, 7)) for k in range(2, n//2+1)}, '2/5', '3/11')
        expected, _, _ = blocks(n, z, e, d)
        s = 2**(n-1)-n
        def entry(a, b):
            value = Q(s-1) if a == b else Q(-1)
            if a ^ b == full:
                value += s-z[a.bit_count()]
            elif not a & b:
                if a.bit_count() == b.bit_count() == 2:
                    value += e
                elif {a.bit_count(), b.bit_count()} == {2, 3}:
                    value += d
            return value
        actual = [[sum(x*y*entry(a, b) for a, x in v.items() for b, y in w.items()) for w in vectors] for v in vectors]
        require(actual == [[4*x for x in row] for row in expected['C2']], 'literal coupled block')
        records.append({'n': n, 'dimensions': dimensions, 'D23_entries': len(pairs)*len(triples), 'U_Gram_entries': len(pairs)**2, 'R3U_entries': n*len(pairs), 'coupled_entries': 16})
    return records


def schur_polynomials(n, z, epsilon):
    """Primitive integer quadratics whose positivity is exactly the six tests.

    All first-coordinate principal remainders must be positive definite.
    This condition is checked and is not assumed on singular boundary faces.
    """
    a0, _, _ = blocks(n, z, epsilon, Q(0))
    a1, _, _ = blocks(n, z, epsilon, Q(1))
    answer = {}
    for name, a in a0.items():
        b = [row[1:] for row in a[1:]]
        require(psd_rank(b) == len(b), 'Schur remainder not positive definite')
        require(a1[name][0][0] == a[0][0], 'delta changes diagonal')
        require([row[1:] for row in a1[name][1:]] == b, 'delta changes remainder')
        inv = inverse(b)
        c = a[0][1:]
        d = [a1[name][0][j]-a[0][j] for j in range(1, len(a))]
        form = lambda x, y: sum(x[i]*inv[i][j]*y[j] for i in range(len(x)) for j in range(len(y)))
        coefficients = [a[0][0]-form(c, c), -2*form(c, d), -form(d, d)]
        scale = lcm(*(x.denominator for x in coefficients))
        integers = [int(scale*x) for x in coefficients]
        divisor = gcd(*integers)
        require(divisor > 0, 'identically zero Schur polynomial')
        answer[name] = {'coefficients_ascending': [x//divisor for x in integers],
                        'positive_scale': str(Q(divisor, scale)),
                        'remainder_rank': len(b)}
    return answer


def negative_controls():
    rejected = []
    def reject(name, function):
        try:
            function()
        except (ValueError, ZeroDivisionError):
            rejected.append(name)
        else:
            raise ValueError('corrupt input accepted: '+name)
    reject('float_coefficient', lambda: rational(0.345))
    reject('decimal_coefficient', lambda: rational('0.345'))
    reject('aliased_six_point_layers', lambda: construct(6, {2: 1, 3: 1}, 0, 0))
    reject('missing_complement_orbit', lambda: construct(9, {2: 6, 3: 2}, 0, 1))
    reject('excess_complement_orbit', lambda: construct(9, {2: 6, 3: 2, 4: 2, 5: 2}, 0, 1))
    reject('nonreflected_block_weights', lambda: blocks(9, {k: Q(k) for k in range(2, 8)}, 0, 1))
    reject('zero_diagonal_indefinite', lambda: psd_rank([[0, 1], [1, 0]]))
    reject('asymmetric_PSD_input', lambda: psd_rank([[1, 1], [0, 1]]))
    z, e, _ = parameters(9, {2: '49/8', 3: '53/20', 4: '21/10'}, 0, '69/200')
    bad, _, _ = blocks(9, z, e, 0)
    reject('removed_two_triple_orbit', lambda: psd_rank(bad['Q0']))
    # Bad metric normalization in the coupled upper block must be detectable.
    good, _, _ = blocks(9, z, e, '69/200')
    wrong = [[Q(502 if i == j else 0)-good['C2'][i][j] for j in range(4)] for i in range(4)]
    reject('forgotten_lift_norm_in_upper_block', lambda: psd_rank(wrong))
    members, L = construct(9, {2: '49/8', 3: '53/20', 4: '21/10'}, 0, '69/200')
    index = {a: i for i, a in enumerate(members)}
    L[index[1]][index[3]] = L[index[3]][index[1]] = Q(1)
    reject('corrupted_intersecting_entry', lambda: check_definition(9, members, L))
    psd_count = 0
    for entries in product((-1, 0, 1), repeat=6):
        a, b, c, d, e, f = entries
        matrix = [[a, b, c], [b, d, e], [c, e, f]]
        expected = (a >= 0 and d >= 0 and f >= 0 and a*d-b*b >= 0
                    and a*f-c*c >= 0 and d*f-e*e >= 0
                    and a*(d*f-e*e)-b*(b*f-c*e)+c*(b*e-c*d) >= 0)
        try:
            rank = psd_rank(matrix)
            actual = True
            require(0 <= rank <= 3, 'rank range')
        except ValueError:
            actual = False
        require(actual == expected, 'ternary principal-minor mismatch')
        psd_count += actual
    return {'rejected': rejected, 'ternary_3x3_matrices': 729, 'ternary_PSD_count': psd_count}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--full-psd', action='store_true', help='Eliminate both entire 502x502 rational slacks')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    n, raw_z, raw_e, raw_d = 9, {2: '49/8', 3: '53/20', 4: '21/10'}, 0, '69/200'
    z, e, d = parameters(n, raw_z, raw_e, raw_d)
    N, s, m = 2**n-n-1, 2**(n-1)-n, 2**n-2*n-2
    small, g0, g1 = blocks(n, z, e, d)
    ranks = {name: psd_rank(a) for name, a in small.items()}
    require(all(ranks[name] == len(a) for name, a in small.items()), 'strict block failure')
    require(all(0 < z[k] < 2*s for k in range(3, n//2+1)), 'strict residual bounds')
    polynomials = schur_polynomials(n, z, e)
    for name, certificate in polynomials.items():
        c = certificate['coefficients_ascending']
        require(sum(Q(x)*d**i for i, x in enumerate(c)) > 0, 'Schur certificate fails')
        certificate['value_at_delta'] = str(sum(Q(x)*d**i for i, x in enumerate(c)))
    members, L = construct(n, raw_z, raw_e, raw_d)
    other, middle, core = reference_lift(n, z, e, d, members)
    require(L == other, 'closed entries differ from independent forced lift')
    del other
    check_definition(n, members, L)
    literal_count = literal_block_checks(n, middle, core, g0, g1, small)
    result = {'author': {'agent': 'six-downset-3', 'role': 'researcher'},
              'status': 'Exact rational checks plus written unformalized all-real reduction; independently unreviewed.',
              'n': n, 'N': N, 's': s, 'middle': m,
              'parameters': {'z': {str(k): str(z[k]) for k in range(2, n//2+1)}, 'epsilon': str(e), 'delta': str(d)},
              'strict_block_ranks': ranks, 'Schur_polynomials': polynomials,
              'derived_lower_rank': N-n, 'derived_upper_rank': N-1,
              'full_entry_comparisons': N*N, 'literal_Q_and_Gram_entries': literal_count,
              'L_sha256': matrix_hash(L),
              'blocks_sha256': {name: matrix_hash(a) for name, a in small.items()},
              'incidence_controls': incidence_controls(), 'negative_controls': negative_controls()}
    if args.full_psd:
        lower = psd_rank(L)
        upper = psd_rank([[Q(N if i == j else 0)-L[i][j] for j in range(N)] for i in range(N)])
        require(lower == N-n and upper == N-1, 'full slack ranks differ')
        result['independent_full_slack_ranks'] = {'lower': lower, 'upper': upper}
    text = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
