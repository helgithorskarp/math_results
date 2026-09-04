#!/usr/bin/env python3
"""Independent audit of the Parts 108/789 rotation-union certificate.

This checker deliberately does not import the submitted verifier.  It uses a
generic multiquadratic-field product and a binary include/exclude hitting-set
search, rather than the verifier's disjoint pivot branching.
"""

from __future__ import annotations

import base64
import hashlib
import json
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path


RADICANDS = (3, 5, 11)
FIELD_DIMENSION = 8
SOURCE_SCALE = 96
COMMON_SCALE = 192
L_SIZE = 374
PARTS_SIZE = 509

POINTS_SHA256 = "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50"
CERTIFICATE_SHA256 = "85ea2050dbc6ff05b2766f899e86ba3b9157e4aa59cc6ef21f54f7531941c728"
BASE_CERTIFICATE_SHA256 = "d354f9629c41639168b80fc1aa6feb6e4187dd37dee7efcb83b4ef6ebe68d16c"
BASE_EDGE_SHA256 = "5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c"
UNION_EDGE_SHA256 = "4f7a2472d60aa0835a256b51dc9d1e3eb050b3e575bb41fa814961ce48496a47"

Field = tuple[int, ...]
Point = tuple[Field, Field]
Edge = tuple[int, int]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def multiply(a: Field, b: Field) -> Field:
    """Multiply in Q(sqrt(3),sqrt(5),sqrt(11)) in the squarefree basis."""
    out = [0] * FIELD_DIMENSION
    for left_mask, left_coefficient in enumerate(a):
        for right_mask, right_coefficient in enumerate(b):
            if not left_coefficient or not right_coefficient:
                continue
            repeated_radicals = left_mask & right_mask
            rational_factor = 1
            for bit, radicand in enumerate(RADICANDS):
                if repeated_radicals & (1 << bit):
                    rational_factor *= radicand
            out[left_mask ^ right_mask] += (
                left_coefficient * right_coefficient * rational_factor
            )
    return tuple(out)


SQRT3: Field = (0, 1, 0, 0, 0, 0, 0, 0)


def subtract(a: Field, b: Field) -> Field:
    return tuple(x - y for x, y in zip(a, b, strict=True))


def read_source_points(path: Path) -> list[Point]:
    assert file_sha256(path) == POINTS_SHA256
    lines = path.read_text(encoding="ascii").splitlines()
    assert lines[0] == "# basis=1,sqrt3,sqrt5,sqrt15,sqrt11,sqrt33,sqrt55,sqrt165 scale=96"
    points: list[Point] = []
    for line in lines[1:]:
        if not line:
            continue
        row = tuple(map(int, line.split()))
        assert len(row) == 16
        points.append((row[:8], row[8:]))
    assert len(points) == PARTS_SIZE == len(set(points))
    return points


def identity(point: Point) -> Point:
    # Convert denominator 96 to denominator 192.
    return tuple(tuple(2 * value for value in axis) for axis in point)  # type: ignore[return-value]


def rotate_minus_120(point: Point) -> Point:
    # x' = (-x + sqrt(3)y)/2 and y' = (-sqrt(3)x - y)/2.
    # Input numerators have denominator 96; output numerators have denominator 192.
    x, y = point
    root3_x = multiply(SQRT3, x)
    root3_y = multiply(SQRT3, y)
    return (
        tuple(-u + v for u, v in zip(x, root3_y, strict=True)),
        tuple(-u - v for u, v in zip(root3_x, y, strict=True)),
    )


def distance_squared(a: Point, b: Point) -> Field:
    dx = subtract(a[0], b[0])
    dy = subtract(a[1], b[1])
    xx = multiply(dx, dx)
    yy = multiply(dy, dy)
    return tuple(x + y for x, y in zip(xx, yy, strict=True))


def construct_union(source: list[Point]) -> tuple[list[Point], list[Edge], dict[int, list[int]]]:
    points = [identity(point) for point in source[:L_SIZE]]
    index = {point: label for label, point in enumerate(points)}
    placements: dict[int, list[int]] = {}
    for event, transform in ((108, rotate_minus_120), (789, identity)):
        labels = list(range(L_SIZE))
        for source_point in source[L_SIZE:]:
            image = transform(source_point)
            if image not in index:
                index[image] = len(points)
                points.append(image)
            labels.append(index[image])
        placements[event] = labels
    assert len(points) == len(index) == 525
    unit = (COMMON_SCALE**2,) + (0,) * 7
    edges = [
        (u, v)
        for u in range(len(points))
        for v in range(u + 1, len(points))
        if distance_squared(points[u], points[v]) == unit
    ]
    return points, edges, placements


def edge_sha256(edges: list[Edge]) -> str:
    payload = "".join(f"{u} {v}\n" for u, v in edges).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def placement_edges(labels: list[int], union_edges: set[Edge]) -> list[Edge]:
    result = []
    for old_u in range(PARTS_SIZE):
        for old_v in range(old_u + 1, PARTS_SIZE):
            mapped = tuple(sorted((labels[old_u], labels[old_v])))
            if mapped in union_edges:
                result.append((old_u, old_v))
    return result


def unpack_colors(encoded: str, count: int) -> list[int]:
    data = base64.b64decode(encoded, validate=True)
    assert len(data) == (count + 3) // 4
    if count % 4:
        assert data[-1] >> (2 * (count % 4)) == 0
    return [(data[position // 4] >> (2 * (position % 4))) & 3 for position in range(count)]


def check_coloring(active: list[int], colors: list[int], edges: list[Edge]) -> int:
    assert len(active) == len(colors)
    by_vertex = [-1] * 525
    for vertex, color in zip(active, colors, strict=True):
        assert 0 <= color < 4 and by_vertex[vertex] == -1
        by_vertex[vertex] = color
    checked = 0
    for u, v in edges:
        if by_vertex[u] >= 0 and by_vertex[v] >= 0:
            assert by_vertex[u] != by_vertex[v]
            checked += 1
    return checked


def irredundant(edges: tuple[int, ...]) -> tuple[int, ...]:
    kept: list[int] = []
    for edge in sorted(set(edges), key=lambda value: (value.bit_count(), value)):
        if not any(previous & edge == previous for previous in kept):
            kept.append(edge)
    return tuple(kept)


def bounded_hitting_set(edges: tuple[int, ...], universe_size: int, limit: int) -> tuple[bool, int]:
    """Binary DPLL for monotone clauses, independent of the submitted search.

    Each mask is a clause saying that at least one of its vertices must be
    selected.  At every state we either select or forbid one high-occurrence
    variable.  Unit clauses are forced, and a greedily found family of
    pairwise-disjoint clauses is a valid lower bound on the remaining budget.
    """
    states = 0

    @lru_cache(maxsize=None)
    def search(clauses: tuple[int, ...], budget: int) -> bool:
        nonlocal states
        states += 1
        clauses = irredundant(clauses)
        if not clauses:
            return True
        if budget < 0 or clauses[0] == 0:
            return False

        forced = 0
        for clause in clauses:
            if clause.bit_count() == 1:
                forced |= clause
        if forced:
            forced_count = forced.bit_count()
            if forced_count > budget:
                return False
            return search(tuple(c for c in clauses if not c & forced), budget - forced_count)

        occupied = 0
        packing_size = 0
        for clause in clauses:
            if not clause & occupied:
                occupied |= clause
                packing_size += 1
        if packing_size > budget:
            return False

        occurrences = [0] * universe_size
        for clause in clauses:
            bits = clause
            while bits:
                bit = bits & -bits
                occurrences[bit.bit_length() - 1] += 1
                bits -= bit
        variable = max(range(universe_size), key=lambda i: (occurrences[i], -i))
        chosen_bit = 1 << variable

        selected = tuple(c for c in clauses if not c & chosen_bit)
        if search(selected, budget - 1):
            return True
        forbidden = tuple(c & ~chosen_bit for c in clauses)
        return search(forbidden, budget)

    return search(irredundant(edges), limit), states


def solver_self_tests() -> None:
    # Clauses {0,1}, {1,2} have a one-element hitting set {1}.
    path = ((1 << 0) | (1 << 1), (1 << 1) | (1 << 2))
    assert bounded_hitting_set(path, 3, 0)[0] is False
    assert bounded_hitting_set(path, 3, 1)[0] is True
    # Two disjoint singleton clauses require exactly two elements.
    singleton_pair = (1 << 0, 1 << 2)
    assert bounded_hitting_set(singleton_pair, 3, 1)[0] is False
    assert bounded_hitting_set(singleton_pair, 3, 2)[0] is True


def main() -> None:
    here = Path(__file__).resolve().parent
    root = here.parent
    submitted = root / "hadwiger_nelson_parts509_rotation_union_minimum"
    points_path = root / "hadwiger_nelson_parts509_completion_census_degree9" / "points.tsv"
    certificate_path = submitted / "certificate.json"
    base_certificate_path = root / "hadwiger_nelson_parts509_criticality" / "certificate.json"

    assert file_sha256(certificate_path) == CERTIFICATE_SHA256
    assert file_sha256(base_certificate_path) == BASE_CERTIFICATE_SHA256
    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
    base_certificate = json.loads(base_certificate_path.read_text(encoding="utf-8"))
    assert certificate["format"] == "parts509-exceptional-rotation-union-minimum-v1"
    assert certificate["events"] == [108, 789]
    assert certificate["vertices"] == 525 and certificate["edges"] == 2551
    assert certificate["edge_sha256"] == UNION_EDGE_SHA256
    assert base_certificate["edge_sha256"] == BASE_EDGE_SHA256
    assert base_certificate["full_graph_four_color_solver_result"] == "UNSAT"

    points, edges, placements = construct_union(read_source_points(points_path))
    assert len(points) == 525 and len(edges) == 2551
    assert edge_sha256(edges) == UNION_EDGE_SHA256
    assert len(set(placements[108]) & set(placements[789])) == 493
    assert all(len(labels) == len(set(labels)) == 509 for labels in placements.values())

    edge_set = set(edges)
    event_108_edges = placement_edges(placements[108], edge_set)
    identity_edges = placement_edges(placements[789], edge_set)
    assert len(event_108_edges) == len(identity_edges) == 2442
    assert edge_sha256(identity_edges) == BASE_EDGE_SHA256

    # Independently check the committed proper 5-coloring on the identity copy.
    base_five_coloring = list(map(int, base_certificate["five_coloring"]))
    assert len(base_five_coloring) == 509 and set(base_five_coloring) <= set(range(5))
    assert all(base_five_coloring[u] != base_five_coloring[v] for u, v in identity_edges)

    forced = certificate["forced_vertices"]
    assert forced == sorted(set(forced)) and len(forced) == 489
    forced_set = set(forced)
    free = sorted(set(range(525)) - forced_set)
    assert free == certificate["free_vertices"] and len(free) == 36

    row_length = certificate["forced_coloring_row_length"]
    assert row_length == 524
    packed_forced = unpack_colors(certificate["forced_colorings_base64"], len(forced) * row_length)
    coloring_edge_checks = 0
    for row_number, deleted_vertex in enumerate(forced):
        colors = packed_forced[row_number * row_length : (row_number + 1) * row_length]
        active = [v for v in range(525) if v != deleted_vertex]
        coloring_edge_checks += check_coloring(active, colors, edges)

    free_index = {vertex: position for position, vertex in enumerate(free)}
    deletion_sets: list[frozenset[int]] = []
    masks: list[int] = []
    for row in certificate["killing_sets"]:
        deleted_list = row["deleted"]
        deleted = frozenset(deleted_list)
        assert deleted and deleted_list == sorted(deleted)
        assert deleted <= set(free) and deleted not in deletion_sets
        active = [v for v in range(525) if v not in deleted]
        colors = unpack_colors(row["coloring_base64"], len(active))
        coloring_edge_checks += check_coloring(active, colors, edges)
        deletion_sets.append(deleted)
        masks.append(sum(1 << free_index[v] for v in deleted))

    assert len(deletion_sets) == 133
    assert all(not a < b for a in deletion_sets for b in deletion_sets)
    size_histogram = dict(sorted(Counter(map(len, deletion_sets)).items()))
    assert size_histogram == {2: 30, 3: 29, 4: 31, 5: 22, 6: 13, 7: 7, 8: 1}

    solver_self_tests()
    exists_at_most_19, dpll_states = bounded_hitting_set(tuple(masks), len(free), 19)
    assert exists_at_most_19 is False

    identity_optional = sorted(set(placements[789]) & set(free))
    assert len(identity_optional) == 20
    assert all(set(identity_optional) & deleted for deleted in deletion_sets)

    assert coloring_edge_checks == 1_577_939
    summary = {
        "all_checks": True,
        "base_five_coloring_verified": True,
        "certificate_sha256": CERTIFICATE_SHA256,
        "coloring_edge_checks": coloring_edge_checks,
        "dpll_states_for_limit_19": dpll_states,
        "edge_sha256": UNION_EDGE_SHA256,
        "edges": len(edges),
        "forced_vertices": len(forced),
        "free_vertices": len(free),
        "identity_optional": identity_optional,
        "killing_set_size_histogram": size_histogram,
        "minimal_killing_sets": len(deletion_sets),
        "minimum_non_four_colorable_order": len(forced) + len(identity_optional),
        "python": sys.version.split()[0],
        "shared_vertices_between_placements": len(set(placements[108]) & set(placements[789])),
        "standard_library_only": True,
        "transversal_number": len(identity_optional),
        "vertices": len(points),
    }
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
