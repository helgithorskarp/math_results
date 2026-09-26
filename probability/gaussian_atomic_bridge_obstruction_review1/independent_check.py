#!/usr/bin/env python3
"""Independent exact audit of the asymmetric nine-atom obstruction.

No reviewed module is imported.  Contracting bijections are found by an
incremental distance-compatible backtracking search (not by filtering 9!),
and the covariance eigenvalue counts use exact characteristic-polynomial
Sturm sequences rather than the reviewed LDL certificates.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, permutations, product
import json
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def dot(x, y):
    return sum(a * b for a, b in zip(x, y, strict=True))


def sub(x, y):
    return tuple(a - b for a, b in zip(x, y, strict=True))


def distance_squared(x, y):
    return dot(sub(x, y), sub(x, y))


def determinant(matrix):
    if not matrix:
        return Q(1)
    return sum(
        (-1) ** column * matrix[0][column]
        * determinant([
            [row[index] for index in range(len(matrix)) if index != column]
            for row in matrix[1:]
        ])
        for column in range(len(matrix))
    )


def matrix_rank(matrix) -> int:
    rows = [[Q(value) for value in row] for row in matrix]
    if not rows:
        return 0
    rank = 0
    for column in range(len(rows[0])):
        pivot = next((row for row in range(rank, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][column]
        rows[rank] = [value / pivot_value for value in rows[rank]]
        for row in range(len(rows)):
            if row == rank or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [a - factor * b
                         for a, b in zip(rows[row], rows[rank], strict=True)]
        rank += 1
    return rank


ZERO = (0, 0, 0)
FIXED = (
    (1, 0, 1),
    (0, 1, 1),
    (-1, 0, 1),
    (0, -1, 1),
)
MOVING = (
    (1, 1, 1),
    (-1, 1, 1),
    (-1, -1, 1),
    (1, -1, 1),
)
SOURCE = (ZERO,) + FIXED + tuple(tuple(-value for value in point)
                                 for point in MOVING)
TARGET = (ZERO,) + FIXED + MOVING
WEIGHT_NUMERATORS = (8, 12, 7, 15, 44, 21, 11, 23, 43)
DENOMINATOR = sum(WEIGHT_NUMERATORS)
WEIGHTS = tuple(Q(value, DENOMINATOR) for value in WEIGHT_NUMERATORS)
require(DENOMINATOR == 184 and len(set(WEIGHT_NUMERATORS)) == 9,
        "weight specification failed")


SOURCE_DISTANCES = tuple(
    tuple(distance_squared(a, b) for b in SOURCE) for a in SOURCE
)
TARGET_DISTANCES = tuple(
    tuple(distance_squared(a, b) for b in TARGET) for a in TARGET
)


def contraction_backtracking():
    # Assign sources in a fixed order but reject a partial bijection as soon as
    # any already visible distance would expand.  This explores a different
    # search tree from the reviewed direct permutation filter.
    assignment = [-1] * 9
    used = [False] * 9
    solutions = []
    nodes = 0
    rejected_extensions = 0

    def visit(source_index: int) -> None:
        nonlocal nodes, rejected_extensions
        nodes += 1
        if source_index == 9:
            solutions.append(tuple(assignment))
            return
        for target_index in range(8, -1, -1):
            if used[target_index]:
                continue
            compatible = True
            for previous in range(source_index):
                if (TARGET_DISTANCES[target_index][assignment[previous]]
                        > SOURCE_DISTANCES[source_index][previous]):
                    compatible = False
                    break
            if not compatible:
                rejected_extensions += 1
                continue
            assignment[source_index] = target_index
            used[target_index] = True
            visit(source_index + 1)
            used[target_index] = False
            assignment[source_index] = -1

    visit(0)
    require(len(set(solutions)) == len(solutions), "duplicate backtracking output")
    return tuple(sorted(solutions)), nodes, rejected_extensions


def group_isometries(points):
    return tuple(
        permutation for permutation in permutations(range(4))
        if all(
            distance_squared(points[first], points[second])
            == distance_squared(points[permutation[first]],
                                points[permutation[second]])
            for first, second in combinations(range(4), 2)
        )
    )


def paired_rank(mapping):
    return matrix_rank([
        SOURCE[index] + TARGET[mapping[index]] for index in range(9)
    ])


def classification_audit():
    losses = Counter(
        SOURCE_DISTANCES[first][second] - TARGET_DISTANCES[first][second]
        for first, second in combinations(range(9), 2)
    )
    require(losses == Counter({0: 28, 8: 8}),
            "prescribed distance-loss distribution failed")
    contractions, nodes, rejected = contraction_backtracking()
    require(len(contractions) == 64, "incorrect contracting-bijection count")
    require(all(mapping[0] == 0 for mapping in contractions),
            "a contraction moves the origin")
    require(all(set(mapping[1:5]) == set(range(1, 5))
                and set(mapping[5:9]) == set(range(5, 9))
                for mapping in contractions), "a contraction mixes the squares")

    fixed_symmetries = group_isometries(FIXED)
    moving_symmetries = group_isometries(MOVING)
    require(len(fixed_symmetries) == len(moving_symmetries) == 8,
            "square symmetry count failed")
    predicted = {
        (0,) + tuple(1 + index for index in first)
        + tuple(5 + index for index in second)
        for first, second in product(fixed_symmetries, moving_symmetries)
    }
    require(set(contractions) == predicted,
            "structural classification misses a contraction")
    ranks = Counter(paired_rank(mapping) for mapping in contractions)
    require(ranks == Counter({4: 8, 5: 32, 6: 24}),
            "paired-rank distribution failed")
    return contractions, {
        "prescribed_pair_losses": {str(key): value for key, value in sorted(losses.items())},
        "search_algorithm": "incremental reverse-target backtracking",
        "search_nodes": nodes,
        "rejected_partial_extensions": rejected,
        "contracting_bijections": len(contractions),
        "square_symmetries_each": len(fixed_symmetries),
        "structural_cover_exact": True,
        "paired_rank_distribution": {str(key): value
                                     for key, value in sorted(ranks.items())},
    }


def covariance(points):
    mean = tuple(
        sum(weight * point[coordinate]
            for weight, point in zip(WEIGHTS, points, strict=True))
        for coordinate in range(3)
    )
    return [
        [
            sum(
                weight * (point[row] - mean[row]) * (point[column] - mean[column])
                for weight, point in zip(WEIGHTS, points, strict=True)
            )
            for column in range(3)
        ]
        for row in range(3)
    ]


def characteristic_polynomial(matrix):
    # Coefficients are low degree first for det(lambda I - matrix).
    trace = sum(matrix[index][index] for index in range(3))
    second = sum(
        matrix[first][first] * matrix[second_index][second_index]
        - matrix[first][second_index] * matrix[second_index][first]
        for first, second_index in combinations(range(3), 2)
    )
    return [-determinant(matrix), second, -trace, Q(1)]


def trim(polynomial):
    polynomial = list(polynomial)
    while polynomial and polynomial[-1] == 0:
        polynomial.pop()
    return polynomial


def polynomial_derivative(polynomial):
    return [index * polynomial[index] for index in range(1, len(polynomial))]


def polynomial_remainder(dividend, divisor):
    remainder = trim(dividend)
    divisor = trim(divisor)
    require(divisor, "polynomial division by zero")
    while len(remainder) >= len(divisor):
        shift = len(remainder) - len(divisor)
        factor = remainder[-1] / divisor[-1]
        for index, value in enumerate(divisor):
            remainder[index + shift] -= factor * value
        remainder = trim(remainder)
    return remainder


def polynomial_value(polynomial, value):
    result = Q(0)
    for coefficient in reversed(polynomial):
        result = result * value + coefficient
    return result


def sign(value):
    return 1 if value > 0 else -1 if value < 0 else 0


def variations(signs):
    nonzero = [value for value in signs if value]
    return sum(first != second for first, second in zip(nonzero, nonzero[1:]))


def sturm_sequence(polynomial):
    sequence = [trim(polynomial), trim(polynomial_derivative(polynomial))]
    while len(sequence[-1]) > 1:
        remainder = polynomial_remainder(sequence[-2], sequence[-1])
        require(remainder, "repeated characteristic root")
        sequence.append([-value for value in remainder])
    return sequence


def roots_above(polynomial, threshold):
    sequence = sturm_sequence(polynomial)
    at_threshold = [sign(polynomial_value(item, threshold)) for item in sequence]
    require(at_threshold[0] != 0, "threshold is an eigenvalue")
    at_infinity = [sign(item[-1]) for item in sequence]
    count = variations(at_threshold) - variations(at_infinity)
    at_negative_infinity = [sign(item[-1]) * (-1) ** (len(item) - 1)
                            for item in sequence]
    require(variations(at_negative_infinity) - variations(at_infinity) == 3,
            "characteristic polynomial does not have three real simple roots")
    return count, sequence


def covariance_audit():
    expected_numerators = (
        (
            (21911, -1939, 4308),
            (-1939, 27407, -13124),
            (4308, -13124, 31984),
        ),
        (
            (22271, 77, 216),
            (77, 22375, -568),
            (216, -568, 1408),
        ),
    )
    records = []
    for name, points, expected, threshold, expected_above in (
        ("source", SOURCE, expected_numerators[0], Q(16, 25), 1),
        ("target", TARGET, expected_numerators[1], Q(13, 20), 2),
    ):
        matrix = covariance(points)
        numerator = tuple(tuple(int(value * DENOMINATOR ** 2) for value in row)
                          for row in matrix)
        require(numerator == expected, f"{name} covariance numerator mismatch")
        polynomial = characteristic_polynomial(matrix)
        above, sequence = roots_above(polynomial, threshold)
        require(above == expected_above, f"{name} eigenvalue count mismatch")
        records.append({
            "law": name,
            "matrix_numerator": [list(row) for row in numerator],
            "denominator": DENOMINATOR ** 2,
            "threshold": str(threshold),
            "eigenvalues_above_threshold": above,
            "characteristic_polynomial": [str(value) for value in polynomial],
            "sturm_degrees": [len(item) - 1 for item in sequence],
            "characteristic_value_at_threshold": str(
                polynomial_value(polynomial, threshold)
            ),
        })
    central_gap = Q(13, 20) - Q(16, 25)
    radius = Q(1, 4000)
    robust_gap = central_gap - 18 * radius
    require(central_gap == Q(1, 100) and robust_gap == Q(11, 2000),
            "robust covariance gap arithmetic failed")
    require(min(WEIGHTS) - radius > 0, "weight ball can reach zero")
    require(min(abs(first - second) for first, second in combinations(WEIGHTS, 2))
            - 2 * radius > 0, "weight ball can merge masses")
    return {
        "certificates": records,
        "central_middle_eigenvalue_gap_lower_bound": str(central_gap),
        "covariance_l1_lipschitz_constant_each": 9,
        "weight_l1_radius": str(radius),
        "robust_middle_eigenvalue_gap": str(robust_gap),
    }


def motion_audit():
    incidences = [
        (fixed, moving)
        for fixed, moving in product(range(4), repeat=2)
        if dot(FIXED[fixed], MOVING[moving]) == 0
    ]
    constraints = [
        [FIXED[fixed][row] * MOVING[moving][column]
         for row, column in product(range(3), repeat=2)]
        for fixed, moving in incidences
    ]
    identity = [int(row == column) for row, column in product(range(3), repeat=2)]
    require(len(incidences) == 8 and matrix_rank(constraints) == 8,
            "projection constraints do not have a one-dimensional kernel")
    require(all(dot(row, identity) == 0 for row in constraints),
            "identity is not in the projection kernel")
    circuit = (1, -1, 1, -1)
    require(all(sum(circuit[index] * MOVING[index][coordinate]
                    for index in range(4)) == 0 for coordinate in range(3)),
            "moving circuit failed")
    gram = [[dot(first, second) for second in MOVING[:3]]
            for first in MOVING[:3]]
    require(determinant(gram) == 16 and matrix_rank(gram) == 3,
            "moving rigid cluster is not three-dimensional")
    return {
        "zero_cross_incidences": len(incidences),
        "projection_constraint_rank": matrix_rank(constraints),
        "projection_kernel": "scalar multiples of the identity",
        "moving_circuit": "b0-b1+b2-b3=0",
        "moving_gram_rank": matrix_rank(gram),
        "moving_gram_determinant": int(determinant(gram)),
        "orthogonal_complement_dimension_in_R5": 2,
    }


def separation_audit(contractions):
    norm = dot(WEIGHTS, WEIGHTS)
    identity = tuple(range(9))
    margins = {
        mapping: norm - dot(
            WEIGHTS, tuple(WEIGHTS[mapping[index]] for index in range(9))
        )
        for mapping in contractions
    }
    require(margins[identity] == 0
            and all(value > 0 for mapping, value in margins.items()
                    if mapping != identity), "mass separation is not strict")
    minimum = min(value for mapping, value in margins.items()
                  if mapping != identity)
    minimizers = [mapping for mapping, value in margins.items()
                  if value == minimum]
    require(minimum == Q(1, 8464), "minimum mass margin is wrong")
    require(any(paired_rank(mapping) == 5 for mapping in minimizers),
            "no liftable map attains the advertised margin")
    coefficient = (max(WEIGHTS) - min(WEIGHTS)) / 2
    output_radius = minimum / coefficient
    require(coefficient == Q(37, 368) and output_radius == Q(1, 851),
            "approximate-output radius arithmetic failed")

    uniform = tuple(Q(1, 9) for _ in range(9))
    rank_four = next(mapping for mapping in contractions
                     if mapping != identity and paired_rank(mapping) == 4)
    require(dot(uniform, uniform) == dot(
        uniform, tuple(uniform[mapping] for mapping in rank_four)
    ), "repeated-weight boundary control failed")
    bad_swap = (1, 0, 2, 3, 4, 5, 6, 7, 8)
    require(bad_swap not in contractions, "origin-moving control was accepted")
    return {
        "minimum_nonidentity_margin": str(minimum),
        "minimizer_count": len(minimizers),
        "minimizer_rank_distribution": {
            str(rank): count for rank, count in sorted(
                Counter(paired_rank(mapping) for mapping in minimizers).items()
            )
        },
        "weight_range_half": str(coefficient),
        "approximate_output_l1_bound": str(output_radius),
        "identity_requires_cited_nonliftability": True,
        "repeated_weight_control": True,
        "origin_swap_rejected": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    contractions, classification = classification_audit()
    result = {
        "status": "INDEPENDENT_ATOMIC_BRIDGE_REVIEW_PASSED",
        "scope": (
            "Exact finite classification, Sturm covariance certificates, "
            "motion linear algebra, and perturbation constants; no Gaussian "
            "majorisation verdict is claimed."
        ),
        "classification": classification,
        "covariance": covariance_audit(),
        "motion_obstruction": motion_audit(),
        "approximate_common_output": separation_audit(contractions),
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (args.out / "result.json").write_text(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
