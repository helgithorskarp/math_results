#!/usr/bin/env python3
"""Exact verifier for order-23 Ehlich-block Hasse obstructions.

Only the Python standard library is used.  Every matrix operation and local
symbol computation is exact (integers or fractions.Fraction).
"""

from __future__ import annotations

import json
from fractions import Fraction
from math import isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
N = 23
RECORD = (2**22) * 3 * (5**6) * 67 * 211


def partitions_desc(total: int, cap: int | None = None):
    """Yield integer partitions as nonincreasing tuples."""
    if total == 0:
        yield ()
        return
    if cap is None or cap > total:
        cap = total
    for first in range(cap, 0, -1):
        for tail in partitions_desc(total - first, first):
            yield (first,) + tail


def ehlich_matrix(partition: tuple[int, ...]) -> list[list[int]]:
    """Return 20 I - J + 4 direct_sum(J_r), for sum(partition)=23."""
    assert sum(partition) == N
    labels = []
    for block, size in enumerate(partition):
        labels.extend([block] * size)
    return [
        [
            20 * (i == j) - 1 + 4 * (labels[i] == labels[j])
            for j in range(N)
        ]
        for i in range(N)
    ]


def ehlich_determinant(partition: tuple[int, ...]) -> int:
    """Evaluate Ehlich's determinant formula exactly."""
    product = 20 ** (N - len(partition))
    correction = Fraction(1)
    for size in partition:
        factor = 20 + 4 * size
        product *= factor
        correction -= Fraction(size, factor)
    value = product * correction
    assert value.denominator == 1
    return value.numerator


def bareiss_determinant(matrix: list[list[int]]) -> int:
    """Fraction-free determinant, with row swaps if required."""
    a = [row[:] for row in matrix]
    n = len(a)
    if n == 0:
        return 1
    previous = 1
    sign = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            pivot_row = next((i for i in range(k + 1, n) if a[i][k]), None)
            if pivot_row is None:
                return 0
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                assert numerator % previous == 0
                a[i][j] = numerator // previous
        previous = pivot
        for i in range(k + 1, n):
            a[i][k] = 0
    return sign * a[-1][-1]


def ldlt_diagonal(matrix: list[list[int]]) -> list[Fraction]:
    """Diagonal form obtained by exact symmetric Gaussian elimination."""
    a = [[Fraction(x) for x in row] for row in matrix]
    diagonal = []
    for k in range(len(a)):
        pivot = a[k][k]
        assert pivot > 0  # all matrices considered here are positive definite
        diagonal.append(pivot)
        for i in range(k + 1, len(a)):
            for j in range(i, len(a)):
                a[j][i] -= a[i][k] * a[j][k] / pivot
                a[i][j] = a[j][i]
    return diagonal


def valuation(number: int, prime: int) -> tuple[int, int]:
    """Return (v_p(number), p-free part), allowing a negative number."""
    assert number
    exponent = 0
    while number % prime == 0:
        number //= prime
        exponent += 1
    return exponent, number


def local_data(value: Fraction, prime: int, modulus: int) -> tuple[int, int]:
    """Return valuation and unit residue of a nonzero rational number."""
    en, numerator = valuation(value.numerator, prime)
    ed, denominator = valuation(value.denominator, prime)
    unit = (numerator % modulus) * pow(denominator % modulus, -1, modulus)
    return en - ed, unit % modulus


def legendre(unit: int, prime: int) -> int:
    residue = pow(unit % prime, (prime - 1) // 2, prime)
    assert residue in (1, prime - 1)
    return 1 if residue == 1 else -1


def hilbert_symbol(a: Fraction, b: Fraction, prime: int) -> int:
    """The rational Hilbert symbol (a,b)_p for a finite prime p."""
    assert a and b
    if prime == 2:
        alpha, u = local_data(a, 2, 8)
        beta, v = local_data(b, 2, 8)
        exponent = (
            ((u - 1) // 2) * ((v - 1) // 2)
            + alpha * ((v * v - 1) // 8)
            + beta * ((u * u - 1) // 8)
        )
        return -1 if exponent % 2 else 1
    alpha, u = local_data(a, prime, prime)
    beta, v = local_data(b, prime, prime)
    answer = -1 if (alpha * beta * ((prime - 1) // 2)) % 2 else 1
    if beta % 2:
        answer *= legendre(u, prime)
    if alpha % 2:
        answer *= legendre(v, prime)
    return answer


def factor_primes(number: int) -> set[int]:
    number = abs(number)
    factors = set()
    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            factors.add(divisor)
            while number % divisor == 0:
                number //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if number > 1:
        factors.add(number)
    return factors


def relevant_primes(diagonal: list[Fraction]) -> list[int]:
    primes = {2}
    for value in diagonal:
        primes |= factor_primes(value.numerator)
        primes |= factor_primes(value.denominator)
    return sorted(primes)


def hasse_invariant(diagonal: list[Fraction], prime: int) -> int:
    answer = 1
    for i, left in enumerate(diagonal):
        for right in diagonal[i + 1 :]:
            answer *= hilbert_symbol(left, right, prime)
    return answer


def self_test_hilbert_symbols() -> None:
    """Check symmetry, square invariance, and Hilbert reciprocity."""
    pairs = [
        (Fraction(-1), Fraction(-1)),
        (Fraction(-3), Fraction(5)),
        (Fraction(6), Fraction(10)),
        (Fraction(3, 5), Fraction(-14, 9)),
        (Fraction(-35, 8), Fraction(-22, 27)),
    ]
    square = Fraction(25, 9)
    for left, right in pairs:
        primes = sorted(
            {2}
            | factor_primes(left.numerator * left.denominator)
            | factor_primes(right.numerator * right.denominator)
            | factor_primes(square.numerator * square.denominator)
        )
        finite_product = 1
        for prime in primes:
            symbol = hilbert_symbol(left, right, prime)
            assert symbol == hilbert_symbol(right, left, prime)
            assert symbol == hilbert_symbol(left * square, right, prime)
            finite_product *= symbol
        real_symbol = -1 if left < 0 and right < 0 else 1
        assert finite_product * real_symbol == 1


def bad_primes(matrix: list[list[int]]) -> list[int]:
    diagonal = ldlt_diagonal(matrix)
    bad = [p for p in relevant_primes(diagonal) if hasse_invariant(diagonal, p) < 0]
    # Hilbert reciprocity: positive definiteness gives c_infinity=+1, so the
    # number of finite bad places must be even.
    assert len(bad) % 2 == 0
    return bad


def read_sign_matrix(path: Path) -> list[list[int]]:
    rows = [line.strip() for line in path.read_text().splitlines() if line.strip()]
    assert len(rows) == N and all(len(row) == N for row in rows)
    assert all(set(row) <= {"+", "-"} for row in rows)
    return [[1 if symbol == "+" else -1 for symbol in row] for row in rows]


def gram(matrix: list[list[int]]) -> list[list[int]]:
    return [
        [sum(left * right for left, right in zip(matrix[i], matrix[j])) for j in range(N)]
        for i in range(N)
    ]


def enumerate_candidates():
    partitions = list(partitions_desc(N))
    assert len(partitions) == 1255
    above = []
    square = []
    for partition in partitions:
        determinant = ehlich_determinant(partition)
        if determinant >= RECORD * RECORD:
            above.append(partition)
            root = isqrt(determinant)
            if root * root == determinant:
                square.append((partition, root))
    return partitions, above, square


def main() -> None:
    self_test_hilbert_symbols()
    certificate = json.loads((HERE / "certificate.json").read_text())
    record_matrix = read_sign_matrix(HERE / "record23.txt")
    record_det = abs(bareiss_determinant(record_matrix))
    assert record_det == RECORD == int(certificate["record_determinant"])

    record_gram = gram(record_matrix)
    assert bareiss_determinant(record_gram) == RECORD * RECORD
    assert {record_gram[i][j] for i in range(N) for j in range(i)} == {-1, 3}
    # Positive controls: an actual rational Gram factor must have no bad place.
    assert bad_primes(record_gram) == []
    known15 = (4, 4, 4, 3)
    labels15 = [block for block, size in enumerate(known15) for _ in range(size)]
    gram15 = [
        [
            12 * (i == j) - 1 + 4 * (labels15[i] == labels15[j])
            for j in range(15)
        ]
        for i in range(15)
    ]
    assert bad_primes(gram15) == []  # known decomposable order-15 optimum

    partitions, above, candidates = enumerate_candidates()
    assert len(above) == int(certificate["partitions_at_or_above_record"])
    assert len(candidates) == len(certificate["square_candidates"]) == 16

    actual = []
    for partition, root in candidates:
        matrix = ehlich_matrix(partition)
        assert bareiss_determinant(matrix) == root * root
        bad = bad_primes(matrix)
        actual.append(
            {
                "partition": list(partition),
                "sqrt_determinant": str(root),
                "normalized_sqrt": str(root // 2**22),
                "bad_primes": bad,
                "rationally_obstructed": bool(bad),
            }
        )

    assert actual == certificate["square_candidates"]
    assert sum(item["rationally_obstructed"] for item in actual) == 11
    survivors = [item["partition"] for item in actual if not item["bad_primes"]]
    assert survivors == certificate["rational_survivors"]

    print(f"record determinant: {RECORD}")
    print(f"integer partitions of 23: {len(partitions)}")
    print(f"Ehlich partitions at/above record: {len(above)}")
    print(f"perfect-square candidates: {len(candidates)}")
    print("Hasse-obstructed candidates: 11")
    print("rational survivors: 5")
    for item in actual:
        tag = "SURVIVES" if not item["bad_primes"] else f"blocked at p={item['bad_primes']}"
        print(f"{tuple(item['partition'])}: {tag}")
    print("certificate verified")


if __name__ == "__main__":
    main()
