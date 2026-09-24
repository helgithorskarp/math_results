#!/usr/bin/env python3
"""Exact symmetry and Burnside certificate for the order-23 Gram tube."""

from __future__ import annotations

import itertools
import json
import math
import sys
from collections import Counter
from pathlib import Path

from verify import bareiss_determinant, gram_matrix, read_record


HERE = Path(__file__).resolve().parent
CORE = (0, 1, 2)
BLOCKS = {
    0: ((7, 8), (9, 10)),
    1: ((3, 4), (5, 6)),
    2: ((11, 12), (13, 14)),
}


def graph_components(gram: list[list[int]]) -> list[frozenset[int]]:
    unseen = set(range(len(gram)))
    components = []
    while unseen:
        start = min(unseen)
        component = {start}
        stack = [start]
        while stack:
            vertex = stack.pop()
            for other in tuple(unseen):
                if other != vertex and gram[vertex][other] == 3:
                    unseen.remove(other)
                    component.add(other)
                    stack.append(other)
        unseen.discard(start)
        components.append(frozenset(component))
    return sorted(components, key=lambda component: (len(component), min(component)))


def verify_graph_structure(gram: list[list[int]]) -> None:
    expected_components = {
        frozenset(range(15)),
        frozenset(range(15, 19)),
        frozenset(range(19, 23)),
    }
    assert set(graph_components(gram)) == expected_components
    degrees = [sum(entry == 3 for entry in row) for row in gram]
    assert tuple(vertex for vertex in range(15) if degrees[vertex] == 6) == CORE
    for missing_core, (inactive, active) in BLOCKS.items():
        block = inactive + active
        assert all(
            gram[left][right] == 3
            for left, right in itertools.combinations(block, 2)
        )
        for vertex in inactive:
            assert degrees[vertex] == 3
            assert all(gram[vertex][core] == -1 for core in CORE)
        for vertex in active:
            assert degrees[vertex] == 5
            assert {
                core for core in CORE if gram[vertex][core] == 3
            } == set(CORE) - {missing_core}
    for component in (range(15, 19), range(19, 23)):
        assert all(
            gram[left][right] == 3
            for left, right in itertools.combinations(component, 2)
        )
    assert all(
        gram[left][right] == -1
        for left in range(15)
        for right in range(15, 23)
    )


def first_factor_permutation(
    core_image: tuple[int, int, int], twin_mask: int
) -> tuple[int, ...]:
    """An element of C2^6 semidirect S3 on vertices 0,...,14."""
    permutation = list(range(15))
    for core in CORE:
        permutation[core] = core_image[core]
    for missing_core in CORE:
        target = core_image[missing_core]
        for kind in range(2):
            swap = (twin_mask >> (2 * missing_core + kind)) & 1
            for position in range(2):
                source_vertex = BLOCKS[missing_core][kind][position]
                permutation[source_vertex] = BLOCKS[target][kind][position ^ swap]
    return tuple(permutation)


def second_factor_permutation(
    first_image: tuple[int, int, int, int],
    second_image: tuple[int, int, int, int],
    swap_components: int,
) -> tuple[int, ...]:
    """An element of S4 wreath C2 on local vertices 0,...,7."""
    permutation = list(range(8))
    for position in range(4):
        permutation[position] = 4 * swap_components + first_image[position]
        permutation[4 + position] = 4 * (1 - swap_components) + second_image[position]
    return tuple(permutation)


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(len(left)))


def generated_group(
    generators: list[tuple[int, ...]], degree: int
) -> set[tuple[int, ...]]:
    identity = tuple(range(degree))
    group = {identity}
    frontier = [identity]
    while frontier:
        element = frontier.pop()
        for generator in generators:
            product = compose(generator, element)
            if product not in group:
                group.add(product)
                frontier.append(product)
    return group


def factor_groups() -> tuple[
    set[tuple[int, ...]],
    set[tuple[int, ...]],
    list[tuple[int, ...]],
    list[tuple[int, ...]],
]:
    first = {
        first_factor_permutation(core_image, mask)
        for core_image in itertools.permutations(CORE)
        for mask in range(64)
    }
    permutations4 = tuple(itertools.permutations(range(4)))
    second = {
        second_factor_permutation(left, right, swap)
        for left in permutations4
        for right in permutations4
        for swap in range(2)
    }
    first_generators = [
        first_factor_permutation(CORE, 1 << bit) for bit in range(6)
    ] + [
        first_factor_permutation((1, 0, 2), 0),
        first_factor_permutation((0, 2, 1), 0),
    ]
    identity4 = (0, 1, 2, 3)
    transposition4 = (1, 0, 2, 3)
    cycle4 = (1, 2, 3, 0)
    second_generators = [
        second_factor_permutation(transposition4, identity4, 0),
        second_factor_permutation(cycle4, identity4, 0),
        second_factor_permutation(identity4, transposition4, 0),
        second_factor_permutation(identity4, cycle4, 0),
        second_factor_permutation(identity4, identity4, 1),
    ]
    assert len(first) == 384
    assert len(second) == 1152
    assert generated_group(first_generators, 15) == first
    assert generated_group(second_generators, 8) == second
    return first, second, first_generators, second_generators


def cycle_lengths(permutation: tuple[int, ...]) -> tuple[int, ...]:
    unseen = set(range(len(permutation)))
    lengths = []
    while unseen:
        start = min(unseen)
        vertex = start
        length = 0
        while vertex in unseen:
            unseen.remove(vertex)
            length += 1
            vertex = permutation[vertex]
        assert vertex == start
        lengths.append(length)
    return tuple(sorted(lengths))


def pair_cycle_lengths(permutation: tuple[int, ...]) -> tuple[int, ...]:
    pairs = tuple(itertools.combinations(range(len(permutation)), 2))
    pair_index = {pair: index for index, pair in enumerate(pairs)}
    pair_image = tuple(
        pair_index[tuple(sorted((permutation[left], permutation[right])))]
        for left, right in pairs
    )
    return cycle_lengths(pair_image)


def action_types(
    group: set[tuple[int, ...]],
) -> Counter[tuple[tuple[int, ...], tuple[int, ...]]]:
    return Counter(
        (cycle_lengths(permutation), pair_cycle_lengths(permutation))
        for permutation in group
    )


def combined_pair_cycles(
    first_type: tuple[tuple[int, ...], tuple[int, ...]],
    second_type: tuple[tuple[int, ...], tuple[int, ...]],
) -> tuple[int, ...]:
    first_vertices, first_pairs = first_type
    second_vertices, second_pairs = second_type
    cross_cycles = []
    for left_length in first_vertices:
        for right_length in second_vertices:
            cross_cycles.extend(
                [math.lcm(left_length, right_length)]
                * math.gcd(left_length, right_length)
            )
    cycles = first_pairs + second_pairs + tuple(cross_cycles)
    assert sum(cycles) == math.comb(23, 2)
    return tuple(sorted(cycles))


def full_pair_action_types(
    first_types: Counter[tuple[tuple[int, ...], tuple[int, ...]]],
    second_types: Counter[tuple[tuple[int, ...], tuple[int, ...]]],
) -> Counter[tuple[int, ...]]:
    answer: Counter[tuple[int, ...]] = Counter()
    for first_type, first_multiplicity in first_types.items():
        for second_type, second_multiplicity in second_types.items():
            answer[combined_pair_cycles(first_type, second_type)] += (
                first_multiplicity * second_multiplicity
            )
    return answer


def fixed_subset_counts(cycles: tuple[int, ...], maximum: int) -> list[int]:
    coefficients = [1] + [0] * maximum
    for length in cycles:
        for degree in range(maximum, length - 1, -1):
            coefficients[degree] += coefficients[degree - length]
    return coefficients


def burnside_counts(
    action_types_by_multiplicity: Counter[tuple[int, ...]], maximum: int
) -> list[int]:
    group_order = sum(action_types_by_multiplicity.values())
    totals = [0] * (maximum + 1)
    for cycles, multiplicity in action_types_by_multiplicity.items():
        fixed = fixed_subset_counts(cycles, maximum)
        for size in range(maximum + 1):
            totals[size] += multiplicity * fixed[size]
    assert all(total % group_order == 0 for total in totals)
    return [total // group_order for total in totals]


def lift_first(permutation: tuple[int, ...]) -> tuple[int, ...]:
    return permutation + tuple(range(15, 23))


def lift_second(permutation: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(range(15)) + tuple(15 + image for image in permutation)


def edge_image(
    edge_set: frozenset[int],
    permutation: tuple[int, ...],
    edges: tuple[tuple[int, int], ...],
    edge_index: dict[tuple[int, int], int],
) -> frozenset[int]:
    return frozenset(
        edge_index[
            tuple(sorted((permutation[edges[index][0]], permutation[edges[index][1]])))
        ]
        for index in edge_set
    )


def direct_small_orbit_count(
    subset_size: int, generators: list[tuple[int, ...]]
) -> int:
    """Independent generator traversal for the small Burnside cases."""
    edges = tuple((i, j) for i in range(23) for j in range(i))
    edge_index = {tuple(sorted(pair)): index for index, pair in enumerate(edges)}
    edge_images = [
        tuple(
            edge_index[
                tuple(sorted((permutation[left], permutation[right])))
            ]
            for left, right in edges
        )
        for permutation in generators
    ]
    unseen = set(itertools.combinations(range(len(edges)), subset_size))
    orbit_count = 0
    while unseen:
        seed = min(unseen)
        unseen.remove(seed)
        frontier = [seed]
        orbit_count += 1
        while frontier:
            current = frontier.pop()
            for image in edge_images:
                successor = tuple(sorted(image[index] for index in current))
                if successor in unseen:
                    unseen.remove(successor)
                    frontier.append(successor)
    return orbit_count


def survivor_orbits(
    result: dict,
    gram: list[list[int]],
    generators: list[tuple[int, ...]],
) -> list[dict]:
    graph_four = result["cases"]["graph_four_edits"]
    assert graph_four["total"] == math.comb(253, 4)
    assert graph_four["survives_48_nonsquare_tests"] == 372
    edges = tuple((i, j) for i in range(23) for j in range(i))
    edge_index = {tuple(sorted(pair)): index for index, pair in enumerate(edges)}
    survivor_sets = set()
    for edits in graph_four["survivor_edits"]:
        assert len(edits) == 4
        edge_set = frozenset(int(index) for index, _ in edits)
        assert len(edge_set) == 4
        for index, new_value in edits:
            left, right = edges[int(index)]
            assert int(new_value) == 2 - gram[left][right]
        survivor_sets.add(edge_set)
    assert len(survivor_sets) == 372

    unseen = set(survivor_sets)
    reports = []
    while unseen:
        seed = min(unseen, key=lambda item: tuple(sorted(item)))
        orbit = {seed}
        frontier = [seed]
        while frontier:
            current = frontier.pop()
            for generator in generators:
                image = edge_image(current, generator, edges, edge_index)
                assert image in survivor_sets
                if image not in orbit:
                    orbit.add(image)
                    frontier.append(image)
        unseen.difference_update(orbit)
        representative = min(tuple(sorted(item)) for item in orbit)
        modified = [row[:] for row in gram]
        representative_edges = []
        for index in representative:
            left, right = edges[index]
            new_value = 2 - gram[left][right]
            modified[left][right] = modified[right][left] = new_value
            representative_edges.append([left, right, new_value])
        determinant = bareiss_determinant(modified)
        root = math.isqrt(determinant)
        assert root * root == determinant
        reports.append(
            {
                "square_root": root,
                "determinant": determinant,
                "orbit_size": len(orbit),
                "representative_edge_indices": list(representative),
                "representative_edges": representative_edges,
            }
        )
    assert sum(report["orbit_size"] for report in reports) == 372
    return sorted(
        reports,
        key=lambda report: (
            -report["square_root"],
            report["orbit_size"],
            report["representative_edge_indices"],
        ),
    )


def calculate(result: dict) -> dict:
    gram = gram_matrix(read_record())
    verify_graph_structure(gram)
    first, second, first_generators, second_generators = factor_groups()
    assert all(
        gram[permutation[i]][permutation[j]] == gram[i][j]
        for permutation in first
        for i in range(15)
        for j in range(15)
    )
    assert all(
        gram[15 + permutation[i]][15 + permutation[j]] == gram[15 + i][15 + j]
        for permutation in second
        for i in range(8)
        for j in range(8)
    )
    first_types = action_types(first)
    second_types = action_types(second)
    full_types = full_pair_action_types(first_types, second_types)
    assert sum(full_types.values()) == len(first) * len(second)
    generators = [lift_first(item) for item in first_generators] + [
        lift_second(item) for item in second_generators
    ]
    assert all(
        gram[permutation[i]][permutation[j]] == gram[i][j]
        for permutation in generators
        for i in range(23)
        for j in range(23)
    )
    orbit_counts = burnside_counts(full_types, 12)
    assert direct_small_orbit_count(1, generators) == orbit_counts[1]
    assert direct_small_orbit_count(2, generators) == orbit_counts[2]
    return {
        "automorphism_group": {
            "structure": "(C2^6 semidirect S3) times (S4 wreath C2)",
            "order": len(first) * len(second),
            "first_factor_order": len(first),
            "second_factor_order": len(second),
            "generator_count": len(generators),
            "first_factor_action_types": len(first_types),
            "second_factor_action_types": len(second_types),
            "unordered_pair_action_types": len(full_types),
        },
        "toggle_subset_orbits": {
            str(size): count
            for size, count in enumerate(orbit_counts)
        },
        "radius_four_square_survivor_orbits": survivor_orbits(
            result, gram, generators
        ),
    }


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python3 symmetry.py RESULT.json")
    result = json.loads(Path(sys.argv[1]).read_text())
    observed = calculate(result)
    expected = json.loads((HERE / "symmetry_certificate.json").read_text())
    assert observed == expected
    print(json.dumps(observed, indent=2))
    print("exact Gram-graph symmetry and orbit certificate verified")


if __name__ == "__main__":
    main()
