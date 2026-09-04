#!/usr/bin/env python3
"""Independent NetworkX audit of the radius-six Ramsey transition map."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "ramsey_r55_catalog_edge_radius6_classification"
CATALOG_SHA256 = "067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb"
MAP_HASHES = {
    2: "5e1cafc6ba00cdf2bd48c8e4c45748ef29cc88328b1119dbda8898c58215afe5",
    3: "d2e3e2a88be4af996bc27f8740945ce73684c9a0e1c62cb7aea9def1c012372d",
    4: "b7265672d34b876ceb1f371ab8b8a6cde7c970a0d0fbf4daed1d783a860a9b3b",
    5: "46efec29ef9e4bcf326fd530d3ebbf43d3adb7687ee68ce356eadfe3a8c991da",
    6: "ea3dd948e333153f0bf844e279d7df2788849dfe676d6e45af1aaf74e1e29e72",
}
EXPECTED_DISTRIBUTION = {
    0: 40, 1: 16, 9: 40, 14: 32, 15: 32, 16: 16, 19: 32,
    23: 8, 25: 8, 28: 24, 29: 16, 30: 8, 35: 16, 37: 8,
    43: 16, 57: 16,
}
EXPECTED_ZERO = [
    39, 41, 170, 171, 173, 175, 176, 177, 178, 188, 190, 191,
    192, 193, 225, 253, 254, 260, 261, 262, 263, 264, 267, 268,
    269, 271, 273, 274, 275, 276, 281, 282, 285, 288, 290, 291,
    294, 305, 326, 327,
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contains_five_clique(graph: nx.Graph) -> bool:
    return any(len(clique) >= 5 for clique in nx.find_cliques(graph))


def parse_edge(text: str) -> tuple[int, int]:
    low, high = map(int, text.split(","))
    if not 0 <= low < high < 42:
        raise ValueError(f"bad edge {text!r}")
    return low, high


def edge_index(edge: tuple[int, int]) -> int:
    low, high = edge
    return high * (high - 1) // 2 + low


def lower_map_targets(radius: int) -> tuple[int, set[tuple[str, int]]]:
    path = ROOT / f"ramsey_r55_catalog_edge_radius{radius}_classification" / f"EDGE_RADIUS{radius}_MAP.tsv"
    assert sha256(path) == MAP_HASHES[radius]
    transitions = 0
    targets = set()
    for line in path.read_text(encoding="ascii").splitlines()[1:]:
        if line.startswith("# SUMMARY "):
            break
        fields = line.split("\t")
        kind, index = fields[-2], int(fields[-1])
        assert kind in {"base", "complement"} and 0 <= index < 328
        transitions += 1
        targets.add((kind, index))
    return transitions, targets


def main() -> None:
    catalog_path = TARGET / "r55_42some.g6"
    map_path = TARGET / "EDGE_RADIUS6_MAP.tsv"
    assert sha256(catalog_path) == CATALOG_SHA256
    assert sha256(map_path) == MAP_HASHES[6]

    catalog = [
        nx.from_graph6_bytes(line.encode("ascii"))
        for line in catalog_path.read_text(encoding="ascii").splitlines()
        if line
    ]
    assert len(catalog) == 328 and all(len(graph) == 42 for graph in catalog)
    complements = [nx.complement(graph) for graph in catalog]
    for index, graph in enumerate(catalog):
        assert not contains_five_clique(graph), index
        assert not contains_five_clique(complements[index]), index

    lines = map_path.read_text(encoding="ascii").splitlines()
    assert lines[0] == (
        "parent\tedge_1\tedge_2\tedge_3\tedge_4\tedge_5\tedge_6\t"
        "target_kind\ttarget_index"
    )
    assert lines[-1] == (
        "# SUMMARY transitions=6384 base_transitions=6334 "
        "complement_transitions=50 distinct_targets=311 "
        "base_targets=288 complement_targets=23"
    )

    seen = set()
    per_parent: Counter[int] = Counter()
    target_kinds: Counter[str] = Counter()
    targets = set()
    for row_number, line in enumerate(lines[1:-1], 2):
        fields = line.split("\t")
        assert len(fields) == 9
        parent = int(fields[0])
        kind, index = fields[7], int(fields[8])
        assert 0 <= parent < 328 and kind in {"base", "complement"} and 0 <= index < 328
        flips = tuple(parse_edge(text) for text in fields[1:7])
        assert len(set(flips)) == 6 and list(flips) == sorted(flips, key=edge_index)
        key = parent, flips
        assert key not in seen, row_number
        seen.add(key)

        variant = catalog[parent].copy()
        for low, high in flips:
            if variant.has_edge(low, high):
                variant.remove_edge(low, high)
            else:
                variant.add_edge(low, high)
        assert not contains_five_clique(variant), row_number
        assert not contains_five_clique(nx.complement(variant)), row_number
        target = catalog[index] if kind == "base" else complements[index]
        assert nx.vf2pp_is_isomorphic(variant, target), row_number
        per_parent[parent] += 1
        target_kinds[kind] += 1
        targets.add((kind, index))

    assert len(seen) == 6384 and target_kinds == {"base": 6334, "complement": 50}
    assert len(targets) == 311
    distribution = Counter(per_parent.get(index, 0) for index in range(328))
    assert dict(sorted(distribution.items())) == EXPECTED_DISTRIBUTION
    assert [index for index in range(328) if not per_parent[index]] == EXPECTED_ZERO

    prior_transitions = 0
    prior_targets: set[tuple[str, int]] = set()
    for radius in range(2, 6):
        transitions, found_targets = lower_map_targets(radius)
        prior_transitions += transitions
        prior_targets.update(found_targets)
    assert prior_transitions == 30872 and len(prior_targets) == 540
    assert len(targets - prior_targets) == 12
    all_targets = prior_targets | targets
    assert len(seen) + prior_transitions == 37256 and len(all_targets) == 552
    assert sum(kind == "base" for kind, _ in all_targets) == 328
    assert sum(kind == "complement" for kind, _ in all_targets) == 224

    print(json.dumps({
        "all_catalog_graphs_ramsey_5_5": True,
        "all_mapped_variants_ramsey_5_5": True,
        "all_target_isomorphisms_verified": True,
        "catalog_representatives": len(catalog),
        "distinct_targets_at_radii_1_to_6": len(all_targets),
        "map_sha256": MAP_HASHES[6],
        "networkx": nx.__version__,
        "new_radius6_targets": len(targets - prior_targets),
        "nonempty_parents": len(per_parent),
        "radius6_distinct_targets": len(targets),
        "radius6_transitions": len(seen),
        "transitions_at_radii_1_to_6": len(seen) + prior_transitions,
        "zero_transition_parents": EXPECTED_ZERO,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
