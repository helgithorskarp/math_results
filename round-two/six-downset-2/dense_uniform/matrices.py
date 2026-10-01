"""Dense two-moment capped-H constructor; exact Python 3.11+ stdlib.

Actual author: six-downset-2, researcher. Domain r>=2,n>=2r.
The unbounded proof is in PROOF.md; functions alone give no PSD verdict.
Uniform harmonics, the singleton/pair trade and full-vertex lift are
restated from the cited public predecessors, with a new dense seed.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations
from math import comb


def require(condition, message):
    if not condition:
        raise ValueError(message)


def falling(a, j):
    require(type(a) is int and type(j) is int and 0 <= j <= a,
            "Falling factorial domain")
    v = 1
    for b in range(j):
        v *= a-b
    return v


def counts(n, r):
    require(type(n) is int and type(r) is int and r >= 2 and n >= 2*r,
            "Integer domain r>=2,n>=2r")
    return sum(comb(n, a) for a in range(r+1)), sum(comb(n-1, a) for a in range(r))


def inverse2(A):
    require(len(A) == 2 and all(len(row) == 2 for row in A), "Moment shape")
    require(A[0][1] == A[1][0], "Moment symmetry")
    d = A[0][0]*A[1][1]-A[0][1]*A[1][0]
    require(A[0][0] > 0 and d > 0, "Positive definite moment")
    return ((Q(A[1][1], d), Q(-A[0][1], d)),
            (Q(-A[1][0], d), Q(A[0][0], d)))


@dataclass(frozen=True)
class Parameters:
    n: int
    r: int
    N: int
    s: int
    moment: tuple
    inverse: tuple
    beta: tuple
    t: Q

    @property
    def alpha(self):
        return Q((self.n-2)*(self.n-3)*(2*self.n-1), 2)

    @property
    def negative_trade(self):
        return (self.n-1)*(self.n-3)

    @property
    def delta(self):
        return Q(self.n*(self.n-1)*(self.n-2)*(self.n-3), 4)

    @property
    def gap(self):
        return Q(2, 3)*(1-1/self.alpha)


def parameters(n, r, t=None):
    """Rational t in [0,1/alpha]; t=0 is the unrepaired seed only."""
    N, s = counts(n, r)
    alpha = Q((n-2)*(n-3)*(2*n-1), 2)
    if t is None:
        t = 1/alpha
    require(type(t) in (int, Q), "Exact rational repair parameter")
    t = Q(t)
    require(0 <= t <= 1/alpha, "Closed sufficient repair interval")
    aa = range(1, r+1)
    A1 = sum(a*comb(n, a) for a in aa)
    A2 = sum(a*a*comb(n, a) for a in aa)
    M = ((N-1, A1), (A1, A2))
    Mi = inverse2(M)
    beta = [[Q(0)]*(r+1) for _ in range(r+1)]
    for a in aa:
        for b in aa:
            h = Mi[0][0]+(a+b)*Mi[0][1]+a*b*Mi[1][1]
            beta[a][b] = Q(comb(n, b), comb(n-a, b))*(1-s*h)
    return Parameters(n, r, N, s, M, Mi, tuple(tuple(row) for row in beta), t)


def coefficient(P):
    return [[Q(int(i == k == 0))-P.s*P.inverse[i][k] for k in range(2)]
            for i in range(2)]


def harmonic_moment(P, j):
    require(type(j) is int and 0 <= j <= P.r, "Moment degree")
    return [[sum((Q(comb(P.n, a))*
                    (Q(falling(a, j), falling(P.n-a, j)) if j else 1)*a**(i+k)
                    for a in range(max(1, j), P.r+1)), Q(0))
             for k in range(2)] for i in range(2)]


def trade(n, a, b):
    if a == b == 1:
        return (n-2)*(n-3)
    if {a, b} == {1, 2}:
        return -(n-3)
    return int(a == b == 2)


def sectors(P):
    """Complete harmonic blocks and positive diagonal metrics, not verdicts."""
    out = []
    for j in range(P.r+1):
        aa = list(range(max(1, j), P.r+1))
        g = [comb(P.n-2*j, a-j) for a in aa]
        K = [[Q(P.s*int(a == b)-(comb(P.n, b) if j == 0 else 0))+
              (-1)**j*(P.beta[a][b]+P.t*trade(P.n, a, b))*comb(P.n-a-j, b-j)
              for b in aa] for a in aa]
        U = [[P.N*int(i == k)-(comb(P.n, b) if j == 0 else 0)-K[i][k]
              for k, b in enumerate(aa)] for i, a in enumerate(aa)]
        out.append((j, aa, g, K, U))
    return out


def slack_entry(P, A, B):
    for v in (A, B):
        require(type(v) is int and 0 <= v < 2**P.n and v.bit_count() <= P.r,
                "Downset vertex")
    if A == B == 0:
        return 1+P.t*P.delta
    if A == 0 or B == 0:
        a = (A | B).bit_count()
        row = Q((P.n-1)*(P.n-2)*(P.n-3), 2) if a == 1 else (
            -Q((P.n-2)*(P.n-3), 2) if a == 2 else Q(0))
        return 1-P.t*row
    if A == B:
        return Q(P.s)
    if A & B:
        return Q(0)
    a, b = A.bit_count(), B.bit_count()
    return P.beta[a][b]+P.t*trade(P.n, a, b)


def literal_matrix(P):
    require(P.N <= 192, "Literal matrix order guard")
    V = [sum(1 << i for i in A) for a in range(P.r+1)
         for A in combinations(range(P.n), a)]
    return V, [[slack_entry(P, A, B) for B in V] for A in V]
