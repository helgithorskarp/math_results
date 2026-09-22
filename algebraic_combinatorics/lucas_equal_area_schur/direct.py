#!/usr/bin/env python3
"""Independent literal Lucas recurrence and factorial division at t=1.

No Gaussian, layer transport or Schur-Pieri imports. Adapted from the
preserved lucas_a2_complete_schur/direct.py to arbitrary canonical a.
"""
from __future__ import annotations

from functools import lru_cache

Poly = tuple[int, ...]


def add(a: Poly, b: Poly) -> Poly:
    return tuple((a[i] if i < len(a) else 0)+(b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b))))


def multiply(a: Poly, b: Poly) -> Poly:
    if not a or not b:
        raise ValueError("empty polynomial")
    result = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i+j] += x*y
    return tuple(result)


def divide_exact(dividend: Poly, divisor: Poly) -> Poly:
    if not dividend or not divisor or divisor[-1] != 1 or len(dividend) < len(divisor):
        raise ValueError("need nonempty polynomials and a monic divisor of suitable degree")
    remainder = list(dividend)
    result = [0]*(len(dividend)-len(divisor)+1)
    for degree in range(len(result)-1, -1, -1):
        value = remainder[degree+len(divisor)-1]
        result[degree] = value
        for j, coefficient in enumerate(divisor):
            remainder[degree+j] -= value*coefficient
    if any(remainder):
        raise ArithmeticError("nonzero remainder in literal factorial quotient")
    return tuple(result)


@lru_cache(maxsize=None)
def lucas(index: int) -> Poly:
    if type(index) is not int or index < 0:
        raise ValueError("Lucas index must be a nonnegative integer")
    if index == 0:
        return (0,)
    if index == 1:
        return (1,)
    if index == 2:
        return (1, 1)
    return add(multiply((1, 1), lucas(index-1)), (0,)+lucas(index-2))


@lru_cache(maxsize=None)
def choose(n: int, k: int) -> Poly:
    if type(n) is not int or type(k) is not int or not 0 <= k <= n:
        raise ValueError("require integers 0 <= k <= n")
    k = min(k, n-k)
    numerator = denominator = (1,)
    for j in range(1, k+1):
        numerator = multiply(numerator, lucas(n-k+j))
        denominator = multiply(denominator, lucas(j))
    quotient = divide_exact(numerator, denominator)
    if len(quotient) != k*(n-k)+1 or quotient != quotient[::-1]:
        raise ArithmeticError("Lucas quotient degree or symmetry mismatch")
    return quotient


def to_schur(poly: Poly) -> tuple[int, ...]:
    if not poly or poly != poly[::-1]:
        raise ValueError("homogeneous specialization must be palindromic")
    return tuple(poly[i]-(poly[i-1] if i else 0)
                 for i in range((len(poly)-1)//2+1))


def validate(a: int, b: int, c: int) -> tuple[int, int]:
    if any(type(v) is not int for v in (a, b, c)) or not 1 <= a < b <= c:
        raise ValueError("require integers 1 <= a < b <= c")
    if b*c % a:
        raise ValueError("unequal area")
    return b*c, b*c//a


def comparison(a: int, b: int, c: int) -> tuple[int, ...]:
    _, d = validate(a, b, c)
    wide, thin = choose(b+c, b), choose(a+d, a)
    if len(wide) != len(thin):
        raise ArithmeticError("inhomogeneous comparison")
    sign = 1 if a % 2 else -1
    return to_schur(tuple(sign*(x-y) for x, y in zip(wide, thin)))


def reference(a: int, b: int, c: int) -> tuple[int, ...]:
    n, _ = validate(a, b, c)
    return to_schur((0,)*(a+1)+lucas(n-2*a-1)+(0,)*(a+1))
