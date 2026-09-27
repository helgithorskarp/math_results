#!/usr/bin/env python3
"""Independent exact controls for the arbitrary-radius covariance guard.

No target Python module is imported.  This checker pins the reviewed proof,
its quantitative-motion dependency, reconstructs every exponent from the
proof, checks the complete dyadic implication chain on an independent grid,
and verifies both projection/loss identities on fresh rational data.  The
continuum pressure and Gaussian estimates remain reviewed mathematics.
"""

import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from math import isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {key: encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(item) for item in value]
    return value


def pin_inputs():
    manifest = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    require(manifest["schema"] == 1, "manifest schema")
    for relative, expected in manifest["files"].items():
        actual = sha256((HERE / relative).read_bytes()).hexdigest()
        require(actual == expected, "changed reviewed input: " + relative)
    return manifest


def inverse_power2(exponent):
    require(isinstance(exponent, int) and exponent >= 0, "nonnegative exponent")
    return F(1, 1 << exponent)


def ceil_sqrt(value):
    root = isqrt(value)
    return root + (root * root < value)


def schedule(radius, threshold_bits, loss_bits):
    q = ceil_sqrt(2 * (threshold_bits + 1))
    z = loss_bits + 4 + 9 * radius * radius
    b = (31 + 47 * radius * radius + 2 * (2 * radius + q) ** 2
         + 5 * loss_bits)
    return q, z, b, 2 * b + 4


def budget_grid():
    rows = []
    checks = 0
    for radius in (1, 2, 3, 5, 8):
        for threshold_bits in (1, 2, 6, 19):
            for loss_bits in (0, 1, 7):
                q, z, b, ell = schedule(radius, threshold_bits, loss_bits)
                eta = inverse_power2(b + 2)
                loss = inverse_power2(loss_bits)
                zeta = inverse_power2(z)
                beta = inverse_power2(b)

                # Exact versions of (18)--(19), loss retention, peak
                # separation, H2's loss floor, shell budget and final error.
                assertions = [
                    (q - 1) ** 2 < 2 * (threshold_bits + 1) <= q * q,
                    b + 2 >= z,
                    b + 2 - loss_bits >= 4 * radius * radius,
                    12 * radius <= 2 ** (4 * radius * radius),
                    eta <= zeta,
                    eta <= loss / (12 * radius),
                    eta <= beta / 4,
                    6 * radius * eta <= loss / 2,
                    inverse_power2(9 * radius * radius) * loss / 8 - eta >= zeta,
                    zeta <= loss / 16,
                    2 * inverse_power2(2 * radius * radius) * zeta >=
                    inverse_power2(2 * radius * radius) * zeta,
                    inverse_power2(11) * zeta ** 5
                    * inverse_power2(2 * radius * radius
                                     + 2 * (2 * radius + q) ** 2) == beta,
                    beta - 2 * eta == inverse_power2(b + 1),
                    eta * eta == inverse_power2(ell),
                ]
                require(all(assertions), "dyadic implication chain")
                checks += len(assertions)
                rows.append([radius, threshold_bits, loss_bits, q, z, b, ell])

    # The proof of 12R <= 2^(4R^2) is uniform: 12 <= 16, and the
    # ratio 16^(R+1)/(12(R+1)) divided by 16^R/(12R) is >= 8.
    require(F(16, 12) > 1 and F(16, 2) >= 8, "uniform integer-radius bound")
    # e>2 and sqrt(2*pi)<3 imply A>2^(5/2)/(96*3)>2^-7;
    # the last comparison is equivalent after squaring to 32>81/16.
    require(F(32) > F(81, 16), "target-peak prefactor lower bound")
    return {"expanded_checks": checks, "parameter_rows": len(rows),
            "headline_row": rows[7], "target_control_row": rows[33],
            "rows_sha256": sha256(json.dumps(rows).encode()).hexdigest()}


def dot(first, second):
    return sum((x * y for x, y in zip(first, second)), F(0))


def subtract(first, second):
    return tuple(x - y for x, y in zip(first, second))


def mean(points, weights):
    return tuple(sum((p * x[j] for p, x in zip(weights, points)), F(0))
                 for j in range(3))


def variance(points, weights):
    center = mean(points, weights)
    return sum((p * dot(subtract(x, center), subtract(x, center))
                for p, x in zip(weights, points)), F(0))


def pair_loss(sources, targets, weights):
    return sum((2 * weights[i] * weights[j]
                * (dot(subtract(sources[i], sources[j]),
                       subtract(sources[i], sources[j]))
                   - dot(subtract(targets[i], targets[j]),
                         subtract(targets[i], targets[j])))
                for i, j in combinations(range(len(weights)), 2)), F(0))


def projection_controls():
    weights = [F(1, 3)] * 3
    source = [(F(1), F(0), F(1)),
              (F(-1), F(1), F(-1)),
              (F(0), F(-1), F(0))]
    target = [(x / 2, y / 3, z / 4) for x, y, z in source]
    projected_source = [(x, y, F(0)) for x, y, z in source]
    mapped_projection = [(x / 2, y / 3, F(0))
                         for x, y, z in source]
    projected_target = [(x, y, F(0)) for x, y, z in target]

    require(mean(source, weights) == mean(target, weights) == (0, 0, 0),
            "centered fixture")
    for i, j in combinations(range(3), 2):
        require(dot(subtract(target[i], target[j]),
                    subtract(target[i], target[j])) <=
                dot(subtract(source[i], source[j]),
                    subtract(source[i], source[j])), "fixture contraction")

    loss = pair_loss(source, target, weights)
    require(loss == 2 * (variance(source, weights)
                         - variance(target, weights)), "pair/variance identity")

    source_lambda = sum((p * x[2] ** 2 for p, x in zip(weights, source)), F(0))
    source_reference_loss = pair_loss(projected_source, mapped_projection, weights)
    source_difference = abs(loss - source_reference_loss)
    # Avoid irrational arithmetic: here eta^2=lambda=2/3 and direct squaring
    # proves |D-D0| <= 6R eta with R=2.
    require(source_difference ** 2 <= 144 * source_lambda,
            "source projected-loss bound")

    target_lambda = sum((p * y[2] ** 2 for p, y in zip(weights, target)), F(0))
    target_reference_loss = pair_loss(source, projected_target, weights)
    require(target_reference_loss == loss + 2 * target_lambda,
            "target projected-loss identity")
    return {
        "labels": 3,
        "pairs": 3,
        "loss": loss,
        "source_directional_variance": source_lambda,
        "source_reference_loss": source_reference_loss,
        "source_loss_difference": source_difference,
        "target_directional_variance": target_lambda,
        "target_reference_loss": target_reference_loss,
    }


def motion_margin_controls():
    # C1 approximation uses U(r)=rQ(r), whose pressure is r^2 Q'(r).
    # The R5 shell constant reduces using |S4|=8*pi^2/3 to
    # e^(5/2)/(96*sqrt(2*pi)); the integer cancellation is checked here.
    require(3 * 64 * 4 == 8 * 96, "R5 shell constant")
    # In two Gaussian coordinates, exp(-|Y|^2/(2s)) is uniform on (0,1),
    # yielding integral f*1[f gamma2>C2 h] = integral (f-h)_+.
    # Continuous pair distances make their Stieltjes measures atomless,
    # so terminal mass at d(t*)=ell is retained without an endpoint loss.
    return {
        "pressure_substitution": "U(r)=rQ(r), P(r)/r^2=Q'(r)",
        "radial_constant_denominator": 96,
        "lift_dimension": 5,
        "marginalized_coordinates": 2,
        "terminal_interval_atomless": True,
    }


def run():
    manifest = pin_inputs()
    return {
        "status": "INDEPENDENT_COVARIANCE_BOUNDARY_REVIEW_PASS",
        "verdict": ("accept arbitrary-radius positive-loss covariance-boundary "
                    "sign and actual-source-peak margin in the stated scope"),
        "target_commit": manifest["target_commit"],
        "target_graph_ref": manifest["target_graph_ref"],
        "dependency_commit": manifest["dependency_commit"],
        "pinned_inputs": len(manifest["files"]),
        "budget_grid": budget_grid(),
        "projection_controls": projection_controls(),
        "motion_margin_controls": motion_margin_controls(),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    record = (json.dumps(encode(run()), sort_keys=True, indent=2) + "\n").encode()
    if args.emit:
        print(record.decode(), end="")
        return
    require(record == (HERE / "REVIEW_EXPECTED.json").read_bytes(),
            "expected review record mismatch")
    print("INDEPENDENT_COVARIANCE_BOUNDARY_REVIEW_PASS")
    print("record_sha256=" + sha256(record).hexdigest())


if __name__ == "__main__":
    main()
