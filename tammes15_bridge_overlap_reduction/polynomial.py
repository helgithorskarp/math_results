"""Exact integer polynomial helpers; ascending coefficients, () is zero."""

from fractions import Fraction

from functools import reduce

from math import comb, gcd
from functools import lru_cache

Z=()
ONE=(1,)
T=(0,1)
F=(-1,-3,2,6,-1,13)
ROOT_LO=Fraction("0.59260590292507377809642492233275")
ROOT_HI=Fraction("0.59260590292507377809642492233276")

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


@lru_cache(None)
def root_count(p,lo=Fraction(1,2),hi=Fraction(3,5)):
    """Number of distinct real roots in the open interval, by exact Sturm."""
    from field import divrem as qdivrem, scale as qscale
    p=tuple(map(Fraction,trim(p)))
    need(p and lo<hi,'Sturm polynomial/domain')
    for endpoint in (lo,hi):
        while len(p)>1 and value(p,endpoint)==0:
            p,r=qdivrem(p,(-endpoint,Fraction(1)))
            need(not r,'endpoint factor division')
    if len(p)==1:return 0
    q=tuple(i*p[i] for i in range(1,len(p)))
    sequence=[p,q]
    while sequence[-1]:
        _,r=qdivrem(sequence[-2],sequence[-1])
        if not r:break
        r=qscale(r,-1/abs(r[-1]))
        sequence.append(r)
    def variations(endpoint):
        signs=[1 if x>0 else -1 for s in sequence if (x:=value(s,endpoint))]
        return sum(x!=y for x,y in zip(signs,signs[1:]))
    return variations(lo)-variations(hi)
