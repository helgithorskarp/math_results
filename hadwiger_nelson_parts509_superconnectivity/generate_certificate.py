#!/usr/bin/env python3
"""Generate a positive vertex-connectivity certificate for the Parts-509 core."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import networkx as nx
from networkx.algorithms.connectivity import build_auxiliary_node_connectivity
from networkx.algorithms.flow import shortest_augmenting_path


DEFAULT_EDGES = Path(__file__).resolve().parent.parent / (
    "hadwiger_nelson_parts509_degree10_replacements/edges.json"
)
DEFAULT_OUTPUT = Path(__file__).with_name("certificate.json")
ROOTS = (0, 1, 2, 3, 4)


def load_graph(path: Path) -> tuple[nx.Graph, list[tuple[int, int]]]:
    raw = json.loads(path.read_text())
    edges = [tuple(map(int, edge)) for edge in raw]
    if len(edges) != 2442 or len(set(edges)) != len(edges):
        raise ValueError("expected 2442 distinct edges")
    if any(not (0 <= u < v < 509) for u, v in edges):
        raise ValueError("edge list is not canonical on vertices 0,...,508")
    graph = nx.Graph()
    graph.add_nodes_from(range(509))
    graph.add_edges_from(edges)
    return graph, edges


def edge_hash(edges: list[tuple[int, int]]) -> str:
    data = "".join(f"{u} {v}\n" for u, v in sorted(edges)).encode()
    return hashlib.sha256(data).hexdigest()


def five_paths(
    graph: nx.Graph,
    source: int,
    target: int,
    auxiliary: nx.DiGraph,
) -> list[list[int]]:
    paths = list(
        nx.node_disjoint_paths(
            graph,
            source,
            target,
            flow_func=shortest_augmenting_path,
            cutoff=5,
            auxiliary=auxiliary,
        )
    )
    if len(paths) < 5:
        raise ValueError(f"only {len(paths)} paths from {source} to {target}")
    paths = [list(map(int, path)) for path in paths[:5]]
    paths.sort(key=lambda path: (len(path), path))
    return paths


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--edges", type=Path, default=DEFAULT_EDGES)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    graph, edges = load_graph(args.edges)
    low = sorted(vertex for vertex, degree in graph.degree() if degree == 4)
    core = graph.copy()
    core.remove_nodes_from(low)
    if low != [310, 313, 316, 319, 322, 325]:
        raise ValueError(f"unexpected degree-four set: {low}")
    if any(root not in core for root in ROOTS):
        raise ValueError("a selected root is absent from the core")

    auxiliary = build_auxiliary_node_connectivity(core)
    path_data: dict[str, dict[str, list[list[int]]]] = {}
    total_paths = 0
    total_vertices = 0
    for root in ROOTS:
        root_data: dict[str, list[list[int]]] = {}
        for target in sorted(core):
            if target == root:
                continue
            paths = five_paths(core, root, target, auxiliary)
            root_data[str(target)] = paths
            total_paths += len(paths)
            total_vertices += sum(len(path) for path in paths)
        path_data[str(root)] = root_data
        print(f"root={root} targets={len(root_data)}", flush=True)

    certificate = {
        "schema": "parts509-superconnectivity-v1",
        "graph": {
            "vertices": 509,
            "edges": 2442,
            "canonical_edge_sha256": edge_hash(edges),
        },
        "degree_four_vertices": low,
        "roots": list(ROOTS),
        "core_order": core.number_of_nodes(),
        "core_size": core.number_of_edges(),
        "root_target_paths": path_data,
        "summary": {
            "root_target_pairs": len(ROOTS) * (core.number_of_nodes() - 1),
            "paths": total_paths,
            "path_vertex_occurrences": total_vertices,
        },
    }
    args.output.write_text(json.dumps(certificate, sort_keys=True, separators=(",", ":")) + "\n")
    print(f"wrote={args.output}")
    print(f"paths={total_paths}")
    print(f"path_vertex_occurrences={total_vertices}")


if __name__ == "__main__":
    main()
