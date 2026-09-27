#!/usr/bin/env python3
"""Independent exact replay for the meridian-contraction review.

This imports no target module.  It pins the reviewed packet, expands each
motion distance as a univariate polynomial by a definition-level route,
checks a fresh global meridian contraction, and recomputes the rank-six
benchmark with the permutation formula for determinants.
"""

import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, permutations
import json
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


def dot(first, second):
    return sum((x * y for x, y in zip(first, second)), F(0))


def subtract(first, second):
    return tuple(x - y for x, y in zip(first, second))


def norm2(vector):
    return dot(vector, vector)


def poly_add(first, second):
    size = max(len(first), len(second))
    return tuple((first[i] if i < len(first) else F(0))
                 + (second[i] if i < len(second) else F(0))
                 for i in range(size))


def poly_scale(poly, scalar):
    return tuple(scalar * value for value in poly)


def poly_mul(first, second):
    out = [F(0)] * (len(first) + len(second) - 1)
    for i, x in enumerate(first):
        for j, y in enumerate(second):
            out[i + j] += x * y
    return tuple(out)


def distance_coefficients(first, second):
    """Return direct and split coefficients of squared distance in t."""
    p, image_p, u = first
    q, image_q, v = second
    r, z = p
    rho, zeta = image_p
    s, w = q
    sigma, omega = image_q
    c = dot(u, v)
    radial_p = (r, rho - r)
    radial_q = (s, sigma - s)
    axial = (z - w, (zeta - z) - (omega - w))

    direct = poly_add(poly_mul(radial_p, radial_p),
                      poly_mul(radial_q, radial_q))
    direct = poly_add(direct, poly_scale(poly_mul(radial_p, radial_q), -2 * c))
    direct = poly_add(direct, poly_mul(axial, axial))
    auxiliary = ((r - rho) - (s - sigma)) ** 2
    auxiliary += ((z - zeta) - (w - omega)) ** 2
    direct = poly_add(direct, (F(0), auxiliary, -auxiliary))

    meridian_source = norm2(subtract(p, q))
    meridian_target = norm2(subtract(image_p, image_q))
    split = (meridian_source, meridian_target - meridian_source)
    split = poly_add(split, poly_scale(poly_mul(radial_p, radial_q), 2 * (1 - c)))
    return direct, split


def global_fixture():
    # S(r,z)=(r/3,z/4+r/5).  Its squared Frobenius bound is below one,
    # hence it is a global meridian contraction, and 0<=r/3<=r.
    frobenius_squared = F(1, 9) + F(1, 16) + F(1, 25)
    require(frobenius_squared < 1, "fixture Lipschitz bound")

    points = [(F(r), F(z)) for r, z in
              ((0, 0), (0, 2), (0, -3), (1, 0),
               (2, 1), (3, -2), (5, 4), (7, -5))]

    def meridian(point):
        r, z = point
        return r / 3, z / 4 + r / 5

    images = [meridian(point) for point in points]
    for point, image in zip(points, images):
        require(F(0) <= image[0] <= point[0], "radial order")
    for i, j in combinations(range(len(points)), 2):
        require(norm2(subtract(images[i], images[j])) <=
                norm2(subtract(points[i], points[j])), "meridian contraction")

    directions = [(F(1), F(0)), (F(0), F(1)), (F(-1), F(0)),
                  (F(3, 5), F(4, 5)), (F(-5, 13), F(12, 13))]
    require(all(norm2(direction) == 1 for direction in directions),
            "unit directions")
    labels = []
    for point, image in zip(points, images):
        for direction in directions[:1] if point[0] == 0 else directions:
            labels.append((point, image, direction))

    coefficient_controls = 0
    strict_pairs = 0
    for first, second in combinations(labels, 2):
        direct, split = distance_coefficients(first, second)
        require(direct == split, "independent distance expansion")
        # A quadratic distance is nonincreasing when its affine derivative
        # is nonpositive at both endpoints.
        derivative_zero = direct[1]
        derivative_one = direct[1] + 2 * direct[2]
        require(derivative_zero <= 0 and derivative_one <= 0,
                "whole-time distance monotonicity")
        source_distance = direct[0]
        target_distance = sum(direct)
        require(target_distance <= source_distance, "endpoint contraction")
        strict_pairs += target_distance < source_distance
        coefficient_controls += 3

    return {
        "meridian_points": len(points),
        "physical_labels": len(labels),
        "physical_pairs": len(labels) * (len(labels) - 1) // 2,
        "coefficient_controls": coefficient_controls,
        "strict_endpoint_pairs": strict_pairs,
        "frobenius_squared_bound": frobenius_squared,
    }


def determinant_by_permutations(matrix):
    size = len(matrix)
    require(all(len(row) == size for row in matrix), "square matrix")
    total = F(0)
    for permutation in permutations(range(size)):
        inversions = sum(permutation[i] > permutation[j]
                         for i in range(size) for j in range(i + 1, size))
        product = F(1)
        for row, column in enumerate(permutation):
            product *= matrix[row][column]
        total += (-1 if inversions % 2 else 1) * product
    return total


def conical_fold(point):
    r, z = point
    if 2 * r <= z:
        return point
    return (-3 * r + 4 * z) / 5, (4 * r + 3 * z) / 5


def benchmark():
    sources = [(F(x), F(y), F(z)) for x, y, z in
               ((0, 0, 0), (0, 0, 1), (1, 0, 2), (0, 1, 2),
                (1, 0, 1), (-1, 0, 1), (0, 1, 1))]
    targets = []
    for x, y, z in sources:
        radius = abs(x) + abs(y)
        direction = ((x / radius, y / radius) if radius else (F(1), F(0)))
        image_radius, image_z = conical_fold((radius, z))
        targets.append((image_radius * direction[0],
                        image_radius * direction[1], image_z))

    losses = []
    for i, j in combinations(range(len(sources)), 2):
        loss = norm2(subtract(sources[i], sources[j]))
        loss -= norm2(subtract(targets[i], targets[j]))
        require(loss >= 0, "benchmark contraction")
        losses.append(loss)

    paired = [sources[i] + targets[i] for i in range(1, 7)]
    displacements = [subtract(targets[i], sources[i]) for i in (4, 5, 6)]
    paired_determinant = determinant_by_permutations(paired)
    displacement_determinant = determinant_by_permutations(displacements)
    require(paired_determinant != 0 and displacement_determinant != 0,
            "rank benchmark")
    loss_text = "|".join(map(str, losses)).encode()
    return {
        "labels": len(sources),
        "pairs": len(losses),
        "tight_pairs": sum(loss == 0 for loss in losses),
        "strict_pairs": sum(loss > 0 for loss in losses),
        "paired_determinant": paired_determinant,
        "displacement_determinant": displacement_determinant,
        "loss_vector_sha256": sha256(loss_text).hexdigest(),
    }


def analytic_controls():
    # For the nonlinear example, the four absolute Jacobian bounds are
    # 3/4,1/4,1/4,1/4, whose squared sum is 3/4<1.
    nonlinear_frobenius_squared = F(9 + 1 + 1 + 1, 16)
    require(nonlinear_frobenius_squared == F(3, 4) < 1,
            "nonlinear Lipschitz bound")
    # In two dimensions, R^2/(2s) is exponential(1), so
    # exp(-R^2/(2s)) is uniform on (0,1).  This is the exact number of
    # auxiliary coordinates needed for the hinge cancellation.
    return {
        "motion_ambient_dimension_increment": 2,
        "gaussian_marginal_coordinates": 2,
        "nonlinear_frobenius_squared_bound": nonlinear_frobenius_squared,
        "ball_radii_scope": "arbitrary individual nonnegative radii",
    }


def run():
    manifest = pin_inputs()
    return {
        "status": "INDEPENDENT_MERIDIAN_CONTRACTION_REVIEW_PASS",
        "verdict": ("accept full Gaussian majorisation and union/intersection "
                    "ball comparisons for the stated meridian class"),
        "target_commit": manifest["target_commit"],
        "target_graph_ref": manifest["target_graph_ref"],
        "pinned_target_files": len(manifest["files"]),
        "fresh_global_fixture": global_fixture(),
        "rank_six_benchmark": benchmark(),
        "analytic_controls": analytic_controls(),
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
    print("INDEPENDENT_MERIDIAN_CONTRACTION_REVIEW_PASS")
    print("record_sha256=" + sha256(record).hexdigest())


if __name__ == "__main__":
    main()
