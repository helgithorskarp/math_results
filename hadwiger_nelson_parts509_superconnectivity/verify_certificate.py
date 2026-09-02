#!/usr/bin/env python3
"""Solver-free replay of the Parts-509 superconnectivity certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import deque
from pathlib import Path


DEFAULT_EDGES = Path(__file__).resolve().parent.parent / (
    "hadwiger_nelson_parts509_degree10_replacements/edges.json"
)
DEFAULT_CERTIFICATE = Path(__file__).with_name("certificate.json")
EXPECTED_EDGE_HASH = "5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c"


def load_edges(path: Path) -> list[tuple[int, int]]:
    raw = json.loads(path.read_text())
    edges = [tuple(map(int, edge)) for edge in raw]
    if len(edges) != 2442 or len(set(edges)) != len(edges):
        raise ValueError("expected 2442 distinct edges")
    if any(not (0 <= u < v < 509) for u, v in edges):
        raise ValueError("edge list is not canonical on vertices 0,...,508")
    digest = hashlib.sha256(
        "".join(f"{u} {v}\n" for u, v in sorted(edges)).encode()
    ).hexdigest()
    if digest != EXPECTED_EDGE_HASH:
        raise ValueError(f"wrong canonical edge hash: {digest}")
    return edges


def adjacency(edges: list[tuple[int, int]]) -> list[set[int]]:
    neighbors = [set() for _ in range(509)]
    for u, v in edges:
        neighbors[u].add(v)
        neighbors[v].add(u)
    return neighbors


def connected_components(
    vertices: set[int], neighbors: list[set[int]]
) -> list[set[int]]:
    unseen = set(vertices)
    components: list[set[int]] = []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        component = {start}
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            for other in neighbors[vertex] & unseen:
                unseen.remove(other)
                component.add(other)
                queue.append(other)
        components.append(component)
    return components


def verify_path_family(
    root: int,
    target: int,
    paths: object,
    core: set[int],
    neighbors: list[set[int]],
) -> tuple[int, int]:
    if not isinstance(paths, list) or len(paths) != 5:
        raise ValueError(f"expected five paths for {root}->{target}")
    used_internal: set[int] = set()
    seen_paths: set[tuple[int, ...]] = set()
    occurrence_count = 0
    for item in paths:
        if not isinstance(item, list) or len(item) < 2:
            raise ValueError(f"malformed path for {root}->{target}")
        path = [int(vertex) for vertex in item]
        path_tuple = tuple(path)
        if path_tuple in seen_paths:
            raise ValueError(f"duplicate path for {root}->{target}: {path}")
        seen_paths.add(path_tuple)
        if path[0] != root or path[-1] != target:
            raise ValueError(f"wrong endpoints for {root}->{target}: {path}")
        if len(set(path)) != len(path) or any(vertex not in core for vertex in path):
            raise ValueError(f"path is not simple in the core: {path}")
        if any(v not in neighbors[u] for u, v in zip(path, path[1:])):
            raise ValueError(f"path uses a nonedge: {path}")
        internal = set(path[1:-1])
        if internal & used_internal:
            raise ValueError(f"paths are not internally disjoint for {root}->{target}")
        used_internal |= internal
        occurrence_count += len(path)
    return len(paths), occurrence_count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--edges", type=Path, default=DEFAULT_EDGES)
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    args = parser.parse_args()

    edges = load_edges(args.edges)
    neighbors = adjacency(edges)
    document = json.loads(args.certificate.read_text())
    if document.get("schema") != "parts509-superconnectivity-v1":
        raise ValueError("wrong certificate schema")
    if document.get("graph") != {
        "vertices": 509,
        "edges": 2442,
        "canonical_edge_sha256": EXPECTED_EDGE_HASH,
    }:
        raise ValueError("certificate identifies the wrong graph")

    degrees = [len(row) for row in neighbors]
    low = [vertex for vertex, degree in enumerate(degrees) if degree == 4]
    if low != document.get("degree_four_vertices"):
        raise ValueError("degree-four vertex list does not match the graph")
    if min(degrees) != 4 or low != [310, 313, 316, 319, 322, 325]:
        raise ValueError("unexpected minimum-degree structure")
    low_set = set(low)
    core = set(range(509)) - low_set
    if any(neighbors[vertex] & low_set for vertex in low):
        raise ValueError("degree-four vertices are not independent")
    low_neighborhoods = [frozenset(neighbors[vertex]) for vertex in low]
    if len(set(low_neighborhoods)) != 6:
        raise ValueError("degree-four neighborhoods are not pairwise distinct")
    core_size = sum(len(neighbors[vertex] & core) for vertex in core) // 2
    core_min_degree = min(len(neighbors[vertex] & core) for vertex in core)
    if (len(core), core_size, core_min_degree) != (503, 2418, 5):
        raise ValueError("unexpected core parameters")

    roots = document.get("roots")
    if not isinstance(roots, list) or len(roots) != 5 or len(set(roots)) != 5:
        raise ValueError("expected five distinct roots")
    if any(root not in core for root in roots):
        raise ValueError("a root is not a core vertex")
    families = document.get("root_target_paths")
    if not isinstance(families, dict) or set(families) != {str(root) for root in roots}:
        raise ValueError("root path data is incomplete")

    total_paths = 0
    total_occurrences = 0
    expected_targets = {str(vertex) for vertex in core}
    for root in roots:
        root_data = families[str(root)]
        if set(root_data) != expected_targets - {str(root)}:
            raise ValueError(f"target set is incomplete for root {root}")
        for target_text, paths in root_data.items():
            path_count, occurrence_count = verify_path_family(
                root, int(target_text), paths, core, neighbors
            )
            total_paths += path_count
            total_occurrences += occurrence_count

    expected_summary = {
        "root_target_pairs": 5 * 502,
        "paths": total_paths,
        "path_vertex_occurrences": total_occurrences,
    }
    if document.get("summary") != expected_summary:
        raise ValueError("certificate summary mismatch")
    if document.get("core_order") != 503 or document.get("core_size") != 2418:
        raise ValueError("certificate core parameters mismatch")

    # Directly replay the six asserted minimum cuts and their component sizes.
    cut_components: dict[str, list[int]] = {}
    all_vertices = set(range(509))
    for vertex in low:
        cut = neighbors[vertex]
        components = connected_components(all_vertices - cut, neighbors)
        sizes = sorted(map(len, components))
        if sizes != [1, 504] or {vertex} not in components:
            raise ValueError(f"N({vertex}) is not the asserted isolating 4-cut")
        cut_components[str(vertex)] = sizes

    print("all_checks=true")
    print(f"canonical_edge_sha256={EXPECTED_EDGE_HASH}")
    print("degree_four_vertices=" + ",".join(map(str, low)))
    print("core_order=503")
    print("core_size=2418")
    print("core_min_degree=5")
    print("certified_core_vertex_connectivity_lower_bound=5")
    print("exact_core_vertex_connectivity=5")
    print("exact_graph_vertex_connectivity=4")
    print("exact_graph_edge_connectivity=4")
    print("minimum_vertex_cuts=6")
    print("minimum_edge_cuts=6")
    print(f"root_target_pairs={5 * 502}")
    print(f"verified_paths={total_paths}")
    print(f"path_vertex_occurrences={total_occurrences}")


if __name__ == "__main__":
    main()
