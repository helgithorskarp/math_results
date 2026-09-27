#!/usr/bin/env python3
"""Clean-room exact checks for the quartic-loss middle-sign review.

This file imports no target code or target expected output.  It uses a
different 80-pair nonlinear contraction for the cubature check and compares
the direct ordered-pair definition of Q with both moment expansions.
"""

from fractions import Fraction as Q
from itertools import combinations
from math import comb
from pathlib import Path
import hashlib
import json
import random


ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "probability" / "gaussian_loss_moment_middle"
HERE = Path(__file__).resolve().parent
PINS = {
    "PROOF.md": "90b10a51afd34487dad7e9a73c314d4845d769f07939373089b68341b31844fb",
    "HANDOFF.md": "e5ce685477c1ffe0e2ea9574a2102971f4ba2aa56b5a0a87943bd4026bf7b1f9",
    "SOURCES.md": "46a4baa288c18260b7b1c4265c65f0e989f772403cbe9fad94018b48e1e9aa3a",
    "INPUTS.json": "4ded948ff9e742cec09dcd181466707684c7059bb91e6e1d69e5c4baa9186713",
    "EXPECTED.json": "f0f53dcc75a41d9bc082187784c5a329a0466690c3381c909c3668c7ea8ef6f8",
    "verify.py": "b9ceda3eb555b1f2194f0b8fc9f3b909c8fa01997a4c3902c61f14706eb172f5",
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def pin_target():
    for name, wanted in PINS.items():
        actual = hashlib.sha256((TARGET / name).read_bytes()).hexdigest()
        need(actual == wanted, f"target pin mismatch: {name}")


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), Q(0))


def sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def dist2(x, y):
    return dot(sub(x, y), sub(x, y))


def weighted_mean(points, weights):
    return tuple(sum((w * x[j] for w, x in zip(weights, points)), Q(0))
                 for j in range(3))


def center(points, weights):
    mean = weighted_mean(points, weights)
    return [sub(point, mean) for point in points]


def matrix_moment(left, right, weights):
    return [[sum((w * x[i] * y[j]
                  for w, x, y in zip(weights, left, right)), Q(0))
             for j in range(3)] for i in range(3)]


def frobenius_square(matrix):
    return sum((value * value for row in matrix for value in row), Q(0))


def direct_losses(x, y, weights):
    """Definitions using all ordered iid pairs, including the diagonal."""
    d = Q(0)
    second = Q(0)
    minimum = None
    for i, j in ((i, j) for i in range(len(weights))
                 for j in range(len(weights))):
        loss = dist2(x[i], x[j]) - dist2(y[i], y[j])
        d += weights[i] * weights[j] * loss
        second += weights[i] * weights[j] * loss * loss
        minimum = loss if minimum is None else min(minimum, loss)
    return d, second, minimum


def centered_formula(x, y, weights):
    xc = center(x, weights)
    yc = center(y, weights)
    a = matrix_moment(xc, xc, weights)
    b = matrix_moment(yc, yc, weights)
    c = matrix_moment(xc, yc, weights)
    h = [dot(u, u) - dot(v, v) for u, v in zip(xc, yc)]
    eh = sum((w * value for w, value in zip(weights, h)), Q(0))
    eh2 = sum((w * value * value for w, value in zip(weights, h)), Q(0))
    second = (2 * eh2 + 2 * eh * eh
              + 4 * (frobenius_square(a) + frobenius_square(b)
                     - 2 * frobenius_square(c)))
    return 2 * eh, second, a, b, c


def raw_formula(x, y, weights):
    z = [u + v for u, v in zip(x, y)]
    signs = (1, 1, 1, -1, -1, -1)
    mean = [sum((w * point[i] for w, point in zip(weights, z)), Q(0))
            for i in range(6)]
    moment = [[sum((w * point[i] * point[j]
                    for w, point in zip(weights, z)), Q(0))
               for j in range(6)] for i in range(6)]
    h = [sum((signs[i] * point[i] * point[i] for i in range(6)), Q(0))
         for point in z]
    vector = [sum((w * value * point[i]
                   for w, value, point in zip(weights, h, z)), Q(0))
              for i in range(6)]
    eh = sum((w * value for w, value in zip(weights, h)), Q(0))
    eh2 = sum((w * value * value for w, value in zip(weights, h)), Q(0))
    trace = sum((signs[i] * signs[j] * moment[i][j] * moment[j][i]
                 for i in range(6) for j in range(6)), Q(0))
    correction = sum((vector[i] * signs[i] * mean[i]
                      for i in range(6)), Q(0))
    return 2 * eh2 + 2 * eh * eh + 4 * trace - 8 * correction


def theorem_constants():
    # Each transcendental comparison in the proof is reduced to one of these
    # rational inequalities using log(2)<3/4 and e<3.
    checks = {
        "exp_three_quarters_gt_two": Q(1) + Q(3, 4) + Q(9, 32) > 2,
        "q_denominator": 3 ** 16 < 2 ** 26,
        "gaussian_peak": Q(44, 7) ** 3 < 256,
        "half_ball_volume": Q(3, 6) == Q(1, 2),
        "window_overlap": Q(121, 96) > 1,
        "covariance_floor": Q(1, 25600) > Q(1, 2 ** 15),
        "bracket": Q(1, 2 ** 32) - Q(1, 2 ** 33) == Q(1, 2 ** 33),
        "margin": Q(1, 16) * Q(1, 2) * Q(1, 4) * Q(1, 2 ** 33)
                  == Q(1, 2 ** 40),
    }
    need(all(checks.values()), "constant chain")
    return len(checks)


VERTICES = (
    (Q(1), Q(1), Q(1)),
    (Q(1), Q(-1), Q(-1)),
    (Q(-1), Q(1), Q(-1)),
    (Q(-1), Q(-1), Q(1)),
)


def scale(value, point):
    return tuple(value * coordinate for coordinate in point)


def add_matrices(left, right):
    return [[left[i][j] + right[i][j] for j in range(3)]
            for i in range(3)]


def outer(x):
    return [[x[i] * x[j] for j in range(3)] for i in range(3)]


def family_bounds():
    zero = [[Q(0) for _ in range(3)] for _ in range(3)]
    vertex_sum = (Q(0), Q(0), Q(0))
    square_sum = zero
    for vertex in VERTICES:
        vertex_sum = tuple(a + b for a, b in zip(vertex_sum, vertex))
        square_sum = add_matrices(square_sum, outer(vertex))
    need(vertex_sum == (Q(0), Q(0), Q(0)), "tetrahedron first moment")
    need(square_sum == [[Q(4) if i == j else Q(0) for j in range(3)]
                        for i in range(3)], "tetrahedron second moment")

    source = [scale(Q(1, 80), v) for v in VERTICES]
    source += [scale(Q(-1, 4), v) for v in VERTICES]
    target_zero = [scale(Q(1, 80), v) for v in VERTICES]
    target_zero += [scale(Q(29, 120), v) for v in VERTICES]

    table = {"core_core": set(), "outer_outer": set(),
             "matched": set(), "unmatched": set()}
    for i, j in combinations(range(8), 2):
        pair = (6400 * dist2(source[i], source[j]),
                6400 * dist2(target_zero[i], target_zero[j]))
        if j < 4:
            table["core_core"].add(pair)
        elif i >= 4:
            table["outer_outer"].add(pair)
        elif i == j - 4:
            table["matched"].add(pair)
        else:
            table["unmatched"].add(pair)
    wanted = {
        "core_core": {(Q(8), Q(8))},
        "outer_outer": {(Q(3200), Q(26912, 9))},
        "matched": {(Q(1323), Q(3025, 3))},
        "unmatched": {(Q(1163), Q(1163))},
    }
    need(table == wanted, "distance table")
    need(all(target_value <= source_value
             for values in table.values()
             for source_value, target_value in values), "endpoint contraction")

    t_max = Q(1, 2 ** 40)
    alpha_max = Q(1, 2 ** 105)
    need(t_max < 1 and alpha_max < Q(1, 19), "parameter enclosure")
    need(Q(11 * 11 * 3, 40 * 40) < Q(1, 4), "centered radius")
    need((1 - alpha_max) ** 2 * (2 - t_max) >= Q(1, 4),
         "core-loss lower-bound factor")

    ratio = t_max / 400 + Q(102400, 3 * 2 ** 65)
    expected = Q(2161, 2400 * 2 ** 48)
    need(ratio == expected < Q(1, 2 ** 48), "uniform Q/d ratio")
    need(Q(1, 25600) > Q(1, 2 ** 15), "source covariance")
    return {
        "distance_pairs": 28,
        "ratio_over_2^-48": str(ratio * 2 ** 48),
        "relative_slack": str(1 - ratio * 2 ** 48),
    }


def random_pair_formula_checks():
    rng = random.Random(27092026)
    cases = 0
    for size in range(2, 14):
        for _ in range(7):
            x = [tuple(Q(rng.randrange(-20, 21), 13) for _ in range(3))
                 for _ in range(size)]
            # Coordinatewise absolute value followed by 1/3 scaling is a
            # nonlinear 1/3-Lipschitz map.
            y = [tuple(abs(value) / 3 for value in point) for point in x]
            raw_weights = [rng.randrange(1, 20) for _ in range(size)]
            weights = [Q(value, sum(raw_weights)) for value in raw_weights]
            direct_d, direct_q, minimum = direct_losses(x, y, weights)
            formula_d, formula_q, _, _, _ = centered_formula(x, y, weights)
            need(minimum >= 0, "nonlinear map did not contract")
            need((direct_d, direct_q) == (formula_d, formula_q),
                 "centered moment identity")
            need(direct_q == raw_formula(x, y, weights), "raw moment identity")
            cases += 1
    return cases


def monomials(max_degree):
    return [(i, j, k) for total in range(1, max_degree + 1)
            for i in range(total + 1)
            for j in range(total + 1 - i)
            for k in (total - i - j,)]


def feature_columns(x, y, weights):
    powers = monomials(4)
    xc = center(x, weights)
    yc = center(y, weights)
    columns = []
    for source, target, source_c, target_c in zip(x, y, xc, yc):
        values = [Q(1)]
        values += [source[0] ** i * source[1] ** j * source[2] ** k
                   for i, j, k in powers]
        values += [target[0] ** i * target[1] ** j * target[2] ** k
                   for i, j, k in powers]
        values += [source_c[i] * target_c[j]
                   for i in range(3) for j in range(3)]
        values.append(dot(source_c, source_c) * dot(target_c, target_c))
        need(len(values) == 2 * comb(7, 3) - 1 + 10, "feature count")
        columns.append(values)
    return columns


def right_to_left_relation(columns):
    """One kernel vector, with a pivot order opposite to the target code."""
    rows = [list(row) for row in zip(*columns)]
    pivot_rows = []
    row = 0
    for column in reversed(range(len(columns))):
        pivot = next((candidate for candidate in range(row, len(rows))
                      if rows[candidate][column]), None)
        if pivot is None:
            continue
        rows[row], rows[pivot] = rows[pivot], rows[row]
        scale_by = rows[row][column]
        rows[row] = [value / scale_by for value in rows[row]]
        for other in range(len(rows)):
            if other == row or not rows[other][column]:
                continue
            multiple = rows[other][column]
            rows[other] = [a - multiple * b
                           for a, b in zip(rows[other], rows[row])]
        pivot_rows.append((row, column))
        row += 1
        if row == len(rows):
            break
    pivot_columns = {column for _, column in pivot_rows}
    free = next(column for column in range(len(columns))
                if column not in pivot_columns)
    relation = [Q(0)] * len(columns)
    relation[free] = Q(1)
    for pivot_row, pivot_column in pivot_rows:
        relation[pivot_column] = -rows[pivot_row][free]
    need(any(value > 0 for value in relation)
         and any(value < 0 for value in relation), "relation signs")
    need(all(sum((relation[j] * columns[j][i]
                  for j in range(len(columns))), Q(0)) == 0
             for i in range(len(columns[0]))), "kernel relation")
    return relation


def expectation(columns, weights):
    return [sum((weight * column[j]
                 for weight, column in zip(weights, columns)), Q(0))
            for j in range(len(columns[0]))]


def independent_cubature():
    rng = random.Random(31415926)
    points = set()
    while len(points) < 80:
        points.add(tuple(Q(rng.randrange(-30, 31), 17) for _ in range(3)))
    x = sorted(points)
    y = [tuple(abs(value) / 3 for value in point) for point in x]
    raw_weights = [rng.randrange(1, 50) for _ in x]
    weights = [Q(value, sum(raw_weights)) for value in raw_weights]
    columns = feature_columns(x, y, weights)
    relation = right_to_left_relation(columns)
    step = min(weight / coefficient
               for weight, coefficient in zip(weights, relation)
               if coefficient > 0)
    reduced_weights = [weight - step * coefficient
                       for weight, coefficient in zip(weights, relation)]
    active = [i for i, weight in enumerate(reduced_weights) if weight > 0]
    new_weights = [reduced_weights[i] for i in active]
    need(all(weight >= 0 for weight in reduced_weights), "negative cubature weight")
    need(len(active) <= 79 and sum(new_weights) == 1, "cubature atom bound")
    need(expectation(columns, weights)
         == expectation([columns[i] for i in active], new_weights),
         "79-feature expectation")

    new_x = [x[i] for i in active]
    new_y = [y[i] for i in active]
    need(weighted_mean(x, weights) == weighted_mean(new_x, new_weights),
         "source mean changed")
    need(weighted_mean(y, weights) == weighted_mean(new_y, new_weights),
         "target mean changed")
    # Recompute centering from the reduced prior instead of trusting the old
    # feature columns.
    need(expectation(columns, weights)
         == expectation(feature_columns(new_x, new_y, new_weights), new_weights),
         "recentered feature expectation")
    old_direct = direct_losses(x, y, weights)[:2]
    new_direct = direct_losses(new_x, new_y, new_weights)[:2]
    need(old_direct == new_direct, "d or Q changed under cubature")
    need(centered_formula(x, y, weights)[:2]
         == centered_formula(new_x, new_y, new_weights)[:2],
         "moment guard changed under cubature")

    corrupted = list(new_weights)
    transfer = min(corrupted[0], corrupted[1]) / 7
    corrupted[0] -= transfer
    corrupted[1] += transfer
    need(expectation(feature_columns(new_x, new_y, new_weights), corrupted)
         != expectation(columns, weights), "corruption not detected")
    return {"input_pairs": len(x), "output_pairs": len(active),
            "features": len(columns[0]), "d": str(old_direct[0]),
            "Q": str(old_direct[1])}


def pairing_countercontrol():
    x = [(Q(value), Q(0), Q(0)) for value in (0, 2, 5, 9)]
    values = (Q(0), Q(1, 5), Q(1, 2), Q(9, 10))
    y1 = [(value, Q(0), Q(0)) for value in values]
    y2 = [y1[i] for i in (2, 0, 3, 1)]
    weights = [Q(1, 4)] * 4
    d1, q1, minimum1 = direct_losses(x, y1, weights)
    d2, q2, minimum2 = direct_losses(x, y2, weights)
    need(minimum1 >= 0 and minimum2 >= 0, "countercontrol contraction")
    need(d1 == d2 and q1 != q2, "marginals did not separate Q")
    return {"d": str(d1), "Q1": str(q1), "Q2": str(q2)}


def main():
    pin_target()
    record = {
        "constant_checks": theorem_constants(),
        "family": family_bounds(),
        "moment_formula_cases": random_pair_formula_checks(),
        "pairing_countercontrol": pairing_countercontrol(),
        "cubature": independent_cubature(),
        "target_pins": len(PINS),
        "status": "LOSS_MOMENT_MIDDLE_INDEPENDENT_ACCEPT",
    }
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    need(record == expected, "independent expected record mismatch")
    print(record["status"])


if __name__ == "__main__":
    main()
