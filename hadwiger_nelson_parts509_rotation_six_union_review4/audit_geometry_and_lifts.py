#!/usr/bin/env python3
"""Clean-room exact geometry and colouring-lift audit for the six-placement union.

The implementation imports no code from the contributed verifiers.  Elements
of Q(sqrt(3),sqrt(5),sqrt(11)) use the square-free radicand basis
1,3,5,15,11,33,55,165; multiplication is performed through gcd reduction.
"""

from __future__ import annotations

import base64
import hashlib
import json
import math
from pathlib import Path


RADICANDS = (1, 3, 5, 15, 11, 33, 55, 165)
RADICAND_INDEX = {value: index for index, value in enumerate(RADICANDS)}
ZERO = (0,) * 8
ONE = (1,) + (0,) * 7
SQRT3 = (0, 1) + (0,) * 6
L_SIZE = 374
TRIPLE_SIZE = 533
EXTENSION_SIZE = 159
W_SIZE = 692
BASE_SIZE = 509

EXPECTED_POINTS_SHA256 = "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50"
EXPECTED_TRIPLE_CERTIFICATE_SHA256 = (
    "46ee849ead7b3601e887cee2aa2d5a1d02d12cf083a673c9890e2d2552bef795"
)
EXPECTED_BASE_EDGE_SHA256 = "5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c"
EXPECTED_W_EDGE_SHA256 = "ee9d50eed3d3ba28d5a687876311fdb23b02a88458eed0c769a04916d1018465"


Element = tuple[int, ...]
Point = tuple[Element, Element]
Edge = tuple[int, int]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add(left: Element, right: Element) -> Element:
    return tuple(a + b for a, b in zip(left, right, strict=True))


def neg(value: Element) -> Element:
    return tuple(-coefficient for coefficient in value)


def scale(value: Element, multiplier: int) -> Element:
    return tuple(multiplier * coefficient for coefficient in value)


def multiply(left: Element, right: Element) -> Element:
    coefficients = [0] * 8
    for i, a in enumerate(left):
        if not a:
            continue
        for j, b in enumerate(right):
            if not b:
                continue
            common = math.gcd(RADICANDS[i], RADICANDS[j])
            reduced = RADICANDS[i] * RADICANDS[j] // (common * common)
            coefficients[RADICAND_INDEX[reduced]] += a * b * common
    return tuple(coefficients)


def read_points(path: Path) -> list[Point]:
    if digest(path) != EXPECTED_POINTS_SHA256:
        raise ValueError("unexpected Parts point file")
    points: list[Point] = []
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        row = tuple(map(int, line.split()))
        if len(row) != 16:
            raise ValueError("expected sixteen coefficients per point")
        points.append((row[:8], row[8:]))
    if len(points) != BASE_SIZE or len(set(points)) != BASE_SIZE:
        raise AssertionError("unexpected Parts point census")
    return points


def rotate(point: Point, cosine: Element, sine: Element) -> Point:
    x, y = point
    return (
        add(multiply(cosine, x), neg(multiply(sine, y))),
        add(multiply(sine, x), multiply(cosine, y)),
    )


def edges(points: list[Point], denominator: int) -> list[Edge]:
    unit = scale(ONE, denominator * denominator)
    result = []
    for i, (x_i, y_i) in enumerate(points):
        for j in range(i + 1, len(points)):
            x_j, y_j = points[j]
            dx = add(x_i, neg(x_j))
            dy = add(y_i, neg(y_j))
            if add(multiply(dx, dx), multiply(dy, dy)) == unit:
                result.append((i, j))
    return result


def edge_digest(edge_list: list[Edge]) -> str:
    raw = "".join(f"{u} {v}\n" for u, v in edge_list).encode("ascii")
    return hashlib.sha256(raw).hexdigest()


def build_triple(
    base: list[Point],
    denominator_multiplier: int,
    rotations: tuple[tuple[int, Element, Element], ...],
) -> tuple[list[Point], dict[int, list[int]]]:
    points = [
        (scale(x, denominator_multiplier), scale(y, denominator_multiplier))
        for x, y in base[:L_SIZE]
    ]
    index = {point: vertex for vertex, point in enumerate(points)}
    placements: dict[int, list[int]] = {}
    for event, cosine, sine in rotations:
        labels = list(range(L_SIZE))
        for point in base[L_SIZE:]:
            image = rotate(point, cosine, sine)
            if image not in index:
                index[image] = len(points)
                points.append(image)
            labels.append(index[image])
        placements[event] = labels
    return points, placements


def packed_colors(payload: bytes, count: int) -> list[int]:
    if len(payload) != (count + 3) // 4:
        raise AssertionError("colour payload length mismatch")
    result = [(payload[i // 4] >> (2 * (i % 4))) & 3 for i in range(count)]
    if count % 4 and payload[-1] >> (2 * (count % 4)):
        raise AssertionError("nonzero packed-colour padding")
    return result


def lift(first_colors: list[int]) -> list[int]:
    if len(first_colors) != TRIPLE_SIZE:
        raise ValueError("expected one canonical triple colouring")
    result = first_colors + [-1] * EXTENSION_SIZE
    for vertex in range(L_SIZE, TRIPLE_SIZE):
        result[vertex + EXTENSION_SIZE] = first_colors[vertex]
    return result


def check_coloring(colors: list[int], edge_list: list[Edge]) -> int:
    checked = 0
    for u, v in edge_list:
        if colors[u] >= 0 and colors[v] >= 0:
            if colors[u] == colors[v]:
                raise AssertionError(f"monochromatic edge {(u, v)}")
            checked += 1
    return checked


def main() -> None:
    here = Path(__file__).resolve().parent
    root = here.parent
    points_path = root / "hadwiger_nelson_parts509_completion_census_degree9" / "points.tsv"
    triple_certificate_path = root / "hadwiger_nelson_parts509_rotation_triple_minimum" / "certificate.json"
    if digest(triple_certificate_path) != EXPECTED_TRIPLE_CERTIFICATE_SHA256:
        raise ValueError("unexpected triple certificate")
    base = read_points(points_path)

    # Numerators for rotations at denominators 2 and 64, respectively.
    first_rotations = (
        (108, neg(ONE), neg(SQRT3)),
        (109, neg(ONE), SQRT3),
        (789, scale(ONE, 2), ZERO),
    )
    second_rotations = (
        (215, (-17, 0, -21, 0, 0, 0, 0, 0), (0, -17, 0, 7, 0, 0, 0, 0)),
        (216, (-17, 0, 21, 0, 0, 0, 0, 0), (0, 17, 0, 7, 0, 0, 0, 0)),
        (690, (34, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, -14, 0, 0, 0, 0)),
    )
    first_points, first_placements = build_triple(base, 2, first_rotations)
    second_points, second_placements = build_triple(base, 64, second_rotations)
    if len(first_points) != TRIPLE_SIZE or len(second_points) != TRIPLE_SIZE:
        raise AssertionError("unexpected triple order")
    first_edges = edges(first_points, 192)
    second_edges = edges(second_points, 6144)
    if first_edges != second_edges or len(first_edges) != 2607:
        raise AssertionError("the canonical triple edge arrays differ")
    if any(first_placements[a] != second_placements[b] for a, b in ((108, 215), (109, 216), (789, 690))):
        raise AssertionError("the placement-label arrays differ")

    scaled_first = [(scale(x, 32), scale(y, 32)) for x, y in first_points]
    if scaled_first[:L_SIZE] != second_points[:L_SIZE]:
        raise AssertionError("the triples do not share the same L coordinates")
    w_points = scaled_first + second_points[L_SIZE:]
    if len(w_points) != W_SIZE or len(set(w_points)) != W_SIZE:
        raise AssertionError("unexpected six-union point census")
    w_edges = edges(w_points, 6144)
    if len(w_edges) != 3354 or edge_digest(w_edges) != EXPECTED_W_EDGE_SHA256:
        raise AssertionError("unexpected six-union edge census")
    w_edge_set = set(w_edges)
    cross_edges = [
        edge for edge in w_edges
        if L_SIZE <= edge[0] < TRIPLE_SIZE <= edge[1]
    ]
    if cross_edges:
        raise AssertionError("unexpected edge between extension copies")

    combined_placements = dict(first_placements)
    for event, labels in second_placements.items():
        combined_placements[event] = [
            vertex if vertex < L_SIZE else vertex + EXTENSION_SIZE
            for vertex in labels
        ]
    placement_edges = {}
    for event, labels in combined_placements.items():
        if len(labels) != BASE_SIZE or len(set(labels)) != BASE_SIZE:
            raise AssertionError(f"event {event} is not a 509-point placement")
        selected = set(labels)
        placement_edges[event] = sum(u in selected and v in selected for u, v in w_edge_set)
    if set(placement_edges.values()) != {2442}:
        raise AssertionError("a constituent placement has the wrong strict-edge count")
    identity_labels = combined_placements[789]
    identity_edges = [
        (u, v)
        for u in range(BASE_SIZE)
        for v in range(u + 1, BASE_SIZE)
        if tuple(sorted((identity_labels[u], identity_labels[v]))) in w_edge_set
    ]
    if edge_digest(identity_edges) != EXPECTED_BASE_EDGE_SHA256:
        raise AssertionError("event 789 does not have the certified Parts edge array")

    certificate = json.loads(triple_certificate_path.read_text(encoding="utf-8"))
    forced = certificate["forced_vertices"]
    free = certificate["free_vertices"]
    if len(forced) != 470 or len(free) != 63 or set(forced) | set(free) != set(range(TRIPLE_SIZE)):
        raise AssertionError("unexpected forced/free partition")
    forced_extension = set(forced) - set(range(L_SIZE))
    if len(forced_extension) != 96 or set(range(L_SIZE)) - set(forced):
        raise AssertionError("unexpected forced-extension partition")

    checked = 0
    row_bytes = (TRIPLE_SIZE - 1 + 3) // 4
    payload = base64.b64decode(certificate["forced_colorings_base64"], validate=True)
    if len(payload) != row_bytes * len(forced):
        raise AssertionError("forced-colouring matrix length mismatch")
    for row, deleted in enumerate(forced):
        raw_colors = packed_colors(payload[row * row_bytes:(row + 1) * row_bytes], TRIPLE_SIZE - 1)
        triple_colors = [-1] * TRIPLE_SIZE
        active = [vertex for vertex in range(TRIPLE_SIZE) if vertex != deleted]
        for vertex, color in zip(active, raw_colors, strict=True):
            triple_colors[vertex] = color
        full_colors = lift(triple_colors)
        if deleted >= L_SIZE:
            full_colors[deleted + EXTENSION_SIZE] = -1
        checked += check_coloring(full_colors, w_edges)

    free_set = set(free)
    for row in certificate["killing_sets"]:
        deleted = set(row["deleted"])
        if not deleted <= free_set:
            raise AssertionError("killing set outside free universe")
        active = [vertex for vertex in range(TRIPLE_SIZE) if vertex not in deleted]
        raw_colors = packed_colors(base64.b64decode(row["coloring_base64"], validate=True), len(active))
        triple_colors = [-1] * TRIPLE_SIZE
        for vertex, color in zip(active, raw_colors, strict=True):
            triple_colors[vertex] = color
        full_colors = lift(triple_colors)
        for vertex in deleted:
            full_colors[vertex + EXTENSION_SIZE] = -1
        checked += check_coloring(full_colors, w_edges)

    identity_extension = set(first_placements[789]) - set(range(L_SIZE))
    if len(identity_extension & free_set) != 39 or not forced_extension <= identity_extension:
        raise AssertionError("identity placement does not realize the 96+39 split")
    edge_partition = {
        "inside_L": sum(v < L_SIZE for _, v in w_edges),
        "first_extension": sum(L_SIZE <= v < TRIPLE_SIZE for _, v in w_edges),
        "second_extension": sum(v >= TRIPLE_SIZE for _, v in w_edges),
        "cross_extension": len(cross_edges),
    }
    summary = {
        "all_checks": True,
        "base_edge_sha256": edge_digest(identity_edges),
        "edges": len(w_edges),
        "edge_partition": edge_partition,
        "edge_sha256": edge_digest(w_edges),
        "forced_extension_positions": len(forced_extension),
        "identity_free_positions": len(identity_extension & free_set),
        "lifted_coloring_edge_checks": checked,
        "placement_edges": placement_edges,
        "vertices": len(w_points),
    }
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
