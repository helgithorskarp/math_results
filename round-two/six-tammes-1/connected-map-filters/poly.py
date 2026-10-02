"""Dense exact polynomials and rational functions used only by the producer."""
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


def gcd(p, q):
    while q:
        p, q = q, divide(p, q)[1]
    return [x / p[-1] for x in p] if p else [F(1)]


class Rat:
    def __init__(self, n, d=(1,)):
        n, d = clean(n), clean(d)
        if not d:
            raise ValueError('zero denominator')
        g = gcd(n, d)
        n, rn = divide(n, g)
        d, rd = divide(d, g)
        if rn or rd:
            raise ValueError('inexact reduction')
        scale = d[0] if d[0] else d[-1]
        self.n, self.d = [x / scale for x in n], [x / scale for x in d]

    def __add__(self, other):
        return Rat(add(mul(self.n, other.d), mul(other.n, self.d)), mul(self.d, other.d))

    def __neg__(self):
        return Rat(neg(self.n), self.d)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        return Rat(mul(self.n, other.n), mul(self.d, other.d))

    def __truediv__(self, other):
        return Rat(mul(self.n, other.d), mul(self.d, other.n))

    def encode(self):
        return {'numerator': [str(x) for x in self.n],
                'denominator': [str(x) for x in self.d]}


def bernstein(p, lo, hi):
    """Affine substitution, followed by the power-to-Bernstein transform."""
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
