#!/usr/bin/env python3
"""Standard-library verifier for the q=3 missing-wall classification."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations, product
from json import dumps


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


def polynomial_add(*polynomials: tuple[F, ...]) -> tuple[F, ...]:
    size = max(map(len, polynomials))
    return trim(tuple(
        sum((polynomial[index] if index < len(polynomial) else F(0)
             for polynomial in polynomials), F(0))
        for index in range(size)
    ))


def polynomial_scale(polynomial: tuple[F, ...], scalar: int | F) -> tuple[F, ...]:
    return trim(tuple(F(scalar) * entry for entry in polynomial))


def polynomial_mul(first: tuple[F, ...], second: tuple[F, ...]) -> tuple[F, ...]:
    answer = [F(0)] * (len(first) + len(second) - 1)
    for first_index, first_entry in enumerate(first):
        for second_index, second_entry in enumerate(second):
            answer[first_index + second_index] += first_entry * second_entry
    return trim(tuple(answer))


def polynomial_power(polynomial: tuple[F, ...], exponent: int) -> tuple[F, ...]:
    answer = (F(1),)
    for _ in range(exponent):
        answer = polynomial_mul(answer, polynomial)
    return answer


def evaluate(polynomial: tuple[F, ...], value: F) -> F:
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
    while sequence[-1] != (F(0),):
        _, remainder = divide_polynomials(sequence[-2], sequence[-1])
        if remainder == (F(0),):
            break
        sequence.append(tuple(-entry for entry in remainder))
    return sequence


def sign_variations(sequence: list[tuple[F, ...]], value: F) -> int:
    signs = []
    for polynomial in sequence:
        result = evaluate(polynomial, value)
        if result:
            signs.append(1 if result > 0 else -1)
    return sum(first != second for first, second in zip(signs, signs[1:]))


def root_count(polynomial: tuple[F, ...], low: F, high: F) -> int:
    sequence = sturm_sequence(polynomial)
    require(evaluate(polynomial, low) and evaluate(polynomial, high),
            "Sturm interval endpoint is a root")
    return sign_variations(sequence, low) - sign_variations(sequence, high)


Interval = tuple[F, F]


def interval_add(first: Interval, second: Interval) -> Interval:
    return first[0] + second[0], first[1] + second[1]


def interval_neg(interval: Interval) -> Interval:
    return -interval[1], -interval[0]


def interval_sub(first: Interval, second: Interval) -> Interval:
    return interval_add(first, interval_neg(second))


def interval_mul(first: Interval, second: Interval) -> Interval:
    values = (
        first[0] * second[0], first[0] * second[1],
        first[1] * second[0], first[1] * second[1],
    )
    return min(values), max(values)


def interval_div(first: Interval, second: Interval) -> Interval:
    require(not (second[0] <= 0 <= second[1]), "interval division by zero")
    reciprocal = (1 / second[1], 1 / second[0])
    if reciprocal[0] > reciprocal[1]:
        reciprocal = reciprocal[1], reciprocal[0]
    return interval_mul(first, reciprocal)


def interval_pow(interval: Interval, exponent: int) -> Interval:
    answer = (F(1), F(1))
    for _ in range(exponent):
        answer = interval_mul(answer, interval)
    return answer


def scalar_interval(value: int | F) -> Interval:
    return F(value), F(value)


def wall_labels(weights: tuple[F, ...], boundary: F):
    answer: dict[F, list[tuple[int, tuple[int, ...]]]] = {}
    for supplier, weight in enumerate(weights):
        others = tuple(index for index in range(3) if index != supplier)
        for mask in range(4):
            tail = tuple(index for bit, index in enumerate(others) if (mask >> bit) & 1)
            value = (
                boundary * (1 / weight - 1)
                + 2 * sum((weights[index] for index in tail), F(0)) / weight
            )
            answer.setdefault(value, []).append((supplier, tail))
    return answer


def label_jump(weights: tuple[F, ...], supplier: int, tail: tuple[int, ...]) -> F:
    weight = weights[supplier]
    denominator = F(1)
    for entry in weights:
        denominator *= entry
    for index, entry in enumerate(weights):
        if index != supplier and index not in tail:
            denominator *= weight - entry
    for index in tail:
        denominator *= weight + weights[index]
    require(denominator, "repeated weights in distinct-weight verifier")
    return (-1) ** len(tail) * weight**4 / denominator


def pair_parameters(bits: str, r: F) -> tuple[F, F]:
    denominator = r**5 + r**4 - r + 1
    if bits == "0100":
        u = r * (r**2 - r + 1) / ((1 - r) * (r**2 + 1))
        beta = 2 * r**2 * (r**2 - r + 1) / ((1 - r) ** 2 * (r**2 + 1))
    elif bits == "1000":
        u = r * (r**4 + r**3 - r + 1) / denominator
        beta = 2 * r**2 / (1 - r)
    elif bits == "1001":
        u = r * (r**2 + 1) * (r**2 + r - 1) / denominator
        beta = 2 * r * (r + 1) * (1 - r**3 - r**4) / denominator
    elif bits == "1100":
        u = r * (r**2 + 1) * (1 - r - r**2) / denominator
        beta = 2 * r**2 * (1 - r) * (r**3 + 2 * r**2 + 2 * r + 2) / denominator
    else:
        raise ValueError(bits)
    return u, beta


def pair_domain(bits: str, r: F) -> bool:
    if bits in ("0100", "1000"):
        return 0 < r < 1
    if bits == "1001":
        return r**2 + r - 1 > 0 and r**4 + r**3 - 1 < 0
    if bits == "1100":
        return r**2 + r - 1 < 0
    return False


def intersect(first, second):
    a, b, c = first
    d, e, f = second
    determinant = a * e - b * d
    if determinant == 0:
        return None
    return ((c * e - b * f) / determinant, (a * f - c * d) / determinant)


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
    hull = convex_hull(vertices)
    twice_area = sum(
        x1 * y2 - y1 * x2
        for (x1, y1), (x2, y2) in zip(hull, hull[1:] + hull[:1])
    )
    return abs(twice_area) / (2 * abs(pivot_weight))


def fit_quadratic(samples):
    matrix = [[F(1), x, x * x, y] for x, y in samples]
    for pivot in range(3):
        row = next(row for row in range(pivot, 3) if matrix[row][pivot])
        matrix[pivot], matrix[row] = matrix[row], matrix[pivot]
        divisor = matrix[pivot][pivot]
        matrix[pivot] = [entry / divisor for entry in matrix[pivot]]
        for row in range(3):
            if row != pivot:
                multiple = matrix[row][pivot]
                matrix[row] = [
                    first - multiple * second
                    for first, second in zip(matrix[row], matrix[pivot])
                ]
    return tuple(matrix[index][3] for index in range(3))


def polygon_sides(weights: tuple[F, F, F], boundary: F, target: F):
    offset = sum(weights, F(0)) + boundary
    walls = sorted(wall_labels(weights, boundary))
    position = walls.index(target)
    gaps = []
    if position:
        gaps.append(target - walls[position - 1])
    if position + 1 < len(walls):
        gaps.append(walls[position + 1] - target)
    step = min(gaps) / 10
    polynomials = []
    for sign in (-1, 1):
        samples = []
        for multiple in (1, 2, 3):
            displacement = sign * multiple * step
            samples.append((
                displacement,
                direct_section(weights, offset, boundary + target + displacement),
            ))
        polynomials.append(fit_quadratic(samples))
    return tuple(polynomials)


def main() -> None:
    root_certificates = {
        "triple_120": (
            (F(-2), F(-9), F(-11), F(1), F(29), F(29), F(15), F(-5), F(-15), F(0), F(4)),
            (F(143177, 200000), F(715887, 1000000)),
        ),
        "triple_310": (
            (F(-4), F(-8), F(-1), F(23), F(13), F(-11), F(-17), F(-3), F(7), F(3)),
            (F(867093, 1000000), F(433547, 500000)),
        ),
        "triple_312_negative_B": (
            (F(4), F(-10), F(-1), F(14), F(2), F(-6), F(0), F(-6), F(0), F(-2), F(1)),
            (F(396409, 500000), F(39641, 50000)),
        ),
        "pair_0100_third_y": (
            (F(-1), F(3), F(-5), F(7), F(-6), F(4), F(-2), F(1)),
            (F(614437, 1000000), F(307219, 500000)),
        ),
        "pair_0100_weight_equality": (
            (F(-1), F(2), F(-2), F(2)),
            (F(323899, 500000), F(647799, 1000000)),
        ),
        "pair_0100_third_xy": (
            (F(-1), F(1), F(0), F(1)),
            (F(682327, 1000000), F(85291, 125000)),
        ),
        "pair_1001_third_empty": (
            (F(-1), F(-2), F(3), F(1), F(3), F(-1), F(-3), F(0), F(1), F(2), F(1)),
            (F(73619, 100000), F(736191, 1000000)),
        ),
        "alpha": ((F(-1), F(1), F(1)), (F(618033, 1000000), F(309017, 500000))),
        "beta": ((F(-1), F(0), F(0), F(1), F(1)), (F(204793, 250000), F(819173, 1000000))),
    }
    for name, (polynomial, interval) in root_certificates.items():
        require(root_count(polynomial, F(0), F(1)) == 1, f"{name}: nonunique unit root")
        require(root_count(polynomial, *interval) == 1, f"{name}: isolation failed")

    one = (F(1),)
    x = (F(0), F(1))
    x2 = polynomial_power(x, 2)

    p1 = root_certificates["triple_120"][0]
    n1 = polynomial_mul(x2, (F(-3), F(-5), F(-7), F(-1), F(2)))
    d1 = polynomial_mul((F(1), F(1)), (F(-2), F(-5), F(-6), F(1), F(2)))
    f1_numerator = polynomial_add(
        polynomial_mul(x2, polynomial_power(d1, 2)),
        polynomial_scale(polynomial_mul(polynomial_mul(x, n1), d1), -1),
        polynomial_power(n1, 2),
        polynomial_scale(polynomial_mul(n1, d1), -1),
    )
    require(divide_polynomials(f1_numerator, p1)[1] == (F(0),),
            "pattern 120 collision is not implied by its eliminant")

    p2 = root_certificates["triple_310"][0]
    cubic = (F(-1), F(1), F(2), F(1))
    n2 = polynomial_scale(
        polynomial_mul(polynomial_mul(polynomial_mul(x, (F(-1), F(1))), (F(2), F(1))), cubic),
        -1,
    )
    d2 = (F(-2), F(-3), F(3), F(3), F(2), F(1))
    f2_numerator = polynomial_add(
        polynomial_mul(polynomial_add(x2, polynomial_scale(one, -1)), polynomial_power(d2, 2)),
        polynomial_scale(polynomial_power(n2, 2), -1),
        polynomial_mul(n2, d2),
    )
    require(divide_polynomials(f2_numerator, p2)[1] == (F(0),),
            "pattern 310 collision is not implied by its eliminant")

    p3 = root_certificates["triple_312_negative_B"][0]
    n3 = polynomial_scale((F(2), F(-2), F(-3), F(1), F(0), F(1)), -1)
    d3 = polynomial_mul(x, (F(-1), F(2), F(2), F(2)))
    f3_numerator = polynomial_add(
        polynomial_mul(polynomial_add(x, polynomial_scale(one, -1)), polynomial_power(d3, 2)),
        polynomial_scale(polynomial_power(n3, 2), -1),
        polynomial_mul(n3, d3),
    )
    require(divide_polynomials(f3_numerator, p3)[1] == (F(0),),
            "pattern 312 collision is not implied by its eliminant")

    algebraic_cases = {
        "120": (
            root_certificates["triple_120"][1],
            lambda x: interval_div(
                interval_mul(interval_pow(x, 2), interval_add(
                    interval_add(interval_add(
                        interval_mul(scalar_interval(2), interval_pow(x, 4)),
                        interval_neg(interval_pow(x, 3))),
                        interval_mul(scalar_interval(-7), interval_pow(x, 2))),
                    interval_add(interval_mul(scalar_interval(-5), x), scalar_interval(-3))),
                ),
                interval_mul(interval_add(x, scalar_interval(1)), interval_add(
                    interval_add(interval_add(
                        interval_mul(scalar_interval(2), interval_pow(x, 4)),
                        interval_pow(x, 3)),
                        interval_mul(scalar_interval(-6), interval_pow(x, 2))),
                    interval_add(interval_mul(scalar_interval(-5), x), scalar_interval(-2))),
                ),
            ),
            1,
            "a2-b",
        ),
        "310": (
            root_certificates["triple_310"][1],
            lambda x: interval_div(
                interval_neg(interval_mul(interval_mul(interval_mul(
                    x, interval_sub(x, scalar_interval(1))),
                    interval_add(x, scalar_interval(2))),
                    interval_add(interval_add(interval_pow(x, 3), interval_mul(scalar_interval(2), interval_pow(x, 2))), interval_sub(x, scalar_interval(1))))),
                interval_add(interval_add(interval_add(interval_pow(x, 5), interval_mul(scalar_interval(2), interval_pow(x, 4))), interval_mul(scalar_interval(3), interval_pow(x, 3))), interval_add(interval_mul(scalar_interval(3), interval_pow(x, 2)), interval_add(interval_mul(scalar_interval(-3), x), scalar_interval(-2)))),
            ),
            1,
            "a2+ab-1",
        ),
        "312": (
            root_certificates["triple_312_negative_B"][1],
            lambda x: interval_div(
                interval_neg(interval_add(interval_add(interval_pow(x, 5), interval_pow(x, 3)), interval_add(interval_mul(scalar_interval(-3), interval_pow(x, 2)), interval_add(interval_mul(scalar_interval(-2), x), scalar_interval(2))))),
                interval_mul(x, interval_add(interval_add(interval_mul(scalar_interval(2), interval_pow(x, 3)), interval_mul(scalar_interval(2), interval_pow(x, 2))), interval_add(interval_mul(scalar_interval(2), x), scalar_interval(-1)))),
            ),
            -1,
            "a2+ab-1",
        ),
    }
    triple_signs = []
    for pattern, (a_interval, b_builder, expected_B_sign, boundary_kind) in algebraic_cases.items():
        b_interval = b_builder(a_interval)
        require(b_interval[0] > 0 and a_interval[0] - b_interval[1] > 0,
                f"{pattern}: weight order not certified")
        if boundary_kind == "a2-b":
            numerator = interval_sub(interval_pow(a_interval, 2), b_interval)
        else:
            numerator = interval_sub(
                interval_add(interval_pow(a_interval, 2), interval_mul(a_interval, b_interval)),
                scalar_interval(1),
            )
        boundary_interval = interval_div(
            interval_mul(scalar_interval(2), numerator),
            interval_sub(scalar_interval(1), a_interval),
        )
        sign = 1 if boundary_interval[0] > 0 else (-1 if boundary_interval[1] < 0 else 0)
        require(sign == expected_B_sign, f"{pattern}: wrong B sign")
        triple_signs.append({
            "pattern": pattern,
            "a_interval": [str(entry) for entry in a_interval],
            "B_sign": "positive" if sign > 0 else "negative",
        })

    pair_checks = 0
    direct_checks = 0
    direct_evaluations = 0
    tested_pairs = set()
    direct_done = set()
    sample_for_direct = {"0100": F(1, 2), "1000": F(1, 2), "1001": F(2, 3), "1100": F(1, 2)}
    for denominator in range(3, 18):
        for numerator in range(1, denominator):
            r = F(numerator, denominator)
            for bits in ("0100", "1000", "1001", "1100"):
                if not pair_domain(bits, r) or (bits, r) in tested_pairs:
                    continue
                tested_pairs.add((bits, r))
                u, beta = pair_parameters(bits, r)
                require(u > 0 and beta > 0 and u != 1 and u != r,
                        "invalid rational normal-form weights")
                scale = max(F(1), u)
                weights = (F(1) / scale, r / scale, u / scale)
                boundary = beta / scale
                e, f, g, h = map(int, bits)
                first_tail = tuple(index for bit, index in ((e, 1), (f, 2)) if bit)
                second_tail = tuple(index for bit, index in ((g, 0), (h, 2)) if bit)
                target = (
                    boundary * (1 / weights[0] - 1)
                    + 2 * sum((weights[index] for index in first_tail), F(0)) / weights[0]
                )
                labels = wall_labels(weights, boundary)[target]
                require(set(labels) == {(0, first_tail), (1, second_tail)},
                        "unexpected third supplier at rational test point")
                require(sum((label_jump(weights, *label) for label in labels), F(0)) == 0,
                        "normal-form coefficient did not cancel")
                pair_checks += 1
                if r == sample_for_direct[bits] and bits not in direct_done:
                    left, right = polygon_sides(weights, boundary, target)
                    require(left == right, "direct polygon retained a classified missing wall")
                    direct_checks += 1
                    direct_evaluations += 6
                    direct_done.add(bits)

    require(direct_checks == 4, "did not exercise all four normal forms directly")
    result = {
        "status": "Q3_MISSING_WALL_CLASSIFICATION_VERIFIED",
        "exact_arithmetic": "fractions.Fraction and integer Sturm sequences",
        "sturm_root_certificates": len(root_certificates),
        "univariate_divisibility_certificates": 3,
        "rational_two_label_instances": pair_checks,
        "direct_polygon_normal_forms": direct_checks,
        "direct_polygon_section_evaluations": direct_evaluations,
        "triple_orbit_signs": triple_signs,
        "positive_boundary_triple_orbits": 2,
        "scope": (
            "PROOF.md combines the aggregate-jump lemma, a 16-pattern pair "
            "factorization, and a 64-pattern exact triple elimination."
        ),
    }
    print(dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
