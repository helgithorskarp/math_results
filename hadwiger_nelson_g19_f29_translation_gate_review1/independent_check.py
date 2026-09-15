#!/usr/bin/env python3
"""Independent exact review of the fixed G19--(F29+i) attachment.

No code is imported from the reviewed package.  The two geometric components
are rebuilt from their displayed radical formulas in a SymPy algebraic field;
all distances are then tested exactly.  A generic MRV backtracker enumerates
the complete normalized boundary colour distributions of both components.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

from sympy import QQ, Rational, sqrt


HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE = HERE.parent / "hadwiger_nelson_g19_f29_translation_gate"
G19_SOURCE = HERE.parent / "hadwiger_nelson_moser_palette_private_bridge"
F29_SOURCE = HERE.parent / "hadwiger_nelson_frozen_centre_transfer"
SOURCE_COMMIT = "039ba6658345ebff92846ff1616004174c1857c3"
SHARED = ((0, 11), (25, 15), (28, 16))
G19_PINS = ((11, 0), (15, 1), (16, 2))
F29_PINS = ((0, 0), (25, 1), (28, 2))


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_digest(value) -> str:
    raw = json.dumps(value, separators=(",", ":"), sort_keys=True).encode()
    return hashlib.sha256(raw).hexdigest()


def point_add(p, q):
    return p[0] + q[0], p[1] + q[1]


def point_sub(p, q):
    return p[0] - q[0], p[1] - q[1]


def point_scale(p, q):
    return p[0] * q, p[1] * q


def complex_mul(p, q):
    return p[0] * q[0] - p[1] * q[1], p[0] * q[1] + p[1] * q[0]


def squared_norm(p):
    return p[0] * p[0] + p[1] * p[1]


def parse_f29_rows(path: Path) -> list[tuple[int, int, int, int]]:
    rows = []
    for line in path.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        label, a, b, c, d = map(int, line.split())
        need(label == len(rows), "nonconsecutive F29 label")
        rows.append((a, b, c, d))
    need(len(rows) == 29, "F29 row count")
    return rows


def parse_certificate_points(rows, basis, field):
    points = []
    for row in rows:
        need(len(row) == 2 and all(len(axis) == 8 for axis in row), "coordinate shape")
        axes = []
        for axis in row:
            value = field.zero
            for coefficient, basis_element in zip(axis, basis):
                value += field.from_sympy(Rational(coefficient)) * basis_element
            axes.append(value)
        points.append(tuple(axes))
    return points


@dataclass
class Geometry:
    g19_points: list
    f29_points: list
    points: list
    g19_edges: list[tuple[int, int]]
    f29_edges: list[tuple[int, int]]
    inherited_edges: list[tuple[int, int]]
    edges: list[tuple[int, int]]
    f29_map: list[int]
    field_degree: int


def reconstruct_geometry(certificate: dict, source_dir: Path) -> Geometry:
    """Rebuild both components, merge exact coordinates, and audit all pairs."""

    need(certificate["schema"] == "g19-f29-translation-gate-v1", "certificate schema")
    field = QQ.algebraic_field(sqrt(3), sqrt(11), sqrt((4 - sqrt(3)) / 2))
    need(field.ext.minpoly.degree() == 8, "displayed field does not have degree eight")
    zero, one = field.zero, field.one
    s = field.from_sympy(sqrt(3))
    t = field.from_sympy(sqrt(11))
    y = field.from_sympy(sqrt((4 - sqrt(3)) / 2))
    two, six, twelve = map(field.convert, (2, 6, 12))
    need(s * s == field.convert(3), "sqrt(3) relation")
    need(t * t == field.convert(11), "sqrt(11) relation")
    need(y * y == (field.convert(4) - s) / two, "y relation")

    # Reconstruct G19 from the source's Moser and cap/diamond formulas.
    rho = ((one + zero) / two, s / two)
    tau = (field.convert(5) / six, t / six)
    origin, unit = (zero, zero), (one, zero)
    moser = [
        origin,
        unit,
        rho,
        point_add(unit, rho),
        tau,
        complex_mul(tau, rho),
        complex_mul(tau, point_add(unit, rho)),
        (rho[0], -rho[1]),
        point_scale(rho, two),
        point_scale(tau, two),
        complex_mul(tau, (rho[0] - one, rho[1])),
    ]
    caps = (
        origin,
        ((one + s) / two, y),
        ((one - s) / two, y),
        unit,
    )
    palette = [caps[1], caps[2]]
    for left, right in zip(caps, caps[1:]):
        delta = point_sub(right, left)
        midpoint = point_scale(point_add(left, right), one / two)
        offset = (-delta[1] * s / six, delta[0] * s / six)
        palette.extend((point_add(midpoint, offset), point_sub(midpoint, offset)))
    multiplier = (-s / two, -one / two)
    translation = (zero, one)
    moved_palette = [
        point_add(translation, complex_mul(multiplier, point_sub(p, caps[1])))
        for p in palette
    ]
    g19 = moser + moved_palette
    need(len(g19) == len(set(g19)) == 19, "G19 collision")

    # Native F29 has (a+b*sqrt(33) + i(c*sqrt(3)+d*sqrt(11)))/12;
    # the reviewed frame translates every point by +i.
    f29 = []
    for a, b, c, d in parse_f29_rows(source_dir / "f29_points.tsv"):
        real = (field.convert(a) + field.convert(b) * s * t) / twelve
        imag = one + (field.convert(c) * s + field.convert(d) * t) / twelve
        f29.append((real, imag))
    need(len(f29) == len(set(f29)) == 29, "F29 collision")

    raw = g19 + f29
    points = []
    raw_map = []
    for point in raw:
        if point not in points:
            points.append(point)
        raw_map.append(points.index(point))
    f29_map = raw_map[19:]
    shared = tuple((i, vertex) for i, vertex in enumerate(f29_map) if vertex < 19)
    need(len(raw) == 48 and len(points) == 45, "merged point count")
    need(raw_map[:19] == list(range(19)), "G19 labels changed")
    need(shared == SHARED, "shared-point identities")
    need(certificate["f29_map"] == f29_map, "F29 merge map")
    need(certificate["shared_vertices"] == [list(pair) for pair in SHARED], "shared rows")

    basis = (one, s, t, s * t, y, s * y, t * y, s * t * y)
    submitted_points = parse_certificate_points(certificate["coordinates"], basis, field)
    need(submitted_points == points, "submitted coordinates differ from reconstructed formulas")

    def exact_edges(vertices):
        edges = []
        for a, b in combinations(range(len(vertices)), 2):
            distance = squared_norm(point_sub(vertices[a], vertices[b]))
            need(distance != zero, "unmerged coordinate collision")
            if distance == one:
                edges.append((a, b))
        return edges

    g19_edges = exact_edges(g19)
    f29_edges = exact_edges(f29)
    edges = exact_edges(points)
    need(len(g19_edges) == 34, "G19 edge count")
    need(len(f29_edges) == 75, "F29 edge count")
    need(len(edges) == 107, "union edge count")
    need(certificate["f29_edges"] == [list(edge) for edge in f29_edges], "F29 edge list")
    need(certificate["edges"] == [list(edge) for edge in edges], "complete union edge list")

    inherited = sorted(
        set(g19_edges)
        | {tuple(sorted((f29_map[a], f29_map[b]))) for a, b in f29_edges}
    )
    extra = sorted(set(edges) - set(inherited))
    need(len(inherited) == 34 + 75 - 3 == 106, "inherited-edge accounting")
    need(inherited == [tuple(edge) for edge in certificate["inherited_edges"]], "inherited edge list")
    need(extra == [(7, 40)], "extra-contact census")
    need(certificate["new_edges"] == [[7, 40]], "submitted extra contact")
    need(f29_map[22] == 40, "F29 contact label")
    need({(11, 15), (11, 16), (15, 16)} <= set(g19_edges), "shared triangle")

    # Source-integrity checks are semantic as well as digest based.
    source_g19 = json.loads((source_dir / "source_g19.json").read_text())
    upstream_g19 = json.loads((G19_SOURCE / "certificate.json").read_text())
    for key in ("coordinates", "edges", "inherited_edges", "new_edges"):
        need(source_g19[key] == upstream_g19[key], "G19 source field mismatch: " + key)
    need(parse_certificate_points(source_g19["coordinates"], basis, field) == g19, "G19 source coordinates")
    need(source_g19["edges"] == [list(edge) for edge in g19_edges], "G19 source edges")
    need((source_dir / "f29_points.tsv").read_bytes() == (F29_SOURCE / "points.tsv").read_bytes(),
         "F29 source table is not byte-identical")

    return Geometry(g19, f29, points, g19_edges, f29_edges, inherited, edges, f29_map, 8)


def check_word(word, colours: int, edges: list[tuple[int, int]], vertices: int) -> None:
    need(len(word) == vertices, "colour-word length")
    need(all(type(c) is int and 0 <= c < colours for c in word), "colour-word domain")
    need(all(word[a] != word[b] for a, b in edges), "improper colour word")


def enumerate_colourings(
    vertices: int,
    edges: list[tuple[int, int]],
    colours: int,
    pins: tuple[tuple[int, int], ...] = (),
    probe: int | None = None,
) -> dict:
    """Count labeled proper colourings with deterministic dynamic MRV."""

    adjacency = [set() for _ in range(vertices)]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    word = [-1] * vertices
    for vertex, colour in pins:
        need(0 <= vertex < vertices and 0 <= colour < colours, "pin domain")
        need(word[vertex] in (-1, colour), "inconsistent pins")
        word[vertex] = colour
    if any(word[a] >= 0 and word[a] == word[b] for a, b in edges):
        return {"total": 0, "by_probe_colour": [0] * colours, "search_nodes": 0}

    counts = [0] * colours
    total = 0
    search_nodes = 0

    def rec() -> None:
        nonlocal total, search_nodes
        search_nodes += 1
        free = [vertex for vertex, colour in enumerate(word) if colour < 0]
        if not free:
            total += 1
            if probe is not None:
                counts[word[probe]] += 1
            return
        domains = {
            vertex: tuple(
                colour
                for colour in range(colours)
                if all(word[neighbour] != colour for neighbour in adjacency[vertex])
            )
            for vertex in free
        }
        vertex = min(free, key=lambda v: (len(domains[v]), -len(adjacency[v]), v))
        if not domains[vertex]:
            return
        for colour in domains[vertex]:
            word[vertex] = colour
            rec()
        word[vertex] = -1

    rec()
    return {"total": total, "by_probe_colour": counts, "search_nodes": search_nodes}


def review(source_dir: Path) -> dict:
    certificate_path = source_dir / "certificate.json"
    certificate = json.loads(certificate_path.read_text())
    geometry = reconstruct_geometry(certificate, source_dir)

    check_word(certificate["four_colouring"], 4, geometry.edges, 45)
    check_word(certificate["five_colouring"], 5, geometry.edges, 45)
    need(set(certificate["five_colouring"]) == set(range(5)), "five-colour word does not use all colours")
    extension_words = [tuple(word) for word in certificate["f29_extension_words"]]
    need(len(extension_words) == 2, "extension-library size")
    for word in extension_words:
        check_word(word, 4, geometry.f29_edges, 29)
        need(tuple(word[v] for v, _colour in F29_PINS) == (0, 1, 2), "extension overlap colours")
    need(sum(a != b for a, b in zip(*extension_words)) == 1, "extension words do not differ once")
    need(tuple(word[22] for word in extension_words) == (1, 3), "extension contact colours")

    # Enumerate the complete two boundary marginals independently of the two
    # submitted witnesses.  These counts are labeled after normalizing the
    # shared triangle to (0,1,2).
    g19_boundary = enumerate_colourings(19, geometry.g19_edges, 4, G19_PINS, 7)
    f29_boundary = enumerate_colourings(29, geometry.f29_edges, 4, F29_PINS, 22)
    need(g19_boundary["total"] == 163584, "G19 normalized count changed")
    need(g19_boundary["by_probe_colour"] == [49536, 25920, 50688, 37440], "G19 boundary distribution")
    need(f29_boundary["total"] == 207309, "F29 normalized count changed")
    need(f29_boundary["by_probe_colour"] == [0, 102261, 0, 105048], "F29 boundary distribution")

    compatibility = []
    compatible_normalized = 0
    conflicting_normalized = 0
    for old_colour in range(4):
        row = []
        for new_colour in range(4):
            pairs = (
                g19_boundary["by_probe_colour"][old_colour]
                * f29_boundary["by_probe_colour"][new_colour]
            )
            if old_colour == new_colour:
                conflicting_normalized += pairs
                row.append(0)
            else:
                compatible_normalized += pairs
                row.append(pairs)
        compatibility.append(row)
    all_pairs = g19_boundary["total"] * f29_boundary["total"]
    need(compatible_normalized + conflicting_normalized == all_pairs, "gluing decomposition")
    need(compatible_normalized == 27328833216, "compatible normalized gluing count")
    need(conflicting_normalized == 6583602240, "conflicting normalized pair count")
    named_colourings = compatible_normalized * math.perm(4, 3)
    need(named_colourings == 655891997184, "named gluing count")

    # G19's contact vertex realizes all four normalized colours.  A single
    # static F29 word necessarily conflicts with one of them.  The submitted
    # words attain both possible F29 contact colours, so two is minimal.
    need(all(g19_boundary["by_probe_colour"]), "G19 contact does not realize all colours")
    possible_f29 = [i for i, count in enumerate(f29_boundary["by_probe_colour"]) if count]
    need(possible_f29 == [1, 3], "F29 contact-colour set")
    need(set(word[22] for word in extension_words) == set(possible_f29), "library misses a contact colour")
    for old_colour in range(4):
        need(any(word[22] != old_colour for word in extension_words), "uncovered G19 contact colour")

    # Independent four-chromatic lower bound: the first seven G19 vertices are
    # the 11-edge Moser spindle and have no proper three-colouring.
    moser7_edges = [edge for edge in geometry.g19_edges if edge[1] < 7]
    need(len(moser7_edges) == 11, "Moser-spindle edge count")
    moser3 = enumerate_colourings(7, moser7_edges, 3)
    need(moser3["total"] == 0, "Moser spindle unexpectedly three-colourable")

    return {
        "status": "ACCEPTED_FIXED_ATTACHMENT_INDEPENDENTLY",
        "reviewed_source_commit": SOURCE_COMMIT,
        "source_certificate_sha256": file_digest(certificate_path),
        "source_integrity": {
            "g19_source_fields_match_upstream": True,
            "g19_source_sha256": file_digest(source_dir / "source_g19.json"),
            "f29_points_byte_identical_to_upstream": True,
            "f29_points_sha256": file_digest(source_dir / "f29_points.tsv"),
        },
        "geometry": {
            "field_degree": geometry.field_degree,
            "raw_labels": 48,
            "distinct_points": len(geometry.points),
            "all_pairs_checked": 990,
            "g19_edges": len(geometry.g19_edges),
            "f29_edges": len(geometry.f29_edges),
            "shared_triangle_edges_counted_twice": 3,
            "inherited_edges": len(geometry.inherited_edges),
            "strict_unit_edges": len(geometry.edges),
            "shared_vertices_f29_to_g19": [list(pair) for pair in SHARED],
            "extra_edges": [[7, 40]],
            "coordinate_sha256": json_digest(certificate["coordinates"]),
            "edge_sha256": json_digest(certificate["edges"]),
        },
        "chromatic": {
            "chromatic_number": 4,
            "moser_spindle_three_colourings": moser3["total"],
            "proper_four_witness_checked": True,
            "proper_all_five_witness_checked": True,
        },
        "normalized_boundary_census": {
            "shared_triangle_colours": [0, 1, 2],
            "g19_contact_vertex": 7,
            "g19": g19_boundary,
            "f29_contact_vertex": 22,
            "f29": f29_boundary,
            "f29_possible_contact_colours": possible_f29,
        },
        "universal_extension": {
            "all_g19_four_colourings_extend": True,
            "all_relations_projected_on_g19_are_unchanged": True,
            "submitted_extension_words_checked": True,
            "submitted_words_differ_only_at_f29_vertex_22": True,
            "minimum_static_extension_library_size": 2,
            "compatibility_matrix_g19_rows_f29_columns": compatibility,
            "all_normalized_component_pairs": all_pairs,
            "conflicting_normalized_pairs": conflicting_normalized,
            "compatible_normalized_gluings": compatible_normalized,
            "named_union_four_colourings": named_colourings,
        },
        "scope": {
            "fixed_translation_only": True,
            "other_f29_placements_classified": False,
            "abstract_graph_only": False,
            "plane_unit_distance_realization_checked": True,
            "ordinary_nonfour_signal": False,
            "five_chromatic_construction": False,
            "record_candidate": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = review(args.source_dir.resolve())
    if args.check_expected:
        need(result == json.loads((HERE / "EXPECTED.json").read_text()), "review expected output mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
