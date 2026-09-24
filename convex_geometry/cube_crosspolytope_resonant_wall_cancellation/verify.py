#!/usr/bin/env python3
"""Exact verifier for the resonant missing-wall families."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations, product
from json import dumps


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def fraction_text(value: F) -> str:
    value = F(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def wall_labels(
    weights: tuple[F, ...], boundary_excess: F
) -> dict[F, list[tuple[int, tuple[int, ...]]]]:
    answer: dict[F, list[tuple[int, tuple[int, ...]]]] = {}
    size = len(weights)
    for supplier, weight in enumerate(weights):
        others = [index for index in range(size) if index != supplier]
        for mask in range(1 << len(others)):
            tail = tuple(
                index
                for bit, index in enumerate(others)
                if (mask >> bit) & 1
            )
            wall = (
                boundary_excess * (1 / weight - 1)
                + 2
                * sum((weights[index] for index in tail), F(0))
                / weight
            )
            answer.setdefault(wall, []).append((supplier, tail))
    return answer


def label_jump(
    weights: tuple[F, ...], supplier: int, tail: tuple[int, ...]
) -> F:
    """Simple-pole jump; used only when supplier weight is unique off tail."""
    weight = weights[supplier]
    denominator = F(1)
    for entry in weights:
        denominator *= entry
    for index, entry in enumerate(weights):
        if index != supplier and index not in tail:
            denominator *= weight - entry
    for index in tail:
        denominator *= weight + weights[index]
    require(denominator != 0, "label does not have a simple supplier pole")
    return (
        (-1) ** len(tail)
        * weight ** (2 * len(weights) - 2)
        / denominator
    )


def family_parameters(multiplicity: int, parameter: F, branch: str) -> tuple[F, F, F]:
    a = parameter**multiplicity
    x = parameter ** (2 * multiplicity + 2)
    if branch == "upper":
        c = (a + x) / (1 - x)
    else:
        require(multiplicity % 2 == 0 and branch == "lower", "invalid branch")
        c = (a - x) / (1 + x)
    boundary_excess = 2 * multiplicity * a * c / (1 - a)
    return a, c, boundary_excess


def intersect(
    first: tuple[F, F, F], second: tuple[F, F, F]
) -> tuple[F, F] | None:
    a, b, c = first
    d, e, f = second
    determinant = a * e - b * d
    if determinant == 0:
        return None
    return (
        (c * e - b * f) / determinant,
        (a * f - c * d) / determinant,
    )


def cross(
    origin: tuple[F, F], first: tuple[F, F], second: tuple[F, F]
) -> F:
    return (
        (first[0] - origin[0]) * (second[1] - origin[1])
        - (first[1] - origin[1]) * (second[0] - origin[0])
    )


def convex_hull(points: set[tuple[F, F]]) -> list[tuple[F, F]]:
    ordered = sorted(points)
    if len(ordered) <= 2:
        return ordered
    lower: list[tuple[F, F]] = []
    for point in ordered:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper: list[tuple[F, F]] = []
    for point in reversed(ordered):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]


def direct_section_n3(
    normal: tuple[F, F, F], offset: F, radius: F
) -> F:
    pivot = next(index for index, entry in enumerate(normal) if entry)
    order = [index for index in range(3) if index != pivot] + [pivot]
    first_weight, second_weight, pivot_weight = (
        normal[index] for index in order
    )
    inequalities: list[tuple[F, F, F]] = []
    for raw_signs in product((-1, 0, 1), repeat=3):
        signs = tuple(raw_signs[index] for index in order)
        support_size = sum(sign != 0 for sign in signs)
        first = F(signs[0]) - F(signs[2]) * first_weight / pivot_weight
        second = F(signs[1]) - F(signs[2]) * second_weight / pivot_weight
        bound = F(radius) + support_size - F(signs[2]) * F(offset) / pivot_weight
        if first == second == 0:
            if bound < 0:
                return F(0)
        else:
            inequalities.append((first, second, bound))
    vertices: set[tuple[F, F]] = set()
    for first, second in combinations(inequalities, 2):
        point = intersect(first, second)
        if point is not None and all(
            a * point[0] + b * point[1] <= c
            for a, b, c in inequalities
        ):
            vertices.add(point)
    hull = convex_hull(vertices)
    if len(hull) < 3:
        return F(0)
    twice_area = sum(
        x1 * y2 - y1 * x2
        for (x1, y1), (x2, y2) in zip(hull, hull[1:] + hull[:1])
    )
    return abs(twice_area) / (2 * abs(pivot_weight))


def fit_quadratic(samples: list[tuple[F, F]]) -> tuple[F, F, F]:
    matrix = [[F(1), x, x * x, y] for x, y in samples]
    for pivot in range(3):
        row = next(row for row in range(pivot, 3) if matrix[row][pivot])
        matrix[pivot], matrix[row] = matrix[row], matrix[pivot]
        divisor = matrix[pivot][pivot]
        matrix[pivot] = [entry / divisor for entry in matrix[pivot]]
        for row in range(3):
            if row == pivot:
                continue
            multiple = matrix[row][pivot]
            matrix[row] = [
                first - multiple * second
                for first, second in zip(matrix[row], matrix[pivot])
            ]
    return tuple(matrix[index][3] for index in range(3))


def polygon_sides(
    normal: tuple[F, F, F], boundary_excess: F, wall: F
) -> tuple[tuple[F, F, F], tuple[F, F, F], int]:
    maximum = max(abs(entry) for entry in normal)
    weights = tuple(abs(entry) / maximum for entry in normal)
    support = sum(abs(entry) for entry in normal)
    offset = support + maximum * boundary_excess
    walls = sorted(wall_labels(weights, boundary_excess))
    position = walls.index(wall)
    distances = []
    if position:
        distances.append(wall - walls[position - 1])
    if position + 1 < len(walls):
        distances.append(walls[position + 1] - wall)
    step = min(distances) / 10
    polynomials = []
    evaluations = 0
    for sign in (-1, 1):
        samples = []
        for multiple in (1, 2, 3):
            displacement = sign * multiple * step
            value = direct_section_n3(
                normal,
                offset,
                boundary_excess + wall + displacement,
            )
            samples.append((displacement, value))
            evaluations += 1
        polynomials.append(fit_quadratic(samples))
    return polynomials[0], polynomials[1], evaluations


def main() -> None:
    parameters = (F(1, 2), F(2, 5), F(1, 3), F(1, 4))
    family_checks = 0
    label_exhaustion_checks = 0
    coefficient_cancellation_checks = 0
    family_summary = []
    for multiplicity in range(1, 11):
        for parameter in parameters:
            branches = ["upper"]
            if multiplicity % 2 == 0:
                branches.append("lower")
            for branch in branches:
                a, c, boundary_excess = family_parameters(
                    multiplicity, parameter, branch
                )
                require(0 < a < 1 and 0 < c < 1 and a != c, "invalid weights")
                weights = (F(1), a) + (c,) * multiplicity
                wall = 2 * multiplicity * c
                labels = wall_labels(weights, boundary_excess)[wall]
                expected = {
                    (0, tuple(range(2, multiplicity + 2))),
                    (1, ()),
                }
                require(set(labels) == expected, "unexpected third wall label")
                jumps = [label_jump(weights, supplier, tail) for supplier, tail in labels]
                require(all(jump != 0 for jump in jumps), "zero individual jump")
                require(sum(jumps, F(0)) == 0, "wall coefficients did not cancel")
                relation_left = ((a - c) / (1 + c)) ** multiplicity
                relation_right = (-1) ** multiplicity * a ** (2 * multiplicity + 2)
                require(relation_left == relation_right, "classification identity failed")
                family_checks += 1
                label_exhaustion_checks += 1
                coefficient_cancellation_checks += 1
                if parameter == F(1, 2):
                    family_summary.append({
                        "active_coordinates": multiplicity + 2,
                        "branch": branch,
                        "a": fraction_text(a),
                        "c": fraction_text(c),
                        "B": fraction_text(boundary_excess),
                        "missing_wall": fraction_text(wall),
                    })

    polygon_identity_checks = 0
    polygon_evaluations = 0
    representative = None
    for parameter in parameters:
        a, c, boundary_excess = family_parameters(1, parameter, "upper")
        wall = 2 * c
        for scale in (F(1), F(7)):
            normal = (scale, -scale * c, scale * a)
            left, right, evaluations = polygon_sides(normal, boundary_excess, wall)
            require(left == right, "direct polygon retained the missing wall")
            polygon_identity_checks += 1
            polygon_evaluations += evaluations
            if parameter == F(1, 2) and scale == 1:
                representative = {
                    "normal": [fraction_text(entry) for entry in normal],
                    "B": fraction_text(boundary_excess),
                    "candidate_wall": fraction_text(wall),
                    "shared_polynomial_in_s_minus_wall": [
                        fraction_text(entry) for entry in left
                    ],
                }

    control_weights = (F(1), F(1, 2), F(2, 3))
    control_B = F(4, 3)
    control_wall = F(4, 3)
    control_labels = wall_labels(control_weights, control_B)[control_wall]
    require(len(control_labels) == 2, "control is not a two-label resonance")
    control_jump = sum(
        (label_jump(control_weights, supplier, tail) for supplier, tail in control_labels),
        F(0),
    )
    require(control_jump != 0, "control unexpectedly canceled")
    control_left, control_right, evaluations = polygon_sides(
        (F(1), F(-2, 3), F(1, 2)), control_B, control_wall
    )
    polygon_evaluations += evaluations
    require(control_left[:2] == control_right[:2], "control lost lower smoothness")
    require(2 * (control_right[2] - control_left[2]) == control_jump,
            "control jump mismatch")

    result = {
        "status": "RESONANT_WALL_CANCELLATION_VERIFIED",
        "exact_arithmetic": "fractions.Fraction",
        "family_instances_checked": family_checks,
        "exact_two_label_exhaustion_checks": label_exhaustion_checks,
        "exact_coefficient_cancellation_checks": coefficient_cancellation_checks,
        "direct_polygon_missing_wall_checks": polygon_identity_checks,
        "direct_polygon_section_evaluations": polygon_evaluations,
        "family_summary_at_t_one_half": family_summary,
        "smallest_representative": representative,
        "noncancelling_resonant_control": {
            "weights": [fraction_text(entry) for entry in control_weights],
            "B": fraction_text(control_B),
            "candidate_wall": fraction_text(control_wall),
            "left_polynomial": [fraction_text(entry) for entry in control_left],
            "right_polynomial": [fraction_text(entry) for entry in control_right],
            "second_derivative_jump": fraction_text(control_jump),
        },
        "scope": (
            "PROOF.md constructs rational missing-wall families for every "
            "active dimension q >= 3 and classifies the displayed two-label "
            "collision pattern in the three-weight-level ansatz."
        ),
    }
    print(dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
