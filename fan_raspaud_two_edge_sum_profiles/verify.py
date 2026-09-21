#!/usr/bin/env python3
"""Definition-level audit for 2-edge-sum FR boundary profiles.

No external packages are used.  Edges have stable string identifiers so the
code also handles parallel edges, although the three fixtures are simple.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
import json
from typing import Hashable, Iterable


Vertex = Hashable
Matching = frozenset[str]
Triple = tuple[Matching, Matching, Matching]
INF = None  # JSON representation of infinity in a profile.


@dataclass(frozen=True)
class Graph:
    name: str
    vertices: tuple[Vertex, ...]
    edges: dict[str, tuple[Vertex, Vertex]]

    def check(self) -> None:
        vertex_set = set(self.vertices)
        assert len(vertex_set) == len(self.vertices)
        for edge_id, (u, v) in self.edges.items():
            assert isinstance(edge_id, str) and u in vertex_set and v in vertex_set
            assert u != v
        degrees = {v: 0 for v in self.vertices}
        for u, v in self.edges.values():
            degrees[u] += 1
            degrees[v] += 1
        assert set(degrees.values()) == {3}, (self.name, degrees)


def k4() -> tuple[Graph, str]:
    vertices = tuple(range(4))
    edges = {
        f"e{i}{j}": (i, j)
        for i in range(4)
        for j in range(i + 1, 4)
    }
    graph = Graph("K4", vertices, edges)
    graph.check()
    return graph, "e01"


def petersen() -> tuple[Graph, str]:
    vertices = tuple(range(10))
    edges: dict[str, tuple[int, int]] = {}
    for i in range(5):
        edges[f"o{i}"] = (i, (i + 1) % 5)
        edges[f"s{i}"] = (i, 5 + i)
        j = (i + 2) % 5
        edge_name = f"i{min(i, j)}{max(i, j)}"
        edges[edge_name] = (5 + i, 5 + j)
    graph = Graph("Petersen", vertices, edges)
    graph.check()
    return graph, "s0"


def perfect_matchings(graph: Graph) -> tuple[Matching, ...]:
    incident: dict[Vertex, list[tuple[str, Vertex]]] = {
        v: [] for v in graph.vertices
    }
    for edge_id, (u, v) in graph.edges.items():
        incident[u].append((edge_id, v))
        incident[v].append((edge_id, u))
    for entries in incident.values():
        entries.sort()

    answer: list[Matching] = []

    def extend(unmatched: frozenset[Vertex], chosen: tuple[str, ...]) -> None:
        if not unmatched:
            answer.append(frozenset(chosen))
            return
        vertex = min(unmatched, key=repr)
        for edge_id, other in incident[vertex]:
            if other in unmatched:
                extend(unmatched - {vertex, other}, chosen + (edge_id,))

    extend(frozenset(graph.vertices), ())
    unique = sorted(set(answer), key=lambda matching: tuple(sorted(matching)))
    for matching in unique:
        covered: list[Vertex] = []
        for edge_id in matching:
            covered.extend(graph.edges[edge_id])
        assert len(covered) == len(graph.vertices)
        assert set(covered) == set(graph.vertices)
    return tuple(unique)


def is_regular(triple: Triple) -> bool:
    return not (triple[0] & triple[1] & triple[2])


def support(triple: Triple, marker: str) -> tuple[int, ...]:
    return tuple(i for i, matching in enumerate(triple) if marker in matching)


def uncovered(graph: Graph, triple: Triple) -> int:
    return len(set(graph.edges) - set().union(*triple))


def profile(graph: Graph, marker: str) -> tuple[int | None, ...]:
    matchings = perfect_matchings(graph)
    minima: list[int | None] = [INF, INF, INF]
    by_support: dict[tuple[int, ...], int] = {}
    for triple in product(matchings, repeat=3):
        typed_triple: Triple = triple
        if not is_regular(typed_triple):
            continue
        boundary = support(typed_triple, marker)
        value = uncovered(graph, typed_triple)
        by_support[boundary] = min(by_support.get(boundary, value), value)
        k = len(boundary)
        current = minima[k]
        minima[k] = value if current is None else min(current, value)

    # Row permutations imply that exact supports of the same size have equal
    # minima.  Check that symmetry rather than assuming it in the audit.
    for k in range(3):
        values = {value for boundary, value in by_support.items() if len(boundary) == k}
        if minima[k] is None:
            assert not values
        else:
            assert values == {minima[k]}, (graph.name, k, values, minima[k])
    assert (0, 1, 2) not in by_support
    return tuple(minima)


@dataclass(frozen=True)
class SumData:
    graph: Graph
    marker_a: str
    marker_b: str
    cut_edges: tuple[str, str]


def two_edge_sum(
    graph_a: Graph,
    marker_a: str,
    graph_b: Graph,
    marker_b: str,
    *,
    crossed: bool = False,
) -> SumData:
    a0, a1 = graph_a.edges[marker_a]
    b0, b1 = graph_b.edges[marker_b]
    if crossed:
        b0, b1 = b1, b0
    vertices = tuple(("A", v) for v in graph_a.vertices) + tuple(
        ("B", v) for v in graph_b.vertices
    )
    edges: dict[str, tuple[Vertex, Vertex]] = {}
    for edge_id, (u, v) in graph_a.edges.items():
        if edge_id != marker_a:
            edges[f"A:{edge_id}"] = (("A", u), ("A", v))
    for edge_id, (u, v) in graph_b.edges.items():
        if edge_id != marker_b:
            edges[f"B:{edge_id}"] = (("B", u), ("B", v))
    edges["cut:0"] = (("A", a0), ("B", b0))
    edges["cut:1"] = (("A", a1), ("B", b1))
    graph = Graph(f"{graph_a.name}*{graph_b.name}", vertices, edges)
    graph.check()
    return SumData(graph, marker_a, marker_b, ("cut:0", "cut:1"))


def restrict_matching(
    matching: Matching, data: SumData
) -> tuple[Matching, Matching]:
    used_cut = set(matching) & set(data.cut_edges)
    assert len(used_cut) in (0, 2)
    left = {edge_id[2:] for edge_id in matching if edge_id.startswith("A:")}
    right = {edge_id[2:] for edge_id in matching if edge_id.startswith("B:")}
    if used_cut:
        left.add(data.marker_a)
        right.add(data.marker_b)
    return frozenset(left), frozenset(right)


def lift_matching(
    left: Matching, right: Matching, data: SumData
) -> Matching:
    uses_left = data.marker_a in left
    uses_right = data.marker_b in right
    if uses_left != uses_right:
        raise ValueError("boundary supports do not match")
    result = {f"A:{edge_id}" for edge_id in left if edge_id != data.marker_a}
    result.update(f"B:{edge_id}" for edge_id in right if edge_id != data.marker_b)
    if uses_left:
        result.update(data.cut_edges)
    return frozenset(result)


def assert_perfect(graph: Graph, matching: Matching) -> None:
    assert matching <= set(graph.edges)
    endpoints: list[Vertex] = []
    for edge_id in matching:
        endpoints.extend(graph.edges[edge_id])
    assert len(endpoints) == len(graph.vertices)
    assert set(endpoints) == set(graph.vertices)


def finite_sum(left: int | None, right: int | None) -> int | None:
    if left is None or right is None:
        return None
    return left + right


def extended_min(values: Iterable[int | None]) -> int | None:
    finite = [value for value in values if value is not None]
    return min(finite) if finite else None


def audit_sum(
    graph_a: Graph,
    marker_a: str,
    graph_b: Graph,
    marker_b: str,
    *,
    crossed: bool = False,
) -> dict[str, object]:
    data = two_edge_sum(
        graph_a, marker_a, graph_b, marker_b, crossed=crossed
    )
    matchings_a = perfect_matchings(graph_a)
    matchings_b = perfect_matchings(graph_b)
    matchings_g = perfect_matchings(data.graph)

    compatible_pairs = {
        (left, right)
        for left in matchings_a
        for right in matchings_b
        if (marker_a in left) == (marker_b in right)
    }
    restricted_pairs = {restrict_matching(matching, data) for matching in matchings_g}
    assert restricted_pairs == compatible_pairs
    for pair in compatible_pairs:
        lifted = lift_matching(*pair, data)
        assert_perfect(data.graph, lifted)
        assert restrict_matching(lifted, data) == pair

    regular_count = 0
    for triple_g_raw in product(matchings_g, repeat=3):
        triple_g: Triple = triple_g_raw
        triple_a_raw: list[Matching] = []
        triple_b_raw: list[Matching] = []
        for matching in triple_g:
            left, right = restrict_matching(matching, data)
            triple_a_raw.append(left)
            triple_b_raw.append(right)
        triple_a: Triple = tuple(triple_a_raw)  # type: ignore[assignment]
        triple_b: Triple = tuple(triple_b_raw)  # type: ignore[assignment]
        assert support(triple_a, marker_a) == support(triple_b, marker_b)
        regular_g = is_regular(triple_g)
        assert regular_g == (is_regular(triple_a) and is_regular(triple_b))
        if regular_g:
            regular_count += 1
            assert uncovered(data.graph, triple_g) == (
                uncovered(graph_a, triple_a) + uncovered(graph_b, triple_b)
            )

    rho_a = profile(graph_a, marker_a)
    rho_b = profile(graph_b, marker_b)
    predicted = extended_min(
        finite_sum(rho_a[k], rho_b[k]) for k in range(3)
    )
    actual = extended_min(
        uncovered(data.graph, triple)
        for triple in product(matchings_g, repeat=3)
        if is_regular(triple)
    )
    assert actual == predicted

    # A mismatched marker status must be rejected by the inverse map.
    left_using = next(m for m in matchings_a if marker_a in m)
    right_avoiding = next(m for m in matchings_b if marker_b not in m)
    rejected_mismatch = False
    try:
        lift_matching(left_using, right_avoiding, data)
    except ValueError:
        rejected_mismatch = True
    assert rejected_mismatch

    return {
        "sum": data.graph.name,
        "pairing": "crossed" if crossed else "straight",
        "perfect_matchings": {
            "left": len(matchings_a),
            "right": len(matchings_b),
            "sum": len(matchings_g),
        },
        "regular_arrays_in_sum": regular_count,
        "rho_left": list(rho_a),
        "rho_right": list(rho_b),
        "convolution": actual,
        "mismatched_support_rejected": rejected_mismatch,
    }


def main() -> None:
    graph_k4, edge_k4 = k4()
    graph_p, edge_p = petersen()
    result = {
        "claim": "exact 2-edge-sum FR boundary-profile convolution",
        "fixtures": {
            "K4": {
                "perfect_matchings": len(perfect_matchings(graph_k4)),
                "rho": list(profile(graph_k4, edge_k4)),
            },
            "Petersen": {
                "perfect_matchings": len(perfect_matchings(graph_p)),
                "rho": list(profile(graph_p, edge_p)),
            },
        },
        "audits": [
            audit_sum(graph_k4, edge_k4, graph_k4, edge_k4),
            audit_sum(graph_p, edge_p, graph_k4, edge_k4, crossed=True),
            audit_sum(graph_p, edge_p, graph_p, edge_p),
        ],
        "universal_claim_source": "README.md parity-and-bijection proof",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
