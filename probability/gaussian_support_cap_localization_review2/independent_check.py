#!/usr/bin/env python3
"""Independent exact checks for support-cap localization.

No target module is imported.  The main geometric check uses a cellwise
interval lower enclosure of the cube-chart integrand, rather than the
target midpoint rule plus one global Lipschitz error.  On every cell it
minorizes the source support function with one affine branch, majorizes the
target support function at all corners, and chooses the denominator endpoint
according to the sign of the resulting gap.
"""

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from math import lcm
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "gaussian_support_cap_localization"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rational(value):
    require(type(value) is int or type(value) is str, "non-rational input")
    return F(value)


def dot(x, y):
    return sum((a * b for a, b in zip(x, y)), F(0))


def sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def norm2(x):
    return dot(x, x)


def center(rows):
    n = len(rows)
    mean = tuple(sum((row[j] for row in rows), F(0)) / n for j in range(3))
    return [sub(row, mean) for row in rows]


def read_input(data):
    x = [tuple(rational(v) for v in row) for row in data["sources"]]
    y = [tuple(rational(v) for v in row) for row in data["targets"]]
    weights = [rational(v) for v in data["weights"]]
    require(x and len(x) == len(y) == len(weights), "list dimensions")
    require(all(len(v) == 3 for v in x + y), "ambient dimension")
    require(all(w > 0 for w in weights) and sum(weights) == 1,
            "positive probability weights")
    x, y = center(x), center(y)
    radius = rational(data["reference_radius"])
    cloud = rational(data["cloud_radius"])
    rho = rational(data["relative_weight_error"])
    require(radius > 0 and cloud >= 0 and 0 <= rho <= F(1, 2),
            "neighborhood parameters")
    require(all(norm2(v) <= radius * radius for v in x + y), "radius guard")
    losses = {}
    for i, j in combinations(range(len(x)), 2):
        loss = norm2(sub(x[i], x[j])) - norm2(sub(y[i], y[j]))
        require(loss >= 0, "reference expansion")
        losses[i, j] = loss
    return x, y, weights, radius, cloud, rho, losses


def integer_points(rows, radius):
    normalized = [[value / radius for value in row] for row in rows]
    denominator = lcm(*(value.denominator for row in normalized for value in row))
    return [tuple(int(value * denominator) for value in row)
            for row in normalized], denominator


def square_minimum(lo, hi):
    return 0 if lo <= 0 <= hi else min(lo * lo, hi * hi)


def interval_width_lower(x, y, radius, mesh, bits):
    """Exact lower Darboux-style enclosure on all six cube charts."""
    require(type(mesh) is int and mesh >= 1 and type(bits) is int and bits >= 1,
            "mesh and precision")
    points, denominator = integer_points(x + y, radius)
    xx, yy = points[:len(x)], points[len(x):]
    scale = 1 << bits
    floor_sum = 0
    negative_cells = 0
    cells = 0
    for axis in range(3):
        other = [j for j in range(3) if j != axis]
        for sign in (-1, 1):
            for a, b in product(range(1 - mesh, mesh, 2), repeat=2):
                midpoint = [0, 0, 0]
                midpoint[axis] = sign * mesh
                midpoint[other[0]], midpoint[other[1]] = a, b
                source_index = max(range(len(xx)), key=lambda i: dot(xx[i], midpoint))
                corners = []
                for u, v in product((a - 1, a + 1), (b - 1, b + 1)):
                    corner = [0, 0, 0]
                    corner[axis] = sign * mesh
                    corner[other[0]], corner[other[1]] = u, v
                    corners.append(tuple(corner))
                source_lower = min(dot(xx[source_index], corner) for corner in corners)
                target_upper = max(dot(row, corner) for row in yy for corner in corners)
                gap = source_lower - target_upper

                amin, amax = a - 1, a + 1
                bmin, bmax = b - 1, b + 1
                q_min = (mesh * mesh + square_minimum(amin, amax)
                         + square_minimum(bmin, bmax))
                q_max = (mesh * mesh + max(amin * amin, amax * amax)
                         + max(bmin * bmin, bmax * bmax))
                q_bound = q_max if gap >= 0 else q_min
                # Cell area times the pointwise integrand lower bound:
                # 4/M^2 * (gap/(H M)) * M^4/q_bound^2.
                numerator = scale * 4 * mesh * gap
                cell_floor = numerator // (denominator * q_bound * q_bound)
                floor_sum += cell_floor
                negative_cells += int(gap < 0)
                cells += 1
    integral_lower = F(floor_sum, scale)
    width_lower = radius * integral_lower / 16 if integral_lower > 0 else None
    return {
        "mesh": mesh,
        "bits": bits,
        "cells": cells,
        "negative_cells": negative_cells,
        "floor_sum": floor_sum,
        "integral_lower": integral_lower,
        "width_lower": width_lower,
    }


def pair_loss(weights, losses):
    return sum((2 * weights[i] * weights[j] * loss
                for (i, j), loss in losses.items()), F(0))


def ceiling(value):
    return -(-value.numerator // value.denominator)


def schedule(radius, cloud, rho, weights, loss, width):
    actual_radius = radius + cloud
    d = (1 - rho) ** 2 * loss - 16 * radius * cloud - 8 * cloud * cloud
    mass = (1 - rho) * min(weights)
    k = 0
    while (1 << k) * mass < 1:
        k += 1
    b = width - 2 * cloud
    require(d > 0 and b > 0, "nonpositive reserve")
    n = max(1, ceiling(actual_radius * (k + 1) / b))
    eta = d * F(1, 2 ** (8 * n)) / (48 * actual_radius * actual_radius)
    require(n * b >= actual_radius * (k + 1), "tail join")
    require(0 < eta <= F(1, 12), "endpoint gap range")
    prefactor = 2112 * actual_radius ** 4 / d
    require(44 * actual_radius * actual_radius / eta
            == prefactor * 2 ** (8 * n), "cutoff constant")
    return {
        "actual_radius": actual_radius,
        "loss_lower": d,
        "mass_lower": mass,
        "mass_exponent": k,
        "tail_slope": b,
        "tail_join": n,
        "cutoff_prefactor": prefactor,
        "cutoff_power_of_two": 8 * n,
    }


def simple_controls():
    source = [(F(-1), F(0), F(0)), (F(1), F(0), F(0))]
    point = [(F(0), F(0), F(0)), (F(0), F(0), F(0))]
    segment = interval_width_lower(source, point, F(1), 32, 36)
    require(segment["width_lower"] is not None
            and 0 < segment["width_lower"] <= F(1, 2), "segment width")

    rotated = [(F(0), F(-1), F(0)), (F(0), F(1), F(0))]
    isometry = interval_width_lower(source, rotated, F(1), 16, 36)
    require(isometry["width_lower"] is None, "isometry falsely certified")
    require(isometry["negative_cells"] > 0, "negative denominator branch unused")
    return {
        "segment_width_lower": segment["width_lower"],
        "isometry_integral_lower": isometry["integral_lower"],
        "negative_cells": isometry["negative_cells"],
    }


def provenance_checks():
    metadata = json.loads((HERE / "TARGET_INPUTS.json").read_text())
    for item in metadata["files"]:
        digest = sha256((HERE / item["relative_path"]).read_bytes()).hexdigest()
        require(digest == item["sha256"], "reviewed input bytes changed")
    return metadata["target"], len(metadata["files"])


def main():
    target, pins = provenance_checks()
    data = json.loads((TARGET / "INPUT.json").read_text())
    certificate = json.loads((TARGET / "CERTIFICATE.json").read_text())
    x, y, weights, radius, cloud, rho, losses = read_input(data)
    width = interval_width_lower(x, y, radius, 64, 40)
    require(width["width_lower"] is not None, "independent width unresolved")
    loss = pair_loss(weights, losses)
    independent = schedule(radius, cloud, rho, weights, loss, width["width_lower"])

    require(str(loss) == certificate["reference_loss"], "reference loss mismatch")
    require(str(independent["loss_lower"]) == certificate["actual_loss_lower"],
            "cloud reserve mismatch")
    require(independent["mass_exponent"] == certificate["mass_exponent"],
            "mass exponent mismatch")
    require(width["cells"] == 6 * 64 * 64 and width["negative_cells"] > 0,
            "chart coverage")

    controls = simple_controls()
    negative_controls = 0
    bad = json.loads(json.dumps(data))
    bad["targets"][0][0] = "100"
    try:
        read_input(bad)
    except RuntimeError:
        negative_controls += 1
    else:
        raise RuntimeError("expanded reference accepted")
    try:
        schedule(radius, cloud, rho, weights, F(0), width["width_lower"])
    except RuntimeError:
        negative_controls += 1
    else:
        raise RuntimeError("zero loss reserve accepted")

    record = {
        "status": "INDEPENDENT_SUPPORT_CAP_REVIEW_PASS",
        "target": target,
        "pinned_files": pins,
        "interval_chart": {
            "mesh": width["mesh"],
            "bits": width["bits"],
            "cells": width["cells"],
            "negative_cells": width["negative_cells"],
            "floor_sum": width["floor_sum"],
            "integral_lower": str(width["integral_lower"]),
            "width_lower": str(width["width_lower"]),
        },
        "independent_schedule": {key: str(value) if isinstance(value, F) else value
                                 for key, value in independent.items()},
        "controls": {key: str(value) if isinstance(value, F) else value
                     for key, value in controls.items()},
        "negative_controls": negative_controls,
        "method": "exact cellwise interval enclosure; no target-code import",
        "trust_boundary": (
            "finite exact corroboration only; spherical-gap dependencies, "
            "support compactness, cap argument, and certificate existence are "
            "reviewed written mathematics"
        ),
    }
    raw = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    print(json.dumps({"record": record, "record_sha256": sha256(raw).hexdigest()},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
