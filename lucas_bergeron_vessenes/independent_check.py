#!/usr/bin/env python3
"""Independent checker using the defining factorial quotient, not atoms."""

from __future__ import annotations

import argparse
import hashlib
import json
from math import isqrt
from pathlib import Path


Poly = tuple[int, ...]


def plus(left: Poly, right: Poly) -> Poly:
    length = max(len(left), len(right))
    return tuple(
        (left[i] if i < len(left) else 0)
        + (right[i] if i < len(right) else 0)
        for i in range(length)
    )


def times(left: Poly, right: Poly) -> Poly:
    answer = [0] * (len(left) + len(right) - 1)
    for left_degree, left_coefficient in enumerate(left):
        for right_degree, right_coefficient in enumerate(right):
            answer[left_degree + right_degree] += (
                left_coefficient * right_coefficient
            )
    return tuple(answer)


def monic_quotient(dividend: Poly, divisor: Poly) -> Poly:
    assert dividend[-1] == divisor[-1] == 1
    remainder = list(dividend)
    answer = [0] * (len(dividend) - len(divisor) + 1)
    for degree in range(len(answer) - 1, -1, -1):
        coefficient = remainder[degree + len(divisor) - 1]
        answer[degree] = coefficient
        for offset, divisor_coefficient in enumerate(divisor):
            remainder[degree + offset] -= coefficient * divisor_coefficient
    assert remainder == [0] * len(remainder)
    return tuple(answer)


def make_lucas(limit: int) -> list[Poly]:
    sequence: list[Poly] = [(0,), (1,)]
    for _ in range(1, limit):
        previous = sequence[-1]
        before_previous = sequence[-2]
        multiplied_by_q_plus_one = plus(previous, (0,) + previous)
        sequence.append(plus(multiplied_by_q_plus_one, (0,) + before_previous))
    return sequence[: limit + 1]


def defining_binomial(n: int, k: int, lucas: list[Poly]) -> Poly:
    """Use L_n...L_(n-k+1)/(L_k...L_1) directly."""
    assert 0 <= k <= n
    k = min(k, n - k)
    numerator: Poly = (1,)
    denominator: Poly = (1,)
    for index in range(1, k + 1):
        numerator = times(numerator, lucas[n - k + index])
        denominator = times(denominator, lucas[index])
    result = monic_quotient(numerator, denominator)
    assert len(result) == k * (n - k) + 1
    assert result == result[::-1]
    return result


def rectangle_pairs(area: int) -> list[tuple[int, int]]:
    answer = []
    for short_side in range(1, isqrt(area) + 1):
        if area % short_side == 0:
            answer.append((short_side, area // short_side))
    return answer


def run(max_product: int) -> dict[str, object]:
    lucas = make_lucas(max_product + 1)
    cache: dict[tuple[int, int], Poly] = {}

    def choose(n: int, k: int) -> Poly:
        key = n, min(k, n - k)
        if key not in cache:
            cache[key] = defining_binomial(n, k, lucas)
        return cache[key]

    digest = hashlib.sha256()
    count = positive = negative = maximum_bits = 0
    for area in range(1, max_product + 1):
        rectangles = rectangle_pairs(area)
        for i, (a, d) in enumerate(rectangles):
            for b, c in rectangles[i + 1 :]:
                first = choose(b + c, b)
                second = choose(a + d, a)
                polynomial = tuple(x - y for x, y in zip(first, second, strict=True))
                half = area // 2
                schur = tuple(
                    polynomial[j] - (polynomial[j - 1] if j else 0)
                    for j in range(half + 1)
                )
                orientation = 1 if a & 1 else -1
                normalized = tuple(orientation * coefficient for coefficient in schur)
                assert normalized[: a + 1] == (0,) * (a + 1)
                assert normalized[a + 1] == 1
                assert min(normalized) >= 0
                line = (
                    f"{area}|{a}|{b}|{c}|{d}|"
                    + ",".join(map(str, normalized))
                    + "\n"
                )
                digest.update(line.encode("ascii"))
                count += 1
                positive += orientation == 1
                negative += orientation == -1
                maximum_bits = max(
                    maximum_bits,
                    max((abs(value).bit_length() for value in schur), default=0),
                )

    return {
        "schema": "lucas-bergeron-vessenes-v1",
        "algorithm": "anti-cyclotomic-atom-factorization",
        "max_product": max_product,
        "comparison_count": count,
        "positive_orientation_count": positive,
        "negative_orientation_count": negative,
        "maximum_schur_coefficient_bits": maximum_bits,
        "records_sha256": digest.hexdigest(),
        "all_sign_normalized_schur_nonnegative": True,
        "all_first_nonzero_coefficients_verified": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=Path(__file__).with_name("certificate.json"))
    arguments = parser.parse_args()
    expected = json.loads(arguments.certificate.read_text(encoding="utf-8"))
    actual = run(expected["max_product"])
    assert actual == expected
    print(json.dumps(actual, indent=2, sort_keys=True))
    print("independent_check=passed")


if __name__ == "__main__":
    main()
