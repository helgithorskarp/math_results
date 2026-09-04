#!/usr/bin/env python3
"""Definition-level audit of the forced 21+21 cross-matrix normal form."""

from __future__ import annotations

import itertools


SIDE = 21
ORDER = 43
# This (4,5;21,100) graph is induced from line 5 of the pinned McKay
# r45_24.g6 catalog by deleting source vertices 0, 1, and 8.  Nothing in the
# normal-form theorem depends on this example; it audits the implementation.
SAMPLE_CORE_G6 = "TJaGmrdI_gqziMTiLYE?ro`dlTI|TTmTiwtQ"


def decode_short_graph6(encoded: str) -> tuple[tuple[bool, ...], ...]:
    data = encoded.strip()
    if not data or ord(data[0]) == 126:
        raise ValueError("only short graph6 headers are supported")
    order = ord(data[0]) - 63
    bit_count = order * (order - 1) // 2
    expected_payload = (bit_count + 5) // 6
    if len(data) != 1 + expected_payload:
        raise ValueError((len(data), 1 + expected_payload))
    bits = []
    for character in data[1:]:
        value = ord(character) - 63
        if value < 0 or value > 63:
            raise ValueError("invalid graph6 character")
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    adjacency = [[False] * order for _ in range(order)]
    position = 0
    for second in range(1, order):
        for first in range(second):
            adjacency[first][second] = adjacency[second][first] = bool(bits[position])
            position += 1
    return tuple(tuple(row) for row in adjacency)


def clique_sets(
    adjacency: tuple[tuple[bool, ...], ...], size: int, color: bool
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        vertices
        for vertices in itertools.combinations(range(len(adjacency)), size)
        if all(adjacency[first][second] == color
               for first, second in itertools.combinations(vertices, 2))
    )


def edge_count(adjacency: tuple[tuple[bool, ...], ...]) -> int:
    return sum(
        adjacency[first][second]
        for second in range(1, len(adjacency))
        for first in range(second)
    )


def cross_variable(first: int, second: int) -> int:
    return first * SIDE + second


def mixed_clauses(
    red_neighbor_core: tuple[tuple[bool, ...], ...],
    blue_neighbor_core: tuple[tuple[bool, ...], ...],
) -> tuple[tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]]:
    """Return cross-variable sets forbidden to be all red and all blue."""
    red_clauses = []
    blue_clauses = []
    # On the blue-neighbor side, red edges are the complement of the supplied
    # blue core.  H has no red K4 and K has no blue K4, so these are exactly
    # the three nonempty mixed splits possible for each monochromatic K5.
    for first_size, second_size in ((1, 4), (2, 3), (3, 2)):
        for first_set in clique_sets(red_neighbor_core, first_size, True):
            for second_set in clique_sets(blue_neighbor_core, second_size, False):
                red_clauses.append(
                    tuple(
                        cross_variable(first, second)
                        for first in first_set
                        for second in second_set
                    )
                )
    for first_size, second_size in ((2, 3), (3, 2), (4, 1)):
        for first_set in clique_sets(red_neighbor_core, first_size, False):
            for second_set in clique_sets(blue_neighbor_core, second_size, True):
                blue_clauses.append(
                    tuple(
                        cross_variable(first, second)
                        for first in first_set
                        for second in second_set
                    )
                )
    return tuple(red_clauses), tuple(blue_clauses)


def cross_patterns() -> tuple[frozenset[int], ...]:
    return (
        frozenset(),
        frozenset(range(SIDE * SIDE)),
        frozenset(
            cross_variable(first, second)
            for first in range(SIDE)
            for second in range(SIDE)
            if (first + second) % 2 == 0
        ),
        frozenset(
            cross_variable(first, second)
            for first in range(SIDE)
            for second in range(SIDE)
            if (first + 2 * second) % 3 != 0
        ),
    )


def direct_monochromatic_fives(
    red_neighbor_core: tuple[tuple[bool, ...], ...],
    blue_neighbor_core: tuple[tuple[bool, ...], ...],
    red_cross_variables: frozenset[int],
) -> tuple[int, int]:
    def is_red(first: int, second: int) -> bool:
        if first > second:
            first, second = second, first
        if first == 0:
            return second <= SIDE
        if second <= SIDE:
            return red_neighbor_core[first - 1][second - 1]
        if first > SIDE:
            return not blue_neighbor_core[first - SIDE - 1][second - SIDE - 1]
        return cross_variable(first - 1, second - SIDE - 1) in red_cross_variables

    red_count = 0
    blue_count = 0
    for vertices in itertools.combinations(range(ORDER), 5):
        colors = [is_red(first, second)
                  for first, second in itertools.combinations(vertices, 2)]
        red_count += all(colors)
        blue_count += not any(colors)
    return red_count, blue_count


def main() -> None:
    core = decode_short_graph6(SAMPLE_CORE_G6)
    if len(core) != SIDE or edge_count(core) != 100:
        raise AssertionError("sample is not an order-21, 100-edge graph")
    clique_counts = {
        color: {size: len(clique_sets(core, size, color)) for size in range(1, 6)}
        for color in (True, False)
    }
    if clique_counts[True] != {1: 21, 2: 100, 3: 113, 4: 0, 5: 0}:
        raise AssertionError(clique_counts[True])
    if clique_counts[False] != {1: 21, 2: 110, 3: 175, 4: 75, 5: 0}:
        raise AssertionError(clique_counts[False])

    red_clauses, blue_clauses = mixed_clauses(core, core)
    if len(red_clauses) != 31505 or len(blue_clauses) != 31505:
        raise AssertionError((len(red_clauses), len(blue_clauses)))
    if len(set(red_clauses)) != len(red_clauses) or len(set(blue_clauses)) != len(blue_clauses):
        raise AssertionError("duplicate mixed clauses")

    for red_cross_variables in cross_patterns():
        clause_counts = (
            sum(all(variable in red_cross_variables for variable in clause)
                for clause in red_clauses),
            sum(all(variable not in red_cross_variables for variable in clause)
                for clause in blue_clauses),
        )
        direct_counts = direct_monochromatic_fives(core, core, red_cross_variables)
        if direct_counts != clause_counts:
            raise AssertionError((len(red_cross_variables), direct_counts, clause_counts))

    degrees = [sum(row) for row in core]
    red_row_bounds = [(17 - degree, 23 - degree) for degree in degrees]
    red_column_bounds = [(degree - 2, degree + 4) for degree in degrees]
    if min(lower for lower, _ in red_row_bounds + red_column_bounds) != 6:
        raise AssertionError("wrong row/column lower bound")
    if max(upper for _, upper in red_row_bounds + red_column_bounds) != 15:
        raise AssertionError("wrong row/column upper bound")
    if {edges - 231 for edges in range(445, 452)} != set(range(214, 221)):
        raise AssertionError("wrong cross-edge cardinality range")

    print("PASS sample (4,5;21,100) core red cliques=21,100,113,0,0")
    print("PASS sample core blue cliques=21,110,175,75,0")
    print("PASS exact mixed clauses: red=31505 blue=31505")
    print("PASS direct K5 equivalence on four deterministic cross matrices")
    print("PASS hard-branch cross ones=214,...,220 and degree bounds")


if __name__ == "__main__":
    main()
