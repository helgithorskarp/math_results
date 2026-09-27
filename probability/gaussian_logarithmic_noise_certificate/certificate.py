"""Compressed universal sign schedules from PROOF.md; exact integers only.

The supplied radius is a mathematical premise, not a measured input geometry.
This is not a full Gaussian-majorisation decision procedure.
"""
import argparse
import json
from math import comb


def need(condition, message):
    if not condition:
        raise ValueError(message)


def nonnegative_integer(n):
    need(type(n) is int and n >= 0, "nonnegative integer degree")


def eligible(k, n):
    nonnegative_integer(n)
    need(type(k) is int and k >= 12, "integer k >= 12")
    need(n.bit_length() <= k - 4, "degree exceeds signed cone")


def schedule(n):
    nonnegative_integer(n)
    k = max(12, 4 + n.bit_length())
    eligible(k, n)
    q = 8 * n + 4 * k + 24
    return {
        "status": "UNIFORM_SIGNED_POLYNOMIAL_CONE_AUTHOR_THEOREM",
        "curvature_degree": n,
        "energy_degree": n + 2,
        "k": k,
        "minimum_variance_over_radius_squared": 8 * k,
        "normalization_interval_left_power_of_two": -2 * k,
        "normalization_interval_right": "1/4",
        "energy_gap_over_loss_and_curvature_norm_lower_power_of_two": -4 * k - 6,
        "taylor_order": q,
        "taylor_error_over_loss_and_curvature_norm_upper_power_of_two": -4 * k - 8,
        "taylor_functional_lower_mantissa": 3,
        "taylor_functional_lower_power_of_two": -4 * k - 8,
        "paired_cubature_atoms_upper": 2 * comb(2 * q + 3, 3) - 1,
        "scope": "all bounded R3 laws and contractions; convex polynomial energies only",
        "review": "independent acceptance pending",
    }


def verify_schedule(record):
    need(isinstance(record, dict), "schedule object")
    need(record == schedule(record.get("curvature_degree")), "schedule mismatch")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--curvature-degree", type=int, required=True)
    args = parser.parse_args()
    print(json.dumps(schedule(args.curvature_degree), indent=2, sort_keys=True))
