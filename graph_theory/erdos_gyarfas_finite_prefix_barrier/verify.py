#!/usr/bin/env python3
"""Exact checker for the order-78 finite-prefix barrier instance.

Only the Python standard library is used.  The universal result is proved in
THEOREM.md; this program audits all definitions on the canonical expansion of
the point-line incidence graph of PG(2,3).
"""

from __future__ import annotations

from collections import deque
from hashlib import sha256
from itertools import product
from typing import Iterable

Adjacency = dict[int, set[int]]
Edge = tuple[int, int]


def require(condition: bool, message: str) -> None:
    """A check that remains active under ``python -O``."""
    if not condition:
        raise RuntimeError(message)


def normalized_projective_vectors() -> list[tuple[int, int, int]]:
    """Return the 13 normalized nonzero vectors in F_3^3."""
    answer: list[tuple[int, int, int]] = []
    for vector in product(range(3), repeat=3):
        if vector == (0, 0, 0):
            continue
        first = next(x for x in vector if x)
        inverse = 1 if first == 1 else 2
        normalized = tuple((inverse * x) % 3 for x in vector)
        if normalized not in answer:
            answer.append(normalized)
    return sorted(answer)


def projective_plane_incidence_graph() -> Adjacency:
    """Build the Levi graph of PG(2,3), with points 0..12 and lines 13..25."""
    vectors = normalized_projective_vectors()
    graph: Adjacency = {v: set() for v in range(26)}
    for point_index, point in enumerate(vectors):
        for line_index, line in enumerate(vectors):
            if sum(x * y for x, y in zip(point, line)) % 3 == 0:
                u, v = point_index, 13 + line_index
                graph[u].add(v)
                graph[v].add(u)
    return graph


def edges(graph: Adjacency) -> list[Edge]:
    return [(u, v) for u in sorted(graph) for v in sorted(graph[u]) if u < v]


def connected(graph: Adjacency) -> bool:
    if not graph:
        return True
    seen = {min(graph)}
    todo = list(seen)
    while todo:
        u = todo.pop()
        for v in graph[u]:
            if v not in seen:
                seen.add(v)
                todo.append(v)
    return len(seen) == len(graph)


def deterministic_euler_orientation(graph: Adjacency) -> list[Edge]:
    """Orient the edges along a deterministic Euler circuit.

    Each returned pair is (tail, head).  Sorted neighbor choices make the
    output—and hence the certificate digest—platform independent.
    """
    if not graph or not connected(graph) or any(len(graph[v]) % 2 for v in graph):
        raise ValueError("Euler orientation requires a connected even graph")

    unused = {frozenset((u, v)) for u, v in edges(graph)}
    stack = [min(graph)]
    reverse_circuit: list[int] = []
    while stack:
        u = stack[-1]
        available = sorted(v for v in graph[u] if frozenset((u, v)) in unused)
        if available:
            v = available[0]
            unused.remove(frozenset((u, v)))
            stack.append(v)
        else:
            reverse_circuit.append(stack.pop())
    if unused:
        raise RuntimeError("Euler traversal left unused edges")
    circuit = list(reversed(reverse_circuit))
    return list(zip(circuit, circuit[1:]))


def strongly_connected(vertices: Iterable[int], arcs: list[Edge]) -> bool:
    vertices = list(vertices)
    out = {v: set() for v in vertices}
    rev = {v: set() for v in vertices}
    for u, v in arcs:
        out[u].add(v)
        rev[v].add(u)

    def reachable(graph: Adjacency) -> set[int]:
        seen = {vertices[0]}
        todo = list(seen)
        while todo:
            for v in graph[todo.pop()]:
                if v not in seen:
                    seen.add(v)
                    todo.append(v)
        return seen

    return bool(vertices) and len(reachable(out)) == len(vertices) == len(reachable(rev))


def eulerian_triangle_expansion(
    base: Adjacency, arcs: list[Edge]
) -> tuple[Adjacency, dict[Edge, int], set[Edge]]:
    """Build X(K).

    Base vertices retain their labels.  The edge-vertex for the i-th sorted
    base edge receives label |V(K)|+i.  The final return value is the set of
    transition matching edges.
    """
    n = len(base)
    base_edges = edges(base)
    edge_vertex = {edge: n + i for i, edge in enumerate(base_edges)}
    expansion: Adjacency = {v: set() for v in range(n + len(base_edges))}

    def add_edge(u: int, v: int) -> None:
        expansion[u].add(v)
        expansion[v].add(u)

    for (u, v), a in edge_vertex.items():
        add_edge(a, u)
        add_edge(a, v)

    incoming = {v: [] for v in base}
    for tail, head in arcs:
        incoming[head].append(edge_vertex[tuple(sorted((tail, head)))])
    matching: set[Edge] = set()
    for v in sorted(base):
        if len(incoming[v]) != 2:
            raise ValueError("orientation is not two-in at every base vertex")
        a, b = sorted(incoming[v])
        add_edge(a, b)
        matching.add((a, b))
    return expansion, edge_vertex, matching


def canonical_cycle(cycle: tuple[int, ...]) -> tuple[int, ...]:
    rotations = []
    for direction in (cycle, tuple(reversed(cycle))):
        rotations.extend(direction[i:] + direction[:i] for i in range(len(cycle)))
    return min(rotations)


def cycles_of_length(graph: Adjacency, length: int) -> set[tuple[int, ...]]:
    """Enumerate undirected simple cycles of one exact length."""
    found: set[tuple[int, ...]] = set()
    for start in sorted(graph):
        path = [start]
        used = {start}

        def search(u: int) -> None:
            if len(path) == length:
                if start in graph[u]:
                    found.add(canonical_cycle(tuple(path)))
                return
            # The minimum-label convention avoids exploring cycles whose
            # canonical start would be a different vertex.
            for v in sorted(graph[u]):
                if v > start and v not in used:
                    used.add(v)
                    path.append(v)
                    search(v)
                    path.pop()
                    used.remove(v)

        search(start)
    return found


def girth_at_most(graph: Adjacency, cutoff: int) -> int | None:
    for length in range(3, cutoff + 1):
        if cycles_of_length(graph, length):
            return length
    return None


def three_core_vertices(graph: Adjacency, omitted_edge: Edge | None = None) -> set[int]:
    """Return the vertices left after repeatedly deleting degree-at-most-2 vertices."""
    remaining = set(graph)
    degree = {}
    omitted = frozenset(omitted_edge) if omitted_edge is not None else None
    for u in graph:
        degree[u] = sum(frozenset((u, v)) != omitted for v in graph[u])
    queue = deque(v for v in graph if degree[v] <= 2)
    while queue:
        u = queue.popleft()
        if u not in remaining:
            continue
        remaining.remove(u)
        for v in graph[u]:
            if v in remaining and frozenset((u, v)) != omitted:
                degree[v] -= 1
                if degree[v] == 2:
                    queue.append(v)
    return remaining


def certificate_lines() -> list[str]:
    base = projective_plane_incidence_graph()
    base_edges = edges(base)
    arcs = deterministic_euler_orientation(base)
    expansion, edge_vertex, matching = eulerian_triangle_expansion(base, arcs)
    expansion_edges = edges(expansion)

    require(len(base) == 26 and len(base_edges) == 52, "wrong base order or size")
    require(connected(base) and set(map(len, base.values())) == {4}, "base is not connected 4-regular")
    require(girth_at_most(base, 6) == 6, "base girth is not six")

    indegree = {v: 0 for v in base}
    outdegree = {v: 0 for v in base}
    for tail, head in arcs:
        outdegree[tail] += 1
        indegree[head] += 1
    require(set(indegree.values()) == {2} == set(outdegree.values()), "orientation is not balanced")
    require(strongly_connected(base, arcs), "orientation is not strongly connected")

    n = len(base)
    a_vertices = set(range(n, len(expansion)))
    b_vertices = set(range(n))
    require(len(expansion) == 78 and len(expansion_edges) == 130, "wrong expansion order or size")
    require({len(expansion[v]) for v in a_vertices} == {3}, "an A-vertex is not cubic")
    require({len(expansion[v]) for v in b_vertices} == {4}, "a B-vertex is not quartic")
    require(all(not (expansion[v] & b_vertices) for v in b_vertices), "B is not independent")
    induced_a_edges = {(u, v) for u, v in expansion_edges if u in a_vertices and v in a_vertices}
    require(induced_a_edges == matching and len(matching) == 26, "A does not induce the matching")
    require({u for edge in matching for u in edge} == a_vertices, "the A-matching is not perfect")
    for u, v in matching:
        common_b = expansion[u] & expansion[v] & b_vertices
        require(len(common_b) == 1, "a transition pair lacks a unique B-closer")

    cycle_counts = {length: len(cycles_of_length(expansion, length)) for length in range(3, 9)}
    require(cycle_counts == {3: 26, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}, "wrong short-cycle profile")

    require(three_core_vertices(expansion) == set(expansion), "the expansion itself lacks full 3-core")
    deletion_failures = [edge for edge in expansion_edges if three_core_vertices(expansion, edge)]
    require(not deletion_failures, "an edge deletion retains a nonempty 3-core")

    digest_material = "\n".join(
        [*(f"K {u} {v}" for u, v in base_edges), *(f"D {u} {v}" for u, v in arcs),
         *(f"X {u} {v}" for u, v in expansion_edges)]
    ).encode()
    digest = sha256(digest_material).hexdigest()

    # The dictionary is intentionally referenced here: checking its range also
    # verifies that every one of the 52 base edges received one A-vertex.
    require(set(edge_vertex.values()) == a_vertices, "base-edge/A-vertex bijection failed")
    return [
        "base: vertices=26 edges=52 regular_degree=4 girth=6",
        "orientation: indegree=2 outdegree=2 strongly_connected=yes",
        "expansion: vertices=78 edges=130 degree3=52 degree4=26",
        "equality: B_independent=yes A_matching=26 unique_closers=yes",
        "cycles: C3=26 C4=0 C5=0 C6=0 C7=0 C8=0",
        "criticality: all_130_single_edge_deletions_have_empty_3_core=yes",
        f"certificate_sha256={digest}",
        "ALL CHECKS PASSED",
    ]


def main() -> None:
    print("\n".join(certificate_lines()))


if __name__ == "__main__":
    main()
