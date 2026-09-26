#!/usr/bin/env python3
"""Independent checks for the near-isometry Gaussian contact review.

The exact part reconstructs the pair-loss, displacement, and Procrustes
bounds for a symmetric two-point law using Fraction arithmetic.  The analytic
part evaluates that example's actual one-dimensional concentration profiles
in closed form; it imports no source-packet code or data.
"""

import argparse
from fractions import Fraction as F
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def normal_cdf(x):
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0


def decimal(x):
    return format(x, ".17g")


def build_report():
    # X is uniform on {-R,R}; Y=cX.  The identity is the Procrustes
    # alignment, Cov(X)=R^2, and the positive top sets below are intervals.
    radius = F(1, 5)
    contraction = F(99, 100)
    kappa = radius**2
    delta = (1 - contraction) * radius
    mean_square_error = delta**2
    pair_loss = 2 * radius**2 * (1 - contraction**2)
    nonzero_pair_loss = 4 * radius**2 * (1 - contraction**2)
    pair_loss_square_mean = nonzero_pair_loss**2 / 2

    require(pair_loss == nonzero_pair_loss / 2, "two-point pair-loss mean")
    require(mean_square_error <= pair_loss_square_mean / (2 * kappa),
            "first Procrustes bound")
    require(pair_loss_square_mean <= 8 * radius * delta * pair_loss,
            "displacement-sensitive pair-loss bound")
    require(mean_square_error <= 4 * radius * delta * pair_loss / kappa,
            "absorbed Procrustes bound")
    require(nonzero_pair_loss <= 8 * radius * delta,
            "pointwise loss bound")

    # For t=v=1 in dimension one, omega_1=2 and r=v/2=1/2.
    # Since R^2<t, z -> .5 phi(z-R)+.5 phi(z+R) is strictly decreasing
    # for z>0: z-R*tanh(R*z)>=(1-R^2)z>0.  Thus the actual source and target
    # top sets are both the interval [-1/2,1/2].
    half_volume = F(1, 2)
    exponent = (half_volume + radius) ** 2 / 2 + (half_volume + 3 * radius) ** 2
    require(exponent == F(291, 200), "q exponent")

    R = float(radius)
    c = float(contraction)
    b = float(half_volume)
    C = 1.0 / math.sqrt(2.0 * math.pi)
    q = math.exp(-float(exponent))
    D = float(pair_loss)
    M = float(mean_square_error)

    source_profile = normal_cdf(b - R) + normal_cdf(b + R) - 1.0
    target_profile = normal_cdf(b - c * R) + normal_cdf(b + c * R) - 1.0
    actual_gap = target_profile - source_profile

    # Derivative of the source mass of [-b,b] along
    # X_theta=(1-theta(1-c))X at theta=0.
    first_variation = (
        R * (1.0 - c) * C
        * (math.exp(-0.5 * (b - R) ** 2) - math.exp(-0.5 * (b + R) ** 2))
    )
    posterior_lower_bound = C * q * D / 4.0
    taylor_lower_bound = first_variation - C * M / 2.0
    theorem_4_bound = C * (q - 8.0 * R * float(delta) / float(kappa)) * D / 4.0
    theorem_6_bound = C * q * D / 8.0
    proximity_threshold = float(kappa) * q / (16.0 * R)

    require(float(delta) < proximity_threshold, "near-isometry hypothesis")
    require(first_variation >= posterior_lower_bound, "posterior derivative bound")
    require(actual_gap >= taylor_lower_bound, "finite Taylor remainder")
    require(actual_gap >= theorem_4_bound >= theorem_6_bound > 0,
            "signed endpoint profile bounds")

    return {
        "scope": (
            "Exact two-point algebra and a closed-form one-dimensional endpoint "
            "profile stress test; the universal analytic theorem remains a "
            "written-proof obligation."
        ),
        "exact_two_point_algebra": {
            "D": str(pair_loss),
            "E_Delta_squared": str(pair_loss_square_mean),
            "M": str(mean_square_error),
            "R": str(radius),
            "delta": str(delta),
            "kappa": str(kappa),
            "q_exponent": str(exponent),
        },
        "closed_form_profile_test": {
            "actual_endpoint_gap": decimal(actual_gap),
            "first_variation": decimal(first_variation),
            "posterior_lower_bound": decimal(posterior_lower_bound),
            "proximity_threshold": decimal(proximity_threshold),
            "theorem_4_lower_bound": decimal(theorem_4_bound),
            "theorem_6_lower_bound": decimal(theorem_6_bound),
            "taylor_lower_bound": decimal(taylor_lower_bound),
        },
        "status": "INDEPENDENT_NEAR_ISOMETRY_CHECK_PASS",
        "unrestricted_dimension_three_majorisation_verified": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    rendered = json.dumps(build_report(), indent=2, sort_keys=True) + "\n"
    if args.emit:
        print(rendered, end="")
        return
    expected = (HERE / "EXPECTED.json").read_text(encoding="utf-8")
    require(rendered == expected, "EXPECTED.json differs from recomputation")
    print("INDEPENDENT_NEAR_ISOMETRY_CHECK_PASS")


if __name__ == "__main__":
    main()
