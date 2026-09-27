#!/usr/bin/env python3
"""Independent exact check of the complete Gaussian beta row N=11.

No target module or target certificate is imported.  The checker uses
decimal square-root enclosures and centered Taylor interval bounds, rather
than the target's dyadic Bernstein/de Casteljau certificate.  The analytic
replica/Jensen reduction remains reviewed written mathematics.
"""

import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from math import comb, isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
SQRT_DENOMINATOR = 10 ** 18

CASES = [
    {"base": 2, "q": 11, "abc": (4348, 28317, 35514),
     "multipliers": ((3, 29017),), "epsilon": F(1, 300),
     "polynomial_intervals": 128, "nonlinear_intervals": 64},
    {"base": 3, "q": 10, "abc": (2372, 11387, 11635),
     "multipliers": ((4, 10857),), "epsilon": F(1, 6000),
     "polynomial_intervals": 64, "nonlinear_intervals": 256},
    {"base": 4, "q": 9, "abc": (1720, 6860, 6163),
     "multipliers": ((4, 866), (5, 4627)), "epsilon": F(1, 30000),
     "polynomial_intervals": 64, "nonlinear_intervals": 256},
    {"base": 5, "q": 8, "abc": (1761, 6225, 5138),
     "multipliers": ((5, 3568),), "epsilon": F(1, 60000),
     "polynomial_intervals": 64, "nonlinear_intervals": 1024},
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pin_inputs():
    manifest = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    require(manifest["schema"] == 1, "manifest schema")
    for relative, expected in manifest["files"].items():
        actual = sha256((HERE / relative).read_bytes()).hexdigest()
        require(actual == expected, "changed target input: " + relative)
    return manifest


def rational_sqrt_bounds(n):
    integer = isqrt(n * SQRT_DENOMINATOR ** 2)
    lower = F(integer, SQRT_DENOMINATOR)
    upper = lower if integer * integer == n * SQRT_DENOMINATOR ** 2 \
        else F(integer + 1, SQRT_DENOMINATOR)
    require(lower * lower <= n <= upper * upper, "square-root enclosure")
    return lower, upper


def taylor_interval_certificate(coefficients, intervals):
    """Prove a rational polynomial positive on [0,1].

    On each equal interval, expand at its midpoint.  If the radius is h,
    p(c+x) >= t_0-sum_{k>0}|t_k|h^k for |x|<=h.  Everything below is a
    Fraction, so this is exact interval arithmetic with no rounding premise.
    """
    degree = len(coefficients) - 1
    radius = F(1, 2 * intervals)
    lower_bounds = []
    for index in range(intervals):
        center = F(2 * index + 1, 2 * intervals)
        taylor = [
            sum((coefficients[j] * comb(j, k) * center ** (j - k)
                 for j in range(k, degree + 1)), F(0))
            for k in range(degree + 1)
        ]
        lower = taylor[0] - sum(
            (abs(taylor[k]) * radius ** k for k in range(1, degree + 1)),
            F(0),
        )
        require(lower > 0, "Taylor interval is not strictly positive")
        lower_bounds.append(lower)
    encoded = "\n".join(map(str, lower_bounds)) + "\n"
    minimum = min(lower_bounds)
    return {
        "intervals": intervals,
        "minimum_numerator_bits": minimum.numerator.bit_length(),
        "minimum_denominator_bits": minimum.denominator.bit_length(),
        "minimum_sha256": sha256(str(minimum).encode()).hexdigest(),
        "bounds_sha256": sha256(encoded.encode()).hexdigest(),
    }


def minorant_polynomial(case):
    m, q = case["base"], case["q"]
    coefficients = []
    for ell in range(q + 1):
        lower, upper = rational_sqrt_bounds(m + ell)
        root = lower if ell % 2 == 0 else upper
        coefficients.append((-1) ** ell * comb(q, ell) * root)

    a, b, c = (F(value, 10000) for value in case["abc"])
    coefficients[0] -= a
    coefficients[1] += b
    coefficients[2] -= c
    for ell, numerator in case["multipliers"]:
        multiplier = F(numerator, 10000)
        require(multiplier >= 0 and 0 <= ell < q,
                "invalid monotonicity multiplier")
        coefficients[ell] -= multiplier
        coefficients[ell + 1] += multiplier * F(m + ell + 1, m + ell) ** 3
        # This is exactly the cancellation turning integral G dnu into
        # [B_(m+ell)-B_(m+ell+1)]/(m+ell)^3.
        require(F(m + ell + 1, m + ell) ** 3
                / (m + ell + 1) ** 3 == F(1, (m + ell) ** 3),
                "shifted-moment cancellation")
    return coefficients


def nonlinear_polynomial(case):
    """Substitute r=z^d into h(r)-epsilon, making it a polynomial."""
    m = case["base"]
    a, b, c = (F(value, 10000) for value in case["abc"])
    A, B, D = a / m ** 3, b / (m + 1) ** 3, c / (m + 2) ** 3
    exponent = F(2 * (m + 1) ** 2, m * (m + 2))
    p, d = exponent.numerator, exponent.denominator
    require(exponent > 1, "Jensen exponent")
    coefficients = [F(0)] * (p + 1)
    coefficients[0] = A - case["epsilon"]
    coefficients[d] = -B
    coefficients[p] = D
    return exponent, coefficients


def replica_controls(m):
    # With the m-cloud centroid at zero, adding U,V gives
    # Q_(m+2)-Q_m=U^2+V^2-(U+V)^2/(m+2).
    direct = (F(m + 1, m + 2), F(-2, m + 2), F(m + 1, m + 2))
    expanded = (1 - F(1, m + 2), F(-2, m + 2),
                1 - F(1, m + 2))
    require(direct == expanded, "two-replica variance increment")
    one_replica_rate = F(m, m + 1)
    tilted_rate = F(m + 1, m + 2)
    single_power = tilted_rate / one_replica_rate
    exponent = 2 * single_power
    require(exponent == F(2 * (m + 1) ** 2, m * (m + 2)),
            "retained-interaction exponent")
    return str(exponent)


def run():
    manifest = pin_inputs()
    records = []
    monotonicity_controls = 0
    for case in CASES:
        polynomial = minorant_polynomial(case)
        minorant = taylor_interval_certificate(
            polynomial, case["polynomial_intervals"])
        exponent, nonlinear = nonlinear_polynomial(case)
        margin = taylor_interval_certificate(
            nonlinear, case["nonlinear_intervals"])
        require(str(exponent) == replica_controls(case["base"]),
                "replica/nonlinear exponent mismatch")
        monotonicity_controls += len(case["multipliers"])
        records.append({
            "base": case["base"],
            "q": case["q"],
            "j": case["base"] - 2,
            "exponent": str(exponent),
            "epsilon": str(case["epsilon"]),
            "minorant": minorant,
            "substituted_degree": exponent.numerator,
            "nonlinear_margin": margin,
        })

    elevation_controls = 0
    for n in range(11):
        for j in range(n + 1):
            left, right = F(n + 1 - j, n + 2), F(j + 1, n + 2)
            require(left + right == 1 and left > 0 and right > 0,
                    "degree-elevation convexity")
            require(left * (n + 2) * comb(n + 1, j)
                    == (n + 1) * comb(n, j), "left normalization")
            require(right * (n + 2) * comb(n + 1, j + 1)
                    == (n + 1) * comb(n, j), "right normalization")
            elevation_controls += 1

    right_row = [[j, 11 - j] for j in range(4, 12)]
    require(all(q <= 7 for _, q in right_row), "seven-factor coverage")
    return {
        "status": "INDEPENDENT_COMPLETE_BETA_ROW_ELEVEN_ACCEPT",
        "verdict": "accept all beta entries in every row N<=11",
        "target_artifact": manifest["target_artifact"],
        "target_source_commit": manifest["target_source_commit"],
        "input_files": len(manifest["files"]),
        "sqrt_denominator": SQRT_DENOMINATOR,
        "sqrt_enclosures": sum(case["q"] + 1 for case in CASES),
        "cases": records,
        "retained_interaction_controls": len(CASES),
        "monotonicity_controls": monotonicity_controls,
        "degree_elevation_controls": elevation_controls,
        "credited_seven_factor_cases": right_row,
        "full_majorisation_proved": False,
        "formalized": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    result = run()
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    if args.emit:
        print(json.dumps(result, indent=2))
        return
    require(result == json.loads((HERE / "EXPECTED.json").read_text()),
            "expected record mismatch")
    print(json.dumps({
        "status": result["status"],
        "cases": len(result["cases"]),
        "exact_intervals": sum(
            row["minorant"]["intervals"]
            + row["nonlinear_margin"]["intervals"]
            for row in result["cases"]),
        "degree_elevation_controls": result["degree_elevation_controls"],
        "record_sha256": sha256(canonical.encode()).hexdigest(),
        "full_majorisation_proved": result["full_majorisation_proved"],
    }, indent=2))


if __name__ == "__main__":
    main()
