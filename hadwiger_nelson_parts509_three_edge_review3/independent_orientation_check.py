#!/usr/bin/env python3
"""Independently check two dense Parts overlap orientations."""

from __future__ import annotations

import itertools
import math
import sys
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path


RADICANDS = (1, 3, 5, 15, 11, 33, 55, 165)
ZERO = (0,) * 8
UNIT = (96 * 96,) + (0,) * 7
SCALE = 10**24
ROOT_FLOORS = tuple(math.isqrt(value * SCALE * SCALE) for value in RADICANDS)
PERMUTATIONS = tuple(itertools.permutations(range(4)))


def add(left, right):
    return tuple(a + b for a, b in zip(left, right, strict=True))


def sub(left, right):
    return tuple(a - b for a, b in zip(left, right, strict=True))


def neg(value):
    return tuple(-coefficient for coefficient in value)


def mul(left, right):
    answer = [0] * 8
    for i, a in enumerate(left):
        if not a:
            continue
        for j, b in enumerate(right):
            if not b:
                continue
            factor = 1
            for bit, prime in enumerate((3, 5, 11)):
                if (i & j) & (1 << bit):
                    factor *= prime
            answer[i ^ j] += a * b * factor
    return tuple(answer)


def squared_norm(vector):
    return add(mul(vector[0], vector[0]), mul(vector[1], vector[1]))


def read_points(path: Path):
    points = []
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        values = tuple(map(int, line.split()))
        if len(values) != 16:
            raise ValueError("bad point row")
        points.append((values[:8], values[8:]))
    if len(points) != 509:
        raise ValueError(len(points))
    return points


def directed_vectors(points):
    answer = defaultdict(set)
    for i, first in enumerate(points):
        for second in points[:i]:
            vector = (sub(first[0], second[0]), sub(first[1], second[1]))
            distance = squared_norm(vector)
            answer[distance].add(vector)
            answer[distance].add((neg(vector[0]), neg(vector[1])))
    return answer


def make_orientation(reflected, numerator_c, numerator_s, distance):
    if any(distance[index] for index in (1, 2, 3, 4, 6, 7)):
        raise AssertionError("common distance escaped Q(sqrt(33))")
    d0, d5 = distance[0], distance[5]
    denominator = d0 * d0 - 33 * d5 * d5
    conjugate = (d0, 0, 0, 0, 0, -d5, 0, 0)
    c = mul(numerator_c, conjugate)
    s = mul(numerator_s, conjugate)
    divisor = abs(denominator)
    for value in (*c, *s):
        divisor = math.gcd(divisor, abs(value))
    denominator //= divisor
    c = tuple(value // divisor for value in c)
    s = tuple(value // divisor for value in s)
    if denominator < 0:
        denominator = -denominator
        c, s = neg(c), neg(s)
    return (int(reflected), denominator, c, s)


def orientations(left_vectors, small_vectors):
    answer = set()
    for distance in left_vectors.keys() & small_vectors.keys():
        for a in left_vectors[distance]:
            for b in small_vectors[distance]:
                rotation_c = add(mul(a[0], b[0]), mul(a[1], b[1]))
                rotation_s = sub(mul(b[0], a[1]), mul(b[1], a[0]))
                answer.add(make_orientation(False, rotation_c, rotation_s, distance))
                reflection_c = sub(mul(a[0], b[0]), mul(a[1], b[1]))
                reflection_s = add(mul(a[0], b[1]), mul(a[1], b[0]))
                answer.add(make_orientation(True, reflection_c, reflection_s, distance))
    return sorted(answer)


def transformed_numerator(orientation, point):
    reflected, _, c, s = orientation
    cx, sy = mul(c, point[0]), mul(s, point[1])
    sx, cy = mul(s, point[0]), mul(c, point[1])
    return (add(cx, sy), sub(sx, cy)) if reflected else (sub(cx, sy), add(sx, cy))


def cross_difference(left, transformed, denominator):
    return (
        tuple(denominator * a - b for a, b in zip(left[0], transformed[0], strict=True)),
        tuple(denominator * a - b for a, b in zip(left[1], transformed[1], strict=True)),
    )


def internal_edges(points):
    answer = set()
    for high, first in enumerate(points):
        for low, second in enumerate(points[:high]):
            if squared_norm((sub(first[0], second[0]), sub(first[1], second[1]))) == UNIT:
                answer.add((low, high))
    return answer


def lower_scaled(field):
    answer = field[0] * SCALE
    for coefficient, floor in zip(field[1:], ROOT_FLOORS[1:], strict=True):
        answer += coefficient * (floor if coefficient >= 0 else floor + 1)
    return answer


def bucket(difference, denominator):
    coordinate_denominator = SCALE * 96 * denominator
    widths = tuple(sum(abs(value) for value in field[1:]) for field in difference)
    if any(10**6 * width >= coordinate_denominator for width in widths):
        raise AssertionError("interval is too wide")
    return tuple(4 * lower_scaled(field) // coordinate_denominator for field in difference)


def unit_separated(first, second, denominator):
    vector = (sub(first[0], second[0]), sub(first[1], second[1]))
    return squared_norm(vector) == ((96 * denominator) ** 2,) + (0,) * 7


def new_edge(pair, overlaps, left_edges, small_edges):
    p, q = divmod(pair, 136)
    q_vertex = 374 + q
    for overlap in overlaps:
        overlap_p, overlap_q = divmod(overlap, 136)
        if q == overlap_q:
            q_vertex = overlap_p
            if tuple(sorted((p, overlap_p))) in left_edges:
                return None
        if p == overlap_p and tuple(sorted((q, overlap_q))) in small_edges:
            return None
    if q_vertex < 374:
        raise AssertionError("unremoved internal L edge")
    return p, q


def read_libraries(path: Path):
    left, small = [], []
    for line in path.read_text(encoding="ascii").splitlines():
        if line.startswith("L:"):
            left.append(tuple(map(int, line[2:])))
        elif line.startswith("S:"):
            small.append(tuple(map(int, line[2:])))
    if (len(left), len(small)) != (135, 194):
        raise AssertionError((len(left), len(small)))
    return left, small


@lru_cache(maxsize=None)
def compatible(left_pattern, small_pattern):
    return any(
        permutation[small_pattern[0]] == left_pattern[0]
        and permutation[small_pattern[1]] == left_pattern[1]
        and all(
            permutation[small_pattern[index]] != left_pattern[index]
            for index in range(2, 5)
        )
        for permutation in PERMUTATIONS
    )


def absorbed(overlaps, edges, left_colours, small_colours):
    left_vertices = [divmod(pair, 136)[0] for pair in overlaps] + [p for p, _ in edges]
    small_vertices = [divmod(pair, 136)[1] for pair in overlaps] + [q for _, q in edges]
    left_patterns = {
        tuple(colours[vertex] for vertex in left_vertices) for colours in left_colours
    }
    small_patterns = {
        tuple(colours[vertex] for vertex in small_vertices) for colours in small_colours
    }
    return any(
        compatible(left_pattern, small_pattern)
        for left_pattern in left_patterns
        for small_pattern in small_patterns
    )


def check_orientation(orientation, left, small, left_edges, small_edges, libraries):
    denominator = orientation[1]
    image = [transformed_numerator(orientation, point) for point in small]
    differences = defaultdict(list)
    for p, left_point in enumerate(left):
        for q, small_point in enumerate(image):
            differences[cross_difference(left_point, small_point, denominator)].append(136 * p + q)
    grid = defaultdict(list)
    for difference in differences:
        grid[bucket(difference, denominator)].append(difference)

    categories = Counter()
    topologies = Counter()
    absorbed_count = 0
    exact_two = 0
    for translation, overlaps in differences.items():
        if len(overlaps) != 2:
            continue
        exact_two += 1
        centre = bucket(translation, denominator)
        genuine = set()
        for dx in range(-6, 7):
            for dy in range(-6, 7):
                for difference in grid.get((centre[0] + dx, centre[1] + dy), ()):
                    if not unit_separated(translation, difference, denominator):
                        continue
                    for pair in differences[difference]:
                        edge = new_edge(pair, overlaps, left_edges, small_edges)
                        if edge is not None:
                            genuine.add(edge)
        categories[min(len(genuine), 4)] += 1
        if len(genuine) == 3:
            edges = sorted(genuine)
            topology = (len({p for p, _ in edges}), len({q for _, q in edges}))
            topologies[topology] += 1
            if not absorbed(overlaps, edges, *libraries):
                raise AssertionError(("unabsorbed", overlaps, edges))
            absorbed_count += 1
    return exact_two, categories, topologies, absorbed_count


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: independent_parts_orientation.py POINTS LIBRARIES")
    points = read_points(Path(sys.argv[1]))
    left = points[:374]
    small = [points[0], *points[374:]]
    left_edges, small_edges = internal_edges(left), internal_edges(small)
    left_vectors, small_vectors = directed_vectors(left), directed_vectors(small)
    all_orientations = orientations(left_vectors, small_vectors)
    # These are the rotation/reflection rows with the largest exact-three
    # stratum in the committed transcript (471 placements apiece).
    selected_indices = (114, 1541)
    libraries = read_libraries(Path(sys.argv[2]))
    print(f"orientations={len(all_orientations)}")
    print(f"rotations={sum(not item[0] for item in all_orientations)}")
    print(f"left_vectors={sum(map(len, left_vectors.values()))}")
    print(f"small_vectors={sum(map(len, small_vectors.values()))}")
    print(f"left_edges={len(left_edges)} small_edges={len(small_edges)}")
    for index in selected_indices:
        orientation = all_orientations[index]
        exact_two, categories, topologies, absorbed_count = check_orientation(
            orientation, left, small, left_edges, small_edges, libraries
        )
        print(f"orientation={index} reflected={orientation[0]} exact_two={exact_two}")
        print("categories=" + ",".join(str(categories[index]) for index in range(5)))
        print(
            "three_topologies="
            + ",".join(
                f"{a}:{b}:{topologies[(a, b)]}"
                for a, b in ((1, 3), (3, 1), (2, 2), (2, 3), (3, 2), (3, 3))
            )
        )
        print(f"three_absorbed={absorbed_count}")
    print("independent_orientation_checks=true")


if __name__ == "__main__":
    main()
