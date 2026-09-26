#!/usr/bin/env python3
"""Exact finite controls for PROOF.md; not a proof of its analytic theorem."""

import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


def sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def mean(points, weights):
    return tuple(sum((p * x[k] for x, p in zip(points, weights)), F(0))
                 for k in range(len(points[0])))


def center(points, weights):
    m = mean(points, weights)
    return [sub(x, m) for x in points]


def cross(xs, ys, weights):
    n = len(xs[0])
    return [[sum((p * x[i] * y[j] for x, y, p in zip(xs, ys, weights)), F(0))
             for j in range(n)] for i in range(n)]


def trace_product(a, b):
    return sum((a[i][j] * b[j][i]
                for i in range(len(a)) for j in range(len(a))), F(0))


def principal_psd_3(a):
    require(len(a) == 3 and all(len(row) == 3 for row in a), "matrix size")
    require(all(a[i][j] == a[j][i] for i in range(3) for j in range(3)),
            "matrix is not symmetric")
    require(all(a[i][i] >= 0 for i in range(3)), "negative principal entry")
    require(all(a[i][i] * a[j][j] - a[i][j] ** 2 >= 0
                for i in range(3) for j in range(i + 1, 3)),
            "negative order-two principal minor")
    det = (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
           - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
           + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))
    require(det >= 0, "negative determinant")


def fixture(name, raw_x, raw_y, weights, radius, kappa):
    require(len(raw_x) == len(raw_y) == len(weights), "label count mismatch")
    require(sum(weights) == 1 and min(weights) > 0, "invalid weights")
    xs, ys = center(raw_x, weights), center(raw_y, weights)
    hs = [sub(y, x) for x, y in zip(xs, ys)]
    count = len(xs)
    require(all(dot(x, x) <= radius ** 2 for x in xs), "radius too small")
    xx = cross(xs, xs, weights)
    principal_psd_3([[xx[i][j] - (kappa if i == j else 0)
                      for j in range(3)] for i in range(3)])
    principal_psd_3(cross(xs, ys, weights))
    # The L1 norm supplies a rational upper bound for each Euclidean norm.
    delta = max(sum(map(abs, h)) for h in hs)
    loss = [[dot(sub(xs[i], xs[j]), sub(xs[i], xs[j]))
             - dot(sub(ys[i], ys[j]), sub(ys[i], ys[j]))
             for j in range(count)] for i in range(count)]
    require(all(0 <= d <= 8 * radius * delta for row in loss for d in row),
            "contraction or displacement bound fails")
    pair = lambda table: sum((weights[i] * weights[j] * table[i][j]
                              for i in range(count) for j in range(count)), F(0))
    d = pair(loss)
    d2 = pair([[value ** 2 for value in row] for row in loss])
    m = sum((p * dot(h, h) for p, h in zip(weights, hs)), F(0))
    rows = [sum((p * z for p, z in zip(weights, row)), F(0)) for row in loss]
    gram = [[dot(xs[i], xs[j]) - dot(ys[i], ys[j])
             for j in range(count)] for i in range(count)]
    require(all(gram[i][j] == -(loss[i][j] - rows[i] - rows[j] + d) / 2
                for i in range(count) for j in range(count)), "double centering")
    h2 = pair([[value ** 2 for value in row] for row in gram])
    us, vs = [add(x, y) for x, y in zip(xs, ys)], [sub(x, y) for x, y in zip(xs, ys)]
    uu, vv, uv = cross(us, us, weights), cross(vs, vs, weights), cross(us, vs, weights)
    rhs = (trace_product(uu, vv) + trace_product(uv, uv)) / 2
    require(h2 == rhs, "Gram expansion")
    require(kappa * m / 2 <= h2 <= d2 / 4, "Gram bounds")
    require(m <= d2 / (2 * kappa) <= 4 * radius * delta * d / kappa,
            "local Procrustes bounds")
    strain = [[dot(sub(xs[i], xs[j]), sub(hs[i], hs[j]))
               for j in range(count)] for i in range(count)]
    require(all(-2 * strain[i][j] == loss[i][j]
                + dot(sub(hs[i], hs[j]), sub(hs[i], hs[j]))
                for i in range(count) for j in range(count)), "strain identity")
    require(-2 * pair(strain) == d + 2 * m, "averaged strain identity")
    # Arbitrary rational posterior weights independently check the covariance
    # normalization in (15), without using Gaussian floating-point values.
    posterior = [F(i + 1, count * (count + 1) // 2) for i in range(count)]
    xm, hm = mean(xs, posterior), mean(hs, posterior)
    covariance = sum((p * dot(sub(x, xm), sub(h, hm))
                      for x, h, p in zip(xs, hs, posterior)), F(0))
    posterior_pair = sum((posterior[i] * posterior[j] * strain[i][j]
                          for i in range(count) for j in range(count)), F(0))
    require(covariance == posterior_pair / 2, "posterior covariance factor")
    return {"name": name, "labels": count, "pair_loss": str(d),
            "mean_square_error": str(m), "gram_norm_squared": str(h2),
            "aligned_displacement_upper_bound": str(delta)}


def build_report():
    axes = [tuple(F(sign if j == axis else 0) for j in range(3))
            for axis in range(3) for sign in (-1, 1)]
    weights = [F(1, 6)] * 6
    diagonal = tuple(map(F, (F(1, 2), F(2, 3), F(3, 4))))
    scaled = [tuple(a * b for a, b in zip(x, diagonal)) for x in axes]
    folded = [(abs(x[0]), x[1], x[2]) for x in axes]
    cube = [tuple(map(F, x)) for x in product((-1, 1), repeat=3)]
    cube_target = [(abs(x[0]), x[1] / 2, x[2] / 3) for x in cube]
    near_target = [tuple(x[i] * (1 - F(i + 1, 10**12)) for i in range(3)) for x in axes]
    ellipsoid = [tuple(x[i] * (i + 1) for i in range(3)) for x in axes]
    gram_cross = [[F(1, 12) if i == j else (F(1, 48) if abs(i-j) == 1 else F(0))
                   for j in range(3)] for i in range(3)]
    linear = [[gram_cross[i][j] * F(3, (j + 1)**2) for j in range(3)] for i in range(3)]
    mixed_target = [tuple(dot(row, x) for row in linear) for x in ellipsoid]
    cases = [fixture("identity", axes, axes, weights, F(1), F(1, 3)),
             fixture("anisotropic", axes, scaled, weights, F(1), F(1, 3)),
             fixture("fold_with_centering", axes, folded, weights, F(1), F(1, 3)),
             fixture("cube_fold_and_scale", cube, cube_target,
                     [F(1, 8)] * 8, F(2), F(1)),
             fixture("near_identity", axes, near_target, weights, F(1), F(1, 3)),
             fixture("noncommuting_gram_matrices", ellipsoid, mixed_target,
                     weights, F(3), F(1, 3))]
    # At t=1, r=1, R=1, q=exp(-18)>3^(-18). This finite fixture
    # satisfies the theorem's sufficient proximity condition nontrivially.
    require(F(cases[4]["aligned_displacement_upper_bound"]) < F(1, 48 * 3**18),
            "near-identity fixture must satisfy the signed sufficient bound")
    # A rigid rotation has D=0 but nonzero unaligned M. The PSD alignment
    # premise of (11) cannot be dropped.
    rotated = [(-x[1], x[0], x[2]) for x in axes]
    unaligned_m = sum((p * dot(sub(y, x), sub(y, x))
                       for x, y, p in zip(axes, rotated, weights)), F(0))
    require(unaligned_m > 0, "rotation must have nonzero unaligned error")
    require(all(dot(sub(x, z), sub(x, z)) == dot(sub(y, w), sub(y, w))
                for x, y in zip(axes, rotated) for z, w in zip(axes, rotated)),
            "negative control must be isometric")

    # Rational enclosures use the analytic facts 8/3<e<3 and 3<pi<22/7.
    # Their application to Gaussian integrals is proved in Section 6.
    tail = 11 * F(3, 8) ** 50
    moment_tail = 1031 * F(3, 8) ** 50
    radius, kappa, delta = F(1, 100), F(1, 2 * 10**6), F(1, 10**10)
    exponent = (1 + radius) ** 2 / 2 + (1 + 3 * radius) ** 2
    q_lower = F(1, 9)
    loss_lower = F(3, 10**14)
    margin_lower = loss_lower / 576
    require(tail < F(1, 10**19) < margin_lower, "core margin must exceed tail")
    require(moment_tail < 1, "conditional covariance bound")
    require(exponent == F(31419, 20000) and exponent < 2, "exponent bound")
    require(delta < kappa * q_lower / (16 * radius), "core proximity condition")
    require(F(44, 7) ** 3 < 256, "Gaussian peak lower bound")
    c = 1 - F(1, 10**8)
    require(2 * (1 - c**2) * 3 * kappa > loss_lower, "pair-loss reserve")
    # Exact bookkeeping in (24), using symbolic coefficients q,kappa,R,delta
    # specialized to rational values independently of the example above.
    q, k, r, delta_control = F(2, 5), F(3, 7), F(5, 4), F(1, 10000)
    require(q - 2 * (4 * r * delta_control / k) == q - 8 * r * delta_control / k,
            "profile absorption coefficient")
    require(q - 8 * r * (k * q / (16 * r)) / k == q / 2,
            "half-margin coefficient")
    return {"status": "CONTACT_NEAR_ISOMETRY_EXACT_CONTROLS_PASS",
            "arithmetic": "fractions.Fraction; no floating point",
            "fixtures": cases,
            "rotation_negative_control": {"pair_loss": "0", "unaligned_error": str(unaligned_m)},
            "auxiliary_gaussian_core": {"exponent": str(exponent),
                "tail_upper_bound": str(tail), "moment_tail_upper_bound": str(moment_tail),
                "conditional_kappa": str(kappa), "aligned_delta": str(delta),
                "q_lower_bound": str(q_lower), "pair_loss_lower_bound": str(loss_lower),
                "core_margin_lower_bound": str(margin_lower),
                "profile_gap_lower_bound": str(margin_lower - tail)},
            "unrestricted_contact_sign_verified": False,
            "analytic_theorem_formalized": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--expected", type=Path, default=Path(__file__).with_name("EXPECTED.json"))
    args = parser.parse_args()
    report = build_report()
    if args.check:
        expected = json.loads(args.expected.read_text(encoding="utf-8"))
        require(report == expected, "expected report differs from exact recomputation")
        print(report["status"])
    else:
        print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
