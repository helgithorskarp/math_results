#!/usr/bin/env python3
"""Independent exact review controls for twisted meridian contractions.

No target module is imported.  Distance derivatives are reconstructed with
dual numbers, and a fresh finite endpoint-data fixture checks the whole-time
pair condition independently of the author's sparse-polynomial code.
"""

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
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
        require(sha256((HERE / relative).read_bytes()).hexdigest() == expected,
                "changed reviewed input: " + relative)
    return manifest


@dataclass(frozen=True)
class Dual:
    value: F
    derivative: F = F(0)

    def __add__(self, other):
        other = as_dual(other)
        return Dual(self.value + other.value, self.derivative + other.derivative)

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.value, -self.derivative)

    def __sub__(self, other):
        return self + (-as_dual(other))

    def __rsub__(self, other):
        return as_dual(other) - self

    def __mul__(self, other):
        other = as_dual(other)
        return Dual(self.value * other.value,
                    self.derivative * other.value + self.value * other.derivative)

    __rmul__ = __mul__


def as_dual(value):
    return value if isinstance(value, Dual) else Dual(F(value))


def square(value):
    return value * value


def norm2(vector):
    return sum((value * value for value in vector), F(0))


def difference(left, right):
    return tuple(a - b for a, b in zip(left, right))


def delayed_clock(root_q, root_c):
    require(F(0) < root_q <= root_c <= 1, "clock domain")
    q = root_q ** 2
    t = (1 - root_c ** 2) / (1 - q)
    phase = root_q * (1 - root_c) / (root_c * (1 - root_q))
    speed = root_q * (1 + root_q) / (2 * root_c ** 3)
    require(phase == (1 / root_c - 1) / (1 / root_q - 1), "clock phase")
    require(speed == ((1 - q) /
                      (2 * (1 / root_q - 1) * root_c ** 3)), "clock speed")
    require(root_c ** 6 * speed ** 2 == root_q ** 2 * (1 + root_q) ** 2 / 4,
            "clock invariant")
    return t, phase, speed


def pair_scalars(p, image_p, phase_p, q, image_q, phase_q, t):
    r, z = p
    rp, zp = q
    rho, zeta = image_p
    rhop, zetap = image_q
    a, ap = r - rho, rp - rhop
    A, Ap = r - t * a, rp - t * ap
    loss = norm2(difference(p, q)) - norm2(difference(image_p, image_q))
    return loss, A * Ap, a * Ap + ap * A, phase_p - phase_q


def dual_distance_control(p, image_p, phase_p, q, image_q, phase_q,
                          time, speed, cosine, sine):
    r, z = map(F, p)
    rp, zp = map(F, q)
    rho, zeta = map(F, image_p)
    rhop, zetap = map(F, image_q)
    phase_difference = F(phase_p) - F(phase_q)
    t = Dual(F(time), F(1))
    A = r + t * (rho - r)
    Ap = rp + t * (rhop - rp)
    Z = z + t * (zeta - z)
    Zp = zp + t * (zetap - zp)
    # d/dt cos(delta)=-sin(delta)*lambda'(t)*d.
    C = Dual(F(cosine), -F(sine) * F(speed) * phase_difference)
    transverse = square(A) + square(Ap) - 2 * A * Ap * C
    radial_auxiliary = t * (1 - t) * (r - rho - rp + rhop) ** 2
    axial_auxiliary = t * (1 - t) * (z - zeta - zp + zetap) ** 2
    direct = transverse + square(Z - Zp) + radial_auxiliary + axial_auxiliary

    loss, P, K, d = pair_scalars((r, z), (rho, zeta), F(phase_p),
                                  (rp, zp), (rhop, zetap), F(phase_q), F(time))
    split = ((1 - F(time)) * norm2((r - rp, z - zp))
             + F(time) * norm2((rho - rhop, zeta - zetap))
             + 2 * P * (1 - F(cosine)))
    derivative = -loss - 2 * K * (1 - F(cosine)) + 2 * P * F(speed) * d * F(sine)
    require(direct.value == split, "dual distance value")
    require(direct.derivative == derivative, "dual distance derivative")
    return direct.value, direct.derivative


def motion_identity_controls():
    angles = [(F(1), F(0)), (F(0), F(1)), (F(-1), F(0)), (F(0), F(-1)),
              (F(3, 5), F(4, 5)), (F(5, 13), F(-12, 13))]
    fixtures = [
        ((F(1), F(-1, 2)), (F(1, 5), F(1, 7)), F(2, 9),
         (F(3, 4), F(2, 3)), (F(1, 8), F(1, 3)), F(-1, 11)),
        ((F(0), F(2, 5)), (F(0), F(-1, 10)), F(4, 7),
         (F(5, 6), F(-1, 4)), (F(1, 6), F(1, 9)), F(1, 8)),
        ((F(7, 9), F(0)), (F(0), F(3, 10)), F(-2, 5),
         (F(2, 9), F(1, 2)), (F(1, 20), F(-1, 8)), F(3, 7)),
    ]
    controls = 0
    for root_q in [F(1, 4), F(2, 5), F(3, 4)]:
        for step in range(6):
            root_c = root_q + (1 - root_q) * F(step, 5)
            time, phase, speed = delayed_clock(root_q, root_c)
            require(F(0) <= time <= 1 and F(0) <= phase <= 1, "clock range")
            for fixture in fixtures:
                for cosine, sine in angles:
                    require(cosine ** 2 + sine ** 2 == 1, "rational angle")
                    dual_distance_control(*fixture, time, speed, cosine, sine)
                    controls += 1
    return {"dual_distance_derivatives": controls, "clock_controls": 18}


def allowance_squared(root_q, meridian_lipschitz):
    return (8 * (1 - meridian_lipschitz ** 2) * (1 - root_q) /
            (root_q ** 2 * (1 + root_q)))


def uniform_budget_controls():
    radial_controls = 0
    exact_allowances = []
    for root_q, g in product([F(1, 7), F(1, 4), F(2, 5), F(3, 4)],
                             [F(1, 3), F(3, 5), F(9, 10)]):
        q = root_q ** 2
        allowance = allowance_squared(root_q, g)
        denominator = 1 / root_q - 1
        require(allowance * (1 - q) == 8 * (1 - g ** 2) * denominator ** 2,
                "allowance identity")
        require(allowance * (1 - q) / (8 * denominator ** 2) == 1 - g ** 2,
                "uniform loss payment")
        exact_allowances.append(allowance)
        for t in [F(j, 9) for j in range(10)]:
            c = 1 - (1 - q) * t
            for r, rp, rho_ratio, rhop_ratio in [
                    (F(1), F(2, 3), q, F(0)),
                    (F(5, 7), F(9, 10), F(0), q),
                    (F(3, 5), F(4, 9), q / 2, q / 3)]:
                rho, rhop = rho_ratio * r, rhop_ratio * rp
                A = (1 - t) * r + t * rho
                Ap = (1 - t) * rp + t * rhop
                P = A * Ap
                K = (r - rho) * Ap + (rp - rhop) * A
                require(A <= c * r and Ap <= c * rp, "transverse radius bound")
                if P:
                    require(K / P >= 2 * (1 - q) / c, "K/P bound")
                if K:
                    require(P ** 2 / K <= c ** 3 * r * rp / (2 * (1 - q)),
                            "P squared over K")
                radial_controls += 1
    require(allowance_squared(F(1, 4), F(9, 16)) == F(105, 2),
            "helical allowance")
    return {
        "parameter_pairs": len(exact_allowances),
        "radial_bound_controls": radial_controls,
        "minimum_allowance_squared": min(exact_allowances),
        "helical_allowance_squared": F(105, 2),
    }


def endpoint_map(point):
    r, z = point
    return (r / 4, z / 2), (r + z) / 100


def endpoint_fixture_controls():
    points = [(F(r, 3), F(z, 2)) for r, z in product(range(4), range(-2, 3))]
    labels = [(point, *endpoint_map(point)) for point in points]
    pair_count = 0
    time_controls = 0
    minimum_surplus = None
    minimum_whole_time_surplus = None
    for (p, image_p, phase_p), (q, image_q, phase_q) in combinations(labels, 2):
        loss0, P0, K0, d = pair_scalars(p, image_p, phase_p,
                                        q, image_q, phase_q, F(0))
        endpoint_surplus = loss0 * (loss0 + 4 * K0) - 4 * P0 ** 2 * d ** 2
        require(endpoint_surplus >= 0, "endpoint certificate")
        for time in [F(j, 10) for j in range(11)]:
            loss, P, K, d = pair_scalars(p, image_p, phase_p,
                                         q, image_q, phase_q, time)
            surplus = loss * (loss + 4 * K) - 4 * P ** 2 * d ** 2
            require(surplus >= 0, "whole-time endpoint certificate")
            if P:
                require(P <= P0 and K / P >= K0 / P0,
                        "endpoint monotonic factors")
            minimum_whole_time_surplus = (surplus if minimum_whole_time_surplus is None
                                          else min(minimum_whole_time_surplus, surplus))
            time_controls += 1
        minimum_surplus = (endpoint_surplus if minimum_surplus is None
                           else min(minimum_surplus, endpoint_surplus))
        pair_count += 1
    return {
        "labels": len(labels),
        "pairs": pair_count,
        "whole_time_controls": time_controls,
        "minimum_endpoint_surplus": minimum_surplus,
        "minimum_whole_time_surplus": minimum_whole_time_surplus,
    }


def matmul(left, right):
    return [[sum(left[i][k] * right[k][j] for k in range(len(right)))
             for j in range(len(right[0]))] for i in range(len(left))]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def determinant3(matrix):
    return (matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
            - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
            + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]))


def helical_jacobian(direction, rotation_sign, axial_sign):
    u, v = direction
    return [[F(rotation_sign, 16), F(0), F(-7 * rotation_sign * v, 32)],
            [F(0), F(rotation_sign, 16), F(7 * rotation_sign * u, 32)],
            [F(u, 2), F(v, 2), F(axial_sign, 4)]]


def scope_separation_controls():
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    jacobians = [helical_jacobian(direction, rotation, axial)
                 for direction, rotation, axial in product(directions, (-1, 1), (-1, 1))]
    mean = [[sum(matrix[i][j] for matrix in jacobians) / len(jacobians)
             for j in range(3)] for i in range(3)]
    require(mean == [[F(0)] * 3 for _ in range(3)], "zero mean Jacobian")
    grams = [matmul(transpose(matrix), matrix) for matrix in jacobians]
    mean_gram = [[sum(matrix[i][j] for matrix in grams) / len(grams)
                  for j in range(3)] for i in range(3)]
    expected = [[F(33, 256), F(0), F(0)],
                [F(0), F(33, 256), F(0)],
                [F(0), F(0), F(113, 1024)]]
    require(mean_gram == expected, "mean Gram")
    require(all(mean_gram[i][i] > 0 for i in range(3)) and determinant3(mean_gram) > 0,
            "scalar-defect contradiction")
    first = matmul(transpose(helical_jacobian((1, 0), 1, 1)),
                      helical_jacobian((1, 0), 1, 1))
    second = matmul(transpose(helical_jacobian((0, 1), 1, 1)),
                       helical_jacobian((0, 1), 1, 1))
    commutator = [[a - b for a, b in zip(row_ab, row_ba)]
                  for row_ab, row_ba in zip(matmul(first, second), matmul(second, first))]
    require(commutator[0][1] == F(4145, 262144), "Gram commutator")
    return {
        "jacobians": len(jacobians),
        "mean_jacobian_zero": True,
        "mean_gram_diagonal": [mean_gram[i][i] for i in range(3)],
        "mean_gram_determinant": determinant3(mean_gram),
        "gram_commutator_01": commutator[0][1],
    }


def corruption_controls():
    rejected = 0
    try:
        delayed_clock(F(0), F(1))
    except ValueError:
        rejected += 1
    else:
        raise RuntimeError("invalid clock accepted")
    try:
        require(F(106, 2) <= allowance_squared(F(1, 4), F(9, 16)),
                "overlarge helical phase")
    except ValueError:
        rejected += 1
    else:
        raise RuntimeError("overlarge phase accepted")
    p, q = (F(1), F(0)), (F(1), F(1, 8))
    image_p, phase_p = (F(1, 16), F(1, 2)), F(0)
    image_q, phase_q = (F(1, 16), F(17, 32)), F(7, 8)
    loss, P, K, d = pair_scalars(p, image_p, phase_p, q, image_q, phase_q, F(0))
    try:
        require(loss * (loss + 4 * K) >= 4 * P ** 2 * d ** 2,
                "invalid linear clock")
    except ValueError:
        rejected += 1
    else:
        raise RuntimeError("invalid linear clock accepted")
    try:
        require(F(104, 2) > allowance_squared(F(1, 4), F(9, 16)),
                "damaged allowance unexpectedly valid")
    except ValueError:
        rejected += 1
    else:
        raise RuntimeError("damaged allowance accepted")
    return rejected


def run():
    manifest = pin_inputs()
    return {
        "status": "INDEPENDENT_TWISTED_MERIDIAN_REVIEW_PASS",
        "verdict": "accept twisted meridian Gaussian and ball-volume comparisons in scope",
        "target_commit": manifest["target_commit"],
        "target_graph_ref": manifest["target_graph_ref"],
        "pinned_inputs": len(manifest["files"]),
        "motion_identity": motion_identity_controls(),
        "uniform_budget": uniform_budget_controls(),
        "endpoint_fixture": endpoint_fixture_controls(),
        "scope_separation": scope_separation_controls(),
        "rejected_corruptions": corruption_controls(),
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
    print("INDEPENDENT_TWISTED_MERIDIAN_REVIEW_PASS")
    print("record_sha256=" + sha256(record).hexdigest())


if __name__ == "__main__":
    main()
