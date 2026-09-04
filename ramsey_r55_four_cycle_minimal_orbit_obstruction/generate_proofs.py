#!/usr/bin/env python3
"""Generate certificates for four-cycle actions with minimum edge-orbit count."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter
from pathlib import Path

import pysat
from pysat.solvers import Solver


ORDER = 43
CYCLE_COUNT = 4
MINIMUM_EDGE_ORBITS = 26


def orbit_count(parts: tuple[int, ...]) -> int:
    return sum(length // 2 for length in parts) + sum(
        math.gcd(parts[i], parts[j])
        for i in range(len(parts))
        for j in range(i + 1, len(parts))
    )


def degree_feasible(parts: tuple[int, ...]) -> bool:
    reachable = {(0,) * len(parts)}
    for i in range(len(parts)):
        for j in range(i + 1, len(parts)):
            divisor = math.gcd(parts[i], parts[j])
            step_i = parts[j] // divisor
            step_j = parts[i] // divisor
            reachable = {
                tuple(
                    degrees[index]
                    + (selected * step_i if index == i else selected * step_j if index == j else 0)
                    for index in range(len(parts))
                )
                for degrees in reachable
                for selected in range(divisor + 1)
            }
    internal = [
        range(length) if length % 2 == 0 else range(0, length, 2)
        for length in parts
    ]
    return any(
        all(any(18 <= cross[i] + degree <= 24 for degree in internal[i]) for i in range(len(parts)))
        for cross in reachable
    )


def cycle_types() -> tuple[list[tuple[int, ...]], int, int]:
    partitions = [
        parts
        for parts in itertools.combinations_with_replacement(range(1, ORDER + 1), CYCLE_COUNT)
        if sum(parts) == ORDER
    ]
    minimum = min(map(orbit_count, partitions))
    minimal = [parts for parts in partitions if orbit_count(parts) == minimum]
    feasible = [parts for parts in minimal if degree_feasible(parts)]
    if (len(partitions), minimum, len(minimal), len(feasible)) != (588, 26, 131, 75):
        raise AssertionError("unexpected four-cycle census")
    return feasible, len(partitions), len(minimal) - len(feasible)


def permutation(parts: tuple[int, ...]) -> tuple[int, ...]:
    result = []
    start = 0
    for length in parts:
        result.extend(start + (offset + 1) % length for offset in range(length))
        start += length
    return tuple(result)


def edge_orbits(parts: tuple[int, ...]) -> list[list[tuple[int, int]]]:
    perm = permutation(parts)
    unused = set(itertools.combinations(range(ORDER), 2))
    orbits = []
    while unused:
        seed = min(unused)
        orbit = []
        edge = seed
        while not orbit or edge != seed:
            orbit.append(edge)
            edge = tuple(sorted((perm[edge[0]], perm[edge[1]])))
        if len(set(orbit)) != len(orbit) or not set(orbit) <= unused:
            raise AssertionError("invalid edge orbit")
        unused.difference_update(orbit)
        orbits.append(orbit)
    if len(orbits) != orbit_count(parts):
        raise AssertionError("edge-orbit formula mismatch")
    return orbits


def five_set_masks(orbits: list[list[tuple[int, int]]]) -> set[int]:
    edge_variable = {
        edge: variable for variable, orbit in enumerate(orbits) for edge in orbit
    }
    masks = set()
    count = 0
    for vertices in itertools.combinations(range(ORDER), 5):
        mask = 0
        for edge in itertools.combinations(vertices, 2):
            mask |= 1 << edge_variable[edge]
        masks.add(mask)
        count += 1
    if count != 962_598:
        raise AssertionError("five-set count mismatch")
    return masks


def clauses_from_masks(masks: set[int], variables: int) -> list[list[int]]:
    clauses = []
    for mask in sorted(masks):
        positive = [i + 1 for i in range(variables) if mask >> i & 1]
        clauses.extend((positive, [-literal for literal in positive]))
    clauses.append([1])
    return clauses


def cnf_sha256(variables: int, clauses: list[list[int]]) -> str:
    digest = hashlib.sha256()
    digest.update(f"p cnf {variables} {len(clauses)}\n".encode())
    for clause in clauses:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode())
    return digest.hexdigest()


def write_candidate(
    path: Path,
    parts: tuple[int, ...],
    orbits: list[list[tuple[int, int]]],
    model: list[int],
) -> None:
    truth = {abs(literal): literal > 0 for literal in model}
    red_edges = [
        list(edge)
        for variable, orbit in enumerate(orbits)
        if truth[variable + 1]
        for edge in orbit
    ]
    path.write_text(
        json.dumps(
            {"cycle_type": list(parts), "order": ORDER, "red_edges": red_edges},
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )


def solve(
    proof_path: Path,
    candidate_path: Path,
    parts: tuple[int, ...],
    orbits: list[list[tuple[int, int]]],
    clauses: list[list[int]],
) -> dict[str, object] | None:
    with Solver(name="glucose42", bootstrap_with=clauses, with_proof=True) as solver:
        satisfiable = solver.solve()
        if satisfiable:
            model = solver.get_model()
            if model is None:
                raise AssertionError("SAT result omitted its model")
            write_candidate(candidate_path, parts, orbits, model)
            return None
        proof = solver.get_proof()
    if proof is None:
        raise AssertionError("UNSAT result omitted its proof")
    proof_path.write_text("\n".join(proof) + "\n")
    return {
        "satisfiable": False,
        "proof_file": str(Path("proofs") / proof_path.name),
        "proof_line_count": len(proof),
        "proof_byte_count": proof_path.stat().st_size,
        "proof_sha256": hashlib.sha256(proof_path.read_bytes()).hexdigest(),
    }


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--proof-dir", type=Path, default=here / "proofs")
    parser.add_argument("--result", type=Path, default=here / "proof_manifest.json")
    parser.add_argument("--candidate", type=Path, default=here / "candidate.json")
    args = parser.parse_args()
    args.proof_dir.mkdir(parents=True, exist_ok=True)

    types, total, infeasible = cycle_types()
    cases = []
    for index, parts in enumerate(types, start=1):
        orbits = edge_orbits(parts)
        masks = five_set_masks(orbits)
        clauses = clauses_from_masks(masks, len(orbits))
        proof = solve(
            args.proof_dir / ("-".join(map(str, parts)) + ".drup"),
            args.candidate,
            parts,
            orbits,
            clauses,
        )
        if proof is None:
            print(f"TARGET_CANDIDATE cycle_type={'+'.join(map(str, parts))} file={args.candidate}")
            raise SystemExit(10)
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
            f"case={index}/75 cycle_type={'+'.join(map(str, parts))} "
            f"clauses={len(clauses)} proof_lines={proof['proof_line_count']}",
            flush=True,
        )

    manifest = {
        "format": "r55-four-cycle-minimal-orbit-obstruction-v1",
        "order": ORDER,
        "degree_window": [18, 24],
        "total_four_cycle_types": total,
        "minimum_edge_orbit_count": MINIMUM_EDGE_ORBITS,
        "minimum_orbit_types": 131,
        "degree_infeasible_minimum_orbit_types": infeasible,
        "certified_minimum_orbit_types": len(types),
        "five_set_count": 962_598,
        "solver": "PySAT Glucose 4.2",
        "python_sat_version": pysat.__version__,
        "cases": cases,
    }
    args.result.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print("PASS generated 75 minimum-orbit four-cycle UNSAT proofs", flush=True)


if __name__ == "__main__":
    main()
