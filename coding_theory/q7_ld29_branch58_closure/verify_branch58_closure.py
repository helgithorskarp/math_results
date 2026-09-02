#!/usr/bin/env python3
"""Verify the exact closure of Q7 locating-domination branch 58.

Generated CNFs are restricted to /scratch.  Proof traces and solver logs are
deliberately not version-controlled.
"""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import itertools
import pathlib
import sys
import time

from pysat.card import CardEnc, EncType


SOURCE_ROOT = pathlib.Path(__file__).resolve().parents[1]
D23_PATH = SOURCE_ROOT / "q7_ld29_branch58_d23" / "verify_branch58_d23.py"
SPLIT_PATH = SOURCE_ROOT / "q7_ld29_branch79_split" / "verify_branch79_split.py"
LOCAL_GRAPHS_PATH = SOURCE_ROOT / "q7_ld29_family_reduction" / "local_graphs.py"
SEARCH_PATH = SOURCE_ROOT / "q7_ld29_family_reduction" / "search_q7_ld29.py"
EXPECTED_SOURCE_HASHES = {
    D23_PATH: "c87ba037a3d0d1b7dcf08742201fed6b6511ae0c50b207fd34ced56891a34cec",
    SPLIT_PATH: "ea313ef366ad3b2da6c4e43d721aef8e96ec9bfa7dafe18c8fdade61c5fdd687",
    LOCAL_GRAPHS_PATH: "35d187198ed332f64551a174096168f101adff309e0dfaf6d94f9ba6d360e1f4",
    SEARCH_PATH: "3d4cc2bd966dbed2e4b585d3725dd37356487ad735eb008e55e730a7b9022614",
}
for source_path, expected_hash in EXPECTED_SOURCE_HASHES.items():
    assert hashlib.sha256(source_path.read_bytes()).hexdigest() == expected_hash

sys.path.insert(0, str(D23_PATH.parent))
sys.path.insert(0, str(SPLIT_PATH.parent))
sys.path.insert(0, str(LOCAL_GRAPHS_PATH.parent))

import verify_branch58_d23 as d23  # noqa: E402
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


BRANCH = 58
MASK = 2012
EXPECTED_STATE_DISTRIBUTION = {1: 1, 2: 2, 3: 5, 4: 12, 5: 29}
EXPECTED_D24_STATE_DISTRIBUTION = {0: 13, 1: 26, 2: 39, 3: 61, 4: 78, 5: 87}
EXPECTED_STABILIZER_ORDER = 8
EXPECTED_CANDIDATE_COUPLES = 202
EXPECTED_COUPLE_ORBITS = 51
EXPECTED_DENSE_PATTERNS = 526
EXPECTED_DENSE_PATTERN_ORBITS = 129
EXPECTED_FORMULAS = {
    "branch58-d25-plus": {
        "variables": 10432,
        "clauses": 183619,
        "bytes": 3433600,
        "sha256": "00827d7530b93aa91b7d399f3414d05b4c8cdf15e13405d228d21ea3d6441c99",
    },
    "branch58-d24-selector": {
        "variables": 11508,
        "clauses": 194262,
        "bytes": 3650639,
        "sha256": "9765f05b04dbaaa5b6265422174e051638b77688ff198a9853348c554703007c",
    },
    "branch58-d23-couple-selector": {
        "variables": 11379,
        "clauses": 193359,
        "bytes": 3638919,
        "sha256": "2857189787f7a40a2e023997c498f48fb955eb70b3af884e4a194b55c00ac48e",
    },
}
EDGES = tuple(itertools.combinations(range(6), 2))


def load_manifest() -> dict[str, dict[str, str]]:
    path = pathlib.Path(__file__).with_name("certificate_manifest.tsv")
    with path.open(newline="") as handle:
        rows = tuple(csv.DictReader(handle, delimiter="\t"))
    result = {row["formula"]: row for row in rows}
    assert len(rows) == len(result) == len(EXPECTED_FORMULAS) == 3
    assert set(result) == set(EXPECTED_FORMULAS)
    for name, expected in EXPECTED_FORMULAS.items():
        row = result[name]
        assert int(row["variables"]) == expected["variables"]
        assert int(row["clauses"]) == expected["clauses"]
        assert int(row["cnf_bytes"]) == expected["bytes"]
        assert row["cnf_sha256"] == expected["sha256"]
        assert int(row["original_total"]) == expected["clauses"]
        assert int(row["proof_bytes"]) > 0
        assert len(row["proof_sha256"]) == 64
        assert int(row["rat_core"]) == 0
    return result


MANIFEST = load_manifest()


def exact_d23_states():
    """Enumerate the capacity-feasible exact-D=23 family states."""
    raw = split.raw_states(MASK, 23)
    states = tuple(filter(split.survives_defect_six_occupancy, raw))
    distribution = Counter(state[0] for state in states)
    assert len(raw) == 88
    assert len(states) == 49
    assert dict(sorted(distribution.items())) == EXPECTED_STATE_DISTRIBUTION
    assert all(state[0] >= 1 for state in states)
    return states


def exact_d24_states():
    """Enumerate D=24 states and certify the couple-or-dense-center split."""
    raw = split.raw_states(MASK, 24)
    states = tuple(filter(split.survives_defect_six_occupancy, raw))
    distribution = Counter(state[0] for state in states)
    assert len(raw) == 314
    assert len(states) == 304
    assert dict(sorted(distribution.items())) == EXPECTED_D24_STATE_DISTRIBUTION
    for couples, extra, _, _ in states:
        # If there is no couple, some family has defect five or six.  Its
        # father has at least seven selected vertices in its closed ball.
        assert couples >= 1 or 5 in extra or 6 in extra
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


def forced_vertices() -> tuple[set[int], set[int]]:
    local_units = local_graph_assumptions(MASK)
    forced_true = {literal - 1 for literal in local_units if literal > 0} | {0}
    forced_false = {-literal - 1 for literal in local_units if literal < 0}
    forced_false |= {1 << coordinate for coordinate in range(7)}
    forced_false |= {1 | (1 << coordinate) for coordinate in range(1, 7)}
    assert forced_true.isdisjoint(forced_false)
    return forced_true, forced_false


def candidate_couple_edges() -> set[tuple[int, int]]:
    """Cube edges compatible with the units as induced code components."""
    forced_true, forced_false = forced_vertices()
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
    assert len(candidates) == EXPECTED_CANDIDATE_COUPLES
    return candidates


def edge_orbit_representatives() -> tuple[tuple[int, int], ...]:
    remaining = candidate_couple_edges()
    group = stabilizer(MASK)
    assert len(group) == EXPECTED_STABILIZER_ORDER
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
    assert len(representatives) == EXPECTED_COUPLE_ORBITS
    return tuple(representatives)


def candidate_dense_patterns() -> set[tuple[int, int]]:
    """Pairs (center, omitted) whose other seven ball vertices may be selected."""
    _, forced_false = forced_vertices()
    candidates: set[tuple[int, int]] = set()
    for center in range(128):
        ball = {center, *NEIGHBORS[center]}
        for omitted in ball:
            if not (ball - {omitted}) & forced_false:
                candidates.add((center, omitted))
    assert len(candidates) == EXPECTED_DENSE_PATTERNS
    return candidates


def dense_pattern_orbit_representatives() -> tuple[tuple[int, int], ...]:
    remaining = candidate_dense_patterns()
    group = stabilizer(MASK)
    representatives: list[tuple[int, int]] = []
    while remaining:
        center, omitted = min(remaining)
        orbit = {
            (
                transform_word(center, permutation),
                transform_word(omitted, permutation),
            )
            for permutation in group
        }
        assert orbit <= remaining
        representatives.append((center, omitted))
        remaining -= orbit
    assert len(representatives) == EXPECTED_DENSE_PATTERN_ORBITS
    return tuple(representatives)


def couple_literals(first: int, second: int) -> list[int]:
    """Literals saying {first,second} is an induced two-codeword component."""
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


def dense_pattern_literals(center: int, omitted: int) -> list[int]:
    """Seven positive literals in N[center] other than the omitted vertex."""
    ball = {center, *NEIGHBORS[center]}
    assert omitted in ball and len(ball) == 8
    literals = [vertex + 1 for vertex in sorted(ball - {omitted})]
    assert len(literals) == len(set(literals)) == 7
    return literals


def add_common_indicators(cnf):
    nonisolated = add_nonisolated_variables(cnf)
    singletons = add_singleton_variables(cnf)
    code_edges = add_pair_indicators(cnf, 1)
    return nonisolated, singletons, code_edges


def add_common_units(cnf) -> None:
    representatives = local_graph_representatives()
    assert len(representatives) == 115
    assert representatives[BRANCH] == MASK
    cnf.extend([[literal] for literal in local_graph_assumptions(MASK)])
    cnf.clauses[:] = [list(dict.fromkeys(clause)) for clause in cnf.clauses]


def build_d25_plus_formula():
    """Necessary locating-domination constraints for total defect D>=25."""
    cnf = base_build(
        lex=False,
        structural=False,
        pair_bounds=False,
        dynamic_pair_bound=False,
    )
    nonisolated, singletons, code_edges = add_common_indicators(cnf)
    # D>=25 gives p>=49, b<=9, p+b<=58 and e(C)<=E_7(9)=13.
    cnf.extend(
        CardEnc.atleast(
            lits=singletons,
            bound=49,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend(
        CardEnc.atmost(
            lits=nonisolated,
            bound=9,
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
            bound=13,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    add_common_units(cnf)
    return cnf


def build_exact_d23_base():
    """Necessary exact-D=23 constraints before selecting a couple orbit."""
    cnf = base_build(
        lex=False,
        structural=False,
        pair_bounds=False,
        dynamic_pair_bound=False,
    )
    nonisolated, singletons, code_edges = add_common_indicators(cnf)
    # D=23 gives p=47, b<=11, p+b<=58 and e(C)<=E_7(11)=17.
    cnf.extend(
        CardEnc.equals(
            lits=singletons,
            bound=47,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend(
        CardEnc.atmost(
            lits=nonisolated,
            bound=11,
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
            bound=17,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    add_common_units(cnf)
    return cnf


def build_exact_d24_base():
    """Necessary exact-D=24 constraints before the structural disjunction."""
    cnf = base_build(
        lex=False,
        structural=False,
        pair_bounds=False,
        dynamic_pair_bound=False,
    )
    nonisolated, singletons, code_edges = add_common_indicators(cnf)
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
    add_common_units(cnf)
    return cnf


def build_d23_selector_formula():
    cnf = build_exact_d23_base()
    representatives = edge_orbit_representatives()
    selectors: list[int] = []
    for first, second in representatives:
        selector = cnf.nv + 1
        selectors.append(selector)
        for literal in couple_literals(first, second):
            cnf.append([-selector, literal])
    cnf.append(selectors)
    return cnf, representatives


def build_d24_selector_formula():
    """Select a couple, or a seven-of-eight closed ball in the q=0 states."""
    cnf = build_exact_d24_base()
    couple_representatives = edge_orbit_representatives()
    dense_representatives = dense_pattern_orbit_representatives()
    selectors: list[int] = []
    for first, second in couple_representatives:
        selector = cnf.nv + 1
        selectors.append(selector)
        for literal in couple_literals(first, second):
            cnf.append([-selector, literal])
    for center, omitted in dense_representatives:
        selector = cnf.nv + 1
        selectors.append(selector)
        for literal in dense_pattern_literals(center, omitted):
            cnf.append([-selector, literal])
    cnf.append(selectors)
    return cnf, couple_representatives, dense_representatives


def scratch_directory(raw: str) -> pathlib.Path:
    path = pathlib.Path(raw).resolve()
    if not path.is_relative_to("/scratch"):
        raise ValueError("CNF output must remain under /scratch")
    path.mkdir(parents=True, exist_ok=True)
    return path


def report_formula(name: str, cnf, output: pathlib.Path | None) -> None:
    payload = dimacs_bytes(cnf)
    digest = hashlib.sha256(payload).hexdigest()
    expected = EXPECTED_FORMULAS[name]
    row = MANIFEST[name]
    assert cnf.nv == expected["variables"]
    assert len(cnf.clauses) == expected["clauses"]
    assert len(payload) == expected["bytes"]
    assert digest == expected["sha256"]
    assert str(cnf.nv) == row["variables"]
    assert str(len(cnf.clauses)) == row["clauses"]
    assert str(len(payload)) == row["cnf_bytes"]
    assert digest == row["cnf_sha256"]
    if output is not None:
        (output / f"{name}.cnf").write_bytes(payload)
    print(
        f"PASS formula={name} variables={cnf.nv} clauses={len(cnf.clauses)} "
        f"bytes={len(payload)} sha256={digest}",
        flush=True,
    )


def solve_formula(name: str, cnf) -> None:
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


def solve_incrementally(cnf, representatives) -> None:
    """Cross-check every couple representative as a separate assumption set."""
    from pysat.solvers import Solver

    started = time.monotonic()
    with Solver(name="cadical195", bootstrap_with=cnf.clauses) as solver:
        for index, edge in enumerate(representatives, 1):
            case_started = time.monotonic()
            satisfiable = solver.solve(assumptions=couple_literals(*edge))
            print(
                f"CASE {index}/{len(representatives)} edge={edge} "
                f"result={'SAT' if satisfiable else 'UNSAT'} "
                f"seconds={time.monotonic() - case_started:.3f}",
                flush=True,
            )
            if satisfiable:
                raise AssertionError(f"unexpected satisfying couple orbit {edge}")
    print(
        f"PASS all {len(representatives)} couple orbits independently UNSAT "
        f"seconds={time.monotonic() - started:.3f}",
        flush=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-directory")
    parser.add_argument("--solve-kissat", action="store_true")
    parser.add_argument("--solve-incrementally", action="store_true")
    args = parser.parse_args()
    output = scratch_directory(args.write_directory) if args.write_directory else None

    assert d23.BRANCH == BRANCH and d23.MASK == MASK
    assert d23.ladder.edge_isoperimetric_table(7)[9:12] == [13, 15, 17]
    states = exact_d23_states()
    d24_states = exact_d24_states()
    representatives = edge_orbit_representatives()
    dense_representatives = dense_pattern_orbit_representatives()
    print(
        f"PASS analytic branch={BRANCH} exact_D23_states={len(states)} "
        f"couple_distribution={EXPECTED_STATE_DISTRIBUTION} q>=1 "
        f"candidate_couples={EXPECTED_CANDIDATE_COUPLES} "
        f"stabilizer={EXPECTED_STABILIZER_ORDER} orbits={len(representatives)}",
        flush=True,
    )
    print(
        f"PASS analytic branch={BRANCH} exact_D24_states={len(d24_states)} "
        f"couple_distribution={EXPECTED_D24_STATE_DISTRIBUTION} "
        f"dense_patterns={EXPECTED_DENSE_PATTERNS} "
        f"dense_orbits={len(dense_representatives)}",
        flush=True,
    )

    d25_plus = build_d25_plus_formula()
    report_formula("branch58-d25-plus", d25_plus, output)
    d24_selector, d24_couples, d24_dense = build_d24_selector_formula()
    assert d24_couples == representatives
    assert d24_dense == dense_representatives
    report_formula("branch58-d24-selector", d24_selector, output)
    d23_selector, selector_representatives = build_d23_selector_formula()
    assert selector_representatives == representatives
    report_formula("branch58-d23-couple-selector", d23_selector, output)

    if args.solve_kissat:
        solve_formula("branch58-d25-plus", d25_plus)
        solve_formula("branch58-d24-selector", d24_selector)
        solve_formula("branch58-d23-couple-selector", d23_selector)
    if args.solve_incrementally:
        solve_incrementally(build_exact_d23_base(), representatives)


if __name__ == "__main__":
    main()
