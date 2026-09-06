#!/usr/bin/env python3
"""Independent exact review of the H560 one-pair Kempe interface.

No executable from the reviewed contribution or its parents is imported.
The checker reconstructs the unit-distance graph using recursive quadratic-
tower arithmetic, derives the complete normalized one-pair Kempe family,
checks every small negative list problem, verifies the ten submitted positive
covers, finds fresh optional colourings, and exhausts the endpoint boundary.
"""

from __future__ import annotations

import argparse
import copy
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from math import comb, gcd
import os
from pathlib import Path
import sys


TARGET_COMMIT = "2160f57c42e26a07a96fc9059419d57f8db10d5e"
TARGET_DIRECTORY = "hadwiger_nelson_heule560_kempe"
TARGET_HASHES = {
    ".gitignore": "0175fcafc5d8328c584d3df3eeba657ad2c5ccda3956d46d15e15adb9ecdd57c",
    "README.md": "a94989bc82648dd3c4d06988896e7d89b885e03839a93a765553bbadc7a53a2e",
    "build.py": "77eff6c2243ac1371000ab085fc6d77705a3febb8489623795fdf48c67045bda",
    "certificate.json": "289785ccccf47d967a3b1c3abd98f3a7fa9d188748f1aa525b292d176323cd4f",
    "expected.json": "21b794ee539d51f830b54d1fef59e403532b20f7cae6821a8fb56ae201e7c14f",
    "plan.json": "56493efdedf418e42b4d540a8e9934ef500c2dd56302e815c30f68b48e46de56",
    "validation.json": "3dd6dee753a1b93ff5b8ce92d61d85cbe8a66c6a295e292b1429b61d96a91082",
    "verify.py": "349be3153e8e6e09adc1f5a339811638845c01ad62ec9b73e7ed3457b258ce1c",
}
TARGET_MANIFEST_HASH = "1c8cd887f940a17e26fa3aef9b3a35f3add03fb73f0055c7f866005484eacdf8"
INPUT_HASHES = {
    "hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json":
        "bc8e0f5f5ec7fa5f2376cc77ba0e65f6023b340cf48990370d5eda575d30ae79",
    "hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json":
        "89345930e1bea184ce2457b0e14a015bcd9a2901cfc609a6468cf050234a8317",
    "hadwiger_nelson_heule632_minimize/boundary.json":
        "8732adbdfe9792d6b6496bfec89da64b0127c388c2bb79f892b1d35a9c396f5e",
    "hadwiger_nelson_heule560_degree_family/certificate.json":
        "357d140cbe9432da75402c5e6ad9d13aff8d90a14319d019a8c0cdf4459d529c",
}
OLD_INPUT = "hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json"
FRESH_INPUT = "hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json"
BOUNDARY_INPUT = "hadwiger_nelson_heule632_minimize/boundary.json"
COLOUR_INPUT = "hadwiger_nelson_heule560_degree_family/certificate.json"
HOST_EDGE_HASH = "8dd36c195b3e252ec2be150ea6a029375707293fec70b63da9fc157eed4140f0"
SEED_EDGE_HASH = "d74d9442321f512ca7bbb7cf0013ab3c65255608bf001b5d1def41367ebc4e68"
EXPECTED_TEMPLATE_HASH = "faad386a59949ff5b2c22cf2b8615cf1cccd777126e09342169299c0a801c3da"
RADICANDS = (1, 3, 5, 15, 11, 33, 55, 165)
SCALE = 96
UNIT = (SCALE * SCALE,) + (0,) * 7


class ReviewFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ReviewFailure(message)


def file_record(path: Path) -> dict[str, int | str]:
    raw = path.read_bytes()
    return {"bytes": len(raw), "sha256": sha256(raw).hexdigest()}


def stream_record(raw: bytes) -> dict[str, int | str]:
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


def verify_sources(repository: Path) -> dict[str, object]:
    target = repository / TARGET_DIRECTORY
    target_records = {}
    for name, expected in TARGET_HASHES.items():
        record = file_record(target / name)
        require(record["sha256"] == expected, "reviewed source identity: " + name)
        target_records[name] = record
    manifest_raw = (target / "SHA256SUMS").read_bytes()
    require(sha256(manifest_raw).hexdigest() == TARGET_MANIFEST_HASH,
            "reviewed manifest identity")
    manifest = {}
    for line in manifest_raw.decode("ascii").splitlines():
        digest, name = line.split(maxsplit=1)
        manifest[name] = digest
    require(manifest == TARGET_HASHES, "reviewed manifest entries")
    target_records["SHA256SUMS"] = {
        "bytes": len(manifest_raw), "sha256": TARGET_MANIFEST_HASH,
    }
    input_records = {}
    for name, expected in INPUT_HASHES.items():
        record = file_record(repository / name)
        require(record["sha256"] == expected, "mathematical input identity: " + name)
        input_records[name] = record
    return {"reviewed_files": target_records, "inputs": input_records}


# Vectors are recursively represented in Q(sqrt(3))(sqrt(5))(sqrt(11)).
# This differs from both reviewed geometry implementations.
def vector_add(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a + b for a, b in zip(left, right))


def vector_scale(value: tuple[int, ...], factor: int) -> tuple[int, ...]:
    return tuple(factor * entry for entry in value)


def tower_product(left: tuple[int, ...], right: tuple[int, ...],
                  primes: tuple[int, ...] = (11, 5, 3)) -> tuple[int, ...]:
    require(len(left) == len(right) == 2 ** len(primes), "tower vector shape")
    if not primes:
        return (left[0] * right[0],)
    half = len(left) // 2
    a, b = left[:half], left[half:]
    c, d = right[:half], right[half:]
    tail = primes[1:]
    low = vector_add(tower_product(a, c, tail),
                     vector_scale(tower_product(b, d, tail), primes[0]))
    high = vector_add(tower_product(a, d, tail), tower_product(b, c, tail))
    return low + high


def multiplication_controls() -> int:
    checks = 0
    for left_index, left_rad in enumerate(RADICANDS):
        for right_index, right_rad in enumerate(RADICANDS):
            left = tuple(int(index == left_index) for index in range(8))
            right = tuple(int(index == right_index) for index in range(8))
            common = gcd(left_rad, right_rad)
            output_rad = left_rad * right_rad // (common * common)
            expected = [0] * 8
            expected[RADICANDS.index(output_rad)] = common
            require(tower_product(left, right) == tuple(expected),
                    "quadratic-tower basis product")
            checks += 1
    require(checks == 64, "complete basis-product table")
    return checks


def scaled_axis(raw) -> tuple[int, ...]:
    require(isinstance(raw, list) and len(raw) == 8, "coordinate axis shape")
    values = [SCALE * Fraction(value) for value in raw]
    require(all(value.denominator == 1 for value in values),
            "coordinate denominator divides 96")
    return tuple(int(value) for value in values)


def scaled_point(raw):
    require(isinstance(raw, list) and len(raw) == 2, "coordinate point shape")
    return scaled_axis(raw[0]), scaled_axis(raw[1])


def squared_distance(left, right) -> tuple[int, ...]:
    total = (0,) * 8
    for axis in range(2):
        delta = tuple(a - b for a, b in zip(left[axis], right[axis]))
        total = vector_add(total, tower_product(delta, delta))
    return total


def edge_stream(edges) -> bytes:
    return "".join(f"{left},{right}\n" for left, right in edges).encode("ascii")


def reconstruct_geometry(repository: Path, boundary: dict) -> dict[str, object]:
    old = json.loads((repository / OLD_INPUT).read_text(encoding="utf-8"))
    old_labels = [int(label) for label in sorted(old["coordinates"], key=int)
                  if "510" in old["provenance"][int(label)]]
    require(len(old_labels) == 510 and old_labels == sorted(set(old_labels)),
            "canonical 510 old-coordinate labels")
    fresh = json.loads((repository / FRESH_INPUT).read_text(encoding="utf-8"))
    fresh_ids = [row["centre_index"] for row in fresh]
    require(len(fresh_ids) == 122 and fresh_ids == sorted(set(fresh_ids)),
            "canonical 122 fresh-coordinate order")
    points = [scaled_point(old["coordinates"][str(label)]) for label in old_labels]
    points.extend(scaled_point(row["coordinates"]) for row in fresh)
    require(len(points) == len(set(points)) == 632, "632 distinct exact points")
    host_edges = [(left, right) for left, right in combinations(range(632), 2)
                  if squared_distance(points[left], points[right]) == UNIT]
    host_raw = edge_stream(host_edges)
    require(len(host_edges) == 3112 and sha256(host_raw).hexdigest() == HOST_EDGE_HASH,
            "complete exact H632 graph")

    mandatory = boundary["mandatory_vertices"]
    optional = boundary["optional_vertices"]
    require(mandatory == sorted(set(mandatory)) and optional == sorted(set(optional)),
            "canonical M/U label streams")
    require(len(mandatory) == 492 and len(optional) == 68
            and not set(mandatory) & set(optional), "M492/U68 partition")
    seed = set(mandatory) | set(optional)
    require(len(seed) == 560, "560 seed vertices")
    seed_edges = [(left, right) for left, right in host_edges
                  if left in seed and right in seed]
    seed_raw = edge_stream(seed_edges)
    require(len(seed_edges) == 2758 and sha256(seed_raw).hexdigest() == SEED_EDGE_HASH,
            "exact accepted H560 graph")
    return {
        "points": points,
        "host_edges": host_edges,
        "host_edge_stream": stream_record(host_raw),
        "seed": seed,
        "seed_edges": seed_edges,
        "seed_edge_stream": stream_record(seed_raw),
        "mandatory": mandatory,
        "optional": optional,
    }


def canonical(text: str, mandatory: list[int]) -> str:
    names = {}
    answer = ["."] * 632
    for vertex in mandatory:
        colour = text[vertex]
        require(colour in "0123", "mandatory colour alphabet")
        if colour not in names:
            names[colour] = str(len(names))
        answer[vertex] = names[colour]
    require(len(names) == 4, "all four colours occur on M")
    return "".join(answer)


def component_closure(vertices: set[int], adjacency: dict[int, set[int]]):
    remaining = set(vertices)
    components = []
    while remaining:
        component = {min(remaining)}
        while True:
            reached = set().union(*(adjacency[vertex] for vertex in component)) & remaining
            enlarged = component | reached
            if enlarged == component:
                break
            component = enlarged
        remaining -= component
        components.append(sorted(component))
    return components


def switched(fixed: str, components: list[list[int]], mask: int,
             first: str, second: str) -> str:
    text = list(fixed)
    for index, component in enumerate(components):
        if mask & (1 << index):
            for vertex in component:
                text[vertex] = second if fixed[vertex] == first else first
    return "".join(text)


def generate_templates(fixed: str, geometry) -> dict[str, object]:
    mandatory = geometry["mandatory"]
    mandatory_set = set(mandatory)
    mandatory_edges = [(left, right) for left, right in geometry["seed_edges"]
                       if left in mandatory_set and right in mandatory_set]
    require(len(mandatory_edges) == 2390, "mandatory edge count")
    require(all(fixed[left] != fixed[right] for left, right in mandatory_edges),
            "base mandatory colouring is proper")
    adjacency = {vertex: set() for vertex in mandatory}
    for left, right in mandatory_edges:
        adjacency[left].add(right)
        adjacency[right].add(left)

    family = set()
    full_slots = 0
    quotient_slots = 0
    complement_checks = 0
    component_stats = []
    for first, second in combinations("0123", 2):
        vertices = {vertex for vertex in mandatory
                    if fixed[vertex] in (first, second)}
        components = component_closure(vertices, adjacency)
        require(sum(map(len, components)) == len(vertices), "component partition")
        canonical_by_mask = {}
        all_mask = (1 << len(components)) - 1
        for mask in range(1 << len(components)):
            normalized = canonical(switched(fixed, components, mask, first, second),
                                   mandatory)
            canonical_by_mask[mask] = normalized
            family.add(normalized)
            full_slots += 1
        for mask, normalized in canonical_by_mask.items():
            require(normalized == canonical_by_mask[mask ^ all_mask],
                    "component complement is global transposition")
            complement_checks += 1
        quotient_slots += 1 << (len(components) - 1)
        component_stats.append({
            "pair": [int(first), int(second)],
            "component_sizes": list(map(len, components)),
            "components": components,
        })
    require([len(row["components"]) for row in component_stats] == [7, 6, 4, 5, 1, 2],
            "six exact component counts")
    require(full_slots == complement_checks == 246 and quotient_slots == 123,
            "full and complement-quotient slot counts")
    family = sorted(family)
    require(len(family) == 118, "118 normalized distinct templates")
    edge_checks = 0
    for text in family:
        for left, right in mandatory_edges:
            require(text[left] != text[right], "generated template is proper on M")
            edge_checks += 1
    require(edge_checks == 282020, "every template/mandatory-edge pair")

    palette_checks = 0
    for text in family:
        for permutation in permutations("0123"):
            mapping = dict(zip("0123", permutation))
            renamed = "".join(mapping.get(colour, colour) for colour in text)
            require(canonical(renamed, mandatory) == text,
                    "canonicalization removes global palette names")
            palette_checks += 1
    require(palette_checks == 118 * 24, "all template palette controls")
    raw = "".join(text + "\n" for text in family).encode("ascii")
    require(sha256(raw).hexdigest() == EXPECTED_TEMPLATE_HASH,
            "canonical template stream")
    return {
        "family": family,
        "mandatory_edges": mandatory_edges,
        "component_stats": [{"pair": row["pair"],
                             "component_sizes": row["component_sizes"]}
                            for row in component_stats],
        "full_slots": full_slots,
        "quotient_slots": quotient_slots,
        "complement_checks": complement_checks,
        "palette_checks": palette_checks,
        "mandatory_edge_checks": edge_checks,
        "stream": stream_record(raw),
    }


def derive_lists(geometry, templates):
    mandatory_set = set(geometry["mandatory"])
    optional_set = set(geometry["optional"])
    mandatory_neighbours = {vertex: set() for vertex in geometry["optional"]}
    optional_edges = []
    for left, right in geometry["seed_edges"]:
        if left in optional_set and right in optional_set:
            optional_edges.append((left, right))
        elif (left in optional_set) != (right in optional_set):
            optional_vertex = left if left in optional_set else right
            mandatory_vertex = right if left in optional_set else left
            require(mandatory_vertex in mandatory_set, "M/U edge partition")
            mandatory_neighbours[optional_vertex].add(mandatory_vertex)
    require(len(optional_edges) == 61, "optional edge count")
    family_lists = []
    rows = []
    for index, text in enumerate(templates["family"]):
        lists = {}
        for vertex in geometry["optional"]:
            forbidden = {int(text[neighbour])
                         for neighbour in mandatory_neighbours[vertex]}
            lists[vertex] = tuple(sorted(set(range(4)) - forbidden))
            rows.append(f"{index},{vertex}:{','.join(map(str, lists[vertex]))}\n")
        family_lists.append(lists)
    return {
        "mandatory_neighbours": mandatory_neighbours,
        "optional_edges": optional_edges,
        "family_lists": family_lists,
        "list_stream": stream_record("".join(rows).encode("ascii")),
    }


def proper_assignments(row: list[int], lists: dict[int, tuple[int, ...]],
                       optional_edge_set: set[tuple[int, int]]):
    examined = 0
    proper = 0
    internal = [(left, right) for left, right in combinations(row, 2)
                if (left, right) in optional_edge_set]
    for values in product(*(lists[vertex] for vertex in row)):
        examined += 1
        colour = dict(zip(row, values))
        if all(colour[left] != colour[right] for left, right in internal):
            proper += 1
    return examined, proper


def verify_negative_boundary(rows, geometry, interface):
    optional_set = set(geometry["optional"])
    require(rows and all(row == sorted(set(row)) and set(row) <= optional_set
                         for row in rows), "canonical nonempty obstruction rows")
    forbidden = [frozenset(row) for row in rows]
    require(len(set(forbidden)) == len(forbidden)
            and not any(left < right for left in forbidden for right in forbidden),
            "minimal obstruction antichain")
    require(list(map(len, rows)) == [3, 3, 3, 3, 4, 4, 4, 4, 4],
            "obstruction sizes")
    optional_edge_set = set(interface["optional_edges"])
    cases = 0
    assignments = 0
    for row in rows:
        require(len(row) <= 4, "small direct negative boundary")
        for lists in interface["family_lists"]:
            examined, proper = proper_assignments(row, lists, optional_edge_set)
            assignments += examined
            cases += 1
            require(proper == 0, "claimed obstruction extends a Kempe template")
    require(cases == 118 * 9 == 1062 and assignments == 822,
            "complete negative boundary counts")
    return forbidden, cases, assignments


def validate_cover(text: str, omitted_optional: list[int], geometry, templates,
                   interface):
    mandatory = geometry["mandatory"]
    optional = geometry["optional"]
    omitted = set(omitted_optional)
    require(omitted_optional == sorted(omitted) and omitted <= set(optional),
            "canonical optional omission set")
    support = set(mandatory) | (set(optional) - omitted)
    require(isinstance(text, str) and len(text) == 632, "cover string shape")
    require(all((text[vertex] in "0123") == (vertex in support)
                for vertex in range(632)), "cover exact support")
    mandatory_text = "".join(text[vertex] if vertex in set(mandatory) else "."
                             for vertex in range(632))
    require(mandatory_text in templates["family"], "cover M restriction belongs to K")
    template_index = templates["family"].index(mandatory_text)
    require(all(int(text[vertex]) in interface["family_lists"][template_index][vertex]
                for vertex in set(optional) - omitted), "cover respects template lists")
    checks = 0
    for left, right in geometry["seed_edges"]:
        if left in support and right in support:
            require(text[left] != text[right], "cover is proper on exact edge")
            checks += 1
    return {"omitted_optional": omitted_optional, "vertices": len(support),
            "edges": checks, "template_index": template_index}


def find_fresh_optional_colouring(template_index: int, omitted_optional: list[int],
                                  geometry, templates, interface):
    selected = set(geometry["optional"]) - set(omitted_optional)
    adjacency = {vertex: set() for vertex in selected}
    for left, right in interface["optional_edges"]:
        if left in selected and right in selected:
            adjacency[left].add(right)
            adjacency[right].add(left)
    lists = interface["family_lists"][template_index]
    assigned = {}
    nodes = 0

    def search():
        nonlocal nodes
        nodes += 1
        if len(assigned) == len(selected):
            return True
        choices = []
        for vertex in selected - set(assigned):
            forbidden = {assigned[neighbour] for neighbour in adjacency[vertex]
                         if neighbour in assigned}
            available = [colour for colour in reversed(lists[vertex])
                         if colour not in forbidden]
            if not available:
                return False
            unassigned_degree = sum(neighbour not in assigned
                                    for neighbour in adjacency[vertex])
            choices.append((len(available), -unassigned_degree, -vertex,
                            vertex, available))
        _, _, _, vertex, available = min(choices)
        for colour in available:
            assigned[vertex] = colour
            if search():
                return True
        assigned.pop(vertex, None)
        return False

    require(search(), "fresh optional cover colouring exists")
    text = list(templates["family"][template_index])
    for vertex, colour in assigned.items():
        text[vertex] = str(colour)
    result = "".join(text)
    validate_cover(result, omitted_optional, geometry, templates, interface)
    return result, nodes


def colouring_stream(rows: list[str]) -> bytes:
    return "".join(text + "\n" for text in rows).encode("ascii")


def endpoint_boundary(forbidden: list[frozenset[int]]):
    endpoints = sorted(set().union(*forbidden))
    require(len(endpoints) == 11, "eleven affected endpoints")
    good = []
    for mask in range(1 << len(endpoints)):
        chosen = frozenset(vertex for index, vertex in enumerate(endpoints)
                           if mask & (1 << index))
        if not any(row <= chosen for row in forbidden):
            good.append(chosen)
    maximal = [chosen for chosen in good
               if not any(chosen < other for other in good)]
    omissions = sorted((sorted(set(endpoints) - chosen) for chosen in maximal),
                       key=lambda row: (len(row), row))
    polynomial = Counter(map(len, good))
    expected_polynomial = [1, 11, 55, 161, 299, 361, 281, 135, 36, 4, 0, 0]
    require(len(good) == 1344 and len(maximal) == 10,
            "complete endpoint boundary counts")
    require([polynomial[degree] for degree in range(12)] == expected_polynomial,
            "endpoint independence polynomial")
    require(all(any(chosen <= larger for larger in maximal) for chosen in good),
            "every good endpoint pattern lies below a maximal one")
    require(all(all(any(row - {vertex} <= chosen for chosen in good)
                    for vertex in row) for row in forbidden),
            "every negative row is inclusion-minimal")
    return endpoints, good, maximal, omissions, expected_polynomial


def exact_counts(good: list[frozenset[int]]):
    polynomial = Counter(map(len, good))
    counts = [sum(number * comb(57, size - degree)
                  for degree, number in polynomial.items()
                  if 0 <= size - degree <= 57)
              for size in range(69)]
    require(sum(counts) == 1344 * 2 ** 57 == 193690812773950291968,
            "all extending subsets")
    require(counts[16] == 1409416830037074, "extending size-16 supports")
    require(comb(68, 16) - counts[16] == 60151956198234,
            "remaining size-16 supports")
    require(sum(counts[:17]) == 1997771244437937,
            "extending supports through size 16")
    return counts


def audit_certificate(certificate, geometry, templates, interface,
                      find_fresh: bool = True):
    require(certificate["quotient_slots"] == templates["quotient_slots"] == 123,
            "certificate quotient slots")
    require(certificate["distinct_templates"] == len(templates["family"]) == 118,
            "certificate template cardinality")
    require(certificate["canonical_template_stream_sha256"]
            == templates["stream"]["sha256"] == EXPECTED_TEMPLATE_HASH,
            "certificate template stream")
    rows = certificate["combined_minimal_nonextending_sets"]
    forbidden, negative_cases, negative_assignments = verify_negative_boundary(
        rows, geometry, interface)
    endpoints, good, maximal, omissions, polynomial = endpoint_boundary(forbidden)

    covers = certificate["maximal_extending_cover_colourings"]
    require(len(covers) == 10, "ten submitted positive covers")
    require(sorted((row["omitted_optional"] for row in covers),
                   key=lambda row: (len(row), row)) == omissions,
            "positive covers equal maximal endpoint boundary")
    target_rows = []
    target_stats = []
    fresh_rows = []
    fresh_nodes = []
    for row in covers:
        statistic = validate_cover(row["colouring"], row["omitted_optional"],
                                   geometry, templates, interface)
        target_stats.append(statistic)
        target_rows.append(row["colouring"])
        if find_fresh:
            fresh, nodes = find_fresh_optional_colouring(
                statistic["template_index"], row["omitted_optional"], geometry,
                templates, interface)
            fresh_rows.append(fresh)
            fresh_nodes.append(nodes)
    require(sum(row["edges"] for row in target_stats) == 27346,
            "all submitted cover edge checks")
    require(len({row["template_index"] for row in target_stats}) == 4,
            "four templates suffice for positive boundary")

    counts = exact_counts(good)
    require(certificate["extending_counts_by_optional_size"] == counts,
            "all 69 cardinality coefficients")
    target_record = stream_record(colouring_stream(target_rows))
    answer = {
        "negative_template_cases": negative_cases,
        "negative_assignments": negative_assignments,
        "obstructions": rows,
        "endpoints": endpoints,
        "endpoint_patterns": 1 << len(endpoints),
        "good_endpoint_patterns": len(good),
        "endpoint_polynomial": polynomial,
        "minimal_hitting_sets": omissions,
        "target_cover_stats": target_stats,
        "target_cover_edge_checks": sum(row["edges"] for row in target_stats),
        "target_colouring_stream": target_record,
        "counts": counts,
    }
    if find_fresh:
        fresh_stats = [validate_cover(text, covers[index]["omitted_optional"],
                                      geometry, templates, interface)
                       for index, text in enumerate(fresh_rows)]
        require(sum(row["edges"] for row in fresh_stats) == 27346,
                "all fresh cover edge checks")
        fresh_record = stream_record(colouring_stream(fresh_rows))
        require(fresh_record["sha256"] != target_record["sha256"],
                "fresh covers differ from submitted rows")
        answer.update({
            "fresh_cover_stats": fresh_stats,
            "fresh_cover_edge_checks": sum(row["edges"] for row in fresh_stats),
            "fresh_search_nodes": fresh_nodes,
            "fresh_colouring_stream": fresh_record,
        })
    return answer


def expect_failure(callback, message: str) -> None:
    try:
        callback()
    except ReviewFailure:
        return
    raise ReviewFailure(message)


def negative_controls(certificate, geometry, templates, interface):
    labels = []
    bad = copy.deepcopy(certificate)
    bad["maximal_extending_cover_colourings"].pop()
    expect_failure(lambda: audit_certificate(bad, geometry, templates, interface, False),
                   "missing cover accepted")
    labels.append("missing_cover")

    bad = copy.deepcopy(certificate)
    bad["combined_minimal_nonextending_sets"][0] = [362, 604]
    expect_failure(lambda: audit_certificate(bad, geometry, templates, interface, False),
                   "false fixed-colouring pair accepted as Kempe obstruction")
    labels.append("false_negative_pair")

    bad = copy.deepcopy(certificate)
    bad["combined_minimal_nonextending_sets"].pop()
    expect_failure(lambda: audit_certificate(bad, geometry, templates, interface, False),
                   "missing obstruction accepted")
    labels.append("missing_obstruction")

    bad = copy.deepcopy(certificate)
    row = bad["maximal_extending_cover_colourings"][0]
    text = list(row["colouring"])
    text[geometry["mandatory"][0]] = str((int(text[geometry["mandatory"][0]]) + 1) % 4)
    row["colouring"] = "".join(text)
    expect_failure(lambda: audit_certificate(bad, geometry, templates, interface, False),
                   "invalid mandatory template accepted")
    labels.append("invalid_mandatory_template")

    bad = copy.deepcopy(certificate)
    row = bad["maximal_extending_cover_colourings"][0]
    missing = row["omitted_optional"][0]
    text = list(row["colouring"])
    text[missing] = "0"
    row["colouring"] = "".join(text)
    expect_failure(lambda: audit_certificate(bad, geometry, templates, interface, False),
                   "wrong cover support accepted")
    labels.append("wrong_cover_support")

    bad = copy.deepcopy(certificate)
    row = bad["maximal_extending_cover_colourings"][0]
    omitted = set(row["omitted_optional"])
    text = list(row["colouring"])
    template_text = "".join(text[vertex] if vertex in set(geometry["mandatory"]) else "."
                            for vertex in range(632))
    index = templates["family"].index(template_text)
    lists = interface["family_lists"][index]
    left, right = next((left, right) for left, right in interface["optional_edges"]
                       if left not in omitted and right not in omitted
                       and set(lists[left]) & set(lists[right]))
    common = min(set(lists[left]) & set(lists[right]))
    text[left] = text[right] = str(common)
    row["colouring"] = "".join(text)
    expect_failure(lambda: audit_certificate(bad, geometry, templates, interface, False),
                   "monochromatic optional edge accepted")
    labels.append("monochromatic_cover_edge")

    bad = copy.deepcopy(certificate)
    bad["canonical_template_stream_sha256"] = "0" * 64
    expect_failure(lambda: audit_certificate(bad, geometry, templates, interface, False),
                   "false template hash accepted")
    labels.append("false_template_hash")

    bad = copy.deepcopy(certificate)
    bad["extending_counts_by_optional_size"][16] += 1
    expect_failure(lambda: audit_certificate(bad, geometry, templates, interface, False),
                   "false count accepted")
    labels.append("false_count")
    return labels


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--work", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    repository = args.repository.resolve()
    work = args.work.resolve()
    work.mkdir(parents=True, exist_ok=False)

    source = verify_sources(repository)
    basis_checks = multiplication_controls()
    boundary = json.loads((repository / BOUNDARY_INPUT).read_text(encoding="utf-8"))
    geometry = reconstruct_geometry(repository, boundary)
    old = json.loads((repository / COLOUR_INPUT).read_text(encoding="utf-8"))
    fixed = old["cover_colouring"]
    templates = generate_templates(fixed, geometry)
    interface = derive_lists(geometry, templates)
    certificate_path = repository / TARGET_DIRECTORY / "certificate.json"
    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
    classification = audit_certificate(certificate, geometry, templates, interface)
    controls = negative_controls(certificate, geometry, templates, interface)
    counts = classification.pop("counts")
    optional_raw = edge_stream(interface["optional_edges"])

    result = {
        "all_checks_passed": True,
        "accepted_claim": ("the complete normalized one-original-pair Kempe family "
                           "has 118 templates, and one extends to G[M union T] exactly "
                           "when T avoids the nine stated minimal obstructions"),
        "reviewed_source_commit": TARGET_COMMIT,
        "source_identity": source,
        "exact_geometry": {
            "basis_product_controls": basis_checks,
            "host_vertices": 632,
            "distinct_points": len(set(geometry["points"])),
            "unordered_pairs_checked": comb(632, 2),
            "host_edges": len(geometry["host_edges"]),
            "host_edge_stream": geometry["host_edge_stream"],
            "seed_vertices": len(geometry["seed"]),
            "seed_edges": len(geometry["seed_edges"]),
            "seed_edge_stream": geometry["seed_edge_stream"],
            "optional_edges": len(interface["optional_edges"]),
            "optional_edge_stream": stream_record(optional_raw),
        },
        "kempe_family": {
            "component_stats": templates["component_stats"],
            "full_switch_slots": templates["full_slots"],
            "component_complement_checks": templates["complement_checks"],
            "quotient_slots": templates["quotient_slots"],
            "distinct_normalized_templates": len(templates["family"]),
            "palette_normalization_controls": templates["palette_checks"],
            "mandatory_template_edge_checks": templates["mandatory_edge_checks"],
            "template_stream": templates["stream"],
            "all_template_list_stream": interface["list_stream"],
        },
        "classification": classification,
        "family_counts": {
            "all_extending_subsets": sum(counts),
            "all_optional_subsets": 2 ** 68,
            "extending_size_16": counts[16],
            "all_size_16": comb(68, 16),
            "remaining_size_16": comb(68, 16) - counts[16],
            "extending_at_most_16": sum(counts[:17]),
            "remaining_at_most_16": sum(comb(68, size) - counts[size]
                                                for size in range(17)),
            "coefficient_stream": stream_record(
                "".join(f"{size},{value}\n" for size, value in enumerate(counts)).encode("ascii")),
        },
        "negative_controls": controls,
        "dependency_and_context": {
            "accepted_parent": "bafkreigrsanib6kfhqwhxdkjpjym6fa7xxyhcrw2phtv6m7or6vludas4i",
            "parent_acceptance": "bafkreicgezlcgpdcdp673itijhhjeh3qdr2bwusmtma2fryh62today2ue",
            "comparison_fixed_interface": "bafkreigujn4nyowcty4pfk3qbswlz3xe7lsdw73jesn5czswkxjsuug2ou",
            "comparison_fixed_interface_acceptance": "bafkreidn6wqp7yrbwct22ysn65j6n2rqwbtosswpqr4u5xunxwk27m5duq",
        },
        "scope": {
            "one_original_colour_pair_components_only": True,
            "all_six_pairs_and_component_subsets": True,
            "global_palette_permutations_quotiented": True,
            "arbitrary_pair_compositions": False,
            "recomputed_components": False,
            "whole_kempe_equivalence_class": False,
            "all_mandatory_colourings": False,
            "remaining_graphs_proved_nonfourcolourable": False,
            "whole_h560_family_closed": False,
            "sub509_graph_established": False,
            "record_improvement": False,
        },
        "trust_boundary": [
            "the four SHA-256-pinned mathematical input files",
            "linear independence of the eight squarefree-radical basis elements",
            "ordinary CPython integer/Fraction arithmetic and exhaustive enumeration",
            "the combinatorial Kempe-switch, palette-quotient, and cover-restriction arguments",
            "the separately accepted H560 M492/U68 theorem for the global family corollary",
            "SHA-256 collision resistance for source and stream identities",
        ],
        "python": sys.version.split()[0],
    }
    atomic_json(args.report.resolve(), result)
    print(json.dumps({
        "all_checks_passed": True,
        "templates": len(templates["family"]),
        "negative_cases": classification["negative_template_cases"],
        "endpoint_patterns": classification["endpoint_patterns"],
        "good_endpoint_patterns": classification["good_endpoint_patterns"],
        "extending_size_16": counts[16],
        "remaining_size_16": comb(68, 16) - counts[16],
        "fresh_colouring_sha256": classification["fresh_colouring_stream"]["sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
