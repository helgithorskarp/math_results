#!/usr/bin/env python3
"""Definition-level independent replay for the small verified range.

This checker neither imports nor reproduces the pruned generating tree or its
specialized pattern detectors.  It enumerates all involutions directly and
standardizes every four-term subsequence.
"""

from __future__ import annotations

import argparse
import itertools
import sys
from collections import Counter
from collections.abc import Iterator

Permutation = tuple[int, ...]


def all_involutions(n: int) -> Iterator[Permutation]:
    image = [0] * n

    def visit() -> Iterator[Permutation]:
        try:
            first = image.index(0)
        except ValueError:
            yield tuple(image)
            return

        image[first] = first + 1
        yield from visit()
        image[first] = 0
        for other in range(first + 1, n):
            if image[other] == 0:
                image[first] = other + 1
                image[other] = first + 1
                yield from visit()
                image[first] = image[other] = 0

    yield from visit()


def standardized(values: tuple[int, ...]) -> str:
    ordered = sorted(values)
    return "".join(str(ordered.index(value) + 1) for value in values)


def avoids(perm: Permutation, pattern: str) -> bool:
    return all(
        standardized(tuple(perm[i] for i in positions)) != pattern
        for positions in itertools.combinations(range(len(perm)), 4)
    )


def descents(perm: Permutation) -> tuple[int, ...]:
    return tuple(i for i, (a, b) in enumerate(zip(perm, perm[1:]), 1) if a > b)


def complement(descent_set: tuple[int, ...], n: int) -> tuple[int, ...]:
    return tuple(i for i in range(1, n) if i not in descent_set)


def telephone_numbers(max_n: int) -> list[int]:
    values = [1]
    if max_n:
        values.append(1)
    for n in range(2, max_n + 1):
        values.append(values[n - 1] + (n - 1) * values[n - 2])
    return values


def verify(max_n: int) -> None:
    if not 0 <= max_n <= 12:
        raise ValueError("independent checker requires 0 <= --max-n <= 12")
    expected_totals = telephone_numbers(max_n)
    for n in range(max_n + 1):
        counters = {pattern: Counter() for pattern in ("1432", "2134", "1243", "3214")}
        total = 0
        for perm in all_involutions(n):
            total += 1
            for pattern in counters:
                if avoids(perm, pattern):
                    counters[pattern][descents(perm)] += 1
        if total != expected_totals[n]:
            raise AssertionError(("involution total", n, total, expected_totals[n]))
        for left, right in (("1432", "2134"), ("1243", "3214")):
            transformed = Counter({complement(d, n): count for d, count in counters[right].items()})
            if counters[left] != transformed:
                raise AssertionError(("descent-complement failure", n, left, right))
        sizes = tuple(sum(counters[p].values()) for p in counters)
        print(f"n={n:2d} involutions={total:8d} avoider_counts={sizes}")
    print(f"independent definition-level replay passed through n={max_n}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=11)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    try:
        verify(args.max_n)
    except (AssertionError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
