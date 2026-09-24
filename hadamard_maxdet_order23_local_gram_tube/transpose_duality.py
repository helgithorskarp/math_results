#!/usr/bin/env python3
"""Construct explicit transpose dualities for the fourteen Gram classes."""

from __future__ import annotations

import itertools
import hashlib
import json
import sys
from collections import deque
from pathlib import Path

import candidate_obstructions
import symmetry
from verify import gram_matrix, read_record
from verify_gram_decompositions import (
    candidate_actions,
    matrix_key,
    representative_matrix,
)


ORDER = 23
EXPECTED_CLASS_MAP = (11, 12, 7, 8, 5, 6, 3, 4, 9, 10, 1, 2, 13, 14)
DECOMPOSITION_CERTIFICATE_SHA256 = (
    "7b94f5918015a250db3619c7e1f2f37a8d31a3e2ad589afe21a99a30a445aa81"
)


def vector_mask(vector: list[int]) -> int:
    if vector[0] < 0:
        vector = [-entry for entry in vector]
    return sum(
        (vector[coordinate] < 0) << (coordinate - 1)
        for coordinate in range(1, ORDER)
    )


def components(adjacency: list[list[bool]]) -> list[list[int]]:
    unseen = set(range(ORDER))
    answer = []
    while unseen:
        seed = min(unseen)
        component = []
        stack = [seed]
        unseen.remove(seed)
        while stack:
            vertex = stack.pop()
            component.append(vertex)
            for neighbor in range(ORDER):
                if adjacency[vertex][neighbor] and neighbor in unseen:
                    unseen.remove(neighbor)
                    stack.append(neighbor)
        answer.append(sorted(component))
    return sorted(answer, key=lambda item: (-len(item), item))


def magnitude_graph_map(
    adjacency: list[list[bool]], base_adjacency: list[list[bool]]
) -> tuple[int, ...]:
    """Map the structured 15+4+4 magnitude-three graph to the base graph."""
    source_components = components(adjacency)
    target_components = components(base_adjacency)
    assert [len(item) for item in source_components] == [15, 4, 4]
    assert [len(item) for item in target_components] == [15, 4, 4]
    source_large = source_components[0]
    target_large = target_components[0]
    source_degree = {
        vertex: sum(adjacency[vertex]) for vertex in source_large
    }
    target_degree = {
        vertex: sum(base_adjacency[vertex]) for vertex in target_large
    }
    source_core = sorted(
        vertex for vertex in source_large if source_degree[vertex] == 6
    )
    target_core = sorted(
        vertex for vertex in target_large if target_degree[vertex] == 6
    )
    assert len(source_core) == len(target_core) == 3

    for core_image in itertools.permutations(target_core):
        image = dict(zip(source_core, core_image))
        for missing_source in source_core:
            source_active = sorted(
                vertex
                for vertex in source_large
                if source_degree[vertex] == 5
                and not adjacency[vertex][missing_source]
            )
            missing_target = image[missing_source]
            target_active = sorted(
                vertex
                for vertex in target_large
                if target_degree[vertex] == 5
                and not base_adjacency[vertex][missing_target]
            )
            if len(source_active) != 2 or len(target_active) != 2:
                break
            image.update(zip(source_active, target_active))
            source_inactive = sorted(
                vertex
                for vertex in source_large
                if source_degree[vertex] == 3
                and any(adjacency[vertex][active] for active in source_active)
            )
            target_inactive = sorted(
                vertex
                for vertex in target_large
                if target_degree[vertex] == 3
                and any(
                    base_adjacency[vertex][active] for active in target_active
                )
            )
            if len(source_inactive) != 2 or len(target_inactive) != 2:
                break
            image.update(zip(source_inactive, target_inactive))
        for source, target in zip(source_components[1:], target_components[1:]):
            image.update(zip(source, target))
        if len(image) != ORDER:
            continue
        permutation = tuple(image[vertex] for vertex in range(ORDER))
        if all(
            adjacency[left][right]
            == base_adjacency[permutation[left]][permutation[right]]
            for left in range(ORDER)
            for right in range(ORDER)
        ):
            return permutation
    raise AssertionError("magnitude-three graph is not isomorphic to the base")


def center_transpose(
    matrix: list[list[int]], base: list[list[int]]
) -> tuple[list[list[int]], tuple[int, ...], tuple[int, ...]]:
    transpose = [list(row) for row in zip(*matrix)]
    column_gram = gram_matrix(transpose)
    adjacency = [
        [abs(column_gram[left][right]) == 3 for right in range(ORDER)]
        for left in range(ORDER)
    ]
    base_adjacency = [
        [base[left][right] == 3 for right in range(ORDER)]
        for left in range(ORDER)
    ]
    signs = [1]
    for vertex in range(1, ORDER):
        desired_sign = 1 if adjacency[0][vertex] else -1
        observed_sign = 1 if column_gram[0][vertex] > 0 else -1
        signs.append(desired_sign * observed_sign)
    assert all(
        signs[left] * signs[right] * column_gram[left][right]
        == (3 if adjacency[left][right] else -1)
        for left in range(ORDER)
        for right in range(left)
    )
    permutation = magnitude_graph_map(adjacency, base_adjacency)
    centered = [[0] * ORDER for _ in range(ORDER)]
    for source in range(ORDER):
        centered[permutation[source]] = [
            signs[source] * entry for entry in transpose[source]
        ]
    assert gram_matrix(centered) == base
    return centered, permutation, tuple(signs)


def find_representative_action(
    seed: tuple[int, ...],
    representative_classes: dict[tuple[int, ...], int],
    actions: list[tuple[int, ...]],
    generators: list[tuple[int, ...]],
) -> tuple[int, tuple[int, ...]]:
    identity = tuple(range(ORDER))
    queue = deque([seed])
    permutations = {seed: identity}
    while queue:
        current = queue.popleft()
        permutation = permutations[current]
        if current in representative_classes:
            return representative_classes[current], permutation
        for action, generator in zip(actions, generators):
            image = tuple(sorted(action[index] for index in current))
            if image not in permutations:
                permutations[image] = tuple(
                    generator[permutation[source]] for source in range(ORDER)
                )
                queue.append(image)
    raise AssertionError("transpose left the certified decomposition classes")


def explicit_equivalence(
    source: list[list[int]],
    target: list[list[int]],
    centering_permutation: tuple[int, ...],
    centering_signs: tuple[int, ...],
    automorphism: tuple[int, ...],
) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
    centered = [[0] * ORDER for _ in range(ORDER)]
    transpose = [list(row) for row in zip(*source)]
    for source_row in range(ORDER):
        centered[centering_permutation[source_row]] = [
            centering_signs[source_row] * entry for entry in transpose[source_row]
        ]
    moved = [[0] * ORDER for _ in range(ORDER)]
    for source_row in range(ORDER):
        moved[automorphism[source_row]] = centered[source_row]

    target_masks = [
        vector_mask([target[row][column] for row in range(ORDER)])
        for column in range(ORDER)
    ]
    target_position = {mask: index for index, mask in enumerate(target_masks)}
    column_permutation = []
    column_signs = []
    for source_column in range(ORDER):
        vector = [moved[row][source_column] for row in range(ORDER)]
        sign = vector[0]
        normalized = [sign * entry for entry in vector]
        mask = vector_mask(normalized)
        column_permutation.append(target_position[mask])
        column_signs.append(sign)
    assert sorted(column_permutation) == list(range(ORDER))

    row_permutation = tuple(
        automorphism[centering_permutation[source_row]]
        for source_row in range(ORDER)
    )
    result = [[0] * ORDER for _ in range(ORDER)]
    for source_row in range(ORDER):
        for source_column in range(ORDER):
            result[row_permutation[source_row]][column_permutation[source_column]] = (
                centering_signs[source_row]
                * column_signs[source_column]
                * transpose[source_row][source_column]
            )
    assert result == target
    return (
        row_permutation,
        centering_signs,
        tuple(column_permutation),
        tuple(column_signs),
    )


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python3 transpose_duality.py DECOMPOSITIONS.json")
    decomposition_path = Path(sys.argv[1])
    decomposition = json.loads(decomposition_path.read_text())
    assert hashlib.sha256(
        decomposition_path.read_bytes()
    ).hexdigest() == DECOMPOSITION_CERTIFICATE_SHA256

    base = gram_matrix(read_record())
    scale, numerator = candidate_obstructions.scaled_inverse(base)
    masks = candidate_obstructions.enumerate_normalized_columns(scale, numerator)
    vectors = [candidate_obstructions.vector_from_mask(mask) for mask in masks]
    mask_index = {mask: index for index, mask in enumerate(masks)}
    _, _, first_generators, second_generators = symmetry.factor_groups()
    generators = [symmetry.lift_first(item) for item in first_generators] + [
        symmetry.lift_second(item) for item in second_generators
    ]
    actions = candidate_actions(masks, vectors, generators)

    reports = decomposition["orbits"]
    matrices = {
        report["class"]: representative_matrix(tuple(report["column_masks"]))
        for report in reports
    }
    representative_classes = {
        tuple(sorted(mask_index[mask] for mask in report["column_masks"])): report[
            "class"
        ]
        for report in reports
    }
    equivalences = []
    observed_map = []
    for source_class in range(1, len(reports) + 1):
        source = matrices[source_class]
        centered, centering_permutation, centering_signs = center_transpose(
            source, base
        )
        seed = matrix_key(centered, mask_index)
        target_class, automorphism = find_representative_action(
            seed, representative_classes, actions, generators
        )
        observed_map.append(target_class)
        target = matrices[target_class]
        row_permutation, row_signs, column_permutation, column_signs = (
            explicit_equivalence(
                source,
                target,
                centering_permutation,
                centering_signs,
                automorphism,
            )
        )
        equivalences.append(
            {
                "source_class": source_class,
                "target_class": target_class,
                "row_permutation": list(row_permutation),
                "row_signs": list(row_signs),
                "column_permutation": list(column_permutation),
                "column_signs": list(column_signs),
            }
        )

    assert tuple(observed_map) == EXPECTED_CLASS_MAP
    assert all(observed_map[observed_map[index] - 1] == index + 1 for index in range(14))
    fixed = [index + 1 for index, image in enumerate(observed_map) if image == index + 1]
    pairs = [
        [index + 1, image]
        for index, image in enumerate(observed_map)
        if index + 1 < image
    ]
    print(
        json.dumps(
            {
                "order": ORDER,
                "decomposition_certificate_sha256": DECOMPOSITION_CERTIFICATE_SHA256,
                "transpose_class_map": observed_map,
                "fixed_classes": fixed,
                "two_cycles": pairs,
                "equivalences": equivalences,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
