#!/usr/bin/env python3
"""Exact constant checks and certified finite hinge controls; not the universal proof.

Python >=3.10, standard library only. Reuses the pinned team's rational
interval/exponential primitive. All new log, pi, sqrt and quadrature bounds
are rational. No floating-point values enter any decision or output.
"""
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from math import isqrt
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
BOUND_DIR = HERE.parent / "gaussian_majorisation_hankel_transport"
PIN = "60ff5166c623797055f37442d5532b1a29c06275b8871fa4fdf34dcd12f54fc7"
if sha256((BOUND_DIR / "bounds.py").read_bytes()).hexdigest() != PIN:
    raise RuntimeError("bounds.py dependency hash changed")
sys.path.insert(0, str(BOUND_DIR))
from bounds import I, exp_negative  # noqa: E402

DIGITS = 26
GUARD = 40


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def square_root(x):
    """Monotone enclosure, with integer square root at each rational endpoint."""
    x = I.of(x)
    require(x.lo >= 0, "negative sqrt argument")
    scale = 10**DIGITS

    def lower(q):
        return isqrt(q.numerator * scale * scale // q.denominator)

    lo, hi = lower(x.lo), lower(x.hi)
    if hi * hi * x.hi.denominator != x.hi.numerator * scale * scale:
        hi += 1
    return I(F(lo, scale), F(hi, scale))


def exp_interval(x):
    x = I.of(x)
    require(x.hi <= 0, "positive exponential argument")
    return I(exp_negative(x.lo, DIGITS).lo,
             exp_negative(x.hi, DIGITS).hi)


def twice_atanh(z):
    """Positive series, with outward rounding and a geometric remainder."""
    require(0 <= z <= F(1, 3), "atanh reduction failed")
    zi = I.of(z).rounded(GUARD)
    z2 = (zi * zi).rounded(GUARD)
    power, total = zi, I.of(0)
    count = 60
    for j in range(count):
        total = (total + power / (2 * j + 1)).rounded(GUARD)
        power = (power * z2).rounded(GUARD)
    tail = power.hi / ((2 * count + 1) * (1 - z2.hi))
    return (I(total.lo, total.hi + tail) * 2).rounded(DIGITS)


@lru_cache(maxsize=8192)
def log_rational(x):
    require(x > 0, "nonpositive logarithm argument")
    reduced, power = x, 0
    while reduced < 1:
        reduced *= 2
        power -= 1
    while reduced > 2:
        reduced /= 2
        power += 1
    base = twice_atanh((reduced - 1) / (reduced + 1))
    return (base + power * twice_atanh(F(1, 3))).rounded(DIGITS)


def arctan_small(x):
    """Alternating series, with its first omitted term bounding the error."""
    total = F(0)
    count = 60
    for j in range(count):
        total += (-1)**j * x**(2*j + 1) / (2*j + 1)
    omitted = (-1)**count * x**(2*count + 1) / (2*count + 1)
    return I(min(total, total + omitted), max(total, total + omitted))


PI = (16 * arctan_small(F(1, 5)) -
      4 * arctan_small(F(1, 239))).rounded(DIGITS)
require(F(314159, 100000) < PI.lo < PI.hi < F(314160, 100000),
        "Machin pi check failed")


def transverse_hinge_rational(a, u):
    """a-u-u log(a/u), cut to zero when a<=u."""
    if a <= u:
        return I.of(0)
    value = I.of(a-u) - u * log_rational(a/u)
    return I(max(F(0), value.lo), max(F(0), value.hi))


def transverse_hinge(a, u):
    # The exact expression is increasing in a and decreasing in u.
    lower = transverse_hinge_rational(a.lo, u.hi).lo
    upper = transverse_hinge_rational(a.hi, u.lo).hi
    return I(lower, upper)


def theorem_bound(radius, variance, ell):
    eps = radius * radius / variance
    kappa, beta = 1-eps, 5-1/(1-eps)
    limit = (4-5*eps)**2 / (32*eps*(1-eps))
    require(0 < eps <= F(1, 2), "variance outside theorem")
    require(eps/2 < ell < limit, "level outside strict window")
    q = square_root(2*eps*ell/kappa) * 4
    require(q.hi < beta, "nonpositive bound factor")
    u = exp_negative(-ell, DIGITS)
    deficit = 2 * radius * radius
    return (u * deficit * exp_interval(I.of(-5*eps)-q) * (I.of(beta)-q)
            * (ell-eps/2) * square_root(ell-eps/2)
            / (square_root(PI) * (12*variance))).rounded(DIGITS)


def hinge_control(ell, cells=256):
    """mu=(delta_-e1+delta_e1)/2, T=0, s=10, using exact 1D reduction.

    Integrating the two transverse coordinates gives
    H_g(Cu)-H_f(Cu) = 2/sqrt(2*pi*s) integral_0^Z [J(ag,u)-J(af,u)] dz.
    J(a,u)=(a-u-u log(a/u)) if a>u, else zero. Beyond Z both vanish.

    On [0,Z], each J has a Lipschitz first derivative, whose a.e. second
    derivative has magnitude <= K=(Z+R)^2/s^2+1/s+R^2/s^2. This follows
    from w=log(a/u), |w'|<=(Z+R)/s, |w''|<=1/s+R^2/s^2, and a<=1.
    At a=u the first derivative is zero from both sides. The composite
    midpoint error for the difference is <=2*K*Z^3/(24*cells^2).
    """
    radius, variance, cutoff = F(1), F(10), F(10)
    require((cutoff-radius)**2 >= 2*variance*ell,
            "truncated interval does not cover the support of the hinges")
    width = cutoff/cells
    u = exp_negative(-ell, DIGITS)
    total = I.of(0)
    for j in range(cells):
        z = (j+F(1, 2))*width
        ag = exp_negative(-z*z/(2*variance), DIGITS)
        af = (exp_negative(-(z-radius)**2/(2*variance), DIGITS)
              + exp_negative(-(z+radius)**2/(2*variance), DIGITS))/2
        term = transverse_hinge(ag, u)-transverse_hinge(af, u)
        total = (total+width*term).rounded(DIGITS)
    k_bound = (cutoff+radius)**2/variance**2+1/variance+radius**2/variance**2
    error = 2*k_bound*cutoff**3/(24*cells**2)
    integral = total+I(-error, error)
    gap = (integral*2/square_root(2*variance*PI)).rounded(DIGITS)
    bound = theorem_bound(radius, variance, ell)
    require(gap.lo > bound.hi > 0, "finite hinge/bound comparison inconclusive")
    return {"R": "1", "s": "10", "log_inverse_normalized_threshold": str(ell),
            "cells": cells, "integration_cutoff": str(cutoff),
            "midpoint_error_before_normalization": str(error),
            "certified_actual_hinge_gap": gap.strings(18),
            "certified_theorem_lower_bound": bound.strings(18),
            "strict_margin_over_bound": str((gap-bound).rounded(18).lo)}


def mul(a, b):
    out = [F(0)]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out


def algebra_controls():
    square = mul([4, -5], [4, -5])
    expanded = mul([1, -1], [16, -24])
    expanded[2] += 1
    require(square == expanded, "large-noise exponent identity failed")
    difference = [2*c for c in square]
    difference[0] -= 9
    difference[1] += 9
    require(difference == mul([1, -2], [23, -25]),
            "simpler cutoff factorization failed")
    beta_integral = 2*(F(1)-F(1, 3))
    require(beta_integral == F(4, 3), "coarea Beta integral failed")
    require(F(1, 4)*beta_integral*F(1, 4) == F(1, 12),
            "quantitative hinge coefficient failed")
    require(F(4, 48) == F(1, 12), "spherical normalization failed")
    # Gamma(5/2)/sqrt(pi)=3/4; a centered 6D Gaussian gives C6*A=D*l^2/2.
    require(F(1, 2)*2/F(3, 4) == F(4, 3), "half derivative normalization failed")
    require(F(4, 3)*F(3, 4) == 1, "centered-kernel Laplace factor failed")
    table = []
    for eps in [F(1, 2), F(1, 4), F(1, 10), F(1, 100)]:
        level = (4-5*eps)**2/(32*eps*(1-eps))
        require(level >= F(9, 64)/eps > eps/2, "threshold table failed")
        table.append({"epsilon": str(eps), "L_epsilon": str(level),
                      "simpler_level": str(F(9, 64)/eps)})
    return {"exact_polynomial_identities": 2, "normalization_controls": 5,
            "parameter_table": table}


def elementary_controls():
    require(log_rational(F(1)).lo <= 0 <= log_rational(F(1)).hi,
            "log(1) control failed")
    for x in [F(1, 16), F(1, 2), F(1), F(2), F(16)]:
        require((log_rational(x)+log_rational(1/x)).lo <= 0 <=
                (log_rational(x)+log_rational(1/x)).hi,
                "reciprocal logarithm control failed")
    for x in [F(0), F(1, 4), F(2), F(9), F(9, 16)]:
        root = square_root(x)
        require(root.lo**2 <= x <= root.hi**2, "sqrt enclosure failed")
    for a, u in [(F(1), F(2)), (F(1), F(1)), (F(2), F(1))]:
        value = transverse_hinge_rational(a, u)
        require(value.lo >= 0, "negative transverse hinge")
        if a <= u:
            require(value == I.of(0), "hinge inactive branch failed")
    return {"logarithm_controls": 6, "sqrt_controls": 5,
            "hinge_branch_controls": 3, "pi_enclosure": PI.strings(20)}


def main():
    result = {"claim_status": "finite rational audits of an analytic author proof",
              "arithmetic": "exact Fraction; outward intervals; no floating point",
              "digits": DIGITS, "bounds_sha256": PIN,
              "algebra": algebra_controls(), "elementary": elementary_controls(),
              "hinge_controls": [hinge_control(F(v)) for v in [1, 2, 4]],
              "scope": "These checks do not prove universal majorisation or replace PROOF.md."}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
