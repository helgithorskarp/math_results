#!/usr/bin/env python3
"""Generate proofs for all feasible four-cycle actions with at least 36 edge orbits."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

import pysat
from pysat.solvers import Solver

from generate_proofs import (
    ORDER,
    clauses_from_masks,
    cnf_sha256,
    degree_feasible,
    edge_orbits,
    five_set_masks,
    orbit_count,
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
    result = [
        parts
        for parts in itertools.combinations_with_replacement(range(1, ORDER + 1), 4)
        if sum(parts) == ORDER and orbit_count(parts) >= LOWER_BOUND and degree_feasible(parts)
    ]
    if len(result) != 164:
        raise AssertionError("expected 164 feasible high-stratum types")
    return result


def prove(path: Path, clauses: list[list[int]]) -> dict[str, object]:
    with Solver(name="glucose42", bootstrap_with=clauses, with_proof=True) as solver:
        satisfiable = solver.solve()
        proof = solver.get_proof() if not satisfiable else None
    if satisfiable or proof is None:
        raise AssertionError("expected UNSAT with proof")
    path.write_text("\n".join(proof) + "\n")
    return {
        "satisfiable": False,
        "proof_file": str(Path("proofs_36_plus") / path.name),
        "proof_line_count": len(proof),
        "proof_byte_count": path.stat().st_size,
        "proof_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def existing_proof(path: Path) -> dict[str, object]:
    payload = path.read_bytes()
    if not payload.endswith(b"\n") or b"\n\n" in payload:
        raise AssertionError(f"malformed existing proof: {path}")
    return {
        "satisfiable": False,
        "proof_file": str(Path("proofs_36_plus") / path.name),
        "proof_line_count": payload.count(b"\n"),
        "proof_byte_count": len(payload),
        "proof_sha256": hashlib.sha256(payload).hexdigest(),
    }


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--proof-dir", type=Path, default=here / "proofs_36_plus")
    parser.add_argument("--result", type=Path, default=here / "proof_manifest_36_plus.json")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    args.proof_dir.mkdir(parents=True, exist_ok=True)

    cases = []
    for index, parts in enumerate(cycle_types(), start=1):
        orbits = edge_orbits(parts)
        masks = five_set_masks(orbits)
        clauses = clauses_from_masks(masks, len(orbits))
        proof_path = args.proof_dir / ("-".join(map(str, parts)) + ".drup")
        reused = args.resume and proof_path.exists()
        proof = existing_proof(proof_path) if reused else prove(proof_path, clauses)
        cases.append(
            {
                "cycle_type": list(parts),
                "variable_count": len(orbits),
                "edge_orbit_size_histogram": {
                    str(size): count
                    for size, count in sorted(Counter(map(len, orbits)).items())
                },
                "distinct_five_set_masks": len(masks),
                "five_set_mask_size_histogram": {
                    str(size): count
                    for size, count in sorted(Counter(mask.bit_count() for mask in masks).items())
                },
                "clause_count": len(clauses),
                "color_swap_unit_clause": 1,
                "cnf_sha256": cnf_sha256(len(orbits), clauses),
                **proof,
            }
        )
        print(
            f"case={index}/164 cycle_type={'+'.join(map(str, parts))} "
            f"variables={len(orbits)} clauses={len(clauses)} "
            f"proof_lines={proof['proof_line_count']} proof_bytes={proof['proof_byte_count']} "
            f"source={'existing' if reused else 'generated'}",
            flush=True,
        )

    manifest = {
        "format": "r55-four-cycle-orbits-36-plus-obstruction-v1",
        "order": ORDER,
        "degree_window": [18, 24],
        "edge_orbit_lower_bound": LOWER_BOUND,
        "high_stratum_types": 195,
        "high_stratum_degree_infeasible": 31,
        "high_stratum_certified": len(cases),
        "stratum_census": {
            str(orbit): {"types": total, "certified": feasible, "degree_infeasible": total - feasible}
            for orbit, (total, feasible) in STRATUM_CENSUS.items()
        },
        "five_set_count": 962_598,
        "solver": "PySAT Glucose 4.2",
        "python_sat_version": pysat.__version__,
        "cases": cases,
    }
    args.result.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print("PASS generated 164 high-stratum UNSAT proofs", flush=True)


if __name__ == "__main__":
    main()
