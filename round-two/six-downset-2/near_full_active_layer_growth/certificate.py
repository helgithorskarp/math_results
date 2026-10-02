"""Rational constant-sector duals for centered capped near-cube H.

Actual agent six-downset-2, researcher. The full lift, forced stars and
real affine completion retain the credits in PROOF.md. The new profiles
use two rank-one degree-zero forms. No numerical solver is a proof input.
"""
from fractions import Fraction as Q
from math import comb


def require(test, message):
    if not test:
        raise ValueError(message)


def choose(n, k):
    require(type(n) is int and n >= 0, 'Nonnegative binomial upper index')
    return comb(n, k) if 0 <= k <= n else 0


def parameters(n):
    require(type(n) is int and n >= 6, 'Integer n>=6')
    T = 2**(n-1)
    return n-2, T, T-n, 2*T-n-2


def base(n):
    """Credited complement-s base; explicit n-2 boundary retained."""
    r, T, s, m = parameters(n)
    B = [[Q(0)]*(r+1) for _ in range(r+1)]
    for a in range(3, n//2+1):
        B[a][n-a] = B[n-a][a] = Q(s)
    for a in range(3, n-2):
        b = n-a
        B[1][a] = B[a][1] = Q(2*(n-2), b)
        B[2][a] = B[a][2] = Q(-2*(n-2), b*(b-1))
    B[1][r] = B[r][1] = Q(n-2)
    B[2][r] = B[r][2] = Q(s-(n-2))
    B[1][1] = Q(T*n*n-9*T*n+16*T-n**3+9*n*n-8*n-16, n*(n-1))
    B[1][2] = B[2][1] = Q(2*(-T*n+4*T+2*n*n-4*n-4), n*(n-1))
    B[2][2] = Q(-4*(-T*n+2*T+2*n*n-2*n-2), n*(n-3)*(n-1))
    return B


def check_rows(n, B):
    r, T, s, m = parameters(n)
    require(len(B) == r+1 and all(len(row) == r+1 for row in B), 'Table shape')
    require(all(type(v) is Q for row in B for v in row), 'Rational entries')
    require(all(B[a][b] == B[b][a] for a in range(r+1) for b in range(r+1)), 'Symmetric table')
    for a in range(1, r+1):
        require(sum(B[a][b]*choose(n-a, b) for b in range(1, r+1)) == m-s, 'Center equation')
        require(sum(b*B[a][b]*choose(n-a, b) for b in range(1, r+1)) == (n-a)*s, 'Star moment equation')


def forms(n, B):
    """Physical layer-constant lower/upper forms; no sector completeness."""
    r, T, s, m = parameters(n)
    g = [comb(n, a) for a in range(1, r+1)]
    K = [[g[a-1]*(s*int(a == b)-comb(n, b)+B[a][b]*choose(n-a, b))
          for b in range(1, r+1)] for a in range(1, r+1)]
    U = [[g[a-1]*((T-1)*int(a == b)-B[a][b]*choose(n-a, b))
          for b in range(1, r+1)] for a in range(1, r+1)]
    require(all(A[i][j] == A[j][i] for A in (K, U) for i in range(r) for j in range(r)), 'Physical symmetry')
    return K, U


def bulk(n, a):
    require(type(a) is int and 3 <= a <= n-3, 'Middle layer')
    z, h = 2*a-n, 2*n+5
    V = 16*n**4+h*h*z*z
    return Q(h**3*z**3, 2*n*n*V), -Q(1, 2*n)+Q(2*h*h*z*z, V)


def profiles(n, k):
    r, T, s, m = parameters(n)
    require(type(k) is int and 2 <= k and 2*k < n, 'Active-layer domain 2<=k<n/2')
    c, d = Q(2, n), -Q(2*n+5, n*n)
    p, q = [], []
    for a in range(1, r+1):
        if a <= k:
            pa, qa = Q(1), c+d*a
        elif n-a <= k:
            pa, qa = Q(-1), c+d*(n-a)
        else:
            pa, qa = bulk(n, a)
        p.append(pa); q.append(qa)
    return p, q


def quadratic(A, v):
    return sum(v[i]*A[i][j]*v[j] for i in range(len(v)) for j in range(len(v)))


def low_upper(n):
    r, T, s, m = parameters(n)
    B = base(n)
    Q1, Q2 = -Q(5, n*n), -Q(2*n+10, n*n)
    g2 = Q(n*(n-1), 2)
    return ((n*(T-1)-n*(n-1)*B[1][1])*Q1*Q1
            +(2*g2*(2*n-3)-g2*Q((n-2)*(n-3), 2)*B[2][2])*Q2*Q2
            -2*(n*Q((n-1)*(n-2), 2)*B[1][2]+n*(n-1)*(n-2))*Q1*Q2)


def scalar(n, k):
    """Exact pairing, derived from odd p and even q in PROOF.md."""
    r, T, s, m = parameters(n)
    p, q = profiles(n, k)
    c = Q(2, n)
    return (4*(T-n-1)+low_upper(n)
            +sum(comb(n, a)*((n-1)*q[a-1]**2-2*(n-2)*c*q[a-1])
                 for a in range(3, n-2)))


def tail(n, k):
    require(type(k) is int and 2 <= k and 2*k < n, 'Tail domain')
    return sum(comb(n, a) for a in range(3, k+1))


def moment_upper(n):
    """Upper bound for W_2; the uniform sign is a coefficient proof."""
    r, T, s, m = parameters(n)
    target = Q(2*(n-2), n*(n-1))
    b, v = -Q(1, 2*n)-target, Q((2*n+5)**2, 16*n**4)
    moment = b*b+4*b*v*n+4*(1-b)*v*v*(3*n*n-2*n)
    return (4*(T-n-1)+low_upper(n)
            -(n-1)*target*target*(2*T-n*n-n-2)+2*T*(n-1)*moment)


def certified_range(n, k):
    require(type(n) is int and n >= 64, 'Uniform sign domain n>=64')
    require(type(k) is int and 2 <= k and 2*k < n, 'Active-layer domain')
    T = 2**(n-1)
    return 6*n*n*tail(n, k) <= T
