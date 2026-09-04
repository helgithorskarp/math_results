#!/usr/bin/env python3
"""Generate DRUP certificates for the low-orbit three-cycle obstruction."""

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
ORBIT_CAP = 25


def internal_degrees(length: int) -> range:
    return range(0, length, 1 if length % 2 == 0 else 2)


def degree_feasible(parts: tuple[int, int, int]) -> bool:
    g01, g02, g12 = (
        __import__("math").gcd(parts[0], parts[1]),
        __import__("math").gcd(parts[0], parts[2]),
        __import__("math").gcd(parts[1], parts[2]),
    )
    for k01 in range(g01 + 1):
        for k02 in range(g02 + 1):
            for k12 in range(g12 + 1):
                cross = (
                    k01 * parts[1] // g01 + k02 * parts[2] // g02,
                    k01 * parts[0] // g01 + k12 * parts[2] // g12,
                    k02 * parts[0] // g02 + k12 * parts[1] // g12,
                )
                if all(
                    any(18 <= cross[i] + d <= 24 for d in internal_degrees(parts[i]))
                    for i in range(3)
                ):
                    return True
    return False


def orbit_count(parts: tuple[int, int, int]) -> int:
    from math import gcd

    return (
        sum(length // 2 for length in parts)
        + gcd(parts[0], parts[1])
        + gcd(parts[0], parts[2])
        + gcd(parts[1], parts[2])
    )


def cycle_types() -> tuple[list[tuple[int, int, int]], int, int, int, int]:
    low = []
    infeasible = high = low_infeasible = high_infeasible = 0
    for parts in itertools.combinations_with_replacement(range(1, ORDER + 1), 3):
        if sum(parts) != ORDER:
            continue
        if not degree_feasible(parts):
            infeasible += 1
            if orbit_count(parts) <= ORBIT_CAP:
                low_infeasible += 1
            else:
                high_infeasible += 1
        elif orbit_count(parts) <= ORBIT_CAP:
            low.append(parts)
        else:
            high += 1
    if (len(low), infeasible, high) != (26, 79, 49):
        raise AssertionError("unexpected cycle-type sieve census")
    return low, infeasible, high, low_infeasible, high_infeasible


def permutation(parts: tuple[int, int, int]) -> tuple[int, ...]:
    result = []
    start = 0
    for length in parts:
        result.extend(start + (offset + 1) % length for offset in range(length))
        start += length
    return tuple(result)


def edge_orbits(parts: tuple[int, int, int]) -> list[list[tuple[int, int]]]:
    perm = permutation(parts)
    unused = set(itertools.combinations(range(ORDER), 2))
    result = []
    while unused:
        seed = min(unused)
        edge = seed
        orbit = []
        while not orbit or edge != seed:
            orbit.append(edge)
            edge = tuple(sorted((perm[edge[0]], perm[edge[1]])))
        if len(set(orbit)) != len(orbit) or not set(orbit) <= unused:
            raise AssertionError("edge orbit is not a fresh cycle")
        unused.difference_update(orbit)
        result.append(orbit)
    if len(result) != orbit_count(parts):
        raise AssertionError("edge-orbit formula mismatch")
    return result


def five_set_masks(orbits: list[list[tuple[int, int]]]) -> set[int]:
    edge_to_variable = {
        edge: variable for variable, orbit in enumerate(orbits) for edge in orbit
    }
    masks = set()
    five_count = 0
    for vertices in itertools.combinations(range(ORDER), 5):
        mask = 0
        for edge in itertools.combinations(vertices, 2):
            mask |= 1 << edge_to_variable[edge]
        masks.add(mask)
        five_count += 1
    if five_count != 962_598:
        raise AssertionError("five-set count mismatch")
    return masks


def clauses_from_masks(masks: set[int], variable_count: int) -> list[list[int]]:
    clauses = []
    for mask in sorted(masks):
        variables = [i + 1 for i in range(variable_count) if mask >> i & 1]
        clauses.append(variables)
        clauses.append([-variable for variable in variables])
    # Global color complementation makes this unit clause equisatisfiable.
    clauses.append([1])
    return clauses


def cnf_sha256(variable_count: int, clauses: list[list[int]]) -> str:
    digest = hashlib.sha256()
    digest.update(f"p cnf {variable_count} {len(clauses)}\n".encode())
    for clause in clauses:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode())
    return digest.hexdigest()


def prove(path: Path, clauses: list[list[int]]) -> dict[str, object]:
    with Solver(name="glucose42", bootstrap_with=clauses, with_proof=True) as solver:
        satisfiable = solver.solve()
        proof = solver.get_proof() if not satisfiable else None
    if satisfiable or proof is None:
        raise AssertionError("expected UNSAT with proof")
    path.write_text("\n".join(proof) + "\n")
    return {
        "satisfiable": False,
        "proof_file": str(Path("proofs") / path.name),
        "proof_line_count": len(proof),
        "proof_byte_count": path.stat().st_size,
        "proof_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--proof-dir", type=Path, default=here / "proofs")
    parser.add_argument("--result", type=Path, default=here / "proof_manifest.json")
    args = parser.parse_args()
    args.proof_dir.mkdir(parents=True, exist_ok=True)

    low, infeasible, high, low_infeasible, high_infeasible = cycle_types()
    cases = []
    for parts in low:
        orbits = edge_orbits(parts)
        masks = five_set_masks(orbits)
        clauses = clauses_from_masks(masks, len(orbits))
        name = "-".join(map(str, parts)) + ".drup"
        proof = prove(args.proof_dir / name, clauses)
        case = {
            "cycle_type": list(parts),
            "variable_count": len(orbits),
            "edge_orbit_size_histogram": {
                str(size): count for size, count in sorted(Counter(map(len, orbits)).items())
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
        cases.append(case)
        print(
            f"cycle_type={'+'.join(map(str, parts))} variables={len(orbits)} "
            f"clauses={len(clauses)} proof_lines={proof['proof_line_count']}"
        )

    manifest = {
        "format": "r55-three-cycle-low-orbit-obstruction-v1",
        "order": ORDER,
        "degree_window": [18, 24],
        "total_three_cycle_types": 154,
        "degree_infeasible_types": infeasible,
        "low_orbit_types": low_infeasible + len(low),
        "degree_infeasible_low_orbit_types": low_infeasible,
        "degree_infeasible_high_orbit_types": high_infeasible,
        "exact_low_orbit_types": len(low),
        "edge_orbit_cap": ORBIT_CAP,
        "feasible_high_orbit_types_open": high,
        "five_set_count": 962_598,
        "solver": "PySAT Glucose 4.2",
        "python_sat_version": pysat.__version__,
        "cases": cases,
    }
    args.result.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print("PASS generated 26 UNSAT proofs")


if __name__ == "__main__":
    main()
