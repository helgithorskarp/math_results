#!/usr/bin/env python3
"""Independent audit of minimal Ramsey-preserving catalog moves through six flips.

This checker imports no target or transition-map code.  It parses all five
pinned maps, recomputes the inclusion minima and domination census, directly
checks the Ramsey property, and uses NetworkX VF2++ only for the separate
target-isomorphism cross-check.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import csv

import networkx as nx


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent
TARGET = REPOSITORY/"ramsey_r55_catalog_minimal_moves"
MAPS = {
    2: ("ramsey_r55_catalog_edge_radius2_classification/EDGE_RADIUS2_MAP.tsv",
        "5e1cafc6ba00cdf2bd48c8e4c45748ef29cc88328b1119dbda8898c58215afe5"),
    3: ("ramsey_r55_catalog_edge_radius3_classification/EDGE_RADIUS3_MAP.tsv",
        "d2e3e2a88be4af996bc27f8740945ce73684c9a0e1c62cb7aea9def1c012372d"),
    4: ("ramsey_r55_catalog_edge_radius4_classification/EDGE_RADIUS4_MAP.tsv",
        "b7265672d34b876ceb1f371ab8b8a6cde7c970a0d0fbf4daed1d783a860a9b3b"),
    5: ("ramsey_r55_catalog_edge_radius5_classification/EDGE_RADIUS5_MAP.tsv",
        "46efec29ef9e4bcf326fd530d3ebbf43d3adb7687ee68ce356eadfe3a8c991da"),
    6: ("ramsey_r55_catalog_edge_radius6_classification/EDGE_RADIUS6_MAP.tsv",
        "ea3dd948e333153f0bf844e279d7df2788849dfe676d6e45af1aaf74e1e29e72"),
}
EXPECTED_RADII = {1: 2040, 2: 5568, 3: 8632, 4: 8408, 5: 6224, 6: 6384}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_digest(path):
    return sha256(path.read_bytes()).hexdigest()


def parse_edge(field):
    parts = field.split(",")
    require(len(parts) == 2, ("edge field", field))
    low, high = map(int, parts)
    require(0 <= low < high < 42, ("edge endpoints", field))
    return low, high


def edge_index(edge):
    low, high = edge
    return high*(high-1)//2+low


def read_transition_maps():
    parents = {index: {} for index in range(328)}
    radii = Counter()
    for file_radius, (relative, expected_hash) in MAPS.items():
        path = REPOSITORY/relative
        require(file_digest(path) == expected_hash, ("map hash", relative))
        lines = path.read_text(encoding="ascii").splitlines()
        require(lines and lines[-1].startswith("# SUMMARY "), ("map summary", relative))
        rows = csv.DictReader(lines[:-1], delimiter="\t")
        file_count = 0
        for row in rows:
            radius = int(row["radius"]) if file_radius == 2 else file_radius
            require(1 <= radius <= 6, ("radius", radius))
            parent = int(row["parent"])
            target_index = int(row["target_index"])
            target_kind = row["target_kind"]
            require(0 <= parent < 328 and 0 <= target_index < 328,
                    ("catalog index", parent, target_index))
            require(target_kind in {"base", "complement"}, ("target kind", target_kind))
            edges = tuple(parse_edge(row[f"edge_{number}"])
                          for number in range(1, radius+1))
            require(len(set(edges)) == radius, ("repeated edge", parent, edges))
            support = frozenset(edges)
            require(support not in parents[parent], ("duplicate support", parent, support))
            parents[parent][support] = (target_kind, target_index)
            radii[radius] += 1
            file_count += 1
        summary = dict(item.split("=", 1) for item in lines[-1].split()[2:])
        declared = (int(summary["radius1"])+int(summary["radius2"])
                    if file_radius == 2 else int(summary["transitions"]))
        require(file_count == declared, ("declared map count", relative))
    require(dict(radii) == EXPECTED_RADII, ("radius histogram", radii))
    return parents


def decode_graph6(record):
    require(record and ord(record[0])-63 == 42, "graph6 order")
    bits = []
    for character in record[1:]:
        value = ord(character)-63
        require(0 <= value < 64, "graph6 byte")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    adjacency = [0]*42
    at = 0
    for high in range(1, 42):
        for low in range(high):
            if bits[at]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            at += 1
    return adjacency


def complement(adjacency):
    mask = (1 << len(adjacency))-1
    return [mask ^ (1 << vertex) ^ neighbors
            for vertex, neighbors in enumerate(adjacency)]


def contains_clique(adjacency, order=5):
    def visit(candidates, remaining):
        if candidates.bit_count() < remaining:
            return False
        if remaining == 1:
            return bool(candidates)
        while candidates.bit_count() >= remaining:
            bit = candidates & -candidates
            candidates ^= bit
            vertex = bit.bit_length()-1
            if visit(candidates & adjacency[vertex], remaining-1):
                return True
        return False
    return visit((1 << len(adjacency))-1, order)


def flipped_graph(parent, support):
    graph = parent.copy()
    for low, high in support:
        graph[low] ^= 1 << high
        graph[high] ^= 1 << low
    return graph


def ramsey(adjacency):
    return not contains_clique(adjacency) and not contains_clique(complement(adjacency))


def graph_from_bits(adjacency):
    graph = nx.Graph()
    graph.add_nodes_from(range(42))
    graph.add_edges_from((low, high) for high in range(1, 42)
                         for low in range(high) if adjacency[low] & (1 << high))
    return graph


def certificate_text(minimal, parents):
    lines = ["parent\tradius\tflips\ttarget_kind\ttarget_index\n"]
    for parent in range(328):
        ordered = sorted(minimal[parent],
                         key=lambda support: (len(support),
                             tuple(sorted(map(edge_index, support)))))
        for support in ordered:
            target_kind, target_index = parents[parent][support]
            edges = ";".join(f"{u},{v}" for u, v in
                             sorted(support, key=edge_index))
            lines.append(f"{parent}\t{len(support)}\t{edges}\t"
                         f"{target_kind}\t{target_index}\n")
    return "".join(lines)


def main():
    parents = read_transition_maps()
    catalog_path = (REPOSITORY/"ramsey_r55_catalog_edge_radius6_classification"/
                    "r55_42some.g6")
    require(file_digest(catalog_path) ==
            "067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb",
            "catalog hash")
    catalog = tuple(decode_graph6(line) for line in
                    catalog_path.read_text(encoding="ascii").splitlines())
    require(len(catalog) == 328 and all(ramsey(graph) for graph in catalog),
            "catalog base validation")
    nx_catalog = tuple(graph_from_bits(graph) for graph in catalog)
    nx_complements = tuple(nx.complement(graph) for graph in nx_catalog)

    minimal = {}
    minima_by_size = Counter()
    dominated = Counter()
    all_transition_ramsey_checks = 0
    proper_subset_checks = 0
    target_isomorphisms = 0
    for parent, transitions in parents.items():
        supports = set(transitions)
        parent_minimal = []
        for support in supports:
            ordered = tuple(support)
            has_valid_part = any(
                frozenset(part) in supports
                for size in range(1, len(ordered))
                for part in combinations(ordered, size)
            )
            if not has_valid_part:
                parent_minimal.append(support)

            graph = flipped_graph(catalog[parent], support)
            require(ramsey(graph), ("mapped move is not Ramsey", parent, support))
            all_transition_ramsey_checks += 1

        minimal[parent] = tuple(parent_minimal)
        minima_by_size.update(map(len, parent_minimal))
        for support in supports:
            contained = [part for part in parent_minimal if part <= support]
            require(contained, ("transition lacks a minimal subset", parent, support))
            smallest = min(map(len, contained))
            dominated[len(support), smallest] += 1

        for support in parent_minimal:
            graph = flipped_graph(catalog[parent], support)
            if len(support) == 4:
                require(len({vertex for edge in support for vertex in edge}) == 8,
                        ("quartet not a matching", parent, support))
                deleted = sum(bool(catalog[parent][u] & (1 << v)) for u, v in support)
                require(deleted == 2, ("quartet not balanced", parent, support))
            ordered = tuple(support)
            for size in range(1, len(ordered)):
                for part in combinations(ordered, size):
                    proper_subset_checks += 1
                    require(not ramsey(flipped_graph(catalog[parent], part)),
                            ("proper subset is Ramsey", parent, support, part))

            target_kind, target_index = transitions[support]
            target = (nx_catalog[target_index] if target_kind == "base"
                      else nx_complements[target_index])
            require(nx.vf2pp_is_isomorphic(graph_from_bits(graph), target),
                    ("wrong target isomorphism", parent, support, transitions[support]))
            target_isomorphisms += 1

    require(minima_by_size == {1: 2040, 4: 160}, minima_by_size)
    require(all_transition_ramsey_checks == sum(EXPECTED_RADII.values()),
            all_transition_ramsey_checks)
    require(proper_subset_checks == 2240, proper_subset_checks)

    produced = certificate_text(minimal, parents)
    committed = (TARGET/"MINIMAL_MOVES.tsv").read_text(encoding="ascii")
    require(produced == committed, "minimal-move certificate mismatch")
    require(sha256(produced.encode("ascii")).hexdigest() ==
            "27bfe713c711ab319bb9eb909cec997049e48c68e22539bbb54f543daea68896",
            "minimal-move certificate digest")

    distribution = Counter(len(minimal[parent]) for parent in minimal)
    require(distribution == {2: 4, 3: 8, 4: 12, 5: 24,
                             6: 72, 7: 104, 8: 96, 9: 8}, distribution)
    expected_dominated = {
        1: (2040, 0), 2: (5568, 0), 3: (8632, 0),
        4: (8248, 160), 5: (5968, 256), 6: (6256, 128),
    }
    for radius, (singles, quartets) in expected_dominated.items():
        require((dominated[radius, 1], dominated[radius, 4]) == (singles, quartets),
                ("domination histogram", radius, dominated))

    print("PASS independently parsed five maps: 37256 unique parent-relative moves")
    print("PASS direct Ramsey checks: 328 parents and all 37256 mapped moves")
    print("PASS inclusion minima: 2040 singletons and 160 balanced four-edge matchings")
    print("PASS proper-subset invalidity checks: 2240")
    print(f"PASS independent NetworkX {nx.__version__} target isomorphisms: {target_isomorphisms}")
    print("PASS certificate byte match: 27bfe713c711ab319bb9eb909cec997049e48c68e22539bbb54f543daea68896")
    print("PASS parent support counts 2..9: 4,8,12,24,72,104,96,8")
    print("PASS singleton-dominated radii 1..6: 2040,5568,8632,8248,5968,6256")
    print("PASS quartet-only radii 1..6: 0,0,0,160,256,128")
    print("SCOPE known catalog and radius-six maps only; no catalog completeness or R(5,5) bound")


if __name__ == "__main__":
    main()
