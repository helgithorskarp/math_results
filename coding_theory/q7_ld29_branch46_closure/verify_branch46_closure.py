#!/usr/bin/env python3
"""Verify the analytic split and reconstruct the branch-46 closure CNFs."""

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
COUPLE_PATH = (
    SOURCE_ROOT
    / "q7_ld29_minimal_defect_couples"
    / "verify_minimal_defect_couples.py"
)
SIBLING_PATH = (
    SOURCE_ROOT
    / "q7_ld29_branches44_47_52_57_closure"
    / "verify_sibling_closures.py"
)
EXPECTED_SOURCE_HASHES = {
    COUPLE_PATH: "a0200279d73eb139a04ea0be45ad94b4cd40651ae2847223abb8c8bd718d52ee",
    SIBLING_PATH: "1069616e39ad4c39e46d0094f91c6e2a9efc13983229033add53cf5551ac4fe6",
}
for source_path, expected_hash in EXPECTED_SOURCE_HASHES.items():
    assert hashlib.sha256(source_path.read_bytes()).hexdigest() == expected_hash
sys.path.insert(0, str(COUPLE_PATH.parent))
sys.path.insert(0, str(SIBLING_PATH.parent))

import verify_minimal_defect_couples as couple  # noqa: E402
import verify_sibling_closures as sibling  # noqa: E402


BRANCH = 46
MASK = 763
EXPECTED_D23_CENTERS = (
    14,
    28,
    38,
    51,
    57,
    63,
    77,
    83,
    85,
    89,
    95,
    101,
    105,
    111,
    113,
    119,
    120,
    123,
    125,
    126,
    127,
)
EXPECTED_D23_DISTRIBUTION = {4: 1, 5: 6}
EXPECTED_D24_DISTRIBUTION = {0: 1, 1: 6, 2: 10, 3: 18, 4: 38, 5: 58}
EXPECTED_Q0_D24 = ((0, (1, 1, 1, 5, 6), 0, 10),)
EXPECTED_D24_COUNTS = {
    "couple_candidates": 205,
    "couple_orbits": 205,
    "f7_centers": 10,
    "f8_centers": 39,
    "center_pairs": 12,
    "center_pair_orbits": 12,
}


def load_manifest() -> dict[str, dict[str, str]]:
    path = pathlib.Path(__file__).with_name("certificate_manifest.tsv")
    with path.open(newline="") as handle:
        rows = tuple(csv.DictReader(handle, delimiter="\t"))
    result = {row["formula"]: row for row in rows}
    expected = {
        "branch46-d23-q4-center-selector",
        "branch46-d24-cover",
        "branch46-d25",
    }
    assert len(rows) == len(result) == len(expected) == 3
    assert set(result) == expected
    for row in rows:
        assert int(row["variables"]) > 0
        assert int(row["clauses"]) == int(row["original_total"])
        assert int(row["cnf_bytes"]) > 0 and int(row["proof_bytes"]) > 0
        assert len(row["cnf_sha256"]) == len(row["proof_sha256"]) == 64
        assert int(row["rat_core"]) == 0
    return result


MANIFEST = load_manifest()


def detailed_states(defect: int):
    local_defect, local_capacity, forced_deficit = couple.local_data(MASK)
    result = []
    for q, extra in couple.states(MASK, defect):
        family_vertices = 104 - defect - 2 * q
        total_capacity = local_capacity + sum(couple.FAMILY_CAPACITY[d] for d in extra)
        free_missing = total_capacity - family_vertices - forced_deficit
        family_codeword_budget = 34 - defect - 2 * q
        result.append((q, extra, free_missing, family_codeword_budget))
    return tuple(result)


def d23_centers() -> tuple[int, ...]:
    candidates = {
        center
        for center in range(128)
        if sibling.d24.center_cost(center, MASK) is not None
        and sibling.d24.center_cost(center, MASK) <= 1
    }
    return sibling.orbit_representatives(
        candidates,
        sibling.d24.stabilizer(MASK),
        sibling.transform_word,
    )


def verify_d23_split() -> None:
    states = detailed_states(23)
    distribution = dict(sorted(collections.Counter(state[0] for state in states).items()))
    assert len(states) == 7
    assert distribution == EXPECTED_D23_DISTRIBUTION
    for q, extra, free_missing, family_codeword_budget in states:
        f7_count = extra.count(5)
        assert q >= 4 and f7_count >= 1
        # Even assigning every free missing slot to one F7 family, a selected
        # father would force too many family codewords.  Thus all F7 fathers
        # are noncodewords with seven selected neighbors.
        assert 7 - free_missing > family_codeword_budget
        # The residual local costs of all F7 centers sum to at most
        # free_missing, so one center has cost at most one.
        assert free_missing < 2 * f7_count
    centers = d23_centers()
    assert centers == EXPECTED_D23_CENTERS
    print(
        f"PASS D23 states={len(states)} q_distribution={distribution} "
        f"center_orbits={centers}"
    )


def zero_slack_center_data():
    group = sibling.d24.stabilizer(MASK)
    forced_true, forced_false = sibling.forced_vertices(MASK)
    wedges = sibling.wedge_words(MASK)
    f7_centers = {
        center
        for center in range(128)
        if center not in forced_true
        and not (set(sibling.NEIGHBORS[center]) & forced_false)
        and sibling.d24.center_cost(center, MASK) == 0
    }
    f8_centers = {
        center
        for center in range(128)
        if not (({center} | set(sibling.NEIGHBORS[center])) & forced_false)
        and sibling.defect_six_local_cost(center, wedges) == 0
    }
    pairs = {
        (f7_center, f8_center)
        for f7_center in f7_centers
        for f8_center in f8_centers
        if (f7_center ^ f8_center).bit_count() >= 5
    }
    representatives = sibling.orbit_representatives(
        pairs,
        group,
        lambda pair, permutation: tuple(
            sibling.transform_word(word, permutation) for word in pair
        ),
    )
    return f7_centers, f8_centers, pairs, representatives


def verify_d24_split() -> None:
    states = detailed_states(24)
    distribution = dict(sorted(collections.Counter(state[0] for state in states).items()))
    assert len(states) == 131
    assert distribution == EXPECTED_D24_DISTRIBUTION
    q0_states = tuple(state for state in states if state[0] == 0)
    assert q0_states == EXPECTED_Q0_D24
    # The q=0 state has one full F7 and one full F8 family.  The F8 father is
    # selected with its full closed ball selected.  A selected F7 father would
    # force 7+8>10 family codewords, so the F7 father is a noncodeword with
    # all seven neighbors selected.  Zero slack forces both local costs zero.
    assert 7 + 8 > q0_states[0][3]
    candidates = sibling.candidate_couple_edges(MASK)
    couple_reps = sibling.couple_representatives(MASK)
    f7_centers, f8_centers, center_pairs, center_reps = zero_slack_center_data()
    observed = {
        "couple_candidates": len(candidates),
        "couple_orbits": len(couple_reps),
        "f7_centers": len(f7_centers),
        "f8_centers": len(f8_centers),
        "center_pairs": len(center_pairs),
        "center_pair_orbits": len(center_reps),
    }
    assert observed == EXPECTED_D24_COUNTS
    assert len(sibling.d24.stabilizer(MASK)) == 1
    print(
        f"PASS D24 states={len(states)} q_distribution={distribution} "
        f"cover_counts={observed}"
    )


def build_common(defect: int, *, exact: bool):
    assert defect in (23, 24, 25)
    cnf = sibling.base_build(
        lex=False,
        structural=False,
        pair_bounds=False,
        dynamic_pair_bound=False,
    )
    nonisolated = sibling.add_nonisolated_variables(cnf)
    singletons = sibling.add_singleton_variables(cnf)
    code_edges = sibling.add_pair_indicators(cnf, 1)
    cnf.extend(
        CardEnc.atmost(
            lits=nonisolated,
            bound=34 - defect,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    singleton_encoder = CardEnc.equals if exact else CardEnc.atleast
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
            lits=[*nonisolated, *singletons],
            bound=58,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend(
        CardEnc.atmost(
            lits=code_edges,
            bound={23: 17, 24: 15, 25: 13}[defect],
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend(
        [[literal] for literal in sibling.local_graph_assumptions(MASK)]
    )
    return cnf


def add_couple_lower_bound(cnf, minimum: int) -> int:
    indicators = []
    for first, second in sorted(sibling.candidate_couple_edges(MASK)):
        literals = sibling.couple_literals(first, second)
        indicator = cnf.nv + 1
        indicators.append(indicator)
        for literal in literals:
            cnf.append([-indicator, literal])
        cnf.append([indicator, *[-literal for literal in literals]])
    cnf.extend(
        CardEnc.atleast(
            lits=indicators,
            bound=minimum,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    return len(indicators)


def add_selector_cases(cnf, cases) -> None:
    selectors = []
    for literals in cases:
        selector = cnf.nv + 1
        selectors.append(selector)
        for literal in literals:
            cnf.append([-selector, literal])
    cnf.append(selectors)


def build_d23():
    cnf = build_common(23, exact=True)
    assert add_couple_lower_bound(cnf, 4) == 205
    cases = [
        [-(center + 1), *[neighbor + 1 for neighbor in sibling.NEIGHBORS[center]]]
        for center in d23_centers()
    ]
    add_selector_cases(cnf, cases)
    cnf.clauses[:] = [list(dict.fromkeys(clause)) for clause in cnf.clauses]
    return cnf


def build_d24():
    cnf = build_common(24, exact=True)
    couple_cases = [
        sibling.couple_literals(first, second)
        for first, second in sibling.couple_representatives(MASK)
    ]
    *_, center_reps = zero_slack_center_data()
    center_cases = [
        sibling.center_pair_literals(first, second)
        for first, second in center_reps
    ]
    add_selector_cases(cnf, [*couple_cases, *center_cases])
    cnf.clauses[:] = [list(dict.fromkeys(clause)) for clause in cnf.clauses]
    return cnf


def build_d25():
    cnf = build_common(25, exact=False)
    cnf.clauses[:] = [list(dict.fromkeys(clause)) for clause in cnf.clauses]
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


def solve_formula(name: str, cnf) -> None:
    from pysat.solvers import Solver

    started = time.monotonic()
    with Solver(name="kissat404", bootstrap_with=cnf.clauses) as solver:
        satisfiable = solver.solve()
    print(
        f"SOLVE formula={name} solver=kissat404 "
        f"result={'SAT' if satisfiable else 'UNSAT'} "
        f"seconds={time.monotonic() - started:.3f}",
        flush=True,
    )
    if satisfiable:
        raise AssertionError(f"unexpected satisfying formula {name}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-directory")
    parser.add_argument("--solve-kissat", action="store_true")
    args = parser.parse_args()
    output = scratch_directory(args.write_directory) if args.write_directory else None

    assert sibling.local_graph_representatives()[BRANCH] == MASK
    verify_d23_split()
    verify_d24_split()
    formulas = {
        "branch46-d23-q4-center-selector": build_d23(),
        "branch46-d24-cover": build_d24(),
        "branch46-d25": build_d25(),
    }
    for name, cnf in formulas.items():
        report_formula(name, cnf, output)
        if args.solve_kissat:
            solve_formula(name, cnf)
    print("PASS aggregate formulas exclude branch 46; 50 normalized branches remain")


if __name__ == "__main__":
    main()
