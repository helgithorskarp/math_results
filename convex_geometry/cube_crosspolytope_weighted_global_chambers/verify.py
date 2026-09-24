#!/usr/bin/env python3
"""Exact verifier for the global arbitrary-normal ray-chamber formula."""

from __future__ import annotations

from fractions import Fraction as F
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


def invert_series(denominator: list[F]) -> list[F]:
    require(denominator and denominator[0], "noninvertible series")
    inverse = [F(0)] * len(denominator)
    inverse[0] = 1 / denominator[0]
    for degree in range(1, len(denominator)):
        inverse[degree] = -sum(
            denominator[index] * inverse[degree - index]
            for index in range(1, degree + 1)
        ) / denominator[0]
    return inverse


def plus_principal_parts(weights: tuple[F, ...]) -> list[tuple[F, int, F]]:
    """Return (lambda, pole order, coefficient) for all plus poles."""
    weights = tuple(F(weight) for weight in weights)
    size = len(weights)
    require(size and min(weights) > 0, "nonempty positive weight set")
    answer: list[tuple[F, int, F]] = []
    for target in sorted(set(weights), reverse=True):
        multiplicity = weights.count(target)
        degree = multiplicity - 1
        root = (target - 1) / target
        denominator = [F(1)] + [F(0)] * degree
        for _ in range(size):
            denominator = multiply_series(
                denominator, [1 - root, F(-1)], degree
            )
        scale = F(1)
        for weight in weights:
            scale *= weight
        scale *= target ** multiplicity
        for weight in weights:
            if weight != target:
                denominator = multiply_series(
                    denominator,
                    [1 - weight + weight * root, weight],
                    degree,
                )
        inverse = invert_series([scale * value for value in denominator])
        lam = (1 - target) / target
        for order in range(1, multiplicity + 1):
            answer.append((lam, order, inverse[multiplicity - order]))
    return answer


def inactive_principal_parts(weights: tuple[F, ...]) -> list[tuple[int, F]]:
    """Principal part at t=1, expressed in powers of (1-t)^(-order)."""
    weights = tuple(F(weight) for weight in weights)
    size = len(weights)
    denominator = [F(1)] + [F(0)] * (size - 1)
    scale = F(1)
    for weight in weights:
        scale *= weight
        denominator = multiply_series(
            denominator, [F(1), -weight], size - 1
        )
    inverse = invert_series([scale * value for value in denominator])
    return [
        (order, inverse[size - order])
        for order in range(1, size + 1)
    ]


def rational_baseline_transform(weights: tuple[F, ...], value: F) -> F:
    answer = (1 - value) ** len(weights)
    for weight in weights:
        answer *= weight * (1 - weight + weight * value)
    return 1 / answer


# A term represents coefficient*(B+bshift)^p*(s-lambda*B-c)_+^r.
Term = tuple[F, int, F, F, F, int]


def compact_terms(terms: list[Term]) -> list[Term]:
    coefficients: dict[tuple[int, F, F, F, int], F] = {}
    for coefficient, power, shift, lam, wall_shift, slack_power in terms:
        key = (power, shift, lam, wall_shift, slack_power)
        coefficients[key] = coefficients.get(key, F(0)) + coefficient
    return [
        (coefficient, *key)
        for key, coefficient in sorted(coefficients.items(), key=str)
        if coefficient
    ]


def baseline_terms(weights: tuple[F, ...]) -> list[Term]:
    size = len(weights)
    answer: list[Term] = []
    for lam, order, coefficient in plus_principal_parts(weights):
        b_power = order - 1
        slack_power = size - order
        answer.append((
            coefficient / (factorial(b_power) * factorial(slack_power)),
            b_power, F(0), lam, F(0), slack_power,
        ))
    return answer


def tail_replace(terms: list[Term], weight: F) -> list[Term]:
    weight = F(weight)
    answer: list[Term] = []
    for coefficient, power, shift, lam, wall_shift, slack_power in terms:
        for moment in range(power + 1):
            eta = (
                weight ** moment
                / (1 + weight + lam * weight) ** (moment + 1)
                - 1 / (weight * (1 + lam) ** (moment + 1))
            )
            factor = (
                comb(power, moment)
                * eta
                * F(
                    factorial(moment) * factorial(slack_power),
                    factorial(moment + slack_power + 1),
                )
            )
            answer.append((
                coefficient * factor,
                power - moment,
                shift + 2 * weight,
                lam,
                wall_shift + 2 * weight * (1 + lam),
                slack_power + moment + 1,
            ))
    return compact_terms(answer)


def active_global_terms(weights: tuple[F, ...]) -> list[Term]:
    weights = tuple(F(weight) for weight in weights)
    size = len(weights)
    answer: list[Term] = []
    for mask in range(1 << size):
        if mask == (1 << size) - 1:
            continue
        remaining = tuple(
            weights[index]
            for index in range(size)
            if not ((mask >> index) & 1)
        )
        terms = baseline_terms(remaining)
        for index, weight in enumerate(weights):
            if (mask >> index) & 1:
                terms = tail_replace(terms, weight)
        answer.extend(terms)
    return compact_terms(answer)


def zero_lift(terms: list[Term], zero_count: int) -> list[Term]:
    answer: list[Term] = []
    for coefficient, power, shift, lam, wall_shift, slack_power in terms:
        for order in range(zero_count + 1):
            answer.append((
                coefficient * 2 ** zero_count * comb(zero_count, order)
                * F(factorial(slack_power), factorial(slack_power + order)),
                power, shift, lam, wall_shift, slack_power + order,
            ))
    return compact_terms(answer)


def evaluate_terms(terms: list[Term], boundary_excess: F, slack: F) -> F:
    answer = F(0)
    for coefficient, power, shift, lam, wall_shift, slack_power in terms:
        hinge = F(slack) - lam * F(boundary_excess) - wall_shift
        if hinge >= 0:
            answer += (
                coefficient * (F(boundary_excess) + shift) ** power
                * hinge ** slack_power
            )
    return answer


def predicted_section(normal: tuple[F, ...], offset: F, radius: F) -> F:
    magnitudes = tuple(abs(F(entry)) for entry in normal)
    maximum = max(magnitudes)
    support = sum(magnitudes)
    boundary_excess = (abs(F(offset)) - support) / maximum
    slack = F(radius) - boundary_excess
    require(boundary_excess > 0 and slack >= 0, "ray-side parameters")
    active = tuple(value / maximum for value in magnitudes if value)
    zero_count = len(normal) - len(active)
    terms = zero_lift(active_global_terms(active), zero_count)
    return evaluate_terms(terms, boundary_excess, slack) / maximum


def candidate_walls(weights: tuple[F, ...], boundary_excess: F) -> set[F]:
    answer: set[F] = set()
    for supplier, weight in enumerate(weights):
        others = [index for index in range(len(weights)) if index != supplier]
        for mask in range(1 << len(others)):
            total = sum(
                weights[index]
                for bit, index in enumerate(others)
                if (mask >> bit) & 1
            )
            answer.add(boundary_excess * (1 / weight - 1) + 2 * total / weight)
    return answer


def local_coefficients(weights: tuple[F, ...]) -> list[F]:
    maximum_count = sum(weight == 1 for weight in weights)
    degree = maximum_count - 1
    coefficients = [F(comb(len(weights) + j - 1, j)) for j in range(degree + 1)]
    scale = F(1)
    for weight in weights:
        scale /= weight
        if weight < 1:
            gap = 1 - weight
            scale /= gap
            coefficients = multiply_series(
                coefficients,
                [(-weight / gap) ** j for j in range(degree + 1)],
                degree,
            )
    return [scale * value for value in coefficients]


def local_section(weights: tuple[F, ...], boundary_excess: F, slack: F) -> F:
    maximum_count = sum(weight == 1 for weight in weights)
    return sum(
        coefficient
        * boundary_excess ** (maximum_count - 1 - j)
        * slack ** (len(weights) - maximum_count + j)
        / (
            factorial(maximum_count - 1 - j)
            * factorial(len(weights) - maximum_count + j)
        )
        for j, coefficient in enumerate(local_coefficients(weights))
    )


def add_polynomial_term(polynomial: dict[tuple[int, int], F], key: tuple[int, int], value: F) -> None:
    polynomial[key] = polynomial.get(key, F(0)) + value
    if not polynomial[key]:
        del polynomial[key]


def diagonal_kernel(size: int) -> dict[tuple[int, int], F]:
    return {
        (size - 1 - degree, degree): F(
            factorial(size + degree - 1),
            factorial(size - 1) * factorial(size - 1 - degree)
            * factorial(degree) ** 2,
        )
        for degree in range(size)
    }


def diagonal_transform(polynomial: dict[tuple[int, int], F]) -> dict[tuple[int, int], F]:
    answer: dict[tuple[int, int], F] = {}
    for (b_power, slack_power), coefficient in polynomial.items():
        for moment in range(b_power + 1):
            value = (
                coefficient * comb(b_power, moment)
                * (F(1, 2 ** (moment + 1)) - 1)
                * F(
                    factorial(moment) * factorial(slack_power),
                    factorial(moment + slack_power + 1),
                )
            )
            add_polynomial_term(
                answer,
                (b_power - moment, slack_power + moment + 1),
                value,
            )
    return answer


def diagonal_section(size: int, boundary_excess: F, slack: F) -> F:
    answer = F(0)
    for order in range(size):
        polynomial = diagonal_kernel(size - order)
        for _ in range(order):
            polynomial = diagonal_transform(polynomial)
        if slack >= 2 * order:
            for (b_power, slack_power), coefficient in polynomial.items():
                answer += (
                    comb(size, order) * coefficient
                    * (boundary_excess + 2 * order) ** b_power
                    * (slack - 2 * order) ** slack_power
                )
    return answer


def intersect(first: tuple[F, F, F], second: tuple[F, F, F]) -> tuple[F, F] | None:
    a, b, c = first
    d, e, f = second
    determinant = a * e - b * d
    if determinant == 0:
        return None
    return ((c * e - b * f) / determinant,
            (a * f - c * d) / determinant)


def cross(origin: tuple[F, F], first: tuple[F, F], second: tuple[F, F]) -> F:
    return ((first[0] - origin[0]) * (second[1] - origin[1])
            - (first[1] - origin[1]) * (second[0] - origin[0]))


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


def direct_section_n3(normal: tuple[F, F, F], offset: F, radius: F) -> tuple[F, int]:
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
            require(bound >= 0, "empty direct section")
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


def main() -> None:
    weight_families = (
        (F(1),),
        (F(1), F(1)),
        (F(1), F(1, 2)),
        (F(1), F(2, 3), F(1, 3)),
        (F(1), F(1), F(1, 2)),
        (F(1), F(3, 4), F(3, 4), F(1, 4)),
        (F(1), F(4, 5), F(3, 5), F(2, 5), F(1, 5)),
    )
    partial_fraction_checks = 0
    for weights in weight_families:
        plus = plus_principal_parts(weights)
        inactive = inactive_principal_parts(weights)
        forbidden = {F(1)} | {-(1 - weight) / weight for weight in weights}
        for value in (F(-3), F(-2, 3), F(1, 7), F(2, 5), F(3, 2), F(5, 2)):
            if value in forbidden:
                continue
            reconstructed = sum(
                coefficient / (value + lam) ** order
                for lam, order, coefficient in plus
            ) + sum(
                coefficient / (1 - value) ** order
                for order, coefficient in inactive
            )
            require(
                reconstructed == rational_baseline_transform(weights, value),
                "partial-fraction identity failed",
            )
            partial_fraction_checks += 1

    first_chamber_checks = 0
    for weights in weight_families:
        if max(weights) != 1:
            continue
        submaximal = [weight for weight in weights if weight < 1]
        for boundary_excess in (F(1), F(2)):
            threshold = F(2)
            if submaximal:
                threshold = min(
                    2 * min(weights),
                    boundary_excess * (1 / max(submaximal) - 1),
                )
            for slack in (F(0), threshold / 3, threshold):
                global_value = evaluate_terms(
                    active_global_terms(weights), boundary_excess, slack
                )
                require(
                    global_value == local_section(weights, boundary_excess, slack),
                    "first weighted chamber mismatch",
                )
                first_chamber_checks += 1

    diagonal_checks = 0
    for size in range(2, 9):
        terms = active_global_terms((F(1),) * size)
        for boundary_excess in (F(1), F(2)):
            for slack in (F(0), F(1), F(2), F(5, 2), F(4), F(7), F(2 * size + 3)):
                require(
                    evaluate_terms(terms, boundary_excess, slack)
                    == diagonal_section(size, boundary_excess, slack),
                    "diagonal global specialization failed",
                )
                diagonal_checks += 1

    normals = (
        (F(1), F(2, 3), F(1, 3)),
        (F(1), F(1), F(1, 2)),
        (F(1), F(2, 3), F(2, 3)),
        (F(2), F(-2), F(2)),
        (F(3), F(3), F(0)),
        (F(5), F(0), F(0)),
        (F(4), F(-3), F(1)),
        (F(0), F(2), F(-1)),
    )
    polygon_checks = 0
    sample_rows = []
    for normal_index, normal in enumerate(normals):
        maximum = max(abs(entry) for entry in normal)
        support = sum(abs(entry) for entry in normal)
        for boundary_excess in (F(1, 2), F(2)):
            for offset_sign in (-1, 1):
                offset = offset_sign * (support + maximum * boundary_excess)
                for slack in (F(0), F(1, 7), F(2, 3), F(1), F(2), F(5), F(17, 2)):
                    radius = boundary_excess + slack
                    direct, vertices = direct_section_n3(normal, offset, radius)
                    predicted = predicted_section(normal, offset, radius)
                    require(direct == predicted, "exact weighted H-polygon mismatch")
                    polygon_checks += 1
                    if (
                        normal_index in (0, 3, 4)
                        and boundary_excess == 2
                        and offset_sign == 1
                        and slack in (F(0), F(2), F(17, 2))
                    ):
                        sample_rows.append({
                            "normal": [fraction_text(entry) for entry in normal],
                            "B": fraction_text(boundary_excess),
                            "slack": fraction_text(slack),
                            "section": fraction_text(direct),
                            "vertices": vertices,
                        })

    wall_checks = 0
    wall_summary = []
    for weights in weight_families[2:]:
        boundary_excess = F(2)
        candidates = candidate_walls(weights, boundary_excess)
        terms = active_global_terms(weights)
        actual_term_walls = {
            lam * boundary_excess + wall_shift
            for _, _, _, lam, wall_shift, _ in terms
        }
        require(actual_term_walls <= candidates, "unexpected chamber wall")
        wall_checks += len(actual_term_walls)
        wall_summary.append({
            "weights": [fraction_text(weight) for weight in weights],
            "candidate_wall_count": len(candidates),
            "surviving_term_wall_count": len(actual_term_walls),
            "aggregated_term_count": len(terms),
        })

    result = {
        "status": "GLOBAL_WEIGHTED_RAY_CHAMBERS_VERIFIED",
        "exact_arithmetic": "fractions.Fraction",
        "partial_fraction_identity_checks": partial_fraction_checks,
        "first_weighted_chamber_checks": first_chamber_checks,
        "diagonal_global_specialization_checks": diagonal_checks,
        "exact_weighted_h_polygon_checks": polygon_checks,
        "candidate_wall_membership_checks": wall_checks,
        "representative_sections": sample_rows,
        "wall_and_term_summary": wall_summary,
        "scope": (
            "Exact partial fractions and subset tail replacements compared "
            "with direct rational H-polygons; PROOF.md establishes every "
            "dimension, normal, ray-side radius, and chamber formula."
        ),
    }
    print(dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
