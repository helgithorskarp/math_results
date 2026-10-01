#!/usr/bin/env python3
"""Complete exact rational basis and literal full-matrix actions at n9.

This checks every finite direction; it does not extrapolate to all orders.
No dense full-slack elimination or floating arithmetic is used.
Author: six-downset-3, researcher.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from math import comb
from pathlib import Path

from arithmetic import matrix_hash, psd_rank
from blocks import blocks
from matrices import construct, parameters, require


def nullspace(a):
    """Exact RREF; free-coordinate identity certifies basis independence."""
    original = [[F(x) for x in row] for row in a]
    b = [row[:] for row in original]
    require(b and len(b[0]) and all(len(row) == len(b[0]) for row in b), 'nullspace shape')
    pivots = []
    for j in range(len(b[0])):
        r = len(pivots)
        pivot = next((i for i in range(r, len(b)) if b[i][j]), None)
        if pivot is None:
            continue
        b[r], b[pivot] = b[pivot], b[r]
        scale = b[r][j]
        b[r] = [x/scale for x in b[r]]
        for i in range(len(b)):
            if i != r:
                scale = b[i][j]
                if scale:
                    b[i] = [x-scale*y for x, y in zip(b[i], b[r])]
        pivots.append(j)
        if len(pivots) == len(b):
            break
    free = [j for j in range(len(b[0])) if j not in pivots]
    vectors = []
    for j in free:
        v = {j: F(1)}
        for i, pivot in enumerate(pivots):
            if b[i][j]:
                v[pivot] = -b[i][j]
        require(all(sum(row[k]*x for k, x in v.items()) == 0 for row in original), 'nullspace residual')
        require(all(v.get(k, 0) == (j == k) for k in free), 'free-coordinate independence')
        vectors.append(v)
    return vectors, {'rows': len(b), 'columns': len(b[0]), 'rank': len(pivots),
                     'nullity': len(free), 'pivot_columns': pivots, 'free_columns': free}


def combine(vectors, coefficients):
    out = {}
    for v, c in zip(vectors, coefficients):
        for i, x in v.items():
            out[i] = out.get(i, F(0))+c*x
    return {i: x for i, x in out.items() if x}


def dot(v, w):
    return sum(x*w.get(i, 0) for i, x in v.items())


def equal_vector(actual, expected, dimension, message):
    require(len(actual) == dimension and all(x == expected.get(i, 0) for i, x in enumerate(actual)), message)


def sparse_columns(a):
    return [[(i, a[i][j]) for i in range(len(a)) if a[i][j]] for j in range(len(a))]


def apply(columns, v):
    out = [F(0) for _ in columns]
    for j, x in v.items():
        for i, y in columns[j]:
            out[i] += x*y
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    n, N, s, m = 9, 502, 247, 492
    raw_z = {2: '49/8', 3: '53/20', 4: '21/10'}
    z, epsilon, delta = parameters(n, raw_z, 0, '69/200')
    members, L = construct(n, raw_z, 0, '69/200')
    middle = [a for a in members if a.bit_count() >= 2]
    full = (1 << n)-1
    index = {a: i for i, a in enumerate(members)}
    ti = {a: i for i, a in enumerate(middle)}
    layers = {k: [a for a in middle if a.bit_count() == k] for k in range(2, 8)}
    incidence = lambda sets: [[int(bool(a >> i & 1)) for a in sets] for i in range(n)]
    R = incidence(middle)
    t = [a.bit_count()-1 for a in middle]
    full_columns = sparse_columns(L)
    mid_L = [[L[index[a]][index[b]] for b in middle] for a in middle]
    mid_columns = sparse_columns(mid_L)
    def q_action(v):
        total = sum(v.values())
        return [x-total for x in apply(mid_columns, v)]
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
    small, g0, g1 = blocks(n, z, epsilon, delta)
    require(all(psd_rank(a) == len(a) for a in small.values()), 'strict block failure')
    require(all(0 < z[k] < 2*s for k in (3, 4)), 'strict scalar failure')
    constants = [{ti[a]: F(1) for a in layers[k]} for k in layers]
    families = []
    b = [comb(n, k) for k in layers]
    alpha = [comb(n-2, k-1) for k in layers]
    families.append(('constant', constants, small['Q0'], g0, b))
    point_vectors = []
    for i in range(n-1):
        vectors = [{ti[a]: F(int(bool(a >> i & 1))-int(bool(a >> (n-1) & 1))) for a in layers[k]} for k in layers]
        vectors = [{j: x for j, x in v.items() if x} for v in vectors]
        point_vectors.append(vectors)
        families.append(('point'+str(i), vectors, small['Q1'], g1, alpha))
    # Literal layer ranks, constant/point independence and orthogonality.
    layer_checks = []
    for k in layers:
        rank_R = psd_rank([[sum(x*y for x, y in zip(row, other)) for other in incidence(layers[k])] for row in incidence(layers[k])])
        a = [constants[k-2]]+[vectors[k-2] for vectors in point_vectors]
        require(psd_rank([[dot(v, w) for w in a] for v in a]) == n, 'constant/point basis rank')
        require(all(dot(a[0], v) == 0 for v in a[1:]), 'constant/point orthogonality')
        require(rank_R == n, 'layer incidence rank')
        layer_checks.append({'layer': k, 'size': len(layers[k]), 'incidence_rank': rank_R, 'constant_point_rank': n})
    pairs, triples, fours = layers[2], layers[3], layers[4]
    f2, r2 = nullspace(incidence(pairs))
    U = [[int(a & b == a) for a in pairs] for b in triples]
    g3, rU = nullspace([list(row) for row in zip(*U)])
    h4, r4 = nullspace(incidence(fours))
    require((len(f2), len(g3), len(h4)) == (27, 48, 117), 'complete residual dimensions')
    f2m = [embed(pairs, v) for v in f2]
    Uf = [{ti[b]: sum(U[j][i]*x for i, x in f.items()) for j, b in enumerate(triples)} for f in f2]
    Uf = [{j: x for j, x in v.items() if x} for v in Uf]
    for i, v in enumerate(Uf):
        require(all(sum(row[j]*x for j, x in v.items()) == 0 for row in R), 'lift not residual')
        for j, w in enumerate(Uf):
            require(dot(v, w) == (n-4)*dot(f2m[i], f2m[j]), 'complete lifted Gram')
    gram2 = [[F(int(i == j)) for j in range(4)] for i in range(4)]
    norms2 = [1, n-4, n-4, 1]
    for i in range(4):
        gram2[i][i] = F(norms2[i])
    for i, f in enumerate(f2m):
        families.append(('coupled'+str(i), [f, Uf[i], complement(Uf[i]), complement(f)], small['C2'], gram2, norms2))
    for kind, sets, vectors, order in [('triple', triples, g3, 3), ('four', fours, h4, 4)]:
        for i, v in enumerate(vectors):
            a = embed(sets, v)
            require(all(sum(row[j]*x for j, x in a.items()) == 0 for row in R), 'residual point sum')
            if kind == 'triple':
                require(all(dot(a, w) == 0 for w in Uf), 'Z3/lift orthogonality')
            c = [[F(s), s-z[order]], [s-z[order], F(s)]]
            families.append((kind+str(i), [a, complement(a)], c, [[F(1), F(0)], [F(0), F(1)]], [1, 1]))
    dimension = sum(len(vectors) for _, vectors, _, _, _ in families)
    require(dimension == m, 'basis is incomplete')
    # Every residual basis is independent by its free coordinates. The lifted
    # Gram and Z3 orthogonality prove the layer3 direct sum; incidence kernels
    # are perpendicular to all layer constants/point functions. Mirroring is
    # a coordinate permutation. These exact witnesses prove all492 independent.
    basis = []
    for name, vectors, q, g, norms in families:
        qop = [[q[i][j]/norms[i] for j in range(len(vectors))] for i in range(len(vectors))]
        gop = [[g[i][j]/norms[i] for j in range(len(vectors))] for i in range(len(vectors))]
        for j, v in enumerate(vectors):
            eq = combine(vectors, [row[j] for row in qop])
            eg = combine(vectors, [row[j] for row in gop])
            equal_vector(q_action(v), eq, m, name+' Q action')
            equal_vector(g_action(v), eg, m, name+' Gram action')
            coefficients = [sum(qop[i][h]*gop[h][j] for h in range(len(vectors))) for i in range(len(vectors))]
            expected = lift(combine(vectors, coefficients))
            sv = lift(v)
            actual = apply(full_columns, sv)
            equal_vector(actual, expected, N, name+' full L action')
            upper = [N*sv.get(i, 0)-actual[i] for i in range(N)]
            expected_upper = combine([sv, expected], [N, -1])
            equal_vector(upper, expected_upper, N, name+' full upper action')
            basis.append(v)
    one = {i: F(1) for i in range(N)}
    equal_vector(apply(full_columns, one), {i: F(N) for i in range(N)}, N, 'constant eigenvector')
    stars = [{i: F(int(bool(a >> point & 1)))-F(s, N) for i, a in enumerate(members)} for point in range(n)]
    for v in stars:
        equal_vector(apply(full_columns, v), {}, N, 'full centered-star kernel')
    require(psd_rank([[dot(v, w) for w in stars] for v in stars]) == n, 'full star independence')
    require(all(sum(lift(v).values()) == 0 and all(dot(lift(v), w) == 0 for w in stars) for v in basis), 'full direct-sum orthogonality')
    rejected = []
    def reject(name, check):
        try:
            check()
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('corruption accepted: '+name)
    damaged = dict(f2m[0]); damaged[next(iter(damaged))] += 1
    reject('damaged_kernel_vector', lambda: require(all(sum(row[j]*x for j, x in damaged.items()) == 0 for row in R), 'damaged residual'))
    wrong = [row[:] for row in small['C2']]; wrong[0][1] -= delta
    reject('wrong_lift_norm', lambda: equal_vector(q_action(Uf[0]), combine(families[9][1], [wrong[i][1]/norms2[i] for i in range(4)]), m, 'wrong lifted coefficient'))
    reject('incomplete_basis_count', lambda: require(len(basis[:-1]) == m, 'one direction missing'))
    encoded = [[[i, str(x)] for i, x in sorted(v.items())] for v in basis]
    result = {'author': {'agent': 'six-downset-3', 'role': 'researcher'}, 'n': n, 'N': N, 's': s,
              'L_sha256': matrix_hash(L), 'basis_sha256': sha256(json.dumps(encoded, separators=(',', ':')).encode()).hexdigest(),
              'middle_basis_dimension': dimension, 'full_basis_dimensions': [1, n, dimension],
              'nullspace_certificates': {'pair': r2, 'triple_inclusion_transpose': rU, 'four': r4},
              'layer_rank_checks': layer_checks, 'family_dimensions': {'constant': 6, 'point': 48, 'coupled': 108, 'triple_residual': 96, 'four_residual': 234},
              'Q_action_coordinates': m*m, 'Gram_action_coordinates': m*m,
              'full_lower_action_coordinates': N*dimension+N*(n+1),
              'full_upper_action_coordinates_on_range': N*dimension,
              'complete_lift_Gram_entries': len(f2)**2, 'negative_controls': rejected,
              'certified_slack_ranks_by_complete_basis_and_strict_blocks': {'lower': N-n, 'upper': N-1},
              'dense_full_slack_eliminations_completed': 0,
              'trust_boundary': 'Exact rational RREF/basis witnesses and literal all-coordinate operator actions; positivity/ranks follow by finite congruence with the exact strict small blocks. Ordinary finite linear algebra proof is unformalized; no independent peer review.'}
    text = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
