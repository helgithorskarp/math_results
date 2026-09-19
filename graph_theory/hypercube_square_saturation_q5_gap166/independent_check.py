#!/usr/bin/env python3
"""Independent endpoint-pair and edge-branching check of the gap-166 result.

This checker does not import the production verifier.  It enumerates Q4
patterns by assigning the 32 global edges, represents boundary restrictions
as canonical Q3 endpoint masks, and checks residual Q5 profiles by constraint
propagation on the 80 global edges.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
import json


DIM = 4
MAX_COST = 26
LIMIT = 166
VERTICES = tuple(range(1 << DIM))
EDGES = tuple(
    sorted(
        (vertex, vertex ^ (1 << coordinate))
        for vertex in VERTICES
        for coordinate in range(DIM)
        if vertex < (vertex ^ (1 << coordinate))
    )
)
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
FACETS = tuple(
    (coordinate, bit) for coordinate in range(DIM) for bit in (0, 1)
)
FACET_VERTEX_SETS = tuple(
    frozenset(vertex for vertex in VERTICES if ((vertex >> coordinate) & 1) == bit)
    for coordinate, bit in FACETS
)
FACET_EDGES = tuple(
    tuple(index for index, edge in enumerate(EDGES) if set(edge) <= vertices)
    for vertices in FACET_VERTEX_SETS
)
EDGE_FACETS = tuple(
    tuple(facet for facet, edges in enumerate(FACET_EDGES) if edge in edges)
    for edge in range(len(EDGES))
)
SQUARES = tuple(
    tuple(
        EDGE_INDEX[tuple(sorted(edge))]
        for edge in (
            (base, base ^ (1 << first)),
            (base, base ^ (1 << second)),
            (base ^ (1 << first), base ^ (1 << first) ^ (1 << second)),
            (base ^ (1 << second), base ^ (1 << first) ^ (1 << second)),
        )
    )
    for first in range(DIM)
    for second in range(first + 1, DIM)
    for base in VERTICES
    if not (base >> first) & 1 and not (base >> second) & 1
)
FACET_SQUARES = tuple(
    tuple(square for square in SQUARES if all(edge in edges for edge in square))
    for edges in map(frozenset, FACET_EDGES)
)


def local_cost(mask: int, facet: int) -> int:
    missing = []
    inactive_incidences = 0
    for square in FACET_SQUARES[facet]:
        chosen = [edge for edge in square if (mask >> edge) & 1]
        if len(chosen) == 4:
            raise ValueError("completed square")
        if len(chosen) == 3:
            missing.append(next(edge for edge in square if edge not in chosen))
        else:
            inactive_incidences += len(chosen)
    return 2 * inactive_incidences + 4 * (len(missing) - len(set(missing))) - len(missing)


def candidates(facet: int) -> tuple[tuple[int, int], ...]:
    result = []
    edges = FACET_EDGES[facet]
    for local_mask in range(1 << len(edges)):
        mask = sum(
            ((local_mask >> position) & 1) << edge
            for position, edge in enumerate(edges)
        )
        try:
            cost = local_cost(mask, facet)
        except ValueError:
            continue
        if cost < 0:
            raise AssertionError("Q3 slack must be nonnegative")
        if cost <= MAX_COST:
            result.append((mask, cost))
    return tuple(result)


def census() -> tuple[set[int], int, int]:
    """Assign all 32 Q4 edges and prune by local-state slack minima."""

    initial = tuple(candidates(facet) for facet in range(len(FACET_EDGES)))
    complete: set[int] = set()
    nodes = 0
    pruned = 0

    def visit(depth: int, values: int, states: tuple[tuple[tuple[int, int], ...], ...]) -> None:
        nonlocal nodes, pruned
        nodes += 1
        if sum(min(cost for _, cost in facet_states) for facet_states in states) > MAX_COST:
            pruned += 1
            return
        if depth == len(EDGES):
            complete.add(values)
            return
        edge = depth
        for bit in (0, 1):
            next_states = list(states)
            possible = True
            for facet in EDGE_FACETS[edge]:
                filtered = tuple(
                    state
                    for state in next_states[facet]
                    if ((state[0] >> edge) & 1) == bit
                )
                if not filtered:
                    possible = False
                    break
                next_states[facet] = filtered
            if possible:
                visit(depth + 1, values | (bit << edge), tuple(next_states))

    visit(0, 0, initial)
    return complete, nodes, pruned


def direct_slack(mask: int) -> int:
    witnesses = []
    for square in SQUARES:
        chosen = [edge for edge in square if (mask >> edge) & 1]
        if len(chosen) == 4:
            raise AssertionError("enumerated pattern is not square-free")
        if len(chosen) == 3:
            witnesses.append(next(edge for edge in square if edge not in chosen))
    multiplicities = Counter(witnesses)
    pairs = sum(count * (count - 1) // 2 for count in multiplicities.values())
    return 6 * mask.bit_count() - 7 * len(witnesses) + 2 * pairs


def normalized_graph_hash(masks: set[int]) -> str:
    rows = [
        tuple(edge for index, edge in enumerate(EDGES) if (mask >> index) & 1)
        for mask in masks
    ]
    canonical = json.dumps(sorted(rows), separators=(",", ":"))
    return sha256(canonical.encode("ascii")).hexdigest()


Q3_EDGES = tuple(
    sorted(
        (vertex, vertex ^ (1 << coordinate))
        for vertex in range(8)
        for coordinate in range(3)
        if vertex < (vertex ^ (1 << coordinate))
    )
)
Q3_EDGE_INDEX = {edge: index for index, edge in enumerate(Q3_EDGES)}


def facet_signature(mask: int, facet_index: int) -> int:
    """Map a Q4 facet restriction to a canonical endpoint-pair Q3 mask."""

    coordinate, _ = FACETS[facet_index]
    free = tuple(index for index in range(DIM) if index != coordinate)
    local_mask = 0
    for edge in FACET_EDGES[facet_index]:
        if not (mask >> edge) & 1:
            continue
        local_vertices = []
        for vertex in EDGES[edge]:
            local_vertex = 0
            for local_coordinate, global_coordinate in enumerate(free):
                local_vertex |= ((vertex >> global_coordinate) & 1) << local_coordinate
            local_vertices.append(local_vertex)
        pair = tuple(sorted(local_vertices))
        local_mask |= 1 << Q3_EDGE_INDEX[pair]
    return local_mask


def permute_vertex(vertex: int, permutation: tuple[int, ...]) -> int:
    image = 0
    for old_coordinate, new_coordinate in enumerate(permutation):
        image |= ((vertex >> old_coordinate) & 1) << new_coordinate
    return image


def transform(mask: int, translation: int, permutation: tuple[int, ...]) -> int:
    image = 0
    for edge_index, (first, second) in enumerate(EDGES):
        if not (mask >> edge_index) & 1:
            continue
        pair = tuple(
            sorted(
                (
                    permute_vertex(first, permutation) ^ translation,
                    permute_vertex(second, permutation) ^ translation,
                )
            )
        )
        image |= 1 << EDGE_INDEX[pair]
    return image


def assert_single_orbit(masks: set[int]) -> tuple[str, int, int]:
    representative = min(masks)
    orbit = {
        transform(representative, translation, permutation)
        for translation in VERTICES
        for permutation in permutations(range(DIM))
    }
    if orbit != masks:
        raise AssertionError("residual class is not the asserted single Q4 orbit")
    return f"0x{representative:08x}", len(orbit), 384 // len(orbit)


def classify_boundaries(
    masks: set[int], slack_by_mask: dict[int, int]
) -> tuple[dict[int, tuple[int, int]], Counter[tuple[int, int, int, int]]]:
    equality = {
        mask
        for mask in masks
        if mask and 17 * slack_by_mask[mask] - 3 * mask.bit_count() == 0
    }
    extendable = {
        facet_signature(mask, facet)
        for mask in equality
        for facet in range(len(FACETS))
    }
    boundary_data = {}
    class_counts: Counter[tuple[int, int, int, int]] = Counter()
    for mask in masks:
        if not mask:
            continue
        signatures = tuple(facet_signature(mask, facet) for facet in range(len(FACETS)))
        bad = sum(signature not in extendable for signature in signatures)
        empty = signatures.count(0)
        boundary_data[mask] = (bad, empty)
        deficit = 17 * slack_by_mask[mask] - 3 * mask.bit_count()
        if 0 < deficit < LIMIT:
            class_counts[(deficit, mask.bit_count(), bad, empty)] += 1
    return boundary_data, class_counts


Q5_DIM = 5
Q5_VERTICES = tuple(range(1 << Q5_DIM))
Q5_EDGES = tuple(
    sorted(
        (vertex, vertex ^ (1 << coordinate))
        for vertex in Q5_VERTICES
        for coordinate in range(Q5_DIM)
        if vertex < (vertex ^ (1 << coordinate))
    )
)
Q5_EDGE_INDEX = {edge: index for index, edge in enumerate(Q5_EDGES)}
Q5_FACETS = tuple(
    (coordinate, bit) for coordinate in range(Q5_DIM) for bit in (0, 1)
)
Q5_FACET_EDGES = tuple(
    tuple(
        edge_index
        for edge_index, edge in enumerate(Q5_EDGES)
        if all(((vertex >> coordinate) & 1) == bit for vertex in edge)
    )
    for coordinate, bit in Q5_FACETS
)
Q5_EDGE_FACETS = tuple(
    tuple(facet for facet, edges in enumerate(Q5_FACET_EDGES) if edge in edges)
    for edge in range(len(Q5_EDGES))
)


def live_capacity_maxima() -> dict[int, int]:
    edge_facets = tuple(frozenset(Q5_FACETS[index] for index in facets) for facets in Q5_EDGE_FACETS)
    return {
        live_count: max(
            sum(containing <= frozenset(live) for containing in edge_facets)
            for live in combinations(Q5_FACETS, live_count)
        )
        for live_count in range(1, 11)
    }


def structural_survivors(
    class_counts: Counter[tuple[int, int, int, int]]
) -> tuple[tuple[object, ...], ...]:
    classes = tuple(sorted(class_counts))
    capacities = live_capacity_maxima()
    survivors: set[tuple[object, ...]] = set()

    def visit(start: int, chosen: tuple[tuple[int, int, int, int], ...], total: int) -> None:
        if chosen and total % 2 == 0:
            positive = len(chosen)
            for equality_count in range(11 - positive):
                empty = 10 - positive - equality_count
                incidence = sum(item[1] for item in chosen) + 17 * equality_count
                if incidence % 4:
                    continue
                edges = incidence // 4
                live = positive + equality_count
                if not edges or edges > capacities[live]:
                    continue
                if any(item[2] > positive + empty - 1 for item in chosen):
                    continue
                survivors.add((total, chosen, equality_count, empty, edges))
        if len(chosen) == 9:
            return
        for index in range(start, len(classes)):
            item = classes[index]
            if total + item[0] >= LIMIT:
                break
            visit(index, chosen + (item,), total + item[0])

    visit(0, (), 0)
    return tuple(sorted(survivors))


def embed_q4(mask: int, facet_index: int) -> int:
    coordinate, bit = Q5_FACETS[facet_index]
    free = tuple(index for index in range(Q5_DIM) if index != coordinate)
    result = 0
    for edge_index, (first, second) in enumerate(EDGES):
        if not (mask >> edge_index) & 1:
            continue
        global_vertices = []
        for local_vertex in (first, second):
            vertex = bit << coordinate
            for local_coordinate, global_coordinate in enumerate(free):
                vertex |= ((local_vertex >> local_coordinate) & 1) << global_coordinate
            global_vertices.append(vertex)
        result |= 1 << Q5_EDGE_INDEX[tuple(sorted(global_vertices))]
    return result


def edge_constraint_search(local_candidates: tuple[tuple[int, ...], ...]) -> tuple[int, int]:
    """Propagate/branch on global Q5 edge values, not on facet choices."""

    states = tuple(
        tuple(embed_q4(mask, facet) for mask in masks)
        for facet, masks in enumerate(local_candidates)
    )
    nodes = 0
    solutions = 0

    def visit(current: tuple[tuple[int, ...], ...]) -> None:
        nonlocal nodes, solutions
        nodes += 1
        current = tuple(tuple(dict.fromkeys(items)) for items in current)
        while True:
            changed = False
            for edge, incident in enumerate(Q5_EDGE_FACETS):
                possible = []
                for bit in (0, 1):
                    if all(any(((mask >> edge) & 1) == bit for mask in current[f]) for f in incident):
                        possible.append(bit)
                if not possible:
                    return
                if len(possible) == 1:
                    bit = possible[0]
                    next_current = list(current)
                    for facet in incident:
                        filtered = tuple(
                            mask for mask in next_current[facet] if ((mask >> edge) & 1) == bit
                        )
                        if not filtered:
                            return
                        if len(filtered) != len(next_current[facet]):
                            changed = True
                            next_current[facet] = filtered
                    current = tuple(next_current)
            if not changed:
                break
        branch = None
        branch_score = -1
        for edge, incident in enumerate(Q5_EDGE_FACETS):
            if not all(
                all(((mask >> edge) & 1) == ((current[facet][0] >> edge) & 1) for mask in current[facet])
                for facet in incident
            ):
                score = sum(len(current[facet]) for facet in incident)
                if score > branch_score:
                    branch_score = score
                    branch = (edge, incident)
        if branch is None:
            solutions += 1
            return
        edge, incident = branch
        for bit in (0, 1):
            next_current = list(current)
            possible = True
            for facet in incident:
                filtered = tuple(
                    mask for mask in next_current[facet] if ((mask >> edge) & 1) == bit
                )
                if not filtered:
                    possible = False
                    break
                next_current[facet] = filtered
            if possible:
                visit(tuple(next_current))

    visit(states)
    return solutions, nodes


def residual_searches(
    masks: set[int],
    slack_by_mask: dict[int, int],
    boundary_data: dict[int, tuple[int, int]],
) -> tuple[dict[str, dict[str, int]], dict[str, tuple[str, int, int]]]:
    equality = tuple(
        mask
        for mask in masks
        if mask and 17 * slack_by_mask[mask] - 3 * mask.bit_count() == 0
    )
    good42 = tuple(
        mask
        for mask in masks
        if 17 * slack_by_mask[mask] - 3 * mask.bit_count() == 42
        and boundary_data[mask] == (0, 0)
    )
    deficit48 = tuple(
        mask
        for mask in masks
        if 17 * slack_by_mask[mask] - 3 * mask.bit_count() == 48
        and boundary_data[mask] == (3, 0)
    )
    orbits = {
        "equality": assert_single_orbit(set(equality)),
        "good42": assert_single_orbit(set(good42)),
        "deficit48": assert_single_orbit(set(deficit48)),
    }
    special = 0
    remaining = tuple(index for index in range(10) if index != special)
    summaries = {}

    def run(cases: list[tuple[tuple[int, ...], ...]]) -> dict[str, int]:
        rows = [edge_constraint_search(case) for case in cases]
        return {
            "cases": len(rows),
            "nodes": sum(row[1] for row in rows),
            "solutions": sum(row[0] for row in rows),
        }

    cases = []
    for empty in remaining:
        catalogs = []
        for facet in range(10):
            catalogs.append(
                (min(good42),)
                if facet == special
                else (0,)
                if facet == empty
                else equality
            )
        cases.append(tuple(catalogs))
    summaries["42"] = run(cases)

    cases = []
    for second in remaining:
        catalogs = []
        for facet in range(10):
            catalogs.append(
                (min(good42),)
                if facet == special
                else good42
                if facet == second
                else equality
            )
        cases.append(tuple(catalogs))
    summaries["84"] = run(cases)

    cases = []
    for positions42 in combinations(remaining, 2):
        for empty in remaining:
            if empty in positions42:
                continue
            catalogs = []
            for facet in range(10):
                catalogs.append(
                    (min(deficit48),)
                    if facet == special
                    else good42
                    if facet in positions42
                    else (0,)
                    if facet == empty
                    else equality
                )
            cases.append(tuple(catalogs))
    summaries["132"] = run(cases)

    cases = []
    for other_positive in combinations(remaining, 2):
        for empty in remaining:
            if empty in other_positive:
                continue
            catalogs = []
            for facet in range(10):
                catalogs.append(
                    (min(deficit48),)
                    if facet == special
                    else deficit48
                    if facet in other_positive
                    else (0,)
                    if facet == empty
                    else equality
                )
            cases.append(tuple(catalogs))
    summaries["144"] = run(cases)
    return summaries, orbits


def independent_check() -> dict[str, object]:
    if len(EDGES) != 32 or len(SQUARES) != 24 or set(map(len, EDGE_FACETS)) != {3}:
        raise AssertionError("incorrect Q4 incidence structure")
    masks, nodes, pruned = census()
    if len(masks) != 92_993:
        raise AssertionError("unexpected Q4 census size")
    slack_by_mask = {mask: direct_slack(mask) for mask in masks}
    graph_hash = normalized_graph_hash(masks)
    expected_hash = "c5b51fe95ded5988f87006471a4edad6ec3f92130e85cae746f54f7a94ef053a"
    if graph_hash != expected_hash:
        raise AssertionError("entry-level Q4 set differs from production")

    boundary_data, class_counts = classify_boundaries(masks, slack_by_mask)
    survivors = structural_survivors(class_counts)
    expected_totals = [42, 84, 132, 144]
    if [row[0] for row in survivors] != expected_totals:
        raise AssertionError("independent structural profile list differs")
    residuals, orbits = residual_searches(masks, slack_by_mask, boundary_data)
    if any(summary["solutions"] for summary in residuals.values()):
        raise AssertionError("an allegedly excluded residual profile has a solution")

    class_rows = [(*key, count) for key, count in sorted(class_counts.items())]
    class_hash = sha256(
        json.dumps(class_rows, separators=(",", ":")).encode("ascii")
    ).hexdigest()
    return {
        "representation": "unordered endpoint pairs",
        "q4_algorithm": "global edge branching with local-state lower bounds",
        "q5_algorithm": "global edge constraint propagation",
        "q4_edge_branch_nodes": nodes,
        "q4_edge_branch_pruned": pruned,
        "q4_patterns_with_slack_at_most_13": len(masks),
        "q4_normalized_graph_set_sha256": graph_hash,
        "profile_class_sha256": class_hash,
        "structural_survivor_totals": expected_totals,
        "residual_searches": residuals,
        "residual_orbits": orbits,
        "q5_deficit_lower_bound": LIMIT,
    }


def main() -> None:
    print(json.dumps(independent_check(), sort_keys=True, indent=2))
    print("status=PASS")


if __name__ == "__main__":
    main()
