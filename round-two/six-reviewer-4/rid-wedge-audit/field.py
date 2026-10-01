"""Exact integer-pair and Q(sqrt5) arithmetic by six-reviewer-4.

Integer-pair implementation reused from this reviewer's published independent
projection audit (commit 413f944878dc972740803f0f8b5d9d098e4440dc).
No researcher implementation or module is imported.
"""
from fractions import Fraction
from functools import total_ordering
from itertools import product
from math import gcd

def need(ok, message):
    if not ok:
        raise ValueError(message)


def plus(x, y):
    return (x[0] + y[0], x[1] + y[1])


def minus(x, y):
    return (x[0] - y[0], x[1] - y[1])


def times(x, y):
    return (x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def sign(x):
    a, b = x
    if not a:
        return (b > 0) - (b < 0)
    if not b or (a > 0) == (b > 0):
        return (a > 0) - (a < 0)
    norm = a * a - 5 * b * b
    need(norm != 0, "irrationality of sqrt5")
    return ((norm > 0) - (norm < 0)) * ((a > 0) - (a < 0))


@total_ordering
class S:
    """(a+b*sqrt5)/d with common integer denominator, never float arithmetic."""
    __slots__ = ("a", "b", "d")

    def __init__(self, a=0, b=0, d=1):
        if isinstance(a, S):
            self.a, self.b, self.d = a.a, a.b, a.d
            return
        need(isinstance(a, int) and isinstance(b, int) and isinstance(d, int), "integer surd data")
        need(d != 0, "nonzero denominator")
        if d < 0:
            a, b, d = -a, -b, -d
        g = gcd(gcd(abs(a), abs(b)), d)
        self.a, self.b, self.d = a // g, b // g, d // g

    def __add__(self, other):
        o = S(other)
        return S(self.a * o.d + o.a * self.d, self.b * o.d + o.b * self.d, self.d * o.d)
    __radd__ = __add__

    def __neg__(self):
        return S(-self.a, -self.b, self.d)

    def __sub__(self, other):
        return self + -S(other)

    def __rsub__(self, other):
        return S(other) + -self

    def __mul__(self, other):
        o = S(other)
        a, b = times((self.a, self.b), (o.a, o.b))
        return S(a, b, self.d * o.d)
    __rmul__ = __mul__

    def __truediv__(self, other):
        o = S(other)
        a, b = times((self.a, self.b), (o.a, -o.b))
        return S(a * o.d, b * o.d, self.d * (o.a * o.a - 5 * o.b * o.b))

    def __rtruediv__(self, other):
        return S(other) / self

    def __pow__(self, exponent):
        need(isinstance(exponent, int) and exponent >= 0, "nonnegative integer power")
        out = S(1)
        for _ in range(exponent):
            out *= self
        return out

    def __eq__(self, other):
        o = S(other)
        return (self.a, self.b, self.d) == (o.a, o.b, o.d)

    def __lt__(self, other):
        o = S(other)
        return sign((self.a * o.d - o.a * self.d, self.b * o.d - o.b * self.d)) < 0

    def __hash__(self):
        return hash((self.a, self.b, self.d))

    def __repr__(self):
        return f"({Fraction(self.a, self.d)})+({Fraction(self.b, self.d)})sqrt5"


def vsub(x, y):
    return tuple(minus(a, b) for a, b in zip(x, y))


def vscale(k, x):
    return tuple((k * a, k * b) for a, b in x)


def dot(x, y):
    out = (0, 0)
    for a, b in zip(x, y):
        out = plus(out, times(a, b))
    return out


def cross(x, y):
    return (minus(times(x[1], y[2]), times(x[2], y[1])),
            minus(times(x[2], y[0]), times(x[0], y[2])),
            minus(times(x[0], y[1]), times(x[1], y[0])))


def zero(x):
    return all(t == (0, 0) for t in x)


def axis(x):
    if zero(x):
        return None
    pivot = next(t for t in x if t != (0, 0))
    conjugate = (pivot[0], -pivot[1])
    y = tuple(times(t, conjugate) for t in x)
    g = 0
    for t in y:
        for c in t:
            g = gcd(g, abs(c))
    orient = next(t[0] for t in y if t != (0, 0))
    return tuple(((a if orient > 0 else -a) // g,
                  (b if orient > 0 else -b) // g) for a, b in y)


def as_fields(x, denominator=1):
    return tuple(S(a, b, denominator) for a, b in x)


def fdot(x, y):
    return sum((a * b for a, b in zip(x, y)), S())


def fcross(x, y):
    return (x[1] * y[2] - x[2] * y[1], x[2] * y[0] - x[0] * y[2], x[0] * y[1] - x[1] * y[0])
