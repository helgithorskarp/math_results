#!/usr/bin/env python3
"""Linear-time stackability analysis for configurations on finite trees.

The implementation follows the transfer-message theorem proved in README.md.
For every oriented edge ``x -> y``, the message is the greatest possible net
change at ``y`` when the component on the ``x`` side is cleared.  A target is
reachable exactly when its root score is positive.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class StackabilityAnalysis:
    """All directed messages and target scores for one configuration."""

    messages: dict[tuple[int, int], int]
    root_scores: tuple[int, ...]

    @property
    def stackable_targets(self) -> tuple[int, ...]:
        return tuple(i for i, score in enumerate(self.root_scores) if score >= 1)

    @property
    def is_stackable(self) -> bool:
        return bool(self.stackable_targets)


def transfer(effective: int) -> int:
    """Return the transfer of a nonempty branch with effective input ``effective``."""

    if effective <= 1:
        return 2 * effective - 3
    if effective % 2 == 0:
        return effective // 2
    return (effective - 3) // 2


def _validate_tree(adjacency: Sequence[Sequence[int]]) -> tuple[tuple[int, ...], ...]:
    n = len(adjacency)
    if n == 0:
        raise ValueError("a tree must have at least one vertex")
    normalized = tuple(tuple(neighbors) for neighbors in adjacency)
    for vertex, neighbors in enumerate(normalized):
        if len(set(neighbors)) != len(neighbors):
            raise ValueError(f"duplicate neighbor at vertex {vertex}")
        for neighbor in neighbors:
            if neighbor < 0 or neighbor >= n or neighbor == vertex:
                raise ValueError(f"invalid edge endpoint {vertex}-{neighbor}")
            if vertex not in normalized[neighbor]:
                raise ValueError(f"adjacency is not symmetric at {vertex}-{neighbor}")
    if sum(map(len, normalized)) != 2 * (n - 1):
        raise ValueError("the graph does not have n-1 edges")
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbor in normalized[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    if len(seen) != n:
        raise ValueError("the graph is disconnected")
    return normalized


def _rooting(adjacency: tuple[tuple[int, ...], ...]) -> tuple[list[int], list[int]]:
    parent = [-2] * len(adjacency)
    parent[0] = -1
    order = [0]
    for vertex in order:
        for neighbor in adjacency[vertex]:
            if neighbor == parent[vertex]:
                continue
            if parent[neighbor] != -2:
                raise ValueError("the graph contains a cycle")
            parent[neighbor] = vertex
            order.append(neighbor)
    return parent, order


def analyze_tree(
    adjacency: Sequence[Sequence[int]], configuration: Sequence[int]
) -> StackabilityAnalysis:
    """Compute all target scores in O(|V|) integer operations.

    ``root_scores[r] >= 1`` if and only if the configuration can be stacked at
    vertex ``r``.  In particular, the configuration is stackable if and only
    if at least one score is positive.
    """

    tree = _validate_tree(adjacency)
    if len(configuration) != len(tree):
        raise ValueError("configuration length does not match the tree")
    if any(not isinstance(value, int) or value < 0 for value in configuration):
        raise ValueError("configuration entries must be nonnegative integers")
    config = tuple(configuration)
    parent, order = _rooting(tree)
    messages: dict[tuple[int, int], int] = {}
    support_count = [int(value > 0) for value in config]

    for vertex in reversed(order[1:]):
        children = [w for w in tree[vertex] if parent[w] == vertex]
        for child in children:
            support_count[vertex] += support_count[child]
        effective = config[vertex] + sum(messages[(child, vertex)] for child in children)
        messages[(vertex, parent[vertex])] = (
            transfer(effective) if support_count[vertex] else 0
        )

    total_support = sum(value > 0 for value in config)
    root_scores = [0] * len(tree)
    for vertex in order:
        score = config[vertex] + sum(messages[(neighbor, vertex)] for neighbor in tree[vertex])
        root_scores[vertex] = score
        for child in tree[vertex]:
            if parent[child] != vertex:
                continue
            complement_is_nonempty = total_support > support_count[child]
            effective = score - messages[(child, vertex)]
            messages[(vertex, child)] = transfer(effective) if complement_is_nonempty else 0

    return StackabilityAnalysis(messages, tuple(root_scores))


def directed_deficits(
    adjacency: Sequence[Sequence[int]],
) -> tuple[dict[tuple[int, int], int], tuple[int, ...]]:
    """Compute the structural deficits and ``sigma_T(v)-1`` at every vertex."""

    tree = _validate_tree(adjacency)
    if len(tree) < 2:
        raise ValueError("the Csernak-Soukup estimate is used here for nontrivial trees")
    parent, order = _rooting(tree)
    deficits: dict[tuple[int, int], int] = {}
    for vertex in reversed(order[1:]):
        children = [w for w in tree[vertex] if parent[w] == vertex]
        deficits[(vertex, parent[vertex])] = (
            1 if not children else 3 + 2 * sum(deficits[(child, vertex)] for child in children)
        )
    for vertex in order:
        for child in tree[vertex]:
            if parent[child] != vertex:
                continue
            other_neighbors = [w for w in tree[vertex] if w != child]
            deficits[(vertex, child)] = (
                1
                if not other_neighbors
                else 3 + 2 * sum(deficits[(w, vertex)] for w in other_neighbors)
            )
    sigma_minus_one = tuple(
        sum(deficits[(neighbor, vertex)] for neighbor in tree[vertex])
        for vertex in range(len(tree))
    )
    return deficits, sigma_minus_one


def tree_estimates(adjacency: Sequence[Sequence[int]]) -> tuple[int, ...]:
    """Return ``sigma_T(v) + leaf(v)`` for every vertex ``v``."""

    tree = _validate_tree(adjacency)
    _, sigma_minus_one = directed_deficits(tree)
    leaf_count = sum(len(neighbors) == 1 for neighbors in tree)
    return tuple(
        sigma_minus_one[vertex]
        + 1
        + leaf_count
        - int(len(tree[vertex]) == 1)
        for vertex in range(len(tree))
    )


def critical_configuration(
    adjacency: Sequence[Sequence[int]], heavy_vertex: int
) -> tuple[int, ...]:
    """Construct the canonical non-stackable configuration associated with a vertex."""

    tree = _validate_tree(adjacency)
    if heavy_vertex < 0 or heavy_vertex >= len(tree):
        raise ValueError("heavy vertex is outside the tree")
    _, sigma_minus_one = directed_deficits(tree)
    config = [0] * len(tree)
    config[heavy_vertex] = sigma_minus_one[heavy_vertex]
    for vertex, neighbors in enumerate(tree):
        if len(neighbors) == 1 and vertex != heavy_vertex:
            config[vertex] = 1
    return tuple(config)


def _parse_edges(text: str) -> tuple[tuple[int, ...], ...]:
    pairs: list[tuple[int, int]] = []
    maximum = -1
    for item in text.split(","):
        first, second = map(int, item.split("-", 1))
        pairs.append((first, second))
        maximum = max(maximum, first, second)
    adjacency = [[] for _ in range(maximum + 1)]
    for first, second in pairs:
        adjacency[first].append(second)
        adjacency[second].append(first)
    return tuple(tuple(neighbors) for neighbors in adjacency)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--edges", required=True, help="comma-separated edges, e.g. 0-1,1-2")
    parser.add_argument("--config", required=True, help="comma-separated pebble counts")
    args = parser.parse_args()
    adjacency = _parse_edges(args.edges)
    configuration = tuple(map(int, args.config.split(",")))
    analysis = analyze_tree(adjacency, configuration)
    estimates = tree_estimates(adjacency) if len(adjacency) >= 2 else ()
    print(
        json.dumps(
            {
                "root_scores": analysis.root_scores,
                "stackable_targets": analysis.stackable_targets,
                "is_stackable": analysis.is_stackable,
                "vertex_estimates": estimates,
                "tree_estimate": max(estimates) if estimates else None,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
