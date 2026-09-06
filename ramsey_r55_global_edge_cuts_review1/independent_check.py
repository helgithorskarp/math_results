#!/usr/bin/env python3
"""Clean-room audit of the global R55 edge-cut theorem.

No target code, certificate, expected output, or graph fixture is imported.
The established bound R(4,5)=25 is kept as an explicit mathematical input.
"""

from functools import lru_cache
from itertools import combinations
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


@lru_cache(maxsize=None)
def complete_multipartite_capacity(vertices, parts):
    """Maximum edge count of a complete graph with at most `parts` parts."""
    if vertices <= 1 or parts <= 1:
        return 0
    return max(
        first * (vertices - first)
        + complete_multipartite_capacity(vertices - first, parts - 1)
        for first in range(vertices + 1)
    )


def theorem_audit(*, order=43, minimum_degree=18, maximum_degree=24,
                  clique_number=4, smaller_side_max=21):
    require(smaller_side_max == order // 2, "Not every bipartition size is covered")
    require(minimum_degree + maximum_degree == order - 1,
            "The complementary degree window is inconsistent")

    capacities = [
        complete_multipartite_capacity(size, clique_number)
        for size in range(1, smaller_side_max + 1)
    ]
    cut_lower = [
        minimum_degree * size - 2 * capacities[size - 1]
        for size in range(1, smaller_side_max + 1)
    ]

    # Motzkin--Straus/Turan bounds a K_{clique_number+1}-free induced
    # subgraph by the corresponding complete multipartite capacity.
    require(cut_lower[0] == 18, "Singleton boundary")
    require(min(cut_lower[1:]) == 34, "Two-or-more-side cut gap")
    require(min(cut_lower[2:]) == 48, "Three-or-more-side cut gap")

    vertex_cut_candidate_upper = maximum_degree
    edge_cut_candidate_lower = 2 * minimum_degree - 2
    edge_cut_candidate_upper = 2 * maximum_degree - 2
    require(vertex_cut_candidate_upper < min(cut_lower[1:]),
            "The ordinary-cut minimizer gap is not strict")
    require(edge_cut_candidate_upper < min(cut_lower[2:]),
            "The restricted-cut minimizer gap is not strict")
    require(edge_cut_candidate_lower == 34 and edge_cut_candidate_upper == 46,
            "The edge-boundary range changed")

    # Applying the same lower bound to the complementary color supplies the
    # upper half of every two-color cut interval.
    for size, lower in enumerate(cut_lower, start=1):
        cross_pairs = size * (order - size)
        require(lower <= cross_pairs - lower,
                "The two color cut bounds are mutually inconsistent")

    return {
        "order": order,
        "imported_ramsey_4_5_upper": 25,
        "degree_window": [minimum_degree, maximum_degree],
        "turan_capacities_sizes_1_to_21": capacities,
        "cut_lower_bounds_sizes_1_to_21": cut_lower,
        "minimum_cut_with_sides_at_least_2": min(cut_lower[1:]),
        "minimum_cut_with_sides_at_least_3": min(cut_lower[2:]),
        "ordinary_candidate_upper": vertex_cut_candidate_upper,
        "restricted_candidate_range": [
            edge_cut_candidate_lower,
            edge_cut_candidate_upper,
        ],
        "ordinary_strict_gap": True,
        "restricted_strict_gap": True,
        "all_minimum_ordinary_cuts_isolate_minimum_degree_vertices": True,
        "all_minimum_restricted_cuts_isolate_minimum_edge_degree_edges": True,
        "both_colors_covered": True,
    }


def graph_data(order, graph_word):
    pairs = list(combinations(range(order), 2))
    adjacency = [0] * order
    for index, (left, right) in enumerate(pairs):
        if graph_word >> index & 1:
            adjacency[left] |= 1 << right
            adjacency[right] |= 1 << left
    return pairs, adjacency


def connected(adjacency):
    order = len(adjacency)
    reached = 1
    frontier = 1
    while frontier:
        vertex_bit = frontier & -frontier
        frontier ^= vertex_bit
        vertex = vertex_bit.bit_length() - 1
        fresh = adjacency[vertex] & ~reached
        reached |= fresh
        frontier |= fresh
    return reached == (1 << order) - 1


def boundary_word(pairs, graph_word, side):
    answer = 0
    for index, (left, right) in enumerate(pairs):
        if graph_word >> index & 1 and ((side >> left) ^ (side >> right)) & 1:
            answer |= 1 << index
    return answer


def has_no_isolates_on_either_side(adjacency, side):
    full = (1 << len(adjacency)) - 1
    other = full ^ side
    for vertex, neighbors in enumerate(adjacency):
        own_side = side if side >> vertex & 1 else other
        if not neighbors & own_side:
            return False
    return True


def minimum_words(words):
    require(words, "No candidate cut")
    size = min(word.bit_count() for word in words)
    return {word for word in words if word.bit_count() == size}


def gap_lemma_controls():
    """Definition-level check of both strict-gap minimizer lemmas."""
    total_graphs = connected_graphs = 0
    ordinary_instances = restricted_instances = 0
    cut_partitions = 0
    for order in range(2, 7):
        edge_count = order * (order - 1) // 2
        full = (1 << order) - 1
        for graph_word in range(1 << edge_count):
            total_graphs += 1
            pairs, adjacency = graph_data(order, graph_word)
            if not connected(adjacency):
                continue
            connected_graphs += 1
            degrees = [neighbors.bit_count() for neighbors in adjacency]
            ordinary = set()
            restricted = set()
            large_two = []
            large_three = []
            for remainder in range(1 << (order - 1)):
                side = 1 | remainder << 1
                if side == full:
                    continue
                boundary = boundary_word(pairs, graph_word, side)
                ordinary.add(boundary)
                smaller = min(side.bit_count(), order - side.bit_count())
                if smaller >= 2:
                    large_two.append(boundary.bit_count())
                if smaller >= 3:
                    large_three.append(boundary.bit_count())
                if has_no_isolates_on_either_side(adjacency, side):
                    restricted.add(boundary)
                cut_partitions += 1

            delta = min(degrees)
            larger_cut_minimum = min(large_two) if large_two else edge_count + 1
            if delta < larger_cut_minimum:
                expected = {
                    boundary_word(pairs, graph_word, 1 << vertex)
                    for vertex, degree in enumerate(degrees) if degree == delta
                }
                require(minimum_words(ordinary) == expected,
                        "Ordinary strict-gap classification failed")
                ordinary_instances += 1

            if delta < 3:
                continue
            edge_boundaries = {
                boundary_word(pairs, graph_word, (1 << left) | (1 << right))
                for index, (left, right) in enumerate(pairs)
                if graph_word >> index & 1
            }
            for edge_boundary in edge_boundaries:
                require(edge_boundary in restricted,
                        "Minimum degree three did not protect an edge cut")
            edge_minimum = min(word.bit_count() for word in edge_boundaries)
            large_cut_minimum = min(large_three) if large_three else edge_count + 1
            if edge_minimum < large_cut_minimum:
                require(minimum_words(restricted) == minimum_words(edge_boundaries),
                        "Restricted strict-gap classification failed")
                restricted_instances += 1

    return {
        "simple_graphs_orders_2_to_6": total_graphs,
        "connected_graphs_orders_2_to_6": connected_graphs,
        "bipartition_controls": cut_partitions,
        "ordinary_strict_gap_instances": ordinary_instances,
        "restricted_strict_gap_instances": restricted_instances,
    }


def main():
    result = theorem_audit()
    mutations = {
        "weaker_degree_window": {"minimum_degree": 17, "maximum_degree": 25},
        "inconsistent_maximum_degree_25": {"maximum_degree": 25},
        "K6_free_only": {"clique_number": 5},
        "missing_balanced_side": {"smaller_side_max": 20},
    }
    rejected = []
    for name, changes in mutations.items():
        try:
            theorem_audit(**changes)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError("Unsound theorem mutation accepted: " + name)
    result.update(gap_lemma_controls())
    result.update({
        "status": "INDEPENDENTLY_VERIFIED_R55_GLOBAL_EDGE_CUTS",
        "scope_mutations_rejected": rejected,
        "target_code_imported": False,
        "target_certificate_imported": False,
        "formal_proof_assistant_check": False,
    })
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
