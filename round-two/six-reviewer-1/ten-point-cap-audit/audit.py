#!/usr/bin/env python3
"""Independent literal subset/operator audit of the ten-point cap, reviewer1.

Descending original-set order, scaled integers, literal bilinear forms.
No author executable, CAS, solver, or floating-point arithmetic is imported.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations, product
from math import comb, lcm
from pathlib import Path
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(x):
    return sha256(json.dumps(x, separators=(',', ':')).encode()).hexdigest()


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def inverse(a):
    d = len(a)
    rows = [[F(x) for x in r] + [F(i == j) for j in range(d)] for i, r in enumerate(a)]
    for j in range(d):
        pivot = next((i for i in range(j, d) if rows[i][j]), None)
        require(pivot is not None, 'singular Gram')
        rows[j], rows[pivot] = rows[pivot], rows[j]
        p = rows[j][j]
        rows[j] = [x / p for x in rows[j]]
        for i in range(d):
            if i != j:
                p = rows[i][j]
                rows[i] = [x - p * y for x, y in zip(rows[i], rows[j])]
    out = [r[d:] for r in rows]
    require(all(sum(F(a[i][k]) * out[k][j] for k in range(d)) == (i == j)
                for i in range(d) for j in range(d)), 'inverse residual')
    return out


def pivots(a):
    d = len(a)
    require(d and all(len(r) == d for r in a), 'square form')
    require(all(a[i][j] == a[j][i] for i in range(d) for j in range(d)), 'symmetric form')
    rows = [[F(x) for x in r] for r in a]
    out = []
    for k in range(d):
        p = rows[k][k]
        require(p > 0, 'nonpositive Schur pivot')
        out.append(p)
        for i in range(k + 1, d):
            for j in range(k + 1, d):
                rows[i][j] -= rows[i][k] * rows[k][j] / p
    return out


def det(a):
    d = len(a)
    scale = lcm(*(F(x).denominator for r in a for x in r))
    rows = [[int(F(x) * scale) for x in r] for r in a]
    old, sign = 1, 1
    for k in range(d - 1):
        pivot = next((i for i in range(k, d) if rows[i][k]), None)
        if pivot is None:
            return F(0)
        if pivot != k:
            rows[k], rows[pivot] = rows[pivot], rows[k]
            sign *= -1
        p = rows[k][k]
        for i in range(k + 1, d):
            for j in range(k + 1, d):
                v = rows[i][j] * p - rows[i][k] * rows[k][j]
                require(v % old == 0, 'nonexact Bareiss division')
                rows[i][j] = v // old
            rows[i][k] = 0
        old = p
    return F(sign * rows[-1][-1], scale ** d)


def principal_certificate(a):
    values = []
    for mask in range(1, 2 ** len(a)):
        ids = [i for i in range(len(a)) if mask & (1 << i)]
        sub = [[a[i][j] for j in ids] for i in ids]
        value = det(sub)
        require(value > 0, 'nonpositive principal minor')
        ps = pivots(sub)
        require(value == __import__('functools').reduce(lambda x, y: x * y, ps, F(1)),
                'independent determinant/Schur agreement')
        values.append(str(value))
    return {'minors': len(values), 'all_positive': True, 'sha256': digest(values)}


def construct():
    n, N, s, scale = 10, 1013, 502, 100
    z = {2: 2076, 3: 214, 4: 222, 5: 220, 6: 222, 7: 214, 8: 2076}
    epsilon, delta = 94, {3: 44, 4: 24}
    full = (1 << n) - 1
    D = [A for A in reversed(range(1 << n)) if A.bit_count() <= 8]
    T = [A for A in D if A.bit_count() >= 2]
    require((len(D), len(T)) == (N, 1002), 'complete vertex sets')
    index = {A: i for i, A in enumerate(D)}
    adjacency = [[] for A in T]
    L = [[0] * N for A in D]
    edge_counts = {'complement': 0, '22': 0, '23': 0, '24': 0}
    for i, A in enumerate(T):
        L[index[A]][index[A]] = s * scale
        for j in range(i + 1, len(T)):
            B = T[j]
            if A & B:
                continue
            k, ell = sorted((A.bit_count(), B.bit_count()))
            if A | B == full:
                val, kind = s * scale - z[k], 'complement'
            elif (k, ell) == (2, 2):
                val, kind = epsilon, '22'
            elif k == 2 and ell in delta:
                val, kind = delta[ell], '2' + str(ell)
            else:
                continue
            adjacency[i].append((j, val)); adjacency[j].append((i, val))
            L[index[A]][index[B]] = L[index[B]][index[A]] = val
            edge_counts[kind] += 1
    # Original-index completion via forced stars, followed by empty row sums.
    for a, A in enumerate(T):
        sums = [s * scale if A & (1 << p) else 0 for p in range(n)]
        for b, val in adjacency[a]:
            B = T[b]
            for p in range(n):
                if B & (1 << p):
                    sums[p] += val
        for p in range(n):
            pi, ai = index[1 << p], index[A]
            L[pi][ai] = L[ai][pi] = s * scale - sums[p]
    for p in range(n):
        pi = index[1 << p]
        L[pi][pi] = s * scale
        for q in range(p + 1, n):
            qi = index[1 << q]
            val = s * scale - sum(L[pi][index[A]] for A in T if A & (1 << q))
            require(val == s * scale - sum(L[qi][index[A]] for A in T if A & (1 << p)),
                    'symmetric singleton completion')
            L[pi][qi] = L[qi][pi] = val
    ei = index[0]
    for A in D:
        if A:
            ai = index[A]
            L[ei][ai] = L[ai][ei] = N * scale - sum(L[ai])
    L[ei][ei] = N * scale - sum(L[ei])
    stars = [[j for j, B in enumerate(D) if B & (1 << p)] for p in range(n)]
    require(all(len(star) == s for star in stars), 'literal largest stars')
    for i, A in enumerate(D):
        require(sum(L[i]) == N * scale, 'every row sum')
        for j, B in enumerate(D):
            require(L[i][j] == L[j][i], 'every symmetry entry')
            require(not A & B or L[i][j] == (s * scale if A == B else 0), 'every support entry')
        for star in stars:
            require(sum(L[i][j] for j in star) == s * scale, 'every forced star equation')
    require(edge_counts == {'complement': 501, '22': 630, '23': 2520, '24': 3150},
            'complete middle orbit sizes')
    return n, N, s, scale, D, T, adjacency, L, edge_counts


def operators(n, N, s, scale, D, T, adjacency):
    t = [A.bit_count() - 1 for A in T]
    index = {A: i for i, A in enumerate(D)}
    incidence = [[j for j, A in enumerate(T) if A & (1 << p)] for p in range(n)]

    def lift(v):
        out = [0] * N
        out[index[0]] = dot(t, v)
        for p in range(n):
            out[index[1 << p]] = -sum(v[j] for j in incidence[p])
        for j, A in enumerate(T):
            out[index[A]] = v[j]
        return out

    def Q(v):
        total = sum(v)
        return [s * scale * v[i] - scale * total + sum(val * v[j] for j, val in neighbors)
                for i, neighbors in enumerate(adjacency)]

    def G(v):
        rv = [sum(v[j] for j in ids) for ids in incidence]
        tv = dot(t, v)
        return [v[i] + sum(rv[p] for p in range(n) if A & (1 << p)) + t[i] * tv
                for i, A in enumerate(T)]

    return lift, Q, G


def literal_forms(n, N, s, scale, D, T, adjacency, L):
    lift, Q, G = operators(n, N, s, scale, D, T, adjacency)
    layers = list(range(2, 9))
    constant = [[int(A.bit_count() == k) for A in T] for k in layers]
    point = [[(int(bool(A & 1)) - int(bool(A & 2))) * int(A.bit_count() == k) for A in T]
             for k in layers]
    cycle = {3: 1, 12: 1, 5: -1, 10: -1}
    require(all(sum(v for A, v in cycle.items() if A & (1 << p)) == 0 for p in range(n)),
            'pair cycle kernel')
    vectors = [[sum(v for pair, v in cycle.items() if pair & A == pair)
                * int(A.bit_count() == k) for A in T] for k in (2, 3, 4)]
    complement = {A: i for i, A in enumerate(T)}
    coupled = vectors + [[v[complement[((1 << n) - 1) ^ A]] for A in T] for v in reversed(vectors)]
    forms, metrics, records = {}, {}, {}
    for name, B in [('constant', constant), ('point', point), ('coupled', coupled)]:
        d = [dot(v, v) for v in B]
        require(all(dot(B[i], B[j]) == (d[i] if i == j else 0)
                    for i in range(len(B)) for j in range(len(B))), 'orthogonal literal basis')
        qv, gv = [Q(v) for v in B], [G(v) for v in B]
        lower = [[F(dot(x, y), scale) for y in qv] for x in B]
        gram = [[dot(x, y) for y in gv] for x in B]
        lifted = [lift(v) for v in B]
        require(gram == [[dot(x, y) for y in lifted] for x in lifted], 'literal range Gram')
        inv = inverse(gram)
        H = [[d[i] * inv[i][j] * d[j] for j in range(len(B))] for i in range(len(B))]
        upper = [[N * H[i][j] - lower[i][j] for j in range(len(B))] for i in range(len(B))]
        for j, v in enumerate(B):
            for i in range(len(T)):
                require(F(qv[j][i], scale) == sum(F(lower[k][j], d[k]) * B[k][i] for k in range(len(B))),
                        'every representative Q action coordinate')
                require(gv[j][i] == sum(F(gram[k][j], d[k]) * B[k][i] for k in range(len(B))),
                        'every representative G action coordinate')
            expected = lift(Q(gv[j]))
            actual = [dot(row, lifted[j]) for row in L]
            require(actual == expected, 'every full representative lower action coordinate')
        for suffix, a in [('lower', lower), ('upper', upper)]:
            key = name + '_' + suffix
            forms[key] = a
            metrics[key] = H
            records[key] = {'dimension': len(a), 'literal_basis_norms': d,
                            'schur_pivots': list(map(str, pivots(a))),
                            'principal': principal_certificate(a),
                            'form_sha256': digest([[str(x) for x in r] for r in a])}
    return forms, metrics, records


def buffer_certificate(forms, metrics):
    for exponent in range(16):
        gap = F(1, 2 ** exponent)
        try:
            for name, a in forms.items():
                h = metrics[name]
                pivots([[a[i][j] - gap * h[i][j] for j in range(len(a))] for i in range(len(a))])
        except ValueError:
            continue
        require(gap < F(107, 50), 'remaining lower modes')
        require(gap < 9 + F(107, 50), 'remaining upper modes')
        trace_G = sum(comb(10, k) * (k * k - k + 2) for k in range(2, 9))
        radius = gap / (2 * 155 * trace_G)
        return {'gap': str(gap), 'six_strict_shifted_forms': True,
                'trace_G': trace_G, 'maximum_perturbation_row_degree': 155,
                'all_seven_parameters_box_radius': str(radius),
                'retained_lower_and_upper_gap': str(gap / 2),
                'optimality_claim': False}
    raise ValueError('No certified rational buffer within the bounded screen')


def incidence_and_remaining_actions(n, N, s, scale, D, T, adjacency, L):
    pairs = [A for A in T if A.bit_count() == 2]
    r2 = [[int(bool(A & (1 << p))) for A in pairs] for p in range(n)]
    require([[dot(x, y) for y in r2] for x in r2] ==
            [[8 * int(p == q) + 1 for q in range(n)] for p in range(n)], 'full pair incidence Gram')
    records = []
    for r in (3, 4):
        members = [A for A in T if A.bit_count() == r]
        columns = [[int(P & A == P) for A in members] for P in pairs]
        q = comb(n - 4, r - 2)
        for i, P in enumerate(pairs):
            for j, B in enumerate(pairs):
                expected = q * int(i == j) + comb(n - 4, r - 3) * (P & B).bit_count()
                if r >= 4:
                    expected += comb(n - 4, r - 4)
                require(dot(columns[i], columns[j]) == expected, 'entire pair inclusion Gram')
            for p in range(n):
                val = sum(x for A, x in zip(members, columns[i]) if A & (1 << p))
                expected = (comb(n - 3, r - 3) + comb(n - 3, r - 2) * int(bool(P & (1 << p))))
                require(val == expected, 'entire forward point inclusion identity')
            for A in members:
                require(int(not P & A) == 1 - (P & A).bit_count() + int(P & A == P),
                        'entire rectangular disjointness identity')
        for A in members:
            for p in range(n):
                require(sum(int(P & A == P) for P in pairs if P & (1 << p)) ==
                        (r - 1) * int(bool(A & (1 << p))), 'entire transpose inclusion identity')
        records.append({'r': r, 'layer_size': len(members), 'q': q,
                        'full_column_rank_from_positive_Gram': len(pairs),
                        'transpose_kernel_dimension': len(members) - len(pairs)})
    full = (1 << n) - 1
    halves = [A for A in T if A.bit_count() == 5 and A < (full ^ A)]
    require(len(halves) == 126, 'all central complement pairs')
    plus = [[int(bool(A & (1 << p))) + int(bool((full ^ A) & (1 << p))) for A in halves]
            for p in range(n)]
    minus = [[int(bool(A & (1 << p))) - int(bool((full ^ A) & (1 << p))) for A in halves]
             for p in range(n)]
    require(all(x == 1 for row in plus for x in row), 'central plus rank1')
    require([[dot(x, y) for y in minus] for x in minus] ==
            [[140 * int(p == q) - 14 for q in range(n)] for p in range(n)], 'central minus rank9 Gram')
    lift, Q, G = operators(n, N, s, scale, D, T, adjacency)
    loc = {A: i for i, A in enumerate(T)}
    seeds = []
    for r in (3, 4, 5):
        coefficients = {}
        fixed = 0 if r == 3 else (1 << 6) if r == 4 else (1 << 6) | (1 << 7)
        for bits in product((0, 1), repeat=3):
            A = fixed | sum(1 << (2 * j + bit) for j, bit in enumerate(bits))
            coefficients[A] = (-1) ** sum(bits)
        v = [coefficients.get(A, 0) for A in T]
        pv = [v[loc[full ^ A]] for A in T]
        require(sum(v) == 0 and all(sum(v[i] for i, A in enumerate(T) if A & (1 << p)) == 0
                                   for p in range(n)), 'alternating-cube point kernel')
        if r in (3, 4):
            require(all(sum(v[i] for i, A in enumerate(T) if P & A == P) == 0 for P in pairs),
                    'alternating-cube pair transpose kernel')
            z = F(107, 50) if r == 3 else F(111, 50)
            for w, mirrored in [(v, pv), (pv, v)]:
                require([F(x, scale) for x in Q(w)] ==
                        [s * x + (s - z) * y for x, y in zip(w, mirrored)], 'whole remainder complement action')
                seeds.append(w)
        else:
            for sign in (1, -1):
                w = [x + sign * y for x, y in zip(v, pv)]
                eigen = 2 * s - F(11, 5) if sign == 1 else F(11, 5)
                require([F(x, scale) for x in Q(w)] == [eigen * x for x in w], 'whole central parity action')
                require([w[loc[full ^ A]] for A in T] == [sign * x for x in w], 'literal central parity')
                seeds.append(w)
    for w in seeds:
        require(G(w) == w, 'remainder range metric is identity')
        require([dot(row, lift(w)) for row in L] == lift(Q(w)), 'full remainder lower action')
    dimensions = {'constant': 7, 'point': 7 * (n - 1), 'coupled': 6 * (len(pairs) - n),
                  'Z3_and_mirror': 2 * records[0]['transpose_kernel_dimension'],
                  'Z4_and_mirror': 2 * records[1]['transpose_kernel_dimension'],
                  'central_plus': len(halves) - 1, 'central_minus': len(halves) - (n - 1)}
    return {'inclusion_records': records, 'central_pair_count': len(halves),
            'central_incidence_ranks': {'plus': 1, 'minus': 9},
            'literal_residual_directions': len(seeds), 'dimensions': dimensions}


def backend_controls():
    for values in product((-1, 0, 1), repeat=6):
        a = [[values[0], values[1], values[2]], [values[1], values[3], values[4]],
             [values[2], values[4], values[5]]]
        literal = 0
        for p in permutations(range(3)):
            sign = (-1) ** sum(p[i] > p[j] for i in range(3) for j in range(i + 1, 3))
            literal += sign * a[0][p[0]] * a[1][p[1]] * a[2][p[2]]
        require(det(a) == literal, '729 determinant controls')
    for bad in ([[0, 1], [1, 0]], [[1, 2], [2, 1]], [[0]], [[1, 0], [0, 0]]):
        try:
            pivots(bad)
        except ValueError:
            continue
        raise ValueError('damaged/indefinite form accepted')
    return {'ternary_symmetric_determinants': 729, 'nonpositive_forms_rejected': 4}


def audit():
    controls = backend_controls()
    n, N, s, scale, D, T, adjacency, L, counts = construct()
    forms, metrics, records = literal_forms(n, N, s, scale, D, T, adjacency, L)
    buffer = buffer_certificate(forms, metrics)
    require(sum(r['principal']['minors'] for r in records.values()) == 634, 'every small principal minor')
    incidence = incidence_and_remaining_actions(n, N, s, scale, D, T, adjacency, L)
    dimensions = incidence['dimensions']
    require(sum(dimensions.values()) == len(T), 'complete decomposition dimension')
    result = {'reviewer': 'six-reviewer-1', 'role': 'independent mathematical reviewer',
              'n': n, 'N': N, 's': s, 'scale': scale, 'original_vertex_order': 'descending bitmasks',
              'full_scaled_matrix_sha256': digest(L), 'full_entries_checked': N * N,
              'row_equations': N, 'star_equations': n * N, 'middle_edge_counts': counts,
              'literal_representative_directions': 26, 'six_literal_forms': records,
              'full_incidence_and_remaining_actions': incidence,
              'complete_dimensions_from_written_proof': dimensions,
              'slack_ranks_from_complete_congruence': {'lower': 1003, 'upper': 1012},
              'rational_buffer_and_box': buffer, 'backend_controls': controls,
              'trust_boundary': 'Written all-order invariant decomposition plus exact literal finite arithmetic; no dense full PSD elimination.'}
    return result, (D, L, forms)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', type=Path)
    args = parser.parse_args()
    result, _ = audit()
    raw = json.dumps(result, indent=2) + '\n'
    if args.check:
        require(raw == args.check.read_text(), 'complete expected output mismatch')
    print(raw, end='')


if __name__ == '__main__':
    main()
