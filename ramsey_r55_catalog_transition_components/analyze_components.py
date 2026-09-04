#!/usr/bin/env python3
"""Derive exact catalog-class transition components through edge radius six.

The input maps are the exact labeled-transition maps in the five sibling
artifacts.  Only the 328 stored representatives were searched there.  Every
transition is therefore lifted under complementation to cover all 656 known
orientations.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
from collections import deque
from dataclasses import dataclass
from pathlib import Path


N_CATALOG = 328
Node = tuple[int, int]  # (0 = stored/base, 1 = complement, catalog index)
Edge = tuple[Node, Node]

INPUTS = {
    2: (
        "ramsey_r55_catalog_edge_radius2_classification/EDGE_RADIUS2_MAP.tsv",
        "5e1cafc6ba00cdf2bd48c8e4c45748ef29cc88328b1119dbda8898c58215afe5",
    ),
    3: (
        "ramsey_r55_catalog_edge_radius3_classification/EDGE_RADIUS3_MAP.tsv",
        "d2e3e2a88be4af996bc27f8740945ce73684c9a0e1c62cb7aea9def1c012372d",
    ),
    4: (
        "ramsey_r55_catalog_edge_radius4_classification/EDGE_RADIUS4_MAP.tsv",
        "b7265672d34b876ceb1f371ab8b8a6cde7c970a0d0fbf4daed1d783a860a9b3b",
    ),
    5: (
        "ramsey_r55_catalog_edge_radius5_classification/EDGE_RADIUS5_MAP.tsv",
        "46efec29ef9e4bcf326fd530d3ebbf43d3adb7687ee68ce356eadfe3a8c991da",
    ),
    6: (
        "ramsey_r55_catalog_edge_radius6_classification/EDGE_RADIUS6_MAP.tsv",
        "ea3dd948e333153f0bf844e279d7df2788849dfe676d6e45af1aaf74e1e29e72",
    ),
}

EXPECTED_EXACT_ROWS = {1: 2040, 2: 5568, 3: 8632, 4: 8408, 5: 6224, 6: 6384}
EXPECTED_NEW_EDGES = {1: 1976, 2: 5248, 3: 7976, 4: 7672, 5: 5488, 6: 4880}
EXPECTED_COMPONENT_SIZES = {
    1: [128, 128, 96, 96, 48, 48, 40, 40, 12, 12, 4, 4],
    2: [128, 128, 96, 96, 48, 48, 40, 40, 12, 12, 4, 4],
    3: [128, 128, 96, 96, 48, 48, 40, 40, 12, 12, 4, 4],
    4: [272, 272, 40, 40, 12, 12, 4, 4],
    5: [272, 272, 40, 40, 12, 12, 4, 4],
    6: [272, 272, 40, 40, 12, 12, 4, 4],
}
EXPECTED_DIAMETERS = {
    1: [7, 7, 8, 8, 6, 6, 6, 6, 4, 4, 2, 2],
    2: [4, 4, 4, 4, 3, 3, 3, 3, 2, 2, 1, 1],
    3: [3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 1, 1],
    4: [5, 5, 2, 2, 1, 1, 1, 1],
    5: [4, 4, 2, 2, 1, 1, 1, 1],
    6: [4, 4, 1, 1, 1, 1, 1, 1],
}


@dataclass(frozen=True)
class Transition:
    radius: int
    parent: int
    target: Node
    flips: tuple[tuple[int, int], ...]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            value.update(block)
    return value.hexdigest()


def parse_edge(text: str) -> tuple[int, int]:
    parts = text.split(",")
    if len(parts) != 2:
        raise RuntimeError(f"bad edge field {text!r}")
    u, v = map(int, parts)
    if not 0 <= u < v < 42:
        raise RuntimeError(f"bad edge endpoints {text!r}")
    return u, v


def read_maps(repo_root: Path) -> dict[int, list[Transition]]:
    by_radius = {radius: [] for radius in range(1, 7)}
    seen_assignments: dict[int, set[tuple[int, frozenset[tuple[int, int]]]]] = {
        radius: set() for radius in range(1, 7)
    }
    for file_radius, (relative, expected_hash) in INPUTS.items():
        path = repo_root / relative
        actual_hash = digest(path)
        if actual_hash != expected_hash:
            raise RuntimeError(
                f"input hash mismatch for {relative}: {actual_hash} != {expected_hash}"
            )
        summary = None
        data_lines = []
        with path.open(encoding="ascii") as source:
            header = source.readline().rstrip("\n").split("\t")
            for line in source:
                if line.startswith("# SUMMARY "):
                    summary = dict(item.split("=", 1) for item in line.split()[2:])
                    break
                if line.strip():
                    data_lines.append(line)
        if summary is None:
            raise RuntimeError(f"missing summary in {relative}")
        rows = csv.DictReader(data_lines, delimiter="\t", fieldnames=header)
        file_count = 0
        for row in rows:
            radius = int(row["radius"]) if "radius" in row else file_radius
            if file_radius == 2:
                if radius not in {1, 2}:
                    raise RuntimeError(f"unexpected radius in {relative}: {radius}")
            elif radius != file_radius:
                raise RuntimeError(f"unexpected radius in {relative}: {radius}")
            parent = int(row["parent"])
            target_index = int(row["target_index"])
            target_kind = row["target_kind"]
            if not 0 <= parent < N_CATALOG or not 0 <= target_index < N_CATALOG:
                raise RuntimeError(f"catalog index out of range in {relative}")
            if target_kind not in {"base", "complement"}:
                raise RuntimeError(f"bad target kind in {relative}: {target_kind}")
            flips = tuple(parse_edge(row[f"edge_{i}"]) for i in range(1, radius + 1))
            if len(set(flips)) != radius:
                raise RuntimeError(f"repeated flip for parent {parent} in {relative}")
            assignment = (parent, frozenset(flips))
            if assignment in seen_assignments[radius]:
                raise RuntimeError(f"duplicate labeled assignment at radius {radius}: {assignment}")
            seen_assignments[radius].add(assignment)
            target = (0 if target_kind == "base" else 1, target_index)
            by_radius[radius].append(Transition(radius, parent, target, flips))
            file_count += 1
        if file_radius == 2:
            summarized = int(summary["radius1"]) + int(summary["radius2"])
        else:
            summarized = int(summary["transitions"])
        if summarized != file_count:
            raise RuntimeError(f"summary count mismatch in {relative}")
    counts = {radius: len(rows) for radius, rows in by_radius.items()}
    if counts != EXPECTED_EXACT_ROWS:
        raise RuntimeError(f"exact-row count mismatch: {counts}")
    return by_radius


def canonical_edge(a: Node, b: Node) -> Edge | None:
    if a == b:
        return None
    return (a, b) if a < b else (b, a)


def lifted_edges(transition: Transition) -> tuple[Edge | None, Edge | None]:
    base_parent = (0, transition.parent)
    target = transition.target
    base_edge = canonical_edge(base_parent, target)
    complement_edge = canonical_edge(
        (1, transition.parent), (1 - target[0], target[1])
    )
    return base_edge, complement_edge


def adjacency(edges: set[Edge]) -> dict[Node, set[Node]]:
    graph = {(kind, index): set() for kind in (0, 1) for index in range(N_CATALOG)}
    for a, b in edges:
        graph[a].add(b)
        graph[b].add(a)
    return graph


def bfs_components(graph: dict[Node, set[Node]]) -> list[list[Node]]:
    seen = set()
    result = []
    for start in sorted(graph):
        if start in seen:
            continue
        seen.add(start)
        queue = deque([start])
        component = []
        while queue:
            vertex = queue.popleft()
            component.append(vertex)
            for neighbor in sorted(graph[vertex]):
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        result.append(sorted(component))
    return sorted(result, key=lambda component: (-len(component), component[0]))


def union_find_components(edges: set[Edge]) -> list[list[Node]]:
    nodes = [(kind, index) for kind in (0, 1) for index in range(N_CATALOG)]
    parent = {node: node for node in nodes}

    def find(node: Node) -> Node:
        while parent[node] != node:
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    def union(a: Node, b: Node) -> None:
        a, b = find(a), find(b)
        if a != b:
            parent[max(a, b)] = min(a, b)

    for a, b in sorted(edges):
        union(a, b)
    groups: dict[Node, list[Node]] = {}
    for node in nodes:
        groups.setdefault(find(node), []).append(node)
    return sorted(
        (sorted(component) for component in groups.values()),
        key=lambda component: (-len(component), component[0]),
    )


def component_diameter(component: list[Node], graph: dict[Node, set[Node]]) -> int:
    allowed = set(component)
    diameter = 0
    for start in component:
        distance = {start: 0}
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            for neighbor in graph[vertex]:
                if neighbor in allowed and neighbor not in distance:
                    distance[neighbor] = distance[vertex] + 1
                    queue.append(neighbor)
        if len(distance) != len(component):
            raise RuntimeError("purported component is disconnected")
        diameter = max(diameter, max(distance.values()))
    return diameter


def component_pairs_outside(components: list[list[Node]]) -> int:
    total = N_CATALOG * 2
    all_pairs = total * (total - 1) // 2
    internal = sum(len(component) * (len(component) - 1) // 2 for component in components)
    return all_pairs - internal


def format_node(node: Node) -> str:
    return f"{'B' if node[0] == 0 else 'C'}{node[1]:03d}"


def membership_text(components: list[list[Node]]) -> str:
    component_of = {node: number for number, component in enumerate(components) for node in component}
    complement_of = {}
    for number, component in enumerate(components):
        complemented = {(1 - kind, index) for kind, index in component}
        partners = {component_of[node] for node in complemented}
        if len(partners) != 1:
            raise RuntimeError(f"component {number} has no unique complement partner")
        complement_of[number] = partners.pop()
    lines = ["component\tcomplement_component\torientation\tcatalog_index"]
    for number, component in enumerate(components):
        for kind, index in component:
            lines.append(
                f"{number}\t{complement_of[number]}\t"
                f"{'base' if kind == 0 else 'complement'}\t{index}"
            )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="directory containing this and the five input artifact directories",
    )
    parser.add_argument(
        "--write-components",
        type=Path,
        help="write the derived radius-six membership table to this path",
    )
    args = parser.parse_args()

    by_radius = read_maps(args.repo_root)
    cumulative_edges: set[Edge] = set()
    radius3_components = None
    radius4_bridge_edges: dict[tuple[int, int], set[Edge]] = {}
    radius4_bridge_rows: dict[tuple[int, int], list[Transition]] = {}
    final_components = None

    for radius in range(1, 7):
        before = set(cumulative_edges)
        if radius == 4:
            radius3_components = bfs_components(adjacency(cumulative_edges))
            radius3_id = {
                node: number
                for number, component in enumerate(radius3_components)
                for node in component
            }
        for transition in by_radius[radius]:
            for lift_number, edge in enumerate(lifted_edges(transition)):
                if edge is None:
                    continue
                if radius == 4 and radius3_id[edge[0]] != radius3_id[edge[1]]:
                    pair = tuple(sorted((radius3_id[edge[0]], radius3_id[edge[1]])))
                    radius4_bridge_edges.setdefault(pair, set()).add(edge)
                    if lift_number == 0:
                        radius4_bridge_rows.setdefault(pair, []).append(transition)
                cumulative_edges.add(edge)
        graph = adjacency(cumulative_edges)
        components = bfs_components(graph)
        if components != union_find_components(cumulative_edges):
            raise RuntimeError(f"BFS/union-find disagreement at radius {radius}")
        sizes = [len(component) for component in components]
        diameters = [component_diameter(component, graph) for component in components]
        new_edges = len(cumulative_edges - before)
        if new_edges != EXPECTED_NEW_EDGES[radius]:
            raise RuntimeError(f"new-edge mismatch at radius {radius}: {new_edges}")
        if sizes != EXPECTED_COMPONENT_SIZES[radius]:
            raise RuntimeError(f"component-size mismatch at radius {radius}: {sizes}")
        if diameters != EXPECTED_DIAMETERS[radius]:
            raise RuntimeError(f"diameter mismatch at radius {radius}: {diameters}")
        complement_edges = {
            canonical_edge((1 - a[0], a[1]), (1 - b[0], b[1]))
            for a, b in cumulative_edges
        }
        if complement_edges != cumulative_edges:
            raise RuntimeError(f"edge set is not complement-invariant at radius {radius}")
        print(
            f"radius={radius} exact_rows={len(by_radius[radius])} "
            f"new_class_edges={new_edges} cumulative_class_edges={len(cumulative_edges)} "
            f"components={len(components)} cross_component_pairs={component_pairs_outside(components)} "
            f"sizes={','.join(map(str, sizes))} diameters={','.join(map(str, diameters))}"
        )
        final_components = components

    if radius3_components is None or final_components is None:
        raise RuntimeError("internal radius bookkeeping failure")
    expected_bridge_pairs = {(0, 3), (0, 4), (1, 2), (1, 5)}
    if set(radius4_bridge_edges) != expected_bridge_pairs:
        raise RuntimeError(f"unexpected radius-four bridge pairs: {radius4_bridge_edges.keys()}")
    if any(len(edges) != 32 for edges in radius4_bridge_edges.values()):
        raise RuntimeError("each radius-four component bridge must contain 32 class edges")
    for pair in ((0, 3), (0, 4)):
        rows = radius4_bridge_rows[pair]
        if len(rows) != 80:
            raise RuntimeError(f"unexpected labeled bridge-row count for {pair}: {len(rows)}")
        witness = min(rows, key=lambda row: (row.parent, row.target, row.flips))
        print(
            f"radius4_bridge={pair[0]}-{pair[1]} "
            f"component_sizes={len(radius3_components[pair[0]])}+{len(radius3_components[pair[1]])} "
            f"class_edges={len(radius4_bridge_edges[pair])} labeled_base_rows={len(rows)} "
            f"witness={format_node((0, witness.parent))}->{format_node(witness.target)} "
            f"flips={';'.join(f'{u},{v}' for u, v in witness.flips)}"
        )
    print("radius4_bridge_complement_pairs=1-2,1-5 class_edges_each=32")

    members = membership_text(final_components)
    counts = []
    component_of = {
        node: number
        for number, component in enumerate(final_components)
        for node in component
    }
    for number, component in enumerate(final_components):
        base_count = sum(kind == 0 for kind, _ in component)
        partner = component_of[(1 - component[0][0], component[0][1])]
        counts.append(f"{number}:{len(component)}:{base_count}/{len(component)-base_count}:{partner}")
    print("radius6_components=id:size:base/complement:partner " + " ".join(counts))
    member_hash = hashlib.sha256(members.encode("ascii")).hexdigest()
    print(f"radius6_membership_sha256={member_hash}")

    committed_members = Path(__file__).resolve().parent / "COMPONENTS_RADIUS6.tsv"
    if committed_members.exists() and committed_members.read_text(encoding="ascii") != members:
        raise RuntimeError("committed COMPONENTS_RADIUS6.tsv does not match the derivation")
    if args.write_components is not None:
        args.write_components.write_text(members, encoding="ascii")


if __name__ == "__main__":
    main()
