#!/usr/bin/env python3
"""Check the densest exact-seven Parts orientation independently."""

from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parent.parent
PRIOR_REVIEW = REPOSITORY / "hadwiger_nelson_parts509_six_edge_review3"
sys.path.insert(0, str(PRIOR_REVIEW))
import independent_dense_orientation as prior  # noqa: E402

exact = prior.exact


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
    absorbed_seven = 0
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
        categories[min(len(genuine), 8)] += 1
        if len(genuine) == 7:
            if not prior.absorbed(overlaps, sorted(genuine), *libraries):
                raise AssertionError(("unabsorbed", overlaps, sorted(genuine)))
            absorbed_seven += 1
    return exact_two, categories, absorbed_seven


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: independent_dense_orientation.py POINTS LIBRARIES")
    points = exact.read_points(Path(sys.argv[1]))
    left = points[:374]
    small = [points[0], *points[374:]]
    left_edges = exact.internal_edges(left)
    small_edges = exact.internal_edges(small)
    libraries = exact.read_libraries(Path(sys.argv[2]))
    prior.validate_libraries(libraries, left_edges, small_edges)
    left_vectors = exact.directed_vectors(left)
    small_vectors = exact.directed_vectors(small)
    orientations = exact.orientations(left_vectors, small_vectors)
    orientation_index = 23
    exact_two, categories, absorbed_seven = check_orientation(
        orientations[orientation_index], left, small, left_edges, small_edges, libraries
    )
    print(f"orientations={len(orientations)}")
    print(f"left_edges={len(left_edges)} small_edges={len(small_edges)}")
    print(
        f"orientation={orientation_index} "
        f"reflected={orientations[orientation_index][0]} exact_two={exact_two}"
    )
    print("categories=" + ",".join(str(categories[index]) for index in range(9)))
    print(f"seven_absorbed={absorbed_seven}")
    print("independent_dense_orientation_check=true")


if __name__ == "__main__":
    main()
