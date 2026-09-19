#!/usr/bin/env python3
"""Exact verifier for the Q5 facet-deficit lower bound 166.

The computation exhausts every square-free Q4 edge pattern with facet slack
at most 13, compresses all possible Q5 deficit profiles below 166, and checks
the four profiles not eliminated by transparent incidence filters.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations
import json


DIM = 4
MAX_SLACK = 13
MAX_TWICE_SLACK = 2 * MAX_SLACK
DEFICIT_LIMIT = 166
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
    """Embed all square-free Q3 patterns whose twice-slack is at most 26."""

    edges = FACET_EDGES[facet]
    patterns = []
    square_free_count = 0
    for local_mask in range(1 << len(edges)):
        mask = sum(
            ((local_mask >> position) & 1) << edge
            for position, edge in enumerate(edges)
        )
        try:
            *_, twice_slack = local_statistics(mask, facet)
        except ValueError:
            continue
        square_free_count += 1
        if twice_slack < 0:
            raise AssertionError("Q3 slack must be nonnegative")
        if twice_slack <= MAX_TWICE_SLACK:
            patterns.append((mask, mask.bit_count(), twice_slack))
    if square_free_count != 2902:
        raise AssertionError("unexpected number of square-free labeled Q3 patterns")
    return tuple(patterns)


def facet_gluing_census() -> tuple[dict[int, int], int, dict[tuple[int, int], int]]:
    """Glue complete Q3 restrictions to enumerate every Q4 with S<=13."""

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

    def visit(depth: int, values: int, incidence: int, twice_slack: int) -> None:
        nonlocal nodes
        nodes += 1
        if twice_slack > MAX_TWICE_SLACK:
            return
        if depth == len(order):
            if incidence != 3 * values.bit_count():
                raise AssertionError("each Q4 edge must occur in three facets")
            if twice_slack % 2:
                raise AssertionError("complete Q4 slack must be integral")
            complete[values] = twice_slack // 2
            return
        facet_mask, overlap, by_overlap = indexes[depth]
        for pattern, edge_count, local_cost in by_overlap.get(values & overlap, ()):
            visit(
                depth + 1,
                (values & ~facet_mask) | pattern,
                incidence + edge_count,
                twice_slack + local_cost,
            )

    visit(0, 0, 0, 0)
    local_table = Counter(
        (edge_count, twice_slack)
        for _, edge_count, twice_slack in patterns[0]
    )
    return complete, nodes, dict(sorted(local_table.items()))


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
    slack = 6 * edge_count - 7 * len(witnesses) + 2 * pairs
    return edge_count, len(witnesses), pairs, slack


def normalized_graph_hash(masks: set[int] | dict[int, int]) -> str:
    rows = []
    for mask in masks:
        rows.append(
            tuple(
                sorted(
                    (vertex, vertex | (1 << direction))
                    for edge_index, (vertex, direction) in enumerate(EDGES)
                    if (mask >> edge_index) & 1
                )
            )
        )
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
        image |= 1 << EDGE_PAIR_INDEX[tuple(sorted((first, second)))]
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
            raise AssertionError("classified set must be closed under Q4 automorphisms")
        result.append((f"0x{representative:08x}", len(orbit), 384 // len(orbit)))
        remaining -= orbit
    return result


Q5_DIM = 5
Q5_VERTICES = tuple(range(1 << Q5_DIM))
Q5_EDGES = tuple(
    (vertex, direction)
    for direction in range(Q5_DIM)
    for vertex in Q5_VERTICES
    if not (vertex >> direction) & 1
)
Q5_EDGE_INDEX = {edge: index for index, edge in enumerate(Q5_EDGES)}
Q5_FACETS = tuple(
    (coordinate, bit) for coordinate in range(Q5_DIM) for bit in (0, 1)
)
Q5_FACET_EDGE_MASKS = {
    facet: sum(
        1 << index
        for index, (vertex, direction) in enumerate(Q5_EDGES)
        if direction != facet[0] and ((vertex >> facet[0]) & 1) == facet[1]
    )
    for facet in Q5_FACETS
}


def embed_q4(mask: int, facet: tuple[int, int]) -> int:
    coordinate, bit = facet
    free = tuple(index for index in range(Q5_DIM) if index != coordinate)
    result = 0
    for local_edge, (local_vertex, local_direction) in enumerate(EDGES):
        if not (mask >> local_edge) & 1:
            continue
        vertex = bit << coordinate
        for local_coordinate, global_coordinate in enumerate(free):
            vertex |= ((local_vertex >> local_coordinate) & 1) << global_coordinate
        result |= 1 << Q5_EDGE_INDEX[(vertex, free[local_direction])]
    return result


def live_support_distribution(live_count: int) -> dict[int, int]:
    edge_facets = tuple(
        frozenset(
            (coordinate, (vertex >> coordinate) & 1)
            for coordinate in range(Q5_DIM)
            if coordinate != direction
        )
        for vertex, direction in Q5_EDGES
    )
    counts = Counter(
        sum(containing <= frozenset(live) for containing in edge_facets)
        for live in combinations(Q5_FACETS, live_count)
    )
    return dict(sorted(counts.items()))


def boundary_classification(
    census: dict[int, int], equality: tuple[int, ...]
) -> tuple[dict[int, tuple[int, int]], Counter[tuple[int, int, int, int]]]:
    """Return mask -> (bad,empty) and counts of low positive profile classes."""

    special = (0, 0)
    side_facets = tuple(facet for facet in Q5_FACETS if facet[0] != special[0])
    embedded_equality = {
        facet: tuple(embed_q4(mask, facet) for mask in equality)
        for facet in side_facets
    }
    boundary_data = {}
    class_counts: Counter[tuple[int, int, int, int]] = Counter()
    for local_mask, slack in census.items():
        if not local_mask:
            continue
        special_mask = embed_q4(local_mask, special)
        bad = 0
        empty = 0
        for facet in side_facets:
            overlap = Q5_FACET_EDGE_MASKS[facet] & Q5_FACET_EDGE_MASKS[special]
            bad += not any(
                not ((candidate ^ special_mask) & overlap)
                for candidate in embedded_equality[facet]
            )
            empty += not (special_mask & overlap)
        boundary_data[local_mask] = (bad, empty)
        deficit = 17 * slack - 3 * local_mask.bit_count()
        if 0 < deficit < DEFICIT_LIMIT:
            class_counts[(deficit, local_mask.bit_count(), bad, empty)] += 1
    return boundary_data, class_counts


def structural_profile_survivors(
    class_counts: Counter[tuple[int, int, int, int]],
    capacity_maxima: dict[int, int],
) -> tuple[tuple[object, ...], ...]:
    classes = tuple(sorted(class_counts))
    survivors: set[tuple[object, ...]] = set()

    def visit(
        start: int,
        chosen: tuple[tuple[int, int, int, int], ...],
        total: int,
    ) -> None:
        if chosen and total % 2 == 0:
            positive_count = len(chosen)
            positive_edges = sum(item[1] for item in chosen)
            for equality_count in range(11 - positive_count):
                empty_count = 10 - positive_count - equality_count
                incidence = positive_edges + 17 * equality_count
                if incidence % 4:
                    continue
                global_edges = incidence // 4
                live_count = positive_count + equality_count
                if not global_edges or global_edges > capacity_maxima[live_count]:
                    continue
                exceptional_neighbors = positive_count + empty_count - 1
                if any(item[2] > exceptional_neighbors for item in chosen):
                    continue
                survivors.add(
                    (total, chosen, equality_count, empty_count, global_edges)
                )
        if len(chosen) == 9:
            return
        for index in range(start, len(classes)):
            item = classes[index]
            if total + item[0] >= DEFICIT_LIMIT:
                break
            visit(index, chosen + (item,), total + item[0])

    visit(0, (), 0)
    return tuple(sorted(survivors))


def exact_q5_search(
    fixed_facet: tuple[int, int],
    fixed_local_mask: int,
    local_candidates: dict[tuple[int, int], tuple[int, ...]],
) -> tuple[int, int, int]:
    """Glue prescribed Q4 facet classes; return solutions, nodes, max depth."""

    embedded = {
        facet: tuple(embed_q4(mask, facet) for mask in masks)
        for facet, masks in local_candidates.items()
    }
    nodes = 0
    solutions = 0
    max_depth = 0

    def visit(
        values: int,
        known: int,
        remaining: tuple[tuple[int, int], ...],
        depth: int,
    ) -> None:
        nonlocal nodes, solutions, max_depth
        nodes += 1
        max_depth = max(max_depth, depth)
        if not remaining:
            solutions += 1
            return
        choices = []
        for facet in remaining:
            overlap = Q5_FACET_EDGE_MASKS[facet] & known
            compatible = tuple(
                mask for mask in embedded[facet] if not ((mask ^ values) & overlap)
            )
            choices.append((len(compatible), facet, compatible))
        count, facet, compatible = min(choices, key=lambda item: item[0])
        if count == 0:
            return
        next_remaining = tuple(item for item in remaining if item != facet)
        for mask in compatible:
            visit(
                values | mask,
                known | Q5_FACET_EDGE_MASKS[facet],
                next_remaining,
                depth + 1,
            )

    visit(
        embed_q4(fixed_local_mask, fixed_facet),
        Q5_FACET_EDGE_MASKS[fixed_facet],
        tuple(facet for facet in Q5_FACETS if facet != fixed_facet),
        0,
    )
    return solutions, nodes, max_depth


def residual_searches(
    census: dict[int, int],
    boundary_data: dict[int, tuple[int, int]],
) -> tuple[dict[str, int], dict[str, list[tuple[str, int, int]]]]:
    equality = tuple(
        mask
        for mask, slack in census.items()
        if mask and 17 * slack - 3 * mask.bit_count() == 0
    )
    good42 = tuple(
        mask
        for mask, slack in census.items()
        if 17 * slack - 3 * mask.bit_count() == 42
        and boundary_data[mask] == (0, 0)
    )
    deficit48 = tuple(
        mask
        for mask, slack in census.items()
        if 17 * slack - 3 * mask.bit_count() == 48
        and boundary_data[mask] == (3, 0)
    )
    if tuple(map(len, (equality, good42, deficit48))) != (64, 32, 192):
        raise AssertionError("unexpected residual catalog sizes")
    orbit_data = {
        "equality": orbit_summary(set(equality)),
        "good42": orbit_summary(set(good42)),
        "deficit48": orbit_summary(set(deficit48)),
    }
    if tuple(map(len, orbit_data.values())) != (1, 1, 1):
        raise AssertionError("each residual catalog must be one Q4 orbit")

    special = (0, 0)
    remaining = tuple(facet for facet in Q5_FACETS if facet != special)
    summaries = {}

    rows = []
    fixed42 = min(good42)
    for empty_facet in remaining:
        candidates = {
            facet: ((0,) if facet == empty_facet else equality)
            for facet in remaining
        }
        rows.append(exact_q5_search(special, fixed42, candidates))
    summaries["42"] = {
        "cases": len(rows),
        "nodes": sum(row[1] for row in rows),
        "max_depth": max(row[2] for row in rows),
        "solutions": sum(row[0] for row in rows),
    }

    rows = []
    for second in remaining:
        candidates = {
            facet: (good42 if facet == second else equality)
            for facet in remaining
        }
        rows.append(exact_q5_search(special, fixed42, candidates))
    summaries["84"] = {
        "cases": len(rows),
        "nodes": sum(row[1] for row in rows),
        "max_depth": max(row[2] for row in rows),
        "solutions": sum(row[0] for row in rows),
    }

    fixed48 = min(deficit48)
    rows = []
    for positions42 in combinations(remaining, 2):
        for empty_facet in remaining:
            if empty_facet in positions42:
                continue
            candidates = {
                facet: (
                    good42
                    if facet in positions42
                    else (0,)
                    if facet == empty_facet
                    else equality
                )
                for facet in remaining
            }
            rows.append(exact_q5_search(special, fixed48, candidates))
    summaries["132"] = {
        "cases": len(rows),
        "nodes": sum(row[1] for row in rows),
        "max_depth": max(row[2] for row in rows),
        "solutions": sum(row[0] for row in rows),
    }

    rows = []
    for other_positive in combinations(remaining, 2):
        for empty_facet in remaining:
            if empty_facet in other_positive:
                continue
            candidates = {
                facet: (
                    deficit48
                    if facet in other_positive
                    else (0,)
                    if facet == empty_facet
                    else equality
                )
                for facet in remaining
            }
            rows.append(exact_q5_search(special, fixed48, candidates))
    summaries["144"] = {
        "cases": len(rows),
        "nodes": sum(row[1] for row in rows),
        "max_depth": max(row[2] for row in rows),
        "solutions": sum(row[0] for row in rows),
    }
    return summaries, orbit_data


def verify() -> dict[str, object]:
    if (len(EDGES), len(SQUARES), len(FACETS)) != (32, 24, 8):
        raise AssertionError("incorrect Q4 incidence structure")
    if (len(Q5_EDGES), len(Q5_FACETS)) != (80, 10):
        raise AssertionError("incorrect Q5 incidence structure")

    census, census_nodes, local_table = facet_gluing_census()
    if len(census) != 92_993 or census_nodes != 58_304_793:
        raise AssertionError("unexpected Q4 low-slack census size")
    for mask, slack in census.items():
        if direct_q4_statistics(mask)[3] != slack:
            raise AssertionError("facet and direct Q4 slack computations disagree")

    spectrum = Counter((mask.bit_count(), slack) for mask, slack in census.items())
    if any(17 * slack - 3 * mask.bit_count() < 0 for mask, slack in census.items()):
        raise AssertionError("the Q4 deficit must be nonnegative")
    equality = tuple(
        mask
        for mask, slack in census.items()
        if mask and 17 * slack - 3 * mask.bit_count() == 0
    )
    if len(equality) != 64:
        raise AssertionError("unexpected number of zero-deficit Q4 patterns")

    boundary_data, class_counts = boundary_classification(census, equality)
    capacity_distributions = {
        live: live_support_distribution(live) for live in range(1, 11)
    }
    capacity_maxima = {
        live: max(distribution)
        for live, distribution in capacity_distributions.items()
    }
    zero_profile_cases = []
    for live_count in range(1, 11):
        incidence = 17 * live_count
        if incidence % 4:
            continue
        global_edges = incidence // 4
        zero_profile_cases.append(
            (live_count, global_edges, capacity_maxima[live_count])
        )
    if zero_profile_cases != [(4, 17, 1), (8, 34, 28)]:
        raise AssertionError("unexpected zero-deficit Q5 profile check")
    survivors = structural_profile_survivors(class_counts, capacity_maxima)
    expected_survivors = (
        (42, ((42, 20, 0, 0),), 8, 1, 39),
        (84, ((42, 20, 0, 0), (42, 20, 0, 0)), 8, 0, 44),
        (
            132,
            ((42, 20, 0, 0), (42, 20, 0, 0), (48, 18, 3, 0)),
            6,
            1,
            40,
        ),
        (
            144,
            ((48, 18, 3, 0), (48, 18, 3, 0), (48, 18, 3, 0)),
            6,
            1,
            39,
        ),
    )
    if survivors != expected_survivors:
        raise AssertionError("unexpected residual Q5 profiles below 166")

    residuals, orbit_data = residual_searches(census, boundary_data)
    expected_residuals = {
        "42": {"cases": 9, "nodes": 10, "max_depth": 1, "solutions": 0},
        "84": {"cases": 9, "nodes": 18, "max_depth": 1, "solutions": 0},
        "132": {"cases": 252, "nodes": 252, "max_depth": 0, "solutions": 0},
        "144": {"cases": 252, "nodes": 252, "max_depth": 0, "solutions": 0},
    }
    if residuals != expected_residuals:
        raise AssertionError("a residual Q5 profile was not excluded")

    q5_edge_cap = 56
    q5_ratio = Fraction(12 * q5_edge_cap + DEFICIT_LIMIT, 34 * q5_edge_cap)
    global_slack_coefficient = q5_ratio / 12
    retained_coefficient = 1 - global_slack_coefficient
    asymptotic_constant = Fraction(19_992, 11_005)
    preceding_constant = Fraction(204, 113)
    if q5_ratio != Fraction(419, 952):
        raise AssertionError("incorrect Q5 slack/edge ratio")
    if global_slack_coefficient != Fraction(419, 11_424):
        raise AssertionError("incorrect global slack coefficient")
    if retained_coefficient != Fraction(11_005, 11_424):
        raise AssertionError("incorrect retained coefficient")
    if asymptotic_constant - preceding_constant != Fraction(14_076, 1_243_565):
        raise AssertionError("incorrect asymptotic improvement")
    if 19_992 * 295 - 204 * 28_979 != -14_076:
        raise AssertionError("incorrect finite-bound cross difference")

    class_rows = [(*key, count) for key, count in sorted(class_counts.items())]
    profile_class_hash = sha256(
        json.dumps(class_rows, separators=(",", ":")).encode("ascii")
    ).hexdigest()
    canonical = {
        "local_table": [(*key, count) for key, count in sorted(local_table.items())],
        "spectrum": [(*key, count) for key, count in sorted(spectrum.items())],
        "profile_classes": class_rows,
        "capacity_distributions": capacity_distributions,
        "zero_profile_cases": zero_profile_cases,
        "survivors": survivors,
        "residuals": residuals,
        "orbits": orbit_data,
    }
    audit_hash = sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("ascii")
    ).hexdigest()
    return {
        "q3_squarefree_patterns": 2902,
        "q3_retained_patterns_per_facet": sum(local_table.values()),
        "q4_facet_gluing_nodes": census_nodes,
        "q4_patterns_with_slack_at_most_13": len(census),
        "q4_normalized_graph_set_sha256": normalized_graph_hash(census),
        "q4_positive_profile_classes_below_166": len(class_counts),
        "profile_class_sha256": profile_class_hash,
        "structural_survivor_totals": [row[0] for row in survivors],
        "zero_profile_live_edges_capacity": zero_profile_cases,
        "residual_searches": residuals,
        "residual_orbits": orbit_data,
        "q5_deficit_lower_bound": DEFICIT_LIMIT,
        "external_q5_squarefree_edge_cap": q5_edge_cap,
        "q5_slack_edge_ratio": str(q5_ratio),
        "bound": "sat(Q_d,Q_2) >= 19992*d*2^d/(11005*d+28979) for d>=5",
        "asymptotic_constant": str(asymptotic_constant),
        "improvement_over_204_113": str(asymptotic_constant - preceding_constant),
        "finite_bound_cross_difference": "14076*(d-1)",
        "d7_real_bound": str(Fraction(19_992 * 7 * 2**7, 11_005 * 7 + 28_979)),
        "d7_integer_lower_bound": 169,
        "d8_integer_lower_bound": 350,
        "audit_sha256": audit_hash,
    }


def main() -> None:
    print(json.dumps(verify(), sort_keys=True, indent=2))
    print("status=PASS")


if __name__ == "__main__":
    main()
