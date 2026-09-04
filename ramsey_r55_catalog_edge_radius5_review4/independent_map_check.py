#!/usr/bin/env python3
"""Independent NetworkX audit of the radius-five Ramsey transition map.

This checker imports no submitted module.  NetworkX supplies a separate
graph6 decoder, maximal-clique implementation, complementation, and VF2++
isomorphism implementation.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

import networkx as nx


CATALOG_SHA256 = "067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb"
MAP_HASHES = {
    2: "5e1cafc6ba00cdf2bd48c8e4c45748ef29cc88328b1119dbda8898c58215afe5",
    3: "d2e3e2a88be4af996bc27f8740945ce73684c9a0e1c62cb7aea9def1c012372d",
    4: "b7265672d34b876ceb1f371ab8b8a6cde7c970a0d0fbf4daed1d783a860a9b3b",
    5: "46efec29ef9e4bcf326fd530d3ebbf43d3adb7687ee68ce356eadfe3a8c991da",
}
EXPECTED_DISTRIBUTION = {
    0: 16,
    1: 8,
    2: 16,
    4: 8,
    5: 8,
    8: 16,
    14: 32,
    20: 48,
    21: 8,
    22: 48,
    23: 32,
    27: 16,
    28: 48,
    33: 8,
    36: 16,
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contains_five_clique(graph: nx.Graph) -> bool:
    return any(len(clique) >= 5 for clique in nx.find_cliques(graph))


def parse_edge(text: str) -> tuple[int, int]:
    fields = text.split(",")
    if len(fields) != 2:
        raise ValueError(f"bad edge {text!r}")
    low, high = map(int, fields)
    if not 0 <= low < high < 42:
        raise ValueError(f"bad edge {text!r}")
    return low, high


def edge_index(edge: tuple[int, int]) -> int:
    low, high = edge
    return high * (high - 1) // 2 + low


def map_rows(path: Path, radius: int):
    lines = path.read_text(encoding="ascii").splitlines()
    for line in lines[1:]:
        if line.startswith("# SUMMARY "):
            break
        fields = line.split("\t")
        if radius == 2:
            if len(fields) != 6:
                raise AssertionError("bad radius-two row")
            yield int(fields[1]), fields[-2], int(fields[-1])
        else:
            if len(fields) != radius + 3:
                raise AssertionError(f"bad radius-{radius} row")
            yield int(fields[0]), fields[-2], int(fields[-1])


def main() -> None:
    here = Path(__file__).resolve().parent
    root = here.parent
    artifact = root / "ramsey_r55_catalog_edge_radius5_classification"
    catalog_path = artifact / "r55_42some.g6"
    map_path = artifact / "EDGE_RADIUS5_MAP.tsv"
    if sha256(catalog_path) != CATALOG_SHA256 or sha256(map_path) != MAP_HASHES[5]:
        raise AssertionError("unexpected catalog or radius-five map bytes")

    catalog = [
        nx.from_graph6_bytes(row.encode("ascii"))
        for row in catalog_path.read_text(encoding="ascii").splitlines()
        if row
    ]
    if len(catalog) != 328 or any(len(graph) != 42 for graph in catalog):
        raise AssertionError("unexpected catalog census")
    complements = [nx.complement(graph) for graph in catalog]
    for index, graph in enumerate(catalog):
        if contains_five_clique(graph) or contains_five_clique(complements[index]):
            raise AssertionError(f"catalog graph {index} is not Ramsey(5,5)")

    lines = map_path.read_text(encoding="ascii").splitlines()
    expected_header = (
        "parent\tedge_1\tedge_2\tedge_3\tedge_4\tedge_5\t"
        "target_kind\ttarget_index"
    )
    expected_summary = (
        "# SUMMARY transitions=6224 base_transitions=6154 "
        "complement_transitions=70 distinct_targets=346 "
        "base_targets=310 complement_targets=36"
    )
    if lines[0] != expected_header or lines[-1] != expected_summary:
        raise AssertionError("unexpected map framing")

    seen = set()
    per_parent: Counter[int] = Counter()
    target_kinds: Counter[str] = Counter()
    targets = set()
    for row_number, line in enumerate(lines[1:-1], start=2):
        fields = line.split("\t")
        if len(fields) != 8:
            raise AssertionError(f"bad map row {row_number}")
        parent = int(fields[0])
        target_kind, target_index = fields[6], int(fields[7])
        if not 0 <= parent < 328 or not 0 <= target_index < 328:
            raise AssertionError(f"bad index at row {row_number}")
        if target_kind not in {"base", "complement"}:
            raise AssertionError(f"bad target kind at row {row_number}")
        flips = tuple(parse_edge(text) for text in fields[1:6])
        if len(set(flips)) != 5 or list(flips) != sorted(flips, key=edge_index):
            raise AssertionError(f"bad flip set at row {row_number}")
        key = parent, flips
        if key in seen:
            raise AssertionError(f"duplicate flip set at row {row_number}")
        seen.add(key)

        variant = catalog[parent].copy()
        for low, high in flips:
            if variant.has_edge(low, high):
                variant.remove_edge(low, high)
            else:
                variant.add_edge(low, high)
        if contains_five_clique(variant) or contains_five_clique(nx.complement(variant)):
            raise AssertionError(f"mapped variant {row_number} is not Ramsey(5,5)")
        target = catalog[target_index] if target_kind == "base" else complements[target_index]
        if not nx.vf2pp_is_isomorphic(variant, target):
            raise AssertionError(f"wrong target isomorphism at row {row_number}")
        per_parent[parent] += 1
        target_kinds[target_kind] += 1
        targets.add((target_kind, target_index))

    if len(seen) != 6224 or target_kinds != {"base": 6154, "complement": 70}:
        raise AssertionError("transition census mismatch")
    if len(targets) != 346:
        raise AssertionError("target-class census mismatch")
    distribution = Counter(per_parent.get(index, 0) for index in range(328))
    if dict(sorted(distribution.items())) != EXPECTED_DISTRIBUTION:
        raise AssertionError("per-parent distribution mismatch")

    all_transitions = 0
    all_targets = set()
    for radius in range(2, 6):
        directory = root / f"ramsey_r55_catalog_edge_radius{radius}_classification"
        lower_path = directory / f"EDGE_RADIUS{radius}_MAP.tsv"
        if sha256(lower_path) != MAP_HASHES[radius]:
            raise AssertionError(f"unexpected radius-{radius} map bytes")
        for _parent, kind, target_index in map_rows(lower_path, radius):
            if kind not in {"base", "complement"} or not 0 <= target_index < 328:
                raise AssertionError(f"bad radius-{radius} target")
            all_transitions += 1
            all_targets.add((kind, target_index))
    if all_transitions != 30872 or len(all_targets) != 540:
        raise AssertionError("radii-one-through-five union mismatch")

    print(json.dumps({
        "all_catalog_graphs_ramsey_5_5": True,
        "all_mapped_variants_ramsey_5_5": True,
        "all_target_isomorphisms_verified": True,
        "catalog_representatives": len(catalog),
        "distinct_targets_at_radii_1_to_5": len(all_targets),
        "map_sha256": MAP_HASHES[5],
        "networkx": nx.__version__,
        "nonempty_parents": len(per_parent),
        "radius5_distinct_targets": len(targets),
        "radius5_transitions": len(seen),
        "transitions_at_radii_1_to_5": all_transitions,
        "zero_transition_parents": [i for i in range(328) if not per_parent[i]],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
