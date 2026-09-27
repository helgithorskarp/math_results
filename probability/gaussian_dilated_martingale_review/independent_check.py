#!/usr/bin/env python3
"""Independent exact review controls for the dilated-martingale theorem.

The target modules and target certificates are never imported.  This checker
constructs a different unequal-geometry, full-paired-rank witness, derives the
affine coupling by adjugate inversion, and checks every mass and conditional
moment with Fraction arithmetic.  The continuum MGF and endpoint argument is
reviewed mathematics rather than a finite computation.
"""

import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
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


def dot(first, second):
    return sum((x * y for x, y in zip(first, second)), F(0))


def dist2(first, second):
    return sum(((x - y) ** 2 for x, y in zip(first, second)), F(0))


def determinant(matrix):
    if not matrix:
        return F(1)
    return sum(((-1) ** j * matrix[0][j]
                * determinant([row[:j] + row[j + 1:] for row in matrix[1:]])
                for j in range(len(matrix))), F(0))


def inverse_adjugate(matrix):
    det = determinant(matrix)
    require(det != 0, "singular covariance")
    size = len(matrix)
    cofactors = []
    for i in range(size):
        row = []
        for j in range(size):
            minor = [[matrix[r][c] for c in range(size) if c != j]
                     for r in range(size) if r != i]
            row.append((-1) ** (i + j) * determinant(minor))
        cofactors.append(row)
    return [[cofactors[j][i] / det for j in range(size)]
            for i in range(size)]


def matmul(first, second):
    return [[sum((first[i][k] * second[k][j]
                  for k in range(len(second))), F(0))
             for j in range(len(second[0]))] for i in range(len(first))]


def rank(matrix):
    rows = [list(map(F, row)) for row in matrix]
    pivot_row = 0
    for column in range(len(rows[0])):
        pivot = next((i for i in range(pivot_row, len(rows))
                      if rows[i][column]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = rows[pivot_row][column]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]
        for i in range(len(rows)):
            if i != pivot_row and rows[i][column]:
                scale = rows[i][column]
                rows[i] = [value - scale * base
                           for value, base in zip(rows[i], rows[pivot_row])]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def center(cloud, weights):
    mean = [sum((weight * point[k]
                 for weight, point in zip(weights, cloud)), F(0))
            for k in range(3)]
    return mean, [[point[k] - mean[k] for k in range(3)] for point in cloud]


def covariance(centered, weights):
    return [[sum((weight * point[i] * point[j]
                  for weight, point in zip(weights, centered)), F(0))
             for j in range(3)] for i in range(3)]


def pair_covariance(cloud, weights):
    return [[sum((weights[p] * weights[q]
                  * (cloud[p][i] - cloud[q][i])
                  * (cloud[p][j] - cloud[q][j]) / 2
                  for p, q in product(range(len(cloud)), repeat=2)), F(0))
             for j in range(3)] for i in range(3)]


def all_principal_minors(matrix):
    return [determinant([[matrix[i][j] for j in indices] for i in indices])
            for size in range(1, len(matrix) + 1)
            for indices in combinations(range(len(matrix)), size)]


def certify_family(scale=F(1), source_shift=(0, 0, 0),
                   target_shift=(0, 0, 0), damping=F(1, 144)):
    base = [(1, 0, 0), (-1, 0, 0), (0, 2, 0), (0, -2, 0),
            (0, 0, 3), (0, 0, -3), (1, 1, 1), (-1, -1, -1)]
    weights = [F(1, 8)] * len(base)
    sources = [[scale * F(value) + F(source_shift[k])
                for k, value in enumerate(point)] for point in base]
    # Coordinatewise absolute value is globally 1-Lipschitz in Euclidean norm.
    targets = [[scale * damping * abs(F(value)) + F(target_shift[k])
                for k, value in enumerate(point)] for point in base]

    for i, j in combinations(range(len(base)), 2):
        require(dist2(targets[i], targets[j]) <= dist2(sources[i], sources[j]),
                "matched map is not a contraction")

    _, x = center(sources, weights)
    _, y = center(targets, weights)
    sigma = covariance(x, weights)
    require(sigma == pair_covariance(sources, weights),
            "two covariance representations disagree")
    source_scatter = sum(sigma[i][i] for i in range(3))
    radius_squared = max(dot(point, point) for point in x)
    kappa = scale ** 2 / 4
    shifted = [[sigma[i][j] - (kappa if i == j else 0)
                for j in range(3)] for i in range(3)]
    minors = all_principal_minors(shifted)
    require(all(value >= 0 for value in minors), "covariance floor")
    require(damping == kappa / (4 * radius_squared), "damping boundary")

    inverse = inverse_adjugate(sigma)
    identity = matmul(sigma, inverse)
    require(identity == [[F(i == j) for j in range(3)] for i in range(3)],
            "adjugate inverse")
    dilation = F(2)
    matrix = [[dilation * value for value in row] for row in inverse]

    masses = [[F(0)] * len(base) for _ in base]
    kernels = [[F(0)] * len(base) for _ in base]
    for i, j in product(range(len(base)), repeat=2):
        kernels[i][j] = 1 + sum(
            (x[i][r] * matrix[r][s] * y[j][s]
             for r, s in product(range(3), repeat=2)), F(0))
        require(kernels[i][j] >= 0, "negative affine coupling density")
        masses[i][j] = weights[i] * weights[j] * kernels[i][j]

    for i in range(len(base)):
        require(sum(masses[i], F(0)) == weights[i], "source marginal")
    for j in range(len(base)):
        require(sum((masses[i][j] for i in range(len(base))), F(0))
                == weights[j], "target marginal")
        for coordinate in range(3):
            conditional = sum((masses[i][j] * x[i][coordinate]
                               for i in range(len(base))), F(0))
            require(conditional == weights[j] * dilation * y[j][coordinate],
                    "dilated conditional mean")

    target_scatter = sum((weights[i] * dot(y[i], y[i])
                          for i in range(len(base))), F(0))
    pair_loss = sum((weights[i] * weights[j]
                     * (dist2(sources[i], sources[j])
                        - dist2(targets[i], targets[j]))
                     for i, j in product(range(len(base)), repeat=2)), F(0))
    require(pair_loss == 2 * (source_scatter - target_scatter),
            "pair-loss identity")
    loss_floor = 2 * (1 - dilation ** -2) * source_scatter
    require(pair_loss >= loss_floor, "conditional Jensen loss floor")

    target_radius_squared = max(dot(point, point) for point in y)
    require(target_radius_squared <= kappa ** 2 / (4 * radius_squared),
            "centered target radius guard")
    gap = (dilation - 1) * source_scatter / (
        96 * dilation * radius_squared)
    theorem_cutoff = 4224 * dilation * radius_squared ** 2 / (
        (dilation - 1) * source_scatter)
    family_cutoff = 2816 * radius_squared ** 2 / kappa
    require(theorem_cutoff * gap == 44 * radius_squared,
            "endpoint substitution")
    require(gap < F(1, 96) and theorem_cutoff > 8 * radius_squared,
            "endpoint regime")
    require(source_scatter >= 3 * kappa
            and theorem_cutoff <= family_cutoff, "uniform family cutoff")
    require(F(9, 64) - F(1, 8) == F(1, 64), "threshold overlap")

    paired_rank = rank([[F(1), *first, *second]
                        for first, second in zip(sources, targets)]) - 1
    require(paired_rank == 6, "full paired affine rank control")
    return {
        "sites": len(base),
        "coupling_entries": len(base) ** 2,
        "paired_affine_rank": paired_rank,
        "source_covariance": [[str(value) for value in row] for row in sigma],
        "covariance_floor": str(kappa),
        "source_radius_squared": str(radius_squared),
        "source_scatter": str(source_scatter),
        "damping": str(damping),
        "minimum_kernel": str(min(map(min, kernels))),
        "pair_loss": str(pair_loss),
        "pair_loss_floor": str(loss_floor),
        "spherical_gap": str(gap),
        "theorem_variance_cutoff": str(theorem_cutoff),
        "corollary_variance_cutoff": str(family_cutoff),
        "target_radius_squared": str(target_radius_squared),
        "positive_covariance_minors": len([value for value in minors if value > 0]),
    }


def corruption_controls():
    rejected = 0
    for action in ("expanding", "failed_kernel", "wrong_inverse"):
        try:
            if action == "expanding":
                certify_family(damping=F(2))
            elif action == "failed_kernel":
                certify_family(damping=F(1))
            else:
                matrix = [[F(1), F(1), F(0)],
                          [F(0), F(1), F(0)],
                          [F(0), F(0), F(1)]]
                inverse = inverse_adjugate(matrix)
                inverse[0][0] += 1
                require(matmul(matrix, inverse)
                        == [[F(i == j) for j in range(3)] for i in range(3)],
                        "damaged inverse accepted")
        except ValueError:
            rejected += 1
        else:
            raise RuntimeError("damaged control accepted: " + action)
    return rejected


def run():
    manifest = pin_inputs()
    base = certify_family()
    transformed = certify_family(
        scale=F(3), source_shift=(5, -2, 7), target_shift=(-3, 4, 1))
    require(transformed["spherical_gap"] == base["spherical_gap"],
            "spherical gap scale invariance")
    require(F(transformed["theorem_variance_cutoff"])
            == 9 * F(base["theorem_variance_cutoff"]),
            "variance scale covariance")
    require(F(transformed["pair_loss"]) == 9 * F(base["pair_loss"]),
            "pair-loss scale covariance")
    require(transformed["minimum_kernel"] == base["minimum_kernel"],
            "coupling scale invariance")
    return {
        "status": "INDEPENDENT_DILATED_MARTINGALE_ACCEPT",
        "verdict": "accept the general theorem and covariance-damped family",
        "target_artifact": manifest["target_artifact"],
        "target_source_commit": manifest["target_source_commit"],
        "pinned_files": len(manifest["files"]),
        "custom_full_rank_family": base,
        "translated_scaled_reproduction": transformed,
        "scale_translation_controls": 4,
        "rejected_corruptions": corruption_controls(),
        "full_all_variance_majorisation_proved": False,
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
        "coupling_entries": result["custom_full_rank_family"]["coupling_entries"],
        "paired_affine_rank": result["custom_full_rank_family"]["paired_affine_rank"],
        "rejected_corruptions": result["rejected_corruptions"],
        "record_sha256": sha256(canonical.encode()).hexdigest(),
        "full_all_variance_majorisation_proved":
            result["full_all_variance_majorisation_proved"],
    }, indent=2))


if __name__ == "__main__":
    main()
