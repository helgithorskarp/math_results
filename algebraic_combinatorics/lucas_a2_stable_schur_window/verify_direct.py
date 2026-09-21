#!/usr/bin/env python3
"""Independent direct-factorial audit of the Lucas a=2 stable window."""

from __future__ import annotations

import hashlib
import json


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
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            answer[i + j] += x * y
    return tuple(answer)


def exact_monic_quotient(dividend: Poly, divisor: Poly) -> Poly:
    assert dividend[-1] == divisor[-1] == 1
    remainder = list(dividend)
    quotient = [0] * (len(dividend) - len(divisor) + 1)
    for degree in range(len(quotient) - 1, -1, -1):
        coefficient = remainder[degree + len(divisor) - 1]
        quotient[degree] = coefficient
        for offset, value in enumerate(divisor):
            remainder[degree + offset] -= coefficient * value
    assert not any(remainder)
    return tuple(quotient)


def make_lucas(limit: int) -> list[Poly]:
    values: list[Poly] = [(0,), (1,)]
    for _ in range(1, limit):
        previous, before = values[-1], values[-2]
        values.append(plus(plus(previous, (0,) + previous), (0,) + before))
    return values[: limit + 1]


def lucas_binomial(n: int, k: int, lucas: list[Poly]) -> Poly:
    k = min(k, n - k)
    numerator: Poly = (1,)
    denominator: Poly = (1,)
    for index in range(1, k + 1):
        numerator = times(numerator, lucas[n - k + index])
        denominator = times(denominator, lucas[index])
    answer = exact_monic_quotient(numerator, denominator)
    assert answer == answer[::-1]
    assert len(answer) == k * (n - k) + 1
    return answer


def run() -> dict[str, object]:
    max_bound = 12
    max_height = 30
    maximum_index = max_bound * max_height // 2 + 2
    lucas = make_lucas(maximum_index)
    cache: dict[tuple[int, int], Poly] = {}

    def choose(n: int, k: int) -> Poly:
        key = n, min(k, n - k)
        if key not in cache:
            cache[key] = lucas_binomial(n, k, lucas)
        return cache[key]

    digest = hashlib.sha256()
    cases = coefficients = 0
    minimum_positive: int | None = None
    maximum_bits = 0
    for bound in range(3, max_bound + 1):
        for height in range(bound, max_height + 1):
            area = bound * height
            if area % 2:
                continue
            half = area // 2
            thin = choose(half + 2, 2)
            wide = choose(bound + height, bound)
            assert len(thin) == len(wide) == area + 1
            polynomial = tuple(x - y for x, y in zip(thin, wide, strict=True))
            schur = tuple(
                polynomial[i] - (polynomial[i - 1] if i else 0)
                for i in range(area // 2 + 1)
            )
            assert schur[:3] == (0, 0, 0)
            assert schur[3] == 1
            assert all(value > 0 for value in schur[3 : height + 1])
            prefix = schur[: height + 1]
            digest.update(
                f"{bound}|{height}|{','.join(map(str, prefix))}\n".encode("ascii")
            )
            cases += 1
            coefficients += len(prefix)
            minimum_positive = min(
                minimum_positive if minimum_positive is not None else prefix[3],
                *prefix[3:],
            )
            maximum_bits = max(maximum_bits, *(value.bit_length() for value in prefix))

    return {
        "schema": "lucas-a2-stable-schur-window-direct-v1",
        "algorithm": "defining-lucas-factorial-quotient",
        "bounds_checked": [3, max_bound],
        "heights_checked_through": max_height,
        "admissible_cases": cases,
        "prefix_coefficients_checked": coefficients,
        "minimum_positive_coefficient": minimum_positive,
        "maximum_coefficient_bits": maximum_bits,
        "prefix_records_sha256": digest.hexdigest(),
        "all_checks": True,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
