#!/usr/bin/env python3
"""Independent controls for the E457 paired-hexagon review."""

from itertools import combinations
from json import dumps

import verify as V
import union_check as U


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    require(V.mul(V.SQRT3, V.SQRT3) == V.scalar(3), "sqrt3 square")
    require(V.mul(V.SQRT47, V.SQRT47) == V.scalar(47), "sqrt47 square")
    require(V.mul(V.SQRT3, V.SQRT47) == V.SQRT141, "mixed radical")
    require(V.mul(V.SQRT141, V.SQRT141) == V.scalar(141), "sqrt141 square")
    require(U.mul(U.SQRT3, U.SQRT3) == U.scale(U.ONE, 3), "union sqrt3 square")
    require(U.mul(U.SQRT11, U.SQRT11) == U.scale(U.ONE, 11), "union sqrt11 square")
    require(U.mul(U.SQRT47, U.SQRT47) == U.scale(U.ONE, 47), "union sqrt47 square")
    require(U.mul(U.SQRT3, U.SQRT11) == U.SQRT33, "union sqrt33 product")
    require(U.mul(U.SQRT3, U.SQRT47) == U.SQRT141, "union sqrt141 product")

    points = V.connector_points()
    rotation_point_controls = 0
    rotation_distance_controls = 0
    for point in points:
        rotated = point
        for _ in range(6):
            rotated = V.rotate60(rotated)
        require(rotated == point, "rotation closure control")
        rotation_point_controls += 1
    rotated_points = tuple(V.rotate60(point) for point in points)
    for left, right in combinations(range(14), 2):
        require(V.norm2(V.psub(points[left], points[right])) ==
                V.norm2(V.psub(rotated_points[left], rotated_points[right])),
                "rotation distance control")
        rotation_distance_controls += 1

    # Compare the independently represented connector coordinates entrywise:
    # nested Q(sqrt(3))[sqrt(47)] versus the eight-basis union field.
    def to_union(value):
        a, b, c, d = V.flatten(value)
        return U.add(U.add(U.scale(U.ONE, a), U.scale(U.SQRT3, b)),
                     U.add(U.scale(U.SQRT47, c), U.scale(U.SQRT141, d)))

    union_horizontal = U.connector_points_horizontal()
    for nested, generic in zip(points, union_horizontal):
        require((to_union(nested[0]), to_union(nested[1])) == generic,
                "cross-representation coordinate control")
    for name, alignment in U.connector_alignments().items():
        require(alignment[0] == (U.ZERO, U.ZERO), name + " origin")
        require(alignment[1] == (U.ZERO, U.scale(U.ONE, U.Q(8, 3))), name + " terminal")

    # Every labelled K2,2-minus-edge pattern is equivalent to the canonical
    # pattern under independent swaps of the two adjacent vertices.
    universe = {(left, right) for left in range(2) for right in range(2)}
    canonical = {(0, 0), (0, 1), (1, 0)}
    triple_symmetry_controls = 0
    for triple in combinations(sorted(universe), 3):
        triple = set(triple)
        images = []
        for swap_left in range(2):
            for swap_right in range(2):
                images.append({(left ^ swap_left, right ^ swap_right) for left, right in triple})
        require(canonical in images, "K2,2 triple symmetry")
        triple_symmetry_controls += 1

    # Damage one coordinate and both positive colouring certificates.
    damaged_points = list(points)
    damaged_points[2] = V.padd(damaged_points[2], (V.scale(V.ONE, V.Q(1, 1000)), V.ZERO))
    require(V.complete_edges(damaged_points) != V.complete_edges(points), "damaged geometry accepted")
    edges = V.complete_edges(points)
    equal_word = list("33010101121212")
    equal_word[8] = equal_word[2]
    require(not V.proper("".join(equal_word), edges, 4), "bad four-word accepted")
    three_word = list("01121212020202")
    three_word[2] = three_word[0]
    require(not V.proper("".join(three_word), edges, 3), "bad three-word accepted")
    require(not V.rational_square(V.Q(47, 3)) and V.rational_square(V.Q(49, 9)),
            "rational-square controls")

    result = {
        "all_controls_passed": True,
        "field_basis_controls": 4,
        "union_field_basis_controls": 5,
        "cross_representation_point_controls": 14,
        "ordered_terminal_alignment_controls": 2,
        "rotation_point_controls": rotation_point_controls,
        "rotation_distance_controls": rotation_distance_controls,
        "k22_labelled_triple_symmetry_controls": triple_symmetry_controls,
        "corruption_controls": 4,
    }
    print(dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
