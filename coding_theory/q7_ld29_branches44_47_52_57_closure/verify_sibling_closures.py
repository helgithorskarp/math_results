#!/usr/bin/env python3
"""Build and check the exact-defect split for Q7 LD29 branches 44,47,52,57.

Generated CNFs, proof traces, and solver logs must remain under /scratch.
This source independently reconstructs each stabilizer quotient used by the
selector formulas; it does not import the branch-50 orbit lists.
"""

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
D24_PATH = SOURCE_ROOT / "q7_ld29_five_branch_d24" / "verify_five_branch_d24.py"
LOCAL_GRAPHS_PATH = SOURCE_ROOT / "q7_ld29_family_reduction" / "local_graphs.py"
SEARCH_PATH = SOURCE_ROOT / "q7_ld29_family_reduction" / "search_q7_ld29.py"
EXPECTED_SOURCE_HASHES = {
    D24_PATH: "6cd1880178ab8ed330db4030459a0247fc6e13016e6cf8321bce8ec7ed0e6ada",
    LOCAL_GRAPHS_PATH: "35d187198ed332f64551a174096168f101adff309e0dfaf6d94f9ba6d360e1f4",
    SEARCH_PATH: "3d4cc2bd966dbed2e4b585d3725dd37356487ad735eb008e55e730a7b9022614",
}
for source_path, expected_hash in EXPECTED_SOURCE_HASHES.items():
    assert hashlib.sha256(source_path.read_bytes()).hexdigest() == expected_hash

sys.path.insert(0, str(D24_PATH.parent))
sys.path.insert(0, str(LOCAL_GRAPHS_PATH.parent))

import verify_five_branch_d24 as d24  # noqa: E402
from local_graphs import local_graph_assumptions, local_graph_representatives  # noqa: E402
from search_q7_ld29 import (  # noqa: E402
    NEIGHBORS,
    add_nonisolated_variables,
    add_pair_indicators,
    add_singleton_variables,
    build as base_build,
    dimacs_bytes,
)


BRANCHES = (44, 47, 52, 57)
MASKS = {44: 703, 47: 766, 52: 1751, 57: 1916}
EXPECTED_STABILIZERS = {44: 2, 47: 2, 52: 2, 57: 2}
EXPECTED_Q0_STATES = (
    (0, (1, 1, 1, 5, 6), 1, 10),
    (0, (1, 2, 5, 6), 0, 10),
    (0, (3, 5, 6), 0, 10),
)
EXPECTED_ORBIT_COUNTS = {
    44: (207, 116, 21, 56, 122, 66),
    47: (204, 139, 19, 55, 92, 62),
    52: (204, 143, 18, 56, 86, 55),
    57: (201, 113, 17, 52, 69, 40),
}
EXPECTED_WEDGE_WORDS = {
    44: (14, 22, 26, 28, 38, 42, 44, 50, 70, 74, 82, 98),
    47: (14, 22, 26, 28, 38, 42, 44, 50, 52, 74, 82, 98),
    52: (14, 22, 26, 28, 38, 42, 44, 52, 56, 70, 74, 82),
    57: (22, 26, 28, 42, 44, 50, 56, 70, 76, 82, 84, 98),
}


def load_manifest() -> dict[str, dict[str, str]]:
    path = pathlib.Path(__file__).with_name("certificate_manifest.tsv")
    with path.open(newline="") as handle:
        rows = tuple(csv.DictReader(handle, delimiter="\t"))
    result = {row["formula"]: row for row in rows}
    expected = {
        f"branch{branch}-{suffix}"
        for branch in BRANCHES
        for suffix in ("d25", "d24-selector")
    }
    assert len(rows) == len(result) == len(expected) == 8
    assert set(result) == expected
    return result


MANIFEST = load_manifest()


def survives_defect_six_occupancy(state) -> bool:
    _, extra, free_missing, family_codeword_budget = state
    return max(0, 8 * extra.count(6) - free_missing) <= family_codeword_budget


def verify_family_split(branch: int, mask: int) -> None:
    assert local_graph_representatives()[branch] == MASKS[branch] == mask
    assert d24.MASKS[branch] == mask
    assert len(d24.stabilizer(mask)) == EXPECTED_STABILIZERS[branch]
    states = tuple(filter(survives_defect_six_occupancy, d24.raw_states(mask, 24)))
    q0_states = tuple(state for state in states if state[0] == 0)
    assert len(states) == 187
    assert q0_states == EXPECTED_Q0_STATES
    for couples, extra, free_missing, family_codeword_budget in q0_states:
        assert couples == 0
        assert extra.count(5) == extra.count(6) == 1
        assert free_missing <= 1
        # A selected F7 father and the selected closed ball of the F8 father
        # would force at least (7-t5)+(8-t6) family codewords.
        assert 15 - free_missing > family_codeword_budget
    print(
        f"PASS family_split branch={branch} D=24 states={len(states)} "
        "q0_forces=noncodeword-F7+codeword-F8"
    )


def transform_word(word: int, permutation: tuple[int, ...]) -> int:
    return d24.transform_word(word, permutation)


def orbit_representatives(items, group, transform):
    remaining = set(items)
    result = []
    while remaining:
        representative = min(remaining)
        orbit = {transform(representative, permutation) for permutation in group}
        assert orbit <= remaining
        result.append(representative)
        remaining -= orbit
    return tuple(result)


def forced_vertices(mask: int) -> tuple[set[int], set[int]]:
    local_units = local_graph_assumptions(mask)
    forced_true = {literal - 1 for literal in local_units if literal > 0} | {0}
    forced_false = {-literal - 1 for literal in local_units if literal < 0}
    forced_false |= {1 << coordinate for coordinate in range(7)}
    forced_false |= {1 | (1 << coordinate) for coordinate in range(1, 7)}
    assert forced_true.isdisjoint(forced_false)
    return forced_true, forced_false


def candidate_couple_edges(mask: int) -> set[tuple[int, int]]:
    forced_true, forced_false = forced_vertices(mask)
    candidates = set()
    for first in range(128):
        for second in NEIGHBORS[first]:
            if second <= first or {first, second} & forced_false:
                continue
            outside = (set(NEIGHBORS[first]) - {second}) | (
                set(NEIGHBORS[second]) - {first}
            )
            if not outside & forced_true:
                candidates.add((first, second))
    return candidates


def couple_representatives(mask: int):
    group = d24.stabilizer(mask)

    def transform_edge(edge, permutation):
        return tuple(sorted(transform_word(word, permutation) for word in edge))

    return orbit_representatives(candidate_couple_edges(mask), group, transform_edge)


def couple_literals(first: int, second: int) -> list[int]:
    assert second in NEIGHBORS[first]
    literals = [first + 1, second + 1]
    literals += [
        -(neighbor + 1) for neighbor in NEIGHBORS[first] if neighbor != second
    ]
    literals += [
        -(neighbor + 1) for neighbor in NEIGHBORS[second] if neighbor != first
    ]
    assert len(literals) == len(set(literals)) == 14
    return literals


def wedge_words(mask: int) -> frozenset[int]:
    edges = d24.selected_edges(mask)
    result = set()
    for support in itertools.combinations(range(6), 3):
        if any(
            sum(
                tuple(sorted((coordinate, other))) in edges
                for other in support
                if other != coordinate
            )
            >= 2
            for coordinate in support
        ):
            result.add(sum(1 << (coordinate + 1) for coordinate in support))
    return frozenset(result)


def defect_six_local_cost(center: int, wedges: frozenset[int]) -> int:
    return len(wedges & ({center} | set(NEIGHBORS[center])))


def center_pair_data(mask: int):
    group = d24.stabilizer(mask)
    forced_true, forced_false = forced_vertices(mask)
    wedges = wedge_words(mask)
    f7_centers = {
        center
        for center in range(128)
        if center not in forced_true
        and not (set(NEIGHBORS[center]) & forced_false)
        and d24.center_cost(center, mask) is not None
        and d24.center_cost(center, mask) <= 1
    }
    f8_centers = {
        center
        for center in range(128)
        if not (({center} | set(NEIGHBORS[center])) & forced_false)
        and defect_six_local_cost(center, wedges) <= 1
    }
    pairs = {
        (f7_center, f8_center)
        for f7_center in f7_centers
        for f8_center in f8_centers
        if (f7_center ^ f8_center).bit_count() >= 5
        and d24.center_cost(f7_center, mask)
        + defect_six_local_cost(f8_center, wedges)
        <= 1
    }

    def transform_pair(pair, permutation):
        return tuple(transform_word(word, permutation) for word in pair)

    representatives = orbit_representatives(pairs, group, transform_pair)
    return f7_centers, f8_centers, pairs, representatives


def center_pair_literals(f7_center: int, f8_center: int) -> list[int]:
    assert (f7_center ^ f8_center).bit_count() >= 5
    literals = [-(f7_center + 1), f8_center + 1]
    literals += [neighbor + 1 for neighbor in NEIGHBORS[f7_center]]
    literals += [neighbor + 1 for neighbor in NEIGHBORS[f8_center]]
    assert len(literals) == len(set(literals)) == 16
    return literals


def selector_cases(branch: int, mask: int):
    assert tuple(sorted(wedge_words(mask))) == EXPECTED_WEDGE_WORDS[branch]
    couple_candidates = candidate_couple_edges(mask)
    couple_reps = couple_representatives(mask)
    f7_centers, f8_centers, center_pairs, center_reps = center_pair_data(mask)
    observed = (
        len(couple_candidates),
        len(couple_reps),
        len(f7_centers),
        len(f8_centers),
        len(center_pairs),
        len(center_reps),
    )
    assert observed == EXPECTED_ORBIT_COUNTS[branch]
    cases = tuple(
        (f"couple-{first}-{second}", couple_literals(first, second))
        for first, second in couple_reps
    ) + tuple(
        (f"centers-{first}-{second}", center_pair_literals(first, second))
        for first, second in center_reps
    )
    print(
        f"PASS orbit_split branch={branch} candidate_couples={observed[0]} "
        f"couple_orbits={observed[1]} center_pairs={observed[4]} "
        f"center_pair_orbits={observed[5]} total_cases={len(cases)}"
    )
    return cases


def build_common(branch: int, defect: int):
    assert branch in BRANCHES and defect in (24, 25)
    cnf = base_build(
        lex=False,
        structural=False,
        pair_bounds=False,
        dynamic_pair_bound=False,
    )
    nonisolated = add_nonisolated_variables(cnf)
    singletons = add_singleton_variables(cnf)
    code_edges = add_pair_indicators(cnf, 1)
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
    cnf.extend([[literal] for literal in local_graph_assumptions(MASKS[branch])])
    cnf.clauses[:] = [list(dict.fromkeys(clause)) for clause in cnf.clauses]
    return cnf


def build_d24_selector(branch: int):
    cnf = build_common(branch, 24)
    selectors = []
    for _, literals in selector_cases(branch, MASKS[branch]):
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
    payload = dimacs_bytes(cnf)
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

    cases = selector_cases(branch, MASKS[branch])
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
        f"PASS branch={branch} all_selector_cases=UNSAT "
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
        mask = MASKS[branch]
        verify_family_split(branch, mask)
        d25 = build_common(branch, 25)
        d24_selector = build_d24_selector(branch)
        report_formula(f"branch{branch}-d25", d25, output)
        report_formula(f"branch{branch}-d24-selector", d24_selector, output)
        if args.solve_kissat:
            solve_formula(f"branch{branch}-d25", d25)
            solve_formula(f"branch{branch}-d24-selector", d24_selector)
        if args.solve_incrementally:
            solve_incrementally(branch)


if __name__ == "__main__":
    main()
