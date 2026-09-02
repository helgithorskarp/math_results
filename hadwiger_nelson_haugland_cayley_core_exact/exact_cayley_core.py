#!/usr/bin/env python3
"""Exact reconstruction of Haugland's T5, T6, G0, and 740-vertex 7-core."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations
from math import isqrt
from pathlib import Path
from typing import Iterable

from exact_field import (
    MODULUS,
    ONE,
    ZERO,
    Element,
    Point,
    add,
    coordinate_hash,
    edge_hash,
    field_constants,
    point_add,
    point_sub,
    point_text,
    squared_norm,
)


SPECIALIZATIONS = ((2521, 1397), (2689, 2025))
ARXIV_V4_TEX_SHA256 = "49bcc56076cf9405fe35acbc0f7035f06e98107f79541136950111674873e357"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_json_hash(value: object) -> str:
    encoded = json.dumps(value, separators=(",", ":"), sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()


def radius_three_ball(vectors: list[Point]) -> dict[Point, int]:
    origin = (ZERO, ZERO)
    distances = {origin: 0}
    frontier = {origin}
    for distance in range(1, 4):
        following = {
            point_add(point, vector) for point in frontier for vector in vectors
        }
        following.difference_update(distances)
        for point in following:
            distances[point] = distance
        frontier = following
    return distances


def translate_distances(
    distances: dict[Point, int], translation: Point
) -> dict[Point, int]:
    return {point_add(translation, point): distance for point, distance in distances.items()}


def construct_t_sets(
    distances_a: dict[Point, int], distances_b: dict[Point, int]
) -> tuple[set[Point], set[Point]]:
    # Since d(A,B)=2, every radius-2 point about either endpoint lies on an
    # A-to-B walk of length at most 6.  All remaining vertices on such a walk
    # have endpoint distances exactly (3,3).
    ball_a2 = {point for point, distance in distances_a.items() if distance <= 2}
    ball_b2 = {point for point, distance in distances_b.items() if distance <= 2}
    sphere_a3 = {point for point, distance in distances_a.items() if distance == 3}
    sphere_b3 = {point for point, distance in distances_b.items() if distance == 3}
    t6 = ball_a2 | ball_b2 | (sphere_a3 & sphere_b3)

    # A vertex on a length-at-most-5 walk is within two steps of one endpoint.
    # The two-step A-B walk then puts it within radius 3 of the other endpoint.
    t5 = {
        point
        for point in distances_a.keys() & distances_b.keys()
        if distances_a[point] + distances_b[point] <= 5
    }
    return t5, t6


def evaluate_element(value: Element, prime: int, zeta_image: int) -> int:
    answer = 0
    for coefficient in reversed(value):
        if coefficient.denominator % prime == 0:
            raise AssertionError("specialization divides a denominator")
        answer = (
            answer * zeta_image
            + coefficient.numerator * pow(coefficient.denominator, -1, prime)
        ) % prime
    return answer


def check_specialization(prime: int, zeta_image: int) -> None:
    if prime < 2 or any(prime % divisor == 0 for divisor in range(2, isqrt(prime) + 1)):
        raise AssertionError("specialization modulus is not prime")
    if pow(zeta_image, 84, prime) != 1:
        raise AssertionError("zeta image is not an 84th root")
    for divisor in (2, 3, 7):
        if pow(zeta_image, 84 // divisor, prime) == 1:
            raise AssertionError("zeta image does not have exact order 84")
    value = 0
    for coefficient in reversed(MODULUS):
        value = (value * zeta_image + coefficient) % prime
    if value:
        raise AssertionError("zeta image does not annihilate Phi_84")


def modular_images(
    points: list[Point], prime: int, zeta_image: int
) -> list[tuple[int, int]]:
    check_specialization(prime, zeta_image)
    return [
        (
            evaluate_element(x, prime, zeta_image),
            evaluate_element(y, prime, zeta_image),
        )
        for x, y in points
    ]


def modular_unit_circle(prime: int) -> list[tuple[int, int]]:
    square_roots: dict[int, list[int]] = {}
    for value in range(prime):
        square_roots.setdefault(value * value % prime, []).append(value)
    circle = [
        (x, y)
        for x in range(prime)
        for y in square_roots.get((1 - x * x) % prime, ())
    ]
    if not circle:
        raise AssertionError("empty modular unit circle")
    return circle


def subset_pair_count(total: int, subset: int) -> int:
    return total * (total - 1) // 2 - (total - subset) * (total - subset - 1) // 2


def strict_pairs_touching_subset(
    points: list[Point], subset: set[int], images: list[list[tuple[int, int]]]
) -> tuple[list[tuple[int, int]], list[int]]:
    prime = SPECIALIZATIONS[0][0]
    buckets: dict[tuple[int, int], list[int]] = {}
    for index, image in enumerate(images[0]):
        buckets.setdefault(image, []).append(index)
    candidates: set[tuple[int, int]] = set()
    circle = modular_unit_circle(prime)
    for left in subset:
        x, y = images[0][left]
        for dx, dy in circle:
            for right in buckets.get(((x + dx) % prime, (y + dy) % prime), ()):
                if left != right:
                    candidates.add(tuple(sorted((left, right))))
    survivor_counts = [len(candidates)]
    for (prime, _), point_images in zip(SPECIALIZATIONS[1:], images[1:], strict=True):
        candidates = {
            (left, right)
            for left, right in candidates
            if (
                (point_images[left][0] - point_images[right][0]) ** 2
                + (point_images[left][1] - point_images[right][1]) ** 2
                - 1
            )
            % prime
            == 0
        }
        survivor_counts.append(len(candidates))
    unit_pairs = [
        pair
        for pair in sorted(candidates)
        if squared_norm(point_sub(points[pair[0]], points[pair[1]])) == ONE
    ]
    return unit_pairs, survivor_counts


def strict_pairs_induced(
    points: list[Point], selected: set[int], images: list[list[tuple[int, int]]]
) -> tuple[list[tuple[int, int]], list[int]]:
    candidates = list(combinations(sorted(selected), 2))
    survivor_counts: list[int] = []
    for (prime, _), point_images in zip(SPECIALIZATIONS, images, strict=True):
        candidates = [
            (left, right)
            for left, right in candidates
            if (
                (point_images[left][0] - point_images[right][0]) ** 2
                + (point_images[left][1] - point_images[right][1]) ** 2
                - 1
            )
            % prime
            == 0
        ]
        survivor_counts.append(len(candidates))
    return (
        [
            pair
            for pair in candidates
            if squared_norm(point_sub(points[pair[0]], points[pair[1]])) == ONE
        ],
        survivor_counts,
    )


def simultaneous_core(
    selected: set[int], edges: Iterable[tuple[int, int]], minimum_degree: int
) -> tuple[set[int], list[int]]:
    adjacency = {vertex: set() for vertex in selected}
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    core = set(selected)
    rounds: list[int] = []
    while True:
        deleted = {
            vertex
            for vertex in core
            if len(adjacency[vertex] & core) < minimum_degree
        }
        if not deleted:
            return core, rounds
        rounds.append(len(deleted))
        core.difference_update(deleted)


def path_points(paths: list[list[int]], vectors: list[Point], target: Point) -> list[Point]:
    origin = (ZERO, ZERO)
    points: list[Point] = []
    index: set[Point] = set()

    def insert(point: Point) -> None:
        if point not in index:
            index.add(point)
            points.append(point)

    insert(origin)
    for path in paths:
        point = origin
        for step in path:
            if not 0 <= step < len(vectors):
                raise AssertionError("path index outside the vector table")
            point = point_add(point, vectors[step])
            insert(point)
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


def compute(graph_path: Path) -> dict:
    payload = json.loads(graph_path.read_text())
    sqrt3, vectors = field_constants()
    origin = (ZERO, ZERO)
    target = (ZERO, sqrt3)
    if point_add(point_add(target, vectors[56]), vectors[70]) != origin:
        raise AssertionError("the declared two-step B-to-A walk failed")

    distances_a = radius_three_ball(vectors)
    distances_b = translate_distances(distances_a, target)
    t5, t6 = construct_t_sets(distances_a, distances_b)
    points = sorted(t6, key=point_text)
    index = {point: vertex for vertex, point in enumerate(points)}
    t5_indices = {index[point] for point in t5}
    images = [modular_images(points, *parameters) for parameters in SPECIALIZATIONS]

    touching_edges, touching_survivors = strict_pairs_touching_subset(
        points, t5_indices, images
    )
    vector_set = set(vectors)
    all_touching_edges_are_generators = all(
        point_sub(points[right], points[left]) in vector_set
        for left, right in touching_edges
    )
    if not all_touching_edges_are_generators:
        raise AssertionError("a strict T6-T5 unit pair is not a declared generator")

    adjacency_to_t5 = [set() for _ in points]
    for left, right in touching_edges:
        adjacency_to_t5[left].add(right)
        adjacency_to_t5[right].add(left)
    g0 = {
        vertex
        for vertex in range(len(points))
        if vertex in t5_indices or len(adjacency_to_t5[vertex] & t5_indices) >= 7
    }
    g0_edges, g0_survivors = strict_pairs_induced(points, g0, images)
    core, peeling_rounds = simultaneous_core(g0, g0_edges, 7)
    core_edges = [edge for edge in g0_edges if edge[0] in core and edge[1] in core]

    published_points = path_points(payload["paths"], vectors, target)
    if set(published_points) != {points[vertex] for vertex in core}:
        raise AssertionError("exact 7-core differs from the Appendix path point set")
    published_index = {point: vertex for vertex, point in enumerate(published_points)}
    published_core_edges = sorted(
        tuple(sorted((published_index[points[left]], published_index[points[right]])))
        for left, right in core_edges
    )
    declared_edges = [tuple(edge) for edge in payload["G1_edges"]]
    if published_core_edges != declared_edges:
        raise AssertionError("exact 7-core strict edges differ from the published reconstruction")

    sphere_counts = Counter(distances_a.values())
    result = {
        "schema": 1,
        "input_graph_sha256": sha256_file(graph_path),
        "source": {
            "arxiv_version": "2608.04542v4",
            "tex_sha256": ARXIV_V4_TEX_SHA256,
            "appendix_path_count": len(payload["paths"]),
            "appendix_path_length_histogram": {
                str(length): count
                for length, count in sorted(Counter(map(len, payload["paths"])).items())
            },
            "appendix_paths_sha256": canonical_json_hash(payload["paths"]),
        },
        "specializations": [
            {"prime": prime, "zeta_image": zeta_image}
            for prime, zeta_image in SPECIALIZATIONS
        ],
        "radius_three_ball": {
            "sphere_counts": {str(k): sphere_counts[k] for k in range(4)},
            "vertices": len(distances_a),
            "coordinate_sha256": coordinate_hash(distances_a),
        },
        "T5": {
            "vertices": len(t5),
            "coordinate_sha256": coordinate_hash(t5),
            "endpoint_distance_histogram": distance_histogram(t5, distances_a, distances_b),
        },
        "T6": {
            "vertices": len(t6),
            "coordinate_sha256": coordinate_hash(t6),
            "endpoint_distance_histogram": distance_histogram(t6, distances_a, distances_b),
        },
        "strict_T6_pairs_touching_T5": {
            "pairs_checked": subset_pair_count(len(points), len(t5_indices)),
            "sieve_survivors": touching_survivors,
            "unit_pairs": len(touching_edges),
            "edge_sha256": edge_hash(touching_edges),
            "all_differences_are_generators": all_touching_edges_are_generators,
        },
        "G0": {
            "vertices": len(g0),
            "coordinate_sha256": coordinate_hash(points[vertex] for vertex in g0),
            "pairs_checked": len(g0) * (len(g0) - 1) // 2,
            "sieve_survivors": g0_survivors,
            "strict_unit_edges": len(g0_edges),
            "edge_sha256_in_T6_order": edge_hash(g0_edges),
        },
        "G1_7core": {
            "vertices": len(core),
            "coordinate_sha256": coordinate_hash(points[vertex] for vertex in core),
            "simultaneous_peeling_rounds": peeling_rounds,
            "strict_unit_edges": len(core_edges),
            "published_order_edge_sha256": edge_hash(published_core_edges),
            "equals_appendix_path_set": True,
            "equals_sibling_strict_edge_set": True,
        },
    }
    return result


def verify_result(actual: dict, expected: dict) -> None:
    if actual != expected:
        raise AssertionError("recomputed result differs from certificate")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("generate", "verify"))
    parser.add_argument("graph", type=Path)
    parser.add_argument("certificate", type=Path)
    arguments = parser.parse_args()
    result = compute(arguments.graph)
    if arguments.mode == "generate":
        arguments.certificate.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    else:
        expected = json.loads(arguments.certificate.read_text())
        verify_result(result, expected)
    print(
        "all_checks=true "
        f"ball3={result['radius_three_ball']['vertices']} "
        f"T5={result['T5']['vertices']} T6={result['T6']['vertices']} "
        f"cross_edges={result['strict_T6_pairs_touching_T5']['unit_pairs']} "
        f"G0=({result['G0']['vertices']},{result['G0']['strict_unit_edges']}) "
        f"G1=({result['G1_7core']['vertices']},{result['G1_7core']['strict_unit_edges']}) "
        f"peeling={result['G1_7core']['simultaneous_peeling_rounds']}"
    )


if __name__ == "__main__":
    main()
