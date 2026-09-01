#!/usr/bin/env python3
"""Check structural balance at maximizing critical tree-stacking leaf classes."""

from __future__ import annotations

import argparse
import json
import random
from collections import deque

import networkx as nx


def distances(tree: nx.Graph, source: int) -> dict[int, int]:
    result = {source: 0}
    queue = deque([source])
    while queue:
        vertex = queue.popleft()
        for neighbor in tree.neighbors(vertex):
            if neighbor not in result:
                result[neighbor] = result[vertex] + 1
                queue.append(neighbor)
    return result


def leaf_excesses(tree: nx.Graph) -> dict[int, int]:
    internal = [vertex for vertex in tree if tree.degree(vertex) > 1]
    return {
        leaf: sum(
            tree.degree(vertex) * (1 << (distance - 1))
            for vertex, distance in distances(tree, leaf).items()
            if vertex in internal
        )
        for leaf in tree
        if tree.degree(leaf) == 1
    }


def check_tree(tree: nx.Graph) -> list[dict[str, int | str]]:
    excess = leaf_excesses(tree)
    maximum = max(excess.values())
    leaves = set(excess)
    failures = []
    maximizing_parents = {
        next(tree.neighbors(leaf)) for leaf, value in excess.items() if value == maximum
    }
    for parent in maximizing_parents:
        siblings = {v for v in tree.neighbors(parent) if tree.degree(v) == 1}
        internal_neighbors = [
            v for v in tree.neighbors(parent) if tree.degree(v) > 1
        ]
        if internal_neighbors and len(internal_neighbors) != 1:
            failures.append(
                {
                    "property": "core_endpoint",
                    "order": len(tree),
                    "graph6": nx.to_graph6_bytes(tree, header=False).strip().decode(),
                    "leaf_class": len(siblings),
                    "internal_neighbors": len(internal_neighbors),
                }
            )
        outside_leaves = leaves - siblings
        internal_height = max(
            (distances(tree, parent)[v] for v in tree if tree.degree(v) > 1),
            default=0,
        )
        if internal_neighbors and internal_height > len(tree) - 2 * len(siblings) - 1:
            failures.append(
                {
                    "property": "height_balance",
                    "order": len(tree),
                    "graph6": nx.to_graph6_bytes(tree, header=False).strip().decode(),
                    "leaf_class": len(siblings),
                    "outside_leaves": len(outside_leaves),
                    "internal_height": internal_height,
                    "height_bound": len(tree) - 2 * len(siblings) - 1,
                }
            )
    return failures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=19)
    parser.add_argument("--random-trials", type=int, default=0)
    parser.add_argument("--random-max-order", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260901)
    args = parser.parse_args()
    checked = 0
    for order in range(3, args.max_order + 1):
        for tree in nx.nonisomorphic_trees(order):
            checked += 1
            failures = check_tree(tree)
            if failures:
                print(json.dumps({"checked": checked, "failures": failures}, sort_keys=True))
                raise SystemExit(1)
    generator = random.Random(args.seed)
    for _ in range(args.random_trials):
        order = generator.randint(3, args.random_max_order)
        tree = nx.from_prufer_sequence(
            [generator.randrange(order) for _ in range(order - 2)]
        )
        checked += 1
        failures = check_tree(tree)
        if failures:
            print(json.dumps({"checked": checked, "failures": failures}, sort_keys=True))
            raise SystemExit(1)
    print(
        json.dumps(
            {
                "all_checks": True,
                "max_order": args.max_order,
                "random_trials": args.random_trials,
                "seed": args.seed,
                "trees_checked": checked,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
