#!/usr/bin/env python3
"""Build and check the exact-defect closure of Q7 LD29 branches 45 and 53.

Generated CNFs, proof traces, and solver logs must remain under /scratch.
The proof manifest records the external CaDiCaL/DRAT-trim certificates; this
program reconstructs the analytic state split, symmetry cover, and exact CNFs.
"""

from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import pathlib
import sys
import time

from pysat.card import CardEnc, EncType


SOURCE_ROOT = pathlib.Path(__file__).resolve().parents[1]
SIBLING_PATH = (
    SOURCE_ROOT
    / "q7_ld29_branches44_47_52_57_closure"
    / "verify_sibling_closures.py"
)
EXPECTED_SOURCE_HASHES = {
    SIBLING_PATH: "1069616e39ad4c39e46d0094f91c6e2a9efc13983229033add53cf5551ac4fe6",
}
for source_path, expected_hash in EXPECTED_SOURCE_HASHES.items():
    assert hashlib.sha256(source_path.read_bytes()).hexdigest() == expected_hash

sys.path.insert(0, str(SIBLING_PATH.parent))

import verify_sibling_closures as sibling  # noqa: E402


BRANCHES = (45, 53)
MASKS = {45: 759, 53: 1781}
EXPECTED_STABILIZERS = {45: 4, 53: 1}
EXPECTED_STATE_DISTRIBUTION = {1: 3, 2: 5, 3: 11, 4: 24, 5: 46}
EXPECTED_COUPLE_COUNTS = {45: (206, 78), 53: (203, 203)}


def load_manifest() -> dict[str, dict[str, str]]:
    path = pathlib.Path(__file__).with_name("certificate_manifest.tsv")
    with path.open(newline="") as handle:
        rows = tuple(csv.DictReader(handle, delimiter="\t"))
    result = {row["formula"]: row for row in rows}
    expected = {
        f"branch{branch}-{suffix}"
        for branch in BRANCHES
        for suffix in ("d25", "d24-couple-selector")
    }
    assert len(rows) == len(result) == len(expected) == 4
    assert set(result) == expected
    for row in rows:
        assert int(row["variables"]) > 0
        assert int(row["clauses"]) == int(row["original_total"])
        assert int(row["cnf_bytes"]) > 0 and int(row["proof_bytes"]) > 0
        assert len(row["cnf_sha256"]) == len(row["proof_sha256"]) == 64
        assert int(row["rat_core"]) == 0
    return result


MANIFEST = load_manifest()


def verify_family_split(branch: int, mask: int) -> None:
    assert sibling.local_graph_representatives()[branch] == MASKS[branch] == mask
    assert len(sibling.d24.stabilizer(mask)) == EXPECTED_STABILIZERS[branch]
    states = tuple(
        filter(
            sibling.survives_defect_six_occupancy,
            sibling.d24.raw_states(mask, 24),
        )
    )
    distribution = collections.Counter(state[0] for state in states)
    assert len(states) == 89
    assert dict(sorted(distribution.items())) == EXPECTED_STATE_DISTRIBUTION
    assert all(couples >= 1 for couples, *_ in states)
    print(
        f"PASS family_split branch={branch} D=24 states={len(states)} "
        f"couple_distribution={dict(sorted(distribution.items()))} q>=1"
    )


def couple_cases(branch: int, mask: int):
    candidates = sibling.candidate_couple_edges(mask)
    representatives = sibling.couple_representatives(mask)
    observed = (len(candidates), len(representatives))
    assert observed == EXPECTED_COUPLE_COUNTS[branch]
    cases = tuple(
        (f"couple-{first}-{second}", sibling.couple_literals(first, second))
        for first, second in representatives
    )
    print(
        f"PASS couple_cover branch={branch} candidates={observed[0]} "
        f"orbits={observed[1]} stabilizer={EXPECTED_STABILIZERS[branch]}"
    )
    return cases


def build_common(branch: int, defect: int):
    assert branch in BRANCHES and defect in (24, 25)
    cnf = sibling.base_build(
        lex=False,
        structural=False,
        pair_bounds=False,
        dynamic_pair_bound=False,
    )
    nonisolated = sibling.add_nonisolated_variables(cnf)
    singletons = sibling.add_singleton_variables(cnf)
    code_edges = sibling.add_pair_indicators(cnf, 1)
    singleton_encoder = CardEnc.equals if defect == 24 else CardEnc.atleast
    cnf.extend(
        singleton_encoder(
            lits=singletons,
            bound=24 + defect,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend(
        CardEnc.atmost(
            lits=nonisolated,
            bound=34 - defect,
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
            bound={24: 15, 25: 13}[defect],
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend(
        [
            [literal]
            for literal in sibling.local_graph_assumptions(MASKS[branch])
        ]
    )
    cnf.clauses[:] = [list(dict.fromkeys(clause)) for clause in cnf.clauses]
    return cnf


def build_d24_selector(branch: int):
    cnf = build_common(branch, 24)
    selectors = []
    for _, literals in couple_cases(branch, MASKS[branch]):
        selector = cnf.nv + 1
        selectors.append(selector)
        for literal in literals:
            cnf.append([-selector, literal])
    cnf.append(selectors)
    return cnf


def scratch_directory(raw: str) -> pathlib.Path:
    path = pathlib.Path(raw).resolve()
    if not path.is_relative_to("/scratch"):
        raise ValueError("CNF output must remain under /scratch")
    path.mkdir(parents=True, exist_ok=True)
    return path


def report_formula(name: str, cnf, output: pathlib.Path | None) -> None:
    payload = sibling.dimacs_bytes(cnf)
    digest = hashlib.sha256(payload).hexdigest()
    row = MANIFEST[name]
    assert cnf.nv == int(row["variables"])
    assert len(cnf.clauses) == int(row["clauses"])
    assert len(payload) == int(row["cnf_bytes"])
    assert digest == row["cnf_sha256"]
    if output is not None:
        (output / f"{name}.cnf").write_bytes(payload)
    print(
        f"PASS formula={name} variables={cnf.nv} clauses={len(cnf.clauses)} "
        f"bytes={len(payload)} sha256={digest}"
    )


def solve_formula(name: str, cnf, solver_name: str = "kissat404") -> None:
    from pysat.solvers import Solver

    started = time.monotonic()
    with Solver(name=solver_name, bootstrap_with=cnf.clauses) as solver:
        satisfiable = solver.solve()
    print(
        f"SOLVE formula={name} solver={solver_name} "
        f"result={'SAT' if satisfiable else 'UNSAT'} "
        f"seconds={time.monotonic() - started:.3f}",
        flush=True,
    )
    if satisfiable:
        raise AssertionError(f"unexpected satisfying formula {name}")


def solve_incrementally(branch: int) -> None:
    from pysat.solvers import Solver

    cases = couple_cases(branch, MASKS[branch])
    cnf = build_common(branch, 24)
    started = time.monotonic()
    with Solver(name="cadical195", bootstrap_with=cnf.clauses) as solver:
        for index, (name, assumptions) in enumerate(cases, 1):
            case_started = time.monotonic()
            satisfiable = solver.solve(assumptions=assumptions)
            print(
                f"CASE branch={branch} {index}/{len(cases)} {name} "
                f"result={'SAT' if satisfiable else 'UNSAT'} "
                f"seconds={time.monotonic() - case_started:.3f}",
                flush=True,
            )
            if satisfiable:
                raise AssertionError(f"unexpected satisfying case {name}")
    print(
        f"PASS branch={branch} all_couple_cases=UNSAT "
        f"seconds={time.monotonic() - started:.3f}",
        flush=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--branches", nargs="+", type=int, default=list(BRANCHES))
    parser.add_argument("--write-directory")
    parser.add_argument("--solve-kissat", action="store_true")
    parser.add_argument("--solve-incrementally", action="store_true")
    args = parser.parse_args()
    if not set(args.branches) <= set(BRANCHES):
        parser.error(f"branches must be drawn from {BRANCHES}")
    output = scratch_directory(args.write_directory) if args.write_directory else None

    for branch in args.branches:
        verify_family_split(branch, MASKS[branch])
        d25 = build_common(branch, 25)
        d24_selector = build_d24_selector(branch)
        report_formula(f"branch{branch}-d25", d25, output)
        report_formula(f"branch{branch}-d24-couple-selector", d24_selector, output)
        if args.solve_kissat:
            solve_formula(f"branch{branch}-d25", d25)
            solve_formula(f"branch{branch}-d24-couple-selector", d24_selector)
        if args.solve_incrementally:
            solve_incrementally(branch)

    print(
        "PASS couple-selector closure excludes branches 45 and 53; "
        "51 normalized branches remain"
    )


if __name__ == "__main__":
    main()
