"""Exact complement-plus-2/2-plus-2/3 blocks; n>=7 only.

The proof of completeness over the reals is separate from this arithmetic.
Author: six-downset-3, researcher.
"""
from fractions import Fraction as F
from math import comb

from matrices import parameters, rational, require


def inverse(a):
    n = len(a)
    b = [[rational(x) for x in row]+[F(i == j) for j in range(n)]
         for i, row in enumerate(a)]
    require(n and all(len(row) == 2*n for row in b), 'inverse shape')
    for j in range(n):
        pivot = next((i for i in range(j, n) if b[i][j]), None)
        require(pivot is not None, 'singular inverse')
        b[j], b[pivot] = b[pivot], b[j]
        scale = b[j][j]
        b[j] = [x/scale for x in b[j]]
        for i in range(n):
            if i != j:
                scale = b[i][j]
                b[i] = [x-scale*y for x, y in zip(b[i], b[j])]
    result = [row[n:] for row in b]
    require(all(sum(a[i][k]*result[k][j] for k in range(n)) == (i == j)
                for i in range(n) for j in range(n)), 'inverse residual')
    return result


def blocks(n, z, epsilon, delta):
    """Input z is already reflected; output all six bilinear PSD blocks."""
    require(type(n) is int and n >= 7, 'integer n>=7 required')
    z = {k: rational(value) for k, value in z.items()}
    epsilon, delta = rational(epsilon), rational(delta)
    layers = list(range(2, n-1)); d = len(layers)
    require(set(z) == set(layers), 'all reflected layers required')
    require(all(z[k] == z[n-k] for k in layers), 'unreflected coefficients')
    N, s = 2**n-n-1, 2**(n-1)-n
    b = [comb(n, k) for k in layers]
    alpha = [comb(n-2, k-1) for k in layers]
    g0 = [[F(b[i] if i == j else 0)+F(k*l*b[i]*b[j], n)
           +(k-1)*(l-1)*b[i]*b[j] for j, l in enumerate(layers)] for i, k in enumerate(layers)]
    g1 = [[F(alpha[i] if i == j else 0)+alpha[i]*alpha[j]
           for j in range(d)] for i in range(d)]
    q0 = [[F(s*b[i] if i == j else 0)-b[i]*b[j]
           for j in range(d)] for i in range(d)]
    q1 = [[F(s*alpha[i] if i == j else 0) for j in range(d)] for i in range(d)]
    for i, k in enumerate(layers):
        j = layers.index(n-k)
        q0[i][j] += b[i]*(s-z[k])
        q1[i][j] -= alpha[i]*(s-z[k])
    q0[0][0] += comb(n-2, 2)*b[0]*epsilon
    q1[0][0] -= (n-3)*alpha[0]*epsilon
    for i, j in ((0, 1), (1, 0)):
        q0[i][j] += b[0]*comb(n-2, 3)*delta
        q1[i][j] -= alpha[0]*comb(n-3, 2)*delta
    inv0, inv1 = inverse(g0), inverse(g1)
    u0 = [[N*b[i]*b[j]*inv0[i][j]-q0[i][j] for j in range(d)] for i in range(d)]
    u1 = [[N*alpha[i]*alpha[j]*inv1[i][j]-q1[i][j] for j in range(d)] for i in range(d)]
    q = n-4
    c2 = [[s+epsilon, q*delta, F(0), s-z[2]],
          [q*delta, F(q*s), q*(s-z[3]), F(0)],
          [F(0), q*(s-z[3]), F(q*s), F(0)],
          [s-z[2], F(0), F(0), F(s)]]
    norms = [1, q, q, 1]
    u2 = [[F(N*norms[i] if i == j else 0)-c2[i][j] for j in range(4)] for i in range(4)]
    return {'Q0': q0, 'Q1': q1, 'U0': u0, 'U1': u1, 'C2': c2, 'U2': u2}, g0, g1


def from_parameters(n, z, epsilon, delta):
    z, epsilon, delta = parameters(n, z, epsilon, delta)
    return blocks(n, z, epsilon, delta)
