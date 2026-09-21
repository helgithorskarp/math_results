#!/usr/bin/env python3
"""Exact audit of the five-exception elimination.

The universal argument is in THEOREM.md.  This program verifies the primary
Figure-1 transcription, computes frustration directly, and checks every
canonical oriented triangle-side gluing.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from typing import Iterable

Edge = tuple[int, int]
Facet = tuple[int, int, int]
SIDE = ((0, 1), (1, 2), (2, 0))


EXCEPTIONS = {
    "Gamma1": {
        "n": 4,
        "positive": ((2, 3), (1, 3), (0, 1), (0, 2)),
        "negative": ((1, 2), (0, 3)),
        "frustration": 2,
    },
    "Gamma2": {
        "n": 5,
        "positive": ((2, 3), (1, 3), (0, 1), (0, 2), (2, 4)),
        "negative": ((1, 4), (0, 3)),
        "frustration": 2,
    },
    "Gamma3": {
        "n": 8,
        "positive": ((1, 2), (2, 3), (3, 4), (4, 5), (1, 6),
                     (0, 2), (0, 6), (3, 7), (5, 7)),
        "negative": ((5, 6), (0, 1), (4, 7)),
        "frustration": 3,
    },
    "Gamma4": {
        "n": 8,
        "positive": ((1, 2), (2, 3), (4, 5), (1, 5), (3, 6), (4, 6),
                     (0, 1), (0, 7), (6, 7)),
        "negative": ((0, 2), (3, 4), (5, 7)),
        "frustration": 3,
    },
    "Gamma5": {
        "n": 8,
        "positive": ((0, 1), (1, 2), (2, 3),
                     (4, 5), (5, 6), (4, 7),
                     (0, 4), (2, 6), (3, 7)),
        "negative": ((0, 3), (6, 7), (1, 5)),
        "frustration": 3,
    },
}

MOBIUS = ((0, 1, 2), (0, 1, 3), (0, 2, 4), (1, 3, 4), (2, 3, 4))
PROJECTIVE_PLANE = (
    (0, 1, 2), (0, 1, 3), (0, 2, 4), (0, 3, 5), (0, 4, 5),
    (1, 2, 5), (1, 3, 4), (1, 4, 5), (2, 3, 4), (2, 3, 5),
)
TETRAHEDRON = tuple(itertools.combinations(range(4), 3))


def normalize_graph(spec):
    n = spec["n"]
    positive = {tuple(sorted(edge)) for edge in spec["positive"]}
    negative = {tuple(sorted(edge)) for edge in spec["negative"]}
    assert positive.isdisjoint(negative)
    edges = positive | negative
    assert all(0 <= u < v < n for u, v in edges)
    neighbors = [[] for _ in range(n)]
    for u, v in sorted(edges):
        neighbors[u].append(v)
        neighbors[v].append(u)
    assert all(2 <= len(row) <= 3 for row in neighbors)
    return n, positive, negative, tuple(tuple(row) for row in neighbors)


def edge_frustration(n: int, edges: Iterable[Edge], negative: set[Edge]) -> int:
    edges = tuple(sorted(tuple(sorted(edge)) for edge in edges))
    return min(
        sum((((mask >> u) ^ (mask >> v)) & 1) != int((u, v) in negative)
            for u, v in edges)
        for mask in range(1 << n)
    )


def facet_data(facets: Iterable[Facet]):
    facets = tuple(sorted(tuple(sorted(facet)) for facet in facets))
    assert facets and all(len(set(facet)) == 3 for facet in facets)
    assert len(facets) == len(set(facets))
    incidence: dict[Edge, list[tuple[int, int]]] = {}
    for i, (a, b, c) in enumerate(facets):
        # Boundary orientation a->b->c->a for a<b<c.
        for edge, start in (((a, b), a), ((b, c), b), ((a, c), c)):
            incidence.setdefault(edge, []).append((i, start))
    assert max(map(len, incidence.values())) <= 2
    dual_edges = set()
    negative = set()
    boundary = []
    for edge, entries in incidence.items():
        if len(entries) == 1:
            boundary.append(edge)
            continue
        (left, start_left), (right, start_right) = entries
        dual = tuple(sorted((left, right)))
        dual_edges.add(dual)
        if start_left == start_right:
            negative.add(dual)
    return facets, dual_edges, negative, tuple(sorted(boundary))


def boundary_even(facets: Iterable[Facet]) -> bool:
    _, _, _, boundary = facet_data(facets)
    degrees = Counter(vertex for edge in boundary for vertex in edge)
    return all(value % 2 == 0 for value in degrees.values())


def connected_after_deleting_edge(n: int, edges: set[Edge], deleted: Edge | None) -> bool:
    adjacency = [set() for _ in range(n)]
    for edge in edges:
        if edge == deleted:
            continue
        u, v = edge
        adjacency[u].add(v)
        adjacency[v].add(u)
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbor in adjacency[vertex] - seen:
            seen.add(neighbor)
            stack.append(neighbor)
    return len(seen) == n


def is_two_edge_connected(n: int, edges: set[Edge]) -> bool:
    return connected_after_deleting_edge(n, edges, None) and all(
        connected_after_deleting_edge(n, edges, edge) for edge in edges
    )


class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))

    def find(self, vertex: int) -> int:
        while self.parent[vertex] != vertex:
            self.parent[vertex] = self.parent[self.parent[vertex]]
            vertex = self.parent[vertex]
        return vertex

    def union(self, left: int, right: int) -> None:
        left, right = self.find(left), self.find(right)
        if left != right:
            self.parent[right] = left


def gluing_quotient(parsed, assignments):
    n, positive, negative, neighbors = parsed
    side_at = {}
    for vertex, (row, selected) in enumerate(zip(neighbors, assignments)):
        side_at.update({(vertex, neighbor): side for neighbor, side in zip(row, selected)})
    union = UnionFind(3 * n)
    for left, right in sorted(positive | negative):
        a0, a1 = SIDE[side_at[(left, right)]]
        b0, b1 = SIDE[side_at[(right, left)]]
        pairings = ((a0, b0), (a1, b1)) if (left, right) in negative else ((a0, b1), (a1, b0))
        for a, b in pairings:
            union.union(3 * left + a, 3 * right + b)
    facets = tuple(
        frozenset(union.find(3 * vertex + corner) for corner in range(3))
        for vertex in range(n)
    )
    if any(len(facet) != 3 for facet in facets) or len(set(facets)) != n:
        return None
    dual_edges = positive | negative
    for left in range(n):
        for right in range(left + 1, n):
            overlap = len(facets[left] & facets[right])
            if (left, right) in dual_edges:
                if overlap != 2:
                    return None
            elif overlap > 1:
                return None
    return facets


def canonical_gluing_scan(spec):
    parsed = normalize_graph(spec)
    n, _, _, neighbors = parsed
    choices = []
    for row in neighbors:
        # Six injections before symmetry reduction.  Cyclic rotations of a
        # facet preserve its oriented edge directions.  Fix the first
        # neighbor to side zero, leaving two exact orbit representatives.
        local = tuple(
            assignment for assignment in itertools.permutations(range(3), len(row))
            if assignment[0] == 0
        )
        assert len(local) == 2
        choices.append(local)
    accepted = 0
    for assignments in itertools.product(*choices):
        accepted += int(gluing_quotient(parsed, assignments) is not None)
    canonical = 2**n
    raw = 6**n
    assert canonical * 3**n == raw
    return raw, canonical, accepted


def spec_from_facets(facets: Iterable[Facet]):
    facets, edges, negative, _ = facet_data(facets)
    return {
        "n": len(facets),
        "positive": tuple(sorted(edges - negative)),
        "negative": tuple(sorted(negative)),
    }


def minimum_surface_bound() -> int:
    # Search the numerical consequences used in Lemma 2.  A closed
    # nonorientable surface has chi<=1, 3f=2e, and a simple 1-skeleton.
    feasible = []
    for vertices in range(2, 30):
        for chi in range(-20, 2):
            facets = 2 * (vertices - chi)
            edges = 3 * facets // 2
            if edges <= vertices * (vertices - 1) // 2:
                feasible.append(facets)
    return min(feasible)


def audit_exceptions():
    rows = {}
    for name, spec in EXCEPTIONS.items():
        n, positive, negative, neighbors = normalize_graph(spec)
        edges = positive | negative
        frustration = edge_frustration(n, edges, negative)
        assert frustration == spec["frustration"]
        boundary_count = 3 * n - 2 * len(edges)
        degrees = tuple(sorted(map(len, neighbors), reverse=True))
        if name == "Gamma2":
            assert boundary_count == 1 and degrees == (3, 3, 3, 3, 2)
        else:
            assert boundary_count == 0 and set(degrees) == {3} and n in (4, 8)
        raw, canonical, accepted = canonical_gluing_scan(spec)
        assert accepted == 0
        rows[name] = {
            "vertices": n,
            "edges": len(edges),
            "degrees": degrees,
            "frustration": frustration,
            "forced_boundary_edges": boundary_count,
            "raw_gluings": raw,
            "canonical_gluings": canonical,
            "accepted": accepted,
        }
    return rows


def audit_positive_controls():
    result = {}
    for name, facets, expected_kappa in (
        ("tetrahedron", TETRAHEDRON, 0),
        ("mobius_five", MOBIUS, 1),
        ("projective_plane", PROJECTIVE_PLANE, 3),
    ):
        facets, dual, negative, boundary = facet_data(facets)
        kappa = edge_frustration(len(facets), dual, negative)
        assert kappa == expected_kappa and boundary_even(facets)
        assert is_two_edge_connected(len(facets), dual)
        raw, canonical, accepted = canonical_gluing_scan(spec_from_facets(facets))
        assert accepted > 0
        result[name] = {
            "facets": len(facets),
            "dual_edges": len(dual),
            "boundary_edges": len(boundary),
            "kappa": kappa,
            "packing": 3 * len(facets) - kappa,
            "cover": 3 * len(facets),
            "canonical_gluings": canonical,
            "accepted_gluings": accepted,
        }
    return result


def main() -> None:
    result = {
        "minimum_closed_nonorientable_facets": minimum_surface_bound(),
        "exceptions": audit_exceptions(),
        "positive_controls": audit_positive_controls(),
    }
    assert result["minimum_closed_nonorientable_facets"] == 10
    certificate = hashlib.sha256(
        json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    print("minimum_closed_nonorientable_facets=10")
    for name, row in result["exceptions"].items():
        print(
            f"{name}: n={row['vertices']} m={row['edges']} F={row['frustration']} "
            f"boundary={row['forced_boundary_edges']} canonical={row['canonical_gluings']} "
            f"accepted={row['accepted']}"
        )
    for name, row in result["positive_controls"].items():
        print(
            f"{name}: f={row['facets']} kappa={row['kappa']} "
            f"packing={row['packing']} cover={row['cover']} "
            f"accepted={row['accepted_gluings']}"
        )
    print(f"certificate_sha256={certificate}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
