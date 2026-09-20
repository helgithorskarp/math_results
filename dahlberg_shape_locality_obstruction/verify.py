#!/usr/bin/env python3
"""Verify the sharp order-five RSK-shape obstruction for 1432/2134.

All enumeration and pattern tests are definition-level.  The script also
checks the RSK implementation by forward/inverse round trips on every element
of S_5 before using tableau transposition.
"""

from __future__ import annotations

import itertools
from collections import Counter


Permutation = tuple[int, ...]
Partition = tuple[int, ...]
DescentSet = tuple[int, ...]


def standardize(values: tuple[int, ...]) -> tuple[int, ...]:
    rank = {value: i + 1 for i, value in enumerate(sorted(values))}
    return tuple(rank[value] for value in values)


def contains(permutation: Permutation, pattern: str) -> bool:
    target = tuple(map(int, pattern))
    return any(
        standardize(tuple(permutation[i] for i in indices)) == target
        for indices in itertools.combinations(range(len(permutation)), len(target))
    )


def is_involution(permutation: Permutation) -> bool:
    return all(permutation[permutation[i] - 1] == i + 1 for i in range(len(permutation)))


def avoiders(n: int, pattern: str) -> tuple[Permutation, ...]:
    return tuple(
        permutation
        for permutation in itertools.permutations(range(1, n + 1))
        if is_involution(permutation) and not contains(permutation, pattern)
    )


def descent_set(permutation: Permutation) -> DescentSet:
    return tuple(i for i in range(1, len(permutation)) if permutation[i - 1] > permutation[i])


def complement(descent: DescentSet, n: int) -> DescentSet:
    return tuple(i for i in range(1, n) if i not in descent)


def rsk(permutation: Permutation) -> tuple[list[list[int]], list[list[int]]]:
    insertion: list[list[int]] = []
    recording: list[list[int]] = []
    for label, value in enumerate(permutation, 1):
        bumped = value
        row = 0
        while True:
            if row == len(insertion):
                insertion.append([bumped])
                recording.append([label])
                break
            column = next(
                (j for j, entry in enumerate(insertion[row]) if entry > bumped),
                len(insertion[row]),
            )
            if column == len(insertion[row]):
                insertion[row].append(bumped)
                recording[row].append(label)
                break
            insertion[row][column], bumped = bumped, insertion[row][column]
            row += 1
    return insertion, recording


def transpose_tableau(tableau: list[list[int]]) -> list[list[int]]:
    return [
        [tableau[i][j] for i in range(len(tableau)) if j < len(tableau[i])]
        for j in range(len(tableau[0]))
    ]


def inverse_rsk(insertion: list[list[int]], recording: list[list[int]]) -> Permutation:
    insertion = [row[:] for row in insertion]
    recording = [row[:] for row in recording]
    result = [0] * sum(map(len, insertion))
    for label in range(len(result), 0, -1):
        row, column = next(
            (i, j)
            for i, entries in enumerate(recording)
            for j, entry in enumerate(entries)
            if entry == label
        )
        bumped = insertion[row].pop(column)
        recording[row].pop(column)
        if not insertion[row]:
            insertion.pop()
            recording.pop()
        for previous_row in range(row - 1, -1, -1):
            column = max(
                j for j, entry in enumerate(insertion[previous_row]) if entry < bumped
            )
            insertion[previous_row][column], bumped = (
                bumped,
                insertion[previous_row][column],
            )
        result[label - 1] = bumped
    return tuple(result)


def tableau_transpose(permutation: Permutation) -> Permutation:
    insertion, recording = rsk(permutation)
    return inverse_rsk(
        transpose_tableau(insertion), transpose_tableau(recording)
    )


def shape(permutation: Permutation) -> Partition:
    insertion, _ = rsk(permutation)
    return tuple(map(len, insertion))


def conjugate(partition: Partition) -> Partition:
    return tuple(
        sum(part >= column for part in partition)
        for column in range(1, partition[0] + 1)
    )


def cell_counter(
    permutations: tuple[Permutation, ...], *, target_side: bool
) -> Counter[tuple[Partition, DescentSet]]:
    result: Counter[tuple[Partition, DescentSet]] = Counter()
    for permutation in permutations:
        if target_side:
            key = (conjugate(shape(permutation)), complement(descent_set(permutation), 5))
        else:
            key = (shape(permutation), descent_set(permutation))
        result[key] += 1
    return result


def verify_rsk() -> None:
    for n in range(1, 6):
        for permutation in itertools.permutations(range(1, n + 1)):
            insertion, recording = rsk(permutation)
            assert inverse_rsk(insertion, recording) == permutation
            transposed = tableau_transpose(permutation)
            assert tableau_transpose(transposed) == permutation
            if is_involution(permutation):
                assert is_involution(transposed)
                assert descent_set(transposed) == complement(descent_set(permutation), n)
                assert shape(transposed) == conjugate(shape(permutation))


def verify() -> None:
    verify_rsk()

    # Tableau transposition works without repair below the first obstruction.
    for n in range(1, 5):
        source = avoiders(n, "1432")
        target = set(avoiders(n, "2134"))
        assert {tableau_transpose(permutation) for permutation in source} == target

    source = avoiders(5, "1432")
    target = avoiders(5, "2134")
    assert len(source) == len(target) == 21

    source_cells = cell_counter(source, target_side=False)
    target_cells = cell_counter(target, target_side=True)
    keys = set(source_cells) | set(target_cells)
    discrepancies = {
        key: (source_cells[key], target_cells[key])
        for key in keys
        if source_cells[key] != target_cells[key]
    }
    expected_discrepancies = {
        ((2, 1, 1, 1), (1, 3, 4)): (1, 0),
        ((2, 2, 1), (1, 3, 4)): (0, 1),
        ((2, 2, 1), (2, 3)): (1, 0),
        ((3, 1, 1), (2, 3)): (0, 1),
        ((2, 2, 1), (2, 4)): (1, 0),
        ((3, 1, 1), (2, 4)): (0, 1),
    }
    assert discrepancies == expected_discrepancies

    maximum_local = sum(min(source_cells[key], target_cells[key]) for key in keys)
    forced_cross_shape = len(source) - maximum_local
    assert maximum_local == 18
    assert forced_cross_shape == 3

    replacements = {
        (5, 2, 4, 3, 1): (3, 4, 1, 2, 5),
        (4, 5, 3, 1, 2): (5, 2, 3, 4, 1),
        (3, 5, 1, 4, 2): (4, 2, 3, 1, 5),
    }
    repaired = {
        permutation: replacements.get(permutation, tableau_transpose(permutation))
        for permutation in source
    }
    assert set(repaired.values()) == set(target)
    assert all(
        descent_set(image) == complement(descent_set(permutation), 5)
        for permutation, image in repaired.items()
    )
    violations = [
        permutation
        for permutation, image in repaired.items()
        if shape(image) != conjugate(shape(permutation))
    ]
    assert set(violations) == set(replacements)

    plain_bad = {
        permutation: tableau_transpose(permutation)
        for permutation in source
        if tableau_transpose(permutation) not in target
    }
    assert plain_bad == {
        (5, 2, 4, 3, 1): (1, 3, 2, 4, 5),
        (4, 5, 3, 1, 2): (2, 1, 3, 5, 4),
        (3, 5, 1, 4, 2): (2, 1, 4, 3, 5),
    }

    print(
        "n=5: |C|=|E|=21, maximum shape-local matches=18, "
        "forced cross-shape moves=3"
    )
    print("verified sharp three-replacement repair and minimal order-five obstruction")


if __name__ == "__main__":
    try:
        verify()
    except AssertionError as error:
        raise SystemExit(f"ERROR: verification failed: {error}")
