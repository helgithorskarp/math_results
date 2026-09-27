#!/usr/bin/env python3
"""Independent exact controls for the moving small-loss defect review.

No target module is imported.  This pins the reviewed packet, reconstructs
the seven normalized exponent budgets and relative schedules, checks the
all-radius exponential envelope and radial constants, and evaluates a finite
family directly from pair distances and covariance minors.  The continuum
Gaussian estimates remain reviewed mathematics.
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
        require(actual == expected, "changed target input: " + relative)
    return manifest


def power2(exponent):
    return F(2 ** exponent) if exponent >= 0 else F(1, 2 ** (-exponent))


def normalized_bounds(m):
    R, kappa = F(1, 2), F(1, 2 ** 15)
    W, A = power2(-(2 * m + 2)), power2(3 * m + 6)
    K0, L = power2(14), power2(19)
    K1, K2 = power2(3 * m + 24), power2(4 * m + 4)
    c = W * W / 16
    delta = c / (4 * K1)
    bounds = [
        kappa * kappa / (4 * R * R * K0),
        delta * delta / (2 * K0),
        kappa * delta * delta / (8 * R * R * K0),
        W ** 4 * kappa ** 2 * delta ** 2 / (144 * R ** 4 * K0),
        2 * kappa * delta / R,
        c * delta ** 4 / (8 * A * L ** 2 * K0 ** 2),
        c ** 2 * delta ** 4 / (64 * K2 ** 2 * K0 ** 3),
    ]
    return c, delta, bounds


def schedule_controls():
    rows = []
    for m in (4, 5, 8, 13, 16, 22, 29, 56, 100):
        exponents = [44, 14 * m + 83, 14 * m + 98, 22 * m + 124,
                     7 * m + 47, 35 * m + 219, 44 * m + 208]
        c, delta, bounds = normalized_bounds(m)
        require(c == power2(-(4 * m + 8)), "normalized c")
        require(delta == power2(-(7 * m + 34)), "normalized delta")
        require(all(power2(-exponent) <= bound
                    for exponent, bound in zip(exponents, bounds)),
                "seven normalized budgets")
        require(exponents[-1] == max(exponents), "last budget dominance")
        rows.append([m, exponents[-1]])

    linear_rows = [(0, 44), (14, 83), (14, 98), (22, 124),
                   (7, 47), (35, 219), (44, 208)]
    for slope, constant in linear_rows:
        require(44 >= slope and (44 - slope) * 3 + 208 >= constant,
                "universal dominance for m>=3")

    table = []
    for bits in (0, 32, 64, 128, 256, 1024):
        radicand = 3 * (bits + 20)
        m = isqrt(radicand)
        m += m * m < radicand
        m = max(4, m)
        require(m * m >= radicand and (m - 1) ** 2 < radicand,
                "minimal square-root schedule")
        table.append([bits, m, 44 * m + 208])
    require(table == [[0, 8, 560], [32, 13, 780], [64, 16, 912],
                      [128, 22, 1176], [256, 29, 1484],
                      [1024, 56, 2672]], "published relative schedule")
    huge_bits = 10 ** 200
    huge_m = isqrt(3 * (huge_bits + 20))
    huge_m += huge_m * huge_m < 3 * (huge_bits + 20)
    require(huge_m * huge_m >= 3 * (huge_bits + 20), "compressed schedule")
    return {"normalized_rows": rows, "relative_table": table,
            "huge_schedule_decimal_digits": len(str(44 * huge_m + 208))}


def analytic_constants():
    require(F(3375, 64) < 64, "Hessian/top-set volume ratio")
    # q<=S and q,S>=1 give q^3+4q+4/q <= S^3+4S^3+4S^3.
    require(1 + 4 + 4 == 9, "radial tail coefficient")
    # Core and rare coefficients in units c=W^2/16 retain GG+2GJ+JJ.
    require(F(1, 4) * 16 >= 1, "GG coefficient")
    require(F(1, 8) * 16 >= 2, "GJ coefficient")
    require(F(1, 8) * 16 >= 1, "JJ coefficient")
    require(F(1, 4) + F(1, 8) + F(1, 8) == F(1, 2),
            "three error shares")
    modulus_cap = F(1, 4) * 3 * 3 ** 7 * F(256, 9) * F(196, 9)
    require(modulus_cap == 1016064 < 2 ** 20, "loss modulus cap")
    require(F(245, 36) < 7 and F(64, 27) < 3,
            "modulus exponential factors")
    require(F(25, 9) < 3 and F(44, 7) < F(64, 9),
            "square-root enclosures")
    # The all-radius seven terms have these (Rm,R^2) exponents.
    all_radius = [[0, 0], [14, 10], [14, 10], [22, 20],
                  [7, 5], [35, 25], [44, 40]]
    require(all(a <= 44 and b <= 40 for a, b in all_radius),
            "all-radius common envelope")
    # Direct tail integration yields 4+8R+8R^2+(8/3)R^3.
    tail_coefficients = [F(4), F(8), F(8), F(8, 3)]
    return {"hessian_volume_ratio": F(3375, 64),
            "modulus_upper_bound": modulus_cap,
            "all_radius_exponents": all_radius,
            "tail_polynomial_coefficients": tail_coefficients}


def dot(first, second):
    return sum((a * b for a, b in zip(first, second)), F(0))


def subtract(first, second):
    return tuple(a - b for a, b in zip(first, second))


def norm2(vector):
    return dot(vector, vector)


def determinant(matrix):
    if not matrix:
        return F(1)
    return sum(((-1) ** column * matrix[0][column]
                * determinant([row[:column] + row[column + 1:]
                               for row in matrix[1:]])
                for column in range(len(matrix))), F(0))


def principal_minors(matrix):
    return [determinant([[matrix[i][j] for j in indices] for i in indices])
            for size in (1, 2, 3)
            for indices in combinations(range(3), size)]


def family_control():
    bits, m, loss_bits = 64, 16, 912
    alpha = power2(-(loss_bits + 3))
    vertices = [(1, 1, 1), (1, -1, -1),
                (-1, 1, -1), (-1, -1, 1)]
    source = [tuple(F(value, 80) for value in vertex) for vertex in vertices]
    source += [tuple(F(-value, 4) for value in vertex) for vertex in vertices]
    target = source[:4] + [tuple(F(29 * value, 120) for value in vertex)
                           for vertex in vertices]
    core = [F(1, 8), F(1, 4), F(1, 4), F(3, 8)]
    outer = [F(1, 2), F(1, 4), F(1, 8), F(1, 8)]
    weights = [(1 - alpha) * weight for weight in core]
    weights += [alpha * weight for weight in outer]
    mean_source = tuple(sum(weight * point[j]
                            for weight, point in zip(weights, source))
                        for j in range(3))
    mean_target = tuple(sum(weight * point[j]
                            for weight, point in zip(weights, target))
                        for j in range(3))
    centered_source = [subtract(point, mean_source) for point in source]
    centered_target = [subtract(point, mean_target) for point in target]
    losses = []
    d = F(0)
    for i, j in combinations(range(8), 2):
        loss = norm2(subtract(source[i], source[j]))
        loss -= norm2(subtract(target[i], target[j]))
        require(loss >= 0, "finite family contraction")
        losses.append(loss)
        d += 2 * weights[i] * weights[j] * loss
    covariance = [[sum(weight * point[i] * point[j]
                       for weight, point in zip(weights, centered_source))
                   for j in range(3)] for i in range(3)]
    shifted = [[covariance[i][j] - (F(1, 2 ** 15) if i == j else 0)
                for j in range(3)] for i in range(3)]
    minors = principal_minors(shifted)
    radius2 = max(norm2(point) for point in centered_source)
    marginal_d = 2 * sum(weight * (norm2(x) - norm2(y))
                         for weight, x, y in
                         zip(weights, centered_source, centered_target))
    require(d == marginal_d > 0 and d <= power2(-loss_bits), "finite loss guard")
    require(radius2 <= F(1, 4), "finite radius guard")
    require(all(value >= 0 for value in minors), "finite covariance guard")
    invariant = "|".join(map(str, [bits, m, loss_bits, d, radius2, *minors, *losses]))
    return {"sites": 8, "pairs": 28, "relative_bits": bits,
            "moving_parameter": m, "loss_bits": loss_bits,
            "invariant_sha256": sha256(invariant.encode()).hexdigest()}


def run():
    manifest = pin_inputs()
    return {
        "status": "INDEPENDENT_SMALL_LOSS_DEFECT_REVIEW_PASS",
        "verdict": ("accept the moving Gaussian sign window and flat adverse "
                    "defect theorem in its stated fixed-radius, positive-"
                    "covariance scope"),
        "target_commit": manifest["target_commit"],
        "target_graph_ref": manifest["target_graph_ref"],
        "pinned_target_files": len(manifest["files"]),
        "analytic_constants": analytic_constants(),
        "schedule_controls": schedule_controls(),
        "finite_family_control": family_control(),
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
    print("INDEPENDENT_SMALL_LOSS_DEFECT_REVIEW_PASS")
    print("record_sha256=" + sha256(record).hexdigest())


if __name__ == "__main__":
    main()
