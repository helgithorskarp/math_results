"""Exact original-pair and empty-row coefficients, without centering.

six-downset-2, researcher. The inherited circle profiles and scalar
certificate are from committed 9201; certificate.py is a credited copy.
No solver output or floating arithmetic is a proof input.
"""
from fractions import Fraction as Q
from math import comb
from certificate import choose, parameters, profiles, require, scalar, tail


def residuals(n, k):
    p, q = profiles(n, k)
    c, d = Q(2, n), -Q(2*n+5, n*n)
    return [v-1 for v in p], [v-c-d*a for a, v in enumerate(q, 1)]


def weight(n, k, a, b):
    """Coefficient before the unordered original-entry multiplier 2*h."""
    r, _, _, _ = parameters(n)
    require(type(a) is int and type(b) is int and 1 <= a <= r and 1 <= b <= r and a+b <= n, 'Supported nonempty sizes')
    f, g = residuals(n, k)
    return f[a-1]*f[b-1]-g[a-1]*g[b-1]


def positive_weight(n, a, b):
    """Closed coefficient when both sizes are in the bulk."""
    require(3 <= a and 3 <= b and a+b <= n, 'Middle supported sizes')
    h = 2*n+5
    t, u = Q(h*(2*a-n), 4*n*n), Q(h*(2*b-n), 4*n*n)
    F = lambda x: 2*x*x+x+1
    return Q(h*(n-a-b), n*n)*F(t)*F(u)/((1+t*t)*(1+u*u))


def row_profile(n, k):
    p, q = profiles(n, k)
    return [2*x-Q(4, n)*(y+Q(1, 2*n)) for x, y in zip(p, q)]


def norm_squared(n, k):
    return sum(comb(n, a)*v*v for a, v in enumerate(row_profile(n, k), 1))


def small_tail(n, k):
    require(type(n) is int and n >= 64 and type(k) is int and 2 <= k and 2*k < n, 'Small-tail domain')
    return 12*n**3*sum(comb(n, a) for a in range(k+1)) <= 2**(n-1)


def broad_tail(n, k):
    require(type(n) is int and n >= 64, 'Factor-two cutoff domain n>=64')
    return 2*n*n*tail(n, k) <= 2**(n-1)


def invariant_defect(n, B):
    r, T, s, m = parameters(n)
    v = [s-m+sum(B[a][b]*choose(n-a, b) for b in range(1, r+1)) for a in range(1, r+1)]
    sigma = sum(comb(n, a)*v[a-1] for a in range(1, r+1))
    return v, sigma


def signed_pair_sum(n, k, B):
    """Sum 2*h*omega*M over unordered ORIGINAL disjoint pairs.

    B=h*M on each invariant disjoint orbit. An equal-size orbit has
    half as many unordered pairs; hence the factor (2-delta_ab).
    """
    r, _, _, _ = parameters(n)
    out = Q(0)
    for a in range(k+1, r+1):
        for b in range(a, r+1):
            if a+b < n:
                out += (2-int(a == b))*comb(n, a)*choose(n-a, b)*weight(n, k, a, b)*B[a][b]
    return out


def predicted_pairing(n, k, B):
    v, sigma = invariant_defect(n, B)
    r = row_profile(n, k)
    return scalar(n, k)+signed_pair_sum(n, k, B)-Q(n*n-6, n*n)*sigma+sum(comb(n, a)*r[a-1]*v[a-1] for a in range(1, n-1))
