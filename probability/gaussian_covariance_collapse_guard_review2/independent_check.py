#!/usr/bin/env python3
"""Independent exact controls for the marginal covariance-collapse review.

No target module is imported.  The checker pins the reviewed packet, uses a
hard-coded Schur-complement witness construction checked against Sylvester's
criterion, reconstructs the target-thin certificate from ordered pairs, and
checks the rational part of the pressure/projection budget.  The continuum
Gaussian argument remains reviewed mathematics.
"""

import argparse
from fractions import Fraction as F
from functools import reduce
from hashlib import sha256
from itertools import product
import json
from math import factorial, gcd, lcm
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
        require(actual == expected, "changed target input: " + relative)
    return manifest


def dot(first, second):
    return sum((a * b for a, b in zip(first, second)), F(0))


def quadratic(matrix, vector):
    return dot(vector, [dot(row, vector) for row in matrix])


def determinant3(matrix):
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def sylvester_spd(matrix):
    return (matrix[0][0] > 0
            and matrix[0][0] * matrix[1][1] - matrix[0][1] ** 2 > 0
            and determinant3(matrix) > 0)


def primitive(vector):
    denominator = lcm(*(value.denominator for value in vector))
    integers = [int(value * denominator) for value in vector]
    divisor = reduce(gcd, map(abs, integers))
    require(divisor != 0, "zero witness")
    integers = [value // divisor for value in integers]
    if next(value for value in integers if value) < 0:
        integers = [-value for value in integers]
    return integers


def schur_witness(matrix):
    """Closed three-dimensional Schur test, independent of target code."""
    matrix = [[F(value) for value in row] for row in matrix]
    a = matrix[0][0]
    if a <= 0:
        return [1, 0, 0]
    first = [F(-matrix[0][1], a), F(1), F(0)]
    first_pivot = quadratic(matrix, first)
    if first_pivot <= 0:
        return primitive(first)
    second = [F(-matrix[0][2], a), F(0), F(1)]
    cross = dot(first, [dot(row, second) for row in matrix])
    last = [second[index] - cross * first[index] / first_pivot
            for index in range(3)]
    if quadratic(matrix, last) <= 0:
        return primitive(last)
    return None


def spectral_controls():
    count = positive = 0
    witnesses = []
    for diagonal in product([-1, 0, 1, 2], repeat=3):
        for off in product([-1, 0, 1], repeat=3):
            matrix = [
                [diagonal[0], off[0], off[1]],
                [off[0], diagonal[1], off[2]],
                [off[1], off[2], diagonal[2]],
            ]
            spd = sylvester_spd(matrix)
            witness = schur_witness(matrix)
            require((witness is None) == spd, "Schur/Sylvester mismatch")
            if witness is not None:
                require(quadratic(matrix, witness) <= 0,
                        "invalid nonpositive witness")
                witnesses.append(",".join(map(str, witness)))
            positive += spd
            count += 1
    require((count, positive) == (1728, 96), "spectral control totals")
    require(schur_witness([[1, 1, 0], [1, 1, 0], [0, 0, 1]])
            == [1, -1, 0], "singular oblique witness")
    return {
        "matrices": count,
        "positive_definite": positive,
        "nonpositive_witnesses": count - positive,
        "witness_sha256": sha256("|".join(witnesses).encode()).hexdigest(),
    }


def distance2(first, second):
    return sum((a - b) ** 2 for a, b in zip(first, second))


def covariance(cloud, weights, mean, variance):
    return [[sum(weight * (point[i] - mean[i]) * (point[j] - mean[j])
                 for weight, point in zip(weights, cloud)) / variance
             for j in range(3)] for i in range(3)]


def target_thin_control():
    data = json.loads((HERE / "../gaussian_covariance_collapse_guard/TARGET_THIN.json").read_text())
    expected = json.loads((HERE / "../gaussian_covariance_collapse_guard/EXPECTED.json").read_text())
    record = expected["records"]["target_thin"]
    source = [[F(value) for value in point] for point in data["sources"]]
    target = [[F(value) for value in point] for point in data["targets"]]
    weights = [F(value) for value in data["weights"]]
    variance = F(data.get("variance", 1))
    require(len(source) == len(target) == len(weights) > 0, "fixture dimensions")
    require(sum(weights) == 1 and all(weight >= 0 for weight in weights),
            "fixture probability")
    losses = [[distance2(source[i], source[j]) - distance2(target[i], target[j])
               for j in range(len(weights))] for i in range(len(weights))]
    require(all(value >= 0 for row in losses for value in row), "fixture contraction")
    d = sum(weights[i] * weights[j] * losses[i][j]
            for i in range(len(weights)) for j in range(len(weights))) / variance
    means = [[sum(weight * point[k] for weight, point in zip(weights, cloud))
              for k in range(3)] for cloud in (source, target)]
    covariances = [covariance(cloud, weights, mean, variance)
                   for cloud, mean in zip((source, target), means)]
    pair_source = sum(weights[i] * weights[j] * distance2(source[i], source[j])
                      for i in range(len(weights)) for j in range(len(weights)))
    radius2 = max(sum(weights[j] * distance2(source[i], source[j])
                      for j in range(len(weights))) - pair_source / 2
                  for i in range(len(weights))) / variance
    direction = [F(value) for value in record["direction"]]
    side = 0 if record["side"] == "source" else 1
    q = quadratic(covariances[side], direction) / dot(direction, direction)
    cutoff = d * d / F(2 ** 86)
    shifted = [[covariances[side][i][j] - (cutoff if i == j else 0)
                for j in range(3)] for i in range(3)]
    require(not sylvester_spd(shifted) and quadratic(shifted, direction) <= 0,
            "independent covariance witness")
    require(d == F(record["D"]), "ordered-pair loss record")
    require(radius2 == F(record["source_radius_squared"]) <= F(1, 4),
            "centered radius record")
    require(q == F(record["directional_variance"]) <= cutoff,
            "directional variance record")
    require(cutoff == F(record["variance_cutoff"]), "cutoff record")
    require(F(record["middle_margin"]) == d / F(2 ** 42), "margin record")
    invariant = "|".join(map(str, (d, q, cutoff, radius2, len(weights) ** 2)))
    return {
        "ordered_pairs": len(weights) ** 2,
        "contracting_pairs": sum(value > 0 for row in losses for value in row),
        "side": record["side"],
        "direction": record["direction"],
        "invariant_sha256": sha256(invariant.encode()).hexdigest(),
    }


def analytic_budget_controls():
    k = F(1, 2 ** 40)
    eta = k / 8
    core = F(4, 45) * F(3, 10) ** 4 / F(3 ** 18)
    require(core > k, "pressure-shell coefficient")
    require(F(44, 7) < 9, "surface/Gaussian rational bound")
    require(sum((F(1, factorial(j)) for j in range(4)), F(0)) == F(8, 3),
            "gradient exponential lower bound")
    # From the 1/6! term onward, successive ratios are at most 1/7.
    e_tail_upper = F(1, factorial(6)) / (1 - F(1, 7))
    e_upper = sum((F(1, factorial(j)) for j in range(6)), F(0)) + e_tail_upper
    require(e_upper < F(11, 4) < F(8, 7) ** 8, "modal exponential bound")
    exp_point_seven_lower = sum((F(7, 10) ** j / factorial(j)
                                 for j in range(5)), F(0))
    require(exp_point_seven_lower > 2, "log two upper bound")
    require(F(441, 25) < 18, "kernel-product exponent")
    require(1 - 4 * eta - eta * eta >= F(1, 2), "source loss transfer")
    require(k / 2 - 2 * eta == F(1, 2 ** 42), "source margin")
    require(k - eta > F(1, 2 ** 42), "target margin")
    replica_coefficients = [F(order - 1, 4) for order in range(2, 9)]
    return {
        "core_coefficient": core,
        "core_exceeds": k,
        "source_margin": k / 2 - 2 * eta,
        "target_margin_lower_bound": k - eta,
        "replica_coefficients_k2_to_k8": replica_coefficients,
    }


def run():
    manifest = pin_inputs()
    return {
        "status": "INDEPENDENT_COVARIANCE_COLLAPSE_REVIEW_PASS",
        "verdict": ("accept the marginal covariance-collapse middle-sign theorem "
                    "in its stated radius, loss, and threshold scope"),
        "target_commit": manifest["target_commit"],
        "target_graph_ref": manifest["target_graph_ref"],
        "pinned_target_files": len(manifest["files"]),
        "analytic_budget": analytic_budget_controls(),
        "spectral_controls": spectral_controls(),
        "target_thin_control": target_thin_control(),
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
    print("INDEPENDENT_COVARIANCE_COLLAPSE_REVIEW_PASS")
    print("record_sha256=" + sha256(record).hexdigest())


if __name__ == "__main__":
    main()
