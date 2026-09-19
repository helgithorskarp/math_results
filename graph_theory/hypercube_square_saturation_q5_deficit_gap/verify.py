#!/usr/bin/env python3
"""Exact low-slack census and arithmetic verifier for the Q5 deficit gap.

The finite computation enumerates every square-free edge pattern in Q4 whose
Q3-facet slack sum is at most five.  It glues complete labeled Q3 restrictions,
so the search is exhaustive without enumerating all 2^32 Q4 edge sets.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations
import json


DIM = 4
MAX_TWICE_SLACK = 10
VERTICES = tuple(range(1 << DIM))
EDGES = tuple(
    (vertex, direction)
    for direction in range(DIM)
    for vertex in VERTICES
    if not (vertex >> direction) & 1
)
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
EDGE_PAIR_INDEX = {
    (vertex, vertex | (1 << direction)): index
    for index, (vertex, direction) in enumerate(EDGES)
}
SQUARES = tuple(
    (
        EDGE_INDEX[(base, first)],
        EDGE_INDEX[(base, second)],
        EDGE_INDEX[(base | (1 << first), second)],
        EDGE_INDEX[(base | (1 << second), first)],
    )
    for first in range(DIM)
    for second in range(first + 1, DIM)
    for base in VERTICES
    if not (base >> first) & 1 and not (base >> second) & 1
)
FACETS = tuple((coordinate, bit) for coordinate in range(DIM) for bit in (0, 1))
FACET_EDGES = {
    facet: tuple(
        edge_index
        for edge_index, (vertex, direction) in enumerate(EDGES)
        if direction != facet[0] and ((vertex >> facet[0]) & 1) == facet[1]
    )
    for facet in FACETS
}
FACET_EDGE_MASKS = {
    facet: sum(1 << edge_index for edge_index in FACET_EDGES[facet])
    for facet in FACETS
}
FACET_SQUARES = {
    facet: tuple(
        square
        for square in SQUARES
        if all(((EDGES[edge][0] >> facet[0]) & 1) == facet[1] for edge in square)
    )
    for facet in FACETS
}


def local_statistics(mask: int, facet: tuple[int, int]) -> tuple[int, int, int, int]:
    """Return (active faces, repeated witnesses, inactive incidences, 2*sigma)."""

    missing_witnesses: list[int] = []
    inactive_incidences = 0
    for square in FACET_SQUARES[facet]:
        present = [edge for edge in square if (mask >> edge) & 1]
        if len(present) == 4:
            raise ValueError("completed square")
        if len(present) == 3:
            missing_witnesses.append(next(edge for edge in square if edge not in present))
        else:
            inactive_incidences += len(present)
    active = len(missing_witnesses)
    repeated = active - len(set(missing_witnesses))
    twice_slack = 2 * inactive_incidences + 4 * repeated - active
    return active, repeated, inactive_incidences, twice_slack


def local_patterns(facet: tuple[int, int]) -> tuple[tuple[int, int, int], ...]:
    """Embed every square-free local Q3 pattern with 2*sigma <= 10."""

    edges = FACET_EDGES[facet]
    patterns = []
    for local_mask in range(1 << len(edges)):
        mask = sum(
            ((local_mask >> position) & 1) << edge
            for position, edge in enumerate(edges)
        )
        try:
            *_, twice_slack = local_statistics(mask, facet)
        except ValueError:
            continue
        if twice_slack <= MAX_TWICE_SLACK:
            patterns.append((mask, mask.bit_count(), twice_slack))
    return tuple(patterns)


def direct_q4_statistics(mask: int) -> tuple[int, int, int, int]:
    """Return (E,T,P,S) directly from Q4 edges and active squares."""

    witnesses = []
    for square in SQUARES:
        present = [edge for edge in square if (mask >> edge) & 1]
        if len(present) == 4:
            raise ValueError("completed square")
        if len(present) == 3:
            witnesses.append(next(edge for edge in square if edge not in present))
    multiplicities = Counter(witnesses)
    pairs = sum(count * (count - 1) // 2 for count in multiplicities.values())
    edge_count = mask.bit_count()
    active = len(witnesses)
    slack = 6 * edge_count - 7 * active + 2 * pairs
    return edge_count, active, pairs, slack


def facet_gluing_census() -> tuple[dict[int, int], int, dict[tuple[int, int], int]]:
    """Glue low-slack Q3 restrictions over all eight Q4 facets."""

    patterns = tuple(local_patterns(facet) for facet in FACETS)
    order = (0, 2, 4, 6, 1, 3, 5, 7)
    assigned = 0
    indexes = []
    for facet_index in order:
        facet = FACETS[facet_index]
        facet_mask = FACET_EDGE_MASKS[facet]
        overlap = facet_mask & assigned
        by_overlap: dict[int, list[tuple[int, int, int]]] = defaultdict(list)
        for pattern in patterns[facet_index]:
            by_overlap[pattern[0] & overlap].append(pattern)
        indexes.append((facet_mask, overlap, dict(by_overlap)))
        assigned |= facet_mask

    complete: dict[int, int] = {}
    nodes = 0

    def visit(depth: int, values: int, edge_incidence_sum: int, twice_slack: int) -> None:
        nonlocal nodes
        nodes += 1
        if twice_slack > MAX_TWICE_SLACK:
            return
        if depth == len(order):
            if edge_incidence_sum != 3 * values.bit_count():
                raise AssertionError("each Q4 edge must occur in three facets")
            if twice_slack % 2:
                raise AssertionError("the complete Q4 slack must be integral")
            complete[values] = twice_slack // 2
            return
        facet_mask, overlap, by_overlap = indexes[depth]
        for pattern, edge_count, local_twice_slack in by_overlap.get(values & overlap, ()):
            visit(
                depth + 1,
                (values & ~facet_mask) | pattern,
                edge_incidence_sum + edge_count,
                twice_slack + local_twice_slack,
            )

    visit(0, 0, 0, 0)
    local_table = Counter(
        (edge_count, twice_slack)
        for _, edge_count, twice_slack in patterns[0]
    )
    return complete, nodes, dict(sorted(local_table.items()))


def normalized_graph_hash(masks: set[int] | dict[int, int]) -> str:
    rows = []
    for mask in masks:
        edge_pairs = tuple(
            (vertex, vertex | (1 << direction))
            for edge_index, (vertex, direction) in enumerate(EDGES)
            if (mask >> edge_index) & 1
        )
        rows.append(tuple(sorted(edge_pairs)))
    canonical = json.dumps(sorted(rows), separators=(",", ":"))
    return sha256(canonical.encode("ascii")).hexdigest()


def permute_vertex(vertex: int, permutation: tuple[int, ...]) -> int:
    image = 0
    for old_coordinate, new_coordinate in enumerate(permutation):
        image |= ((vertex >> old_coordinate) & 1) << new_coordinate
    return image


def transform(mask: int, translation: int, permutation: tuple[int, ...]) -> int:
    image = 0
    for edge_index, (vertex, direction) in enumerate(EDGES):
        if not (mask >> edge_index) & 1:
            continue
        first = permute_vertex(vertex, permutation) ^ translation
        second = permute_vertex(vertex | (1 << direction), permutation) ^ translation
        pair = tuple(sorted((first, second)))
        image |= 1 << EDGE_PAIR_INDEX[pair]
    return image


def orbit_summary(masks: set[int]) -> list[tuple[str, int, int]]:
    remaining = set(masks)
    result = []
    coordinate_permutations = tuple(permutations(range(DIM)))
    while remaining:
        representative = min(remaining)
        orbit = {
            transform(representative, translation, permutation)
            for translation in VERTICES
            for permutation in coordinate_permutations
        }
        if not orbit <= masks:
            raise AssertionError("the census must be closed under cube automorphisms")
        result.append((f"0x{representative:08x}", len(orbit), 384 // len(orbit)))
        remaining -= orbit
    return result


def q5_support_distribution(live_count: int) -> dict[int, int]:
    dim = 5
    edges = tuple(
        (vertex, direction)
        for direction in range(dim)
        for vertex in range(1 << dim)
        if not (vertex >> direction) & 1
    )
    facets = tuple((coordinate, bit) for coordinate in range(dim) for bit in (0, 1))
    edge_facets = tuple(
        frozenset(
            (coordinate, (vertex >> coordinate) & 1)
            for coordinate in range(dim)
            if coordinate != direction
        )
        for vertex, direction in edges
    )
    counts = Counter(
        sum(containing <= frozenset(live) for containing in edge_facets)
        for live in combinations(facets, live_count)
    )
    return dict(sorted(counts.items()))


def verify() -> dict[str, object]:
    if len(EDGES) != 32 or len(SQUARES) != 24 or len(FACETS) != 8:
        raise AssertionError("incorrect Q4 incidence structure")
    if {len(FACET_EDGES[facet]) for facet in FACETS} != {12}:
        raise AssertionError("each Q3 facet must have twelve edges")
    if {len(FACET_SQUARES[facet]) for facet in FACETS} != {6}:
        raise AssertionError("each Q3 facet must have six squares")

    patterns, nodes, local_table = facet_gluing_census()
    expected_local_table = {
        (0, 0): 1,
        (7, 0): 48,
        (8, 1): 24,
        (6, 3): 64,
        (1, 4): 12,
        (8, 4): 42,
        (3, 5): 24,
        (5, 6): 108,
        (9, 6): 8,
        (7, 7): 216,
        (2, 8): 66,
        (8, 8): 72,
        (4, 9): 192,
        (6, 10): 396,
    }
    if local_table != expected_local_table:
        raise AssertionError("unexpected low-slack Q3 table")

    spectrum = Counter((mask.bit_count(), slack) for mask, slack in patterns.items())
    expected_spectrum = {(0, 0): 1, (17, 3): 64, (19, 5): 192}
    if spectrum != expected_spectrum:
        raise AssertionError("unexpected low-slack Q4 spectrum")
    for mask, slack in patterns.items():
        direct = direct_q4_statistics(mask)
        if direct[3] != slack:
            raise AssertionError("facet and direct slack computations disagree")

    nonempty_deficits = [
        17 * slack - 3 * mask.bit_count()
        for mask, slack in patterns.items()
        if mask
    ]
    positive_deficits = [deficit for deficit in nonempty_deficits if deficit > 0]
    if min(positive_deficits) != 28:
        raise AssertionError("the least positive Q4 facet deficit must be 28")
    defect_minimizers = {
        mask
        for mask, slack in patterns.items()
        if 17 * slack - 3 * mask.bit_count() == 28
    }
    orbits = orbit_summary(defect_minimizers)
    if orbits != [("0x0fff163c", 192, 2)]:
        raise AssertionError("unexpected defect-28 orbit classification")

    live4 = q5_support_distribution(4)
    live8 = q5_support_distribution(8)
    if live4 != {0: 130, 1: 80} or live8 != {16: 5, 28: 40}:
        raise AssertionError("unexpected Q5 live-facet support capacities")

    q5_edge_cap = 56  # Dejter--Emamy-K--Guan, imported finite theorem.
    q5_deficit_gap = 28
    q5_slack_edge_ratio = Fraction(12 * q5_edge_cap + q5_deficit_gap, 34 * q5_edge_cap)
    global_slack_coefficient = q5_slack_edge_ratio / 12
    retained_coefficient = 1 - global_slack_coefficient
    asymptotic_constant = Fraction(204, 113)
    preceding_constant = Fraction(5_183_640, 2_874_791)
    if q5_slack_edge_ratio != Fraction(175, 476):
        raise AssertionError("incorrect Q5 uniform ratio")
    if global_slack_coefficient != Fraction(175, 5712):
        raise AssertionError("incorrect global slack coefficient")
    if retained_coefficient != Fraction(5537, 5712):
        raise AssertionError("incorrect retained coefficient")
    if asymptotic_constant <= preceding_constant:
        raise AssertionError("the new asymptotic bound must be stronger")
    if 204 * 2_874_791 - 5_183_640 * 113 != 706_044:
        raise AssertionError("incorrect finite-bound cross difference")
    if 204 * 7 * 2**7 != 182_784 or 113 * 7 + 295 != 1086:
        raise AssertionError("incorrect d=7 specialization")

    canonical_data = {
        "local_table": [(*key, count) for key, count in sorted(local_table.items())],
        "spectrum": [(*key, count) for key, count in sorted(spectrum.items())],
        "defect_minimizer_orbits": orbits,
        "live4": live4,
        "live8": live8,
    }
    audit_hash = sha256(
        json.dumps(canonical_data, sort_keys=True, separators=(",", ":")).encode("ascii")
    ).hexdigest()
    return {
        "q3_local_masks_checked_per_facet": 1 << 12,
        "q3_low_slack_patterns_per_facet": sum(local_table.values()),
        "facet_gluing_nodes": nodes,
        "q4_low_slack_patterns": len(patterns),
        "q4_low_slack_spectrum_E_S_count": [
            [edge_count, slack, count]
            for (edge_count, slack), count in sorted(spectrum.items())
        ],
        "q4_least_positive_deficit": min(positive_deficits),
        "q4_defect_28_patterns": len(defect_minimizers),
        "q4_defect_28_orbits": orbits,
        "normalized_graph_set_sha256": normalized_graph_hash(patterns),
        "audit_sha256": audit_hash,
        "q5_live4_support_distribution": live4,
        "q5_live8_support_distribution": live8,
        "q5_deficit_lower_bound": q5_deficit_gap,
        "external_q5_squarefree_edge_cap": q5_edge_cap,
        "q5_slack_edge_ratio": str(q5_slack_edge_ratio),
        "bound": "sat(Q_d,Q_2) >= 204*d*2^d/(113*d+295) for d>=5",
        "asymptotic_constant": str(asymptotic_constant),
        "improvement_over_5183640_2874791": str(asymptotic_constant - preceding_constant),
        "finite_bound_cross_difference": "706044*(d-1)",
        "d7_real_bound": "30464/181",
        "d7_integer_lower_bound": 169,
    }


def main() -> None:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    print("status=PASS")


if __name__ == "__main__":
    main()
