#!/usr/bin/env python3
"""Verify that power constraints leave exactly six order-15 cycle types."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from generate_formula import CASES, ORDER


def build_result() -> dict[str, object]:
    surviving = []
    for cycles15 in range(ORDER // 15 + 1):
        for cycles5 in range(ORDER // 5 + 1):
            for cycles3 in range(ORDER // 3 + 1):
                fixed = ORDER - 15 * cycles15 - 5 * cycles5 - 3 * cycles3
                if fixed < 0:
                    continue
                cycle_lengths = (
                    [15] * cycles15 + [5] * cycles5 + [3] * cycles3 + [1] * fixed
                )
                permutation_order = math.lcm(*cycle_lengths)
                if permutation_order != 15:
                    continue
                fifth_power_cycles = 3 * cycles15 + cycles5
                third_power_cycles = 5 * cycles15 + cycles3
                if fifth_power_cycles not in (7, 8) or third_power_cycles < 7:
                    continue
                surviving.append((cycles15, cycles5, cycles3, fixed))
    if tuple(surviving) != CASES:
        raise AssertionError((surviving, CASES))
    return {
        "cycle_count_order": [15, 5, 3, 1],
        "format": "r55-order15-power-filter-v1",
        "order": ORDER,
        "power_constraints": {
            "cube_order5_cycle_counts": [7, 8],
            "fifth_power_order3_minimum_cycles": 7,
        },
        "surviving_types": [
            {
                "cycle_counts": list(case),
                "cube_cycles_5": 3 * case[0] + case[1],
                "fifth_power_cycles_3": 5 * case[0] + case[2],
            }
            for case in CASES
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    result = build_result()
    args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS surviving_order15_types=6")


if __name__ == "__main__":
    main()
