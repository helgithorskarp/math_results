#!/usr/bin/env python3
"""Independent audits for the all-forward r=4, N=4m+2 boundary theorem.

The checker first constructs copies from omitted pairs, before using any
cyclic occurrence formulas.  Its coupled-repair audit enumerates actual
R-start subsets modulo translation and computes exact hitting numbers for the
resulting Q- and S-start families by a 2^r-state dynamic program.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import deque
from functools import lru_cache
from itertools import combinations
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def pairs(n: int) -> list[tuple[int, int]]:
    return list(combinations(range(n), 2))


def canonical_pair(a: int, b: int, n: int) -> tuple[int, int]:
    a %= n
    b %= n
    assert a != b
    return (a, b) if a < b else (b, a)


def q_edges(n: int, m: int, start: int) -> frozenset[tuple[int, int]]:
    vertices = [(start + j) % n for j in range(m + 1)]
    return frozenset(tuple(sorted(edge)) for edge in combinations(vertices, 2))


def r_edges(n: int, m: int, start: int) -> frozenset[tuple[int, int]]:
    left = [(start + j) % n for j in range(m)]
    right = [(start + m + 1 + j) % n for j in range(m)]
    return frozenset(canonical_pair(a, b, n) for a in left for b in right)


def s_edges(n: int, m: int, start: int) -> frozenset[tuple[int, int]]:
    half = 2 * m + 1
    left = [(start + j) % n for j in range(m)]
    right = [(start + half + j) % n for j in range(m)]
    return frozenset(canonical_pair(a, b, n) for a in left for b in right)


def direct_incidence(m: int):
    """Construct canonical copies and incidences solely from the definition."""
    n = 4 * m + 2
    omissions = pairs(n)
    copies: list[tuple[tuple[int, int, int, int], ...]] = []
    occurrences: dict[tuple[int, int, int, int], set[tuple[int, int]]] = {}
    for omitted in omissions:
        omitted_set = set(omitted)
        remaining = [v for v in range(n) if v not in omitted_set]
        copy = tuple(
            (
                remaining[j],
                remaining[m + j],
                remaining[2 * m + j],
                remaining[3 * m + j],
            )
            for j in range(m)
        )
        copies.append(copy)
        for edge in copy:
            occurrences.setdefault(edge, set()).add(omitted)
    return n, omissions, copies, occurrences


def graph_shape(edge_set: set[tuple[int, int]], m: int) -> str:
    support = {v for edge in edge_set for v in edge}
    degrees = {v: sum(v in edge for edge in edge_set) for v in support}
    if (
        len(support) == m + 1
        and len(edge_set) == m * (m + 1) // 2
        and set(degrees.values()) == {m}
    ):
        return "clique"
    if len(support) != 2 * m or len(edge_set) != m * m or set(degrees.values()) != {m}:
        return "other"
    adjacency = {v: set() for v in support}
    for a, b in edge_set:
        adjacency[a].add(b)
        adjacency[b].add(a)
    colors: dict[int, int] = {}
    for root in support:
        if root in colors:
            continue
        colors[root] = 0
        stack = [root]
        while stack:
            v = stack.pop()
            for w in adjacency[v]:
                if w not in colors:
                    colors[w] = 1 - colors[v]
                    stack.append(w)
                elif colors[w] == colors[v]:
                    return "other"
    side_sizes = sorted(sum(color == side for color in colors.values()) for side in (0, 1))
    return "biclique" if side_sizes == [m, m] else "other"


def as_mask(edge_set: set[tuple[int, int]] | frozenset[tuple[int, int]], index) -> int:
    value = 0
    for edge in edge_set:
        value |= 1 << index[edge]
    return value


def audit_classification(m: int):
    n, omissions, copies, occurrences = direct_incidence(m)
    half = 2 * m + 1
    omission_index = {edge: i for i, edge in enumerate(omissions)}
    direct_masks = {as_mask(graph, omission_index) for graph in occurrences.values()}
    q_masks = {as_mask(q_edges(n, m, s), omission_index) for s in range(n)}
    r_masks = {as_mask(r_edges(n, m, s), omission_index) for s in range(n)}
    s_masks = {as_mask(s_edges(n, m, s), omission_index) for s in range(half)}
    shapes = {"clique": 0, "biclique": 0, "other": 0}
    for graph in occurrences.values():
        shapes[graph_shape(graph, m)] += 1
    assert len(occurrences) == 2 * n + half
    assert len(direct_masks) == 2 * n + half
    assert len(q_masks) == n and len(r_masks) == n and len(s_masks) == half
    assert len(q_masks | r_masks | s_masks) == 2 * n + half
    assert direct_masks == q_masks | r_masks | s_masks
    assert shapes == {"clique": n, "biclique": n + half, "other": 0}
    return n, omissions, copies, occurrences, shapes


def exact_no_fourteen(m: int, copies, occurrences, omissions):
    """Definition-level decision search for a blocker of size at most 14."""
    candidates = sorted(occurrences)
    candidate_index = {edge: i for i, edge in enumerate(candidates)}
    omission_index = {edge: i for i, edge in enumerate(omissions)}
    masks = []
    for edge in candidates:
        masks.append(as_mask(occurrences[edge], omission_index))
    copy_options = [tuple(candidate_index[edge] for edge in copy) for copy in copies]
    full = (1 << len(copies)) - 1
    calls = 0

    @lru_cache(maxsize=None)
    def can_cover(uncovered: int, budget: int) -> bool:
        nonlocal calls
        calls += 1
        if uncovered == 0:
            return True
        if budget == 0:
            return False
        gains = [(mask & uncovered).bit_count() for mask in masks]
        best = max(gains)
        if best == 0 or (uncovered.bit_count() + best - 1) // best > budget:
            return False
        if uncovered.bit_count() > sum(sorted(gains, reverse=True)[:budget]):
            return False

        chosen_options = None
        chosen_profile = None
        remaining = uncovered
        while remaining:
            bit = remaining & -remaining
            copy_id = bit.bit_length() - 1
            options = copy_options[copy_id]
            profile = tuple(sorted((gains[i] for i in options), reverse=True))
            if chosen_profile is None or profile < chosen_profile:
                chosen_profile = profile
                chosen_options = options
            remaining ^= bit
        assert chosen_options is not None
        for candidate in sorted(chosen_options, key=lambda i: gains[i], reverse=True):
            new_uncovered = uncovered & ~masks[candidate]
            if new_uncovered != uncovered and can_cover(new_uncovered, budget - 1):
                return True
        return False

    fourteen_exists = can_cover(full, 14)
    n = 4 * m + 2
    upper = [
        edge
        for edge in combinations(range(n), 4)
        if all(edge[i + 1] - edge[i] >= m for i in range(3))
        and edge[3] <= n - m
    ]
    assert len(upper) == 15
    upper_mask = 0
    for edge in upper:
        upper_mask |= masks[candidate_index[edge]]
    assert upper_mask == full
    return {
        "m": m,
        "copies": len(copies),
        "active_four_edges": len(candidates),
        "fourteen_blocker_exists": fourteen_exists,
        "fifteen_blocker_verified": True,
        "search_states": can_cover.cache_info().currsize,
        "search_calls": calls,
    }


def cyclic_distance(n: int, edge: tuple[int, int]) -> int:
    delta = edge[1] - edge[0]
    return min(delta, n - delta)


def hitting_number(containers: list[set[int]], start_count: int) -> int:
    """Minimum number of starts hitting every set in containers."""
    target = (1 << len(containers)) - 1
    coverage = []
    for start in range(start_count):
        mask = sum(1 << i for i, choices in enumerate(containers) if start in choices)
        if mask:
            coverage.append(mask)
    distances = [-1] * (target + 1)
    distances[0] = 0
    queue = deque([0])
    while queue:
        state = queue.popleft()
        if state == target:
            return distances[state]
        for cover in coverage:
            new_state = state | cover
            if distances[new_state] < 0:
                distances[new_state] = distances[state] + 1
                queue.append(new_state)
    raise AssertionError("repair family has no hitting set")


def normalized_repair_audit(m: int):
    """Enumerate actual R-start subsets modulo translation, without gap formulas."""
    n = 4 * m + 2
    half = 2 * m + 1
    omission_list = pairs(n)
    index = {edge: i for i, edge in enumerate(omission_list)}
    q_by_start = [q_edges(n, m, s) for s in range(n)]
    r_by_start = [r_edges(n, m, s) for s in range(n)]
    s_by_start = [s_edges(n, m, s) for s in range(half)]
    q_containers = {
        edge: {s for s, graph in enumerate(q_by_start) if edge in graph}
        for edge in omission_list
    }
    r_containers = {
        edge: {s for s, graph in enumerate(r_by_start) if edge in graph}
        for edge in omission_list
    }
    s_containers = {
        edge: {s for s, graph in enumerate(s_by_start) if edge in graph}
        for edge in omission_list
    }
    middle = {edge for edge in omission_list if cyclic_distance(n, edge) == m + 1}
    middle_mask = as_mask(middle, index)
    r_middle_masks = [as_mask(graph, index) & middle_mask for graph in r_by_start]

    record = {
        "m": m,
        "normalized_five_start_sets": 0,
        "five_middle_covers": 0,
        "five_q_hit_five": 0,
        "five_s_hit_five": 0,
        "normalized_six_start_sets": 0,
        "six_middle_covers": 0,
        "six_q_hit_five": 0,
        "six_q_hit_six": 0,
        "six_min_total": 99,
    }

    for count in (5, 6):
        for tail in combinations(range(1, n), count - 1):
            starts = (0,) + tail
            record[f"normalized_{'five' if count == 5 else 'six'}_start_sets"] += 1
            covered = 0
            for start in starts:
                covered |= r_middle_masks[start]
            if covered != middle_mask:
                continue
            label = "five" if count == 5 else "six"
            record[f"{label}_middle_covers"] += 1
            selected_r = set(starts)
            q_repairs: list[set[int]] = []
            s_repairs: list[set[int]] = []
            for i, start in enumerate(starts):
                successor = starts[i + 1] if i + 1 < count else n
                gap = successor - start
                assert 1 <= gap <= m
                deficit = m - gap
                repair_length = deficit + 1
                low_pair = canonical_pair(start + m, start + m + gap, n)
                high_x = successor - 1
                high_pair = canonical_pair(
                    high_x, high_x + m + 1 + repair_length, n
                )
                assert selected_r.isdisjoint(r_containers[low_pair])
                assert selected_r.isdisjoint(r_containers[high_pair])
                assert q_containers[low_pair]
                assert s_containers[high_pair]
                q_repairs.append(q_containers[low_pair])
                s_repairs.append(s_containers[high_pair])

            q_hit = hitting_number(q_repairs, n)
            s_hit = hitting_number(s_repairs, half)
            total = count + q_hit + max(3, s_hit)
            assert total >= 15
            if count == 5:
                assert q_hit == 5 and s_hit == 5
                record["five_q_hit_five"] += 1
                record["five_s_hit_five"] += 1
            else:
                assert q_hit in (5, 6)
                record["six_q_hit_five" if q_hit == 5 else "six_q_hit_six"] += 1
                if q_hit == 5:
                    assert s_hit >= 4
                record["six_min_total"] = min(record["six_min_total"], total)
    assert record["five_middle_covers"] > 0 and record["six_middle_covers"] > 0
    return record


def boundary_audit():
    m = 1
    n, omissions, copies, occurrences = direct_incidence(m)
    assert n == 6 and len(copies) == 15 and len(occurrences) == 15
    assert all(len(graph) == 1 for graph in occurrences.values())
    return {
        "excluded_m1_formula_value": 0,
        "excluded_m1_required_blocker": 15,
        "ambient_4m_plus_1_omissions": 1,
        "ambient_4m_plus_2_omissions": 2,
        "ambient_4m_plus_3_omissions": 3,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--classification-max", type=int, default=20)
    parser.add_argument("--repair-max", type=int, default=10)
    parser.add_argument("--search-max", type=int, default=4)
    args = parser.parse_args()
    assert 2 <= args.search_max <= args.classification_max
    assert 2 <= args.repair_max <= args.classification_max

    classification = []
    searches = []
    for m in range(2, args.classification_max + 1):
        n, omissions, copies, occurrences, shapes = audit_classification(m)
        classification.append(
            {"m": m, "N": n, "copies": len(copies), "active": len(occurrences), "shapes": shapes}
        )
        if m <= args.search_max:
            searches.append(exact_no_fourteen(m, copies, occurrences, omissions))
    repairs = [normalized_repair_audit(m) for m in range(2, args.repair_max + 1)]
    result = {
        "status": "VERIFIED",
        "classification": classification,
        "definition_level_search": searches,
        "normalized_repair_audit": repairs,
        "boundary": boundary_audit(),
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(canonical).hexdigest()
    expected_path = ROOT / "EXPECTED.json"
    if expected_path.exists() and (
        args.classification_max,
        args.repair_max,
        args.search_max,
    ) == (20, 10, 4):
        expected = json.loads(expected_path.read_text())
        assert expected == {
            "classification_max": args.classification_max,
            "repair_max": args.repair_max,
            "result_sha256": digest,
            "search_max": args.search_max,
        }
    print(json.dumps(result, indent=2, sort_keys=True))
    print("result_sha256", digest)


if __name__ == "__main__":
    main()
