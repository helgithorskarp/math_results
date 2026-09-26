#!/usr/bin/env python3
"""Independent source and exact-sign controls for the Theorem G review.

These finite controls catch source drift and the central algebraic sign mistakes.
They do not prove the W^{1,1} approximation or the volume-limit argument.
"""

import argparse
from fractions import Fraction as F
from hashlib import sha256
import json
from pathlib import Path


EXPECTED = {
    "REGULARITY.md": "20a2d4cfa3ff8222247b952b31379ea208c2fee8f77c71035a6b3e3ed6efbfeb",
    "MATRIX_PATHS.md": "c4f20586c2612df285d8b6d5245d00370e507f71df70ce2bac36cdcf4208beb7",
    "ROBUSTNESS.md": "101d42be18afe3d9a8c0364e2da8af25d58a50d178c1ddee291f6dbf3837d69c",
}


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path,
                        default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()

    observed = {name: file_hash(args.source / name) for name in EXPECTED}
    if observed != EXPECTED:
        raise ValueError("reviewed source identity mismatch")

    # Section 3's exact diagnostic values.
    t = F(3, 4)
    distance = 1 - 2 * t + 2 * t * t
    derivative = 4 * t - 2
    full_bracket = derivative - F(1, F(1, 2)) * distance
    half_bracket = derivative - F(1, 2) / F(1, 2) * distance
    assert (derivative, full_bracket, half_bracket) == (1, F(-1, 4), F(3, 8))

    # Generic scaling lemma on a dense exact rational control grid.
    scaling_controls = 0
    for b_num in range(1, 9):
        b = F(b_num, 8)
        for excess in range(9):
            distance_control = b + F(excess, 8)
            for e_num in range(9):
                error = F(e_num, 8)
                for slack in range(9):
                    distance_derivative = error - F(slack, 8)
                    bracket = (distance_derivative
                               - (error / b) * distance_control)
                    assert bracket <= 0
                    scaling_controls += 1

    # Equation (10)--(11): integrate e=2 B ((J-2)/J) k exactly.
    critical_controls = 0
    for j_num in range(17, 41):
        support_cost = F(j_num, 8)
        for b_num in range(9):
            cross_height = F(b_num, 8)
            for sigma_num in range(1, 9):
                sigma_squared = F(sigma_num, 8)
                epsilon = (support_cost - 2) / support_cost
                integrated_error = 2 * cross_height * epsilon * support_cost
                exponent = integrated_error / sigma_squared
                assert integrated_error == 2 * cross_height * (support_cost - 2)
                assert exponent == 2 * cross_height * (support_cost - 2) / sigma_squared
                critical_controls += 1

    # Robustness equation (R4), including all equality faces on a rational grid.
    reserve_controls = 0
    denominator = 24
    for lambda_num in range(1, denominator + 1):
        lam = F(lambda_num, denominator)
        for eta_num in range(lambda_num + 1):
            eta = F(eta_num, denominator)
            for r_num in range(lambda_num + eta_num, denominator + 1):
                reserve = F(r_num, denominator)
                lhs = (lam * lam - reserve * lam + eta * eta
                       + abs(2 * lam - reserve) * eta)
                rhs = max((lam + eta) * (lam + eta - reserve),
                          (lam - eta) * (lam - eta - reserve))
                assert lhs == rhs <= 0
                reserve_controls += 1

    first_segment_controls = 0
    for epsilon_num in range(denominator):
        epsilon = F(epsilon_num, denominator)
        for r_num in range(1, denominator - epsilon_num + 1):
            reserve = F(r_num, denominator)
            assert reserve * (reserve - 1 + epsilon) <= 0
            first_segment_controls += 1

    report = {
        "status": "REGULARITY_REVIEW2_CONTROLS_PASS",
        "source_sha256": observed,
        "section3_values": [str(derivative), str(full_bracket), str(half_bracket)],
        "scaling_controls": scaling_controls,
        "critical_budget_controls": critical_controls,
        "reserve_controls": reserve_controls,
        "first_segment_controls": first_segment_controls,
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    print(report["status"], sha256(canonical).hexdigest())
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
