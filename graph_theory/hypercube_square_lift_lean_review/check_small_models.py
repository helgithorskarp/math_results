#!/usr/bin/env python3
"""Exhaust the two-layer square-saturation theorem on base sets of size <= 4.

This is a definition-level model check, independent of Lean and Mathlib.  A
graph is represented by ordinary Python neighbor sets.
"""

from __future__ import annotations

from itertools import combinations


EXPECTED_COUNTS = {1: 1, 2: 3, 3: 16, 4: 909}


def edge_list(order: int) -> list[tuple[int, int]]:
    return list(combinations(range(order), 2))


def graph_from_mask(order: int, mask: int, edges: list[tuple[int, int]]) -> list[set[int]]:
    adjacency = [set() for _ in range(order)]
    for index, (left, right) in enumerate(edges):
        if mask >> index & 1:
            adjacency[left].add(right)
            adjacency[right].add(left)
    return adjacency


def square_witness(adjacency: list[set[int]], x: int, y: int) -> bool:
    """Return whether x-a-b-y is the other side of a genuine four-cycle."""
    order = len(adjacency)
    return any(
        x != b
        and a != y
        and a in adjacency[x]
        and b in adjacency[a]
        and y in adjacency[b]
        for a in range(order)
        for b in range(order)
    )


def square_free(adjacency: list[set[int]]) -> bool:
    return all(
        not square_witness(adjacency, x, y)
        for x in range(len(adjacency))
        for y in adjacency[x]
    )


def square_saturated_in(graph: list[set[int]], host: list[set[int]]) -> bool:
    order = len(graph)
    return (
        all(neighbor in host[vertex] for vertex in range(order) for neighbor in graph[vertex])
        and square_free(graph)
        and all(
            y in graph[x] or square_witness(graph, x, y)
            for x in range(order)
            for y in host[x]
            if x < y
        )
    )


def independent_dominating_in_intersection(
    graph_zero: list[set[int]], graph_one: list[set[int]], chosen: set[int]
) -> bool:
    intersection = [graph_zero[v] & graph_one[v] for v in range(len(graph_zero))]
    independent = all(v not in intersection[u] for u in chosen for v in chosen)
    dominating = all(v in chosen or bool(intersection[v] & chosen) for v in range(len(graph_zero)))
    return independent and dominating


def two_layer_lift(
    graph_zero: list[set[int]], graph_one: list[set[int]], chosen: set[int]
) -> list[set[int]]:
    order = len(graph_zero)
    result = [set() for _ in range(2 * order)]
    for graph, offset in ((graph_zero, 0), (graph_one, order)):
        for vertex in range(order):
            result[vertex + offset].update(neighbor + offset for neighbor in graph[vertex])
    for vertex in chosen:
        result[vertex].add(order + vertex)
        result[order + vertex].add(vertex)
    return result


def edge_count(adjacency: list[set[int]]) -> int:
    return sum(map(len, adjacency)) // 2


def main() -> None:
    total = 0
    for order in range(1, 5):
        edges = edge_list(order)
        full_mask = (1 << len(edges)) - 1
        verified = 0
        for host_mask in range(full_mask + 1):
            host = graph_from_mask(order, host_mask, edges)
            saturated_subgraphs: list[tuple[int, list[set[int]]]] = []
            graph_mask = host_mask
            while True:
                graph = graph_from_mask(order, graph_mask, edges)
                if square_saturated_in(graph, host):
                    saturated_subgraphs.append((graph_mask, graph))
                if graph_mask == 0:
                    break
                graph_mask = (graph_mask - 1) & host_mask

            for mask_zero, graph_zero in saturated_subgraphs:
                for mask_one, graph_one in saturated_subgraphs:
                    for chosen_mask in range(1 << order):
                        chosen = {v for v in range(order) if chosen_mask >> v & 1}
                        if not independent_dominating_in_intersection(
                            graph_zero, graph_one, chosen
                        ):
                            continue
                        lift = two_layer_lift(graph_zero, graph_one, chosen)
                        lift_host = two_layer_lift(host, host, set(range(order)))
                        if not square_saturated_in(lift, lift_host):
                            raise AssertionError(
                                (order, host_mask, mask_zero, mask_one, chosen_mask)
                            )
                        if edge_count(lift) != (
                            mask_zero.bit_count() + mask_one.bit_count() + len(chosen)
                        ):
                            raise AssertionError("two-layer edge formula failed")
                        verified += 1

        if verified != EXPECTED_COUNTS[order]:
            raise AssertionError((order, verified, EXPECTED_COUNTS[order]))
        print(f"n={order} verified_instances={verified}")
        total += verified
    print(f"total_verified_instances={total}")


if __name__ == "__main__":
    main()
