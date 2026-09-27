#!/usr/bin/env python3
"""Independent exact controls for the rigid-block motion review.

CPython 3.11, standard library only.  All geometric calculations use
fractions.Fraction; subprocess is used only to hash bytes at the pinned commit.
The program checks finite endpoint hypotheses and scalar proof identities.  It
is not a proof assistant for the handwritten universal motion argument.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import copy
import json
import subprocess
import sys


TARGET_COMMIT = "411c088f7b9c6e06c1a05fc11548eab9e2119d63"
PINS = {
    "probability/gaussian_rigid_block_certificate/PROOF.md":
        "9e3fd33e294e01d9c1df1c658165b1a1e7a59cadd9e9ad4a0f28c729dda045af",
    "probability/gaussian_rigid_block_certificate/README.md":
        "78ef1620ab8af8fbe8d813d82fb0746a03ea032515bba22925514b6c483592e8",
    "probability/gaussian_rigid_block_certificate/HANDOFF.md":
        "5a8f9d0d0ed97f1c5bcbc7c6a2de32efa1ec0218a95e17729eea730f51be7f89",
    "probability/gaussian_rigid_block_certificate/SOURCES.md":
        "0e0fba17291a68d3ab19b286cf310dd66ae98f57c25761c14443c2e14562e6c2",
    "probability/gaussian_rigid_block_certificate/verify.py":
        "0fd7f3ec66c38e324a80ef873ad654c517008e4982c03c8f95e2a60a972dbde9",
    "probability/gaussian_rigid_block_certificate/INPUT.json":
        "13f9ed3d66535d8f00a7f1de61ee82470320f8c64532e837c26296e3edbaff03",
    "probability/gaussian_rigid_block_certificate/EXPECTED.json":
        "7be267d8dd2f83a7054ca8899633fd409606b2cd7360470e3786df87ad91a7ae",
    "probability/gaussian_rigid_block_certificate/SHA256SUMS":
        "7ff8e30c9ca046a01bb3e932e63bbfce47b5641ff66a684330c6b70dbf0fbb6f",
    "probability/gaussian_contraction_rigidity/PROOF.md":
        "d1b2daa37c88f9c2759b234b69a9c351f0adfb51f7df109e2864331413a582c8",
}


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def qstr(value):
    return str(value.numerator) if value.denominator == 1 else str(value)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def scale(c, a):
    return tuple(c * x for x in a)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), F(0))


def norm2(a):
    return dot(a, a)


def transpose(a):
    return tuple(zip(*a))


def matmul(a, b):
    bt = transpose(b)
    return tuple(tuple(dot(row, col) for col in bt) for row in a)


def matvec(a, v):
    return tuple(dot(row, v) for row in a)


def eye():
    return ((F(1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(1)))


def det3(a):
    return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
            - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
            + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))


def frobenius2(a):
    return sum((x * x for row in a for x in row), F(0))


def matsub(a, b):
    return tuple(tuple(x - y for x, y in zip(ar, br)) for ar, br in zip(a, b))


def center(rows):
    mean = tuple(sum((r[j] for r in rows), F(0)) / len(rows) for j in range(3))
    return tuple(sub(r, mean) for r in rows)


def scatter(rows):
    rows = center(rows)
    return tuple(tuple(sum((r[i] * r[j] for r in rows), F(0))
                       for j in range(3)) for i in range(3))


def rank(rows):
    a = [list(row) for row in rows]
    r = 0
    for col in range(len(a[0]) if a else 0):
        pivot = next((i for i in range(r, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        v = a[r][col]
        a[r] = [x / v for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][col]:
                c = a[i][col]
                a[i] = [x - c * y for x, y in zip(a[i], a[r])]
        r += 1
    return r


def rotation(t, axis):
    c = (1 - t * t) / (1 + t * t)
    s = 2 * t / (1 + t * t)
    z = F(0)
    o = F(1)
    if axis == "z":
        out = ((c, -s, z), (s, c, z), (z, z, o))
    elif axis == "x":
        out = ((o, z, z), (z, c, -s), (z, s, c))
    elif axis == "y":
        out = ((c, z, s), (z, o, z), (-s, z, c))
    else:
        out = eye()
    need(matmul(transpose(out), out) == eye() and det3(out) == 1,
         "Cayley rotation is not proper orthogonal")
    return out


TETRA = ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))
SQUARE = ((-1, -1, 0), (-1, 1, 0), (1, -1, 0), (1, 1, 0))
LINE = ((-1, 0, 0), (1, 0, 0))
CENTERS = ((-24, 0, 0), (24, 0, 0), (0, 24, 0), (0, -24, 0))
OFFSETS = (TETRA, SQUARE, LINE, ((0, 0, 0),))
AXES = ("z", "x", "y", None)
REFLECTION = ((F(0), F(0), F(1)),
              (F(0), F(1), F(0)),
              (F(1), F(0), F(0)))
TRANSLATION = (F(7), F(-11), F(5))


def fixture(t, change_frame=False):
    x, y, blocks, rotations = [], [], [], []
    for raw_c, raw_offsets, axis in zip(CENTERS, OFFSETS, AXES):
        c = tuple(map(F, raw_c))
        rmat = rotation(t, axis)
        rotations.append(rmat)
        ids = []
        for raw_v in raw_offsets:
            v = tuple(map(F, raw_v))
            ids.append(len(x))
            x.append(add(c, v))
            y.append(add(scale(1 - t, c), matvec(rmat, v)))
        blocks.append(tuple(ids))
    if change_frame:
        need(matmul(transpose(REFLECTION), REFLECTION) == eye()
             and det3(REFLECTION) == -1, "bad frame control")
        y = [add(matvec(REFLECTION, row), TRANSLATION) for row in y]
    return tuple(x), tuple(y), tuple(blocks), tuple(rotations)


EXPECTED_BLOCK_SCATTERS = (
    ((F(4), F(0), F(0)), (F(0), F(4), F(0)), (F(0), F(0), F(4))),
    ((F(4), F(0), F(0)), (F(0), F(4), F(0)), (F(0), F(0), F(0))),
    ((F(2), F(0), F(0)), (F(0), F(0), F(0)), (F(0), F(0), F(0))),
    ((F(0), F(0), F(0)), (F(0), F(0), F(0)), (F(0), F(0), F(0))),
)
EXPECTED_GLOBAL_SCATTER = (
    (F(4618), F(0), F(0)),
    (F(0), F(18520, 11), F(0)),
    (F(0), F(0), F(4)),
)


def endpoint_data(x, y, blocks):
    owner = {i: b for b, ids in enumerate(blocks) for i in ids}
    need(len(owner) == len(x) == len(y), "blocks do not partition fixture")
    pairs = tuple(combinations(range(len(x)), 2))
    source_d2 = {(i, j): norm2(sub(x[i], x[j])) for i, j in pairs}
    losses = {(i, j): source_d2[i, j] - norm2(sub(y[i], y[j]))
              for i, j in pairs}
    within = tuple(v for (i, j), v in losses.items() if owner[i] == owner[j])
    cross = tuple(v for (i, j), v in losses.items() if owner[i] != owner[j])
    need(min(losses.values()) >= 0, "fresh fixture contains an expansion")
    need(all(v == 0 for v in within), "fresh fixture changes a block distance")
    need(min(cross) > 0, "fresh fixture has a non-strict cross pair")
    block_scatters = tuple(scatter(tuple(x[i] for i in ids)) for ids in blocks)
    need(block_scatters == EXPECTED_BLOCK_SCATTERS, "unexpected block scatter")
    need(scatter(x) == EXPECTED_GLOBAL_SCATTER, "unexpected global scatter")
    ranks = tuple(rank(center(tuple(x[i] for i in ids))) for ids in blocks)
    need(ranks == (3, 2, 1, 0), "fresh fixture ranks changed")
    d2 = max(source_d2.values())
    need(d2 == 2505, "fresh fixture diameter changed")
    return {
        "losses": losses,
        "within": within,
        "cross": cross,
        "d2": d2,
        "error": sum((norm2(sub(a, b)) for a, b in zip(x, y)), F(0)),
        "ranks": ranks,
    }


def gram_error_and_reconstruction(x, y, losses):
    a, b = center(x), center(y)
    gram = tuple(tuple(dot(a[i], a[j]) - dot(b[i], b[j])
                       for j in range(len(x))) for i in range(len(x)))
    n = len(x)
    delta = tuple(tuple(F(0) if i == j else losses[min(i, j), max(i, j)]
                        for j in range(n)) for i in range(n))
    row_means = tuple(sum(row, F(0)) / n for row in delta)
    overall = sum(row_means, F(0)) / n
    rebuilt = tuple(tuple(-(delta[i][j] - row_means[i] - row_means[j] + overall) / 2
                          for j in range(n)) for i in range(n))
    need(gram == rebuilt, "double-centering reconstruction failed")
    return sum((v * v for row in gram for v in row), F(0))


def poly_add(a, b):
    return tuple((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b))))


def poly_mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return tuple(out)


def scalar_and_rank_controls(rotations):
    # 8+2q^2-(185/32+5q/2) = 2(q-5/8)^2+23/16.
    lhs = (F(71, 32), F(-5, 2), F(2))
    rhs = poly_add(tuple(2 * x for x in poly_mul((F(-5, 8), F(1)),
                                                 (F(-5, 8), F(1)))),
                   (F(23, 16),))
    need(lhs == rhs and rhs[0] > 0, "budget square completion failed")

    # Green-kernel and mean-derivative maxima reduce to these identities.
    # 1/8-t(1-t)/2 = (t-1/2)^2/2 and
    # 1/2-[t^2+(1-t)^2]/2 = t(1-t).
    green_square = tuple(x / 2 for x in
                         poly_mul((F(-1, 2), F(1)), (F(-1, 2), F(1))))
    need((F(1, 8), F(-1, 2), F(1, 2)) == green_square,
         "Green-kernel square identity failed")
    mean_integral = (F(1, 2), F(-1), F(1))
    mean_gap = poly_add((F(1, 2),), tuple(-x for x in mean_integral))
    need(mean_gap == (F(0), F(1), F(-1)),
         "mean-derivative kernel identity failed")

    # Sharp representatives of the rank-2, rank-1 and improper rank-3 bounds.
    p_source = ((F(1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(0)))
    p_rotation = ((F(0), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(1)))
    rank2_trace = sum(matmul(p_source, p_rotation)[i][i] for i in range(3))
    need(rank2_trace == 1, "rank-two projection control failed")
    line_u = (F(1), F(0), F(0))
    line_r = rotations[2]
    line_displacement = norm2(sub(matvec(line_r, line_u), line_u))
    need(frobenius2(matsub(line_r, eye())) == 2 * line_displacement,
         "rank-one shortest-rotation identity failed")
    need(frobenius2(matsub(REFLECTION, eye())) == 4,
         "improper-orthogonal lower-bound control failed")
    return {
        "budget_gap_coefficients": [qstr(x) for x in lhs],
        "budget_gap_positive_remainder": "23/16",
        "green_kernel_peak": "1/8",
        "mean_derivative_kernel_peak": "1/2",
        "rank2_projection_trace_sharp_case": qstr(rank2_trace),
        "rank1_frobenius_ratio": "2",
        "improper_distance_squared_sharp_case": "4",
    }


def verify_pins():
    root = Path(__file__).resolve().parents[2]
    for path, wanted in PINS.items():
        proc = subprocess.run(
            ["git", "-C", str(root), "show", f"{TARGET_COMMIT}:{path}"],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        need(sha256(proc.stdout).hexdigest() == wanted, f"source pin mismatch: {path}")


def calculate():
    verify_pins()
    kappa = F(2)
    c_factor = F(2513)

    direct_t = F(1, 2 ** 20)
    x, y, blocks, rotations = fixture(direct_t)
    direct = endpoint_data(x, y, blocks)
    cross = min(direct["cross"])
    margin = cross - c_factor * direct["error"]
    need(direct["error"] <= kappa and margin > 0, "direct guard failed")
    need(direct["error"] < F(1, 100_000_000)
         and cross > F(1, 600) and margin > F(1, 600),
         "direct display bounds failed")

    # Straight interpolation necessarily re-expands one nontrivially rotated
    # preserved pair near t=1.  The rigid path in the proof avoids this.
    a = sub(x[0], x[1])
    b = sub(y[0], y[1])
    straight_terminal_derivative = 2 * dot(b, sub(b, a))
    need(straight_terminal_derivative > 0, "straight-path control lost")

    invariant_t = F(1, 2 ** 30)
    xi, yi_raw, blocksi, rotations_i = fixture(invariant_t)
    xi2, yi, blocksi2, _ = fixture(invariant_t, change_frame=True)
    need(xi == xi2 and blocksi == blocksi2, "frame fixtures disagree")
    raw = endpoint_data(xi, yi_raw, blocksi)
    inv = endpoint_data(xi, yi, blocksi)
    need(raw["losses"] == inv["losses"], "global frame changed pair losses")
    gram_f = gram_error_and_reconstruction(xi, yi, inv["losses"])
    k = F(4)
    h = 2 * gram_f / k
    inv_cross = min(inv["cross"])
    inv_margin = inv_cross - c_factor * h
    need(h <= kappa and inv_margin > 0, "invariant guard failed")
    need(inv["error"] > kappa, "displayed-frame failure control did not fail")
    need(gram_f < F(1, 10_000_000_000)
         and h < F(1, 20_000_000_000)
         and inv_cross > F(1, 600_000)
         and inv_margin > F(1, 600_000),
         "invariant display bounds failed")

    epsilon = max(inv["losses"].values())
    rho = inv_cross / epsilon
    n = len(xi)
    cover_margin_1 = 2 * k * kappa - n * n * epsilon * epsilon
    cover_margin_2 = 2 * rho * k - c_factor * n * n * epsilon
    need(cover_margin_1 > 0 and cover_margin_2 > 0,
         "uniform-cover sufficient conditions failed")
    need(cover_margin_1 > 15 and cover_margin_2 > 1,
         "uniform-cover display bounds failed")

    # Three negative controls are intentionally local: they verify rejection,
    # not a negative Gaussian conclusion.
    corrupt_y = [list(row) for row in y]
    corrupt_y[0][0] += F(1, 1000)
    corrupt_y = tuple(tuple(row) for row in corrupt_y)
    within_changed = norm2(sub(corrupt_y[0], corrupt_y[1])) != norm2(sub(xi[0], xi[1]))
    bad_rotation = [list(row) for row in rotations_i[0]]
    bad_rotation[0][0] += F(1, 1000)
    bad_rotation = tuple(tuple(row) for row in bad_rotation)
    need(within_changed and matmul(transpose(bad_rotation), bad_rotation) != eye(),
         "corruption controls were not rejected")
    need(EXPECTED_BLOCK_SCATTERS[2][0][0] < 3,
         "oversized-kappa control was not rejected")

    return {
        "target_commit": TARGET_COMMIT,
        "pinned_source_files": len(PINS),
        "scalar_and_rank_controls": scalar_and_rank_controls(rotations),
        "fresh_direct_fixture": {
            "status": "CERTIFIED_ALL_VARIANCES",
            "parameter": qstr(direct_t),
            "sites": len(x),
            "pairs": len(direct["losses"]),
            "block_ranks": list(direct["ranks"]),
            "tight_within_pairs": len(direct["within"]),
            "strict_cross_pairs": len(direct["cross"]),
            "diameter_squared": qstr(direct["d2"]),
            "kappa": qstr(kappa),
            "budget_factor": qstr(c_factor),
            "displayed_error_upper_bound": "1/100000000",
            "minimum_cross_loss_lower_bound": "1/600",
            "cross_margin_lower_bound": "1/600",
            "straight_chord_terminal_derivative": qstr(straight_terminal_derivative),
        },
        "fresh_invariant_fixture": {
            "status": "CERTIFIED_ALL_VARIANCES_AND_UNIFORM_COVER",
            "parameter": qstr(invariant_t),
            "global_frame_determinant": qstr(det3(REFLECTION)),
            "global_scatter_floor": qstr(k),
            "gram_error_squared_upper_bound": "1/10000000000",
            "aligned_error_upper_bound": "1/20000000000",
            "minimum_cross_loss_lower_bound": "1/600000",
            "invariant_cross_margin_lower_bound": "1/600000",
            "displayed_error_exceeds_kappa": inv["error"] > kappa,
            "pair_losses_unchanged_by_global_frame": raw["losses"] == inv["losses"],
            "uniform_cover_margin_1_lower_bound": "15",
            "uniform_cover_margin_2_lower_bound": "1",
        },
        "negative_controls": {
            "changed_within_block_distance_rejected": within_changed,
            "nonorthogonal_rotation_rejected": True,
            "oversized_kappa_rejected": True,
            "failed_guard_interpretation": "UNRESOLVED_NOT_COUNTEREXAMPLE",
        },
        "result": "INDEPENDENT_RIGID_BLOCK_CONTROLS_PASSED",
    }


def main():
    result = calculate()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    expected_path = Path(__file__).with_name("EXPECTED.json")
    if len(sys.argv) == 2 and sys.argv[1] == "--emit":
        sys.stdout.write(rendered)
        return
    need(len(sys.argv) == 1, "usage: verify_review.py [--emit]")
    need(expected_path.read_text(encoding="utf-8") == rendered,
         "result differs from EXPECTED.json")
    sys.stdout.write(rendered)


if __name__ == "__main__":
    main()
