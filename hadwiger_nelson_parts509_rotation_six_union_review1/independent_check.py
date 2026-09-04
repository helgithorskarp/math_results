#!/usr/bin/env python3
"""Clean-room audit of the all-six exceptional Parts-placement theorem."""

from __future__ import annotations

import base64
import hashlib
import json
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path


RADICANDS = (3, 5, 11)
DIMENSION = 8
L_SIZE = 374
PARTS_SIZE = 509
TRIPLE_SIZE = 533
EXTENSION_SIZE = 159
UNION_SIZE = 692
SCALE = 96 * 64

POINTS_SHA256 = "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50"
TRIPLE_CERTIFICATE_SHA256 = "46ee849ead7b3601e887cee2aa2d5a1d02d12cf083a673c9890e2d2552bef795"
SIX_CERTIFICATE_SHA256 = "e11993c16d16551fd2be06d7a52a17b9f02d2116912db59770f4cdcc0a34b99f"
BASE_CERTIFICATE_SHA256 = "d354f9629c41639168b80fc1aa6feb6e4187dd37dee7efcb83b4ef6ebe68d16c"
BASE_EDGE_SHA256 = "5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c"
UNION_EDGE_SHA256 = "ee9d50eed3d3ba28d5a687876311fdb23b02a88458eed0c769a04916d1018465"

Field = tuple[int, ...]
Point = tuple[Field, Field]
Edge = tuple[int, int]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def multiply(a: Field, b: Field) -> Field:
    """Generic squarefree-basis product in Q(sqrt(3),sqrt(5),sqrt(11))."""
    result = [0] * DIMENSION
    for left_mask, left_coefficient in enumerate(a):
        for right_mask, right_coefficient in enumerate(b):
            if not left_coefficient or not right_coefficient:
                continue
            factor = 1
            for bit, radicand in enumerate(RADICANDS):
                if left_mask & right_mask & (1 << bit):
                    factor *= radicand
            result[left_mask ^ right_mask] += left_coefficient * right_coefficient * factor
    return tuple(result)


def add(a: Field, b: Field) -> Field:
    return tuple(x + y for x, y in zip(a, b, strict=True))


def subtract(a: Field, b: Field) -> Field:
    return tuple(x - y for x, y in zip(a, b, strict=True))


def read_points(path: Path) -> list[Point]:
    assert file_sha256(path) == POINTS_SHA256
    lines = path.read_text(encoding="ascii").splitlines()
    assert lines[0].endswith("scale=96")
    points = []
    for line in lines[1:]:
        if not line:
            continue
        row = tuple(map(int, line.split()))
        assert len(row) == 16
        points.append((row[:8], row[8:]))
    assert len(points) == len(set(points)) == PARTS_SIZE
    return points


def rotate(point: Point, cosine: Field, sine: Field) -> Point:
    """Rotate a denominator-96 point by c,s numerators of denominator 64."""
    x, y = point
    return (
        subtract(multiply(cosine, x), multiply(sine, y)),
        add(multiply(sine, x), multiply(cosine, y)),
    )


ZERO: Field = (0,) * 8
ROTATIONS: tuple[tuple[int, Field, Field], ...] = (
    (108, (-32, 0, 0, 0, 0, 0, 0, 0), (0, -32, 0, 0, 0, 0, 0, 0)),
    (109, (-32, 0, 0, 0, 0, 0, 0, 0), (0, 32, 0, 0, 0, 0, 0, 0)),
    (789, (64, 0, 0, 0, 0, 0, 0, 0), ZERO),
    (215, (-17, 0, -21, 0, 0, 0, 0, 0), (0, -17, 0, 7, 0, 0, 0, 0)),
    (216, (-17, 0, 21, 0, 0, 0, 0, 0), (0, 17, 0, 7, 0, 0, 0, 0)),
    (690, (34, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, -14, 0, 0, 0, 0)),
)


def construct_union(source: list[Point]) -> tuple[list[Point], list[Edge], dict[int, list[int]]]:
    for _, cosine, sine in ROTATIONS:
        assert add(multiply(cosine, cosine), multiply(sine, sine)) == (4096,) + (0,) * 7

    identity = ROTATIONS[2][1]
    points = [rotate(point, identity, ZERO) for point in source[:L_SIZE]]
    index = {point: label for label, point in enumerate(points)}
    placements: dict[int, list[int]] = {}
    for event, cosine, sine in ROTATIONS:
        labels = list(range(L_SIZE))
        for source_point in source[L_SIZE:]:
            image = rotate(source_point, cosine, sine)
            if image not in index:
                index[image] = len(points)
                points.append(image)
            labels.append(index[image])
        placements[event] = labels
    assert len(points) == len(index) == UNION_SIZE

    unit = (SCALE**2,) + (0,) * 7
    edges = []
    for u in range(len(points)):
        for v in range(u + 1, len(points)):
            dx = subtract(points[u][0], points[v][0])
            dy = subtract(points[u][1], points[v][1])
            if add(multiply(dx, dx), multiply(dy, dy)) == unit:
                edges.append((u, v))
    return points, edges, placements


def edge_sha256(edges: list[Edge]) -> str:
    payload = "".join(f"{u} {v}\n" for u, v in edges).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def placement_edges(labels: list[int], edge_set: set[Edge]) -> list[Edge]:
    result = []
    for old_u in range(PARTS_SIZE):
        for old_v in range(old_u + 1, PARTS_SIZE):
            if tuple(sorted((labels[old_u], labels[old_v]))) in edge_set:
                result.append((old_u, old_v))
    return result


def unpack_colors(encoded: str, count: int) -> list[int]:
    data = base64.b64decode(encoded, validate=True)
    assert len(data) == (count + 3) // 4
    if count % 4:
        assert data[-1] >> (2 * (count % 4)) == 0
    return [(data[position // 4] >> (2 * (position % 4))) & 3 for position in range(count)]


def check_lifted_coloring(active: list[int], colors: list[int], edges: list[Edge]) -> tuple[int, set[int]]:
    """Duplicate colors from a 533-vertex triple onto both extension copies."""
    assert len(active) == len(colors)
    lifted = [-1] * UNION_SIZE
    for vertex, color in zip(active, colors, strict=True):
        assert 0 <= color < 4 and lifted[vertex] == -1
        lifted[vertex] = color
        if vertex >= L_SIZE:
            lifted[vertex + EXTENSION_SIZE] = color
    checks = 0
    for u, v in edges:
        if lifted[u] >= 0 and lifted[v] >= 0:
            assert lifted[u] != lifted[v]
            checks += 1
    return checks, {vertex for vertex, color in enumerate(lifted) if color >= 0}


def irredundant(clauses: tuple[int, ...]) -> tuple[int, ...]:
    kept: list[int] = []
    for clause in sorted(set(clauses), key=lambda value: (value.bit_count(), value)):
        if not any(old & clause == old for old in kept):
            kept.append(clause)
    return tuple(kept)


def bounded_hitting_set(clauses: tuple[int, ...], variables: int, limit: int) -> tuple[bool, int]:
    """Binary select/forbid DPLL with exact unit and packing bounds."""
    states = 0

    @lru_cache(maxsize=None)
    def search(current: tuple[int, ...], budget: int) -> bool:
        nonlocal states
        states += 1
        current = irredundant(current)
        if not current:
            return True
        if budget < 0 or current[0] == 0:
            return False

        units = 0
        for clause in current:
            if clause.bit_count() == 1:
                units |= clause
        if units:
            needed = units.bit_count()
            return needed <= budget and search(
                tuple(clause for clause in current if not clause & units), budget - needed
            )

        used = 0
        packing = 0
        for clause in current:
            if not clause & used:
                used |= clause
                packing += 1
        if packing > budget:
            return False

        counts = [0] * variables
        for clause in current:
            bits = clause
            while bits:
                bit = bits & -bits
                counts[bit.bit_length() - 1] += 1
                bits -= bit
        variable = max(range(variables), key=lambda i: (counts[i], -i))
        bit = 1 << variable
        if search(tuple(clause for clause in current if not clause & bit), budget - 1):
            return True
        return search(tuple(clause & ~bit for clause in current), budget)

    return search(irredundant(clauses), limit), states


def solver_self_tests() -> None:
    path = ((1 << 0) | (1 << 1), (1 << 1) | (1 << 2))
    assert bounded_hitting_set(path, 3, 0)[0] is False
    assert bounded_hitting_set(path, 3, 1)[0] is True
    disjoint = (1 << 0, 1 << 2)
    assert bounded_hitting_set(disjoint, 3, 1)[0] is False
    assert bounded_hitting_set(disjoint, 3, 2)[0] is True


def main() -> None:
    here = Path(__file__).resolve().parent
    root = here.parent
    points_path = root / "hadwiger_nelson_parts509_completion_census_degree9" / "points.tsv"
    triple_certificate_path = root / "hadwiger_nelson_parts509_rotation_triple_minimum" / "certificate.json"
    six_certificate_path = root / "hadwiger_nelson_parts509_rotation_six_union_minimum" / "certificate.json"
    base_certificate_path = root / "hadwiger_nelson_parts509_criticality" / "certificate.json"
    assert file_sha256(triple_certificate_path) == TRIPLE_CERTIFICATE_SHA256
    assert file_sha256(six_certificate_path) == SIX_CERTIFICATE_SHA256
    assert file_sha256(base_certificate_path) == BASE_CERTIFICATE_SHA256
    triple_certificate = json.loads(triple_certificate_path.read_text(encoding="utf-8"))
    six_certificate = json.loads(six_certificate_path.read_text(encoding="utf-8"))
    base_certificate = json.loads(base_certificate_path.read_text(encoding="utf-8"))
    assert six_certificate["canonical_event_order"] == [108, 109, 789, 215, 216, 690]
    assert six_certificate["edge_sha256"] == UNION_EDGE_SHA256

    points, edges, placements = construct_union(read_points(points_path))
    assert len(points) == UNION_SIZE and len(edges) == 3354
    assert edge_sha256(edges) == UNION_EDGE_SHA256
    assert all(len(labels) == len(set(labels)) == PARTS_SIZE for labels in placements.values())

    edge_set = set(edges)
    placement_counts = {event: len(placement_edges(labels, edge_set)) for event, labels in placements.items()}
    assert placement_counts == {event: 2442 for event, _, _ in ROTATIONS}
    identity_edges = placement_edges(placements[789], edge_set)
    assert edge_sha256(identity_edges) == BASE_EDGE_SHA256 == base_certificate["edge_sha256"]
    five_colors = list(map(int, base_certificate["five_coloring"]))
    assert len(five_colors) == 509 and set(five_colors) <= set(range(5))
    assert all(five_colors[u] != five_colors[v] for u, v in identity_edges)

    inside_l = sum(v < L_SIZE for _, v in edges)
    first_extension = sum(L_SIZE <= v < TRIPLE_SIZE for _, v in edges)
    second_extension = sum(v >= TRIPLE_SIZE for _, v in edges)
    cross = [(u, v) for u, v in edges if L_SIZE <= u < TRIPLE_SIZE <= v]
    partition = {
        "cross_extension": len(cross),
        "first_extension_contribution": first_extension,
        "inside_L": inside_l,
        "second_extension_contribution": second_extension,
    }
    assert partition == {
        "cross_extension": 0,
        "first_extension_contribution": 747,
        "inside_L": 1860,
        "second_extension_contribution": 747,
    }

    first_edges = [(u, v) for u, v in edges if v < TRIPLE_SIZE]
    mapped_second = sorted(
        (
            u if u < L_SIZE else u - EXTENSION_SIZE,
            v if v < L_SIZE else v - EXTENSION_SIZE,
        )
        for u, v in edges
        if (u < L_SIZE or u >= TRIPLE_SIZE) and (v < L_SIZE or v >= TRIPLE_SIZE)
    )
    assert first_edges == mapped_second

    forced = triple_certificate["forced_vertices"]
    free = triple_certificate["free_vertices"]
    assert forced == sorted(set(forced)) and free == sorted(set(free))
    assert set(forced) | set(free) == set(range(TRIPLE_SIZE))
    forced_extension = sorted(set(forced) - set(range(L_SIZE)))
    assert set(range(L_SIZE)) <= set(forced) and len(forced_extension) == 96 and len(free) == 63

    row_length = triple_certificate["forced_coloring_row_length"]
    assert row_length == TRIPLE_SIZE - 1
    packed_forced = unpack_colors(triple_certificate["forced_colorings_base64"], len(forced) * row_length)
    coloring_checks = 0
    for row_number, deleted in enumerate(forced):
        colors = packed_forced[row_number * row_length : (row_number + 1) * row_length]
        active = [v for v in range(TRIPLE_SIZE) if v != deleted]
        checks, lifted_domain = check_lifted_coloring(active, colors, edges)
        expected_deleted = {deleted} if deleted < L_SIZE else {deleted, deleted + EXTENSION_SIZE}
        assert lifted_domain == set(range(UNION_SIZE)) - expected_deleted
        coloring_checks += checks

    free_index = {vertex: position for position, vertex in enumerate(free)}
    deletion_sets: list[frozenset[int]] = []
    masks = []
    for row in triple_certificate["killing_sets"]:
        deleted_list = row["deleted"]
        deleted = frozenset(deleted_list)
        assert deleted and deleted_list == sorted(deleted)
        assert deleted <= set(free) and deleted not in deletion_sets
        active = [v for v in range(TRIPLE_SIZE) if v not in deleted]
        colors = unpack_colors(row["coloring_base64"], len(active))
        checks, lifted_domain = check_lifted_coloring(active, colors, edges)
        doubled = set(deleted) | {v + EXTENSION_SIZE for v in deleted}
        assert lifted_domain == set(range(UNION_SIZE)) - doubled
        coloring_checks += checks
        deletion_sets.append(deleted)
        masks.append(sum(1 << free_index[v] for v in deleted))
    assert len(deletion_sets) == 330
    assert all(not left < right for left in deletion_sets for right in deletion_sets)
    histogram = dict(sorted(Counter(map(len, deletion_sets)).items()))
    assert histogram == {2: 145, 3: 89, 4: 34, 5: 29, 6: 17, 7: 7, 8: 7, 9: 1, 11: 1}

    solver_self_tests()
    exists_at_most_38, dpll_states = bounded_hitting_set(tuple(masks), len(free), 38)
    assert exists_at_most_38 is False

    identity_extension = set(placements[789]) - set(range(L_SIZE))
    identity_free = sorted(identity_extension & set(free))
    assert len(identity_extension) == 135
    assert set(forced_extension) <= identity_extension and len(identity_free) == 39
    assert all(set(identity_free) & deleted for deleted in deletion_sets)
    assert coloring_checks == 2_659_622
    assert L_SIZE + len(forced_extension) + len(identity_free) == 509

    summary = {
        "all_checks": True,
        "base_five_coloring_verified": True,
        "dpll_states_for_limit_38": dpll_states,
        "edge_partition": partition,
        "edge_sha256": UNION_EDGE_SHA256,
        "edges": len(edges),
        "event_placement_edge_counts": placement_counts,
        "forced_common_L": L_SIZE,
        "forced_extension_pairs": len(forced_extension),
        "identity_projected_free": identity_free,
        "killing_set_size_histogram": histogram,
        "lifted_coloring_edge_checks": coloring_checks,
        "minimum_non_four_colorable_order": 509,
        "projected_free_positions": len(free),
        "projected_transversal_number": len(identity_free),
        "python": sys.version.split()[0],
        "six_certificate_sha256": SIX_CERTIFICATE_SHA256,
        "standard_library_only": True,
        "triple_certificate_sha256": TRIPLE_CERTIFICATE_SHA256,
        "vertices": len(points),
    }
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
