#!/usr/bin/env python3
"""Exact audits for vexillary identity inflation and flag dilation."""

from __future__ import annotations

from functools import cache
from itertools import combinations, combinations_with_replacement, permutations, product
from math import comb
from random import Random


Permutation = tuple[int, ...]


def require(condition: bool, message: str = "exact check failed") -> None:
    if not condition:
        raise AssertionError(message)


def inversions(w: Permutation) -> int:
    return sum(w[i] > w[j] for i in range(len(w)) for j in range(i + 1, len(w)))


def lehmer_code(w: Permutation) -> tuple[int, ...]:
    return tuple(sum(w[i] > w[j] for j in range(i + 1, len(w))) for i in range(len(w)))


def contains_2143(w: Permutation) -> bool:
    for a, b, c, d in combinations(range(len(w)), 4):
        x1, x2, x3, x4 = w[a], w[b], w[c], w[d]
        if x2 < x1 < x4 < x3:
            return True
    return False


def is_vexillary(w: Permutation) -> bool:
    return not contains_2143(w)


def inflate_identity(w: Permutation, k: int) -> Permutation:
    require(k >= 1)
    return tuple(k * value + residue for value in w for residue in range(k))


def vexillary_data(w: Permutation) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """Canonical shape and flag; intended for vexillary permutations."""
    code = lehmer_code(w)
    lam = tuple(sorted((part for part in code if part > 0), reverse=True))
    flag = tuple(max(i + 1 for i, part in enumerate(code) if part >= row) for row in lam)
    return lam, flag


def dilate(values: tuple[int, ...], k: int) -> tuple[int, ...]:
    return tuple(k * value for value in values for _ in range(k))


def det_bareiss(matrix: list[list[int]]) -> int:
    """Fraction-free exact determinant."""
    n = len(matrix)
    if n == 0:
        return 1
    a = [row[:] for row in matrix]
    sign = 1
    previous = 1
    for column in range(n - 1):
        pivot_row = next((row for row in range(column, n) if a[row][column]), None)
        if pivot_row is None:
            return 0
        if pivot_row != column:
            a[column], a[pivot_row] = a[pivot_row], a[column]
            sign = -sign
        pivot = a[column][column]
        for row in range(column + 1, n):
            for j in range(column + 1, n):
                numerator = a[row][j] * pivot - a[row][column] * a[column][j]
                require(numerator % previous == 0, "Bareiss division was not exact")
                a[row][j] = numerator // previous
        previous = pivot
    return sign * a[-1][-1]


def complete_at_ones(degree: int, variables: int) -> int:
    if degree < 0:
        return 0
    if degree == 0:
        return 1
    return comb(variables + degree - 1, degree)


def flagged_count(lam: tuple[int, ...], flag: tuple[int, ...]) -> int:
    require(len(lam) == len(flag))
    r = len(lam)
    matrix = [
        [complete_at_ones(lam[i] - i + j, flag[i]) for j in range(r)]
        for i in range(r)
    ]
    return det_bareiss(matrix)


@cache
def transition_upsilon(w: Permutation) -> int:
    """Principal specialization via the Lascoux transition recurrence."""
    while w and w[-1] == len(w) - 1:
        w = w[:-1]
    if len(w) < 2:
        return 1
    descents = [i for i in range(len(w) - 1) if w[i] > w[i + 1]]
    if not descents:
        return 1
    r = descents[-1]
    s = max(j for j in range(r + 1, len(w)) if w[j] < w[r])
    v = list(w)
    v[r], v[s] = v[s], v[r]
    v = tuple(v)
    length_v = inversions(v)
    total = transition_upsilon(v)
    for q in range(r):
        child = list(v)
        child[q], child[r] = child[r], child[q]
        child = tuple(child)
        if inversions(child) == length_v + 1:
            total += transition_upsilon(child)
    return total


def direct_flagged_count(lam: tuple[int, ...], flag: tuple[int, ...]) -> int:
    cells = [(i, j) for i, length in enumerate(lam) for j in range(length)]
    values: dict[tuple[int, int], int] = {}

    def rec(index: int) -> int:
        if index == len(cells):
            return 1
        i, j = cells[index]
        lower = 1
        if j:
            lower = max(lower, values[i, j - 1])
        if i and j < lam[i - 1]:
            lower = max(lower, values[i - 1, j] + 1)
        total = 0
        for value in range(lower, flag[i] + 1):
            values[i, j] = value
            total += rec(index + 1)
        values.pop((i, j), None)
        return total

    return rec(0)


def partitions(rows: int, largest: int):
    for candidate in product(range(1, largest + 1), repeat=rows):
        if all(candidate[i] >= candidate[i + 1] for i in range(rows - 1)):
            yield candidate


def admissible_flags(rows: int, maximum: int):
    for flag in combinations_with_replacement(range(1, maximum + 1), rows):
        if all(flag[i] >= i + 1 for i in range(rows)):
            yield flag


def audit_permutations() -> tuple[list[int], int, int]:
    counts = []
    k3_cases = 0
    for n in range(1, 8):
        count = 0
        for w in permutations(range(n)):
            if not is_vexillary(w):
                continue
            count += 1
            lam, flag = vexillary_data(w)
            require(flagged_count(lam, flag) == transition_upsilon(w))
            for k in (2,):
                image = inflate_identity(w, k)
                require(is_vexillary(image))
                require(lehmer_code(image) == dilate(lehmer_code(w), k))
                require(vexillary_data(image) == (dilate(lam, k), dilate(flag, k)))
            if n <= 6:
                k = 3
                image = inflate_identity(w, k)
                require(is_vexillary(image))
                require(lehmer_code(image) == dilate(lehmer_code(w), k))
                require(vexillary_data(image) == (dilate(lam, k), dilate(flag, k)))
                k3_cases += 1
        counts.append(count)
    return counts, sum(counts), k3_cases


def audit_direct_tableaux() -> int:
    cases = 0
    for rows in range(1, 4):
        for lam in partitions(rows, 3):
            for flag in admissible_flags(rows, 5):
                require(flagged_count(lam, flag) == direct_flagged_count(lam, flag))
                cases += 1
    return cases


def audit_exhaustive_frontier() -> int:
    cases = 0
    for rows in range(1, 5):
        for lam in partitions(rows, 5):
            for flag in admissible_flags(rows, 7):
                base = flagged_count(lam, flag)
                image = flagged_count(dilate(lam, 2), dilate(flag, 2))
                require(image >= base**4)
                cases += 1
    return cases


def audit_sampled_frontier() -> dict[int, int]:
    rng = Random(20260921)
    counts = {}
    for k in (2, 3, 4):
        cases = 0
        for _ in range(2000):
            rows = rng.randint(1, 7 if k == 2 else 5)
            lam = tuple(sorted((rng.randint(1, 15) for _ in range(rows)), reverse=True))
            raw = sorted(rng.randint(1, 18) for _ in range(rows))
            flag = tuple(max(raw[i], i + 1) for i in range(rows))
            base = flagged_count(lam, flag)
            image = flagged_count(dilate(lam, k), dilate(flag, k))
            require(image >= base ** (k * k))
            cases += 1
        counts[k] = cases
    return counts


def main() -> None:
    counts, permutation_cases, k3_cases = audit_permutations()
    direct_cases = audit_direct_tableaux()
    exhaustive_cases = audit_exhaustive_frontier()
    sampled = audit_sampled_frontier()

    example = (2, 0, 3, 1)  # one-based 3142
    lam, flag = vexillary_data(example)
    base = flagged_count(lam, flag)
    image = flagged_count(dilate(lam, 2), dilate(flag, 2))
    require((lam, flag, base, image) == ((2, 1), (1, 3), 2, 20))

    print(f"vexillary_counts_through_S7={counts}")
    print(f"permutation_bridge_cases={permutation_cases}")
    print(f"additional_k3_bridge_cases={k3_cases}")
    print(f"direct_tableau_determinant_cases={direct_cases}")
    print(f"exhaustive_k2_frontier_cases={exhaustive_cases}")
    print(f"sampled_frontier_cases={sampled}")
    print(f"example_3142=(lambda={lam}, flag={flag}, base={base}, inflated_k2={image})")
    print("status=PASS")


if __name__ == "__main__":
    main()
