"""Outward rational enclosures; no floating point or external dependencies."""
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from math import isqrt


@dataclass(frozen=True)
class I:
    lo: F
    hi: F

    def __post_init__(self):
        object.__setattr__(self, "lo", F(self.lo))
        object.__setattr__(self, "hi", F(self.hi))
        if self.lo > self.hi:
            raise ValueError("reversed interval")

    @staticmethod
    def of(x):
        return x if isinstance(x, I) else I(F(x), F(x))

    def __add__(self, other):
        other = I.of(other)
        return I(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -I.of(other)

    def __mul__(self, other):
        other = I.of(other)
        values = [x * y for x in (self.lo, self.hi)
                  for y in (other.lo, other.hi)]
        return I(min(values), max(values))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = I.of(other)
        if other.lo <= 0 <= other.hi:
            raise ValueError("division through zero")
        return self * I(1 / other.hi, 1 / other.lo)

    def rounded(self, digits):
        scale = 10**digits
        return I(F((self.lo * scale).__floor__(), scale),
                 F((self.hi * scale).__ceil__(), scale))

    def strings(self, digits=24):
        value = self.rounded(digits)
        return [str(value.lo), str(value.hi)]


@lru_cache(maxsize=16384)
def exp_negative(x, digits=70):
    """Enclose exp(x), x<=0, by reduction, Taylor remainder, and squaring.

    All retained terms and all squarings use outward rational rounding.
    The first omitted Taylor term and a geometric tail bound enclose the
    entire omitted series. Precision affects width, never validity.
    """
    x = F(x)
    if x > 0 or type(digits) is not int or not 10 <= digits <= 1000:
        raise ValueError("requires x<=0 and integer precision 10..1000")
    if not x:
        return I.of(1)
    reduced, squares = -x, 0
    while reduced > F(1, 2):
        reduced /= 2
        squares += 1
    guard = digits + 20 + squares
    count = 2 * digits + 16
    term = total = I.of(1)
    for j in range(1, count + 1):
        term = (term * (reduced / j)).rounded(guard)
        total = (total + term).rounded(guard)
    tail = term.hi * reduced / (count + 1) / (1 - reduced / (count + 2))
    result = I(total.lo, total.hi + tail)
    for _ in range(squares):
        result = (result * result).rounded(guard)
    return (I.of(1) / result).rounded(digits)


def sqrt_integer(k, digits=70):
    if type(k) is not int or k < 0:
        raise ValueError("requires a nonnegative integer")
    root = isqrt(k)
    if root * root == k:
        return I.of(root)
    scale = 10**digits
    root = isqrt(k * scale * scale)
    return I(F(root, scale), F(root + 1, scale))
