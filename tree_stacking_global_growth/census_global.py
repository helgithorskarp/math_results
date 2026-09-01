#!/usr/bin/env python3
"""Linear-time critical-count evaluation and global unlabeled-tree census."""

from __future__ import annotations

import argparse
import json
import platform
import time
from math import comb

import networkx as nx


KNOWN_TREE_COUNTS = {
    2: 1,
    3: 1,
    4: 2,
    5: 3,
    6: 6,
    7: 11,
    8: 23,
    9: 47,
    10: 106,
    11: 235,
    12: 551,
    13: 1301,
    14: 3159,
    15: 7741,
    16: 19320,
    17: 48629,
    18: 123867,
    19: 317955,
    20: 823065,
    21: 2144505,
    22: 5623756,
}


def critical_data(tree: nx.Graph) -> dict[str, object]:
    """Return the exact critical count and maximizing sibling classes in O(n)."""

    order = len(tree)
    if order == 2:
        return {"critical_count": 1, "classes": [[0], [1]]}

    root = 0
    parent = {root: -1}
    traversal = [root]
    for vertex in traversal:
        for neighbor in tree.neighbors(vertex):
            if neighbor != parent[vertex]:
                parent[neighbor] = vertex
                traversal.append(neighbor)

    weight = {
        vertex: (tree.degree(vertex) if tree.degree(vertex) > 1 else 0)
        for vertex in tree
    }
    down = dict(weight)
    for vertex in reversed(traversal):
        for neighbor in tree.neighbors(vertex):
            if parent.get(neighbor) == vertex:
                down[vertex] += 2 * down[neighbor]

    potential = {root: down[root]}
    for vertex in traversal[1:]:
        ancestor = parent[vertex]
        potential[vertex] = 2 * potential[ancestor] - 3 * down[vertex]

    leaves = [vertex for vertex in tree if tree.degree(vertex) == 1]
    if any(potential[leaf] % 2 for leaf in leaves):
        raise AssertionError("leaf potential must be even")
    excess = {leaf: potential[leaf] // 2 for leaf in leaves}
    maximum = max(excess.values())
    maximizing_parents = {
        next(tree.neighbors(leaf)) for leaf, value in excess.items() if value == maximum
    }

    classes = []
    count = 0
    for class_parent in sorted(maximizing_parents):
        siblings = sorted(
            vertex
            for vertex in tree.neighbors(class_parent)
            if tree.degree(vertex) == 1
        )
        d = len(siblings)
        count += comb(maximum + d - 1, d - 1)
        classes.append(siblings)
    return {
        "critical_count": count,
        "maximizing_excess": maximum,
        "classes": classes,
    }


def slow_critical_count(tree: nx.Graph) -> int:
    """Independent distance-based implementation used only for cross-checking."""

    if len(tree) == 2:
        return 1
    internal = [vertex for vertex in tree if tree.degree(vertex) > 1]
    excess = {
        leaf: sum(
            tree.degree(vertex)
            * (1 << (nx.shortest_path_length(tree, leaf, vertex) - 1))
            for vertex in internal
        )
        for leaf in tree
        if tree.degree(leaf) == 1
    }
    maximum = max(excess.values())
    parents = {
        next(tree.neighbors(leaf)) for leaf, value in excess.items() if value == maximum
    }
    return sum(
        comb(
            maximum
            + sum(tree.degree(vertex) == 1 for vertex in tree.neighbors(class_parent))
            - 1,
            sum(tree.degree(vertex) == 1 for vertex in tree.neighbors(class_parent))
            - 1,
        )
        for class_parent in parents
    )


def identify_family(tree: nx.Graph) -> dict[str, object]:
    degrees = dict(tree.degree())
    order = len(tree)
    if max(degrees.values()) == order - 1:
        return {"family": "star", "leaves": order - 1}
    hubs = [vertex for vertex, degree in degrees.items() if degree > 2]
    if len(hubs) != 2 or degrees[hubs[0]] != degrees[hubs[1]]:
        return {"family": "other"}
    d = degrees[hubs[0]] - 1
    if any(
        sum(degrees[neighbor] == 1 for neighbor in tree.neighbors(hub)) != d
        for hub in hubs
    ):
        return {"family": "other"}
    if any(degree not in (1, 2, d + 1) for degree in degrees.values()):
        return {"family": "other"}
    return {
        "family": "symmetric_double_broom",
        "hub_distance": nx.shortest_path_length(tree, hubs[0], hubs[1]),
        "leaves_per_hub": d,
    }


def census(order: int) -> dict[str, object]:
    started = time.monotonic()
    checked = 0
    best = -1
    maximizers = []
    for tree in nx.nonisomorphic_trees(order):
        checked += 1
        value = int(critical_data(tree)["critical_count"])
        if value > best:
            best = value
            maximizers = [tree.copy()]
        elif value == best:
            maximizers.append(tree.copy())
    if checked != KNOWN_TREE_COUNTS[order]:
        raise AssertionError((order, checked, KNOWN_TREE_COUNTS[order]))
    return {
        "order": order,
        "trees_checked": checked,
        "maximum": best,
        "maximizer_count": len(maximizers),
        "maximizers": [
            {
                "graph6": nx.to_graph6_bytes(tree, header=False).strip().decode(),
                "degree_sequence": sorted(dict(tree.degree()).values()),
                **identify_family(tree),
            }
            for tree in maximizers
        ],
        "elapsed_seconds": round(time.monotonic() - started, 6),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-order", type=int, default=20)
    parser.add_argument("--max-order", type=int, default=20)
    parser.add_argument("--cross-check-order", type=int, default=12)
    args = parser.parse_args()

    cross_checked = 0
    for order in range(2, args.cross_check_order + 1):
        for tree in nx.nonisomorphic_trees(order):
            fast = int(critical_data(tree)["critical_count"])
            slow = slow_critical_count(tree)
            if fast != slow:
                raise AssertionError((order, fast, slow))
            cross_checked += 1

    records = [census(order) for order in range(args.min_order, args.max_order + 1)]
    print(
        json.dumps(
            {
                "python": platform.python_version(),
                "networkx": nx.__version__,
                "cross_checked_trees": cross_checked,
                "census": records,
                "all_checks": True,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
