#!/usr/bin/env python3
"""Independent exact-arithmetic verifier for the q=4 two-level theorem."""

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


def bareiss_determinant(matrix: list[list[int]]) -> int:
    work = [row[:] for row in matrix]
    size = len(work)
    sign = 1
    previous = 1
    for pivot_index in range(size - 1):
        if work[pivot_index][pivot_index] == 0:
            swap = next(
                (row for row in range(pivot_index + 1, size) if work[row][pivot_index]),
                None,
            )
            if swap is None:
                return 0
            work[pivot_index], work[swap] = work[swap], work[pivot_index]
            sign = -sign
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = work[row][column] * pivot - work[row][pivot_index] * work[pivot_index][column]
                require(numerator % previous == 0, "nonexact Bareiss division")
                work[row][column] = numerator // previous
        previous = pivot
    return sign * work[-1][-1]


def resultant(first: tuple[int, ...], second: tuple[int, ...]) -> int:
    first_high = list(reversed(first))
    second_high = list(reversed(second))
    first_degree = len(first) - 1
    second_degree = len(second) - 1
    size = first_degree + second_degree
    matrix = []
    for shift in range(second_degree):
        matrix.append([0] * shift + first_high + [0] * (second_degree - shift - 1))
    for shift in range(first_degree):
        matrix.append([0] * shift + second_high + [0] * (first_degree - shift - 1))
    require(all(len(row) == size for row in matrix), "bad Sylvester matrix")
    return bareiss_determinant(matrix)


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


def build_table(entries):
    table = defaultdict(lambda: defaultdict(F))
    for entry in entries:
        add_hinge(table, *entry)
    return {wall: dict(vector) for wall, vector in table.items()}


def expected_31(a: F, boundary: F):
    lam = (1 - a) / a
    return build_table((
        (F(0), 1, -boundary**2 / (2 * a * (a - 1))),
        (F(0), 2, -boundary * (5 * a - 4) / (2 * a * (a - 1) ** 2)),
        (F(0), 3, -(15 * a**2 - 24 * a + 10) / (6 * a * (a - 1) ** 3)),
        (2 * a, 1, -(boundary + 2 * a) ** 2 / (2 * a * (a + 1))),
        (2 * a, 2, -(boundary + 2 * a) * (5 * a + 4) / (2 * a * (a + 1) ** 2)),
        (2 * a, 3, -(15 * a**2 + 24 * a + 10) / (6 * a * (a + 1) ** 3)),
        (F(2), 2, 3 * (boundary + 2) / (4 * a * (a - 1))),
        (F(2), 3, (11 * a - 9) / (8 * a * (a - 1) ** 2)),
        (2 * (a + 1), 2, 3 * (boundary + 2 * a + 2) / (4 * a * (a + 1))),
        (2 * (a + 1), 3, (11 * a + 9) / (8 * a * (a + 1) ** 2)),
        (F(4), 3, -1 / (8 * a * (a - 1))),
        (2 * (a + 2), 3, -1 / (8 * a * (a + 1))),
        (lam * boundary, 3, a**5 / (6 * (a - 1) ** 3)),
        (lam * boundary + 2 / a, 3, -a**5 / (2 * (a - 1) ** 2 * (a + 1))),
        (lam * boundary + 4 / a, 3, a**5 / (2 * (a - 1) * (a + 1) ** 2)),
        (lam * boundary + 6 / a, 3, -a**5 / (6 * (a + 1) ** 3)),
    ))


def expected_22(a: F, boundary: F):
    lam = (1 - a) / a
    return build_table((
        (F(0), 2, boundary / (2 * a**2 * (a - 1) ** 2)),
        (F(0), 3, (3 * a - 2) / (3 * a**2 * (a - 1) ** 3)),
        (2 * a, 2, (boundary + 2 * a) / (a**2 * (a - 1) * (a + 1))),
        (2 * a, 3, 2 * (3 * a**2 - 2) / (3 * a**2 * (a - 1) ** 2 * (a + 1) ** 2)),
        (4 * a, 2, (boundary + 4 * a) / (2 * a**2 * (a + 1) ** 2)),
        (4 * a, 3, (3 * a + 2) / (3 * a**2 * (a + 1) ** 3)),
        (F(2), 3, -1 / (6 * a**2 * (a - 1) ** 2)),
        (2 * (a + 1), 3, -1 / (3 * a**2 * (a - 1) * (a + 1))),
        (2 * (2 * a + 1), 3, -1 / (6 * a**2 * (a + 1) ** 2)),
        (lam * boundary, 2, boundary * a**2 / (2 * (a - 1) ** 2)),
        (lam * boundary, 3, a**3 * (2 * a - 3) / (3 * (a - 1) ** 3)),
        (lam * boundary + 2, 3, -a**3 / (6 * (a - 1) ** 2)),
        (lam * boundary + 2 / a, 2, -a**2 * (boundary + 2) / ((a - 1) * (a + 1))),
        (lam * boundary + 2 / a, 3, -2 * a**3 * (2 * a**2 - 3) / (3 * (a - 1) ** 2 * (a + 1) ** 2)),
        (lam * boundary + 2 + 2 / a, 3, a**3 / (3 * (a - 1) * (a + 1))),
        (lam * boundary + 4 / a, 2, a**2 * (boundary + 4) / (2 * (a + 1) ** 2)),
        (lam * boundary + 4 / a, 3, a**3 * (2 * a + 3) / (3 * (a + 1) ** 3)),
        (lam * boundary + 2 + 4 / a, 3, -a**3 / (6 * (a + 1) ** 2)),
    ))


def expected_13(a: F, boundary: F):
    lam = (1 - a) / a
    return build_table((
        (F(0), 3, -1 / (6 * a**3 * (a - 1) ** 3)),
        (2 * a, 3, -1 / (2 * a**3 * (a - 1) ** 2 * (a + 1))),
        (4 * a, 3, -1 / (2 * a**3 * (a - 1) * (a + 1) ** 2)),
        (6 * a, 3, -1 / (6 * a**3 * (a + 1) ** 3)),
        (lam * boundary, 1, boundary**2 / (2 * a * (a - 1))),
        (lam * boundary, 2, boundary * (4 * a - 5) / (2 * (a - 1) ** 2)),
        (lam * boundary, 3, a * (10 * a**2 - 24 * a + 15) / (6 * (a - 1) ** 3)),
        (lam * boundary + 2, 2, -3 * (boundary + 2 * a) / (4 * (a - 1))),
        (lam * boundary + 2, 3, -a * (9 * a - 11) / (8 * (a - 1) ** 2)),
        (lam * boundary + 4, 3, a / (8 * (a - 1))),
        (lam * boundary + 2 / a, 1, -(boundary + 2) ** 2 / (2 * a * (a + 1))),
        (lam * boundary + 2 / a, 2, -(boundary + 2) * (4 * a + 5) / (2 * (a + 1) ** 2)),
        (lam * boundary + 2 / a, 3, -a * (10 * a**2 + 24 * a + 15) / (6 * (a + 1) ** 3)),
        (lam * boundary + 2 + 2 / a, 2, 3 * (boundary + 2 * a + 2) / (4 * (a + 1))),
        (lam * boundary + 2 + 2 / a, 3, a * (9 * a + 11) / (8 * (a + 1) ** 2)),
        (lam * boundary + 4 + 2 / a, 3, -a / (8 * (a + 1))),
    ))


def expected_40(boundary: F):
    return {
        F(0): {0: boundary**3 / 6, 1: 2 * boundary**2, 2: 5 * boundary, 3: F(10, 3)},
        F(2): {1: -(boundary + 2) ** 2, 2: -9 * (boundary + 2) / 2, 3: F(-49, 12)},
        F(4): {2: 3 * (boundary + 4) / 4, 3: F(5, 4)},
        F(6): {3: F(-1, 12)},
    }


def structural_candidates():
    answer = []
    for p, r in ((3, 1), (2, 2), (1, 3)):
        for k in range(p):
            for ell in range(r + 1):
                for i in range(p + 1):
                    for j in range(r):
                        if r + k == p + j and ell + k - j - i > 0:
                            answer.append((p, r, k, ell, i, j))
    return answer


def aggregate_formula(key, a: F) -> F:
    p, r, k, ell, i, j = key
    formulas = {
        (3, 1, 2, 0, 0, 0): (4*a**6 - 3*a**2 + 6*a - 3) / (24*a*(a-1)**3),
        (3, 1, 2, 0, 1, 0): -(2*a**2 - 1)*(2*a**4 + a**2 + 1) / (8*a*(a-1)**2*(a+1)),
        (3, 1, 2, 1, 0, 0): (4*a**7 + 4*a**6 - 3*a**3 + 9*a**2 - 9*a + 3) / (24*a*(a-1)**3*(a+1)),
        (3, 1, 2, 1, 1, 0): -(4*a**6 + a**2 - 2*a + 1) / (8*a*(a-1)**2*(a+1)),
        (3, 1, 2, 1, 2, 0): (4*a**6 - a**2 + 1) / (8*a*(a-1)*(a+1)**2),
        (2, 2, 0, 1, 0, 0): -(a**6 + a**5 + 2*a - 2) / (a*(a-1)**3*(a+1)),
        (2, 2, 0, 2, 0, 0): -2*(a**7 + 2*a**6 + a**5 + a**2 - 2*a + 1) / (a*(a-1)**3*(a+1)**2),
        (2, 2, 0, 2, 1, 0): (2*a-1)*(2*a**6 + 2*a**5 - a + 1) / (a**2*(a-1)**2*(a+1)**2),
        (2, 2, 1, 1, 0, 1): -(a**6 + a**5 + 2*a - 2) / (6*a**2*(a-1)**2*(a+1)),
        (2, 2, 1, 2, 0, 1): -(a**7 + 2*a**6 + a**5 + a**2 - 2*a + 1) / (6*a**2*(a-1)**2*(a+1)**2),
        (2, 2, 1, 2, 1, 1): (2*a**6 + 2*a**5 - a + 1) / (6*a**2*(a-1)*(a+1)**2),
        (1, 3, 0, 3, 0, 2): (3*a**7 + 9*a**6 + 9*a**5 + 3*a**4 - 4*a + 4) / (24*a**3*(a-1)*(a+1)**3),
    }
    return formulas[key]


def determinant3(rows) -> F:
    return (
        rows[0][0] * (rows[1][1] * rows[2][2] - rows[1][2] * rows[2][1])
        - rows[0][1] * (rows[1][0] * rows[2][2] - rows[1][2] * rows[2][0])
        + rows[0][2] * (rows[1][0] * rows[2][1] - rows[1][1] * rows[2][0])
    )


def intersect3(first, second, third):
    rows = [first[:3], second[:3], third[:3]]
    determinant = determinant3(rows)
    if not determinant:
        return None
    bounds = [first[3], second[3], third[3]]
    coordinates = []
    for column in range(3):
        replaced = [list(row) for row in rows]
        for row in range(3):
            replaced[row][column] = bounds[row]
        coordinates.append(determinant3(replaced) / determinant)
    return tuple(coordinates)


def cross2(origin, first, second):
    return (
        (first[0] - origin[0]) * (second[1] - origin[1])
        - (first[1] - origin[1]) * (second[0] - origin[0])
    )


def convex_hull_2d(points):
    ordered = sorted(set(points))
    lower = []
    for point in ordered:
        while len(lower) >= 2 and cross2(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper = []
    for point in reversed(ordered):
        while len(upper) >= 2 and cross2(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]


def direct_section_4d(normal: tuple[F, F, F, F], offset: F, radius: F) -> F:
    pivot = next(index for index, weight in enumerate(normal) if weight)
    order = [index for index in range(4) if index != pivot] + [pivot]
    weights = tuple(normal[index] for index in order)
    inequalities = set()
    for raw_signs in product((-1, 0, 1), repeat=4):
        signs = tuple(raw_signs[index] for index in order)
        support_size = sum(sign != 0 for sign in signs)
        coefficients = tuple(
            F(signs[index]) - F(signs[3]) * weights[index] / weights[3]
            for index in range(3)
        )
        bound = radius + support_size - F(signs[3]) * offset / weights[3]
        if coefficients == (F(0), F(0), F(0)):
            if bound < 0:
                return F(0)
        else:
            inequalities.add((*coefficients, bound))
    inequalities = sorted(inequalities)
    vertices = set()
    for triple in combinations(inequalities, 3):
        point = intersect3(*triple)
        if point is not None and all(
            sum(row[index] * point[index] for index in range(3)) <= row[3]
            for row in inequalities
        ):
            vertices.add(point)
    require(len(vertices) >= 4, "degenerate direct section")
    vertices = sorted(vertices)
    center = tuple(sum(point[index] for point in vertices) / len(vertices) for index in range(3))
    facet_sets = set()
    facets = []
    for inequality in inequalities:
        face = tuple(
            point for point in vertices
            if sum(inequality[index] * point[index] for index in range(3)) == inequality[3]
        )
        if len(face) < 3:
            continue
        key = frozenset(face)
        if key in facet_sets:
            continue
        facet_sets.add(key)
        dropped = next(index for index in range(3) if inequality[index])
        kept = [index for index in range(3) if index != dropped]
        projected = {(point[kept[0]], point[kept[1]]): point for point in face}
        hull = [projected[point] for point in convex_hull_2d(projected)]
        if len(hull) >= 3:
            facets.append(hull)
    volume = F(0)
    for face in facets:
        for index in range(1, len(face) - 1):
            rows = [
                tuple(vertex[coordinate] - center[coordinate] for coordinate in range(3))
                for vertex in (face[0], face[index], face[index + 1])
            ]
            volume += abs(determinant3(rows)) / 6
    return volume / abs(weights[3])


def evaluate_terms(terms: list[Term], boundary: F, slack: F) -> F:
    answer = F(0)
    for coefficient, b_power, shift, lam, wall_shift, slack_power in terms:
        hinge = slack - lam * boundary - wall_shift
        if hinge >= 0:
            answer += coefficient * (boundary + shift) ** b_power * hinge**slack_power
    return answer


def main() -> None:
    p1 = (F(-3), F(6), F(-3), F(0), F(0), F(0), F(4))
    p2 = (F(-2), F(2), F(0), F(0), F(0), F(1), F(1))
    p3 = (F(-1), F(0), F(2))
    intervals = (
        (F(663190523, 10**9), F(165797631, 250000000)),
        (F(766427599, 10**9), F(1916069, 2500000)),
        (F(707106781, 10**9), F(353553391, 500000000)),
    )
    for polynomial, interval in zip((p1, p2, p3), intervals):
        require(root_count(polynomial, F(0), F(1)) == 1, "nonunique exceptional root")
        require(root_count(polynomial, *interval) == 1, "root isolation failed")

    obstruction = (4, -4, -6, 6, 0, -3, -4, 1, 2)
    require(resultant(tuple(map(int, p2)), obstruction) == 896, "wrong exact resultant")
    _, remainder = divide_polynomials(tuple(map(F, obstruction)), p2)
    require(remainder == (F(-2), F(0), F(0), F(2)), "wrong obstruction remainder")

    expected_candidates = {
        (3, 1, 2, 0, 0, 0), (3, 1, 2, 0, 1, 0),
        (3, 1, 2, 1, 0, 0), (3, 1, 2, 1, 1, 0), (3, 1, 2, 1, 2, 0),
        (2, 2, 0, 1, 0, 0), (2, 2, 0, 2, 0, 0), (2, 2, 0, 2, 1, 0),
        (2, 2, 1, 1, 0, 1), (2, 2, 1, 2, 0, 1), (2, 2, 1, 2, 1, 1),
        (1, 3, 0, 3, 0, 2),
    }
    candidates = structural_candidates()
    require(set(candidates) == expected_candidates, "wrong structural candidate set")

    rational_parameters = sorted({
        F(numerator, denominator)
        for denominator in range(3, 11)
        for numerator in range(1, denominator)
    })
    table_instances = 0
    for a in rational_parameters:
        for boundary in (F(1, 3), F(7, 5), F(11, 3)):
            require(grouped_hinges((F(1), F(1), F(1), a), boundary) == expected_31(a, boundary), "111a table mismatch")
            require(grouped_hinges((F(1), F(1), a, a), boundary) == expected_22(a, boundary), "11aa table mismatch")
            require(grouped_hinges((F(1), a, a, a), boundary) == expected_13(a, boundary), "1aaa table mismatch")
            table_instances += 3
    for boundary in (F(1, 3), F(7, 5), F(11, 3)):
        require(grouped_hinges((F(1),) * 4, boundary) == expected_40(boundary), "diagonal table mismatch")
        table_instances += 1

    aggregate_instances = 0
    for key in candidates:
        p, r, k, ell, i, j = key
        degree = r + k
        for a in rational_parameters:
            if a == F(1, 2):
                continue
            positivity = ell * a * a + (k - j) * a - i
            if positivity <= 0:
                continue
            wall = 2 * (k + ell * a)
            boundary = a * (wall - 2 * i / a - 2 * j) / (1 - a)
            weights = (F(1),) * p + (a,) * r
            coefficient = grouped_hinges(weights, boundary)[wall][degree]
            require(coefficient == aggregate_formula(key, a), f"aggregate mismatch for {key}")
            aggregate_instances += 1

    no_root_polynomials = (
        (1, 0, 1, 0, 2),
        (3, -9, 9, -3, 0, 0, 4, 4),
        (1, -2, 1, 0, 0, 0, 4),
        (1, 0, -1, 0, 0, 0, 4),
        (1, -2, 1, 0, 0, 1, 2, 1),
        (1, -1, 0, 0, 0, 2, 2),
        (4, -4, 0, 0, 3, 9, 9, 3),
    )
    for polynomial in no_root_polynomials:
        require(root_count(tuple(map(F, polynomial)), F(0), F(1)) == 0, "unexpected auxiliary root")

    # The only internal subset-sum collisions in the open interval.
    special22 = grouped_hinges((F(1), F(1), F(1, 2), F(1, 2)), F(2))
    require(special22[F(2)][2] > 0, "constant internal collision disappeared")
    special13 = grouped_hinges((F(1), F(1, 2), F(1, 2), F(1, 2)), F(2))
    require(special13[F(6)][1] != 0, "moving internal collision lost its linear term")

    direct_cases = (
        ((F(1), F(1), F(1), F(2, 3)), F(5, 4), F(4)),
        ((F(1), F(1), F(1), intervals[0][0]), 4 * intervals[0][0] / (1 - intervals[0][0]), F(4)),
        ((F(1), F(1), F(1), intervals[0][1]), 4 * intervals[0][1] / (1 - intervals[0][1]), F(4)),
        ((F(1), F(1), intervals[1][0], intervals[1][0]), 2 * intervals[1][0] ** 2 / (1 - intervals[1][0]), 2 * (1 + intervals[1][0])),
        ((F(1), F(1), intervals[1][1], intervals[1][1]), 2 * intervals[1][1] ** 2 / (1 - intervals[1][1]), 2 * (1 + intervals[1][1])),
        ((F(1), F(2, 3), F(2, 3), F(2, 3)), F(5, 4), F(5)),
        ((F(1), F(1), F(1), F(1)), F(5, 4), F(5)),
    )
    for weights, boundary, slack in direct_cases:
        predicted = evaluate_terms(global_terms(weights), boundary, slack)
        observed = direct_section_4d(weights, sum(weights, F(0)) + boundary, boundary + slack)
        require(predicted == observed, "direct four-dimensional section mismatch")

    result = {
        "status": "Q4_TWO_LEVEL_MISSING_WALLS_VERIFIED",
        "exact_arithmetic": "fractions.Fraction, integer Sturm sequences, and Bareiss resultant",
        "root_certificates": 3,
        "obstruction_resultant": 896,
        "structural_candidates": len(candidates),
        "rational_hinge_table_instances": table_instances,
        "rational_aggregate_instances": aggregate_instances,
        "special_internal_collisions_checked": 2,
        "missing_wall_orbits": 3,
        "direct_4d_section_cases": len(direct_cases),
        "scope": "The checker independently rebuilds the repeated-pole expansion and compares seven values with the original 81-halfspace sections.",
    }
    print(dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
