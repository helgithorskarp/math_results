#!/usr/bin/env python3
"""Independent exact audit by six-reviewer-5; stdlib, no author inputs.

Polynomials use one fixed denominator, without rational-function reduction.
Dense PSD checks use rational symmetric Schur congruence, not Bareiss.
The all-order completeness and Schur argument are written in REVIEW.md.
"""
import argparse
from fractions import Fraction as F
from functools import reduce
import hashlib
from itertools import combinations, permutations, product
import json
from math import comb, factorial, gcd, lcm
from pathlib import Path


def need(condition, message):
    if not condition:
        raise ValueError(message)


def poly(v):
    a = list(map(F, v))
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return tuple(a)


def add(a, b):
    return poly([(a[i] if i < len(a) else 0) +
                 (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])


def scale(a, c):
    return poly([x*c for x in a])


def sub(a, b):
    return add(a, scale(b, -1))


def mul(a, b):
    c = [F(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i+j] += x*y
    return poly(c)


def pmul(*a):
    r = (F(1),)
    for x in a:
        r = mul(r, x)
    return r


def psum(a):
    r = (F(0),)
    for x in a:
        r = add(r, x)
    return r


def choose(a, k):
    if k < 0:
        return (F(0),)
    return scale(pmul(*[sub(a, (F(i),)) for i in range(k)]),
                 F(1, factorial(k)))


def pdet2(a):
    return sub(mul(a[0][0], a[1][1]), mul(a[0][1], a[1][0]))


def integer_record(num, den):
    need(num[0] > 0 and den[0] > 0, 'nonpositive constant')
    need(all(x >= 0 for x in num+den), 'negative coefficient')
    d = lcm(*(x.denominator for x in num+den))
    nn, dd = [int(d*x) for x in num], [int(d*x) for x in den]
    g = gcd(*nn, *dd)
    return {'numerator_ascending': [x//g for x in nn],
            'denominator_ascending': [x//g for x in dd]}


def symbolic():
    n = poly([6, 1])
    nm = lambda k: sub(n, (F(k),))
    Q = pmul(nm(2), nm(3), nm(5))
    s = scale(add(sub(mul(n, n), n), (F(2),)), F(1, 2))
    N = scale(psum([pmul(n, n, n), scale(n, 5), (F(6),)]), F(1, 6))
    B = [[(F(0),), scale(pmul(nm(4), nm(3), nm(5)), -1),
          pmul(add(n, (F(3),)), nm(2), nm(5))],
         [None, scale(mul(sub(scale(n, 4), (F(9),)), nm(5)), 2), None],
         [None, None, pmul(add(n, (F(1),)), nm(2), nm(3))]]
    B[1][0], B[1][2], B[2][0], B[2][1] = B[0][1], B[0][2], B[0][2], B[0][2]
    checks = 0
    for a in range(1, 4):
        lhs = psum([mul(B[a-1][b-1], choose(nm(a+1), b-1)) for b in range(1, 4)])
        need(lhs == mul(Q, s), 'star polynomial equation')
        lhs = psum([mul(B[a-1][b-1], choose(nm(a), b)) for b in range(1, 4)])
        need(lhs == mul(Q, sub(sub(N, (F(1),)), s)), 'constant polynomial equation')
        checks += 2
    sectors = []
    for j in range(4):
        layers = list(range(max(1, j), 4))
        A = [[psum([mul(Q, s) if a == b else (F(0),),
                    scale(mul(Q, choose(n, b)), -1) if j == 0 else (F(0),),
                    scale(mul(B[a-1][b-1], choose(nm(a+j), b-j)), (-1)**j)])
              for b in layers] for a in layers]
        G = [choose(nm(2*j), a-j) for a in layers]
        for i in range(len(A)):
            for k in range(len(A)):
                need(mul(G[i], A[i][k]) == mul(G[k], A[k][i]), 'sector metric symmetry')
                checks += 1
        nulls = ([1, 1, 1], [1, 2, 3]) if j == 0 else (([1, 1, 1],) if j == 1 else ())
        for v in nulls:
            for row in A:
                need(psum([scale(x, c) for x, c in zip(row, v)]) == (F(0),), 'sector kernel')
                checks += 1
        sectors.append(A)
    A0, A1, A2, A3 = sectors
    t0 = psum([A0[i][i] for i in range(3)])
    t1 = psum([A1[i][i] for i in range(3)])
    d1 = psum([sub(mul(A1[i][i], A1[k][k]), mul(A1[i][k], A1[k][i]))
               for i, k in combinations(range(3), 2)])
    H = mul(sub(N, (F(1),)), Q)
    shift2 = lambda a, z, sign: [[add(scale(a[i][k], sign), z if i == k else (F(0),))
                                for k in range(2)] for i in range(2)]
    entries = {
        'C0_gap1': (sub(t0, Q), Q),
        'U0_gap1': (sub(H, t0), Q),
        'C1_shift_trace': (sub(t1, scale(Q, 2)), Q),
        'C1_shift_det': (psum([d1, scale(mul(t1, Q), -1), mul(Q, Q)]), mul(Q, Q)),
        'U1_shift_trace': (sub(scale(H, 2), t1), Q),
        'U1_shift_det': (psum([mul(H, H), scale(mul(H, t1), -1), d1]), mul(Q, Q)),
        'C2_shift_diag': (sub(A2[0][0], Q), Q),
        'C2_shift_det': (pdet2(shift2(A2, scale(Q, -1), 1)), mul(Q, Q)),
        'U2_shift_diag': (sub(H, A2[0][0]), Q),
        'U2_shift_det': (pdet2(shift2(A2, H, -1)), mul(Q, Q)),
        'C3_gap1': (sub(A3[0][0], Q), Q),
        'U3_gap1': (sub(H, A3[0][0]), Q)}
    records = {k: integer_record(*v) for k, v in entries.items()}
    # Projection norm identity, density monotonicity, enlarged-interval ratio.
    m = sub(N, (F(1),))
    g = psum([scale(mul(n, n), 3), scale(n, -5), (F(4),)])
    f = psum([mul(n, n), scale(n, 5), (F(-8),)])
    h_num = pmul(n, nm(1), f)
    h_den = scale(g, 6)
    need(mul(sub(mul(m, g), scale(mul(n, mul(s, s)), 2)), h_den)
         == mul(h_num, g), 'exact projection norm')
    abc = pmul(nm(1), nm(2), nm(3))
    delta = scale(mul(n, abc), F(1, 4))
    bound = scale(abc, F(3, 2))
    t_num, t_den = g, scale(pmul(abc, psum([pmul(n, n, n), scale(mul(n, n), 7),
                                                       scale(n, -18), (F(12),)])), 3)
    need(pmul(t_num, scale(bound, 2), add(mul(bound, h_num), mul(delta, h_den)))
         == pmul(t_den, delta, h_den), 'larger interval formula')
    # Coefficients about n=5, generated by substitution rather than sampled.
    x = poly([5, 1])
    improve = sub(mul(add(mul(x, x), (F(5),)),
                      psum([scale(mul(x, x), 3), scale(x, -5), (F(4),)])),
                  mul(x, psum([pmul(x, x, x), scale(mul(x, x), 7), scale(x, -18), (F(12),)])))
    need(improve == poly([510, 433, 157, 28, 2]), 'ratio exceeds four n')
    # Cross multiplication of p(n)-p(n+1), with p numerator 6s and denominator 6N.
    nn = add(n, (F(1),))
    sn = scale(add(sub(mul(nn, nn), nn), (F(2),)), F(1, 2))
    Nn = scale(psum([pmul(nn, nn, nn), scale(nn, 5), (F(6),)]), F(1, 6))
    need(sub(mul(s, Nn), mul(sn, N)) == scale(pmul(nm(1), nm(2),
              psum([mul(n, n), scale(n, 3), (F(6),)])), F(1, 12)), 'strict density identity')
    return {'domain': 'Q[u], n=6+u', 'fixed_denominator': [str(x) for x in Q],
            'polynomial_identities': checks+4, 'positive_margins': records,
            'improvement_ratio_positive_at_n_5': [int(x) for x in improve]}


def matvec(A, v):
    return [sum((a*x for a, x in zip(row, v)), F(0)) for row in A]


def rank(A):
    A = [list(map(F, row)) for row in A]
    if not A:
        return 0
    r = 0
    for c in range(len(A[0])):
        p = next((i for i in range(r, len(A)) if A[i][c]), None)
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        d = A[r][c]
        for i in range(r+1, len(A)):
            if A[i][c]:
                t = A[i][c]/d
                for j in range(c, len(A[0])):
                    A[i][j] -= t*A[r][j]
        r += 1
        if r == len(A):
            break
    return r


def psd_rank(A):
    """Positive pivots and Schur complements; zero diagonal requires zero row."""
    A = [list(map(F, row)) for row in A]
    n = len(A)
    need(all(len(row) == n for row in A), 'nonsquare')
    need(all(A[i][j] == A[j][i] for i in range(n) for j in range(i)), 'asymmetric')
    r = 0
    for k in range(n):
        need(all(A[i][i] >= 0 for i in range(k, n)), 'negative pivot')
        p = next((i for i in range(k, n) if A[i][i]), None)
        if p is None:
            need(all(A[i][j] == 0 for i in range(k, n) for j in range(k, n)),
                 'zero form with nonzero image')
            break
        if p != k:
            A[p], A[k] = A[k], A[p]
            for row in A:
                row[p], row[k] = row[k], row[p]
        d = A[k][k]
        for i in range(k+1, n):
            t = A[i][k]/d
            for j in range(i, n):
                A[i][j] -= t*A[k][j]
                A[j][i] = A[i][j]
        r += 1
    return r


def beta(n):
    need(n >= 5, 'excluded small order')
    if n == 5:
        return [[F(x) for x in row] for row in [[-1, 1, 3], [1, 1, 8], [3, 8, 0]]]
    return [[F(0), -F(n-4, n-2), F(n+3, n-3)],
            [-F(n-4, n-2), F(2*(4*n-9), (n-3)*(n-2)), F(n+3, n-3)],
            [F(n+3, n-3), F(n+3, n-3), F(n+1, n-5)]]


def vertices(n):
    return [x for x in range(1 << n) if x.bit_count() <= 3]


def core(n, V):
    s, b = F((n*n-n+2)//2), beta(n)
    return [[s*(i == j)-1+(b[x.bit_count()-1][y.bit_count()-1] if x & y == 0 else 0)
             for j, y in enumerate(V)] for i, x in enumerate(V)]


def trade(n, V):
    weights = {(1, 1): (n-2)*(n-3), (1, 2): -(n-3), (2, 2): 1}
    return [[F(weights.get(tuple(sorted((x.bit_count(), y.bit_count()))), 0) if x & y == 0 else 0)
             for y in V] for x in V]


def lift(C):
    m = len(C)
    rows = [sum(row) for row in C]
    return [[1+sum(rows)]+[1-x for x in rows]] + [
        [1-rows[i]]+[1+x for x in row] for i, row in enumerate(C)]


def slack(L, N):
    return [[N*(i == j)-x for j, x in enumerate(row)] for i, row in enumerate(L)]


def canonical_hash(A, V):
    """Compare ordering-neutral meaning in the author's explicitly stated order."""
    order = sorted(range(len(V)), key=lambda i: (V[i].bit_count(),
                    tuple(j for j in range(max(V).bit_length()) if V[i] >> j & 1)))
    body = json.dumps([[str(A[i][j]) for j in order] for i in order], separators=(',', ':'))
    return hashlib.sha256(body.encode()).hexdigest()


def harmonic_controls(n, V):
    count = 0
    dims = []
    for j in range(4):
        d = comb(n, j)-(comb(n, j-1) if j else 0)
        if j == 3 and n == 5:
            d = 0
        dims.append(d)
        if not d:
            continue
        W = {a: {x: 1 if j == 0 else
                  reduce(lambda z, t: z*t,
                  [((x >> (2*r)) & 1)-((x >> (2*r+1)) & 1) for r in range(j)], 1)
                  for x in V if x.bit_count() == a}
             for a in range(max(1, j), 4)}
        for a, va in W.items():
            for b, vb in W.items():
                k = (-1)**j*(comb(n-a-j, b-j) if n-a-j >= b-j else 0)
                for x, value in va.items():
                    need(sum(v for y, v in vb.items() if x & y == 0) == k*value,
                         'literal harmonic disjoint action')
                    count += 1
                need(sum(v*v for v in vb.values()) == (2**j)*comb(n-2*j, b-j),
                     'paired harmonic norm')
    need(sum(dims[j]*(3-max(1, j)+1) for j in range(4)) == len(V)-1,
         'dimension exhaustion')
    return {'dimensions': dims, 'literal_actions': count}


def finite(n):
    V = vertices(n)
    Fv = V[1:]
    N, m, s = len(V), len(Fv), (n*n-n+2)//2
    C, D = core(n, Fv), trade(n, Fv)
    stars = [[F(bool(x >> i & 1)) for x in Fv] for i in range(n)]
    zero = [F(0)]*m
    need(matvec(C, [F(1)]*m) == zero, 'centered constant kernel')
    need(all(matvec(C, v) == zero and matvec(D, v) == zero for v in stars), 'star kernel')
    need(rank(stars+[[F(1)]*m]) == n+1, 'centered forced dimension')
    delta = sum(sum(row) for row in D)
    B = max(sum(abs(x) for x in row) for row in D)
    need(delta == F(n*(n-1)*(n-2)*(n-3), 4), 'trade total')
    need(B == F(3*(n-1)*(n-2)*(n-3), 2), 'trade row norm')
    h = [1-F(s, s+(n-1)**2)*x.bit_count() for x in Fv]
    need(all(sum(a*b for a, b in zip(h, v)) == 0 for v in stars), 'projection orthogonality')
    h2 = sum(x*x for x in h)
    need(h2 == F(n*(n-1)*(n*n+5*n-8), 6*(3*n*n-5*n+4)), 'projection norm')
    new_t = F(3*n*n-5*n+4, 3*(n-1)*(n-2)*(n-3)*(n**3+7*n*n-18*n+12))
    old_t = F(1, 12*(n*n+5)*(n-1)*(n-2)*(n-3))
    need(new_t == delta/(2*B*(B*h2+delta)) and new_t/old_t > 4*n, 'improved interval')
    parameters = [('target', old_t), ('improved_closed_endpoint', new_t)] if n <= 8 else [('improved_closed_endpoint', new_t)]
    results = []
    for name, t in parameters:
        Cp = [[c+t*d for c, d in zip(row, dr)] for row, dr in zip(C, D)]
        L = lift(Cp)
        need(all(sum(row) == N for row in L), 'lift row sums')
        need(all(L[i][j] == (s if i == j else 0)
                 for i, x in enumerate(V) for j, y in enumerate(V) if x & y), 'lift support')
        for v in stars:
            z = [-F(s, N)]+[x-F(s, N) for x in v]
            need(matvec(L, z) == [F(0)]*N, 'full centered star kernel')
        rl, ru = psd_rank(L), psd_rank(slack(L, N))
        need((rl, ru) == (N-n, N-1), 'full ranks')
        a = delta/h2
        need(t*B < F(1, 2) and a-t*B*B/(1-t*B) > a/2, 'strict Schur margin')
        results.append({'parameter': name, 'epsilon': str(t), 'L_rank': rl,
                        'upper_rank': ru, 'full_L_sha256': canonical_hash(L, V)})
    return {'n': n, 'N': N, 's': s, 'projection_squared_norm': str(h2),
            'trade_total': str(delta), 'row_norm_bound': str(B),
            'repair_ratio': str(new_t/old_t), 'centered_core_sha256': canonical_hash(C, Fv),
            'parameters': results, 'harmonic_controls': harmonic_controls(n, V)}


def solve_unique(rows, variables):
    A = [[F(x) for x in row] for row in rows]
    r, pivots = 0, []
    for c in range(variables):
        p = next((i for i in range(r, len(A)) if A[i][c]), None)
        if p is None:
            continue
        A[p], A[r] = A[r], A[p]
        d = A[r][c]
        A[r] = [x/d for x in A[r]]
        for i in range(len(A)):
            if i != r and A[i][c]:
                t = A[i][c]
                A[i] = [x-t*y for x, y in zip(A[i], A[r])]
        pivots.append(c)
        r += 1
    need(all(any(row[:-1]) or not row[-1] for row in A), 'inconsistent forced system')
    need(r == variables, 'nonunique forced system')
    return [A[i][-1] for i in range(r)]


def boundary_four():
    V = vertices(4)
    Fv = V[1:]
    families = []
    nodes = 0
    def visit(available, selected):
        nonlocal nodes
        nodes += 1
        if not available:
            families.append(selected)
            return
        i = (available & -available).bit_length()-1
        left = available & ~(1 << i)
        visit(left, selected)
        compatible = sum(1 << j for j, x in enumerate(Fv) if x & Fv[i])
        visit(left & compatible, selected | (1 << i))
    visit((1 << len(Fv))-1, 0)
    biggest = max(x.bit_count() for x in families)
    maxima = sorted(x for x in families if x.bit_count() == biggest)
    wanted, S, B = [], [], []
    for i in range(4):
        sv = [int(bool(x >> i & 1)) for x in Fv]
        bv = [int(x.bit_count() == 3 or (x.bit_count() == 2 and x >> i & 1)) for x in Fv]
        tv = [int(x.bit_count() == 3 or (x.bit_count() == 2 and not (x >> i & 1))) for x in Fv]
        S.append([0]+sv)
        B.append([0]+bv)
        wanted += [sum(v << j for j, v in enumerate(z)) for z in [sv, bv, tv]]
    need(len(families) == 688 and biggest == 7 and maxima == sorted(wanted), 'boundary census')
    Z = [[15*x-7 for x in y] for y in S+B]
    need(rank(Z) == 8, 'universal forced kernel rank')
    C = [[F(7*int(x == y or x ^ y == 15)-1) for y in Fv] for x in Fv]
    L = lift(C)
    M = [[(x-7*(i == j))/8 for j, x in enumerate(row)] for i, row in enumerate(L)]
    need(psd_rank(C) == 6 and psd_rank(L) == 7 and psd_rank(slack(L, 15)) == 14, 'boundary PSD ranks')
    for y in S+B:
        need(matvec(M, y) == [F(7, 8)*(1-x) for x in y], 'forced family eigenvector')
    variables = [(i, j) for i, x in enumerate(V) for j in range(i, len(V)) if not x & V[j]]
    equations = []
    maximum_vectors = [[0]+[int(w >> j & 1) for j in range(len(Fv))] for w in maxima]
    for v, rhs in [([F(1)]*15, [F(1)]*15)] + [(v, [F(7, 8)*(1-x) for x in v]) for v in maximum_vectors]:
        for k in range(15):
            row = [F(0)]*len(variables)
            for q, (i, j) in enumerate(variables):
                if k == i:
                    row[q] += v[j]
                if k == j and i != j:
                    row[q] += v[i]
            equations.append(row+[rhs[k]])
    need(len(variables) == 40, 'supported variable count')
    solution = solve_unique(equations, len(variables))
    need(solution == [M[i][j] for i, j in variables], 'unique boundary matrix')
    need(M[0][0] == -F(3, 4), 'empty loop')
    # The eight-dimensional forced span already contains the centered empty vector.
    empty = [14]+[-1]*14
    need(rank(Z+[empty]) == 8, 'empty direction not additional')
    D = trade(4, Fv)
    y = B[0][1:]
    image = matvec(D, y)
    need(sum(x*z for x, z in zip(y, image)) == 0 and sum(x*x for x in image) == 15,
         'trade obstruction')
    # Check the exact nonconstant spectral identity (M-7/8 I)(M+7/8 I)=15/64 J/15.
    for i in range(15):
        for j in range(15):
            m2 = sum(M[i][k]*M[k][j] for k in range(15))
            need(m2-F(49, 64)*(i == j) == F(1, 64), 'boundary spectral identity')
    return {'N': 15, 's': 7, 'search_nodes': nodes, 'intersecting_families': len(families),
            'maximum_families': 12, 'maximum_size': biggest,
            'supported_variables': 40, 'unique_real_H': True,
            'forced_kernel_dimension': 8, 'L_rank': 7, 'upper_rank': 14,
            'trade_image_squared_norm': 15, 'full_L_sha256': canonical_hash(L, V),
            'spectrum': {'1': 1, '7/8': 6, '-7/8': 8}}


def determinant3(a):
    return sum(((-1 if sum(p[i] > p[j] for i in range(3) for j in range(i+1, 3)) % 2 else 1)
                *a[0][p[0]]*a[1][p[1]]*a[2][p[2]] for p in permutations(range(3))), F(0))


def five_sectors():
    n, s, N, b = 5, 11, 26, beta(5)
    K = []
    for j in range(3):
        layers = range(max(1, j), 4)
        A = [[F(s*(a == c))-(comb(n, c) if j == 0 else 0)
              +(-1)**j*b[a-1][c-1]*(comb(n-a-j, c-j) if n-a-j >= c-j else 0)
              for c in layers] for a in layers]
        K.append(A)
    trace0 = sum(K[0][i][i] for i in range(3))
    tau = sum(K[1][i][i] for i in range(3))
    d = sum(K[1][i][i]*K[1][k][k]-K[1][i][k]*K[1][k][i]
            for i, k in combinations(range(3), 2))
    margins = [trace0-1, N-1-trace0, tau-2, d-tau+1,
               2*(N-1)-tau, (N-1)**2-(N-1)*tau+d,
               K[2][0][0]-1,
               (K[2][0][0]-1)*(K[2][1][1]-1)-K[2][0][1]*K[2][1][0],
               N-1-K[2][0][0],
               (N-1-K[2][0][0])*(N-1-K[2][1][1])-K[2][0][1]*K[2][1][0]]
    need(margins == list(map(F, [6, 18, 30, 214, 18, 70, 11, 46, 13, 118])),
         'separate n=5 sector margins')
    return {'gap_one_margins': [str(x) for x in margins],
            'K1': [[str(x) for x in row] for row in K[1]],
            'K2': [[str(x) for x in row] for row in K[2]], 'absent_H3_dimension': 0}


def product_controls():
    additive = []
    for w in product((0, 1), repeat=4):
        if w[0]+w[3] == w[1]+w[2]:
            need(w[0] == w[1] and w[2] == w[3] or w[0] == w[2] and w[1] == w[3],
                 'additive Boolean rectangle')
            additive.append(w)
    need(len(additive) == 6, 'additive rectangle count')
    family = [x for x in range(8) if x.bit_count() >= 2]
    need(len(family) == 4 and all(x & y for x in family for y in family), 'half-density family')
    need(all(family != [x for x in range(8) if x >> i & 1] for i in range(3)),
         'half-density noncylinder')
    eigenvalues = {F(1): 1, F(7, 8): 6, -F(7, 8): 8}
    tensored = {}
    for x, a in eigenvalues.items():
        for y, b in eigenvalues.items():
            tensored[x*y] = tensored.get(x*y, 0)+a*b
    need(min(tensored) == -F(7, 8) and tensored[-F(7, 8)] == 16 and tensored[F(1)] == 1
         and sum(tensored.values()) == 225, 'four by four tensor spectrum')
    return {'Boolean_rectangles_checked': 16, 'additive_rectangles': 6,
            'half_density_nonstar_maximum': family,
            'four_by_four_spectral_multiplicities': {str(x): v for x, v in sorted(tensored.items())},
            'four_by_four_L_rank': 209}


def controls():
    count = 0
    for values in product((-1, 0, 1), repeat=6):
        a, b, c, d, e, f = values
        A = [[a, d, e], [d, b, f], [e, f, c]]
        expected = min(a, b, c, a*b-d*d, a*c-e*e, b*c-f*f, determinant3(A)) >= 0
        try:
            psd_rank(A)
            got = True
        except ValueError:
            got = False
        need(got == expected, 'PSD/principal-minor disagreement')
        count += 1
    rejected = 0
    for A in [[[0, 1], [1, 0]], [[-1]], [[1, 2], [0, 1]], [[1, 0]],
              [[1, 1], [1, F(1, 2)]]]:
        try:
            psd_rank(A)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('malformed or indefinite control accepted')
    need(psd_rank([[F(1, 3), F(2, 3)], [F(2, 3), F(4, 3)]]) == 1, 'rational Gram control')
    try:
        integer_record((F(-1), F(1)), (F(1),))
    except ValueError:
        rejected += 1
    else:
        raise ValueError('invalid positivity record accepted')
    return {'symmetric_3_by_3_principal_minor_comparisons': count,
            'invalid_inputs_rejected': rejected, 'rational_Gram_rank': 1}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', type=Path)
    ap.add_argument('--check', type=Path)
    args = ap.parse_args()
    result = {'agent': 'six-reviewer-5', 'role': 'independent mathematical reviewer',
              'method': 'fixed-denominator polynomials, rational Schur congruence, recursive census and forced linear system',
              'symbolic': symbolic(), 'separate_five': five_sectors(), 'boundary_four': boundary_four(),
              'finite': [finite(n) for n in range(5, 10)], 'controls': controls(),
              'product_controls': product_controls()}
    body = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.write:
        args.write.write_text(body)
    if args.check:
        need(args.check.read_text() == body, 'expected summary differs')
    print('Independent uniform rank-three audit passed; summary SHA256 '+hashlib.sha256(body.encode()).hexdigest())


if __name__ == '__main__':
    main()
