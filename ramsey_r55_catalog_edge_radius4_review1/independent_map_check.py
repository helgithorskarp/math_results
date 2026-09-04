#!/usr/bin/env python3
"""Independent positive-map and target-isomorphism audit for radius four."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

import networkx as nx


CATALOG_SHA256 = "067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb"
MAP_SHA256 = "b7265672d34b876ceb1f371ab8b8a6cde7c970a0d0fbf4daed1d783a860a9b3b"
RADIUS2_MAP_SHA256 = "5e1cafc6ba00cdf2bd48c8e4c45748ef29cc88328b1119dbda8898c58215afe5"
RADIUS3_MAP_SHA256 = "d2e3e2a88be4af996bc27f8740945ce73684c9a0e1c62cb7aea9def1c012372d"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def has_clique_of_order_five(graph: nx.Graph) -> bool:
    # Bron--Kerbosch through NetworkX, independent of the submitted bitset checker.
    return any(len(clique) >= 5 for clique in nx.find_cliques(graph))


def parse_edge(text: str) -> tuple[int, int]:
    pieces = text.split(",")
    assert len(pieces) == 2
    u, v = map(int, pieces)
    assert 0 <= u < v < 42
    return u, v


def main() -> None:
    here = Path(__file__).resolve().parent
    artifact = here.parent / "ramsey_r55_catalog_edge_radius4_classification"
    catalog_path = artifact / "r55_42some.g6"
    map_path = artifact / "EDGE_RADIUS4_MAP.tsv"
    assert sha256(catalog_path) == CATALOG_SHA256
    assert sha256(map_path) == MAP_SHA256

    catalog = [
        nx.from_graph6_bytes(record.encode("ascii"))
        for record in catalog_path.read_text(encoding="ascii").splitlines()
        if record
    ]
    assert len(catalog) == 328
    assert all(len(graph) == 42 for graph in catalog)
    assert all(
        not has_clique_of_order_five(graph)
        and not has_clique_of_order_five(nx.complement(graph))
        for graph in catalog
    )
    complements = [nx.complement(graph) for graph in catalog]

    rows = map_path.read_text(encoding="ascii").splitlines()
    assert rows[0] == (
        "parent\tedge_1\tedge_2\tedge_3\tedge_4\t"
        "target_kind\ttarget_index"
    )
    assert rows[-1] == (
        "# SUMMARY transitions=8408 base_transitions=8284 "
        "complement_transitions=124 distinct_targets=380 "
        "base_targets=318 complement_targets=62"
    )

    seen_flip_sets: set[tuple[int, tuple[tuple[int, int], ...]]] = set()
    per_parent: Counter[int] = Counter()
    target_kinds: Counter[str] = Counter()
    targets: set[tuple[str, int]] = set()
    for row_number, line in enumerate(rows[1:-1], start=2):
        fields = line.split("\t")
        assert len(fields) == 7
        parent = int(fields[0])
        target_kind = fields[5]
        target_index = int(fields[6])
        assert 0 <= parent < 328 and 0 <= target_index < 328
        assert target_kind in {"base", "complement"}
        flips = tuple(parse_edge(text) for text in fields[1:5])
        assert len(set(flips)) == 4
        key = parent, tuple(sorted(flips))
        assert key not in seen_flip_sets, f"duplicate flip set at row {row_number}"
        seen_flip_sets.add(key)

        variant = catalog[parent].copy()
        for u, v in flips:
            if variant.has_edge(u, v):
                variant.remove_edge(u, v)
            else:
                variant.add_edge(u, v)
        assert not has_clique_of_order_five(variant)
        assert not has_clique_of_order_five(nx.complement(variant))
        target = catalog[target_index] if target_kind == "base" else complements[target_index]
        assert nx.vf2pp_is_isomorphic(variant, target), f"wrong target at row {row_number}"

        per_parent[parent] += 1
        target_kinds[target_kind] += 1
        targets.add((target_kind, target_index))

    assert len(seen_flip_sets) == 8408
    assert target_kinds == {"base": 8284, "complement": 124}
    assert len(targets) == 380
    assert Counter(per_parent.values()) == {
        1: 8,
        6: 8,
        8: 24,
        10: 8,
        15: 16,
        16: 16,
        17: 16,
        24: 16,
        26: 16,
        29: 16,
        31: 32,
        32: 16,
        35: 72,
        36: 48,
        37: 8,
    }
    assert sorted(set(range(328)) - set(per_parent)) == [39, 170, 171, 190, 191, 192, 193, 305]

    # Independently recompute the advertised aggregate across radii 1--4.
    lower_maps = [
        root
        for root in (
            here.parent / "ramsey_r55_catalog_edge_radius2_classification" / "EDGE_RADIUS2_MAP.tsv",
            here.parent / "ramsey_r55_catalog_edge_radius3_classification" / "EDGE_RADIUS3_MAP.tsv",
        )
    ]
    assert sha256(lower_maps[0]) == RADIUS2_MAP_SHA256
    assert sha256(lower_maps[1]) == RADIUS3_MAP_SHA256
    all_targets = set(targets)
    all_transitions = len(seen_flip_sets)
    for lower_map in lower_maps:
        for line in lower_map.read_text(encoding="ascii").splitlines()[1:]:
            if line.startswith("# SUMMARY "):
                break
            fields = line.split("\t")
            all_transitions += 1
            all_targets.add((fields[-2], int(fields[-1])))
    assert all_transitions == 24_648 and len(all_targets) == 508

    summary = {
        "all_catalog_graphs_ramsey_5_5": True,
        "all_mapped_variants_ramsey_5_5": True,
        "all_target_isomorphisms_verified": True,
        "catalog_representatives": len(catalog),
        "catalog_sha256": CATALOG_SHA256,
        "distinct_targets_at_radii_1_to_4": len(all_targets),
        "distinct_targets": len(targets),
        "map_sha256": MAP_SHA256,
        "networkx": nx.__version__,
        "nonempty_parents": len(per_parent),
        "transitions": len(seen_flip_sets),
        "transitions_at_radii_1_to_4": all_transitions,
        "zero_parents": sorted(set(range(328)) - set(per_parent)),
    }
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
