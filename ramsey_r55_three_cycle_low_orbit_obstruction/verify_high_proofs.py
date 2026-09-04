#!/usr/bin/env python3
"""Independently reconstruct and replay the higher-orbit proof family."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

from verify_proofs import (
    ORDER,
    ORBIT_CAP,
    clauses_from_masks,
    cnf_sha256,
    degree_feasible,
    reconstruct,
    replay,
    variable_count,
)


def high_types() -> list[tuple[int, int, int]]:
    result = []
    for first in range(1, ORDER // 3 + 1):
        for second in range(first, (ORDER - first) // 2 + 1):
            parts = (first, second, ORDER - first - second)
            if degree_feasible(parts) and variable_count(parts) > ORBIT_CAP:
                result.append(parts)
    if len(result) != 49:
        raise AssertionError("expected 49 degree-feasible high-orbit types")
    return result


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, default=here / "high_proof_manifest.json")
    args = parser.parse_args()
    document = json.loads(args.result.read_text())
    types = high_types()
    expected_top = {
        "format": "r55-three-cycle-high-orbit-obstruction-v1",
        "order": ORDER,
        "degree_window": [18, 24],
        "edge_orbit_lower_bound": ORBIT_CAP + 1,
        "feasible_high_orbit_types": len(types),
        "five_set_count": 962_598,
    }
    for key, value in expected_top.items():
        if document.get(key) != value:
            raise AssertionError(f"manifest mismatch at {key}")
    cases = document.get("cases")
    if not isinstance(cases, list) or len(cases) != len(types):
        raise AssertionError("manifest case count mismatch")

    additions = deletions = proof_bytes = 0
    for index, (parts, case) in enumerate(zip(types, cases, strict=True), start=1):
        representatives, masks, orbit_sizes = reconstruct(parts)
        variables = len(representatives)
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
            f"PASS case={index}/49 cycle_type={'+'.join(map(str, parts))} "
            f"variables={variables} clauses={len(clauses)} "
            f"additions={added} deletions={deleted}",
            flush=True,
        )
    print(
        f"PASS replayed 49 high-orbit proofs additions={additions} "
        f"deletions={deletions} proof_bytes={proof_bytes}",
        flush=True,
    )


if __name__ == "__main__":
    main()
