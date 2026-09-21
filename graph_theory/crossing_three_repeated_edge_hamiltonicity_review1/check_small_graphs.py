#!/usr/bin/env python3
"""Definition-level census for the relative projective-planar theorem.

For n <= 6 every simple graph is projective-planar because it is a
subgraph of K_6.  We enumerate every labelled graph G on 5 and 6 vertices,
retain the 4-connected ones, and check for every edge xy of G that G-xy has
a Hamiltonian x--y path.  Equivalently, every edge of G lies on a
Hamiltonian cycle.

The checker uses only Python integers and exhaustive permutations.  Graph
mask bit i corresponds to EDGES[n][i], in lexicographic pair order.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import platform
from collections import Counter


def edge_list(n: int) -> tuple[tuple[int, int], ...]:
    return tuple(itertools.combinations(range(n), 2))


def adjacency(n: int, mask: int) -> tuple[int, ...]:
    adj = [0] * n
    for bit, (u, v) in enumerate(edge_list(n)):
        if mask >> bit & 1:
            adj[u] |= 1 << v
            adj[v] |= 1 << u
    return tuple(adj)


def connected_after_deleting(adj: tuple[int, ...], deleted: int) -> bool:
    alive = ((1 << len(adj)) - 1) & ~deleted
    if alive == 0:
        return True
    reached = alive & -alive
    frontier = reached
    while frontier:
        vertex_bit = frontier & -frontier
        frontier ^= vertex_bit
        vertex = vertex_bit.bit_length() - 1
        new = adj[vertex] & alive & ~reached
        reached |= new
        frontier |= new
    return reached == alive


def is_k_connected(adj: tuple[int, ...], k: int) -> bool:
    n = len(adj)
    if n <= k:
        return False
    vertices = range(n)
    for size in range(k):
        for removed in itertools.combinations(vertices, size):
            deleted = sum(1 << v for v in removed)
            if not connected_after_deleting(adj, deleted):
                return False
    return True


def vertex_connectivity(adj: tuple[int, ...]) -> int:
    """Return the usual vertex connectivity for a noncomplete graph."""
    n = len(adj)
    for size in range(n - 1):
        for removed in itertools.combinations(range(n), size):
            deleted = sum(1 << v for v in removed)
            if not connected_after_deleting(adj, deleted):
                return size
    return n - 1


def hamilton_path_witness(
    adj: tuple[int, ...], x: int, y: int
) -> tuple[int, ...] | None:
    middle = tuple(v for v in range(len(adj)) if v not in (x, y))
    for order in itertools.permutations(middle):
        path = (x,) + order + (y,)
        if all(adj[u] >> v & 1 for u, v in zip(path, path[1:])):
            return path
    return None


def valid_path(adj: tuple[int, ...], x: int, y: int, path: tuple[int, ...]) -> bool:
    return (
        len(path) == len(adj)
        and path[0] == x
        and path[-1] == y
        and set(path) == set(range(len(adj)))
        and all(adj[u] >> v & 1 for u, v in zip(path, path[1:]))
    )


def run_census() -> dict[str, object]:
    digest = hashlib.sha256()
    by_order: dict[str, dict[str, int]] = {}
    h_connectivity = Counter()
    failures: list[dict[str, int]] = []

    for n in (5, 6):
        edges = edge_list(n)
        graphs_4_connected = 0
        edge_instances = 0
        for mask in range(1 << len(edges)):
            adj_g = adjacency(n, mask)
            if not is_k_connected(adj_g, 4):
                continue
            graphs_4_connected += 1
            for edge_index, (x, y) in enumerate(edges):
                if not (mask >> edge_index & 1):
                    continue
                edge_instances += 1
                h_mask = mask ^ (1 << edge_index)
                adj_h = adjacency(n, h_mask)
                kappa_h = vertex_connectivity(adj_h)
                h_connectivity[kappa_h] += 1
                witness = hamilton_path_witness(adj_h, x, y)
                if witness is None:
                    failures.append(
                        {"n": n, "graph_mask": mask, "edge_index": edge_index}
                    )
                    witness_text = "NONE"
                else:
                    assert valid_path(adj_h, x, y, witness)
                    witness_text = ",".join(map(str, witness))
                record = f"{n}|{mask}|{edge_index}|{kappa_h}|{witness_text}\n"
                digest.update(record.encode("ascii"))
        by_order[str(n)] = {
            "labelled_graphs": 1 << len(edges),
            "four_connected_graphs": graphs_4_connected,
            "tested_edge_instances": edge_instances,
        }

    # Hand-auditable boundary fixtures and rejection check.
    fixtures: dict[str, dict[str, object]] = {}
    for n in (5, 6):
        complete_mask = (1 << len(edge_list(n))) - 1
        edge_index = 0  # edge (0,1)
        h_mask = complete_mask ^ (1 << edge_index)
        adj_h = adjacency(n, h_mask)
        witness = hamilton_path_witness(adj_h, 0, 1)
        assert witness is not None and valid_path(adj_h, 0, 1, witness)
        fixtures[f"K{n}_minus_edge"] = {
            "vertex_connectivity": vertex_connectivity(adj_h),
            "hamilton_path": list(witness),
            "planarity_by_edge_bound": (
                "nonplanar" if n == 6 and len(edge_list(n)) - 1 > 3 * n - 6 else "not_decided"
            ),
        }
    bad_path = (0, 2, 3, 2, 1)  # correct ends, but repeats 2 and omits 4
    adj_k5_minus_01 = adjacency(5, (1 << len(edge_list(5))) - 2)
    assert not valid_path(adj_k5_minus_01, 0, 1, bad_path)

    # A definition-level certificate for the one topological census premise:
    # these ten triangular faces make K_6 a closed triangulated surface of
    # Euler characteristic 1, hence a projective-plane triangulation.
    k6_faces = (
        (0, 1, 2), (0, 1, 3), (0, 2, 4), (0, 3, 5), (0, 4, 5),
        (1, 2, 5), (1, 3, 4), (1, 4, 5), (2, 3, 4), (2, 3, 5),
    )
    face_edge_counts = Counter(
        tuple(sorted(edge))
        for face in k6_faces
        for edge in itertools.combinations(face, 2)
    )
    assert set(face_edge_counts) == set(edge_list(6))
    assert set(face_edge_counts.values()) == {2}
    link_degrees: dict[int, Counter[int]] = {}
    for vertex in range(6):
        degrees: Counter[int] = Counter()
        link_edges = []
        for face in k6_faces:
            if vertex in face:
                edge = tuple(v for v in face if v != vertex)
                link_edges.append(edge)
                degrees.update(edge)
        assert len(link_edges) == 5 and set(degrees.values()) == {2}
        reached = {link_edges[0][0]}
        changed = True
        while changed:
            changed = False
            for u, v in link_edges:
                if u in reached and v not in reached:
                    reached.add(v)
                    changed = True
                if v in reached and u not in reached:
                    reached.add(u)
                    changed = True
        assert len(reached) == 5
        link_degrees[vertex] = degrees

    return {
        "python": platform.python_version(),
        "representation": "labelled vertices 0..n-1; lexicographic edge-mask bits",
        "orders": by_order,
        "H_vertex_connectivity_distribution": {
            str(k): h_connectivity[k] for k in sorted(h_connectivity)
        },
        "fixtures": fixtures,
        "K6_projective_triangulation": {
            "faces": [list(face) for face in k6_faces],
            "each_edge_face_incidence": 2,
            "each_vertex_link": "connected 5-cycle",
            "euler_characteristic": 6 - 15 + len(k6_faces),
        },
        "failures": failures,
        "entrywise_sha256": digest.hexdigest(),
    }


if __name__ == "__main__":
    print(json.dumps(run_census(), indent=2, sort_keys=True))
