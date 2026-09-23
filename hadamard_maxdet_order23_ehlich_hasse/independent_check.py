#!/usr/bin/env python3
"""Independent structural check of the Hasse calculations.

Unlike verify.py, this checker diagonalizes each block analytically and only
performs symmetric elimination on the small block-sum core.  It independently
generates partitions in ascending order and uses direct Bareiss determinants.
"""

from fractions import Fraction
from pathlib import Path
import importlib.util


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("primary_verifier", HERE / "verify.py")
assert SPEC and SPEC.loader
primary = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(primary)


def partitions_ascending(total: int, minimum: int = 1):
    if total == 0:
        yield ()
        return
    for first in range(minimum, total + 1):
        for tail in partitions_ascending(total - first, first):
            yield (first,) + tail


def small_ldlt(matrix: list[list[Fraction]]) -> list[Fraction]:
    a = [row[:] for row in matrix]
    result = []
    for k in range(len(a)):
        pivot = a[k][k]
        assert pivot > 0
        result.append(pivot)
        column = [a[i][k] for i in range(k + 1, len(a))]
        for ii, i in enumerate(range(k + 1, len(a))):
            for jj, j in enumerate(range(k + 1, len(a))):
                a[i][j] -= column[ii] * column[jj] / pivot
    return result


def analytic_diagonal(partition: tuple[int, ...]) -> list[Fraction]:
    """Diagonalize internal zero-sum directions, then the block-sum core."""
    a = 20
    diagonal = []
    for size in partition:
        # With y_i = average(x_1,...,x_i)-x_{i+1}, sum x_j^2 has
        # coefficients i/(i+1), and the block sum z has coefficient 1/size.
        diagonal.extend(Fraction(a * i, i + 1) for i in range(1, size))
    core = []
    for i, size_i in enumerate(partition):
        row = []
        for j, _size_j in enumerate(partition):
            row.append(Fraction(a, size_i) + 3 if i == j else Fraction(-1))
        core.append(row)
    diagonal.extend(small_ldlt(core))
    assert len(diagonal) == 23
    return diagonal


def main() -> None:
    parts = list(partitions_ascending(23))
    assert len(parts) == 1255
    candidates = []
    for ascending in parts:
        partition = tuple(reversed(ascending))
        matrix = primary.ehlich_matrix(partition)
        determinant = primary.bareiss_determinant(matrix)
        if determinant < primary.RECORD**2:
            continue
        root = primary.isqrt(determinant)
        if root * root == determinant:
            candidates.append((partition, root, matrix))
    candidates.sort(reverse=True)
    assert len(candidates) == 16

    survivors = []
    for partition, root, matrix in candidates:
        diagonal = analytic_diagonal(partition)
        product = Fraction(1)
        for value in diagonal:
            product *= value
        # Congruence changes a determinant by det(T)^2.  Confirm the expected
        # determinant square class rather than equality in these coordinates.
        ratio = product / (root * root)
        assert primary.isqrt(ratio.numerator) ** 2 == ratio.numerator
        assert primary.isqrt(ratio.denominator) ** 2 == ratio.denominator
        bad = [
            p
            for p in primary.relevant_primes(diagonal)
            if primary.hasse_invariant(diagonal, p) < 0
        ]
        full_bad = primary.bad_primes(matrix)
        assert bad == full_bad
        if not bad:
            survivors.append(list(partition))
        print(f"{partition}: {bad or 'SURVIVES'}")

    expected = primary.json.loads((HERE / "certificate.json").read_text())
    assert survivors == expected["rational_survivors"]
    print("independent analytic diagonalization agrees on all 16 candidates")


if __name__ == "__main__":
    main()
