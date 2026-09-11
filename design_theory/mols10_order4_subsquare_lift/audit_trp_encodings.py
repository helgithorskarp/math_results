#!/usr/bin/env python3
"""Exhaustively compare the two TRP characterizations at order four."""

from __future__ import annotations

import itertools

N = 4


def latin(square: tuple[tuple[int, ...], ...] | list[list[int]]) -> bool:
    target = list(range(N))
    return all(sorted(row) == target for row in square) and all(
        sorted(square[i][j] for i in range(N)) == target for j in range(N)
    )


def trp_direct(a, b) -> bool:
    return all(
        sum(a[i][j] == b[ip][j] for j in range(N)) <= 1
        for i in range(N)
        for ip in range(N)
    )


def composition(a, b) -> list[list[int]]:
    inverse_columns = [
        {a[i][j]: i for i in range(N)}
        for j in range(N)
    ]
    return [[inverse_columns[j][b[ip][j]] for j in range(N)] for ip in range(N)]


def generate_latin_squares():
    rows = list(itertools.permutations(range(N)))
    for candidate in itertools.product(rows, repeat=N):
        if all(len({candidate[i][j] for i in range(N)}) == N for j in range(N)):
            yield candidate


def main() -> None:
    squares = list(generate_latin_squares())
    assert len(squares) == 576
    direct_count = 0
    composition_count = 0
    for a in squares:
        for b in squares:
            direct = trp_direct(a, b)
            via_composition = latin(composition(a, b))
            assert direct == via_composition
            direct_count += direct
            composition_count += via_composition
    assert direct_count == composition_count
    print(f"latin_squares={len(squares)}")
    print(f"ordered_pairs={len(squares)**2}")
    print(f"trp_pairs={direct_count}")
    print("direct_equals_composition=true")


if __name__ == "__main__":
    main()
