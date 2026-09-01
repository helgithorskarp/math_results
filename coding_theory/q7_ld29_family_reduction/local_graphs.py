"""Canonical orphan-local graph branches for the Q_7 size-29 search."""

from __future__ import annotations

import itertools


DIMENSION = 7


def local_graph_representatives() -> list[int]:
    """Return the canonical allowed graphs on coordinates 1,...,6."""
    coordinates = range(1, DIMENSION)
    edges = list(itertools.combinations(coordinates, 2))
    edge_index = {edge: index for index, edge in enumerate(edges)}
    permutation_maps: list[list[int]] = []
    for image_tuple in itertools.permutations(coordinates):
        image = dict(zip(coordinates, image_tuple, strict=True))
        permutation_maps.append(
            [
                edge_index[tuple(sorted((image[first], image[second])))]
                for first, second in edges
            ]
        )

    def transform(mask: int, edge_map: list[int]) -> int:
        result = 0
        for source, destination in enumerate(edge_map):
            if (mask >> source) & 1:
                result |= 1 << destination
        return result

    def admissible(mask: int) -> bool:
        adjacency = {coordinate: set() for coordinate in coordinates}
        for index, (first, second) in enumerate(edges):
            if (mask >> index) & 1:
                adjacency[first].add(second)
                adjacency[second].add(first)
        if any(not neighbors for neighbors in adjacency.values()):
            return False
        for vertex, neighbors in adjacency.items():
            if len(neighbors) == 1:
                (neighbor,) = neighbors
                if adjacency[neighbor] == {vertex}:
                    return False
        return True

    seen: set[int] = set()
    representatives: list[int] = []
    for mask in range(1 << len(edges)):
        if mask in seen or not admissible(mask):
            continue
        orbit = {transform(mask, edge_map) for edge_map in permutation_maps}
        seen.update(orbit)
        representatives.append(min(orbit))
    return sorted(representatives, key=lambda mask: (mask.bit_count(), mask))


def local_graph_assumptions(mask: int) -> list[int]:
    """Fix all weight-two variables not containing the orphan coordinate."""
    assumptions = []
    for index, (first, second) in enumerate(
        itertools.combinations(range(1, DIMENSION), 2)
    ):
        variable = (1 << first) | (1 << second)
        literal = variable + 1
        assumptions.append(literal if (mask >> index) & 1 else -literal)
    return assumptions
