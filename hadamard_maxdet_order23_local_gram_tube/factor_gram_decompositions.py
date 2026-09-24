#!/usr/bin/env python3
"""Factor the record-Gram decomposition census through four column orbits."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path

import candidate_obstructions
import symmetry
from verify import gram_matrix, read_record
from verify_gram_decompositions import build_graph, candidate_actions


ORDER = 23
GROUP_ORDER = 442_368
DECOMPOSITION_CERTIFICATE_SHA256 = (
    "7b94f5918015a250db3619c7e1f2f37a8d31a3e2ad589afe21a99a30a445aa81"
)
EXPECTED_ORBIT_SIZES = [6, 512, 432, 432]
EXPECTED_QUOTIENT = [
    [2, 512, 216, 216],
    [6, 131, 216, 216],
    [3, 256, 73, 108],
    [3, 256, 108, 73],
]


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


def clique_enumeration(
    adjacency: list[int], target: int, retain: bool
) -> tuple[int, int, list[tuple[int, ...]]]:
    count = 0
    nodes = 0
    clique: list[int] = []
    solutions: list[tuple[int, ...]] = []

    def expand(candidates: int, size: int) -> None:
        nonlocal count, nodes
        nodes += 1
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
            if size + bounds[position] < target:
                return
            vertex = order[position]
            bit = 1 << vertex
            successor = candidates & adjacency[vertex]
            clique.append(vertex)
            if size + 1 == target:
                count += 1
                if retain:
                    solutions.append(tuple(sorted(clique)))
            elif size + 1 + successor.bit_count() >= target:
                expand(successor, size + 1)
            clique.pop()
            candidates ^= bit

    expand((1 << len(adjacency)) - 1, 0)
    return count, nodes, solutions


def mask_tuple(
    solution: tuple[int, ...], orbit: list[int], masks: list[int]
) -> tuple[int, ...]:
    return tuple(sorted(masks[orbit[index]] for index in solution))


def hash_tuples(tuples: list[tuple[int, ...]]) -> str:
    digest = hashlib.sha256()
    for item in sorted(tuples):
        digest.update((",".join(map(str, item)) + "\n").encode("ascii"))
    return digest.hexdigest()


def is_clique(vertices: int, adjacency: list[int]) -> bool:
    remaining = vertices
    while remaining:
        bit = remaining & -remaining
        vertex = bit.bit_length() - 1
        remaining ^= bit
        if remaining & ~adjacency[vertex]:
            return False
    return True


def are_cross_complete(left: int, right: int, adjacency: list[int]) -> bool:
    remaining = left
    while remaining:
        bit = remaining & -remaining
        vertex = bit.bit_length() - 1
        remaining ^= bit
        if right & ~adjacency[vertex]:
            return False
    return True


def solution_orbits(
    solutions: list[tuple[int, ...]],
    orbit: list[int],
    actions: list[tuple[int, ...]],
    masks: list[int],
) -> tuple[list[dict[str, object]], dict[tuple[int, ...], int]]:
    position = {vertex: index for index, vertex in enumerate(orbit)}
    local_actions = [
        tuple(position[action[vertex]] for vertex in orbit) for action in actions
    ]
    solution_set = set(solutions)
    unseen = set(solutions)
    raw_reports = []
    raw_labels: dict[tuple[int, ...], int] = {}
    while unseen:
        seed = min(unseen)
        current_orbit = {seed}
        queue = [seed]
        representative = mask_tuple(seed, orbit, masks)
        while queue:
            current = queue.pop()
            representative = min(
                representative, mask_tuple(current, orbit, masks)
            )
            for action in local_actions:
                image = tuple(sorted(action[index] for index in current))
                assert image in solution_set
                if image not in current_orbit:
                    current_orbit.add(image)
                    queue.append(image)
        unseen.difference_update(current_orbit)
        raw_label = len(raw_reports)
        for item in current_orbit:
            raw_labels[item] = raw_label
        raw_reports.append(
            {
                "orbit_size": len(current_orbit),
                "representative_masks": list(representative),
                "seed": seed,
            }
        )
    order = sorted(
        range(len(raw_reports)),
        key=lambda index: raw_reports[index]["representative_masks"],
    )
    renumber = {old: new + 1 for new, old in enumerate(order)}
    reports = []
    for old in order:
        report = dict(raw_reports[old])
        report["middle_orbit"] = renumber[old]
        report["stabilizer_order"] = GROUP_ORDER // report["orbit_size"]
        reports.append(report)
    labels = {solution: renumber[label] for solution, label in raw_labels.items()}
    return reports, labels


def oriented_orbit_size(
    seed: tuple[int, ...],
    triangle: tuple[int, ...],
    orbit: list[int],
    actions: list[tuple[int, ...]],
    triangles: list[tuple[int, ...]],
) -> int:
    position = {vertex: index for index, vertex in enumerate(orbit)}
    local_actions = [
        tuple(position[action[vertex]] for vertex in orbit) for action in actions
    ]
    triangle_index = {item: index for index, item in enumerate(triangles)}
    seed_state = (seed, triangle_index[triangle])
    seen = {seed_state}
    queue = [seed_state]
    while queue:
        current, triangle_label = queue.pop()
        for action, local_action in zip(actions, local_actions):
            image = tuple(sorted(local_action[index] for index in current))
            triangle_image = tuple(
                sorted(action[vertex] for vertex in triangles[triangle_label])
            )
            state = (image, triangle_index[triangle_image])
            if state not in seen:
                seen.add(state)
                queue.append(state)
    return len(seen)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(
            "usage: python3 factor_gram_decompositions.py DECOMPOSITIONS.json"
        )
    decomposition_path = Path(sys.argv[1])
    assert hashlib.sha256(
        decomposition_path.read_bytes()
    ).hexdigest() == DECOMPOSITION_CERTIFICATE_SHA256
    decomposition = json.loads(decomposition_path.read_text())

    base = gram_matrix(read_record())
    scale, numerator = candidate_obstructions.scaled_inverse(base)
    masks = candidate_obstructions.enumerate_normalized_columns(scale, numerator)
    vectors = [candidate_obstructions.vector_from_mask(mask) for mask in masks]
    adjacency, edge_count = build_graph(vectors, numerator)
    assert edge_count == 338_582
    _, _, first_generators, second_generators = symmetry.factor_groups()
    generators = [symmetry.lift_first(item) for item in first_generators] + [
        symmetry.lift_second(item) for item in second_generators
    ]
    actions = candidate_actions(masks, vectors, generators)
    orbits, labels = point_orbits(len(masks), actions, masks)
    assert [len(item) for item in orbits] == EXPECTED_ORBIT_SIZES

    quotient = []
    for label, orbit in enumerate(orbits):
        patterns = {
            tuple(
                sum((adjacency[vertex] >> neighbor) & 1 for neighbor in target)
                for target in orbits
            )
            for vertex in orbit
        }
        assert len(patterns) == 1
        quotient.append(list(patterns.pop()))
    assert quotient == EXPECTED_QUOTIENT

    induced = [induced_graph(orbit, adjacency) for orbit in orbits]
    maximum_targets = [3, 8, 6, 6]
    clique_reports = []
    retained: dict[int, list[tuple[int, ...]]] = {}
    for label, target in enumerate(maximum_targets):
        too_large, bound_nodes, _ = clique_enumeration(
            induced[label], target + 1, False
        )
        assert too_large == 0
        count, count_nodes, solutions = clique_enumeration(
            induced[label], target, label in (0, 1)
        )
        expected_count = [2, 276_480, 11_520, 11_520][label]
        assert count == expected_count
        if solutions:
            retained[label] = solutions
        clique_reports.append(
            {
                "point_orbit": label,
                "vertices": len(orbits[label]),
                "clique_number": target,
                "maximum_cliques": count,
                "upper_bound_nodes": bound_nodes,
                "enumeration_nodes": count_nodes,
            }
        )

    core_triangles = sorted(
        tuple(orbits[0][index] for index in solution)
        for solution in retained[0]
    )
    assert len(core_triangles) == 2
    middle_solutions = retained[1]
    assert len(middle_solutions) == 276_480
    middle_hash = hash_tuples(
        [mask_tuple(solution, orbits[1], masks) for solution in middle_solutions]
    )

    orbit_bits = [sum(1 << vertex for vertex in orbit) for orbit in orbits]
    allowed = []
    for triangle in core_triangles:
        by_side = []
        for side in (2, 3):
            candidates = orbit_bits[side]
            for vertex in triangle:
                candidates &= adjacency[vertex]
            assert candidates.bit_count() == 216
            by_side.append(candidates)
        allowed.append(by_side)

    full_digest = hashlib.sha256()
    completion_count = 0
    ordered_middle = sorted(
        middle_solutions,
        key=lambda solution: mask_tuple(solution, orbits[1], masks),
    )
    for triangle_index, triangle in enumerate(core_triangles):
        for middle in ordered_middle:
            global_middle = tuple(orbits[1][index] for index in middle)
            completions = []
            for side_index in range(2):
                common = allowed[triangle_index][side_index]
                for vertex in global_middle:
                    common &= adjacency[vertex]
                assert common.bit_count() == 6
                assert is_clique(common, adjacency)
                completions.append(common)
            assert are_cross_complete(completions[0], completions[1], adjacency)
            vertices = list(triangle) + list(global_middle)
            for completion in completions:
                while completion:
                    bit = completion & -completion
                    vertices.append(bit.bit_length() - 1)
                    completion ^= bit
            assert len(vertices) == ORDER
            full_masks = tuple(sorted(masks[vertex] for vertex in vertices))
            full_digest.update(
                (",".join(map(str, full_masks)) + "\n").encode("ascii")
            )
            completion_count += 1
    assert completion_count == 552_960

    middle_reports, middle_labels = solution_orbits(
        middle_solutions, orbits[1], actions, masks
    )
    assert len(middle_reports) == 10
    triangle_actions = {
        tuple(sorted(action[vertex] for vertex in triangle))
        for action in actions
        for triangle in core_triangles
    }
    assert triangle_actions == set(core_triangles)

    mask_index = {mask: index for index, mask in enumerate(masks)}
    point_position = {vertex: index for index, vertex in enumerate(orbits[1])}
    full_classes: dict[int, list[int]] = defaultdict(list)
    full_sizes = {}
    for report in decomposition["orbits"]:
        middle = tuple(
            sorted(
                point_position[mask_index[mask]]
                for mask in report["column_masks"]
                if labels[mask_index[mask]] == 1
            )
        )
        assert len(middle) == 8
        middle_label = middle_labels[middle]
        full_classes[middle_label].append(report["class"])
        full_sizes[report["class"]] = report["orbit_size"]

    merge_count = split_count = 0
    for report in middle_reports:
        middle_label = report["middle_orbit"]
        seed = report.pop("seed")
        oriented_size = oriented_orbit_size(
            seed, core_triangles[0], orbits[1], actions, core_triangles
        )
        swaps_core = oriented_size == 2 * report["orbit_size"]
        assert oriented_size in (report["orbit_size"], 2 * report["orbit_size"])
        classes = sorted(full_classes[middle_label])
        if swaps_core:
            merge_count += 1
            assert len(classes) == 1
            assert full_sizes[classes[0]] == 2 * report["orbit_size"]
        else:
            split_count += 1
            assert len(classes) == 2
            assert all(full_sizes[item] == report["orbit_size"] for item in classes)
        report["core_extensions_merge"] = swaps_core
        report["full_classes"] = classes
    assert (merge_count, split_count) == (6, 4)

    output = {
        "order": ORDER,
        "decomposition_certificate_sha256": DECOMPOSITION_CERTIFICATE_SHA256,
        "candidate_columns": len(masks),
        "candidate_orbit_sizes": EXPECTED_ORBIT_SIZES,
        "equitable_quotient": quotient,
        "induced_clique_census": clique_reports,
        "core_triangle_masks": [
            [masks[vertex] for vertex in triangle] for triangle in core_triangles
        ],
        "middle_clique_sha256": middle_hash,
        "middle_clique_orbits": middle_reports,
        "unique_extensions_per_middle_clique": 2,
        "factorized_full_cliques": completion_count,
        "full_clique_stream_sha256": full_digest.hexdigest(),
        "merged_middle_orbits": merge_count,
        "split_middle_orbits": split_count,
        "decomposition_classes": merge_count + 2 * split_count,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
