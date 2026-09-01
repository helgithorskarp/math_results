#!/usr/bin/env python3
"""Verify the family split and build the two certificates closing branch 50.

Generated CNFs, solver traces, and logs are deliberately restricted to
/scratch.  Only this deterministic source and the compact certificate
manifest belong in version control.
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


BRANCH = 50
MASK = 957
EXPECTED_Q0_STATES = (
    (0, (1, 1, 1, 5, 6), 1, 10),
    (0, (1, 2, 5, 6), 0, 10),
    (0, (3, 5, 6), 0, 10),
)
EXPECTED_WEDGE_WORDS = (14, 22, 26, 28, 38, 44, 50, 70, 76, 82, 98, 100)
EXPECTED_COUPLE_REPRESENTATIVES = (
    (6, 7),
    (11, 15),
    (11, 27),
    (11, 43),
    (12, 13),
    (15, 31),
    (15, 47),
    (24, 25),
    (24, 56),
    (27, 31),
    (27, 59),
    (30, 31),
    (30, 62),
    (31, 63),
    (34, 35),
    (34, 42),
    (39, 47),
    (39, 103),
    (41, 43),
    (41, 45),
    (41, 57),
    (41, 105),
    (43, 47),
    (43, 59),
    (43, 107),
    (45, 47),
    (45, 61),
    (45, 109),
    (46, 47),
    (46, 62),
    (46, 110),
    (47, 63),
    (47, 111),
    (57, 59),
    (57, 121),
    (58, 59),
    (58, 62),
    (58, 122),
    (59, 63),
    (59, 123),
    (62, 63),
    (62, 126),
    (63, 127),
    (97, 99),
    (97, 105),
    (99, 103),
    (99, 107),
    (99, 115),
    (102, 103),
    (102, 110),
    (103, 111),
    (104, 105),
    (104, 106),
    (104, 108),
    (104, 120),
    (105, 107),
    (105, 109),
    (105, 121),
    (106, 107),
    (106, 110),
    (106, 122),
    (107, 111),
    (107, 123),
    (108, 109),
    (108, 110),
    (108, 124),
    (109, 111),
    (109, 125),
    (110, 111),
    (110, 126),
    (111, 127),
    (120, 121),
    (120, 122),
    (121, 123),
    (122, 123),
    (122, 126),
    (123, 127),
    (126, 127),
)
EXPECTED_CENTER_PAIR_REPRESENTATIVES = (
    (38, 57),
    (38, 75),
    (38, 89),
    (38, 91),
    (38, 95),
    (38, 105),
    (38, 120),
    (38, 121),
    (38, 123),
    (43, 85),
    (43, 87),
    (43, 93),
    (43, 94),
    (43, 117),
    (43, 118),
    (43, 124),
    (57, 79),
    (57, 94),
    (57, 103),
    (57, 110),
    (63, 70),
    (105, 23),
    (105, 31),
    (105, 38),
    (105, 55),
    (105, 62),
    (105, 118),
    (120, 31),
    (120, 47),
    (120, 103),
    (123, 38),
)


def load_manifest() -> dict[str, dict[str, str]]:
    path = pathlib.Path(__file__).with_name("certificate_manifest.tsv")
    with path.open(newline="") as handle:
        rows = tuple(csv.DictReader(handle, delimiter="\t"))
    result = {row["formula"]: row for row in rows}
    assert len(rows) == len(result) == 2
    assert set(result) == {"branch50-d25", "branch50-d24-selector"}
    return result


MANIFEST = load_manifest()


def survives_defect_six_occupancy(state) -> bool:
    _, extra, free_missing, family_codeword_budget = state
    forced_family_codewords = max(0, 8 * extra.count(6) - free_missing)
    return forced_family_codewords <= family_codeword_budget


def verify_family_split() -> None:
    assert local_graph_representatives()[BRANCH] == MASK
    assert d24.MASKS[BRANCH] == MASK
    assert len(d24.stabilizer(MASK)) == 4
    states = tuple(filter(survives_defect_six_occupancy, d24.raw_states(MASK, 24)))
    q0_states = tuple(state for state in states if state[0] == 0)
    assert q0_states == EXPECTED_Q0_STATES
    for couples, extra, free_missing, family_codeword_budget in q0_states:
        assert couples == 0
        assert extra.count(5) == extra.count(6) == 1
        assert free_missing <= 1
        # If the defect-five father were a codeword, its family and the
        # defect-six family would force at least 7-t5 and 8-t6 family
        # codewords.  Since t5+t6 <= free_missing, this exceeds the budget.
        assert 15 - free_missing > family_codeword_budget
    print(
        f"PASS family_split branch={BRANCH} D=24 states={len(states)} "
        f"q0_states={q0_states} q0_forces=noncodeword-F7+codeword-F8"
    )


def selected_edges() -> frozenset[tuple[int, int]]:
    return d24.selected_edges(MASK)


def transform_word(word: int, permutation: tuple[int, ...]) -> int:
    return d24.transform_word(word, permutation)


def orbit_representatives(items, transform):
    remaining = set(items)
    result = []
    group = d24.stabilizer(MASK)
    while remaining:
        representative = min(remaining)
        orbit = {transform(representative, permutation) for permutation in group}
        assert orbit <= remaining
        result.append(representative)
        remaining -= orbit
    return tuple(result)


def forced_vertices() -> tuple[set[int], set[int]]:
    local_units = local_graph_assumptions(MASK)
    forced_true = {literal - 1 for literal in local_units if literal > 0} | {0}
    forced_false = {-literal - 1 for literal in local_units if literal < 0}
    forced_false |= {1 << coordinate for coordinate in range(7)}
    forced_false |= {1 | (1 << coordinate) for coordinate in range(1, 7)}
    assert forced_true.isdisjoint(forced_false)
    return forced_true, forced_false


def candidate_couple_edges() -> set[tuple[int, int]]:
    forced_true, forced_false = forced_vertices()
    candidates = set()
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
    assert len(candidates) == 204
    return candidates


def couple_representatives() -> tuple[tuple[int, int], ...]:
    def transform_edge(edge, permutation):
        return tuple(sorted(transform_word(word, permutation) for word in edge))

    representatives = orbit_representatives(candidate_couple_edges(), transform_edge)
    assert representatives == EXPECTED_COUPLE_REPRESENTATIVES
    return representatives


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


def wedge_words() -> frozenset[int]:
    edges = selected_edges()
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
    assert tuple(sorted(result)) == EXPECTED_WEDGE_WORDS
    return frozenset(result)


WEDGE_WORDS = wedge_words()


def defect_six_local_cost(center: int) -> int:
    return len(WEDGE_WORDS & ({center} | set(NEIGHBORS[center])))


def center_pair_representatives() -> tuple[tuple[int, int], ...]:
    forced_true, forced_false = forced_vertices()
    f7_centers = {
        center
        for center in range(128)
        if center not in forced_true
        and not (set(NEIGHBORS[center]) & forced_false)
        and d24.center_cost(center, MASK) is not None
        and d24.center_cost(center, MASK) <= 1
    }
    f8_centers = {
        center
        for center in range(128)
        if not (({center} | set(NEIGHBORS[center])) & forced_false)
        and defect_six_local_cost(center) <= 1
    }
    pairs = {
        (f7_center, f8_center)
        for f7_center in f7_centers
        for f8_center in f8_centers
        if (f7_center ^ f8_center).bit_count() >= 5
        and d24.center_cost(f7_center, MASK)
        + defect_six_local_cost(f8_center)
        <= 1
    }

    def transform_pair(pair, permutation):
        return tuple(transform_word(word, permutation) for word in pair)

    representatives = orbit_representatives(pairs, transform_pair)
    assert len(pairs) == 96
    assert representatives == EXPECTED_CENTER_PAIR_REPRESENTATIVES
    return representatives


def center_pair_literals(f7_center: int, f8_center: int) -> list[int]:
    assert (f7_center ^ f8_center).bit_count() >= 5
    literals = [-(f7_center + 1), f8_center + 1]
    literals += [neighbor + 1 for neighbor in NEIGHBORS[f7_center]]
    literals += [neighbor + 1 for neighbor in NEIGHBORS[f8_center]]
    assert len(literals) == len(set(literals)) == 16
    return literals


def selector_cases() -> tuple[tuple[str, list[int]], ...]:
    cases = tuple(
        (f"couple-{first}-{second}", couple_literals(first, second))
        for first, second in couple_representatives()
    ) + tuple(
        (f"centers-{first}-{second}", center_pair_literals(first, second))
        for first, second in center_pair_representatives()
    )
    assert len(cases) == 109
    print(
        f"PASS orbit_split candidate_couples=204 couple_orbits=78 "
        f"center_pairs=96 center_pair_orbits=31 total_cases={len(cases)}"
    )
    return cases


def build_common(defect: int):
    assert defect in (24, 25)
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
    cnf.extend([[literal] for literal in local_graph_assumptions(MASK)])
    cnf.clauses[:] = [list(dict.fromkeys(clause)) for clause in cnf.clauses]
    return cnf


def build_d25():
    return build_common(25)


def build_d24_selector():
    cnf = build_common(24)
    selectors = []
    for _, literals in selector_cases():
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


def check_formula(name: str, cnf, output: pathlib.Path | None) -> None:
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


def solve_formula(name: str, cnf, solver_name: str) -> None:
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


def solve_incrementally(cnf) -> None:
    from pysat.solvers import Solver

    cases = selector_cases()
    started = time.monotonic()
    with Solver(name="cadical195", bootstrap_with=cnf.clauses) as solver:
        for index, (name, assumptions) in enumerate(cases, 1):
            case_started = time.monotonic()
            satisfiable = solver.solve(assumptions=assumptions)
            print(
                f"CASE {index}/{len(cases)} {name} "
                f"result={'SAT' if satisfiable else 'UNSAT'} "
                f"seconds={time.monotonic() - case_started:.3f}",
                flush=True,
            )
            if satisfiable:
                raise AssertionError(f"unexpected satisfying selector case {name}")
    print(
        f"PASS all_selector_cases=UNSAT seconds={time.monotonic()-started:.3f}",
        flush=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-directory")
    parser.add_argument("--solve-kissat", action="store_true")
    parser.add_argument("--solve-incrementally", action="store_true")
    args = parser.parse_args()
    output = scratch_directory(args.write_directory) if args.write_directory else None

    verify_family_split()
    d25 = build_d25()
    d24_selector = build_d24_selector()
    check_formula("branch50-d25", d25, output)
    check_formula("branch50-d24-selector", d24_selector, output)
    if args.solve_kissat:
        solve_formula("branch50-d25", d25, "kissat404")
        solve_formula("branch50-d24-selector", d24_selector, "kissat404")
    if args.solve_incrementally:
        solve_incrementally(build_common(24))


if __name__ == "__main__":
    main()
