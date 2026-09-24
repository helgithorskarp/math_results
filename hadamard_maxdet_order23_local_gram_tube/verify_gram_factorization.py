#!/usr/bin/env python3
"""Independent orbit-and-anchor checker for the factored decomposition census."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

import candidate_obstructions
import symmetry
from verify import gram_matrix, read_record


ORDER = 23
GROUP_ORDER = 442_368
DECOMPOSITION_CERTIFICATE_SHA256 = (
    "7b94f5918015a250db3619c7e1f2f37a8d31a3e2ad589afe21a99a30a445aa81"
)


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
    edges = 0
    for left in range(len(vectors)):
        for right in range(left):
            product = sum(
                vectors[left][coordinate] * transformed[right][coordinate]
                for coordinate in range(ORDER)
            )
            if product == 0:
                adjacency[left] |= 1 << right
                adjacency[right] |= 1 << left
                edges += 1
    return adjacency, edges


def vector_mask(vector: list[int]) -> int:
    if vector[0] < 0:
        vector = [-entry for entry in vector]
    return sum(
        (vector[coordinate] < 0) << (coordinate - 1)
        for coordinate in range(1, ORDER)
    )


def candidate_actions(
    masks: list[int],
    vectors: list[list[int]],
    generators: list[tuple[int, ...]],
) -> list[tuple[int, ...]]:
    mask_index = {mask: index for index, mask in enumerate(masks)}
    actions = []
    for generator in generators:
        action = []
        for vector in vectors:
            image = [0] * ORDER
            for coordinate in range(ORDER):
                image[generator[coordinate]] = vector[coordinate]
            action.append(mask_index[vector_mask(image)])
        actions.append(tuple(action))
    return actions


def point_orbits(
    size: int, actions: list[tuple[int, ...]], masks: list[int]
) -> tuple[list[list[int]], list[int]]:
    unseen = set(range(size))
    orbits = []
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
        orbits.append(sorted(orbit))
    rank = {6: 0, 512: 1, 432: 2}
    orbits.sort(key=lambda item: (rank[len(item)], min(masks[index] for index in item)))
    labels = [-1] * size
    for label, orbit in enumerate(orbits):
        for vertex in orbit:
            labels[vertex] = label
    return orbits, labels


def induced_graph(orbit: list[int], adjacency: list[int]) -> list[int]:
    position = {vertex: index for index, vertex in enumerate(orbit)}
    return [
        sum(
            1 << position[neighbor]
            for neighbor in orbit
            if (adjacency[vertex] >> neighbor) & 1
        )
        for vertex in orbit
    ]


def count_cliques(candidates: int, size: int, adjacency: list[int]) -> int:
    if size == 0:
        return 1
    if candidates.bit_count() < size:
        return 0
    answer = 0
    while candidates:
        bit = candidates & -candidates
        vertex = bit.bit_length() - 1
        candidates ^= bit
        answer += count_cliques(candidates & adjacency[vertex], size - 1, adjacency)
    return answer


def is_clique(vertices: tuple[int, ...], adjacency: list[int]) -> bool:
    return all(
        (adjacency[vertices[left]] >> vertices[right]) & 1
        for left in range(len(vertices))
        for right in range(left)
    )


def bitset_is_clique(vertices: int, adjacency: list[int]) -> bool:
    remaining = vertices
    while remaining:
        bit = remaining & -remaining
        vertex = bit.bit_length() - 1
        remaining ^= bit
        if remaining & ~adjacency[vertex]:
            return False
    return True


def cross_complete(left: int, right: int, adjacency: list[int]) -> bool:
    remaining = left
    while remaining:
        bit = remaining & -remaining
        vertex = bit.bit_length() - 1
        remaining ^= bit
        if right & ~adjacency[vertex]:
            return False
    return True


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(
            "usage: python3 verify_gram_factorization.py "
            "DECOMPOSITIONS.json FACTORIZATION.json"
        )
    decomposition_path = Path(sys.argv[1])
    factorization_path = Path(sys.argv[2])
    assert hashlib.sha256(
        decomposition_path.read_bytes()
    ).hexdigest() == DECOMPOSITION_CERTIFICATE_SHA256
    decomposition = json.loads(decomposition_path.read_text())
    certificate = json.loads(factorization_path.read_text())
    assert certificate["decomposition_certificate_sha256"] == DECOMPOSITION_CERTIFICATE_SHA256

    base = gram_matrix(read_record())
    scale, numerator = candidate_obstructions.scaled_inverse(base)
    masks = candidate_obstructions.enumerate_normalized_columns(scale, numerator)
    vectors = [candidate_obstructions.vector_from_mask(mask) for mask in masks]
    adjacency, edges = build_graph(vectors, numerator)
    assert edges == 338_582 and len(masks) == certificate["candidate_columns"] == 1_382
    _, _, first_generators, second_generators = symmetry.factor_groups()
    generators = [symmetry.lift_first(item) for item in first_generators] + [
        symmetry.lift_second(item) for item in second_generators
    ]
    actions = candidate_actions(masks, vectors, generators)
    orbits, labels = point_orbits(len(masks), actions, masks)
    assert [len(item) for item in orbits] == certificate["candidate_orbit_sizes"]

    quotient = []
    for orbit in orbits:
        patterns = {
            tuple(
                sum((adjacency[vertex] >> neighbor) & 1 for neighbor in target)
                for target in orbits
            )
            for vertex in orbit
        }
        assert len(patterns) == 1
        quotient.append(list(patterns.pop()))
    assert quotient == certificate["equitable_quotient"]

    induced = [induced_graph(orbit, adjacency) for orbit in orbits]
    for report in certificate["induced_clique_census"]:
        label = report["point_orbit"]
        clique_number = report["clique_number"]
        graph = induced[label]
        anchored_maximum = count_cliques(
            graph[0], clique_number - 1, graph
        )
        anchored_too_large = count_cliques(graph[0], clique_number, graph)
        assert anchored_too_large == 0
        total = len(graph) * anchored_maximum // clique_number
        assert total == report["maximum_cliques"]

    core = certificate["core_triangle_masks"]
    mask_index = {mask: index for index, mask in enumerate(masks)}
    core_triangles = [tuple(mask_index[mask] for mask in item) for item in core]
    assert len(core_triangles) == 2
    assert all(is_clique(item, adjacency) for item in core_triangles)
    assert set(sum((list(item) for item in core_triangles), [])) == set(orbits[0])

    middle = orbits[1]
    middle_position = {vertex: index for index, vertex in enumerate(middle)}
    local_actions = [
        tuple(middle_position[action[vertex]] for vertex in middle)
        for action in actions
    ]
    all_middle: set[tuple[int, ...]] = set()
    middle_labels: dict[tuple[int, ...], int] = {}
    triangle_index = {item: index for index, item in enumerate(core_triangles)}
    allowed = []
    for triangle in core_triangles:
        sides = []
        for point_orbit in (2, 3):
            candidates = sum(1 << vertex for vertex in orbits[point_orbit])
            for vertex in triangle:
                candidates &= adjacency[vertex]
            assert candidates.bit_count() == 216
            sides.append(candidates)
        allowed.append(sides)

    class_groups: dict[int, list[int]] = defaultdict(list)
    for report in certificate["middle_clique_orbits"]:
        label = report["middle_orbit"]
        seed = tuple(
            sorted(middle_position[mask_index[mask]] for mask in report["representative_masks"])
        )
        assert len(seed) == 8
        assert is_clique(tuple(middle[index] for index in seed), adjacency)
        orbit = {seed}
        queue = [seed]
        while queue:
            current = queue.pop()
            for action in local_actions:
                image = tuple(sorted(action[index] for index in current))
                assert is_clique(tuple(middle[index] for index in image), adjacency)
                if image not in orbit:
                    orbit.add(image)
                    queue.append(image)
        assert len(orbit) == report["orbit_size"]
        assert GROUP_ORDER // len(orbit) == report["stabilizer_order"]
        assert all_middle.isdisjoint(orbit)
        all_middle.update(orbit)
        for item in orbit:
            middle_labels[item] = label

        oriented = {(seed, 0)}
        queue_oriented = [(seed, 0)]
        while queue_oriented:
            current, core_label = queue_oriented.pop()
            for action, local_action in zip(actions, local_actions):
                image = tuple(sorted(local_action[index] for index in current))
                triangle_image = tuple(
                    sorted(action[vertex] for vertex in core_triangles[core_label])
                )
                state = (image, triangle_index[triangle_image])
                if state not in oriented:
                    oriented.add(state)
                    queue_oriented.append(state)
        merges = len(oriented) == 2 * len(orbit)
        assert len(oriented) in (len(orbit), 2 * len(orbit))
        assert merges == report["core_extensions_merge"]

        global_seed = tuple(middle[index] for index in seed)
        for core_label in range(2):
            completion = []
            for side in range(2):
                common = allowed[core_label][side]
                for vertex in global_seed:
                    common &= adjacency[vertex]
                assert common.bit_count() == 6
                assert bitset_is_clique(common, adjacency)
                completion.append(common)
            assert cross_complete(completion[0], completion[1], adjacency)

    expected_middle = certificate["induced_clique_census"][1]["maximum_cliques"]
    assert len(all_middle) == expected_middle == 276_480
    middle_digest = hashlib.sha256()
    for item in sorted(
        tuple(sorted(masks[middle[index]] for index in clique))
        for clique in all_middle
    ):
        middle_digest.update((",".join(map(str, item)) + "\n").encode("ascii"))
    assert middle_digest.hexdigest() == certificate["middle_clique_sha256"]

    full_digest = hashlib.sha256()
    full_count = 0
    ordered_middle = sorted(
        all_middle,
        key=lambda item: tuple(sorted(masks[middle[index]] for index in item)),
    )
    for core_label, triangle in enumerate(core_triangles):
        for clique in ordered_middle:
            global_middle = tuple(middle[index] for index in clique)
            vertices = list(triangle) + list(global_middle)
            for side in range(2):
                common = allowed[core_label][side]
                for vertex in global_middle:
                    common &= adjacency[vertex]
                while common:
                    bit = common & -common
                    vertices.append(bit.bit_length() - 1)
                    common ^= bit
            assert len(vertices) == ORDER
            encoded = tuple(sorted(masks[vertex] for vertex in vertices))
            full_digest.update((",".join(map(str, encoded)) + "\n").encode("ascii"))
            full_count += 1
    assert full_count == certificate["factorized_full_cliques"] == 552_960
    assert full_digest.hexdigest() == certificate["full_clique_stream_sha256"]

    full_sizes = {}
    for report in decomposition["orbits"]:
        clique = tuple(
            sorted(
                middle_position[mask_index[mask]]
                for mask in report["column_masks"]
                if labels[mask_index[mask]] == 1
            )
        )
        label = middle_labels[clique]
        class_groups[label].append(report["class"])
        full_sizes[report["class"]] = report["orbit_size"]
    merges = splits = 0
    for report in certificate["middle_clique_orbits"]:
        classes = sorted(class_groups[report["middle_orbit"]])
        assert classes == report["full_classes"]
        if report["core_extensions_merge"]:
            merges += 1
            assert len(classes) == 1
            assert full_sizes[classes[0]] == 2 * report["orbit_size"]
        else:
            splits += 1
            assert len(classes) == 2
            assert all(full_sizes[item] == report["orbit_size"] for item in classes)
    assert (merges, splits) == (
        certificate["merged_middle_orbits"],
        certificate["split_middle_orbits"],
    ) == (6, 4)
    assert merges + 2 * splits == certificate["decomposition_classes"] == 14

    print("candidate compatibility graph factors into clique numbers 3+8+6+6")
    print("276480 middle 8-cliques independently counted by vertex anchoring")
    print("each middle clique has one completion over each of two core triangles")
    print("six merged and four split middle orbits give exactly fourteen classes")


if __name__ == "__main__":
    main()
