"""Exact sparse Q-polynomials; ascending univariate quotient arithmetic."""
from fractions import Fraction as Q
from math import comb


class P:
    def __init__(self, n, terms=0):
        self.n = n
        if not isinstance(terms, dict):
            terms = {(0,) * n: Q(terms)}
        self.d = {e: Q(c) for e, c in terms.items() if c}
        if any(len(e) != n or any(type(k) is not int or k < 0 for k in e)
               for e in self.d):
            raise ValueError("invalid polynomial exponent")

    def coerce(self, other):
        if isinstance(other, P):
            if other.n != self.n:
                raise ValueError("ring mismatch")
            return other
        return P(self.n, other)

    def __add__(self, other):
        other = self.coerce(other)
        d = dict(self.d)
        for e, c in other.d.items():
            d[e] = d.get(e, Q(0)) + c
        return P(self.n, d)

    __radd__ = __add__

    def __neg__(self):
        return P(self.n, {e: -c for e, c in self.d.items()})

    def __sub__(self, other):
        return self + -self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        d = {}
        for e, c in self.d.items():
            for f, b in other.d.items():
                g = tuple(x + y for x, y in zip(e, f))
                d[g] = d.get(g, Q(0)) + c * b
        return P(self.n, d)

    __rmul__ = __mul__

    def __truediv__(self, c):
        c = Q(c)
        if not c:
            raise ZeroDivisionError
        return P(self.n, {e: b / c for e, b in self.d.items()})

    def __pow__(self, k):
        if type(k) is not int or k < 0:
            raise ValueError("invalid power")
        p, r = self, P(self.n, 1)
        while k:
            if k & 1:
                r = r * p
            k >>= 1
            if k:
                p = p * p
        return r

    def diff(self, j):
        d = {}
        for e, c in self.d.items():
            if e[j]:
                f = list(e)
                f[j] -= 1
                d[tuple(f)] = c * e[j]
        return P(self.n, d)

    def sub(self, replacements):
        if len(replacements) != self.n:
            raise ValueError("substitution dimension")
        target = next((r.n for r in replacements if isinstance(r, P)), 0)
        values = [r if isinstance(r, P) else P(target, r)
                  for r in replacements]
        out = P(target, 0)
        for e, c in self.d.items():
            t = P(target, c)
            for r, k in zip(values, e):
                t = t * r**k
            out = out + t
        return out

    def record(self):
        return [[list(e), str(c)] for e, c in sorted(self.d.items())]


def vars(n):
    return tuple(P(n, {tuple(int(j == i) for j in range(n)): Q(1)})
                 for i in range(n))


def zero(p, name):
    if p.d:
        raise ValueError("nonzero identity: " + name)


def add(p, q):
    n = p[0].n
    return [(p[i] if i < len(p) else P(n)) +
            (q[i] if i < len(q) else P(n))
            for i in range(max(len(p), len(q)))]


def mul(p, q):
    r = [P(p[0].n) for _ in range(len(p) + len(q) - 1)]
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i + j] = r[i + j] + a * b
    return r


def rem(p, monic):
    r = list(p)
    d = len(monic) - 1
    zero(monic[-1] - 1, "monic modulus")
    for k in range(len(r) - 1, d - 1, -1):
        for j in range(d):
            r[k - d + j] = r[k - d + j] - r[k] * monic[j]
    return r[:d] + [P(monic[0].n) for _ in range(max(0, d - len(r)))]


def trace(p, monic):
    """Newton sums from coefficients, never a multiplication-matrix trace."""
    d = len(monic) - 1
    sums = [P(monic[0].n, d)]
    for k in range(1, len(p)):
        t = P(monic[0].n)
        for j in range(1, min(k, d) + 1):
            t = t + monic[d - j] * (j if j == k else sums[k - j])
        sums.append(-t)
    return sum((a * b for a, b in zip(p, sums)), P(monic[0].n))


def bernstein(p, degrees):
    """Entire tensor power-to-Bernstein basis and exact inverse controls."""
    if p.n != len(degrees) or any(any(e[j] > degrees[j]
                                     for j in range(p.n)) for e in p.d):
        raise ValueError("Bernstein degree bound")
    from itertools import product
    indices = list(product(*(range(d + 1) for d in degrees)))
    bs = {}
    for k in indices:
        v = Q(0)
        for e, c in p.d.items():
            if all(e[j] <= k[j] for j in range(p.n)):
                f = Q(1)
                for j in range(p.n):
                    f *= Q(comb(k[j], e[j]), comb(degrees[j], e[j]))
                v += c * f
        bs[k] = v
    xx = vars(p.n)
    out = P(p.n)
    for k, c in bs.items():
        t = P(p.n, c)
        for j in range(p.n):
            t *= comb(degrees[j], k[j]) * xx[j]**k[j] * (1 - xx[j])**(degrees[j] - k[j])
        out += t
    zero(out - p, "full Bernstein inverse")
    return bs
