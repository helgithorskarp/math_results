#!/usr/bin/env python3
"""Independent exact review of the H560 fixed-colouring interface.

This checker imports no executable from the reviewed contribution or its
parents.  It reconstructs the 632-point graph with recursive quadratic-tower
arithmetic, derives the M492/U68 lists, verifies the submitted covers, finds
fresh covers, and proves the all-2^68 classification by exhaustive enumeration
of the five affected endpoints plus exact binomial convolution.
"""

from __future__ import annotations

import argparse
import copy
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from math import comb, gcd
import os
from pathlib import Path
import sys


TARGET_COMMIT = "b2ac55ad66b0c86c45b53fe8c68089f6e95ccd67"
TARGET_DIRECTORY = "hadwiger_nelson_heule560_interface"
TARGET_HASHES = {
    ".gitignore": "0175fcafc5d8328c584d3df3eeba657ad2c5ccda3956d46d15e15adb9ecdd57c",
    "README.md": "b83d53c43ee1a05f96e9f1addf60f17359d8d8766dccd7a46f110c5601377bc9",
    "build.py": "30ef4a47fde2f6063a6534e6c6dabf5888d55ca9bf84bdb42d0182b9ca9151cd",
    "certificate.json": "3df21aa84154341f7db3e10c1082e3948842b213c7211be7b2d763f1ddcd0bb7",
    "expected.json": "12b14c4bf9bf2238a6503a480d72839ff6004e2abc1fbffc4ca85345b4d0f176",
    "plan.json": "b793bbbaf02cc69a445b99f52be3ddd15e1dd9ecf3fc8af9f2ad44d156259b81",
    "validation.json": "5a2f178bd2053fd3ec062d8a7cb8d9c90be5f91b990cbefee9daa1b8863cf914",
    "verify.py": "5775719e950d393e16ca4bd75e54db72a9dd2d71f1d7f774e2ff5deb1f7cecc7",
}
TARGET_MANIFEST_HASH = "94fc020fa1bafa4f2de332f1423507548b773a781bb68edf062793970da52b0e"
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
    records = {}
    for name, expected in TARGET_HASHES.items():
        record = file_record(target / name)
        require(record["sha256"] == expected, "reviewed source identity: " + name)
        records[name] = record
    manifest_raw = (target / "SHA256SUMS").read_bytes()
    require(sha256(manifest_raw).hexdigest() == TARGET_MANIFEST_HASH,
            "reviewed manifest identity")
    manifest = {}
    for line in manifest_raw.decode("ascii").splitlines():
        digest, name = line.split(maxsplit=1)
        manifest[name] = digest
    require(manifest == TARGET_HASHES, "reviewed manifest entries")
    records["SHA256SUMS"] = {
        "bytes": len(manifest_raw), "sha256": TARGET_MANIFEST_HASH,
    }
    inputs = {}
    for name, expected in INPUT_HASHES.items():
        record = file_record(repository / name)
        require(record["sha256"] == expected, "mathematical input identity: " + name)
        inputs[name] = record
    return {"reviewed_files": records, "mathematical_inputs": inputs}


# Coefficient vectors are recursively interpreted in
# Q(sqrt(3))(sqrt(5))(sqrt(11)).  This is neither the submitted producer's
# ordered XOR convolution nor its verifier's sparse-radicand multiplication.
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


def multiplication_table_controls() -> int:
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
    require(checks == 64, "complete multiplication table controls")
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
            "canonical mandatory and optional labels")
    require(len(mandatory) == 492 and len(optional) == 68,
            "M492/U68 cardinalities")
    require(not set(mandatory) & set(optional), "disjoint M/U partition")
    seed = set(mandatory) | set(optional)
    require(len(seed) == 560, "560-vertex seed support")
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
        "old_labels": old_labels,
        "fresh_ids": fresh_ids,
    }


def derive_interface(fixed: str, geometry: dict[str, object]):
    mandatory = geometry["mandatory"]
    optional = geometry["optional"]
    seed_edges = geometry["seed_edges"]
    require(isinstance(fixed, str) and len(fixed) == 632, "fixed colouring shape")
    require(all(fixed[vertex] in "0123" for vertex in mandatory),
            "fixed colour on every mandatory vertex")
    mandatory_set = set(mandatory)
    optional_set = set(optional)
    mandatory_edges = []
    optional_edges = []
    mandatory_neighbours = {vertex: set() for vertex in optional}
    for left, right in seed_edges:
        if left in mandatory_set and right in mandatory_set:
            require(fixed[left] != fixed[right], "fixed M colouring is proper")
            mandatory_edges.append((left, right))
        elif left in optional_set and right in optional_set:
            optional_edges.append((left, right))
        else:
            optional_vertex = left if left in optional_set else right
            mandatory_vertex = right if left in optional_set else left
            require(optional_vertex in optional_set and mandatory_vertex in mandatory_set,
                    "M/U edge partition")
            mandatory_neighbours[optional_vertex].add(mandatory_vertex)
    lists = {}
    for vertex in optional:
        forbidden = {int(fixed[neighbour])
                     for neighbour in mandatory_neighbours[vertex]}
        lists[vertex] = tuple(sorted(set(range(4)) - forbidden))
        require(lists[vertex], "nonempty optional list")
    require(len(mandatory_edges) == 2390, "mandatory edge count")
    require(len(optional_edges) == 61, "optional edge count")
    require(Counter(map(len, lists.values())) == Counter({1: 49, 2: 17, 3: 2}),
            "optional list-size histogram")
    return {
        "fixed": fixed,
        "lists": lists,
        "mandatory_edges": mandatory_edges,
        "optional_edges": optional_edges,
        "mandatory_neighbours": mandatory_neighbours,
    }


def validate_cover(text: str, omitted_optional: list[int], geometry, interface):
    mandatory = geometry["mandatory"]
    optional = geometry["optional"]
    omitted = set(omitted_optional)
    require(omitted_optional == sorted(omitted) and omitted <= set(optional),
            "canonical optional omission set")
    support = set(mandatory) | (set(optional) - omitted)
    require(isinstance(text, str) and len(text) == 632, "cover string shape")
    require(all((text[vertex] in "0123") == (vertex in support)
                for vertex in range(632)), "cover exact support")
    require(all(text[vertex] == interface["fixed"][vertex] for vertex in mandatory),
            "cover agrees with fixed M colouring")
    require(all(int(text[vertex]) in interface["lists"][vertex]
                for vertex in set(optional) - omitted), "cover respects lists")
    checks = 0
    for left, right in geometry["seed_edges"]:
        if left in support and right in support:
            require(text[left] != text[right], "cover is proper on exact edge")
            checks += 1
    return {"vertices": len(support), "edges": checks,
            "omitted_optional": omitted_optional}


def find_fresh_cover(omitted_optional: list[int], geometry, interface):
    selected = set(geometry["optional"]) - set(omitted_optional)
    adjacency = {vertex: set() for vertex in selected}
    for left, right in interface["optional_edges"]:
        if left in selected and right in selected:
            adjacency[left].add(right)
            adjacency[right].add(left)
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
            available = [colour for colour in reversed(interface["lists"][vertex])
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

    require(search(), "fresh cover colouring exists")
    text = ["."] * 632
    for vertex in geometry["mandatory"]:
        text[vertex] = interface["fixed"][vertex]
    for vertex, colour in assigned.items():
        text[vertex] = str(colour)
    result = "".join(text)
    validate_cover(result, omitted_optional, geometry, interface)
    return result, nodes


def colouring_stream(rows: list[str]) -> bytes:
    return "".join(row + "\n" for row in rows).encode("ascii")


def forced_pair_classification(interface):
    pairs = []
    for left, right in interface["optional_edges"]:
        left_list = interface["lists"][left]
        right_list = interface["lists"][right]
        if len(left_list) == len(right_list) == 1 and left_list == right_list:
            pairs.append((left, right))
    require(pairs == [(362, 604), (406, 613), (409, 613)],
            "exact forced singleton-edge pairs")
    endpoints = sorted({vertex for pair in pairs for vertex in pair})
    require(len(endpoints) == 5, "five affected endpoints")
    good = []
    for mask in range(1 << len(endpoints)):
        chosen = frozenset(vertex for index, vertex in enumerate(endpoints)
                           if mask & (1 << index))
        if not any(set(pair) <= chosen for pair in pairs):
            good.append(chosen)
    maximal = [chosen for chosen in good
               if not any(chosen < other for other in good)]
    omissions = sorted((sorted(set(endpoints) - chosen) for chosen in maximal),
                       key=lambda row: (len(row), row))
    require(len(good) == 15 and len(maximal) == 4, "endpoint pattern classification")
    require(Counter(map(len, good)) == Counter({0: 1, 1: 5, 2: 7, 3: 2}),
            "endpoint independence polynomial")
    require(omissions == [[362, 613], [604, 613],
                          [362, 406, 409], [406, 409, 604]],
            "four minimal hitting sets")
    return pairs, endpoints, good, maximal, omissions


def exact_counts(good: list[frozenset[int]]):
    free_vertices = 63
    counts = [sum(comb(free_vertices, size - len(chosen))
                  for chosen in good if 0 <= size - len(chosen) <= free_vertices)
              for size in range(69)]
    require(sum(counts) == 15 * 2 ** 63, "all extending subsets")
    require(counts[16] == 1259701602040917, "extending size-16 supports")
    require(comb(68, 16) - counts[16] == 209867184194391,
            "remaining size-16 supports")
    require(sum(counts[:17]) == 1793849422050660,
            "extending supports through size 16")
    return counts


def audit_certificate(certificate, geometry, interface, find_fresh: bool = True):
    lists = {str(vertex): list(interface["lists"][vertex])
             for vertex in geometry["optional"]}
    require(certificate["optional_vertices"] == geometry["optional"],
            "certificate optional labels")
    require(certificate["lists"] == lists, "certificate interface lists")
    target_optional_edges = [list(edge) for edge in interface["optional_edges"]]
    require(certificate["optional_edges"] == target_optional_edges,
            "certificate optional edges")

    pairs, endpoints, good, maximal, omissions = forced_pair_classification(interface)
    require(certificate["minimal_nonextending_sets"] == [list(pair) for pair in pairs],
            "certificate complete minimal obstructions")
    rows = certificate["maximal_extending_cover_colourings"]
    require(len(rows) == 4, "four submitted cover colourings")
    require(sorted((row["omitted_optional"] for row in rows),
                   key=lambda row: (len(row), row)) == omissions,
            "submitted covers are exactly maximal endpoint supports")
    target_rows = []
    target_stats = []
    fresh_rows = []
    fresh_nodes = []
    for row in rows:
        target_stats.append(validate_cover(row["colouring"], row["omitted_optional"],
                                           geometry, interface))
        target_rows.append(row["colouring"])
        if find_fresh:
            fresh, nodes = find_fresh_cover(row["omitted_optional"], geometry, interface)
            fresh_rows.append(fresh)
            fresh_nodes.append(nodes)
    require(sum(item["edges"] for item in target_stats) == 10958,
            "all submitted cover edge checks")

    # Each good endpoint set lies below a maximal good endpoint set.  All 63
    # unaffected optional vertices occur in every cover, so restriction proves
    # extension for every subset of U avoiding the three pairs.
    require(all(any(chosen <= larger for larger in maximal) for chosen in good),
            "all good endpoint patterns covered")
    counts = exact_counts(good)
    require(certificate["extending_counts_by_optional_size"] == counts,
            "all 69 exact cardinality counts")

    result = {
        "forced_pairs": [list(pair) for pair in pairs],
        "affected_endpoints": endpoints,
        "endpoint_patterns": 32,
        "extending_endpoint_patterns": len(good),
        "endpoint_size_histogram": {
            str(size): count for size, count in sorted(Counter(map(len, good)).items())},
        "minimal_hitting_sets": omissions,
        "target_cover_stats": target_stats,
        "target_cover_edge_checks": sum(item["edges"] for item in target_stats),
        "target_colouring_stream": stream_record(colouring_stream(target_rows)),
        "counts": counts,
    }
    if find_fresh:
        require(len(fresh_rows) == 4, "four fresh covers")
        fresh_stats = [validate_cover(text, rows[index]["omitted_optional"],
                                      geometry, interface)
                       for index, text in enumerate(fresh_rows)]
        require(sum(item["edges"] for item in fresh_stats) == 10958,
                "all fresh cover edge checks")
        target_record = result["target_colouring_stream"]
        fresh_record = stream_record(colouring_stream(fresh_rows))
        require(target_record["sha256"] != fresh_record["sha256"],
                "fresh covers differ from submitted witnesses")
        result.update({
            "fresh_cover_stats": fresh_stats,
            "fresh_cover_edge_checks": sum(item["edges"] for item in fresh_stats),
            "fresh_search_nodes": fresh_nodes,
            "fresh_colouring_stream": fresh_record,
        })
    return result


def expect_failure(callback, message: str) -> None:
    try:
        callback()
    except ReviewFailure:
        return
    raise ReviewFailure(message)


def negative_controls(certificate, geometry, interface):
    labels = []
    bad = copy.deepcopy(certificate)
    del bad["lists"]["604"]
    expect_failure(lambda: audit_certificate(bad, geometry, interface, False),
                   "missing list accepted")
    labels.append("missing_list")

    bad = copy.deepcopy(certificate)
    bad["minimal_nonextending_sets"].pop()
    expect_failure(lambda: audit_certificate(bad, geometry, interface, False),
                   "missing obstruction accepted")
    labels.append("missing_obstruction")

    bad = copy.deepcopy(certificate)
    bad["maximal_extending_cover_colourings"].pop()
    expect_failure(lambda: audit_certificate(bad, geometry, interface, False),
                   "missing cover accepted")
    labels.append("missing_cover")

    bad = copy.deepcopy(certificate)
    first = bad["maximal_extending_cover_colourings"][0]
    text = list(first["colouring"])
    omitted = set(first["omitted_optional"])
    edge = next((left, right) for left, right in interface["optional_edges"]
                if left not in omitted and right not in omitted
                and set(interface["lists"][left]) & set(interface["lists"][right]))
    common = min(set(interface["lists"][edge[0]]) & set(interface["lists"][edge[1]]))
    text[edge[0]] = text[edge[1]] = str(common)
    first["colouring"] = "".join(text)
    expect_failure(lambda: audit_certificate(bad, geometry, interface, False),
                   "monochromatic optional edge accepted")
    labels.append("monochromatic_cover_edge")

    bad = copy.deepcopy(certificate)
    first = bad["maximal_extending_cover_colourings"][0]
    missing = first["omitted_optional"][0]
    text = list(first["colouring"])
    text[missing] = str(interface["lists"][missing][0])
    first["colouring"] = "".join(text)
    expect_failure(lambda: audit_certificate(bad, geometry, interface, False),
                   "wrong cover support accepted")
    labels.append("wrong_cover_support")

    bad = copy.deepcopy(certificate)
    bad["extending_counts_by_optional_size"][16] += 1
    expect_failure(lambda: audit_certificate(bad, geometry, interface, False),
                   "false cardinality count accepted")
    labels.append("false_count")

    bad_fixed = list(interface["fixed"])
    left, right = interface["mandatory_edges"][0]
    bad_fixed[right] = bad_fixed[left]
    expect_failure(lambda: derive_interface("".join(bad_fixed), geometry),
                   "monochromatic fixed-M edge accepted")
    labels.append("monochromatic_fixed_edge")
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
    basis_checks = multiplication_table_controls()
    boundary = json.loads((repository / BOUNDARY_INPUT).read_text(encoding="utf-8"))
    geometry = reconstruct_geometry(repository, boundary)
    old = json.loads((repository / COLOUR_INPUT).read_text(encoding="utf-8"))
    fixed = old["cover_colouring"]
    interface = derive_interface(fixed, geometry)
    certificate_path = repository / TARGET_DIRECTORY / "certificate.json"
    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
    classification = audit_certificate(certificate, geometry, interface)
    controls = negative_controls(certificate, geometry, interface)
    counts = classification.pop("counts")
    optional_raw = edge_stream(interface["optional_edges"])
    list_raw = "".join(f"{vertex}:{','.join(map(str, interface['lists'][vertex]))}\n"
                       for vertex in geometry["optional"]).encode("ascii")

    result = {
        "all_checks_passed": True,
        "accepted_claim": ("for the specified fixed colouring c of M492, extension to "
                           "G[M union T] holds exactly when T avoids the three stated "
                           "pairs, with the claimed counts and inherited family corollary"),
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
        },
        "fixed_interface": {
            "mandatory_vertices": len(geometry["mandatory"]),
            "optional_vertices": len(geometry["optional"]),
            "mandatory_edge_checks": len(interface["mandatory_edges"]),
            "optional_edges": len(interface["optional_edges"]),
            "optional_edge_stream": stream_record(optional_raw),
            "list_size_histogram": {
                str(size): count for size, count
                in sorted(Counter(map(len, interface["lists"].values())).items())},
            "list_stream": stream_record(list_raw),
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
        "dependency": {
            "accepted_parent": "bafkreigrsanib6kfhqwhxdkjpjym6fa7xxyhcrw2phtv6m7or6vludas4i",
            "parent_independent_acceptance": "bafkreicgezlcgpdcdp673itijhhjeh3qdr2bwusmtma2fryh62today2ue",
            "fixed_colour_source": "bafkreihwchy7p2lgnrpyqdxblehcz7tmwas2tlllsib6jb6tdwm2xmlkmi",
        },
        "scope": {
            "fixed_mandatory_colouring_classified": True,
            "all_optional_subsets_covered": True,
            "arbitrary_recolouring_of_m_classified": False,
            "remaining_graphs_proved_nonfourcolourable": False,
            "whole_h560_family_closed": False,
            "sub509_graph_established": False,
            "record_improvement": False,
        },
        "trust_boundary": [
            "the four SHA-256-pinned mathematical input files",
            "linear independence of the eight squarefree-radical basis elements",
            "ordinary CPython integer/Fraction arithmetic and exhaustive enumeration",
            "the elementary restriction argument from four maximal positive covers",
            "the separately accepted H560 M492/U68 parent theorem for the global family corollary",
            "SHA-256 collision resistance for source and canonical stream identities",
        ],
        "python": sys.version.split()[0],
    }
    atomic_json(args.report.resolve(), result)
    print(json.dumps({
        "all_checks_passed": True,
        "host_edges": len(geometry["host_edges"]),
        "seed_edges": len(geometry["seed_edges"]),
        "forced_pairs": classification["forced_pairs"],
        "extending_size_16": counts[16],
        "remaining_size_16": comb(68, 16) - counts[16],
        "fresh_colouring_sha256": classification["fresh_colouring_stream"]["sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
