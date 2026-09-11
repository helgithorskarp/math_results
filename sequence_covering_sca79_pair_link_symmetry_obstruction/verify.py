#!/usr/bin/env python3
"""Exact certificate for the coordinate-symmetric pair-link obstruction."""

from __future__ import annotations

from itertools import permutations
from math import comb, factorial
from pathlib import Path


POINT_CELL = (560, 70, 20, 10, 8, 10, 20, 70, 560)
Q_BY_SORTED_COMPOSITION = {
    (7, 0, 0): 70,
    (6, 1, 0): 10,
    (5, 2, 0): 5,
    (5, 1, 1): 0,
    (4, 3, 0): 1,
    (4, 2, 1): 1,
    (3, 3, 1): 1,
    (3, 2, 2): 0,
}


def multinomial(parts: tuple[int, ...]) -> int:
    answer = factorial(sum(parts))
    for part in parts:
        answer //= factorial(part)
    return answer


def load_r() -> dict[tuple[int, int, int], int]:
    path = (
        Path(__file__).resolve().parents[1]
        / "sequence_covering_sca79_pair_link_kernel"
        / "ASYMMETRIC_PROFILE.tsv"
    )
    lines = path.read_text(encoding="ascii").splitlines()
    assert lines[0] == "before\tbetween\tafter\tvalue"
    table: dict[tuple[int, int, int], int] = {}
    for line in lines[1:]:
        a, b, c, value = map(int, line.split("\t"))
        table[a, b, c] = value
    assert len(table) == 36
    return table


def main() -> None:
    # Every symbol occurs 560 times in each position under the uniform point
    # profile: choose its exact predecessor set, then use that point-link cell.
    position_counts = tuple(comb(8, i) * POINT_CELL[i] for i in range(9))
    assert position_counts == (560,) * 9

    composition = (0, 2, 5)
    labelled_cells = multinomial(composition)
    quotient, remainder = divmod(position_counts[0], labelled_cells)
    assert labelled_cells == 21
    assert (quotient, remainder) == (26, 14)

    # The previous bundle passes the unresolved global composition identity.
    # Q(0,2,5)=5.  Across the six region relabellings, R takes the six values
    # obtained by permuting the entries of (0,2,5).
    r = load_r()
    q_value = Q_BY_SORTED_COMPOSITION[tuple(sorted(composition, reverse=True))]
    r_orbit_values = tuple(r[tuple(composition[i] for i in sigma)] for sigma in permutations(range(3)))
    aggregate_cell_value = 36 * q_value + 6 * sum(r_orbit_values)
    assert q_value == 5
    assert sorted(r_orbit_values) == [0, 0, 2, 2, 3, 3]
    assert aggregate_cell_value == factorial(0) * factorial(2) * factorial(5) == 240
    assert labelled_cells * aggregate_cell_value == 5040

    # List every positional region-size triple for which coordinate symmetry
    # would force a divisor of the uniform count 560.
    failing: list[tuple[tuple[int, int, int], int, int]] = []
    for i in range(9):
        for j in range(i + 1, 9):
            parts = (i, j - i - 1, 8 - j)
            divisor = multinomial(parts)
            rem = 560 % divisor
            if rem:
                failing.append((parts, divisor, rem))
    assert len(failing) == 18
    assert (composition, 21, 14) in failing

    print("point-position counts:", " ".join(map(str, position_counts)))
    print("certificate: C(7,2)=21, 560 mod 21=14")
    print("Q/R aggregate at (0,2,5): 240 cells, 21*240=5040")
    print("failing positional triples:", len(failing))
    print("conclusion: every symbol needs an outgoing and an incoming asymmetric pair link")
    print("minimum asymmetric ordered-pair links: 9")
    print("all checks passed")


if __name__ == "__main__":
    main()
