#!/usr/bin/env python3
"""Independent finite checks for the tree transfer theorem.

The decisive comparison uses the raw move DAG: for each configuration it
recursively unions the targets reachable after every legal first move.  It
does not use transfer messages in the reference calculation.
"""

from __future__ import annotations

import argparse
import hashlib
from collections import deque
from functools import cache
from itertools import combinations

import networkx as nx

from tree_stackability import (
    analyze_tree,
    critical_configuration,
    tree_estimates,
)


def compositions(weight: int, parts: int):
    """Yield all weak compositions in deterministic lexicographic bar order."""

    for bars in combinations(range(weight + parts - 1), parts - 1):
        result = []
        previous = -1
        for bar in bars + (weight + parts - 1,):
            result.append(bar - previous - 1)
            previous = bar
        yield tuple(result)


def adjacency_of(graph: nx.Graph) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(sorted(graph.neighbors(vertex))) for vertex in range(len(graph)))


def direct_estimates(adjacency: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    """Evaluate the published distance/degree expression directly."""

    leaf_count = sum(len(neighbors) == 1 for neighbors in adjacency)
    result = []
    for root in range(len(adjacency)):
        distance = [-1] * len(adjacency)
        distance[root] = 0
        queue = deque([root])
        while queue:
            vertex = queue.popleft()
            for neighbor in adjacency[vertex]:
                if distance[neighbor] < 0:
                    distance[neighbor] = distance[vertex] + 1
                    queue.append(neighbor)
        result.append(
            1
            + leaf_count
            + sum(
                len(adjacency[vertex]) * (1 << distance[vertex])
                for vertex in range(len(adjacency))
                if len(adjacency[vertex]) > 1
            )
        )
    return tuple(result)


def exact_target_oracle(adjacency: tuple[tuple[int, ...], ...]):
    """Build an independent memoized oracle returning all reachable targets."""

    @cache
    def reachable_targets(configuration: tuple[int, ...]) -> int:
        support = [i for i, value in enumerate(configuration) if value]
        targets = (1 << support[0]) if len(support) == 1 else 0
        for source, value in enumerate(configuration):
            if value < 2:
                continue
            for target in adjacency[source]:
                child = list(configuration)
                child[source] -= 2
                child[target] += 1
                targets |= reachable_targets(tuple(child))
                if targets == (1 << len(adjacency)) - 1:
                    return targets
        return targets

    return reachable_targets


def graph_catalog(max_order: int):
    for order in range(2, max_order + 1):
        for index, graph in enumerate(nx.nonisomorphic_trees(order)):
            yield order, index, nx.convert_node_labels_to_integers(graph)


def verify_move_dag(max_order: int, max_weight: int, digest) -> tuple[int, int]:
    trees = 0
    configurations = 0
    for order, index, graph in graph_catalog(max_order):
        adjacency = adjacency_of(graph)
        oracle = exact_target_oracle(adjacency)
        graph6 = nx.to_graph6_bytes(graph, header=False).strip()
        for weight in range(1, max_weight + 1):
            for configuration in compositions(weight, order):
                exact_mask = oracle(configuration)
                analysis = analyze_tree(adjacency, configuration)
                message_mask = sum(1 << target for target in analysis.stackable_targets)
                assert message_mask == exact_mask, (
                    order,
                    index,
                    configuration,
                    exact_mask,
                    analysis.root_scores,
                )
                digest.update(graph6)
                digest.update(bytes((weight,)))
                digest.update(",".join(map(str, configuration)).encode())
                digest.update(exact_mask.to_bytes(2, "little"))
                digest.update(",".join(map(str, analysis.root_scores)).encode())
                configurations += 1
        trees += 1
    return trees, configurations


def verify_structural_identities(max_order: int, digest) -> tuple[int, int]:
    trees = 0
    critical_cases = 0
    for order, index, graph in graph_catalog(max_order):
        adjacency = adjacency_of(graph)
        estimates = tree_estimates(adjacency)
        assert estimates == direct_estimates(adjacency)
        leaves = [vertex for vertex in range(order) if len(adjacency[vertex]) == 1]
        assert max(estimates) == max(estimates[vertex] for vertex in leaves)
        for heavy_vertex in range(order):
            configuration = critical_configuration(adjacency, heavy_vertex)
            analysis = analyze_tree(adjacency, configuration)
            assert not analysis.is_stackable
            assert set(analysis.root_scores) == {0}
            assert sum(configuration) == estimates[heavy_vertex] - 1
            digest.update(f"S:{order}:{index}:{heavy_vertex}:".encode())
            digest.update(",".join(map(str, configuration)).encode())
            critical_cases += 1
        trees += 1
    return trees, critical_cases


def verify_fixed_target_boundary(max_order: int, digest) -> tuple[int, int]:
    trees = 0
    configurations = 0
    for order, index, graph in graph_catalog(max_order):
        if order < 3:
            continue
        adjacency = adjacency_of(graph)
        estimate = max(tree_estimates(adjacency))
        internal = [vertex for vertex in range(order) if len(adjacency[vertex]) > 1]
        for configuration in compositions(estimate, order):
            scores = analyze_tree(adjacency, configuration).root_scores
            assert all(scores[target] >= 1 for target in internal), (
                order,
                index,
                estimate,
                configuration,
                scores,
            )
            digest.update(f"B:{order}:{index}:".encode())
            digest.update(",".join(map(str, configuration)).encode())
            configurations += 1
        trees += 1
    return trees, configurations


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-exact-order", type=int, default=7)
    parser.add_argument("--max-exact-weight", type=int, default=10)
    parser.add_argument("--max-structural-order", type=int, default=12)
    parser.add_argument("--max-boundary-order", type=int, default=5)
    args = parser.parse_args()
    if not 2 <= args.max_exact_order <= 15:
        raise ValueError("exact order must lie between 2 and 15")
    if args.max_exact_weight < 1:
        raise ValueError("exact weight must be positive")
    if args.max_structural_order < 2 or args.max_boundary_order < 2:
        raise ValueError("tree orders must be at least two")

    digest = hashlib.sha256()
    move_trees, move_configs = verify_move_dag(
        args.max_exact_order, args.max_exact_weight, digest
    )
    structural_trees, critical_cases = verify_structural_identities(
        args.max_structural_order, digest
    )
    boundary_trees, boundary_configs = verify_fixed_target_boundary(
        args.max_boundary_order, digest
    )
    print(f"networkx={nx.__version__}")
    print(f"move_dag_trees={move_trees}")
    print(f"move_dag_configurations={move_configs}")
    print(f"structural_trees={structural_trees}")
    print(f"critical_configurations={critical_cases}")
    print(f"fixed_target_boundary_trees={boundary_trees}")
    print(f"fixed_target_boundary_configurations={boundary_configs}")
    print(f"record_sha256={digest.hexdigest()}")
    print("all_checks=true")


if __name__ == "__main__":
    main()
