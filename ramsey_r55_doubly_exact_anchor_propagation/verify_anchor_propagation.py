#!/usr/bin/env python3
"""Audit local-count propagation from a doubly exact 21+21 Ramsey anchor."""

from __future__ import annotations

import hashlib
import itertools
from pathlib import Path


SIDE = 21
ORDER = 43
SAMPLE_CORE_G6 = "TJaGmrdI_gqziMTiLYE?ro`dlTI|TTmTiwtQ"
EXTREMAL_R4514_G6 = "MznZ\\lle{vYVlhsm_"
EXTREMAL_EDGES = {18: 85, 19: 92, 20: 100, 21: 107,
                  22: 114, 23: 122, 24: 132}
SMALL_EXTREMAL_EDGES = {14: 60, 15: 66, 16: 72, 17: 79, 18: 85}
R35_EDGE_COVER_HISTOGRAMS = {
    9: {
        (7, 2): 1,
        (8, 2): 3,
        (9, 2): 10, (9, 3): 1,
        (10, 1): 1, (10, 2): 27,
        (11, 1): 3, (11, 2): 56,
        (12, 1): 8, (12, 2): 65,
        (13, 1): 8, (13, 2): 54,
        (14, 1): 5, (14, 2): 28,
        (15, 1): 1, (15, 2): 13,
        (16, 2): 4,
        (17, 2): 2,
    },
    10: {
        (10, 3): 1,
        (11, 2): 1, (11, 3): 1,
        (12, 2): 3, (12, 3): 7,
        (13, 2): 15, (13, 3): 17,
        (14, 2): 37, (14, 3): 32,
        (15, 2): 59, (15, 3): 27,
        (16, 2): 48, (16, 3): 17,
        (17, 2): 24, (17, 3): 8,
        (18, 2): 8, (18, 3): 4,
        (19, 2): 2, (19, 3): 1,
        (20, 3): 1,
    },
    11: {
        (15, 3): 1, (16, 3): 6, (17, 3): 19, (18, 3): 31,
        (19, 3): 30, (20, 3): 13, (21, 3): 4, (22, 3): 1,
    },
    12: {(20, 4): 1, (21, 4): 2, (22, 4): 5, (23, 4): 2, (24, 4): 2},
    13: {(26, 5): 1},
}
R35_EDGE_HISTOGRAMS = {
    order: {
        edge_count: sum(
            count
            for (candidate_edges, _), count in histogram.items()
            if candidate_edges == edge_count
        )
        for edge_count in sorted({entry[0] for entry in histogram})
    }
    for order, histogram in R35_EDGE_COVER_HISTOGRAMS.items()
}
MINIMUM_R35_EDGES = {
    order: min(histogram)
    for order, histogram in R35_EDGE_HISTOGRAMS.items()
}
DEGREE_WEIGHTS = {18: 21, 19: 12, 20: 3, 21: 0,
                  22: 3, 23: 12, 24: 21}


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


def weak_compositions(total: int, parts: int):
    """Yield ordered weak compositions without relying on a solver."""
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for suffix in weak_compositions(total - first, parts - 1):
            yield (first,) + suffix


def hard_split_degree_profiles():
    """Enumerate side degree-count pairs allowed by (S) and (W39)."""
    degrees = tuple(range(18, 25))
    side_profiles = []
    for counts in weak_compositions(SIDE, len(degrees)):
        deviation = sum((degree - 21) * count
                        for degree, count in zip(degrees, counts, strict=True))
        weight = sum(DEGREE_WEIGHTS[degree] * count
                     for degree, count in zip(degrees, counts, strict=True))
        if weight <= 39:
            side_profiles.append((deviation, weight, counts))

    profiles_by_cross_count = {}
    for edge_count in range(214, 221):
        pairs = []
        for first_deviation, first_weight, first_counts in side_profiles:
            if first_deviation != edge_count - 220:
                continue
            for second_deviation, second_weight, second_counts in side_profiles:
                total_weight = first_weight + second_weight
                if (
                    second_deviation == edge_count - 221
                    and total_weight <= 39
                    and total_weight % 6 == 3
                ):
                    pairs.append((total_weight, first_counts, second_counts))
        profiles_by_cross_count[edge_count] = tuple(pairs)
    return profiles_by_cross_count


def turan_edges(order: int, parts: int) -> int:
    """Number of edges in the balanced complete `parts`-partite graph."""
    quotient, remainder = divmod(order, parts)
    class_sizes = [quotient + 1] * remainder + [quotient] * (parts - remainder)
    return (order * order - sum(size * size for size in class_sizes)) // 2


def clique_number(adjacency: tuple[tuple[bool, ...], ...]) -> int:
    """Return the clique number by exhaustive subset enumeration."""
    order = len(adjacency)
    for size in range(order, 0, -1):
        for vertices in itertools.combinations(range(order), size):
            if all(adjacency[first][second]
                   for first, second in itertools.combinations(vertices, 2)):
                return size
    return 0


def complement_adjacency(
    adjacency: tuple[tuple[bool, ...], ...]
) -> tuple[tuple[bool, ...], ...]:
    """Return the loopless complement of an adjacency matrix."""
    return tuple(
        tuple(first != second and not adjacency[first][second]
              for second in range(len(adjacency)))
        for first in range(len(adjacency))
    )


def minimum_triangle_transversal(
    adjacency: tuple[tuple[bool, ...], ...]
) -> tuple[int, int]:
    """Return the number of triangles and their minimum vertex-cover size."""
    triangles = tuple(
        vertices
        for vertices in itertools.combinations(range(len(adjacency)), 3)
        if all(adjacency[first][second]
               for first, second in itertools.combinations(vertices, 2))
    )
    for size in range(len(adjacency) + 1):
        if any(
            all(set(vertices).intersection(triangle) for triangle in triangles)
            for vertices in itertools.combinations(range(len(adjacency)), size)
        ):
            return len(triangles), size
    raise AssertionError("finite triangle family has no transversal")


def circulant_adjacency(
    order: int, positive_steps: tuple[int, ...]
) -> tuple[tuple[bool, ...], ...]:
    """Return the undirected circulant with the supplied positive steps."""
    residues = set(positive_steps)
    residues.update(order - step for step in positive_steps)
    return tuple(
        tuple(first != second and (second - first) % order in residues
              for second in range(order))
        for first in range(order)
    )


def triangle_pair_sieve(split_profiles):
    """Return admissible triangle pairs and maximum excess in each color."""
    degrees = tuple(range(18, 25))
    triangle_pairs = {}
    maximum_excess = {}
    for edge_count, pairs in split_profiles.items():
        values = set()
        maximum_red_excess = 0
        maximum_blue_excess = 0
        for weight, first_counts, second_counts in pairs:
            global_counts = [
                first_counts[index] + second_counts[index] + (degree == 21)
                for index, degree in enumerate(degrees)
            ]
            total_excess = (43 - weight) // 2
            red_baseline = sum(
                (EXTREMAL_EDGES[degree] - 7) * count
                for degree, count in zip(degrees, global_counts, strict=True)
            )
            blue_baseline = sum(
                (EXTREMAL_EDGES[42 - degree] - 7) * count
                for degree, count in zip(degrees, global_counts, strict=True)
            )
            for red_excess in range(total_excess + 1):
                blue_excess = total_excess - red_excess
                if (
                    (red_baseline - red_excess) % 3 == 0
                    and (blue_baseline - blue_excess) % 3 == 0
                ):
                    values.add(
                        (
                            (red_baseline - red_excess) // 3,
                            (blue_baseline - blue_excess) // 3,
                        )
                    )
                    maximum_red_excess = max(maximum_red_excess, red_excess)
                    maximum_blue_excess = max(maximum_blue_excess, blue_excess)
        triangle_pairs[edge_count] = tuple(sorted(values))
        maximum_excess[edge_count] = (maximum_red_excess, maximum_blue_excess)
    return triangle_pairs, maximum_excess


def component_pair_edge_histogram(
    first_order: int, second_order: int, backbone_order: int
) -> tuple[tuple[int, int], ...]:
    """Count cover-feasible R(3,5) type pairs by joined edge count.

    The returned edge count includes all edges between the two components.
    Components of different orders are distinguished by their orders.  For
    equal orders, swapping the two is not counted a second time.  A type is
    retained only if its forced cross-edge total can provide every outside
    vertex a transversal of its independent four-sets.
    """
    first_histogram = R35_EDGE_COVER_HISTOGRAMS[first_order]
    second_histogram = R35_EDGE_COVER_HISTOGRAMS[second_order]
    pair_counts: dict[int, int] = {}
    cross_edges = first_order * second_order
    outside_order = ORDER - backbone_order
    for (first_edges, first_cover), first_count in first_histogram.items():
        for (second_edges, second_cover), second_count in second_histogram.items():
            first_key = (first_edges, first_cover)
            second_key = (second_edges, second_cover)
            if first_order == second_order and first_key > second_key:
                continue
            if first_order == second_order and first_key == second_key:
                type_pairs = first_count * (first_count + 1) // 2
            else:
                type_pairs = first_count * second_count
            first_cross_edges = (
                first_order * (first_order + 21 - backbone_order)
                - 2 * first_edges
            )
            second_cross_edges = (
                second_order * (second_order + 21 - backbone_order)
                - 2 * second_edges
            )
            if (
                first_cross_edges < outside_order * first_cover
                or second_cross_edges < outside_order * second_cover
            ):
                continue
            total_edges = cross_edges + first_edges + second_edges
            pair_counts[total_edges] = pair_counts.get(total_edges, 0) + type_pairs
    return tuple(sorted(pair_counts.items()))


def excess_triangle_splits(
    weight: int,
    first_counts: tuple[int, ...],
    second_counts: tuple[int, ...],
) -> tuple[tuple[int, int, int, int], ...]:
    """Return all exact (red excess, blue excess, red/blue triangles)."""
    degrees = tuple(range(18, 25))
    global_counts = [
        first_counts[index] + second_counts[index] + (degree == 21)
        for index, degree in enumerate(degrees)
    ]
    total_excess = (43 - weight) // 2
    red_baseline = sum(
        (EXTREMAL_EDGES[degree] - 7) * count
        for degree, count in zip(degrees, global_counts, strict=True)
    )
    blue_baseline = sum(
        (EXTREMAL_EDGES[42 - degree] - 7) * count
        for degree, count in zip(degrees, global_counts, strict=True)
    )
    return tuple(
        (
            red_excess,
            total_excess - red_excess,
            (red_baseline - red_excess) // 3,
            (blue_baseline - (total_excess - red_excess)) // 3,
        )
        for red_excess in range(total_excess + 1)
        if (red_baseline - red_excess) % 3 == 0
        and (blue_baseline - (total_excess - red_excess)) % 3 == 0
    )


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
    degree_weights = []
    degree21_counts = []
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
        degrees = [profile[0] for profile in formulas]
        if (
            sum(degree - 21 for degree in degrees[:SIDE]) != edge_count - 220
            or sum(degree - 21 for degree in degrees[SIDE:]) != edge_count - 221
        ):
            raise AssertionError("wrong split degree-deviation identity")
        degree_weights.append(sum(DEGREE_WEIGHTS[degree] for degree in degrees))
        degree21_counts.append(degrees.count(21))

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
    if degree_weights != [105, 105, 111, 105, 105, 99, 105]:
        raise AssertionError(degree_weights)
    if degree21_counts != [19, 19, 17, 19, 19, 21, 19]:
        raise AssertionError(degree21_counts)

    # The prior theorem's uniform count gives 29 secondary degree-21 vertices.
    minimum_degree21_vertices = ORDER - 13
    minimum_secondary_degree21 = minimum_degree21_vertices - 1
    if (minimum_degree21_vertices, minimum_secondary_degree21) != (30, 29):
        raise AssertionError("wrong anchor-propagation count")
    if set(range(3, 40, 6)) != {3, 9, 15, 21, 27, 33, 39}:
        raise AssertionError("wrong hard degree-weight range")
    if 2 * (ORDER - 1) != 84:
        raise AssertionError("wrong number of propagated local inequalities")

    split_profiles = hard_split_degree_profiles()
    expected_histograms = {
        214: {39: 1},
        215: {33: 1, 39: 4},
        216: {27: 1, 33: 4, 39: 12},
        217: {21: 1, 27: 4, 33: 11, 39: 24},
        218: {15: 1, 21: 4, 27: 9, 33: 19, 39: 36},
        219: {9: 1, 15: 3, 21: 6, 27: 13, 33: 25, 39: 47},
        220: {3: 1, 9: 2, 15: 4, 21: 9, 27: 17, 33: 32, 39: 57},
    }
    for edge_count, pairs in split_profiles.items():
        histogram = {
            weight: sum(pair[0] == weight for pair in pairs)
            for weight in range(3, 40, 6)
            if any(pair[0] == weight for pair in pairs)
        }
        if histogram != expected_histograms[edge_count]:
            raise AssertionError((edge_count, histogram))
    split_counts = [len(split_profiles[edge_count]) for edge_count in range(214, 221)]
    if split_counts != [1, 5, 17, 40, 69, 95, 122] or sum(split_counts) != 349:
        raise AssertionError(split_counts)
    if split_profiles[214] != (
        (39, (0, 0, 6, 15, 0, 0, 0), (0, 0, 7, 14, 0, 0, 0)),
    ):
        raise AssertionError(split_profiles[214])

    triangle_pairs, maximum_color_excess = triangle_pair_sieve(split_profiles)
    triangle_pair_counts = [
        len(triangle_pairs[edge_count]) for edge_count in range(214, 221)
    ]
    triangle_ranges = [
        (
            min(red for red, _ in triangle_pairs[edge_count]),
            max(red for red, _ in triangle_pairs[edge_count]),
            min(blue for _, blue in triangle_pairs[edge_count]),
            max(blue for _, blue in triangle_pairs[edge_count]),
        )
        for edge_count in range(214, 221)
    ]
    expected_triangle_ranges = [
        (1403, 1403, 1463, 1463),
        (1406, 1407, 1458, 1459),
        (1410, 1412, 1452, 1455),
        (1414, 1417, 1446, 1451),
        (1417, 1422, 1441, 1446),
        (1421, 1427, 1435, 1442),
        (1425, 1432, 1429, 1437),
    ]
    exact_red_side_minima = [
        43 - maximum_color_excess[edge_count][0] for edge_count in range(214, 221)
    ]
    exact_blue_side_minima = [
        43 - maximum_color_excess[edge_count][1] for edge_count in range(214, 221)
    ]
    canonical_triangle_pairs = "".join(
        f"{edge_count} {red} {blue}\n"
        for edge_count in range(214, 221)
        for red, blue in triangle_pairs[edge_count]
    ).encode("ascii")
    triangle_pair_digest = hashlib.sha256(canonical_triangle_pairs).hexdigest()
    if triangle_pair_counts != [1, 3, 8, 15, 20, 27, 39] or sum(triangle_pair_counts) != 113:
        raise AssertionError(triangle_pair_counts)
    if triangle_ranges != expected_triangle_ranges:
        raise AssertionError(triangle_ranges)
    if exact_red_side_minima != [43, 38, 36, 34, 29, 27, 25]:
        raise AssertionError(exact_red_side_minima)
    if exact_blue_side_minima != [41, 40, 36, 32, 31, 27, 23]:
        raise AssertionError(exact_blue_side_minima)
    if triangle_pair_digest != "ccaf9ccec34aa4633cf2019d3f85f34e714c1f0bb17db444e9f8034c650c936c":
        raise AssertionError(triangle_pair_digest)

    # The unique M=214 split, plus the selected degree-21 anchor, has thirteen
    # degree-20 and thirty degree-21 vertices.  Divisibility of each color's
    # local-edge sum by three forces both excess-deficiency units to be blue.
    _, first_counts, second_counts = split_profiles[214][0]
    global_counts = [
        first_counts[index] + second_counts[index] + (degree == 21)
        for index, degree in enumerate(range(18, 25))
    ]
    if global_counts != [0, 0, 13, 30, 0, 0, 0]:
        raise AssertionError(global_counts)
    total_deficiency = (1247 - 39) // 2
    total_excess = total_deficiency - 86 * 7
    red_baseline = sum(
        (EXTREMAL_EDGES[degree] - 7) * count
        for degree, count in zip(range(18, 25), global_counts, strict=True)
    )
    blue_baseline = sum(
        (EXTREMAL_EDGES[42 - degree] - 7) * count
        for degree, count in zip(range(18, 25), global_counts, strict=True)
    )
    admissible_red_excess = [
        excess
        for excess in range(total_excess + 1)
        if (red_baseline - excess) % 3 == 0
        and (blue_baseline - (total_excess - excess)) % 3 == 0
    ]
    if (
        total_deficiency,
        total_excess,
        red_baseline,
        blue_baseline,
        admissible_red_excess,
    ) != (604, 2, 4209, 4391, [0]):
        raise AssertionError("wrong M=214 excess split")
    red_triangles = red_baseline // 3
    blue_triangles = (blue_baseline - total_excess) // 3
    if (red_triangles, blue_triangles) != (1403, 1463):
        raise AssertionError((red_triangles, blue_triangles))

    # There are 28--30 doubly exact vertices at M=214.  Reanchoring at each
    # one gives internal minimum red/blue degrees 13 and 12.  Turan's exact
    # K5-free edge bound forces component orders at least 18 and 16, while
    # three disjoint closed neighborhoods exclude diameter six.
    backbone_order_bounds = (28, global_counts[3])
    backbone_minimum_degrees = (13, 12)
    minimum_component_orders = tuple(
        next(
            order
            for order in range(minimum_degree + 1, backbone_order_bounds[1] + 1)
            if 2 * turan_edges(order, 4) >= minimum_degree * order
        )
        for minimum_degree in backbone_minimum_degrees
    )
    if backbone_order_bounds != (28, 30):
        raise AssertionError(backbone_order_bounds)
    if minimum_component_orders != (18, 16):
        raise AssertionError(minimum_component_orders)
    if not all(2 * component_order > backbone_order_bounds[1]
               for component_order in minimum_component_orders):
        raise AssertionError("Turan component bound does not force connectivity")

    deletion_component_orders = {
        "red": [
            next(
                order
                for order in range(backbone_minimum_degrees[0] - deleted + 1,
                                   backbone_order_bounds[1] + 1)
                if 2 * turan_edges(order, 4)
                >= (backbone_minimum_degrees[0] - deleted) * order
            )
            for deleted in range(4)
        ],
        "blue": [
            next(
                order
                for order in range(backbone_minimum_degrees[1] - deleted + 1,
                                   backbone_order_bounds[1] + 1)
                if 2 * turan_edges(order, 4)
                >= (backbone_minimum_degrees[1] - deleted) * order
            )
            for deleted in range(2)
        ],
    }
    if deletion_component_orders != {"red": [18, 16, 15, 14], "blue": [16, 15]}:
        raise AssertionError(deletion_component_orders)
    if not all(
        2 * component_order + deleted > backbone_order_bounds[1]
        for orders in deletion_component_orders.values()
        for deleted, component_order in enumerate(orders)
    ):
        raise AssertionError("Turan deletion bound does not force connectivity")
    if not all(3 * (minimum_degree + 1) > backbone_order_bounds[1]
               for minimum_degree in backbone_minimum_degrees):
        raise AssertionError("closed-neighborhood packing does not bound diameter")

    # The five M=215 degree profiles have at most 33 degree-21 vertices, while
    # the anchor multiplicity and side bounds give order >=27 and minimum
    # red/blue degrees 11/10.  Turan component orders reach R(5,3)=14 in both
    # colors, so two components would combine independent triples into a
    # forbidden opposite-color clique.
    ramsey_5_3 = 14
    m215_pairs = split_profiles[215]
    m215_order_bounds = (
        242 - 215,
        max(first_counts[3] + second_counts[3] + 1
            for _, first_counts, second_counts in m215_pairs),
    )
    m215_minimum_degrees = (441 - 2 * 215, 440 - 2 * 215)
    m215_component_orders = tuple(
        next(
            order
            for order in range(minimum_degree + 1, m215_order_bounds[1] + 1)
            if 2 * turan_edges(order, 4) >= minimum_degree * order
        )
        for minimum_degree in m215_minimum_degrees
    )
    m215_red_after_one_deletion = next(
        order
        for order in range(m215_minimum_degrees[0], m215_order_bounds[1] + 1)
        if 2 * turan_edges(order, 4) >= (m215_minimum_degrees[0] - 1) * order
    )
    if m215_order_bounds != (27, 33):
        raise AssertionError(m215_order_bounds)
    if m215_minimum_degrees != (11, 10):
        raise AssertionError(m215_minimum_degrees)
    if m215_component_orders != (15, 14):
        raise AssertionError(m215_component_orders)
    if not all(order >= ramsey_5_3 for order in m215_component_orders):
        raise AssertionError("Ramsey component argument does not force connectivity")
    if m215_red_after_one_deletion != ramsey_5_3:
        raise AssertionError(m215_red_after_one_deletion)
    if 3 * (m215_minimum_degrees[0] + 1) <= m215_order_bounds[1]:
        raise AssertionError("wrong M=215 red diameter packing")
    if 4 * (m215_minimum_degrees[1] + 1) <= m215_order_bounds[1]:
        raise AssertionError("wrong M=215 blue diameter packing")

    # At M=216 the red backbone remains connected.  If it were disconnected,
    # the order lower bound and R(5,3)=14 would force two components of order
    # 13 and independence number two.  The complement within either component
    # would then be triangle-free and subcubic.  Brooks gives a 3-coloring,
    # hence an independent 5-set there and a red K5, a contradiction.
    m216_pairs = split_profiles[216]
    m216_order_bounds = (
        242 - 216,
        max(first_counts[3] + second_counts[3] + 1
            for _, first_counts, second_counts in m216_pairs),
    )
    m216_minimum_degrees = (441 - 2 * 216, 440 - 2 * 216)
    if m216_order_bounds != (26, 36):
        raise AssertionError(m216_order_bounds)
    if m216_minimum_degrees != (9, 8):
        raise AssertionError(m216_minimum_degrees)
    if m216_minimum_degrees[0] + 1 != 10:
        raise AssertionError("red components need not contain a nonedge")
    if 2 * (ramsey_5_3 - 1) != m216_order_bounds[0]:
        raise AssertionError("Ramsey orders do not force two 13-vertex components")
    if (ramsey_5_3 - 1) - 1 - m216_minimum_degrees[0] != 3:
        raise AssertionError("the forced component complement is not subcubic")
    if 4 * (m216_minimum_degrees[0] + 1) <= m216_order_bounds[1]:
        raise AssertionError("wrong M=216 red diameter packing")

    # If blue is disconnected, the same component-independence argument
    # forces exactly two order-13 components with independence number two.
    # Their red complements H_i are triangle-free with alpha at most four.
    # The blue degree bound gives Delta(H_i)<=4; R(3,4)=9 gives delta(H_i)>=4,
    # since a degree-at-most-three vertex would have nine nonneighbors
    # containing an independent four-set, and adjoining the vertex makes five.
    ramsey_3_4 = 9
    exceptional_component_order = ramsey_5_3 - 1
    exceptional_red_maximum_degree = (
        exceptional_component_order - 1 - m216_minimum_degrees[1]
    )
    minimum_nonneighbors_at_degree_three = exceptional_component_order - 1 - 3
    if (
        exceptional_component_order,
        exceptional_red_maximum_degree,
        minimum_nonneighbors_at_degree_three,
    ) != (13, 4, ramsey_3_4):
        raise AssertionError("wrong disconnected-blue critical-component bounds")

    # The color-asymmetric limit is real at the abstract backbone level.
    # H=Cay(Z_13,{+/-1,+/-5}) is triangle-free, 4-regular, and has alpha 4.
    # Put copies of H in red on two 13-sets and color every cross edge red.
    # Red then has clique number 2+2=4, while blue is two disconnected copies
    # of complement(H), also with clique number alpha(H)=4.  Its minimum blue
    # degree is exactly eight, matching the M=216 bound.
    ramsey_circulant = circulant_adjacency(13, (1, 5))
    ramsey_circulant_complement = tuple(
        tuple(first != second and not ramsey_circulant[first][second]
              for second in range(13))
        for first in range(13)
    )
    circulant_degrees = {sum(row) for row in ramsey_circulant}
    circulant_clique = clique_number(ramsey_circulant)
    circulant_independence = clique_number(ramsey_circulant_complement)
    if (circulant_degrees, circulant_clique, circulant_independence) != ({4}, 2, 4):
        raise AssertionError(
            (circulant_degrees, circulant_clique, circulant_independence)
        )
    abstract_red_minimum_degree = 13 + next(iter(circulant_degrees))
    abstract_blue_minimum_degree = 12 - next(iter(circulant_degrees))
    if (abstract_red_minimum_degree, abstract_blue_minimum_degree) != (17, 8):
        raise AssertionError("wrong disconnected-blue backbone degrees")

    # Every vertex in D has global degree 21 in each color.  If |D|=d, both
    # induced colors therefore have minimum degree at least d-22.  At d>=27,
    # every component has at least six vertices and hence an independent pair
    # in its own color.  Avoiding an opposite K5 forces exactly two alpha-two
    # components, each of order at most 13 by R(5,3)=14, contradicting d>=27.
    # Thus the profile bound L>=27 forces both colors connected for every M.
    forced_connected_profile_counts = []
    diameter_eight_profile_counts = []
    diameter_five_profile_counts = []
    escape_profile_counts = []
    escape_profile_lines = []
    escape_lower_bound_histograms = []
    all_exact_anchor_lower_bounds = []
    minimum_internal_degree_at_27 = 21 - (43 - 27)
    minimum_component_order_at_27 = minimum_internal_degree_at_27 + 1
    if (minimum_internal_degree_at_27, minimum_component_order_at_27) != (5, 6):
        raise AssertionError("balanced-degree component lower bound is wrong")
    for edge_count in range(214, 221):
        forced_count = 0
        diameter_eight_count = 0
        diameter_five_count = 0
        escape_histogram = {}
        for weight, first_counts, second_counts in split_profiles[edge_count]:
            degree21_vertices = first_counts[3] + second_counts[3] + 1
            excess_budget = (43 - weight) // 2
            exact_anchor_lower_bound = degree21_vertices - excess_budget
            all_exact_anchor_lower_bounds.append(exact_anchor_lower_bound)
            diameter_eight_count += exact_anchor_lower_bound >= 29
            diameter_five_count += exact_anchor_lower_bound >= 32
            if exact_anchor_lower_bound >= 27:
                forced_count += 1
                continue
            escape_histogram[exact_anchor_lower_bound] = (
                escape_histogram.get(exact_anchor_lower_bound, 0) + 1
            )
            escape_profile_lines.append(
                f"{edge_count} {weight} {exact_anchor_lower_bound} "
                f"{','.join(map(str, first_counts))} "
                f"{','.join(map(str, second_counts))}\n"
            )
        forced_connected_profile_counts.append(forced_count)
        diameter_eight_profile_counts.append(diameter_eight_count)
        diameter_five_profile_counts.append(diameter_five_count)
        escape_profile_counts.append(len(split_profiles[edge_count]) - forced_count)
        escape_lower_bound_histograms.append(escape_histogram)
    escape_profile_digest = hashlib.sha256(
        "".join(escape_profile_lines).encode("ascii")
    ).hexdigest()
    if forced_connected_profile_counts != [1, 5, 16, 37, 63, 85, 107]:
        raise AssertionError(forced_connected_profile_counts)
    if diameter_eight_profile_counts != [0, 2, 11, 30, 52, 70, 88]:
        raise AssertionError(diameter_eight_profile_counts)
    if diameter_five_profile_counts != [0, 0, 5, 16, 28, 37, 49]:
        raise AssertionError(diameter_five_profile_counts)
    if 4 * (29 - 21) <= 29 or 3 * (32 - 21) <= 32:
        raise AssertionError("balanced-degree diameter packing is wrong")

    # Edge accounting rules out every d=26 disconnection.  It would force
    # two alpha-two components of order 13.  The opposite-color graph inside
    # each component is triangle-free with alpha at most four and hence has
    # minimum degree at least four by R(3,4)=9.  Thus the opposite color has
    # at least 13^2+2*26=221 edges inside D.  Balanced degree then leaves at
    # least 120 edges on the other 17 vertices, above ex(17,K5)=108.
    d26_opposite_internal_edges = 13 * 13 + 2 * (13 * 4 // 2)
    least_global_color_total = min(
        total
        for edge_count in range(214, 221)
        for total in (231 + edge_count, 672 - edge_count)
    )
    d26_outside_edges = (
        least_global_color_total + d26_opposite_internal_edges - 21 * 26
    )
    if (
        least_global_color_total,
        d26_opposite_internal_edges,
        d26_outside_edges,
        turan_edges(17, 4),
    ) != (445, 221, 120, 108):
        raise AssertionError("wrong d=26 outside-edge obstruction")
    if d26_outside_edges <= turan_edges(17, 4):
        raise AssertionError("d=26 edge count does not contradict Turan")

    # At d=25 in M=217 or 218, the side-specific minimum degrees are at
    # least four, so the two components have orders 12 and 13 and alpha two.
    # Their opposite-color complements have minimum degrees at least three
    # and four, yielding 156+18+26=200 internal opposite-color edges.  The
    # least relevant global color total is 448, forcing 123 edges on the
    # other 18 vertices, above ex(18,K5)=121.
    if min(441 - 2 * edge_count for edge_count in (217, 218)) < 4:
        raise AssertionError("red d=25 components may have order four")
    if min(440 - 2 * edge_count for edge_count in (217, 218)) < 4:
        raise AssertionError("blue d=25 components may have order four")
    d25_opposite_internal_edges = 12 * 13 + (12 * 3 // 2) + (13 * 4 // 2)
    least_d25_color_total = min(
        total
        for edge_count in (217, 218)
        for total in (231 + edge_count, 672 - edge_count)
    )
    d25_outside_edges = (
        least_d25_color_total + d25_opposite_internal_edges - 21 * 25
    )
    if (
        least_d25_color_total,
        d25_opposite_internal_edges,
        d25_outside_edges,
        turan_edges(18, 4),
    ) != (448, 200, 123, 121):
        raise AssertionError("wrong d=25 outside-edge obstruction")
    if d25_outside_edges <= turan_edges(18, 4):
        raise AssertionError("d=25 edge count does not contradict Turan")

    # The sole remaining M=218 profile has W=15 and L=24.  If a backbone
    # color were disconnected, the preceding d=25 obstruction would force
    # |D|=24.  Its two alpha-two components then have orders 11+13 or 12+12.
    # In the opposite color their interiors are R(3,5)-graphs.  McKay's
    # complete small catalogs give minimum edge counts 15, 20, and 26, so
    # either partition has at least 184 opposite-color edges on D.
    m218_low_profiles = []
    for weight, first_counts, second_counts in split_profiles[218]:
        degree21_vertices = first_counts[3] + second_counts[3] + 1
        exact_anchor_lower_bound = degree21_vertices - (43 - weight) // 2
        if exact_anchor_lower_bound < 25:
            m218_low_profiles.append(
                (weight, exact_anchor_lower_bound, first_counts, second_counts)
            )
    expected_m218_low_profile = (
        15,
        24,
        (0, 0, 2, 19, 0, 0, 0),
        (0, 0, 3, 18, 0, 0, 0),
    )
    if m218_low_profiles != [expected_m218_low_profile]:
        raise AssertionError(m218_low_profiles)
    m218_global_counts = [0, 0, 5, 38, 0, 0, 0]
    m218_excess_budget = (43 - expected_m218_low_profile[0]) // 2
    m218_nonexact_degree21 = m218_global_counts[3] - 24
    m218_red_baseline = sum(
        (EXTREMAL_EDGES[degree] - 7) * count
        for degree, count in zip(range(18, 25), m218_global_counts, strict=True)
    )
    m218_blue_baseline = sum(
        (EXTREMAL_EDGES[42 - degree] - 7) * count
        for degree, count in zip(range(18, 25), m218_global_counts, strict=True)
    )
    m218_admissible_excess_splits = [
        (
            red_excess,
            m218_excess_budget - red_excess,
            (m218_red_baseline - red_excess) // 3,
            (m218_blue_baseline - (m218_excess_budget - red_excess)) // 3,
        )
        for red_excess in range(m218_excess_budget + 1)
        if (m218_red_baseline - red_excess) % 3 == 0
        and (m218_blue_baseline - (m218_excess_budget - red_excess)) % 3 == 0
    ]
    if (
        m218_excess_budget,
        m218_nonexact_degree21,
        m218_red_baseline,
        m218_blue_baseline,
        m218_admissible_excess_splits,
    ) != (
        14,
        14,
        4265,
        4335,
        [
            (2, 12, 1421, 1441),
            (5, 9, 1420, 1442),
            (8, 6, 1419, 1443),
            (11, 3, 1418, 1444),
            (14, 0, 1417, 1445),
        ],
    ):
        raise AssertionError("wrong M=218 zero-slack profile")

    component_partitions = ((11, 13), (12, 12))
    opposite_internal_minima = tuple(
        first * second
        + MINIMUM_R35_EDGES[first]
        + MINIMUM_R35_EDGES[second]
        for first, second in component_partitions
    )
    if opposite_internal_minima != (184, 184):
        raise AssertionError(opposite_internal_minima)

    # Red disconnection makes the opposite blue color dense on D.  At least
    # 184 such edges leave at most 37 red edges on the outside 19-set O.
    # Brouwer's exact extension of Turan says that an n-vertex graph with
    # alpha at most t and at most T(n,t)+floor(n/t)-2 edges is the union of
    # t cliques.  Here T(19,4)=36 and the threshold is 38.  Four cliques
    # covering 19 vertices contain a K5, so red disconnection is impossible.
    outside_order = ORDER - 24
    outside_pairs = outside_order * (outside_order - 1) // 2
    m218_red_total = 231 + 218
    m218_blue_total = 672 - 218
    red_outside_upper_if_red_disconnected = outside_pairs - (
        m218_blue_total + min(opposite_internal_minima) - 21 * 24
    )
    brouwer_minimum = outside_pairs - turan_edges(outside_order, 4)
    brouwer_threshold = brouwer_minimum + outside_order // 4 - 2
    if (
        outside_order,
        outside_pairs,
        m218_red_total,
        m218_blue_total,
        red_outside_upper_if_red_disconnected,
        brouwer_minimum,
        brouwer_threshold,
    ) != (19, 171, 449, 454, 37, 36, 38):
        raise AssertionError("wrong M=218 red-disconnection obstruction")

    # A second small lemma handles blue disconnection.  Every (5,5;19)
    # graph has at least 43 edges.  If F had at most 42, its minimum degree
    # would be at least four: at degree d<=3 the complement of the graph on
    # the 18-d nonneighbors is an R(4,5)-graph, and the exact E(4,5,n) values
    # give the audited lower bounds below.  Equality at d=3 leaves its three
    # neighbors mutually nonadjacent and anticomplete to the other 15
    # vertices, immediately producing an independent five-set.
    low_degree_edge_bounds = tuple(
        (
            degree,
            (18 - degree) * (17 - degree) // 2
            - SMALL_EXTREMAL_EDGES[18 - degree]
            + degree,
        )
        for degree in range(4)
    )
    if low_degree_edge_bounds != ((0, 68), (1, 58), (2, 50), (3, 42)):
        raise AssertionError(low_degree_edge_bounds)

    # Thus a degree-four vertex exists.  On its 14 nonneighbors, the red
    # complement is R(4,5;14), so the induced graph has at least 31 edges.
    # If it has at least 32, the four neighbors cannot all retain degree four:
    # their K4-free interior has at most five edges and their remaining edge
    # budget is at most six.  Equality at 31 forces the unique 60-edge
    # R(4,5;14) core, a K4-minus-edge on the four neighbors, and only two
    # cross edges.  The missing pair avoids some independent triple because
    # the core's triangles have transversal number four.
    extremal_r4514 = decode_short_graph6(EXTREMAL_R4514_G6)
    extremal_r4514_complement = complement_adjacency(extremal_r4514)
    extremal_triangle_data = minimum_triangle_transversal(extremal_r4514)
    if (
        len(extremal_r4514),
        core_edge_count(extremal_r4514),
        clique_number(extremal_r4514),
        clique_number(extremal_r4514_complement),
        extremal_triangle_data,
    ) != (14, 60, 3, 4, (80, 4)):
        raise AssertionError("wrong extremal R(4,5;14) core data")
    neighbor_internal_edge_cap = turan_edges(4, 3)
    larger_core_extra_budget = 42 - 4 - 32
    extremal_core_extra_budget = 42 - 4 - 31
    if (
        neighbor_internal_edge_cap,
        larger_core_extra_budget,
        neighbor_internal_edge_cap + larger_core_extra_budget,
        extremal_core_extra_budget,
        extremal_core_extra_budget - neighbor_internal_edge_cap,
    ) != (5, 6, 11, 7, 2):
        raise AssertionError("wrong R(5,5;19) degree-four budget")
    r5519_minimum_edges = 43

    # If blue were disconnected on D, the same 184-edge bound is red.  It
    # leaves at least 129 red, hence at most 42 blue, edges on O, contradicting
    # the just-proved order-19 lemma.  The unique M=218 profile therefore has
    # both backbone colors connected.
    blue_outside_upper_if_blue_disconnected = outside_pairs - (
        m218_red_total + min(opposite_internal_minima) - 21 * 24
    )
    if blue_outside_upper_if_blue_disconnected != 42:
        raise AssertionError(blue_outside_upper_if_blue_disconnected)
    if blue_outside_upper_if_blue_disconnected >= r5519_minimum_edges:
        raise AssertionError("order-19 edge lemma does not close blue disconnection")

    # The order-19 lemma bootstraps to the sharper e(5,5,20)>=50.  If an
    # order-20 graph F had at most 49 edges, a minimum-degree vertex would
    # have degree at most four.  Degrees zero through three force the lower
    # bounds below by looking at the complementary R(4,5)-graph on its
    # nonneighbors.  At degree four, put a=e(F[N(v)]) and b=e(N(v),S).
    # The order-15 extremal value gives a+b<=6.  Minimum degree gives
    # 2a+b>=12, hence a>=6, whereas N(v) is K4-free and has a<=5.
    combined_r45_maxima = {**SMALL_EXTREMAL_EDGES, **EXTREMAL_EDGES}
    order20_low_degree_bounds = tuple(
        (
            degree,
            degree
            + (19 - degree) * (18 - degree) // 2
            - combined_r45_maxima[19 - degree],
        )
        for degree in range(4)
    )
    if order20_low_degree_bounds != ((0, 79), (1, 69), (2, 59), (3, 51)):
        raise AssertionError(order20_low_degree_bounds)
    order20_degree_four_core_minimum = 15 * 14 // 2 - SMALL_EXTREMAL_EDGES[15]
    order20_degree_four_extra_budget = 49 - 4 - order20_degree_four_core_minimum
    order20_degree_four_neighbor_cap = turan_edges(4, 3)
    order20_degree_four_required_internal = (
        4 * 4 - 4 - order20_degree_four_extra_budget
    )
    if (
        order20_degree_four_core_minimum,
        order20_degree_four_extra_budget,
        4 * 4 - 4,
        order20_degree_four_required_internal,
        order20_degree_four_neighbor_cap,
    ) != (39, 6, 12, 6, 5):
        raise AssertionError("wrong R(5,5;20) degree-four budget")
    if order20_degree_four_required_internal <= order20_degree_four_neighbor_cap:
        raise AssertionError("degree-four contradiction was not strict")
    r5520_minimum_edges = 50

    # Every edge of a 21-vertex graph occurs in 19 of its 21 one-vertex
    # deletions.  Applying the order-20 bound to every deletion gives 19e >=
    # 21*50 and hence e(5,5,21)>=56.
    r5521_minimum_edges = (
        21 * r5520_minimum_edges + (21 - 2) - 1
    ) // (21 - 2)
    if r5521_minimum_edges != 56:
        raise AssertionError(r5521_minimum_edges)

    # The same ingredients close every d=24 or d=25 disconnection in the
    # M=219 and M=220 escape profiles.  The universal internal minimum degree
    # d-22 makes a component with independence number one a K3/K4 at d=24 or
    # a K4 at d=25.  Such a clique needs so many of its color-neighbors in the
    # outside set that it immediately extends to a K5: at d=25 the K4 sees
    # all 18 outside vertices; at d=24 a K4 has a common outside neighbor,
    # while a K3 sees all 19 outside vertices and extends using any outside
    # edge.  Thus every component has independence number at least two.
    # Since the independence numbers sum to at most four, there are exactly
    # two alpha-two components.  Their orders and opposite-color minima are
    # therefore 11+13 or 12+12 at d=24, and 12+13 at d=25.
    high_order_component_partitions = {
        24: ((11, 13), (12, 12)),
        25: ((12, 13),),
    }
    high_order_opposite_internal_minima = {
        order: min(
            first * second
            + MINIMUM_R35_EDGES[first]
            + MINIMUM_R35_EDGES[second]
            for first, second in partitions
        )
        for order, partitions in high_order_component_partitions.items()
    }
    if high_order_opposite_internal_minima != {24: 184, 25: 202}:
        raise AssertionError(high_order_opposite_internal_minima)

    # Brouwer's theorem already gives e(5,5,18)>=35: T(18,4)=32 and every
    # graph through 34 edges with alpha<=4 is a union of four cliques, one of
    # which has order at least five.  Complementing gives the outside maxima
    # 118 at order 18 and 128 at order 19.  All eight color/order cases below
    # exceed the applicable maximum.
    order18_pairs = 18 * 17 // 2
    order18_brouwer_minimum = order18_pairs - turan_edges(18, 4)
    r55_minimum_edges = {
        18: order18_brouwer_minimum + 18 // 4 - 1,
        19: r5519_minimum_edges,
        20: r5520_minimum_edges,
        21: r5521_minimum_edges,
    }
    if r55_minimum_edges != {18: 35, 19: 43, 20: 50, 21: 56}:
        raise AssertionError(r55_minimum_edges)
    high_order_outside_checks = []
    for edge_count in (219, 220):
        color_totals = {"red": 231 + edge_count, "blue": 672 - edge_count}
        for backbone_order in (24, 25):
            outside_order = ORDER - backbone_order
            outside_maximum = (
                outside_order * (outside_order - 1) // 2
                - r55_minimum_edges[outside_order]
            )
            for disconnected_color, opposite_color in (
                ("red", "blue"),
                ("blue", "red"),
            ):
                outside_lower_bound = (
                    color_totals[opposite_color]
                    + high_order_opposite_internal_minima[backbone_order]
                    - 21 * backbone_order
                )
                high_order_outside_checks.append(
                    (
                        edge_count,
                        backbone_order,
                        disconnected_color,
                        outside_lower_bound,
                        outside_maximum,
                    )
                )
    expected_high_order_outside_checks = [
        (219, 24, "red", 133, 128),
        (219, 24, "blue", 130, 128),
        (219, 25, "red", 130, 118),
        (219, 25, "blue", 127, 118),
        (220, 24, "red", 132, 128),
        (220, 24, "blue", 131, 128),
        (220, 25, "red", 129, 118),
        (220, 25, "blue", 128, 118),
    ]
    if high_order_outside_checks != expected_high_order_outside_checks:
        raise AssertionError(high_order_outside_checks)
    if not all(lower > maximum for _, _, _, lower, maximum in high_order_outside_checks):
        raise AssertionError("a high-order disconnection survives edge accounting")

    final_forced_connected_profile_counts = []
    surviving_escape_profile_counts = []
    surviving_escape_profile_lines = []
    surviving_escape_profiles = []
    for edge_count in range(214, 221):
        forced_count = 0
        for weight, first_counts, second_counts in split_profiles[edge_count]:
            degree21_vertices = first_counts[3] + second_counts[3] + 1
            exact_anchor_lower_bound = degree21_vertices - (43 - weight) // 2
            forced = (
                exact_anchor_lower_bound >= 26
                or (edge_count == 217 and exact_anchor_lower_bound >= 25)
                or (edge_count in (218, 219, 220) and exact_anchor_lower_bound >= 24)
            )
            if forced:
                forced_count += 1
            else:
                surviving_escape_profiles.append(
                    (
                        edge_count,
                        weight,
                        exact_anchor_lower_bound,
                        first_counts,
                        second_counts,
                    )
                )
                surviving_escape_profile_lines.append(
                    f"{edge_count} {weight} {exact_anchor_lower_bound} "
                    f"{','.join(map(str, first_counts))} "
                    f"{','.join(map(str, second_counts))}\n"
                )
        final_forced_connected_profile_counts.append(forced_count)
        surviving_escape_profile_counts.append(
            len(split_profiles[edge_count]) - forced_count
        )
    surviving_escape_profile_digest = hashlib.sha256(
        "".join(surviving_escape_profile_lines).encode("ascii")
    ).hexdigest()
    if final_forced_connected_profile_counts != [1, 5, 17, 40, 69, 94, 119]:
        raise AssertionError(final_forced_connected_profile_counts)
    if surviving_escape_profile_counts != [0, 0, 0, 0, 0, 1, 3]:
        raise AssertionError(surviving_escape_profile_counts)
    if surviving_escape_profile_digest != "d69a53973b619bd63eccebe7641657f606f537b752972b67518d1b2d74e136ed":
        raise AssertionError(surviving_escape_profile_digest)

    vertex_connectivity_spectrum = [
        sum(lower_bound >= 26 + connectivity
            for lower_bound in all_exact_anchor_lower_bounds)
        for connectivity in range(1, 12)
    ]
    vertex_connectivity_spectrum[0] = sum(final_forced_connected_profile_counts)
    if vertex_connectivity_spectrum != [
        345, 291, 253, 231, 193, 135, 128, 97, 22, 22, 20
    ]:
        raise AssertionError(vertex_connectivity_spectrum)
    if escape_profile_counts != [0, 0, 1, 3, 6, 10, 15]:
        raise AssertionError(escape_profile_counts)
    if escape_lower_bound_histograms != [
        {},
        {},
        {26: 1},
        {25: 1, 26: 2},
        {24: 1, 25: 2, 26: 3},
        {23: 1, 24: 2, 25: 3, 26: 4},
        {22: 1, 23: 2, 24: 3, 25: 4, 26: 5},
    ]:
        raise AssertionError(escape_lower_bound_histograms)
    if escape_profile_digest != "bf0f2ef8a84453435e00778f04ff0892b16719ba244a7773d02ebddade99ca32":
        raise AssertionError(escape_profile_digest)
    expected_escape_file = (
        "# M W L A_counts_degrees_18_to_24 B_counts_degrees_18_to_24\n"
        + "".join(surviving_escape_profile_lines)
    )
    actual_escape_file = Path(__file__).with_name(
        "BACKBONE_ESCAPE_PROFILES.txt"
    ).read_text(encoding="ascii")
    if actual_escape_file != expected_escape_file:
        raise AssertionError("BACKBONE_ESCAPE_PROFILES.txt does not match enumeration")

    # The four remaining abstract profiles have only the orders 22 and 23 to
    # consider.  Record their exact global degree multisets, their possible
    # actual backbone orders, the corresponding excess slack d-L, and every
    # color-excess/triangle split.
    expected_residual_profiles = [
        (
            219,
            9,
            23,
            (0, 0, 1, 20, 0, 0, 0),
            (0, 0, 2, 19, 0, 0, 0),
        ),
        (
            220,
            3,
            22,
            (0, 0, 0, 21, 0, 0, 0),
            (0, 0, 1, 20, 0, 0, 0),
        ),
        (
            220,
            9,
            23,
            (0, 0, 0, 21, 0, 0, 0),
            (0, 0, 2, 18, 1, 0, 0),
        ),
        (
            220,
            9,
            23,
            (0, 0, 1, 19, 1, 0, 0),
            (0, 0, 1, 20, 0, 0, 0),
        ),
    ]
    if surviving_escape_profiles != expected_residual_profiles:
        raise AssertionError(surviving_escape_profiles)
    residual_profile_ids = (
        "M219-W9",
        "M220-W3",
        "M220-W9-A21",
        "M220-W9-mixed",
    )
    expected_global_counts = (
        (0, 0, 3, 40, 0, 0, 0),
        (0, 0, 1, 42, 0, 0, 0),
        (0, 0, 2, 40, 1, 0, 0),
        (0, 0, 2, 40, 1, 0, 0),
    )
    expected_residual_splits = (
        (
            (1, 16, 1426, 1435),
            (4, 13, 1425, 1436),
            (7, 10, 1424, 1437),
            (10, 7, 1423, 1438),
            (13, 4, 1422, 1439),
            (16, 1, 1421, 1440),
        ),
        (
            (0, 20, 1431, 1429),
            (3, 17, 1430, 1430),
            (6, 14, 1429, 1431),
            (9, 11, 1428, 1432),
            (12, 8, 1427, 1433),
            (15, 5, 1426, 1434),
            (18, 2, 1425, 1435),
        ),
        (
            (0, 17, 1431, 1430),
            (3, 14, 1430, 1431),
            (6, 11, 1429, 1432),
            (9, 8, 1428, 1433),
            (12, 5, 1427, 1434),
            (15, 2, 1426, 1435),
        ),
        (
            (0, 17, 1431, 1430),
            (3, 14, 1430, 1431),
            (6, 11, 1429, 1432),
            (9, 8, 1428, 1433),
            (12, 5, 1427, 1434),
            (15, 2, 1426, 1435),
        ),
    )
    residual_excess_lines = [
        "# profile M W L d slack global_degree_multiset "
        "red_excess blue_excess red_triangles blue_triangles\n"
    ]
    observed_global_counts = []
    observed_residual_splits = []
    for profile_id, profile in zip(
        residual_profile_ids, surviving_escape_profiles, strict=True
    ):
        edge_count, weight, lower_bound, first_counts, second_counts = profile
        global_counts = tuple(
            first_counts[index] + second_counts[index] + (degree == 21)
            for index, degree in enumerate(range(18, 25))
        )
        observed_global_counts.append(global_counts)
        splits = excess_triangle_splits(weight, first_counts, second_counts)
        observed_residual_splits.append(splits)
        degree_multiset = ",".join(
            f"{degree}^{count}"
            for degree, count in zip(range(18, 25), global_counts, strict=True)
            if count
        )
        for backbone_order in range(lower_bound, 24):
            slack = backbone_order - lower_bound
            for red_excess, blue_excess, red_triangles, blue_triangles in splits:
                residual_excess_lines.append(
                    f"{profile_id} {edge_count} {weight} {lower_bound} "
                    f"{backbone_order} {slack} {degree_multiset} "
                    f"{red_excess} {blue_excess} "
                    f"{red_triangles} {blue_triangles}\n"
                )
    if tuple(observed_global_counts) != expected_global_counts:
        raise AssertionError(observed_global_counts)
    if tuple(observed_residual_splits) != expected_residual_splits:
        raise AssertionError(observed_residual_splits)
    if len(residual_excess_lines) != 33:
        raise AssertionError(len(residual_excess_lines))
    expected_residual_excess_file = "".join(residual_excess_lines)
    actual_residual_excess_file = Path(__file__).with_name(
        "RESIDUAL_EXCESS_SPLITS.tsv"
    ).read_text(encoding="ascii")
    if actual_residual_excess_file != expected_residual_excess_file:
        raise AssertionError("RESIDUAL_EXCESS_SPLITS.tsv does not match enumeration")

    # At d=23 the universal induced minimum degree is one.  A component with
    # independence number one would be K2, K3, or K4.  Its vertices have the
    # stated numbers of same-color outside neighbors; inclusion-exclusion
    # leaves common outside sets of orders 20,17,12.  These respectively hold
    # a same-color triangle by R(3,5)=14, an edge because alpha<=4, or a
    # vertex, so each clique extends to K5.  The same calculation excludes
    # every nonsingleton alpha-one component at d=22.
    alpha_one_component_data = {
        23: tuple(
            (
                component_order,
                22 - component_order,
                20 - component_order * (component_order - 2),
            )
            for component_order in range(2, 5)
        ),
        22: tuple(
            (
                component_order,
                22 - component_order,
                21 - component_order * (component_order - 1),
            )
            for component_order in range(2, 5)
        ),
    }
    if alpha_one_component_data != {
        23: ((2, 20, 20), (3, 19, 17), (4, 18, 12)),
        22: ((2, 20, 19), (3, 19, 15), (4, 18, 9)),
    }:
        raise AssertionError(alpha_one_component_data)
    if alpha_one_component_data[23][0][2] < 14:
        raise AssertionError("the d=23 K2 common set need not contain a triangle")
    if alpha_one_component_data[22][0][2] < 14:
        raise AssertionError("the d=22 K2 common set need not contain a triangle")
    if min(alpha_one_component_data[23][1][2], alpha_one_component_data[22][1][2]) < 5:
        raise AssertionError("a K3 common set need not contain an edge")
    if min(alpha_one_component_data[23][2][2], alpha_one_component_data[22][2][2]) < 1:
        raise AssertionError("a K4 common set can be empty")

    # Hence a d=23 disconnection consists of exactly two alpha-two
    # components, of orders 10+13 or 11+12.  At d=22, either there are two
    # alpha-two components of orders 9+13, 10+12, or 11+11, or one singleton
    # and one order-21 alpha-three component.  Complete R(3,5) catalog edge
    # histograms enumerate the two-component isomorphism-type pairs.  Global
    # edge accounting and the just-proved diagonal minima filter the menu.
    residual_component_partitions = {
        23: ((10, 13), (11, 12)),
        22: ((9, 13), (10, 12), (11, 11)),
    }
    r35_catalog_counts = {
        order: sum(histogram.values())
        for order, histogram in R35_EDGE_HISTOGRAMS.items()
    }
    if r35_catalog_counts != {9: 290, 10: 313, 11: 105, 12: 12, 13: 1}:
        raise AssertionError(r35_catalog_counts)
    cover_spectra = {
        order: {
            cover: sum(
                count
                for (_, candidate_cover), count in histogram.items()
                if candidate_cover == cover
            )
            for cover in sorted({entry[1] for entry in histogram})
        }
        for order, histogram in R35_EDGE_COVER_HISTOGRAMS.items()
    }
    if cover_spectra != {
        9: {1: 26, 2: 263, 3: 1},
        10: {2: 197, 3: 116},
        11: {3: 105},
        12: {4: 12},
        13: {5: 1},
    }:
        raise AssertionError(cover_spectra)

    # If H is the opposite-color graph in a Q-component C, then for every
    # outside vertex its opposite-color neighbors in C must hit every
    # independent four-set of H: otherwise its Q-neighbors contain a Q-K4.
    # If tau_4(H) is the minimum such transversal, the opposite-color cross
    # degree sum from C is therefore at least |O| tau_4(H).  Exact degree 21
    # on C computes that sum as |C|(|C|+21-d)-2e(H).  In particular the unique
    # order-13 graph has e=26 and tau_4=5, excluding the 10+13 partition at
    # d=23 (91<100) and the 9+13 partition at d=22 (104<105).  For 11+12 at
    # d=23, the order-12 graph must be the unique 20-edge type, and the
    # order-11 graph has at most 19 edges.
    critical_cover_checks = (
        (13 * (13 + 21 - 23) - 2 * 26, (43 - 23) * 5),
        (13 * (13 + 21 - 22) - 2 * 26, (43 - 22) * 5),
        (12 * (12 + 21 - 23) - 2 * 20, (43 - 23) * 4),
        (12 * (12 + 21 - 23) - 2 * 21, (43 - 23) * 4),
        (11 * (11 + 21 - 23) - 2 * 19, (43 - 23) * 3),
        (11 * (11 + 21 - 23) - 2 * 20, (43 - 23) * 3),
    )
    if critical_cover_checks != (
        (91, 100),
        (104, 105),
        (80, 80),
        (78, 80),
        (61, 60),
        (59, 60),
    ):
        raise AssertionError(critical_cover_checks)
    menu_case_specs = (
        (23, 219, "red"),
        (23, 219, "blue"),
        (23, 220, "red"),
        (23, 220, "blue"),
        (22, 220, "red"),
        (22, 220, "blue"),
    )
    residual_menu_lines = [
        "# d M disconnected_color component_orders opposite_edges_D "
        "opposite_edges_outside candidate_unordered_type_pairs\n"
    ]
    menu_summary = {}
    for backbone_order, edge_count, disconnected_color in menu_case_specs:
        outside_order = ORDER - backbone_order
        outside_minimum = r55_minimum_edges[outside_order]
        outside_maximum = outside_order * (outside_order - 1) // 2 - outside_minimum
        color_totals = {"red": 231 + edge_count, "blue": 672 - edge_count}
        opposite_color = "blue" if disconnected_color == "red" else "red"
        partition_counts = {}
        for first_order, second_order in residual_component_partitions[backbone_order]:
            retained_count = 0
            for opposite_edges, type_pairs in component_pair_edge_histogram(
                first_order, second_order, backbone_order
            ):
                outside_edges = (
                    color_totals[opposite_color]
                    + opposite_edges
                    - 21 * backbone_order
                )
                if not outside_minimum <= outside_edges <= outside_maximum:
                    continue
                retained_count += type_pairs
                residual_menu_lines.append(
                    f"{backbone_order} {edge_count} {disconnected_color} "
                    f"{first_order}+{second_order} {opposite_edges} "
                    f"{outside_edges} {type_pairs}\n"
                )
            partition_counts[(first_order, second_order)] = retained_count
        menu_summary[(backbone_order, edge_count, disconnected_color)] = partition_counts
    expected_menu_summary = {
        (23, 219, "red"): {(10, 13): 0, (11, 12): 57},
        (23, 219, "blue"): {(10, 13): 0, (11, 12): 87},
        (23, 220, "red"): {(10, 13): 0, (11, 12): 87},
        (23, 220, "blue"): {(10, 13): 0, (11, 12): 87},
        (22, 220, "red"): {(9, 13): 0, (10, 12): 2676, (11, 11): 5564},
        (22, 220, "blue"): {(9, 13): 0, (10, 12): 2676, (11, 11): 5565},
    }
    if menu_summary != expected_menu_summary:
        raise AssertionError(menu_summary)
    expected_residual_menu_file = "".join(residual_menu_lines)
    residual_menu_digest = hashlib.sha256(
        expected_residual_menu_file.encode("ascii")
    ).hexdigest()
    if residual_menu_digest != "8b58b0cbba85e55def6083a90d7ef21397cd2c0a39de5bfe95df7f704434baac":
        raise AssertionError(residual_menu_digest)
    actual_residual_menu_file = Path(__file__).with_name(
        "RESIDUAL_COMPONENT_MENUS.tsv"
    ).read_text(encoding="ascii")
    if actual_residual_menu_file != expected_residual_menu_file:
        raise AssertionError("RESIDUAL_COMPONENT_MENUS.tsv does not match enumeration")

    # The only d=22 profile has red-degree multiset 20^1,21^42 and 451 red
    # edges.  If an exact vertex u were a singleton of the red backbone, its
    # two exact local cores would force 100 red edges on the outside O and 110
    # red edges on the other 21 anchors C.  Global accounting then gives 220
    # red C--O edges, while the degree sum on O gives only 219.  A blue
    # singleton is consistent, but exactness forces G[C] and complement(G)[O]
    # both to be R(4,5;21,100) cores and fixes the red C--O count at 220.
    d22_red_total = 231 + 220
    d22_outside_red_degree_sum = 20 + 20 * 21
    red_singleton_cross_global = d22_red_total - 21 - 100 - 110
    red_singleton_cross_degrees = d22_outside_red_degree_sum - 2 * 100 - 21
    blue_singleton_cross_global = d22_red_total - 21 - 100 - 110
    blue_singleton_cross_degrees = d22_outside_red_degree_sum - 2 * 110
    if (
        d22_red_total,
        d22_outside_red_degree_sum,
        red_singleton_cross_global,
        red_singleton_cross_degrees,
        blue_singleton_cross_global,
        blue_singleton_cross_degrees,
    ) != (451, 440, 220, 219, 220, 220):
        raise AssertionError("wrong d=22 singleton accounting")

    residual_excess_digest = hashlib.sha256(
        expected_residual_excess_file.encode("ascii")
    ).hexdigest()
    if residual_excess_digest != "2bb0a8f67e346f1066a9cf2d8219ef89e97480bcf973372fe59040bacefed857":
        raise AssertionError(residual_excess_digest)
    if len(residual_menu_lines) != 77:
        raise AssertionError(len(residual_menu_lines))

    # If W is the degree weight, at most W/3 secondary vertices are
    # noncentral and at most (43-W)/2 local sides exceed deficiency seven.
    # Audit both the structural 241-M lower bound and its attainment within
    # the integer-profile superset for every cross total.
    secondary_anchor_minima = []
    first_side_anchor_minima = []
    second_side_anchor_minima = []
    for edge_count, pairs in split_profiles.items():
        if not all(weight >= 3 * (441 - 2 * edge_count)
                   for weight, _, _ in pairs):
            raise AssertionError("degree-weight triangle inequality failed")
        profile_bounds = []
        for weight, first_counts, second_counts in pairs:
            secondary_degree21 = first_counts[3] + second_counts[3]
            exceptional_sides = (43 - weight) // 2
            profile_bounds.append(secondary_degree21 - exceptional_sides)
        first_side_anchor_minima.append(
            min(max(0, first_counts[3] - (43 - weight) // 2)
                for weight, first_counts, _ in pairs)
        )
        second_side_anchor_minima.append(
            min(max(0, second_counts[3] - (43 - weight) // 2)
                for weight, _, second_counts in pairs)
        )
        secondary_anchor_minima.append(min(profile_bounds))
    if secondary_anchor_minima != [27, 26, 25, 24, 23, 22, 21]:
        raise AssertionError(secondary_anchor_minima)
    if secondary_anchor_minima != [241 - edge_count for edge_count in range(214, 221)]:
        raise AssertionError("wrong closed anchor-multiplicity formula")
    if first_side_anchor_minima != [13, 11, 9, 7, 5, 3, 1]:
        raise AssertionError(first_side_anchor_minima)
    if second_side_anchor_minima != [12, 10, 8, 6, 4, 2, 0]:
        raise AssertionError(second_side_anchor_minima)

    print("PASS exact row/column formulas on 7 matrices and 294 vertex profiles")
    print("PASS exact one-cross-flip updates on 14 flips and 588 vertex profiles")
    print("PASS all test matrices satisfy cross cardinality and first-degree bounds")
    print("PASS split degree deviations equal M-220 and M-221")
    print("PASS first-degree-feasible test weights=99,...,111 exceed hard limit 39")
    print("PASS hard split degree-profile counts=1,5,17,40,69,95,122 total=349")
    print("PASS triangle-pair counts=1,3,8,15,20,27,39 total=113 "
          "sha256=ccaf9ccec34aa4633cf2019d3f85f34e714c1f0bb17db444e9f8034c650c936c")
    print("PASS exact local-side minima red=43,38,36,34,29,27,25 "
          "blue=41,40,36,32,31,27,23")
    print("PASS M=214 forces degrees 20^13,21^30 and excess split red=0 blue=2")
    print("PASS M=214 forces monochromatic triangle counts red=1403 blue=1463")
    print("PASS M=214 exact-anchor backbone order=28,...,30 min degrees red=13 blue=12")
    print("PASS backbone vertex connectivity is at least red=4 blue=2")
    print("PASS both backbone colors have diameter at most 5")
    print("PASS M=215 exact-anchor backbone order=27,...,33 min degrees red=11 blue=10")
    print("PASS M=215 backbones connected; red connectivity>=2 diameters red<=5 blue<=8")
    print("PASS M=216 red backbone order=26,...,36 is connected with diameter<=8")
    print("PASS M=216 blue disconnection forces two 13-vertex critical components")
    print("PASS C13(1,5) gives a sharp disconnected-blue abstract backbone")
    print("PASS outside-edge obstructions eliminate d=26 and M217/218 d=25 cuts")
    print("PASS small R(3,5) catalog counts at orders 9,...,13 are "
          "290,313,105,12,1")
    print("PASS every R(5,5;19) graph has at least 43 edges")
    print("PASS diagonal edge minima at orders 20,21 are at least 50,56")
    print("PASS the unique M=218 profile has both backbone colors connected")
    print("PASS d=24/25 cuts are impossible in the M=219/220 escape profiles")
    print("PASS both-color connectivity profiles M214..220="
          "1/1,5/5,17/17,40/40,69/69,94/95,119/122")
    print("PASS backbone escape profiles=0,0,0,0,0,1,3 total=4 "
          "sha256=d69a53973b619bd63eccebe7641657f606f537b752972b67518d1b2d74e136ed")
    print("PASS residual excess split counts=6,7,6,6 rows=32 "
          f"sha256={residual_excess_digest}")
    print("PASS independent-four cover sieve removes d=23 10+13 and d=22 9+13")
    print("PASS d=23 component-pair menus M219 red/blue=57/87 "
          "M220 red/blue=87/87")
    print("PASS d=22 two-component menus red/blue=8240/8241")
    print("PASS d=22 red singleton impossible; blue singleton reanchors two "
          "R(4,5;21,100) cores")
    print("PASS residual component menu rows=76 "
          f"sha256={residual_menu_digest}")
    print("PASS profile diameter bounds <=8 for 253 profiles and <=5 for 135")
    print("PASS profile vertex-connectivity counts k=1,...,11 are "
          "345,291,253,231,193,135,128,97,22,22,20")
    print("PASS first-degree-feasible tests have 0 secondary exact anchors")
    print("PASS side anchor minima A=13,11,9,7,5,3,1 B=12,10,8,6,4,2,0")
    print("PASS hard branch forces secondary exact anchors=27,26,25,24,23,22,21")


if __name__ == "__main__":
    main()
