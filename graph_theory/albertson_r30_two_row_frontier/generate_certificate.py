#!/usr/bin/env python3
"""Generate the exact Albertson r=30 numerical-frontier certificate.

The recursive crossing tables use the greatest convex minorant of previously
certified integer tables.  This implementation constructs that minorant in
two ways (a monotone chain and pooled adjacent slopes) and requires agreement.
"""

from __future__ import annotations

import argparse
import json
from bisect import bisect_right
from fractions import Fraction
from hashlib import sha256
from math import comb
from pathlib import Path


R = 30
TARGET = 9555
MAX_RECURSIVE_ORDER = 60
R27_PREFIX_DIGEST = (
    "79e615e691c84d697b2dbc3d6fded0d9657c37d3f91f4bebc1a61097fb39f7f6"
)
EXPECTED_FULL_DIGEST = (
    "8d15e75fbb647b6cd6899bd4466ec0ce7a0185e23a918a878bdfd3aebfb6b115"
)


def ceil_fraction(value: Fraction) -> int:
    return -((-value.numerator) // value.denominator)


def hill_number(r: int) -> int:
    return (
        (r // 2)
        * ((r - 1) // 2)
        * ((r - 2) // 2)
        * ((r - 3) // 2)
        // 4
    )


LINEAR_BOUNDS = (
    (Fraction(1), Fraction(3)),
    (Fraction(7, 3), Fraction(25, 3)),
    (Fraction(37, 9), Fraction(155, 9)),
    (Fraction(5), Fraction(203, 9)),
)


def base_crossing_floor(n: int, m: int) -> int:
    return max(
        [0]
        + [
            ceil_fraction(slope * m - intercept * (n - 2))
            for slope, intercept in LINEAR_BOUNDS
        ]
    )


def reviewed_order24_seed(n: int, m: int) -> int:
    """Reviewed consequence of cr(24,132)>=165 and 4-planar deletion."""
    return max(0, 5 * m - 495) if n == 24 else 0


Point = tuple[int, int]


def monotone_chain_hull(values: list[int]) -> list[Point]:
    hull: list[Point] = []
    for point in enumerate(values):
        while len(hull) >= 2:
            x0, y0 = hull[-2]
            x1, y1 = hull[-1]
            x2, y2 = point
            left = Fraction(y1 - y0, x1 - x0)
            right = Fraction(y2 - y1, x2 - x1)
            if left >= right:
                hull.pop()
            else:
                break
        hull.append(point)
    return hull


def pooled_slope_hull(values: list[int]) -> list[Point]:
    blocks: list[list[int]] = []
    for left, right in zip(values, values[1:]):
        blocks.append([1, right - left])
        while len(blocks) >= 2:
            run0, rise0 = blocks[-2]
            run1, rise1 = blocks[-1]
            if Fraction(rise0, run0) < Fraction(rise1, run1):
                break
            blocks[-2:] = [[run0 + run1, rise0 + rise1]]
    hull = [(0, values[0])]
    x, y = hull[0]
    for run, rise in blocks:
        x += run
        y += rise
        hull.append((x, y))
    return hull


def hull_value(hull: list[Point], x: Fraction) -> Fraction:
    xs = [point[0] for point in hull]
    index = bisect_right(xs, x) - 1
    if index == len(hull) - 1 or x == hull[index][0]:
        return Fraction(hull[index][1])
    x0, y0 = hull[index]
    x1, y1 = hull[index + 1]
    return y0 + (x - x0) * Fraction(y1 - y0, x1 - x0)


def audit_hull(values: list[int], hull: list[Point]) -> None:
    assert hull[0] == (0, values[0])
    assert hull[-1] == (len(values) - 1, values[-1])
    slopes = [
        Fraction(y1 - y0, x1 - x0)
        for (x0, y0), (x1, y1) in zip(hull, hull[1:])
    ]
    assert all(a < b for a, b in zip(slopes, slopes[1:]))
    for m, value in enumerate(values):
        assert hull_value(hull, Fraction(m)) <= value


def sampled_floor(n: int, m: int, s: int, hull: list[Point]) -> int:
    mean_edges = Fraction(m * s * (s - 1), n * (n - 1))
    local_sum = comb(n, s) * hull_value(hull, mean_edges)
    crossing_multiplicity = comb(n - 4, s - 4)
    return ceil_fraction(local_sum / crossing_multiplicity)


def recursive_tables(max_order: int):
    tables: dict[int, list[int]] = {}
    hulls: dict[int, list[Point]] = {}
    digest = sha256()
    prefix_digests: dict[int, str] = {}
    for n in range(4, max_order + 1):
        row = []
        for m in range(comb(n, 2) + 1):
            value = max(base_crossing_floor(n, m), reviewed_order24_seed(n, m))
            for s in range(4, n):
                value = max(value, sampled_floor(n, m, s, hulls[s]))
            row.append(value)
            digest.update(f"{n}:{m}:{value}\n".encode("ascii"))
        hull_a = monotone_chain_hull(row)
        hull_b = pooled_slope_hull(row)
        assert hull_a == hull_b
        audit_hull(row, hull_a)
        tables[n] = row
        hulls[n] = hull_a
        prefix_digests[n] = digest.hexdigest()
    return tables, prefix_digests


def integral_sample_bound(n: int, m: int, q: int) -> Fraction:
    """One-stage rounded B-K sample bound, before its final ceiling."""
    local_constant = -(203 * (q - 2) // 9)
    return (
        Fraction(5 * m * (n - 2) * (n - 3), (q - 2) * (q - 3))
        + Fraction(
            local_constant * n * (n - 1) * (n - 2) * (n - 3),
            q * (q - 1) * (q - 2) * (q - 3),
        )
    )


def best_integral_sample(n: int, m: int) -> tuple[int, int, Fraction]:
    raw, negative_q = max(
        (integral_sample_bound(n, m, q), -q) for q in range(4, n + 1)
    )
    return ceil_fraction(raw), -negative_q, raw


def gks_floor(r: int, n: int) -> int:
    assert r + 2 <= n <= 2 * r - 1
    numerator = (r - 1) * n + (n - r) * (2 * r - n) - 2
    return ceil_fraction(Fraction(numerator, 2))


def join_floor(r: int, n: int) -> int:
    p = n - r
    assert r - 12 <= p <= r - 2
    numerator = r * r + 2 * p * r - p * p - r + 1
    return ceil_fraction(Fraction(numerator, 2))


def edge_floor(n: int) -> tuple[int, dict[str, int]]:
    sources = {"minimum_degree": 15 * n}
    if R + 2 <= n <= 2 * R - 1:
        sources["gallai_kostochka_stiebitz"] = gks_floor(R, n)
    if n <= 2 * R - 2 and R - 12 <= n - R <= R - 2:
        sources["strengthened_join"] = join_floor(R, n)
    return max(sources.values()), sources


def candidate_orders() -> list[int]:
    answer = []
    for n in range(R, 85):
        small = n <= R + 4
        intermediate = 250 * n >= 307 * R and 125 * n <= 221 * R
        if not small and not intermediate:
            answer.append(n)
    return answer


def integer_partitions(total: int, largest: int | None = None):
    if total == 0:
        yield []
        return
    if largest is None or largest > total:
        largest = total
    for part in range(largest, 0, -1):
        for rest in integer_partitions(total - part, part):
            yield [part] + rest


def specialized_structural_arithmetic() -> list[dict]:
    """Finite inequalities in the D=28, A in {2,4} Tutte--Hall closure."""
    d = 28
    order = 59
    records = []
    for deficit in (2, 4):
        barrier_sizes = []
        for s in range(3, 31):
            least_component = max(1, d - deficit - s + 1)
            least_odd_component = (
                least_component
                if least_component % 2 == 1
                else least_component + 1
            )
            if (s - 1) * least_odd_component > order - s:
                continue
            largest_component = order - 2 * s + 2
            twice_outside_edge_cap = largest_component * (largest_component - 1)
            twice_inside_edge_cap = (
                twice_outside_edge_cap + d * (2 * s - order) + deficit
            )
            if twice_inside_edge_cap < 0:
                continue
            barrier_sizes.append(s)
        assert barrier_sizes == [3, 30]

        small_barrier_coloring_cap = 59 - 2 * (28 - deficit - 3)
        total_weight_cap = d + deficit
        edge_endpoint_weight_cap = (d + deficit) // 2 + 1
        max_hall_h = deficit + 2
        hall_costs = [[h, h * (d - h)] for h in range(2, max_hall_h + 1)]
        assert small_barrier_coloring_cap < 30
        assert 5 * (d - deficit) > 2 * order
        assert 2 * d - edge_endpoint_weight_cap > 29
        assert min(cost for _, cost in hall_costs) > total_weight_cap
        assert d - 1 > max(deficit, edge_endpoint_weight_cap)
        records.append(
            {
                "total_deficit": deficit,
                "aes_five_delta_minus_two_n": 5 * (d - deficit) - 2 * order,
                "barrier_sizes_after_exact_filters": barrier_sizes,
                "small_barrier_coloring_cap": small_barrier_coloring_cap,
                "total_weight_cap": total_weight_cap,
                "edge_endpoint_weight_cap": edge_endpoint_weight_cap,
                "max_hall_h": max_hall_h,
                "hall_costs": hall_costs,
            }
        )
    return records


def make_certificate() -> dict:
    assert hill_number(R) == TARGET
    assert candidate_orders() == [35, 36] + list(range(54, 85))

    # The reviewed local theorem supplies the whole order-24 seed line.
    assert all(base_crossing_floor(24, m) >= 5 * m - 495 for m in range(132))
    assert 165 == 5 * 132 - 495

    tables, prefix_digests = recursive_tables(MAX_RECURSIVE_ORDER)
    assert prefix_digests[53] == R27_PREFIX_DIGEST
    assert prefix_digests[60] == EXPECTED_FULL_DIGEST
    assert tables[53][713] == 6089

    records = []
    crossing_survivors = []
    for n in candidate_orders():
        minimum, sources = edge_floor(n)
        if n <= MAX_RECURSIVE_ORDER:
            row = tables[n]
            threshold = next(m for m, value in enumerate(row) if value >= TARGET)
            assert all(value >= TARGET for value in row[threshold:])
            floor_bound = row[minimum]
            threshold_bound = row[threshold]
            method = "recursive_convex_sampling"
            witness = None
        else:
            threshold = next(
                m
                for m in range(comb(n, 2) + 1)
                if best_integral_sample(n, m)[0] >= TARGET
            )
            assert all(
                best_integral_sample(n, m)[0] >= TARGET
                for m in range(threshold, comb(n, 2) + 1)
            )
            floor_bound, q, raw = best_integral_sample(n, minimum)
            threshold_bound, threshold_q, threshold_raw = best_integral_sample(
                n, threshold
            )
            method = "one_stage_integer_sampling"
            witness = {
                "floor_q": q,
                "floor_raw": str(raw),
                "threshold_q": threshold_q,
                "threshold_raw": str(threshold_raw),
            }
        survivors = list(range(minimum, threshold))
        crossing_survivors.extend([n, m] for m in survivors)
        records.append(
            {
                "n": n,
                "edge_floor": minimum,
                "edge_floor_sources": sources,
                "crossing_method": method,
                "crossing_floor_at_edge_floor": floor_bound,
                "crossing_closure_threshold": threshold,
                "crossing_bound_at_threshold": threshold_bound,
                "crossing_survivor_edges": survivors,
                "witness": witness,
            }
        )

    assert crossing_survivors == [[59, m] for m in (885, 886, 887)]

    # At m=885 the degree floor is tight, so G is 30-regular.  Rabern's
    # inequality then forces a proper K_30 in a 59-vertex 30-critical graph.
    rabern_radicand = 48 * 59 + 73
    assert 53 * 53 < rabern_radicand < 54 * 54
    assert tables[59][888] >= TARGET and tables[59][887] < TARGET
    final_rows = [[59, 886], [59, 887]]

    complement_data = []
    for _, m in final_rows:
        h_edges = comb(59, 2) - m
        deficit = 59 * 28 - 2 * h_edges
        complement_data.append(
            {
                "g_edges": m,
                "h_edges": h_edges,
                "max_h_degree": 28,
                "total_28_degree_deficit": deficit,
                "deficit_partitions": list(integer_partitions(deficit)),
            }
        )
    assert [row["total_28_degree_deficit"] for row in complement_data] == [2, 4]

    return {
        "schema": "albertson-r30-two-row-frontier-v1",
        "claim_scope": (
            "Exact arithmetic reduction, conditional only on the imported "
            "graph-theoretic and crossing-number theorems listed in README.md."
        ),
        "r": R,
        "z_r": TARGET,
        "order_dispatch": {
            "small_topological": [30, 34],
            "uncovered_then_checked": [[35, 36], [54, 84]],
            "cranston_intermediate": [37, 53],
            "cranston_large": [85, "infinity"],
            "cranston_constants": ["307/250", "221/125", "14059/5000"],
        },
        "reviewed_local_seed": "cr(24,m) >= max(0,5m-495)",
        "recursive_max_order": MAX_RECURSIVE_ORDER,
        "r27_prefix_digest_through_53": prefix_digests[53],
        "recursive_table_digest_through_60": prefix_digests[60],
        "candidate_records": records,
        "crossing_only_survivors": crossing_survivors,
        "rabern_regular_exclusion": {
            "row": [59, 885],
            "radicand": rabern_radicand,
            "sqrt_bracket": [53, 54],
            "ceiling_term": 18,
        },
        "final_frontier": final_rows,
        "disconnected_complement_edge_floor_at_59": 899,
        "complement_arithmetic": complement_data,
        "specialized_structural_closure": specialized_structural_arithmetic(),
        "unresolved_after_structural_closure": [],
        "status": "PASS_FRONTIER_AND_SPECIALIZED_CLOSURE",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    certificate = make_certificate()
    encoded = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    print(
        "PASS Albertson r=30 exact frontier: "
        "(n,m) in {(59,886),(59,887)}"
    )
    print(
        "recursive_table_sha256="
        + certificate["recursive_table_digest_through_60"]
    )


if __name__ == "__main__":
    main()
