#!/usr/bin/env python3
"""Exact checks for the arbitrary-normal first-ray classification.

Three distinct calculations are compared:

1. the truncated generating function C_w(t);
2. direct enumeration of all plus/inactive coordinate states and their
   simplex moments;
3. for N=3, exact rational reconstruction of the original section polygon
   from all 27 defining halfspaces.

Only Python integers and fractions.Fraction are used.
"""

from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
from json import dumps
from math import comb, factorial


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def fraction_text(value: F) -> str:
    value = F(value)
    return str(value.numerator) if value.denominator == 1 else str(value)


def multiply_series(left: list[F], right: list[F], degree: int) -> list[F]:
    answer = [F(0)] * (degree + 1)
    for i, first in enumerate(left):
        for j, second in enumerate(right):
            if i + j <= degree:
                answer[i + j] += first * second
    return answer


def active_coefficients(weights: tuple[F, ...]) -> list[F]:
    """Return c_0,...,c_{k-1} from the displayed C_w(t)."""
    weights = tuple(F(weight) for weight in weights)
    require(weights and max(weights) == 1 and min(weights) > 0,
            "active weights must lie in (0,1] and have maximum one")
    size = len(weights)
    maximum_count = sum(weight == 1 for weight in weights)
    degree = maximum_count - 1
    coefficients = [F(comb(size + j - 1, j)) for j in range(degree + 1)]
    scale = F(1)
    for weight in weights:
        scale /= weight
        if weight < 1:
            gap = 1 - weight
            scale /= gap
            inverse = [(-weight / gap) ** j for j in range(degree + 1)]
            coefficients = multiply_series(coefficients, inverse, degree)
    return [scale * coefficient for coefficient in coefficients]


def formula_polynomial(weights: tuple[F, ...], zero_count: int = 0) -> dict[tuple[int, int], F]:
    """Map (B exponent, slack exponent) to the theorem coefficient."""
    size = len(weights)
    maximum_count = sum(weight == 1 for weight in weights)
    answer: dict[tuple[int, int], F] = {}
    for j, coefficient in enumerate(active_coefficients(weights)):
        b_power = maximum_count - 1 - j
        base_slack = size - maximum_count + j
        for tail_count in range(zero_count + 1):
            slack_power = base_slack + tail_count
            value = (
                F(2 ** zero_count * comb(zero_count, tail_count))
                * coefficient
                / (factorial(b_power) * factorial(slack_power))
            )
            answer[b_power, slack_power] = (
                answer.get((b_power, slack_power), F(0)) + value
            )
    return {key: value for key, value in answer.items() if value}


def complete_homogeneous(parameters: list[F], degree: int) -> list[F]:
    coefficients = [F(1)] + [F(0)] * degree
    for parameter in parameters:
        coefficients = multiply_series(
            coefficients,
            [parameter ** j for j in range(degree + 1)],
            degree,
        )
    return coefficients


def state_polynomial(weights: tuple[F, ...]) -> dict[tuple[int, int], F]:
    """Independent plus/inactive state enumeration for active coordinates."""
    weights = tuple(F(weight) for weight in weights)
    size = len(weights)
    answer: dict[tuple[int, int], F] = {}
    for plus_mask in product((False, True), repeat=size):
        maximal_plus = sum(
            is_plus and weight == 1
            for is_plus, weight in zip(plus_mask, weights)
        )
        if maximal_plus == 0:
            continue
        jacobian = F(1)
        parameters: list[F] = []
        for is_plus, weight in zip(plus_mask, weights):
            if weight == 1:
                if not is_plus:
                    parameters.append(F(1))
            elif is_plus:
                jacobian /= 1 - weight
                parameters.append(-weight / (1 - weight))
            else:
                jacobian /= weight
                parameters.append(F(1))
        moments = complete_homogeneous(parameters, maximal_plus - 1)
        variable_count = size - maximal_plus
        for moment_degree, moment in enumerate(moments):
            b_power = maximal_plus - 1 - moment_degree
            slack_power = variable_count + moment_degree
            value = (
                jacobian * moment
                / (factorial(b_power) * factorial(slack_power))
            )
            answer[b_power, slack_power] = (
                answer.get((b_power, slack_power), F(0)) + value
            )
    return {key: value for key, value in answer.items() if value}


def chamber_threshold(weights: tuple[F, ...], boundary_excess: F) -> F | None:
    weights = tuple(F(weight) for weight in weights if weight)
    if len(weights) == 1:
        return None
    negative_tail = 2 * min(weights)
    submaximal = [weight for weight in weights if weight < 1]
    if not submaximal:
        return negative_tail
    next_weight = max(submaximal)
    missing_maximum = F(boundary_excess) * (1 / next_weight - 1)
    return min(negative_tail, missing_maximum)


def predicted_section(
    normal: tuple[F, ...], offset: F, radius: F
) -> F:
    magnitudes = tuple(abs(F(entry)) for entry in normal)
    maximum = max(magnitudes)
    support = sum(magnitudes)
    boundary_excess = (abs(F(offset)) - support) / maximum
    slack = F(radius) - boundary_excess
    require(boundary_excess > 0 and slack >= 0, "point is not on the ray chamber")
    active = tuple(weight / maximum for weight in magnitudes if weight)
    zero_count = len(normal) - len(active)
    polynomial = formula_polynomial(active, zero_count)
    return sum(
        coefficient * boundary_excess ** b_power * slack ** slack_power
        for (b_power, slack_power), coefficient in polynomial.items()
    ) / maximum


def intersect(
    first: tuple[F, F, F], second: tuple[F, F, F]
) -> tuple[F, F] | None:
    a, b, c = first
    d, e, f = second
    determinant = a * e - b * d
    if determinant == 0:
        return None
    return ((c * e - b * f) / determinant,
            (a * f - c * d) / determinant)


def cross(origin: tuple[F, F], a: tuple[F, F], b: tuple[F, F]) -> F:
    return ((a[0] - origin[0]) * (b[1] - origin[1])
            - (a[1] - origin[1]) * (b[0] - origin[0]))


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


def polygon_area(vertices: list[tuple[F, F]]) -> F:
    if len(vertices) < 3:
        return F(0)
    twice = sum(
        x1 * y2 - y1 * x2
        for (x1, y1), (x2, y2) in zip(vertices, vertices[1:] + vertices[:1])
    )
    return abs(twice) / 2


def direct_section_n3(
    normal: tuple[F, F, F], offset: F, radius: F
) -> tuple[F, int]:
    """Original delta-normalized section from its exact H-polygon."""
    normal = tuple(F(entry) for entry in normal)
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
            require(bound >= 0, "empty section encountered")
        else:
            inequalities.append((first, second, bound))

    vertices: set[tuple[F, F]] = set()
    for first, second in combinations(inequalities, 2):
        point = intersect(first, second)
        if point is None:
            continue
        x, y = point
        if all(a * x + b * y <= c for a, b, c in inequalities):
            vertices.add(point)
    hull = convex_hull(vertices)
    return polygon_area(hull) / abs(pivot_weight), len(hull)


def legendre_value(degree: int, argument: F) -> F:
    if degree == 0:
        return F(1)
    previous, current = F(1), F(argument)
    for n in range(1, degree):
        following = ((2 * n + 1) * argument * current - n * previous) / (n + 1)
        previous, current = current, following
    return current


def main() -> None:
    state_checks = 0
    weight_pool = (F(1, 2), F(2, 3), F(3, 4), F(1, 3))
    for size in range(1, 9):
        for maximum_count in range(1, size + 1):
            weights = (F(1),) * maximum_count + tuple(
                weight_pool[index % len(weight_pool)]
                for index in range(size - maximum_count)
            )
            require(
                formula_polynomial(weights) == state_polynomial(weights),
                f"state/generating-function mismatch for {weights}",
            )
            state_checks += 1

    legendre_checks = 0
    for size in range(1, 16):
        weights = (F(1),) * size
        for boundary_excess, slack in ((F(1), F(0)), (F(2), F(1, 3)), (F(5, 2), F(2))):
            polynomial = formula_polynomial(weights)
            section = sum(
                coefficient * boundary_excess ** b_power * slack ** slack_power
                for (b_power, slack_power), coefficient in polynomial.items()
            )
            expected = (
                boundary_excess ** (size - 1) / factorial(size - 1)
                * legendre_value(size - 1, 1 + 2 * slack / boundary_excess)
            )
            require(section == expected, "Legendre specialization failed")
            legendre_checks += 1

    geometric_specs = (
        ((F(1), F(2, 3), F(1, 3)), F(2), (F(1, 10), F(2, 3))),
        ((F(1), F(1), F(1, 2)), F(2), (F(1, 4), F(1))),
        ((F(1), F(1), F(9, 10)), F(1), (F(1, 20), F(1, 9))),
        ((F(2), F(-2), F(2)), F(3, 2), (F(0), F(1, 2), F(2))),
        ((F(3), F(3), F(0)), F(2), (F(0), F(1, 2), F(2))),
        ((F(5), F(0), F(0)), F(2), (F(0), F(1, 2), F(3))),
    )
    geometry = []
    geometric_checks = 0
    for case_index, (normal, boundary_excess, slacks) in enumerate(geometric_specs):
        maximum = max(abs(entry) for entry in normal)
        support = sum(abs(entry) for entry in normal)
        sign = -1 if case_index == 3 else 1
        offset = sign * (support + maximum * boundary_excess)
        normalized_active = tuple(
            abs(entry) / maximum for entry in normal if entry
        )
        threshold = chamber_threshold(normalized_active, boundary_excess)
        rows = []
        for slack in slacks:
            require(threshold is None or slack <= threshold,
                    "geometric test outside first chamber")
            radius = boundary_excess + slack
            direct, vertices = direct_section_n3(normal, offset, radius)
            predicted = predicted_section(normal, offset, radius)
            require(direct == predicted, "exact H-polygon mismatch")
            rows.append({
                "slack": fraction_text(slack),
                "section": fraction_text(direct),
                "vertices": vertices,
            })
            geometric_checks += 1
        geometry.append({
            "normal": [fraction_text(entry) for entry in normal],
            "B": fraction_text(boundary_excess),
            "threshold": (
                "infinity" if threshold is None else fraction_text(threshold)
            ),
            "samples": rows,
        })

    outside_specs = (
        ((F(1), F(2, 3), F(1, 3)), F(2), F(3, 4)),
        ((F(1), F(1), F(9, 10)), F(1), F(1, 8)),
        ((F(1), F(1), F(1)), F(2), F(9, 4)),
    )
    outside = []
    for normal, boundary_excess, slack in outside_specs:
        maximum = max(abs(entry) for entry in normal)
        support = sum(abs(entry) for entry in normal)
        offset = support + maximum * boundary_excess
        radius = boundary_excess + slack
        direct, vertices = direct_section_n3(normal, offset, radius)
        predicted = predicted_section(normal, offset, radius)
        require(direct != predicted, "negative control did not cross a threshold")
        outside.append({
            "normal": [fraction_text(entry) for entry in normal],
            "slack": fraction_text(slack),
            "direct": fraction_text(direct),
            "local_polynomial": fraction_text(predicted),
            "vertices": vertices,
        })

    onset_checks = 0
    for size in range(2, 13):
        for maximum_count in range(1, size + 1):
            weights = (F(1),) * maximum_count + (F(1, 2),) * (size - maximum_count)
            polynomial = formula_polynomial(weights)
            minimum_slack = min(slack_power for _, slack_power in polynomial)
            require(minimum_slack == size - maximum_count,
                    "wrong onset vanishing order")
            leading = polynomial[maximum_count - 1, size - maximum_count]
            c_zero = active_coefficients(weights)[0]
            expected = c_zero / (
                factorial(maximum_count - 1) * factorial(size - maximum_count)
            )
            require(leading == expected, "wrong onset derivative coefficient")
            onset_checks += 1

    scale_normal = (F(1), F(-1), F(1, 2))
    scale_boundary = F(3, 2)
    scale_slack = F(1, 3)
    support = sum(abs(entry) for entry in scale_normal)
    scale_offset = support + scale_boundary
    base = predicted_section(
        scale_normal, scale_offset, scale_boundary + scale_slack
    )
    multiplier = F(7, 3)
    scaled = predicted_section(
        tuple(multiplier * entry for entry in scale_normal),
        multiplier * scale_offset,
        scale_boundary + scale_slack,
    )
    require(scaled == base / multiplier, "delta scaling failed")

    result = {
        "status": "WEIGHTED_RAY_BOUNDARY_CLASSIFICATION_VERIFIED",
        "exact_arithmetic": "fractions.Fraction",
        "state_vs_generating_function_checks": state_checks,
        "legendre_recurrence_checks": legendre_checks,
        "onset_order_checks": onset_checks,
        "exact_h_polygon_checks": geometric_checks,
        "geometric_samples": geometry,
        "outside_chamber_negative_controls": outside,
        "normal_scaling_check": {
            "multiplier": fraction_text(multiplier),
            "base": fraction_text(base),
            "scaled": fraction_text(scaled),
        },
    }
    record = dumps(result, indent=2, sort_keys=True) + "\n"
    print(record, end="")


if __name__ == "__main__":
    main()
