#!/usr/bin/env python3
"""Independent exact review of the 462-point generated-anchor network.

No target executable is imported.  The finite network is reconstructed from
its address-box definition using an explicit multiplier matrix and a direct
Gram form on the cyclotomic power basis.  General Q(zeta_5) arithmetic is
used separately for the registered fixed-base overlay comparison.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "hadwiger_nelson_golden_generated_anchor_box_stop"
OVERLAY = ROOT / "hadwiger_nelson_golden_reciprocal_closure"

REVIEWED_MATHEMATICAL_COMMIT = "3beda50683c9d24e033e30e4b35e9d0d5927f0d7"
REVIEWED_RECEIPT_COMMIT = "14f6cf9288764cb9190f2a96f66d8a6a813b9d3e"

PINNED = {
    TARGET / "README.md":
        "7e4c0ce3275fee3a1d0984862aedf79e877c7c88179127756ad262e641a48466",
    TARGET / "PROOF.md":
        "3b3cad3e1def068207e8d4d9f2bd8313d1fced1385cf8f60e70bb6cef1e68aff",
    TARGET / "ARCHITECTURE.json":
        "5524bf063add5f339472dc4004a34490b66ebae4758cd81e4ee6edc3f3c1006e",
    TARGET / "PROVENANCE.json":
        "740a629e942e43415062a40703078be8b8dff0ad47d898cb754579e7a5a46a6b",
    TARGET / "VERIFY.json":
        "5d669a07084380b2db6c76b748e29fa3a9d7e6348d973f9db03d4e5dc2655600",
    TARGET / "certificate.json":
        "be89c4c158f25a734cecc393ceffd32fd8cb972dabf2e2f952e10d1ece8d5f35",
    TARGET / "points.csv":
        "c4705ba3e02ef24680a4357f9e52a22007526606548cfc6458ef343e2061b03c",
    TARGET / "edges.csv":
        "44716e51e7b5c4798d10e6a1103dc1b6ecb75df689a7b33e10ca79d8a2c96c28",
    TARGET / "reproduce.py":
        "f459933ad7004cc77507ac057fdafdd4c6ee3198fb6a46a5bea1b883aa64d626",
    TARGET / "verify.py":
        "f4113d79e069b003dd15a56eb38a0a5493225e3ecf9aa4373b3f9b39594b056b",
    OVERLAY / "README.md":
        "bb8e20aee95b9b958aa54569d638fa5d42d88c3fbe50e9dac8d9500fc025cfd5",
    OVERLAY / "PROOF.md":
        "04c6321aeab0b80631c99f7f94fe9bfb25e787e1f7503c0e396a0bf61e48cce7",
    OVERLAY / "model.py":
        "18ba0b0bf277283b46fa944ae57db22bc9fbceafefdf4c451bc6333e421f2677",
}

ZERO = (F(0),) * 4
ONE = (F(1), F(0), F(0), F(0))
ZETA = (F(0), F(1), F(0), F(0))
ZETA4 = (F(-1),) * 4
SQRT5 = (F(-1), F(0), F(-2), F(-2))
LAMBDA = (F(0), F(-1), F(0), F(-1))
UNIT_NORM_PAIR = (F(5), F(-1))
GOLDEN_NORM_PAIR = (F(5), F(1))
RESIDUE_FORM = (0, 1, 2, 1)

BITS = (
    (0, 0, 0, 0), (1, 0, 0, 0), (0, 0, 0, 1), (1, 0, 0, 1),
    (0, 1, 0, 0), (0, 0, 1, 0), (1, 0, 1, 0), (0, 1, 0, 1),
    (1, 1, 0, 0), (0, 0, 1, 1), (1, 1, 0, 1), (1, 0, 1, 1),
    (0, 1, 1, 0), (1, 1, 1, 0), (0, 1, 1, 1), (1, 1, 1, 1),
)

SOURCE_UNIT_LABELS = (
    (1, 2), (1, 3), (2, 4), (2, 5), (3, 4), (3, 6), (4, 7),
    (4, 8), (5, 6), (5, 8), (5, 9), (6, 7), (6, 10), (7, 9),
    (7, 12), (7, 13), (8, 10), (8, 11), (8, 13), (9, 11),
    (10, 12), (11, 12), (11, 14), (12, 15), (13, 14), (13, 15),
    (14, 16), (15, 16),
)

SOURCE_GOLDEN_LABELS = (
    (1, 5), (1, 6), (2, 3), (2, 6), (2, 7), (2, 9), (3, 5),
    (3, 8), (3, 10), (4, 9), (4, 10), (4, 11), (4, 12),
    (5, 13), (6, 13), (7, 10), (7, 14), (8, 9), (8, 15),
    (9, 13), (9, 14), (10, 13), (10, 15), (11, 15), (11, 16),
    (12, 14), (12, 16), (14, 15),
)


class ReviewFailure(RuntimeError):
    pass


def need(condition, message):
    if not condition:
        raise ReviewFailure(message)


def sha256(blob):
    return hashlib.sha256(blob).hexdigest()


def stream_hash(rows):
    return sha256(("\n".join(rows) + "\n").encode("ascii"))


def check_pins():
    for path, expected in PINNED.items():
        need(path.is_file(), f"missing pinned file: {path.relative_to(ROOT)}")
        need(sha256(path.read_bytes()) == expected,
             f"hash mismatch: {path.relative_to(ROOT)}")
    return len(PINNED)


def add(first, second):
    return tuple(a + b for a, b in zip(first, second, strict=True))


def neg(value):
    return tuple(-a for a in value)


def sub(first, second):
    return add(first, neg(second))


def scale(scalar, value):
    scalar = F(scalar)
    return tuple(scalar * a for a in value)


def linear_combination(coefficients, vectors):
    return tuple(sum(F(coefficient) * vector[index]
                     for coefficient, vector in zip(coefficients, vectors, strict=True))
                 for index in range(4))


def multiply(first, second):
    """Multiply in Q[zeta_5], reducing exponents modulo five then zeta^4."""
    coefficients = [F(0)] * 5
    for i, a in enumerate(first):
        for j, b in enumerate(second):
            coefficients[(i + j) % 5] += a * b
    zeta4 = coefficients[4]
    return tuple(coefficients[index] - zeta4 for index in range(4))


def conjugate(value):
    a0, a1, a2, a3 = value
    return (a0 - a1, -a1, -a1 + a3, -a1 + a2)


def norm_pair(value):
    """Return (R,S) with 2*z*conj(z)=R+S*sqrt(5)."""
    a0, a1, a2, a3 = value
    adjacent = a0 * a1 + a1 * a2 + a2 * a3
    other = a0 * a2 + a0 * a3 + a1 * a3
    return (2 * sum(coefficient * coefficient for coefficient in value)
            - adjacent - other,
            adjacent - other)


def real_element(rational, radical):
    return add(scale(rational, ONE), scale(radical, SQRT5))


def inverse(value):
    rational, radical = norm_pair(value)
    denominator = rational * rational - 5 * radical * radical
    need(denominator != 0, "division by zero")
    inverse_norm = real_element(2 * rational / denominator,
                                -2 * radical / denominator)
    result = multiply(conjugate(value), inverse_norm)
    need(multiply(value, result) == ONE, "field inverse")
    return result


def divide(first, second):
    return multiply(first, inverse(second))


def multiply_lambda(value):
    """Explicit matrix for (-zeta-zeta^3)*value."""
    a0, a1, a2, a3 = value
    return (a1 - a2 + a3, -a0 + a1, a3,
            -a0 + a1 - a2 + a3)


def serialize_csv(rows):
    return "".join(",".join(map(str, row)) + "\n" for row in rows).encode("ascii")


def source_geometry():
    basis = tuple(tuple(F(index == coordinate) for coordinate in range(4))
                  for index in range(4))
    differences = tuple(sub(basis[index], ZETA4) for index in range(4))
    base_corner = scale(5, ZETA4)
    points = tuple(add(base_corner, linear_combination(bits, differences))
                   for bits in BITS)
    need(len(set(points)) == 16, "source collisions")
    need(multiply_lambda(ONE) == LAMBDA and
         all(multiply_lambda(value) == multiply(LAMBDA, value)
             for value in differences), "lambda matrix")
    return base_corner, differences, points


def source_edges(points):
    unit = tuple((left + 1, right + 1)
                 for left, right in combinations(range(16), 2)
                 if norm_pair(sub(points[right], points[left])) == UNIT_NORM_PAIR)
    golden = tuple((left + 1, right + 1)
                   for left, right in combinations(range(16), 2)
                   if norm_pair(sub(points[right], points[left])) == GOLDEN_NORM_PAIR)
    need(unit == SOURCE_UNIT_LABELS and golden == SOURCE_GOLDEN_LABELS,
         "source distance lists")
    return unit, golden


def network_geometry():
    base_corner, differences, base = source_geometry()
    grid = {
        address: add(base_corner, multiply_lambda(
            linear_combination(address, differences)))
        for address in product(range(4), range(4), range(4), range(7))
    }
    need(len(grid) == 448 and len(set(grid.values())) == 448,
         "grid address independence")
    copies = {
        address: tuple(grid[tuple(address[index] + bits[index]
                                  for index in range(4))]
                       for bits in BITS)
        for address in product(range(3), range(3), range(3), range(6))
    }
    need(len(copies) == 162 and
         set().union(*(set(values) for values in copies.values())) == set(grid.values()),
         "whole-copy union")
    need(copies[(0, 0, 0, 0)][0] == base[0] and
         copies[(0, 0, 0, 0)][4] == base[1], "root anchor roles")

    seen = set(base)
    generated = 0
    parent_faces = []
    intersection_histogram = Counter()
    for address, values in copies.items():
        intersection_histogram[len(set(values) & set(base))] += 1
        if any(address):
            coordinate = next(index for index in range(4) if address[index])
            parent = tuple(address[index] - (index == coordinate) for index in range(4))
            face = set(values) & set(copies[parent])
            need(len(face) == 8 and face <= seen, "unavailable parent face")
            need(len(face - set(base)) >= 2, "parent face lacks generated anchors")
            generated += 1
            parent_faces.append((address, parent, len(face - set(base))))
        seen.update(values)
    need(generated == 161 and intersection_histogram == Counter({0: 160, 1: 1, 2: 1}),
         "generated-anchor census")

    terminal_address = (2, 2, 2, 5)
    terminal_corner = grid[(3, 3, 3, 6)]
    need(not (set(copies[terminal_address]) & set(base)), "terminal base incidence")
    need(sum(terminal_corner in values for values in copies.values()) == 1 and
         terminal_corner in copies[terminal_address], "terminal unique corner")

    merged = set(base) | set(grid.values())
    need(len(set(base) & set(grid.values())) == 2 and len(merged) == 462,
         "physical collision quotient")
    points = tuple(sorted(merged))
    need(all(all(value.denominator == 1 for value in row) for row in points),
         "nonintegral network coordinate")
    rows = tuple(tuple(int(value) for value in row) for row in points)
    index = {point: position for position, point in enumerate(points)}
    edges = tuple((left, right)
                  for left, right in combinations(range(len(points)), 2)
                  if norm_pair(sub(points[right], points[left])) == UNIT_NORM_PAIR)
    return {
        "base": base,
        "grid": grid,
        "copies": copies,
        "points": points,
        "rows": rows,
        "edges": edges,
        "base_indices": [index[point] for point in base],
        "terminal_corner_index": index[terminal_corner],
        "intersection_histogram": dict(sorted(intersection_histogram.items())),
        "generated": generated,
        "parent_faces": parent_faces,
    }


def scaled_norm_pair(pair, sign):
    """Multiply R+S*sqrt(5) by (3+sign*sqrt(5))/2."""
    rational, radical = pair
    return ((3 * rational + sign * 5 * radical) / 2,
            (sign * rational + 3 * radical) / 2)


def enumerate_registered_copies(base, sign):
    pairs = tuple(combinations(range(16), 2))
    differences = {pair: sub(base[pair[1]], base[pair[0]]) for pair in pairs}
    norms = {pair: norm_pair(value) for pair, value in differences.items()}
    copies = set()
    raw = 0
    for source_pair in pairs:
        required = scaled_norm_pair(norms[source_pair], sign)
        for target_pair in pairs:
            if norms[target_pair] != required:
                continue
            for image_left, image_right in (target_pair,
                                            (target_pair[1], target_pair[0])):
                image_difference = sub(base[image_right], base[image_left])
                for reflected in (False, True):
                    raw += 1
                    source_left = (conjugate(base[source_pair[0]]) if reflected
                                   else base[source_pair[0]])
                    source_difference = (conjugate(differences[source_pair]) if reflected
                                         else differences[source_pair])
                    multiplier = divide(image_difference, source_difference)
                    moved = tuple(add(base[image_left], multiply(
                        multiplier,
                        sub(conjugate(point) if reflected else point, source_left)))
                        for point in base)
                    copies.add(tuple(sorted(moved)))
    return raw, copies


def registered_overlay(base):
    groups = {}
    closure = set(base)
    for name, sign in (("down", -1), ("up", 1)):
        raw, copies = enumerate_registered_copies(base, sign)
        histogram = Counter(len(set(copy) & set(base)) for copy in copies)
        need(raw == 5568 and len(copies) == 328 and
             histogram == Counter({2: 186, 3: 64, 4: 16,
                                    5: 24, 6: 20, 7: 18}),
             f"registered {name} copy census")
        for copy in copies:
            closure.update(copy)
        groups[name] = {
            "raw_specifications": raw,
            "distinct_copies": len(copies),
            "base_overlap_histogram": dict(sorted(histogram.items())),
        }
    need(len(closure) == 1386, "registered overlay order")
    return closure, groups


def residue(value):
    value = F(value)
    denominator = value.denominator % 3
    need(denominator != 0, "coefficient outside Z_(3)")
    return (value.numerator % 3) * pow(denominator, -1, 3) % 3


def residue_colour(point):
    coefficients = tuple(residue(value) for value in point)
    return sum(weight * value
               for weight, value in zip(RESIDUE_FORM, coefficients, strict=True)) % 3


def residue_theorem():
    unit_residues = []
    for row in product(range(3), repeat=4):
        norm = norm_pair(tuple(F(value) for value in row))
        if (int(norm[0]) % 3, int(norm[1]) % 3) == (2, 2):
            unit_residues.append(row)
    need(len(unit_residues) == 10, "unit residue census")
    values = [sum(weight * value for weight, value in
                  zip(RESIDUE_FORM, row, strict=True)) % 3
              for row in unit_residues]
    need(set(values) == {1, 2} and 0 not in values,
         "residue form vanishes on a possible unit")
    return tuple(unit_residues), tuple(values)


def adjacency(vertices, edges):
    graph = [set() for _ in range(vertices)]
    for first, second in edges:
        graph[first].add(second)
        graph[second].add(first)
    return graph


def graph_structure(vertices, edges):
    graph = adjacency(vertices, edges)
    discovery = [-1] * vertices
    low = [0] * vertices
    timer = 0
    components = 0
    articulations = set()
    bridges = set()

    def visit(vertex, parent=-1):
        nonlocal timer
        discovery[vertex] = low[vertex] = timer
        timer += 1
        children = 0
        for other in sorted(graph[vertex]):
            if other == parent:
                continue
            if discovery[other] >= 0:
                low[vertex] = min(low[vertex], discovery[other])
            else:
                visit(other, vertex)
                children += 1
                low[vertex] = min(low[vertex], low[other])
                if low[other] > discovery[vertex]:
                    bridges.add(tuple(sorted((vertex, other))))
                if parent >= 0 and low[other] >= discovery[vertex]:
                    articulations.add(vertex)
        if parent < 0 and children > 1:
            articulations.add(vertex)

    for start in range(vertices):
        if discovery[start] < 0:
            components += 1
            visit(start)

    cores = {}
    for degree in (2, 3, 4, 5):
        live = set(range(vertices))
        queue = [vertex for vertex in live if len(graph[vertex]) < degree]
        while queue:
            vertex = queue.pop()
            if vertex not in live:
                continue
            live.remove(vertex)
            for other in graph[vertex] & live:
                if len(graph[other] & live) < degree:
                    queue.append(other)
        cores[str(degree)] = len(live)
    return graph, {
        "components": components,
        "articulation_vertices": len(articulations),
        "bridges": len(bridges),
        "minimum_degree": min(map(len, graph)),
        "maximum_degree": max(map(len, graph)),
        "core_orders": cores,
    }


def proper(word, colours, vertices, edges):
    return (isinstance(word, str) and len(word) == vertices and
            set(word) <= set(str(value) for value in range(colours)) and
            all(word[first] != word[second] for first, second in edges))


def validate_certificate(certificate, data):
    need(certificate["architecture_sha256"] == PINNED[TARGET / "ARCHITECTURE.json"],
         "architecture identity")
    need(certificate["vertices"] == 462 and certificate["edges"] == 1532,
         "physical counts")
    need(certificate["source_points"] == 16 and certificate["grid_points"] == 448 and
         certificate["intersection"] == 2 and certificate["whole_copies"] == 162,
         "architecture counts")
    need(certificate["generated_anchored_copies"] == 161 and
         certificate["base_intersection_histogram"] == {"0": 160, "1": 1, "2": 1},
         "generated-anchor metadata")
    need(certificate["terminal_unique_corner_index"] == data["terminal_corner_index"] == 461,
         "terminal corner")
    need(certificate["outside_closed_overlay_points"] == data["outside_overlay"] == 406,
         "overlay boundary")
    need(certificate["registered_overlay_points"] == 1386,
         "registered overlay metadata")
    need(certificate["base_indices"] == data["base_indices"], "base roles")
    need(certificate["point_sha256"] == data["point_sha256"] and
         certificate["edge_sha256"] == data["edge_sha256"], "graph hashes")
    need(proper(certificate["four_word"], 4, 462, data["edges"]),
         "submitted four-word")
    source_word = "".join(certificate["four_word"][index]
                          for index in data["base_indices"])
    need(source_word == certificate["source_restriction_word"] == "0213102001131001",
         "submitted source restriction")
    failed = [[first, second] for first, second in SOURCE_GOLDEN_LABELS
              if source_word[first - 1] == source_word[second - 1]]
    need(failed == certificate["golden_source_constraints_violated"] and
         len(failed) == 12, "submitted source obstruction failure")
    five_word = certificate["source_five_word"]
    need(len(five_word) == 16 and set(five_word) <= set(range(5)) and
         all(five_word[first - 1] != five_word[second - 1]
             for first, second in SOURCE_UNIT_LABELS + SOURCE_GOLDEN_LABELS),
         "source five-word")
    clique = certificate["source_K5_labels_one_based"]
    source_edges_set = set(SOURCE_UNIT_LABELS + SOURCE_GOLDEN_LABELS)
    need(clique == [1, 2, 3, 5, 6] and
         all(tuple(sorted(edge)) in source_edges_set
             for edge in combinations(clique, 2)), "source K5")
    need(certificate["ordinary_four_colourable"] is True and
         certificate["record_candidate"] is False and
         certificate["non_four_signal"] is False, "claim status")


def reconstruct():
    need(multiply(ZETA, multiply(ZETA, multiply(ZETA, multiply(ZETA, ZETA)))) == ONE,
         "fifth root relation")
    need(multiply(SQRT5, SQRT5) == scale(5, ONE), "sqrt(5) relation")
    base_corner, differences, base = source_geometry()
    unit_labels, golden_labels = source_edges(base)
    network = network_geometry()

    point_blob = serialize_csv(network["rows"])
    edge_blob = serialize_csv(network["edges"])
    need(point_blob == (TARGET / "points.csv").read_bytes(), "point-stream mismatch")
    need(edge_blob == (TARGET / "edges.csv").read_bytes(), "edge-stream mismatch")
    point_sha = sha256(point_blob)
    edge_sha = sha256(edge_blob)
    need(point_sha == PINNED[TARGET / "points.csv"] and
         edge_sha == PINNED[TARGET / "edges.csv"], "stream identities")
    need(len(network["edges"]) == 1532, "complete edge count")

    overlay, overlay_groups = registered_overlay(base)
    outside = set(network["points"]) - overlay
    need(len(outside) == 406, "outside-overlay count")
    need(network["points"][network["terminal_corner_index"]] in outside,
         "terminal corner lies in registered overlay")

    residues, residue_values = residue_theorem()
    three_word = "".join(str(residue_colour(point)) for point in network["points"])
    need(proper(three_word, 3, 462, network["edges"]), "residue three-word")
    base_three_word = "".join(three_word[index] for index in network["base_indices"])

    # The source labels 6-3-1-2-5 form an exact unit C5.
    source_cycle_labels = (6, 3, 1, 2, 5)
    source_unit_set = set(unit_labels)
    need(all(tuple(sorted((source_cycle_labels[index],
                           source_cycle_labels[(index + 1) % 5]))) in source_unit_set
             for index in range(5)), "source unit five-cycle")
    cycle = [network["base_indices"][label - 1] for label in source_cycle_labels]
    edge_set = set(network["edges"])
    need(all(tuple(sorted((cycle[index], cycle[(index + 1) % 5]))) in edge_set
             for index in range(5)), "physical unit five-cycle")

    need(all(all(value.denominator % 3 != 0 for value in point)
             for point in overlay), "overlay leaves Z_(3)[zeta]")
    overlay_colours = Counter(residue_colour(point) for point in overlay)

    graph, structure = graph_structure(462, network["edges"])
    need(structure == {
        "components": 1,
        "articulation_vertices": 0,
        "bridges": 0,
        "minimum_degree": 2,
        "maximum_degree": 10,
        "core_orders": {"2": 462, "3": 457, "4": 428, "5": 332},
    }, "graph structure")

    network.update({
        "point_sha256": point_sha,
        "edge_sha256": edge_sha,
        "outside_overlay": len(outside),
        "overlay_groups": overlay_groups,
        "overlay_points": len(overlay),
        "overlay_colour_frequencies": dict(sorted(overlay_colours.items())),
        "residues": residues,
        "residue_values": residue_values,
        "three_word": three_word,
        "base_three_word": base_three_word,
        "five_cycle_labels": source_cycle_labels,
        "five_cycle_indices": cycle,
        "structure": structure,
        "source_unit_edges": unit_labels,
        "source_golden_edges": golden_labels,
    })
    return network


def verify():
    pinned = check_pins()
    data = reconstruct()
    certificate = json.loads((TARGET / "certificate.json").read_text())
    validate_certificate(certificate, data)
    residue_rows = tuple(" ".join(map(str, row)) for row in data["residues"])
    result = {
        "status": "ACCEPT_AND_STRENGTHEN_GOLDEN_NETWORK_TO_EXACT_THREE_CHROMATIC",
        "reviewed_mathematical_commit": REVIEWED_MATHEMATICAL_COMMIT,
        "reviewed_receipt_commit": REVIEWED_RECEIPT_COMMIT,
        "pinned_public_files": pinned,
        "construction": {
            "vertices": len(data["points"]),
            "complete_pairs": 462 * 461 // 2,
            "complete_unit_edges": len(data["edges"]),
            "grid_points": len(data["grid"]),
            "whole_copies": len(data["copies"]),
            "generated_anchor_copies": data["generated"],
            "base_overlap": 2,
            "base_intersection_histogram": {
                str(key): value for key, value in data["intersection_histogram"].items()
            },
            "terminal_corner_index": data["terminal_corner_index"],
            "outside_registered_overlay_points": data["outside_overlay"],
            "point_sha256": data["point_sha256"],
            "edge_sha256": data["edge_sha256"],
            **data["structure"],
        },
        "chromatic_strengthening": {
            "chromatic_number": 3,
            "three_colour_formula": "a1+2*a2+a3 mod 3",
            "three_word_sha256": sha256((data["three_word"] + "\n").encode("ascii")),
            "three_colour_frequencies": dict(sorted(Counter(data["three_word"]).items())),
            "source_three_word": data["base_three_word"],
            "unit_five_cycle_source_labels_one_based": list(data["five_cycle_labels"]),
            "unit_five_cycle_final_indices": data["five_cycle_indices"],
            "submitted_four_word_checked": True,
            "source_two_distance_chromatic_number": 5,
        },
        "module_theorem": {
            "module": "q*Z_(3)[zeta_5]",
            "statement": "the complete strict unit-distance graph on the module has chromatic number exactly 3",
            "coefficient_residue_form": list(RESIDUE_FORM),
            "possible_unit_difference_residues": len(data["residues"]),
            "unit_residue_stream_sha256": stream_hash(residue_rows),
            "residue_colour_values": list(data["residue_values"]),
            "lower_bound_witness": "the source unit five-cycle is contained in the module",
            "historical_priority_claimed": False,
        },
        "registered_overlay_corollary": {
            "points": data["overlay_points"],
            "down": {
                "raw_specifications": data["overlay_groups"]["down"]["raw_specifications"],
                "distinct_copies": data["overlay_groups"]["down"]["distinct_copies"],
                "base_overlap_histogram": {
                    str(key): value for key, value in
                    data["overlay_groups"]["down"]["base_overlap_histogram"].items()
                },
            },
            "up": {
                "raw_specifications": data["overlay_groups"]["up"]["raw_specifications"],
                "distinct_copies": data["overlay_groups"]["up"]["distinct_copies"],
                "base_overlap_histogram": {
                    str(key): value for key, value in
                    data["overlay_groups"]["up"]["base_overlap_histogram"].items()
                },
            },
            "points_outside_generated_network":
                data["overlay_points"] - (462 - data["outside_overlay"]),
            "all_coefficients_integral_at_3": True,
            "chromatic_number": 3,
            "colour_frequencies": {
                str(key): value for key, value in data["overlay_colour_frequencies"].items()
            },
        },
        "record_candidate": False,
        "scope": "the frozen network plus the explicit q*Z_(3)[zeta_5] module obstruction",
    }
    need(result["chromatic_strengthening"]["three_word_sha256"] ==
         "3d554880750584f595f70c72c1b76a26d5f64dd7b373973e61645741fae0987a",
         "three-word identity")
    need(result["module_theorem"]["unit_residue_stream_sha256"] ==
         "72a4922ae2dfb980b4caf4f752a60ac99d07adf7076884429e9c69bb569acaa3",
         "unit-residue identity")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = verify()
    if args.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        need(result == expected, "EXPECTED.json mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
