#!/usr/bin/env python3
"""Exact checks supporting PROOF.md; not a formalization or a hinge oracle.

Standard library only. All mathematical checks use Fraction or integers.
Decimal is used solely for outward-rounded human-readable interval endpoints.
"""

from __future__ import annotations

from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F
from math import isqrt
import json


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


# Laurent polynomials in (h,r,p,q,z,g,gp), with rational coefficients.
NV = 7


def term(coefficient=1, **powers):
    names = ("h", "r", "p", "q", "z", "g", "gp")
    exponents = tuple(powers.get(name, 0) for name in names)
    return {exponents: F(coefficient)} if coefficient else {}


def add(*polys):
    result = {}
    for poly in polys:
        for exponent, coefficient in poly.items():
            result[exponent] = result.get(exponent, F(0)) + coefficient
    return {e: c for e, c in result.items() if c}


def mul(first, second):
    result = {}
    for x, a in first.items():
        for y, b in second.items():
            z = tuple(i + j for i, j in zip(x, y))
            result[z] = result.get(z, F(0)) + a * b
    return {e: c for e, c in result.items() if c}


def partial(poly, variable):
    result = {}
    for exponent, coefficient in poly.items():
        degree = exponent[variable]
        if degree:
            next_exponent = list(exponent)
            next_exponent[variable] -= 1
            result[tuple(next_exponent)] = degree * coefficient
    return result


def radial_derivative(poly):
    # h'=hg, r'=1, p'=q, q'=z, g'=gp. No derivative of z or gp is needed.
    require(not partial(poly, 4), "unexpected derivative of V''' required")
    require(not partial(poly, 6), "unexpected derivative of g' required")
    return add(
        mul(partial(poly, 0), term(h=1, g=1)),
        partial(poly, 1),
        mul(partial(poly, 2), term(q=1)),
        mul(partial(poly, 3), term(z=1)),
        mul(partial(poly, 5), term(gp=1)),
    )


def level_derivative(poly):
    return mul(term(p=-1), radial_derivative(poly))


def check_radial_identity():
    raw = term(h=1, r=5, p=-1)
    first = level_derivative(raw)
    second = level_derivative(first)
    claimed_first = add(
        term(h=1, g=1, r=5, p=-2),
        term(5, h=1, r=4, p=-2),
        term(-1, h=1, q=1, r=5, p=-3),
    )
    claimed_second = add(
        term(h=1, g=2, r=5, p=-3),
        term(h=1, gp=1, r=5, p=-3),
        term(10, h=1, g=1, r=4, p=-3),
        term(-3, h=1, g=1, q=1, r=5, p=-4),
        term(20, h=1, r=3, p=-3),
        term(-15, h=1, q=1, r=4, p=-4),
        term(-1, h=1, z=1, r=5, p=-4),
        term(3, h=1, q=2, r=5, p=-5),
    )
    require(first == claimed_first, "first coarea derivative identity")
    require(second == claimed_second, "second coarea derivative identity")
    return {"first_terms": len(first), "second_terms": len(second)}


def check_formal_factorizations():
    # Here r and p stand for a and b, respectively. These are identities
    # of Laurent polynomials, rather than checks at selected values.
    coefficient = add(term(20, r=-3), term(-15, p=1, r=-4),
                      term(3, p=2, r=-5))
    square = mul(add(term(2, r=1), term(-1, p=1)),
                 add(term(2, r=1), term(-1, p=1)))
    require(not add(partial(coefficient, 1), mul(term(15, r=-6), square)),
            "formal derivative factorization")
    corner_difference = add(term(12, r=-3), term(-15, r=-4), term(3, r=-5))
    factored = mul(term(3, r=-5), mul(add(term(4, r=1), term(-1)),
                                    add(term(r=1), term(-1))))
    require(corner_difference == factored, "formal corner factorization")
    return 2


def c0(a, b):
    return 20 / a**3 - 15 * b / a**4 + 3 * b**2 / a**5


def check_rational_bounds():
    count = 0
    for k in [F(1, 2), F(5, 8), F(3, 4), F(7, 8), F(1)]:
        require(
            c0(k, F(1)) - c0(k, k)
            == 3 * (4 * k - 1) * (k - 1) / k**5,
            "corner factorization",
        )
        for i in range(33):
            a = k + (1 - k) * F(i, 32)
            for j in range(33):
                b = k + (1 - k) * F(j, 32)
                derivative = -60 / a**4 + 60 * b / a**5 - 15 * b**2 / a**6
                require(derivative == -15 * (2 * a - b)**2 / a**6,
                        "radial coefficient derivative factorization")
                require(0 <= 5/a**2-b/a**3 <= 4/k**2, "first bound")
                require(0 <= 10/a**3-3*b/a**4 <= 7/k**3, "second bound")
                require(8 <= c0(a, b) <= 8/k**3, "third bound")
                count += 1
    # The universal inequalities are proved in PROOF.md, not by this grid.
    return count


# Exact positive interval arithmetic for one explicit constant enclosure.
def point(x):
    return F(x), F(x)


def plus(a, b):
    return a[0] + b[0], a[1] + b[1]


def times(a, b):
    endpoints = [x*y for x in a for y in b]
    return min(endpoints), max(endpoints)


def reciprocal(a):
    require(a[0] > 0, "positive reciprocal")
    return 1/a[1], 1/a[0]


def sqrt_exact_interval(x, bits):
    require(x >= 0, "nonnegative square root")
    denominator = 1 << bits
    lo = isqrt((x.numerator << (2*bits)) // x.denominator)
    lower = F(lo, denominator)
    if lower*lower == x:
        return lower, lower
    return lower, F(lo+1, denominator)


def sqrt_interval(a, bits):
    return sqrt_exact_interval(a[0], bits)[0], sqrt_exact_interval(a[1], bits)[1]


def exp_exact_interval(x, bits):
    if x < 0:
        return reciprocal(exp_exact_interval(-x, bits))
    total, current, n = F(1), F(1), 0
    tolerance = F(1, 1 << bits)
    while True:
        next_term = current * x / (n+1)
        if x < n+2:
            remainder = next_term / (1-x/F(n+2))
            if remainder <= tolerance:
                return total, total+remainder
        n += 1
        current = next_term
        total += current


def exp_interval(a, bits):
    return exp_exact_interval(a[0], bits)[0], exp_exact_interval(a[1], bits)[1]


def atan_reciprocal_interval(denominator, bits):
    z = F(1, denominator)
    total, n = F(0), 0
    tolerance = F(1, 1 << bits)
    while True:
        total += (-1)**n * z**(2*n+1) / (2*n+1)
        next_term = (-1)**(n+1) * z**(2*n+3) / (2*n+3)
        if abs(next_term) <= tolerance:
            return min(total, total+next_term), max(total, total+next_term)
        n += 1


def pi_interval(bits):
    # Machin's formula. Check its rational tangent identity independently.
    t = F(1, 5)
    t = 2*t/(1-t*t)
    t = 2*t/(1-t*t)
    require((t-F(1,239))/(1+t/F(239)) == 1, "Machin tangent identity")
    a = atan_reciprocal_interval(5, bits+8)
    b = atan_reciprocal_interval(239, bits+8)
    return 16*a[0]-4*b[1], 16*a[1]-4*b[0]


def middle_slope_interval(epsilon, ell, bits):
    require(0 < epsilon <= F(1,2) and ell > 0, "theorem domain")
    kappa = 1-epsilon
    q = times(point(4), sqrt_interval(point(2*epsilon*ell/kappa), bits))
    polynomial = plus(point(8), plus(
        times(point(7+epsilon/(2*kappa)), q),
        times(point(F(5,4)), times(q,q))))
    numerator = times(exp_interval(plus(point(5*epsilon), q), bits), polynomial)
    numerator = times(numerator, sqrt_interval(point(ell), bits))
    denominator = times(point(16*kappa**3), sqrt_interval(pi_interval(bits), bits))
    return times(numerator, reciprocal(denominator))


def outward_decimal(x, upper=False):
    with localcontext() as ctx:
        ctx.prec = 80
        ctx.rounding = ROUND_CEILING if upper else ROUND_FLOOR
        value = Decimal(x.numerator)/Decimal(x.denominator)
        return str(value.quantize(Decimal("0.000000000001")))


def main():
    identities = check_radial_identity()
    factorizations = check_formal_factorizations()
    instances = check_rational_bounds()
    intervals = [middle_slope_interval(F(1,8), F(4), bits) for bits in (80,128)]
    require(max(i[0] for i in intervals) <= min(i[1] for i in intervals),
            "precision enclosures must overlap")
    require(intervals[1][1]-intervals[1][0] < F(1, 10**30),
            "128-bit enclosure width")
    # This threshold is outside the already-signed window for epsilon=1/8.
    cutoff = (4-5*F(1,8))**2/(32*F(1,8)*(1-F(1,8)))
    require(cutoff == F(729,224) and cutoff < 4, "middle threshold control")
    result = {
        "schema": "loss-normalized-hinge-check-v1",
        "formal_coarea_derivatives": identities,
        "formal_coefficient_factorizations": factorizations,
        "exact_rational_bound_instances": instances,
        "constant_epsilon": "1/8",
        "constant_log_threshold": "4",
        "old_signed_log_cutoff": str(cutoff),
        "M_epsilon_L_interval": [outward_decimal(intervals[1][0]),
                                  outward_decimal(intervals[1][1], upper=True)],
        "precisions_bits": [80,128],
        "scope": "algebra and a slope constant; no computed hinge sign",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
