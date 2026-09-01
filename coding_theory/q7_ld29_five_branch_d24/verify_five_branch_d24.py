#!/usr/bin/env python3
"""Verify and build the center-split certificates raising five branches to D>=24."""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import pathlib
import sys

from pysat.card import CardEnc, EncType


SOURCE_ROOT = pathlib.Path(__file__).resolve().parents[1]
D23_PATH = SOURCE_ROOT / "q7_ld29_five_branch_d23" / "verify_five_branch_d23.py"
LOCAL_GRAPHS_PATH = SOURCE_ROOT / "q7_ld29_family_reduction" / "local_graphs.py"
SEARCH_PATH = SOURCE_ROOT / "q7_ld29_family_reduction" / "search_q7_ld29.py"
EXPECTED_D23_SHA256 = "08183ecd8deb3cb83a59b0e88e483d3ca0838bda24b1e28179d54cdaa0e6ce73"
EXPECTED_LOCAL_GRAPHS_SHA256 = "35d187198ed332f64551a174096168f101adff309e0dfaf6d94f9ba6d360e1f4"
EXPECTED_SEARCH_SHA256 = "3d4cc2bd966dbed2e4b585d3725dd37356487ad735eb008e55e730a7b9022614"
assert hashlib.sha256(D23_PATH.read_bytes()).hexdigest() == EXPECTED_D23_SHA256
assert hashlib.sha256(LOCAL_GRAPHS_PATH.read_bytes()).hexdigest() == EXPECTED_LOCAL_GRAPHS_SHA256
assert hashlib.sha256(SEARCH_PATH.read_bytes()).hexdigest() == EXPECTED_SEARCH_SHA256
sys.path.insert(0, str(D23_PATH.parent))
sys.path.insert(0, str(LOCAL_GRAPHS_PATH.parent))

import verify_five_branch_d23 as d23  # noqa: E402
from local_graphs import local_graph_assumptions, local_graph_representatives  # noqa: E402
from search_q7_ld29 import (  # noqa: E402
    NEIGHBORS,
    add_nonisolated_variables,
    add_pair_indicators,
    add_singleton_variables,
    build as base_build,
    dimacs_bytes,
)


BRANCHES = (44, 47, 50, 52, 57)
MASKS = {44: 703, 47: 766, 50: 957, 52: 1751, 57: 1916}
EXPECTED_STABILIZERS = {44: 2, 47: 2, 50: 4, 52: 2, 57: 2}
EXPECTED_CENTERS = {
    44: (14, 26, 53, 63, 77, 85, 89, 95, 113, 116, 119, 125, 126, 127),
    47: (26, 28, 57, 63, 71, 77, 89, 95, 101, 105, 111, 120, 123, 125, 126, 127),
    50: (38, 43, 57, 63, 105, 111, 120, 123, 126, 127),
    52: (22, 51, 63, 77, 85, 95, 99, 101, 111, 113, 119, 125, 126, 127),
    57: (15, 28, 39, 53, 63, 101, 111, 113, 119, 125, 126, 127),
}
EDGES = tuple(itertools.combinations(range(6), 2))
EXPECTED_VARIABLES = 10432
EXPECTED_CLAUSES = 183627


def load_manifest() -> dict[str, dict[str, str]]:
    path = pathlib.Path(__file__).with_name("certificate_manifest.tsv")
    with path.open(newline="") as handle:
        rows = tuple(csv.DictReader(handle, delimiter="\t"))
    result = {row["formula"]: row for row in rows}
    expected_names = {
        f"branch{branch}-d23-center{center}"
        for branch in BRANCHES
        for center in EXPECTED_CENTERS[branch]
    }
    assert len(rows) == len(result) == 66
    assert set(result) == expected_names
    return result


MANIFEST = load_manifest()


def selected_edges(mask: int) -> frozenset[tuple[int, int]]:
    return frozenset(edge for index, edge in enumerate(EDGES) if mask >> index & 1)


def center_cost(center: int, mask: int) -> int | None:
    """Lower-bound residual local slots forced by a noncodeword F7 center."""

    weight = center.bit_count()
    edges = selected_edges(mask)
    local_words = tuple((1 << (i + 1)) | (1 << (j + 1)) for i, j in edges)
    if weight <= 2:
        return None
    if weight == 3:
        if center & 1:
            return None
        support = tuple(index - 1 for index in range(1, 7) if center & (1 << index))
        return 1 if all(edge in edges for edge in itertools.combinations(support, 2)) else None
    if weight == 4:
        return sum((center & word) == word for word in local_words)
    if weight == 5:
        nonorphan_support = tuple(index - 1 for index in range(1, 7) if center & (1 << index))
        assert len(nonorphan_support) >= 4
        assert any(edge in edges for edge in itertools.combinations(nonorphan_support, 2))
        return 3
    return 0


def transform_word(word: int, permutation: tuple[int, ...]) -> int:
    result = word & 1
    for coordinate in range(6):
        if word & (1 << (coordinate + 1)):
            result |= 1 << (permutation[coordinate] + 1)
    return result


def stabilizer(mask: int) -> tuple[tuple[int, ...], ...]:
    edges = selected_edges(mask)
    return tuple(
        permutation
        for permutation in itertools.permutations(range(6))
        if {
            tuple(sorted((permutation[first], permutation[second])))
            for first, second in edges
        }
        == edges
    )


def center_orbit_representatives(mask: int) -> tuple[int, ...]:
    group = stabilizer(mask)
    candidates = {
        center
        for center in range(128)
        if center_cost(center, mask) is not None and center_cost(center, mask) <= 1
    }
    result = []
    while candidates:
        center = min(candidates)
        orbit = {transform_word(center, permutation) for permutation in group}
        assert orbit <= candidates
        result.append(center)
        candidates -= orbit
    return tuple(result)


def surviving_d23_states(mask: int):
    _, _, local_defect, local_capacity, forced_deficit, _ = d23.local_data(mask)
    states = []
    for state in raw_states(mask, 23):
        couples, extra, _, _ = state
        if d23.ladder.arithmetic_state_survives(
            23,
            couples,
            extra,
            local_defect,
            local_capacity,
            forced_deficit,
        ):
            states.append(state)
    return tuple(states)


def raw_states(mask: int, defect: int):
    _, _, local_defect, local_capacity, forced_deficit, _ = d23.local_data(mask)
    states = []
    for couples in range((34 - defect) // 2 + 1):
        family_vertices = 104 - defect - 2 * couples
        family_budget = 34 - defect - 2 * couples
        for extra in d23.defect_partitions(defect - local_defect):
            capacity = local_capacity + sum(d23.ladder.FAMILY_CAPACITY[d] for d in extra)
            free_missing = capacity - family_vertices - forced_deficit
            if free_missing >= 0:
                states.append((couples, extra, free_missing, family_budget))
    return tuple(states)


def verify_split(branch: int, mask: int) -> tuple[int, ...]:
    states = surviving_d23_states(mask)
    assert len(states) == 13
    for _, extra, free_missing, family_budget in states:
        f5 = extra.count(5)
        assert f5 >= 1
        # A codeword F7 father would force at least 7-free_missing family
        # codewords, already exceeding the entire family-codeword budget.
        assert 7 - free_missing > family_budget
        # If there is one F7 family then free_missing<=1.  If there are at
        # least two, free_missing<=3, so one has center cost at most one.
        assert (f5 == 1 and free_missing <= 1) or (f5 >= 2 and free_missing <= 3)
    group = stabilizer(mask)
    assert len(group) == EXPECTED_STABILIZERS[branch]
    centers = center_orbit_representatives(mask)
    assert centers == EXPECTED_CENTERS[branch]
    print(
        f"PASS branch={branch} mask={mask} D23_states={len(states)} "
        f"stabilizer={len(group)} center_orbits={centers}"
    )
    return centers


def build_formula(branch: int):
    cnf = base_build(
        lex=False,
        structural=False,
        pair_bounds=False,
        dynamic_pair_bound=False,
    )
    nonisolated = add_nonisolated_variables(cnf)
    singleton = add_singleton_variables(cnf)
    edges = add_pair_indicators(cnf, 1)
    cnf.extend(
        CardEnc.atmost(
            lits=nonisolated,
            bound=11,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend(
        CardEnc.atleast(
            lits=singleton,
            bound=47,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend(
        CardEnc.atmost(
            lits=[*nonisolated, *singleton],
            bound=58,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend(
        CardEnc.atmost(
            lits=edges,
            bound=17,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    mask = local_graph_representatives()[branch]
    assert mask == MASKS[branch]
    cnf.extend([[literal] for literal in local_graph_assumptions(mask)])
    cnf.clauses[:] = [list(dict.fromkeys(clause)) for clause in cnf.clauses]
    return cnf, mask


def add_center(cnf, center: int) -> None:
    cnf.extend(
        [[-(center + 1)], *[[neighbor + 1] for neighbor in NEIGHBORS[center]]]
    )
    cnf.clauses[:] = [list(dict.fromkeys(clause)) for clause in cnf.clauses]


def scratch_directory(raw: str) -> pathlib.Path:
    path = pathlib.Path(raw).resolve()
    if not path.is_relative_to("/scratch"):
        raise ValueError("CNF output must remain under /scratch")
    path.mkdir(parents=True, exist_ok=True)
    return path


def check_formula(cnf, name: str, output: pathlib.Path | None) -> None:
    payload = dimacs_bytes(cnf)
    digest = hashlib.sha256(payload).hexdigest()
    assert cnf.nv == EXPECTED_VARIABLES
    assert len(cnf.clauses) == EXPECTED_CLAUSES
    assert digest == MANIFEST[name]["cnf_sha256"]
    if output is not None:
        (output / f"{name}.cnf").write_bytes(payload)
    print(
        f"PASS formula={name} variables={cnf.nv} clauses={len(cnf.clauses)} "
        f"sha256={digest}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-directory")
    parser.add_argument("--solve-kissat", action="store_true")
    args = parser.parse_args()
    output = scratch_directory(args.write_directory) if args.write_directory else None

    for branch in BRANCHES:
        base, mask = build_formula(branch)
        centers = verify_split(branch, mask)
        for center in centers:
            cnf = base.copy()
            add_center(cnf, center)
            name = f"branch{branch}-d23-center{center}"
            check_formula(cnf, name, output)
            if args.solve_kissat:
                from pysat.solvers import Solver

                with Solver(name="kissat404", bootstrap_with=cnf.clauses) as solver:
                    assert not solver.solve()
                print(f"PASS Kissat 4.0.4 returned UNSAT for {name}")
    print("PASS all 66 center formulas reconstructed; hence D>=24 in all five branches")


if __name__ == "__main__":
    main()
