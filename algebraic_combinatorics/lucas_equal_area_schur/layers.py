#!/usr/bin/env python3
"""Gaussian q-Pascal / Schur-Pieri implementation, exact integers only.

Generalizes the preserved lucas_a2_complete_schur implementation. No use
of the literal Lucas-factorial implementation in direct.py.
"""
from __future__ import annotations

from fractions import Fraction
from functools import lru_cache


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ArithmeticError(message)


def parameters(a: int, b: int, c: int) -> tuple[int, int, int]:
    if any(type(v) is not int for v in (a, b, c)) or not 1 <= a < b <= c:
        raise ValueError("require integers 1 <= a < b <= c")
    n = b*c
    if n % a:
        raise ValueError("a must divide b*c")
    return n, n//a, a+1


@lru_cache(maxsize=None)
def gaussian(n: int, k: int) -> tuple[int, ...]:
    """Coefficients of [n choose k]_z in ascending order."""
    if type(n) is not int or type(k) is not int or not 0 <= k <= n:
        raise ValueError("require integers 0 <= k <= n")
    if k in (0, n):
        return (1,)
    result = [0]*(k*(n-k)+1)
    for i, value in enumerate(gaussian(n-1, k)):
        result[i] += value
    for i, value in enumerate(gaussian(n-1, k-1)):
        result[i+n-k] += value
    require(result == result[::-1], "Gaussian symmetry failure")
    return tuple(result)


@lru_cache(maxsize=None)
def lucas_schur(degree: int) -> tuple[int, ...]:
    """Coefficient r is [s_(degree-r,r)] F_(degree+1), via Pieri."""
    if type(degree) is not int or degree < 0:
        raise ValueError("degree must be a nonnegative integer")
    if degree == 0:
        return (1,)
    prev = lucas_schur(degree-1)
    before = lucas_schur(degree-2) if degree >= 2 else ()
    result = []
    for r in range(degree//2+1):
        value = prev[r] if r < len(prev) else 0
        if r >= 1:
            value += prev[r-1]
            value += before[r-1] if r-1 < len(before) else 0
        result.append(value)
    return tuple(result)


def gaussian_layers(a: int, b: int, c: int) -> tuple[int, ...]:
    n, d, _ = parameters(a, b, c)
    wide, thin = gaussian(b+c, b), gaussian(a+d, a)
    return tuple(wide[i]-thin[i]-(wide[i-1]-thin[i-1] if i else 0)
                 for i in range(n//2+1))


def transport(n: int, first: int, u: tuple[int, ...]) -> tuple[int, ...]:
    if (type(n) is not int or n < 0 or type(first) is not int or first < 0
            or len(u) > n//2+1 or any(type(v) is not int for v in u)):
        raise ValueError("invalid layer data")
    result = [0]*(n//2+1)
    for i, coefficient in enumerate(u):
        sign = 1 if (first+i) % 2 == 0 else -1
        for j, value in enumerate(lucas_schur(n-2*i)):
            result[i+j] += sign*coefficient*value
    return tuple(result)


def comparison(a: int, b: int, c: int) -> tuple[int, ...]:
    n, _, first = parameters(a, b, c)
    return transport(n, first, gaussian_layers(a, b, c))


def reference(a: int, b: int, c: int) -> tuple[int, ...]:
    n, _, first = parameters(a, b, c)
    return (0,)*first+lucas_schur(n-2*first)


def partitions_through(limit: int, smallest: int = 1,
                       largest: int | None = None) -> tuple[int, ...]:
    if type(limit) is not int or limit < 0 or type(smallest) is not int or smallest < 1:
        raise ValueError("invalid partition parameters")
    if largest is None:
        largest = limit
    if type(largest) is not int or largest < 0:
        raise ValueError("invalid largest part")
    result = [1]+[0]*limit
    for part in range(smallest, min(largest, limit)+1):
        for total in range(part, limit+1):
            result[total] += result[total-part]
    return tuple(result)


def boundary_parameters() -> tuple[tuple[int, int, int, int], ...]:
    """Complete finite complement of g=c-a>=3; see PROOF.md (18)."""
    result = []
    for a in range(1, 5):
        for g in (1, 2):
            for delta in range(1, g+1):
                if delta*g % a == 0:
                    b, c = a+delta, a+g
                    result.append((a, b, c, b*c//a))
    return tuple(result)


def tail_budget() -> dict[str, str]:
    """Rational inequalities in the written Euler-product argument."""
    x = Fraction(1, 3)
    product = Fraction(1)
    for j in range(1, 4):
        product /= 1-x**j
    require(x**4/(1-x) == Fraction(1, 54), "geometric tail mismatch")
    product /= 1-Fraction(1, 54)
    simple = Fraction(43, 24)
    coefficient = 1+x**3+x**4+(x**8+x**10)/(1-x*x)
    upper = coefficient*simple-Fraction(14, 9)
    margin = Fraction(2, 3)-Fraction(3, 2)*upper
    require(product == Fraction(19683, 11024) and product < simple,
            "partition product bound failure")
    require(coefficient == Fraction(27545, 26244), "envelope coefficient mismatch")
    require(upper == Fraction(204659, 629856) and upper < Fraction(1, 3),
            "tail bound failure")
    require(margin == Fraction(75277, 419904) and margin > Fraction(1, 6),
            "margin failure")
    return {"partition_product_upper": str(product), "simpler_upper": str(simple),
            "envelope_multiplier": str(coefficient), "tail_upper": str(upper),
            "gap_at_least_three_margin": str(margin), "uniform_margin": "1/6"}
