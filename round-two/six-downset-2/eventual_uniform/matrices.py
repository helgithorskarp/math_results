"""Rational uniform core with weights supported on the last two layers.

Author: six-downset-2, researcher. Affine formulas work at r>=2,n>=2r;
the written theorem certifies capped maximal rank at n>=32*r*r.
The core lift, harmonic sectors and sparse repair are credited prior work.
No matrix or spectrum is inferred to be PSD from the affine constructor.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations
from math import comb


def require(condition, message):
    if not condition:
        raise ValueError(message)


def domain(n, r):
    require(type(n) is int and type(r) is int and r >= 2 and n >= 2*r,
            "Integers r>=2,n>=2r required")


@dataclass(frozen=True)
class Parameters:
    n: int
    r: int
    N: int
    s: int
    beta: tuple
    epsilon: Q
    delta: Q
    trade_bound: Q


def parameters(n, r, *, certified=True):
    domain(n, r)
    require(not certified or n >= 32*r*r, "The unbounded theorem requires n>=32r^2")
    N = sum(comb(n, a) for a in range(r+1))
    s = sum(comb(n-1, a) for a in range(r))
    T, p = N-1-s, r-1
    b = [[Q(0) for _ in range(r+1)] for _ in range(r+1)]
    for a in range(1, p):
        x = r*T-(n-a)*s
        b[a][p] = b[p][a] = Q(x, comb(n-a, p))
        b[a][r] = b[r][a] = Q(T-x, comb(n-a, r))
    Lp = sum((b[p][a]*comb(n-p, a) for a in range(1, p)), Q(0))
    Hp = sum((a*b[p][a]*comb(n-p, a) for a in range(1, p)), Q(0))
    X = r*(T-Lp)-((n-p)*s-Hp)
    Y = T-Lp-X
    b[p][p] = Q(X)/comb(n-p, p)
    b[p][r] = b[r][p] = Q(Y)/comb(n-p, r)
    Lr = sum((b[r][a]*comb(n-r, a) for a in range(1, p)), Q(0))
    b[r][r] = Q(T-Lr-b[r][p]*comb(n-r, p))/comb(n-r, r)
    require(all(type(v) is Q for row in b for v in row), "Nonrational coefficient")
    delta = Q(n*(n-1)*(n-2)*(n-3), 4)
    B = Q(3*(n-1)*(n-2)*(n-3), 2)
    eps = delta/(8*(N-1)*B*B)
    return Parameters(n, r, N, s, tuple(tuple(row) for row in b), eps, delta, B)


def trade(n, a, b):
    if a == b == 1:
        return (n-2)*(n-3)
    if {a, b} == {1, 2}:
        return -(n-3)
    return int(a == b == 2)


def sectors(P, *, repaired=False):
    """Return (j,layer_indices,metric,lower_core,upper_core) for all sectors."""
    n, r, N, s = P.n, P.r, P.N, P.s
    out = []
    for j in range(r+1):
        aa = list(range(max(1, j), r+1))
        g = [comb(n-2*j, a-j) for a in aa]
        K = [[Q(s*int(a == b)-(comb(n, b) if j == 0 else 0)) +
              (-1)**j*(P.beta[a][b]+(P.epsilon*trade(n,a,b) if repaired else 0))*
              comb(n-a-j, b-j) for b in aa] for a in aa]
        U = [[N*int(a == b)-(comb(n,b) if j == 0 else 0)-K[i][k]
              for k,b in enumerate(aa)] for i,a in enumerate(aa)]
        out.append((j, aa, g, K, U))
    return out


def quotients(P):
    """Matrices on the forced-kernel quotients, then the higher sectors."""
    blocks = sectors(P)
    K0, K1, p, r = blocks[0][3], blocks[1][3], P.r-1, P.r
    A0 = [[K0[a-1][b-1]+(a-r)*K0[p-1][b-1]+(p-a)*K0[r-1][b-1]
           for b in range(1,p)] for a in range(1,p)]
    A1 = [[K1[a-1][b-1]-K1[r-1][b-1]
           for b in range(1,r)] for a in range(1,r)]
    return [A0, A1]+[z[3] for z in blocks[2:]]


def residual(H, g, low_count, scale):
    """Exact Schur residual when the leading block is scale*diag(g)."""
    d = len(H)
    require(d-low_count <= 2 and scale > 0, "Residual domain")
    require(all(H[i][k] == scale*g[i]*int(i == k)
                for i in range(low_count) for k in range(low_count)),
            "Leading block is not the claimed diagonal")
    return [[H[i][k]-sum((H[a][i]*H[a][k]/(scale*g[a])
                         for a in range(low_count)), Q(0))
             for k in range(low_count,d)] for i in range(low_count,d)]


def residuals(P):
    """Criterion for the centered, UNREPAIRED core and cap only.

    The repaired trade changes the leading block. It must not be passed
    through this criterion. Degree-zero C uses its separate scalar inertia
    condition s-sum_{a=1}^{r-2} binomial(n,a).
    """
    out = []
    for j, aa, g, K, U in sectors(P):
        h = sum(a <= P.r-2 for a in aa)
        HC = [[g[i]*v for v in row] for i,row in enumerate(K)]
        HU = [[g[i]*v for v in row] for i,row in enumerate(U)]
        C = None if j == 0 else residual(HC, g, h, P.s)
        cap = residual(HU, g, h, P.N-P.s)
        out.append((j,h,C,cap))
    return P.s-sum(comb(P.n,a) for a in range(1,P.r-1)), out


def slack_entry(P, A, B, *, repaired=True):
    for v in (A, B):
        require(type(v) is int and v >= 0 and v.bit_length() <= P.n and v.bit_count() <= P.r,
                "Vertex is outside the downset")
    eps = P.epsilon if repaired else Q(0)
    if A == B == 0:
        return Q(1)+eps*P.delta
    if A == 0 or B == 0:
        a = (A|B).bit_count()
        row_sum = Q((P.n-1)*(P.n-2)*(P.n-3),2) if a == 1 else \
                  -Q((P.n-2)*(P.n-3),2) if a == 2 else Q(0)
        return Q(1)-eps*row_sum
    if A == B:
        return Q(P.s)
    if A&B:
        return Q(0)
    a, b = A.bit_count(), B.bit_count()
    return P.beta[a][b]+eps*trade(P.n,a,b)


def hoffman_entry(P, A, B):
    return (slack_entry(P,A,B)-P.s*int(A == B))/(P.N-P.s)


def literal_matrix(P, *, max_order=256):
    require(P.N <= max_order, "Use entry/sector formulas for larger orders")
    V = [sum(1 << i for i in A) for a in range(P.r+1) for A in combinations(range(P.n),a)]
    return V, [[slack_entry(P,A,B) for B in V] for A in V]
