#!/usr/bin/env python3
"""Verify the codeword-couple closure of Q7 LD29 branches 61 and 62.

Generated CNF files are deliberately restricted to /scratch.  Solver proofs,
logs, and traces are not part of this source contribution.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import pathlib
import sys
import time

from pysat.card import CardEnc, EncType


SOURCE_ROOT = pathlib.Path(__file__).resolve().parents[1]
EXACT_D24_PATH = (
    SOURCE_ROOT
    / "q7_ld29_branches61_62_exact_defect24"
    / "verify_exact_defect24.py"
)
SPLIT_PATH = SOURCE_ROOT / "q7_ld29_branch79_split" / "verify_branch79_split.py"
LOCAL_GRAPHS_PATH = SOURCE_ROOT / "q7_ld29_family_reduction" / "local_graphs.py"
SEARCH_PATH = SOURCE_ROOT / "q7_ld29_family_reduction" / "search_q7_ld29.py"
EXPECTED_SOURCE_HASHES = {
    EXACT_D24_PATH: "9500400daf4723912f56e5a0e3464a876fc18f52d279831ee38b1c34f6aef71e",
    SPLIT_PATH: "ea313ef366ad3b2da6c4e43d721aef8e96ec9bfa7dafe18c8fdade61c5fdd687",
    LOCAL_GRAPHS_PATH: "35d187198ed332f64551a174096168f101adff309e0dfaf6d94f9ba6d360e1f4",
    SEARCH_PATH: "3d4cc2bd966dbed2e4b585d3725dd37356487ad735eb008e55e730a7b9022614",
}
for source_path, expected_hash in EXPECTED_SOURCE_HASHES.items():
    assert hashlib.sha256(source_path.read_bytes()).hexdigest() == expected_hash

sys.path.insert(0, str(SOURCE_ROOT / "q7_ld29_family_reduction"))
sys.path.insert(0, str(SPLIT_PATH.parent))

import verify_branch79_split as split  # noqa: E402
from local_graphs import local_graph_assumptions, local_graph_representatives  # noqa: E402
from search_q7_ld29 import (  # noqa: E402
    NEIGHBORS,
    add_nonisolated_variables,
    add_pair_indicators,
    add_singleton_variables,
    build as base_build,
    dimacs_bytes,
)


MASKS = {61: 5941, 62: 5948}
EXPECTED_STATE_DISTRIBUTION = {1: 3, 2: 5, 3: 11, 4: 24, 5: 46}
EXPECTED_ORBITS = {61: 58, 62: 76}
EXPECTED_FORMULAS = {
    61: {
        "variables": 11386,
        "clauses": 193457,
        "bytes": 3640388,
        "sha256": "685d071c82ce9325653f438d90f7822a12f6f666f713af4c9dabc5cecb4f51db",
    },
    62: {
        "variables": 11404,
        "clauses": 193709,
        "bytes": 3643674,
        "sha256": "af2c03482eff31a48d492b42bb919a507e18399e83c6aa96edb05c56a5f8e897",
    },
}
EDGES = tuple(itertools.combinations(range(6), 2))


def exact_defect_states(mask: int):
    """Enumerate all capacity-feasible D=24 family arithmetic states."""
    states = tuple(
        filter(
            split.survives_defect_six_occupancy,
            split.raw_states(mask, 24),
        )
    )
    distribution = Counter(state[0] for state in states)
    assert len(states) == 89
    assert dict(sorted(distribution.items())) == EXPECTED_STATE_DISTRIBUTION
    assert all(state[0] >= 1 for state in states)
    return states


def selected_edges(mask: int) -> frozenset[tuple[int, int]]:
    return frozenset(edge for index, edge in enumerate(EDGES) if mask >> index & 1)


def stabilizer(mask: int) -> tuple[tuple[int, ...], ...]:
    graph_edges = selected_edges(mask)
    return tuple(
        permutation
        for permutation in itertools.permutations(range(6))
        if {
            tuple(sorted((permutation[first], permutation[second])))
            for first, second in graph_edges
        }
        == graph_edges
    )


def transform_word(word: int, permutation: tuple[int, ...]) -> int:
    """Apply a permutation of coordinates 1,...,6, fixing coordinate 0."""
    result = word & 1
    for coordinate in range(6):
        if word & (1 << (coordinate + 1)):
            result |= 1 << (permutation[coordinate] + 1)
    return result


def forced_vertices(mask: int) -> tuple[set[int], set[int]]:
    local_units = local_graph_assumptions(mask)
    forced_true = {literal - 1 for literal in local_units if literal > 0} | {0}
    forced_false = {-literal - 1 for literal in local_units if literal < 0}
    forced_false |= {1 << coordinate for coordinate in range(7)}
    forced_false |= {1 | (1 << coordinate) for coordinate in range(1, 7)}
    assert forced_true.isdisjoint(forced_false)
    return forced_true, forced_false


def candidate_couple_edges(mask: int) -> set[tuple[int, int]]:
    """Return cube edges not already forbidden as induced two-codeword components."""
    forced_true, forced_false = forced_vertices(mask)
    candidates: set[tuple[int, int]] = set()
    for first in range(128):
        for second in NEIGHBORS[first]:
            if second <= first or {first, second} & forced_false:
                continue
            outside = (set(NEIGHBORS[first]) - {second}) | (
                set(NEIGHBORS[second]) - {first}
            )
            if outside & forced_true:
                continue
            candidates.add((first, second))
    assert len(candidates) == 200
    return candidates


def edge_orbit_representatives(branch: int) -> tuple[tuple[int, int], ...]:
    mask = MASKS[branch]
    remaining = candidate_couple_edges(mask)
    group = stabilizer(mask)
    assert len(group) == 4
    representatives: list[tuple[int, int]] = []
    while remaining:
        edge = min(remaining)
        orbit = {
            tuple(
                sorted(
                    (
                        transform_word(edge[0], permutation),
                        transform_word(edge[1], permutation),
                    )
                )
            )
            for permutation in group
        }
        assert orbit <= remaining
        representatives.append(edge)
        remaining -= orbit
    assert len(representatives) == EXPECTED_ORBITS[branch]
    return tuple(representatives)


def couple_literals(first: int, second: int) -> list[int]:
    """Literals saying {first,second} is an induced code component."""
    assert second in NEIGHBORS[first]
    literals = [first + 1, second + 1]
    literals += [
        -(neighbor + 1) for neighbor in NEIGHBORS[first] if neighbor != second
    ]
    literals += [
        -(neighbor + 1) for neighbor in NEIGHBORS[second] if neighbor != first
    ]
    assert len(literals) == 14
    assert len(set(literals)) == 14
    return literals


def build_exact_d24_base(branch: int):
    """Build the exact-D=24 relaxation before selecting a couple orbit."""
    cnf = base_build(
        lex=False,
        structural=False,
        pair_bounds=False,
        dynamic_pair_bound=False,
    )
    nonisolated = add_nonisolated_variables(cnf)
    singletons = add_singleton_variables(cnf)
    code_edges = add_pair_indicators(cnf, 1)

    # D=24 gives p=48, b<=10, p+b<=58 and
    # e(Q_7[C])<=E_7(10)=15.  Each encoder is added sequentially so that
    # its auxiliaries start above the current variable maximum.
    cnf.extend(
        CardEnc.equals(
            lits=singletons,
            bound=48,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend(
        CardEnc.atmost(
            lits=nonisolated,
            bound=10,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend(
        CardEnc.atmost(
            lits=[*nonisolated, *singletons],
            bound=58,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend(
        CardEnc.atmost(
            lits=code_edges,
            bound=15,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )

    representatives = local_graph_representatives()
    assert len(representatives) == 115
    mask = representatives[branch]
    assert mask == MASKS[branch]
    cnf.extend([[literal] for literal in local_graph_assumptions(mask)])
    cnf.clauses[:] = [list(dict.fromkeys(clause)) for clause in cnf.clauses]
    return cnf


def build_selector_formula(branch: int):
    """Build one disjunction over local-stabilizer couple representatives."""
    cnf = build_exact_d24_base(branch)
    representatives = edge_orbit_representatives(branch)
    selectors: list[int] = []
    for first, second in representatives:
        selector = cnf.nv + 1
        selectors.append(selector)
        for literal in couple_literals(first, second):
            cnf.append([-selector, literal])
    cnf.append(selectors)
    return cnf, representatives


def scratch_directory(raw: str) -> pathlib.Path:
    path = pathlib.Path(raw).resolve()
    if not path.is_relative_to("/scratch"):
        raise ValueError("CNF output must remain under /scratch")
    path.mkdir(parents=True, exist_ok=True)
    return path


def solve_incrementally(cnf, branch: int, representatives) -> None:
    """Independently solve each representative with PySAT CaDiCaL 1.9.5."""
    from pysat.solvers import Solver

    started = time.monotonic()
    with Solver(name="cadical195", bootstrap_with=cnf.clauses) as solver:
        for index, edge in enumerate(representatives, 1):
            case_started = time.monotonic()
            satisfiable = solver.solve(assumptions=couple_literals(*edge))
            print(
                f"CASE branch={branch} {index}/{len(representatives)} "
                f"edge={edge} result={'SAT' if satisfiable else 'UNSAT'} "
                f"seconds={time.monotonic() - case_started:.3f}",
                flush=True,
            )
            if satisfiable:
                raise AssertionError(f"unexpected satisfying couple orbit {edge}")
        stats = solver.accum_stats()
    print(
        f"PASS branch={branch} all_couple_orbits=UNSAT "
        f"seconds={time.monotonic() - started:.3f} stats={stats}",
        flush=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-directory")
    parser.add_argument("--solve-incrementally", action="store_true")
    args = parser.parse_args()
    output = scratch_directory(args.write_directory) if args.write_directory else None

    for branch in sorted(MASKS):
        states = exact_defect_states(MASKS[branch])
        print(
            f"PASS analytic branch={branch} D=24 states={len(states)} "
            f"couple_distribution={EXPECTED_STATE_DISTRIBUTION} q>=1"
        )
        cnf, representatives = build_selector_formula(branch)
        payload = dimacs_bytes(cnf)
        expected = EXPECTED_FORMULAS[branch]
        digest = hashlib.sha256(payload).hexdigest()
        assert cnf.nv == expected["variables"]
        assert len(cnf.clauses) == expected["clauses"]
        assert len(payload) == expected["bytes"]
        assert digest == expected["sha256"]
        if output is not None:
            (output / f"branch{branch}-couple-selector.cnf").write_bytes(payload)
        print(
            f"PASS formula=branch{branch}-couple-selector mask={MASKS[branch]} "
            f"candidate_edges=200 orbits={len(representatives)} "
            f"stabilizer=4 variables={cnf.nv} clauses={len(cnf.clauses)} "
            f"bytes={len(payload)} sha256={digest}"
        )
        if args.solve_incrementally:
            # Use the base formula: assumptions select exactly one orbit.
            solve_incrementally(build_exact_d24_base(branch), branch, representatives)


if __name__ == "__main__":
    main()
