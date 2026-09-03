#!/usr/bin/env python3
"""Direct adjacency-list and BFS audit of the tree-stacking counterexample."""

from collections import deque
from math import comb


Graph = dict[str, set[str]]


def add_edge(graph: Graph, u: str, v: str) -> None:
    graph.setdefault(u, set()).add(v)
    graph.setdefault(v, set()).add(u)


def branched_broom(d: int, e: int, t: int) -> Graph:
    graph: Graph = {}
    path = ["p"] + [f"v{j}" for j in range(1, t)] + ["q"]
    for u, v in zip(path, path[1:]):
        add_edge(graph, u, v)
    for i in range(d):
        add_edge(graph, "p", f"left_leaf_{i}")
    for i in range(e):
        add_edge(graph, "q", f"arm_{i}")
        add_edge(graph, f"arm_{i}", f"arm_leaf_{i}")
    return graph


def symmetric_double_broom(a: int, ell: int) -> Graph:
    graph: Graph = {}
    path = ["p"] + [f"v{j}" for j in range(1, ell)] + ["q"]
    for u, v in zip(path, path[1:]):
        add_edge(graph, u, v)
    for i in range(a):
        add_edge(graph, "p", f"left_leaf_{i}")
        add_edge(graph, "q", f"right_leaf_{i}")
    return graph


def distances(graph: Graph, source: str) -> dict[str, int]:
    distance = {source: 0}
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if v not in distance:
                distance[v] = distance[u] + 1
                queue.append(v)
    assert len(distance) == len(graph)
    return distance


def validate_tree(graph: Graph) -> None:
    edge_count = sum(map(len, graph.values())) // 2
    assert edge_count == len(graph) - 1
    distances(graph, next(iter(graph)))


def critical_multiplicity(graph: Graph) -> tuple[int, int, dict[str, int]]:
    """Evaluate N(T) directly from leaf distances and sibling classes."""
    validate_tree(graph)
    leaves = [v for v in graph if len(graph[v]) == 1]
    nonleaves = [v for v in graph if len(graph[v]) > 1]

    leaf_potential: dict[str, int] = {}
    for leaf in leaves:
        distance = distances(graph, leaf)
        # For a graph leaf z, X(z)=sum deg(u)*2^(dist(z,u)-1).
        leaf_potential[leaf] = sum(
            len(graph[u]) * 2 ** (distance[u] - 1) for u in nonleaves
        )

    maximum = max(leaf_potential.values())
    maximizing_parents = {
        next(iter(graph[leaf]))
        for leaf, value in leaf_potential.items()
        if value == maximum
    }

    parent_potential: dict[str, int] = {}
    total = 0
    for parent in maximizing_parents:
        child_leaves = [v for v in graph[parent] if len(graph[v]) == 1]
        values = {leaf_potential[v] for v in child_leaves}
        assert values == {maximum}
        d_parent = len(child_leaves)
        parent_potential[parent] = maximum
        total += comb(maximum + d_parent - 1, d_parent - 1)
    return total, maximum, parent_potential


def main() -> None:
    candidate_graph = branched_broom(8, 4, 6)
    assert len(candidate_graph) == 23
    candidate, maximum, parents = critical_multiplicity(candidate_graph)
    assert maximum == 1477
    assert parents == {"p": 1477}
    assert candidate == 3_100_645_395_776_119_256

    rows: list[tuple[int, int, int]] = []
    for a in range(1, 11):
        ell = 22 - 2 * a
        graph = symmetric_double_broom(a, ell)
        assert len(graph) == 23
        value, _, maximizing_parents = critical_multiplicity(graph)
        assert set(maximizing_parents) == {"p", "q"}
        rows.append((a, ell, value))

    best = max(rows, key=lambda row: row[2])
    assert best == (6, 10, 1_111_665_975_462_168_688)
    difference = candidate - best[2]
    assert difference == 1_988_979_420_313_950_568

    print("a ell N_from_adjacency_and_BFS")
    for row in rows:
        print(*row)
    print(f"candidate_order={len(candidate_graph)}")
    print(f"candidate_maximum_leaf_potential={maximum}")
    print(f"candidate_maximizing_parents={sorted(parents)}")
    print(f"candidate_N={candidate}")
    print(f"best_symmetric_parameters=({best[0]},{best[0]},{best[1]})")
    print(f"best_symmetric_N={best[2]}")
    print(f"difference={difference}")
    print("status=VERIFIED")


if __name__ == "__main__":
    main()
