#!/usr/bin/env python3
"""Intrinsic rooted-lens statistic for the Ray--West correction j(beta)."""

from __future__ import annotations

import argparse
from functools import lru_cache


Permutation = tuple[int, ...]
RootedPermutation = tuple[Permutation, int]


def validate_permutation(beta: Permutation) -> None:
    if sorted(beta) != list(range(1, len(beta) + 1)):
        raise ValueError("the entries must be a permutation of 1,...,n")


def standardize(values) -> Permutation:
    values = tuple(values)
    if len(set(values)) != len(values):
        raise ValueError("standardization requires distinct entries")
    order = {value: rank for rank, value in enumerate(sorted(values), 1)}
    return tuple(order[value] for value in values)


def least_rooted_interval(beta: Permutation, boundary: int) -> RootedPermutation:
    """Return the least interval at a 1-based adjacent-position boundary.

    The result is its standardization together with the local 1-based boundary.
    """
    validate_permutation(beta)
    if not 1 <= boundary < len(beta):
        raise ValueError("boundary must lie between 1 and n-1")

    left = boundary - 1
    right = boundary
    low = min(beta[left : right + 1])
    high = max(beta[left : right + 1])

    while True:
        positions = [
            index for index, value in enumerate(beta) if low <= value <= high
        ]
        new_left = min(positions)
        new_right = max(positions)
        new_low = min(beta[new_left : new_right + 1])
        new_high = max(beta[new_left : new_right + 1])
        if (new_left, new_right, new_low, new_high) == (
            left,
            right,
            low,
            high,
        ):
            block = standardize(beta[left : right + 1])
            return block, boundary - left
        left, right, low, high = new_left, new_right, new_low, new_high


def lens(a: int, h: int, c: int, w: int) -> RootedPermutation:
    """Construct a base rooted lens Lambda(a,h,c,w).

    Valid parameters have a,c >= 0, h,w >= 1, and
    w <= min(a+h,h+c).  Plot points are returned as a permutation together
    with the distinguished adjacent-position boundary.
    """
    if min(a, c) < 0 or min(h, w) < 1 or w > min(a + h, h + c):
        raise ValueError("invalid lens parameters")

    d = h + c - w
    f = a + h - w

    upper_rows = [1]
    upper_columns = [d + 2]
    upper_row_steps = [1] * a + [2] * (h - 1)
    upper_column_steps = [2] * (w - 1) + [1] * f
    if len(upper_row_steps) != len(upper_column_steps):
        raise AssertionError("upper track lengths disagree")
    for row_step, column_step in zip(upper_row_steps, upper_column_steps):
        upper_rows.append(upper_rows[-1] + row_step)
        upper_columns.append(upper_columns[-1] + column_step)

    lower_rows = [a + 2]
    lower_columns = [1]
    lower_row_steps = [2] * (h - 1) + [1] * c
    lower_column_steps = [1] * d + [2] * (w - 1)
    if len(lower_row_steps) != len(lower_column_steps):
        raise AssertionError("lower track lengths disagree")
    for row_step, column_step in zip(lower_row_steps, lower_column_steps):
        lower_rows.append(lower_rows[-1] + row_step)
        lower_columns.append(lower_columns[-1] + column_step)

    n = a + 2 * h + c
    points = list(zip(upper_columns, upper_rows))
    points.extend(zip(lower_columns, lower_rows))
    if sorted(column for column, _ in points) != list(range(1, n + 1)):
        raise AssertionError("lens columns do not form a permutation")
    if sorted(row for _, row in points) != list(range(1, n + 1)):
        raise AssertionError("lens rows do not form a permutation")

    beta = tuple(row for column, row in sorted(points))
    boundary = d + 1
    if beta[boundary - 1] <= beta[boundary]:
        raise AssertionError("base lens boundary must be a descent")
    return beta, boundary


@lru_cache(maxsize=None)
def rooted_lenses(n: int) -> frozenset[RootedPermutation]:
    """Return all size-n base lenses and their position reversals."""
    if n < 2:
        return frozenset()
    result: set[RootedPermutation] = set()
    for h in range(1, n // 2 + 1):
        for a in range(n - 2 * h + 1):
            c = n - 2 * h - a
            for w in range(1, min(a + h, h + c) + 1):
                beta, boundary = lens(a, h, c, w)
                result.add((beta, boundary))
                result.add((beta[::-1], n - boundary))
    return frozenset(result)


def intrinsic_boundaries(beta: Permutation) -> tuple[int, ...]:
    """Return the boundaries counted by the intrinsic statistic j(beta)."""
    validate_permutation(beta)
    result = []
    for boundary in range(1, len(beta)):
        rooted_interval = least_rooted_interval(beta, boundary)
        if rooted_interval in rooted_lenses(len(rooted_interval[0])):
            result.append(boundary)
    return tuple(result)


def intrinsic_j(beta: Permutation) -> int:
    return len(intrinsic_boundaries(beta))


def parse_permutation(text: str) -> Permutation:
    try:
        beta = tuple(int(entry) for entry in text.replace(",", " ").split())
    except ValueError as error:
        raise argparse.ArgumentTypeError("entries must be integers") from error
    try:
        validate_permutation(beta)
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error
    return beta


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("permutation", type=parse_permutation)
    args = parser.parse_args()
    boundaries = intrinsic_boundaries(args.permutation)
    print(f"beta={args.permutation}")
    print(f"lens_boundaries={boundaries}")
    print(f"j={len(boundaries)}")


if __name__ == "__main__":
    main()
