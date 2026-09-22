#!/usr/bin/env python3
"""Independent defining-recurrence / literal-factorial implementation.

No imports from layers.py, no Gaussian polynomials, and no Schur-Pieri
recurrence. The variable is q with t=1; homogeneity recovers two variables.
"""

from __future__ import annotations

from functools import lru_cache

Poly = tuple[int, ...]


def add(a: Poly, b: Poly) -> Poly:
    return tuple((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b))))


def multiply(a: Poly, b: Poly) -> Poly:
    if not a or not b:
        raise ValueError("empty polynomial")
    result = [0] * (len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            result[i+j] += x*y
    return tuple(result)


def divide_exact(dividend: Poly, divisor: Poly) -> Poly:
    if not dividend or not divisor or divisor[-1] != 1 or len(dividend) < len(divisor):
        raise ValueError("need nonempty polynomials and monic divisor of suitable degree")
    remainder = list(dividend)
    result = [0] * (len(dividend)-len(divisor)+1)
    for degree in range(len(result)-1, -1, -1):
        value = remainder[degree+len(divisor)-1]
        result[degree] = value
        for j, coefficient in enumerate(divisor):
            remainder[degree+j] -= value*coefficient
    if any(remainder):
        raise ArithmeticError("Lucas factorial quotient has a nonzero remainder")
    return tuple(result)


@lru_cache(maxsize=None)
def lucas(index: int) -> Poly:
    if type(index) is not int or index < 0:
        raise ValueError("Lucas index must be a nonnegative integer")
    if index == 0:
        return (0,)
    if index == 1:
        return (1,)
    # F_n(q,1) = (1+q)F_(n-1)(q,1) + q F_(n-2)(q,1).
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
    return tuple(poly[i]-(poly[i-1] if i else 0) for i in range((len(poly)-1)//2+1))


def comparison(b: int, c: int) -> tuple[int, ...]:
    if type(b) is not int or type(c) is not int or not 2 <= b <= c or b*c % 2:
        raise ValueError("require integers 2 <= b <= c and even b*c")
    narrow = choose(b*c//2+2, 2)
    wide = choose(b+c, b)
    if len(narrow) != len(wide):
        raise ArithmeticError("inhomogeneous comparison")
    return to_schur(tuple(a-b for a, b in zip(narrow, wide)))


def reference(b: int, c: int) -> tuple[int, ...]:
    if type(b) is not int or type(c) is not int or not 2 <= b <= c or b*c % 2 or b*c < 6:
        raise ValueError("invalid reference parameters")
    return to_schur((0, 0, 0)+lucas(b*c-5)+(0, 0, 0))
