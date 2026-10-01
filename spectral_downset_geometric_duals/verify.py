#!/usr/bin/env python3
"""Exact geometric and projected two-vector cap bounds; six-downset-3 researcher."""
from fractions import Fraction as Q
from itertools import combinations, product
from math import comb, lcm
from pathlib import Path
import argparse
import copy
import hashlib
import json
import re


def require(ok, why):
    if not ok:
        raise ValueError(why)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def sparse_rank(rows):
    basis = {}
    for source in rows:
        row = {i: Q(v) for i, v in source.items() if v}
        while row:
            p = min(row)
            if p not in basis:
                scale = row[p]
                basis[p] = {i: v/scale for i, v in row.items()}
                break
            t = row[p]
            for i, v in basis[p].items():
                row[i] = row.get(i, 0)-t*v
                if not row[i]:
                    del row[i]
    return len(basis)


def integer_matrix(a):
    require(a and all(len(row) == len(a) for row in a), 'matrix shape')
    d = 1
    for row in a:
        for x in row:
            d = lcm(d, Q(x).denominator)
    return [[int(Q(x)*d) for x in row] for row in a], d


def psd_rank(a):
    z, _ = integer_matrix(a)
    N = len(z)
    require(all(z[i][j] == z[j][i] for i in range(N) for j in range(N)), 'PSD asymmetry')
    previous = 1
    rank = 0
    for k in range(N):
        require(all(z[i][i] >= 0 for i in range(k, N)), 'negative Schur diagonal')
        piv = next((i for i in range(k, N) if z[i][i] > 0), None)
        if piv is None:
            require(all(z[i][j] == 0 for i in range(k, N) for j in range(k, N)),
                    'zero diagonal with nonzero residual')
            break
        if piv != k:
            z[k], z[piv] = z[piv], z[k]
            for row in z:
                row[k], row[piv] = row[piv], row[k]
        pivot = z[k][k]
        for i in range(k+1, N):
            for j in range(i, N):
                value = pivot*z[i][j] - z[i][k]*z[k][j]
                require(value % previous == 0, 'nonexact Bareiss division')
                z[i][j] = z[j][i] = value//previous
        for i in range(k+1, N):
            z[i][k] = z[k][i] = 0
        previous = pivot
        rank += 1
    return rank



def data(n):
    require(n >= 4, 'n')
    full = (1 << n)-1
    F = [1 << i for i in range(n)]+[a for a in range(1 << n)
                                    if 2 <= a.bit_count() <= n-2]
    pairs = [(a, full ^ a) for a in F[n:] if a < (full ^ a)]
    index = {a: i for i, a in enumerate(F)}
    p = 2**(n-1)-n-1
    require(len(pairs) == p and len(F) == n+2*p, 'counts')
    return F, pairs, index, p+1, len(F)+1


def matrix(n, z):
    F, pairs, index, s, N = data(n)
    require(len(z) == len(pairs), 'weights')
    K = [[s*int(i == j) for j in range(len(F))] for i in range(len(F))]
    for i in range(n):
        for j in range(i):
            K[i][j] = K[j][i] = s
    for (A, B), weight in zip(pairs, z):
        a, b = index[A], index[B]
        K[a][b] = K[b][a] = s-weight
        for i in range(n):
            if A & (1 << i):
                K[i][b] = K[b][i] = weight
            else:
                K[i][a] = K[a][i] = weight
            for j in range(i):
                if bool(A & (1 << i)) != bool(A & (1 << j)):
                    K[i][j] -= weight
                    K[j][i] -= weight
    C = [[v-1 for v in row] for row in K]
    sums = [sum(row) for row in C]
    L = [[1+sum(sums)]+[1-v for v in sums]]+[
        [1-sums[i]]+[v+1 for v in row] for i, row in enumerate(C)]
    return C, K, L


def lift(C):
    totals = [sum(row) for row in C]
    return [[1+sum(totals)]+[1-x for x in totals]]+[
        [1-totals[i]]+[1+x for x in row] for i, row in enumerate(C)]


def from_middle(n, middle):
    """Independent forced-star block construction C=[-R;I]Q[-R^T,I]."""
    F, _, _, s, _ = data(n)
    T = F[n:]
    require(len(middle) == len(T), 'middle shape')
    RQ = [[sum(middle[a][b] for a, A in enumerate(T) if A & (1 << i))
           for b in range(len(T))] for i in range(n)]
    C = [[sum(RQ[i][a] for a, A in enumerate(T) if A & (1 << j))
          for j in range(n)]+[-x for x in RQ[i]] for i in range(n)]
    C += [[-RQ[i][a] for i in range(n)]+list(row)
          for a, row in enumerate(middle)]
    K = [[x+1 for x in row] for row in C]
    require(all(K[i][i] == s for i in range(len(F))), 'factor diagonal')
    return C, K, lift(C)


def edge_direction(n, A, B):
    """Sparse derivative of the literal K and row-normalized full L."""
    F, _, index, _, _ = data(n)
    require(A in index and B in index and not A & B and
            min(A.bit_count(), B.bit_count()) >= 2, 'free middle edge')
    K = {}

    def add(i, j, x):
        for a, b in ((i, j), (j, i)):
            K[a, b] = K.get((a, b), 0)+x
            if K[a, b] == 0:
                del K[a, b]

    a, b = index[A], index[B]
    add(a, b, 1)
    for i in range(n):
        if B & (1 << i):
            add(i, a, -1)
        if A & (1 << i):
            add(i, b, -1)
            for j in range(n):
                if B & (1 << j):
                    add(i, j, 1)
    totals = [0]*len(F)
    L = {(i+1, j+1): x for (i, j), x in K.items()}
    for (i, _), x in K.items():
        totals[i] += x
    L[0, 0] = sum(totals)
    for i, x in enumerate(totals):
        if x:
            L[0, i+1] = L[i+1, 0] = -x
    return K, L


def affine_audit(n, complement_only):
    F, pairs, _, s, _ = data(n)
    full = (1 << n)-1
    free = [(A, B) for a, A in enumerate(F[n:]) for B in F[n:][a+1:]
            if not A & B and (not complement_only or A ^ B == full)]
    unknown = [(i, j) for i in range(len(F)) for j in range(i)
               if not F[i] & F[j] and
               (not complement_only or j < n or F[i] ^ F[j] == full)]
    lookup = {tuple(sorted(pair)): k for k, pair in enumerate(unknown)}
    rows = []
    for i in range(n):
        for a, A in enumerate(F):
            if A & (1 << i):
                continue
            row = {}
            for b, B in enumerate(F):
                key = tuple(sorted((a, b)))
                if B & (1 << i) and key in lookup:
                    row[lookup[key]] = 1
            rows.append(row)
    zero = matrix(n, [Q(0)]*len(pairs))[1]
    require(all(sum(zero[unknown[k][0]][unknown[k][1]]*v for k, v in row.items()) == s
                for row in rows), 'affine constant solution')
    rank = sparse_rank(rows)
    require(len(unknown)-rank == len(free), 'complete affine dimension')
    for A, B in free:
        direction, _ = edge_direction(n, A, B)
        values = [direction.get((i, j), 0) for i, j in unknown]
        require(all(sum(values[k]*v for k, v in row.items()) == 0 for row in rows),
                'every independent middle derivative in star kernel')
    return {'n': n, 'complement_only': complement_only,
            'unknowns': len(unknown), 'equations': len(rows), 'rank': rank,
            'affine_dimension': len(free)}


def rational(value):
    require(type(value) is str and re.fullmatch(r'-?\d+(?:/[1-9]\d*)?', value),
            'rational string required')
    return Q(value)


def quadratic(a, v):
    return sum(v[i]*dot(row, v) for i, row in enumerate(a))


def sparse_quadratic(a, v):
    return sum(x*v[i]*v[j] for (i, j), x in a.items())


def moments(n, r):
    counts = [comb(n, k) for k in range(n-1)]
    N, s = sum(counts), sum(comb(n-1, k) for k in range(n-2))
    m = N-n-1
    A = sum(k*counts[k] for k in range(n-1))
    B = sum(k*k*counts[k] for k in range(n-1))
    R = sum(counts[k]*r**k for k in range(2, n-1))
    AR = sum(k*counts[k]*r**k for k in range(2, n-1))
    RR = sum(counts[k]*r**(2*k) for k in range(2, n-1))
    V, D = Q(N*B-A*A), N*AR-A*R
    E = (N-s)*RR+r**n*m*(s-m)
    d = (n+1)*A-N*n
    require(A == n*s and V > 0, 'cardinality moments and positive variance')
    return counts, N, s, m, V, D, E, Q(d)


def scalar_certificate(case):
    n = case['n']
    require(type(n) is int and n in (6, 7, 8, 9, 10), 'finite certificate orders')
    r = rational(case['r'])
    require(r > 1, 'geometric ratio domain')
    counts, N, s, m, V, D, E, d = moments(n, r)
    original = [rational(x) for x in case['original_upper_layers']]
    require(len(original) == n-1 and original[0] == 0, 'original upper layers')
    tau = D/V
    scale = original[1]/tau
    require(scale > 0 and original == [Q(0), scale*tau]+[
        scale*(tau*k-r**k) for k in range(2, n-1)], 'optimal geometric upper vector')
    gamma = rational(case['gamma'])
    require(gamma == scale*scale*r**n > 0, 'geometric lower multiplier')
    total = sum(counts[k]*original[k] for k in range(n-1))
    w = [x-total/N for x in original]
    u0 = [Q(2 <= k <= n-2)-Q(m, N) for k in range(n-1)]
    x = [Q(k)-Q(n*s, N) for k in range(n-1)]
    u = [u0[k]-(d/V)*x[k] for k in range(n-1)]
    require(u == [rational(v) for v in case['projected_lower_layers']], 'forced-star projection')
    require(sum(counts[k]*u[k] for k in range(n-1)) == 0 and
            sum(counts[k]*k*u[k] for k in range(n-1)) == 0, 'lower projection orthogonality')
    require(sum(counts[k]*w[k] for k in range(n-1)) == 0 and
            sum(counts[k]*k*w[k] for k in range(n-1)) == 0, 'upper projection orthogonality')
    old_constant = scale*scale*(E-D*D/V)
    require(old_constant == rational(case['old_constant']), 'old optimal constant')
    wn = sum(counts[k]*w[k]*w[k] for k in range(n-1))
    un = sum(counts[k]*u[k]*u[k] for k in range(n-1))
    q = sum(counts[k]*w[k]*u[k] for k in range(n-1))
    S = wn+gamma*un
    t = rational(case['rotation_parameter'])
    den = gamma-t*t
    require(den > 0 and q != 0, 'rotation domain and overlap')
    require(abs(t-gamma*q/S) <= Q(1, 2), 'exact nearest-integer choice')
    gap = N*(2*gamma*t*q-t*t*S)/den
    require(gap > 0, 'positive extra gap')
    constant = old_constant-gap
    require(constant == rational(case['expected_rotated_constant']), 'rotated constant')
    weights = {tuple(map(int, k.split('/'))): rational(v) for k, v in case['orbit_weights'].items()}
    actual = {}
    for a in range(2, n-1):
        for b in range(a, n-1):
            if a+b < n:
                actual[a, b] = 2*(gamma-(original[a]-a*original[1])*
                                 (original[b]-b*original[1]))
    unit = rational(case['coefficient_unit'])
    require(unit > 0 and actual == {key: unit*value for key, value in weights.items()},
            'every extra orbit coefficient')
    rhs = -constant/(unit*(N-s))
    require(rhs == rational(case['M_rhs']) > rational(case['clean_strict_rhs']),
            'strong and clean signed M bounds')
    return {'n': n, 'N': N, 's': s, 'original': original, 'w_layers': w,
            'u_layers': u, 'gamma': gamma, 't': t, 'den': den, 'constant': constant,
            'gap': gap, 'weights': weights, 'unit': unit, 'rhs': rhs,
            'wn': wn, 'un': un, 'q': q, 'projection': d/V,
            'tau': tau, 'V': V, 'D': D, 'E': E}


def vectors(info):
    F, _, _, _, _ = data(info['n'])
    members = [0]+F
    w = [info['w_layers'][A.bit_count()] for A in members]
    u = [info['u_layers'][A.bit_count()] for A in members]
    plus = [a-info['t']*b for a, b in zip(w, u)]
    minus = [info['t']*a-info['gamma']*b for a, b in zip(w, u)]
    return w, u, plus, minus


def rotated_value(L, info):
    _, _, plus, minus = vectors(info)
    upper = [[info['N']*int(i == j)-v for j, v in enumerate(row)] for i, row in enumerate(L)]
    return (info['gamma']*quadratic(upper, plus)+quadratic(L, minus))/info['den']


def full_definition(n, L):
    F, _, _, s, N = data(n)
    members = [0]+F
    require(all(len(row) == N for row in L), 'full matrix shape')
    require(all(L[i][j] == L[j][i] for i in range(N) for j in range(N)), 'full symmetry')
    require(all(sum(row) == N for row in L), 'full row sums')
    require(all(L[i][j] == s*int(i == j) for i, A in enumerate(members)
                for j, B in enumerate(members) if A & B), 'full support and diagonal')
    for point in range(n):
        y = [int(bool(A & (1 << point))) for A in members]
        require(sum(y) == s and all(dot(row, y) == s for row in L), 'literal full star equations')


def coefficient_audit(info):
    n, N, gamma, den = (info[k] for k in ('n', 'N', 'gamma', 'den'))
    F, pairs, _, _, _ = data(n)
    members = [0]+F
    w, u, plus, minus = vectors(info)
    # All entries of the exact rank-one PSD splitting, independent of H support.
    require(any(plus) and any(minus), 'two nonzero rank-one duals')
    for i in range(N):
        for j in range(i+1):
            require((minus[i]*minus[j]-gamma*plus[i]*plus[j])/den ==
                    gamma*u[i]*u[j]-w[i]*w[j], 'full PSD decomposition coefficient')
    require(N*(dot(w, w)-gamma*dot(plus, plus)/den) == info['gap'],
            'full PSD decomposition constant')
    _, _, base = matrix(n, [Q(0)]*len(pairs))
    full_definition(n, base)
    require(rotated_value(base, info) == info['constant'], 'full literal dual constant')
    counts, coefficients, records = {}, {}, []
    for a, A in enumerate(F[n:]):
        for B in F[n:][a+1:]:
            if A & B:
                continue
            Kdir, Ldir = edge_direction(n, A, B)
            require(all(i == j == 0 or (i != j and not members[i] & members[j])
                        for (i, j), v in Ldir.items() if v), 'full derivative support')
            totals, stars = [0]*N, [[0]*len(F) for _ in range(n)]
            for (i, _), v in Ldir.items():
                totals[i] += v
            for (i, j), v in Kdir.items():
                for point in range(n):
                    if F[j] & (1 << point):
                        stars[point][i] += v
            require(not any(totals) and not any(v for row in stars for v in row),
                    'all row/star homogeneous derivatives')
            value = (-gamma*sparse_quadratic(Ldir, plus)+sparse_quadratic(Ldir, minus))/den
            key = tuple(sorted((A.bit_count(), B.bit_count())))
            expected = info['unit']*info['weights'].get(key, 0)
            require(value == expected, 'every free affine coefficient')
            counts[key] = counts.get(key, 0)+1
            coefficients[key] = str(value)
            records.append([A, B, str(value)])
    affine = affine_audit(n, False)
    require(affine['affine_dimension'] == len(records), 'unsymmetrized affine completeness')
    require(len(records) == (130 if n == 6 else 546), 'full finite coefficient count')
    return {'affine_system': affine, 'free_middle_edges': len(records),
            'counts': {'/'.join(map(str, k)): v for k, v in counts.items()},
            'coefficients': {'/'.join(map(str, k)): v for k, v in coefficients.items()},
            'coefficient_sha256': hashlib.sha256(json.dumps(records, separators=(',', ':')).encode()).hexdigest(),
            'PSD_decomposition_entries': N*(N+1)//2, 'two_dual_ranks': [1, 1]}


def literal_audit(info):
    n, N = info['n'], info['N']
    F, pairs, _, _, _ = data(n)
    cases = []
    for name, z in [('common_one', [Q(1)]*len(pairs)),
                    ('asymmetric_positive', [Q(1)+Q(k % 3, 20) for k in range(len(pairs))]),
                    ('signed_extra_cancellation', [Q(1)]*len(pairs))]:
        C, K, L = matrix(n, z)
        if name == 'signed_extra_cancellation':
            extras = [(A, B) for a, A in enumerate(F[n:]) for B in F[n:][a+1:]
                      if not A & B and A.bit_count() == B.bit_count() == 2]
            for sign, (A, B) in zip((1, -1), extras[:2]):
                _, direction = edge_direction(n, A, B)
                for (i, j), v in direction.items():
                    L[i][j] += sign*Q(v, 1000)
            K = [row[1:] for row in L[1:]]
            C = [[v-1 for v in row] for row in K]
        require(from_middle(n, [row[n:] for row in C[n:]]) == (C, K, L),
                'independent middle-factor reconstruction')
        full_definition(n, L)
        require(psd_rank(C) == N-n-1 and psd_rank(L) == N-n, 'literal full ordinary ranks')
        value = rotated_value(L, info)
        require(value == info['constant'] < 0, 'literal rotated upper obstruction')
        cases.append({'name': name, 'lower_rank': N-n, 'rotated_value': str(value)})
    return cases


def orbit_audit(info):
    """Exact representative derivatives; invariant duals, arbitrary primal matrices.

    The written all-orders forced-star factorization supplies completeness.
    No dense matrix or rank enumeration is claimed for these higher orders.
    """
    n, N, s = info['n'], info['N'], info['s']
    counts = [comb(n, k) for k in range(n-1)]
    w, u = info['w_layers'], info['u_layers']
    gamma, t, den = info['gamma'], info['t'], info['den']
    plus = [a-t*b for a, b in zip(w, u)]
    minus = [t*a-gamma*b for a, b in zip(w, u)]
    require(any(plus) and any(minus), 'nonzero higher-order rank-one duals')
    for a in range(n-1):
        for b in range(a+1):
            require((minus[a]*minus[b]-gamma*plus[a]*plus[b])/den ==
                    gamma*u[a]*u[b]-w[a]*w[b], 'all layer PSD decomposition entries')

    def norm(v):
        return sum(counts[k]*v[k]*v[k] for k in range(n-1))

    def zero_pair_quadratic(v):
        # Literal middle core Q=sI-J and C=[-R;I]Q[-R^T,I].
        b = [v[k]-k*v[1]+(k-1)*v[0] for k in range(2, n-1)]
        total = sum(counts[k]*v[k] for k in range(n-1))
        bn = sum(counts[k]*b[k-2]**2 for k in range(2, n-1))
        bs = sum(counts[k]*b[k-2] for k in range(2, n-1))
        return total*total+s*bn-bs*bs

    base_value = (gamma*(N*norm(plus)-zero_pair_quadratic(plus))+
                  zero_pair_quadratic(minus))/den
    require(base_value == info['constant'] < 0, 'compressed literal full dual constant')
    full_w, full_u, full_plus, full_minus = vectors(info)
    orbit_counts, coefficients = {}, {}
    for a in range(2, n-1):
        for b in range(a, n-1):
            if a+b > n:
                continue
            A, B = (1 << a)-1, ((1 << b)-1) << a
            _, direction = edge_direction(n, A, B)
            value = (-gamma*sparse_quadratic(direction, full_plus)+
                     sparse_quadratic(direction, full_minus))/den
            expected = info['unit']*info['weights'].get((a, b), 0)
            require(value == expected, 'every higher-order orbit representative')
            multiplicity = comb(n, a)*comb(n-a, b)//(1+int(a == b))
            key = f'{a}/{b}'
            orbit_counts[key], coefficients[key] = multiplicity, str(value)
    # Independently enumerate every unordered disjoint pair to check orbit counts.
    F, _, _, _, _ = data(n)
    enumerated = {}
    for i, A in enumerate(F[n:]):
        for B in F[n:][i+1:]:
            if not A & B:
                a, b = sorted((A.bit_count(), B.bit_count()))
                key = f'{a}/{b}'
                enumerated[key] = enumerated.get(key, 0)+1
    require(enumerated == orbit_counts, 'complete higher-order pair multiplicities')
    require(N*(norm(w)-gamma*norm(plus)/den) == info['gap'], 'compressed constant gap')
    return {'scope': 'All orbit representatives and complete pair counts; written proof supplies the all-real affine bridge.',
            'free_middle_edges': sum(orbit_counts.values()), 'counts': orbit_counts,
            'coefficients': coefficients, 'orbit_representatives': len(orbit_counts),
            'PSD_decomposition_layer_entries': n*(n-1)//2,
            'full_entries_covered_by_layers': N*(N+1)//2, 'two_dual_ranks': [1, 1]}


def capped_six_baseline(info):
    F, _, _, s, N = data(6)
    beta = [[Q(x) for x in row] for row in
            [[-2, 0, 2, 4], [0, Q(4, 3), 0, 22], [2, 0, 24, 0], [4, 22, 0, 0]]]
    C = [[s*int(A == B)-1+(beta[A.bit_count()-1][B.bit_count()-1] if not A & B else 0)
          for B in F] for A in F]
    trade = {(1, 1): 12, (1, 2): -3, (2, 2): 1}
    delta = [[trade.get(tuple(sorted((A.bit_count(), B.bit_count()))), 0)
              if A != B and not A & B else 0 for B in F] for A in F]
    result = []
    for name, epsilon, rank in [('published_centered', Q(0), 50),
                                ('published_repaired', Q(1, 40320), 51)]:
        core = [[v+epsilon*delta[i][j] for j, v in enumerate(row)] for i, row in enumerate(C)]
        L = lift(core)
        full_definition(6, L)
        require(psd_rank(core) == rank-1 and psd_rank(L) == rank, 'known capped lower ranks')
        upper = [[N*int(i == j)-L[i][j] for j in range(N)] for i in range(N)]
        require(psd_rank(upper) == N-1, 'known capped upper rank')
        value = rotated_value(L, info)
        orbit_value = Q(0)
        for i, A in enumerate(F):
            for j in range(i):
                B = F[j]
                if not A & B:
                    key = tuple(sorted((A.bit_count(), B.bit_count())))
                    orbit_value += info['weights'].get(key, 0)*L[i+1][j+1]
        require(value == info['constant']+info['unit']*orbit_value >= 0,
                'known capped entire dual and inequality')
        require(orbit_value/(N-s) >= info['rhs'], 'known capped signed bound')
        result.append({'name': name, 'lower_rank': rank, 'upper_rank': N-1,
                       'weighted_L_orbit_sum': str(orbit_value), 'rotated_value': str(value)})
    return {'attribution': 'Prior graph7980 by six-downset-3 researcher; validation, not new feasibility.',
            'cases': result}


def moment_audit():
    checks = 0
    for n in range(4, 33):
        for r in (Q(3, 2), Q(5, 3), Q(2)):
            counts, N, s, m, V, D, E, d = moments(n, r)
            tau = D/V
            w = [Q(0), tau]+[tau*k-r**k for k in range(2, n-1)]
            b = [-r**k for k in range(2, n-1)]
            wn = sum(counts[k]*w[k]*w[k] for k in range(n-1))
            total = sum(counts[k]*w[k] for k in range(n-1))
            bnorm = sum(counts[k]*b[k-2]**2 for k in range(2, n-1))
            bsum = sum(counts[k]*b[k-2] for k in range(2, n-1))
            constant = N*wn-total*total+s*(r**n*m-bnorm)-r**n*m*m+bsum*bsum
            require(constant == E-D*D/V, 'direct trace versus optimized moments')
            x = [Q(k)-Q(n*s, N) for k in range(n-1)]
            u = [Q(2 <= k <= n-2)-Q(m, N)-(d/V)*x[k] for k in range(n-1)]
            require(sum(counts[k]*u[k] for k in range(n-1)) == 0 and
                    sum(counts[k]*u[k]*x[k] for k in range(n-1)) == 0, 'general scalar projection')
            un = sum(counts[k]*u[k]*u[k] for k in range(n-1))
            wc = [v-total/N for v in w]
            W = sum(counts[k]*wc[k]*wc[k] for k in range(n-1))
            q = sum(counts[k]*wc[k]*u[k] for k in range(n-1))
            S = W+r**n*un
            require(S > 0 and S*S >= 4*r**n*q*q, 'exact Gram inequality')
            t = r**n*q/S
            require(t*t < r**n, 'general rational rotation domain')
            gap = N*(2*r**n*t*q-t*t*S)/(r**n-t*t)
            require(gap == N*r**n*q*q*S/(S*S-r**n*q*q) >= 0, 'general rational positive-gap formula')
            checks += 1
    return {'orders': [4, 32], 'geometric_ratios': ['3/2', '5/3', '2'],
            'exact_parameter_cases': checks, 'scope': 'Finite identity controls; all-orders claims use written proof.'}


def backend_audit():
    count = 0
    for a, b, c, d, e, f in product((-1, 0, 1), repeat=6):
        z = [[a, b, c], [b, d, e], [c, e, f]]
        det = a*d*f+2*b*c*e-a*e*e-d*c*c-f*b*b
        expected = min(a, d, f) >= 0 and min(a*d-b*b, a*f-c*c, d*f-e*e) >= 0 and det >= 0
        try:
            psd_rank(z)
            passed = True
        except ValueError:
            passed = False
        require(passed == expected, 'PSD engine versus all principal minors')
        count += passed
    require(count == 24, 'ternary PSD count')
    return {'symmetric_ternary_3x3': 729, 'PSD_count': count}


def negative_controls(cases):
    names = []

    def reject(name, work):
        try:
            work()
        except (ValueError, ZeroDivisionError):
            names.append(name)
            return
        raise ValueError('negative control accepted: '+name)

    for name, field, value in [('wrong_gamma', 'gamma', '7868026'),
                               ('wrong_rotation_domain', 'rotation_parameter', '3000'),
                               ('wrong_constant', 'expected_rotated_constant', '-1'),
                               ('wrong_M_bound', 'M_rhs', '1'),
                               ('wrong_coefficient_scale', 'coefficient_unit', '1')]:
        wrong = copy.deepcopy(cases[0])
        wrong[field] = value
        reject(name, lambda c=wrong: scalar_certificate(c))
    wrong = copy.deepcopy(cases[1])
    wrong['projected_lower_layers'][0] = '0'
    reject('unprojected_or_wrong_lower_vector', lambda: scalar_certificate(wrong))
    wrong = copy.deepcopy(cases[1])
    wrong['orbit_weights']['2/3'] = '16'
    reject('wrong_seven_orbit_coefficient', lambda: scalar_certificate(wrong))
    wrong = copy.deepcopy(cases[4])
    wrong['rotation_parameter'] = '0'
    reject('unrotated_ten_point_certificate', lambda: scalar_certificate(wrong))
    wrong = copy.deepcopy(cases[3])
    wrong['orbit_weights']['4/4'] = '255'
    reject('wrong_higher_order_orbit_coefficient', lambda: scalar_certificate(wrong))
    wrong = copy.deepcopy(cases[2])
    wrong['M_rhs'] = '159'
    reject('wrong_eight_point_bound', lambda: scalar_certificate(wrong))
    reject('numeric_float_input', lambda: rational(0.5))
    reject('decimal_string_input', lambda: rational('0.5'))
    reject('zero_denominator', lambda: rational('1/0'))
    reject('zero_diagonal_indefinite_matrix', lambda: psd_rank([[0, 1], [1, 0]]))
    return names


def earlier_review_comparison(info):
    """Credited review8196: same residual contraction, different rational dual."""
    previous = Q(510305, 1240558)
    difference = info['rhs']-previous
    require(difference == Q(639000305, 29260727684826) > 0,
            'exact comparison with review8196 rational bound')
    S = info['wn']+info['gamma']*info['un']
    disc = S*S-4*info['gamma']*info['q']**2
    # delta_opt=N/2*(S-sqrt(disc)). Squaring a nonnegative quantity
    # proves our gain is smaller, without evaluating any square root.
    residual = S-2*info['gap']/info['N']
    require(disc > 0 and residual > 0 and residual*residual > disc,
            'our rational gain lies below the algebraic relaxed optimum')
    c = Q(2805, 2)
    require(info['gamma']/c**2 == 4 and info['wn']/c**2 == Q(1696, 935) and
            info['un'] == Q(600, 187) and info['q']/c == Q(112, 561),
            'same projected six-point data as review8196')
    return {'review_graph_height': 8196,
            'review_rational_bound': str(previous),
            'our_rational_excess': str(difference),
            'credited_algebraic_review_bound_strictly_stronger': True,
            'scope': 'Review8196 confirms8154 and six-point refinements; new higher orders are not independently reviewed.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    certificate = json.loads(Path(__file__).with_name('CERTIFICATE.json').read_text())
    cases = certificate['cases']
    require(type(cases) is list and [x['n'] for x in cases] == [6, 7, 8, 9, 10], 'exact finite certificate coverage')
    infos = [scalar_certificate(case) for case in cases]
    output = []
    for info in infos:
        coefficient = coefficient_audit(info) if info['n'] <= 7 else orbit_audit(info)
        output.append({'n': info['n'], 'N': info['N'], 's': info['s'],
                       'geometric_tau': str(info['tau']), 'lower_star_projection': str(info['projection']),
                       'rotation_parameter': str(info['t']), 'positive_gap': str(info['gap']),
                       'rotated_constant': str(info['constant']), 'M_rhs': str(info['rhs']),
                       'literal_ordinary_cases': literal_audit(info) if info['n'] <= 7 else [],
                       **coefficient})
    result = {'agent': 'six-downset-3', 'role': 'researcher',
              'status': 'Written author-checked unformalized proof, not independently reviewed. Exact finite checks are supplementary.',
              'dual_cases': output, 'known_capped_six_baseline': capped_six_baseline(infos[0]),
              'credited_six_point_review_comparison': earlier_review_comparison(infos[0]),
              'general_moment_controls': moment_audit(), 'PSD_engine': backend_audit(),
              'negative_controls': negative_controls(cases)}
    raw = json.dumps(result, indent=2)+'\n'
    if args.output:
        args.output.write_text(raw)
    print(raw, end='')


if __name__ == '__main__':
    main()
