"""Exact rational affine sections of a cube--crosspolytope Minkowski sum."""

from fractions import Fraction as F
from functools import lru_cache
from math import comb, factorial


def monomial_integral(power, lower, upper):
    if upper <= lower:
        return F(0)
    return (F(upper) ** (power + 1) - F(lower) ** (power + 1)) / (power + 1)


def two_sided(a, b, inactive, shifted_sum, radius):
    """One inclusion-exclusion term with both tail signs present."""
    top = min(F(radius), F(shifted_sum))
    if top <= -radius:
        return F(0)
    answer = F(0)
    for i in range(a):
        for j in range(b):
            radial_power = a + b - 2 - i - j
            v_base = i + j
            coefficient = comb(a - 1, i) * comb(b - 1, j) * (-1) ** j
            for k in range(inactive):
                term = (F(coefficient * comb(inactive - 1, k) * (-1) ** k)
                        * F(shifted_sum) ** (inactive - 1 - k))
                v_power = v_base + k
                for lower, upper, sign in (
                    (-F(radius), min(top, F(0)), -1),
                    (F(0), top, 1),
                ):
                    answer += term / (radial_power + 1) * (
                        F(radius) ** (radial_power + 1)
                        * monomial_integral(v_power, lower, upper)
                        - sign ** (radial_power + 1)
                        * monomial_integral(
                            v_power + radial_power + 1, lower, upper
                        )
                    )
    return answer / (
        2 ** (a + b - 1)
        * factorial(a - 1)
        * factorial(b - 1)
        * factorial(inactive - 1)
    )


@lru_cache(None)
def stratum(a, b, inactive, radius, total):
    """Delta-normalized section for fixed positive/negative tail labels."""
    radius, total = F(radius), F(total)
    if min(a, b, inactive) < 0 or a + b + inactive < 2 or radius < 0:
        raise ValueError("invalid stratum")

    if a == b == 0:
        target = total + inactive
        return sum(
            (F((-1) ** j * comb(inactive, j), factorial(inactive - 1))
             * max(target - 2 * j, 0) ** (inactive - 1))
            for j in range(inactive + 1)
        )

    if inactive == 0:
        if not b:
            excess = total - a
            if excess <= 0 or excess > radius:
                return F(0)
            return excess ** (a - 1) / factorial(a - 1)
        if not a:
            excess = -total - b
            if excess <= 0 or excess > radius:
                return F(0)
            return excess ** (b - 1) / factorial(b - 1)
        shifted_sum = total - a + b
        if abs(shifted_sum) >= radius:
            return F(0)
        answer = F(0)
        for i in range(a):
            for j in range(b):
                answer += (
                    comb(a - 1, i)
                    * comb(b - 1, j)
                    * (-1) ** j
                    * shifted_sum ** (i + j)
                    * monomial_integral(
                        a + b - 2 - i - j, abs(shifted_sum), radius
                    )
                )
        return answer / (
            2 ** (a + b - 1) * factorial(a - 1) * factorial(b - 1)
        )

    if a == 0:
        return stratum(b, 0, inactive, radius, -total)

    answer = F(0)
    for j in range(inactive + 1):
        shifted_sum = total + inactive - a + b - 2 * j
        if b:
            part = two_sided(a, b, inactive, shifted_sum, radius)
        else:
            cap = min(radius, shifted_sum)
            if cap <= 0:
                part = F(0)
            else:
                part = sum(
                    (
                        F(comb(inactive - 1, k) * (-1) ** k)
                        * shifted_sum ** (inactive - 1 - k)
                        * monomial_integral(a - 1 + k, 0, cap)
                    )
                    for k in range(inactive)
                ) / (factorial(a - 1) * factorial(inactive - 1))
        answer += (-1) ** j * comb(inactive, j) * part
    if answer < 0:
        raise ArithmeticError("negative stratum volume")
    return answer


def section(size, radius, total):
    """Delta-normalized volume with sum x_i=total and excess budget radius."""
    if type(size) is not int or size < 2:
        raise ValueError("size must be an integer at least two")
    radius, total = F(radius), F(total)
    if radius < 0:
        raise ValueError("negative radius")
    return sum(
        (
            F(factorial(size), factorial(a) * factorial(b) * factorial(size - a - b))
            * stratum(a, b, size - a - b, radius, total)
        )
        for a in range(size + 1)
        for b in range(size + 1 - a)
    )


def normalized_constant(n, rho, theta):
    """n! A_(n+1)(theta(n+1),rho(n+1))/(n+1)^n."""
    if type(n) is not int or n < 1:
        raise ValueError("n must be a positive integer")
    size = n + 1
    return (section(size, F(rho) * size, F(theta) * size)
            * F(factorial(n), size ** n))
