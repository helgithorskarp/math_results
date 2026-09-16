#!/usr/bin/env python3
"""Solver-free exact verifier for the E477 core translation-union stop."""

from __future__ import annotations

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, product
import json
from math import gcd
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_overlapping_forcing_seed"
RADICANDS = (1, 3, 11, 33)
RINDEX = {radicand: index for index, radicand in enumerate(RADICANDS)}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def file_hash(path):
    return sha256(path.read_bytes()).hexdigest()


def fadd(left, right):
    return tuple(a + b for a, b in zip(left, right))


def fsub(left, right):
    return tuple(a - b for a, b in zip(left, right))


def fmul(left, right):
    output = [0, 0, 0, 0]
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            common = gcd(RADICANDS[i], RADICANDS[j])
            radicand = RADICANDS[i] * RADICANDS[j] // (common * common)
            output[RINDEX[radicand]] += common * a * b
    return tuple(output)


def point(row):
    require(type(row) is list and len(row) == 4 and all(type(value) is int for value in row), "point row")
    a, b, c, d = row
    return (0, a, b, 0), (c, 0, 0, d)


def unit(left, right):
    dx = fsub(left[0], right[0])
    dy = fsub(left[1], right[1])
    return fadd(fmul(dx, dx), fmul(dy, dy)) == (36 * 36, 0, 0, 0)


def row_add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def row_sub(left, right):
    return tuple(a - b for a, b in zip(left, right))


def line_hash(lines):
    return sha256("".join(lines).encode()).hexdigest()


def rebuild(certificate):
    require(certificate.get("format") == "E477 mandatory-core maximum-translation union certificate v1", "format")
    for name, expected in certificate["input_sha256"].items():
        require(file_hash(SOURCE / name) == expected, "input hash: " + name)
    equal = json.loads((SOURCE / "certificate.json").read_text())["equal"]
    mandatory = json.loads((SOURCE / "mandatory_vertices.json").read_text())
    require(equal["denominator"] == 1 and len(equal["points"]) == 477, "E477 source")
    rows = equal["points"]
    deleted = [entry["deleted"] for entry in mandatory]
    require(len(deleted) == len(set(deleted)) == 253 and not {0, 1} & set(deleted), "mandatory labels")
    core_labels = sorted({0, 1, *deleted})
    core_rows = [rows[label] for label in core_labels]
    require(len(core_rows) == certificate["source_core_points"] == 255, "core order")

    # This is a complete finite selection, not a sampled translation list.
    counts = Counter(
        row_sub(right, left)
        for left in core_rows
        for right in core_rows
        if left != right
    )
    maximum = max(counts.values())
    maximizing = sorted(delta for delta, count in counts.items() if count == maximum)
    selected = tuple(certificate["selected_translation"])
    require(maximum == certificate["translation_overlap_maximum"] == 75, "maximum overlap")
    require(len(maximizing) == certificate["maximum_translation_count"] == 2, "maximum translation count")
    require(selected == maximizing[0], "translation selection rule")

    representations = defaultdict(list)
    for core_index, row in enumerate(core_rows):
        representations[tuple(row)].append((0, core_index, core_labels[core_index]))
        representations[row_add(row, selected)].append((1, core_index, core_labels[core_index]))
    physical_rows = sorted(representations)
    physical_points = [point(list(row)) for row in physical_rows]
    require(len(set(physical_points)) == len(physical_points) == certificate["union_points"] == 435, "union order")
    row_index = {row: index for index, row in enumerate(physical_rows)}

    edges = [pair for pair in combinations(range(len(physical_points)), 2) if unit(physical_points[pair[0]], physical_points[pair[1]])]
    require(len(edges) == certificate["union_complete_unit_edges"] == 1589, "complete edge count")
    edge_set = set(edges)
    core_points = [point(row) for row in core_rows]
    core_edges = [pair for pair in combinations(range(len(core_points)), 2) if unit(core_points[pair[0]], core_points[pair[1]])]
    require(len(core_edges) == certificate["source_core_edges"] == 659, "core edge count")
    inherited = set()
    for copy in (0, 1):
        image = [
            row_index[tuple(row) if copy == 0 else row_add(row, selected)]
            for row in core_rows
        ]
        for left, right in core_edges:
            inherited.add(tuple(sorted((image[left], image[right]))))
    require(inherited <= edge_set, "inherited edge loss")
    private = edge_set - inherited
    require(len(inherited) == certificate["union_inherited_edge_union"] == 1231, "inherited edge union")
    require(len(private) == certificate["union_private_contacts"] == 358, "private contact count")
    overlaps = [row for row in physical_rows if {entry[0] for entry in representations[row]} == {0, 1}]
    require(len(overlaps) == maximum, "physical overlap count")

    point_hash = line_hash(f"{','.join(map(str, row))}\n" for row in physical_rows)
    edge_hash = line_hash(f"{left},{right}\n" for left, right in edges)
    require(point_hash == certificate["point_sha256"], "point hash")
    require(edge_hash == certificate["edge_sha256"], "edge hash")

    word = certificate["four_colouring"]
    require(type(word) is str and len(word) == len(physical_rows) and all(char in "0123" for char in word), "four-colour word")
    require(all(word[left] != word[right] for left, right in edges), "monochromatic complete edge")

    # A seven-vertex Moser spindle inside the first core proves that the upper
    # bound four is sharp.  The exhaustive check is tiny and names no palette.
    moser_labels = certificate["moser_source_labels"]
    require(len(moser_labels) == len(set(moser_labels)) == 7 and set(moser_labels) <= set(core_labels), "Moser labels")
    moser_vertices = [row_index[tuple(rows[label])] for label in moser_labels]
    moser_edges = [
        (i, j)
        for i, j in combinations(range(7), 2)
        if tuple(sorted((moser_vertices[i], moser_vertices[j]))) in edge_set
    ]
    require(len(moser_edges) == 11, "Moser edge count")
    proper_three = sum(
        all(colours[left] != colours[right] for left, right in moser_edges)
        for colours in product(range(3), repeat=7)
    )
    require(proper_three == 0, "Moser three-colouring")

    return {
        "status": "VERIFIED_FOUR_CHROMATIC_STOP",
        "source_points": len(rows),
        "source_core_points": len(core_rows),
        "source_core_complete_unit_edges": len(core_edges),
        "maximal_nonzero_translation_overlap": maximum,
        "maximizing_translations": len(maximizing),
        "selected_translation": list(selected),
        "union_points": len(physical_rows),
        "union_complete_unit_edges": len(edges),
        "physical_overlaps": len(overlaps),
        "inherited_edge_union": len(inherited),
        "private_contacts": len(private),
        "four_colouring_verified": True,
        "embedded_moser_vertices": len(moser_vertices),
        "embedded_moser_edges": len(moser_edges),
        "embedded_moser_proper_three_colourings": proper_three,
        "chromatic_number": 4,
        "point_sha256": point_hash,
        "edge_sha256": edge_hash,
        "record_candidate": False,
    }


def verify(certificate=None):
    if certificate is None:
        certificate = json.loads((HERE / "certificate.json").read_text())
    return rebuild(certificate)


def main():
    result = verify()
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    require(result == expected, "expected output")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
