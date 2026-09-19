#!/usr/bin/env python3
"""Exact arithmetic checks accompanying the 2p+1 inertia proof."""

from __future__ import annotations


PRIMES = (3, 5, 7, 11, 13, 17, 19)


def partitions(total: int, length: int, minimum: int = 1):
    """Yield nondecreasing positive tuples with fixed sum and length."""
    if length == 0:
        if total == 0:
            yield ()
        return
    maximum = total // length
    for first in range(minimum, maximum + 1):
        for tail in partitions(total - first, length - 1, first):
            yield (first,) + tail


def singleton_gap_admissible(profile: tuple[int, ...], p: int) -> bool:
    if 1 not in profile:
        return True
    return all(x == 1 or x >= p for x in profile)


def admissible_profiles(p: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        profile
        for profile in partitions(2 * p + 1, p)
        if singleton_gap_admissible(profile, p)
    )


def matvec(matrix: list[list[int]], vector: list[int]) -> list[int]:
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def dot(left: list[int], right: list[int]) -> int:
    return sum(a * b for a, b in zip(left, right))


def block_gram(p: int, r: int) -> list[list[int]]:
    """Matrix (10), represented with exact Python integers."""
    s = p - 1
    k = r + s
    size = k
    matrix = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(r):
        for j in range(r):
            matrix[i][j] = (k if i == j else 0) - s
    for i in range(r, size):
        for j in range(r, size):
            matrix[i][j] = (r - 1 if i == j else 0) + 1
    for i in range(r):
        for j in range(r, size):
            matrix[i][j] = matrix[j][i] = 1
    return matrix


def check_prime(p: int) -> str:
    profiles = admissible_profiles(p)
    if p == 3:
        expected = ((1, 1, 5), (1, 3, 3), (2, 2, 3))
    else:
        expected = ((1,) * (p - 1) + (p + 2,), (2,) * (p - 1) + (3,))
    assert profiles == expected, (p, profiles, expected)

    r = p + 2
    k = r + p - 1
    vector = [k - 1] * r + [-r] * (p - 1)
    value = dot(vector, matvec(block_gram(p, r), vector))
    formula = -r * (k - 1) * (r - 1) * (p - 2) * k
    assert value == formula < 0

    profile_text = ",".join("(" + ",".join(map(str, q)) + ")" for q in profiles)
    inertia = "saturates" if p == 3 else "contradicts-rank3"
    return (
        f"p={p} profiles={profile_text} "
        f"block_witness={value} inertia={inertia}"
    )


def main() -> None:
    for p in PRIMES:
        print(check_prime(p))
    assert 2310 == 2 * 3 * 5 * 7 * 11
    assert 23 == 2 * 11 + 1
    assert 2310 % 23 != 0
    print("Z2310 p=11 cardinality=23 divisor_test=impossible")
    print("ALL_EXACT_CHECKS_PASS")


if __name__ == "__main__":
    main()
