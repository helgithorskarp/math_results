#!/usr/bin/env python3
"""Verify exact block-sum moment obstructions for all 16 square candidates.

The only dependencies are Python's standard library.  All quadratic tests and
moment calculations use integers or fractions.Fraction.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from itertools import product
from pathlib import Path


HERE = Path(__file__).resolve().parent
N = 23


def inverse_condition(
    partition: tuple[int, ...], block_sums: tuple[int, ...], order: int
) -> Fraction:
    """Return the denominator-cleared diagonal condition from X^T G^-1 X."""
    diagonal_base = order - 3
    denominators = [diagonal_base + 4 * size for size in partition]
    schur = 1 - sum(
        Fraction(size, denominator)
        for size, denominator in zip(partition, denominators)
    )
    weighted_sum = sum(
        Fraction(value, denominator)
        for value, denominator in zip(block_sums, denominators)
    )
    return sum(
        Fraction(4 * value * value, denominator)
        for value, denominator in zip(block_sums, denominators)
    ) - diagonal_base * weighted_sum * weighted_sum / schur


def admissible_types(
    partition: tuple[int, ...], order: int = N
) -> list[tuple[int, ...]]:
    """Enumerate every normalized column block-sum type allowed by G^{-1}."""
    assert sum(partition) == order
    candidates = product(*(range(-size, size + 1, 2) for size in partition))
    return [
        values
        for values in candidates
        if sum(values) % 4 == 3
        and inverse_condition(partition, values, order) == 3
    ]


def moment_matrix(
    partition: tuple[int, ...], order: int = N
) -> list[list[int]]:
    """Return P G P^T, where P sums coordinates in each Ehlich block."""
    diagonal_base = order - 3
    return [
        [
            size_i * (diagonal_base + 4 * size_i) * (i == j)
            - size_i * size_j
            for j, size_j in enumerate(partition)
        ]
        for i, size_i in enumerate(partition)
    ]


def type_hash(types: list[tuple[int, ...]]) -> str:
    encoded = "".join(",".join(map(str, values)) + "\n" for values in types)
    return hashlib.sha256(encoded.encode("ascii")).hexdigest()


def polynomial(values: tuple[int, ...], certificate: dict) -> int:
    answer = int(certificate["constant"])
    for term in certificate["terms"]:
        i, j = term["pair"]
        answer += int(term["coefficient"]) * values[i] * values[j]
    return answer


def target_value(partition: tuple[int, ...], certificate: dict) -> int:
    moments = moment_matrix(partition)
    answer = N * int(certificate["constant"])
    for term in certificate["terms"]:
        i, j = term["pair"]
        answer += int(term["coefficient"]) * moments[i][j]
    return answer


def self_test_known_order7_decomposition() -> None:
    """Positive control from a Sylvester Hadamard matrix of order eight."""
    hadamard = [[1]]
    while len(hadamard) < 8:
        hadamard = (
            [row + row for row in hadamard]
            + [row + [-value for value in row] for row in hadamard]
        )
    design = [row[1:] for row in hadamard[1:]]
    gram = [
        [sum(left * right for left, right in zip(row_i, row_j)) for row_j in design]
        for row_i in design
    ]
    assert gram == [[7 if i == j else -1 for j in range(7)] for i in range(7)]

    columns = []
    for j in range(7):
        column = [design[i][j] for i in range(7)]
        if sum(column) % 4 != 3:
            column = [-value for value in column]
        values = tuple(column)  # seven row blocks of size one
        assert inverse_condition((1,) * 7, values, 7) == 3
        columns.append(values)
    observed = [
        [sum(column[i] * column[j] for column in columns) for j in range(7)]
        for i in range(7)
    ]
    assert observed == moment_matrix((1,) * 7, 7)


def main() -> None:
    self_test_known_order7_decomposition()
    data = json.loads((HERE / "moment_certificate.json").read_text())
    hasse_data = json.loads((HERE / "certificate.json").read_text())
    expected_partitions = [
        tuple(item["partition"]) for item in hasse_data["square_candidates"]
    ]
    assert data["order"] == N
    assert len(data["cases"]) == len(expected_partitions) == 16
    assert [tuple(case["partition"]) for case in data["cases"]] == expected_partitions

    for case in data["cases"]:
        partition = tuple(case["partition"])
        assert sum(partition) == N
        certificate = case["certificate"]
        types = admissible_types(partition)
        assert len(types) == case["admissible_type_count"]
        assert type_hash(types) == case["admissible_types_sha256"]
        if not types:
            assert certificate is None
            print(f"{partition}: no admissible normalized column type")
            continue

        assert certificate is not None
        terms = certificate["terms"]
        assert len({tuple(term["pair"]) for term in terms}) == len(terms)
        assert all(
            0 <= term["pair"][0] <= term["pair"][1] < len(partition)
            for term in terms
        )
        values = [polynomial(item, certificate) for item in types]
        target = target_value(partition, certificate)

        assert min(values) == certificate["minimum_on_types"] >= 0
        assert max(values) == certificate["maximum_on_types"]
        assert target == certificate["target_moment_value"] < 0

        print(
            f"{partition}: {len(types)} types, "
            f"certificate range [{min(values)}, {max(values)}], target {target}"
        )

    print("all 16 block-sum moment obstructions verified")


if __name__ == "__main__":
    main()
