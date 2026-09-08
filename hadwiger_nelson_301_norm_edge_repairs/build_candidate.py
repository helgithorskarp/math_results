#!/usr/bin/env python3
"""Build any h3993 one-edge repair candidate used in this package."""
from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1] / "math_results"
SOURCE = REPO / "hadwiger_nelson_h516_k23free_edge_repair"
SOURCE_GRAPH_SHA256 = "7be0344d1811866429181436b2f85653fc801272a7a3efddad6125539e50cbbb"
SOURCE_FIVE_SHA256 = "720466c1b6403de7d8247a33bb2844fccca306dfa21cc339b763968e6b2aea1d"
ANCHOR_TRIANGLE = (1, 189, 192)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cnf(labels, edges):
    position = {label: index for index, label in enumerate(labels)}
    lines = [f"p cnf {4 * len(labels)} {len(labels) + 4 * len(edges) + 3}\n"]
    for label in labels:
        lines.append(" ".join(str(4 * position[label] + colour + 1) for colour in range(4)) + " 0\n")
    for left, right in edges:
        for colour in range(4):
            lines.append(f"{-4 * position[left] - colour - 1} {-4 * position[right] - colour - 1} 0\n")
    for colour, label in enumerate(ANCHOR_TRIANGLE):
        lines.append(f"{4 * position[label] + colour + 1} 0\n")
    return "".join(lines).encode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--deleted-edge", type=int, nargs=2, default=(0, 143), metavar=("LEFT", "RIGHT"))
    args = parser.parse_args()
    deleted_edge = tuple(sorted(args.deleted_edge))
    args.out.mkdir(parents=True, exist_ok=False)
    if sha256(SOURCE / "graph.json") != SOURCE_GRAPH_SHA256:
        raise ValueError("source graph identity")
    if sha256(SOURCE / "five_colouring.json") != SOURCE_FIVE_SHA256:
        raise ValueError("source five-colouring identity")
    source = json.loads((SOURCE / "graph.json").read_text())
    source_edges = [tuple(edge) for edge in source["edges"]]
    if deleted_edge not in source_edges:
        raise ValueError("deleted source edge")
    edges = [edge for edge in source_edges if edge != deleted_edge]
    edge_set = set(edges)
    if any(tuple(sorted(pair)) not in edge_set for pair in combinations(ANCHOR_TRIANGLE, 2)):
        raise ValueError("surviving anchor triangle")
    graph = {
        "claim": "single-edge repair candidate from h3993 necessary interface",
        "source_graph_sha256": SOURCE_GRAPH_SHA256,
        "source_contribution": "bafkreib67bj2x2xsk2tsvlxtw4a2rp3z65eysayh7yiaxyc7e2v6wlwpsm",
        "interface_contribution": "bafkreiaht6wdxk2gkh4uor2pyynmnzkmeqofcybncbeo6rnaxcxxto7u2i",
        "deleted_edge": list(deleted_edge),
        "labels": source["labels"],
        "edges": [list(edge) for edge in edges],
        "vertices": len(source["labels"]),
        "edge_count": len(edges),
        "triangle": list(ANCHOR_TRIANGLE),
        "geometry_status": "UNDECIDED",
    }
    graph_path = args.out / "graph.json"
    graph_path.write_text(json.dumps(graph, separators=(",", ":"), sort_keys=True) + "\n")
    five_path = args.out / "five_colouring.json"
    five_path.write_bytes((SOURCE / "five_colouring.json").read_bytes())
    cnf_path = args.out / "four_colour.cnf"
    cnf_path.write_bytes(cnf(graph["labels"], edges))
    print(json.dumps({
        "vertices": graph["vertices"],
        "edges": graph["edge_count"],
        "deleted_edge": graph["deleted_edge"],
        "graph_sha256": sha256(graph_path),
        "five_colouring_sha256": sha256(five_path),
        "CNF_variables": 4 * graph["vertices"],
        "CNF_clauses": graph["vertices"] + 4 * graph["edge_count"] + 3,
        "CNF_sha256": sha256(cnf_path),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
