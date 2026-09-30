#!/usr/bin/env python3
"""Exact uniform rank-three certificates. Python 3.11+, standard library only.

Author: six-downset-3, researcher. All checks use explicit exceptions.
Polynomial identities hold in Q(u), not by finite interpolation. Finite
dense-matrix and complete harmonic-basis audits validate the implementation;
the all-orders reduction and classification are written in PROOF.md.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, permutations
import json
from math import comb, gcd, lcm
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


# Independent rational-function arithmetic; ascending polynomial coefficients.
def trim(a):
    a = [Q(x) for x in a] or [Q(0)]
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return tuple(a)


def padd(a, b):
    return trim([(a[i] if i < len(a) else 0) +
                 (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])


def pscale(a, c):
    return trim([x * c for x in a])


def pmul(a, b):
    out = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return trim(out)


def pdivmod(a, b):
    a, b = list(trim(a)), trim(b)
    require(b != (Q(0),), 'zero polynomial divisor')
    out = [Q(0)] * max(1, len(a) - len(b) + 1)
    while trim(a) != (Q(0),) and len(a) >= len(b):
        k, c = len(a) - len(b), a[-1] / b[-1]
        out[k] += c
        for i, x in enumerate(b):
            a[i+k] -= c*x
        a = list(trim(a))
    return trim(out), trim(a)


def pgcd(a, b):
    a, b = trim(a), trim(b)
    while b != (Q(0),):
        a, b = b, pdivmod(a, b)[1]
    return pscale(a, 1/a[-1])


def pvalue(a, x):
    out = Q(0)
    for v in reversed(a):
        out = out*x + v
    return out


class RF:
    """Reduced exact element of Q(u), normalized to monic denominator."""
    def __init__(self, numerator=0, denominator=1):
        if isinstance(numerator, RF):
            require(denominator == 1, 'RF copy with denominator')
            self.p, self.q = numerator.p, numerator.q
            return
        p = trim(numerator if isinstance(numerator, (list, tuple)) else [numerator])
        q = trim(denominator if isinstance(denominator, (list, tuple)) else [denominator])
        require(q != (Q(0),), 'zero rational-function denominator')
        g = pgcd(p, q)
        p, rp = pdivmod(p, g)
        q, rq = pdivmod(q, g)
        require(rp == rq == (Q(0),), 'polynomial gcd division')
        self.p, self.q = pscale(p, 1/q[-1]), pscale(q, 1/q[-1])

    def __add__(self, other):
        b = RF(other)
        return RF(padd(pmul(self.p, b.q), pmul(b.p, self.q)), pmul(self.q, b.q))

    __radd__ = __add__

    def __neg__(self):
        return RF(pscale(self.p, -1), self.q)

    def __sub__(self, other):
        return self + (-RF(other))

    def __rsub__(self, other):
        return RF(other) + (-self)

    def __mul__(self, other):
        b = RF(other)
        return RF(pmul(self.p, b.p), pmul(self.q, b.q))

    __rmul__ = __mul__

    def __truediv__(self, other):
        b = RF(other)
        return RF(pmul(self.p, b.q), pmul(self.q, b.p))

    def __rtruediv__(self, other):
        return RF(other) / self

    def __pow__(self, k):
        require(type(k) is int and k >= 0, 'RF exponent')
        out = RF(1)
        for _ in range(k):
            out *= self
        return out

    def __eq__(self, other):
        b = RF(other)
        return pmul(self.p, b.q) == pmul(b.p, self.q)

    def value(self, u):
        d = pvalue(self.q, Q(u))
        require(d != 0, 'rational-function pole at specialization')
        return pvalue(self.p, Q(u)) / d


def choose(x, k):
    require(type(k) is int and k >= 0, 'binomial lower argument')
    out = 1
    for i in range(k):
        out = out * (x-i) / (i+1)
    return out


def determinant(a):
    n = len(a)
    require(all(len(row) == n for row in a), 'determinant shape')
    out = 0
    for p in permutations(range(n)):
        term = 1
        for i in range(n):
            term *= a[i][p[i]]
        if sum(p[i] > p[j] for i in range(n) for j in range(i+1, n)) % 2:
            term = -term
        out += term
    return out


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def e2(a):
    return sum(a[i][i]*a[j][j] - a[i][j]*a[j][i]
               for i in range(len(a)) for j in range(i+1, len(a)))


def shift_diagonal(a, shift, negate=False):
    return [[(-a[i][j] if negate else a[i][j]) + shift*int(i == j)
             for j in range(len(a))] for i in range(len(a))]


def weights(n):
    if type(n) is int and n == 5:
        return [[Q(-1), Q(1), Q(3)], [Q(1), Q(1), Q(8)], [Q(3), Q(8), Q(0)]]
    return [[0, -(n-4)/(n-2), (n+3)/(n-3)],
            [-(n-4)/(n-2), 2*(4*n-9)/((n-3)*(n-2)), (n+3)/(n-3)],
            [(n+3)/(n-3), (n+3)/(n-3), (n+1)/(n-5)]]


def exact_weights(n):
    require(n >= 5, 'weights require n>=5')
    if n == 5:
        return weights(5)
    u = RF([0, 1])
    return [[RF(x).value(n-6) for x in row] for row in weights(u+6)]


def sectors(n, beta):
    N = 1 + sum(choose(n, k) for k in (1, 2, 3))
    s = 1 + (n-1) + choose(n-1, 2)
    result = []
    for j in range(4):
        layers = list(range(max(1, j), 4))
        K = [[s*int(a == b) - (choose(n, b) if j == 0 else 0) +
              (-1)**j * beta[a-1][b-1] * choose(n-a-j, b-j)
              for b in layers] for a in layers]
        G = [choose(n-2*j, a-j) for a in layers]
        result.append((K, G))
    return N, s, result


def linear_checks(n, beta, N, s):
    count = 0
    for a in (1, 2, 3):
        require(sum(beta[a-1][b-1]*choose(n-a-1, b-1) for b in (1, 2, 3)) == s,
                'coordinate-star equation')
        require(sum(beta[a-1][b-1]*choose(n-a, b) for b in (1, 2, 3)) == N-1-s,
                'centering equation')
        count += 2
    return count


def margins(N, blocks, last=True):
    K0, K1, K2, K3 = [pair[0] for pair in blocks]
    tau, d = trace(K1), e2(K1)
    result = {'C0_gap1': trace(K0)-1, 'U0_gap1': N-trace(K0)-1,
              'C1_shift_trace': tau-2, 'C1_shift_det': d-tau+1,
              'U1_shift_trace': 2*(N-1)-tau,
              'U1_shift_det': (N-1)**2-(N-1)*tau+d,
              'C2_shift_diag': K2[0][0]-1,
              'C2_shift_det': determinant(shift_diagonal(K2, -1)),
              'U2_shift_diag': N-1-K2[0][0],
              'U2_shift_det': determinant(shift_diagonal(K2, N-1, True))}
    if last:
        result.update({'C3_gap1': trace(K3)-1, 'U3_gap1': N-trace(K3)-1})
    return result


def certify_margins(calculated, certificate):
    require(set(calculated) == set(certificate), 'positivity margin names')
    for name, value in calculated.items():
        entry = certificate[name]
        a, b = entry['numerator_ascending'], entry['denominator_ascending']
        require(type(a) is list and type(b) is list and a and b, 'coefficient arrays')
        require(all(type(x) is int and x >= 0 for x in a+b), 'nonnegative integer coefficients')
        require(a[0] > 0 and b[0] > 0 and a[-1] > 0 and b[-1] > 0,
                'strictly positive constants and nonzero leading terms')
        require(value == RF(a, b), 'wrong rational-function identity: '+name)
    return len(calculated)


def symbolic_check(certificate):
    u = RF([0, 1])
    n = u+6
    beta = weights(n)
    N, s, blocks = sectors(n, beta)
    identities = linear_checks(n, beta, N, s)
    for K, G in blocks:
        for i in range(len(K)):
            for j in range(len(K)):
                require(G[i]*K[i][j] == G[j]*K[j][i], 'harmonic metric symmetry')
                identities += 1
    K0, K1 = blocks[0][0], blocks[1][0]
    for v in ([1, 1, 1], [1, 2, 3]):
        for row in K0:
            require(sum(x*y for x, y in zip(row, v)) == 0, 'trivial kernel')
            identities += 1
    for row in K1:
        require(sum(row) == 0, 'degree-one kernel')
        identities += 1
    require(determinant(K0) == 0 and e2(K0) == 0 and determinant(K1) == 0,
            'sector nullities')
    identities += 3
    gap_count = certify_margins(margins(N, blocks), certificate['margins'])
    identities += gap_count
    m = N-1
    delta = n*(n-1)*(n-2)*(n-3)/4
    B = 3*(n-1)*(n-2)*(n-3)/2
    epsilon = 1/(12*(n*n+5)*(n-1)*(n-2)*(n-3))
    require(epsilon == delta/(8*m*B**2), 'trade epsilon identity')
    require(epsilon*B == 1/(8*(n*n+5)), 'trade norm bound identity')
    require(N-2*s == (n-1)*(n-2)*(n-3)/6, 'strict half density identity')
    identities += 3
    # Strict density decrease for all integers n>=4, checked as an identity.
    n4 = u+4
    def density(x):
        NN = 1+sum(choose(x, k) for k in (1, 2, 3))
        ss = 1+(x-1)+choose(x-1, 2)
        return ss/NN
    difference = density(n4)-density(n4+1)
    require(difference == 3*(n4-1)*(n4-2)*(n4*n4+3*n4+6) /
            ((n4+1)*(n4*n4-n4+6)*(n4+2)*(n4*n4+n4+6)), 'density decrease identity')
    identities += 1
    return {'coefficient_domain': 'Q(u)', 'substitution': 'n=6+u, u>=0',
            'identities_checked': identities, 'positive_margins': gap_count,
            'finite_specializations_used_to_prove_infinite_signs': 0,
            'density_decreases_for_all_n_at_least': 4}


# Direct exact matrix checks by fraction-free symmetric Schur elimination.
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


def nullspace(a, width):
    """Integer basis, with no reduction modulo a prime."""
    z = [[Q(x) for x in row] for row in a]
    require(all(len(row) == width for row in z), 'nullspace shape')
    pivots = []
    r = 0
    for j in range(width):
        pivot = next((i for i in range(r, len(z)) if z[i][j]), None)
        if pivot is None:
            continue
        z[r], z[pivot] = z[pivot], z[r]
        p = z[r][j]
        z[r] = [x/p for x in z[r]]
        for i in range(len(z)):
            if i != r and z[i][j]:
                c = z[i][j]
                z[i] = [x-c*y for x, y in zip(z[i], z[r])]
        pivots.append(j)
        r += 1
        if r == len(z):
            break
    basis = []
    for f in range(width):
        if f in pivots:
            continue
        v = [Q(0)]*width
        v[f] = 1
        for i, j in enumerate(pivots):
            v[j] = -z[i][f]
        d = lcm(*(x.denominator for x in v))
        v = [int(x*d) for x in v]
        g = gcd(*v)
        basis.append([x//g for x in v])
    require(all(sum(x*y for x, y in zip(row, v)) == 0 for row in a for v in basis),
            'nullspace residual')
    return basis


def inner(a, b):
    return sum(x*y for x, y in zip(a, b))


def matvec(a, x):
    return [inner(row, x) for row in a]


def inverse(a):
    N = len(a)
    require(all(len(row) == N for row in a), 'inverse shape')
    z = [[Q(x) for x in row]+[Q(i == j) for j in range(N)] for i, row in enumerate(a)]
    for k in range(N):
        p = next((i for i in range(k, N) if z[i][k]), None)
        require(p is not None, 'singular inverse')
        z[k], z[p] = z[p], z[k]
        pivot = z[k][k]
        z[k] = [x/pivot for x in z[k]]
        for i in range(N):
            if i != k and z[i][k]:
                c = z[i][k]
                z[i] = [x-c*y for x, y in zip(z[i], z[k])]
    result = [row[N:] for row in z]
    require(all(sum(a[i][k]*result[k][j] for k in range(N)) == int(i == j)
                for i in range(N) for j in range(N)), 'inverse residual')
    return result


def matrix_hash(a):
    raw = json.dumps([[str(Q(x)) for x in row] for row in a], separators=(',', ':')).encode()
    return sha256(raw).hexdigest()


def characteristic_polynomial_integer(a):
    """Integer Faddeev--LeVerrier, with exact trace divisions and Cayley check."""
    z, denominator = integer_matrix(a)
    N = len(z)
    B = [[int(i == j) for j in range(N)] for i in range(N)]
    coefficients = [1]
    for k in range(1, N+1):
        product = [[sum(z[i][r]*B[r][j] for r in range(N)) for j in range(N)] for i in range(N)]
        t = sum(product[i][i] for i in range(N))
        require(t % k == 0, 'characteristic-polynomial trace division')
        c = -t//k
        coefficients.append(c)
        B = [[product[i][j]+c*int(i == j) for j in range(N)] for i in range(N)]
    require(all(x == 0 for row in B for x in row), 'Cayley-Hamilton residual')
    return coefficients, denominator


def vertices(n):
    return [sum(1 << i for i in a) for k in range(4) for a in combinations(range(n), k)]


def harmonic_audit(n, beta, members):
    """All basis vectors, all three levels, not selected harmonic samples."""
    level = {a: [x for x in members if x.bit_count() == a] for a in range(4)}
    _, s, blocks = sectors(Q(n), beta)
    all_lifts = []
    dimensions = []
    actions = 0
    for j in range(4):
        basis = [[1]] if j == 0 else nullspace(
            [[int(r & x == r) for x in level[j]] for r in level[j-1]], len(level[j]))
        target = comb(n, j) - (comb(n, j-1) if j else 0)
        require(len(basis) == target, 'harmonic dimension')
        dimensions.append(target)
        if not basis:
            continue
        hgram = [[inner(v, w) for w in basis] for v in basis]
        require(psd_rank(hgram) == len(basis), 'harmonic basis independence')
        layers = list(range(max(1, j), 4))
        lifts = {}
        for a in layers:
            lifts[a] = [[sum(h[i] for i, x in enumerate(level[j]) if x & A == x)
                         for A in level[a]] for h in basis]
            for i, v in enumerate(lifts[a]):
                if j:
                    require(sum(v) == 0, 'nontrivial harmonic lift has nonzero mean')
                for k, w in enumerate(lifts[a]):
                    require(inner(v, w) == comb(n-2*j, a-j)*hgram[i][k],
                            'harmonic lift norm identity')
                full = [0]*len(members)
                index = {x: i for i, x in enumerate(members)}
                for A, value in zip(level[a], v):
                    full[index[A]] = value
                all_lifts.append((j, a, full))
        for b in layers:
            for a in (1, 2, 3):
                Dab = [[int(A & B == 0) for B in level[b]] for A in level[a]]
                for hidx, v in enumerate(lifts[b]):
                    image = matvec(Dab, v)
                    if a < j:
                        require(all(x == 0 for x in image), 'disjoint operator below harmonic degree')
                    else:
                        c = (-1)**j*comb(n-a-j, b-j) if n-a-j >= b-j >= 0 else 0
                        require(image == [c*x for x in lifts[a][hidx]], 'harmonic disjoint action')
                    core_image = [s*(v[i] if a == b else 0)-sum(v)+beta[a-1][b-1]*d
                                  for i, d in enumerate(image)]
                    if a < j:
                        require(all(x == 0 for x in core_image), 'core below harmonic degree')
                    else:
                        entry = blocks[j][0][layers.index(a)][layers.index(b)]
                        require(core_image == [entry*x for x in lifts[a][hidx]], 'complete core block action')
                    actions += 1
    for i, (j, a, v) in enumerate(all_lifts):
        for k, b, w in all_lifts[:i]:
            if j != k or a != b:
                require(inner(v, w) == 0, 'harmonic-sector orthogonality')
    require(len(all_lifts) == len(members)-1, 'complete nonempty-layer harmonic decomposition')
    return {'harmonic_dimensions': dimensions, 'complete_lifted_basis_size': len(all_lifts),
            'disjoint_basis_actions_checked': actions}


def core(n, members, beta):
    s = 1+n-1+comb(n-1, 2)
    return [[Q(s*int(A == B)-1) + (beta[A.bit_count()-1][B.bit_count()-1] if A & B == 0 else 0)
             for B in members[1:]] for A in members[1:]]


def trade(n, members):
    table = {(1, 1): (n-2)*(n-3), (1, 2): -(n-3), (2, 2): 1}
    return [[table.get(tuple(sorted((A.bit_count(), B.bit_count()))), 0)
             if A != B and A & B == 0 else 0 for B in members[1:]] for A in members[1:]]


def lift(C):
    m = len(C)
    r = [sum(row) for row in C]
    return [[1+sum(r)] + [1-x for x in r]] + \
           [[1-r[i]] + [1+x for x in C[i]] for i in range(m)]


def definition_check(n, members, L, s):
    N = len(members)
    require(members[0] == 0 and len(set(members)) == N, 'vertex ordering')
    require(all((A & ~(1 << i)) in members for A in members for i in range(n) if A >> i & 1),
            'downward closure')
    require(2*s < N, 'strict half density')
    require(all(len(row) == N for row in L), 'lift dimension')
    require(all(L[i][j] == L[j][i] for i in range(N) for j in range(N)), 'lift symmetry')
    require(all(sum(row) == N for row in L), 'H rows')
    require(all(L[i][j] == s*int(i == j) for i, A in enumerate(members)
                for j, B in enumerate(members) if A & B), 'H support and diagonal')
    stars = [[int(A >> i & 1) for A in members] for i in range(n)]
    require(all(sum(x) == s for x in stars), 'actual star sizes')
    require(all(matvec(L, x) == [s]*N for x in stars), 'forced full star kernel')
    return stars


def finite_case(n):
    members = vertices(n)
    N, m = len(members), len(members)-1
    s = 1+n-1+comb(n-1, 2)
    beta = exact_weights(n)
    NN, ss, blocks = sectors(Q(n), beta)
    require((NN, ss) == (N, s), 'size formula')
    linear_checks(Q(n), beta, NN, ss)
    mg = margins(NN, blocks, last=n >= 6)
    require(all(x > 0 for x in mg.values()), 'finite gap-one sector margin')
    C = core(n, members, beta)
    require(all(sum(row) == 0 for row in C), 'centered core')
    U = [[N*int(i == j)-1-C[i][j] for j in range(m)] for i in range(m)]
    centered_L = lift(C)
    stars = definition_check(n, members, centered_L, s)
    base_rank = psd_rank(C)
    require(base_rank == m-n-1 and psd_rank(U) == m, 'centered PSD/cap/rank')
    X = [[1]+[int(A >> i & 1) for i in range(n)] for A in members[1:]]
    gram = [[sum(row[i]*row[j] for row in X) for j in range(n+1)] for i in range(n+1)]
    Ginv = inverse(gram)
    XGinv = [[sum(row[k]*Ginv[k][j] for k in range(n+1)) for j in range(n+1)] for row in X]
    P = [[Q(i == j)-inner(XGinv[i], X[j]) for j in range(m)] for i in range(m)]
    require(psd_rank(P) == m-n-1 and all(matvec(P, [row[i] for row in X]) == [0]*m
                for i in range(n+1)), 'exact positive-complement projector')
    require(psd_rank([[C[i][j]-P[i][j] for j in range(m)] for i in range(m)]) == m-n-1,
            'direct full-core lower gap one')
    require(psd_rank([[U[i][j]-int(i == j) for j in range(m)] for i in range(m)]) == m-1,
            'direct full-core upper gap one')
    Delta = trade(n, members)
    delta = Q(n*(n-1)*(n-2)*(n-3), 4)
    B = Q(3*(n-1)*(n-2)*(n-3), 2)
    require(sum(map(sum, Delta)) == delta, 'trade total')
    require(max(sum(map(abs, row)) for row in Delta) == B, 'trade absolute row norm')
    require(all(matvec(Delta, x[1:]) == [0]*m for x in stars), 'trade star kernel')
    epsilon = Q(1, 12*(n*n+5)*(n-1)*(n-2)*(n-3))
    require(epsilon == delta/(8*m*B*B) and epsilon <= 1 and epsilon*B <= Q(1, 4),
            'trade parameter bounds')
    Cp = [[C[i][j]+epsilon*Delta[i][j] for j in range(m)] for i in range(m)]
    Up = [[U[i][j]-epsilon*Delta[i][j] for j in range(m)] for i in range(m)]
    Lp = lift(Cp)
    definition_check(n, members, Lp, s)
    require(psd_rank(Cp) == m-n and psd_rank(Up) == m, 'repaired PSD/cap/rank')
    require(psd_rank(Lp) == N-n, 'full lower rank')
    cap = [[N*int(i == j)-Lp[i][j] for j in range(N)] for i in range(N)]
    require(psd_rank(cap) == N-1, 'full upper rank')
    output = {'n': n, 'N': N, 's': s,
              'beta': [[str(x) for x in row] for row in beta],
              'centered_core_rank': base_rank, 'centered_full_rank': base_rank+1,
              'epsilon': str(epsilon), 'repaired_core_rank': m-n,
              'repaired_full_rank': N-n, 'upper_slack_rank': N-1,
              'maximum_families_from_kernel_proof': n,
              'full_core_gap_one_checks': True,
              'centered_core_sha256': matrix_hash(C), 'repaired_full_L_sha256': matrix_hash(Lp),
              'gap_one_margins': {k: str(v) for k, v in mg.items()}}
    output.update(harmonic_audit(n, beta, members))
    return output


def boundary_four():
    n = 4
    members = vertices(n)
    F = members[1:]
    N, m, s = len(members), len(F), 7
    C = [[Q(7*int(A == B or A ^ B == 15)-1) for B in F] for A in F]
    L = lift(C)
    stars = definition_check(n, members, L, s)
    require(psd_rank(C) == 6 and psd_rank(L) == 7, 'four-point lower ranks')
    U = [[N*int(i == j)-1-C[i][j] for j in range(m)] for i in range(m)]
    require(psd_rank(U) == m, 'four-point strict upper cap')
    M = [[(L[i][j]-s*int(i == j))/(N-s) for j in range(N)] for i in range(N)]
    for i, A in enumerate(members):
        for j, B in enumerate(members):
            expected = Q(-3, 4) if i == j == 0 else Q(1, 8) if i == 0 or j == 0 else \
                       Q(7, 8) if A ^ B == 15 else Q(0)
            require(M[i][j] == expected, 'four-point closed M formula')
    polynomial, denominator = characteristic_polynomial_integer(M)
    expected = [1]
    for root, multiplicity in ((8, 1), (7, 6), (-7, 8)):
        for _ in range(multiplicity):
            expanded = [0]*(len(expected)+1)
            for i, c in enumerate(expected):
                expanded[i] += c
                expanded[i+1] -= root*c
            expected = expanded
    require(denominator == 8 and polynomial == expected, 'exact boundary M spectrum')
    Bs = [[int(A.bit_count() == 3 or (A.bit_count() == 2 and A >> i & 1)) for A in members]
          for i in range(n)]
    Ts = [[int(A.bit_count() == 3 or (A.bit_count() == 2 and not (A >> i & 1))) for A in members]
          for i in range(n)]
    families = stars+Bs+Ts
    require(len({tuple(x) for x in families}) == 12, 'twelve distinct boundary families')
    for y in families:
        require(sum(y) == s, 'boundary family size')
        support = [A for A, x in zip(members, y) if x]
        require(all(A & B for A in support for B in support), 'boundary intersection')
        require(matvec(L, y) == [s]*N, 'boundary forced nonstar kernel')
    vectors = [[Q(x)-Q(s, N) for x in y] for y in stars+Bs]
    gram = [[inner(v, w) for w in vectors] for v in vectors]
    require(psd_rank(gram) == 8, 'universal eight-vector rank obstruction')
    for i in range(n):
        require(Ts[i] == [Q(sum(Bs[j][k] for j in range(n)), 2)-Bs[i][k] for k in range(N)],
                'triangle-family span identity')
    require([sum(stars[i][k] for i in range(n))-Q(sum(Bs[i][k] for i in range(n)), 2)
             for k in range(N)] == [int(k != 0) for k in range(N)],
            'constant nonempty vector is forced by maximum indicators')
    allowed = [(i,j) for i in range(N) for j in range(i,N) if members[i] & members[j] == 0]
    equations = [[int(i == a)*y[b] + (int(i == b)*y[a] if a != b else 0)
                  for a,b in allowed] for y in [[1]*N]+stars+Bs for i in range(N)]
    require(len(allowed) == 40 and not nullspace(equations, len(allowed)),
            'uniqueness from homogeneous supported row and forced-kernel equations')
    Delta = trade(n, members)
    y = Bs[0][1:]
    image = matvec(Delta,y)
    require(matvec(C,y) == [0]*m and inner(y,image) == 0 and inner(image,image) == 15,
            'universal four-point trade obstruction')
    # Exhaust all 2^14 nonempty-vertex subsets: no search shortcut or timeout.
    maxima = []
    largest = 0
    intersecting = 0
    for mask in range(1 << m):
        chosen = [F[i] for i in range(m) if mask >> i & 1]
        if all(A & B for A, B in combinations(chosen, 2)):
            intersecting += 1
            if len(chosen) > largest:
                largest, maxima = len(chosen), []
            if len(chosen) == largest:
                maxima.append(mask)
    encoded = [sum(x << i for i, x in enumerate(y[1:])) for y in families]
    require(largest == s and set(maxima) == set(encoded), 'complete boundary maximum-family census')
    return {'n': n, 'N': N, 's': s, 'core_rank': 6, 'full_L_rank': 7,
            'upper_slack_rank': N-1, 'universal_forced_kernel_dimension': 8,
            'maximum_families': 12, 'stars': 4, 'nonstars': 8,
            'unique_real_H_matrix': True, 'supported_symmetric_variables': len(allowed),
            'homogeneous_forced_constraint_nullity': 0,
            'constant_core_vector_forced_by_maxima': True,
            'trade_zero_form_nonzero_image_squared_norm': 15,
            'labelled_subset_domain': 1 << m, 'intersecting_subsets': intersecting,
            'maximum_family_masks_sorted': sorted(encoded), 'full_L_sha256': matrix_hash(L),
            'M_spectrum': {'1': 1, '7/8': 6, '-7/8': 8}}


def negative_controls(certificate):
    rejected = []
    def reject(name, f):
        try:
            f()
        except (ValueError, ZeroDivisionError, KeyError):
            rejected.append(name)
            return
        raise ValueError('damaged control was accepted: '+name)
    changed = deepcopy(certificate)
    changed['margins']['C0_gap1']['numerator_ascending'][0] += 1
    reject('changed polynomial coefficient', lambda: symbolic_check(changed))
    changed2 = deepcopy(certificate)
    changed2['margins']['U3_gap1']['denominator_ascending'][0] = 0
    reject('nonpositive denominator constant', lambda: symbolic_check(changed2))
    reject('zero quadratic-form with nonzero image', lambda: psd_rank([[0, 1], [1, 0]]))
    reject('negative eigenvalue', lambda: psd_rank([[1, 2], [2, 1]]))
    reject('asymmetry', lambda: psd_rank([[1, 0], [1, 1]]))
    beta = exact_weights(6)
    beta[0][2] += 1
    reject('damaged star equation', lambda: linear_checks(Q(6), beta, 42, 16))
    reject('excluded n=5 rational pole', lambda: RF(1, [1, 1]).value(-1))
    require(len(rejected) == 7, 'control count')
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path, default=Path(__file__).with_name('POSITIVITY_CERTIFICATE.json'))
    parser.add_argument('--check', type=Path)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--symbolic-only', action='store_true')
    args = parser.parse_args()
    certificate = json.loads(args.certificate.read_text())
    result = {'agent': 'six-downset-3', 'role': 'researcher',
              'claim_status': 'Written unformalized proof with exact rational-function and finite implementation checks; no independent review claim.',
              'symbolic': symbolic_check(certificate),
              'certificate_sha256': sha256(args.certificate.read_bytes()).hexdigest()}
    if not args.symbolic_only:
        result['boundary_four'] = boundary_four()
        result['finite_validation'] = [finite_case(n) for n in (5, 6, 7, 8)]
        result['negative_controls_rejected'] = negative_controls(certificate)
    if args.check:
        require(result == json.loads(args.check.read_text()), 'expected result differs')
    if args.output:
        args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'ok': True, 'symbolic_identities': result['symbolic']['identities_checked'],
                      'positive_margins': result['symbolic']['positive_margins'],
                      'finite_orders': [x['n'] for x in result.get('finite_validation', [])],
                      'boundary_four_maxima': result.get('boundary_four', {}).get('maximum_families'),
                      'negative_controls': len(result.get('negative_controls_rejected', []))}))


if __name__ == '__main__':
    main()
