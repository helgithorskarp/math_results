#!/usr/bin/env python3
"""Audit the structural certificate for K_{1,m} square C_3.

This program does not calculate crossing numbers.  It checks that deleting
specified edges produces subdivisions of K_{3,m} and K_{1,1,1,m}, and audits
all accompanying size and formula identities.
"""

from __future__ import annotations

from collections.abc import Iterable


Vertex = tuple[str, int, int]
Edge = tuple[Vertex, Vertex]


def centre(i: int) -> Vertex:
    return ("c", -1, i)


def leaf(j: int, i: int) -> Vertex:
    return ("x", j, i)


def canonical_edge(u: Vertex, v: Vertex) -> Edge:
    if u == v:
        raise ValueError("loops are not allowed")
    return (u, v) if u < v else (v, u)


def edge_set(edges: Iterable[tuple[Vertex, Vertex]]) -> set[Edge]:
    return {canonical_edge(u, v) for u, v in edges}


def product_graph(m: int) -> tuple[set[Vertex], set[Edge]]:
    """Return K_{1,m} square C_3 with a fixed coordinate labelling."""
    if m < 1:
        raise ValueError("m must be positive")

    vertices = {centre(i) for i in range(3)}
    edges: set[Edge] = set()
    for i in range(3):
        edges.add(canonical_edge(centre(i), centre((i + 1) % 3)))
    for j in range(m):
        vertices.update(leaf(j, i) for i in range(3))
        for i in range(3):
            edges.add(canonical_edge(leaf(j, i), leaf(j, (i + 1) % 3)))
            edges.add(canonical_edge(centre(i), leaf(j, i)))
    return vertices, edges


def subdivision_paths(m: int) -> dict[tuple[Vertex, Vertex], tuple[Vertex, ...]]:
    """Paths giving a subdivision of K_{3,m} inside the product."""
    if m < 1:
        raise ValueError("m must be positive")
    paths: dict[tuple[Vertex, Vertex], tuple[Vertex, ...]] = {}
    for j in range(m):
        branch = leaf(j, 1)
        paths[(branch, centre(0))] = (branch, leaf(j, 0), centre(0))
        paths[(branch, centre(1))] = (branch, centre(1))
        paths[(branch, centre(2))] = (branch, leaf(j, 2), centre(2))
    return paths


def path_edges(path: tuple[Vertex, ...]) -> set[Edge]:
    if len(path) < 2 or len(set(path)) != len(path):
        raise ValueError("path must be simple and nontrivial")
    return edge_set(zip(path, path[1:]))


def crossing_formula(m: int) -> int:
    if m < 1:
        raise ValueError("m must be positive")
    return (m // 2) * ((m - 1) // 2)


def audit_instance(m: int, explicit: bool = True) -> None:
    """Check counts, paths, and (optionally) explicit edge-set identities."""
    if m < 1:
        raise ValueError("m must be positive")

    # Product, K_{3,m} subdivision, and K_{1,1,1,m} subdivision counts.
    assert 3 * (m + 1) == 3 * m + 3
    assert 6 * m + 3 - (m + 3) == 5 * m
    assert 6 * m + 3 - m == 5 * m + 3
    assert (3 * m) + (2 * m) == 5 * m

    # Closed-form parity audit.
    expected = (m * m - 2 * m + (m % 2)) // 4
    assert crossing_formula(m) == expected

    if not explicit:
        return

    vertices, product_edges = product_graph(m)
    assert len(vertices) == 3 * m + 3
    assert len(product_edges) == 6 * m + 3

    centre_triangle = edge_set(
        (centre(i), centre((i + 1) % 3)) for i in range(3)
    )
    deleted_leaf_edges = edge_set(
        (leaf(j, 0), leaf(j, 2)) for j in range(m)
    )
    k3m_subdivision = product_edges - centre_triangle - deleted_leaf_edges
    k111m_subdivision = product_edges - deleted_leaf_edges

    paths = subdivision_paths(m)
    assert len(paths) == 3 * m

    branch_vertices = {centre(i) for i in range(3)} | {
        leaf(j, 1) for j in range(m)
    }
    internal_seen: set[Vertex] = set()
    path_edge_union: set[Edge] = set()
    for (start, end), path in paths.items():
        assert path[0] == start and path[-1] == end
        assert start in branch_vertices and end in branch_vertices
        internal = set(path[1:-1])
        assert internal.isdisjoint(branch_vertices)
        assert internal.isdisjoint(internal_seen)
        internal_seen.update(internal)
        edges = path_edges(path)
        assert edges <= product_edges
        assert path_edge_union.isdisjoint(edges)
        path_edge_union.update(edges)

    expected_internal = {
        leaf(j, i) for j in range(m) for i in (0, 2)
    }
    assert internal_seen == expected_internal
    assert path_edge_union == k3m_subdivision
    assert len(k3m_subdivision) == 5 * m
    assert k111m_subdivision == path_edge_union | centre_triangle
    assert len(k111m_subdivision) == 5 * m + 3


def main() -> None:
    explicit_values = list(range(1, 65)) + [100, 127, 256, 511, 1000]
    for m in explicit_values:
        audit_instance(m, explicit=True)
    for m in range(1, 10001):
        audit_instance(m, explicit=False)

    m = 10000
    print("star-triangle product structural audit")
    print("formula instances checked: 10000")
    print("explicit subdivision instances checked: 69")
    print("parameter range: 1 <= m <= 10000")
    print(f"largest product counts: vertices={3*m+3}, edges={6*m+3}")
    print(f"largest K3m-subdivision counts: vertices={3*m+3}, edges={5*m}")
    print(f"crossing formula at m=10000: {crossing_formula(m)}")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
