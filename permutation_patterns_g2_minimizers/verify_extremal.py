#!/usr/bin/env python3
"""Exact intrinsic census for the Ray--West extremal classification."""

from __future__ import annotations

import argparse
from functools import lru_cache
from itertools import permutations


Permutation = tuple[int, ...]
RootedPermutation = tuple[Permutation, int]


def standardize(values) -> Permutation:
    values = tuple(values)
    order = {value: rank for rank, value in enumerate(sorted(values), 1)}
    return tuple(order[value] for value in values)


def least_rooted_interval(beta: Permutation, boundary: int) -> RootedPermutation:
    left = boundary - 1
    right = boundary
    low = min(beta[left], beta[right])
    high = max(beta[left], beta[right])
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
            return standardize(beta[left : right + 1]), boundary - left
        left, right, low, high = new_left, new_right, new_low, new_high


def lens(a: int, h: int, c: int, w: int) -> RootedPermutation:
    if min(a, c) < 0 or min(h, w) < 1 or w > min(a + h, h + c):
        raise ValueError("invalid lens parameters")
    d = h + c - w
    f = a + h - w

    upper_rows = [1]
    upper_columns = [d + 2]
    for row_step, column_step in zip(
        [1] * a + [2] * (h - 1),
        [2] * (w - 1) + [1] * f,
    ):
        upper_rows.append(upper_rows[-1] + row_step)
        upper_columns.append(upper_columns[-1] + column_step)

    lower_rows = [a + 2]
    lower_columns = [1]
    for row_step, column_step in zip(
        [2] * (h - 1) + [1] * c,
        [1] * d + [2] * (w - 1),
    ):
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
    return beta, d + 1


@lru_cache(maxsize=None)
def rooted_lenses(n: int) -> frozenset[RootedPermutation]:
    result: set[RootedPermutation] = set()
    for h in range(1, n // 2 + 1):
        for a in range(n - 2 * h + 1):
            c = n - 2 * h - a
            for w in range(1, min(a + h, h + c) + 1):
                beta, boundary = lens(a, h, c, w)
                result.add((beta, boundary))
                result.add((beta[::-1], n - boundary))
    return frozenset(result)


def all_boundaries_are_lenses(beta: Permutation) -> bool:
    for boundary in range(1, len(beta)):
        rooted_interval = least_rooted_interval(beta, boundary)
        if rooted_interval not in rooted_lenses(len(rooted_interval[0])):
            return False
    return True


def sum_components(beta: Permutation) -> tuple[Permutation, ...]:
    cuts = [0]
    running_max = 0
    for index, value in enumerate(beta, 1):
        running_max = max(running_max, value)
        if running_max == index:
            cuts.append(index)
    result = []
    for left, right in zip(cuts, cuts[1:]):
        result.append(standardize(beta[left:right]))
    return tuple(result)


def is_layered(beta: Permutation) -> bool:
    return all(component == tuple(range(len(component), 0, -1))
               for component in sum_components(beta))


def complement(beta: Permutation) -> Permutation:
    n = len(beta)
    return tuple(n + 1 - value for value in beta)


def is_colayered(beta: Permutation) -> bool:
    return is_layered(complement(beta))


def is_direct_sum_at_root(beta: Permutation, boundary: int) -> bool:
    return max(beta[:boundary]) < min(beta[boundary:])


def is_skew_sum_at_root(beta: Permutation, boundary: int) -> bool:
    return min(beta[:boundary]) > max(beta[boundary:])


def decreasing(n: int) -> Permutation:
    return tuple(range(n, 0, -1))


def increasing(n: int) -> Permutation:
    return tuple(range(1, n + 1))


def direct_sum(alpha: Permutation, gamma: Permutation) -> Permutation:
    return alpha + tuple(len(alpha) + value for value in gamma)


def skew_sum(alpha: Permutation, gamma: Permutation) -> Permutation:
    return tuple(len(gamma) + value for value in alpha) + gamma


def audit_lens_cut_lemma(max_n: int) -> None:
    for n in range(2, max_n + 1):
        for h in range(1, n // 2 + 1):
            for a in range(n - 2 * h + 1):
                c = n - 2 * h - a
                for w in range(1, min(a + h, h + c) + 1):
                    beta, boundary = lens(a, h, c, w)
                    expected_skew = h == w == 1
                    actual_skew = is_skew_sum_at_root(beta, boundary)
                    if actual_skew != expected_skew:
                        raise AssertionError((a, h, c, w, "skew criterion"))
                    if actual_skew and beta != skew_sum(
                        increasing(c + 1), increasing(a + 1)
                    ):
                        raise AssertionError((a, h, c, w, "skew blocks"))

                    reverse = beta[::-1]
                    reverse_boundary = n - boundary
                    actual_sum = is_direct_sum_at_root(reverse, reverse_boundary)
                    if actual_sum != expected_skew:
                        raise AssertionError((a, h, c, w, "sum criterion"))
                    if actual_sum and reverse != direct_sum(
                        decreasing(a + 1), decreasing(c + 1)
                    ):
                        raise AssertionError((a, h, c, w, "sum blocks"))

                    if beta[boundary] != 1:
                        raise AssertionError((a, h, c, w, "base root misses 1"))
                    if reverse[reverse_boundary - 1] != 1:
                        raise AssertionError((a, h, c, w, "reverse root misses 1"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=9)
    parser.add_argument("--lens-max-n", type=int, default=40)
    args = parser.parse_args()
    if not 1 <= args.max_n <= 10:
        parser.error("--max-n must lie between 1 and 10")
    if args.lens_max_n < 2:
        parser.error("--lens-max-n must be at least 2")

    total = 0
    for n in range(1, args.max_n + 1):
        extremals = 0
        count = 0
        for beta in permutations(range(1, n + 1)):
            intrinsic = all_boundaries_are_lenses(beta)
            structural = is_layered(beta) or is_colayered(beta)
            if intrinsic != structural:
                raise AssertionError((beta, intrinsic, structural))
            extremals += intrinsic
            count += 1
        expected = 1 if n == 1 else 2**n - 2
        if extremals != expected:
            raise AssertionError((n, extremals, expected))
        total += count
        print(f"n={n}: checked {count} permutations; extremals={extremals}", flush=True)

    print(
        f"verified {total} permutations through n={args.max_n}; "
        "exact extremal classification holds"
    )
    audit_lens_cut_lemma(args.lens_max_n)
    print(f"lens cut lemma verified through size {args.lens_max_n}")


if __name__ == "__main__":
    main()
