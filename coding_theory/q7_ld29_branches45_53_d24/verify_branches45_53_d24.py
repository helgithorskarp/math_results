#!/usr/bin/env python3
"""Verify the exact D>=24 center split for Q7 LD29 branches 45 and 53."""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import pathlib
import sys
import time

from pysat.card import CardEnc, EncType


SOURCE_ROOT = pathlib.Path(__file__).resolve().parents[1]
LADDER_PATH = SOURCE_ROOT / "q7_ld29_branches0_62_bounds" / "verify_lower_frontier_bounds.py"
SPLIT_PATH = SOURCE_ROOT / "q7_ld29_branch79_split" / "verify_branch79_split.py"
PREVIOUS_CENTER_SPLIT_PATH = (
    SOURCE_ROOT / "q7_ld29_branches61_62_split" / "verify_branches61_62_split.py"
)
EXPECTED_SOURCE_HASHES = {
    LADDER_PATH: "acde98fb29c8673d57ceddc47b36e5b46a62a0cfa13ed542886e96fbaf0c4852",
    SPLIT_PATH: "ea313ef366ad3b2da6c4e43d721aef8e96ec9bfa7dafe18c8fdade61c5fdd687",
    PREVIOUS_CENTER_SPLIT_PATH: "c91531e6cc12c993a2a59a8e83b2bcede8fba8fc50d4589eac415b28670456c9",
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


MASKS = {45: 759, 53: 1781}
EXPECTED_LOCAL_DATA = {
    45: ((1, 1, 3, 3, 4, 4), 4, 10, 36, 20, 3),
    53: ((1, 2, 3, 3, 3, 4), 3, 10, 36, 20, 3),
}
EXPECTED_STATES = (
    (5, (1, 1, 1, 5, 5), 1, 1),
    (5, (1, 2, 5, 5), 0, 1),
    (5, (3, 5, 5), 0, 1),
)
EXPECTED_RAW_PAIR_COUNTS = {45: 20, 53: 12}
EXPECTED_STABILIZER_ORDERS = {45: 4, 53: 1}
EXPECTED_CASES = {
    45: ((14, 105), (14, 113), (14, 119), (14, 123), (26, 105), (26, 111), (26, 125)),
    53: (
        (22, 111), (22, 113), (22, 123), (22, 125),
        (28, 111), (28, 113), (28, 119), (28, 123),
        (44, 95), (44, 113), (44, 119), (44, 123),
    ),
}
EXPECTED_VARIABLES = 10432
EXPECTED_CLAUSES = 183635


def expected_formula_names() -> set[str]:
    return {
        f"branch{branch}-d23-f{first}-g{second}"
        for branch, cases in EXPECTED_CASES.items()
        for first, second in cases
    }


def load_manifest() -> dict[str, dict[str, str]]:
    with pathlib.Path(__file__).with_name("certificate_manifest.tsv").open(newline="") as handle:
        rows = tuple(csv.DictReader(handle, delimiter="\t"))
    result = {row["formula"]: row for row in rows}
    assert len(rows) == len(result) == 19
    assert set(result) == expected_formula_names()
    for row in rows:
        assert int(row["variables"]) == EXPECTED_VARIABLES
        assert int(row["clauses"]) == int(row["original_total"]) == EXPECTED_CLAUSES
        assert int(row["cnf_bytes"]) > 0 and int(row["proof_bytes"]) > 0
        assert len(row["cnf_sha256"]) == len(row["proof_sha256"]) == 64
        assert int(row["rat_core"]) == 0
    return result


MANIFEST = load_manifest()


def transform_word(word: int, permutation: tuple[int, ...]) -> int:
    result = word & 1
    for old, new in enumerate(permutation):
        if word & (1 << (old + 1)):
            result |= 1 << (new + 1)
    return result


def stabilizer(mask: int) -> tuple[tuple[int, ...], ...]:
    edges = split.selected_edges(mask)
    return tuple(
        permutation
        for permutation in itertools.permutations(range(6))
        if {tuple(sorted((permutation[x], permutation[y]))) for x, y in edges} == edges
    )


def exceptional_pairs(mask: int) -> set[tuple[int, int]]:
    return {
        (first, second)
        for first, second in itertools.combinations(range(128), 2)
        if split.center_cost(first, mask) is not None
        and split.center_cost(second, mask) is not None
        and split.center_cost(first, mask) + split.center_cost(second, mask) <= 1
        and split.hamming_distance(first, second) >= 5
    }


def orbit_representatives(mask: int) -> tuple[tuple[int, int], ...]:
    remaining = exceptional_pairs(mask)
    group = stabilizer(mask)
    representatives = []
    while remaining:
        pair = min(remaining)
        orbit = {
            tuple(sorted((transform_word(pair[0], permutation), transform_word(pair[1], permutation))))
            for permutation in group
        }
        assert orbit <= remaining
        representatives.append(pair)
        remaining -= orbit
    return tuple(representatives)


def verify_analytic_split(branch: int, mask: int) -> tuple[tuple[int, int], ...]:
    assert split.local_data(mask) == EXPECTED_LOCAL_DATA[branch]
    states = tuple(filter(split.survives_defect_six_occupancy, split.raw_states(mask, 23)))
    assert states == EXPECTED_STATES

    zero_cost = tuple(center for center in range(128) if split.center_cost(center, mask) == 0)
    assert all(
        split.hamming_distance(first, second) <= 4
        for first, second in itertools.combinations(zero_cost, 2)
    )

    pairs = exceptional_pairs(mask)
    assert len(pairs) == EXPECTED_RAW_PAIR_COUNTS[branch]
    group = stabilizer(mask)
    assert len(group) == EXPECTED_STABILIZER_ORDERS[branch]
    representatives = orbit_representatives(mask)
    assert representatives == EXPECTED_CASES[branch]
    print(
        f"PASS analytic branch={branch} mask={mask} local_data={split.local_data(mask)} "
        f"stabilizer={len(group)} pairs={len(pairs)} orbits={len(representatives)}"
    )
    return representatives


def build_base(branch: int, mask: int):
    cnf = base_build(lex=False, structural=False, pair_bounds=False, dynamic_pair_bound=False)
    nonisolated = add_nonisolated_variables(cnf)
    singletons = add_singleton_variables(cnf)
    code_edges = add_pair_indicators(cnf, 1)
    cnf.extend(CardEnc.atmost(lits=nonisolated, bound=11, top_id=cnf.nv, encoding=EncType.totalizer).clauses)
    cnf.extend(CardEnc.atleast(lits=singletons, bound=47, top_id=cnf.nv, encoding=EncType.totalizer).clauses)
    cnf.extend(CardEnc.atmost(lits=[*nonisolated, *singletons], bound=58, top_id=cnf.nv, encoding=EncType.totalizer).clauses)
    cnf.extend(CardEnc.atmost(lits=code_edges, bound=17, top_id=cnf.nv, encoding=EncType.totalizer).clauses)
    representatives = local_graph_representatives()
    assert len(representatives) == 115 and representatives[branch] == mask
    cnf.extend([[literal] for literal in local_graph_assumptions(mask)])
    cnf.clauses[:] = [list(dict.fromkeys(clause)) for clause in cnf.clauses]
    return cnf


def add_centers(cnf, first: int, second: int) -> None:
    units = [
        -(first + 1),
        -(second + 1),
        *(neighbor + 1 for neighbor in NEIGHBORS[first]),
        *(neighbor + 1 for neighbor in NEIGHBORS[second]),
    ]
    assert len(units) == len(set(units)) == 16
    cnf.extend([[literal] for literal in units])
    cnf.clauses[:] = [list(dict.fromkeys(clause)) for clause in cnf.clauses]


def scratch_directory(raw: str) -> pathlib.Path:
    path = pathlib.Path(raw).resolve()
    if not path.is_relative_to("/scratch"):
        raise ValueError("CNF output must remain under /scratch")
    path.mkdir(parents=True, exist_ok=True)
    return path


def report_formula(branch: int, first: int, second: int, cnf, output: pathlib.Path | None) -> str:
    name = f"branch{branch}-d23-f{first}-g{second}"
    row = MANIFEST[name]
    payload = dimacs_bytes(cnf)
    digest = hashlib.sha256(payload).hexdigest()
    assert cnf.nv == int(row["variables"]) == EXPECTED_VARIABLES
    assert len(cnf.clauses) == int(row["clauses"]) == EXPECTED_CLAUSES
    assert len(payload) == int(row["cnf_bytes"])
    assert digest == row["cnf_sha256"]
    if output is not None:
        (output / f"{name}.cnf").write_bytes(payload)
    print(
        f"PASS formula={name} variables={cnf.nv} clauses={len(cnf.clauses)} "
        f"bytes={len(payload)} sha256={digest}",
        flush=True,
    )
    return name


def solve_kissat(name: str, cnf) -> None:
    from pysat.solvers import Solver

    started = time.monotonic()
    with Solver(name="kissat404", bootstrap_with=cnf.clauses) as solver:
        result = solver.solve()
    print(
        f"SOLVE formula={name} result={'SAT' if result else 'UNSAT'} "
        f"seconds={time.monotonic() - started:.3f}",
        flush=True,
    )
    if result:
        raise AssertionError(f"unexpected satisfying assignment for {name}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-directory")
    parser.add_argument("--solve-kissat", action="store_true")
    args = parser.parse_args()
    output = scratch_directory(args.write_directory) if args.write_directory else None

    formula_count = 0
    for branch, mask in MASKS.items():
        cases = verify_analytic_split(branch, mask)
        base = build_base(branch, mask)
        for first, second in cases:
            cnf = base.copy()
            add_centers(cnf, first, second)
            name = report_formula(branch, first, second, cnf, output)
            formula_count += 1
            if args.solve_kissat:
                solve_kissat(name, cnf)
    assert formula_count == 19
    print("PASS 19 certified center cases exclude D=23 in branches 45 and 53; hence D>=24")


if __name__ == "__main__":
    main()
