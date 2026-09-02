#!/usr/bin/env python3
"""Exact insertion-based verification of the layered-pattern theorem."""

from __future__ import annotations

import argparse
from itertools import combinations_with_replacement


Permutation = tuple[int, ...]
Triple = tuple[Permutation, tuple[int, int], tuple[int, int]]


def compositions(n: int):
    """Yield all compositions of n in a deterministic order."""
    if n < 1:
        raise ValueError("n must be positive")
    for mask in range(1 << (n - 1)):
        parts: list[int] = []
        current = 1
        for bit in range(n - 1):
            if mask & (1 << bit):
                parts.append(current)
                current = 1
            else:
                current += 1
        parts.append(current)
        yield tuple(parts)


def layered(parts: tuple[int, ...]) -> Permutation:
    result: list[int] = []
    offset = 0
    for size in parts:
        result.extend(range(offset + size, offset, -1))
        offset += size
    return tuple(result)


def is_active_site(beta: Permutation, row: int, column: int) -> bool:
    """Ray--West activity for a one-point grid site, in 1-based coordinates."""
    m = len(beta)
    hit_on_right = column <= m and beta[column - 1] == row
    hit_on_left = column > 1 and beta[column - 2] == row
    return not (hit_on_right or hit_on_left)


def is_active_triple(beta: Permutation, triple: Triple) -> bool:
    rho, rows, columns = triple
    return all(
        is_active_site(beta, rows[rho[j] - 1], columns[j])
        for j in range(2)
    )


def insert(beta: Permutation, triple: Triple) -> Permutation:
    """Insert a 2-permutation using Ray--West multigrid coordinates."""
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


def internal_layer_witness(beta: Permutation, q: int) -> tuple[Triple, Triple]:
    """Witness for a boundary q|q+1 inside a decreasing layer."""
    v = beta[q]  # beta(q+1), because q is 1-based but tuples are 0-based
    if beta[q - 1] != v + 1:
        raise AssertionError("not a descending bond")
    left = ((2, 1), (v, v), (q, q))
    right = ((2, 1), (v + 2, v + 2), (q + 2, q + 2))
    return left, right


def between_layer_witness(p: int, q: int, r: int) -> tuple[Triple, Triple]:
    """Witness when adjacent layers occupy p+1..q and q+1..r."""
    first = (p + 1, q)
    second = (q + 2, r + 1)
    return ((1, 2), first, second), ((1, 2), second, first)


def expected_g2(m: int) -> int:
    return (m**4 + 2 * m**3 + m**2 + 2 * m + 6) // 2


def verify_pattern(parts: tuple[int, ...]) -> None:
    beta = layered(parts)
    boundary_count = 0
    p = 0
    for layer_index, size in enumerate(parts):
        q_end = p + size
        for q in range(p + 1, q_end):
            left, right = internal_layer_witness(beta, q)
            if not is_active_triple(beta, left):
                raise AssertionError((beta, q, "inactive internal witness"))
            if insert(beta, left) != insert(beta, right):
                raise AssertionError((beta, q, "failed internal synonymity"))
            boundary_count += 1

        if layer_index + 1 < len(parts):
            r = q_end + parts[layer_index + 1]
            left, right = between_layer_witness(p, q_end, r)
            if not is_active_triple(beta, left):
                raise AssertionError((beta, q_end, "inactive inter-layer witness"))
            if insert(beta, left) != insert(beta, right):
                raise AssertionError((beta, q_end, "failed inter-layer synonymity"))
            boundary_count += 1
        p = q_end

    if boundary_count != len(beta) - 1:
        raise AssertionError((beta, boundary_count, "wrong witness count"))

    actual = len({insert(beta, triple) for triple in active_triples(beta)})
    expected = expected_g2(len(beta))
    if actual != expected:
        raise AssertionError((beta, actual, expected, "wrong upper-shadow size"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=9)
    args = parser.parse_args()
    if not 1 <= args.max_n <= 11:
        parser.error("--max-n must lie between 1 and 11")

    total = 0
    for n in range(1, args.max_n + 1):
        count = 0
        for parts in compositions(n):
            verify_pattern(parts)
            count += 1
        expected_count = 1 << (n - 1)
        if count != expected_count:
            raise AssertionError((n, count, expected_count))
        total += count
        print(f"n={n}: verified {count} layered patterns; g2={expected_g2(n)}")
    print(
        f"verified {total} layered patterns through n={args.max_n}; "
        "all witnesses and g2 values agree"
    )


if __name__ == "__main__":
    main()
