#!/usr/bin/env python3
"""Exact audits for the residue-tagged flagged-tableau row union."""

from __future__ import annotations

import hashlib
import json
import sys
from functools import cache
from itertools import combinations_with_replacement, product
from math import comb


Shape = tuple[int, ...]
Flag = tuple[int, ...]
Tableau = tuple[tuple[int, ...], ...]


def require(condition: bool, message: str = "exact check failed") -> None:
    if not condition:
        raise AssertionError(message)


def is_partition(shape: Shape) -> bool:
    return all(part >= 0 for part in shape) and all(
        shape[i] >= shape[i + 1] for i in range(len(shape) - 1)
    )


def is_flag(flag: Flag) -> bool:
    return all(value >= 1 for value in flag) and all(
        flag[i] <= flag[i + 1] for i in range(len(flag) - 1)
    )


def is_flagged_tableau(tableau: Tableau, shape: Shape, flag: Flag) -> bool:
    if not (len(tableau) == len(shape) == len(flag)):
        return False
    if not is_partition(shape) or not is_flag(flag):
        return False
    for i, row in enumerate(tableau):
        if len(row) != shape[i]:
            return False
        if any(value < 1 or value > flag[i] for value in row):
            return False
        if any(row[j] > row[j + 1] for j in range(len(row) - 1)):
            return False
        if i and any(tableau[i - 1][j] >= row[j] for j in range(len(row))):
            return False
    return True


@cache
def tableaux(shape: Shape, flag: Flag) -> tuple[Tableau, ...]:
    require(len(shape) == len(flag) and is_partition(shape) and is_flag(flag))
    cells = tuple((i, j) for i, length in enumerate(shape) for j in range(length))
    values: dict[tuple[int, int], int] = {}
    result: list[Tableau] = []

    def visit(index: int) -> None:
        if index == len(cells):
            result.append(
                tuple(tuple(values[i, j] for j in range(shape[i])) for i in range(len(shape)))
            )
            return
        i, j = cells[index]
        lower = 1
        if j:
            lower = max(lower, values[i, j - 1])
        if i and j < shape[i - 1]:
            lower = max(lower, values[i - 1, j] + 1)
        for value in range(lower, flag[i] + 1):
            values[i, j] = value
            visit(index + 1)
        values.pop((i, j), None)

    visit(0)
    return tuple(result)


def merge(tableaux_: tuple[Tableau, ...]) -> Tableau:
    k = len(tableaux_)
    require(k >= 1)
    rows = len(tableaux_[0])
    require(all(len(tableau) == rows for tableau in tableaux_))
    return tuple(
        tuple(
            sorted(
                k * (value - 1) + q
                for q, tableau in enumerate(tableaux_, start=1)
                for value in tableau[i]
            )
        )
        for i in range(rows)
    )


def split(merged: Tableau, shapes: tuple[Shape, ...]) -> tuple[Tableau, ...]:
    k = len(shapes)
    require(k >= 1)
    rows = len(merged)
    require(all(len(shape) == rows for shape in shapes))
    recovered: list[list[tuple[int, ...]]] = [[] for _ in range(k)]
    for i, row in enumerate(merged):
        buckets: list[list[int]] = [[] for _ in range(k)]
        for value in row:
            q = (value - 1) % k
            buckets[q].append(1 + (value - (q + 1)) // k)
        for q in range(k):
            require(len(buckets[q]) == shapes[q][i], "wrong residue multiplicity")
            recovered[q].append(tuple(buckets[q]))
    return tuple(tuple(rows_) for rows_ in recovered)


def weight(tableau: Tableau) -> tuple[tuple[int, int], ...]:
    counts: dict[int, int] = {}
    for row in tableau:
        for value in row:
            counts[value] = counts.get(value, 0) + 1
    return tuple(sorted(counts.items()))


def transformed_weight(tableaux_: tuple[Tableau, ...]) -> tuple[tuple[int, int], ...]:
    k = len(tableaux_)
    counts: dict[int, int] = {}
    for q, tableau in enumerate(tableaux_, start=1):
        for row in tableau:
            for value in row:
                image = k * (value - 1) + q
                counts[image] = counts.get(image, 0) + 1
    return tuple(sorted(counts.items()))


def complete_at_ones(degree: int, variables: int) -> int:
    if degree < 0:
        return 0
    return comb(variables + degree - 1, degree)


def det_bareiss(matrix: list[list[int]]) -> int:
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
                require(numerator % previous == 0, "nonexact Bareiss division")
                a[row][j] = numerator // previous
        previous = pivot
    return sign * a[-1][-1]


def flagged_count(shape: Shape, flag: Flag) -> int:
    require(len(shape) == len(flag))
    n = len(shape)
    return det_bareiss(
        [
            [complete_at_ones(shape[i] - i + j, flag[i]) for j in range(n)]
            for i in range(n)
        ]
    )


def shapes(rows: int, maximum: int):
    for shape in product(range(maximum + 1), repeat=rows):
        if is_partition(shape):
            yield shape


def flags(rows: int, maximum: int):
    yield from combinations_with_replacement(range(1, maximum + 1), rows)


def audit_injection() -> dict[str, int]:
    source_tuples = 0
    target_checks = 0
    distinctness_checks = 0
    determinant_checks = 0

    for rows in range(1, 4):
        shape_box = tuple(shapes(rows, 3))
        for flag in flags(rows, 4):
            for shape in shape_box:
                direct = tableaux(shape, flag)
                require(len(direct) == flagged_count(shape, flag))
                determinant_checks += 1

            # Different-shape theorem, k=2.  Bound total cells so the full
            # Cartesian product remains a transparent definition-level audit.
            for first in shape_box:
                first_tableaux = tableaux(first, flag)
                if not first_tableaux:
                    continue
                for second in shape_box:
                    if sum(first) + sum(second) > 8:
                        continue
                    second_tableaux = tableaux(second, flag)
                    if not second_tableaux:
                        continue
                    target_shape = tuple(a + b for a, b in zip(first, second))
                    target_flag = tuple(2 * value for value in flag)
                    images = set()
                    for pair in product(first_tableaux, second_tableaux):
                        image = merge(pair)
                        require(is_flagged_tableau(image, target_shape, target_flag))
                        require(split(image, (first, second)) == pair)
                        require(weight(image) == transformed_weight(pair))
                        images.add(image)
                        source_tuples += 1
                        target_checks += 1
                    require(len(images) == len(first_tableaux) * len(second_tableaux))
                    require(flagged_count(target_shape, target_flag) >= len(images))
                    distinctness_checks += len(images)

    # Equal-shape k=3 checks, kept deliberately small but entry-complete.
    for rows in range(1, 3):
        for flag in flags(rows, 3):
            for shape in shapes(rows, 2):
                inputs = tableaux(shape, flag)
                if not inputs or len(inputs) ** 3 > 20_000:
                    continue
                target_shape = tuple(3 * value for value in shape)
                target_flag = tuple(3 * value for value in flag)
                images = set()
                for triple in product(inputs, repeat=3):
                    image = merge(triple)
                    require(is_flagged_tableau(image, target_shape, target_flag))
                    require(split(image, (shape, shape, shape)) == triple)
                    require(weight(image) == transformed_weight(triple))
                    images.add(image)
                    source_tuples += 1
                    target_checks += 1
                require(len(images) == len(inputs) ** 3)
                require(flagged_count(target_shape, target_flag) >= len(images))
                distinctness_checks += len(images)

    return {
        "source_tuples": source_tuples,
        "target_tableau_checks": target_checks,
        "distinct_images": distinctness_checks,
        "direct_determinant_checks": determinant_checks,
    }


def audit_boundary() -> dict[str, int]:
    shape = (1,)
    flag = (1,)
    horizontal_shape = (2,)
    horizontal_flag = (2,)
    full_shape = (2, 2)
    full_flag = (2, 2)
    base = flagged_count(shape, flag)
    horizontal = flagged_count(horizontal_shape, horizontal_flag)
    full = flagged_count(full_shape, full_flag)
    require((base, horizontal, full) == (1, 3, 1))
    return {"base": base, "horizontal": horizontal, "full_dilation": full}


def main() -> None:
    record = {
        "arithmetic": "exact Python integers and tuples",
        "boundary": audit_boundary(),
        "injection_audit": audit_injection(),
        "python": sys.version.split()[0],
    }
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"))
    print(json.dumps(record, sort_keys=True, indent=2))
    print(f"record_sha256={hashlib.sha256(canonical.encode()).hexdigest()}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
