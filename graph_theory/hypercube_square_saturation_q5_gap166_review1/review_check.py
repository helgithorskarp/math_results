#!/usr/bin/env python3
"""Independent spot checker for the Q5 gap-166 review.

This program does not import the reviewed implementation.  It rebuilds the
three residual Q4 automorphism orbits from endpoint-pair representatives,
checks their defining statistics and boundary profiles, excludes the four
remaining Q5 facet profiles by exact overlap gluing, and verifies the global
rational arithmetic.  It is deliberately not a third full Q4 census.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations
import json


def cube_edges(dimension: int) -> tuple[tuple[int, int], ...]:
    return tuple(
        sorted(
            (vertex, vertex ^ (1 << coordinate))
            for vertex in range(1 << dimension)
            for coordinate in range(dimension)
            if vertex < (vertex ^ (1 << coordinate))
        )
    )


def cube_squares(
    dimension: int, edges: tuple[tuple[int, int], ...]
) -> tuple[tuple[tuple[int, int], ...], ...]:
    result = []
    for first in range(dimension):
        for second in range(first + 1, dimension):
            for base in range(1 << dimension):
                if (base >> first) & 1 or (base >> second) & 1:
                    continue
                result.append(
                    tuple(
                        tuple(sorted(edge))
                        for edge in (
                            (base, base ^ (1 << first)),
                            (base, base ^ (1 << second)),
                            (
                                base ^ (1 << first),
                                base ^ (1 << first) ^ (1 << second),
                            ),
                            (
                                base ^ (1 << second),
                                base ^ (1 << first) ^ (1 << second),
                            ),
                        )
                    )
                )
    return tuple(result)


Q3_EDGES = cube_edges(3)
Q3_SQUARES = cube_squares(3, Q3_EDGES)
Q4_EDGES = cube_edges(4)
Q4_SQUARES = cube_squares(4, Q4_EDGES)
Q5_EDGES = cube_edges(5)
Q4_FACETS = tuple((coordinate, bit) for coordinate in range(4) for bit in (0, 1))
Q5_FACETS = tuple((coordinate, bit) for coordinate in range(5) for bit in (0, 1))


def q3_census() -> tuple[int, int]:
    squarefree = 0
    zero_slack = 0
    edge_index = {edge: index for index, edge in enumerate(Q3_EDGES)}
    indexed_squares = tuple(
        tuple(edge_index[edge] for edge in square) for square in Q3_SQUARES
    )
    for mask in range(1 << len(Q3_EDGES)):
        missing = []
        inactive_incidences = 0
        valid = True
        for square in indexed_squares:
            present = [edge for edge in square if (mask >> edge) & 1]
            if len(present) == 4:
                valid = False
                break
            if len(present) == 3:
                missing.append(next(edge for edge in square if edge not in present))
            else:
                inactive_incidences += len(present)
        if not valid:
            continue
        squarefree += 1
        repeated = len(missing) - len(set(missing))
        twice_slack = 2 * inactive_incidences + 4 * repeated - len(missing)
        if twice_slack < 0:
            raise AssertionError("negative Q3 slack")
        zero_slack += twice_slack == 0
    return squarefree, zero_slack


def mask_edges(mask: int) -> frozenset[tuple[int, int]]:
    return frozenset(edge for index, edge in enumerate(Q4_EDGES) if (mask >> index) & 1)


def permute_vertex(vertex: int, permutation: tuple[int, ...]) -> int:
    result = 0
    for old_coordinate, new_coordinate in enumerate(permutation):
        result |= ((vertex >> old_coordinate) & 1) << new_coordinate
    return result


def transform(
    pattern: frozenset[tuple[int, int]],
    translation: int,
    permutation: tuple[int, ...],
) -> frozenset[tuple[int, int]]:
    return frozenset(
        tuple(
            sorted(
                (
                    permute_vertex(first, permutation) ^ translation,
                    permute_vertex(second, permutation) ^ translation,
                )
            )
        )
        for first, second in pattern
    )


def orbit(mask: int) -> frozenset[frozenset[tuple[int, int]]]:
    pattern = mask_edges(mask)
    return frozenset(
        transform(pattern, translation, permutation)
        for translation in range(16)
        for permutation in permutations(range(4))
    )


def q4_statistics(pattern: frozenset[tuple[int, int]]) -> tuple[int, int, int, int]:
    witnesses = []
    for square in Q4_SQUARES:
        present = [edge for edge in square if edge in pattern]
        if len(present) == 4:
            raise AssertionError("residual orbit contains a square")
        if len(present) == 3:
            witnesses.append(next(edge for edge in square if edge not in present))
    multiplicities = Counter(witnesses)
    pairs = sum(value * (value - 1) // 2 for value in multiplicities.values())
    edges = len(pattern)
    slack = 6 * edges - 7 * len(witnesses) + 2 * pairs
    deficit = 17 * slack - 3 * edges
    return edges, len(witnesses), slack, deficit


def delete_coordinate(vertex: int, coordinate: int, dimension: int) -> int:
    result = 0
    target = 0
    for source in range(dimension):
        if source == coordinate:
            continue
        result |= ((vertex >> source) & 1) << target
        target += 1
    return result


def facet_signature(
    pattern: frozenset[tuple[int, int]], facet: tuple[int, int]
) -> frozenset[tuple[int, int]]:
    coordinate, bit = facet
    return frozenset(
        tuple(
            sorted(
                (
                    delete_coordinate(first, coordinate, 4),
                    delete_coordinate(second, coordinate, 4),
                )
            )
        )
        for first, second in pattern
        if ((first >> coordinate) & 1) == bit
        and ((second >> coordinate) & 1) == bit
    )


def boundary_profile(
    catalog: frozenset[frozenset[tuple[int, int]]],
    extendable: frozenset[frozenset[tuple[int, int]]],
) -> tuple[int, int]:
    profiles = set()
    for pattern in catalog:
        signatures = tuple(facet_signature(pattern, facet) for facet in Q4_FACETS)
        profiles.add(
            (
                sum(signature not in extendable for signature in signatures),
                sum(not signature for signature in signatures),
            )
        )
    if len(profiles) != 1:
        raise AssertionError("boundary profile is not orbit-invariant")
    return profiles.pop()


def embed_q4(
    pattern: frozenset[tuple[int, int]], facet: tuple[int, int]
) -> frozenset[tuple[int, int]]:
    coordinate, bit = facet
    free = tuple(index for index in range(5) if index != coordinate)

    def embed_vertex(local_vertex: int) -> int:
        result = bit << coordinate
        for local_coordinate, global_coordinate in enumerate(free):
            result |= ((local_vertex >> local_coordinate) & 1) << global_coordinate
        return result

    return frozenset(
        tuple(sorted((embed_vertex(first), embed_vertex(second))))
        for first, second in pattern
    )


Q5_FACET_EDGES = tuple(
    frozenset(
        edge
        for edge in Q5_EDGES
        if all(((vertex >> coordinate) & 1) == bit for vertex in edge)
    )
    for coordinate, bit in Q5_FACETS
)


def gluing_solutions(
    catalogs: tuple[tuple[frozenset[tuple[int, int]], ...], ...]
) -> int:
    embedded = tuple(
        tuple(embed_q4(pattern, Q5_FACETS[facet]) for pattern in catalog)
        for facet, catalog in enumerate(catalogs)
    )

    def visit(
        ones: frozenset[tuple[int, int]],
        known: frozenset[tuple[int, int]],
        remaining: tuple[int, ...],
    ) -> int:
        if not remaining:
            return 1
        choices = []
        for facet in remaining:
            overlap = Q5_FACET_EDGES[facet] & known
            compatible = tuple(
                candidate
                for candidate in embedded[facet]
                if (candidate & overlap) == (ones & overlap)
            )
            choices.append((len(compatible), facet, compatible))
        count, facet, compatible = min(choices, key=lambda row: row[0])
        if count == 0:
            return 0
        next_remaining = tuple(item for item in remaining if item != facet)
        return sum(
            visit(
                ones | candidate,
                known | Q5_FACET_EDGES[facet],
                next_remaining,
            )
            for candidate in compatible
        )

    return visit(frozenset(), frozenset(), tuple(range(10)))


def residual_closure(
    equality: frozenset[frozenset[tuple[int, int]]],
    good42: frozenset[frozenset[tuple[int, int]]],
    deficit48: frozenset[frozenset[tuple[int, int]]],
) -> dict[str, dict[str, int]]:
    empty = (frozenset(),)
    equality_rows = tuple(equality)
    good42_rows = tuple(good42)
    deficit48_rows = tuple(deficit48)
    fixed42 = (mask_edges(0x0DFFE55A),)
    fixed48 = (mask_edges(0x001F7EFE),)
    remaining = tuple(range(1, 10))
    cases: dict[str, list[tuple[tuple[frozenset[tuple[int, int]], ...], ...]]] = {
        "42": [],
        "84": [],
        "132": [],
        "144": [],
    }

    for empty_facet in remaining:
        cases["42"].append(
            tuple(
                fixed42
                if facet == 0
                else empty
                if facet == empty_facet
                else equality_rows
                for facet in range(10)
            )
        )
    for second in remaining:
        cases["84"].append(
            tuple(
                fixed42 if facet == 0 else good42_rows if facet == second else equality_rows
                for facet in range(10)
            )
        )
    for positions42 in combinations(remaining, 2):
        for empty_facet in remaining:
            if empty_facet in positions42:
                continue
            cases["132"].append(
                tuple(
                    fixed48
                    if facet == 0
                    else good42_rows
                    if facet in positions42
                    else empty
                    if facet == empty_facet
                    else equality_rows
                    for facet in range(10)
                )
            )
    for other_positive in combinations(remaining, 2):
        for empty_facet in remaining:
            if empty_facet in other_positive:
                continue
            cases["144"].append(
                tuple(
                    fixed48
                    if facet == 0
                    else deficit48_rows
                    if facet in other_positive
                    else empty
                    if facet == empty_facet
                    else equality_rows
                    for facet in range(10)
                )
            )

    result = {}
    for name, rows in cases.items():
        solutions = sum(gluing_solutions(row) for row in rows)
        result[name] = {"cases": len(rows), "solutions": solutions}
    return result


def live_capacity_maxima() -> list[int]:
    edge_facets = []
    for first, second in Q5_EDGES:
        direction = (first ^ second).bit_length() - 1
        edge_facets.append(
            frozenset(
                (coordinate, (first >> coordinate) & 1)
                for coordinate in range(5)
                if coordinate != direction
            )
        )
    return [
        max(
            sum(containing <= frozenset(live) for containing in edge_facets)
            for live in combinations(Q5_FACETS, live_count)
        )
        for live_count in range(1, 11)
    ]


def check() -> dict[str, object]:
    if (len(Q3_EDGES), len(Q3_SQUARES), len(Q4_EDGES), len(Q4_SQUARES), len(Q5_EDGES)) != (
        12,
        6,
        32,
        24,
        80,
    ):
        raise AssertionError("cube incidence construction failed")
    squarefree, zero_slack = q3_census()
    if (squarefree, zero_slack) != (2902, 49):
        raise AssertionError("unexpected Q3 census")

    equality = orbit(0x000DFFDD)
    good42 = orbit(0x0DFFE55A)
    deficit48 = orbit(0x001F7EFE)
    if tuple(map(len, (equality, good42, deficit48))) != (64, 32, 192):
        raise AssertionError("unexpected residual orbit size")
    expected_statistics = {
        "equality": (17, 15, 3, 0),
        "good42": (20, 18, 6, 42),
        "deficit48": (18, 16, 6, 48),
    }
    catalogs = {"equality": equality, "good42": good42, "deficit48": deficit48}
    for name, catalog in catalogs.items():
        if set(map(q4_statistics, catalog)) != {expected_statistics[name]}:
            raise AssertionError(f"incorrect statistics in {name} orbit")

    extendable = frozenset(
        facet_signature(pattern, facet)
        for pattern in equality
        for facet in Q4_FACETS
    )
    profiles = {
        "good42": boundary_profile(good42, extendable),
        "deficit48": boundary_profile(deficit48, extendable),
    }
    if profiles != {"good42": (0, 0), "deficit48": (3, 0)}:
        raise AssertionError("incorrect residual boundary profile")

    residuals = residual_closure(equality, good42, deficit48)
    expected_cases = {"42": 9, "84": 9, "132": 252, "144": 252}
    if {name: row["cases"] for name, row in residuals.items()} != expected_cases:
        raise AssertionError("incomplete residual placement list")
    if any(row["solutions"] for row in residuals.values()):
        raise AssertionError("residual profile admits a Q5 gluing")

    capacities = live_capacity_maxima()
    if capacities != [0, 0, 0, 1, 5, 9, 16, 28, 48, 80]:
        raise AssertionError("incorrect live-facet capacities")

    q5_ratio = Fraction(12 * 56 + 166, 34 * 56)
    global_coefficient = q5_ratio / 12
    if (q5_ratio, global_coefficient) != (Fraction(419, 952), Fraction(419, 11424)):
        raise AssertionError("incorrect Q5 or global ratio")
    if (2 * (11424 - 419), 7 * 11424) != (22010, 79968):
        raise AssertionError("incorrect clearing of the active-square inequality")
    if (39984 - 11005, 39984 // 2) != (28979, 19992):
        raise AssertionError("incorrect final substitution")
    integer_bounds = {}
    for dimension in (7, 8):
        value = Fraction(
            19992 * dimension * 2**dimension,
            11005 * dimension + 28979,
        )
        integer_bounds[str(dimension)] = (value.numerator + value.denominator - 1) // value.denominator
    if integer_bounds != {"7": 169, "8": 350}:
        raise AssertionError("incorrect finite-dimensional ceiling")

    return {
        "q3_squarefree_patterns": squarefree,
        "q3_zero_slack_patterns": zero_slack,
        "residual_orbit_sizes": {name: len(catalog) for name, catalog in catalogs.items()},
        "residual_statistics": expected_statistics,
        "residual_boundary_profiles": profiles,
        "residual_gluing": residuals,
        "live_facet_capacity_maxima": capacities,
        "q5_slack_edge_ratio": str(q5_ratio),
        "global_slack_coefficient": str(global_coefficient),
        "cleared_inequality": "11005*(d-1)*E >= 39984*M",
        "final_bound": "(11005*d+28979)*E >= 19992*d*2^d",
        "integer_bounds": integer_bounds,
        "status": "PASS",
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2, sort_keys=True))
