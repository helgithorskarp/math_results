#!/usr/bin/env python3
"""Clean-room review of the P36 cyclic quarter-turn collar theorem.

This checker imports no code from the target package.  It uses exact integer
coefficients for Q(sqrt(3))/4, enumerates all raw anchor pairs, finds fresh
four-colourings by a generic DSATUR search, transports them through explicit
dihedral isometries, and checks the transported word on every raw graph.

The target's positive-word file is audited separately and is not a premise of
the fresh-colouring route.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_TARGET = HERE.parent / "hadwiger_nelson_p36_quarter_turn_collars"

# (r, s, u, v) represents ((r+s*sqrt(3))/4, (u+v*sqrt(3))/4).
Point = tuple[int, int, int, int]
Edge = tuple[int, int]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def add(x: Point, y: Point) -> Point:
    return (x[0] + y[0], x[1] + y[1], x[2] + y[2], x[3] + y[3])


def neg(x: Point) -> Point:
    return (-x[0], -x[1], -x[2], -x[3])


def sub(x: Point, y: Point) -> Point:
    return add(x, neg(y))


def multiply_i(x: Point) -> Point:
    return (-x[2], -x[3], x[0], x[1])


def rotate_quarters(x: Point, turns: int) -> Point:
    for _ in range(turns % 4):
        x = multiply_i(x)
    return x


def conjugate(x: Point) -> Point:
    return (x[0], x[1], -x[2], -x[3])


def divide_two(x: Point) -> Point:
    require(all(value % 2 == 0 for value in x), "unexpected half coefficient")
    return tuple(value // 2 for value in x)  # type: ignore[return-value]


def multiply_omega(x: Point) -> Point:
    """Multiply by omega=(1+i*sqrt(3))/2 in coefficient form."""
    r, s, u, v = x
    return divide_two((r - 3 * v, s - u, 3 * s + u, r + v))


def apply_dihedral(x: Point, reflected: bool, sixth_turns: int) -> Point:
    if reflected:
        x = conjugate(x)
    for _ in range(sixth_turns % 6):
        x = multiply_omega(x)
    return x


def dihedral_images(x: Point) -> list[tuple[Point, bool, int]]:
    return [
        (apply_dihedral(x, reflected, turns), reflected, turns)
        for reflected in (False, True)
        for turns in range(6)
    ]


def patch_points() -> tuple[list[tuple[int, int]], list[Point]]:
    rows: list[tuple[Point, tuple[int, int]]] = []
    # The quadratic form is positive definite.  |a|,|b| <= 12 is a generous
    # definition-level box for a^2+ab+b^2 <= 36.
    for a in range(-12, 13):
        for b in range(-12, 13):
            if a * a + a * b + b * b <= 36:
                rows.append(((4 * a + 2 * b, 0, 0, 2 * b), (a, b)))
    rows.sort()
    return [label for _, label in rows], [point for point, _ in rows]


def squared_norm_coefficients(x: Point) -> tuple[int, int]:
    """Return (A,B) such that 16 |x|^2 = A+B*sqrt(3)."""
    r, s, u, v = x
    return (r * r + 3 * s * s + u * u + 3 * v * v,
            2 * (r * s + u * v))


def undirected_unit_steps() -> tuple[Point, ...]:
    # If |x|=1, rational-basis independence gives A=16 and B=0.
    # A is a sum of nonnegative squares, so these bounds are exhaustive.
    all_steps = []
    for r in range(-4, 5):
        for s in range(-2, 3):
            for u in range(-4, 5):
                for v in range(-2, 3):
                    x = (r, s, u, v)
                    if squared_norm_coefficients(x) == (16, 0):
                        all_steps.append(x)
    require(len(all_steps) == 12, "the exact unit-vector census is not twelve")
    step_set = set(all_steps)
    require(all(neg(x) in step_set for x in all_steps),
            "unit-vector census is not centrally symmetric")
    return tuple(sorted(x for x in all_steps if x > neg(x)))


def anchor_center(p: Point, q: Point) -> Point:
    # c=(p-iq)/(1-i)=(p+q+i(p-q))/2.
    return divide_two(add(add(p, q), multiply_i(sub(p, q))))


def physical_graph(center: Point, patch: list[Point], steps: tuple[Point, ...]):
    occurrences: dict[Point, list[tuple[int, int]]] = defaultdict(list)
    for layer in range(4):
        for local_index, source in enumerate(patch):
            image = add(center, rotate_quarters(sub(source, center), layer))
            occurrences[image].append((layer, local_index))
    points = sorted(occurrences)
    index = {point: position for position, point in enumerate(points)}
    edges: list[Edge] = []
    for point_position, point in enumerate(points):
        for step in steps:
            other = index.get(add(point, step))
            if other is not None:
                edges.append((min(point_position, other), max(point_position, other)))
    require(len(edges) == len(set(edges)), "duplicate undirected edge generated")
    edges.sort()
    return points, edges, occurrences


def pairwise_edges(points: list[Point]) -> list[Edge]:
    answer = []
    for first, point in enumerate(points):
        for second in range(first + 1, len(points)):
            if squared_norm_coefficients(sub(point, points[second])) == (16, 0):
                answer.append((first, second))
    return answer


def proper(word: list[int], edges: list[Edge]) -> bool:
    return (all(colour in range(4) for colour in word)
            and all(word[x] != word[y] for x, y in edges))


def find_triangle(adjacency: list[set[int]], edges: list[Edge]) -> tuple[int, int, int]:
    for x, y in edges:
        common = adjacency[x].intersection(adjacency[y])
        if common:
            return (x, y, min(common))
    raise ValueError("the collar graph unexpectedly has no triangle")


def fresh_four_colouring(vertices: int, edges: list[Edge]) -> tuple[list[int], int, int]:
    """Find one positive word with a deterministic generic DSATUR search."""
    adjacency = [set() for _ in range(vertices)]
    for x, y in edges:
        adjacency[x].add(y)
        adjacency[y].add(x)
    colours = [-1] * vertices
    forbidden = [0] * vertices
    nodes = 0
    backtracks = 0

    def place(vertex: int, colour: int):
        bit = 1 << colour
        if forbidden[vertex] & bit:
            return None
        changes: list[tuple[int, int]] = []
        colours[vertex] = colour
        for neighbour in adjacency[vertex]:
            if colours[neighbour] == colour:
                for changed, old in reversed(changes):
                    forbidden[changed] = old
                colours[vertex] = -1
                return None
            if colours[neighbour] < 0:
                old = forbidden[neighbour]
                new = old | bit
                if new != old:
                    changes.append((neighbour, old))
                    forbidden[neighbour] = new
                    if new == 15:
                        for changed, previous in reversed(changes):
                            forbidden[changed] = previous
                        colours[vertex] = -1
                        return None
        return changes

    def remove(vertex: int, changes: list[tuple[int, int]]) -> None:
        for changed, old in reversed(changes):
            forbidden[changed] = old
        colours[vertex] = -1

    # A triangle uses three distinct colours in every proper colouring, so
    # fixing its names removes only global colour symmetry.
    triangle = find_triangle(adjacency, edges)
    seeds: list[tuple[int, list[tuple[int, int]]]] = []
    for colour, vertex in enumerate(triangle):
        changes = place(vertex, colour)
        require(changes is not None, "failed to seed a proper triangle")
        seeds.append((vertex, changes))

    sys.setrecursionlimit(max(2000, vertices + 100))

    def visit(uncoloured: int) -> bool:
        nonlocal nodes, backtracks
        nodes += 1
        if uncoloured == 0:
            return True
        pending = (vertex for vertex in range(vertices) if colours[vertex] < 0)
        vertex = max(
            pending,
            key=lambda item: (forbidden[item].bit_count(),
                              len(adjacency[item]), -item),
        )
        available = 15 & ~forbidden[vertex]
        for colour in range(4):
            if available & (1 << colour):
                changes = place(vertex, colour)
                if changes is not None:
                    if visit(uncoloured - 1):
                        return True
                    remove(vertex, changes)
                    backtracks += 1
        return False

    require(visit(vertices - 3), "generic search found no four-colouring")
    answer = colours.copy()
    require(proper(answer, edges), "generic search returned an invalid word")
    return answer, nodes, backtracks


def graph_stream_update(digest, representative: Point,
                        points: list[Point], edges: list[Edge]) -> None:
    # This exactly matches the target's representative graph-stream format,
    # providing an integrity comparison while the reconstruction code differs.
    payload = [list(representative), [list(point) for point in points],
               [list(edge) for edge in edges]]
    digest.update(json.dumps(payload, separators=(",", ":")).encode())
    digest.update(b"\n")


def raw_stream_update(digest, representative: Point, center: Point,
                      points: list[Point], edges: list[Edge], word: list[int]) -> None:
    inner = hashlib.sha256()
    inner.update(b"p36-quarter-turn-review-raw-graph-v1\0")
    for point in points:
        inner.update(struct.pack(">4i", *point))
    inner.update(b"\xff")
    for edge in edges:
        inner.update(struct.pack(">2H", *edge))
    row = [list(representative), list(center), len(points), len(edges),
           inner.hexdigest(), "".join(map(str, word))]
    digest.update(json.dumps(row, separators=(",", ":")).encode())
    digest.update(b"\n")


def audit(target_dir: Path, representative_limit: int | None = None) -> dict[str, object]:
    labels, patch = patch_points()
    require(len(labels) == len(patch) == 127, "P36 does not have 127 points")
    require(len(set(patch)) == 127, "P36 construction contains duplicates")
    steps = undirected_unit_steps()
    require(len(steps) == 6, "the undirected unit-step census is not six")
    patch_index = {point: position for position, point in enumerate(patch)}
    patch_edges = []
    for position, point in enumerate(patch):
        for step in steps:
            other = patch_index.get(add(point, step))
            if other is not None:
                patch_edges.append((min(position, other), max(position, other)))
    patch_edges = sorted(set(patch_edges))
    require(len(patch_edges) == 342, "P36 does not have 342 unit edges")

    members: dict[Point, list[tuple[Point, int, int]]] = defaultdict(list)
    centers = []
    diagonal_centers = set()
    for p_index, p in enumerate(patch):
        for q_index, q in enumerate(patch):
            center = anchor_center(p, q)
            centers.append(center)
            if p_index == q_index:
                diagonal_centers.add(center)
            images = dihedral_images(center)
            representative = min(image for image, _, _ in images)
            members[representative].append((center, p_index, q_index))
    require(len(centers) == 127 * 127, "anchor-pair enumeration is incomplete")
    require(len(set(centers)) == len(centers), "anchor centers are not injective")
    require(diagonal_centers == set(patch), "diagonal centers are not exactly P36")
    require(set(members).issubset(set(centers)),
            "a dihedral representative left the center family")

    all_representatives = sorted(members)
    if representative_limit is not None:
        require(representative_limit > 0, "representative limit must be positive")
        representatives = all_representatives[:representative_limit]
    else:
        representatives = all_representatives

    certificate_bytes = (target_dir / "colourings.json").read_bytes()
    certificate_payload = json.loads(certificate_bytes)
    require(certificate_payload.get("schema") ==
            "p36-quarter-turn-collar-positive-colourings-v1",
            "target certificate has an unexpected schema")
    stored = {}
    for row in certificate_payload.get("certificates", []):
        center = tuple(row["center"])
        require(center not in stored, "duplicate target certificate center")
        stored[center] = row

    orbit_histogram = Counter()
    edge_histogram = Counter()
    total_search_nodes = 0
    maximum_search_nodes = 0
    total_search_backtracks = 0
    stored_words_checked = 0
    empty_placements = 0
    common_placements = 0
    extra_contact_placements = 0
    extra_contact_orbits = 0
    raw_transports = 0
    pairwise_graph_audits = 0
    representative_graph_digest = hashlib.sha256()
    fresh_cover_digest = hashlib.sha256()
    raw_coverage_digest = hashlib.sha256()
    corrupted_word_rejected = False

    for representative in representatives:
        row_members = sorted(members[representative])
        orbit_histogram[len(row_members)] += 1
        points, edges, occurrences = physical_graph(representative, patch, steps)
        graph_stream_update(representative_graph_digest, representative, points, edges)
        index = {point: position for position, point in enumerate(points)}

        fourfold = sum(len(rows) == 4 for rows in occurrences.values())
        is_common = fourfold > 0
        if (len(edges) > 4 * len(patch_edges)) or is_common:
            require(pairwise_edges(points) == edges,
                    "definition-level pair audit disagrees with step lookup")
            pairwise_graph_audits += 1

        word, nodes, backtracks = fresh_four_colouring(len(points), edges)
        total_search_nodes += nodes
        maximum_search_nodes = max(maximum_search_nodes, nodes)
        total_search_backtracks += backtracks
        fresh_cover_digest.update(json.dumps(
            [list(representative), "".join(map(str, word))],
            separators=(",", ":")).encode())
        fresh_cover_digest.update(b"\n")

        stored_row = stored.get(representative)
        if stored_row is not None:
            stored_word = [int(value) for value in stored_row["word"]]
            require(len(stored_word) == len(points),
                    "stored certificate has the wrong word length")
            require(stored_row["vertices"] == len(points),
                    "stored certificate has the wrong vertex count")
            require(stored_row["edges"] == len(edges),
                    "stored certificate has the wrong edge count")
            require(proper(stored_word, edges), "stored positive word is invalid")
            stored_words_checked += 1
            if not corrupted_word_rejected:
                corrupted = stored_word.copy()
                x, y = edges[0]
                corrupted[x] = corrupted[y]
                corrupted_word_rejected = not proper(corrupted, edges)

        representative_index = index
        for center, p_index, q_index in row_members:
            transform = next(
                (reflected, turns)
                for image, reflected, turns in dihedral_images(center)
                if image == representative
            )
            raw_points, raw_edges, raw_occurrences = physical_graph(center, patch, steps)
            reflected, turns = transform
            mapped = [apply_dihedral(point, reflected, turns)
                      for point in raw_points]
            require(set(mapped) == set(points) and len(mapped) == len(points),
                    "raw collar does not map bijectively to its representative")
            raw_word = [word[representative_index[image]] for image in mapped]
            require(proper(raw_word, raw_edges),
                    "transported fresh word fails on a raw physical graph")
            raw_transports += 1

            raw_fourfold = sum(len(rows) == 4 for rows in raw_occurrences.values())
            if p_index != q_index:
                require(len(raw_points) == 504,
                        "off-diagonal collar does not have 504 physical points")
                require(raw_fourfold == 0,
                        "off-diagonal collar has a fourfold common point")
                multiplicities = Counter(map(len, raw_occurrences.values()))
                require(multiplicities == Counter({1: 500, 2: 4}),
                        "off-diagonal collision pattern is not 500 singles plus four pairs")
                empty_placements += 1
                edge_histogram[len(raw_edges)] += 1
                if len(raw_edges) > 4 * len(patch_edges):
                    extra_contact_placements += 1
            else:
                require(raw_fourfold == 1,
                        "diagonal collar does not have exactly one common point")
                common_placements += 1
            raw_stream_update(raw_coverage_digest, representative, center,
                              raw_points, raw_edges, raw_word)

        if not is_common and len(edges) > 4 * len(patch_edges):
            extra_contact_orbits += 1

    full_run = representative_limit is None
    if full_run:
        require(len(representatives) == 1408, "dihedral orbit count is not 1,408")
        require(orbit_histogram == Counter({12: 1281, 6: 126, 1: 1}),
                "dihedral orbit-size histogram changed")
        require(empty_placements == 16002, "empty-intersection count changed")
        require(common_placements == 127, "common-point count changed")
        require(raw_transports == 16129, "not every raw collar was checked")
        require(stored_words_checked == len(stored) == 611,
                "target positive-word cover was not audited exactly once")
        require(extra_contact_placements == 660,
                "extra-contact placement count changed")
        require(extra_contact_orbits == 58,
                "extra-contact orbit count changed")
        require(min(edge_histogram) == 1368 and max(edge_histogram) == 1592,
                "empty-collar edge range changed")
        require(pairwise_graph_audits >= 58,
                "the interacting representatives missed the pairwise audit")
        require(corrupted_word_rejected, "corrupted target word was accepted")

    result = {
        "status": "PASS" if full_run else "SMOKE_PASS",
        "coordinate_model": "Q(sqrt(3))/4 coefficient pairs",
        "patch_vertices": len(patch),
        "patch_edges": len(patch_edges),
        "undirected_unit_steps": len(steps),
        "ordered_anchor_pairs": len(centers),
        "distinct_anchor_centers": len(set(centers)),
        "dihedral_representatives_checked": len(representatives),
        "orbit_size_histogram": sorted([size, count]
                                       for size, count in orbit_histogram.items()),
        "fresh_dsat_colours_checked": len(representatives),
        "fresh_dsat_total_nodes": total_search_nodes,
        "fresh_dsat_maximum_nodes": maximum_search_nodes,
        "fresh_dsat_total_backtracks": total_search_backtracks,
        "raw_transported_colours_checked": raw_transports,
        "stored_positive_words_checked": stored_words_checked,
        "definition_level_pairwise_graph_audits": pairwise_graph_audits,
        "empty_intersection_placements": empty_placements,
        "common_point_placements": common_placements,
        "empty_extra_contact_placements": extra_contact_placements,
        "empty_extra_contact_orbits": extra_contact_orbits,
        "minimum_empty_edges": min(edge_histogram) if edge_histogram else None,
        "maximum_empty_edges": max(edge_histogram) if edge_histogram else None,
        "corrupted_word_rejected": corrupted_word_rejected,
        "target_certificate_sha256": hashlib.sha256(certificate_bytes).hexdigest(),
        "representative_graph_stream_sha256": representative_graph_digest.hexdigest(),
        "fresh_representative_colour_cover_sha256": fresh_cover_digest.hexdigest(),
        "raw_graph_and_transport_cover_sha256": raw_coverage_digest.hexdigest(),
    }
    if full_run:
        require(result["target_certificate_sha256"] ==
                "aaa9a6813981c01d69e4ca278a6e882dbee0de6d27b30b57f8a567662e1a8221",
                "target certificate bytes changed")
        require(result["representative_graph_stream_sha256"] ==
                "17a1dcfc78e3fb9069ed9deaff70a7cedd0916a0cece473eb8b558dc3d075b46",
                "independent graph stream differs from the target")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-dir", type=Path, default=DEFAULT_TARGET)
    parser.add_argument("--representative-limit", type=int)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = audit(args.target_dir, args.representative_limit)
    if args.check_expected:
        require(args.representative_limit is None,
                "expected output applies only to a full run")
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        require(result == expected, "output differs from EXPECTED.json")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
