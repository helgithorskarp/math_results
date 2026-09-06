#!/usr/bin/env python3
"""Independent exact review of the fixed 122-centre incidence theorem.

No executable code from the reviewed package is imported. Coordinates are
scaled to integer coefficient vectors in Q(sqrt(3),sqrt(5),sqrt(11)); graph
components and the unique cycle are recovered by exhaustive bridge testing.
"""

from __future__ import annotations

import argparse
from collections import Counter, deque
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from math import lcm
import os
from pathlib import Path
import sys


DENOMINATOR = 96
RADICANDS = (1, 3, 5, 15, 11, 33, 55, 165)
EXPECTED_NORM_HASH = "f319dfe814bb9a2259a914b74c79adde9272422e4e761d57dc308fc750a638f7"
EXPECTED_EDGE_HASH = "76bb5adb53ddc6cb7def884a6a999cf3d570af5ed27bbb3a199be6eba3e012d4"
EXPECTED_CYCLE = [1239, 1370, 1522, 1371]
EXPECTED_MIXED = [170, 436, 1239, 1527]


class ReviewFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReviewFailure(message)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def file_record(path: Path) -> dict[str, int | str]:
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": sha256(raw).hexdigest()}


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def verify_sha256s(directory: Path) -> dict[str, dict[str, int | str]]:
    records = {}
    for line in (directory / "SHA256SUMS").read_text(encoding="ascii").splitlines():
        expected, name = line.split(maxsplit=1)
        record = file_record(directory / name)
        require(record["sha256"] == expected, "submitted source hash: " + name)
        records[name] = record
    return records


def scaled_axis(raw: list[object]) -> tuple[int, ...]:
    require(isinstance(raw, list) and len(raw) == 8, "radical-basis axis width")
    values = [Fraction(value) * DENOMINATOR for value in raw]
    require(all(value.denominator == 1 for value in values),
            "coordinate denominator divides 96")
    return tuple(int(value) for value in values)


def scaled_point(raw: list[list[object]]) -> tuple[tuple[int, ...], tuple[int, ...]]:
    require(isinstance(raw, list) and len(raw) == 2, "point has two axes")
    return scaled_axis(raw[0]), scaled_axis(raw[1])


def ring_product(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    """Coefficient convolution in the eight-dimensional multiquadratic basis."""
    require(len(left) == len(right) == 8, "coefficient-vector width")
    result = [0] * 8
    for left_mask, left_value in enumerate(left):
        for right_mask, right_value in enumerate(right):
            overlap = left_mask & right_mask
            square_factor = 1
            for bit, prime in enumerate((3, 5, 11)):
                if overlap & (1 << bit):
                    square_factor *= prime
            result[left_mask ^ right_mask] += left_value * right_value * square_factor
    return tuple(result)


def exact_squared_distance(left, right) -> tuple[int, ...]:
    answer = [0] * 8
    for axis in (0, 1):
        delta = tuple(a - b for a, b in zip(left[axis], right[axis]))
        square = ring_product(delta, delta)
        answer = [a + b for a, b in zip(answer, square)]
    return tuple(answer)


def histogram(values) -> dict[str, int]:
    counts = Counter(values)
    return {str(key): counts[key] for key in sorted(counts)}


def graph_components(vertices: list[int], adjacency: dict[int, set[int]]) -> list[list[int]]:
    unseen = set(vertices)
    answer = []
    while unseen:
        root = min(unseen)
        queue = deque([root])
        component = {root}
        while queue:
            vertex = queue.popleft()
            for neighbour in sorted(adjacency[vertex] - component):
                component.add(neighbour)
                queue.append(neighbour)
        unseen -= component
        answer.append(sorted(component))
    return answer


def reachable_without_edge(start: int, finish: int, omitted: tuple[int, int], adjacency) -> bool:
    omitted = tuple(sorted(omitted))
    seen = {start}
    queue = deque([start])
    while queue:
        vertex = queue.popleft()
        for neighbour in adjacency[vertex]:
            if tuple(sorted((vertex, neighbour))) == omitted or neighbour in seen:
                continue
            if neighbour == finish:
                return True
            seen.add(neighbour)
            queue.append(neighbour)
    return False


def canonical_cycle(cycle_edges: list[tuple[int, int]]) -> list[int]:
    cycle_adjacency = {vertex: set() for edge in cycle_edges for vertex in edge}
    for left, right in cycle_edges:
        cycle_adjacency[left].add(right)
        cycle_adjacency[right].add(left)
    require(cycle_adjacency and all(len(row) == 2 for row in cycle_adjacency.values()),
            "non-bridge edges form one cycle")
    start = min(cycle_adjacency)
    cycle = [start, min(cycle_adjacency[start])]
    while True:
        options = cycle_adjacency[cycle[-1]] - {cycle[-2]}
        require(len(options) == 1, "cycle continuation")
        next_vertex = next(iter(options))
        if next_vertex == start:
            break
        require(next_vertex not in cycle, "simple cycle")
        cycle.append(next_vertex)
    require(set(cycle) == set(cycle_adjacency), "cycle exhausts all non-bridge vertices")
    return cycle


def reconstruct(repository: Path):
    old_path = repository / "hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json"
    fresh_path = repository / "hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json"
    old = load(old_path)
    labels = [index for index, provenance in enumerate(old["provenance"]) if "510" in provenance]
    require(len(labels) == 510 and labels == sorted(set(labels)), "exact increasing H510 labels")
    old_points = [scaled_point(old["coordinates"][str(label)]) for label in labels]
    rows = load(fresh_path)
    centre_ids = [row["centre_index"] for row in rows]
    require(len(centre_ids) == 122 and centre_ids == sorted(set(centre_ids)),
            "exact increasing fresh-centre labels")
    fresh_points = [scaled_point(row["coordinates"]) for row in rows]
    coordinate_denominator = 1
    for raw_point in [old["coordinates"][str(label)] for label in labels] \
            + [row["coordinates"] for row in rows]:
        for axis in raw_point:
            for coefficient in axis:
                coordinate_denominator = lcm(coordinate_denominator, Fraction(coefficient).denominator)
    require(coordinate_denominator == DENOMINATOR, "least common coefficient denominator is 96")
    require(len(set(old_points + fresh_points)) == 632, "632 distinct exact points")
    large = {
        vertex for vertex, point in enumerate(old_points)
        if all(point[axis][basis] == 0 for axis in (0, 1) for basis in (2, 3, 6, 7))
    }
    require(len(large) == 375, "375 old large-block vertices")

    unit = (DENOMINATOR * DENOMINATOR,) + (0,) * 7
    zero_axis = (0,) * 8
    zero = (zero_axis, zero_axis)
    rational_unit = ((DENOMINATOR,) + (0,) * 7, zero_axis)
    half_sqrt3 = ((0, DENOMINATOR // 2) + (0,) * 6,
                  (DENOMINATOR // 2,) + (0,) * 7)
    sqrt3_plus_sqrt5 = ((0, DENOMINATOR, DENOMINATOR) + (0,) * 5, zero_axis)
    arithmetic_controls = [
        (zero, rational_unit, unit),
        (zero, half_sqrt3, unit),
        (zero, sqrt3_plus_sqrt5,
         (8 * DENOMINATOR * DENOMINATOR, 0, 0,
          2 * DENOMINATOR * DENOMINATOR, 0, 0, 0, 0)),
        (sqrt3_plus_sqrt5, sqrt3_plus_sqrt5, (0,) * 8),
    ]
    for left, right, expected in arithmetic_controls:
        require(exact_squared_distance(left, right) == expected, "exact norm arithmetic control")
    norm_digest = sha256()
    fresh_edges = []
    fresh_pair_checks = 0
    for left_position, right_position in combinations(range(122), 2):
        norm = exact_squared_distance(fresh_points[left_position], fresh_points[right_position])
        left = centre_ids[left_position]
        right = centre_ids[right_position]
        norm_digest.update((f"F {left} {right} " + " ".join(map(str, norm)) + "\n").encode("ascii"))
        fresh_pair_checks += 1
        if norm == unit:
            fresh_edges.append((left, right))

    attachments = {}
    attachment_types = {}
    attachment_pair_checks = 0
    for position, row in enumerate(rows):
        neighbours = []
        centre = centre_ids[position]
        for vertex, old_point in enumerate(old_points):
            norm = exact_squared_distance(fresh_points[position], old_point)
            norm_digest.update((f"H {centre} {vertex} " + " ".join(map(str, norm)) + "\n").encode("ascii"))
            attachment_pair_checks += 1
            if norm == unit:
                neighbours.append(vertex)
        require(neighbours == row["neighbors"] and len(neighbours) == row["degree"] >= 4,
                "entrywise old-neighbour reconstruction")
        require(row["witness"] == sorted(set(row["witness"]))
                and len(row["witness"]) == 3 and set(row["witness"]) <= set(neighbours),
                "archived witness triple belongs to the exact neighbourhood")
        attachments[centre] = set(neighbours)
        large_count = len(set(neighbours) & large)
        attachment_types[centre] = (
            "L" if large_count == len(neighbours)
            else "S" if large_count == 0
            else "M"
        )
    require((fresh_pair_checks, attachment_pair_checks) == (7381, 62220),
            "complete pair domains")
    require(norm_digest.hexdigest() == EXPECTED_NORM_HASH, "complete exact norm-stream identity")

    adjacency = {vertex: set() for vertex in centre_ids}
    for left, right in fresh_edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    components = graph_components(centre_ids, adjacency)
    component_records = []
    for component in components:
        edge_count = sum(len(adjacency[vertex]) for vertex in component) // 2
        old_neighbours = set().union(*(attachments[vertex] for vertex in component))
        component_records.append({
            "centres": component,
            "edges": edge_count,
            "cycle_rank": edge_count - len(component) + 1,
            "types": histogram(attachment_types[vertex] for vertex in component),
            "old_L_neighbors": sorted(old_neighbours & large),
            "old_S_neighbors": sorted(old_neighbours - large),
        })

    cycle_edges = [
        edge for edge in fresh_edges
        if reachable_without_edge(edge[0], edge[1], edge, adjacency)
    ]
    bridges = [edge for edge in fresh_edges if edge not in cycle_edges]
    cycle = canonical_cycle(cycle_edges)
    require(cycle == EXPECTED_CYCLE, "exact unique four-cycle")
    require(len(cycle_edges) == 4 and len(bridges) == 53, "four cyclic edges and 53 bridges")
    require(all(record["cycle_rank"] in (0, 1) for record in component_records)
            and sum(record["cycle_rank"] for record in component_records) == 1,
            "65 tree components and one unicyclic component")

    edge_type_histogram = histogram(
        "".join(sorted((attachment_types[left], attachment_types[right])))
        for left, right in fresh_edges
    )
    mixed = sorted(vertex for vertex in centre_ids if attachment_types[vertex] == "M")
    require(mixed == EXPECTED_MIXED, "exact four mixed centres")
    require(all(attachments[vertex] & large == {0} for vertex in mixed),
            "origin is the only large neighbour of every mixed centre")
    require(edge_type_histogram == {"LL": 1, "MM": 3, "MS": 7, "SS": 46},
            "fresh edge types and large separation")
    mixed_edges = [edge for edge in fresh_edges if edge[0] in mixed and edge[1] in mixed]
    require(mixed_edges == [(170, 436), (436, 1239), (1239, 1527)],
            "H514 mixed-centre path inside the full fresh graph")
    large_touching = [edge for edge in fresh_edges if "L" in
                      (attachment_types[edge[0]], attachment_types[edge[1]])]
    require(all(attachment_types[left] == attachment_types[right] == "L"
                for left, right in large_touching), "no L-to-M or L-to-S fresh edge")

    large_component = next(record for record in component_records if len(record["centres"]) == 37)
    require(large_component["cycle_rank"] == 1
            and large_component["types"] == {"M": 4, "S": 33}
            and large_component["old_L_neighbors"] == [0]
            and len(large_component["old_S_neighbors"]) == 100,
            "complete 37-vertex coupled component interface")

    submitted_certificate = load(repository / "hadwiger_nelson_heule_fresh122_incidence/certificate.json")
    expected_certificate = {
        "attachment_types": {str(vertex): attachment_types[vertex] for vertex in centre_ids},
        "centre_ids": centre_ids,
        "components": component_records,
        "fresh_edges": [list(edge) for edge in fresh_edges],
        "unique_cycle": cycle,
    }
    require(submitted_certificate == expected_certificate,
            "entrywise submitted component and edge certificate")

    edge_stream = "".join(f"{left},{right}\n" for left, right in fresh_edges).encode("ascii")
    require(sha256(edge_stream).hexdigest() == EXPECTED_EDGE_HASH,
            "canonical ordered fresh-edge identity")
    return {
        "rows": rows,
        "centre_ids": centre_ids,
        "fresh_edges": fresh_edges,
        "attachments": attachments,
        "types": attachment_types,
        "adjacency": adjacency,
        "components": components,
        "component_records": component_records,
        "cycle": cycle,
        "cycle_edges": cycle_edges,
        "bridges": bridges,
        "large": large,
        "norm_stream_sha256": norm_digest.hexdigest(),
        "edge_stream_sha256": sha256(edge_stream).hexdigest(),
        "fresh_pair_checks": fresh_pair_checks,
        "attachment_pair_checks": attachment_pair_checks,
        "edge_type_histogram": edge_type_histogram,
        "arithmetic_controls": len(arithmetic_controls),
    }


def find_cycle_colouring(list_masks: tuple[int, ...]) -> tuple[int, ...] | None:
    for colouring in product(range(4), repeat=len(list_masks)):
        if all(list_masks[index] & (1 << colour) for index, colour in enumerate(colouring)) \
                and all(colouring[index] != colouring[(index + 1) % len(colouring)]
                        for index in range(len(colouring))):
            return colouring
    return None


def construct_full_two_list_colouring(data, cycle_masks: tuple[int, ...], case: int):
    pair_masks = [sum(1 << colour for colour in pair) for pair in combinations(range(4), 2)]
    lists = {
        vertex: pair_masks[(case + 3 * position + vertex) % len(pair_masks)]
        for position, vertex in enumerate(data["centre_ids"])
    }
    for vertex, mask in zip(data["cycle"], cycle_masks):
        lists[vertex] = mask
    colouring = {}
    cycle_colouring = find_cycle_colouring(cycle_masks)
    require(cycle_colouring is not None, "four-cycle two-list assignment is colourable")
    colouring.update(zip(data["cycle"], cycle_colouring))

    cycle_set = set(data["cycle"])
    for component in data["components"]:
        roots = [vertex for vertex in component if vertex in cycle_set]
        if not roots:
            roots = [min(component)]
            root = roots[0]
            colouring[root] = min(colour for colour in range(4) if lists[root] & (1 << colour))
        parent = {root: None for root in roots}
        queue = deque(roots)
        while queue:
            vertex = queue.popleft()
            for neighbour in sorted(data["adjacency"][vertex]):
                if neighbour in cycle_set or neighbour in parent:
                    continue
                parent[neighbour] = vertex
                available = [colour for colour in range(4)
                             if lists[neighbour] & (1 << colour) and colour != colouring[vertex]]
                require(available, "two-list tree extension")
                colouring[neighbour] = min(available)
                queue.append(neighbour)
    require(set(colouring) == set(data["centre_ids"]), "constructive colouring covers F")
    require(all(lists[vertex] & (1 << colouring[vertex]) for vertex in colouring),
            "constructive colouring respects lists")
    require(all(colouring[left] != colouring[right] for left, right in data["fresh_edges"]),
            "constructive colouring is proper")


def list_controls(data) -> dict[str, object]:
    pair_masks = tuple(sum(1 << colour for colour in pair) for pair in combinations(range(4), 2))
    cases = 0
    for cycle_masks in product(pair_masks, repeat=4):
        require(find_cycle_colouring(cycle_masks) is not None,
                "all four-cycle two-list assignments")
        construct_full_two_list_colouring(data, cycle_masks, cases)
        cases += 1
    require(cases == 1296, "six-to-the-four cycle-list domain")
    require(find_cycle_colouring((3, 3, 3)) is None,
            "identical two-lists expose the odd-cycle obstruction")
    return {
        "four_colour_pair_lists": len(pair_masks),
        "four_cycle_list_assignments": cases,
        "full_F_constructive_colourings": cases,
        "odd_triangle_identical_list_control_rejected": True,
    }


def rejection_controls(repository: Path, reconstructed) -> list[str]:
    certificate = load(repository / "hadwiger_nelson_heule_fresh122_incidence/certificate.json")
    rejected = []

    def reject(name, corrupted):
        try:
            require(corrupted == certificate, "entrywise certificate equality")
        except ReviewFailure:
            rejected.append(name)
        else:
            raise ReviewFailure("accepted malformed control: " + name)

    missing_edge = json.loads(json.dumps(certificate))
    missing_edge["fresh_edges"].pop()
    reject("missing_fresh_edge", missing_edge)
    wrong_cycle = json.loads(json.dumps(certificate))
    wrong_cycle["unique_cycle"][1], wrong_cycle["unique_cycle"][2] = (
        wrong_cycle["unique_cycle"][2], wrong_cycle["unique_cycle"][1])
    reject("noncycle_order", wrong_cycle)
    wrong_type = json.loads(json.dumps(certificate))
    wrong_type["attachment_types"]["170"] = "S"
    reject("wrong_attachment_type", wrong_type)
    require(len(reconstructed["cycle_edges"]) == 4, "positive bridge-control baseline")
    rejected.append("odd_cycle_two_list_obstruction")
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--target", type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    repository = args.repository.resolve()
    target = (args.target or repository / "hadwiger_nelson_heule_fresh122_incidence").resolve()

    reviewed_source = verify_sha256s(target)
    manifest = load(target / "manifest.json")
    for name, expected in manifest["input_files"].items():
        require(file_record(repository / name)["sha256"] == expected, "manifest input: " + name)
    data = reconstruct(repository)
    list_evidence = list_controls(data)

    component_histogram = histogram(len(component) for component in data["components"])
    degree_histogram = histogram(len(data["adjacency"][vertex]) for vertex in data["centre_ids"])
    type_histogram = histogram(data["types"].values())
    require(component_histogram == {"1": 55, "2": 7, "4": 1, "6": 2, "37": 1},
            "exact component-order histogram")
    require(degree_histogram == {"0": 55, "1": 33, "2": 23, "3": 10, "5": 1},
            "exact fresh-degree histogram")
    require(type_histogram == {"L": 43, "M": 4, "S": 75},
            "exact old-attachment type histogram")
    require(sum(len(data["attachments"][vertex]) for vertex in data["centre_ids"]) == 551,
            "exact 551 old attachments")

    submitted = load(target / "result.json")
    require((submitted["fresh_edges"], submitted["old_attachments"],
             submitted["components"], submitted["component_order_histogram"],
             submitted["attachment_type_histogram"], submitted["edge_type_histogram"],
             submitted["norm_stream_sha256"])
            == (len(data["fresh_edges"]), 551, len(data["components"]), component_histogram,
                type_histogram, data["edge_type_histogram"], data["norm_stream_sha256"]),
            "independent totals match submitted summary")

    result = {
        "all_checks_passed": True,
        "scope": "exact mutual incidence and two-list extension structure of the fixed 122 archived completion centres",
        "python": sys.version.split()[0],
        "reviewed_source_commit": "ac6553bd4ede54bea77c6ef4bd66c02638d8f297",
        "reviewed_source": reviewed_source,
        "inputs": {
            name: file_record(repository / name)
            for name in sorted(manifest["input_files"])
        },
        "exact_geometry": {
            "old_vertices": 510,
            "fresh_vertices": 122,
            "all_points_distinct": 632,
            "common_denominator": DENOMINATOR,
            "exact_norm_arithmetic_controls": data["arithmetic_controls"],
            "fresh_pair_checks": data["fresh_pair_checks"],
            "attachment_pair_checks": data["attachment_pair_checks"],
            "total_norm_vectors": data["fresh_pair_checks"] + data["attachment_pair_checks"],
            "norm_stream_sha256": data["norm_stream_sha256"],
            "fresh_edge_stream_sha256": data["edge_stream_sha256"],
            "fresh_edges": len(data["fresh_edges"]),
            "old_attachments": 551,
        },
        "decomposition": {
            "components": len(data["components"]),
            "component_order_histogram": component_histogram,
            "fresh_degree_histogram": degree_histogram,
            "bridges": len(data["bridges"]),
            "non_bridge_cycle_edges": [list(edge) for edge in data["cycle_edges"]],
            "unique_cycle": data["cycle"],
            "unique_cycle_length_even": len(data["cycle"]) % 2 == 0,
            "tree_components": sum(record["cycle_rank"] == 0 for record in data["component_records"]),
            "unicyclic_components": sum(record["cycle_rank"] == 1 for record in data["component_records"]),
        },
        "old_fresh_interface": {
            "old_large_vertices": len(data["large"]),
            "old_small_vertices": 510 - len(data["large"]),
            "attachment_type_histogram": type_histogram,
            "mixed_centres": EXPECTED_MIXED,
            "mixed_large_neighbour_sets": {
                str(vertex): sorted(data["attachments"][vertex] & data["large"])
                for vertex in EXPECTED_MIXED
            },
            "fresh_edge_type_histogram": data["edge_type_histogram"],
            "H514_mixed_path_edges": [[170, 436], [436, 1239], [1239, 1527]],
            "large_to_mixed_or_small_fresh_edges": 0,
            "coupled_component_order": 37,
            "coupled_component_old_large_neighbours": [0],
            "coupled_component_old_small_neighbours": 100,
        },
        "two_list_evidence": {
            **list_evidence,
            "structural_reason": "each component is a tree or consists of trees attached to the certified even four-cycle",
            "arbitrary_colour_universe_argument": "reduce to two-element sublists; greedily colour trees, while an even cycle alternates for equal lists and closes from an adjacent unequal-list pair otherwise",
        },
        "conclusion": {
            "fixed_F_exact_incidence_verified": True,
            "fixed_F_and_all_subgraphs_two_choosable": True,
            "uniform_four_colour_extension_criterion_valid": True,
            "arbitrary_list_dynamic_reduction_valid": True,
            "full_H_union_F_four_colourability_decided": False,
            "sub509_five_chromatic_graph_produced": False,
            "record_improvement": False,
        },
        "negative_controls_rejected": rejection_controls(repository, data),
        "trust_boundary": [
            "the two pinned raw coordinate tables and the standard degree-eight squarefree radical basis",
            "ordinary CPython integer/Fraction arithmetic, JSON decoding, and completeness of explicit finite loops",
            "the elementary tree and even-cycle list-colouring arguments stated in the review",
            "SHA-256 collision resistance for source and canonical stream identities",
            "the original 21,978,620-triple centre enumeration is intentionally outside the claim and is not trusted or repeated",
        ],
    }
    atomic_json(args.report, result)
    print(json.dumps({
        "all_checks_passed": True,
        "fresh_edges": len(data["fresh_edges"]),
        "components": len(data["components"]),
        "unique_cycle": data["cycle"],
        "two_list_cycle_cases": list_evidence["four_cycle_list_assignments"],
        "fixed_F_two_choosable": True,
        "whole_632_support_decided": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
