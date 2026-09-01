#!/usr/bin/env python3
"""Certify asymmetry and canonical hashes by exact color refinement.

The input graphs are the strict Parts-509 graph G and the eleven exceptional
one-point swaps recorded by the preceding swap-closure contribution.  No graph
isomorphism package, SAT solver, randomization, or floating point is used.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


N = 509
ADDED = 509
EXPECTED_RAW_EDGE_SHA256 = (
    "2308fe8a798113e1c3bee9b571ed21875c44997a9916712bd76b6983f24861c8"
)
EXPECTED_CANONICAL_EDGE_SHA256 = (
    "5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c"
)
EXPECTED_SWAP_SHA256 = (
    "a36a11bf3e63d3ec887b0f4507d51623773b968842a964a314e364713ac46ca3"
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_edge_bytes(edges: set[tuple[int, int]]) -> bytes:
    return "".join(f"{u} {v}\n" for u, v in sorted(edges)).encode("ascii")


def load_inputs(edge_path: Path, swap_path: Path):
    edge_bytes = edge_path.read_bytes()
    if sha256_bytes(edge_bytes) != EXPECTED_RAW_EDGE_SHA256:
        raise ValueError("raw base-edge file hash mismatch")
    raw_edges = json.loads(edge_bytes)
    edges = {tuple(map(int, e)) for e in raw_edges}
    if len(raw_edges) != 2442 or len(edges) != 2442:
        raise ValueError("expected 2,442 distinct base edges")
    if any(not (0 <= u < v < N) for u, v in edges):
        raise ValueError("base edge is not normalized or is out of range")
    if sha256_bytes(canonical_edge_bytes(edges)) != EXPECTED_CANONICAL_EDGE_SHA256:
        raise ValueError("canonical base-edge hash mismatch")

    swap_bytes = swap_path.read_bytes()
    if sha256_bytes(swap_bytes) != EXPECTED_SWAP_SHA256:
        raise ValueError("swap-certificate file hash mismatch")
    swaps = json.loads(swap_bytes).get("swaps")
    if not isinstance(swaps, list) or len(swaps) != 11:
        raise ValueError("expected eleven swaps")
    return edges, swaps


def make_adjacency(vertices: set[int], edges: set[tuple[int, int]]):
    adjacency = {v: set() for v in vertices}
    for u, v in edges:
        if u not in adjacency or v not in adjacency or u == v:
            raise ValueError(f"invalid edge {(u, v)}")
        adjacency[u].add(v)
        adjacency[v].add(u)
    if any(v not in adjacency[w] for v in vertices for w in adjacency[v]):
        raise AssertionError("asymmetric adjacency representation")
    return adjacency


def build_graphs(base_edges: set[tuple[int, int]], swaps: list[dict]):
    yield "G", None, None, make_adjacency(set(range(N)), base_edges)
    for i, record in enumerate(swaps):
        deleted = int(record["u"])
        neighbors = tuple(map(int, record["q_neighbors"]))
        if not (0 <= deleted < N):
            raise ValueError(f"swap S{i} deletes an invalid vertex")
        if len(neighbors) != len(set(neighbors)) or any(
            not (0 <= v < N) for v in neighbors
        ):
            raise ValueError(f"swap S{i} has an invalid neighbor list")
        vertices = (set(range(N)) - {deleted}) | {ADDED}
        edges = {e for e in base_edges if deleted not in e}
        edges |= {
            (min(ADDED, v), max(ADDED, v)) for v in neighbors if v != deleted
        }
        yield (
            f"S{i}",
            deleted,
            sum(v != deleted for v in neighbors),
            make_adjacency(vertices, edges),
        )


def relabel(signatures: dict[int, tuple]) -> dict[int, int]:
    """Assign consecutive IDs to distinct signatures in lexicographic order."""
    identifiers = {sig: i for i, sig in enumerate(sorted(set(signatures.values())))}
    return {v: identifiers[sig] for v, sig in signatures.items()}


def refine(adjacency: dict[int, set[int]]):
    """Run degree-seeded 1-WL until discrete, returning its exact transcript."""
    colors = relabel({v: (len(nbrs),) for v, nbrs in adjacency.items()})
    cell_counts = [len(set(colors.values()))]
    while cell_counts[-1] < len(adjacency):
        signatures = {
            v: (colors[v], tuple(sorted(colors[w] for w in adjacency[v])))
            for v in adjacency
        }
        new_colors = relabel(signatures)
        new_count = len(set(new_colors.values()))
        if new_count <= cell_counts[-1]:
            raise ValueError(
                f"color refinement stabilized non-discretely at {new_count} cells"
            )
        colors = new_colors
        cell_counts.append(new_count)
    return colors, cell_counts


def canonical_hash(adjacency: dict[int, set[int]], colors: dict[int, int]) -> str:
    if set(colors.values()) != set(range(len(adjacency))):
        raise ValueError("final coloring is not a consecutive discrete coloring")
    edges = {
        (min(colors[u], colors[v]), max(colors[u], colors[v]))
        for u, neighbors in adjacency.items()
        for v in neighbors
        if u < v
    }
    return sha256_bytes(canonical_edge_bytes(edges))


def make_certificate(edge_path: Path, swap_path: Path) -> dict:
    base_edges, swaps = load_inputs(edge_path, swap_path)
    summaries = []
    for name, deleted, added_degree, adjacency in build_graphs(base_edges, swaps):
        colors, counts = refine(adjacency)
        summaries.append(
            {
                "name": name,
                "vertices": len(adjacency),
                "edges": sum(map(len, adjacency.values())) // 2,
                "deleted_vertex": deleted,
                "added_degree": added_degree,
                "initial_degree_classes": counts[0],
                "refinement_cell_counts": counts,
                "rounds_to_discrete": len(counts) - 1,
                "canonical_edge_sha256": canonical_hash(adjacency, colors),
            }
        )
    hashes = [record["canonical_edge_sha256"] for record in summaries]
    if len(set(hashes)) != len(hashes):
        raise ValueError("the twelve canonical hashes are not distinct")
    return {
        "format": "parts509-asymmetry-color-refinement-v1",
        "claim": (
            "Degree-seeded one-dimensional Weisfeiler-Leman refinement is "
            "discrete on the Parts-509 graph and each of its eleven certified "
            "one-point swaps; consequently all twelve graphs are asymmetric."
        ),
        "proof_note": (
            "Every automorphism preserves degrees and every subsequent color "
            "class. A discrete final partition therefore fixes every vertex. "
            "The lexicographically assigned discrete colors also give a "
            "canonical labeling for this family."
        ),
        "input_hashes": {
            "raw_edges_json_sha256": EXPECTED_RAW_EDGE_SHA256,
            "canonical_base_edges_sha256": EXPECTED_CANONICAL_EDGE_SHA256,
            "swap_certificate_json_sha256": EXPECTED_SWAP_SHA256,
        },
        "graphs": summaries,
        "all_discrete": True,
        "all_asymmetric": True,
        "all_canonical_hashes_distinct": True,
    }


def main() -> None:
    here = Path(__file__).resolve().parent
    root = here.parent
    parser = argparse.ArgumentParser()
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
    parser.add_argument("--certificate", type=Path, default=here / "certificate.json")
    parser.add_argument("mode", choices=("certify", "verify"))
    args = parser.parse_args()

    document = make_certificate(args.edges, args.swaps)
    encoded = (json.dumps(document, indent=2, sort_keys=True) + "\n").encode()
    if args.mode == "certify":
        args.certificate.write_bytes(encoded)
        action = "written"
    else:
        if args.certificate.read_bytes() != encoded:
            raise ValueError("certificate differs from exact recomputation")
        action = "verified"
    print(f"certificate_{action}=true")
    for record in document["graphs"]:
        print(
            f"{record['name']}: edges={record['edges']} "
            f"cells={record['refinement_cell_counts']} "
            f"canonical_sha256={record['canonical_edge_sha256']}"
        )
    print("all_asymmetric=true")
    print("all_canonical_hashes_distinct=true")


if __name__ == "__main__":
    main()
