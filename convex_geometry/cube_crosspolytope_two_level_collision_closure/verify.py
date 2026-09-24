#!/usr/bin/env python3
"""Independent exact verifier for the two-level multirow closure theorem."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from json import dumps
from math import comb, factorial, gcd


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


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
            beta = F(
                comb(b_power, moment) * factorial(moment) * factorial(slack_power),
                factorial(moment + slack_power + 1),
            )
            answer.append(
                (
                    coefficient * eta * beta,
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


def affine_rows(weights: tuple[F, ...]):
    rows = defaultdict(lambda: defaultdict(list))
    for coefficient, b_power, shift, lam, wall_shift, degree in global_terms(weights):
        rows[(lam, wall_shift)][degree].append((coefficient, b_power, shift))
    return rows


def row_value(row, degree: int, boundary: F) -> F:
    return sum(
        (
            coefficient * (boundary + shift) ** b_power
            for coefficient, b_power, shift in row.get(degree, ())
        ),
        F(0),
    )


def collision_parameters(p: int, r: int):
    answer = set()
    for s in range(1, min(p, r - 1) + 1):
        for t in range(s + 1, r + 1):
            if gcd(s, t) != 1:
                continue
            if (s <= p - 1 and t <= r) or (s <= p and t <= r - 1):
                answer.add(F(s, t))
    return sorted(answer)


def structural_groups(p: int, r: int, a: F):
    unit = defaultdict(list)
    moving = defaultdict(list)
    for k in range(p):
        for ell in range(r + 1):
            unit[2 * (k + a * ell)].append((k, ell))
    for i in range(p + 1):
        for j in range(r):
            moving[2 * i / a + 2 * j].append((i, j))
    return unit, moving


def full_expansion_census():
    counts = {}
    vanished = 0
    degree_checks = 0
    for q in range(4, 10):
        cross_count = 0
        multirow_count = 0
        for p in range(1, q):
            r = q - p
            for a in collision_parameters(p, r):
                lam = (1 - a) / a
                rows = affine_rows((F(1),) * p + (a,) * r)
                unit_groups, moving_groups = structural_groups(p, r, a)
                for unit_wall, unit_indices in unit_groups.items():
                    unit_row = rows[(F(0), unit_wall)]
                    for moving_offset, moving_indices in moving_groups.items():
                        boundary = (unit_wall - moving_offset) / lam
                        if boundary <= 0:
                            continue
                        cross_count += 1
                        if len(unit_indices) == len(moving_indices) == 1:
                            continue
                        multirow_count += 1
                        moving_row = rows[(lam, moving_offset)]
                        vector = [
                            row_value(unit_row, degree, boundary)
                            + row_value(moving_row, degree, boundary)
                            for degree in range(q)
                        ]
                        degree_checks += q
                        vanished += not any(vector)
        counts[str(q)] = {
            "positive_cross_walls_at_collision_parameters": cross_count,
            "multirow_walls": multirow_count,
        }
    require(vanished == 0, "a full-expansion multirow wall vanished")
    return counts, degree_checks


def valuation(integer: int, prime: int) -> int:
    require(integer > 0 and prime > 1, "bad valuation input")
    answer = 0
    while integer % prime == 0:
        integer //= prime
        answer += 1
    return answer


def factorial_valuation(size: int, prime: int) -> int:
    answer = 0
    power = prime
    while power <= size:
        answer += size // power
        power *= prime
    return answer


def smallest_odd_prime_divisor(integer: int) -> int:
    candidate = 3
    while candidate * candidate <= integer:
        if integer % candidate == 0:
            return candidate
        candidate += 2
    require(integer % 2 == 1 and integer > 1, "integer has no odd prime divisor")
    return integer


def unit_lowest(p: int, r: int, k: int, ell: int, a: F, boundary: F) -> F:
    m = p - k
    degree = r + k
    shift = boundary + 2 * k + 2 * a * ell
    sign = -1 if (k + ell) % 2 else 1
    return F(
        sign * comb(p, k) * comb(r, ell),
        factorial(m - 1) * factorial(degree) * 2**k,
    ) * shift ** (m - 1) / (
        a**r * (1 - a) ** (r - ell) * (1 + a) ** ell
    )


def magnitude_ratio(p: int, r: int, m: int, ell: int, i: int, a: F) -> F:
    unit = F(comb(p, m) * comb(r, ell), 2 ** (p - m)) / (
        a**r * (1 - a) ** (r - ell) * (1 + a) ** ell
    )
    moving = F(comb(p, i) * comb(r, m), 2 ** (r - m)) * a ** (2 * p - 1) / (
        (1 - a) ** (p - i) * (1 + a) ** i
    )
    return unit / moving


def structural_audit():
    cases = {"two_jet": 0, "reciprocal_even_extra": 0, "reciprocal_odd_valuation": 0}
    patterns = 0
    parity_relevant = 0
    accidental_leading_equalities = 0
    extra_ratio_checks = 0
    valuation_checks = 0

    for q in range(4, 31):
        for p in range(1, q):
            r = q - p
            for s in range(1, min(p, r - 1) + 1):
                for t in range(s + 1, r + 1):
                    if gcd(s, t) != 1:
                        continue
                    a = F(s, t)
                    for m in range(1, min(p, r) + 1):
                        k, j = p - m, r - m
                        for ell in range(r + 1):
                            unit_minimal = k < s or ell + t > r
                            if not unit_minimal:
                                continue
                            unit_duplicate = k + s < p and ell >= t
                            for i in range(p + 1):
                                moving_minimal = i + s > p or j < t
                                if not moving_minimal:
                                    continue
                                moving_duplicate = i >= s and j + t < r
                                if not (unit_duplicate or moving_duplicate):
                                    continue
                                boundary_numerator = a * k + a * a * ell - i - a * j
                                if boundary_numerator <= 0:
                                    continue
                                patterns += 1
                                require(m >= 2, "multirow leading multiplicity is one")
                                x = k - i + a * (ell - j)
                                require(x > 0, "positive boundary did not imply X>0")
                                margin = q * (1 + a) ** 2 - 4 * a * (i + ell)
                                require(
                                    margin == q * (1 - a) ** 2 + 4 * a * (q - i - ell),
                                    "margin identity failed",
                                )
                                difference = -F(m - 1) * margin / (
                                    4 * x * (q - m + 1) * (1 + a)
                                )
                                require(difference < 0, "two-jet difference is not negative")

                                if (r - ell) % 2:
                                    parity_relevant += 1
                                    accidental_leading_equalities += (
                                        magnitude_ratio(p, r, m, ell, i, a) == 1
                                    )

                                if s >= 2 or not unit_duplicate:
                                    cases["two_jet"] += 1
                                    continue

                                require(s == 1 and ell >= t, "bad reciprocal case")
                                if t % 2 == 0:
                                    cases["reciprocal_even_extra"] += 1
                                    boundary = 2 * boundary_numerator / (1 - a)
                                    base = unit_lowest(p, r, k, ell, a, boundary)
                                    extra = unit_lowest(p, r, k + 1, ell - t, a, boundary)
                                    direct_ratio = extra / base
                                    sign = -1 if (1 - t) % 2 else 1
                                    shift = boundary + 2 * k + 2 * a * ell
                                    closed_ratio = F(
                                        sign * m * (m - 1),
                                        2 * (k + 1) * (q - m + 1),
                                    ) * F(comb(ell, t), comb(r - ell + t, t)) * (
                                        (1 + a) / (1 - a)
                                    ) ** t / shift
                                    require(direct_ratio == closed_ratio, "extra-row ratio failed")
                                    require(direct_ratio < 0, "even reciprocal extra has wrong sign")
                                    require(difference + direct_ratio < 0, "next coefficient could vanish")
                                    extra_ratio_checks += 1
                                else:
                                    cases["reciprocal_odd_valuation"] += 1
                                    prime = smallest_odd_prime_divisor(t)
                                    main = (p + 2 * r - 1) * valuation(t, prime)
                                    denominator_valuation = valuation(comb(p, i), prime) + valuation(
                                        comb(r, m), prime
                                    )
                                    factorial_bound = factorial_valuation(p, prime) + factorial_valuation(
                                        r, prime
                                    )
                                    require(
                                        denominator_valuation <= factorial_bound,
                                        "binomial valuation bound failed",
                                    )
                                    require(
                                        factorial_bound * (prime - 1) < q,
                                        "Legendre valuation bound failed",
                                    )
                                    ratio_valuation = (
                                        main
                                        + valuation(comb(p, m), prime)
                                        + valuation(comb(r, ell), prime)
                                        - denominator_valuation
                                    )
                                    require(ratio_valuation > 0, "odd reciprocal valuation vanished")
                                    ratio = magnitude_ratio(p, r, m, ell, i, a)
                                    actual_valuation = valuation(ratio.numerator, prime) - valuation(
                                        ratio.denominator, prime
                                    )
                                    require(actual_valuation == ratio_valuation, "valuation formula failed")
                                    require(ratio != 1, "odd reciprocal leading magnitudes agree")
                                    valuation_checks += 1

    require(accidental_leading_equalities == 0, "bounded leading equality found")
    require(patterns == sum(cases.values()), "case partition is incomplete")
    return {
        "dimensions": [4, 30],
        "equal_minimum_multirow_patterns": patterns,
        "parity_relevant_patterns": parity_relevant,
        "case_counts": cases,
        "even_extra_ratio_checks": extra_ratio_checks,
        "odd_prime_valuation_checks": valuation_checks,
        "bounded_accidental_leading_equalities": accidental_leading_equalities,
    }


def main() -> None:
    full_counts, degree_checks = full_expansion_census()
    structural = structural_audit()
    payload = {
        "status": "TWO_LEVEL_COLLISION_CLOSURE_VERIFIED",
        "arithmetic": "fractions.Fraction and Python integers only",
        "full_expansion_dimensions": [4, 9],
        "full_expansion_counts": full_counts,
        "full_expansion_multirow_walls": sum(
            entry["multirow_walls"] for entry in full_counts.values()
        ),
        "full_expansion_degree_coefficients": degree_checks,
        "full_expansion_vanishing_multirow_walls": 0,
        "structural_audit": structural,
    }
    canonical = dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["certificate_sha256"] = sha256(canonical.encode()).hexdigest()
    print(dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
