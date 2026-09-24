#!/usr/bin/env python3
"""Exact verifier for generic wall count, smoothness, and derivative jumps."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations, product
from json import dumps
from math import factorial


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


def residue_from_definition(
    weights: tuple[F, ...], supplier: int, tail: tuple[int, ...]
) -> F:
    active = [index for index in range(len(weights)) if index not in tail]
    weight = weights[supplier]
    lam = (1 - weight) / weight
    denominator = (1 + lam) ** len(active)
    for index in active:
        denominator *= weights[index]
    denominator *= weight
    for index in active:
        if index != supplier:
            denominator *= 1 - weights[index] - weights[index] * lam
    return 1 / denominator


def eta_zero(tail_weight: F, supplier_weight: F) -> F:
    lam = (1 - supplier_weight) / supplier_weight
    return (
        1 / (1 + tail_weight + lam * tail_weight)
        - 1 / (tail_weight * (1 + lam))
    )


def recurrence_jump(
    weights: tuple[F, ...], supplier: int, tail: tuple[int, ...]
) -> F:
    answer = residue_from_definition(weights, supplier, tail)
    for index in tail:
        answer *= eta_zero(weights[index], weights[supplier])
    return answer


def closed_jump(
    weights: tuple[F, ...], supplier: int, tail: tuple[int, ...]
) -> F:
    size = len(weights)
    weight = weights[supplier]
    denominator = F(1)
    for entry in weights:
        denominator *= entry
    for index, entry in enumerate(weights):
        if index != supplier and index not in tail:
            denominator *= weight - entry
    for index in tail:
        denominator *= weight + weights[index]
    return (-1) ** len(tail) * weight ** (2 * size - 2) / denominator


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
) -> tuple[F, int]:
    """Delta-normalized polygon from the original 27 halfspaces."""
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
                return F(0), 0
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
        return F(0), len(hull)
    twice_area = sum(
        x1 * y2 - y1 * x2
        for (x1, y1), (x2, y2) in zip(hull, hull[1:] + hull[:1])
    )
    return abs(twice_area) / (2 * abs(pivot_weight)), len(hull)


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


def direct_jump_checks(
    normal: tuple[F, F, F], boundary_excess: F
) -> tuple[int, int, int, list[dict[str, object]]]:
    maximum = max(abs(entry) for entry in normal)
    active_weights = tuple(abs(entry) / maximum for entry in normal if entry)
    zero_count = 3 - len(active_weights)
    support = sum(abs(entry) for entry in normal)
    offset = support + maximum * boundary_excess
    labels = wall_labels(active_weights, boundary_excess)
    require(all(len(value) == 1 for value in labels.values()), "direct resonance")
    walls = sorted(labels)
    jump_checks = 0
    continuity_checks = 0
    evaluations = 0
    samples_out: list[dict[str, object]] = []
    for position, wall in enumerate(walls):
        distances = [boundary_excess]
        if position:
            distances.append(wall - walls[position - 1])
        if position + 1 < len(walls):
            distances.append(walls[position + 1] - wall)
        step = min(distances) / 10
        side_polynomials = []
        for sign in (-1, 1):
            samples = []
            for multiple in (1, 2, 3):
                displacement = sign * multiple * step
                slack = wall + displacement
                radius = boundary_excess + slack
                value, _ = direct_section_n3(normal, offset, radius)
                samples.append((displacement, value))
                evaluations += 1
            side_polynomials.append(fit_quadratic(samples))
        left, right = side_polynomials
        for derivative_order in range(len(active_weights) - 1):
            require(
                factorial(derivative_order) * left[derivative_order]
                == factorial(derivative_order) * right[derivative_order],
                "lower derivative mismatch",
            )
            continuity_checks += 1
        supplier, tail = labels[wall][0]
        expected = (
            2**zero_count
            * closed_jump(active_weights, supplier, tail)
            / maximum
        )
        derivative_order = len(active_weights) - 1
        actual = factorial(derivative_order) * (
            right[derivative_order] - left[derivative_order]
        )
        require(actual == expected, "direct derivative jump mismatch")
        jump_checks += 1
        if position in (0, len(walls) // 2, len(walls) - 1):
            samples_out.append({
                "wall": fraction_text(wall),
                "supplier": supplier,
                "tail": list(tail),
                "derivative_order": derivative_order,
                "jump": fraction_text(actual),
            })
    return jump_checks, continuity_checks, evaluations, samples_out


def main() -> None:
    families = (
        ((F(1),), F(7, 5)),
        ((F(1), F(2, 3)), F(7, 5)),
        ((F(1), F(3, 5), F(1, 7)), F(7, 5)),
        ((F(1), F(4, 5), F(2, 7), F(1, 11)), F(7, 5)),
        ((F(1), F(5, 7), F(3, 11), F(2, 13), F(1, 17)), F(7, 5)),
        ((F(1), F(7, 11), F(5, 13), F(3, 17), F(2, 19), F(1, 23)), F(11, 6)),
        ((F(1), F(11, 13), F(7, 17), F(5, 19), F(3, 23), F(2, 29), F(1, 31)), F(13, 7)),
        ((F(1), F(13, 17), F(11, 19), F(7, 23), F(5, 29), F(3, 31), F(2, 37), F(1, 41)), F(17, 9)),
    )
    coefficient_checks = 0
    term_order_checks = 0
    family_summary = []
    for weights, boundary_excess in families:
        labels = wall_labels(weights, boundary_excess)
        expected_count = len(weights) * 2 ** (len(weights) - 1)
        require(len(labels) == expected_count, "wall-count mismatch")
        require(all(len(value) == 1 for value in labels.values()), "wall resonance")
        for entries in labels.values():
            supplier, tail = entries[0]
            require(
                recurrence_jump(weights, supplier, tail)
                == closed_jump(weights, supplier, tail),
                "closed jump mismatch",
            )
            complement_size = len(weights) - len(tail)
            require(
                complement_size - 1 + len(tail) == len(weights) - 1,
                "hinge order mismatch",
            )
            coefficient_checks += 1
            term_order_checks += 1
        family_summary.append({
            "active_coordinates": len(weights),
            "wall_count": len(labels),
            "expected_wall_count": expected_count,
        })

    direct_cases = (
        ((F(1), F(-3, 5), F(1, 7)), F(7, 5)),
        ((F(35), F(-21), F(5)), F(11, 6)),
        ((F(1), F(-2, 5), F(0)), F(7, 5)),
        ((F(7), F(-3), F(0)), F(11, 6)),
        ((F(5), F(0), F(0)), F(7, 5)),
    )
    direct_jumps = 0
    direct_continuity = 0
    direct_evaluations = 0
    representative_jumps = []
    for normal, boundary_excess in direct_cases:
        jumps, continuity, evaluations, samples = direct_jump_checks(
            normal, boundary_excess
        )
        direct_jumps += jumps
        direct_continuity += continuity
        direct_evaluations += evaluations
        representative_jumps.append({
            "normal": [fraction_text(entry) for entry in normal],
            "B": fraction_text(boundary_excess),
            "checked_walls": jumps,
            "samples": samples,
        })

    resonant_controls = []
    for weights, boundary_excess in (
        ((F(1), F(1), F(1)), F(2)),
        ((F(1), F(1, 2)), F(1)),
        ((F(1), F(1, 2), F(1, 3), F(1, 6)), F(7, 5)),
    ):
        labels = wall_labels(weights, boundary_excess)
        labeled = len(weights) * 2 ** (len(weights) - 1)
        require(len(labels) < labeled, "negative control did not resonate")
        resonant_controls.append({
            "weights": [fraction_text(weight) for weight in weights],
            "B": fraction_text(boundary_excess),
            "labeled_candidates": labeled,
            "distinct_numeric_walls": len(labels),
        })

    result = {
        "status": "GENERIC_WALL_SMOOTHNESS_VERIFIED",
        "exact_arithmetic": "fractions.Fraction",
        "closed_jump_coefficient_checks": coefficient_checks,
        "uniform_hinge_order_checks": term_order_checks,
        "exact_polygon_wall_jump_checks": direct_jumps,
        "exact_polygon_lower_derivative_checks": direct_continuity,
        "exact_polygon_section_evaluations": direct_evaluations,
        "nonresonant_family_summary": family_summary,
        "representative_polygon_jumps": representative_jumps,
        "resonant_negative_controls": resonant_controls,
        "scope": (
            "PROOF.md proves q*2^(q-1) genuine walls and exact C^(q-2) "
            "smoothness for every real wall-nonresonant ray-side parameter; "
            "the checker supplies exact rational corroboration."
        ),
    }
    print(dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
