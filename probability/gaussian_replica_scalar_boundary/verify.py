#!/usr/bin/env python3
"""Exact finite audits and negative-index producer for PROOF.md.

The parameter-uniform analytic theorem is the manuscript, not a finite scan.
Only integers and fractions are used; assertions remain enabled under -O.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from math import comb, factorial
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def text(x: F | int) -> str:
    return str(x)


def ceil(x: F) -> int:
    return -(-x.numerator // x.denominator)


def poly_add(p: dict, q: dict) -> dict:
    result = p.copy()
    for key, value in q.items():
        result[key] = result.get(key, 0) + value
    return {key: value for key, value in result.items() if value}


def poly_scale(p: dict, scale: F | int) -> dict:
    return {key: value * scale for key, value in p.items() if value * scale}


def poly_mul(p: dict, q: dict) -> dict:
    result = {}
    for a, x in p.items():
        for b, y in q.items():
            key = tuple(i + j for i, j in zip(a, b))
            result[key] = result.get(key, 0) + x * y
    return {key: value for key, value in result.items() if value}


def dx(p: dict) -> dict:
    return {(a - 1, b): a * v for (a, b), v in p.items() if a}


def exp_derivative(p: dict) -> dict:
    """d/dx [exp(-x w) p(x,w)], with the exponential suppressed."""
    return poly_add(dx(p), {(a, b + 1): -v for (a, b), v in p.items()})


def factorial_bound(p: dict, rate: int, b_power: int) -> F:
    """Bound a nonnegative polynomial times exp(-rate*b*x).

    Each monomial coefficient*x^a*b^k has k-a=-b_power. The bound is
    b^(-b_power) sum coefficient*a!/rate^a.
    """
    require(all(v >= 0 and k - a == -b_power for (a, k), v in p.items()),
            "factorial bound has incorrect homogeneity or sign")
    return sum((F(v * factorial(a), rate**a) for (a, _), v in p.items()), F(0))


def exponential_bracket(x: F, tolerance: F) -> tuple[F, F, int]:
    """Taylor's theorem: S_(2n+1)<=exp(-x)<=S_(2n), x>=0."""
    require(0 <= x <= 2 and tolerance > 0, "invalid exponential input")
    partial = F(1)
    term = F(1)
    upper = partial
    n = 0
    while True:
        n += 1
        term *= -x / n
        partial += term
        if n % 2:
            lower = partial
            require(upper >= lower, "Taylor parity error")
            if upper - lower <= tolerance:
                return lower, upper, n
        else:
            upper = partial


def make_parameters(order: int, b: F, wedge: F | None = None) -> dict:
    require(order >= 12 and 0 < b <= F(1, 2), "invalid K or b")
    eps1 = b**4 / 20000
    eps2 = b**(order + 5) / (
        2**(order + 2) * (order + 1)**(order + 5) * factorial(order + 5)
    )
    eps = min(eps1, eps2)
    rho = eps**2 / 20000
    require(0 < eps <= b / 20000 and eps <= F(1, 20000), "bump scale")
    strip_budget = eps * 2**order * (order + 1)**(order + 5) * (
        factorial(order + 5) / b**(order + 5)
    )
    require(strip_budget <= F(1, 4), "finite-strip budget")
    require(1 - 312 * eps / b**4 > 0, "monotonicity margin")
    require(1 - 7944 * eps / b**4 - 48000 * eps**2 / b**8 > F(1, 2),
            "log-convexity margin")
    require(rho * (F(3, 2) + 24 * eps / b**4) < 1, "replica cap")
    x = 2 * b + F(5, 2) * eps
    lo, hi, degree = exponential_bracket(x, eps / 100)
    # Round onto a compact rational grid. The raw Taylor midpoint can have
    # thousands of denominator digits; retaining it is unnecessary.
    grid = ceil(400 / eps)
    midpoint_on_grid = (lo + hi) * grid / 2
    r = F(midpoint_on_grid.numerator // midpoint_on_grid.denominator, grid)
    require(0 < lo <= hi < 1 and 0 < r < 1
            and max(abs(r - lo), abs(r - hi)) <= eps / 100,
            "r does not enclose the desired center")
    n0 = ceil(F(32000000000) / eps**4)
    n = n0
    if wedge is not None:
        require(wedge > 0 and b <= min(F(1, 8), wedge / 32), "wedge parameters")
        n = max(n, ceil(16 / wedge))
    j = (n * r).numerator // (n * r).denominator
    q = n - j
    require(0 < j < n, "invalid beta index")
    mean = F(j + 1, n + 2)
    mean_error = abs(mean - r) + eps / 100
    require(n0 >= 200 / eps and mean_error <= eps / 50 < eps / 40,
            "mean fails to concentrate inside the negative interval")
    variance = F((j + 1) * (q + 1), (n + 2)**2 * (n + 3))
    require(variance <= F(1, 4 * (n + 3)), "beta variance cap")
    d = eps / 20
    probability_cap = 1 / ((n + 3) * d**2)
    negative_size = eps**2 / 15000000
    require(probability_cap <= eps**2 / 80000000 < negative_size / 4,
            "Chebyshev error exceeds the negative contribution")
    expectation_cap = -negative_size + 2 * probability_cap
    require(expectation_cap <= -negative_size / 2, "negative beta sign lost")
    if wedge is not None:
        require(r >= 1 - 4 * b >= F(1, 2), "wedge lower center bound")
        require((1 - r) / r <= wedge / 4 and q <= wedge * (j + 2),
                "index not in the claimed wedge")
    return {
        "K": order, "b": text(b), "epsilon": text(eps), "rho": text(rho),
        "r": text(r), "Taylor_degree": degree,
        "N0": text(n0), "N": text(n), "j": text(j), "q": text(q),
        "N_decimal_digits": len(str(n)), "strip_budget": text(strip_budget),
        "negative_beta_upper_bound": text(-negative_size / 2),
        "wedge": None if wedge is None else text(wedge),
        "status": "rational producer certified; enormous beta sum not evaluated",
    }


def shifted_beta_identity(q: int) -> None:
    # Variables (t,u). Expand the entire binomial identity, without evaluation.
    right = {}
    for k in range(q + 1):
        for a in range(q - k + 1):
            for c in range(k + 1):
                key = (a + k, c)
                value = comb(q, k) * comb(q - k, a) * comb(k, c) * (-1)**(a + c)
                right[key] = right.get(key, 0) + value
    right = {key: value for key, value in right.items() if value}
    left = {(a, a): comb(q, a) * (-1)**a for a in range(q + 1)}
    require(left == right, "shifted beta expansion")


def audit() -> dict:
    # Polynomial bump: factorization ensures nonnegativity on its support.
    psi = [F(0), F(0), F(30), F(-60), F(30)]
    derivative = [(i + 1) * psi[i + 1] for i in range(len(psi) - 1)]
    second = [(i + 1) * derivative[i + 1] for i in range(len(derivative) - 1)]
    integral = sum((v / (i + 1) for i, v in enumerate(psi)), F(0))
    require(integral == 1 and sum(psi) == psi[0] == 0, "bump mass or endpoint")
    require(sum(derivative) == derivative[0] == 0, "bump derivative endpoint")
    require(sum(map(abs, derivative)) == 360 and sum(map(abs, second)) == 780,
            "bump derivative norm")
    require(poly_mul({(2, 0): 30}, {(0, 0): 1, (1, 0): -2, (2, 0): 1})
            == {(i, 0): v for i, v in enumerate(psi) if v}, "bump factorization")

    p1 = exp_derivative({(3, 0): 1})
    p2 = exp_derivative(p1)
    require(p1 == {(2, 0): 3, (3, 1): -1}, "first exponential derivative")
    require(p2 == {(1, 0): 6, (2, 1): -6, (3, 2): 1}, "second exponential derivative")
    b0 = {(-1, 0): 1, (-2, 0): 1}
    determinant = poly_add(poly_mul(b0, dx(dx(b0))), poly_scale(poly_mul(dx(b0), dx(b0)), -1))
    require(determinant == {(-4, 0): 1, (-5, 0): 4, (-6, 0): 2}, "baseline determinant")
    first_constant = factorial_bound({(4, 0): 3, (5, 1): 2}, 1, 4)
    cross_constant = factorial_bound({(4, 0): 21, (5, 1): 26, (6, 2): 6}, 1, 4)
    quadratic_constant = factorial_bound({(8, 0): 15, (9, 1): 24, (10, 2): 8}, 2, 8)
    require((first_constant, cross_constant, quadratic_constant)
            == (312, 7944, F(95445, 2)), "factorial constants")
    margin = 1 - F(7944, 20000) - F(48000, 20000**2)
    require(margin > F(1, 2) and quadratic_constant < 48000, "uniform log-convexity")
    require(F(8, 9)**3 * (1 + F(5, 2808)) < 1, "averaged rank-gap coefficient")
    f0_coeffs = [F(4**n * factorial(n), factorial(2 * n)) for n in (3, 4)]
    require(f0_coeffs == [F(8, 15), F(16, 105)], "half-integral constants")
    require(f0_coeffs[0] * 7 + f0_coeffs[1] * 25 < 8, "F0 weighted supremum")
    require(F(4, 3) * 3 + F(8, 15) * 7 < 8, "F0 derivative supremum")
    require(f0_coeffs[0] * 6 + f0_coeffs[1] * 12 < 8, "local baseline bound")
    require(F(2, 35) - F(1, 12) < -F(1, 40), "negative-interval margin")
    require(140**2 < 20000 and 4 * 27 < 12**2, "square-root constants")
    require(F(1088, 20000) == F(34, 625) < F(7, 50), "absolute hinge bound")
    require(F(3436, 20000) < 1, "derivative hinge bound")
    require(F(1, 80000000) < F(1, 4 * 15000000), "Chebyshev margin")

    # Exact mean, variance and beta-normalization checks, including endpoints.
    beta_controls = 0
    for j in range(6):
        for q in range(6):
            n = j + q
            norm = (n + 1) * comb(n, j)
            moments = [norm * F(factorial(j + k) * factorial(q), factorial(n + k + 1)) for k in range(3)]
            require(moments[0] == 1 and moments[1] == F(j + 1, n + 2), "beta normalization/mean")
            require(moments[2] - moments[1]**2 == F((j + 1) * (q + 1), (n + 2)**2 * (n + 3)), "beta variance")
            beta_controls += 1
    for q in range(13):
        shifted_beta_identity(q)

    # Detect representative corruptions; no checks rely on Python assertions.
    rejections = []
    mutations = (
        ("negative factorial coefficient", lambda: factorial_bound({(4, 0): -1}, 1, 4)),
        ("incorrect b homogeneity", lambda: factorial_bound({(4, 1): 1}, 1, 4)),
        ("invalid parameter", lambda: make_parameters(12, F(3, 4))),
        ("unprotected order", lambda: make_parameters(11, F(1, 4))),
        ("invalid wedge", lambda: make_parameters(12, F(1, 4), F(1, 10))),
    )
    for name, mutation in mutations:
        try:
            mutation()
        except ValueError:
            rejections.append(name)
        else:
            raise ValueError("corruption not rejected: " + name)

    cases = [make_parameters(12, F(1, 4)), make_parameters(20, F(1, 8)),
             make_parameters(12, F(1, 320), F(1, 10))]
    return {
        "status": "PASS", "arithmetic": "exact integers and fractions; no floats",
        "uniform_log_convexity_margin": text(margin),
        "factorial_constants": list(map(text, (first_constant, cross_constant, quadratic_constant))),
        "beta_probability_controls": beta_controls, "shift_identities": 13,
        "rejected_corruptions": rejections, "produced_cases": cases,
        "scope": "finite algebra/constant/index audits; universal analytic proof is PROOF.md",
        "not_claimed": "a realizable Gaussian or iid-replica counterexample",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="print exact expected audit")
    parser.add_argument("--produce", action="store_true", help="produce a certified negative beta index")
    parser.add_argument("--order", type=int, default=12, help="number K of protected diagonals")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--b", type=F, help="rational bump location, default 1/4")
    group.add_argument("--wedge", type=F, help="positive rational c in q<=c(j+2)")
    args = parser.parse_args()
    if args.produce:
        b = (min(F(1, 8), args.wedge / 32) if args.wedge is not None
             else (F(1, 4) if args.b is None else args.b))
        result = make_parameters(args.order, b, args.wedge)
    else:
        result = audit()
        if not args.emit:
            expected = json.loads(Path(__file__).with_name("EXPECTED.json").read_text())
            require(result == expected, "EXPECTED.json mismatch")
            print("PASS: exact constants; 36 beta controls; 13 shift identities; 5 rejected corruptions; 3 certified indices")
            print("Universal analytic theorem: PROOF.md. Actual R3 Gaussian majorisation remains open.")
            return
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
