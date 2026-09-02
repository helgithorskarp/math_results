#!/usr/bin/env python3
"""Independent SymPy/multiset checker for the exact Haugland Cayley core.

This checker does not import the primary tuple-field implementation.  It
enumerates commutative step multisets rather than expanding BFS frontiers, and
it screens all relevant unordered pairs directly rather than using modular
unit-circle buckets.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, deque
from itertools import combinations, combinations_with_replacement
from pathlib import Path
from typing import Any, Iterable

import sympy as sp


RECONSTRUCTION_DIRECTORY = "hadwiger_nelson_haugland2131_exact_reproduction"
SPECIALIZATIONS = ((1009, 527), (2521, 1397))
Point = tuple[Any, Any]


def load_reconstruct():
    sibling = Path(__file__).resolve().parent.parent / RECONSTRUCTION_DIRECTORY
    sys.path.insert(0, str(sibling))
    import reconstruct  # type: ignore[import-not-found]

    return reconstruct


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def coefficient_text(coefficient: Any) -> str:
    numerator = int(coefficient.numerator)
    denominator = int(coefficient.denominator)
    return str(numerator) if denominator == 1 else f"{numerator}/{denominator}"


def anp_text(element: Any) -> str:
    coefficients = list(reversed(element.to_list()))
    coefficients.extend([0] * (24 - len(coefficients)))
    if len(coefficients) != 24:
        raise AssertionError("unexpected algebraic-field degree")
    return ",".join(coefficient_text(value) for value in coefficients)


def point_text(point: Point) -> str:
    return anp_text(point[0]) + ";" + anp_text(point[1])


def coordinate_hash(points: Iterable[Point]) -> str:
    digest = hashlib.sha256()
    for point in sorted(points, key=point_text):
        digest.update((point_text(point) + "\n").encode())
    return digest.hexdigest()


def edge_hash(edges: Iterable[tuple[int, int]]) -> str:
    digest = hashlib.sha256()
    for left, right in sorted(edges):
        digest.update(f"{left} {right}\n".encode())
    return digest.hexdigest()


def point_add(left: Point, right: Point) -> Point:
    return left[0] + right[0], left[1] + right[1]


def point_sub(left: Point, right: Point) -> Point:
    return left[0] - right[0], left[1] - right[1]


def squared_norm(point: Point) -> Any:
    return point[0] * point[0] + point[1] * point[1]


def multiset_radius_three_ball(field: Any, vectors: list[Point]) -> dict[Point, int]:
    """Enumerate all unordered step multisets of sizes zero through three."""
    origin = (field.zero, field.zero)
    distances = {origin: 0}
    for length in range(1, 4):
        level: set[Point] = set()
        for step_indices in combinations_with_replacement(range(len(vectors)), length):
            point = origin
            for step in step_indices:
                point = point_add(point, vectors[step])
            level.add(point)
        for point in level:
            distances.setdefault(point, length)
    return distances


def construct_t_sets(
    distances_a: dict[Point, int], distances_b: dict[Point, int]
) -> tuple[set[Point], set[Point]]:
    t5 = {
        point
        for point in distances_a.keys() & distances_b.keys()
        if distances_a[point] + distances_b[point] <= 5
    }
    ball_a2 = {point for point, distance in distances_a.items() if distance <= 2}
    ball_b2 = {point for point, distance in distances_b.items() if distance <= 2}
    sphere_a3 = {point for point, distance in distances_a.items() if distance == 3}
    sphere_b3 = {point for point, distance in distances_b.items() if distance == 3}
    return t5, ball_a2 | ball_b2 | (sphere_a3 & sphere_b3)


def evaluate_anp(element: Any, prime: int, zeta_image: int) -> int:
    value = 0
    for coefficient in element.to_list():
        numerator = int(coefficient.numerator)
        denominator = int(coefficient.denominator)
        if denominator % prime == 0:
            raise AssertionError("specialization divides a denominator")
        value = (
            value * zeta_image
            + numerator * pow(denominator, -1, prime)
        ) % prime
    return value


def check_specialization(field: Any, prime: int, zeta_image: int) -> None:
    if not sp.isprime(prime):
        raise AssertionError("specialization modulus is not prime")
    if pow(zeta_image, 84, prime) != 1:
        raise AssertionError("zeta image is not an 84th root")
    for divisor in (2, 3, 7):
        if pow(zeta_image, 84 // divisor, prime) == 1:
            raise AssertionError("zeta image does not have exact order 84")
    modulus_value = 0
    for coefficient in field.field.mod.to_list():
        modulus_value = (
            modulus_value * zeta_image + int(coefficient.numerator)
        ) % prime
    if modulus_value:
        raise AssertionError("zeta image does not annihilate the field modulus")


def modular_images(
    field: Any, points: list[Point], prime: int, zeta_image: int
) -> list[tuple[int, int]]:
    check_specialization(field, prime, zeta_image)
    return [
        (
            evaluate_anp(x, prime, zeta_image),
            evaluate_anp(y, prime, zeta_image),
        )
        for x, y in points
    ]


def is_modular_unit(
    left: int, right: int, images: list[tuple[int, int]], prime: int
) -> bool:
    dx = images[left][0] - images[right][0]
    dy = images[left][1] - images[right][1]
    return (dx * dx + dy * dy - 1) % prime == 0


def brute_strict_pairs_touching_subset(
    field: Any,
    points: list[Point],
    subset: set[int],
    images: list[list[tuple[int, int]]],
) -> tuple[list[tuple[int, int]], list[int]]:
    candidates: list[tuple[int, int]] = []
    for left, right in combinations(range(len(points)), 2):
        if left not in subset and right not in subset:
            continue
        if is_modular_unit(left, right, images[0], SPECIALIZATIONS[0][0]):
            candidates.append((left, right))
    survivor_counts = [len(candidates)]
    for (prime, _), point_images in zip(SPECIALIZATIONS[1:], images[1:], strict=True):
        candidates = [
            pair
            for pair in candidates
            if is_modular_unit(pair[0], pair[1], point_images, prime)
        ]
        survivor_counts.append(len(candidates))
    return (
        [
            pair
            for pair in candidates
            if squared_norm(point_sub(points[pair[0]], points[pair[1]])) == field.one
        ],
        survivor_counts,
    )


def brute_strict_pairs_induced(
    field: Any,
    points: list[Point],
    selected: set[int],
    images: list[list[tuple[int, int]]],
) -> tuple[list[tuple[int, int]], list[int]]:
    candidates = list(combinations(sorted(selected), 2))
    survivor_counts: list[int] = []
    for (prime, _), point_images in zip(SPECIALIZATIONS, images, strict=True):
        candidates = [
            pair
            for pair in candidates
            if is_modular_unit(pair[0], pair[1], point_images, prime)
        ]
        survivor_counts.append(len(candidates))
    return (
        [
            pair
            for pair in candidates
            if squared_norm(point_sub(points[pair[0]], points[pair[1]])) == field.one
        ],
        survivor_counts,
    )


def queue_core(
    selected: set[int], edges: Iterable[tuple[int, int]], minimum_degree: int
) -> set[int]:
    adjacency = {vertex: set() for vertex in selected}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    core = set(selected)
    queue = deque(vertex for vertex in core if len(adjacency[vertex]) < minimum_degree)
    while queue:
        vertex = queue.popleft()
        if vertex not in core or len(adjacency[vertex] & core) >= minimum_degree:
            continue
        core.remove(vertex)
        for neighbour in adjacency[vertex] & core:
            if len(adjacency[neighbour] & core) < minimum_degree:
                queue.append(neighbour)
    return core


def path_points(payload: dict, field: Any, vectors: list[Point]) -> list[Point]:
    origin = (field.zero, field.zero)
    target = (field.zero, field.sqrt3)
    points: list[Point] = []
    index: set[Point] = set()
    for path_number, path in enumerate([[]] + payload["paths"]):
        point = origin
        if path_number == 0:
            index.add(point)
            points.append(point)
            continue
        for step in path:
            point = point_add(point, vectors[step])
            if point not in index:
                index.add(point)
                points.append(point)
        if point != target:
            raise AssertionError("Appendix path does not end at B")
    return points


def distance_histogram(
    points: set[Point], distances_a: dict[Point, int], distances_b: dict[Point, int]
) -> dict[str, int]:
    histogram = Counter(
        (distances_a.get(point, 4), distances_b.get(point, 4)) for point in points
    )
    return {f"{left},{right}": histogram[left, right] for left, right in sorted(histogram)}


def require_equal(actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: actual {actual!r} != expected {expected!r}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("graph", type=Path)
    parser.add_argument("certificate", type=Path)
    arguments = parser.parse_args()
    payload = json.loads(arguments.graph.read_text())
    certificate = json.loads(arguments.certificate.read_text())
    require_equal(sha256_file(arguments.graph), certificate["input_graph_sha256"], "input hash")

    reconstruct = load_reconstruct()
    field = reconstruct.Cyclotomic84()
    vectors = field.unit_vectors()
    origin = (field.zero, field.zero)
    target = (field.zero, field.sqrt3)
    require_equal(point_add(point_add(target, vectors[56]), vectors[70]), origin, "B-A walk")

    distances_a = multiset_radius_three_ball(field, vectors)
    distances_b = {
        point_add(target, point): distance for point, distance in distances_a.items()
    }
    t5, t6 = construct_t_sets(distances_a, distances_b)
    points = sorted(t6, key=point_text)
    index = {point: vertex for vertex, point in enumerate(points)}
    t5_indices = {index[point] for point in t5}
    images = [
        modular_images(field, points, prime, zeta_image)
        for prime, zeta_image in SPECIALIZATIONS
    ]

    require_equal(
        Counter(distances_a.values()),
        Counter({0: 1, 1: 84, 2: 3444, 3: 80052}),
        "sphere counts",
    )
    require_equal(len(distances_a), certificate["radius_three_ball"]["vertices"], "ball size")
    require_equal(
        coordinate_hash(distances_a),
        certificate["radius_three_ball"]["coordinate_sha256"],
        "ball hash",
    )
    for name, point_set in (("T5", t5), ("T6", t6)):
        require_equal(len(point_set), certificate[name]["vertices"], f"{name} size")
        require_equal(
            coordinate_hash(point_set),
            certificate[name]["coordinate_sha256"],
            f"{name} hash",
        )
        require_equal(
            distance_histogram(point_set, distances_a, distances_b),
            certificate[name]["endpoint_distance_histogram"],
            f"{name} endpoint-distance histogram",
        )

    touching_edges, touching_survivors = brute_strict_pairs_touching_subset(
        field, points, t5_indices, images
    )
    touching_expected = certificate["strict_T6_pairs_touching_T5"]
    require_equal(len(touching_edges), touching_expected["unit_pairs"], "touching edge count")
    require_equal(edge_hash(touching_edges), touching_expected["edge_sha256"], "touching edge hash")
    vector_set = set(vectors)
    require_equal(
        all(point_sub(points[right], points[left]) in vector_set for left, right in touching_edges),
        True,
        "touching edges use generators",
    )

    adjacency_to_t5 = [set() for _ in points]
    for left, right in touching_edges:
        adjacency_to_t5[left].add(right)
        adjacency_to_t5[right].add(left)
    g0 = {
        vertex
        for vertex in range(len(points))
        if vertex in t5_indices or len(adjacency_to_t5[vertex] & t5_indices) >= 7
    }
    g0_edges, g0_survivors = brute_strict_pairs_induced(field, points, g0, images)
    g0_expected = certificate["G0"]
    require_equal(len(g0), g0_expected["vertices"], "G0 size")
    require_equal(
        coordinate_hash(points[vertex] for vertex in g0),
        g0_expected["coordinate_sha256"],
        "G0 hash",
    )
    require_equal(len(g0_edges), g0_expected["strict_unit_edges"], "G0 edge count")
    require_equal(edge_hash(g0_edges), g0_expected["edge_sha256_in_T6_order"], "G0 edge hash")

    core = queue_core(g0, g0_edges, 7)
    core_edges = [edge for edge in g0_edges if edge[0] in core and edge[1] in core]
    core_expected = certificate["G1_7core"]
    require_equal(len(core), core_expected["vertices"], "7-core size")
    require_equal(
        coordinate_hash(points[vertex] for vertex in core),
        core_expected["coordinate_sha256"],
        "7-core hash",
    )
    require_equal(len(core_edges), core_expected["strict_unit_edges"], "7-core edge count")

    published_points = path_points(payload, field, vectors)
    require_equal(
        set(published_points),
        {points[vertex] for vertex in core},
        "Appendix/core point sets",
    )
    published_index = {point: vertex for vertex, point in enumerate(published_points)}
    published_edges = sorted(
        tuple(sorted((published_index[points[left]], published_index[points[right]])))
        for left, right in core_edges
    )
    require_equal(
        published_edges,
        [tuple(edge) for edge in payload["G1_edges"]],
        "published edge list",
    )
    require_equal(
        edge_hash(published_edges),
        core_expected["published_order_edge_sha256"],
        "published edge hash",
    )

    print(
        "independent_all_checks=true method=sympy_multisets_and_bruteforce_pairs "
        f"primes={SPECIALIZATIONS[0][0]},{SPECIALIZATIONS[1][0]} "
        f"ball3={len(distances_a)} T5={len(t5)} T6={len(t6)} "
        f"cross_sieve={touching_survivors} cross_edges={len(touching_edges)} "
        f"G0_sieve={g0_survivors} G0=({len(g0)},{len(g0_edges)}) "
        f"G1=({len(core)},{len(core_edges)})"
    )


if __name__ == "__main__":
    main()
