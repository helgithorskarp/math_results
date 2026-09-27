#!/usr/bin/env python3
"""Independent exact controls for the affine-slice contraction theorem.

No author module is imported.  The controls use a fresh triangular-prism
fixture with a different anisotropic affine family and axial fold, exact
moving-frame tangent identities, and a finite exact model of the sampled
density tail transfer.  The continuum proof and ODE existence remain written
mathematics rather than conclusions inferred from the finite fixture.
"""

import argparse
import copy
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
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


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matmul(left, right):
    require(left and right and len(left[0]) == len(right), "matrix shape")
    return [[sum(left[i][k] * right[k][j] for k in range(len(right)))
             for j in range(len(right[0]))] for i in range(len(left))]


def madd(left, right, scale=F(1)):
    require(len(left) == len(right) and len(left[0]) == len(right[0]),
            "matrix addition shape")
    return [[left[i][j] + scale * right[i][j]
             for j in range(len(left[0]))] for i in range(len(left))]


def mscale(value, matrix):
    return [[value * entry for entry in row] for row in matrix]


def mv(matrix, vector):
    return [sum(entry * value for entry, value in zip(row, vector))
            for row in matrix]


def identity(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def dot(left, right):
    return sum(a * b for a, b in zip(left, right))


def norm2(vector):
    return dot(vector, vector)


def vadd(left, right, scale=F(1)):
    return [left[i] + scale * right[i] for i in range(len(left))]


def inverse2(matrix):
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    require(determinant != 0, "singular 2 by 2 matrix")
    return [[matrix[1][1] / determinant, -matrix[0][1] / determinant],
            [-matrix[1][0] / determinant, matrix[0][0] / determinant]]


def diagonal(a, b):
    return [[a, F(0)], [F(0), b]]


def rotation(parameter):
    denominator = 1 + parameter * parameter
    return [[(1 - parameter * parameter) / denominator,
             -2 * parameter / denominator],
            [2 * parameter / denominator,
             (1 - parameter * parameter) / denominator]]


def block_rows(top, bottom):
    return [*top, *bottom]


def frame_controls():
    # A fresh rational point of the Stiefel bundle.  The two endpoint frames
    # and source frame are all different, avoiding a diagonal special case.
    q, r, wrot = rotation(F(1, 2)), rotation(F(1, 3)), rotation(F(2, 5))
    A = matmul(matmul(q, diagonal(F(3, 5), F(5, 13))), wrot)
    B = matmul(matmul(r, diagonal(F(4, 5), F(12, 13))), wrot)
    V = block_rows(A, B)
    D = madd(identity(2), matmul(transpose(A), A), F(-1))
    P = madd(identity(2), matmul(A, transpose(A)), F(-1))
    require(matmul(transpose(B), B) == D, "frame completion")
    require(matmul(transpose(V), V) == identity(2), "Stiefel frame")

    Ap = [[F(1, 37), F(-2, 41)], [F(3, 43), F(1, 47)]]
    bp = [F(2, 53), F(-3, 59)]
    BinvT = inverse2(transpose(B))
    Bp = mscale(F(-1), matmul(matmul(BinvT, transpose(A)), Ap))
    dp = mscale(F(-1), [mv(matmul(BinvT, transpose(A)), bp)])[0]
    Vp = block_rows(Ap, Bp)
    ep = [*bp, *dp]
    zero22 = [[F(0), F(0)], [F(0), F(0)]]
    require(madd(matmul(transpose(Bp), B),
                 matmul(transpose(B), Bp))
            == mscale(F(-1), madd(matmul(transpose(Ap), A),
                                  matmul(transpose(A), Ap))),
            "ODE Gram invariant")
    require(matmul(transpose(V), Vp) == zero22,
            "horizontal frame velocity")
    require(mv(transpose(V), ep) == [F(0), F(0)],
            "horizontal translation velocity")

    Pinv = inverse2(P)
    speed_checks = 0
    for u in ([F(0), F(0)], [F(1, 2), F(-1, 3)],
              [F(-2, 5), F(3, 7)], [F(5, 11), F(1, 13)]):
        little_w = vadd(mv(Ap, u), bp)
        Eprime = vadd(mv(Vp, u), ep)
        require(mv(transpose(V), Eprime) == [F(0), F(0)],
                "point velocity normality")
        require(norm2(Eprime) == dot(little_w, mv(Pinv, little_w)),
                "normal speed identity")
        speed_checks += 1

    # Independent completion-of-square check, with nontrivial eta.
    xi, eta, hp = [F(2, 3), F(-1, 4)], F(5, 7), F(1, 3)
    little_w = vadd(mv(Ap, [F(2, 5), F(-3, 8)]), bp)
    displacement = mv(inverse2(D), mv(transpose(A), little_w))
    shifted = vadd(xi, displacement, -eta)
    lhs = (norm2(xi) + eta * eta
           - norm2(vadd(mv(A, xi), little_w, eta))
           - hp * hp * eta * eta)
    rhs = (dot(shifted, mv(D, shifted))
           + (1 - hp * hp - dot(little_w, mv(Pinv, little_w)))
           * eta * eta)
    require(lhs == rhs, "Schur completion identity")

    wrong_Bp = mscale(F(-1), matmul(matmul(inverse2(B), transpose(A)), Ap))
    require(matmul(transpose(V), block_rows(Ap, wrong_Bp)) != zero22,
            "inverse-transpose negative control")
    require(mv(transpose(V), [*bp, F(0), F(0)]) != [F(0), F(0)],
            "translation negative control")
    return {
        "rational_frame_rows": len(V),
        "normal_speed_checks": speed_checks,
        "gram_invariant": True,
        "schur_identity": True,
        "wrong_inverse_rejected": True,
        "omitted_translation_rejected": True,
    }


def transverse(point):
    u, v, z = point
    return [((F(1, 5) + z / 20) * u + (z / 30) * v + z * z / 50),
            ((-z / 40) * u + (F(1, 6) + z / 25) * v + z / 30)]


def target_height(z):
    return F(3, 5) * z if z <= 0 else F(-5, 13) * z


def unfolded_height(z):
    return F(3, 5) * z if z <= 0 else F(5, 13) * z


def split_lengths(z, w):
    low, high = sorted((z, w))
    negative = max(F(0), min(high, F(0)) - low)
    positive = max(F(0), high - max(low, F(0)))
    require(negative + positive == high - low, "height partition")
    return negative, positive


def triangular_prism_controls():
    # K=conv{(-1,-1),(1,-1),(0,1)}.  The displayed coordinate bounds
    # give a global Jacobian Frobenius bound, independently of sampling.
    jacobian_bound = (F(1, 4) ** 2 + F(1, 30) ** 2
                      + F(1, 40) ** 2 + F(31, 150) ** 2
                      + F(37, 300) ** 2 + F(59, 600) ** 2
                      + F(3, 5) ** 2)
    require(jacobian_bound == F(88529, 180000) < 1,
            "global derivative bound")
    section_points = [
        [F(-1), F(-1)], [F(1), F(-1)], [F(0), F(1)],
        [F(0), F(-1)], [F(1, 2), F(0)], [F(-1, 2), F(0)],
        [F(0), F(0)],
    ]
    heights = [F(-1), F(-1, 2), F(0), F(1, 2), F(1)]
    labels = [[u, v, z] for u, v in section_points for z in heights]
    nodes = [
        [F(0), F(1), F(1)],
        [F(33, 50), F(19, 25), F(43, 65)],
        [F(125, 242), F(9, 11), F(107, 143)],
        [F(231, 256), F(13, 20), F(25, 52)],
        [F(1), F(3, 5), F(5, 13)],
    ]
    for t, qnegative, qpositive in nodes:
        require(qnegative ** 2 == 1 - t + t * F(9, 25),
                "negative-height clock")
        require(qpositive ** 2 == 1 - t + t * F(25, 169),
                "positive-height clock")

    pair_count = phase_controls = fold_controls = 0
    minimum_bridge_slack = None
    maximum_raw_derivative = None
    fold_nodes = [[r * r / (1 + r * r), r / (1 + r * r)]
                  for r in (F(0), F(1, 3), F(2, 3), F(3, 2), F(3))]
    fold_nodes.append([F(1), F(0)])
    for x, y in combinations(labels, 2):
        duv2 = norm2(vadd(x[:2], y[:2], F(-1)))
        newuv2 = norm2(vadd(transverse(x), transverse(y), F(-1)))
        dz = x[2] - y[2]
        dh = target_height(x[2]) - target_height(y[2])
        require(newuv2 + dh * dh <= duv2 + dz * dz,
                "fixture endpoint contraction")
        negative, positive = split_lengths(x[2], y[2])
        omega_integral = F(4, 5) * negative + F(12, 13) * positive
        gain = newuv2 - duv2
        bridge_slack = omega_integral ** 2 - gain
        require(bridge_slack >= 0, "transverse bridge")
        minimum_bridge_slack = (bridge_slack if minimum_bridge_slack is None
                                else min(minimum_bridge_slack, bridge_slack))

        first_endpoint = (newuv2
                          + (unfolded_height(x[2])
                             - unfolded_height(y[2])) ** 2)
        for t, qnegative, qpositive in nodes:
            length = negative * qnegative + positive * qpositive
            cost = (negative * F(16, 25) / qnegative
                    + positive * F(144, 169) / qpositive)
            require(length * cost >= omega_integral ** 2 >= gain,
                    "Cauchy bridge chain")
            derivative = gain - length * cost
            require(derivative <= 0, "first-phase derivative")
            distance = ((1 - t) * duv2 + t * newuv2 + length ** 2)
            require(first_endpoint <= distance <= duv2 + dz * dz,
                    "first-phase distance interval")
            phase_controls += 1

        hx, hy = unfolded_height(x[2]), unfolded_height(y[2])
        gx, gy = target_height(x[2]), target_height(y[2])
        require((gx - gy) ** 2 <= (hx - hy) ** 2, "fold Lipschitz")
        for s, root in fold_nodes:
            require(root * root == s * (1 - s), "fold clock")
            first = (1 - s) * (hx - hy) + s * (gx - gy)
            second = root * ((hx - gx) - (hy - gy))
            require(first * first + second * second
                    == (1 - s) * (hx - hy) ** 2
                    + s * (gx - gy) ** 2, "leapfrog identity")
            fold_controls += 1

        raw_derivative = gain + 2 * dh * (dh - dz)
        maximum_raw_derivative = (raw_derivative
                                  if maximum_raw_derivative is None
                                  else max(maximum_raw_derivative,
                                           raw_derivative))
        pair_count += 1
    require(maximum_raw_derivative > 0,
            "raw linear height clock negative control")
    return {
        "global_jacobian_frobenius_bound": str(jacobian_bound),
        "global_contraction_margin": str(1 - jacobian_bound),
        "labels": len(labels),
        "unordered_pairs": pair_count,
        "exact_first_phase_controls": phase_controls,
        "exact_fold_controls": fold_controls,
        "minimum_bridge_slack": str(minimum_bridge_slack),
        "largest_raw_clock_derivative": str(maximum_raw_derivative),
        "clock_nodes": [[str(value) for value in node] for node in nodes],
    }


def sampled_density_controls():
    # A finite piecewise-constant density model checks the exact conditioning
    # algebra in (19): X chooses cell j with mass volume_j*density_j and an
    # independent Z~Uniform[0,1].  This does not numerically approximate a
    # Gaussian; the analytic review proves gamma_2(Y)/gamma_2(0) is uniform.
    densities = [F(1, 5), F(1, 2), F(4, 3), F(7, 4)]
    volumes = [F(1), F(1, 2), F(3, 20), F(1, 5)]
    normalization = sum(a * b for a, b in zip(densities, volumes))
    volumes = [volume / normalization for volume in volumes]
    require(sum(a * b for a, b in zip(densities, volumes)) == 1,
            "density normalization")
    thresholds = [F(0), F(1, 7), F(2, 5), F(1), F(3, 2), F(2)]
    for threshold in thresholds:
        sampled_tail = sum(
            density * volume
            * (max(F(0), 1 - threshold / density) if density else 0)
            for density, volume in zip(densities, volumes))
        hinge = sum(volume * max(F(0), density - threshold)
                    for density, volume in zip(densities, volumes))
        require(sampled_tail == hinge, "sampled tail equals hinge")
    return {
        "piecewise_constant_cells": len(densities),
        "thresholds": len(thresholds),
        "tail_identity_exact": True,
    }


def corruption_controls(record):
    def validate(item):
        bound = F(item["global_jacobian_frobenius_bound"])
        margin = F(item["global_contraction_margin"])
        require(bound + margin == 1 and bound < 1, "global bound record")
        require(F(item["largest_raw_clock_derivative"]) > 0,
                "raw clock control")

    validate(record)
    damaged = []
    item = copy.deepcopy(record)
    item["global_contraction_margin"] = "0"
    damaged.append(item)
    item = copy.deepcopy(record)
    item["global_jacobian_frobenius_bound"] = "2"
    damaged.append(item)
    item = copy.deepcopy(record)
    item["largest_raw_clock_derivative"] = "0"
    damaged.append(item)
    rejected = 0
    for item in damaged:
        try:
            validate(item)
        except ValueError:
            rejected += 1
        else:
            raise RuntimeError("damaged record accepted")
    return rejected


def run():
    manifest = pin_inputs()
    prism = triangular_prism_controls()
    return {
        "status": "INDEPENDENT_AFFINE_SLICE_ACCEPT",
        "verdict": "accept the stated affine-slice prism contraction theorem",
        "target_artifact": manifest["target_artifact"],
        "target_proof_commit": manifest["target_proof_commit"],
        "target_publishing_commit": manifest["target_publishing_commit"],
        "pinned_files": len(manifest["files"]),
        "frame_controls": frame_controls(),
        "triangular_prism_controls": prism,
        "sampled_density_controls": sampled_density_controls(),
        "rejected_corruptions": corruption_controls(prism),
        "all_variances_in_stated_map_class": True,
        "unrestricted_dimension_three_proved": False,
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
        "fixture_pairs": result["triangular_prism_controls"]["unordered_pairs"],
        "phase_controls": result["triangular_prism_controls"]["exact_first_phase_controls"],
        "fold_controls": result["triangular_prism_controls"]["exact_fold_controls"],
        "rejected_corruptions": result["rejected_corruptions"],
        "record_sha256": sha256(canonical.encode()).hexdigest(),
        "unrestricted_dimension_three_proved": result["unrestricted_dimension_three_proved"],
    }, indent=2))


if __name__ == "__main__":
    main()

