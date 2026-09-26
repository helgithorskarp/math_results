#!/usr/bin/env python3
"""Reproduce compact exact controls. No search output is a theorem."""
import argparse
from collections import defaultdict
from copy import deepcopy
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

from bounds import I, exp_negative, sqrt_integer
from certify import (distance_matrix, evaluate_case, moment_gap,
                     parse_case, replica_histogram, square_coefficients,
                     difference_histogram)

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def ordered_histogram(points, weights, k, variance):
    """Independent literal ordered-replica expansion, including repetitions."""
    out = defaultdict(F)
    for labels in product(range(len(points)), repeat=k):
        coefficient = F(1)
        for i in labels:
            coefficient *= weights[i]
        spread = F(0)
        for a in range(k):
            for b in range(a):
                spread += sum((u - v)**2
                              for u, v in zip(points[labels[a]], points[labels[b]]))
        out[-spread / (2 * k * variance)] += coefficient
    return dict(out)


def case(x, y, w, p, variance="1"):
    return {"dimension": 3, "variance": variance,
            "x": x, "y": y, "weights": w,
            "polynomial_square_root": p}


def controls():
    axis = [[-1, 0, 0], [0, 0, 0], [1, 0, 0]]
    fold = [[1, 0, 0], [0, 0, 0], [1, 0, 0]]
    tetra = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]
    asym = [[-1, 0, 0], [0, 0, 0], [1, 1, 0], [0, -1, 1]]
    reflected = [[2, -row[0], 3] for row in axis]
    return {
        "fold_quartic": case(axis, fold, ["1/4", "1/2", "1/4"], ["-1/4", 1]),
        "tetrahedron_collapse": case(tetra, [[0, 0, 0]] * 4,
                                     ["1/4"] * 4, [1, -4, 4]),
        "seven_point_rank_six_fold": json.loads((ROOT / "example.json").read_text()),
        "asymmetric_fold": case(asym, [[abs(t) for t in row] for row in asym],
                                ["1/10", "1/5", "3/10", "2/5"], ["1/50", "-1/2", 1]),
        "translated_isometry": case(axis, reflected, ["1/5", "1/2", "3/10"],
                                    ["1/50", "-1/2", 1]),
    }


def matrix_rank(matrix):
    a = [[F(x) for x in row] for row in matrix]
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        value = a[row][col]
        a[row] = [x / value for x in a[row]]
        for i in range(len(a)):
            if i != row:
                value = a[i][col]
                a[i] = [u - value * v for u, v in zip(a[i], a[row])]
        row += 1
        if row == len(a):
            break
    return row


def negative_control():
    # The classical catalytic-majorisation vectors. These are step densities,
    # NOT Gaussian convolutions and NOT a contraction counterexample.
    x = [F(2, 5), F(2, 5), F(1, 10), F(1, 10)]
    y = [F(1, 2), F(1, 4), F(1, 4), F(0)]
    catalyst = [F(3, 5), F(2, 5)]
    sx = sorted((a * b for a in x for b in catalyst), reverse=True)
    sy = sorted((a * b for a in y for b in catalyst), reverse=True)
    require(all(sum(sx[:k]) <= sum(sy[:k]) for k in range(1, 9)),
            "catalyst majorisation check failed")
    require(sum(x[:2]) > sum(y[:2]), "uncatalysed negative control lost")
    moments = [(sum(v**(j + 2) for v in y) - sum(v**(j + 2) for v in x))
               / ((j + 1) * (j + 2)) for j in range(9)]
    require(all(a > 0 for a in moments), "positive entries control failed")
    p = list(map(F, ["38448913/189092800000", "-2040157/94546400",
                     "13858457/47273200", "-1", "1"]))
    coeff = square_coefficients(p)
    value = sum(a * b for a, b in zip(coeff, moments))
    expected = F(-1442909906179, 1089174528000000000000)
    require(value == expected < 0, "negative Hankel witness failed")

    def hinge(t):
        return sum(max(v - t, 0) for v in y) - sum(max(v - t, 0) for v in x)

    # Independently integrate the actual piecewise-linear hinge curve.
    breaks = sorted(set([F(0), F(1)] + x + y))
    direct = F(0)
    for left, right in zip(breaks, breaks[1:]):
        slope = (hinge(right) - hinge(left)) / (right - left)
        intercept = hinge(left) - slope * left
        for j, c in enumerate(coeff):
            direct += c * (intercept * (right**(j + 1) - left**(j + 1)) / (j + 1)
                           + slope * (right**(j + 2) - left**(j + 2)) / (j + 2))
    require(direct == value, "hinge integration and moment witness disagree")
    return {"scope": "NON_GAUSSIAN_VALIDATOR_CONTROL",
            "positive_hankel_entries": len(moments),
            "matrix_order": 5, "energy_degree": 10,
            "square_root_coefficients": list(map(str, p)),
            "exact_negative_gap": str(value),
            "hinge_gap_at_one_quarter": str(hinge(F(1, 4))),
            "catalyst_partial_sums_checked": 8}


def transport_controls():
    records, direct_checks = [], 0
    for eps in [F(1, 2), F(1, 16), F(1, 100)]:
        for radius in [F(1, 2), F(1), F(2)]:
            a = radius**2
            h = exp_negative(-a / 2)
            z0 = (1 - eps) + eps * h
            zbar = (1 - eps) * (I.of(1) + exp_negative(-2 * a)) / 2 + eps * h
            lower = I.of(1 - eps) / z0 + eps * h / zbar
            require(lower.lo > 1, "uniform all-orthogonal transport obstruction failed")
            for c in [F(-1), F(-1, 2), F(0), F(1, 2), F(1)]:
                zp = (1 - eps) * exp_negative(-a * (1 - c)) + eps * h
                zm = (1 - eps) * exp_negative(-a * (1 + c)) + eps * h
                row = I.of(1 - eps) / z0 + eps * h * (I.of(1) / zp + I.of(1) / zm) / 2
                require(row.lo > 1, "direct rotated coupling check failed")
                direct_checks += 1
            x = [[-radius, F(0), F(0)], [F(0)] * 3, [radius, F(0), F(0)]]
            y = [[abs(v) for v in row] for row in x]
            weights = [eps / 2, 1 - eps, eps / 2]
            hist = difference_histogram(distance_matrix(x), distance_matrix(y), weights, 2, F(1))
            gap = moment_gap(hist, 2, 70)
            formula = eps**2 * (I.of(1) - exp_negative(-a)) / (4 * sqrt_integer(2))
            require(max(gap.lo, formula.lo) <= min(gap.hi, formula.hi), "fold d2 identity failed")
            ex = sum(w * v[0] for w, v in zip(weights, x))
            ey = sum(w * v[0] for w, v in zip(weights, y))
            covariance = sum(w * (v[0] - ex) * (u[0] - ey)
                             for w, v, u in zip(weights, x, y))
            variance_sum = sum(w * ((v[0] - ex)**2 + (u[0] - ey)**2)
                               for w, v, u in zip(weights, x, y))
            require(covariance == 0 and variance_sum == radius**2 * eps * (2 - eps),
                    "independent centered geometry identity failed")
            records.append({"epsilon": str(eps), "radius": str(radius),
                            "uniform_lower_bound_for_row_at_zero": lower.strings(),
                            "rho_squared": str(variance_sum)})
    return records, direct_checks


def invalid_controls(template):
    callbacks = []
    for key, value in [("dimension", 2), ("variance", 0), ("weights", ["1/2"] * 7),
                       ("polynomial_square_root", [0])]:
        item = deepcopy(template)
        item[key] = value
        callbacks.append(lambda item=item: evaluate_case(item))
    item = deepcopy(template)
    item["x"][1][0] = 0.5
    callbacks.append(lambda item=item: evaluate_case(item))
    item = deepcopy(template)
    item["y"][1][0] = 10
    callbacks.append(lambda item=item: evaluate_case(item))
    item = deepcopy(template)
    item["x"][1] = item["x"][0]
    callbacks.append(lambda item=item: evaluate_case(item))
    item = deepcopy(template)
    item["y"][1] = [0, 0]
    callbacks.append(lambda item=item: evaluate_case(item))
    callbacks.extend([lambda: evaluate_case(template, digits=0),
                      lambda: evaluate_case(template, max_states=1),
                      lambda: exp_negative(F(1)),
                      lambda: I.of(1) / I(-1, 1),
                      lambda: I(1, 0), lambda: sqrt_integer(-1)])
    for callback in callbacks:
        try:
            callback()
        except ValueError:
            continue
        raise RuntimeError("invalid-input control unexpectedly accepted")
    return len(callbacks)


def reproduce():
    fixtures = controls()
    evaluations = []
    for name, item in fixtures.items():
        result = evaluate_case(item)
        require(result["verdict"] == "NO_NEGATIVE_WITNESS", "positive control failed: " + name)
        if name == "translated_isometry":
            require(result["energy_gap_interval"] == ["0", "0"], "isometry cancellation failed")
        evaluations.append({"name": name, **result})
    example = fixtures["seven_point_rank_six_fold"]
    joint = [x + y for x, y in zip(example["x"], example["y"])]
    require(matrix_rank([[a - b for a, b in zip(row, joint[0])] for row in joint[1:]]) == 6,
            "seven-point control is not full joined affine rank six")
    crosschecks, tuples = 0, 0
    for name, maximum in [("fold_quartic", 6), ("tetrahedron_collapse", 5)]:
        x, y, w, _, s, dx, dy, _ = parse_case(fixtures[name])
        for points, distances in [(x, dx), (y, dy)]:
            for k in range(2, maximum + 1):
                a = replica_histogram(distances, w, k, s)
                b = ordered_histogram(points, w, k, s)
                require(a == b, "ordered and multinomial replicas disagree")
                require(sum(a.values()) == 1, "replica coefficient mass lost")
                crosschecks += 1
                tuples += len(w)**k
    transport, direct_checks = transport_controls()
    artificial = (2 * sqrt_integer(2) - 3) / 16
    require(artificial.hi < 0, "abstract square-root multiplier obstruction failed")
    for k in [0, 1, 2, 3, 5, 97]:
        root = sqrt_integer(k)
        square = root * root
        require(square.lo <= k <= square.hi, "integer square-root enclosure failed")
    require(exp_negative(F(0)) == I.of(1), "exact exponential identity failed")
    for a, b in [(F(1, 3), F(2, 3)), (F(3), F(5)), (F(100), F(156))]:
        direct = exp_negative(-a - b)
        separate = exp_negative(-a) * exp_negative(-b)
        require(max(direct.lo, separate.lo) <= min(direct.hi, separate.hi),
                "independent exponential decomposition disagrees")
    return {"status": "VERIFIED_REDUCTION_CONTROLS",
            "conjecture_status": "OPEN; no admissible negative Gaussian certificate supplied",
            "gaussian_polynomial_controls": evaluations,
            "literal_replica_crosschecks": crosschecks,
            "ordered_tuples_checked": tuples,
            "joined_affine_rank_of_seven_point_control": 6,
            "transport_uniform_bounds": transport,
            "direct_rotation_samples": direct_checks,
            "abstract_eta_dirac_determinant": artificial.strings(),
            "negative_validator_control": negative_control(),
            "invalid_inputs_rejected": invalid_controls(example)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write-expected", action="store_true")
    args = parser.parse_args()
    result = reproduce()
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    expected = ROOT / "EXPECTED.json"
    if args.write_expected:
        expected.write_text(output)
    if args.check:
        require(output == expected.read_text(), "expected output mismatch")
    print(output, end="")


if __name__ == "__main__":
    main()
