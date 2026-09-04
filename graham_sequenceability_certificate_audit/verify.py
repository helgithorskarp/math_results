#!/usr/bin/env python3
"""Definition-level verifier for certificate.json; standard library only."""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent


def rank_q(rows: list[list[int]]) -> int:
    if not rows:
        return 0
    matrix = [[Fraction(value) for value in row] for row in rows]
    rank = 0
    for column in range(len(matrix[0])):
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
                    value - scale * pivot_value
                    for value, pivot_value in zip(matrix[row], matrix[rank])
                ]
        rank += 1
    return rank


def in_rational_row_span(rows: list[list[int]], target: list[int]) -> bool:
    return rank_q(rows) == rank_q(rows + [target])


def standard_targets(n: int) -> list[list[int]]:
    targets: list[list[int]] = []
    for i in range(n):
        targets.append([int(j == i) for j in range(n)])
    for i, j in combinations(range(n), 2):
        targets.append([int(k == i) - int(k == j) for k in range(n)])
    return targets


def transition(ordering: list[int], interval: list[int]) -> tuple[list[int], list[int]]:
    """Apply the archived generate_children transition and return (order,row)."""
    i, j = interval
    n = len(ordering)
    assert 0 <= i < j < n
    assert j - i <= n // 2
    relation = [0] * n
    for position in range(i, j + 1):
        relation[ordering[position] - 1] = 1
    new_ordering = ordering.copy()
    if i >= 1:
        new_ordering[i], new_ordering[i - 1] = (
            new_ordering[i - 1],
            new_ordering[i],
        )
    else:
        new_ordering[j], new_ordering[j + 1] = (
            new_ordering[j + 1],
            new_ordering[j],
        )
    return new_ordering, relation


def group_sum(row: list[int], labels: list[list[int]]) -> tuple[int, ...]:
    width = len(labels[0])
    return tuple(
        sum(coefficient * label[coordinate] for coefficient, label in zip(row, labels))
        % 2
        for coordinate in range(width)
    )


def main() -> None:
    data = json.loads((HERE / "certificate.json").read_text())
    n = data["dimension"]
    constraints = data["constraints"]
    target = data["target"]
    labels = data["labels"]

    assert data["orderings"][0] == list(range(1, n + 1))
    ordering = data["orderings"][0]
    generated: list[list[int]] = []
    targets = standard_targets(n)
    for depth, interval in enumerate(data["path"]):
        ordering, relation = transition(ordering, interval)
        generated.append(relation)
        assert relation == constraints[depth]
        assert ordering == data["orderings"][depth + 1]
        if depth + 1 < len(data["path"]):
            assert not any(
                in_rational_row_span(generated, candidate) for candidate in targets
            )

    assert in_rational_row_span(constraints, target)
    coefficients = data["integer_relation_coefficients"]
    multiplier = data["integer_relation_multiplier"]
    combined = [
        sum(coefficient * row[column] for coefficient, row in zip(coefficients, constraints))
        for column in range(n)
    ]
    assert combined == [multiplier * value for value in target]
    assert multiplier == 2

    label_tuples = [tuple(label) for label in labels]
    assert len(set(label_tuples)) == n
    assert (0, 0, 0) not in label_tuples
    assert all(group_sum(row, labels) == (0, 0, 0) for row in constraints)
    target_value = group_sum(target, labels)
    assert target_value == tuple(labels[4]) != (0, 0, 0)
    assert tuple((multiplier * value) % 2 for value in target_value) == (0, 0, 0)

    print("path_reconstruction=PASS")
    print("proper_ancestors_nonterminal_over_Q=PASS")
    print("final_rational_terminal=e_5")
    print("integer_consequence=2*a_5=0")
    print("group_countermodel=(Z/2Z)^3")
    print("labels_pairwise_distinct_nonzero=PASS")
    print("all_four_recorded_relations=PASS")
    print("a_5_nonzero=PASS")
    print("rational_row_span_rule_sound_for_arbitrary_abelian_groups=FALSE")


if __name__ == "__main__":
    main()
