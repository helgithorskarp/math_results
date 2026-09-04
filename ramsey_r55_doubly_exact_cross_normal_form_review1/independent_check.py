#!/usr/bin/env python3
"""Clean-room audit of the 21+21 Ramsey cross-matrix normal form."""

from __future__ import annotations

import itertools


SIDE = 21
TOTAL = 43
CORE_G6 = "TJaGmrdI_gqziMTiLYE?ro`dlTI|TTmTiwtQ"
UPPER = {18: 85, 19: 92, 20: 100, 21: 107, 22: 114, 23: 122, 24: 132}


def graph6_edges(text: str) -> frozenset[tuple[int, int]]:
    """Decode short graph6 through one flat bit string."""
    order = ord(text[0]) - 63
    payload = "".join(f"{ord(char) - 63:06b}" for char in text[1:])
    pairs = [(first, second) for second in range(1, order) for first in range(second)]
    if order != SIDE or len(payload) < len(pairs):
        raise AssertionError("unexpected graph6 dimensions")
    if any(bit == "1" for bit in payload[len(pairs) :]):
        raise AssertionError("nonzero graph6 padding")
    return frozenset(pair for pair, bit in zip(pairs, payload, strict=False) if bit == "1")


def edge(edges: frozenset[tuple[int, int]], first: int, second: int) -> bool:
    if first > second:
        first, second = second, first
    return (first, second) in edges


def homogeneous(edges: frozenset[tuple[int, int]], vertices: tuple[int, ...], red: bool) -> bool:
    return all(
        edge(edges, first, second) == red
        for first, second in itertools.combinations(vertices, 2)
    )


def cross_mask(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    mask = 0
    for first in left:
        for second in right:
            mask |= 1 << (SIDE * first + second)
    return mask


def clauses_from_five_sets(
    h_edges: frozenset[tuple[int, int]], k_edges: frozenset[tuple[int, int]]
) -> tuple[frozenset[int], frozenset[int]]:
    """Scan mixed five-sets directly, without clique-family products."""
    red = set()
    blue = set()
    vertices = tuple(range(SIDE))
    for left_size in range(1, 5):
        for left in itertools.combinations(vertices, left_size):
            left_red = homogeneous(h_edges, left, True)
            left_blue = homogeneous(h_edges, left, False)
            if not left_red and not left_blue:
                continue
            for right in itertools.combinations(vertices, 5 - left_size):
                mask = cross_mask(left, right)
                # K records blue edges on B.  Hence a red internal edge on B
                # is a nonedge of K, while a blue one is an edge of K.
                if left_red and homogeneous(k_edges, right, False):
                    red.add(mask)
                if left_blue and homogeneous(k_edges, right, True):
                    blue.add(mask)
    return frozenset(red), frozenset(blue)


def direct_fives(
    h_edges: frozenset[tuple[int, int]],
    k_edges: frozenset[tuple[int, int]],
    red_cross: int,
) -> tuple[int, int]:
    def is_red(first: int, second: int) -> bool:
        if first > second:
            first, second = second, first
        if first == 0:
            return second <= SIDE
        if second <= SIDE:
            return edge(h_edges, first - 1, second - 1)
        if first > SIDE:
            return not edge(k_edges, first - SIDE - 1, second - SIDE - 1)
        variable = SIDE * (first - 1) + (second - SIDE - 1)
        return bool(red_cross & (1 << variable))

    red_count = 0
    blue_count = 0
    for five in itertools.combinations(range(TOTAL), 5):
        colors = tuple(is_red(first, second) for first, second in itertools.combinations(five, 2))
        red_count += all(colors)
        blue_count += not any(colors)
    return red_count, blue_count


def independent_formula_audit() -> None:
    core = graph6_edges(CORE_G6)
    if len(core) != 100:
        raise AssertionError(len(core))
    counts = {
        red: tuple(
            sum(homogeneous(core, subset, red) for subset in itertools.combinations(range(SIDE), size))
            for size in range(1, 6)
        )
        for red in (True, False)
    }
    if counts[True] != (21, 100, 113, 0, 0):
        raise AssertionError(counts[True])
    if counts[False] != (21, 110, 175, 75, 0):
        raise AssertionError(counts[False])

    red_clauses, blue_clauses = clauses_from_five_sets(core, core)
    if (len(red_clauses), len(blue_clauses)) != (31505, 31505):
        raise AssertionError((len(red_clauses), len(blue_clauses)))
    clause_lengths = {
        mask.bit_count() for mask in itertools.chain(red_clauses, blue_clauses)
    }
    if clause_lengths != {4, 6}:
        raise AssertionError(clause_lengths)

    all_cross = (1 << (SIDE * SIDE)) - 1
    patterns = (
        0,
        all_cross,
        sum(
            1 << (SIDE * first + second)
            for first in range(SIDE)
            for second in range(SIDE)
            if (3 * first + 5 * second + first * second) % 7 < 3
        ),
    )
    for pattern in patterns:
        formula_counts = (
            sum(mask & pattern == mask for mask in red_clauses),
            sum(mask & pattern == 0 for mask in blue_clauses),
        )
        if direct_fives(core, core, pattern) != formula_counts:
            raise AssertionError((pattern.bit_count(), direct_fives(core, core, pattern), formula_counts))

    degrees = [sum(edge(core, vertex, other) for other in range(SIDE)) for vertex in range(SIDE)]
    for degree in degrees:
        for cross_degree in range(SIDE + 1):
            if (18 <= 1 + degree + cross_degree <= 24) != (
                17 - degree <= cross_degree <= 23 - degree
            ):
                raise AssertionError("row interval is not exact")
            if (18 <= 20 - degree + cross_degree <= 24) != (
                degree - 2 <= cross_degree <= degree + 4
            ):
                raise AssertionError("column interval is not exact")
    if {global_edges - 231 for global_edges in range(445, 452)} != set(range(214, 221)):
        raise AssertionError("wrong cross cardinalities")

    print("formula_sample_edges=100")
    print("formula_sample_cliques=21,100,113,0,0")
    print("formula_sample_independent_sets=21,110,175,75,0")
    print("five_set_scan_clauses=31505_red,31505_blue")
    print("clause_lengths=4,6")
    print("direct_equivalence_patterns=3")
    print("row_column_intervals=exact")
    print("cross_cardinalities=214,...,220")


def independent_anchor_arithmetic() -> None:
    coefficients = {
        degree: 2 * (UPPER[degree] + UPPER[42 - degree])
        - 2 * 861
        + 3 * degree * (42 - degree)
        for degree in range(18, 25)
    }
    if tuple(coefficients.values()) != (8, 17, 26, 29, 26, 17, 8):
        raise AssertionError(coefficients)
    if 42 * coefficients[21] + coefficients[20] != 1244:
        raise AssertionError("deficiency parity bound")

    weights = {degree: 29 - coefficient for degree, coefficient in coefficients.items()}
    outer_degrees = (18, 19, 20, 22, 23, 24)
    ranges = [range(39 // weights[degree] + 1) for degree in outer_degrees]
    profiles = []
    for outer_counts in itertools.product(*ranges):
        used = sum(outer_counts)
        if used > 43:
            continue
        counts = dict(zip(outer_degrees, outer_counts, strict=True))
        counts[21] = 43 - used
        weight = sum(weights[degree] * counts.get(degree, 0) for degree in range(18, 25))
        degree_sum = sum(degree * counts.get(degree, 0) for degree in range(18, 25))
        if weight <= 39 and degree_sum % 2 == 0 and degree_sum <= 902:
            profiles.append((counts, degree_sum))
    if len(profiles) != 104:
        raise AssertionError(len(profiles))
    if {degree_sum // 2 for _, degree_sum in profiles} != set(range(445, 452)):
        raise AssertionError("wrong hard-branch edge range")
    minimum_central = min(counts[21] for counts, _ in profiles)
    if minimum_central != 30:
        raise AssertionError(minimum_central)

    # Delta <= 622, whereas 86 deficiencies of at least seven total 602.
    # Thus at most 20 sides are nonexact.  At least 30 degree-21 vertices
    # minus those 20 exceptions leaves at least 10 exact on both sides.
    if 622 - 86 * 7 != 20 or minimum_central - 20 != 10:
        raise AssertionError("wrong doubly exact anchor count")

    print("imported_extremal_maxima=85,92,100,107,114,122,132")
    print("twice_deficiency_coefficients=8,17,26,29,26,17,8")
    print("hard_profiles=104")
    print("minimum_degree21_vertices=30")
    print("maximum_nonexact_sides=20")
    print("minimum_doubly_exact_anchors=10")
    print("independent_checks=true")


if __name__ == "__main__":
    independent_formula_audit()
    independent_anchor_arithmetic()
