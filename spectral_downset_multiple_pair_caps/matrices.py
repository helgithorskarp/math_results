"""Closed rational capped-H candidates with multiple pair/r middle orbits.

Constructing a matrix does not presume positivity. Actual author
six-downset-3, role researcher. Python3.10+ standard library only.
"""
from fractions import Fraction as F
from math import comb, lcm
import re


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rational(x):
    if type(x) in (int, F):
        return F(x)
    require(type(x) is str and re.fullmatch(r'-?\d+(?:/[1-9]\d*)?', x),
            'Exact integer/Fraction/rational string required')
    return F(x)


def mapping(raw):
    require(type(raw) is dict, 'Coefficient mapping required')
    out = {}
    for key, value in raw.items():
        require(type(key) is int or type(key) is str and key.isdigit(),
                'Integer coefficient key required')
        k = int(key)
        require(k not in out, 'Duplicate coefficient key')
        out[k] = rational(value)
    return out


def parameters(n, z, epsilon, delta):
    require(type(n) is int and n >= 7, 'Integer n>=7 required')
    z, delta = mapping(z), mapping(delta)
    require(set(z) == set(range(2, n//2+1)), 'Independent reflected layers required')
    require(all(3 <= r and 2*r < n for r in delta),
            'Selected sizes must satisfy3<=r<n/2; central/mirror aliases excluded')
    return ({k: z[min(k, n-k)] for k in range(2, n-1)}, rational(epsilon), delta)


def construct(n, z, epsilon, delta):
    """Canonical vertices and complete L=(N-s)M+sI, without any PSD verdict."""
    z, epsilon, delta = parameters(n, z, epsilon, delta)
    N, s = 2**n-n-1, 2**(n-1)-n
    full = (1 << n)-1
    members = [a for a in range(1 << n) if a.bit_count() <= n-2]
    singleton_middle = {
        k: z[k]-(n-3)*epsilon*int(k == 2)
        -sum((comb(n-3, r-1) if k == 2 else n-r-1 if k == r else 0)*d
             for r, d in delta.items()) for k in z}
    singleton_pair = (s-sum(comb(n-2, k-1)*z[k] for k in z)
                      +(n-2)*(n-3)*epsilon
                      +sum(2*(n-2)*comb(n-3, r-1)*d for r, d in delta.items()))
    empty_middle = {
        k: N-2*s-(n-k-1)*z[k]+comb(n-2, 2)*epsilon*int(k == 2)
        +sum(((r-1)*comb(n-2, r) if k == 2 else comb(n-r, 2) if k == r else 0)*d
             for r, d in delta.items()) for k in z}
    # These two entries complete the singleton and empty row equations.
    empty_singleton = N-s-(n-1)*singleton_pair-sum(comb(n-1, k)*singleton_middle[k] for k in z)
    empty_diagonal = N-n*empty_singleton-sum(comb(n, k)*empty_middle[k] for k in z)
    diagonal = F(s)
    zero = F(0)
    L = []
    for a in members:
        ka = a.bit_count(); row = []
        for b in members:
            kb = b.bit_count()
            if a == b:
                value = empty_diagonal if a == 0 else diagonal
            elif not a or not b:
                k = max(ka, kb)
                value = empty_singleton if k == 1 else empty_middle[k]
            elif a & b:
                value = zero
            elif ka == kb == 1:
                value = singleton_pair
            elif min(ka, kb) == 1:
                value = singleton_middle[max(ka, kb)]
            elif a | b == full:
                value = s-z[ka]
            elif ka == kb == 2:
                value = epsilon
            elif min(ka, kb) == 2 and max(ka, kb) in delta:
                value = delta[max(ka, kb)]
            else:
                value = zero
            row.append(value)
        L.append(row)
    return members, L


def scaled_integer_matrix(a):
    denominator = lcm(*(rational(x).denominator for row in a for x in row))
    result = [[int(rational(x)*denominator) for x in row] for row in a]
    require(all(F(result[i][j], denominator) == a[i][j]
                for i in range(len(a)) for j in range(len(a[i]))), 'Integer scaling residual')
    return result, denominator
