"""Dense exact kernel from six-tammes-1 source3f1da6e (9878); stdlib Fraction."""
from fractions import Fraction as F
from math import comb


def clean(p):
    p = [F(x) for x in p]
    while p and not p[-1]:
        p.pop()
    return p


def add(p, q):
    return clean([(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0)
                  for i in range(max(len(p), len(q)))])


def neg(p):
    return [-x for x in p]


def mul(p, q):
    if not p or not q:
        return []
    ans = [F(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            ans[i + j] += x * y
    return clean(ans)


def divide(p, q):
    p, q = clean(p), clean(q)
    if not q:
        raise ValueError('zero divisor')
    quotient = [F(0)] * max(0, len(p) - len(q) + 1)
    while p and len(p) >= len(q):
        power, scale = len(p) - len(q), p[-1] / q[-1]
        quotient[power] += scale
        p = add(p, neg([F(0)] * power + [scale * x for x in q]))
    return clean(quotient), p


def bezout(p, q):
    """Return monic H and witnesses U,V with U*p+V*q=H; forbid (0,0)."""
    p, q = clean(p), clean(q)
    if not p and not q:
        raise ValueError('both contact gaps zero')
    old_r, r = p, q
    old_u, u = [F(1)], []
    old_v, v = [], [F(1)]
    while r:
        quot, rem = divide(old_r, r)
        old_r, r = r, rem
        old_u, u = u, add(old_u, neg(mul(quot, u)))
        old_v, v = v, add(old_v, neg(mul(quot, v)))
    scale = old_r[-1]
    h, u, v = ([x / scale for x in z] for z in (old_r, old_u, old_v))
    if add(mul(u, p), mul(v, q)) != h:
        raise ValueError('producer Bezout identity')
    return h, u, v


def bernstein(p, lo, hi):
    """Affine power expansion followed by conversion to Bernstein degree deg(p)."""
    p = clean(p)
    if not p:
        return [F(0)]
    power = [F(0)] * len(p)
    for j, x in enumerate(p):
        for k in range(j + 1):
            power[k] += x * comb(j, k) * lo ** (j - k) * (hi - lo) ** k
    degree = len(p) - 1
    return [sum(power[k] * F(comb(i, k), comb(degree, k)) for k in range(i + 1))
            for i in range(degree + 1)]
