#!/usr/bin/env python3
"""Compact formula audit, not a rigorous quadrature certificate.

The universal results are analytic proofs in PROOF.md. Numerical checks here
use an exactly specified, already-known-safe two-point contraction. The tail
is integrated by its Gaussian/erfc antiderivative, not by the inequalities in
the proof. Explicit exceptions keep all checks active under python -O.
"""
import argparse
from fractions import Fraction as F
import json
import math
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def simpson(function, n):
    require(n > 0 and n % 2 == 0, "invalid Simpson panel count")
    return math.fsum(
        (1 if j in (0, n) else 4 if j % 2 else 2) * function(j / n)
        for j in range(n + 1)
    ) / (3 * n)


def logcosh(x):
    return abs(x) + math.log1p(math.exp(-2 * abs(x))) - math.log(2)


def boundary_offset(z, A, R):
    # Input: equal atoms at +/-epsilon e1, epsilon=A/R, lambda=A, L=1.
    # Solve for u=R(r-R); Gaussian level is C exp(-R^2/2).
    def equation(u):
        return u + u * u / (2 * R * R) + A * A / (2 * R * R) - logcosh(
            A * (1 + u / (R * R)) * z
        )
    lo, hi = -A, A
    require(equation(lo) <= 1e-13 and equation(hi) >= -1e-13,
            "root bracket failed")
    for _ in range(80):
        mid = (lo + hi) / 2
        if equation(mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def tail_over_level(r, z, A, R):
    # Integral_r^infinity t^2 F(t theta) dt / (C exp(-R^2/2)).
    # Complete the square in each of the two Gaussian summands.
    epsilon = A / R
    terms = []
    for m in (-epsilon * z, epsilon * z):
        common = (R * R - epsilon * epsilon + m * m) / 2
        terms.append((r + m) * math.exp(common - (r - m) ** 2 / 2))
        terms.append((1 + m * m) * math.sqrt(math.pi / 2)
                     * math.exp(common) * math.erfc((r - m) / math.sqrt(2)))
    return math.fsum(terms) / 2


def normalized_hinge_gap(A, R, panels):
    point_tail = R + math.sqrt(math.pi / 2) * math.exp(R * R / 2) * math.erfc(
        R / math.sqrt(2)
    )
    def integrand(z):
        u = boundary_offset(z, A, R)
        r = R + u / R
        volume = u + u * u / (R * R) + u ** 3 / (3 * R ** 4)
        return volume + (tail_over_level(r, z, A, R) - point_tail) / R
    # In R3, theta.e1 is uniform on [-1,1]; the integrand is even.
    return simpson(integrand, panels)


def exact_constant_checks():
    count = 0
    for A in (F(0), F(1, 8), F(1, 2), F(1), F(2), F(5), F(20)):
        for multiplier in (1, 2, 7):
            R2 = max(F(1), 4 * A) * multiplier
            qmax = 4 * A / (3 * R2)
            require(qmax <= F(1, 3), "q bound")
            require(3 * A * A + A ** 3 / (3 * R2) <= 4 * A * A,
                    "volume constant")
            require(4 * A * A + F(5, 2) * A + 3 <= 4 * A * A + 3 * A + 3,
                    "combined constant")
            count += 1
    # Reproduce an exact conditional variance selection, not a real witness.
    lam, L, eta = F(3, 2), F(2), F(1, 100)
    A = lam * L
    K = 4 * A * A + 3 * A + 3
    R2 = max(F(1), 4 * A, 2 * K / eta) + 1
    s = R2 / (lam * lam)
    require(lam * lam * s == R2, "variance rescaling")
    require(2 * K / R2 < eta, "strict negative-gap transfer condition")
    return count, {"hypothetical_eta": str(eta), "lambda": str(lam),
                   "L": str(L), "s": str(s),
                   "error_bound": str(2 * K / R2),
                   "status": "conditional arithmetic only; no witness supplied"}


def run():
    count, conditional = exact_constant_checks()
    records = []
    max_refinement_error = 0.0
    for A in (0.5, 1.0, 2.0):
        target = simpson(lambda z: logcosh(A * z), 1024)
        require(target > 0, "known-safe fixture has wrong spherical sign")
        for R in (4.0, 8.0, 16.0, 32.0):
            require(R * R >= max(1, 4 * A), "invalid fixture regime")
            coarse = normalized_hinge_gap(A, R, 256)
            fine = normalized_hinge_gap(A, R, 512)
            refinement_error = abs(fine - coarse)
            max_refinement_error = max(max_refinement_error, refinement_error)
            require(refinement_error < 2e-9, "floating quadrature did not stabilize")
            bound = 2 * (4 * A * A + 3 * A + 3) / (R * R)
            require(abs(fine - target) <= bound + 1e-9, "formula audit outside bound")
            require(fine > 0, "known-safe fixture has wrong hinge sign")
            records.append({"lambda": A, "R": R,
                            "spherical_gap": round(target, 8),
                            "normalized_hinge_gap": round(fine, 8),
                            "R_squared_times_error": round((fine - target) * R * R, 7),
                            "analytic_error_bound": round(bound, 8)})
    return {
        "status": "FORMULA_AUDITS_PASSED",
        "trust_boundary": "analytic proof; floating quadrature only audits solvable fixtures",
        "exact_constant_fixtures": count,
        "conditional_variance_arithmetic": conditional,
        "angular_quadrature": "composite Simpson 256 and 512 panels; target 1024",
        "radial_tail": "Gaussian erfc antiderivative",
        "refinement_error_below": 2e-9,
        "fixtures": records,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = run()
    if args.check:
        expected = json.loads(Path(__file__).with_name("EXPECTED.json").read_text())
        require(result == expected, "compact expected audit differs")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
