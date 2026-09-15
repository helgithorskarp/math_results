#!/usr/bin/env python3
"""Independent exact review of the five T375 marked-triangle D3 self-gluings.

No submitted module is imported.  The source orbit is rebuilt by group
closure, the finite unit-direction set by a complete coefficient-box scan,
and every graph by translated-neighbour lookup rather than pairwise distance
tests.  A separate assignment-based DSATUR search checks the crucial marked-
triangle obstruction without using the source's domain-propagation routine.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter, deque
from dataclasses import dataclass
from itertools import permutations
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_REPOSITORY = HERE.parent
SOURCE_NAME = "hadwiger_nelson_small_triangle_forcer375"
TARGET_NAME = "hadwiger_nelson_t375_d3_selfglue_closure"
SOURCE_COMMIT = "f88d7ee5b1d0b5c640750dc287bda159b8775423"
TARGET_COMMIT = "fb5f760378654f5a8184bae7ed5b3732b593a638"
SOURCE_HASHES = {
    "appendix.json": "dd74c3ef0bb3e9cc1c9c32f7ecc703c1d85cacaca6fca97834d162e8c05997fa",
    "certificate.json": "282fd209157b0c327e02451c32a3d2f2dbb40c4ec31e6531bdd3b8316854b28e",
    "colour_check.py": "c5ffcb2c0a0ff93a6ee06364e307648933274b6df4cbcc6f990e5ddc35294e1a",
    "geometry.py": "921fa358c620ed86bd11c6fc9f97ae03ddb491da94612f086cd165a94ffc77bd",
}
TARGET_CERTIFICATE_SHA256 = "97f4c136a4bfa5c4411cde367a9261b24082510f1c0b7f65d4b4052e8591ce93"
TERMINAL_POINTS = ((0, 0, 12, 0), (-6, 0, -6, 0), (6, 0, -6, 0))
NONMONO_PATTERNS = ("001", "010", "011", "012")
ACTIONS = ((1, False), (2, False), (0, True), (1, True), (2, True))
MOSER_PATTERN_EDGES = (
    (0, 1), (0, 2), (0, 4), (0, 5), (1, 2), (1, 3),
    (2, 3), (3, 6), (4, 5), (4, 6), (5, 6),
)
MOSER_T375_VERTICES = (62, 2, 65, 240, 57, 202, 197)


class ReviewFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ReviewFailure(message)


def read_json(path: Path):
    return json.loads(path.read_text())


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def object_digest(value) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def add(left, right):
    return tuple(a + b for a, b in zip(left, right))


def negate(point):
    return tuple(-value for value in point)


def rotate_120(point):
    a, b, c, d = point
    doubled = (-a - c, -b - 3 * d, 3 * a - c, b - d)
    need(all(value % 2 == 0 for value in doubled), "rotation left the integer lattice")
    return tuple(value // 2 for value in doubled)


def reflect_y_axis(point):
    a, b, c, d = point
    return -a, -b, c, d


def transform(point, rotation: int, reflected_first: bool):
    result = reflect_y_axis(point) if reflected_first else point
    for _ in range(rotation):
        result = rotate_120(result)
    return result


def symmetry_orbit(seed):
    """Close under the two generators rather than assuming a six-row orbit."""

    seen = {seed}
    queue = deque([seed])
    while queue:
        point = queue.popleft()
        for image in (rotate_120(point), reflect_y_axis(point)):
            if image not in seen:
                seen.add(image)
                queue.append(image)
    return seen


def squared_distance_coefficients(delta):
    """Return numerator coefficients of 1 and sqrt(33), denominator 1296."""

    a, b, c, d = delta
    return 3 * a * a + 11 * b * b + c * c + 33 * d * d, 2 * (a * b + c * d)


def is_unit_direction(delta) -> bool:
    return squared_distance_coefficients(delta) == (1296, 0)


def enumerate_unit_directions():
    """Scan the complete box forced by the positive rational coefficient."""

    bounds = (
        math.isqrt(1296 // 3),
        math.isqrt(1296 // 11),
        math.isqrt(1296),
        math.isqrt(1296 // 33),
    )
    directions = []
    tested = 0
    for a in range(-bounds[0], bounds[0] + 1):
        for b in range(-bounds[1], bounds[1] + 1):
            for c in range(-bounds[2], bounds[2] + 1):
                for d in range(-bounds[3], bounds[3] + 1):
                    tested += 1
                    delta = (a, b, c, d)
                    if is_unit_direction(delta):
                        directions.append(delta)
    directions.sort()
    need(tested == 817089, "unit-direction box size")
    need(len(directions) == len(set(directions)) == 54, "unit-direction count")
    need(set(map(negate, directions)) == set(directions), "direction negation closure")
    return directions, tested


def edges_by_directions(points, directions):
    """Generate the complete unit graph using the exhaustive direction set."""

    need(len(points) == len(set(points)), "duplicate physical point")
    index = {point: vertex for vertex, point in enumerate(points)}
    edges = set()
    for left, point in enumerate(points):
        for direction in directions:
            right = index.get(add(point, direction))
            if right is not None and left < right:
                edges.add((left, right))
    result = sorted(edges)
    need(all(is_unit_direction(tuple(points[b][i] - points[a][i] for i in range(4)))
             for a, b in result), "nonunit generated edge")
    return result


@dataclass
class SourceGraph:
    points: list[tuple[int, int, int, int]]
    edges: list[tuple[int, int]]
    reference_points: list[tuple[int, int, int, int]]
    reference_edges: list[tuple[int, int]]
    certificate: dict
    orbit_size_histogram: Counter


@dataclass
class CaseGraph:
    rotation: int
    reflected: bool
    terminal_permutation: tuple[int, int, int]
    points: list[tuple[int, int, int, int]]
    edges: list[tuple[int, int]]
    inherited_edges: list[tuple[int, int]]
    incidental_edges: list[tuple[int, int]]
    moved_map: list[int]


def reconstruct_source(source_dir: Path, directions) -> SourceGraph:
    for name, expected in SOURCE_HASHES.items():
        need(file_digest(source_dir / name) == expected, "changed source dependency: " + name)
    appendix = read_json(source_dir / "appendix.json")
    need(type(appendix) is list and len(appendix) == 109, "appendix row count")
    need(all(type(row) is list and len(row) == 4 and all(type(x) is int for x in row)
             for row in appendix), "malformed appendix row")

    orbit = set()
    orbit_sizes = Counter()
    for row in appendix:
        local = symmetry_orbit(tuple(row))
        orbit_sizes[len(local)] += 1
        orbit.update(local)
    need(orbit_sizes == Counter({6: 100, 3: 9}), "source orbit-size histogram")
    need(len(orbit) == 627 and set(TERMINAL_POINTS) <= orbit, "reference orbit")
    reference = list(TERMINAL_POINTS) + sorted(orbit - set(TERMINAL_POINTS))
    reference_edges = edges_by_directions(reference, directions)
    need(len(reference_edges) == 2982, "reference edge count")

    certificate = read_json(source_dir / "certificate.json")
    retained = certificate.get("retained_reference_indices")
    need(type(retained) is list and len(retained) == 375, "retained-index count")
    need(retained == sorted(set(retained)) and retained[:3] == [0, 1, 2],
         "retained-index normalization")
    need(all(type(i) is int and 0 <= i < 627 for i in retained), "retained-index domain")
    points = [reference[i] for i in retained]
    edges = edges_by_directions(points, directions)
    need(len(edges) == 1661, "T375 edge count")
    need(certificate.get("vertices") == 375 and certificate.get("edges") == 1661,
         "source inventory fields")
    need(certificate.get("terminals") == [0, 1, 2], "source terminal labels")
    need(certificate.get("terminal_distance_squared") == [1, 3], "terminal distance field")
    need(all(squared_distance_coefficients(tuple(points[b][i] - points[a][i]
                                                 for i in range(4))) == (432, 0)
             for a, b in ((0, 1), (0, 2), (1, 2))), "marked triangle geometry")
    need(object_digest(points) == certificate.get("point_sha256"), "source point hash")
    need(object_digest(edges) == certificate.get("edge_sha256"), "source edge hash")
    need(certificate.get("forcing_gate_reached") is True, "source forcing flag")
    need(certificate.get("target_found") is False, "source target flag")

    word = certificate.get("unpinned_colouring")
    check_word(word, len(points), edges)
    return SourceGraph(points, edges, reference, reference_edges, certificate, orbit_sizes)


def check_word(word, order: int, edges, pattern: str | None = None) -> None:
    need(type(word) is str and len(word) == order and set(word) <= set("0123"),
         "malformed four-colour word")
    if pattern is not None:
        need(word[:3] == pattern, "terminal pattern mismatch")
    need(all(word[a] != word[b] for a, b in edges), "monochromatic edge")


def solve_colouring(order: int, edges, colours: int, pins=()):
    """Assignment-based dynamic DSATUR with unused-colour symmetry only.

    Unlike the source checker, this routine keeps no propagated domain masks:
    it recomputes legal colours from the current assignment at every node.
    Trying one representative of all globally unused colours is complete
    because edge constraints and equal-colour pins distinguish no unused name.
    """

    adjacency = [set() for _ in range(order)]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    word = [-1] * order
    for vertex, colour in pins:
        need(0 <= vertex < order and 0 <= colour < colours, "pin domain")
        need(word[vertex] in (-1, colour), "inconsistent pins")
        word[vertex] = colour
    if any(word[a] >= 0 and word[a] == word[b] for a, b in edges):
        return None, {"nodes": 0, "dead_ends": 1}

    nodes = 0
    dead_ends = 0

    def rec():
        nonlocal nodes, dead_ends
        nodes += 1
        best_key = None
        best_vertex = None
        best_domain = None
        globally_used = {colour for colour in word if colour >= 0}
        for vertex in range(order):
            if word[vertex] >= 0:
                continue
            domain = tuple(
                colour for colour in range(colours)
                if all(word[neighbour] != colour for neighbour in adjacency[vertex])
            )
            if not domain:
                dead_ends += 1
                return None
            saturation = len({word[n] for n in adjacency[vertex] if word[n] >= 0})
            key = (len(domain), -saturation, -len(adjacency[vertex]), vertex)
            if best_key is None or key < best_key:
                best_key, best_vertex, best_domain = key, vertex, domain
        if best_vertex is None:
            return tuple(word)

        candidates = [colour for colour in best_domain if colour in globally_used]
        unused = [colour for colour in best_domain if colour not in globally_used]
        if unused:
            candidates.append(unused[0])
        for colour in candidates:
            word[best_vertex] = colour
            answer = rec()
            if answer is not None:
                return answer
        word[best_vertex] = -1
        return None

    answer = rec()
    return answer, {"nodes": nodes, "dead_ends": dead_ends}


def build_case(source: SourceGraph, directions, rotation: int, reflected: bool) -> CaseGraph:
    moved = [transform(point, rotation, reflected) for point in source.points]
    points = list(source.points)
    index = {point: vertex for vertex, point in enumerate(points)}
    moved_map = []
    for point in moved:
        if point not in index:
            index[point] = len(points)
            points.append(point)
        moved_map.append(index[point])
    terminal_permutation = tuple(TERMINAL_POINTS.index(transform(point, rotation, reflected))
                                 for point in TERMINAL_POINTS)
    need(set(moved_map[:3]) == {0, 1, 2}, "marked triangle not shared")
    inherited = set(source.edges)
    inherited.update(tuple(sorted((moved_map[a], moved_map[b]))) for a, b in source.edges)
    edges = edges_by_directions(points, directions)
    need(inherited <= set(edges), "inherited unit edge missing")
    incidental = sorted(set(edges) - inherited)
    return CaseGraph(rotation, reflected, terminal_permutation, points, edges,
                     sorted(inherited), incidental, moved_map)


def reconstruct_cases(source: SourceGraph, directions):
    all_actions = ((0, False),) + ACTIONS
    action_permutations = [
        tuple(TERMINAL_POINTS.index(transform(point, rotation, reflected))
              for point in TERMINAL_POINTS)
        for rotation, reflected in all_actions
    ]
    need(len(set(action_permutations)) == 6, "D3 action collision")
    need(set(action_permutations) == set(permutations(range(3))), "D3 action incompleteness")
    need(action_permutations[0] == (0, 1, 2), "D3 identity action")
    for rotation, reflected in all_actions:
        need({transform(direction, rotation, reflected) for direction in directions}
             == set(directions), "D3 action fails to preserve unit directions")
    return [build_case(source, directions, *action) for action in ACTIONS]


def validate_target(certificate: dict, cases: list[CaseGraph]) -> None:
    need(certificate.get("schema") == 1, "target schema")
    rows = certificate.get("cases")
    need(type(rows) is list and len(rows) == 5, "target case count")
    for row, case in zip(rows, cases):
        need(row.get("rotation_steps_120") == case.rotation, "case rotation")
        need(row.get("reflected_in_y_axis_first") is case.reflected, "case reflection")
        need(row.get("points") == len(case.points), "case point count")
        need(row.get("collisions_between_copies") == 750 - len(case.points), "case overlap count")
        need(row.get("edges") == len(case.edges), "case edge count")
        need(row.get("inherited_edge_union") == len(case.inherited_edges), "inherited count")
        need(row.get("point_sha256") == object_digest(case.points), "case point hash")
        need(row.get("edge_sha256") == object_digest(case.edges), "case edge hash")
        witnesses = row.get("terminal_witnesses")
        need(type(witnesses) is dict and tuple(sorted(witnesses)) == NONMONO_PATTERNS,
             "terminal witness keys")
        for pattern in NONMONO_PATTERNS:
            check_word(witnesses[pattern], len(case.points), case.edges, pattern)


def review(repository: Path) -> dict:
    source_dir = repository / SOURCE_NAME
    target_dir = repository / TARGET_NAME
    need(file_digest(target_dir / "certificate.json") == TARGET_CERTIFICATE_SHA256,
         "changed target certificate")
    directions, box_rows = enumerate_unit_directions()
    source = reconstruct_source(source_dir, directions)
    cases = reconstruct_cases(source, directions)
    target_certificate = read_json(target_dir / "certificate.json")
    validate_target(target_certificate, cases)

    monochromatic_answer, monochromatic_stats = solve_colouring(
        375, source.edges, 4, ((0, 0), (1, 0), (2, 0))
    )
    need(monochromatic_answer is None, "T375 admits a monochromatic marked triangle")
    need(monochromatic_stats == {"nodes": 21593, "dead_ends": 367},
         "independent monochromatic search trace changed")

    induced_moser = []
    source_edge_set = set(source.edges)
    for a in range(7):
        for b in range(a + 1, 7):
            if tuple(sorted((MOSER_T375_VERTICES[a], MOSER_T375_VERTICES[b]))) in source_edge_set:
                induced_moser.append((a, b))
    need(tuple(induced_moser) == MOSER_PATTERN_EDGES, "induced Moser spindle mismatch")
    moser_three_answer, moser_three_stats = solve_colouring(
        7, MOSER_PATTERN_EDGES, 3
    )
    need(moser_three_answer is None, "Moser spindle three-colouring")

    summaries = []
    total_pairs = 0
    for case in cases:
        pair_count = math.comb(len(case.points), 2)
        total_pairs += pair_count
        overlap = sum(vertex < 375 for vertex in case.moved_map)
        need(overlap == 750 - len(case.points), "overlap accounting")
        duplicated_edges = 2 * len(source.edges) - len(case.inherited_edges)
        summaries.append({
            "rotation_steps_120": case.rotation,
            "reflected_in_y_axis_first": case.reflected,
            "terminal_permutation": list(case.terminal_permutation),
            "points": len(case.points),
            "all_pairs_covered_by_direction_census": pair_count,
            "overlap_points": overlap,
            "complete_unit_edges": len(case.edges),
            "inherited_unit_edges": len(case.inherited_edges),
            "duplicated_inherited_edges": duplicated_edges,
            "incidental_cross_contacts": len(case.incidental_edges),
            "incidental_edges_sha256": object_digest(case.incidental_edges),
            "moved_map_sha256": object_digest(case.moved_map),
            "all_four_nonmonochromatic_terminal_patterns_extend": True,
            "canonical_terminal_relation": list(NONMONO_PATTERNS),
            "chromatic_number": 4,
        })

    expected_headlines = [
        (431, 1944, 1936, 8),
        (431, 1944, 1936, 8),
        (443, 2000, 1984, 16),
        (393, 1770, 1768, 2),
        (416, 1865, 1861, 4),
    ]
    need([(row["points"], row["complete_unit_edges"], row["inherited_unit_edges"],
           row["incidental_cross_contacts"]) for row in summaries] == expected_headlines,
         "case headline inventory")
    need(total_pairs == 446581, "total pair coverage")

    return {
        "status": "ACCEPTED_T375_D3_SELFGLUE_CLOSURE_INDEPENDENTLY",
        "reviewed_source_commit": TARGET_COMMIT,
        "target_certificate_sha256": file_digest(target_dir / "certificate.json"),
        "source_integrity": {
            "t375_source_commit": SOURCE_COMMIT,
            "dependency_sha256": SOURCE_HASHES,
            "appendix_rows": 109,
            "orbit_size_histogram": {str(k): v for k, v in sorted(source.orbit_size_histogram.items())},
            "reference_points": len(source.reference_points),
            "reference_unit_edges": len(source.reference_edges),
            "retained_points": len(source.points),
            "retained_unit_edges": len(source.edges),
            "retained_point_sha256": object_digest(source.points),
            "retained_edge_sha256": object_digest(source.edges),
        },
        "exact_geometry": {
            "coordinate_model": "((a*sqrt(3)+b*sqrt(11))/36,(c+d*sqrt(33))/36)",
            "unit_direction_box_rows": box_rows,
            "oriented_unit_directions": len(directions),
            "unit_direction_sha256": object_digest(directions),
            "d3_actions_including_identity": 6,
            "all_terminal_permutations_realized": True,
            "nonidentity_cases": len(cases),
            "total_unordered_pairs_covered": total_pairs,
        },
        "t375_forcing": {
            "marked_triangle_squared_distance": "1/3",
            "monochromatic_four_colour_extension_exists": False,
            "independent_assignment_dsat_search": monochromatic_stats,
            "all_canonical_nonmonochromatic_patterns_witnessed_in_every_case": True,
            "canonical_relation": list(NONMONO_PATTERNS),
        },
        "chromatic_refinement": {
            "t375_induced_moser_spindle_vertices": list(MOSER_T375_VERTICES),
            "induced_moser_spindle_edges": [list(edge) for edge in MOSER_PATTERN_EDGES],
            "moser_three_colour_extension_exists": False,
            "moser_three_colour_search": moser_three_stats,
            "t375_chromatic_number": 4,
            "all_five_unions_chromatic_number": 4,
        },
        "cases": summaries,
        "scope": {
            "common_marked_triangle_d3_self_gluings_only": True,
            "all_five_nonidentity_d3_actions_closed": True,
            "other_relative_placements_classified": False,
            "three_or_more_copies_classified": False,
            "abstract_graph_only": False,
            "plane_unit_distance_realizations_checked": True,
            "ordinary_nonfour_signal": False,
            "five_chromatic_construction": False,
            "record_candidate": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, default=DEFAULT_REPOSITORY)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = review(args.repository.resolve())
    if args.check_expected:
        need(result == read_json(HERE / "EXPECTED.json"), "review expected output mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
