#!/usr/bin/env python3
"""Exact finite audit for cactus line-graph degeneracy.

The universal theorem is proved in README.md.  This standard-library checker
audits the block, multiedge, degeneracy, and even-cycle list conventions.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
import json


@dataclass(frozen=True)
class MultiGraph:
    order: int
    edges: tuple[tuple[int, int], ...]

    def check(self) -> None:
        for u, v in self.edges:
            assert 0 <= u < self.order and 0 <= v < self.order and u != v

    def degrees(self) -> tuple[int, ...]:
        answer = [0] * self.order
        for u, v in self.edges:
            answer[u] += 1
            answer[v] += 1
        return tuple(answer)


def edge_blocks(graph: MultiGraph) -> tuple[tuple[int, ...], ...]:
    """Tarjan biconnected edge blocks, with edge IDs preserving parallels."""
    graph.check()
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(graph.order)]
    for edge_id, (u, v) in enumerate(graph.edges):
        adjacency[u].append((v, edge_id))
        adjacency[v].append((u, edge_id))

    discovery = [-1] * graph.order
    low = [-1] * graph.order
    edge_stack: list[int] = []
    blocks: list[tuple[int, ...]] = []
    clock = 0

    def visit(vertex: int, parent_edge: int | None) -> None:
        nonlocal clock
        discovery[vertex] = low[vertex] = clock
        clock += 1
        for other, edge_id in adjacency[vertex]:
            if discovery[other] < 0:
                edge_stack.append(edge_id)
                visit(other, edge_id)
                low[vertex] = min(low[vertex], low[other])
                if low[other] >= discovery[vertex]:
                    block: list[int] = []
                    while True:
                        popped = edge_stack.pop()
                        block.append(popped)
                        if popped == edge_id:
                            break
                    blocks.append(tuple(sorted(block)))
            elif edge_id != parent_edge and discovery[other] < discovery[vertex]:
                edge_stack.append(edge_id)
                low[vertex] = min(low[vertex], discovery[other])

    for vertex in range(graph.order):
        if discovery[vertex] < 0:
            visit(vertex, None)
            assert not edge_stack
    flattened = sorted(edge_id for block in blocks for edge_id in block)
    assert flattened == list(range(len(graph.edges)))
    return tuple(sorted(blocks))


def is_cycle_block(graph: MultiGraph, block: tuple[int, ...]) -> bool:
    if len(block) < 2:
        return False
    block_degrees: dict[int, int] = {}
    for edge_id in block:
        u, v = graph.edges[edge_id]
        block_degrees[u] = block_degrees.get(u, 0) + 1
        block_degrees[v] = block_degrees.get(v, 0) + 1
    return len(block) == len(block_degrees) and set(block_degrees.values()) == {2}


def is_cactus(graph: MultiGraph) -> bool:
    return all(
        len(block) == 1 or is_cycle_block(graph, block)
        for block in edge_blocks(graph)
    )


def cycle_lengths(graph: MultiGraph) -> tuple[int, ...]:
    assert is_cactus(graph)
    return tuple(
        sorted(len(block) for block in edge_blocks(graph) if len(block) > 1)
    )


def line_adjacency(graph: MultiGraph) -> tuple[frozenset[int], ...]:
    adjacency = [set() for _ in graph.edges]
    for left, right in combinations(range(len(graph.edges)), 2):
        if set(graph.edges[left]) & set(graph.edges[right]):
            adjacency[left].add(right)
            adjacency[right].add(left)
    return tuple(frozenset(neighbors) for neighbors in adjacency)


def degeneracy(adjacency: tuple[frozenset[int], ...]) -> int:
    remaining = set(range(len(adjacency)))
    answer = 0
    while remaining:
        vertex = min(
            remaining,
            key=lambda v: (len(adjacency[v] & remaining), v),
        )
        answer = max(answer, len(adjacency[vertex] & remaining))
        remaining.remove(vertex)
    return answer


def predicted_line_degeneracy(graph: MultiGraph) -> int:
    assert is_cactus(graph)
    maximum_degree = max(graph.degrees(), default=0)
    if maximum_degree <= 1:
        return 0
    if maximum_degree == 2:
        return 2 if any(length >= 3 for length in cycle_lengths(graph)) else 1
    return maximum_degree - 1


def audit_graph(graph: MultiGraph) -> None:
    assert is_cactus(graph)
    observed = degeneracy(line_adjacency(graph))
    expected = predicted_line_degeneracy(graph)
    assert observed == expected, (graph, observed, expected, edge_blocks(graph))


def enumerate_simple(max_order: int) -> dict[str, object]:
    counts: dict[str, int] = {}
    degeneracies: dict[str, int] = {}
    tested = 0
    for order in range(1, max_order + 1):
        pairs = tuple(combinations(range(order), 2))
        count = 0
        for mask in range(1 << len(pairs)):
            edges = tuple(pair for bit, pair in enumerate(pairs) if mask >> bit & 1)
            graph = MultiGraph(order, edges)
            if is_cactus(graph):
                audit_graph(graph)
                count += 1
                tested += 1
                key = str(predicted_line_degeneracy(graph))
                degeneracies[key] = degeneracies.get(key, 0) + 1
        counts[str(order)] = count
    return {
        "maximum_order": max_order,
        "labelled_cacti_by_order": counts,
        "line_degeneracy_distribution": dict(sorted(degeneracies.items())),
        "tested": tested,
    }


def enumerate_multigraphs(max_order: int) -> dict[str, object]:
    counts: dict[str, int] = {}
    tested = 0
    for order in range(1, max_order + 1):
        pairs = tuple(combinations(range(order), 2))
        count = 0
        for multiplicities in product(range(3), repeat=len(pairs)):
            edges = tuple(
                pair
                for pair, multiplicity in zip(pairs, multiplicities)
                for _ in range(multiplicity)
            )
            graph = MultiGraph(order, edges)
            if is_cactus(graph):
                audit_graph(graph)
                count += 1
                tested += 1
        counts[str(order)] = count
    return {
        "maximum_order": max_order,
        "pair_multiplicity_range": [0, 2],
        "labelled_cactus_multigraphs_by_order": counts,
        "tested": tested,
    }


def color_even_cycle(lists: tuple[frozenset[int], ...]) -> tuple[int, ...]:
    order = len(lists)
    assert order >= 2 and order % 2 == 0
    assert all(len(available) >= 2 for available in lists)
    colors: list[int | None] = [None] * order
    if all(available == lists[0] for available in lists):
        first, second = sorted(lists[0])[:2]
        return tuple(first if i % 2 == 0 else second for i in range(order))

    start = next(i for i in range(order) if lists[i] != lists[(i + 1) % order])
    next_edge = (start + 1) % order
    colors[start] = min(lists[start] - lists[next_edge])
    for step in range(1, order):
        edge = (start - step) % order
        successor_color = colors[(edge + 1) % order]
        colors[edge] = min(lists[edge] - {successor_color})
    result = tuple(int(color) for color in colors)
    assert all(result[i] in lists[i] for i in range(order))
    assert all(result[i] != result[(i + 1) % order] for i in range(order))
    return result


def audit_even_cycles() -> dict[str, int]:
    two_lists = tuple(frozenset(pair) for pair in combinations(range(4), 2))
    answer: dict[str, int] = {}
    for order in (2, 4, 6):
        count = 0
        for assignment in product(two_lists, repeat=order):
            color_even_cycle(assignment)
            count += 1
        answer[str(order)] = count
    return answer


def audit_explicit_multigraphs() -> list[dict[str, object]]:
    fixtures = {
        "two_digons_at_a_cut_vertex": MultiGraph(
            3, ((0, 1), (0, 1), (1, 2), (1, 2))
        ),
        "triangle_with_leaf_digon": MultiGraph(
            4, ((0, 1), (1, 2), (2, 0), (0, 3), (0, 3))
        ),
        "digon_with_pendant_edge": MultiGraph(3, ((0, 1), (0, 1), (0, 2))),
    }
    answer = []
    for name, graph in fixtures.items():
        audit_graph(graph)
        answer.append(
            {
                "name": name,
                "degrees": list(graph.degrees()),
                "cycle_lengths": list(cycle_lengths(graph)),
                "line_degeneracy": degeneracy(line_adjacency(graph)),
            }
        )
    return answer


def rejection_controls() -> dict[str, bool]:
    triple_edge = MultiGraph(2, ((0, 1), (0, 1), (0, 1)))
    complete_four = MultiGraph(4, tuple(combinations(range(4), 2)))
    result = {
        "triple_parallel_edge_block_rejected": not is_cactus(triple_edge),
        "K4_rejected": not is_cactus(complete_four),
    }
    assert all(result.values())
    return result


def main() -> None:
    result = {
        "claim": "exact line-graph degeneracy of cactus multigraphs",
        "simple_audit": enumerate_simple(6),
        "multigraph_audit": enumerate_multigraphs(5),
        "parallel_edge_fixtures": audit_explicit_multigraphs(),
        "even_cycle_two_list_assignments": audit_even_cycles(),
        "rejection_controls": rejection_controls(),
        "universal_claim_source": "README.md block-cut proof",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
