#!/usr/bin/env python3
"""Independent exact-isomorphism check for the Parts-509 swap classification."""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path

import networkx as nx


N = 509
Q = 509


def load_graphs(edges_path: Path, swaps_path: Path) -> list[tuple[str, nx.Graph]]:
    raw_edges = json.loads(edges_path.read_text())
    edges = [tuple(map(int, edge)) for edge in raw_edges]
    swaps = json.loads(swaps_path.read_text())["swaps"]

    base = nx.Graph()
    base.add_nodes_from(range(N))
    base.add_edges_from(edges)
    graphs = [("G", base)]

    for index, swap in enumerate(swaps):
        deleted = int(swap["u"])
        graph = nx.Graph()
        graph.add_nodes_from((set(range(N)) - {deleted}) | {Q})
        graph.add_edges_from(edge for edge in edges if deleted not in edge)
        graph.add_edges_from(
            (Q, int(neighbor))
            for neighbor in swap["q_neighbors"]
            if int(neighbor) != deleted
        )
        graphs.append((f"S{index}", graph))
    return graphs


def main() -> None:
    here = Path(__file__).resolve().parent
    root = here.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--edges",
        type=Path,
        default=root / "hadwiger_nelson_parts509_degree10_replacements" / "edges.json",
    )
    parser.add_argument(
        "--swaps",
        type=Path,
        default=root / "hadwiger_nelson_parts509_swap_closure" / "swap_certificate.json",
    )
    arguments = parser.parse_args()

    graphs = load_graphs(arguments.edges, arguments.swaps)
    comparisons = 0
    for (left_name, left), (right_name, right) in combinations(graphs, 2):
        if nx.is_isomorphic(left, right):
            raise SystemExit(f"unexpected isomorphism: {left_name} ~= {right_name}")
        comparisons += 1
    print(
        json.dumps(
            {
                "all_checks": True,
                "graphs": len(graphs),
                "pairwise_nonisomorphic": comparisons,
                "networkx_version": nx.__version__,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
