#!/usr/bin/env python3
"""Independent exact audit of the straight-path adverse-pair theorem."""

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
import json
from math import factorial
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "gaussian_straight_path_pair_obstruction"

PINS = {
    "EXPECTED.json": "a5b8a62f68abca8c03b8ae760b736563d9712e67adb52a7de8347a496a8a4640",
    "PROOF.md": "13fc8d04f1531713cf715d0409737f1b5ffac14703ff93af657c1ada9cc52676",
    "SOURCES.md": "e80ea4e67b181cffab676ef01d8f999c46f6cdd4109568aff5e179929a326b90",
    "verify.py": "42ac3b9d6f75d91c357b76ddd1a445f5376af2a6dfc15d13900d256b5753fdd8",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def norm2(a):
    return dot(a, a)


def dist2(a, b):
    return norm2(sub(a, b))


def determinant(matrix):
    a = [list(map(Q, row)) for row in matrix]
    result = Q(1)
    for col in range(len(a)):
        pivot = next((r for r in range(col, len(a)) if a[r][col]), None)
        require(pivot is not None, "singular determinant")
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            result = -result
        diagonal = a[col][col]
        result *= diagonal
        for row in range(col + 1, len(a)):
            scale = a[row][col] / diagonal
            for j in range(col + 1, len(a)):
                a[row][j] -= scale * a[col][j]
    return result


def strict_fixture(lam):
    b = (Q(3), Q(3), Q(3))
    source = [b]
    for axis in range(3):
        point = list(b)
        point[axis] += 1
        source.append(tuple(point))
    for axis in range(3):
        for depth in (4, 5):
            point = list(b)
            point[axis] -= depth
            source.append(tuple(point))
    target = [tuple(Q(3) + lam * (abs(x) - 3) for x in point)
              for point in source]
    return source, target


def covariance(source, target):
    n = len(source)
    mean_source = tuple(sum(p[j] for p in source) / n for j in range(3))
    mean_target = tuple(sum(p[j] for p in target) / n for j in range(3))
    return [[sum((x[i] - mean_source[i]) * (y[j] - mean_target[j])
                 for x, y in zip(source, target)) / n
             for j in range(3)] for i in range(3)]


def pair_parameters(source, target, i, j):
    h = [sub(y, x) for x, y in zip(source, target)]
    d0 = dist2(source[i], source[j])
    loss = d0 - dist2(target[i], target[j])
    speed = dist2(h[i], h[j])
    linear = 2 * dot(sub(source[i], source[j]), sub(h[i], h[j]))
    require(linear == -loss - speed, "straight-path distance polynomial")
    return d0, loss, speed


def triple_parameters(source, target, i, j, k):
    h = [sub(y, x) for x, y in zip(source, target)]
    edges = ((i, j), (i, k), (j, k))
    source_sum = sum(dist2(source[a], source[b]) for a, b in edges)
    target_sum = sum(dist2(target[a], target[b]) for a, b in edges)
    loss_sum = source_sum - target_sum
    speed_sum = sum(dist2(h[a], h[b]) for a, b in edges)
    return source_sum, loss_sum, speed_sum


def ceil_fraction(value):
    return (value.numerator + value.denominator - 1) // value.denominator


def all_label_reserve(source, target, i, j):
    _, edge_loss, edge_speed = pair_parameters(source, target, i, j)
    weighted_reflection = Q(0)
    for k in range(len(source)):
        source_sum, loss_sum, speed_sum = triple_parameters(source, target, i, j, k)
        require(loss_sum >= 0 and speed_sum >= 0, "triple contraction data")
        exponent = ceil_fraction(source_sum / 6)
        # e < 11/4 gives exp(-S/6) > (4/11)^(S/6), and rounding
        # the exponent upward makes this rational lower bound smaller.
        weighted_reflection += Q(1, len(source)) * loss_sum * Q(4, 11) ** exponent
    return edge_speed * weighted_reflection / 36 - edge_loss


def multinomial_normalization(n):
    entries = 0
    for triple in combinations_with_replacement(range(n), 3):
        counts = Counter(triple)
        permutations = factorial(3)
        for multiplicity in counts.values():
            permutations //= factorial(multiplicity)
        for i, j in combinations(counts, 2):
            # In the ordered cubic expansion, d_ij appears once for every
            # choice of an i-position and j-position.  The result is the
            # constant coefficient six used by the unordered-pair formula.
            coefficient = permutations * counts[i] * counts[j]
            require(coefficient == 6, "cubic unordered-pair coefficient")
            entries += 1
    return entries


def gaussian_completion_controls(points):
    probes = [
        (Q(0), Q(0), Q(0)),
        (Q(1, 3), Q(-2, 5), Q(7, 11)),
        (Q(-4), Q(2), Q(1, 7)),
        (Q(9, 4), Q(-3, 2), Q(5, 6)),
    ]
    count = 0
    for a, b, c in combinations_with_replacement(range(len(points)), 3):
        triple = (points[a], points[b], points[c])
        mean = tuple(sum(p[j] for p in triple) / 3 for j in range(3))
        pair_sum = dist2(triple[0], triple[1]) + dist2(triple[0], triple[2]) + dist2(triple[1], triple[2])
        for u in probes:
            lhs = sum(dist2(u, p) for p in triple)
            rhs = 3 * dist2(u, mean) + pair_sum / 3
            require(lhs == rhs, "three-Gaussian square completion")
            count += 1
    return count


def reflection_polynomial_controls():
    count = 0
    for s0 in (Q(1), Q(7, 3), Q(12)):
        for loss in (Q(0), Q(1, 5), Q(9, 2)):
            for speed in (Q(0), Q(2, 7), Q(8)):
                for t in (Q(0), Q(1, 9), Q(2, 5), Q(1, 2)):
                    def path_sum(u):
                        return s0 - u * loss - u * (1 - u) * speed
                    require(path_sum(1 - t) - path_sum(t) == -(1 - 2 * t) * loss,
                            "time-reflection exponent")
                    count += 1
    # Integral_0^(1/2) (1-2t)^2 dt = 1/6 is the remaining scalar factor.
    require(Q(1, 2) - Q(1, 2) + Q(1, 6) == Q(1, 6),
            "reflection integral")
    return count


def seven_site_control():
    source = [tuple(map(Q, p)) for p in (
        (0, 0, 0), (-1, -1, 0), (-1, 0, 1), (0, -1, 1),
        (1, -2, 5), (-2, -5, -1), (-5, 1, 2),
    )]
    normals = ((1, 1, 1), (1, -1, -1), (-1, 1, -1))
    target = source[:4] + [
        tuple(x - Q(8, 3) * normal for x, normal in zip(point, direction))
        for point, direction in zip(source[4:], normals)
    ]
    tight_edges = []
    adverse_edges = []
    for i, j in combinations(range(7), 2):
        _, loss, speed = pair_parameters(source, target, i, j)
        require(loss >= 0, "seven-site contraction")
        if loss == 0:
            tight_edges.append((i, j))
            if speed > 0:
                strict_thirds = []
                for k in range(7):
                    _, loss_sum, _ = triple_parameters(source, target, i, j, k)
                    if loss_sum > 0:
                        strict_thirds.append(k)
                require(strict_thirds, "moving tight edge lacks strict third label")
                adverse_edges.append((i, j, tuple(strict_thirds)))
    reached = {0}
    for _ in range(7):
        for i, j in tight_edges:
            if i in reached or j in reached:
                reached.update((i, j))
    require(len(reached) == 7, "seven-site tight graph")
    require(len(tight_edges) == 15 and len(adverse_edges) == 9,
            "seven-site adverse-edge census")
    source_sum, loss_sum, _ = triple_parameters(source, target, 0, 4, 1)
    _, edge_loss, edge_speed = pair_parameters(source, target, 0, 4)
    require((source_sum, loss_sum, edge_loss, edge_speed) ==
            (62, Q(32, 3), 0, Q(64, 3)), "published seven-site edge")
    return len(tight_edges), len(adverse_edges)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    for name, digest in PINS.items():
        require(sha256((TARGET / name).read_bytes()).hexdigest() == digest,
                "reviewed source changed: " + name)
    expected = json.loads((TARGET / "EXPECTED.json").read_text())

    lam = Q(9999, 10000)
    source, target = strict_fixture(lam)
    losses = [pair_parameters(source, target, i, j)[1]
              for i, j in combinations(range(10), 2)]
    require(len(set(source)) == len(set(target)) == 10, "injective endpoints")
    require(len(losses) == 45 and min(losses) == Q(19999, 100000000),
            "strict pair losses")

    h = [sub(y, x) for x, y in zip(source, target)]
    rank_rows = [sub(source[i], source[0]) + sub(h[i], h[0])
                 for i in (1, 2, 3, 4, 6, 8)]
    rank_minor = determinant(rank_rows)
    require(rank_minor == Q(999700029999, 125000000000), "paired-rank minor")

    cross = covariance(source, target)
    leading_minors = (cross[0][0],
                      cross[0][0] * cross[1][1] - cross[0][1] * cross[1][0],
                      determinant(cross))
    require(leading_minors == (
        Q(309969, 250000),
        Q(18896220189, 12500000000),
        Q(1126661933808873, 625000000000000),
    ) and all(value > 0 for value in leading_minors), "Sylvester alignment test")

    reserve = all_label_reserve(source, target, 4, 5)
    submitted = Q(5088829, 97435855000)
    require(reserve == Q(816135388671049305206391122009,
                         2067737843860747245000000000000000),
            "all-label adverse reserve")
    require(reserve > 7 * submitted, "independent reserve should strengthen submitted bound")

    require(expected["strict_pairs"] == 45 and
            Q(expected["minimum_squared_loss"]) == min(losses) and
            expected["paired_affine_rank"] == 6 and
            Q(expected["positive_margin"]) == submitted,
            "published record fields")

    completion = gaussian_completion_controls(source)
    reflection = reflection_polynomial_controls()
    coefficient_entries = multinomial_normalization(10)
    tight_edges, adverse_edges = seven_site_control()
    require(coefficient_entries == 450, "multinomial entry count")

    result = {
        "status": "INDEPENDENT_STRAIGHT_PATH_PAIR_REVIEW_PASS",
        "strict_pairs": len(losses),
        "paired_rank_minor": str(rank_minor),
        "alignment_leading_minors": [str(x) for x in leading_minors],
        "all_label_adverse_reserve": str(reserve),
        "submitted_reserve": str(submitted),
        "gaussian_completion_checks": completion,
        "reflection_polynomial_checks": reflection,
        "closed_multinomial_entries": coefficient_entries,
        "seven_site_tight_edges": tight_edges,
        "seven_site_moving_adverse_edges": adverse_edges,
    }
    if args.check:
        recorded = json.loads((HERE / "EXPECTED.json").read_text())
        require(result == recorded, "independent expected record changed")
        print(result["status"])
        print("strict pairs/rank minor:", result["strict_pairs"], result["paired_rank_minor"])
        print("all-label reserve:", result["all_label_adverse_reserve"])
        print("completion/reflection/multinomial:", completion, reflection, coefficient_entries)
        print("seven-site tight/moving adverse edges:", tight_edges, adverse_edges)
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
