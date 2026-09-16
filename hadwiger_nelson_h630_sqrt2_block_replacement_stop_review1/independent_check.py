#!/usr/bin/env python3
"""Independent exact review of the 508-point H630 block replacement.

No target executable is imported.  Coordinates are reconstructed from the
three pinned archives and evaluated in recursive quadratic-field towers,
rather than either of the target's bitmask and sparse-radicand arithmetic
implementations.
"""

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "hadwiger_nelson_h630_sqrt2_block_replacement_stop"
SOURCE_REVIEW = ROOT / "hadwiger_nelson_heule630_seed_review1"
OLD_INPUT = ROOT / "hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json"
FRESH_INPUT = ROOT / "hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json"
SOURCE_CERT = ROOT / "hadwiger_nelson_heule632_pair_pilot/certificate.json"
REVIEWED_TARGET_COMMIT = "53b90e407c24fdd029346f8c9f2de72a51b0d062"
DENOMINATOR = 96
OLD_PRIMES = (3, 5, 11)
NEW_PRIMES = (2, 3, 11)
UNIT = (DENOMINATOR * DENOMINATOR,) + (0,) * 7

PINNED = {
    TARGET / "README.md": "39510534e0a4d7ad9e9e425768b42a7df355466264d08c927ace43a12522bed5",
    TARGET / "ARCHITECTURE.json": "562d448d2129c2c30ad31648ba9d8fff5a66397d4bc9ee58f61649b2ca3dd21f",
    TARGET / "PROVENANCE.json": "c8118607460d86caef387ca502fd559e4703f32f7a540f2c7a2f79f37d711ef3",
    TARGET / "VERIFY.json": "59e531031ab5cedd4ff539328573ef27680b9342c2251fc088a6786ee82c5338",
    TARGET / "certificate.json": "808305a7886defe529236badf3bdcbde73a037b6c87d29836e095e9731878293",
    TARGET / "points.csv": "0e665d7cf9767d2c0068429e138a686bfdcc8bbc51f310ef27a03763188ac4ee",
    TARGET / "edges.csv": "b5f75973a1319a52ba22dcf1ee256ea075065095637268d0521bb112aafb7fb0",
    TARGET / "h632.csv": "5bc6df88afed13c6ccff2154c749fc1f5e74a9892b6b13f79ab08bbc49cd2e17",
    TARGET / "reproduce.py": "f8c4456003a88fb8e27637ae56a07c4089ceafe05d002babd007c8f62af5c70e",
    TARGET / "verify.py": "7b15cd98f99a02f2f9224404a3a2368fedefe17eea403801576009e9fcea2e12",
    OLD_INPUT: "bc8e0f5f5ec7fa5f2376cc77ba0e65f6023b340cf48990370d5eda575d30ae79",
    FRESH_INPUT: "89345930e1bea184ce2457b0e14a015bcd9a2901cfc609a6468cf050234a8317",
    SOURCE_CERT: "fffa224298854425f7c40726a9dd96196b1c5e82b75ffa4d8c6c19fefbc8274f",
    SOURCE_REVIEW / "README.md": "14fa8f8dcce9d1cc2d8d9e0b9eaceb5add3f39b030816ecbfca70dee5a29febc",
    SOURCE_REVIEW / "result.json": "0842824cf98202fc5bad22263e81c14c21a02a7345d04f50f0c04384b246126c",
}


class ReviewFailure(RuntimeError):
    pass


def need(condition, message):
    if not condition:
        raise ReviewFailure(message)


def sha256(blob):
    return hashlib.sha256(blob).hexdigest()


def check_pins():
    for path, expected in PINNED.items():
        need(path.is_file(), f"missing pinned file: {path.relative_to(ROOT)}")
        need(sha256(path.read_bytes()) == expected,
             f"hash mismatch: {path.relative_to(ROOT)}")
    return len(PINNED)


def add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def scale(vector, scalar):
    return tuple(scalar * value for value in vector)


def tower_product(left, right, primes):
    """Multiply in a recursive tower Q(sqrt(p1),...,sqrt(pk))."""
    need(len(left) == len(right) == 1 << len(primes), "tower dimensions")
    if not primes:
        return (left[0] * right[0],)
    half = len(left) // 2
    a, b = left[:half], left[half:]
    c, d = right[:half], right[half:]
    lower_primes = primes[:-1]
    ac = tower_product(a, c, lower_primes)
    bd = tower_product(b, d, lower_primes)
    ad = tower_product(a, d, lower_primes)
    bc = tower_product(b, c, lower_primes)
    return add(ac, scale(bd, primes[-1])) + add(ad, bc)


def tower_square(vector, primes):
    need(len(vector) == 1 << len(primes), "tower square dimensions")
    if not primes:
        return (vector[0] * vector[0],)
    half = len(vector) // 2
    a, b = vector[:half], vector[half:]
    lower_primes = primes[:-1]
    aa = tower_square(a, lower_primes)
    bb = tower_square(b, lower_primes)
    ab = tower_product(a, b, lower_primes)
    return add(aa, scale(bb, primes[-1])) + scale(ab, 2)


def squared_distance(left, right, primes):
    total = (0,) * 8
    for offset in (0, 8):
        delta = tuple(left[offset + index] - right[offset + index]
                      for index in range(8))
        total = add(total, tower_square(delta, primes))
    return total


def complete_edges(points, primes):
    return [
        (left, right)
        for left, right in combinations(range(len(points)), 2)
        if squared_distance(points[left], points[right], primes) == UNIT
    ]


def point_bytes(points):
    return "".join(",".join(map(str, point)) + "\n" for point in points).encode("ascii")


def edge_bytes(edges):
    return "".join(f"{left},{right}\n" for left, right in edges).encode("ascii")


def scaled_point(row):
    need(isinstance(row, list) and len(row) == 2 and
         all(isinstance(axis, list) and len(axis) == 8 for axis in row),
         "source coordinate shape")
    values = []
    for axis in row:
        for token in axis:
            value = DENOMINATOR * Fraction(token)
            need(value.denominator == 1, "source denominator")
            values.append(value.numerator)
    return tuple(values)


def parse_point_csv(blob):
    rows = [tuple(map(int, line.split(","))) for line in blob.decode("ascii").splitlines()]
    need(all(len(row) == 16 for row in rows), "CSV point dimensions")
    return rows


def reconstruct_source():
    old = json.loads(OLD_INPUT.read_text())
    fresh = json.loads(FRESH_INPUT.read_text())
    source_certificate = json.loads(SOURCE_CERT.read_text())
    old_labels = [index for index, provenance in enumerate(old["provenance"])
                  if "510" in provenance]
    need(len(old_labels) == 510 and old_labels == sorted(set(old_labels)),
         "archived 510-point selection")
    need([old_labels[index] for index in (399, 462)] == [436, 505],
         "omitted source-label mapping")
    fresh_ids = [row["centre_index"] for row in fresh]
    need(len(fresh_ids) == 122 and fresh_ids == sorted(set(fresh_ids)),
         "fresh-centre ordering")
    points = [scaled_point(old["coordinates"][str(label)]) for label in old_labels]
    points.extend(scaled_point(row["coordinates"]) for row in fresh)
    need(len(points) == len(set(points)) == 632, "H632 point census")
    archive = (TARGET / "h632.csv").read_bytes()
    need(point_bytes(points) == archive, "entry-level H632 archive reconstruction")

    edges = complete_edges(points, OLD_PRIMES)
    need(len(edges) == 3112, "complete H632 edge census")
    host_edge_hash = sha256(edge_bytes(edges))
    need(host_edge_hash == "8dd36c195b3e252ec2be150ea6a029375707293fec70b63da9fc157eed4140f0",
         "H632 edge identity")
    omitted = {399, 462}
    seed_edges = [edge for edge in edges if not omitted.intersection(edge)]
    need(len(seed_edges) == 3098, "H630 edge census")
    seed_edge_hash = sha256(edge_bytes(seed_edges))
    need(seed_edge_hash == "14dfca558a986c73226f39e1cfcf10081d2c77d19abb087ccc31913f9bb00758",
         "H630 edge identity")
    degree = Counter(vertex for edge in edges for vertex in edge)
    need(degree[399] == degree[462] == 7 and (399, 462) not in set(edges),
         "omitted source vertices")

    five_word = source_certificate["five_colouring"]
    need(len(five_word) == 632 and
         [index for index, value in enumerate(five_word) if value == "."] == [399, 462],
         "source five-word shape")
    need(all(five_word[left] != five_word[right] for left, right in seed_edges),
         "source five-word")
    prior_review = json.loads((SOURCE_REVIEW / "result.json").read_text())
    need(prior_review["all_checks_passed"] is True and
         prior_review["geometry"]["host_edge_sha256"] == host_edge_hash and
         prior_review["geometry"]["seed_edge_sha256"] == seed_edge_hash,
         "prior independent source review alignment")
    return points, edges, seed_edges, five_word, host_edge_hash, seed_edge_hash


def convert_old(point):
    result = [0] * 16
    for offset in (0, 8):
        for old_index, new_index in ((0, 0), (1, 2), (4, 4), (5, 6)):
            result[offset + new_index] = point[offset + old_index]
    return tuple(result)


def disk_point(m, n):
    """Closed Cartesian formula at denominator 96."""
    a = m + 2 * n
    return (48 * m, 0, 0, -16 * a, 0, 0, 0, 0,
            0, 48 * m, 16 * a, 0, 0, 0, 0, 0)


def source_box(points):
    """Independent rational radical enclosure at scale 2^80."""
    radicands = (1, 3, 5, 15, 11, 33, 55, 165)
    grid = 1 << 80
    bounds = []
    for radicand in radicands:
        k = isqrt(radicand * grid * grid)
        exact = k * k == radicand * grid * grid
        bounds.append((k, k if exact else k + 1))
    global_lower = None
    global_upper = None
    for point in points:
        for axis in (point[:8], point[8:]):
            lower = sum(coefficient * bounds[index][0 if coefficient >= 0 else 1]
                        for index, coefficient in enumerate(axis))
            upper = sum(coefficient * bounds[index][1 if coefficient >= 0 else 0]
                        for index, coefficient in enumerate(axis))
            global_lower = lower if global_lower is None else min(global_lower, lower)
            global_upper = upper if global_upper is None else max(global_upper, upper)
    need(-3 * DENOMINATOR * grid < global_lower <= global_upper < 3 * DENOMINATOR * grid,
         "H632 source box")
    return {
        "grid_bits": 80,
        "coordinate_lower_bound": str(Fraction(global_lower, DENOMINATOR * grid)),
        "coordinate_upper_bound": str(Fraction(global_upper, DENOMINATOR * grid)),
        "squared_diameter_strict_upper_bound": 72,
    }


def adjacency(vertex_count, edges):
    graph = [set() for _ in range(vertex_count)]
    for left, right in edges:
        graph[left].add(right)
        graph[right].add(left)
    return graph


def graph_structure(vertices, graph):
    vertices = set(vertices)
    seen = set()
    components = []
    for start in sorted(vertices):
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        component = []
        while stack:
            vertex = stack.pop()
            component.append(vertex)
            for other in graph[vertex] & vertices:
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
        components.append(component)

    timer = 0
    entry = {}
    low = {}
    articulations = set()
    bridges = set()

    def visit(vertex, parent=None):
        nonlocal timer
        entry[vertex] = low[vertex] = timer
        timer += 1
        children = 0
        for other in graph[vertex] & vertices:
            if other == parent:
                continue
            if other in entry:
                low[vertex] = min(low[vertex], entry[other])
            else:
                visit(other, vertex)
                children += 1
                low[vertex] = min(low[vertex], low[other])
                if parent is not None and low[other] >= entry[vertex]:
                    articulations.add(vertex)
                if low[other] > entry[vertex]:
                    bridges.add(tuple(sorted((vertex, other))))
        if parent is None and children > 1:
            articulations.add(vertex)

    for vertex in sorted(vertices):
        if vertex not in entry:
            visit(vertex)
    return {
        "components": len(components),
        "largest_component": max(map(len, components)),
        "articulation_vertices": len(articulations),
        "bridges": len(bridges),
    }


def enumerate_induced_moser_spindles(graph, retained, reverse_old_map):
    role_embeddings = 0
    centres = set()
    vertex_sets = set()
    for origin in range(len(graph)):
        diamonds = []
        for tip in range(len(graph)):
            if tip == origin or tip in graph[origin]:
                continue
            common = sorted(graph[origin] & graph[tip])
            diamonds.extend(
                (tip, left, right)
                for left, right in combinations(common, 2)
                if right in graph[left]
            )
        for first in diamonds:
            for second in diamonds:
                if second[0] not in graph[first[0]]:
                    continue
                vertices = {origin, *first, *second}
                if len(vertices) != 7:
                    continue
                induced_edges = sum(right in graph[left]
                                    for left, right in combinations(sorted(vertices), 2))
                need(induced_edges == 11, "chorded Moser role embedding")
                role_embeddings += 1
                centres.add(origin)
                vertex_sets.add(tuple(sorted(vertices)))
    need(role_embeddings == 2 * len(vertex_sets), "Moser role multiplicity")
    need(all(set(vertices) <= retained for vertices in vertex_sets),
         "replacement point appears in a Moser spindle")
    final_stream = "".join(" ".join(map(str, vertices)) + "\n"
                           for vertices in sorted(vertex_sets)).encode("ascii")
    source_sets = sorted(
        tuple(sorted(reverse_old_map[vertex] for vertex in vertices))
        for vertices in vertex_sets
    )
    source_stream = "".join(" ".join(map(str, vertices)) + "\n"
                            for vertices in source_sets).encode("ascii")
    return {
        "induced_vertex_sets": len(vertex_sets),
        "role_embeddings": role_embeddings,
        "possible_origins": len(centres),
        "all_entirely_retained": True,
        "final_index_set_stream_sha256": sha256(final_stream),
        "source_label_set_stream_sha256": sha256(source_stream),
    }, vertex_sets


def first_triangle(vertices, graph):
    vertices = set(vertices)
    for left in sorted(vertices):
        for right in sorted(graph[left] & vertices):
            if left >= right:
                continue
            common = graph[left] & graph[right] & vertices
            if common:
                top = min(vertex for vertex in common if vertex > right) if any(
                    vertex > right for vertex in common) else None
                if top is not None:
                    return [left, right, top]
    raise ReviewFailure("no triangle")


def validate_certificate(certificate, data):
    need(certificate["vertices"] == 508 and certificate["unit_edges"] == 2341,
         "certificate graph size")
    need(certificate["source_vertices"] == 630 and certificate["source_edges"] == 3098,
         "certificate source size")
    need(certificate["retained_vertices"] == 418 and certificate["removed_vertices"] == 212 and
         certificate["replacement_formal_points"] == 91 and
         certificate["added_points"] == 90 and certificate["net_reduction"] == 122,
         "certificate physical budget")
    for key in ("retained_labels", "removed_labels", "old_to_final", "disk_to_final",
                "edge_split", "old_new_edges", "point_sha256", "edge_sha256"):
        need(certificate[key] == data[key], f"certificate field {key}")
    need(certificate["architecture_sha256"] == data["architecture_sha256"],
         "certificate architecture identity")
    need(certificate["two_anchor_old_labels"] == [0, 193], "certificate anchors")
    need(certificate["outside_original_field_points"] == 90, "outside-field count")
    need(certificate["status"] == "SAT_FOUR" and certificate["record_certified"] is False,
         "certificate claim status")
    word = certificate["four_word"]
    need(isinstance(word, str) and len(word) == 508 and set(word) <= set("0123"),
         "four-word schema")
    need(all(word[left] != word[right] for left, right in data["edges"]),
         "improper four-word")
    witness = certificate["moser_witness"]
    need(isinstance(witness, list) and len(witness) == len(set(witness)) == 7 and
         all(type(vertex) is int and 0 <= vertex < 508 for vertex in witness),
         "Moser witness schema")
    need(tuple(sorted(witness)) in data["moser_sets"], "submitted Moser witness")
    need(certificate["chromatic_number"] == 4, "chromatic claim")
    return word, witness


def verify():
    pinned = check_pins()
    source_points, source_edges, seed_edges, five_word, host_hash, seed_hash = reconstruct_source()
    source_indices = set(range(632)) - {399, 462}
    retained_labels = sorted(
        vertex for vertex in source_indices
        if all(source_points[vertex][offset + index] == 0
               for offset in (0, 8) for index in (2, 3, 6, 7))
    )
    removed_labels = sorted(source_indices - set(retained_labels))
    need((len(retained_labels), len(removed_labels)) == (418, 212), "whole-block sizes")
    retained_points = [convert_old(source_points[vertex]) for vertex in retained_labels]

    addresses = [(m, n) for m in range(-5, 6) for n in range(-5, 6)
                 if max(abs(m), abs(n), abs(m + n)) <= 5]
    disk_points = [disk_point(m, n) for m, n in addresses]
    zero = (0,) * 16
    need(len(disk_points) == len(set(disk_points)) == 91, "disk point census")
    need(set(retained_points) & set(disk_points) == {zero}, "unique physical collision")
    need(all(point[1] or point[3] or point[9] or point[11]
             for point in disk_points if point != zero),
         "nonzero disk point without sqrt(2)")

    points = sorted(set(retained_points) | set(disk_points))
    need(len(points) == 508, "final physical order")
    raw_points = point_bytes(points)
    need(raw_points == (TARGET / "points.csv").read_bytes(), "canonical final points")
    edges = complete_edges(points, NEW_PRIMES)
    raw_edges = edge_bytes(edges)
    need(raw_edges == (TARGET / "edges.csv").read_bytes(), "complete final edge census")
    need(len(edges) == 2341, "final edge count")

    positions = {point: index for index, point in enumerate(points)}
    old_to_final = {str(vertex): positions[convert_old(source_points[vertex])]
                    for vertex in retained_labels}
    disk_to_final = [
        {"m": m, "n": n, "vertex": positions[disk_point(m, n)]}
        for m, n in addresses
    ]
    retained = set(old_to_final.values())
    private = set(range(508)) - retained
    edge_split = {"old_old": 0, "old_new": 0, "new_new": 0}
    old_new_edges = []
    for left, right in edges:
        if left in retained and right in retained:
            kind = "old_old"
        elif left in private and right in private:
            kind = "new_new"
        else:
            kind = "old_new"
            old_new_edges.append([left, right])
        edge_split[kind] += 1
    need(edge_split == {"old_old": 2095, "old_new": 12, "new_new": 234},
         "edge partition")

    graph = adjacency(508, edges)
    reverse_old_map = {final: old for old, final in
                       ((int(key), value) for key, value in old_to_final.items())}
    moser_report, moser_sets = enumerate_induced_moser_spindles(
        graph, retained, reverse_old_map
    )
    expected_input_hashes = {
        str(OLD_INPUT.relative_to(ROOT)): PINNED[OLD_INPUT],
        str(FRESH_INPUT.relative_to(ROOT)): PINNED[FRESH_INPUT],
        str(SOURCE_CERT.relative_to(ROOT)): PINNED[SOURCE_CERT],
    }
    provenance = json.loads((TARGET / "PROVENANCE.json").read_text())
    need(provenance["input_hashes"] == expected_input_hashes,
         "provenance source identities")
    need(provenance["source_five_word"] == five_word,
         "provenance source word identity")
    data = {
        "retained_labels": retained_labels,
        "removed_labels": removed_labels,
        "old_to_final": old_to_final,
        "disk_to_final": disk_to_final,
        "edge_split": edge_split,
        "old_new_edges": old_new_edges,
        "point_sha256": sha256(raw_points),
        "edge_sha256": sha256(raw_edges),
        "architecture_sha256": sha256((TARGET / "ARCHITECTURE.json").read_bytes()),
        "edges": edges,
        "moser_sets": moser_sets,
    }
    certificate = json.loads((TARGET / "certificate.json").read_text())
    word, witness = validate_certificate(certificate, data)

    private_colours = {
        row["vertex"]: (row["m"] - row["n"]) % 3
        for row in disk_to_final if row["vertex"] in private
    }
    need(len(private_colours) == 90 and all(
        private_colours[left] != private_colours[right]
        for left, right in edges if left in private and right in private
    ), "private disk three-colouring")
    private_triangle = first_triangle(private, graph)

    origin = positions[zero]
    ten_unit_pairs = []
    for m, n in ((5, 0), (0, 5), (5, -5)):
        left = positions[disk_point(m, n)]
        right = positions[disk_point(-m, -n)]
        need(squared_distance(points[left], points[right], NEW_PRIMES) ==
             (100 * DENOMINATOR * DENOMINATOR,) + (0,) * 7,
             "ten-unit diameter pair")
        ten_unit_pairs.append([left, right])
    need(len({vertex for pair in ten_unit_pairs for vertex in pair}) == 6,
         "disjoint diameter pairs")

    target_source_labels = [reverse_old_map[vertex] for vertex in witness]
    full_colours = dict(sorted(Counter(word).items()))
    retained_colours = dict(sorted(Counter(word[vertex] for vertex in retained).items()))
    private_four_colours = dict(sorted(Counter(word[vertex] for vertex in private).items()))
    source_bounds = source_box(source_points)
    return {
        "status": "ACCEPT_AND_STRENGTHEN_H630_508_BLOCK_REPLACEMENT_STOP",
        "reviewed_target_commit": REVIEWED_TARGET_COMMIT,
        "pinned_public_files": pinned,
        "source_reconstruction": {
            "h632_vertices": 632,
            "h632_edges": len(source_edges),
            "h632_pairs_checked": 199396,
            "h632_edge_sha256": host_hash,
            "h630_vertices": 630,
            "h630_edges": len(seed_edges),
            "h630_edge_sha256": seed_hash,
            "source_five_word_checked": True,
            "prior_independent_review_aligned": True,
        },
        "construction": {
            "retained_points": len(retained),
            "removed_points": len(removed_labels),
            "formal_disk_points": len(disk_points),
            "unique_collision_points": 1,
            "private_disk_points": len(private),
            "physical_vertices": len(points),
            "complete_pairs_checked": 128778,
            "complete_unit_edges": len(edges),
            "edge_split": edge_split,
            "point_sha256": sha256(raw_points),
            "edge_sha256": sha256(raw_edges),
            "net_reduction_from_h630": 122,
        },
        "chromatic_certificate": {
            "chromatic_number": 4,
            "submitted_four_word_checked": True,
            "full_colour_frequencies": full_colours,
            "retained_colour_frequencies": retained_colours,
            "private_disk_four_word_frequencies": private_four_colours,
            "submitted_moser_final_indices": witness,
            "submitted_moser_source_labels": target_source_labels,
        },
        "structural_strengthening": {
            "induced_moser_spindles": moser_report,
            "retained_graph": {
                "vertices": len(retained),
                "edges": edge_split["old_old"],
                "chromatic_number": 4,
                **graph_structure(retained, graph),
            },
            "private_disk_graph": {
                "vertices": len(private),
                "edges": edge_split["new_new"],
                "chromatic_number": 3,
                "three_colouring_formula": "(m-n) mod 3",
                "triangle": private_triangle,
                **graph_structure(private, graph),
            },
            "full_graph": graph_structure(range(508), graph),
        },
        "containment_boundary": {
            "source_box": source_bounds,
            "ten_unit_disjoint_pairs": ten_unit_pairs,
            "origin_final_index": origin,
            "registered_H632_H560_H516_containment_excluded": True,
            "H516_plus_one_containment_excluded": True,
        },
        "scope": "one frozen H630 whole-block replacement and one radius-5 triangular disk",
        "record_candidate": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    arguments = parser.parse_args()
    report = verify()
    if arguments.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        need(report == expected, "expected output mismatch")
    print(json.dumps(report, indent=2, sort_keys=True))
