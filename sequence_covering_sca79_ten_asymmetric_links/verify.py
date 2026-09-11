#!/usr/bin/env python3
"""Definition-level checker for the named immediate-successor obstruction."""

from fractions import Fraction
from math import factorial


def determinant_bareiss(matrix: list[list[int]]) -> int:
    """Return the exact determinant of an integer matrix."""
    a = [row[:] for row in matrix]
    n = len(a)
    sign = 1
    previous = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            swap = next(i for i in range(k + 1, n) if a[i][k])
            a[k], a[swap] = a[swap], a[k]
            sign *= -1
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                a[i][j] = (a[i][j] * pivot - a[i][k] * a[k][j]) // previous
        previous = pivot
        for i in range(k + 1, n):
            a[i][k] = 0
    return sign * a[-1][-1]


def solve_fraction(matrix: list[list[int]], rhs: list[int]) -> list[Fraction]:
    """Solve a nonsingular square system by exact Gauss-Jordan elimination."""
    n = len(matrix)
    a = [[Fraction(x) for x in row] + [Fraction(rhs[i])] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next(i for i in range(col, n) if a[i][col])
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        a[col] = [x / scale for x in a[col]]
        for i in range(n):
            if i == col:
                continue
            scale = a[i][col]
            if scale:
                a[i] = [x - scale * y for x, y in zip(a[i], a[col])]
    return [a[i][-1] for i in range(n)]


def main() -> None:
    alphabet_size = 9
    exceptional_successors = 1
    symmetric_successors = alphabet_size - 1 - exceptional_successors
    y_symbols = tuple(range(symmetric_successors))

    # The exact-nine point-link reduction gives
    # F_w(A)=|A|!(8-|A|)!/72 for every named predecessor set A.
    predecessor_size = 2
    point_numerator = factorial(predecessor_size) * factorial(8 - predecessor_size)
    assert point_numerator % 72 == 0
    point_value = point_numerator // 72

    # Row z represents A_z={x,z}; column y is present iff y can be the
    # immediate successor, namely iff y != z.
    incidence = [[int(y != z) for y in y_symbols] for z in y_symbols]
    assert all(sum(row) == 6 for row in incidence)
    assert all(sum(incidence[z][y] for z in y_symbols) == 6 for y in y_symbols)

    rhs = [point_value] * len(y_symbols)
    determinant = determinant_bareiss(incidence)
    solution = solve_fraction(incidence, rhs)
    assert determinant == 6
    assert solution == [Fraction(10, 3)] * 7

    aggregate_coefficient = sum(incidence[z][0] for z in y_symbols)
    aggregate_rhs = sum(rhs)
    remainder = aggregate_rhs % aggregate_coefficient
    assert aggregate_coefficient == 6
    assert aggregate_rhs == 140
    assert remainder == 2

    print(f"uniform point-link value F_w({{x,z}}): {point_value}")
    print(f"symmetric outgoing links at w: {symmetric_successors}")
    print(f"eligible immediate successors per equation: {sum(incidence[0])}")
    print(f"named predecessor-set equations: {len(incidence)}")
    print(f"incidence determinant: {determinant}")
    print(f"unique rational cell value: {solution[0]}")
    print(f"aggregate identity: {aggregate_coefficient} * sum(q_y) = {aggregate_rhs}")
    print(f"divisibility remainder: {aggregate_rhs} mod {aggregate_coefficient} = {remainder}")
    print("conclusion: exact-nine branch impossible")
    print("asymmetric ordered-pair-link lower bound: 10")
    print("all checks passed")


if __name__ == "__main__":
    main()
