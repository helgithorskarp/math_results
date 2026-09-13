#!/usr/bin/env python3
"""Independent exact verifier for the Albertson r=30 frontier certificate.

This implementation does not import the generator.  It uses recursive exact
QuickHull splits, falling-factorial incidence ratios, and integer-numerator
forms of all base bounds.
"""

from __future__ import annotations

import argparse
import json
from bisect import bisect_right
from fractions import Fraction
from hashlib import sha256
from math import comb
from pathlib import Path


TARGET = 9555
KNOWN_PREFIX_53 = "79e615e691c84d697b2dbc3d6fded0d9657c37d3f91f4bebc1a61097fb39f7f6"
KNOWN_DIGEST_60 = "8d15e75fbb647b6cd6899bd4466ec0ce7a0185e23a918a878bdfd3aebfb6b115"
Point = tuple[int, int]


def ceil_ratio(numerator: int, denominator: int) -> int:
    assert denominator > 0
    return -((-numerator) // denominator)


def universal_floor(n: int, m: int) -> int:
    z = n - 2
    return max(
        0,
        m - 3 * z,
        ceil_ratio(7 * m - 25 * z, 3),
        ceil_ratio(37 * m - 155 * z, 9),
        ceil_ratio(45 * m - 203 * z, 9),
    )


def local24_floor(n: int, m: int) -> int:
    return max(0, 5 * m - 495) if n == 24 else 0


def orientation(a: Point, b: Point, p: Point) -> int:
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])


def quickhull_arc(a: Point, b: Point, points: list[Point]) -> list[Point]:
    below = [p for p in points if orientation(a, b, p) < 0]
    if not below:
        return [a, b]
    pivot = min(below, key=lambda p: (orientation(a, b, p), p[0]))
    left = quickhull_arc(a, pivot, below)
    right = quickhull_arc(pivot, b, below)
    return left[:-1] + right


def lower_hull(values: list[int]) -> list[Point]:
    points = list(enumerate(values))
    return quickhull_arc(points[0], points[-1], points[1:-1])


def hull_value(hull: list[Point], numerator: int, denominator: int) -> Fraction:
    floor_x = numerator // denominator
    index = bisect_right([p[0] for p in hull], floor_x) - 1
    x0, y0 = hull[index]
    if numerator == x0 * denominator:
        return Fraction(y0)
    x1, y1 = hull[index + 1]
    left_weight = x1 * denominator - numerator
    right_weight = numerator - x0 * denominator
    return Fraction(
        y0 * left_weight + y1 * right_weight,
        (x1 - x0) * denominator,
    )


def audit_hull(values: list[int], hull: list[Point]) -> None:
    assert hull[0] == (0, values[0])
    assert hull[-1] == (len(values) - 1, values[-1])
    assert all(
        orientation(a, b, c) > 0
        for a, b, c in zip(hull, hull[1:], hull[2:])
    )
    for m, value in enumerate(values):
        assert hull_value(hull, m, 1) <= value


def sampled_floor(n: int, m: int, s: int, hull: list[Point]) -> int:
    local = hull_value(hull, m * s * (s - 1), n * (n - 1))
    ratio = Fraction(
        n * (n - 1) * (n - 2) * (n - 3),
        s * (s - 1) * (s - 2) * (s - 3),
    )
    result = ratio * local
    return ceil_ratio(result.numerator, result.denominator)


def build_tables(max_order: int):
    tables: dict[int, list[int]] = {}
    hulls: dict[int, list[Point]] = {}
    digest = sha256()
    prefixes = {}
    for n in range(4, max_order + 1):
        row = []
        for m in range(comb(n, 2) + 1):
            candidates = [universal_floor(n, m), local24_floor(n, m)]
            candidates.extend(sampled_floor(n, m, s, hulls[s]) for s in range(4, n))
            value = max(candidates)
            row.append(value)
            digest.update(f"{n}:{m}:{value}\n".encode("ascii"))
        hull = lower_hull(row)
        audit_hull(row, hull)
        tables[n] = row
        hulls[n] = hull
        prefixes[n] = digest.hexdigest()
    return tables, prefixes


def one_stage_floor(n: int, m: int) -> tuple[int, int, Fraction]:
    best = None
    for q in range(4, n + 1):
        local_constant = -(203 * (q - 2) // 9)
        numerator = (
            5 * m * comb(n - 2, q - 2)
            + local_constant * comb(n, q)
        )
        denominator = comb(n - 4, q - 4)
        raw = Fraction(numerator, denominator)
        value = ceil_ratio(raw.numerator, raw.denominator)
        candidate = (value, raw, -q)
        if best is None or candidate > best:
            best = candidate
    assert best is not None
    return best[0], -best[2], best[1]


def gks(n: int) -> int:
    return ceil_ratio(29 * n + (n - 30) * (60 - n) - 2, 2)


def join(n: int) -> int:
    p = n - 30
    return ceil_ratio(900 + 60 * p - p * p - 30 + 1, 2)


def edge_floor(n: int) -> tuple[int, dict[str, int]]:
    parts = {"minimum_degree": 15 * n}
    if 32 <= n <= 59:
        parts["gallai_kostochka_stiebitz"] = gks(n)
    if 48 <= n <= 58:
        parts["strengthened_join"] = join(n)
    return max(parts.values()), parts


def checked_orders() -> list[int]:
    result = []
    for n in range(30, 85):
        small = n <= 34
        cranston = 250 * n >= 307 * 30 and 125 * n <= 221 * 30
        if not small and not cranston:
            result.append(n)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path, nargs="?", default=Path("certificate.json"))
    args = parser.parse_args()
    cert = json.loads(args.certificate.read_text(encoding="utf-8"))

    assert cert["schema"] == "albertson-r30-two-row-frontier-v1"
    assert cert["status"] == "PASS_FRONTIER_AND_SPECIALIZED_CLOSURE"
    assert cert["r"] == 30 and cert["z_r"] == TARGET
    assert cert["reviewed_local_seed"] == "cr(24,m) >= max(0,5m-495)"
    assert cert["recursive_max_order"] == 60
    assert cert["order_dispatch"] == {
        "small_topological": [30, 34],
        "uncovered_then_checked": [[35, 36], [54, 84]],
        "cranston_intermediate": [37, 53],
        "cranston_large": [85, "infinity"],
        "cranston_constants": ["307/250", "221/125", "14059/5000"],
    }
    assert checked_orders() == [35, 36] + list(range(54, 85))
    assert 5000 * 85 >= 14059 * 30 and 5000 * 84 < 14059 * 30

    assert all(universal_floor(24, m) >= 5 * m - 495 for m in range(132))
    assert 5 * 132 - 495 == 165
    tables, prefixes = build_tables(60)
    assert prefixes[53] == KNOWN_PREFIX_53
    assert prefixes[60] == KNOWN_DIGEST_60
    assert prefixes[53] == cert["r27_prefix_digest_through_53"]
    assert prefixes[60] == cert["recursive_table_digest_through_60"]
    assert tables[53][713] == 6089

    survivors = []
    records = cert["candidate_records"]
    assert [record["n"] for record in records] == checked_orders()
    for record in records:
        n = record["n"]
        minimum, sources = edge_floor(n)
        assert minimum == record["edge_floor"]
        assert sources == record["edge_floor_sources"]
        if n <= 60:
            assert record["crossing_method"] == "recursive_convex_sampling"
            assert record["witness"] is None
            row = tables[n]
            threshold = next(m for m, value in enumerate(row) if value >= TARGET)
            assert all(value >= TARGET for value in row[threshold:])
            floor_value = row[minimum]
            threshold_value = row[threshold]
        else:
            assert record["crossing_method"] == "one_stage_integer_sampling"
            threshold = next(
                m
                for m in range(comb(n, 2) + 1)
                if one_stage_floor(n, m)[0] >= TARGET
            )
            assert all(
                one_stage_floor(n, m)[0] >= TARGET
                for m in range(threshold, comb(n, 2) + 1)
            )
            floor_value, floor_q, floor_raw = one_stage_floor(n, minimum)
            threshold_value, threshold_q, threshold_raw = one_stage_floor(n, threshold)
            assert {
                "floor_q": floor_q,
                "floor_raw": str(floor_raw),
                "threshold_q": threshold_q,
                "threshold_raw": str(threshold_raw),
            } == record["witness"]
        assert threshold == record["crossing_closure_threshold"]
        assert floor_value == record["crossing_floor_at_edge_floor"]
        assert threshold_value == record["crossing_bound_at_threshold"]
        local_survivors = list(range(minimum, threshold))
        assert local_survivors == record["crossing_survivor_edges"]
        survivors.extend([n, m] for m in local_survivors)

    assert survivors == [[59, 885], [59, 886], [59, 887]]
    assert cert["crossing_only_survivors"] == survivors
    assert tables[59][885:889] == [9454, 9490, 9525, 9561]

    # Exact arithmetic behind the regular-row and complement reductions.
    assert 2 * 885 == 59 * 30
    radicand = 48 * 59 + 73
    assert 53 * 53 < radicand < 54 * 54
    assert cert["rabern_regular_exclusion"]["row"] == [59, 885]
    assert cert["rabern_regular_exclusion"]["radicand"] == radicand
    assert cert["rabern_regular_exclusion"]["sqrt_bracket"] == [53, 54]
    assert cert["rabern_regular_exclusion"]["ceiling_term"] == 18
    assert cert["disconnected_complement_edge_floor_at_59"] == 30 * 30 - 1
    assert cert["final_frontier"] == [[59, 886], [59, 887]]
    assert [
        (entry["g_edges"], entry["h_edges"], entry["total_28_degree_deficit"])
        for entry in cert["complement_arithmetic"]
    ] == [(886, 825, 2), (887, 824, 4)]
    assert [entry["deficit_partitions"] for entry in cert["complement_arithmetic"]] == [
        [[2], [1, 1]],
        [[4], [3, 1], [2, 2], [2, 1, 1], [1, 1, 1, 1]],
    ]

    # Independently exhaust the numerical inequalities in the specialized
    # D=28 Tutte--Hall lemma.  The graph-theoretic bridge is in README.md.
    structural = []
    for a in (2, 4):
        possible_s = []
        for s in range(3, 31):
            low = max(1, 29 - a - s)
            low += (low + 1) % 2  # least odd integer at least low
            if (s - 1) * low > 59 - s:
                continue
            outside_cap_twice = (61 - 2 * s) * (60 - 2 * s)
            inside_cap_twice = outside_cap_twice + 28 * (2 * s - 59) + a
            if inside_cap_twice >= 0:
                possible_s.append(s)
        assert possible_s == [3, 30]
        color_cap = 59 - 2 * (25 - a)
        sum_w_cap = 28 + a
        edge_w_cap = 15 + a // 2
        max_h = a + 2
        costs = [[h, h * (28 - h)] for h in range(2, max_h + 1)]
        assert 5 * (28 - a) - 118 > 0
        assert color_cap < 30
        assert 56 - edge_w_cap > 29
        assert all(cost > sum_w_cap for _, cost in costs)
        assert 27 > a and 27 > edge_w_cap
        structural.append(
            {
                "total_deficit": a,
                "aes_five_delta_minus_two_n": 5 * (28 - a) - 118,
                "barrier_sizes_after_exact_filters": possible_s,
                "small_barrier_coloring_cap": color_cap,
                "total_weight_cap": sum_w_cap,
                "edge_endpoint_weight_cap": edge_w_cap,
                "max_hall_h": max_h,
                "hall_costs": costs,
            }
        )
    assert structural == cert["specialized_structural_closure"]
    assert cert["unresolved_after_structural_closure"] == []

    print("PASS independent QuickHull verification")
    print("crossing-only survivors: (59,885), (59,886), (59,887)")
    print("Rabern excludes the 30-regular row (59,885)")
    print("final frontier: (59,886), (59,887); complement connected")
    print("specialized D=28 Tutte-Hall closure: both rows excluded")
    print("verdict: r=30 conclusion independently supported")
    print(f"recursive_table_sha256={prefixes[60]}")


if __name__ == "__main__":
    main()
