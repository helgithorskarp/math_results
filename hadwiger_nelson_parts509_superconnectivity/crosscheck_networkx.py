#!/usr/bin/env python3
"""Independent algorithmic cross-check of the four connectivity values."""

from __future__ import annotations

import json
from pathlib import Path

import networkx as nx


EDGE_PATH = Path(__file__).resolve().parent.parent / (
    "hadwiger_nelson_parts509_degree10_replacements/edges.json"
)


def main() -> None:
    graph = nx.Graph()
    graph.add_nodes_from(range(509))
    graph.add_edges_from(json.loads(EDGE_PATH.read_text()))
    low = sorted(vertex for vertex, degree in graph.degree() if degree == 4)
    core = graph.subgraph(set(graph) - set(low)).copy()
    values = {
        "graph_vertex_connectivity": nx.node_connectivity(graph),
        "graph_edge_connectivity": nx.edge_connectivity(graph),
        "core_vertex_connectivity": nx.node_connectivity(core),
        "core_edge_connectivity": nx.edge_connectivity(core),
    }
    expected = {
        "graph_vertex_connectivity": 4,
        "graph_edge_connectivity": 4,
        "core_vertex_connectivity": 5,
        "core_edge_connectivity": 5,
    }
    if values != expected:
        raise ValueError(f"connectivity mismatch: {values}")
    for key, value in values.items():
        print(f"{key}={value}")
    print("independent_connectivity_crosscheck=true")


if __name__ == "__main__":
    main()
