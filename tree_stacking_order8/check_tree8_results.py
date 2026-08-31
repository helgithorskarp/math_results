#!/usr/bin/env python3
"""Independently check the order-eight tree catalog and C++ result summary."""

from __future__ import annotations

import argparse
import re
from functools import cache
from itertools import permutations
from pathlib import Path

import networkx as nx


def parse_catalog(path: Path) -> list[tuple[int, int, nx.Graph]]:
    result: list[tuple[int, int, nx.Graph]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        tree_id_text, estimate_text, edges_text = line.split("\t")
        edges = [tuple(map(int, item.split("-"))) for item in edges_text.split(",")]
        graph = nx.Graph()
        graph.add_nodes_from(range(8))
        graph.add_edges_from(edges)
        result.append((int(tree_id_text), int(estimate_text), graph))
    return result


def tree_estimate(graph: nx.Graph) -> int:
    values = []
    for root in graph:
        distance = nx.single_source_shortest_path_length(graph, root)
        sigma = sum(
            graph.degree(vertex) * 2 ** distance[vertex]
            for vertex in graph
            if vertex == root or graph.degree(vertex) > 1
        )
        leaves = sum(
            vertex != root and graph.degree(vertex) == 1 for vertex in graph
        )
        values.append(sigma + leaves + 1)
    return max(values)


def automorphisms(graph: nx.Graph) -> tuple[tuple[int, ...], ...]:
    adjacency = {
        (min(first, second), max(first, second)) for first, second in graph.edges
    }
    result = []
    for permutation in permutations(range(8)):
        if all(
            ((min(first, second), max(first, second)) in adjacency)
            == (
                (
                    min(permutation[first], permutation[second]),
                    max(permutation[first], permutation[second]),
                )
                in adjacency
            )
            for first in range(8)
            for second in range(8)
        ):
            result.append(permutation)
    return tuple(result)


RESULT_PATTERN = re.compile(
    r"^RESULT tree=(?P<tree>\d+) "
    r"stacking_number=(?P<stack>\d+) "
    r"estimate=(?P<estimate>\d+) "
    r"automorphisms=(?P<automorphisms>\d+) "
    r"peak_weight=(?P<peak_weight>\d+) "
    r"peak_nonstackable_orbits=(?P<peak>\d+) "
    r"critical_witness=\[(?P<witness>[0-9,]+)\]$"
)


def parse_run(path: Path) -> dict[int, dict[str, object]]:
    result: dict[int, dict[str, object]] = {}
    complete = False
    for line in path.read_text(encoding="utf-8").splitlines():
        match = RESULT_PATTERN.match(line)
        if match:
            fields: dict[str, object] = {
                key: int(value)
                for key, value in match.groupdict().items()
                if key != "witness"
            }
            fields["witness"] = tuple(map(int, match.group("witness").split(",")))
            result[int(fields["tree"])] = fields
        if line == "COMPLETE trees=23 all_equal=true":
            complete = True
    if not complete:
        raise AssertionError("run log lacks the complete 23-tree marker")
    return result


def witness_is_stackable(
    graph: nx.Graph, group: tuple[tuple[int, ...], ...], witness: tuple[int, ...]
) -> tuple[bool, int]:
    directed_edges = [(a, b) for a, b in graph.edges for a, b in ((a, b), (b, a))]

    def canonical(config: tuple[int, ...]) -> tuple[int, ...]:
        return min(tuple(config[permutation[index]] for index in range(8)) for permutation in group)

    @cache
    def visit(config: tuple[int, ...]) -> bool:
        if sum(value != 0 for value in config) == 1:
            return True
        for source, target in directed_edges:
            if config[source] < 2:
                continue
            child = list(config)
            child[source] -= 2
            child[target] += 1
            if visit(canonical(tuple(child))):
                return True
        return False

    answer = visit(canonical(witness))
    return answer, visit.cache_info().currsize


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("catalog", type=Path)
    parser.add_argument("run_log", type=Path)
    parser.add_argument(
        "--witness-tree",
        action="append",
        type=int,
        default=[],
        help="independently recurse over the critical witness for this tree ID",
    )
    args = parser.parse_args()

    catalog = parse_catalog(args.catalog)
    assert len(catalog) == 23
    assert [tree_id for tree_id, _estimate, _graph in catalog] == list(range(23))
    generated = list(nx.nonisomorphic_trees(8))
    assert len(generated) == 23

    match_matrix = [
        [nx.is_isomorphic(graph, candidate) for candidate in generated]
        for _tree_id, _estimate, graph in catalog
    ]
    assert all(sum(row) == 1 for row in match_matrix)
    assert all(sum(row[index] for row in match_matrix) == 1 for index in range(23))

    run = parse_run(args.run_log)
    assert sorted(run) == list(range(23))
    requested_witnesses = set(args.witness_tree)
    assert requested_witnesses <= set(range(23))
    witness_states = 0
    for tree_id, recorded_estimate, graph in catalog:
        assert nx.is_tree(graph)
        assert tree_estimate(graph) == recorded_estimate
        group = automorphisms(graph)
        fields = run[tree_id]
        assert fields["stack"] == recorded_estimate
        assert fields["estimate"] == recorded_estimate
        assert fields["automorphisms"] == len(group)
        witness = fields["witness"]
        assert isinstance(witness, tuple) and len(witness) == 8
        assert sum(witness) == recorded_estimate - 1
        if tree_id in requested_witnesses:
            stackable, states = witness_is_stackable(graph, group, witness)
            assert not stackable
            witness_states += states

    print("catalog_trees=23")
    print("networkx_nonisomorphic_trees=23")
    print("unique_isomorphism_matching=true")
    print("estimates_and_automorphism_orders_match=true")
    print("cpp_stacking_numbers_match_estimates=true")
    if requested_witnesses:
        print("critical_witnesses_independently_nonstackable=true")
        print(f"critical_witness_tree_ids={sorted(requested_witnesses)}")
        print(f"independent_witness_states={witness_states}")


if __name__ == "__main__":
    main()
