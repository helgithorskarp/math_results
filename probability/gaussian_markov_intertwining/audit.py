#!/usr/bin/env python3
"""Exact finite controls for PROOF.md; not verification of its analytic theorem."""
import argparse
from fractions import Fraction as Q
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def exp_upper(x, degree):
    """Taylor polynomial plus a geometric majorant of its positive tail."""
    require(x >= 0 and degree >= 0, "invalid Taylor parameters")
    term = Q(1)
    total = term
    for k in range(1, degree + 1):
        term *= x / k
        total += term
    first_omitted = term * x / (degree + 1)
    ratio = x / (degree + 2)
    require(ratio < 1, "geometric tail does not converge")
    return total + first_omitted / (1 - ratio)


def run():
    xs = (Q(-1), Q(0), Q(1))
    ys = (Q(1, 2), Q(0), Q(3, 4))
    require(len(set(ys)) == 3, "target labels collide")
    require(tuple(Q(5, 8) * abs(x) + Q(1, 8) * x for x in xs) == ys,
            "global Lipschitz map has wrong images")
    ratios = []
    for i, j in ((0, 1), (1, 2), (0, 2)):
        ratio = abs(ys[i] - ys[j]) / abs(xs[i] - xs[j])
        require(0 < ratio <= Q(3, 4) < 1, "not a strict injective contraction")
        ratios.append(str(ratio))

    exponents = [Q(1, 2) - m - m * m / 2 for m in (ys[0], ys[2])]
    require(all(e <= -Q(1, 8) for e in exponents), "slab exponent margin fails")
    e1 = exp_upper(Q(1), 3)
    ehalf = exp_upper(Q(1, 2), 3)
    require(e1 < Q(11, 4), "exp(1) upper bound fails")
    require(e1 * e1 < Q(8), "exp(2) upper bound fails")
    require(ehalf < 2, "exp(1/2) upper bound fails")
    # Analytic inputs: pi<4, exp(x)>=1+x, Gaussian density monotonicity.
    require(2 * 4 < 3 * 3, "sqrt(2*pi)<3 control fails")
    loss = 1 - 1 / (1 + Q(1, 8))
    slab_mass = Q(1, 3) * Q(1, 8)
    denominator = Q(3)
    bound = loss * slab_mass / denominator
    require(bound == Q(1, 648), "TV normalization or error denominator fails")
    require(Q(1, 2) * (ys[0] + ys[2]) != ys[1], "midpoint obstruction vanishes")
    return {
        "status": "GAUSSIAN_CHANNEL_OBSTRUCTION_CONSTANTS_PASS",
        "distance_ratios": ratios,
        "target_midpoint_defect": str(ys[1] - (ys[0] + ys[2]) / 2),
        "slab_log_ratio_upper_bounds": [str(e) for e in exponents],
        "exp_1_upper": str(e1),
        "exp_half_upper": str(ehalf),
        "exp_2_upper": str(e1 * e1),
        "slab_mass_strict_lower": str(slab_mass),
        "relative_loss_lower": str(loss),
        "tv_error_strict_lower": str(bound),
        "scope": "finite geometry and constants only; analytic proof not formalized",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = run()
    if args.check:
        require(json.loads(args.check.read_text()) == result, "expected record mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))
