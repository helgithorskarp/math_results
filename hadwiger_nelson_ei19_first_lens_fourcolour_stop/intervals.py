"""Outward rational-grid intervals for the exact EI19 lens checker."""

from fractions import Fraction
from math import isqrt

Q = 1 << 160

def ceildiv(a, b):
    if b <= 0:
        raise ValueError("positive divisor required")
    return -((-a) // b)

class I:
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi):
        if type(lo) is not int or type(hi) is not int or lo > hi:
            raise ValueError("invalid interval")
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
        p = [a*b for a in (self.lo, self.hi) for b in (other.lo, other.hi)]
        return I(min(p)//Q, ceildiv(max(p), Q))

    def square(self):
        low = 0 if self.lo <= 0 <= self.hi else min(self.lo**2, self.hi**2)
        high = max(self.lo**2, self.hi**2)
        return I(low//Q, ceildiv(high, Q))

    def reciprocal(self):
        if self.lo <= 0 <= self.hi:
            raise ValueError("division by interval containing zero")
        if self.hi < 0:
            return -((-self).reciprocal())
        return I(Q*Q//self.hi, ceildiv(Q*Q, self.lo))

    def __truediv__(self, other):
        return self * other.reciprocal()

    def sqrt(self):
        if self.lo < 0:
            raise ValueError("negative square root")
        lo = isqrt(self.lo*Q)
        hi = isqrt(self.hi*Q)
        return I(lo, hi if hi*hi == self.hi*Q else hi+1)

    def contains(self, integer):
        return self.lo <= integer*Q <= self.hi

ONE = I.rational(1)

def norm(vector):
    return sum((x.square() for x in vector), I.rational(0))

def subtract(a, b):
    return tuple(x-y for x, y in zip(a, b))

def squared_distance(a, b):
    return norm(subtract(a, b))
