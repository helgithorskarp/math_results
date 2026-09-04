#!/usr/bin/env python3
"""Independent exact checks for rectangular Grassmannian identity inflation.

This checker deliberately does not import the reviewed implementation.  It
evaluates the relevant Schur specialization by a Jacobi--Trudi determinant
and the boxed-plane-partition number by the hyperfactorial formula.
"""

from __future__ import annotations

import functools
import hashlib
import itertools
import math
import sys


def rectangular_permutation(a: int, b: int, c: int) -> tuple[int, ...]:
    """Return w(a,b,c) in one-based one-line notation."""
    assert a >= 1 and b >= 1 and c >= 0
    return tuple(
        list(range(1, c + 1))
        + list(range(c + b + 1, c + b + a + 1))
        + list(range(c + 1, c + b + 1))
    )


def tensor_identity(w: tuple[int, ...], k: int) -> tuple[int, ...]:
    """Inflate each permutation-matrix 1-entry by a k by k identity."""
    assert k >= 1
    return tuple(k * (value - 1) + residue for value in w for residue in range(1, k + 1))


def descents(w: tuple[int, ...]) -> tuple[int, ...]:
    """Return descent positions in one-based notation."""
    return tuple(i + 1 for i in range(len(w) - 1) if w[i] > w[i + 1])


def grassmannian_shape(w: tuple[int, ...]) -> tuple[int, ...]:
    """Recover the partition of a permutation having exactly one descent."""
    ds = descents(w)
    assert len(ds) == 1
    d = ds[0]
    parts = tuple(w[position - 1] - position for position in range(d, 0, -1))
    assert all(parts[i] >= parts[i + 1] for i in range(len(parts) - 1))
    return tuple(part for part in parts if part)


def bareiss_determinant(matrix: list[list[int]]) -> int:
    """Fraction-free exact determinant."""
    n = len(matrix)
    if n == 0:
        return 1
    assert all(len(row) == n for row in matrix)
    work = [row[:] for row in matrix]
    previous_pivot = 1
    sign = 1
    for column in range(n - 1):
        if work[column][column] == 0:
            pivot_row = next(row for row in range(column + 1, n) if work[row][column])
            work[column], work[pivot_row] = work[pivot_row], work[column]
            sign = -sign
        pivot = work[column][column]
        for row in range(column + 1, n):
            for j in range(column + 1, n):
                numerator = work[row][j] * pivot - work[row][column] * work[column][j]
                assert numerator % previous_pivot == 0
                work[row][j] = numerator // previous_pivot
            work[row][column] = 0
        previous_pivot = pivot
    return sign * work[-1][-1]


def complete_specialization(degree: int, variables: int) -> int:
    """h_degree(1^variables), with h_negative=0."""
    if degree < 0:
        return 0
    if degree == 0:
        return 1
    return math.comb(variables + degree - 1, degree)


def schur_rectangle_jacobi_trudi(a: int, b: int, variables: int) -> int:
    """Evaluate s_(b^a)(1^variables) by Jacobi--Trudi."""
    matrix = [
        [complete_specialization(b - row + column, variables) for column in range(a)]
        for row in range(a)
    ]
    return bareiss_determinant(matrix)


def schur_partition_jacobi_trudi(partition: tuple[int, ...]) -> int:
    """Evaluate s_partition(1^d), padding is explicit in len(partition)=d."""
    d = len(partition)
    assert d >= 1
    assert all(partition[i] >= partition[i + 1] for i in range(d - 1))
    assert partition[-1] >= 0
    matrix = [
        [complete_specialization(partition[row] - row + column, d) for column in range(d)]
        for row in range(d)
    ]
    return bareiss_determinant(matrix)


@functools.cache
def hyperfactorial(n: int) -> int:
    """H(n)=product_(0<=j<n) j!."""
    assert n >= 0
    return math.prod(math.factorial(j) for j in range(n))


def boxed_plane_partitions(a: int, b: int, c: int) -> int:
    """MacMahon's value in its symmetric hyperfactorial form."""
    numerator = hyperfactorial(a) * hyperfactorial(b) * hyperfactorial(c)
    numerator *= hyperfactorial(a + b + c)
    denominator = hyperfactorial(a + b) * hyperfactorial(a + c) * hyperfactorial(b + c)
    quotient, remainder = divmod(numerator, denominator)
    assert remainder == 0
    return quotient


def weyl_dimension(partition: tuple[int, ...]) -> int:
    """Evaluate s_partition(1^d) using the GL_d Weyl dimension product."""
    d = len(partition)
    assert d >= 1
    assert all(partition[i] >= partition[i + 1] for i in range(d - 1))
    assert partition[-1] >= 0
    numerator = 1
    denominator = 1
    for i in range(d):
        for j in range(i + 1, d):
            numerator *= partition[i] - partition[j] + j - i
            denominator *= j - i
    quotient, remainder = divmod(numerator, denominator)
    assert remainder == 0
    return quotient


def inflate_partition(partition: tuple[int, ...], k: int) -> tuple[int, ...]:
    """Shape induced by identity-block inflation of a Grassmannian permutation."""
    assert k >= 1
    return tuple(k * part for part in partition for _ in range(k))


def reflect(cell: tuple[int, int], k: int) -> tuple[int, int]:
    alpha, beta = cell
    return k + 1 - alpha, k + 1 - beta


def verify_reflected_factor_identity(q: int, c: int, k: int) -> None:
    """Check every orbit and the exact cross-multiplied surplus identity."""
    assert q >= 0 and c >= 0 and k >= 1
    visited: set[tuple[int, int]] = set()
    for alpha in range(1, k + 1):
        for beta in range(1, k + 1):
            cell = (alpha, beta)
            if cell in visited:
                continue
            mate = reflect(cell, k)
            assert reflect(mate, k) == cell
            visited.add(cell)
            visited.add(mate)
            t = alpha + beta - 1
            reflected_t = mate[0] + mate[1] - 1
            assert reflected_t == 2 * k - t

            a_value = k * (c + q + 1)
            b_value = k * (q + 1)
            x = t - k
            assert b_value * b_value - x * x > 0
            assert a_value * a_value - x * x > 0

            if t == k:
                # Every central-antidiagonal factor equals R, even when the
                # geometric reflection swaps two different subcells.
                assert (k * (c + q) + t) * (q + 1) == (c + q + 1) * (k * q + t)
            else:
                excess = b_value * b_value * (a_value * a_value - x * x)
                excess -= a_value * a_value * (b_value * b_value - x * x)
                assert excess == x * x * (a_value * a_value - b_value * b_value)
                assert excess >= 0
                assert (excess > 0) == (c > 0)
    assert len(visited) == k * k


def verify_weyl_factor_block(partition: tuple[int, ...], i: int, j: int, k: int) -> None:
    """Audit the residue-pair proof for one original Weyl factor."""
    assert 0 <= i < j < len(partition) and k >= 1
    difference = partition[i] - partition[j]
    assert difference >= 0
    a_value = k * (difference + j - i)
    b_value = k * (j - i)
    for r in range(1, k + 1):
        for s in range(1, k + 1):
            x = s - r
            assert a_value + x > 0 and a_value - x > 0
            assert b_value + x > 0 and b_value - x > 0
            excess = b_value * b_value * (a_value * a_value - x * x)
            excess -= a_value * a_value * (b_value * b_value - x * x)
            assert excess == x * x * (a_value * a_value - b_value * b_value)
            assert excess >= 0
            assert (excess > 0) == (difference > 0 and x != 0)


def main() -> None:
    digest = hashlib.sha256()

    permutation_cases = 0
    for a in range(1, 6):
        for b in range(1, 6):
            for c in range(5):
                w = rectangular_permutation(a, b, c)
                assert descents(w) == (a + c,)
                assert grassmannian_shape(w) == (b,) * a
                for k in range(1, 6):
                    assert tensor_identity(w, k) == rectangular_permutation(k * a, k * b, k * c)
                    permutation_cases += 1

    schur_cases = 0
    for a in range(1, 8):
        for b in range(1, 8):
            for c in range(7):
                schur = schur_rectangle_jacobi_trudi(a, b, a + c)
                plane_partitions = boxed_plane_partitions(a, b, c)
                assert schur == plane_partitions
                schur_cases += 1

    inequality_cases = 0
    for a in range(1, 7):
        for b in range(1, 7):
            for c in range(6):
                base = boxed_plane_partitions(a, b, c)
                for k in range(1, 6):
                    inflated = boxed_plane_partitions(k * a, k * b, k * c)
                    bound = base ** (k * k)
                    assert inflated >= bound
                    assert (inflated == bound) == (c == 0 or k == 1)
                    digest.update(f"{a},{b},{c},{k}:{base},{inflated},{bound}\n".encode())
                    inequality_cases += 1

    block_cases = 0
    for q in range(13):
        for c in range(8):
            for k in range(1, 9):
                verify_reflected_factor_identity(q, c, k)
                block_cases += 1

    # The same factor pairing proves the stronger result for every
    # Grassmannian shape, not just a rectangle followed by zero parts.
    grassmannian_cases = 0
    for d in range(1, 7):
        for ascending in itertools.combinations_with_replacement(range(6), d):
            partition = tuple(reversed(ascending))
            base = weyl_dimension(partition)
            assert schur_partition_jacobi_trudi(partition) == base
            for k in range(1, 6):
                inflated_partition = inflate_partition(partition, k)
                inflated = weyl_dimension(inflated_partition)
                bound = base ** (k * k)
                assert inflated >= bound
                assert (inflated == bound) == (k == 1 or len(set(partition)) == 1)
                for i in range(d):
                    for j in range(i + 1, d):
                        verify_weyl_factor_block(partition, i, j, k)
                digest.update(f"G{partition},{k}:{base},{inflated},{bound}\n".encode())
                grassmannian_cases += 1

    assert boxed_plane_partitions(2, 2, 2) == 20
    assert boxed_plane_partitions(4, 4, 4) == 232848
    print(
        "PASS "
        f"permutation_cases={permutation_cases} "
        f"schur_cases={schur_cases} "
        f"inequality_cases={inequality_cases} "
        f"block_cases={block_cases} "
        f"grassmannian_cases={grassmannian_cases} "
        f"digest={digest.hexdigest()} "
        f"python={sys.version.split()[0]}"
    )
    print("representative PP(2,2,2)=20 PP(4,4,4)=232848 bound=160000")


if __name__ == "__main__":
    main()
