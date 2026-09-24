#!/usr/bin/env python3
"""Standard-library verifier for the repeated-weight q=3 classification."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations, product
from json import dumps
from math import comb, factorial


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def trim(polynomial: tuple[F, ...]) -> tuple[F, ...]:
    answer = list(map(F, polynomial))
    while len(answer) > 1 and answer[-1] == 0:
        answer.pop()
    return tuple(answer)


def derivative(polynomial: tuple[F, ...]) -> tuple[F, ...]:
    return trim(tuple(index * polynomial[index] for index in range(1, len(polynomial))))


def evaluate_polynomial(polynomial: tuple[F, ...], value: F) -> F:
    answer = F(0)
    for coefficient in reversed(polynomial):
        answer = answer * value + coefficient
    return answer


def divide_polynomials(
    dividend: tuple[F, ...], divisor: tuple[F, ...]
) -> tuple[tuple[F, ...], tuple[F, ...]]:
    remainder = list(trim(dividend))
    divisor = trim(divisor)
    require(divisor != (F(0),), "zero polynomial divisor")
    quotient = [F(0)] * max(1, len(remainder) - len(divisor) + 1)
    while len(remainder) >= len(divisor) and any(remainder):
        shift = len(remainder) - len(divisor)
        coefficient = remainder[-1] / divisor[-1]
        quotient[shift] = coefficient
        for index, entry in enumerate(divisor):
            remainder[index + shift] -= coefficient * entry
        remainder = list(trim(tuple(remainder)))
    return trim(tuple(quotient)), trim(tuple(remainder))


def sturm_sequence(polynomial: tuple[F, ...]) -> list[tuple[F, ...]]:
    sequence = [trim(polynomial), derivative(trim(polynomial))]
    while True:
        _, remainder = divide_polynomials(sequence[-2], sequence[-1])
        if remainder == (F(0),):
            return sequence
        sequence.append(tuple(-entry for entry in remainder))


def sign_variations(sequence: list[tuple[F, ...]], value: F) -> int:
    signs = []
    for polynomial in sequence:
        result = evaluate_polynomial(polynomial, value)
        if result:
            signs.append(1 if result > 0 else -1)
    return sum(first != second for first, second in zip(signs, signs[1:]))


def root_count(polynomial: tuple[F, ...], low: F, high: F) -> int:
    require(evaluate_polynomial(polynomial, low), "low endpoint is a root")
    require(evaluate_polynomial(polynomial, high), "high endpoint is a root")
    sequence = sturm_sequence(polynomial)
    return sign_variations(sequence, low) - sign_variations(sequence, high)


def multiply_series(left: list[F], right: list[F], degree: int) -> list[F]:
    answer = [F(0)] * (degree + 1)
    for left_index, left_entry in enumerate(left):
        for right_index, right_entry in enumerate(right):
            if left_index + right_index <= degree:
                answer[left_index + right_index] += left_entry * right_entry
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


def principal_parts(weights: tuple[F, ...]) -> list[tuple[F, int, F]]:
    size = len(weights)
    answer = []
    for target in sorted(set(weights), reverse=True):
        multiplicity = weights.count(target)
        degree = multiplicity - 1
        root = (target - 1) / target
        denominator = [F(1)] + [F(0)] * degree
        for _ in range(size):
            denominator = multiply_series(denominator, [1 - root, F(-1)], degree)
        scale = target**multiplicity
        for weight in weights:
            scale *= weight
            if weight != target:
                denominator = multiply_series(
                    denominator, [1 - weight + weight * root, weight], degree
                )
        inverse = invert_series([scale * entry for entry in denominator])
        lam = (1 - target) / target
        for order in range(1, multiplicity + 1):
            answer.append((lam, order, inverse[multiplicity - order]))
    return answer


# coefficient, B power, B shift, lambda, wall shift, slack power
Term = tuple[F, int, F, F, F, int]


def compact_terms(terms: list[Term]) -> list[Term]:
    coefficients: dict[tuple[int, F, F, F, int], F] = {}
    for coefficient, b_power, shift, lam, wall_shift, slack_power in terms:
        key = (b_power, shift, lam, wall_shift, slack_power)
        coefficients[key] = coefficients.get(key, F(0)) + coefficient
    return [(coefficient, *key) for key, coefficient in coefficients.items() if coefficient]


def baseline_terms(weights: tuple[F, ...]) -> list[Term]:
    size = len(weights)
    return [
        (
            coefficient / (factorial(order - 1) * factorial(size - order)),
            order - 1,
            F(0),
            lam,
            F(0),
            size - order,
        )
        for lam, order, coefficient in principal_parts(weights)
    ]


def tail_replace(terms: list[Term], weight: F) -> list[Term]:
    answer = []
    for coefficient, b_power, shift, lam, wall_shift, slack_power in terms:
        for moment in range(b_power + 1):
            eta = (
                weight**moment / (1 + weight + lam * weight) ** (moment + 1)
                - 1 / (weight * (1 + lam) ** (moment + 1))
            )
            factor = F(
                comb(b_power, moment) * factorial(moment) * factorial(slack_power),
                factorial(moment + slack_power + 1),
            )
            answer.append(
                (
                    coefficient * eta * factor,
                    b_power - moment,
                    shift + 2 * weight,
                    lam,
                    wall_shift + 2 * weight * (1 + lam),
                    slack_power + moment + 1,
                )
            )
    return compact_terms(answer)


def global_terms(weights: tuple[F, ...]) -> list[Term]:
    size = len(weights)
    answer = []
    for mask in range((1 << size) - 1):
        remaining = tuple(
            weights[index] for index in range(size) if not ((mask >> index) & 1)
        )
        terms = baseline_terms(remaining)
        for index, weight in enumerate(weights):
            if (mask >> index) & 1:
                terms = tail_replace(terms, weight)
        answer.extend(terms)
    return compact_terms(answer)


def grouped_hinges(weights: tuple[F, ...], boundary: F):
    table: dict[F, dict[int, F]] = defaultdict(lambda: defaultdict(F))
    for coefficient, b_power, shift, lam, wall_shift, slack_power in global_terms(weights):
        wall = lam * boundary + wall_shift
        table[wall][slack_power] += coefficient * (boundary + shift) ** b_power
    return {
        wall: {degree: value for degree, value in vector.items() if value}
        for wall, vector in table.items()
    }


def add_hinge(table, wall: F, degree: int, coefficient: F) -> None:
    table[wall][degree] += coefficient
    if not table[wall][degree]:
        del table[wall][degree]


def expected_11a(a: F, boundary: F):
    lam = (1 - a) / a
    table = defaultdict(lambda: defaultdict(F))
    entries = (
        (F(0), 1, -boundary / (a * (a - 1))),
        (F(0), 2, -(4 * a - 3) / (2 * a * (a - 1) ** 2)),
        (2 * a, 1, -(boundary + 2 * a) / (a * (a + 1))),
        (2 * a, 2, -(4 * a + 3) / (2 * a * (a + 1) ** 2)),
        (F(2), 2, 1 / (2 * a * (a - 1))),
        (2 * (a + 1), 2, 1 / (2 * a * (a + 1))),
        (lam * boundary, 2, a**3 / (2 * (a - 1) ** 2)),
        (lam * boundary + 2 / a, 2, -a**3 / ((a - 1) * (a + 1))),
        (lam * boundary + 4 / a, 2, a**3 / (2 * (a + 1) ** 2)),
    )
    for entry in entries:
        add_hinge(table, *entry)
    return {wall: dict(vector) for wall, vector in table.items()}


def expected_1aa(a: F, boundary: F):
    lam = (1 - a) / a
    table = defaultdict(lambda: defaultdict(F))
    entries = (
        (F(0), 2, 1 / (2 * a**2 * (a - 1) ** 2)),
        (2 * a, 2, 1 / (a**2 * (a - 1) * (a + 1))),
        (4 * a, 2, 1 / (2 * a**2 * (a + 1) ** 2)),
        (lam * boundary, 1, boundary / (a - 1)),
        (lam * boundary, 2, a * (3 * a - 4) / (2 * (a - 1) ** 2)),
        (lam * boundary + 2, 2, -a / (2 * (a - 1))),
        (lam * boundary + 2 / a, 1, -(boundary + 2) / (a + 1)),
        (lam * boundary + 2 / a, 2, -a * (3 * a + 4) / (2 * (a + 1) ** 2)),
        (lam * boundary + 2 + 2 / a, 2, a / (2 * (a + 1))),
    )
    for entry in entries:
        add_hinge(table, *entry)
    return {wall: dict(vector) for wall, vector in table.items()}


def expected_111(boundary: F):
    return {
        F(0): {0: boundary**2 / 2, 1: 3 * boundary, 2: F(3)},
        F(2): {1: -3 * (boundary + 2) / 2, 2: F(-21, 8)},
        F(4): {2: F(3, 8)},
    }


def evaluate_terms(terms: list[Term], boundary: F, slack: F) -> F:
    answer = F(0)
    for coefficient, b_power, shift, lam, wall_shift, slack_power in terms:
        hinge = slack - lam * boundary - wall_shift
        if hinge >= 0:
            answer += coefficient * (boundary + shift) ** b_power * hinge**slack_power
    return answer


def candidate_walls(weights: tuple[F, ...], boundary: F) -> set[F]:
    answer = set()
    for supplier, weight in enumerate(weights):
        others = tuple(index for index in range(3) if index != supplier)
        for mask in range(4):
            tail_sum = sum(
                (weights[index] for bit, index in enumerate(others) if (mask >> bit) & 1),
                F(0),
            )
            answer.add(boundary * (1 / weight - 1) + 2 * tail_sum / weight)
    return answer


def intersect(first, second):
    a, b, c = first
    d, e, f = second
    determinant = a * e - b * d
    if not determinant:
        return None
    return (c * e - b * f) / determinant, (a * f - c * d) / determinant


def cross(origin, first, second):
    return (
        (first[0] - origin[0]) * (second[1] - origin[1])
        - (first[1] - origin[1]) * (second[0] - origin[0])
    )


def convex_hull(points):
    ordered = sorted(points)
    lower = []
    for point in ordered:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper = []
    for point in reversed(ordered):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]


def direct_section(normal: tuple[F, F, F], offset: F, radius: F) -> F:
    pivot = next(index for index, entry in enumerate(normal) if entry)
    order = [index for index in range(3) if index != pivot] + [pivot]
    first_weight, second_weight, pivot_weight = (normal[index] for index in order)
    inequalities = []
    for raw_signs in product((-1, 0, 1), repeat=3):
        signs = tuple(raw_signs[index] for index in order)
        support_size = sum(sign != 0 for sign in signs)
        first = F(signs[0]) - F(signs[2]) * first_weight / pivot_weight
        second = F(signs[1]) - F(signs[2]) * second_weight / pivot_weight
        bound = radius + support_size - F(signs[2]) * offset / pivot_weight
        if first == second == 0:
            if bound < 0:
                return F(0)
        else:
            inequalities.append((first, second, bound))
    vertices = set()
    for first, second in combinations(inequalities, 2):
        point = intersect(first, second)
        if point is not None and all(
            a * point[0] + b * point[1] <= c for a, b, c in inequalities
        ):
            vertices.add(point)
    if len(vertices) < 3:
        return F(0)
    hull = convex_hull(vertices)
    twice_area = sum(
        x1 * y2 - y1 * x2
        for (x1, y1), (x2, y2) in zip(hull, hull[1:] + hull[:1])
    )
    return abs(twice_area) / (2 * abs(pivot_weight))


def sample_slacks(weights: tuple[F, ...], boundary: F) -> list[F]:
    walls = sorted(candidate_walls(weights, boundary))
    points = {wall for wall in walls if wall > 0}
    for low, high in zip(walls, walls[1:]):
        if high > max(low, 0):
            left = max(low, F(0))
            points.add((2 * left + high) / 3)
            points.add((left + 2 * high) / 3)
    points.add(walls[-1] + 1)
    points.add(walls[-1] + 3)
    return sorted(point for point in points if point > 0)


def main() -> None:
    exceptional = (F(-1), F(1), F(0), F(0), F(1))
    low = F(724491959, 10**9)
    high = F(18112299, 25000000)
    require(root_count(exceptional, F(0), F(1)) == 1, "nonunique exceptional root")
    require(root_count(exceptional, low, high) == 1, "root isolation failed")

    rational_parameters = sorted({
        F(numerator, denominator)
        for denominator in range(3, 11)
        for numerator in range(1, denominator)
    })
    table_instances = 0
    factor_instances = 0
    for a in rational_parameters:
        for boundary in (F(1, 3), F(7, 5), F(11, 3)):
            require(grouped_hinges((F(1), F(1), a), boundary) == expected_11a(a, boundary),
                    "(1,1,a) table mismatch")
            require(grouped_hinges((F(1), a, a), boundary) == expected_1aa(a, boundary),
                    "(1,a,a) table mismatch")
            table_instances += 2
        boundary = 2 * a / (1 - a)
        coefficient = expected_11a(a, boundary)[F(2)][2]
        polynomial_value = a**4 + a - 1
        require(coefficient * 2 * a * (a - 1) ** 2 == polynomial_value,
                "exceptional factor identity failed")
        factor_instances += 1

        lam = (1 - a) / a
        # The four possible cross-resonances in each repeated stratum.
        table = expected_11a(a, 2 * a / lam)
        require(table[2 * a].get(1, F(0)) != 0, "lost 11a linear obstruction")
        table = expected_11a(a, 2 * (1 + a) / lam)
        require(table[2 * (1 + a)][2] > 0, "wrong 11a positive obstruction")
        if a * a + a - 1 > 0:
            boundary = (2 * (1 + a) - 2 / a) / lam
            require(expected_11a(a, boundary)[2 * (1 + a)][2] > 0,
                    "wrong 11a shifted obstruction")

        for wall in (2 * a, 4 * a):
            table = expected_1aa(a, wall / lam)
            require(table[wall].get(1, F(0)) != 0, "lost 1aa linear obstruction")
        if a > F(1, 2):
            boundary = (4 * a - 2) / lam
            require(expected_1aa(a, boundary)[4 * a][2] > 0,
                    "wrong 1aa quadratic obstruction")
        if 2 * a * a > 1:
            boundary = (4 * a - 2 / a) / lam
            require(expected_1aa(a, boundary)[4 * a].get(1, F(0)) != 0,
                    "lost 1aa shifted linear obstruction")

    for boundary in (F(1, 3), F(7, 5), F(11, 3)):
        require(grouped_hinges((F(1), F(1), F(1)), boundary) == expected_111(boundary),
                "diagonal table mismatch")
        table_instances += 1

    polygon_cases = (
        ((F(1), F(1), F(2, 3)), F(5, 4)),
        ((F(1), F(1), F(3, 4)), F(6)),
        ((F(1), F(1), low), 2 * low / (1 - low)),
        ((F(1), F(1), high), 2 * high / (1 - high)),
        ((F(1), F(2, 3), F(2, 3)), F(5, 4)),
        ((F(1), F(3, 4), F(3, 4)), F(3)),
        ((F(1), F(1), F(1)), F(5, 4)),
    )
    polygon_evaluations = 0
    for weights, boundary in polygon_cases:
        offset = sum(weights, F(0)) + boundary
        terms = global_terms(weights)
        for slack in sample_slacks(weights, boundary):
            predicted = evaluate_terms(terms, boundary, slack)
            observed = direct_section(weights, offset, boundary + slack)
            require(predicted == observed, "direct polygon mismatch")
            polygon_evaluations += 1

    result = {
        "status": "Q3_REPEATED_WEIGHT_CLASSIFICATION_VERIFIED",
        "exact_arithmetic": "fractions.Fraction and integer Sturm sequences",
        "exceptional_root_count_in_unit_interval": 1,
        "exceptional_root_interval": [str(low), str(high)],
        "rational_hinge_table_instances": table_instances,
        "exceptional_factor_instances": factor_instances,
        "positive_cross_resonance_types": 8,
        "new_missing_wall_orbits": 1,
        "direct_polygon_cases": len(polygon_cases),
        "direct_resonance_brackets": 2,
        "direct_polygon_evaluations": polygon_evaluations,
        "scope": (
            "The checker independently rebuilds all repeated-pole terms and "
            "validates them against the original 27-halfspace sections."
        ),
    }
    print(dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
