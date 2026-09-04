#!/usr/bin/env python3
"""Independently rebuild and replay four-cycle strata 32 and 34."""

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


STRATA = (32, 34)


def cycle_types() -> list[tuple[int, ...]]:
    partitions = all_partitions()
    counts = {
        orbit: [parts for parts in partitions if orbit_count(parts) == orbit]
        for orbit in STRATA
    }
    feasible = {
        orbit: [parts for parts in counts[orbit] if degree_feasible(parts)]
        for orbit in STRATA
    }
    if tuple((len(counts[o]), len(feasible[o])) for o in STRATA) != ((120, 74), (27, 21)):
        raise AssertionError("stratum census mismatch")
    selected = set(feasible[32] + feasible[34])
    return [parts for parts in partitions if parts in selected]


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, default=here / "proof_manifest_32_34.json")
    args = parser.parse_args()
    document = json.loads(args.result.read_text())
    types = cycle_types()
    expected_top = {
        "format": "r55-four-cycle-orbits-32-34-obstruction-v1",
        "order": ORDER,
        "degree_window": [18, 24],
        "edge_orbit_counts": list(STRATA),
        "orbit_32_types": 120,
        "orbit_32_degree_infeasible": 46,
        "orbit_32_certified": 74,
        "orbit_34_types": 27,
        "orbit_34_degree_infeasible": 6,
        "orbit_34_certified": 21,
        "five_set_count": 962_598,
    }
    for key, value in expected_top.items():
        if document.get(key) != value:
            raise AssertionError(f"manifest mismatch at {key}")
    cases = document.get("cases")
    if not isinstance(cases, list) or len(cases) != 95:
        raise AssertionError("manifest case count mismatch")

    additions = deletions = proof_bytes = 0
    for index, (parts, case) in enumerate(zip(types, cases, strict=True), start=1):
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
            f"PASS case={index}/95 cycle_type={'+'.join(map(str, parts))} "
            f"variables={variables} clauses={len(clauses)} "
            f"additions={added} deletions={deleted}",
            flush=True,
        )
    print(
        f"PASS replayed 95 mid-stratum proofs additions={additions} "
        f"deletions={deletions} proof_bytes={proof_bytes}",
        flush=True,
    )


if __name__ == "__main__":
    main()
