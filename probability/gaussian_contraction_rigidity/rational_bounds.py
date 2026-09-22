"""Rational enclosures; no floating point, external library, or adaptive precision.

For 0<=x<=1/2, exp(x) is bounded by its degree-32 Taylor sum and
that sum plus t_33/(1-x/34). Positive x is halved first; intervals
are squared back. For negative x, invert the positive enclosure.
Every returned exponential interval is rounded outward to the 2^-160
grid to bound denominator growth. All rounding uses integer division.

For 1<=x<=2, z=(x-1)/(x+1) lies in [0,1/3]. The first 80 terms
of 2*atanh(z) give a lower bound on log(x), with remainder at most
2*z^161/(161*(1-z*z)). Powers of 2 reduce every positive argument
to this interval; log(2) uses the same series.
"""
from fractions import Fraction as F
from functools import lru_cache


def binary_round(lo, hi):
    scale = 2**160
    return (F((lo.numerator * scale) // lo.denominator, scale),
            F(-((-hi.numerator * scale) // hi.denominator), scale))


@lru_cache(None)
def exp_bounds(x):
    x = F(x)
    if x < 0:
        lo, hi = exp_bounds(-x)
        return binary_round(1 / hi, 1 / lo)
    k = 0
    while x > F(1, 2):
        x /= 2
        k += 1
    term = total = F(1)
    for j in range(1, 33):
        term *= x / j
        total += term
    tail = term * x / 33 / (1 - x / 34)
    lo, hi = total, total + tail
    for _ in range(k):
        lo, hi = lo * lo, hi * hi
    return binary_round(lo, hi)


def _log_unit(x):
    z = (x - 1) / (x + 1)
    if not 0 <= z <= F(1, 3):
        raise ValueError("log series argument outside [1,2]")
    power, total = z, F(0)
    for j in range(80):
        total += 2 * power / (2 * j + 1)
        power *= z * z
    return total, total + 2 * power / (161 * (1 - z * z))


@lru_cache(None)
def log_bounds(x):
    x = F(x)
    if x <= 0:
        raise ValueError("log requires a positive argument")
    k = 0
    while x > 2:
        x /= 2
        k += 1
    while x < 1:
        x *= 2
        k -= 1
    lo, hi = _log_unit(x)
    a, b = _log_unit(F(2))
    return (lo + k * a, hi + k * b) if k >= 0 else (lo + k * b, hi + k * a)


def outward_grid(interval, digits=12):
    """Return integer endpoints divided by 10**digits; exact outward rounding."""
    scale = 10 ** digits
    lo, hi = interval
    left = (lo.numerator * scale) // lo.denominator
    right = -((-hi.numerator * scale) // hi.denominator)
    return [str(F(left, scale)), str(F(right, scale))]
