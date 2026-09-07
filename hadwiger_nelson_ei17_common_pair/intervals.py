"""Outward intervals [lo,hi]/2**100; integer arithmetic only."""
from fractions import Fraction
from math import isqrt

Q = 1 << 100


def ceildiv(a, b):
    if b <= 0:
        raise ValueError('positive divisor required')
    return -((-a) // b)


class I:
    __slots__ = ('lo', 'hi')

    def __init__(self, lo, hi):
        if not isinstance(lo, int) or not isinstance(hi, int) or lo > hi:
            raise ValueError('invalid endpoints')
        self.lo, self.hi = lo, hi

    @classmethod
    def rational(cls, x):
        x = Fraction(x)
        return cls(x.numerator * Q // x.denominator,
                   ceildiv(x.numerator * Q, x.denominator))

    def __add__(self, other):
        return I(self.lo + other.lo, self.hi + other.hi)

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        p = [a * b for a in (self.lo, self.hi) for b in (other.lo, other.hi)]
        return I(min(p) // Q, ceildiv(max(p), Q))

    def square(self):
        low = 0 if self.lo <= 0 <= self.hi else min(self.lo**2, self.hi**2)
        high = max(self.lo**2, self.hi**2)
        return I(low // Q, ceildiv(high, Q))

    def reciprocal(self):
        if self.lo <= 0 <= self.hi:
            raise ValueError('division by interval containing zero')
        if self.hi < 0:
            return -((-self).reciprocal())
        return I(Q * Q // self.hi, ceildiv(Q * Q, self.lo))

    def __truediv__(self, other):
        return self * other.reciprocal()

    def sqrt(self):
        if self.lo < 0:
            raise ValueError('negative square root interval')
        a, b = isqrt(self.lo * Q), isqrt(self.hi * Q)
        return I(a, b if b * b == self.hi * Q else b + 1)

    def contains(self, integer):
        return self.lo <= integer * Q <= self.hi


ZERO = I.rational(0)
ONE = I.rational(1)


def subtract(a, b):
    return a[0] - b[0], a[1] - b[1]


def norm(a):
    return a[0].square() + a[1].square()


def squared_distance(a, b):
    return norm(subtract(a, b))
