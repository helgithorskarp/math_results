#!/usr/bin/env python3
"""Generate proofs for feasible four-cycle actions with 28 or 30 edge orbits."""

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


STRATA = (28, 30)


def cycle_types() -> list[tuple[int, ...]]:
    result = [
        parts
        for parts in itertools.combinations_with_replacement(range(1, ORDER + 1), 4)
        if sum(parts) == ORDER and orbit_count(parts) in STRATA and degree_feasible(parts)
    ]
    if len(result) != 69:
        raise AssertionError("expected 69 feasible types in strata 28 and 30")
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
        "proof_file": str(Path("proofs_28_30") / path.name),
        "proof_line_count": len(proof),
        "proof_byte_count": path.stat().st_size,
        "proof_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--proof-dir", type=Path, default=here / "proofs_28_30")
    parser.add_argument("--result", type=Path, default=here / "proof_manifest_28_30.json")
    args = parser.parse_args()
    args.proof_dir.mkdir(parents=True, exist_ok=True)

    cases = []
    for index, parts in enumerate(cycle_types(), start=1):
        orbits = edge_orbits(parts)
        masks = five_set_masks(orbits)
        clauses = clauses_from_masks(masks, len(orbits))
        proof = prove(args.proof_dir / ("-".join(map(str, parts)) + ".drup"), clauses)
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
            f"case={index}/69 cycle_type={'+'.join(map(str, parts))} "
            f"variables={len(orbits)} clauses={len(clauses)} "
            f"proof_lines={proof['proof_line_count']}",
            flush=True,
        )

    manifest = {
        "format": "r55-four-cycle-orbits-28-30-obstruction-v1",
        "order": ORDER,
        "degree_window": [18, 24],
        "edge_orbit_counts": list(STRATA),
        "orbit_28_types": 33,
        "orbit_28_degree_infeasible": 11,
        "orbit_28_certified": 22,
        "orbit_30_types": 82,
        "orbit_30_degree_infeasible": 35,
        "orbit_30_certified": 47,
        "five_set_count": 962_598,
        "solver": "PySAT Glucose 4.2",
        "python_sat_version": pysat.__version__,
        "cases": cases,
    }
    args.result.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print("PASS generated 69 UNSAT proofs for strata 28 and 30", flush=True)


if __name__ == "__main__":
    main()
