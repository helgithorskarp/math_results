#!/usr/bin/env python3
"""Critical non-stackable configurations on finite trees.

This is a self-contained implementation of the transfer-message criterion and
the sibling-leaf classification proved in README.md.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from itertools import combinations
from math import comb
from typing import Iterator, Sequence


Tree = tuple[tuple[int, ...], ...]
Configuration = tuple[int, ...]


@dataclass(frozen=True)
class ParentClass:
    """One sibling-leaf class of critical configurations."""

    parent: int
    leaves: tuple[int, ...]
    heavy_value: int
    excess_units: int
    configuration_count: int


def validate_tree(adjacency: Sequence[Sequence[int]]) -> Tree:
    """Normalize and validate an undirected finite tree."""

    tree = tuple(tuple(sorted(neighbors)) for neighbors in adjacency)
    n = len(tree)
    if n < 2:
        raise ValueError("the classification requires a tree with at least two vertices")
    for vertex, neighbors in enumerate(tree):
        if len(set(neighbors)) != len(neighbors):
            raise ValueError(f"duplicate neighbor at vertex {vertex}")
        for neighbor in neighbors:
            if neighbor < 0 or neighbor >= n or neighbor == vertex:
                raise ValueError(f"invalid edge endpoint {vertex}-{neighbor}")
            if vertex not in tree[neighbor]:
                raise ValueError(f"adjacency is not symmetric at {vertex}-{neighbor}")
    if sum(map(len, tree)) != 2 * (n - 1):
        raise ValueError("the graph does not have n-1 edges")
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbor in tree[vertex]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    if len(seen) != n:
        raise ValueError("the graph is disconnected")
    return tree


def rooting(tree: Tree) -> tuple[list[int], list[int]]:
    """Return a parent array and parent-before-child order rooted at zero."""

    parent = [-2] * len(tree)
    parent[0] = -1
    order = [0]
    for vertex in order:
        for neighbor in tree[vertex]:
            if neighbor == parent[vertex]:
                continue
            if parent[neighbor] != -2:
                raise ValueError("the graph contains a cycle")
            parent[neighbor] = vertex
            order.append(neighbor)
    return parent, order


def transfer(effective: int) -> int:
    """Maximum net branch transfer for a nonempty branch."""

    if effective <= 1:
        return 2 * effective - 3
    if effective % 2 == 0:
        return effective // 2
    return (effective - 3) // 2


def root_scores(
    adjacency: Sequence[Sequence[int]], configuration: Sequence[int]
) -> tuple[int, ...]:
    """Compute the exact stackability score at every target in linear time."""

    tree = validate_tree(adjacency)
    if len(configuration) != len(tree):
        raise ValueError("configuration length does not match tree order")
    if any(not isinstance(value, int) or value < 0 for value in configuration):
        raise ValueError("configuration entries must be nonnegative integers")
    config = tuple(configuration)
    parent, order = rooting(tree)
    messages: dict[tuple[int, int], int] = {}
    support_count = [int(value > 0) for value in config]

    for vertex in reversed(order[1:]):
        children = [child for child in tree[vertex] if parent[child] == vertex]
        support_count[vertex] += sum(support_count[child] for child in children)
        effective = config[vertex] + sum(messages[(child, vertex)] for child in children)
        messages[(vertex, parent[vertex])] = (
            transfer(effective) if support_count[vertex] else 0
        )

    total_support = sum(value > 0 for value in config)
    scores = [0] * len(tree)
    for vertex in order:
        score = config[vertex] + sum(messages[(neighbor, vertex)] for neighbor in tree[vertex])
        scores[vertex] = score
        for child in tree[vertex]:
            if parent[child] != vertex:
                continue
            complement_is_nonempty = total_support > support_count[child]
            effective = score - messages[(child, vertex)]
            messages[(vertex, child)] = transfer(effective) if complement_is_nonempty else 0
    return tuple(scores)


def directed_deficits(
    adjacency: Sequence[Sequence[int]],
) -> tuple[dict[tuple[int, int], int], tuple[int, ...]]:
    """Return all structural deficits and H(v)=sigma_T(v)-1."""

    tree = validate_tree(adjacency)
    parent, order = rooting(tree)
    deficits: dict[tuple[int, int], int] = {}
    for vertex in reversed(order[1:]):
        children = [child for child in tree[vertex] if parent[child] == vertex]
        deficits[(vertex, parent[vertex])] = (
            1 if not children else 3 + 2 * sum(deficits[(child, vertex)] for child in children)
        )
    for vertex in order:
        for child in tree[vertex]:
            if parent[child] != vertex:
                continue
            others = [neighbor for neighbor in tree[vertex] if neighbor != child]
            deficits[(vertex, child)] = (
                1 if not others else 3 + 2 * sum(deficits[(neighbor, vertex)] for neighbor in others)
            )
    h_values = tuple(
        sum(deficits[(neighbor, vertex)] for neighbor in tree[vertex])
        for vertex in range(len(tree))
    )
    return deficits, h_values


def vertex_estimates(adjacency: Sequence[Sequence[int]]) -> tuple[int, ...]:
    """Return sigma_T(v)+leaf(v) at every vertex."""

    tree = validate_tree(adjacency)
    _, h_values = directed_deficits(tree)
    leaf_count = sum(len(neighbors) == 1 for neighbors in tree)
    return tuple(
        h_values[vertex] + 1 + leaf_count - int(len(tree[vertex]) == 1)
        for vertex in range(len(tree))
    )


def weak_compositions(total: int, parts: int) -> Iterator[tuple[int, ...]]:
    """Yield weak compositions in deterministic lexicographic bar order."""

    if total < 0 or parts < 1:
        raise ValueError("a weak composition needs a nonnegative total and positive length")
    if parts == 1:
        yield (total,)
        return
    for bars in combinations(range(total + parts - 1), parts - 1):
        result = []
        previous = -1
        for bar in bars + (total + parts - 1,):
            result.append(bar - previous - 1)
            previous = bar
        yield tuple(result)


def parent_classes(adjacency: Sequence[Sequence[int]]) -> tuple[ParentClass, ...]:
    """Return the maximizing sibling-leaf classes in the theorem."""

    tree = validate_tree(adjacency)
    if len(tree) == 2:
        return (ParentClass(0, (1,), 1, 0, 1),)
    estimates = vertex_estimates(tree)
    maximum = max(estimates)
    _, h_values = directed_deficits(tree)
    leaves = [vertex for vertex, neighbors in enumerate(tree) if len(neighbors) == 1]
    maximizing_parents = sorted({tree[leaf][0] for leaf in leaves if estimates[leaf] == maximum})
    result = []
    for parent in maximizing_parents:
        siblings = tuple(leaf for leaf in leaves if tree[leaf][0] == parent)
        heavy_value = h_values[siblings[0]]
        excess_units = (heavy_value - 1) // 2
        result.append(
            ParentClass(
                parent,
                siblings,
                heavy_value,
                excess_units,
                comb(excess_units + len(siblings) - 1, len(siblings) - 1),
            )
        )
    return tuple(result)


def critical_configuration_count(adjacency: Sequence[Sequence[int]]) -> int:
    """Count all size-stack(T)-1 non-stackable configurations."""

    return sum(item.configuration_count for item in parent_classes(adjacency))


def classified_extremizers(adjacency: Sequence[Sequence[int]]) -> Iterator[Configuration]:
    """Generate exactly all critical non-stackable configurations."""

    tree = validate_tree(adjacency)
    if len(tree) == 2:
        yield (1, 1)
        return
    leaves = tuple(vertex for vertex, neighbors in enumerate(tree) if len(neighbors) == 1)
    for item in parent_classes(tree):
        for allocation in weak_compositions(item.excess_units, len(item.leaves)):
            configuration = [0] * len(tree)
            for leaf in leaves:
                configuration[leaf] = 1
            for leaf, excess in zip(item.leaves, allocation, strict=True):
                configuration[leaf] = 1 + 2 * excess
            yield tuple(configuration)


def parse_edges(text: str) -> Tree:
    """Parse comma-separated edges such as 0-1,1-2."""

    pairs = []
    maximum = -1
    for item in text.split(","):
        first, second = map(int, item.split("-", 1))
        pairs.append((first, second))
        maximum = max(maximum, first, second)
    adjacency = [[] for _ in range(maximum + 1)]
    for first, second in pairs:
        adjacency[first].append(second)
        adjacency[second].append(first)
    return validate_tree(adjacency)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--edges", required=True, help="comma-separated edges, e.g. 0-1,1-2")
    parser.add_argument(
        "--list-configurations",
        action="store_true",
        help="include all classified configurations in the JSON output",
    )
    args = parser.parse_args()
    tree = parse_edges(args.edges)
    result: dict[str, object] = {
        "tree_order": len(tree),
        "vertex_estimates": vertex_estimates(tree),
        "stacking_number": max(vertex_estimates(tree)),
        "critical_configuration_count": critical_configuration_count(tree),
        "parent_classes": [item.__dict__ for item in parent_classes(tree)],
    }
    if args.list_configurations:
        result["configurations"] = list(classified_extremizers(tree))
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
