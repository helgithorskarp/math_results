#!/usr/bin/env python3
"""Exact definition-level checks for the all-forward rank-six theorem."""

from __future__ import annotations

import hashlib
import itertools
import json
import platform
from functools import lru_cache


def cyclic_interval(start: int, length: int, modulus: int) -> tuple[int, ...]:
    return tuple((start + offset) % modulus for offset in range(length))


def pairs(vertices) -> frozenset[tuple[int, int]]:
    return frozenset(tuple(sorted(pair)) for pair in itertools.combinations(vertices, 2))


def modeled_occurrences(m: int):
    n = 6 * m + 2
    half = n // 2
    result = {}
    for start in range(n):
        result[(0, start)] = pairs(cyclic_interval(start, m + 1, n))
    for band in (1, 2):
        for start in range(n):
            left = cyclic_interval(start, m, n)
            right = cyclic_interval(start + band * m + 1, m, n)
            result[(band, start)] = frozenset(
                tuple(sorted((x, y))) for x in left for y in right
            )
    for start in range(half):
        left = cyclic_interval(start, m, n)
        right = cyclic_interval(start + half, m, n)
        result[(3, start)] = frozenset(
            tuple(sorted((x, y))) for x in left for y in right
        )
    return result


def direct_occurrences(m: int):
    n = 6 * m + 2
    occurrences: dict[tuple[int, ...], set[tuple[int, int]]] = {}
    for omitted in itertools.combinations(range(n), 2):
        omitted_set = set(omitted)
        retained = [vertex for vertex in range(n) if vertex not in omitted_set]
        assert len(retained) == 6 * m
        for offset in range(m):
            active = tuple(retained[offset + part * m] for part in range(6))
            occurrences.setdefault(active, set()).add(omitted)
    return {edge: frozenset(omitted) for edge, omitted in occurrences.items()}


def private_layer_counts(graph: frozenset[tuple[int, int]], n: int):
    counts = {}
    for x, y in graph:
        distance = min(y - x, n - (y - x))
        counts[distance] = counts.get(distance, 0) + 1
    return counts


def blocker_edges(m: int):
    return {
        tuple(y[i] + i * (m - 1) for i in range(6))
        for y in itertools.combinations(range(8), 6)
    }


def canonical_copies(m: int):
    n = 6 * m + 2
    for omitted in itertools.combinations(range(n), 2):
        omitted_set = set(omitted)
        retained = [vertex for vertex in range(n) if vertex not in omitted_set]
        yield omitted, {
            tuple(retained[offset + part * m] for part in range(6))
            for offset in range(m)
        }


def weak_compositions(total: int, parts: int, cap: int):
    row = [0] * parts

    def rec(index: int, left: int):
        if index == parts:
            if left == 0:
                yield tuple(row)
            return
        low = max(0, left - cap * (parts - index - 1))
        high = min(cap, left)
        for value in range(low, high + 1):
            row[index] = value
            yield from rec(index + 1, left - value)

    yield from rec(0, total)


def interval_mask(start: int, length: int, modulus: int) -> int:
    mask = 0
    for offset in range(length):
        mask |= 1 << ((start + offset) % modulus)
    return mask


def repair_intervals(m: int, deficits: tuple[int, ...]):
    n = 6 * m + 2
    half = n // 2
    starts = [0]
    for deficit in deficits[:-1]:
        starts.append(starts[-1] + m - deficit)
    assert starts[-1] + m - deficits[-1] == n
    js = []
    ks = []
    count = len(deficits)
    for i, deficit in enumerate(deficits):
        next_start = starts[(i + 1) % count]
        if i == count - 1:
            next_start += n
        js.append(interval_mask(next_start, deficit + 1, n))
        ks.append(interval_mask(next_start - m, deficit + 1, half))
    return tuple(js), tuple(ks), tuple(starts)


def transversal_number(intervals: tuple[int, ...]) -> int:
    """Minimum hit count by exact subset DP on common intersections."""
    count = len(intervals)
    full = (1 << count) - 1
    common = [0] * (1 << count)
    common[0] = -1
    for subset in range(1, 1 << count):
        bit = subset & -subset
        index = bit.bit_length() - 1
        rest = subset ^ bit
        common[subset] = intervals[index] if not rest else common[rest] & intervals[index]

    @lru_cache(maxsize=None)
    def solve(subset: int) -> int:
        if not subset:
            return 0
        pivot = subset & -subset
        best = count
        group = subset
        while group:
            if group & pivot and common[group]:
                best = min(best, 1 + solve(subset ^ group))
            group = (group - 1) & subset
        return best

    return solve(full)


def audit_occurrences():
    records = []
    for m in range(2, 11):
        modeled = modeled_occurrences(m)
        direct = direct_occurrences(m)
        modeled_values = set(modeled.values())
        direct_values = set(direct.values())
        assert len(modeled_values) == len(modeled)
        assert len(direct_values) == len(direct)
        assert modeled_values == direct_values

        n = 6 * m + 2
        centers = (1, m + 1, 2 * m + 1, 3 * m + 1)
        type_counts = []
        for band, center in enumerate(centers):
            values = [graph for (kind, _), graph in modeled.items() if kind == band]
            expected = m
            assert all(private_layer_counts(graph, n).get(center, 0) == expected for graph in values)
            for other_band in range(4):
                if other_band == band:
                    continue
                others = [graph for (kind, _), graph in modeled.items() if kind == other_band]
                assert all(private_layer_counts(graph, n).get(center, 0) == 0 for graph in others)
            type_counts.append(len(values))

        blocker = blocker_edges(m)
        assert len(blocker) == 28
        copy_count = 0
        for _, copy in canonical_copies(m):
            copy_count += 1
            assert copy & blocker
        records.append(
            {
                "m": m,
                "active_edges": len(direct),
                "type_counts": type_counts,
                "canonical_copies": copy_count,
            }
        )
    return records


def audit_repairs():
    rows = 0
    cases = {"t7": 0, "t8_r7": 0, "t8_tight": 0, "t9_r7": 0}
    propagation = 0
    for m in range(2, 6):
        for t in (7, 8, 9):
            total = (t - 6) * m - 2
            for deficits in weak_compositions(total, t, m - 1):
                rows += 1
                js, ks, starts = repair_intervals(m, deficits)
                tau_j = transversal_number(js)
                tau_k = transversal_number(ks)
                if t == 7:
                    assert tau_k == 7
                    cases["t7"] += 1
                elif t == 8:
                    if tau_j <= 7:
                        assert tau_k >= 6
                        cases["t8_r7"] += 1
                    if tau_j == 8 and tau_k <= 4:
                        assert all(
                            sum(deficits[(i + offset) % 8] for offset in range(3)) <= m - 1
                            for i in range(8)
                        )
                        cases["t8_tight"] += 1
                        if m <= 4:
                            n = 6 * m + 2
                            for offsets in itertools.product(*(range(value + 1) for value in deficits)):
                                e = tuple(
                                    deficits[(i + 1) % 8]
                                    - offsets[(i + 1) % 8]
                                    + offsets[i]
                                    for i in range(8)
                                )
                                if min(e) < 0:
                                    continue
                                b = tuple(
                                    (starts[(i + 1) % 8] + (n if i == 7 else 0) + offsets[i]) % n
                                    for i in range(8)
                                )
                                q_repairs = tuple(
                                    interval_mask(b[(i + 1) % 8], e[i] + 1, n)
                                    for i in range(8)
                                )
                                assert transversal_number(q_repairs) == 8
                                propagation += 1
                else:
                    if tau_j <= 7:
                        assert tau_k >= 5
                        cases["t9_r7"] += 1
    return {"rows": rows, "cases": cases, "propagation_placements": propagation}


def main():
    occurrence_records = audit_occurrences()
    repair_record = audit_repairs()
    record = {
        "python": platform.python_version(),
        "occurrence_m_range": [2, 10],
        "occurrence_records": occurrence_records,
        "repair_m_range": [2, 5],
        "repair": repair_record,
    }
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    print(f"occurrence_instances={len(occurrence_records)}")
    print(f"active_edges_total={sum(row['active_edges'] for row in occurrence_records)}")
    print(f"canonical_copies_total={sum(row['canonical_copies'] for row in occurrence_records)}")
    print(f"repair_signatures={repair_record['rows']}")
    print(f"repair_cases={json.dumps(repair_record['cases'], sort_keys=True)}")
    print(f"propagation_placements={repair_record['propagation_placements']}")
    print(f"record_sha256={digest}")
    print("VERIFIED")


if __name__ == "__main__":
    main()
