"""Exact ascending-coefficient polynomials over Z or Q. () represents zero."""
from fractions import Fraction as Q
from functools import reduce
from math import comb, gcd, lcm

ZERO, ONE, T, S = (), (1,), (0, 1), (1, 1)

def need(condition, message):
    if not condition:
        raise ValueError(message)

def trim(p):
    p = list(p)
    while p and not p[-1]:
        p.pop()
    return tuple(p)

def add(a, b):
    return trim((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
                for i in range(max(len(a), len(b))))

def scale(p, a):
    return trim(a*x for x in p)

def sub(a, b):
    return add(a, scale(b, -1))

def mul(a, b):
    if not a or not b:
        return ZERO
    result = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i+j] += x*y
    return trim(result)

def power(p, k):
    need(type(k) is int and k >= 0, 'nonnegative polynomial exponent')
    return reduce(mul, [p]*k, ONE)

def integer_divrem(a, b):
    need(bool(b), 'nonzero polynomial divisor')
    r = list(a); q = [0] * max(0, len(a)-len(b)+1)
    while r and len(r) >= len(b):
        if r[-1] % b[-1]:
            return None, trim(r)
        v = r[-1] // b[-1]; k = len(r)-len(b)
        q[k] = v
        for j, x in enumerate(b):
            r[k+j] -= v*x
        r = list(trim(r))
    return trim(q), trim(r)

def integer_polynomial(p):
    p = tuple(Q(x) for x in p)
    denominator = lcm(*(x.denominator for x in p)) if p else 1
    return tuple(int(x*denominator) for x in p), denominator

def positive_content(p):
    p, denominator = integer_polynomial(p)
    if not p:
        return p
    g = reduce(gcd, p, 0)
    return tuple(x//g for x in p)

def value(p, x):
    out = Q(0)
    for c in reversed(p):
        out = out*x+c
    return out

def bernstein(p, lo, hi):
    """Exact coefficients in the degree-n Bernstein basis on [lo,hi]."""
    n = len(p)-1
    c = [sum(Q(p[j])*comb(j,k)*lo**(j-k)*(hi-lo)**k
             for j in range(k,n+1)) for k in range(n+1)]
    return [sum(c[k]*Q(comb(i,k),comb(n,k)) for k in range(i+1))
            for i in range(n+1)]

def closed_sign(p, lo, hi):
    """A conservative strict sign on a CLOSED interval; None means unproved."""
    if not p:
        return 0
    b = bernstein(positive_content(p),lo,hi)
    if b[0] > 0 and b[-1] > 0 and all(x >= 0 for x in b):
        return 1
    if b[0] < 0 and b[-1] < 0 and all(x <= 0 for x in b):
        return -1
    return None

def dot(x, y):
    return reduce(add,(mul(a,b) for a,b in zip(x,y)),ZERO)

def cross(x, y):
    return [sub(mul(x[1],y[2]),mul(x[2],y[1])),
            sub(mul(x[2],y[0]),mul(x[0],y[2])),
            sub(mul(x[0],y[1]),mul(x[1],y[0]))]

def metric(x, y):
    """x^T H(t) y, H diagonal1 and off-diagonalt."""
    diagonal = dot(x,y)
    all_pairs = mul(reduce(add,x,ZERO),reduce(add,y,ZERO))
    return add(diagonal,mul(T,sub(all_pairs,diagonal)))

def determinant(rows):
    return dot(rows[0],cross(rows[1],rows[2]))

def normal(x):
    return [add(x[j],mul(T,reduce(add,(x[k] for k in range(3) if k != j),ZERO)))
            for j in range(3)]

def decode(x):
    need(type(x) is list and len(x)==2 and all(type(v) is int for v in x) and x[1]>0,
         'rational pair with positive denominator')
    return Q(*x)

def encode(x):
    x = Q(x)
    return [x.numerator,x.denominator]
