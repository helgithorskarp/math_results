#!/usr/bin/env python3
"""Generate a DRUP proof for the order-21 automorphism obstruction."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

import pysat
from pysat.solvers import Solver


ORDER = 43
GROUP = tuple(sorted({pow(x, 2, ORDER) for x in range(1, ORDER)}))
VARIABLE_COUNT = 43


def edge_orbits() -> list[list[tuple[int, int]]]:
    unused = set(itertools.combinations(range(ORDER), 2))
    result = []
    while unused:
        seed = min(unused)
        orbit = {
            tuple(sorted((multiplier * seed[0] % ORDER, multiplier * seed[1] % ORDER)))
            for multiplier in GROUP
        }
        result.append(sorted(orbit))
        unused -= orbit
    result.sort(key=lambda orbit: orbit[0])
    if len(result) != VARIABLE_COUNT or Counter(map(len, result)) != Counter({21: 43}):
        raise AssertionError("unexpected edge-orbit decomposition")
    return result


def five_set_masks(orbits: list[list[tuple[int, int]]]) -> set[int]:
    edge_to_variable = {
        edge: index for index, orbit in enumerate(orbits) for edge in orbit
    }
    masks = set()
    for vertices in itertools.combinations(range(ORDER), 5):
        mask = 0
        for edge in itertools.combinations(vertices, 2):
            mask |= 1 << edge_to_variable[edge]
        masks.add(mask)
    if len(masks) != 43_655:
        raise AssertionError("unexpected distinct five-set mask count")
    return masks


def inclusion_minimal_masks(masks: set[int]) -> list[int]:
    minimal = []
    for mask in sorted(masks, key=lambda value: (value.bit_count(), value)):
        submask = (mask - 1) & mask
        while submask and submask not in masks:
            submask = (submask - 1) & mask
        if not submask:
            minimal.append(mask)
    if len(minimal) != 32_126:
        raise AssertionError("unexpected inclusion-minimal mask count")
    return minimal


def clauses_from_masks(masks: list[int]) -> list[list[int]]:
    clauses = []
    for mask in masks:
        variables = [index + 1 for index in range(VARIABLE_COUNT) if mask >> index & 1]
        clauses.append(variables)
        clauses.append([-variable for variable in variables])
    # Color complementation maps every solution to a solution, so fixing the
    # first edge orbit red is equisatisfiable.
    clauses.append([1])
    return clauses


def dimacs_sha256(clauses: list[list[int]]) -> str:
    digest = hashlib.sha256()
    digest.update(f"p cnf {VARIABLE_COUNT} {len(clauses)}\n".encode())
    for clause in clauses:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode())
    return digest.hexdigest()


def write_proof(path: Path, clauses: list[list[int]]) -> dict[str, int | str | bool]:
    with Solver(name="glucose42", bootstrap_with=clauses, with_proof=True) as solver:
        satisfiable = solver.solve()
        proof = solver.get_proof() if not satisfiable else None
    if satisfiable or proof is None:
        raise AssertionError("expected an UNSAT result with a proof trace")
    path.write_text("\n".join(proof) + "\n")
    payload: dict[str, int | str | bool] = {
        "solver": "PySAT Glucose 4.2",
        "python_sat_version": pysat.__version__,
        "satisfiable": False,
        "proof_line_count": len(proof),
        "proof_byte_count": path.stat().st_size,
        "proof_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }
    return payload


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--proof", type=Path, default=here / "obstruction.drup")
    parser.add_argument("--result", type=Path, default=here / "result.json")
    arguments = parser.parse_args()

    orbits = edge_orbits()
    masks = five_set_masks(orbits)
    minimal = inclusion_minimal_masks(masks)
    clauses = clauses_from_masks(minimal)
    solver_payload = write_proof(arguments.proof, clauses)
    result = {
        "format": "r55-order21-automorphism-obstruction-v1",
        "order": ORDER,
        "group_elements": list(GROUP),
        "vertex_orbit_sizes": [1, 21, 21],
        "edge_orbit_count": len(orbits),
        "edge_orbit_size_histogram": {"21": 43},
        "five_set_count": 962_598,
        "distinct_five_set_masks": len(masks),
        "five_set_mask_size_histogram": {
            str(key): value for key, value in sorted(Counter(x.bit_count() for x in masks).items())
        },
        "inclusion_minimal_mask_count": len(minimal),
        "minimal_mask_size_histogram": {
            str(key): value
            for key, value in sorted(Counter(x.bit_count() for x in minimal).items())
        },
        "variable_count": VARIABLE_COUNT,
        "clause_count": len(clauses),
        "color_swap_unit_clause": 1,
        "cnf_sha256": dimacs_sha256(clauses),
        **solver_payload,
    }
    arguments.result.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS generated UNSAT proof for order-21 automorphism family")
    print(
        f"variables={VARIABLE_COUNT} clauses={len(clauses)} "
        f"five_set_masks={len(masks)} minimal_masks={len(minimal)}"
    )
    print(
        f"proof_lines={result['proof_line_count']} proof_bytes={result['proof_byte_count']} "
        f"proof_sha256={result['proof_sha256']}"
    )


if __name__ == "__main__":
    main()
