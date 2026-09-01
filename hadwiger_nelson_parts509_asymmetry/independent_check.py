#!/usr/bin/env python3
"""Independent exact checker for the Parts-509 asymmetry certificate.

This implementation imports none of refinement_certificate.py.  It refines an
ordered partition by neighbor-count vectors, rather than assigning colors from
multiset signatures, and compares the resulting transcript and canonical edge
hashes with certificate.json.
"""

from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path


N = 509
NEW = 509
EDGE_RAW_HASH = "2308fe8a798113e1c3bee9b571ed21875c44997a9916712bd76b6983f24861c8"
EDGE_CANONICAL_HASH = "5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c"
SWAP_HASH = "a36a11bf3e63d3ec887b0f4507d51623773b968842a964a314e364713ac46ca3"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def edge_encoding(edges) -> bytes:
    return "".join(f"{a} {b}\n" for a, b in sorted(edges)).encode("ascii")


def graph(vertices, edges):
    adj = {v: set() for v in vertices}
    for a, b in edges:
        assert a in adj and b in adj and a != b
        adj[a].add(b)
        adj[b].add(a)
    assert sum(map(len, adj.values())) == 2 * len(edges)
    return adj


def ordered_partition_refinement(adj):
    """Refine degree blocks by exact counts into every preceding block."""
    by_degree = defaultdict(list)
    for v, neighbors in adj.items():
        by_degree[len(neighbors)].append(v)
    blocks = [sorted(by_degree[d]) for d in sorted(by_degree)]
    cell_counts = [len(blocks)]
    while any(len(block) > 1 for block in blocks):
        block_of = {v: i for i, block in enumerate(blocks) for v in block}
        next_blocks = []
        for block in blocks:
            groups = defaultdict(list)
            for v in block:
                counts = [0] * len(blocks)
                for w in adj[v]:
                    counts[block_of[w]] += 1
                groups[tuple(counts)].append(v)
            # The certificate specifies lexicographic order of the expanded
            # sorted neighbor-color multiset, not lexicographic order of its
            # count vector.  The two give the same partition but generally a
            # different canonical labeling.
            def expanded(signature):
                return tuple(
                    color
                    for color, multiplicity in enumerate(signature)
                    for _ in range(multiplicity)
                )

            for signature in sorted(groups, key=expanded):
                next_blocks.append(sorted(groups[signature]))
        if len(next_blocks) <= len(blocks):
            raise AssertionError("partition stabilized before becoming discrete")
        blocks = next_blocks
        cell_counts.append(len(blocks))
    return blocks, cell_counts


def canonical_hash(adj, singleton_blocks):
    label = {block[0]: i for i, block in enumerate(singleton_blocks)}
    edges = {
        (min(label[v], label[w]), max(label[v], label[w]))
        for v in adj
        for w in adj[v]
        if v < w
    }
    return digest(edge_encoding(edges))


def main() -> None:
    here = Path(__file__).resolve().parent
    root = here.parent
    cert_path = Path(sys.argv[1]) if len(sys.argv) > 1 else here / "certificate.json"
    edge_path = root / "hadwiger_nelson_parts509_degree10_replacements" / "edges.json"
    swap_path = root / "hadwiger_nelson_parts509_swap_closure" / "swap_certificate.json"

    edge_raw = edge_path.read_bytes()
    swap_raw = swap_path.read_bytes()
    assert digest(edge_raw) == EDGE_RAW_HASH
    assert digest(swap_raw) == SWAP_HASH
    listed_edges = [tuple(map(int, edge)) for edge in json.loads(edge_raw)]
    edges = set(listed_edges)
    assert len(listed_edges) == len(edges) == 2442
    assert all(0 <= a < b < N for a, b in edges)
    assert digest(edge_encoding(edges)) == EDGE_CANONICAL_HASH
    swaps = json.loads(swap_raw)["swaps"]
    assert len(swaps) == 11

    descriptions = [("G", None, None, graph(set(range(N)), edges))]
    for i, swap in enumerate(swaps):
        deleted = int(swap["u"])
        neighbors = list(map(int, swap["q_neighbors"]))
        assert len(neighbors) == len(set(neighbors))
        vertices = (set(range(N)) - {deleted}) | {NEW}
        new_edges = {e for e in edges if deleted not in e}
        new_edges.update(
            (min(NEW, v), max(NEW, v)) for v in neighbors if v != deleted
        )
        descriptions.append(
            (
                f"S{i}",
                deleted,
                sum(v != deleted for v in neighbors),
                graph(vertices, new_edges),
            )
        )

    cert = json.loads(cert_path.read_text())
    assert cert["all_discrete"] and cert["all_asymmetric"]
    assert cert["input_hashes"] == {
        "raw_edges_json_sha256": EDGE_RAW_HASH,
        "canonical_base_edges_sha256": EDGE_CANONICAL_HASH,
        "swap_certificate_json_sha256": SWAP_HASH,
    }
    expected = {record["name"]: record for record in cert["graphs"]}
    hashes = []
    for name, deleted, added_degree, adj in descriptions:
        blocks, counts = ordered_partition_refinement(adj)
        h = canonical_hash(adj, blocks)
        hashes.append(h)
        record = expected[name]
        assert record["vertices"] == len(adj) == N
        assert record["edges"] == sum(map(len, adj.values())) // 2
        assert record["deleted_vertex"] == deleted
        assert record["added_degree"] == added_degree
        assert record["initial_degree_classes"] == counts[0]
        assert record["refinement_cell_counts"] == counts
        assert record["rounds_to_discrete"] == len(counts) - 1
        assert record["canonical_edge_sha256"] == h
        print(f"{name}: cells={counts} canonical_sha256={h}")
    assert len(set(hashes)) == 12
    assert cert["all_canonical_hashes_distinct"]
    print("independent_partition_check=true")
    print("all_12_graphs_asymmetric=true")
    print("all_12_canonical_hashes_distinct=true")


if __name__ == "__main__":
    main()
