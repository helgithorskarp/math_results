#!/usr/bin/env python3
"""Exact Gaussian-layer / Schur-Pieri implementation. Standard library only."""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ArithmeticError(message)


def parameters(b: int, c: int) -> int:
    if type(b) is not int or type(c) is not int or not 2 <= b <= c or b*c % 2:
        raise ValueError("require integers 2 <= b <= c and even b*c")
    return b*c


@lru_cache(maxsize=None)
def gaussian(n: int, k: int) -> tuple[int, ...]:
    """[n choose k]_z, coefficients in ascending powers, via q-Pascal."""
    if type(n) is not int or type(k) is not int or not 0 <= k <= n:
        raise ValueError("require integers 0 <= k <= n")
    if k in (0, n):
        return (1,)
    result = [0] * (k*(n-k) + 1)
    for i, value in enumerate(gaussian(n-1, k)):
        result[i] += value
    for i, value in enumerate(gaussian(n-1, k-1)):
        result[i+n-k] += value
    require(result == result[::-1], "Gaussian symmetry failure")
    return tuple(result)


@lru_cache(maxsize=None)
def lucas_schur(degree: int) -> tuple[int, ...]:
    """Coefficient r is [s_(degree-r,r)] F_(degree+1)."""
    if type(degree) is not int or degree < 0:
        raise ValueError("degree must be a nonnegative integer")
    if degree == 0:
        return (1,)
    prev = lucas_schur(degree-1)
    before = lucas_schur(degree-2) if degree >= 2 else ()
    result = []
    for r in range(degree//2+1):
        # e1 adds one cell to a valid row; e2 adds one cell to both rows.
        value = prev[r] if r < len(prev) else 0
        if r >= 1:
            value += prev[r-1]
            value += before[r-1] if r-1 < len(before) else 0
        result.append(value)
    return tuple(result)


def comparison(b: int, c: int) -> tuple[int, ...]:
    n = parameters(b, c)
    rectangle = gaussian(b+c, b)
    thin = gaussian(n//2+2, 2)
    u = []
    for i in range(n//2+1):
        hi = rectangle[i] - thin[i]
        before = rectangle[i-1] - thin[i-1] if i else 0
        u.append(hi-before)
    result = [0] * (n//2+1)
    for i, coefficient in enumerate(u):
        coefficient *= 1 if i % 2 else -1
        for j, value in enumerate(lucas_schur(n-2*i)):
            result[i+j] += coefficient*value
    return tuple(result)


def reference(b: int, c: int) -> tuple[int, ...]:
    """Schur coefficients of G = e2^3 F_(bc-5)."""
    n = parameters(b, c)
    if n < 6:
        raise ValueError("reference requires b*c >= 6")
    return (0, 0, 0) + lucas_schur(n-6)


def partitions_through(limit: int, smallest: int = 1,
                       largest: int | None = None) -> tuple[int, ...]:
    if type(limit) is not int or limit < 0 or type(smallest) is not int or smallest < 1:
        raise ValueError("invalid partition parameters")
    if largest is None:
        largest = limit
    if type(largest) is not int or largest < 0:
        raise ValueError("invalid largest part")
    result = [1] + [0]*limit
    for part in range(smallest, min(largest, limit)+1):
        for total in range(part, limit+1):
            result[total] += result[total-part]
    return tuple(result)


def tail_budget() -> dict[str, str]:
    """Exact arithmetic for the written infinite-product bound, not a truncation claim."""
    p = partitions_through(11)
    require(p == (1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42, 56),
            "partition prefix mismatch")
    product = Fraction(1)
    for j in range(1, 7):
        product /= 1-Fraction(1, 2**j)
    # For j>=7, product(1-2^-j) >= 1-sum(2^-j) = 63/64.
    product /= 1-Fraction(1, 64)
    require(product == Fraction(134217728, 38757285), "Euler upper bound mismatch")
    require(product < Fraction(52, 15), "Euler upper bound insufficient")
    prefix = sum((Fraction(value, 2**i) for i, value in enumerate(p)), Fraction(0))
    require(prefix == Fraction(1745, 512), "weighted prefix mismatch")
    loss = 8*(Fraction(52, 15)-prefix)
    margin = Fraction(1, 2)-loss
    require(loss == Fraction(449, 960) and margin == Fraction(31, 960),
            "tail budget mismatch")
    return {"euler_product_upper": str(product), "simpler_upper": "52/15",
            "prefix_through_11": str(prefix), "tail_loss_upper": str(loss),
            "schur_margin": str(margin)}
