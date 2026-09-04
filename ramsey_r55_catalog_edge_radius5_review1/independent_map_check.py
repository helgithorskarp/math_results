#!/usr/bin/env python3
"""Independent positive-map and target-isomorphism audit for radius five."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

import networkx as nx


CATALOG_SHA256 = "067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb"
MAP_SHA256 = "46efec29ef9e4bcf326fd530d3ebbf43d3adb7687ee68ce356eadfe3a8c991da"
LOWER_MAP_HASHES = (
    "5e1cafc6ba00cdf2bd48c8e4c45748ef29cc88328b1119dbda8898c58215afe5",
    "d2e3e2a88be4af996bc27f8740945ce73684c9a0e1c62cb7aea9def1c012372d",
    "b7265672d34b876ceb1f371ab8b8a6cde7c970a0d0fbf4daed1d783a860a9b3b",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def has_five_clique(graph: nx.Graph) -> bool:
    return any(len(clique) >= 5 for clique in nx.find_cliques(graph))


def parse_edge(text: str) -> tuple[int, int]:
    pieces = text.split(",")
    assert len(pieces) == 2
    u, v = map(int, pieces)
    assert 0 <= u < v < 42
    return u, v


def main() -> None:
    here = Path(__file__).resolve().parent
    repo = here.parent
    artifact = repo / "ramsey_r55_catalog_edge_radius5_classification"
    catalog_path = artifact / "r55_42some.g6"
    map_path = artifact / "EDGE_RADIUS5_MAP.tsv"
    assert sha256(catalog_path) == CATALOG_SHA256
    assert sha256(map_path) == MAP_SHA256

    catalog = [
        nx.from_graph6_bytes(record.encode("ascii"))
        for record in catalog_path.read_text(encoding="ascii").splitlines()
        if record
    ]
    assert len(catalog) == 328 and all(len(graph) == 42 for graph in catalog)
    assert all(not has_five_clique(graph) and not has_five_clique(nx.complement(graph))
               for graph in catalog)
    complements = [nx.complement(graph) for graph in catalog]

    lines = map_path.read_text(encoding="ascii").splitlines()
    assert lines[0] == (
        "parent\tedge_1\tedge_2\tedge_3\tedge_4\tedge_5\t"
        "target_kind\ttarget_index"
    )
    assert lines[-1] == (
        "# SUMMARY transitions=6224 base_transitions=6154 "
        "complement_transitions=70 distinct_targets=346 "
        "base_targets=310 complement_targets=36"
    )

    seen: set[tuple[int, tuple[tuple[int, int], ...]]] = set()
    per_parent: Counter[int] = Counter()
    kinds: Counter[str] = Counter()
    targets: set[tuple[str, int]] = set()
    for row_number, line in enumerate(lines[1:-1], start=2):
        fields = line.split("\t")
        assert len(fields) == 8
        parent = int(fields[0])
        target_kind = fields[6]
        target_index = int(fields[7])
        assert 0 <= parent < 328 and 0 <= target_index < 328
        assert target_kind in {"base", "complement"}
        flips = tuple(parse_edge(text) for text in fields[1:6])
        assert len(set(flips)) == 5
        key = parent, tuple(sorted(flips))
        assert key not in seen, f"duplicate flip set at row {row_number}"
        seen.add(key)

        variant = catalog[parent].copy()
        for u, v in flips:
            if variant.has_edge(u, v):
                variant.remove_edge(u, v)
            else:
                variant.add_edge(u, v)
        assert not has_five_clique(variant)
        assert not has_five_clique(nx.complement(variant))
        target = catalog[target_index] if target_kind == "base" else complements[target_index]
        assert nx.vf2pp_is_isomorphic(variant, target), f"wrong target at row {row_number}"
        per_parent[parent] += 1
        kinds[target_kind] += 1
        targets.add((target_kind, target_index))

    assert len(seen) == 6224 and kinds == {"base": 6154, "complement": 70}
    assert len(targets) == 346
    assert Counter(per_parent.values()) == {
        1: 8, 2: 16, 4: 8, 5: 8, 8: 16, 14: 32, 20: 48,
        21: 8, 22: 48, 23: 32, 27: 16, 28: 48, 33: 8, 36: 16,
    }
    zero_parents = sorted(set(range(328)) - set(per_parent))
    assert zero_parents == [39, 41, 170, 171, 177, 188, 190, 191, 192, 193, 225, 253, 254, 271, 294, 305]

    lower_maps = (
        repo / "ramsey_r55_catalog_edge_radius2_classification" / "EDGE_RADIUS2_MAP.tsv",
        repo / "ramsey_r55_catalog_edge_radius3_classification" / "EDGE_RADIUS3_MAP.tsv",
        repo / "ramsey_r55_catalog_edge_radius4_classification" / "EDGE_RADIUS4_MAP.tsv",
    )
    assert tuple(sha256(path) for path in lower_maps) == LOWER_MAP_HASHES
    all_targets = set(targets)
    all_transitions = len(seen)
    for lower_map in lower_maps:
        for line in lower_map.read_text(encoding="ascii").splitlines()[1:]:
            if line.startswith("# SUMMARY "):
                break
            fields = line.split("\t")
            all_transitions += 1
            all_targets.add((fields[-2], int(fields[-1])))
    assert all_transitions == 30_872 and len(all_targets) == 540

    print(json.dumps({
        "all_catalog_graphs_ramsey_5_5": True,
        "all_mapped_variants_ramsey_5_5": True,
        "all_target_isomorphisms_verified": True,
        "catalog_representatives": len(catalog),
        "distinct_targets": len(targets),
        "distinct_targets_at_radii_1_to_5": len(all_targets),
        "map_sha256": MAP_SHA256,
        "networkx": nx.__version__,
        "nonempty_parents": len(per_parent),
        "transitions": len(seen),
        "transitions_at_radii_1_to_5": all_transitions,
        "zero_parents": zero_parents,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
