#!/usr/bin/env python3
"""Solver-free verifier for the 108/109/789 placement-union theorem."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path


K = 4
BASIS = 8
PRIMES = (3, 5, 11)
SCALE = 192
L_SIZE = 374
BASE_SIZE = 509
EXPECTED_POINTS_SHA256 = "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50"
EXPECTED_BASE_EDGE_SHA256 = "5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c"
EXPECTED_BASE_CERTIFICATE_SHA256 = "d354f9629c41639168b80fc1aa6feb6e4187dd37dee7efcb83b4ef6ebe68d16c"
EXPECTED_ROTATION_CERTIFICATE_SHA256 = "f3d1ff76e031dc0bfe50153db43512428d073d25ea243173d26d5ebfaa8cdedf"
EXPECTED_UNION_EDGE_SHA256 = "cc3f6ad98f3d1198b6bde17628326d690b17789bd880f84303a2c6ff58be454f"

Field = tuple[int, ...]
Point = tuple[Field, Field]
Edge = tuple[int, int]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def field_multiply(left: Field, right: Field) -> Field:
    result = [0] * BASIS
    for i, a in enumerate(left):
        if not a:
            continue
        for j, b in enumerate(right):
            if not b:
                continue
            factor = 1
            for bit, prime in enumerate(PRIMES):
                if (i & j) & (1 << bit):
                    factor *= prime
            result[i ^ j] += factor * a * b
    return tuple(result)


def multiply_sqrt3(value: Field) -> Field:
    result = [0] * BASIS
    for mask, coefficient in enumerate(value):
        if mask & 1:
            result[mask ^ 1] += 3 * coefficient
        else:
            result[mask ^ 1] += coefficient
    return tuple(result)


def read_scaled_points(path: Path) -> list[Point]:
    if sha256(path) != EXPECTED_POINTS_SHA256:
        raise ValueError("unexpected points.tsv SHA-256")
    points = []
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        values = tuple(map(int, line.split()))
        if len(values) != 2 * BASIS:
            raise ValueError("point row does not have 16 integer coefficients")
        points.append((values[:BASIS], values[BASIS:]))
    if len(points) != BASE_SIZE or len(set(points)) != BASE_SIZE:
        raise ValueError("expected 509 distinct source points")
    return points


def rotate_108(point: Point) -> Point:
    """Apply (c,s)=(-1/2,-sqrt(3)/2), returning coefficients at scale 192."""
    x, y = point
    sqrt3_x = multiply_sqrt3(x)
    sqrt3_y = multiply_sqrt3(y)
    return (
        tuple(-a + b for a, b in zip(x, sqrt3_y, strict=True)),
        tuple(-a - b for a, b in zip(sqrt3_x, y, strict=True)),
    )


def rotate_109(point: Point) -> Point:
    """Apply (c,s)=(-1/2,+sqrt(3)/2), returning coefficients at scale 192."""
    x, y = point
    sqrt3_x = multiply_sqrt3(x)
    sqrt3_y = multiply_sqrt3(y)
    return (
        tuple(-a - b for a, b in zip(x, sqrt3_y, strict=True)),
        tuple(a - b for a, b in zip(sqrt3_x, y, strict=True)),
    )


def identity_scaled(point: Point) -> Point:
    return tuple(tuple(2 * coefficient for coefficient in coordinate) for coordinate in point)  # type: ignore[return-value]


def rotate_scaled64(point: Point, cosine: Field, sine: Field) -> Point:
    """Rotate a scale-96 point by field numerators with denominator 64."""
    x, y = point
    cx = field_multiply(cosine, x)
    sy = field_multiply(sine, y)
    sx = field_multiply(sine, x)
    cy = field_multiply(cosine, y)
    return (
        tuple(a - b for a, b in zip(cx, sy, strict=True)),
        tuple(a + b for a, b in zip(sx, cy, strict=True)),
    )


def identity_scaled64(point: Point) -> Point:
    return tuple(tuple(64 * coefficient for coefficient in coordinate) for coordinate in point)  # type: ignore[return-value]


def squared_distance(left: Point, right: Point) -> Field:
    dx = tuple(a - b for a, b in zip(left[0], right[0], strict=True))
    dy = tuple(a - b for a, b in zip(left[1], right[1], strict=True))
    xx = field_multiply(dx, dx)
    yy = field_multiply(dy, dy)
    return tuple(a + b for a, b in zip(xx, yy, strict=True))


def strict_edges(points: list[Point], scale: int) -> list[Edge]:
    unit = (scale * scale,) + (0,) * (BASIS - 1)
    return [
        (i, j)
        for i in range(len(points))
        for j in range(i + 1, len(points))
        if squared_distance(points[i], points[j]) == unit
    ]


def build_union(points_path: Path) -> tuple[list[Point], list[Edge], dict[int, list[int]], Counter[int]]:
    base = read_scaled_points(points_path)
    points = [identity_scaled(point) for point in base[:L_SIZE]]
    point_index = {point: i for i, point in enumerate(points)}
    placements: dict[int, list[int]] = {}
    multiplicity: Counter[int] = Counter()
    for event, transform in ((108, rotate_108), (109, rotate_109), (789, identity_scaled)):
        labels = list(range(L_SIZE))
        for point in base[L_SIZE:]:
            image = transform(point)
            if image not in point_index:
                point_index[image] = len(points)
                points.append(image)
            label = point_index[image]
            labels.append(label)
            multiplicity[label] += 1
        placements[event] = labels
    if len(points) != len(set(points)):
        raise AssertionError("coordinate deduplication failed")
    edges = strict_edges(points, SCALE)
    return points, edges, placements, Counter(multiplicity.values())


def build_equivalent_union(points_path: Path) -> tuple[list[Point], list[Edge], dict[int, list[int]], Counter[int]]:
    """Build events 215/216/690 independently at common scale 96*64."""
    base = read_scaled_points(points_path)
    points = [identity_scaled64(point) for point in base[:L_SIZE]]
    point_index = {point: i for i, point in enumerate(points)}
    placements: dict[int, list[int]] = {}
    multiplicity: Counter[int] = Counter()
    rotations = (
        (215, (-17, 0, -21, 0, 0, 0, 0, 0), (0, -17, 0, 7, 0, 0, 0, 0)),
        (216, (-17, 0, 21, 0, 0, 0, 0, 0), (0, 17, 0, 7, 0, 0, 0, 0)),
        (690, (34, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, -14, 0, 0, 0, 0)),
    )
    if any(len(cosine) != BASIS or len(sine) != BASIS for _, cosine, sine in rotations):
        raise AssertionError("malformed rotation numerator")
    for event, cosine, sine in rotations:
        cc = field_multiply(cosine, cosine)
        ss = field_multiply(sine, sine)
        norm = tuple(a + b for a, b in zip(cc, ss, strict=True))
        if norm != (4096,) + (0,) * (BASIS - 1):
            raise AssertionError(f"event {event} is not a unit rotation")
        labels = list(range(L_SIZE))
        for point in base[L_SIZE:]:
            image = rotate_scaled64(point, cosine, sine)
            if image not in point_index:
                point_index[image] = len(points)
                points.append(image)
            label = point_index[image]
            labels.append(label)
            multiplicity[label] += 1
        placements[event] = labels
    if len(points) != len(set(points)):
        raise AssertionError("equivalent-union coordinate deduplication failed")
    edges = strict_edges(points, 96 * 64)
    return points, edges, placements, Counter(multiplicity.values())


def edge_digest(edges: list[Edge]) -> str:
    payload = "".join(f"{u} {v}\n" for u, v in edges).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def placement_edge_digest(labels: list[int], edge_set: set[Edge]) -> tuple[int, str]:
    old_edges = []
    for u in range(BASE_SIZE):
        for v in range(u + 1, BASE_SIZE):
            if tuple(sorted((labels[u], labels[v]))) in edge_set:
                old_edges.append((u, v))
    return len(old_edges), edge_digest(old_edges)


def unpack_colors(payload: bytes, count: int) -> list[int]:
    expected_bytes = (count + 3) // 4
    if len(payload) != expected_bytes:
        raise ValueError("packed colouring has the wrong byte length")
    colors = [(payload[i // 4] >> (2 * (i % 4))) & 3 for i in range(count)]
    if count % 4:
        used_bits = 2 * (count % 4)
        if payload[-1] >> used_bits:
            raise ValueError("nonzero padding bits in packed colouring")
    return colors


def check_coloring(colors: dict[int, int], edges: list[Edge]) -> int:
    checks = 0
    for u, v in edges:
        if u in colors and v in colors:
            if colors[u] == colors[v]:
                raise AssertionError(f"monochromatic edge {(u, v)}")
            checks += 1
    return checks


def minimal_masks(masks: list[int]) -> tuple[int, ...]:
    answer: list[int] = []
    for mask in sorted(set(masks), key=lambda value: (value.bit_count(), value)):
        if not any(old & mask == old for old in answer):
            answer.append(mask)
    return tuple(answer)


def has_hitting_set_at_most(hyperedges: tuple[int, ...], universe_size: int, limit: int) -> tuple[bool, int]:
    """Exact disjoint-branch enumeration with unit propagation and a packing bound."""
    nodes = 0

    def propagate(edges: tuple[int, ...], chosen: int, forbidden: int):
        while True:
            available = [edge & ~forbidden for edge in edges if not edge & chosen]
            if any(edge == 0 for edge in available):
                return None
            available = list(minimal_masks(available))
            units = 0
            for edge in available:
                if edge.bit_count() == 1:
                    units |= edge
            new_units = units & ~chosen
            if not new_units:
                return tuple(available), chosen
            chosen |= new_units
            if chosen.bit_count() > limit:
                return None

    def search(edges: tuple[int, ...], chosen: int, forbidden: int) -> bool:
        nonlocal nodes
        nodes += 1
        reduced = propagate(edges, chosen, forbidden)
        if reduced is None:
            return False
        edges, chosen = reduced
        budget = limit - chosen.bit_count()
        if not edges:
            return True
        used = 0
        packing = 0
        for edge in sorted(edges, key=int.bit_count):
            if not edge & used:
                used |= edge
                packing += 1
        if packing > budget:
            return False
        pivot = min(edges, key=lambda edge: (edge.bit_count(), edge))
        choices = [1 << i for i in range(universe_size) if pivot & (1 << i)]
        choices.sort(key=lambda bit: (-sum(bool(edge & bit) for edge in edges), bit))
        earlier = 0
        for bit in choices:
            if search(edges, chosen | bit, forbidden | earlier):
                return True
            earlier |= bit
        return False

    return search(hyperedges, 0, 0), nodes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?", type=Path, default=Path(__file__).with_name("certificate.json"))
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    root = here.parent
    points_path = root / "hadwiger_nelson_parts509_completion_census_degree9" / "points.tsv"
    base_certificate_path = root / "hadwiger_nelson_parts509_criticality" / "certificate.json"
    if sha256(base_certificate_path) != EXPECTED_BASE_CERTIFICATE_SHA256:
        raise ValueError("unexpected Parts criticality certificate SHA-256")
    base_certificate = json.loads(base_certificate_path.read_text(encoding="utf-8"))
    if base_certificate["edge_sha256"] != EXPECTED_BASE_EDGE_SHA256:
        raise ValueError("base certificate edge digest mismatch")
    rotation_certificate_path = root / "hadwiger_nelson_parts509_rotation_scan" / "rotation_certificate.json"
    if sha256(rotation_certificate_path) != EXPECTED_ROTATION_CERTIFICATE_SHA256:
        raise ValueError("unexpected rotation certificate SHA-256")
    rotation_certificate = json.loads(rotation_certificate_path.read_text(encoding="utf-8"))
    expected_rotations = {
        108: ((Fraction(-1, 2), 0, 0, 0, 0, 0, 0, 0), (0, Fraction(-1, 2), 0, 0, 0, 0, 0, 0)),
        109: ((Fraction(-1, 2), 0, 0, 0, 0, 0, 0, 0), (0, Fraction(1, 2), 0, 0, 0, 0, 0, 0)),
        215: ((Fraction(-17, 64), 0, Fraction(-21, 64), 0, 0, 0, 0, 0), (0, Fraction(-17, 64), 0, Fraction(7, 64), 0, 0, 0, 0)),
        216: ((Fraction(-17, 64), 0, Fraction(21, 64), 0, 0, 0, 0, 0), (0, Fraction(17, 64), 0, Fraction(7, 64), 0, 0, 0, 0)),
        690: ((Fraction(17, 32), 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, Fraction(-7, 32), 0, 0, 0, 0)),
        789: ((Fraction(1), 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0)),
    }
    for event, expected in expected_rotations.items():
        row = rotation_certificate["events"][event]
        actual = tuple(tuple(Fraction(value) for value in row[key]) for key in ("cos", "sin"))
        if actual != expected:
            raise AssertionError(f"rotation certificate event {event} mismatch")

    certificate = json.loads(args.certificate.read_text(encoding="utf-8"))
    if certificate["format"] != "parts509-exceptional-rotation-triple-minimum-v1":
        raise ValueError("unknown certificate format")
    if certificate["events"] != [108, 109, 789]:
        raise ValueError("unexpected exceptional-placement triple")
    if certificate["equivalent_events"] != [215, 216, 690]:
        raise ValueError("unexpected equivalent exceptional-placement triple")
    points, edges, placements, multiplicity = build_union(points_path)
    if len(points) != 533 or certificate["vertices"] != 533:
        raise AssertionError("union vertex count mismatch")
    if len(edges) != 2607 or certificate["edges"] != 2607:
        raise AssertionError("union edge count mismatch")
    digest = edge_digest(edges)
    if digest != EXPECTED_UNION_EDGE_SHA256 or digest != certificate["edge_sha256"]:
        raise AssertionError("union edge digest mismatch")
    if multiplicity != Counter({3: 111, 2: 24, 1: 24}):
        raise AssertionError("unexpected rotated-S overlap profile")
    other_points, other_edges, other_placements, other_multiplicity = build_equivalent_union(points_path)
    if len(other_points) != 533 or len(other_edges) != 2607:
        raise AssertionError("equivalent-union census mismatch")
    if edge_digest(other_edges) != EXPECTED_UNION_EDGE_SHA256 or other_edges != edges:
        raise AssertionError("the two canonical strict edge arrays differ")
    if other_multiplicity != multiplicity:
        raise AssertionError("the two overlap profiles differ")
    event_map = {108: 215, 109: 216, 789: 690}
    if any(placements[first] != other_placements[second] for first, second in event_map.items()):
        raise AssertionError("corresponding placement-label arrays differ")
    edge_set = set(edges)
    placement_counts = {}
    for event, labels in placements.items():
        if len(labels) != BASE_SIZE or len(set(labels)) != BASE_SIZE:
            raise AssertionError("placement does not have 509 distinct points")
        count, placement_digest = placement_edge_digest(labels, edge_set)
        if count != 2442:
            raise AssertionError("placement strict-edge count mismatch")
        placement_counts[event] = count
        if event == 789 and placement_digest != EXPECTED_BASE_EDGE_SHA256:
            raise AssertionError("identity placement is not the certified Parts graph")
    other_edge_set = set(other_edges)
    for event, labels in other_placements.items():
        count, _ = placement_edge_digest(labels, other_edge_set)
        if count != 2442:
            raise AssertionError(f"equivalent placement {event} strict-edge count mismatch")

    forced = certificate["forced_vertices"]
    if forced != sorted(set(forced)) or len(forced) != 470:
        raise AssertionError("forced-vertex list mismatch")
    forced_set = set(forced)
    free = sorted(set(range(len(points))) - forced_set)
    if free != certificate["free_vertices"] or len(free) != 63:
        raise AssertionError("free-vertex list mismatch")
    row_bytes = ((len(points) - 1) + 3) // 4
    if certificate["forced_coloring_row_length"] != len(points) - 1:
        raise AssertionError("forced colouring row length mismatch")
    forced_payload = base64.b64decode(certificate["forced_colorings_base64"], validate=True)
    if len(forced_payload) != row_bytes * len(forced):
        raise AssertionError("forced colouring payload length mismatch")
    coloring_checks = 0
    for row_index, deleted in enumerate(forced):
        payload = forced_payload[row_index * row_bytes : (row_index + 1) * row_bytes]
        colors = unpack_colors(payload, len(points) - 1)
        active = [v for v in range(len(points)) if v != deleted]
        coloring_checks += check_coloring(dict(zip(active, colors, strict=True)), edges)

    free_index = {v: i for i, v in enumerate(free)}
    masks = []
    killing_checks = 0
    seen = set()
    for row in certificate["killing_sets"]:
        deleted = row["deleted"]
        key = tuple(deleted)
        if key != tuple(sorted(set(deleted))) or key in seen or not set(deleted) <= set(free):
            raise AssertionError("malformed or duplicate killing set")
        seen.add(key)
        active = [v for v in range(len(points)) if v not in set(deleted)]
        colors = unpack_colors(base64.b64decode(row["coloring_base64"], validate=True), len(active))
        killing_checks += check_coloring(dict(zip(active, colors, strict=True)), edges)
        masks.append(sum(1 << free_index[v] for v in deleted))
    hyperedges = minimal_masks(masks)
    if len(hyperedges) != 330 or len(masks) != 330:
        raise AssertionError("certificate killing sets are not inclusion-minimal")
    exists_38, search_nodes = has_hitting_set_at_most(hyperedges, len(free), 38)
    if exists_38:
        raise AssertionError("found a hitting set of size at most 38")
    if search_nodes != certificate["transversal_search_nodes"]:
        raise AssertionError("transversal search node count mismatch")
    identity_optional = set(placements[789]) & set(free)
    if not forced_set <= set(placements[789]):
        raise AssertionError("the identity placement omits a forced vertex")
    if len(identity_optional) != 39 or not all(identity_optional & set(row["deleted"]) for row in certificate["killing_sets"]):
        raise AssertionError("identity placement is not a size-39 transversal")

    pairwise_shared = {
        f"{left}/{right}": len(set(placements[left]) & set(placements[right]))
        for left, right in ((108, 109), (108, 789), (109, 789))
    }
    if set(pairwise_shared.values()) != {493}:
        raise AssertionError("unexpected pairwise placement intersections")
    triple_shared = len(set.intersection(*(set(labels) for labels in placements.values())))
    if triple_shared != 485:
        raise AssertionError("unexpected triple placement intersection")

    summary = {
        "all_checks": True,
        "vertices": len(points),
        "edges": len(edges),
        "pairwise_shared_vertices": pairwise_shared,
        "shared_vertices_all_three": triple_shared,
        "equivalent_event_map": {str(key): value for key, value in event_map.items()},
        "strict_edge_arrays_identical": True,
        "forced_vertices": len(forced),
        "free_vertices": len(free),
        "minimal_killing_sets": len(hyperedges),
        "transversal_number": 39,
        "transversal_search_nodes": search_nodes,
        "minimum_non_four_colorable_order": 509,
        "coloring_edge_checks": coloring_checks + killing_checks,
        "edge_sha256": digest,
    }
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
