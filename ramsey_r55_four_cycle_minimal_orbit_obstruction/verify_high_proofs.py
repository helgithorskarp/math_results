#!/usr/bin/env python3
"""Independently rebuild and replay all four-cycle strata from 36 upward."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from verify_next_proofs import all_partitions
from verify_proofs import (
    ORDER,
    clauses_from_masks,
    cnf_sha256,
    degree_feasible,
    orbit_count,
    reconstruct,
    replay,
)


LOWER_BOUND = 36
STRATUM_CENSUS = {
    36: (47, 39),
    38: (57, 44),
    40: (23, 22),
    42: (17, 13),
    44: (20, 17),
    46: (5, 5),
    48: (12, 12),
    50: (4, 4),
    52: (1, 1),
    54: (4, 4),
    56: (2, 2),
    60: (1, 1),
    62: (1, 0),
    66: (1, 0),
}


def cycle_types() -> list[tuple[int, ...]]:
    partitions = all_partitions()
    observed = {}
    selected = []
    for orbit in sorted({orbit_count(parts) for parts in partitions if orbit_count(parts) >= LOWER_BOUND}):
        types = [parts for parts in partitions if orbit_count(parts) == orbit]
        feasible = [parts for parts in types if degree_feasible(parts)]
        observed[orbit] = (len(types), len(feasible))
        selected.extend(feasible)
    if observed != STRATUM_CENSUS:
        raise AssertionError("high-stratum census mismatch")
    selected_set = set(selected)
    result = [parts for parts in partitions if parts in selected_set]
    if len(result) != 164:
        raise AssertionError("high-stratum feasible count mismatch")
    return result


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, default=here / "proof_manifest_36_plus.json")
    filters = parser.add_mutually_exclusive_group()
    filters.add_argument("--only-cycle-type")
    filters.add_argument("--exclude-cycle-type")
    args = parser.parse_args()
    document = json.loads(args.result.read_text())
    types = cycle_types()
    expected_top = {
        "format": "r55-four-cycle-orbits-36-plus-obstruction-v1",
        "order": ORDER,
        "degree_window": [18, 24],
        "edge_orbit_lower_bound": LOWER_BOUND,
        "high_stratum_types": 195,
        "high_stratum_degree_infeasible": 31,
        "high_stratum_certified": len(types),
        "stratum_census": {
            str(orbit): {"types": total, "certified": feasible, "degree_infeasible": total - feasible}
            for orbit, (total, feasible) in STRATUM_CENSUS.items()
        },
        "five_set_count": 962_598,
    }
    for key, value in expected_top.items():
        if document.get(key) != value:
            raise AssertionError(f"manifest mismatch at {key}")
    cases = document.get("cases")
    if not isinstance(cases, list) or len(cases) != 164:
        raise AssertionError("manifest case count mismatch")

    def requested(value: str | None) -> tuple[int, ...] | None:
        if value is None:
            return None
        try:
            parts = tuple(map(int, value.split("+")))
        except ValueError as error:
            raise ValueError("cycle type must look like 1+6+18+18") from error
        if (
            len(parts) != 4
            or any(part <= 0 for part in parts)
            or tuple(sorted(parts)) != parts
            or sum(parts) != ORDER
        ):
            raise ValueError("cycle type must be four nondecreasing positive parts summing to 43")
        return parts

    only = requested(args.only_cycle_type)
    exclude = requested(args.exclude_cycle_type)
    selected = [
        (index, parts, case)
        for index, (parts, case) in enumerate(zip(types, cases, strict=True), start=1)
        if (only is None or parts == only) and (exclude is None or parts != exclude)
    ]
    if only is not None and len(selected) != 1:
        raise ValueError("requested cycle type is not a certified high-stratum case")

    additions = deletions = proof_bytes = 0
    for index, parts, case in selected:
        variables = orbit_count(parts)
        masks, orbit_sizes = reconstruct(parts)
        clauses = clauses_from_masks(masks, variables)
        expected_case = {
            "cycle_type": list(parts),
            "variable_count": variables,
            "edge_orbit_size_histogram": {
                str(size): count for size, count in sorted(orbit_sizes.items())
            },
            "distinct_five_set_masks": len(masks),
            "five_set_mask_size_histogram": {
                str(size): count
                for size, count in sorted(Counter(mask.bit_count() for mask in masks).items())
            },
            "clause_count": len(clauses),
            "color_swap_unit_clause": 1,
            "cnf_sha256": cnf_sha256(variables, clauses),
            "satisfiable": False,
        }
        for key, value in expected_case.items():
            if case.get(key) != value:
                raise AssertionError(f"case {parts} mismatch at {key}")
        path = here / case["proof_file"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != case["proof_sha256"]:
            raise AssertionError(f"case {parts} proof hash mismatch")
        if path.stat().st_size != case["proof_byte_count"]:
            raise AssertionError(f"case {parts} proof size mismatch")
        added, deleted = replay(variables, clauses, path)
        if added + deleted != case["proof_line_count"]:
            raise AssertionError(f"case {parts} proof line count mismatch")
        additions += added
        deletions += deleted
        proof_bytes += path.stat().st_size
        print(
            f"PASS case={index}/164 cycle_type={'+'.join(map(str, parts))} "
            f"variables={variables} clauses={len(clauses)} "
            f"additions={added} deletions={deleted}",
            flush=True,
        )
    print(
        f"PASS replayed {len(selected)} high-stratum proofs additions={additions} "
        f"deletions={deletions} proof_bytes={proof_bytes}",
        flush=True,
    )


if __name__ == "__main__":
    main()
