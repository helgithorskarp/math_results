#!/usr/bin/env python3
"""Exact audit for sharp remote-resolver bounds and the tree classification."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import deque
from typing import Iterable


Graph = tuple[frozenset[int], ...]


def graph_from_edges(order: int, edges: Iterable[tuple[int, int]]) -> Graph:
    adjacency = [set() for _ in range(order)]
    for left, right in edges:
        if not (0 <= left < right < order):
            raise ValueError("edges must be canonical distinct vertex pairs")
        adjacency[left].add(right)
        adjacency[right].add(left)
    return tuple(frozenset(neighbours) for neighbours in adjacency)


def distances(graph: Graph, root: int) -> tuple[int, ...]:
    result = [-1] * len(graph)
    result[root] = 0
    queue = deque([root])
    while queue:
        vertex = queue.popleft()
        for neighbour in graph[vertex]:
            if result[neighbour] == -1:
                result[neighbour] = result[vertex] + 1
                queue.append(neighbour)
    return tuple(result)


def connected(graph: Graph) -> bool:
    return bool(graph) and -1 not in distances(graph, 0)


def direction_signature(graph: Graph, root: int, target: int) -> frozenset[int]:
    if target == root:
        return graph[root]
    distance_to_target = distances(graph, target)
    root_distance = distance_to_target[root]
    if root_distance < 1:
        raise ValueError("direction signature requires a connected graph")
    return frozenset(
        neighbour
        for neighbour in graph[root]
        if distance_to_target[neighbour] == root_distance - 1
    )


def remote_vertices(graph: Graph, root: int) -> tuple[int, ...]:
    return tuple(
        vertex
        for vertex in range(len(graph))
        if vertex == root or (vertex not in graph[root] and vertex != root)
    )


def remote_resolver(graph: Graph, root: int) -> bool:
    signatures = [
        direction_signature(graph, root, target)
        for target in remote_vertices(graph, root)
    ]
    return len(signatures) == len(set(signatures))


def equality_signature_condition(graph: Graph, root: int) -> bool:
    neighbours = graph[root]
    proper_nonempty = {
        frozenset(subset)
        for size in range(1, len(neighbours))
        for subset in itertools.combinations(sorted(neighbours), size)
    }
    actual = {
        direction_signature(graph, root, target)
        for target in range(len(graph))
        if target != root and target not in neighbours
    }
    return actual == proper_nonempty and len(actual) == len(graph) - 1 - len(neighbours)


def extremal_graph(degree: int) -> tuple[Graph, int]:
    if degree < 1:
        raise ValueError("degree must be positive")
    if degree == 1:
        return graph_from_edges(2, [(0, 1)]), 0
    root = 0
    first = list(range(1, degree + 1))
    edges = [(root, vertex) for vertex in first]
    next_vertex = degree + 1
    for mask in range(1, (1 << degree) - 1):
        for index, vertex in enumerate(first):
            if mask & (1 << index):
                edges.append((min(vertex, next_vertex), max(vertex, next_vertex)))
        next_vertex += 1
    return graph_from_edges(next_vertex, edges), root


def bipartite(graph: Graph) -> bool:
    colour: list[int | None] = [None] * len(graph)
    for start in range(len(graph)):
        if colour[start] is not None:
            continue
        colour[start] = 0
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            for neighbour in graph[vertex]:
                if colour[neighbour] is None:
                    colour[neighbour] = 1 - colour[vertex]  # type: ignore[operator]
                    queue.append(neighbour)
                elif colour[neighbour] == colour[vertex]:
                    return False
    return True


def diameter(graph: Graph) -> int:
    return max(max(distances(graph, vertex)) for vertex in range(len(graph)))


def rooted_spider(degree: int, subdivided_mask: int) -> tuple[Graph, int]:
    if degree < 1 or not 0 <= subdivided_mask < (1 << degree):
        raise ValueError("invalid rooted-spider parameters")
    edges: list[tuple[int, int]] = []
    next_vertex = degree + 1
    for index in range(degree):
        neighbour = index + 1
        edges.append((0, neighbour))
        if subdivided_mask & (1 << index):
            edges.append((neighbour, next_vertex))
            next_vertex += 1
    return graph_from_edges(next_vertex, edges), 0


def tree_classifier(graph: Graph, root: int) -> bool:
    degree = len(graph[root])
    if degree == 1:
        return len(graph) == 2
    if degree < 2:
        return False
    root_distances = distances(graph, root)
    if max(root_distances) > 2:
        return False
    branch_counts = {neighbour: 0 for neighbour in graph[root]}
    for target, distance in enumerate(root_distances):
        if distance != 2:
            continue
        first_steps = direction_signature(graph, root, target)
        if len(first_steps) != 1:
            return False
        branch = next(iter(first_steps))
        branch_counts[branch] += 1
    return max(branch_counts.values(), default=0) <= 1


def prufer_tree(sequence: tuple[int, ...]) -> Graph:
    order = len(sequence) + 2
    degrees = [1] * order
    for vertex in sequence:
        degrees[vertex] += 1
    edges: list[tuple[int, int]] = []
    for vertex in sequence:
        leaf = next(index for index, degree in enumerate(degrees) if degree == 1)
        edges.append((min(leaf, vertex), max(leaf, vertex)))
        degrees[leaf] -= 1
        degrees[vertex] -= 1
    leaves = [index for index, degree in enumerate(degrees) if degree == 1]
    edges.append((min(leaves), max(leaves)))
    return graph_from_edges(order, edges)


def connected_labelled_graphs(order: int) -> Iterable[Graph]:
    pairs = list(itertools.combinations(range(order), 2))
    for mask in range(1 << len(pairs)):
        edges = [pair for index, pair in enumerate(pairs) if mask & (1 << index)]
        graph = graph_from_edges(order, edges)
        if connected(graph):
            yield graph


def audit_general_graphs(max_order: int = 5) -> tuple[int, int, int]:
    graph_count = 0
    rooted_count = 0
    resolver_count = 0
    for order in range(2, max_order + 1):
        for graph in connected_labelled_graphs(order):
            graph_count += 1
            for root in range(order):
                rooted_count += 1
                if not remote_resolver(graph, root):
                    continue
                resolver_count += 1
                degree = len(graph[root])
                bound = (1 << degree) + degree - 1
                if order > bound:
                    raise AssertionError("degree--order bound failed")
                if (order == bound) != equality_signature_condition(graph, root):
                    raise AssertionError("equality characterization failed")
    return graph_count, rooted_count, resolver_count


def audit_extremal_family(max_degree: int = 8) -> tuple[int, int]:
    total_vertices = 0
    total_signatures = 0
    for degree in range(1, max_degree + 1):
        graph, root = extremal_graph(degree)
        expected_order = (1 << degree) + degree - 1
        if len(graph) != expected_order or len(graph[root]) != degree:
            raise AssertionError("extremal construction has wrong parameters")
        if not connected(graph) or not bipartite(graph):
            raise AssertionError("extremal construction lost connectivity/bipartiteness")
        if not remote_resolver(graph, root):
            raise AssertionError("extremal root does not resolve")
        if not equality_signature_condition(graph, root):
            raise AssertionError("extremal signatures are incomplete")
        if degree >= 2 and diameter(graph) != 4:
            raise AssertionError("extremal construction has wrong diameter")
        total_vertices += len(graph)
        total_signatures += len(remote_vertices(graph, root))
    return total_vertices, total_signatures


def audit_spider_family(max_degree: int = 8) -> tuple[int, int]:
    instances = 0
    vertices = 0
    for degree in range(1, max_degree + 1):
        for mask in range(1 << degree):
            graph, root = rooted_spider(degree, mask)
            expected = degree == 1 and mask == 0 or degree >= 2
            if remote_resolver(graph, root) != expected:
                raise AssertionError("rooted-spider classification failed")
            if tree_classifier(graph, root) != expected:
                raise AssertionError("structural classifier failed on a spider")
            if degree >= 2 and len(graph) > 2 * degree + 1:
                raise AssertionError("tree order bound failed")
            instances += 1
            vertices += len(graph)
    return instances, vertices


def audit_all_labelled_trees(max_order: int = 8) -> tuple[int, int, int]:
    trees = 0
    rooted = 0
    resolvers = 0
    for order in range(2, max_order + 1):
        for sequence in itertools.product(range(order), repeat=order - 2):
            graph = prufer_tree(sequence)
            trees += 1
            for root in range(order):
                rooted += 1
                actual = remote_resolver(graph, root)
                predicted = tree_classifier(graph, root)
                if actual != predicted:
                    raise AssertionError("labelled-tree classification failed")
                if actual:
                    resolvers += 1
                    degree = len(graph[root])
                    bound = 2 if degree == 1 else 2 * degree + 1
                    if order > bound:
                        raise AssertionError("sharp tree order bound failed")
    return trees, rooted, resolvers


def main() -> None:
    general = audit_general_graphs()
    extremal = audit_extremal_family()
    spiders = audit_spider_family()
    trees = audit_all_labelled_trees()
    payload = {
        "connected_graphs_through_5": general[0],
        "extremal_degrees": 8,
        "extremal_signature_domains": extremal[1],
        "extremal_vertices": extremal[0],
        "labelled_trees_through_8": trees[0],
        "remote_resolver_graph_roots": general[2],
        "remote_resolver_tree_roots": trees[2],
        "rooted_graphs_checked": general[1],
        "rooted_spider_instances": spiders[0],
        "rooted_spider_vertices": spiders[1],
        "rooted_trees_checked": trees[1],
    }
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    for key in sorted(payload):
        print(f"{key}={payload[key]}")
    print(f"audit_sha256={digest}")
    print("VERIFIED: sharp general bound, extremal family, and all rooted trees through order 8")


if __name__ == "__main__":
    main()
