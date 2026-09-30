"""Exact integer polynomials, ascending coefficients, () zero.
Adapted from six-tammes-2, tammes15_bridge_overlap_reduction/polynomial.py,
verified source 34d5a62d025ea9ade24e17c9ba848d297469063f.
Only integer polynomial operations and the Bernstein transform are used.
"""

from fractions import Fraction

from functools import reduce

from math import comb, gcd

Z=()
ONE=(1,)
T=(0,1)

def need(condition, message):
    if not condition:
        raise ValueError(message)

def trim(p):
    p = list(p)
    while p and not p[-1]:
        p.pop()
    return tuple(p)

def add(a, b):
    return trim([(a[i] if i < len(a) else 0) +
                 (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])

def scale(p, a):
    return trim([a * x for x in p])

def sub(a, b):
    return add(a, scale(b, -1))

def mul(a, b):
    if not a or not b:
        return Z
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return trim(c)

def power(p, k):
    v = ONE
    for _ in range(k):
        v = mul(v, p)
    return v

def divrem(a, b):
    """Integer polynomial division when all quotient coefficients are integral."""
    need(bool(b), 'division by zero')
    r = list(a)
    q = [0] * max(0, len(a) - len(b) + 1)
    while r and len(r) >= len(b):
        if r[-1] % b[-1]:
            return None, trim(r)
        v = r[-1] // b[-1]
        k = len(r) - len(b)
        q[k] = v
        for j, x in enumerate(b):
            r[k + j] -= v * x
        r = list(trim(r))
    return trim(q), trim(r)

def exactdiv(a, b):
    q, r = divrem(a, b)
    need(q is not None and not r, 'nonexact polynomial division')
    return q

def primitive(p):
    if not p:
        return p
    g = reduce(gcd, p, 0)
    if p[-1] < 0:
        g = -g
    return tuple(x // g for x in p)

def prem(a, b):
    """Primitive pseudoremainder: preserves the Q[t] gcd up to a unit."""
    while a and len(a) >= len(b):
        shift = (0,) * (len(a) - len(b)) + scale(b, a[-1])
        a = primitive(sub(scale(a, b[-1]), shift))
    return a

def pgcd(a, b):
    a, b = primitive(a), primitive(b)
    while b:
        a, b = b, prem(a, b)
    return primitive(a)

def value(p, x):
    a = Fraction(0)
    for y in reversed(p):
        a = a * x + y
    return a

def bernstein(p, lo=Fraction(1, 2), hi=Fraction(3, 5)):
    """Coefficients in the degree-n Bernstein basis on [lo,hi]."""
    n = len(p) - 1
    a = [sum(Fraction(p[j]) * comb(j, k) * lo ** (j - k) *
             (hi - lo) ** k for j in range(k, n + 1)) for k in range(n + 1)]
    return [sum(a[k] * Fraction(comb(i, k), comb(n, k))
                for k in range(i + 1)) for i in range(n + 1)]
