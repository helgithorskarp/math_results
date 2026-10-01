"""Exact capped H constructor for D(n,5), n >= 7.

The layer/core/lift and sparse rank repair extend the credited rank-four
construction by six-downset-3. The nine generic weights and five boundary
tables are the rank-five contribution of six-downset-2, researcher.
"""
from fractions import Fraction as Q
from itertools import combinations
from math import comb, factorial, prod
import json
from pathlib import Path

from poly import require


def choose(x, k):
    require(type(k) is int and k >= 0, 'nonnegative binomial index required')
    v = Q(1)
    for i in range(k):
        v = v*(x-i)/(i+1)
    return v


def sizes(n):
    return 1+sum(choose(n, a) for a in range(1, 6)), sum(choose(n-1, k) for k in range(5))


def parts(n):
    """Polynomial numerator and denominator factors (n-i) for beta_ab."""
    return {
        (1,4): (-(n-6)*(3*n**2-5*n+16), (2,3,4)),
        (1,5): (n**4+6*n**3-69*n**2+166*n-360, (2,3,4,5)),
        (2,4): (-2*(n**4-10*n**3+23*n**2-62*n+36), (2,3,4,5)),
        (2,5): (n**4+6*n**3-9*n**2+66*n-40, (2,3,4,5)),
        (3,4): (-(n**4-14*n**3+23*n**2-106*n+48), (3,4,5,6)),
        (3,5): (n**5-5*n**4-15*n**3+5*n**2-346*n+120, (3,4,5,6,7)),
        (4,4): (8*(2*n**5-12*n**4+14*n**3-279*n**2+335*n-942), (2,3,4,5,6,7)),
        (4,5): (n**7-15*n**6+51*n**5-165*n**4+684*n**3+6420*n**2-8416*n+27840, (2,3,4,5,6,7,8)),
        (5,5): (n**8-24*n**7+226*n**6-1064*n**5+3649*n**4-8096*n**3-15396*n**2+24544*n-102720,
                (2,3,4,5,6,7,8,9)),
    }


def generic_weights(n):
    n = Q(n)
    require(n >= 12 and n.denominator == 1, 'generic formula is certified only at integer n >= 12')
    B = [[Q(0) for _ in range(5)] for _ in range(5)]
    for (a,b), (p, factors) in parts(n).items():
        v = p/prod(n-i for i in factors)
        B[a-1][b-1] = B[b-1][a-1] = v
    return B


def weights(n):
    require(type(n) is int and n >= 7, 'integer n >= 7 required')
    if n >= 12:
        return generic_weights(n)
    data = json.loads(Path(__file__).with_name('BOUNDARY_CERTIFICATES.json').read_text())
    record = data[str(n)]
    B = [[Q(0) for _ in range(5)] for _ in range(5)]
    for key, v in record['beta'].items():
        a, b = map(int, key)
        B[a-1][b-1] = B[b-1][a-1] = Q(v)
    return B


def sectors(n, B, repaired=False):
    require(type(n) is int and n >= 7, 'integer n >= 7 required')
    N, s = sizes(Q(n))
    N, s = int(N), int(s)
    if repaired:
        B = [row[:] for row in B]
        eps, delta, bound = repair_constants(n)
        B[0][0] += eps*(n-2)*(n-3)
        B[0][1] -= eps*(n-3)
        B[1][0] -= eps*(n-3)
        B[1][1] += eps
    out = []
    for j in range(min(5, n//2)+1):
        layers = list(range(max(1,j), min(5,n-j)+1))
        g = [comb(n-2*j, a-j) for a in layers]
        K = [[Q(s*int(a == b) - (comb(n,b) if j == 0 else 0)) +
              (-1)**j * B[a-1][b-1] * (comb(n-a-j,b-j) if n-a-j >= b-j >= 0 else 0)
              for b in layers] for a in layers]
        out.append((K, g, layers))
    return N, s, out


def repair_constants(n):
    N, s = sizes(Q(n))
    m = N-1
    delta = Q(n*(n-1)*(n-2)*(n-3),4)
    bound = Q(3*(n-1)*(n-2)*(n-3),2)
    eps = delta/(8*m*bound**2)
    return eps, delta, bound


def members(n):
    return [sum(1 << i for i in A) for a in range(6) for A in combinations(range(n),a)]


def matrix(n, repaired=True):
    """Return (members, L), L=(N-s)M+sI; dense output, use small orders."""
    B = weights(n)
    V = members(n)
    N, s = sizes(Q(n))
    N, s = int(N), int(s)
    eps, delta, bound = repair_constants(n) if repaired else (Q(0),Q(0),Q(0))
    def entry(A, T):
        if A == 0 and T == 0:
            return 1+eps*delta
        if A == 0 or T == 0:
            a = (A | T).bit_count()
            r = Q((n-1)*(n-2)*(n-3),2) if a == 1 else -Q((n-2)*(n-3),2) if a == 2 else 0
            return 1-eps*r
        a,b = A.bit_count(),T.bit_count()
        if A == T:
            return Q(s)
        if A & T:
            return Q(0)
        trade = (n-2)*(n-3) if a == b == 1 else -(n-3) if {a,b} == {1,2} else 1 if a == b == 2 else 0
        return B[a-1][b-1]+eps*trade
    return V, [[entry(A,T) for T in V] for A in V]
