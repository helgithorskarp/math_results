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

