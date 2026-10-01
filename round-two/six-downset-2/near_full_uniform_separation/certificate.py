"""Rational rank-one duals for a real affine support face, not H matrices.

The centered lift, star equations and degree0/1 forms retain the credits
in PROOF.md. Author six-downset-2, researcher. Standard library only.
"""
from fractions import Fraction as Q
from math import comb
from poly import require


def choose(n, k):
    require(type(n) is int and n >= 0, 'Nonnegative binomial upper index')
    return comb(n, k) if 0 <= k <= n else 0


def parameters(n):
    require(type(n) is int and n >= 6, 'Integer n>=6')
    T = 2**(n-1)
    return n-2, T, T-n, 2*T-n-2


def beta(n, deficits=None):
    """Complete the restricted face independently of the RREF in verify.py."""
    r, T, s, m = parameters(n)
    deficits = {} if deficits is None else dict(deficits)
    allowed = [(a, n-a) for a in range(3, n//2+1)]
    require(all(p in allowed and type(v) is Q for p, v in deficits.items()), 'Exact complement deficits')
    out = [[Q(0)]*(r+1) for _ in range(r+1)]
    for a, b in allowed:
        out[a][b] = out[b][a] = s-deficits.get((a, b), Q(0))
    for a in range(3, r+1):
        h = n-a
        S0 = sum(out[a][b]*choose(h, b) for b in range(3, r+1))
        S1 = sum(out[a][b]*choose(h-1, b-1) for b in range(3, r+1))
        out[2][a] = out[a][2] = Q(h*(s-S1)-(m-s-S0), comb(h, 2))
        out[1][a] = out[a][1] = s-S1-(h-1)*out[a][2]
    h = n-2
    S0 = sum(out[2][b]*choose(h, b) for b in range(3, r+1))
    S1 = sum(out[2][b]*choose(h-1, b-1) for b in range(3, r+1))
    out[2][2] = Q(h*(s-S1)-(m-s-S0), comb(h, 2))
    out[1][2] = out[2][1] = s-S1-(h-1)*out[2][2]
    out[1][1] = s-(n-2)*out[1][2]-sum(out[1][b]*choose(n-2, b-1) for b in range(3, r+1))
    for a in range(1, r+1):
        require(sum(out[a][b]*choose(n-a, b) for b in range(1, r+1)) == m-s, 'Center equation')
        require(sum(out[a][b]*choose(n-a-1, b-1) for b in range(1, r+1)) == s, 'Star equation')
    return out


def upper(n, table):
    r, T, s, m = parameters(n)
    out = []
    for j in (0, 1):
        g = [comb(n, a) if j == 0 else comb(n-2, a-1) for a in range(1, r+1)]
        A = [[g[a-1]*(Q((T-1)*int(a == b))+(-1)**(j+1)*table[a][b]*choose(n-a-j, b-j))
              for b in range(1, r+1)] for a in range(1, r+1)]
        require(all(A[i][k] == A[k][i] for i in range(r) for k in range(r)), 'Physical form symmetry')
        out.append(A)
    return out


def quadratic(A, v):
    return sum(v[i]*A[i][j]*v[j] for i in range(len(v)) for j in range(len(v)))


def witness(n):
    r, T, s, m = parameters(n)
    eta, k = Q(2)+Q(6, n*n), Q(2)+Q(3, n)
    p0, p1 = [Q(0)]*r, [Q(0)]*r
    p0[0], p0[1], p0[-1] = eta-k, 2*eta-k, 2*eta-k
    p1[1], p1[-1] = Q(1), Q(-1)
    for a in range(3, n-2):
        d, x = 2*a-n, (2*a-n)**2
        V = n*n*(3*n-4)**2+8*(3*n-2)*x
        Z = 43*n**4+32*n*n*x-48*n*n+48*x
        Y = 24*n**5-107*n**4+136*n**3+32*n*n*x-48*n*n+48*x
        require(V > 0, 'Positive witness denominator')
        p0[a-1] = -Q(x*Z, n**3*V)
        p1[a-1] = Q(2*d*Y, n**3*V)
    return p0, p1


def scalar(n):
    """Literal closed scalar; finite evaluation is not the uniform proof."""
    r, T, s, m = parameters(n)
    eta, k = Q(2)+Q(6, n*n), Q(2)+Q(3, n)
    K0 = n*(-T*n+2*T+5*n*n-9*n+3)
    K1 = 2*(n-2)*(2*T*n-4*T+2*n**3-9*n*n+7*n+4)
    low = eta*eta*K0+K1-2*k*n*(2*n-1)*eta+k*k*n*n
    A, B = n*n*(3*n-4)**2, 8*(3*n-2)
    a1 = n*n*(32*n**5+16*n**4+97*n**3-571*n*n-264*n+720)
    a2 = 8*(2*n*n+3)*(4*n**3-13*n*n+11*n-30)
    total = low
    for a in range(3, n-2):
        x = (2*a-n)**2
        F = (n-2)*k*k-Q(x*(a1+a2*x), n**4*(A+B*x))
        total += comb(n, a)*F
    return total
