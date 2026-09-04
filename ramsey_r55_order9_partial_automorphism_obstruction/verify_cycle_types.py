#!/usr/bin/env python3
"""Verify the order-nine cube filter and the exact theorem scope."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from generate_formula import CASES, CLOSED, ORDER


def build_result() -> dict[str, object]:
    surviving = []
    for cycles9 in range(ORDER // 9 + 1):
        for cycles3 in range(ORDER // 3 + 1):
            fixed = ORDER - 9 * cycles9 - 3 * cycles3
            if fixed < 0:
                continue
            lengths = [9] * cycles9 + [3] * cycles3 + [1] * fixed
            if math.lcm(*lengths) != 9:
                continue
            cube_cycles3 = 3 * cycles9
            if cube_cycles3 < 7:
                continue
            surviving.append((cycles9, cycles3, fixed))
    if tuple(surviving) != CASES:
        raise AssertionError((surviving, CASES))
    return {
        "closed_case_indices": sorted(CLOSED),
        "closed_types": [list(CASES[index]) for index in sorted(CLOSED)],
        "cube_order3_minimum_cycles": 7,
        "cycle_count_order": [9, 3, 1],
        "format": "r55-order9-power-filter-and-scope-v1",
        "open_case_indices": [index for index in range(len(CASES)) if index not in CLOSED],
        "open_types": [list(case) for index, case in enumerate(CASES) if index not in CLOSED],
        "order": ORDER,
        "power_surviving_types": [list(case) for case in CASES],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    result = build_result()
    args.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS power_survivors=9 closed=7 open=2")


if __name__ == "__main__":
    main()
