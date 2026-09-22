#!/usr/bin/env python3
"""Exact audit of the low-triple collision lower-bound table."""

from __future__ import annotations

import itertools
import json
import math


def minimum_collision(pair_count: int, intersection_sum: int, maximum: int,
                      require_maximum: bool) -> tuple[int, list[int]]:
    """Minimize sum C(s,3) over all integer intersection histograms."""
    infinity = 10**9
    states: dict[tuple[int, int, bool], tuple[int, list[int]]] = {
        (0, 0, False): (0, [])
    }
    for value in range(maximum + 1):
        following: dict[tuple[int, int, bool], tuple[int, list[int]]] = {}
        for (used, total, saw), (cost, histogram) in states.items():
            for count in range(pair_count - used + 1):
                new_total = total + value * count
                if new_total > intersection_sum:
                    break
                key = (
                    used + count,
                    new_total,
                    saw or (value == maximum and count > 0),
                )
                candidate = (
                    cost + count * math.comb(value, 3),
                    histogram + [count],
                )
                if candidate[0] < following.get(key, (infinity, []))[0]:
                    following[key] = candidate
        states = following
    choices = [
        value
        for (used, total, saw), value in states.items()
        if used == pair_count
        and total == intersection_sum
        and (saw or not require_maximum)
    ]
    assert choices
    return min(choices, key=lambda item: item[0])


def record(pair_count: int, intersection_sum: int, maximum: int,
           require_maximum: bool = True) -> dict[str, object]:
    cost, histogram = minimum_collision(
        pair_count, intersection_sum, maximum, require_maximum
    )
    assert sum(histogram) == pair_count
    assert sum(value * count for value, count in enumerate(histogram)) == intersection_sum
    assert sum(math.comb(value, 3) * count
               for value, count in enumerate(histogram)) == cost
    if require_maximum:
        assert histogram[maximum] > 0
    return {"minimum": cost, "histogram_s0_up": histogram}


def main() -> None:
    inequality = [
        {
            "s": s,
            "binomial_s_3": math.comb(s, 3),
            "surplus_over_s_minus_2": math.comb(s, 3) - (s - 2),
        }
        for s in range(13)
    ]
    assert all(item["surplus_over_s_minus_2"] >= 0 for item in inequality)

    a = {str(k): record(66, 120, k) for k in (2, 3, 4)}
    b = {str(l): record(28, 72, l) for l in (3, 4, 5)}
    cross = record(96, 240, 5, require_maximum=False)
    assert [a[str(k)]["minimum"] for k in (2, 3, 4)] == [0, 1, 4]
    assert [b[str(l)]["minimum"] for l in (3, 4, 5)] == [16, 18, 23]
    assert cross["minimum"] == 48

    table = {
        str(k): {
            str(l): a[str(k)]["minimum"] + b[str(l)]["minimum"]
            + cross["minimum"] - 60
            for l in (3, 4, 5)
        }
        for k in (2, 3, 4)
    }
    assert table == {
        "2": {"3": 4, "4": 6, "5": 11},
        "3": {"3": 5, "4": 7, "5": 12},
        "4": {"3": 8, "4": 10, "5": 15},
    }

    result = {
        "status": "VERIFIED_LOW_TRIPLE_COLLISION_TABLE",
        "forced_ranges": {
            "a_maximum_intersection": [2, 3, 4],
            "b_maximum_intersection": [3, 4, 5],
        },
        "a_pair_intersections": a,
        "b_pair_intersections": b,
        "cross_pair_intersections": cross,
        "higher_multiplicity_excess_table": table,
        "incidence_totals": {
            "low_triples": math.comb(12, 3),
            "a_triple_incidences": 12 * math.comb(5, 3),
            "b_triple_incidences": 8 * math.comb(6, 3),
            "duplicate_incidences": 12 * math.comb(5, 3)
            + 8 * math.comb(6, 3) - math.comb(12, 3),
            "a_pair_intersection_sum": 12 * math.comb(5, 2),
            "b_pair_intersection_sum": 12 * math.comb(4, 2),
            "cross_intersection_sum": 12 * 5 * 4,
        },
        "integer_inequality_audit": inequality,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
