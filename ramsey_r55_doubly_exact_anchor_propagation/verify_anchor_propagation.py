#!/usr/bin/env python3
"""Audit local-count propagation from a doubly exact 21+21 Ramsey anchor."""

from __future__ import annotations

import hashlib
import itertools


SIDE = 21
ORDER = 43
SAMPLE_CORE_G6 = "TJaGmrdI_gqziMTiLYE?ro`dlTI|TTmTiwtQ"
EXTREMAL_EDGES = {18: 85, 19: 92, 20: 100, 21: 107,
                  22: 114, 23: 122, 24: 132}
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
    print("PASS first-degree-feasible tests have 0 secondary exact anchors")
    print("PASS side anchor minima A=13,11,9,7,5,3,1 B=12,10,8,6,4,2,0")
    print("PASS hard branch forces secondary exact anchors=27,26,25,24,23,22,21")


if __name__ == "__main__":
    main()
