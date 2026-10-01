#!/usr/bin/env python3
"""Complete canonical integer basis and literal full actions at order ten.

This checker covers every finite direction. It does not extrapolate or do
dense full-slack elimination. Positivity uses the checked small forms and
ordinary finite congruence in PROOF.md. Author six-downset-3, researcher.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from math import gcd, lcm
from pathlib import Path

from arithmetic import matrix_hash, positive, positive_ldl
from blocks import blocks
from matrices import construct, parameters, require, scaled_integer_matrix


def nullspace(a):
    """Exact RREF, then primitive integer vectors with diagonal free witnesses."""
    original = [row[:] for row in a]
    rows = [[F(x) for x in row] for row in a]
    require(rows and rows[0] and all(len(row) == len(rows[0]) for row in rows), 'Kernel shape')
    pivots = []
    for j in range(len(rows[0])):
        r = len(pivots)
        pivot = next((i for i in range(r, len(rows)) if rows[i][j]), None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        scale = rows[r][j]; rows[r] = [x/scale for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][j]:
                scale = rows[i][j]
                rows[i] = [x-scale*y for x, y in zip(rows[i], rows[r])]
        pivots.append(j)
        if len(pivots) == len(rows):
            break
    require(all(not any(row) for row in rows[len(pivots):]), 'Unaccounted kernel row')
    free = [j for j in range(len(rows[0])) if j not in pivots]
    vectors, witnesses = [], []
    for j in free:
        raw = {j: F(1)}
        for i, k in enumerate(pivots):
            if rows[i][j]:
                raw[k] = -rows[i][j]
        scale = lcm(*(x.denominator for x in raw.values()))
        v = {k: int(x*scale) for k, x in raw.items()}
        divisor = gcd(*v.values()); v = {k: x//divisor for k, x in v.items()}
        require(v[j] > 0 and all(v.get(k, 0) == (v[j] if k == j else 0) for k in free),
                'Free-coordinate independence witness')
        require(all(sum(row[k]*x for k, x in v.items()) == 0 for row in original), 'Original kernel equation')
        vectors.append(v); witnesses.append(v[j])
    return vectors, {'rows': len(a), 'columns': len(a[0]), 'rank': len(pivots), 'nullity': len(free),
                     'pivot_columns': pivots, 'free_columns': free, 'free_diagonal': witnesses}


def combine(vectors, coefficients):
    out = {}
    for v, c in zip(vectors, coefficients):
        if c:
            for i, x in v.items():
                out[i] = out.get(i, 0)+c*x
    return {i: x for i, x in out.items() if x}


def dot(v, w):
    return sum(x*w.get(i, 0) for i, x in v.items())


def equal(actual, expected, dimension, message):
    require(len(actual) == dimension and all(x == expected.get(i, 0) for i, x in enumerate(actual)), message)


def sparse_columns(a):
    return [[(i, a[i][j]) for i in range(len(a)) if a[i][j]] for j in range(len(a))]


def apply(columns, v):
    out = [0]*len(columns)
    for j, x in v.items():
        for i, y in columns[j]:
            out[i] += x*y
    return out


def integral(x):
    x = F(x); require(x.denominator == 1, 'Integral action coefficient required')
    return x.numerator


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    c = json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text())
    n, N, s, m = 10, 1013, 502, 1002
    require(c['n'] == n and c['N'] == N and c['s'] == s, 'Finite n10 certificate required')
    z, epsilon, delta = parameters(n, c['z'], c['epsilon'], c['delta'])
    small, meta = blocks(n, c['z'], c['epsilon'], c['delta'])
    require(all(positive(a)['rank'] == len(a) for a in small.values()), 'Strict six-block failure')
    require(all(0 < z[k] < 2*s for k in (3, 4, 5)), 'Strict scalar failure')
    members, L = construct(n, c['z'], c['epsilon'], c['delta'])
    full_num, D = scaled_integer_matrix(L)
    require(D == 50, 'Published integer matrix scale')
    full = (1 << n)-1
    index = {a: i for i, a in enumerate(members)}
    middle = [a for a in members if a.bit_count() >= 2]
    ti = {a: i for i, a in enumerate(middle)}
    layers = {k: [a for a in middle if a.bit_count() == k] for k in range(2, 9)}
    incidence = lambda sets: [[int(bool(a >> i & 1)) for a in sets] for i in range(n)]
    R, t = incidence(middle), [a.bit_count()-1 for a in middle]
    Hnum = [[full_num[index[a]][index[b]] for b in middle] for a in middle]
    Hcols, Lcols = sparse_columns(Hnum), sparse_columns(full_num)
    def q_action(v):
        total = sum(v.values())
        return [x-D*total for x in apply(Hcols, v)]
    def g_action(v):
        rv = [sum(row[j]*x for j, x in v.items()) for row in R]
        tv = sum(t[j]*x for j, x in v.items())
        return [v.get(j, 0)+sum(R[i][j]*rv[i] for i in range(n))+t[j]*tv for j in range(m)]
    def lift(v):
        out = {index[middle[j]]: x for j, x in v.items()}
        out[0] = sum(t[j]*x for j, x in v.items())
        for i in range(n):
            out[index[1 << i]] = -sum(R[i][j]*x for j, x in v.items())
        return {i: x for i, x in out.items() if x}
    def complement(v):
        return {ti[full ^ middle[j]]: x for j, x in v.items()}
    def embed(sets, v):
        return {ti[sets[j]]: x for j, x in v.items()}
    constants = [{ti[a]: 1 for a in layers[k]} for k in layers]
    families = [('constant', constants, small['Q0'], meta['G0'], meta['b'])]
    point_vectors = []
    for i in range(n-1):
        vectors = [{ti[a]: int(bool(a >> i & 1))-int(bool(a >> (n-1) & 1)) for a in layers[k]}
                   for k in layers]
        vectors = [{j: x for j, x in v.items() if x} for v in vectors]
        point_vectors.append(vectors)
        families.append(('point'+str(i), vectors, small['Q1'], meta['G1'], meta['alpha']))
    layer_ranks = []
    for j, k in enumerate(layers):
        rr = incidence(layers[k])
        positive_ldl([[sum(x*y for x, y in zip(row, other)) for other in rr] for row in rr])
        directions = [constants[j]]+[v[j] for v in point_vectors]
        positive_ldl([[dot(v, w) for w in directions] for v in directions])
        require(all(dot(constants[j], v[j]) == 0 for v in point_vectors), 'Constant/point orthogonality')
        layer_ranks.append({'layer': k, 'size': len(layers[k]), 'incidence_rank': n, 'constant_point_rank': n})
    pair_basis, pair_witness = nullspace(incidence(layers[2]))
    require(len(pair_basis) == 35, 'Complete W2 dimension')
    pair_embedded = [embed(layers[2], f) for f in pair_basis]
    lifted, remainders, inclusion_witness = {}, {}, {}
    for r in (3, 4):
        U = [[int(a & b == a) for a in layers[2]] for b in layers[r]]
        Z, witness = nullspace([list(row) for row in zip(*U)])
        require(witness['rank'] == 45 and len(Z) == len(layers[r])-45, 'Full inclusion rank/remainder dimension')
        inclusion_witness[str(r)] = witness
        lifts = [{ti[b]: sum(U[j][h]*x for h, x in f.items()) for j, b in enumerate(layers[r])}
                 for f in pair_basis]
        lifts = [{j: x for j, x in v.items() if x} for v in lifts]
        q = 6 if r == 3 else 15
        for i, v in enumerate(lifts):
            require(all(sum(row[j]*x for j, x in v.items()) == 0 for row in R), 'Lift not in point kernel')
            for j, w in enumerate(lifts):
                require(dot(v, w) == q*dot(pair_embedded[i], pair_embedded[j]), 'Full lifted Gram identity')
        zz = [embed(layers[r], v) for v in Z]
        for v in zz:
            require(all(sum(row[j]*x for j, x in v.items()) == 0 for row in R), 'Inclusion transpose kernel not residual')
            require(all(dot(v, w) == 0 for w in lifts), 'Remainder/lift orthogonality')
        lifted[r], remainders[r] = lifts, zz
    norms = meta['coupled_norms']
    identity_coupled = [[F(norms[i] if i == j else 0) for j in range(6)] for i in range(6)]
    for i, f in enumerate(pair_embedded):
        vectors = [f, lifted[3][i], lifted[4][i], complement(lifted[4][i]), complement(lifted[3][i]), complement(f)]
        families.append(('coupled'+str(i), vectors, small['C'], identity_coupled, norms))
    for r in (3, 4):
        q = [[F(s), s-z[r]], [s-z[r], F(s)]]
        for i, v in enumerate(remainders[r]):
            families.append(('Z'+str(r)+'-'+str(i), [v, complement(v)], q,
                             [[F(1), F(0)], [F(0), F(1)]], [1, 1]))
    # The central complement parity decomposition is constructed literally.
    representatives = [a for a in layers[5] if a < full ^ a]
    require(len(representatives) == 126, 'Central complement-pair count')
    plus, plus_witness = nullspace([[1]*len(representatives)])
    minus_incidence = [[int(bool(a >> i & 1))-int(bool((full ^ a) >> i & 1))
                        for a in representatives] for i in range(n)]
    minus, minus_witness = nullspace(minus_incidence)
    require((len(plus), len(minus), plus_witness['rank'], minus_witness['rank']) == (125, 117, 1, 9),
            'Complete central parity dimensions')
    for kind, coefficients, sign in [('plus', plus, 1), ('minus', minus, -1)]:
        for i, coeff in enumerate(coefficients):
            v = {}
            for j, x in coeff.items():
                a = representatives[j]; v[ti[a]] = x; v[ti[full ^ a]] = sign*x
            require(all(sum(row[j]*x for j, x in v.items()) == 0 for row in R), 'Central parity point kernel')
            require(complement(v) == {j: sign*x for j, x in v.items()}, 'Central complement parity')
            q = [[F(s)+sign*(s-z[5])]]
            families.append(('central-'+kind+str(i), [v], q, [[F(1)]], [1]))
    dimension = sum(len(vectors) for _, vectors, _, _, _ in families)
    require(dimension == m, 'Incomplete finite basis')
    basis = []
    for name, vectors, q, g, gram_norms in families:
        size = len(vectors)
        qop = [[integral(D*q[i][j]/gram_norms[i]) for j in range(size)] for i in range(size)]
        gop = [[integral(g[i][j]/gram_norms[i]) for j in range(size)] for i in range(size)]
        for j, v in enumerate(vectors):
            eq = combine(vectors, [row[j] for row in qop])
            eg = combine(vectors, [row[j] for row in gop])
            equal(q_action(v), eq, m, name+' Q action')
            equal(g_action(v), eg, m, name+' G action')
            coefficients = [sum(qop[i][h]*gop[h][j] for h in range(size)) for i in range(size)]
            expected = lift(combine(vectors, coefficients))
            sv = lift(v); actual = apply(Lcols, sv)
            equal(actual, expected, N, name+' full L action')
            upper = [N*D*sv.get(i, 0)-actual[i] for i in range(N)]
            equal(upper, combine([sv, expected], [N*D, -1]), N, name+' full upper action')
            basis.append(v)
    equal(apply(Lcols, {i: 1 for i in range(N)}), {i: N*D for i in range(N)}, N, 'Full constant eigenvector')
    stars = [{i: N*int(bool(a >> point & 1))-s for i, a in enumerate(members)} for point in range(n)]
    for v in stars:
        equal(apply(Lcols, v), {}, N, 'Full centered-star kernel')
    positive_ldl([[dot(v, w) for w in stars] for v in stars])
    for v in basis:
        sv = lift(v)
        require(sum(sv.values()) == 0 and all(dot(sv, w) == 0 for w in stars), 'Full direct-sum orthogonality')
    rejected = []
    def reject(name, test):
        try:
            test()
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('Corruption accepted: '+name)
    damaged = dict(pair_embedded[0]); damaged[next(iter(damaged))] += 1
    reject('damaged_pair_kernel', lambda: require(all(sum(row[j]*x for j, x in damaged.items()) == 0 for row in R), 'Damaged residual'))
    wrong_vectors = [pair_embedded[0], lifted[3][0], lifted[4][0], complement(lifted[4][0]), complement(lifted[3][0]), complement(pair_embedded[0])]
    wrong_coefficients = [integral(D*small['C'][i][2]/norms[i]) for i in range(6)]
    wrong_coefficients[0] -= integral(D*delta[4])
    reject('wrong_pair_four_norm', lambda: equal(q_action(lifted[4][0]), combine(wrong_vectors, wrong_coefficients), m, 'Wrong coupling'))
    reject('missing_one_basis_direction', lambda: require(len(basis[:-1]) == m, 'Incomplete basis'))
    encoded = [[[i, x] for i, x in sorted(v.items())] for v in basis]
    result = {'agent': 'six-downset-3', 'role': 'researcher', 'n': n, 'N': N, 's': s,
              'L_sha256': matrix_hash(L), 'basis_sha256': sha256(json.dumps(encoded, separators=(',', ':')).encode()).hexdigest(),
              'middle_basis_dimension': m, 'full_basis_dimensions': [1, n, m],
              'kernel_witnesses': {'pair': pair_witness, 'selected_inclusion_transpose': inclusion_witness,
                                   'central_plus': plus_witness, 'central_minus': minus_witness},
              'layer_rank_checks': layer_ranks,
              'family_dimensions': {'constant': 7, 'point': 63, 'coupled': 210, 'Z3_and_mirror': 150,
                                    'Z4_and_mirror': 330, 'central_plus': 125, 'central_minus': 117},
              'lift_Gram_entries_per_selected_orbit': 35**2,
              'Q_action_coordinates': m*m, 'G_action_coordinates': m*m,
              'full_lower_action_coordinates': N*(m+n+1), 'full_upper_action_coordinates_on_range': N*m,
              'negative_controls': rejected,
              'certified_slack_ranks_by_complete_basis_and_strict_forms': {'lower': N-n, 'upper': N-1},
              'dense_full_slack_eliminations_completed': 0,
              'trust_boundary': 'Exact integer basis, rational RREF/free witnesses, literal all-coordinate actions and checked strict small forms; finite congruence positivity argument unformalized, author-checked, independently unreviewed.'}
    output = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(output)
    else:
        print(output, end='')


if __name__ == '__main__':
    main()
