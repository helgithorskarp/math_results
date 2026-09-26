"""Exact rational enclosures. No floating point, external library, or asserts."""
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from math import isqrt


@dataclass(frozen=True)
class Interval:
    lo: F
    hi: F

    def __post_init__(self):
        object.__setattr__(self, "lo", F(self.lo))
        object.__setattr__(self, "hi", F(self.hi))
        if self.lo > self.hi:
            raise ValueError("reversed interval")

    @staticmethod
    def of(x):
        return x if isinstance(x, Interval) else Interval(F(x), F(x))

    def __add__(self, other):
        other = self.of(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -self.of(other)

    def __mul__(self, other):
        other = self.of(other)
        p = [a * b for a in (self.lo, self.hi) for b in (other.lo, other.hi)]
        return Interval(min(p), max(p))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.of(other)
        if other.lo <= 0 <= other.hi:
            raise ValueError("division interval contains zero")
        return self * Interval(1 / other.hi, 1 / other.lo)

    def rounded(self, digits=40):
        scale = 10**digits
        return Interval(F((self.lo * scale).__floor__(), scale),
                        F((self.hi * scale).__ceil__(), scale))


@lru_cache(maxsize=None)
def exp_bounds(x):
    """128 terms; tail bounded by a geometric series after the first omitted term."""
    x = F(x)
    if x == 0:
        return Interval(1, 1)
    if x < 0:
        return (Interval.of(1) / exp_bounds(-x)).rounded()
    terms = 128
    if x >= terms + 2:
        raise ValueError("argument exceeds fixed Taylor enclosure domain")
    term = total = F(1)
    for j in range(1, terms + 1):
        term *= x / j
        total += term
    first_omitted = term * x / (terms + 1)
    tail = first_omitted / (1 - x / (terms + 2))
    return Interval(total, total + tail).rounded()


def log_point(x):
    """160 atanh terms, with a symmetric explicit geometric tail enclosure."""
    x = F(x)
    if x <= 0:
        raise ValueError("logarithm requires a positive argument")
    t = (x - 1) / (x + 1)
    if abs(t) > F(3, 4):
        raise ValueError("argument outside fixed logarithm enclosure domain")
    power = Interval.of(t).rounded()
    total = Interval.of(0)
    terms = 160
    for j in range(terms):
        total = (total + power / (2 * j + 1)).rounded()
        power = (power * (t * t)).rounded()
    # The fixed bound |t|<=3/4 controls the entire omitted series. Rounding
    # errors in retained terms have already been enclosed by Interval.
    tail = 2 * F(3, 4)**(2 * terms + 1) / ((2 * terms + 1) * (1 - F(3, 4)**2))
    if t == 0:
        return Interval.of(0)
    return Interval(2 * total.lo - tail, 2 * total.hi + tail).rounded()


def log_bounds(x):
    x = Interval.of(x).rounded()
    return Interval(log_point(x.lo).lo, log_point(x.hi).hi)


def sqrt_bounds(x):
    """Integer square root gives rigorous rational endpoints at denominator 10^40."""
    x = F(x)
    if x < 0:
        raise ValueError("negative square root")
    a, b = isqrt(x.numerator), isqrt(x.denominator)
    if a * a == x.numerator and b * b == x.denominator:
        return Interval.of(F(a, b))
    scale = 10**40
    k = isqrt(x.numerator * scale * scale // x.denominator)
    return Interval(F(k, scale), F(k + 1, scale))


def compact(x):
    """Outward rational rounding for short printed certificates only."""
    x = Interval.of(x)
    scale = 10**18
    low = (x.lo * scale).__floor__()
    high = (x.hi * scale).__ceil__()
    return [str(F(low, scale)), str(F(high, scale))]
