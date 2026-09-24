#!/usr/bin/env python3
"""Standard-library verifier for the q=5 two-level classification."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F
from itertools import product
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


def candidates(q: int):
    answer = []
    for p in range(1, q):
        r = q - p
        for m in range(1, min(p, r) + 1):
            k, j = p - m, r - m
            for ell in range(r + 1):
                for i in range(p + 1):
                    if ell + k - j - i > 0:
                        answer.append((p, r, m, k, ell, i, j))
    return answer


def lowest_formula(p: int, r: int, m: int, ell: int, i: int, a: F) -> F:
    q = p + r
    k, j = p - m, r - m
    x = k - i + a * (ell - j)
    common = F(2) ** (m - 1) * x ** (m - 1) / (
        factorial(m - 1) * factorial(q - m) * (1 - a) ** (m - 1)
    )
    unit = F(
        comb(p, m) * comb(r, ell) * (-1) ** (p - m + ell),
        2 ** (p - m),
    ) / (a**r * (1 - a) ** (r - ell) * (1 + a) ** ell)
    moving = F(
        comb(p, i) * comb(r, m) * (-1) ** (q - m),
        2 ** (r - m),
    ) * a ** (2 * p - 1) / ((1 - a) ** (p - i) * (1 + a) ** i)
    return common * (unit + moving)


def internal_collisions(p: int, r: int):
    answer = []
    constant = [(k, ell) for k in range(p) for ell in range(r + 1)]
    for index, first in enumerate(constant):
        for second in constant[index + 1 :]:
            k1, ell1 = first
            k2, ell2 = second
            if ell1 != ell2:
                value = F(k2 - k1, ell1 - ell2)
                if 0 < value < 1:
                    answer.append(("constant", value, first, second))
    moving = [(i, j) for i in range(p + 1) for j in range(r)]
    for index, first in enumerate(moving):
        for second in moving[index + 1 :]:
            i1, j1 = first
            i2, j2 = second
            if j1 != j2:
                value = F(i2 - i1, j1 - j2)
                if 0 < value < 1:
                    answer.append(("moving", value, first, second))
    return answer


def expected_diagonal(boundary: F):
    return {
        F(0): {0: boundary**4 / 24, 1: 5 * boundary**3 / 6, 2: 15 * boundary**2 / 4, 3: 35 * boundary / 6, 4: F(35, 12)},
        F(2): {1: -5 * (boundary + 2) ** 3 / 12, 2: -55 * (boundary + 2) ** 2 / 16, 3: -355 * (boundary + 2) / 48, 4: F(-585, 128)},
        F(4): {2: 5 * (boundary + 4) ** 2 / 8, 3: 5 * (boundary + 4) / 2, 4: F(415, 192)},
        F(6): {3: -5 * (boundary + 6) / 24, 4: F(-65, 192)},
        F(8): {4: F(5, 384)},
    }


def main() -> None:
    orbit_data = (
        ((-1, 3, -3, 1, 0, 0, 0, 0, 2), (F(630979443162, 10**12), F(630979443163, 10**12))),
        ((-1, 1, 1, -1, 0, 0, 0, 0, 8), (F(636690912035, 10**12), F(636690912036, 10**12))),
        ((-1, -1, 1, 1, 0, 0, 0, 0, 12), (F(716658280303, 10**12), F(716658280304, 10**12))),
        ((-3, 6, -3, 0, 0, 0, 0, 2, 2), (F(697890411717, 10**12), F(697890411718, 10**12))),
        ((-1, 1, 0, 0, 0, 0, 0, 2), (F(745071972941, 10**12), F(745071972942, 10**12))),
        ((-4, 4, 0, 0, 0, 0, 1, 2, 1), (F(795592019016, 10**12), F(795592019017, 10**12))),
    )
    for coefficients, interval in orbit_data:
        polynomial = tuple(map(F, coefficients))
        require(root_count(polynomial, F(0), F(1)) == 1, "nonunique orbit root")
        require(root_count(polynomial, *interval) == 1, "orbit isolation failed")

    obstruction_data = (
        (
            (-3, 6, -3, 0, 0, 0, 0, 1, 1),
            (33, -66, -12, 90, -45, 0, 0, -16, -22, 4, 10),
            908446872528,
        ),
        (
            (-1, 1, 0, 0, 0, 0, 0, 1),
            (11, -11, -15, 15, 0, 0, 0, -16, -2, 10),
            55973,
        ),
        (
            (-2, 2, 0, 0, 0, 0, 1, 2, 1),
            (20, -16, -36, 32, 0, 0, -15, -34, -12, 18, 11),
            1429061632,
        ),
    )
    for first, second, expected in obstruction_data:
        require(abs(resultant(first, second)) == expected, "wrong obstruction resultant")
        _, remainder = divide_polynomials(tuple(map(F, second)), tuple(map(F, first)))
        require(remainder != (F(0),), "obstruction polynomials share by division")

    q5_candidates = candidates(5)
    parity_candidates = [entry for entry in q5_candidates if (entry[1] - entry[4]) % 2]
    require(len(q5_candidates) == 26, "wrong q=5 candidate count")
    require(len(parity_candidates) == 9, "wrong parity candidate count")
    require(sum(entry[2] == 1 for entry in parity_candidates) == 6, "wrong simple-pole count")
    require(sum(entry[2] > 1 for entry in parity_candidates) == 3, "wrong higher-pole count")

    rational_parameters = sorted({
        F(numerator, denominator)
        for denominator in range(4, 13)
        for numerator in range(1, denominator)
        if F(numerator, denominator) not in (F(1, 3), F(1, 2))
    })
    formula_instances = 0
    for entry in q5_candidates:
        p, r, m, k, ell, i, j = entry
        for a in rational_parameters:
            positivity = ell * a * a + (k - j) * a - i
            if positivity <= 0:
                continue
            wall = 2 * (k + ell * a)
            boundary = 2 * positivity / (1 - a)
            table = grouped_hinges((F(1),) * p + (a,) * r, boundary)
            require(table[wall][5 - m] == lowest_formula(p, r, m, ell, i, a), f"closed coefficient mismatch for {entry}")
            formula_instances += 1

    expected_internal = {
        (4, 1): [],
        (3, 2): [
            ("constant", F(1, 2), (0, 2), (1, 0)),
            ("constant", F(1, 2), (1, 2), (2, 0)),
        ],
        (2, 3): [
            ("constant", F(1, 2), (0, 2), (1, 0)),
            ("constant", F(1, 3), (0, 3), (1, 0)),
            ("constant", F(1, 2), (0, 3), (1, 1)),
            ("moving", F(1, 2), (0, 2), (1, 0)),
            ("moving", F(1, 2), (1, 2), (2, 0)),
        ],
        (1, 4): [
            ("moving", F(1, 2), (0, 2), (1, 0)),
            ("moving", F(1, 3), (0, 3), (1, 0)),
            ("moving", F(1, 2), (0, 3), (1, 1)),
        ],
    }
    require(all(internal_collisions(*key) == value for key, value in expected_internal.items()), "wrong internal collision list")

    special_cases = {
        (3, 2): [F(1, 2)],
        (2, 3): [F(1, 3), F(1, 2)],
        (1, 4): [F(1, 3), F(1, 2)],
    }
    cross_checks = 0
    for (p, r), values in special_cases.items():
        for a in values:
            lam = (1 - a) / a
            constant_walls = {2 * (k + a * ell) for k in range(p) for ell in range(r + 1)}
            offsets = {2 * i / a + 2 * j for i in range(p + 1) for j in range(r)}
            boundaries = sorted({(wall - offset) / lam for wall in constant_walls for offset in offsets if wall > 0 and wall > offset})
            for boundary in boundaries:
                table = grouped_hinges((F(1),) * p + (a,) * r, boundary)
                require(all(vector for wall, vector in table.items() if wall > 0), "special collision disappeared")
                cross_checks += 1
    require(cross_checks == 25, "wrong special audit count")

    diagonal_checks = 0
    for boundary in (F(1, 3), F(7, 5), F(11, 3)):
        require(grouped_hinges((F(1),) * 5, boundary) == expected_diagonal(boundary), "diagonal mismatch")
        diagonal_checks += 1

    result = {
        "status": "Q5_TWO_LEVEL_MISSING_WALLS_VERIFIED",
        "exact_arithmetic": "fractions.Fraction, rational Sturm sequences, and integer Bareiss resultants",
        "q5_equal_multiplicity_positive_candidates": len(q5_candidates),
        "q5_parity_compatible_candidates": len(parity_candidates),
        "arbitrary_q_formula_rational_instances": formula_instances,
        "root_certificates": len(orbit_data),
        "higher_multiplicity_resultants": [entry[2] for entry in obstruction_data],
        "special_internal_pair_collisions": sum(map(len, expected_internal.values())),
        "special_cross_resonance_checks": cross_checks,
        "diagonal_table_checks": diagonal_checks,
        "missing_wall_orbits": 6,
        "scope": "Independent exact reconstruction of the q=5 two-level resonance classification.",
    }
    print(dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
