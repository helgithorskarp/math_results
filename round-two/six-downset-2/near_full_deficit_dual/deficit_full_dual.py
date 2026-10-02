"""Private exact odd-sensitive complementary-deficit dual certificates.

The written ordinary proof supplies all-order coverage. Rational profiles
are checkable dual witnesses; neither these nor relaxed maximizers are H.
Only supplied rational multipliers are checked here; no floating-point arithmetic is used.
"""
from fractions import Fraction as Q
from math import comb, ceil
from deficit_functional import parameters, phi, optimizer, sqrt_bracket, require


def derivative(n, a, z):
    N = 2**n-n-1
    r = n-1
    x = Q(a)-Q(n, 2)
    require(type(z) is Q and 0 <= z < N, 'Exact derivative domain')
    return Q(n*n*r*r, 4)/(r+z)**2-Q(N*N)*x*x/(N-z)**2


def root_bracket(n, a, lam, denominator=2**44):
    """Bracket the unique derivative root, or return the inactive z=0."""
    N = 2**n-n-1
    s = 2**(n-1)-n
    r = n-1
    Z = 2*s-2
    require(type(lam) is Q and lam > Q(n*n*r*r, 4*(r+Z)**2),
            'Multiplier above the uniform endpoint threshold')
    require(type(denominator) is int and denominator > 0, 'Root precision')
    if lam >= a*(n-a):
        return Q(0), Q(0)
    x = Q(a)-Q(n, 2)
    sqlo, sqhi = sqrt_bracket(lam+x*x, 2**60)
    require(sqlo > 0, 'Nonzero exact square-root lower bound')
    # The complement-even stationary point bounds the full stationary
    # point from above, since N^2/(N-z)^2 >= 1.
    top = min(Q(Z), Q(r)*(Q(n, 2)/sqlo-1))
    hi = ceil(top*denominator)
    hi = min(Z*denominator, hi)
    require(hi > 0 and derivative(n, a, Q(hi, denominator)) <= lam,
            'Exact upper root bracket')
    lo = 0
    while hi-lo > 1:
        mid = (lo+hi)//2
        if derivative(n, a, Q(mid, denominator)) > lam:
            lo = mid
        else:
            hi = mid
    low, high = Q(lo, denominator), Q(hi, denominator)
    require(derivative(n, a, low) > lam >= derivative(n, a, high),
            'Complete derivative bracket')
    return low, high


def dual_profile(n, k, lam, denominator=2**44):
    N, s, h, r, c = parameters(n, k)
    records = []
    for a in range(k+1, n-k):
        low, high = root_bracket(n, a, lam, denominator)
        v, t = optimizer(n, a, high)
        f = Q(a)-v-t
        fc = Q(n-a)-v+t
        w = f*fc
        cost = r*v*v+N*t*t
        require(0 <= low <= high <= 2*s-2 and w <= lam,
                'Exact odd-sensitive dual feasibility')
        records.append({'a': a, 'lo': low, 'hi': high, 'v': v, 't': t,
                        'f': f, 'fc': fc, 'w': w, 'cost': cost})
    require(all(q['f'] > 0 and q['fc'] > 0 for q in records),
            'Positive original proper-support coefficients')
    require(all(q['f'] < p['f'] for q, p in zip(records, records[1:])),
            'Strictly increasing rational cardinality profile')
    by_a = {q['a']: q for q in records}
    require(all(q['hi'] == by_a[n-q['a']]['hi'] and
                q['v'] == by_a[n-q['a']]['v'] and
                q['t'] == -by_a[n-q['a']]['t'] and
                q['fc'] == by_a[n-q['a']]['f'] for q in records),
            'Exact complementary even and odd conventions')
    bound = c+lam*(4*s-4)+sum(comb(n, q['a'])*q['cost'] for q in records)
    lo_mass = sum(comb(n, q['a'])*q['lo'] for q in records)
    hi_mass = sum(comb(n, q['a'])*q['hi'] for q in records)
    rho = [(a, b, 1-by_a[a]['f']*by_a[b]['f']/lam)
           for a in by_a for b in by_a if a <= b and a+b < n]
    require(all(0 < value < 1 for a, b, value in rho),
            'Every original proper-pair weight is strictly positive')
    maxrho = max((value for a, b, value in rho), default=Q(0))
    mass_floor = -bound/(2*h*lam*maxrho) if bound < 0 and maxrho else None
    return {'n': n, 'k': k, 'lam': lam, 'constant': c, 'bound': bound,
            'lo_mass': lo_mass, 'hi_mass': hi_mass, 'budget': Q(4*s-4),
            'profiles': records, 'rho': rho, 'maxrho': maxrho,
            'positive_original_mass_floor': mass_floor}


def scalar_square(n, a, z, lam, v, t):
    N = 2**n-n-1
    r = n-1
    x = Q(a)-Q(n, 2)
    v0, t0 = optimizer(n, a, z)
    w = (Q(a)-v-t)*(Q(n-a)-v+t)
    left = r*v*v+N*t*t+lam*z-phi(n, a, z)
    right = (r+z)*(v-v0)**2+(N-z)*(t-t0)**2+z*(lam-w)
    require(left == right, 'Original odd-sensitive square identity')
    return left, right
