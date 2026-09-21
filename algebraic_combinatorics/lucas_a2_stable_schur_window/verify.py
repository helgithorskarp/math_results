#!/usr/bin/env python3
"""Exact structural audit for the universal Lucas a=2 stable window."""

from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
import hashlib
import json


Poly = tuple[int, ...]


def add(left: Poly, right: Poly) -> Poly:
    size = max(len(left), len(right))
    return tuple(
        (left[i] if i < len(left) else 0)
        + (right[i] if i < len(right) else 0)
        for i in range(size)
    )


def shift(poly: Poly, amount: int) -> Poly:
    return (0,) * amount + poly


def q_binomial(n: int, k: int, cache: dict[tuple[int, int], Poly]) -> Poly:
    """Gaussian binomial by q-Pascal, coefficients low degree first."""
    if k < 0 or k > n:
        return (0,)
    k = min(k, n - k)
    key = n, k
    if key in cache:
        return cache[key]
    if k == 0:
        answer = (1,)
    else:
        answer = add(
            q_binomial(n - 1, k, cache),
            shift(q_binomial(n - 1, k - 1, cache), n - k),
        )
    cache[key] = answer
    return answer


def partition_counts(bound: int, limit: int) -> list[int]:
    counts = [0] * (limit + 1)
    counts[0] = 1
    for part in range(2, bound + 1):
        for total in range(part, limit + 1):
            counts[total] += counts[total - part]
    return counts


@lru_cache(maxsize=None)
def partitions(total: int, bound: int, least: int = 2) -> tuple[tuple[int, ...], ...]:
    if total == 0:
        return ((),)
    answer: list[tuple[int, ...]] = []
    for first in range(least, min(bound, total) + 1):
        for tail in partitions(total - first, bound, first):
            answer.append((first,) + tail)
    return tuple(answer)


def lower_smallest_non_two(partition: tuple[int, ...]) -> tuple[int, ...]:
    values = list(partition)
    position = next(i for i, value in enumerate(values) if value > 2)
    values[position] -= 1
    values.sort()
    return tuple(values)


def first_differences(poly: Poly) -> Poly:
    return tuple(value - (poly[i - 1] if i else 0) for i, value in enumerate(poly))


def lucas_polynomials(limit: int) -> list[Poly]:
    values: list[Poly] = [(0,), (1,)]
    for _ in range(1, limit):
        previous, before = values[-1], values[-2]
        values.append(add(add(previous, shift(previous, 1)), shift(before, 1)))
    return values[: limit + 1]


def subtract_scaled(left: Poly, right: Poly, scale: int, offset: int) -> Poly:
    size = max(len(left), len(right) + offset)
    answer = [0] * size
    for i, value in enumerate(left):
        answer[i] += value
    for i, value in enumerate(right):
        answer[i + offset] -= scale * value
    return tuple(answer)


def run() -> dict[str, object]:
    max_bound = 12
    max_total = 48
    fibre_cases = fibre_sources = maximum_fibre = 0
    injection_digest = hashlib.sha256()

    for bound in range(3, max_bound + 1):
        counts = partition_counts(bound, max_total + 1)
        for odd in range(1, max_total, 2):
            domain = [
                item
                for item in partitions(odd + 1, bound)
                if any(part > 2 for part in item)
            ]
            fibres: dict[tuple[int, ...], list[tuple[int, ...]]] = defaultdict(list)
            for item in domain:
                image = lower_smallest_non_two(item)
                assert sum(image) == odd
                assert image == tuple(sorted(image))
                assert all(2 <= part <= bound for part in image)
                fibres[image].append(item)
                injection_digest.update(
                    f"{bound}|{odd}|{','.join(map(str, item))}|"
                    f"{','.join(map(str, image))}\n".encode("ascii")
                )
            assert len(domain) == counts[odd + 1] - 1
            assert len(partitions(odd, bound)) == counts[odd]
            assert all(len(sources) <= 2 for sources in fibres.values())
            assert counts[odd + 1] - 1 <= 2 * counts[odd]
            fibre_cases += 1
            fibre_sources += len(domain)
            maximum_fibre = max(
                [maximum_fibre] + [len(sources) for sources in fibres.values()]
            )

    q_cache: dict[tuple[int, int], Poly] = {}
    layer_cases = layer_values = adjacent_pairs = 0
    layer_digest = hashlib.sha256()
    maximum_area = 0
    for bound in range(3, 17):
        counts = partition_counts(bound, 40)
        for height in range(bound, 41):
            area = bound * height
            if area % 2:
                continue
            half = area // 2
            wide = q_binomial(bound + height, bound, q_cache)
            thin = q_binomial(half + 2, 2, q_cache)
            difference = tuple(
                (wide[i] if i < len(wide) else 0)
                - (thin[i] if i < len(thin) else 0)
                for i in range(area + 1)
            )
            layers = first_differences(difference)
            assert layers[:3] == (0, 0, 0)
            assert layers[3] == 1
            for index in range(height + 1):
                expected = counts[index] - int(index % 2 == 0)
                assert layers[index] == expected
                layer_digest.update(
                    f"{bound}|{height}|{index}|{layers[index]}\n".encode("ascii")
                )
                layer_values += 1
            for odd in range(1, height, 2):
                even = odd + 1
                assert layers[odd] >= 0
                assert layers[even] >= 0
                assert 2 * layers[odd] - layers[even] >= 0
                adjacent_pairs += 1
            layer_cases += 1
            maximum_area = max(maximum_area, area)

    lucas = lucas_polynomials(maximum_area + 1)
    kernel_checks = 0
    for m in range(3, maximum_area + 1):
        kernel = subtract_scaled(lucas[m], lucas[m - 2], 2, 1)
        assert kernel == kernel[::-1]
        schur = first_differences(kernel)[: (m - 1) // 2 + 1]
        assert min(schur) >= 0
        kernel_checks += len(schur)

    return {
        "schema": "lucas-a2-stable-schur-window-v1",
        "partition_bounds_checked": [3, max_bound],
        "odd_partition_totals_checked": [1, max_total - 1],
        "partition_fibre_cases": fibre_cases,
        "partition_sources_checked": fibre_sources,
        "maximum_fibre_size": maximum_fibre,
        "injection_records_sha256": injection_digest.hexdigest(),
        "gaussian_bounds_checked": [3, 16],
        "gaussian_heights_checked_through": 40,
        "admissible_layer_cases": layer_cases,
        "layer_values_checked": layer_values,
        "adjacent_pairs_checked": adjacent_pairs,
        "maximum_area": maximum_area,
        "layer_records_sha256": layer_digest.hexdigest(),
        "kernel_schur_coefficients_checked": kernel_checks,
        "all_checks": True,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
