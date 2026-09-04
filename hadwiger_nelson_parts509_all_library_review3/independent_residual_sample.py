#!/usr/bin/env python3
"""Independently check geometry and noncomposition for residual samples."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parent.parent
PRIOR_REVIEW = REPOSITORY / "hadwiger_nelson_parts509_six_edge_review3"
sys.path.insert(0, str(PRIOR_REVIEW))
import independent_dense_orientation as prior  # noqa: E402

exact = prior.exact
SAMPLE_POSITIONS = (101, 303, 505, 707, 909, 1111, 1515, 1717, 1919, 2121, 2323, 2525)


def check_case(case, orientations, left, small, left_edges, small_edges, libraries):
    orientation = orientations[case["orientation"]]
    if orientation[0] != int(case["orientation"] >= 1420):
        raise AssertionError("orientation parity mismatch")
    if orientation[1] != case["denominator"]:
        raise AssertionError("orientation denominator mismatch")
    image = [exact.transformed_numerator(orientation, point) for point in small]
    overlaps = case["overlaps"]
    first_p, first_q = divmod(overlaps[0], 136)
    second_p, second_q = divmod(overlaps[1], 136)
    translation = exact.cross_difference(
        left[first_p], image[first_q], orientation[1]
    )
    if translation != (tuple(case["x"]), tuple(case["y"])):
        raise AssertionError("translation coefficient mismatch")
    if translation != exact.cross_difference(
        left[second_p], image[second_q], orientation[1]
    ):
        raise AssertionError("second overlap mismatch")

    edges = set()
    for p, left_point in enumerate(left):
        for q, small_point in enumerate(image):
            difference = exact.cross_difference(left_point, small_point, orientation[1])
            if not exact.unit_separated(translation, difference, orientation[1]):
                continue
            edge = exact.new_edge(136 * p + q, overlaps, left_edges, small_edges)
            if edge is not None:
                edges.add(edge)
    ordered = sorted(edges)
    encoded = [510 * p + 374 + q for p, q in ordered]
    if encoded != case["edges"]:
        raise AssertionError("direct cross-edge reconstruction mismatch")
    if prior.absorbed(overlaps, ordered, *libraries):
        raise AssertionError("reported residual has a compatible library pair")
    return len(ordered)


def main():
    if len(sys.argv) != 4:
        raise SystemExit(
            "usage: independent_residual_sample.py POINTS LIBRARIES RESIDUAL.jsonl"
        )
    points = exact.read_points(Path(sys.argv[1]))
    left = points[:374]
    small = [points[0], *points[374:]]
    left_edges = exact.internal_edges(left)
    small_edges = exact.internal_edges(small)
    libraries = exact.read_libraries(Path(sys.argv[2]))
    prior.validate_libraries(libraries, left_edges, small_edges)
    orientations = exact.orientations(
        exact.directed_vectors(left), exact.directed_vectors(small)
    )
    cases = [json.loads(line) for line in Path(sys.argv[3]).read_text().splitlines()]
    if len(cases) != 2772 or len(orientations) != 2840:
        raise AssertionError("input census mismatch")
    print(f"residual_cases={len(cases)}")
    for position in SAMPLE_POSITIONS:
        case = cases[position]
        edge_count = check_case(
            case, orientations, left, small, left_edges, small_edges, libraries
        )
        print(
            f"sample_position={position} orientation={case['orientation']} "
            f"overlaps={case['overlaps']} new_edges={edge_count}"
        )
    print("independent_sample_geometry_and_noncomposition=true")


if __name__ == "__main__":
    main()
