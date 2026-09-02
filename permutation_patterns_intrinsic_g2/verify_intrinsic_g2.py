#!/usr/bin/env python3
"""Insertion-level exhaustive verifier for the rooted-lens formula."""

from __future__ import annotations

import argparse
from collections import defaultdict
from itertools import combinations_with_replacement, permutations

from intrinsic_g2 import intrinsic_boundaries, lens, rooted_lenses


Permutation = tuple[int, ...]
Triple = tuple[Permutation, tuple[int, int], tuple[int, int]]


def is_active_site(beta: Permutation, row: int, column: int) -> bool:
    m = len(beta)
    hit_on_right = column <= m and beta[column - 1] == row
    hit_on_left = column > 1 and beta[column - 2] == row
    return not (hit_on_right or hit_on_left)


def is_active_triple(beta: Permutation, triple: Triple) -> bool:
    rho, rows, columns = triple
    return all(
        is_active_site(beta, rows[rho[index] - 1], columns[index])
        for index in range(2)
    )


def insert(beta: Permutation, triple: Triple) -> Permutation:
    rho, rows, columns = triple
    m = len(beta)
    result: list[int | None] = [None] * (m + 2)

    for column_rank, row_rank in enumerate(rho, start=1):
        full_column = columns[column_rank - 1] + column_rank - 1
        full_row = rows[row_rank - 1] + row_rank - 1
        result[full_column - 1] = full_row

    for old_column, old_row in enumerate(beta, start=1):
        full_column = old_column + sum(column <= old_column for column in columns)
        full_row = old_row + sum(row <= old_row for row in rows)
        if result[full_column - 1] is not None:
            raise AssertionError("insertion collision")
        result[full_column - 1] = full_row

    answer = tuple(value for value in result if value is not None)
    if len(answer) != m + 2 or sorted(answer) != list(range(1, m + 3)):
        raise AssertionError("insertion did not produce a permutation")
    return answer


def active_triples(beta: Permutation):
    sites = range(1, len(beta) + 2)
    for rows in combinations_with_replacement(sites, 2):
        for columns in combinations_with_replacement(sites, 2):
            for rho in ((1, 2), (2, 1)):
                triple = (rho, rows, columns)
                if is_active_triple(beta, triple):
                    yield triple


def insertion_data(beta: Permutation) -> tuple[int, tuple[int, ...]]:
    """Return g2 and the boundaries of separated-grid synonymities."""
    images: dict[Permutation, list[Triple]] = defaultdict(list)
    for triple in active_triples(beta):
        images[insert(beta, triple)].append(triple)

    boundaries: set[int] = set()
    for triples in images.values():
        triples.sort(key=lambda triple: triple[1])
        for index, left in enumerate(triples[:-1]):
            for right in reversed(triples[index + 1 :]):
                rows_separated = max(left[1]) < min(right[1])
                columns_forward = max(left[2]) < min(right[2])
                columns_backward = max(right[2]) < min(left[2])
                if rows_separated and (columns_forward or columns_backward):
                    boundary = (
                        max(left[2])
                        if columns_forward
                        else min(left[2]) - 2
                    )
                    if not 1 <= boundary < len(beta):
                        raise AssertionError((beta, left, right, boundary))
                    boundaries.add(boundary)
                    break
    return len(images), tuple(sorted(boundaries))


def check_lens_witnesses(n: int) -> None:
    for h in range(1, n // 2 + 1):
        for a in range(n - 2 * h + 1):
            c = n - 2 * h - a
            for w in range(1, min(a + h, h + c) + 1):
                beta, boundary = lens(a, h, c, w)
                d = h + c - w
                left = ((2, 1), (1, a + 1), (1, d + 1))
                right = (
                    (2, 1),
                    (a + 2 * h + 1, n + 1),
                    (d + 2 * w + 1, n + 1),
                )
                if boundary != d + 1:
                    raise AssertionError("wrong distinguished boundary")
                if not is_active_triple(beta, left):
                    raise AssertionError((beta, left, "inactive lens witness"))
                if insert(beta, left) != insert(beta, right):
                    raise AssertionError((beta, left, right, "failed synonymity"))


def expected_j_from_g2(n: int, g2: int) -> int:
    numerator = n**4 + 2 * n**3 + n**2 + 4 * n + 4 - 2 * g2
    if numerator % 2:
        raise AssertionError((n, g2, numerator))
    return numerator // 2


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=7)
    args = parser.parse_args()
    if not 1 <= args.max_n <= 8:
        parser.error("--max-n must lie between 1 and 8")

    total = 0
    for n in range(1, args.max_n + 1):
        check_lens_witnesses(n)
        count = 0
        for beta in permutations(range(1, n + 1)):
            predicted = intrinsic_boundaries(beta)
            g2, separated_boundaries = insertion_data(beta)
            j = expected_j_from_g2(n, g2)
            if predicted != separated_boundaries or len(predicted) != j:
                raise AssertionError(
                    (beta, predicted, separated_boundaries, g2, j)
                )
            count += 1
        total += count
        print(
            f"n={n}: verified {count} permutations; "
            f"rooted_lens_catalogue={len(rooted_lenses(n))}",
            flush=True,
        )
    print(
        f"verified {total} permutations through n={args.max_n}; "
        "intrinsic, separated-grid, and Ray-West j values agree"
    )


if __name__ == "__main__":
    main()
