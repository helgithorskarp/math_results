#!/usr/bin/env python3
"""Check the densest exact-six Parts orientation with independent arithmetic."""

from __future__ import annotations

import sys
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parent.parent
PRIOR_REVIEW = REPOSITORY / "hadwiger_nelson_parts509_three_edge_review3"
sys.path.insert(0, str(PRIOR_REVIEW))
import independent_orientation_check as exact  # noqa: E402


def canonical(pattern):
    rename = {}
    return tuple(rename.setdefault(value, len(rename)) for value in pattern)


@lru_cache(maxsize=None)
def compatible(left, small):
    """Test extendability to a colour permutation by explicit matching."""
    image = {}
    used = set()
    for source, target in zip(small[:2], left[:2], strict=True):
        if source in image and image[source] != target:
            return False
        if source not in image and target in used:
            return False
        image[source] = target
        used.add(target)
    for source, target in zip(small[2:], left[2:], strict=True):
        if image.get(source) == target:
            return False

    masks = []
    for source in sorted(set(small) - image.keys()):
        allowed = set(range(4)) - used
        for position in range(2, len(small)):
            if small[position] == source:
                allowed.discard(left[position])
        if not allowed:
            return False
        masks.append(allowed)

    masks.sort(key=len)

    def inject(index, occupied):
        if index == len(masks):
            return True
        return any(
            inject(index + 1, occupied | {target})
            for target in masks[index] - occupied
        )

    return inject(0, set())


def absorbed(overlaps, edges, left_colours, small_colours):
    left_vertices = [divmod(pair, 136)[0] for pair in overlaps]
    left_vertices += [left for left, _ in edges]
    small_vertices = [divmod(pair, 136)[1] for pair in overlaps]
    small_vertices += [small for _, small in edges]
    left_patterns = {
        canonical(tuple(row[vertex] for vertex in left_vertices))
        for row in left_colours
    }
    small_patterns = {
        canonical(tuple(row[vertex] for vertex in small_vertices))
        for row in small_colours
    }
    return any(
        compatible(left, small)
        for left in left_patterns
        for small in small_patterns
    )


def validate_libraries(libraries, left_edges, small_edges):
    for rows, edges, vertex_count in (
        (libraries[0], left_edges, 374),
        (libraries[1], small_edges, 136),
    ):
        for row in rows:
            if len(row) != vertex_count or any(not 0 <= value < 4 for value in row):
                raise AssertionError("invalid colour row")
            if any(row[first] == row[second] for first, second in edges):
                raise AssertionError("improper library colouring")


def check_orientation(
    orientation, left, small, left_edges, small_edges, libraries
):
    denominator = orientation[1]
    image = [exact.transformed_numerator(orientation, point) for point in small]
    differences = defaultdict(list)
    for left_index, left_point in enumerate(left):
        for small_index, small_point in enumerate(image):
            difference = exact.cross_difference(left_point, small_point, denominator)
            differences[difference].append(136 * left_index + small_index)
    grid = defaultdict(list)
    for difference in differences:
        grid[exact.bucket(difference, denominator)].append(difference)

    categories = Counter()
    exact_two = 0
    absorbed_six = 0
    for translation, overlaps in differences.items():
        if len(overlaps) != 2:
            continue
        exact_two += 1
        centre = exact.bucket(translation, denominator)
        genuine = set()
        for dx in range(-6, 7):
            for dy in range(-6, 7):
                for difference in grid.get((centre[0] + dx, centre[1] + dy), ()):
                    if not exact.unit_separated(translation, difference, denominator):
                        continue
                    for pair in differences[difference]:
                        edge = exact.new_edge(pair, overlaps, left_edges, small_edges)
                        if edge is not None:
                            genuine.add(edge)
        categories[min(len(genuine), 7)] += 1
        if len(genuine) == 6:
            if not absorbed(overlaps, sorted(genuine), *libraries):
                raise AssertionError(("unabsorbed", overlaps, sorted(genuine)))
            absorbed_six += 1
    return exact_two, categories, absorbed_six


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: independent_dense_orientation.py POINTS LIBRARIES")
    points = exact.read_points(Path(sys.argv[1]))
    left = points[:374]
    small = [points[0], *points[374:]]
    left_edges = exact.internal_edges(left)
    small_edges = exact.internal_edges(small)
    libraries = exact.read_libraries(Path(sys.argv[2]))
    validate_libraries(libraries, left_edges, small_edges)
    left_vectors = exact.directed_vectors(left)
    small_vectors = exact.directed_vectors(small)
    orientations = exact.orientations(left_vectors, small_vectors)
    orientation_index = 78
    exact_two, categories, absorbed_six = check_orientation(
        orientations[orientation_index], left, small, left_edges, small_edges, libraries
    )
    print(f"orientations={len(orientations)}")
    print(f"left_edges={len(left_edges)} small_edges={len(small_edges)}")
    print(
        f"orientation={orientation_index} "
        f"reflected={orientations[orientation_index][0]} exact_two={exact_two}"
    )
    print("categories=" + ",".join(str(categories[index]) for index in range(8)))
    print(f"six_absorbed={absorbed_six}")
    print("independent_dense_orientation_check=true")


if __name__ == "__main__":
    main()
