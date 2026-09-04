#!/usr/bin/env python3
"""Extract and directly check the inclusion-minimal valid catalog moves."""

import argparse
from collections import Counter
import hashlib
import importlib.util
from itertools import combinations
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def module(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    value = importlib.util.module_from_spec(spec)
    sys.modules[name] = value
    spec.loader.exec_module(value)
    return value


maps = module("component_maps", "ramsey_r55_catalog_transition_components/analyze_components.py")
direct = module("direct_graphs", "ramsey_r55_catalog_edge_radius6_classification/validate_variants.py")


def load():
    by_radius = maps.read_maps(ROOT)
    parents = {i: {} for i in range(328)}
    for radius, rows in by_radius.items():
        for row in rows:
            key = frozenset(row.flips)
            if key in parents[row.parent]:
                raise RuntimeError("duplicate transition")
            parents[row.parent][key] = row
    return parents


def proper_subsets(edges):
    edges = sorted(edges, key=direct.edge_index)
    for size in range(1, len(edges)):
        yield from (frozenset(c) for c in combinations(edges, size))


def valid(catalog, parent, edges):
    graph = catalog[parent].copy()
    for low, high in edges:
        graph[low] ^= 1 << high
        graph[high] ^= 1 << low
    return not direct.contains_clique(graph) and not direct.contains_clique(direct.complement(graph))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", type=Path, help="write the minimal-move certificate to a new path")
    args = parser.parse_args()
    parents = load()
    catalog_path = ROOT / "ramsey_r55_catalog_edge_radius6_classification/r55_42some.g6"
    if maps.digest(catalog_path) != "067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb":
        raise RuntimeError("catalog hash")
    catalog = [direct.decode_graph6(row) for row in catalog_path.read_text().splitlines()]
    primitive, dominated, counts = {}, Counter(), Counter()
    rows = ["parent\tradius\tflips\ttarget_kind\ttarget_index\n"]
    proper_checks = quartet_checks = 0
    for parent, transitions in parents.items():
        minimal = []
        # Definition-level test: enumerate every proper nonempty subset.
        for edges in transitions:
            if not any(part in transitions for part in proper_subsets(edges)):
                minimal.append(edges)
        minimal.sort(key=lambda s: (len(s), tuple(sorted(map(direct.edge_index, s)))))
        primitive[parent] = minimal
        counts.update(map(len, minimal))
        for edges in minimal:
            if not valid(catalog, parent, edges):
                raise RuntimeError("invalid minimal move")
            if len(edges) == 4:
                if len({vertex for edge in edges for vertex in edge}) != 8:
                    raise RuntimeError("quartet is not a matching")
                if sum(bool(catalog[parent][u] & (1 << v)) for u, v in edges) != 2:
                    raise RuntimeError("quartet is not color balanced")
                quartet_checks += 1
            for part in proper_subsets(edges):
                proper_checks += 1
                if valid(catalog, parent, part):
                    raise RuntimeError("a claimed primitive has a valid proper subset")
            row = transitions[edges]
            flips = ";".join(f"{u},{v}" for u, v in sorted(edges, key=direct.edge_index))
            kind = "base" if row.target[0] == 0 else "complement"
            rows.append(f"{parent}\t{len(edges)}\t{flips}\t{kind}\t{row.target[1]}\n")
        # Separate characterization: every transition contains a minimal move.
        for edges in transitions:
            first = min((len(part) for part in minimal if part <= edges), default=0)
            if not first:
                raise RuntimeError("uncovered transition")
            dominated[(len(edges), first)] += 1
    if counts != Counter({1: 2040, 4: 160}):
        raise RuntimeError(f"unexpected minimal counts {counts}")
    text = "".join(rows)
    if args.write:
        args.write.write_text(text, encoding="ascii")
    elif (HERE / "MINIMAL_MOVES.tsv").read_text(encoding="ascii") != text:
        raise RuntimeError("certificate differs")
    dist = Counter(len(m) for m in primitive.values())
    print("minimal_moves=2200 singles=2040 quartets=160 parents=328")
    print(f"direct_validity_checks=2200 proper_subset_invalidity_checks={proper_checks}")
    print(f"balanced_four_edge_matchings={quartet_checks}")
    print("blocking_clause_distribution=" + ",".join(f"{k}:{v}" for k, v in sorted(dist.items())))
    for radius in range(1, 7):
        print(f"radius={radius} valid_moves={sum(v for (r, k), v in dominated.items() if r == radius)} "
              f"contains_single={dominated[radius,1]} contains_quartet_only={dominated[radius,4]}")
    print("minimal_moves_sha256=" + hashlib.sha256(text.encode("ascii")).hexdigest())


if __name__ == "__main__":
    main()
