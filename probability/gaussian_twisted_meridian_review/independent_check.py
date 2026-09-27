#!/usr/bin/env python3
"""Independent exact controls for twisted meridian contractions.

No author code or expected record is imported.  The distance derivative is
reconstructed directly from Euclidean coordinate velocities at rational
unit-circle points, rather than by sparse formal-polynomial expansion.
"""

import argparse
import copy
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


def circle(parameter):
    denominator = 1 + parameter * parameter
    return ((1 - parameter * parameter) / denominator,
            2 * parameter / denominator)


def quarter_turn(unit):
    return (-unit[1], unit[0])


def meridian_data(label, time):
    p, image, phase = label
    displacement = sub(p, image)
    radial = p[0] - time * displacement[0]
    axial = p[1] - time * displacement[1]
    return radial, axial, displacement, phase


def pair_quantities(first, second, time):
    p, image, phase = first
    q, target, other_phase = second
    A, _, displacement, _ = meridian_data(first, time)
    B, _, other_displacement, _ = meridian_data(second, time)
    M = norm2(sub(p, q)) - norm2(sub(image, target))
    P = A * B
    K = displacement[0] * B + other_displacement[0] * A
    return M, P, K, phase - other_phase


def coordinate_identity_controls():
    labels = [
        ((F(1), F(0)), (F(1, 4), F(1, 3)), F(2)),
        ((F(3, 2), F(-1, 2)), (F(1, 2), F(-1, 4)), F(-1)),
        ((F(0), F(2)), (F(0), F(1)), F(5)),
        ((F(2), F(1)), (F(0), F(0)), F(3, 2)),
    ]
    units = [circle(value) for value in [F(-1), F(0), F(1, 2), F(2)]]
    times = [F(0), F(1, 5), F(1, 2), F(4, 5), F(1)]
    speeds = [F(0), F(3, 7)]
    controls = 0
    for first, second in combinations(labels, 2):
        p, image, phase = first
        q, target, other_phase = second
        for unit, other_unit, time, speed in product(units, units, times, speeds):
            A, Z, displacement, _ = meridian_data(first, time)
            B, W, other_displacement, _ = meridian_data(second, time)
            transverse_difference = sub(scale(A, unit), scale(B, other_unit))
            direct_square = (norm2(transverse_difference) + (Z - W) ** 2
                             + time * (1 - time)
                             * norm2(sub(displacement, other_displacement)))
            M, P, K, phase_difference = pair_quantities(first, second, time)
            split_square = ((1 - time) * norm2(sub(p, q))
                            + time * norm2(sub(image, target))
                            + 2 * P * (1 - dot(unit, other_unit)))
            require(direct_square == split_square, "distance identity")

            first_velocity = add(scale(-displacement[0], unit),
                                 scale(A * speed * phase, quarter_turn(unit)))
            second_velocity = add(scale(-other_displacement[0], other_unit),
                                  scale(B * speed * other_phase,
                                        quarter_turn(other_unit)))
            direct_derivative = (
                2 * dot(transverse_difference,
                        sub(first_velocity, second_velocity))
                + 2 * (Z - W) * (-displacement[1] + other_displacement[1])
                + (1 - 2 * time)
                * norm2(sub(displacement, other_displacement))
            )
            sine_difference = (unit[1] * other_unit[0]
                               - unit[0] * other_unit[1])
            formula_derivative = (-M - 2 * K * (1 - dot(unit, other_unit))
                                  + 2 * P * speed * phase_difference
                                  * sine_difference)
            require(direct_derivative == formula_derivative,
                    "coordinate derivative identity")
            controls += 1
    return controls


def allowance_squared(root_q, g):
    require(0 < root_q < 1 and 0 <= g < 1, "uniform parameter domain")
    return 8 * (1 - g * g) * (1 - root_q) / (
        root_q * root_q * (1 + root_q))


def clock(root_q, root_c):
    q = root_q * root_q
    require(0 < root_q < 1 and root_q <= root_c <= 1, "clock domain")
    time = (1 - root_c * root_c) / (1 - q)
    value = (1 / root_c - 1) / (1 / root_q - 1)
    speed = (1 - q) / (2 * (1 / root_q - 1) * root_c ** 3)
    require(root_c ** 3 * speed == (1 - q) / (2 * (1 / root_q - 1)),
            "clock invariant")
    return time, value, speed


def uniform_budget_controls():
    controls = 0
    clock_controls = 0
    for root_q, g in product([F(1, 8), F(1, 4), F(1, 2), F(3, 4)],
                             [F(0), F(1, 2), F(3, 4)]):
        q = root_q ** 2
        phase_lipschitz_squared = allowance_squared(root_q, g)
        last_value = F(-1)
        for index in range(9):
            root_c = 1 - (1 - root_q) * F(index, 8)
            time, value, speed = clock(root_q, root_c)
            require(0 <= time <= 1 and last_value <= value <= 1,
                    "clock normalization")
            require(root_c ** 6 * speed ** 2
                    == (1 - q) ** 2 / (4 * (1 / root_q - 1) ** 2),
                    "squared clock invariant")
            last_value = value
            clock_controls += 1
            for r, other_r, x, y in product(
                    [F(1, 3), F(1)], [F(1, 3), F(1)],
                    [1 - q, 1 - q / 2, F(1)],
                    [1 - q, 1 - q / 2, F(1)]):
                A = r * (1 - time * x)
                B = other_r * (1 - time * y)
                P = A * B
                K = r * x * B + other_r * y * A
                meridian_square = F(1)
                M = (1 - g * g) * meridian_square
                phase_difference_squared = (phase_lipschitz_squared
                                             * meridian_square)
                if K:
                    require(P * P / K
                            <= root_c ** 6 * r * other_r / (2 * (1 - q)),
                            "P squared over K")
                    adverse = (P * P * speed * speed
                               * phase_difference_squared / K)
                else:
                    require(P == 0, "zero K boundary")
                    adverse = F(0)
                require(adverse <= M, "uniform adverse phase budget")
                require(M * (M + 4 * K)
                        >= 4 * P * P * speed * speed
                        * phase_difference_squared,
                        "full phase budget")
                controls += 1
        require(last_value == 1, "terminal phase")
    return clock_controls, controls


def endpoint_monotonicity_controls():
    controls = 0
    for r, other_r, x, y in product(
            [F(1, 3), F(1)], [F(1, 2), F(1)],
            [F(0), F(1, 4), F(1, 2), F(1)],
            [F(0), F(1, 4), F(1, 2), F(1)]):
        previous_P = None
        previous_H = None
        P0 = r * other_r
        K0 = r * x * other_r + other_r * y * r
        phase_difference = F(1, 10)
        M = F(1) + 2 * P0 * abs(phase_difference)
        require(M * (M + 4 * K0)
                >= 4 * P0 * P0 * phase_difference ** 2,
                "endpoint premise")
        for index in range(9):
            time = F(index, 8)
            A = r * (1 - time * x)
            B = other_r * (1 - time * y)
            P = A * B
            K = r * x * B + other_r * y * A
            H = K / P if P else None
            if previous_P is not None:
                require(P <= previous_P, "P monotonicity")
            if H is not None and previous_H is not None:
                require(H >= previous_H, "K over P monotonicity")
            require(M * (M + 4 * K)
                    >= 4 * P * P * phase_difference ** 2,
                    "endpoint criterion propagation")
            previous_P = P
            if H is not None:
                previous_H = H
            controls += 1
    return controls


def regularization_controls():
    first = ((F(1), F(0)), (F(1, 4), F(0)), F(0))
    second = ((F(1), F(1)), (F(1, 4), F(1, 4)), F(1, 10))
    root_q = F(1, 2)
    controls = 0
    p, image, _ = first
    q, target, _ = second
    M = norm2(sub(p, q)) - norm2(sub(image, target))
    for epsilon, time in product([F(1, 10), F(1, 3), F(3, 4)],
                                 [F(0), F(1, 4), F(1, 2), F(1)]):
        h = 1 - epsilon
        tau = h * time
        root_c_squared = 1 - (1 - root_q ** 2) * tau
        # The chosen grid makes this square rational only when checked through
        # the algebraic speed invariant; no square-root approximation is used.
        P_data = pair_quantities(first, second, tau)
        original_M, P, K, phase_difference = P_data
        require(original_M == M, "time-independent loss")
        delta_p = sub(p, q)
        delta_target = sub(image, target)
        regular_delta = add(scale(epsilon, delta_p),
                            scale(h, delta_target))
        regular_M = norm2(delta_p) - norm2(regular_delta)
        require(regular_M == h * M + epsilon * h
                * norm2(sub(delta_p, delta_target)),
                "regularized loss identity")
        # Compare after clearing lambda'(tau)^2 via c(tau)^3 lambda'^2.
        invariant = (1 - root_q ** 2) ** 2 / (
            4 * (1 / root_q - 1) ** 2)
        speed_squared = invariant / root_c_squared ** 3
        original_residual = (M * (M + 4 * K)
                             - 4 * P * P * speed_squared
                             * phase_difference ** 2)
        regular_residual = (regular_M * (regular_M + 4 * h * K)
                            - 4 * P * P * h * h * speed_squared
                            * phase_difference ** 2)
        require(original_residual >= 0, "original regularization premise")
        require(regular_residual >= h * h * original_residual,
                "regularized phase budget")
        controls += 1
    return controls


def matmul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def jacobian(unit, rotation_sign, axial_sign):
    return [[F(rotation_sign, 16), F(0),
             -F(7 * rotation_sign * unit[1], 32)],
            [F(0), F(rotation_sign, 16),
             F(7 * rotation_sign * unit[0], 32)],
            [F(unit[0], 2), F(unit[1], 2), F(axial_sign, 4)]]


def example_controls():
    g = F(9, 16)
    root_q = F(1, 4)
    require(F(1, 256) + F(1, 4) + F(1, 16) == g * g,
            "meridian Frobenius bound")
    require(allowance_squared(root_q, g) == F(105, 2),
            "helical allowance")
    require(F(49) < F(105, 2), "helical phase budget")
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    matrices = [jacobian(unit, rotation, sign)
                for unit, rotation, sign
                in product(directions, [-1, 1], [-1, 1])]
    total = [[sum((matrix[i][j] for matrix in matrices), F(0))
              for j in range(3)] for i in range(3)]
    require(total == [[F(0)] * 3 for _ in range(3)], "mean Jacobian")
    grams = [matmul(transpose(matrix), matrix) for matrix in matrices]
    mean = [[sum((matrix[i][j] for matrix in grams), F(0)) / len(grams)
             for j in range(3)] for i in range(3)]
    expected = [[F(33, 256), F(0), F(0)],
                [F(0), F(33, 256), F(0)],
                [F(0), F(0), F(113, 1024)]]
    require(mean == expected and all(mean[i][i] > 0 for i in range(3)),
            "positive mean Gram matrix")
    first = jacobian((1, 0), 1, 1)
    second = jacobian((0, 1), 1, 1)
    first_gram = matmul(transpose(first), first)
    second_gram = matmul(transpose(second), second)
    commutator = [[x - y for x, y in zip(row_a, row_b)]
                  for row_a, row_b in zip(matmul(first_gram, second_gram),
                                          matmul(second_gram, first_gram))]
    require(commutator[0][1] == F(4145, 262144),
            "noncommuting Jacobian Grams")
    return {
        "jacobians": len(matrices),
        "mean_gram_diagonal": [str(mean[i][i]) for i in range(3)],
        "commutator_01": str(commutator[0][1]),
        "allowance_squared": "105/2",
    }


def main_map(point):
    r, z = point
    return (r / 16, r / 2 + abs(z) / 4), 7 * z


def negative_controls():
    first_point, second_point = (F(1), F(0)), (F(1), F(1, 8))
    first_image, first_phase = main_map(first_point)
    second_image, second_phase = main_map(second_point)
    first = (first_point, first_image, first_phase)
    second = (second_point, second_image, second_phase)
    M, P, K, d = pair_quantities(first, second, F(0))
    linear = M * (M + 4 * K) - 4 * P * P * d * d
    require(linear == F(-3095839, 1048576), "linear-clock damage")
    M, P, K, d = pair_quantities(first, second, F(1))
    _, _, terminal_speed = clock(F(1, 4), F(1, 4))
    doubled = M * (M + 4 * K) - 4 * P * P * terminal_speed ** 2 * (2 * d) ** 2
    require(doubled == F(-12175, 1048576), "doubled-phase damage")
    return {"linear_clock": str(linear), "doubled_phase": str(doubled)}


def corruption_controls():
    base = {"root_q": F(1, 4), "g": F(9, 16), "L2": F(49)}

    def validate(record):
        require(record["L2"] <= allowance_squared(record["root_q"], record["g"]),
                "phase allowance")

    validate(base)
    damaged = []
    item = copy.deepcopy(base); item["L2"] = F(53); damaged.append(item)
    item = copy.deepcopy(base); item["root_q"] = F(0); damaged.append(item)
    item = copy.deepcopy(base); item["root_q"] = F(1); damaged.append(item)
    item = copy.deepcopy(base); item["g"] = F(1); damaged.append(item)
    rejected = 0
    for item in damaged:
        try:
            validate(item)
        except ValueError:
            rejected += 1
        else:
            raise RuntimeError("damaged uniform record accepted")
    return rejected


def run():
    manifest = pin_inputs()
    clock_controls, budget_controls = uniform_budget_controls()
    return {
        "status": "INDEPENDENT_TWISTED_MERIDIAN_ACCEPT",
        "verdict": "accept the stated twisted-meridian Gaussian and ball-volume class",
        "target_artifact": manifest["target_artifact"],
        "target_source_commit": manifest["target_source_commit"],
        "pinned_files": len(manifest["files"]),
        "coordinate_identity_controls": coordinate_identity_controls(),
        "clock_controls": clock_controls,
        "uniform_budget_controls": budget_controls,
        "endpoint_monotonicity_controls": endpoint_monotonicity_controls(),
        "regularization_controls": regularization_controls(),
        "example_controls": example_controls(),
        "negative_controls": negative_controls(),
        "rejected_corruptions": corruption_controls(),
        "unrestricted_majorisation_proved": False,
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
        "coordinate_identity_controls": result["coordinate_identity_controls"],
        "uniform_budget_controls": result["uniform_budget_controls"],
        "regularization_controls": result["regularization_controls"],
        "record_sha256": sha256(canonical.encode()).hexdigest(),
        "unrestricted_majorisation_proved": result["unrestricted_majorisation_proved"],
    }, indent=2))


if __name__ == "__main__":
    main()
