#!/usr/bin/env python3
"""Reviewer-owned exact check of the order-23 Ehlich moment obstruction.

This program imports no target code.  It enumerates integer partitions by a
dynamic set construction, evaluates determinants through the induced operator
on block-constant vectors, and derives the column quadratic form by inverting
each full Gram matrix over ``fractions.Fraction``.  The published separating
polynomials are then checked against those independently derived type sets and
against block moments summed directly from the Gram matrices.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from math import isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "hadamard_maxdet_order23_ehlich_hasse"
ORDER = 23
RECORD = (2**22) * 3 * (5**6) * 67 * 211


class CheckError(RuntimeError):
    """Raised for a failed mathematical or input check."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def partitions_by_dynamic_sets(total: int) -> list[tuple[int, ...]]:
    """Generate partitions without the target's recursive capped generator."""
    layers: list[set[tuple[int, ...]]] = [set() for _ in range(total + 1)]
    layers[0].add(())
    for subtotal in range(1, total + 1):
        for new_part in range(1, subtotal + 1):
            for previous in layers[subtotal - new_part]:
                layers[subtotal].add(
                    tuple(sorted(previous + (new_part,), reverse=True))
                )
    return sorted(layers[total], reverse=True)


def bareiss(matrix: list[list[int]]) -> int:
    """Exact determinant of an integer matrix by fraction-free elimination."""
    n = len(matrix)
    require(all(len(row) == n for row in matrix), "determinant matrix not square")
    if n == 0:
        return 1
    work = [row[:] for row in matrix]
    divisor = 1
    sign = 1
    for column in range(n - 1):
        pivot_row = next(
            (row for row in range(column, n) if work[row][column] != 0), None
        )
        require(pivot_row is not None, "unexpected singular determinant matrix")
        if pivot_row != column:
            work[column], work[pivot_row] = work[pivot_row], work[column]
            sign = -sign
        pivot = work[column][column]
        for row in range(column + 1, n):
            for other in range(column + 1, n):
                numerator = (
                    work[row][other] * pivot
                    - work[row][column] * work[column][other]
                )
                require(
                    numerator % divisor == 0,
                    "Bareiss division was not exact",
                )
                work[row][other] = numerator // divisor
            work[row][column] = 0
        divisor = pivot
    return sign * work[-1][-1]


def block_operator(partition: tuple[int, ...], order: int) -> list[list[int]]:
    """Operator induced by G on vectors constant on every block."""
    base = order - 3
    return [
        [
            (base + 4 * left) * (i == j) - right
            for j, right in enumerate(partition)
        ]
        for i, left in enumerate(partition)
    ]


def ehlich_determinant(partition: tuple[int, ...], order: int) -> int:
    """Use the zero-sum/block-constant invariant-space decomposition."""
    require(sum(partition) == order, "partition has wrong total")
    return (order - 3) ** (order - len(partition)) * bareiss(
        block_operator(partition, order)
    )


def block_indices(partition: tuple[int, ...]) -> list[list[int]]:
    result = []
    offset = 0
    for size in partition:
        result.append(list(range(offset, offset + size)))
        offset += size
    return result


def gram_matrix(partition: tuple[int, ...], order: int) -> list[list[int]]:
    require(sum(partition) == order, "partition has wrong total")
    labels = [block for block, size in enumerate(partition) for _ in range(size)]
    base = order - 3
    return [
        [base * (i == j) + 4 * (labels[i] == labels[j]) - 1 for j in range(order)]
        for i in range(order)
    ]


def inverse(matrix: list[list[int]]) -> list[list[Fraction]]:
    """Exact Gauss--Jordan inversion, with no imported linear algebra."""
    n = len(matrix)
    require(all(len(row) == n for row in matrix), "inverse matrix not square")
    work = [
        [Fraction(value) for value in row]
        + [Fraction(i == j) for j in range(n)]
        for i, row in enumerate(matrix)
    ]
    for column in range(n):
        pivot_row = next(
            (row for row in range(column, n) if work[row][column] != 0), None
        )
        require(pivot_row is not None, "Gram matrix is singular")
        if pivot_row != column:
            work[column], work[pivot_row] = work[pivot_row], work[column]
        pivot = work[column][column]
        work[column] = [value / pivot for value in work[column]]
        for row in range(n):
            if row == column:
                continue
            multiplier = work[row][column]
            if multiplier:
                work[row] = [
                    left - multiplier * right
                    for left, right in zip(work[row], work[column])
                ]
    result = [row[n:] for row in work]
    for i in range(n):
        for j in range(n):
            product = sum(
                Fraction(matrix[i][k]) * result[k][j] for k in range(n)
            )
            require(product == (i == j), "exact inverse multiplication failed")
    return result


def inverse_block_form(
    partition: tuple[int, ...], matrix_inverse: list[list[Fraction]]
) -> tuple[Fraction, list[Fraction], list[list[Fraction]]]:
    """Derive v^T G^-1 v from the directly computed inverse.

    The return values satisfy

        v^T G^-1 v = constant + sum_i square[i] u_i^2
                      + 2 sum_{i<j} cross[i][j] u_i u_j,

    where u_i is the sign sum on block i.
    """
    blocks = block_indices(partition)
    constant = Fraction(0)
    square: list[Fraction] = []
    cross = [
        [Fraction(0) for _ in partition]
        for _ in partition
    ]
    for block in blocks:
        diagonal = matrix_inverse[block[0]][block[0]]
        require(
            all(matrix_inverse[i][i] == diagonal for i in block),
            "inverse diagonal is not block-constant",
        )
        if len(block) == 1:
            off_diagonal = Fraction(0)
        else:
            off_diagonal = matrix_inverse[block[0]][block[1]]
            require(
                all(
                    matrix_inverse[i][j] == off_diagonal
                    for i in block
                    for j in block
                    if i != j
                ),
                "inverse within-block entries are not constant",
            )
        constant += len(block) * (diagonal - off_diagonal)
        square.append(off_diagonal)
    for i, left in enumerate(blocks):
        for j in range(i + 1, len(blocks)):
            right = blocks[j]
            value = matrix_inverse[left[0]][right[0]]
            require(
                all(matrix_inverse[a][b] == value for a in left for b in right),
                "inverse cross-block entries are not constant",
            )
            cross[i][j] = value
    return constant, square, cross


def quadratic_value(
    values: tuple[int, ...],
    form: tuple[Fraction, list[Fraction], list[list[Fraction]]],
) -> Fraction:
    constant, square, cross = form
    answer = constant + sum(c * value * value for c, value in zip(square, values))
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            answer += 2 * cross[i][j] * values[i] * values[j]
    return answer


def cartesian_block_sums(partition: tuple[int, ...]) -> list[tuple[int, ...]]:
    values: list[tuple[int, ...]] = [()]
    for size in partition:
        values = [
            prefix + (entry,)
            for prefix in values
            for entry in range(-size, size + 1, 2)
        ]
    return values


def admissible_types(
    partition: tuple[int, ...], order: int
) -> tuple[list[tuple[int, ...]], list[list[int]]]:
    matrix = gram_matrix(partition, order)
    form = inverse_block_form(partition, inverse(matrix))
    types = [
        values
        for values in cartesian_block_sums(partition)
        if sum(values) % 4 == 3 and quadratic_value(values, form) == 1
    ]
    return types, matrix


def types_hash(types: list[tuple[int, ...]]) -> str:
    encoded = "".join(",".join(map(str, values)) + "\n" for values in types)
    return hashlib.sha256(encoded.encode("ascii")).hexdigest()


def direct_block_moments(
    partition: tuple[int, ...], matrix: list[list[int]]
) -> list[list[int]]:
    blocks = block_indices(partition)
    return [
        [sum(matrix[a][b] for a in left for b in right) for right in blocks]
        for left in blocks
    ]


def polynomial(values: tuple[int, ...], certificate: dict) -> int:
    answer = int(certificate["constant"])
    for term in certificate["terms"]:
        i, j = map(int, term["pair"])
        answer += int(term["coefficient"]) * values[i] * values[j]
    return answer


def check_obstruction(
    partition: tuple[int, ...],
    types: list[tuple[int, ...]],
    matrix: list[list[int]],
    case: dict,
) -> tuple[int, int, int]:
    certificate = case["certificate"]
    require(certificate is not None, "nonempty type set lacks a certificate")
    terms = certificate["terms"]
    pairs = [tuple(map(int, term["pair"])) for term in terms]
    require(len(pairs) == len(set(pairs)), "duplicate polynomial term")
    require(
        all(0 <= i <= j < len(partition) for i, j in pairs),
        "polynomial index outside partition",
    )
    values = [polynomial(item, certificate) for item in types]
    minimum = min(values)
    maximum = max(values)
    moments = direct_block_moments(partition, matrix)
    target = ORDER * int(certificate["constant"])
    for term in terms:
        i, j = map(int, term["pair"])
        target += int(term["coefficient"]) * moments[i][j]
    require(minimum >= 0, "certificate is negative on an admissible type")
    require(target < 0, "certificate aggregate is not contradictory")
    require(minimum == int(certificate["minimum_on_types"]), "minimum mismatch")
    require(maximum == int(certificate["maximum_on_types"]), "maximum mismatch")
    require(target == int(certificate["target_moment_value"]), "target mismatch")
    return minimum, maximum, target


def parse_sign_matrix(text: str, order: int) -> list[list[int]]:
    rows = [line.strip() for line in text.splitlines() if line.strip()]
    require(len(rows) == order, "sign matrix has wrong row count")
    require(all(len(row) == order for row in rows), "sign matrix has wrong width")
    require(all(set(row) <= {"+", "-"} for row in rows), "invalid sign symbol")
    return [[1 if symbol == "+" else -1 for symbol in row] for row in rows]


def positive_order7_control() -> dict:
    hadamard = [[1]]
    while len(hadamard) < 8:
        hadamard = [row + row for row in hadamard] + [
            row + [-value for value in row] for row in hadamard
        ]
    design = [row[1:] for row in hadamard[1:]]
    partition = (1,) * 7
    types, matrix = admissible_types(partition, 7)
    columns = []
    for j in range(7):
        column = tuple(design[i][j] for i in range(7))
        if sum(column) % 4 != 3:
            column = tuple(-value for value in column)
        require(column in types, "known order-7 column is not admissible")
        columns.append(column)
    observed = [
        [sum(column[i] * column[j] for column in columns) for j in range(7)]
        for i in range(7)
    ]
    require(observed == matrix, "known order-7 moment identity failed")
    return {"admissible_types": len(types), "normalized_columns": len(columns)}


def expect_failure(action, description: str) -> None:
    try:
        action()
    except CheckError:
        return
    raise CheckError(f"negative control was accepted: {description}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()

    certificate_path = TARGET / "certificate.json"
    moment_path = TARGET / "moment_certificate.json"
    hasse_data = json.loads(certificate_path.read_text())
    moment_data = json.loads(moment_path.read_text())

    record_text = (TARGET / "record23.txt").read_text()
    record_matrix = parse_sign_matrix(record_text, ORDER)
    require(abs(bareiss(record_matrix)) == RECORD, "record determinant mismatch")

    partitions = partitions_by_dynamic_sets(ORDER)
    require(len(partitions) == 1255, "integer-partition count mismatch")
    scan_records = []
    above = []
    candidates = []
    for partition in partitions:
        determinant = ehlich_determinant(partition, ORDER)
        at_record = determinant >= RECORD * RECORD
        root = isqrt(determinant)
        square = root * root == determinant
        scan_records.append(
            f"{','.join(map(str, partition))}|{determinant}|{int(at_record)}|{int(square)}"
        )
        if at_record:
            above.append(partition)
            if square:
                candidates.append((partition, root))

    expected_candidates = [
        (tuple(item["partition"]), int(item["sqrt_determinant"]))
        for item in hasse_data["square_candidates"]
    ]
    require(len(above) == 894, "record-threshold partition count mismatch")
    require(candidates == expected_candidates, "square-candidate list mismatch")
    require(
        [tuple(case["partition"]) for case in moment_data["cases"]]
        == [partition for partition, _ in candidates],
        "moment cases do not equal the complete square-candidate list",
    )

    counts = []
    type_records = []
    obstruction_records = []
    empty_cases = 0
    matrices: dict[tuple[int, ...], list[list[int]]] = {}
    type_sets: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
    for case in moment_data["cases"]:
        partition = tuple(case["partition"])
        types, matrix = admissible_types(partition, ORDER)
        matrices[partition] = matrix
        type_sets[partition] = types
        digest = types_hash(types)
        require(len(types) == int(case["admissible_type_count"]), "type count mismatch")
        require(digest == case["admissible_types_sha256"], "type digest mismatch")
        counts.append(len(types))
        type_records.append(f"{','.join(map(str, partition))}|{len(types)}|{digest}")
        if not types:
            require(case["certificate"] is None, "empty type set has a certificate")
            empty_cases += 1
            obstruction_records.append(f"{','.join(map(str, partition))}|empty")
            continue
        minimum, maximum, target = check_obstruction(partition, types, matrix, case)
        obstruction_records.append(
            f"{','.join(map(str, partition))}|{minimum}|{maximum}|{target}"
        )

    require(empty_cases == 1, "wrong number of empty-type obstructions")

    negative_controls = 0
    expect_failure(
        lambda: parse_sign_matrix("0" + record_text[1:], ORDER),
        "invalid record symbol",
    )
    negative_controls += 1
    expect_failure(
        lambda: require(
            candidates[:-1] == expected_candidates,
            "candidate omission was detected",
        ),
        "omitted square candidate",
    )
    negative_controls += 1
    first_case = json.loads(json.dumps(moment_data["cases"][0]))
    first_case["certificate"]["constant"] -= 1
    first_partition = tuple(first_case["partition"])
    expect_failure(
        lambda: check_obstruction(
            first_partition,
            type_sets[first_partition],
            matrices[first_partition],
            first_case,
        ),
        "altered separating polynomial",
    )
    negative_controls += 1

    result = {
        "admissible_type_counts": counts,
        "candidate_partitions_sha256": hashlib.sha256(
            ("\n".join(scan_records) + "\n").encode("ascii")
        ).hexdigest(),
        "certificate_sha256": sha256_file(certificate_path),
        "empty_type_obstructions": empty_cases,
        "integer_partitions": len(partitions),
        "moment_certificate_sha256": sha256_file(moment_path),
        "negative_controls_rejected": negative_controls,
        "partitions_at_or_above_record": len(above),
        "perfect_square_candidates": len(candidates),
        "positive_order7_control": positive_order7_control(),
        "quadratic_obstructions": len(candidates) - empty_cases,
        "record_determinant": RECORD,
        "status": "INDEPENDENT_EHLICH_MOMENT_REVIEW_PASSED",
        "type_sets_sha256": hashlib.sha256(
            ("\n".join(type_records) + "\n").encode("ascii")
        ).hexdigest(),
        "obstruction_records_sha256": hashlib.sha256(
            ("\n".join(obstruction_records) + "\n").encode("ascii")
        ).hexdigest(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
