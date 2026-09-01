#!/usr/bin/env python3
"""Verify the center split raising Q7 LD29 branch 58 to defect at least 23."""

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
LOCAL_GRAPHS_PATH = SOURCE_ROOT / "q7_ld29_family_reduction" / "local_graphs.py"
SEARCH_PATH = SOURCE_ROOT / "q7_ld29_family_reduction" / "search_q7_ld29.py"
EXPECTED_SOURCE_HASHES = {
    LADDER_PATH: "acde98fb29c8673d57ceddc47b36e5b46a62a0cfa13ed542886e96fbaf0c4852",
    LOCAL_GRAPHS_PATH: "35d187198ed332f64551a174096168f101adff309e0dfaf6d94f9ba6d360e1f4",
    SEARCH_PATH: "3d4cc2bd966dbed2e4b585d3725dd37356487ad735eb008e55e730a7b9022614",
}
for source_path, expected_hash in EXPECTED_SOURCE_HASHES.items():
    assert hashlib.sha256(source_path.read_bytes()).hexdigest() == expected_hash

sys.path.insert(0, str(LADDER_PATH.parent))
sys.path.insert(0, str(LOCAL_GRAPHS_PATH.parent))

import verify_lower_frontier_bounds as ladder  # noqa: E402
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
EXPECTED_LOCAL_DATA = ((2, 2, 3, 3, 3, 3), 0, 10, 36, 16)
EXPECTED_STABILIZER_ORDER = 8
EXPECTED_D22_STATES = (
    (5, (1, 1, 5, 5), 0, 2),
    (6, (1, 1, 1, 1, 1, 1, 1, 5), 0, 0),
    (6, (1, 1, 1, 4, 5), 0, 0),
    (6, (1, 1, 5, 5), 2, 0),
    (6, (2, 5, 5), 1, 0),
)
EXPECTED_CENTER_REPRESENTATIVES = (15, 63, 75, 95, 126, 127)
COORDINATES = tuple(range(6))
EDGES = tuple(itertools.combinations(COORDINATES, 2))
EXPECTED_VARIABLES = 10432
EXPECTED_CLAUSES = 183627


def load_manifest() -> dict[str, dict[str, str]]:
    path = pathlib.Path(__file__).with_name("certificate_manifest.tsv")
    with path.open(newline="") as handle:
        rows = tuple(csv.DictReader(handle, delimiter="\t"))
    result = {row["formula"]: row for row in rows}
    expected = {
        f"branch58-d22-center{center}" for center in EXPECTED_CENTER_REPRESENTATIVES
    }
    assert len(rows) == len(result) == len(expected) == 6
    assert set(result) == expected
    return result


MANIFEST = load_manifest()


def selected_edges(mask: int) -> frozenset[tuple[int, int]]:
    return frozenset(edge for index, edge in enumerate(EDGES) if mask >> index & 1)


def transform_word(word: int, permutation: tuple[int, ...]) -> int:
    result = word & 1
    for coordinate in COORDINATES:
        if word & (1 << (coordinate + 1)):
            result |= 1 << (permutation[coordinate] + 1)
    return result


def stabilizer(mask: int) -> tuple[tuple[int, ...], ...]:
    edges = selected_edges(mask)
    return tuple(
        permutation
        for permutation in itertools.permutations(COORDINATES)
        if {
            tuple(sorted((permutation[first], permutation[second])))
            for first, second in edges
        }
        == edges
    )


def surviving_d22_states(mask: int):
    degrees, triangles, local_defect, local_capacity, forced_deficit = ladder.local_data(mask)
    assert (degrees, triangles, local_defect, local_capacity, forced_deficit) == EXPECTED_LOCAL_DATA
    result = []
    total_defect = 22
    for couples in range((34 - total_defect) // 2 + 1):
        family_vertices = 104 - total_defect - 2 * couples
        family_budget = 34 - total_defect - 2 * couples
        for extra in ladder.defect_partitions(total_defect - local_defect):
            capacity = local_capacity + sum(ladder.FAMILY_CAPACITY[d] for d in extra)
            free_missing = capacity - family_vertices - forced_deficit
            if free_missing < 0:
                continue
            if ladder.arithmetic_state_survives(
                total_defect,
                couples,
                extra,
                local_defect,
                local_capacity,
                forced_deficit,
            ):
                result.append((couples, extra, free_missing, family_budget))
    return tuple(result)


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
        nonorphan_support = tuple(
            index - 1 for index in range(1, 7) if center & (1 << index)
        )
        assert len(nonorphan_support) >= 4
        assert any(edge in edges for edge in itertools.combinations(nonorphan_support, 2))
        return 3
    return 0


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


def verify_split() -> tuple[int, ...]:
    representatives = local_graph_representatives()
    assert len(representatives) == 115
    assert representatives[BRANCH] == MASK
    assert MASK.bit_count() == 8
    assert ladder.method_bound(MASK) == 22
    assert ladder.local_data(MASK) == EXPECTED_LOCAL_DATA
    assert len(stabilizer(MASK)) == EXPECTED_STABILIZER_ORDER

    states = surviving_d22_states(MASK)
    assert states == EXPECTED_D22_STATES
    for _, extra, free_missing, family_budget in states:
        defect_five_fathers = extra.count(5)
        assert defect_five_fathers >= 1
        # Even assigning every free missing slot to one selected F7 family
        # would leave more forced family codewords than the global budget.
        assert 7 - free_missing > family_budget
        # The residual costs of the noncodeword F7 centers sum to at most
        # free_missing, so at least one has cost at most one.
        assert free_missing < 2 * defect_five_fathers

    centers = center_orbit_representatives(MASK)
    assert centers == EXPECTED_CENTER_REPRESENTATIVES
    edge_table = ladder.edge_isoperimetric_table(7)
    assert edge_table[12] == 20 and edge_table[11] == 17
    print(
        f"PASS branch={BRANCH} mask={MASK} local_data={EXPECTED_LOCAL_DATA} "
        f"D22_states={states} stabilizer={EXPECTED_STABILIZER_ORDER} "
        f"center_orbits={centers}"
    )
    return centers


def build_formula(center: int):
    cnf = base_build(
        lex=False,
        structural=False,
        pair_bounds=False,
        dynamic_pair_bound=False,
    )
    nonisolated = add_nonisolated_variables(cnf)
    singletons = add_singleton_variables(cnf)
    code_edges = add_pair_indicators(cnf, 1)
    cnf.extend(
        CardEnc.atmost(
            lits=nonisolated,
            bound=12,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend(
        CardEnc.atleast(
            lits=singletons,
            bound=46,
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
            bound=20,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend([[literal] for literal in local_graph_assumptions(MASK)])
    cnf.extend([[-(center + 1)], *[[neighbor + 1] for neighbor in NEIGHBORS[center]]])
    cnf.clauses[:] = [list(dict.fromkeys(clause)) for clause in cnf.clauses]
    return cnf


def scratch_directory(raw: str) -> pathlib.Path:
    path = pathlib.Path(raw).resolve()
    if not path.is_relative_to("/scratch"):
        raise ValueError("CNF output must remain under /scratch")
    path.mkdir(parents=True, exist_ok=True)
    return path


def check_formula(center: int, cnf, output: pathlib.Path | None) -> None:
    name = f"branch58-d22-center{center}"
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
        f"bytes={len(payload)} sha256={digest}"
    )


def solve_formula(center: int, cnf) -> None:
    from pysat.solvers import Solver

    started = time.monotonic()
    with Solver(name="kissat404", bootstrap_with=cnf.clauses) as solver:
        assert not solver.solve()
    print(
        f"PASS Kissat 4.0.4 returned UNSAT for branch58-d22-center{center} "
        f"in {time.monotonic() - started:.3f}s"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-directory")
    parser.add_argument("--solve-kissat", action="store_true")
    args = parser.parse_args()
    output = scratch_directory(args.write_directory) if args.write_directory else None

    centers = verify_split()
    for center in centers:
        cnf = build_formula(center)
        check_formula(center, cnf, output)
        if args.solve_kissat:
            solve_formula(center, cnf)
    print("PASS six certified center cases exclude D=22; hence branch 58 has D>=23")


if __name__ == "__main__":
    main()
