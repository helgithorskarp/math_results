"""Canonical rational functions over Q(t); geometric divisions are audited in the proof."""
from functools import reduce
from math import gcd
from polynomial import Z,ONE,trim,need,pgcd,exactdiv,add,scale,mul,power

class Rat:
    """A reduced rational function over Q(t); numerical divisions are audited."""
    __slots__ = ('n', 'd')

    def __init__(self, n=Z, d=ONE):
        n, d = trim(n), trim(d)
        need(bool(d), 'zero rational-function denominator')
        if not n:
            self.n, self.d = Z, ONE
            return
        content = reduce(gcd, n+d)
        if d[-1] < 0:
            content = -content
        n, d = tuple(c//content for c in n), tuple(c//content for c in d)
        common = pgcd(n, d)
        self.n, self.d = exactdiv(n, common), exactdiv(d, common)

    @staticmethod
    def convert(x):
        return x if isinstance(x, Rat) else Rat((x,))

    def __add__(self, other):
        other = self.convert(other)
        common = pgcd(self.d, other.d)
        p, q = exactdiv(self.d, common), exactdiv(other.d, common)
        return Rat(add(mul(self.n, q), mul(other.n, p)), mul(p, other.d))

    __radd__ = __add__

    def __neg__(self):
        return Rat(scale(self.n, -1), self.d)

    def __sub__(self, other):
        return self + (-self.convert(other))

    def __rsub__(self, other):
        return self.convert(other) - self

    def __mul__(self, other):
        other = self.convert(other)
        g1, g2 = pgcd(self.n, other.d), pgcd(other.n, self.d)
        return Rat(mul(exactdiv(self.n, g1), exactdiv(other.n, g2)),
                   mul(exactdiv(self.d, g2), exactdiv(other.d, g1)))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.convert(other)
        need(bool(other.n), "identically-zero rational-function divisor")
        return self * Rat(other.d, other.n)

    def __rtruediv__(self, other):
        return self.convert(other) / self

    def __pow__(self, exponent):
        need(type(exponent) is int and exponent >= 0, 'nonnegative integer power required')
        return Rat(power(self.n, exponent), power(self.d, exponent))

    def __eq__(self, other):
        other = self.convert(other)
        return self.n == other.n and self.d == other.d
