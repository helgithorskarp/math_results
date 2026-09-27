#!/usr/bin/env python3
"""Independent exact controls for the uniform Lipschitz Gaussian endpoint.

No author module or certificate is imported.  This checks the theorem-level
constant chain and reconstructs the thin 18-site separation family directly.
The universal frame/Jensen argument remains written mathematics.
"""

import argparse
import copy
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations, product
import json
from math import factorial
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pin_inputs():
    manifest = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    require(manifest["schema"] == 1, "manifest schema")
    for relative, expected in manifest["files"].items():
        actual = sha256((HERE / relative).read_bytes()).hexdigest()
        require(actual == expected, "changed reviewed input: " + relative)
    return manifest


def determinant(matrix):
    n = len(matrix)
    require(all(len(row) == n for row in matrix), "square determinant")
    total = F(0)
    for permutation in permutations(range(n)):
        inversions = sum(permutation[i] > permutation[j]
                         for i in range(n) for j in range(i + 1, n))
        term = F(-1 if inversions % 2 else 1)
        for i, j in enumerate(permutation):
            term *= matrix[i][j]
        total += term
    return total


def covariance(points):
    n = len(points)
    mean = [sum(point[k] for point in points) / n for k in range(3)]
    return [[sum((point[i] - mean[i]) * (point[j] - mean[j])
                 for point in points) / n for j in range(3)] for i in range(3)]


def distance(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b))


def thin_family(epsilon):
    sources = [tuple(map(F, item))
               for item in product([-1, 0, 1], [-1, 0, 1],
                                   [-epsilon, epsilon])]
    targets = [(F(abs(u), 12), F(abs(v), 12), F(abs(u + v), 12))
               for u, v, _ in sources]
    return sources, targets


def frame_product_controls():
    records = []
    # Coefficients of d*product(1+u_j)-sum_j(1+u_j).
    for dimension in range(2, 9):
        coefficients = {}
        for mask in product([0, 1], repeat=dimension):
            coefficient = F(dimension)
            if not any(mask):
                coefficient -= dimension
            if sum(mask) == 1:
                coefficient -= 1
            require(coefficient >= 0, "frame product coefficient")
            coefficients[mask] = coefficient
        require(coefficients[(0,) * dimension] == 0,
                "frame product constant")
        records.append([dimension, len(coefficients),
                        str(min(v for v in coefficients.values() if v))])
    return records


def analytic_constant_controls():
    # phi(u)=cosh(sqrt(u)); these are the first exact coefficients of phi''.
    cosh_second = [F((k + 2) * (k + 1), factorial(2 * k + 4))
                   for k in range(32)]
    require(all(value > 0 for value in cosh_second), "cosh radial convexity")

    # The MGF estimate at lambda_0 R=1/2 gives 1/16 before log,
    # 1/32 after log, and 1/96 after the S^2 covariance average.
    exponential_variance = F(1, 2) ** 2 / 4
    log_variance = exponential_variance / 2
    spherical_variance = log_variance / 3
    require((exponential_variance, log_variance, spherical_variance)
            == (F(1, 16), F(1, 32), F(1, 96)), "scatter constants")

    schedules = 0
    for q, radius_squared, scatter_ratio in product(
            [F(1, 97), F(1, 8), F(1, 2), F(3, 4), F(7, 8),
             1 - F(1, 2 ** 60)],
            [F(1, 100), F(1), F(3), F(10000)],
            [F(1), F(1, 3), F(1, 2 ** 100)]):
        scatter = scatter_ratio * radius_squared
        eta = (1 - q) * scatter / (96 * radius_squared)
        cutoff = 4224 * radius_squared ** 2 / ((1 - q) * scatter)
        require(cutoff * eta == 44 * radius_squared,
                "endpoint error budget")
        require(cutoff > 8 * radius_squared, "high-noise budget")
        require(eta / (2 * scatter)
                == (1 - q) / (192 * radius_squared),
                "loss-normalized margin")
        schedules += 1

    require(F(27, 36) <= F(7, 8) ** 2, "one-sixth pair factor")
    require(F(4224, 1 - F(7, 8)) == 33792,
            "one-sixth cutoff")
    require(F(9, 64) - F(1, 8) == F(1, 64), "threshold overlap")
    require(3 ** 3 * F(1, 27) == 1,
            "dimension-three spherical factor squared")

    automatic = 0
    for z in [F(0), F(1, 101), F(27, 48), 1 - F(1, 2 ** 80)]:
        q = (1 + z) / 2
        require(q ** 2 - z == (1 - z) ** 2 / 4 and q < 1,
                "automatic factor")
        automatic += 1
    return {
        "frame_product_dimensions": frame_product_controls(),
        "cosh_second_derivative_coefficients": len(cosh_second),
        "cosh_second_derivative_last": str(cosh_second[-1]),
        "scatter_constant": str(spherical_variance),
        "endpoint_error_constant": 44,
        "threshold_overlap": "1/64",
        "cutoff_coefficient": 4224,
        "one_sixth_cutoff_coefficient": 33792,
        "parameter_schedules": schedules,
        "automatic_factor_controls": automatic,
    }


def family_controls():
    expected_target_covariance = [
        [F(1, 648), F(0), F(1, 1944)],
        [F(0), F(1, 648), F(1, 1944)],
        [F(1, 1944), F(1, 1944), F(11, 2916)],
    ]
    pair_controls = 0
    records = []
    for epsilon in [F(1, 100), F(1, 1000), F(1, 2 ** 70)]:
        sources, targets = thin_family(epsilon)
        ratios = []
        for i in range(len(sources)):
            for j in range(i):
                source_distance = distance(sources[i], sources[j])
                target_distance = distance(targets[i], targets[j])
                require(48 * target_distance <= source_distance,
                        "thin-family Lipschitz bound")
                if source_distance:
                    ratios.append(target_distance / source_distance)
                pair_controls += 1
        source_covariance = covariance(sources)
        target_covariance = covariance(targets)
        expected_source = [[F(2, 3) if i == j and i < 2
                            else epsilon ** 2 if i == j else F(0)
                            for j in range(3)] for i in range(3)]
        require(source_covariance == expected_source, "source covariance")
        require(target_covariance == expected_target_covariance,
                "target covariance")
        scatter = sum(source_covariance[i][i] for i in range(3))
        radius_squared = max(distance(point, (F(0), F(0), F(0)))
                             for point in sources)
        require(scatter == F(4, 3) + epsilon ** 2,
                "thin-family scatter")
        require(radius_squared == 2 + epsilon ** 2,
                "thin-family radius")
        require(max(ratios) == F(1, 48), "sharp family pair ratio")
        records.append([str(epsilon), str(scatter), str(radius_squared)])

    shifted = [[expected_target_covariance[i][j]
                - (F(1, 972) if i == j else 0) for j in range(3)]
               for i in range(3)]
    scaled = [[5832 * value for value in row] for row in shifted]
    leading_minors = [determinant([row[:k] for row in scaled[:k]])
                      for k in range(1, 4)]
    require(leading_minors == [3, 9, 90], "target covariance floor")
    require(F(1, 10000) < F(1, 972), "source-target covariance separation")

    determinant_values = []
    for epsilon in [F(0), F(1)]:
        sources, targets = thin_family(epsilon)
        rows = [[F(1), *sources[i], *targets[i]]
                for i in [0, 1, 2, 4, 6, 12, 16]]
        determinant_values.append(determinant(rows))
    require(determinant_values == [0, F(-1, 54)],
            "paired affine determinant")

    uniform_upper = (16896 * (2 + F(1, 10000)) ** 2 / F(4, 3))
    require(uniform_upper < 51000, "uniform family cutoff")
    epsilon = F(1, 100)
    exact_cutoff = (16896 * (2 + epsilon ** 2) ** 2
                    / (F(4, 3) + epsilon ** 2))
    require(exact_cutoff == F(1267326723168, 25001875),
            "published family cutoff")
    return {
        "pair_controls": pair_controls,
        "operator_remainder": "(a-b)^2",
        "sharp_squared_lipschitz": "1/48",
        "parameter_records": records,
        "target_covariance": [[str(value) for value in row]
                              for row in expected_target_covariance],
        "covariance_floor_scaled_leading_minors": list(map(int, leading_minors)),
        "paired_affine_determinant_coefficient": "-1/54",
        "uniform_cutoff_upper": str(uniform_upper),
        "published_epsilon_cutoff": str(exact_cutoff),
    }


def validate_schedule(record):
    q, beta = record["q"], record["beta"]
    radius_squared, scatter = record["B"], record["V"]
    require(0 < q < 1 and 0 < scatter <= radius_squared,
            "schedule parameter domain")
    require(q ** 2 >= 27 * beta, "schedule pair factor")
    eta = (1 - q) * scatter / (96 * radius_squared)
    cutoff = 4224 * radius_squared ** 2 / ((1 - q) * scatter)
    require(record["eta"] == eta and record["cutoff"] == cutoff,
            "schedule constants")
    require(cutoff * eta == 44 * radius_squared, "schedule endpoint")
    require(record["signed"] == (record["s"] >= cutoff),
            "schedule status")


def corruption_controls():
    base = {"q": F(3, 4), "beta": F(1, 48),
            "B": F(20001, 10000), "V": F(40003, 30000),
            "s": F(51000), "signed": True}
    base["eta"] = (1 - base["q"]) * base["V"] / (96 * base["B"])
    base["cutoff"] = 4224 * base["B"] ** 2 / ((1 - base["q"]) * base["V"])
    validate_schedule(base)
    damaged = []
    item = copy.deepcopy(base); item["eta"] *= 2; damaged.append(item)
    item = copy.deepcopy(base); item["cutoff"] -= 1; damaged.append(item)
    item = copy.deepcopy(base); item["q"] = F(1); damaged.append(item)
    item = copy.deepcopy(base); item["s"] = base["cutoff"] - 1; damaged.append(item)
    rejected = 0
    for item in damaged:
        try:
            validate_schedule(item)
        except ValueError:
            rejected += 1
        else:
            raise RuntimeError("damaged schedule accepted")
    return rejected


def run():
    manifest = pin_inputs()
    return {
        "status": "INDEPENDENT_UNIFORM_LIPSCHITZ_ACCEPT",
        "verdict": "accept the stated uniform eventual Gaussian majorisation family",
        "target_artifact": manifest["target_artifact"],
        "target_source_commit": manifest["target_source_commit"],
        "pinned_files": len(manifest["files"]),
        "analytic_constant_controls": analytic_constant_controls(),
        "thin_family_controls": family_controls(),
        "rejected_corruptions": corruption_controls(),
        "all_variances_proved": False,
        "unrestricted_contractions_proved": False,
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
        "pinned_files": result["pinned_files"],
        "parameter_schedules": result["analytic_constant_controls"]["parameter_schedules"],
        "family_pair_controls": result["thin_family_controls"]["pair_controls"],
        "rejected_corruptions": result["rejected_corruptions"],
        "record_sha256": sha256(canonical.encode()).hexdigest(),
        "all_variances_proved": result["all_variances_proved"],
    }, indent=2))


if __name__ == "__main__":
    main()
