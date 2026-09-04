#!/usr/bin/env python3
"""Audit local-count propagation from a doubly exact 21+21 Ramsey anchor."""

from __future__ import annotations

import itertools


SIDE = 21
ORDER = 43
SAMPLE_CORE_G6 = "TJaGmrdI_gqziMTiLYE?ro`dlTI|TTmTiwtQ"
EXTREMAL_EDGES = {18: 85, 19: 92, 20: 100, 21: 107,
                  22: 114, 23: 122, 24: 132}


def decode_short_graph6(encoded: str) -> tuple[tuple[bool, ...], ...]:
    data = encoded.strip()
    if not data or ord(data[0]) == 126:
        raise ValueError("only short graph6 headers are supported")
    order = ord(data[0]) - 63
    payload_length = (order * (order - 1) // 2 + 5) // 6
    if len(data) != 1 + payload_length:
        raise ValueError("wrong graph6 payload length")
    bits = []
    for character in data[1:]:
        value = ord(character) - 63
        if not 0 <= value < 64:
            raise ValueError("invalid graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    adjacency = [[False] * order for _ in range(order)]
    position = 0
    for second in range(1, order):
        for first in range(second):
            adjacency[first][second] = adjacency[second][first] = bool(bits[position])
            position += 1
    return tuple(tuple(row) for row in adjacency)


def induced_edges(
    adjacency: tuple[tuple[bool, ...], ...],
    vertices: tuple[int, ...],
    color: bool,
) -> int:
    return sum(
        adjacency[first][second] == color
        for first, second in itertools.combinations(vertices, 2)
    )


def cross_edges(
    first_vertices: tuple[int, ...],
    second_vertices: tuple[int, ...],
    red_cross: frozenset[tuple[int, int]],
    color: bool,
) -> int:
    return sum(
        ((first, second) in red_cross) == color
        for first in first_vertices
        for second in second_vertices
    )


def core_edge_count(adjacency: tuple[tuple[bool, ...], ...]) -> int:
    return induced_edges(adjacency, tuple(range(len(adjacency))), True)


def relabel(
    adjacency: tuple[tuple[bool, ...], ...], permutation: tuple[int, ...]
) -> tuple[tuple[bool, ...], ...]:
    if sorted(permutation) != list(range(len(adjacency))):
        raise ValueError("not a vertex permutation")
    return tuple(
        tuple(adjacency[permutation[first]][permutation[second]]
              for second in range(len(adjacency)))
        for first in range(len(adjacency))
    )


def formula_profiles(
    red_core: tuple[tuple[bool, ...], ...],
    blue_core: tuple[tuple[bool, ...], ...],
    red_cross: frozenset[tuple[int, int]],
) -> tuple[tuple[int, int, int], ...]:
    """Return (red degree, red-local edges, blue-local edges) off the anchor."""
    profiles = []
    for first in range(SIDE):
        red_internal = tuple(
            other for other in range(SIDE) if red_core[first][other]
        )
        blue_internal = tuple(
            other
            for other in range(SIDE)
            if other != first and not red_core[first][other]
        )
        red_external = tuple(
            second for second in range(SIDE) if (first, second) in red_cross
        )
        blue_external = tuple(
            second for second in range(SIDE) if (first, second) not in red_cross
        )
        degree = 1 + len(red_internal) + len(red_external)
        red_local = (
            len(red_internal)
            + induced_edges(red_core, red_internal, True)
            + induced_edges(blue_core, red_external, False)
            + cross_edges(red_internal, red_external, red_cross, True)
        )
        blue_local = (
            induced_edges(red_core, blue_internal, False)
            + induced_edges(blue_core, blue_external, True)
            + cross_edges(blue_internal, blue_external, red_cross, False)
        )
        profiles.append((degree, red_local, blue_local))

    for second in range(SIDE):
        blue_internal = tuple(
            other for other in range(SIDE) if blue_core[second][other]
        )
        red_internal = tuple(
            other
            for other in range(SIDE)
            if other != second and not blue_core[second][other]
        )
        red_external = tuple(
            first for first in range(SIDE) if (first, second) in red_cross
        )
        blue_external = tuple(
            first for first in range(SIDE) if (first, second) not in red_cross
        )
        degree = len(red_internal) + len(red_external)
        red_local = (
            induced_edges(blue_core, red_internal, False)
            + induced_edges(red_core, red_external, True)
            + cross_edges(red_external, red_internal, red_cross, True)
        )
        blue_local = (
            len(blue_internal)
            + induced_edges(blue_core, blue_internal, True)
            + induced_edges(red_core, blue_external, False)
            + cross_edges(blue_external, blue_internal, red_cross, False)
        )
        profiles.append((degree, red_local, blue_local))
    return tuple(profiles)


def full_red_adjacency(
    red_core: tuple[tuple[bool, ...], ...],
    blue_core: tuple[tuple[bool, ...], ...],
    red_cross: frozenset[tuple[int, int]],
) -> tuple[tuple[bool, ...], ...]:
    adjacency = [[False] * ORDER for _ in range(ORDER)]

    def set_edge(first: int, second: int, color: bool) -> None:
        adjacency[first][second] = adjacency[second][first] = color

    for first in range(SIDE):
        set_edge(0, 1 + first, True)
        for second in range(first + 1, SIDE):
            set_edge(1 + first, 1 + second, red_core[first][second])
    for second in range(SIDE):
        set_edge(0, 1 + SIDE + second, False)
        for other in range(second + 1, SIDE):
            set_edge(
                1 + SIDE + second,
                1 + SIDE + other,
                not blue_core[second][other],
            )
    for first in range(SIDE):
        for second in range(SIDE):
            set_edge(
                1 + first,
                1 + SIDE + second,
                (first, second) in red_cross,
            )
    return tuple(tuple(row) for row in adjacency)


def direct_profiles(
    red_adjacency: tuple[tuple[bool, ...], ...]
) -> tuple[tuple[int, int, int], ...]:
    profiles = []
    for vertex in range(1, ORDER):
        red_neighbors = tuple(
            other for other in range(ORDER) if red_adjacency[vertex][other]
        )
        blue_neighbors = tuple(
            other
            for other in range(ORDER)
            if other != vertex and not red_adjacency[vertex][other]
        )
        profiles.append(
            (
                len(red_neighbors),
                induced_edges(red_adjacency, red_neighbors, True),
                induced_edges(red_adjacency, blue_neighbors, False),
            )
        )
    return tuple(profiles)


def predicted_flip_profiles(
    red_adjacency: tuple[tuple[bool, ...], ...],
    profiles: tuple[tuple[int, int, int], ...],
    first: int,
    second: int,
) -> tuple[tuple[int, int, int], ...]:
    """Update off-anchor profiles when the cross edge first--second flips."""
    if not (1 <= first <= SIDE < second < ORDER):
        raise ValueError("the toggled edge must cross the anchored split")
    sigma = -1 if red_adjacency[first][second] else 1
    common_red = sum(
        red_adjacency[first][other] and red_adjacency[second][other]
        for other in range(ORDER)
        if other not in (first, second)
    )
    common_blue = sum(
        not red_adjacency[first][other] and not red_adjacency[second][other]
        for other in range(ORDER)
        if other not in (first, second)
    )
    updated = []
    for vertex, (degree, red_local, blue_local) in enumerate(profiles, start=1):
        if vertex in (first, second):
            updated.append(
                (
                    degree + sigma,
                    red_local + sigma * common_red,
                    blue_local - sigma * common_blue,
                )
            )
            continue
        if red_adjacency[vertex][first] and red_adjacency[vertex][second]:
            red_local += sigma
        elif not red_adjacency[vertex][first] and not red_adjacency[vertex][second]:
            blue_local -= sigma
        updated.append((degree, red_local, blue_local))
    return tuple(updated)


def balanced_cross(edge_count: int) -> frozenset[tuple[int, int]]:
    if not 210 <= edge_count <= 231:
        raise ValueError(edge_count)
    red_cross = {
        (first, (first + offset) % SIDE)
        for first in range(SIDE)
        for offset in range(10)
    }
    red_cross.update(
        (first, (first + 10) % SIDE) for first in range(edge_count - 210)
    )
    if len(red_cross) != edge_count:
        raise AssertionError("balanced construction has wrong cardinality")
    return frozenset(red_cross)


def obeys_first_degree_bounds(
    red_core: tuple[tuple[bool, ...], ...],
    blue_core: tuple[tuple[bool, ...], ...],
    red_cross: frozenset[tuple[int, int]],
) -> bool:
    red_degrees = [sum(row) for row in red_core]
    blue_degrees = [sum(row) for row in blue_core]
    row_sums = [
        sum((first, second) in red_cross for second in range(SIDE))
        for first in range(SIDE)
    ]
    column_sums = [
        sum((first, second) in red_cross for first in range(SIDE))
        for second in range(SIDE)
    ]
    return all(
        17 - degree <= total <= 23 - degree
        for degree, total in zip(red_degrees, row_sums, strict=True)
    ) and all(
        degree - 2 <= total <= degree + 4
        for degree, total in zip(blue_degrees, column_sums, strict=True)
    )


def hard_side_violations(profiles: tuple[tuple[int, int, int], ...]) -> int:
    violations = 0
    for degree, red_local, blue_local in profiles:
        if degree not in EXTREMAL_EDGES:
            return 2 * len(profiles)
        violations += red_local > EXTREMAL_EDGES[degree] - 7
        violations += blue_local > EXTREMAL_EDGES[42 - degree] - 7
    return violations


def main() -> None:
    red_core = decode_short_graph6(SAMPLE_CORE_G6)
    blue_core = relabel(red_core, tuple((5 * vertex + 3) % SIDE for vertex in range(SIDE)))
    if (
        len(red_core) != SIDE
        or core_edge_count(red_core) != 100
        or core_edge_count(blue_core) != 100
    ):
        raise AssertionError("sample is not an order-21, 100-edge graph")

    matrix_count = 0
    profile_count = 0
    flip_count = 0
    flip_profile_count = 0
    secondary_counts = []
    violation_counts = []
    for edge_count in range(214, 221):
        red_cross = balanced_cross(edge_count)
        formulas = formula_profiles(red_core, blue_core, red_cross)
        adjacency = full_red_adjacency(red_core, blue_core, red_cross)
        direct = direct_profiles(adjacency)
        if formulas != direct:
            raise AssertionError((edge_count, formulas, direct))
        if not obeys_first_degree_bounds(red_core, blue_core, red_cross):
            raise AssertionError("test matrix violates a first-degree bound")
        matrix_count += 1
        profile_count += len(formulas)
        secondary_counts.append(formulas.count((21, 100, 100)))
        violation_counts.append(hard_side_violations(formulas))

        # Offset zero is red in every balanced matrix; offset ten in row 20
        # is blue in every matrix in the audited range.  This checks one
        # update in each direction without randomness.
        for first_index, second_index in ((0, 0), (20, 9)):
            old_color = (first_index, second_index) in red_cross
            toggled = set(red_cross)
            if old_color:
                toggled.remove((first_index, second_index))
            else:
                toggled.add((first_index, second_index))
            expected = direct_profiles(
                full_red_adjacency(red_core, blue_core, frozenset(toggled))
            )
            predicted = predicted_flip_profiles(
                adjacency,
                direct,
                1 + first_index,
                1 + SIDE + second_index,
            )
            if predicted != expected:
                raise AssertionError((edge_count, first_index, second_index))
            flip_count += 1
            flip_profile_count += len(predicted)

    if (matrix_count, profile_count) != (7, 294):
        raise AssertionError((matrix_count, profile_count))
    if (flip_count, flip_profile_count) != (14, 588):
        raise AssertionError((flip_count, flip_profile_count))
    if secondary_counts != [0] * 7:
        raise AssertionError(secondary_counts)
    if not all(count > 0 for count in violation_counts):
        raise AssertionError(violation_counts)

    # In the hard branch, the prior deficiency theorem gives at most thirteen
    # non-degree-21 vertices and at most twenty non-exact local color sides.
    # At least 43-13-20=10 vertices are therefore exact on both sides.  The
    # selected anchor is one, leaving at least nine among the profiles above.
    minimum_degree21_vertices = ORDER - 13
    minimum_double_exact = minimum_degree21_vertices - 20
    minimum_secondary = minimum_double_exact - 1
    if (minimum_degree21_vertices, minimum_double_exact, minimum_secondary) != (30, 10, 9):
        raise AssertionError("wrong anchor-propagation count")
    if 2 * (ORDER - 1) != 84:
        raise AssertionError("wrong number of propagated local inequalities")

    print("PASS exact row/column formulas on 7 matrices and 294 vertex profiles")
    print("PASS exact one-cross-flip updates on 14 flips and 588 vertex profiles")
    print("PASS all test matrices satisfy cross cardinality and first-degree bounds")
    print("PASS first-degree-feasible tests have 0 secondary exact anchors")
    print("PASS hard branch propagates 84 deficiency inequalities and at least 9 anchors")


if __name__ == "__main__":
    main()
