#!/usr/bin/env python3
"""Independent exact checker for all sign decompositions of the record Gram."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import candidate_obstructions
import symmetry
from verify import bareiss_determinant, gram_matrix, read_record
from verify_multicenter import (
    RECORD,
    ROW_PERMUTATION,
    ROW_SIGNS,
    read_second,
)


ORDER = 23
EXPECTED_COLUMN_HASH = (
    "bc8cd93dff3f9d88ffddcf428f4d107d452be4a197ec902fc53364f3cfd05ecb"
)


def center_second() -> list[list[int]]:
    second = read_second()
    centered = [[0] * ORDER for _ in range(ORDER)]
    for source in range(ORDER):
        centered[ROW_PERMUTATION[source]] = [
            ROW_SIGNS[source] * entry for entry in second[source]
        ]
    return centered


def column_mask(vector: list[int]) -> int:
    if vector[0] < 0:
        vector = [-entry for entry in vector]
    return sum(
        (vector[coordinate] < 0) << (coordinate - 1)
        for coordinate in range(1, ORDER)
    )


def matrix_key(matrix: list[list[int]], mask_index: dict[int, int]) -> tuple[int, ...]:
    key = tuple(
        sorted(
            mask_index[
                column_mask([matrix[row][column] for row in range(ORDER)])
            ]
            for column in range(ORDER)
        )
    )
    assert len(key) == ORDER and len(set(key)) == ORDER
    return key


def build_graph(
    vectors: list[list[int]], numerator: list[list[int]]
) -> tuple[list[int], int]:
    transformed = [
        [
            sum(numerator[row][column] * vector[column] for column in range(ORDER))
            for row in range(ORDER)
        ]
        for vector in vectors
    ]
    adjacency = [0] * len(vectors)
    edge_count = 0
    for left in range(len(vectors)):
        for right in range(left):
            product = sum(
                vectors[left][coordinate] * transformed[right][coordinate]
                for coordinate in range(ORDER)
            )
            if product == 0:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
                edge_count += 1
    return adjacency, edge_count


def clique_census(adjacency: list[int]) -> tuple[int, int]:
    """Count 23-cliques with Python integers and a greedy-color upper bound."""
    clique_count = 0
    node_count = 0

    def expand(candidates: int, size: int) -> None:
        nonlocal clique_count, node_count
        node_count += 1
        remaining = candidates
        order = []
        bounds = []
        color = 0
        while remaining:
            color += 1
            available = remaining
            while available:
                bit = available & -available
                vertex = bit.bit_length() - 1
                order.append(vertex)
                bounds.append(color)
                remaining ^= bit
                available ^= bit
                available &= ~adjacency[vertex]
                available &= remaining

        for position in range(len(order) - 1, -1, -1):
            if size + bounds[position] < ORDER:
                return
            vertex = order[position]
            bit = 1 << vertex
            successor = candidates & adjacency[vertex]
            if size + 1 == ORDER:
                clique_count += 1
            elif size + 1 + successor.bit_count() >= ORDER:
                expand(successor, size + 1)
            candidates ^= bit

    expand((1 << len(adjacency)) - 1, 0)
    return clique_count, node_count


def candidate_actions(
    masks: list[int], vectors: list[list[int]], generators: list[tuple[int, ...]]
) -> list[tuple[int, ...]]:
    mask_index = {mask: index for index, mask in enumerate(masks)}
    actions = []
    for generator in generators:
        action = []
        for vector in vectors:
            image = [0] * ORDER
            for coordinate in range(ORDER):
                image[generator[coordinate]] = vector[coordinate]
            action.append(mask_index[column_mask(image)])
        actions.append(tuple(action))
    return actions


def point_orbit_sizes(actions: list[tuple[int, ...]], size: int) -> list[int]:
    unseen = set(range(size))
    sizes = []
    while unseen:
        seed = min(unseen)
        orbit = {seed}
        stack = [seed]
        while stack:
            current = stack.pop()
            for action in actions:
                image = action[current]
                if image not in orbit:
                    orbit.add(image)
                    stack.append(image)
        unseen.difference_update(orbit)
        sizes.append(len(orbit))
    return sorted(sizes)


def solution_orbit(
    seed: tuple[int, ...], actions: list[tuple[int, ...]], masks: list[int]
) -> tuple[int, tuple[int, ...], set[tuple[int, ...]]]:
    orbit = {seed}
    stack = [seed]
    canonical = tuple(sorted(masks[index] for index in seed))
    while stack:
        current = stack.pop()
        current_masks = tuple(sorted(masks[index] for index in current))
        canonical = min(canonical, current_masks)
        for action in actions:
            image = tuple(sorted(action[index] for index in current))
            if image not in orbit:
                orbit.add(image)
                stack.append(image)
    return len(orbit), canonical, orbit


def representative_matrix(masks: tuple[int, ...]) -> list[list[int]]:
    columns = [candidate_obstructions.vector_from_mask(mask) for mask in masks]
    return [[columns[column][row] for column in range(ORDER)] for row in range(ORDER)]


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python3 verify_gram_decompositions.py RESULT.json")
    result = json.loads(Path(sys.argv[1]).read_text())

    first_matrix = read_record()
    base = gram_matrix(first_matrix)
    second_matrix = center_second()
    assert gram_matrix(second_matrix) == base
    assert abs(bareiss_determinant(first_matrix)) == RECORD
    assert abs(bareiss_determinant(second_matrix)) == RECORD

    scale, numerator = candidate_obstructions.scaled_inverse(base)
    assert scale == result["inverse_scale"] == 170_492_220
    masks = candidate_obstructions.enumerate_normalized_columns(scale, numerator)
    assert len(masks) == result["normalized_columns"] == 1_382
    assert candidate_obstructions.mask_hash(masks) == EXPECTED_COLUMN_HASH
    vectors = [candidate_obstructions.vector_from_mask(mask) for mask in masks]
    adjacency, edge_count = build_graph(vectors, numerator)
    assert edge_count == result["compatibility_edges"] == 338_582
    degree_counts = Counter(neighbors.bit_count() for neighbors in adjacency)
    assert degree_counts == Counter({440: 864, 569: 512, 946: 6})
    assert result["degree_counts"] == {
        str(degree): multiplicity for degree, multiplicity in degree_counts.items()
    }

    clique_count, node_count = clique_census(adjacency)
    assert clique_count == result["cliques"] == 552_960
    assert node_count == result["search_nodes"] == 9_804_083
    assert result["clique_size"] == ORDER

    first_factor, second_factor, first_generators, second_generators = (
        symmetry.factor_groups()
    )
    generators = [symmetry.lift_first(item) for item in first_generators] + [
        symmetry.lift_second(item) for item in second_generators
    ]
    assert len(generators) == result["automorphism_generators"] == 13
    group_order = len(first_factor) * len(second_factor)
    assert group_order == result["automorphism_group_order"] == 442_368
    assert all(
        base[generator[left]][generator[right]] == base[left][right]
        for generator in generators
        for left in range(ORDER)
        for right in range(ORDER)
    )
    actions = candidate_actions(masks, vectors, generators)
    assert point_orbit_sizes(actions, len(masks)) == result[
        "candidate_column_orbit_sizes"
    ] == [6, 432, 432, 512]

    mask_index = {mask: index for index, mask in enumerate(masks)}
    first_key = matrix_key(first_matrix, mask_index)
    second_key = matrix_key(second_matrix, mask_index)
    observed_sizes = Counter()
    canonical_representatives = set()
    covered_count = 0
    first_class = second_class = None
    for report in result["orbits"]:
        mask_tuple = tuple(report["column_masks"])
        assert len(mask_tuple) == ORDER
        assert tuple(sorted(mask_tuple)) == mask_tuple
        key = tuple(sorted(mask_index[mask] for mask in mask_tuple))
        assert all(
            (adjacency[key[left]] >> key[right]) & 1
            for left in range(ORDER)
            for right in range(left)
        )
        matrix = representative_matrix(mask_tuple)
        assert gram_matrix(matrix) == base
        assert abs(bareiss_determinant(matrix)) == RECORD

        orbit_size, canonical, orbit = solution_orbit(key, actions, masks)
        assert orbit_size == report["orbit_size"]
        assert canonical == mask_tuple
        assert group_order // orbit_size == report["stabilizer_order"]
        assert (first_key in orbit) == report["contains_record23"]
        assert (second_key in orbit) == report["contains_record23_class2"]
        if first_key in orbit:
            first_class = report["class"]
        if second_key in orbit:
            second_class = report["class"]
        assert canonical not in canonical_representatives
        canonical_representatives.add(canonical)
        observed_sizes[orbit_size] += 1
        covered_count += orbit_size

    assert observed_sizes == Counter({18_432: 6, 55_296: 8})
    assert covered_count == clique_count
    assert len(canonical_representatives) == result["decomposition_classes"] == 14
    assert (first_class, second_class) == (14, 13)

    print("normalized sign-column and compatibility graph census verified")
    print("552960 exact 23-cliques independently enumerated")
    print("14 decomposition orbits cover every clique")
    print("orbit sizes: 6*18432 + 8*55296; stabilizers: 24 and 8")


if __name__ == "__main__":
    main()
