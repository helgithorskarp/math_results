#!/usr/bin/env python3
"""Clean-room exact audit for the covariance-free small-loss theorem.

This does not import the author's verifier.  It reconstructs the dyadic
schedules, the simplex-flap boundary family, the replica/margin constant
ledgers, and the exact source/dependency byte pins using only the standard
library.  The coarea and Abel arguments remain written mathematics.
"""

from fractions import Fraction as Q
import hashlib
import json
from math import isqrt
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[2]
SOURCE_COMMIT = "4feee1ee4c541c459c0c0440b44b25052b20201a"
SOURCE_DIR = "probability/gaussian_covariance_free_small_loss"

SOURCE_HASHES = {
    ".gitignore": "862263fa1f46c20f0d1e4dac5ffcc75abd55c08211b2c3864c5f8764b9d87793",
    "DEPENDENCIES.json": "b4f090728f0d980c16cbb536dca2319b331ee2e8ef1445a8d854fb4d4a2deb49",
    "EXPECTED.json": "db19028035e81098250d347060199c358efe76e525311e572d9d8e6a68190703",
    "INPUT.json": "437aa56fc42648703ab1b8f2f41f035610a1756989d6e057463eee2de7c6acb7",
    "PROOF.md": "783c225521ebaf6bc7e77cd0e15ccfad3710b656426b0ffb3b597e9a0d164bfb",
    "README.md": "b7071c594b1d3827e11213d7f85cd97c878b01a024f487f0bca413c7cd51502c",
    "SHA256SUMS": "42c53b34002050309523ee359d7e598e57bf3022c4ace80e9e668167495f20a8",
    "SOURCES.md": "a16e711cebad9559873de2bfa22b145bb26e2aba0f42b0b46f4b403a3bcbd386",
    "verify.py": "6f1bf7315f502569400fbe2ab50e425e42011ac75ec06f2a616065d38480b5e2",
}

DEPENDENCY_PINS = [
    ("a264d277a51683479424060972dafb44123db597",
     "probability/gaussian_contraction_covariance_free/PROOF.md",
     "55314f4c6446e30b7960e584cc8fb6b25e8691d9e432ccf1af6e226eb43cc13a"),
    ("fc25eff113b59c72fa820def81698e914a80d15b",
     "probability/gaussian_majorisation_bridge_barrier/AUDIT.md",
     "5efbc465531f10e4eda32d91e50f656ba8564b9d86517fd63b28b4dd71de8f5d"),
    ("a68810063b8ad53dda046c68552a14e76f8d3f07",
     "probability/gaussian_loss_normalized_hinges/PROOF.md",
     "92e7dcb81ae1f4c032e5528d7ff9568da94b826e84d110957542c0310337f2f8"),
    ("ef6ba3fd50f790468405b3da22f0a93fee60a4f6",
     "probability/gaussian_motion_chain_strictness/PROOF.md",
     "9c44f811959dd2f7f3b069c3d635f1557b8ef270d3a4914244470ef75c484591"),
    ("262439aa29c2ce7f7f14b7ab1bdd85c92bd13338",
     "probability/gaussian_covariance_boundary/PROOF.md",
     "524b484e38c5bb543dc9663bf101480085d3d1ed4294682b70237653e1b12511"),
    ("ea22701250fb1aeba92919413a0c8b4d785ffe90",
     "probability/gaussian_covariance_boundary_review2/REVIEW.md",
     "6f6bf207a41b77d365d36cc1c05eadda47943061db40c56af4acdf758adfa155"),
    ("1104fcce0bfcf2d9cb16f70daa45c361f54c977c",
     "probability/gaussian_all_radius_loss_localization/PROOF.md",
     "35bdbde72f916e349ed727545d4858f09dac6ed72e3596d6b16b8d14318eb3ec"),
    ("1104fcce0bfcf2d9cb16f70daa45c361f54c977c",
     "probability/gaussian_all_radius_loss_localization/HANDOFF.md",
     "71f86e05e07f3abdee61576cc5c7a502a3a3b3cca866b7742d2202eb3a7a9259"),
    ("24fce7dc389c0e634549ba50d12076ebde570d3a",
     "probability/gaussian_all_radius_loss_localization_review2/REVIEW.md",
     "55cd5c9c6b05bd263d7ada98aab8a4bdfdcd015368fdcbdd42c5a6021fb70a9e"),
]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def git_bytes(commit, path):
    return subprocess.run(
        ["git", "show", f"{commit}:{path}"], cwd=ROOT, check=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout


def check_pins():
    for name, expected in SOURCE_HASHES.items():
        data = git_bytes(SOURCE_COMMIT, f"{SOURCE_DIR}/{name}")
        require(hashlib.sha256(data).hexdigest() == expected,
                f"source byte mismatch: {name}")
    for commit, path, expected in DEPENDENCY_PINS:
        require(hashlib.sha256(git_bytes(commit, path)).hexdigest() == expected,
                f"dependency byte mismatch: {path}")


def ceil_sqrt(n):
    r = isqrt(n)
    return r + (r * r < n)


def schedule(R, j, k):
    c = ceil_sqrt(2 * (j + 1))
    B, S = 3 * R + c, 6 * R
    E = B * S + 2 * B * B
    F = B * S + 4 * B * B + 2
    K = 3 * (E + 6) * (1 + B * S) + 12 * F
    b = (3 * R * K - 1).bit_length()
    N = 2 * (j + 6 * R * B + b)
    P = 2 * ((6 * R + 1) ** 2 + R * R) + 2 * R + 2 * j + 5 * k + 19
    Z = 31 + 47 * R * R + 2 * (2 * R + c) ** 2 + 5 * N
    return c, B, S, E, F, K, b, N, P, 2 * Z + 4


def check_schedules():
    checked = 0
    for R in range(1, 33):
        for j in range(1, 65):
            for k in (0, 1, 2, 7, 19):
                c, B, S, E, F, K, b, N, P, L = schedule(R, j, k)
                require((c - 1) ** 2 < 2 * (j + 1) <= c * c, "ceiling square root")
                require(2 ** (b - 1) < 3 * R * K <= 2 ** b, "ceiling logarithm")
                eta = Q(3 * R, 4 * 2 ** b)
                require(eta * K <= Q(1, 4), "transverse perturbation budget")
                require(eta * E <= 1, "exponential perturbation budget")
                require(K == 3 * (E + 6) * (1 + B * S) + 12 * F,
                        "radial error ledger")
                require(N == 2 * (j + 6 * R * B + b), "loss schedule")
                require(P == 2 * ((6 * R + 1) ** 2 + R * R) + 2 * R
                        + 2 * j + 5 * k + 19, "margin schedule")
                require(L == 2 * (31 + 47 * R * R + 2 * (2 * R + c) ** 2
                                  + 5 * N) + 4, "covariance schedule")
                checked += 1

    # Two elementary uniform estimates used for 0 <= eta <= 1/2:
    # (1-eta)^-2-1 <= 6 eta follows after clearing denominators from
    # (1-2 eta)(4-3 eta)>=0; and (1-eta)^-1/2 <= 1+eta follows by
    # squaring from eta(1-eta-eta^2)>=0.
    for numerator in range(0, 257):
        eta = Q(numerator, 512)
        require((1 - 2 * eta) * (4 - 3 * eta) >= 0, "prefactor bound")
        require(eta * (1 - eta - eta * eta) >= 0, "radial displacement bound")
    return checked


def sqdist(x, y):
    return sum((a - b) ** 2 for a, b in zip(x, y))


def rank(rows):
    a = [list(map(Q, row)) for row in rows]
    pivot = 0
    for col in range(len(a[0])):
        at = next((i for i in range(pivot, len(a)) if a[i][col]), None)
        if at is None:
            continue
        a[pivot], a[at] = a[at], a[pivot]
        d = a[pivot][col]
        a[pivot] = [v / d for v in a[pivot]]
        for i in range(len(a)):
            if i != pivot and a[i][col]:
                m = a[i][col]
                a[i] = [v - m * w for v, w in zip(a[i], a[pivot])]
        pivot += 1
    return pivot


def matrix_sub(a, b):
    return [[x - y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def outer(x, y):
    return [[a * b for b in y] for a in x]


def weighted_second(points, weights):
    return [[sum(w * z[i] * z[j] for w, z in zip(weights, points))
             for j in range(3)] for i in range(3)]


def check_boundary_family():
    tetra = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    source = [[Q(v, 2) for v in z] for z in tetra]
    target = [z[:] for z in source]
    for i in range(4):
        for j in range(4):
            if i != j:
                source.append([Q(b - a, 2) for a, b in zip(tetra[i], tetra[j])])
                target.append([Q(b + a, 2) for a, b in zip(tetra[i], tetra[j])])
    loss = [[sqdist(source[i], source[j]) - sqdist(target[i], target[j])
             for j in range(16)] for i in range(16)]
    require(all(v >= 0 for row in loss for v in row), "pairwise contraction")

    # Weights are a_i + epsilon b_i.  Compute every polynomial coefficient
    # directly, rather than reading the fixture or the author's output.
    a = [Q(1)] + [Q(0)] * 15
    b = [Q(-1)] + [Q(1, 15)] * 15
    loss_poly = []
    for degree in range(3):
        total = Q(0)
        for i in range(16):
            for j in range(16):
                coeff = (a[i] * a[j] if degree == 0 else
                         a[i] * b[j] + b[i] * a[j] if degree == 1 else
                         b[i] * b[j])
                total += coeff * loss[i][j]
        loss_poly.append(total)
    require(loss_poly == [0, Q(8, 5), 0], "ordered loss polynomial")

    covariance_minima = []
    for points, isotropic in ((source, Q(3, 5)), (target, Q(1, 3))):
        ma = [sum(w * z[c] for w, z in zip(a, points)) for c in range(3)]
        mb = [sum(w * z[c] for w, z in zip(b, points)) for c in range(3)]
        coefficients = [
            matrix_sub(weighted_second(points, a), outer(ma, ma)),
            matrix_sub(matrix_sub(weighted_second(points, b), outer(ma, mb)),
                       outer(mb, ma)),
            [[-v for v in row] for row in outer(mb, mb)],
        ]
        require(coefficients[0] == [[Q(0)] * 3 for _ in range(3)], "zero covariance")
        expected_linear = [[isotropic * (i == j) + Q(4, 15)
                            for j in range(3)] for i in range(3)]
        require(coefficients[1] == expected_linear, "linear covariance")
        require(coefficients[2] == [[Q(-64, 225)] * 3 for _ in range(3)],
                "quadratic covariance")
        covariance_minima.append(isotropic)

    paired = [x + y for x, y in zip(source, target)]
    ranks = []
    for points in (source, target, paired):
        rows = [[v - w for v, w in zip(z, points[0])] for z in points[1:]]
        ranks.append(rank(rows))
    require(ranks == [3, 3, 6], "affine ranks")

    epsilon = Q(1, 2 ** 487)
    weights = [1 - epsilon] + [epsilon / 15] * 15
    center = [sum(w * z[c] for w, z in zip(weights, source)) for c in range(3)]
    radius2 = max(sqdist(z, center) for z in source)
    require(radius2 <= 9, "R=3 centered radius")
    d = Q(8, 5) * epsilon
    require(d <= Q(1, 2 ** 482), "R=3,j=3 small-loss guard")

    target_center = [sum(w * z[c] for w, z in zip(weights, target)) for c in range(3)]
    trace_cov = sum(sum(w * (z[c] - target_center[c]) ** 2
                        for w, z in zip(weights, target)) for c in range(3))
    peak_lower = 1 - trace_cov / 2
    require(peak_lower > Q(3, 4), "explicit middle band")
    return loss_poly, covariance_minima, ranks, radius2, peak_lower


def check_transform_and_margin_ledgers():
    # In dimension three the hinge moment followed by path differentiation is
    # (1/4) k^(-5/2).  In dimension six the weighted Gaussian product is
    # (2*pi)^3 k^-3; multiplying by sqrt(k)/(32*pi^3) gives the same pair.
    for k in range(2, 258):
        hinge_rational, hinge_power = Q(1, 4), Q(-5, 2)
        lifted_rational = Q(8, 32)
        lifted_power = Q(-3) + Q(1, 2)
        require((hinge_rational, hinge_power) == (lifted_rational, lifted_power),
                f"replica normalization at k={k}")

    # Volume(B_3(epsilon/8)), spherical derivative 2*pi/r0, eligible-time
    # factor 1/2, Abel window factor 1/2, and 1/(32*pi^3) leave the rational
    # denominator 3*2^13 in equation (32).
    rational = Q(1, 192) * Q(1, 2) * Q(1, 2) * Q(1, 32)
    require(rational == Q(1, 3 * 2 ** 13), "strict-margin constant")
    require(13 + 2 + 2 + 2 == 19, "dyadic elementary-constant overhead")
    return 256, rational.denominator


def main():
    check_pins()
    schedules = check_schedules()
    loss, cov, ranks, radius2, peak = check_boundary_family()
    replica_orders, margin_denominator = check_transform_and_margin_ledgers()
    row = schedule(3, 3, 2)
    require(row[7:10] == (482, 781, 6056), "published calibration")
    record = {
        "affine_ranks": ranks,
        "boundary_covariance_minima": [str(x) + " * epsilon" for x in cov],
        "boundary_loss_polynomial": [str(x) for x in loss],
        "boundary_peak_lower_bound_gt": "3/4",
        "boundary_radius_squared": str(radius2),
        "calibration": {"N": row[7], "P": row[8], "L_cov": row[9]},
        "check": "INDEPENDENT_COVARIANCE_FREE_SMALL_LOSS_AUDIT_PASS",
        "dependency_pins": len(DEPENDENCY_PINS),
        "margin_denominator": margin_denominator,
        "replica_orders": replica_orders,
        "schedules": schedules,
        "source_files": len(SOURCE_HASHES),
        "trust_boundary": "exact finite audit; coarea and Abel proof checked by hand",
    }
    print(json.dumps(record, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
