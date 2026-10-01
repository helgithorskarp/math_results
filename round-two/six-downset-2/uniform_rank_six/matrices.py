"""Exact rank-six uniform constructor; actual author six-downset-2, researcher.

Domain n>=8. The finite tables cover n=8,...,11. The n>=12 branch is the
published dense two-moment seed (LEMMA8843), specialized to rank six.
Complete truncated harmonics, trade, and empty-inclusive lift are credited
in PROOF.md. A constructor alone is not a PSD proof.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations
import json
from math import comb
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def choose(n, k):
    require(type(n) is int and type(k) is int and n >= 0,
            "Binomial integer domain")
    return comb(n, k) if 0 <= k <= n else 0


def counts(n):
    require(type(n) is int and n >= 8, "Integer domain n>=8, rank six")
    return sum(comb(n, a) for a in range(7)), sum(comb(n-1, a) for a in range(6))


def inverse2(M):
    require(len(M) == 2 and all(len(row) == 2 for row in M), "Moment shape")
    require(M[0][1] == M[1][0], "Moment symmetry")
    d = M[0][0]*M[1][1]-M[0][1]*M[1][0]
    require(M[0][0] > 0 and d > 0, "Positive moment determinant")
    return ((Q(M[1][1], d), Q(-M[0][1], d)),
            (Q(-M[1][0], d), Q(M[0][0], d)))


def read_tables(path=None):
    obj = json.loads(Path(path or Path(__file__).with_name("tables.json")).read_text())
    require(obj["schema"] == 1 and set(obj["cases"]) == {"8", "9", "10", "11"},
            "Exactly four boundary certificates")
    result = {}
    for key, entry in obj["cases"].items():
        n = int(key)
        require((entry["N"], entry["s"]) == counts(n), "Table cardinalities")
        rows = entry["weights"]
        require(len(rows) == 6 and all(len(row) == 6 for row in rows), "Table shape")
        require(all(type(v) is str and str(Q(v)) == v for row in rows for v in row),
                "Canonical rational table strings")
        beta = [[Q(0)]*7]+[[Q(0)]+[Q(v) for v in row] for row in rows]
        result[n] = tuple(tuple(row) for row in beta)
    return result


@dataclass(frozen=True)
class Parameters:
    n: int
    N: int
    s: int
    beta: tuple
    t: Q

    @property
    def r(self):
        return 6

    @property
    def branch(self):
        return "finite exact table" if self.n <= 11 else "LEMMA8843 dense seed"

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
        return Q(1, 8)


def validate_weights(P):
    require((P.N, P.s) == counts(P.n), "Whole-vertex cardinalities")
    require(len(P.beta) == 7 and all(len(row) == 7 for row in P.beta), "Weight shape")
    require(all(type(v) is Q for row in P.beta for v in row), "Exact rational weights")
    for a in range(7):
        for b in range(7):
            require(P.beta[a][b] == P.beta[b][a], "Weight symmetry")
            if a == 0 or b == 0 or a+b > P.n:
                require(P.beta[a][b] == 0, "Absent disjoint layer weight")
    for a in range(1, 7):
        require(sum(P.beta[a][b]*choose(P.n-a, b) for b in range(1, 7)) == P.N-1-P.s,
                "Centered disjoint row identity")
        require(sum(b*P.beta[a][b]*choose(P.n-a, b) for b in range(1, 7)) == (P.n-a)*P.s,
                "Star disjoint row identity")


def parameters(n, t=None):
    """Exact t in [0,1/(8 alpha)]; zero is only the unrepaired seed."""
    N, s = counts(n)
    alpha = Q((n-2)*(n-3)*(2*n-1), 2)
    if t is None:
        t = 1/(8*alpha)
    require(type(t) in (int, Q), "Exact rational repair parameter")
    t = Q(t)
    require(0 <= t <= 1/(8*alpha), "Closed sufficient repair interval")
    if n <= 11:
        beta = read_tables()[n]
    else:
        moment = ((N-1, n*s), (n*s, sum(a*a*comb(n, a) for a in range(1, 7))))
        Mi = inverse2(moment)
        weights = [[Q(0)]*7 for _ in range(7)]
        for a in range(1, 7):
            for b in range(1, 7):
                h = Mi[0][0]+(a+b)*Mi[0][1]+a*b*Mi[1][1]
                weights[a][b] = Q(comb(n, b), comb(n-a, b))*(1-s*h)
        beta = tuple(tuple(row) for row in weights)
    P = Parameters(n, N, s, beta, t)
    validate_weights(P)
    return P


def trade(n, a, b):
    if a == b == 1:
        return (n-2)*(n-3)
    if {a, b} == {1, 2}:
        return -(n-3)
    return int(a == b == 2)


def sectors(P):
    """All degrees and actual layer ranges, including above the middle layer."""
    out = []
    for j in range(min(6, P.n//2)+1):
        aa = list(range(max(1, j), min(6, P.n-j)+1))
        g = [comb(P.n-2*j, a-j) for a in aa]
        K = [[Q(P.s*int(a == b)-(comb(P.n, b) if j == 0 else 0))+
              (-1)**j*(P.beta[a][b]+P.t*trade(P.n, a, b))*choose(P.n-a-j, b-j)
              for b in aa] for a in aa]
        U = [[P.N*int(i == k)-(comb(P.n, b) if j == 0 else 0)-K[i][k]
              for k, b in enumerate(aa)] for i, a in enumerate(aa)]
        out.append((j, aa, g, K, U))
    return out


def slack_entry(P, A, B):
    for v in (A, B):
        require(type(v) is int and v >= 0 and not (v >> P.n) and v.bit_count() <= 6,
                "Original downset vertex")
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
    require(P.N <= 247, "Original matrix order guard 247")
    V = [sum(1 << i for i in A) for a in range(7)
         for A in combinations(range(P.n), a)]
    return V, [[slack_entry(P, A, B) for B in V] for A in V]
