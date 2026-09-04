#!/usr/bin/env python3
"""Independent exact audit of the rational-row-span terminal objection."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations, product
from math import gcd

Vector = tuple[int, ...]

PATH = ((0, 3), (1, 3), (2, 5), (2, 4))
ROWS = (
    (1, 1, 1, 1, 0, 0),
    (0, 1, 1, 0, 1, 0),
    (0, 0, 1, 1, 1, 1),
    (1, 0, 0, 1, 1, 0),
)
E5 = (0, 0, 0, 0, 1, 0)
CLAIMED_LABELS = (
    (1, 1, 0),
    (1, 0, 1),
    (1, 1, 1),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
)


def transition(ordering: Vector, interval: tuple[int, int]) -> tuple[Vector, Vector]:
    """The child transition implemented in the archived treeSearch.py."""
    i, j = interval
    n = len(ordering)
    assert 0 <= i < j < n and j - i <= n // 2
    row = tuple(int(label in ordering[i : j + 1]) for label in range(1, n + 1))
    child = list(ordering)
    if i:
        child[i - 1], child[i] = child[i], child[i - 1]
    else:
        child[j], child[j + 1] = child[j + 1], child[j]
    return tuple(child), row


def reconstruct_branch() -> tuple[tuple[Vector, ...], tuple[Vector, ...]]:
    ordering = tuple(range(1, 7))
    orderings = [ordering]
    rows = []
    for interval in PATH:
        ordering, row = transition(ordering, interval)
        orderings.append(ordering)
        rows.append(row)
    assert tuple(rows) == ROWS
    return tuple(orderings), tuple(rows)


def rank_q(rows: tuple[Vector, ...] | list[Vector]) -> int:
    if not rows:
        return 0
    matrix = [[Fraction(x) for x in row] for row in rows]
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next((r for r in range(rank, len(matrix)) if matrix[r][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [x / scale for x in matrix[rank]]
        for r in range(len(matrix)):
            if r != rank and matrix[r][column]:
                scale = matrix[r][column]
                matrix[r] = [x - scale * y for x, y in zip(matrix[r], matrix[rank])]
        rank += 1
    return rank


def in_span_q(rows: tuple[Vector, ...], target: Vector) -> bool:
    return rank_q(rows) == rank_q([*rows, target])


def standard_targets(n: int = 6) -> list[tuple[str, Vector]]:
    result = []
    for i in range(n):
        result.append((f"e{i + 1}", tuple(int(j == i) for j in range(n))))
    for i, j in combinations(range(n), 2):
        result.append(
            (f"e{i + 1}-e{j + 1}", tuple(int(k == i) - int(k == j) for k in range(n)))
        )
    return result


def rational_terminals(rows: tuple[Vector, ...]) -> list[str]:
    return [name for name, target in standard_targets() if in_span_q(rows, target)]


def determinant(matrix: list[list[int]]) -> int:
    """Fraction-free Bareiss determinant."""
    a = [row[:] for row in matrix]
    n = len(a)
    sign = 1
    previous = 1
    for column in range(n - 1):
        pivot = next((r for r in range(column, n) if a[r][column]), None)
        if pivot is None:
            return 0
        if pivot != column:
            a[column], a[pivot] = a[pivot], a[column]
            sign = -sign
        value = a[column][column]
        for r in range(column + 1, n):
            for c in range(column + 1, n):
                a[r][c] = (a[r][c] * value - a[r][column] * a[column][c]) // previous
        previous = value
    return sign * a[-1][-1]


def maximal_minors(rows: tuple[Vector, ...]) -> list[int]:
    return [
        determinant([[row[column] for column in columns] for row in rows])
        for columns in combinations(range(6), 4)
    ]


def xor_sum(row: Vector, labels: tuple[Vector, ...]) -> Vector:
    return tuple(
        sum(coefficient * label[c] for coefficient, label in zip(row, labels)) % 2
        for c in range(3)
    )


def countermodel(labels: tuple[Vector, ...]) -> bool:
    return (
        len(labels) == 6
        and len(set(labels)) == 6
        and (0, 0, 0) not in labels
        and all(xor_sum(row, labels) == (0, 0, 0) for row in ROWS)
        and xor_sum(E5, labels) != (0, 0, 0)
    )


def enumerate_countermodels() -> list[tuple[Vector, ...]]:
    nonzero = tuple(bits for bits in product((0, 1), repeat=3) if any(bits))
    return [labels for labels in permutations(nonzero, 6) if countermodel(labels)]


def audit() -> dict[str, object]:
    orderings, rows = reconstruct_branch()
    prefix_terminals = [rational_terminals(rows[:depth]) for depth in range(1, 5)]
    assert prefix_terminals == [[], [], [], ["e5"]]

    # The unique rational coefficients are (-1/2,1/2,0,1/2), since the rows
    # are independent and -r1+r2+r4=2e5.  Thus e5 is in Sat(L), not in L.
    assert rank_q(rows) == 4
    relation = tuple(-rows[0][i] + rows[1][i] + rows[3][i] for i in range(6))
    assert relation == tuple(2 * x for x in E5)
    rational_coefficients = (Fraction(-1, 2), Fraction(1, 2), Fraction(0), Fraction(1, 2))
    assert tuple(
        sum(coefficient * row[i] for coefficient, row in zip(rational_coefficients, rows))
        for i in range(6)
    ) == E5

    minors = maximal_minors(rows)
    nonzero_minors = [value for value in minors if value]
    index = 0
    for value in nonzero_minors:
        index = gcd(index, abs(value))
    assert set(nonzero_minors) == {-2, 2}
    assert index == 2  # [Sat(row_Z(C)) : row_Z(C)]

    models = enumerate_countermodels()
    assert len(models) == 168
    assert CLAIMED_LABELS in models

    return {
        "path": PATH,
        "orderings": orderings,
        "prefix_rational_terminals": prefix_terminals,
        "rational_coefficients_for_e5": [str(x) for x in rational_coefficients],
        "nonzero_maximal_minors": sorted(nonzero_minors),
        "row_lattice_saturation_index": index,
        "injective_nonzero_F2_3_assignments_tested": 5040,
        "F2_3_countermodels": len(models),
        "claimed_countermodel_present": True,
    }


def main() -> None:
    result = audit()
    for key, value in result.items():
        print(f"{key}={value}")
    print("VERDICT=rational row-span is not a sound arbitrary-abelian terminal")


if __name__ == "__main__":
    main()
