#!/usr/bin/env python3
"""Exact checker for the ternary ordered-pair link of PSCA(9,7,1)."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations, product
from math import comb, factorial
from pathlib import Path


BASE = (560, 70, 20, 10, 8, 10, 20, 70, 560)
ORBITS = (
    (7, 0, 0),
    (6, 1, 0),
    (5, 2, 0),
    (5, 1, 1),
    (4, 3, 0),
    (4, 2, 1),
    (3, 3, 1),
    (3, 2, 2),
)
Q_VALUES = (70, 10, 5, 0, 1, 1, 1, 0)
Q = dict(zip(ORBITS, Q_VALUES, strict=True))


def q_value(word: tuple[int, ...] | list[int]) -> int:
    counts = tuple(sorted((word.count(0), word.count(1), word.count(2)), reverse=True))
    return Q[counts]


def load_asymmetric_profile() -> dict[tuple[int, int, int], int]:
    path = Path(__file__).with_name("ASYMMETRIC_PROFILE.tsv")
    lines = path.read_text(encoding="ascii").splitlines()
    assert lines[0] == "before\tbetween\tafter\tvalue"
    table = {}
    for line in lines[1:]:
        first, second, third, value = map(int, line.split("\t"))
        assert first + second + third == 7
        table[first, second, third] = value
    assert len(table) == 36
    return table


def composition_value(
    word: tuple[int, ...] | list[int], table: dict[tuple[int, int, int], int]
) -> int:
    counts = tuple(word.count(value) for value in range(3))
    return table[counts]


def verify_all_marginals(value_function) -> int:
    checked = 0
    for omitted in combinations(range(7), 2):
        fixed_coordinates = [i for i in range(7) if i not in omitted]
        for fixed_values in product(range(3), repeat=5):
            word = [0] * 7
            for coordinate, value in zip(fixed_coordinates, fixed_values, strict=True):
                word[coordinate] = value
            observed = 0
            for first, second in product(range(3), repeat=2):
                word[omitted[0]] = first
                word[omitted[1]] = second
                observed += value_function(word)
            counts = [fixed_values.count(value) for value in range(3)]
            expected = factorial(counts[0]) * factorial(counts[1]) * factorial(counts[2])
            assert observed == expected
            checked += 1
    assert checked == comb(7, 2) * 3**5 == 5103
    return checked


def verify_boundary_projections(value_function) -> int:
    checked = 0
    coordinates = range(7)
    for mask in range(1 << 7):
        zero_set = {i for i in coordinates if mask >> i & 1}
        free = [i for i in coordinates if i not in zero_set]
        observed = 0
        for values in product((1, 2), repeat=len(free)):
            word = [0] * 7
            for i in zero_set:
                word[i] = 0
            for i, value in zip(free, values, strict=True):
                word[i] = value
            observed += value_function(word)
        assert observed == BASE[len(zero_set)]
        checked += 1

        non_after_set = zero_set
        observed = 0
        for values in product((0, 1), repeat=len(non_after_set)):
            word = [2] * 7
            for i, value in zip(sorted(non_after_set), values, strict=True):
                word[i] = value
            observed += value_function(word)
        assert observed == BASE[len(non_after_set) + 1]
        checked += 1
    assert checked == 256
    return checked


def gf2_marginal_rank() -> int:
    """Rank over F_2 of the 5103-by-2187 marginal matrix."""

    powers = [3**i for i in range(7)]
    pivots: dict[int, int] = {}
    for omitted in combinations(range(7), 2):
        fixed_coordinates = [i for i in range(7) if i not in omitted]
        for fixed_values in product(range(3), repeat=5):
            base_index = sum(
                value * powers[coordinate]
                for coordinate, value in zip(fixed_coordinates, fixed_values, strict=True)
            )
            row = 0
            for first, second in product(range(3), repeat=2):
                index = (
                    base_index
                    + first * powers[omitted[0]]
                    + second * powers[omitted[1]]
                )
                row ^= 1 << index
            while row:
                pivot = row.bit_length() - 1
                if pivot in pivots:
                    row ^= pivots[pivot]
                else:
                    pivots[pivot] = row
                    break
    return len(pivots)


def modular_rank(rows: list[list[int]], modulus: int = 101) -> int:
    matrix = [[entry % modulus for entry in row] for row in rows]
    rank = 0
    columns = len(matrix[0])
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, modulus)
        matrix[rank] = [(value * inverse) % modulus for value in matrix[rank]]
        for row in range(len(matrix)):
            if row != rank and matrix[row][column]:
                scale = matrix[row][column]
                matrix[row] = [
                    (left - scale * right) % modulus
                    for left, right in zip(matrix[row], matrix[rank], strict=True)
                ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def projection_rank() -> int:
    # Ternary one-coordinate basis: constant, p, q.  Under grouping
    # 0 | {1,2}, their images are (1,2), (1,-1), (0,0).  Under grouping
    # {0,1} | 2, they are (2,1), (0,0), (1,-1).
    rows: list[list[int]] = []
    for projection in range(2):
        constant = (1, 2) if projection == 0 else (2, 1)
        contrast = (1, -1)
        for missing in range(8):
            # missing=0,...,6 means support six; missing=7 means support seven.
            vector = []
            for mask in range(1 << 7):
                value = 1
                for coordinate in range(7):
                    bit = mask >> coordinate & 1
                    if missing < 7 and coordinate == missing:
                        value *= constant[bit]
                    else:
                        value *= contrast[bit]
                vector.append(value)
            rows.append(([0] * 128 + vector) if projection else (vector + [0] * 128))
    assert modular_rank(rows) == 16
    return 16


def symmetric_equations():
    index = {orbit: i for i, orbit in enumerate(ORBITS)}
    rows: list[list[Fraction]] = []
    right: list[Fraction] = []

    for first in range(6):
        for second in range(6 - first):
            composition = (first, second, 5 - first - second)
            row = [0] * 8
            for region in range(3):
                lifted = list(composition)
                lifted[region] += 2
                row[index[tuple(sorted(lifted, reverse=True))]] += 1
            for left, right_region in combinations(range(3), 2):
                lifted = list(composition)
                lifted[left] += 1
                lifted[right_region] += 1
                row[index[tuple(sorted(lifted, reverse=True))]] += 2
            rows.append(list(map(Fraction, row)))
            right.append(Fraction(prod_factorials(composition)))

    # Under S_3 symmetry these eight predecessor-set projections also imply
    # the eight successor-side projections.
    for size in range(8):
        row = [0] * 8
        for middle in range(8 - size):
            composition = (size, middle, 7 - size - middle)
            row[index[tuple(sorted(composition, reverse=True))]] += comb(7 - size, middle)
        rows.append(list(map(Fraction, row)))
        right.append(Fraction(BASE[size]))
    return rows, right


def prod_factorials(composition: tuple[int, int, int]) -> int:
    return factorial(composition[0]) * factorial(composition[1]) * factorial(composition[2])


def rref_affine(rows: list[list[Fraction]], right: list[Fraction]):
    matrix = [row + [value] for row, value in zip(rows, right, strict=True)]
    rank = 0
    pivots = []
    variables = len(rows[0])
    for column in range(variables):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for row in range(len(matrix)):
            if row != rank and matrix[row][column]:
                scale = matrix[row][column]
                matrix[row] = [
                    left - scale * right_entry
                    for left, right_entry in zip(matrix[row], matrix[rank], strict=True)
                ]
        pivots.append(column)
        rank += 1
    for row in matrix:
        if not any(row[:variables]):
            assert row[-1] == 0
    return matrix, pivots


def verify_symmetric_uniqueness():
    rows, right = symmetric_equations()
    matrix, pivots = rref_affine(rows, right)
    assert pivots == list(range(7))
    free = 7
    # Each pivot variable is constant minus its RREF coefficient times t,
    # where t=x_(3,2,2).
    family = []
    for row in matrix[:7]:
        family.append((row[-1], -row[free]))
    family.append((Fraction(0), Fraction(1)))
    expected = (
        (Fraction(70), Fraction(0)),
        (Fraction(10), Fraction(0)),
        (Fraction(5), Fraction(-5)),
        (Fraction(0), Fraction(5)),
        (Fraction(1), Fraction(3)),
        (Fraction(1), Fraction(-1)),
        (Fraction(1), Fraction(-3, 2)),
        (Fraction(0), Fraction(1)),
    )
    assert tuple(family) == expected

    solutions = []
    # Nonnegativity of x_(3,2,2)=t and x_(5,2,0)=5-5t gives 0<=t<=1.
    for t in range(2):
        values = [constant + coefficient * t for constant, coefficient in family]
        if all(value.denominator == 1 and value >= 0 for value in values):
            solutions.append(tuple(int(value) for value in values))
    assert solutions == [Q_VALUES]
    return len(pivots), family


def main() -> None:
    cells = 3**7
    marginal_checks = verify_all_marginals(q_value)
    boundary_checks = verify_boundary_projections(q_value)
    assert sum(q_value(word) for word in product(range(3), repeat=7)) == 2520

    asymmetric = load_asymmetric_profile()
    asymmetric_value = lambda word: composition_value(word, asymmetric)
    asymmetric_marginal_checks = verify_all_marginals(asymmetric_value)
    asymmetric_boundary_checks = verify_boundary_projections(asymmetric_value)
    assert sum(asymmetric_value(word) for word in product(range(3), repeat=7)) == 2520

    rank = gf2_marginal_rank()
    expected_rank = sum(comb(7, support) * 2**support for support in range(6))
    assert rank == expected_rank == 1611
    kernel_dimension = cells - rank
    assert kernel_dimension == 576
    visible_projection_rank = projection_rank()
    fixed_projection_dimension = kernel_dimension - visible_projection_rank
    assert fixed_projection_dimension == 560

    symmetric_rank, family = verify_symmetric_uniqueness()
    assert symmetric_rank == 7

    # If Q were assigned to all 72 ordered symbol pairs, composition (5,1,1)
    # would contribute zero at positions (5,7), although every one of the 5040
    # permutations contributes exactly one ordered pair there.
    all_q_count = 72 * (factorial(7) // (factorial(5) * factorial(1) * factorial(1))) * Q[(5, 1, 1)]
    assert all_q_count == 0

    # A globally composition-balanced bundle consists of 36 copies of Q and
    # six copies of every region relabelling of the asymmetric profile.
    region_permutations = tuple(permutations(range(3)))
    assert len(region_permutations) == 6
    orbit_marginal_checks = 0
    orbit_boundary_checks = 0
    for permutation in region_permutations:
        conjugate = {
            composition: asymmetric[
                tuple(composition[permutation[i]] for i in range(3))
            ]
            for composition in asymmetric
        }
        conjugate_value = lambda word, table=conjugate: composition_value(word, table)
        orbit_marginal_checks += verify_all_marginals(conjugate_value)
        orbit_boundary_checks += verify_boundary_projections(conjugate_value)
    for composition in asymmetric:
        orbit_sum = sum(
            asymmetric[tuple(composition[permutation[i]] for i in range(3))]
            for permutation in region_permutations
        )
        symmetric_value = Q[tuple(sorted(composition, reverse=True))]
        bundle_sum = 36 * symmetric_value + 6 * orbit_sum
        assert bundle_sum == prod_factorials(composition)

    print(f"ternary cells: {cells}")
    print(f"exact five-coordinate marginal checks: {marginal_checks}")
    print(f"uniform boundary projection checks: {boundary_checks}")
    print(f"asymmetric-profile marginal checks: {asymmetric_marginal_checks}")
    print(f"asymmetric-profile boundary checks: {asymmetric_boundary_checks}")
    print(f"six-orbit marginal checks: {orbit_marginal_checks}")
    print(f"six-orbit boundary checks: {orbit_boundary_checks}")
    print(f"marginal matrix rank: {rank}")
    print(f"homogeneous kernel dimension: {kernel_dimension}")
    print(f"two boundary projections expose: {visible_projection_rank}")
    print(f"fixed-boundary affine dimension: {fixed_projection_dimension}")
    print(f"S7xS3 orbit variables: {len(ORBITS)}")
    print(f"symmetric system rank: {symmetric_rank}")
    print("unique nonnegative integral symmetric solution:")
    for orbit, value in zip(ORBITS, Q_VALUES, strict=True):
        print(f"  {orbit[0]}{orbit[1]}{orbit[2]}: {value}")
    print(f"all-Q global count at composition 511: {all_q_count} (required 5040)")
    print("72-profile asymmetric composition bundle: OK")
    print("all exact checks: OK")


if __name__ == "__main__":
    main()
