#!/usr/bin/env python3
"""Finite checks for the critical tree-stacking classification."""

from __future__ import annotations

import argparse
import hashlib
from functools import cache
from itertools import combinations

import networkx as nx

from tree_extremizers import (
    classified_extremizers,
    critical_configuration_count,
    root_scores,
    vertex_estimates,
    weak_compositions,
)


def adjacency_of(graph: nx.Graph) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(sorted(graph.neighbors(vertex))) for vertex in range(len(graph)))


def configurations(weight: int, parts: int):
    """Yield every weak composition of weight into parts entries."""

    yield from weak_compositions(weight, parts)


def graph_catalog(max_order: int):
    for order in range(2, max_order + 1):
        for index, graph in enumerate(nx.nonisomorphic_trees(order)):
            yield order, index, nx.convert_node_labels_to_integers(graph)


def exact_target_oracle(adjacency: tuple[tuple[int, ...], ...]):
    """Return a raw move-DAG oracle independent of transfer messages."""

    @cache
    def reachable_targets(configuration: tuple[int, ...]) -> int:
        support = [vertex for vertex, value in enumerate(configuration) if value]
        targets = (1 << support[0]) if len(support) == 1 else 0
        for source, value in enumerate(configuration):
            if value < 2:
                continue
            for target in adjacency[source]:
                child = list(configuration)
                child[source] -= 2
                child[target] += 1
                targets |= reachable_targets(tuple(child))
        return targets

    return reachable_targets


def verify_all_classified(max_order: int, digest) -> tuple[int, int]:
    trees = 0
    classified = 0
    for order, index, graph in graph_catalog(max_order):
        adjacency = adjacency_of(graph)
        estimate = max(vertex_estimates(adjacency))
        configurations_seen = list(classified_extremizers(adjacency))
        assert len(configurations_seen) == len(set(configurations_seen))
        assert len(configurations_seen) == critical_configuration_count(adjacency)
        for configuration in configurations_seen:
            assert sum(configuration) == estimate - 1
            assert set(root_scores(adjacency, configuration)) == {0}
            digest.update(f"C:{order}:{index}:".encode())
            digest.update(",".join(map(str, configuration)).encode())
        trees += 1
        classified += len(configurations_seen)
    return trees, classified


def verify_leaf_frontier(max_order: int, digest) -> tuple[int, int, int]:
    """Exhaust every positive-odd leaf configuration at the critical mass."""

    trees = 0
    candidates = 0
    accepted = 0
    for order, index, graph in graph_catalog(max_order):
        adjacency = adjacency_of(graph)
        leaves = tuple(vertex for vertex in range(order) if len(adjacency[vertex]) == 1)
        estimate = max(vertex_estimates(adjacency))
        excess_units = (estimate - 1 - len(leaves)) // 2
        expected = set(classified_extremizers(adjacency))
        found = set()
        for allocation in weak_compositions(excess_units, len(leaves)):
            configuration = [0] * order
            for leaf, excess in zip(leaves, allocation, strict=True):
                configuration[leaf] = 1 + 2 * excess
            candidate = tuple(configuration)
            if max(root_scores(adjacency, candidate)) <= 0:
                found.add(candidate)
            candidates += 1
        assert found == expected, (order, index, found - expected, expected - found)
        digest.update(f"L:{order}:{index}:{len(found)}".encode())
        trees += 1
        accepted += len(found)
    return trees, candidates, accepted


def verify_full_frontier(max_order: int, digest) -> tuple[int, int, int]:
    """Exhaust every configuration at mass stack(T)-1."""

    trees = 0
    candidates = 0
    accepted = 0
    for order, index, graph in graph_catalog(max_order):
        adjacency = adjacency_of(graph)
        weight = max(vertex_estimates(adjacency)) - 1
        expected = set(classified_extremizers(adjacency))
        found = set()
        for configuration in configurations(weight, order):
            if max(root_scores(adjacency, configuration)) <= 0:
                found.add(configuration)
            candidates += 1
        assert found == expected, (order, index, found - expected, expected - found)
        digest.update(f"F:{order}:{index}:{len(found)}".encode())
        trees += 1
        accepted += len(found)
    return trees, candidates, accepted


def verify_raw_move_dag(max_order: int, digest) -> tuple[int, int, int]:
    """Independently check every classified small-tree obstruction."""

    trees = 0
    configurations_checked = 0
    states = 0
    for order, index, graph in graph_catalog(max_order):
        adjacency = adjacency_of(graph)
        oracle = exact_target_oracle(adjacency)
        for configuration in classified_extremizers(adjacency):
            assert oracle(configuration) == 0, (order, index, configuration)
            digest.update(f"D:{order}:{index}:".encode())
            digest.update(",".join(map(str, configuration)).encode())
            configurations_checked += 1
        states += oracle.cache_info().currsize
        trees += 1
    return trees, configurations_checked, states


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-classified-order", type=int, default=9)
    parser.add_argument("--max-leaf-frontier-order", type=int, default=8)
    parser.add_argument("--max-full-frontier-order", type=int, default=5)
    parser.add_argument("--max-move-dag-order", type=int, default=5)
    args = parser.parse_args()
    if not 2 <= args.max_move_dag_order <= args.max_full_frontier_order:
        raise ValueError("move-DAG order must lie between 2 and full-frontier order")
    if not args.max_full_frontier_order <= args.max_leaf_frontier_order:
        raise ValueError("full-frontier order cannot exceed leaf-frontier order")
    if not args.max_leaf_frontier_order <= args.max_classified_order:
        raise ValueError("leaf-frontier order cannot exceed classified order")

    digest = hashlib.sha256()
    classified_trees, classified_count = verify_all_classified(
        args.max_classified_order, digest
    )
    leaf_trees, leaf_candidates, leaf_accepted = verify_leaf_frontier(
        args.max_leaf_frontier_order, digest
    )
    full_trees, full_candidates, full_accepted = verify_full_frontier(
        args.max_full_frontier_order, digest
    )
    dag_trees, dag_configurations, dag_states = verify_raw_move_dag(
        args.max_move_dag_order, digest
    )
    print(f"python_networkx={nx.__version__}")
    print(f"classified_trees={classified_trees}")
    print(f"classified_configurations={classified_count}")
    print(f"leaf_frontier_trees={leaf_trees}")
    print(f"leaf_frontier_candidates={leaf_candidates}")
    print(f"leaf_frontier_accepted={leaf_accepted}")
    print(f"full_frontier_trees={full_trees}")
    print(f"full_frontier_candidates={full_candidates}")
    print(f"full_frontier_accepted={full_accepted}")
    print(f"move_dag_trees={dag_trees}")
    print(f"move_dag_configurations={dag_configurations}")
    print(f"move_dag_states={dag_states}")
    print(f"record_sha256={digest.hexdigest()}")
    print("all_checks=true")


if __name__ == "__main__":
    main()
