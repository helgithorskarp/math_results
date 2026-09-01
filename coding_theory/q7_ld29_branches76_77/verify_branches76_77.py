#!/usr/bin/env python3
"""Verify defect-25 rigidity and build exact Q7 LD29 branch 76/77 CNFs."""

from __future__ import annotations

import argparse
import functools
import hashlib
import itertools
import pathlib
import sys

from pysat.card import CardEnc, EncType


SOURCE_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE_ROOT / "q7_ld29_family_reduction"))

from local_graphs import local_graph_assumptions, local_graph_representatives  # noqa: E402
from search_q7_ld29 import (  # noqa: E402
    add_nonisolated_variables,
    add_pair_indicators,
    add_singleton_variables,
    build as base_build,
    dimacs_bytes,
)


COORDINATES = tuple(range(6))
EDGES = tuple(itertools.combinations(COORDINATES, 2))
FAMILY_CAPACITY = {1: 4, 2: 7, 3: 11, 4: 16, 5: 22, 6: 29}
EXPECTED = {
    76: (5875, "6955a5b3bcbff062a20967a981ab4d1257d5524d7a0db86ad6a2e28786c29369"),
    77: (5919, "041eaf6fc23e01e20c09a4c86983570d084d02b50631f5ca1c8bfbecd150987c"),
}
EXPECTED_RAW_D24 = {
    76: (
        (3, (6, 6), 1, 4),
        (4, (1, 5, 6), 0, 2),
        (4, (6, 6), 3, 2),
        (5, (1, 1, 1, 1, 1, 1, 6), 0, 0),
        (5, (1, 1, 4, 6), 0, 0),
        (5, (1, 5, 6), 2, 0),
        (5, (6, 6), 5, 0),
    ),
    77: (
        (3, (6, 6), 1, 4),
        (4, (1, 5, 6), 0, 2),
        (4, (6, 6), 3, 2),
        (5, (1, 1, 1, 1, 1, 1, 6), 0, 0),
        (5, (1, 1, 4, 6), 0, 0),
        (5, (1, 5, 6), 2, 0),
        (5, (6, 6), 5, 0),
    ),
}
EXPECTED_VARIABLES = 10432
EXPECTED_CLAUSES = 183619


def local_data(mask: int) -> tuple[tuple[int, ...], int, int, int, int]:
    adjacency = [[False] * 6 for _ in COORDINATES]
    degrees = [0] * 6
    graph_edges: list[tuple[int, int]] = []
    for index, (first, second) in enumerate(EDGES):
        if (mask >> index) & 1:
            adjacency[first][second] = adjacency[second][first] = True
            degrees[first] += 1
            degrees[second] += 1
            graph_edges.append((first, second))
    fathers = {vertex for vertex, degree in enumerate(degrees) if degree >= 2}
    triangles = sum(
        adjacency[first][second]
        and adjacency[first][third]
        and adjacency[second][third]
        for first, second, third in itertools.combinations(COORDINATES, 3)
    )
    local_defect = sum(degrees[vertex] - 1 for vertex in fathers)
    local_capacity = sum(FAMILY_CAPACITY[degrees[vertex] - 1] for vertex in fathers)
    father_edges = sum(first in fathers and second in fathers for first, second in graph_edges)
    forced_deficit = 2 * father_edges + 2 * triangles
    return tuple(sorted(degrees)), triangles, local_defect, local_capacity, forced_deficit


@functools.cache
def defect_partitions(total: int, minimum_part: int = 1) -> tuple[tuple[int, ...], ...]:
    if total == 0:
        return ((),)
    return tuple(
        (part,) + remainder
        for part in range(minimum_part, 7)
        if part <= total
        for remainder in defect_partitions(total - part, part)
    )


def raw_states(mask: int, total_defect: int) -> tuple[tuple[int, tuple[int, ...], int, int], ...]:
    _, _, local_defect, local_capacity, forced_deficit = local_data(mask)
    states = []
    for couples in range((34 - total_defect) // 2 + 1):
        family_vertices = 104 - total_defect - 2 * couples
        family_codeword_budget = 34 - total_defect - 2 * couples
        for extra in defect_partitions(total_defect - local_defect):
            capacity = local_capacity + sum(FAMILY_CAPACITY[d] for d in extra)
            free_missing = capacity - family_vertices - forced_deficit
            if free_missing >= 0:
                states.append((couples, extra, free_missing, family_codeword_budget))
    return tuple(states)


def verify_defect_25(branch: int, mask: int) -> None:
    degrees, triangles, local_defect, local_capacity, forced_deficit = local_data(mask)
    assert mask.bit_count() == 9
    assert local_defect == 12
    assert raw_states(mask, 23) == ()
    states = raw_states(mask, 24)
    assert states == EXPECTED_RAW_D24[branch]
    for _, extra, free_missing, family_codeword_budget in states:
        defect_six_families = extra.count(6)
        forced_family_codewords = max(0, 8 * defect_six_families - free_missing)
        assert defect_six_families >= 1
        assert forced_family_codewords > family_codeword_budget
    print(
        f"PASS branch={branch} mask={mask} degrees={degrees} triangles={triangles} "
        f"local_defect={local_defect} local_capacity={local_capacity} "
        f"forced_deficit={forced_deficit} D>=25"
    )


def build(branch: int):
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
            bound=9,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend(
        CardEnc.atleast(
            lits=singleton,
            bound=49,
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
            bound=13,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    mask = local_graph_representatives()[branch]
    cnf.extend([[literal] for literal in local_graph_assumptions(mask)])
    cnf.clauses[:] = [list(dict.fromkeys(clause)) for clause in cnf.clauses]
    return cnf, mask


def scratch_directory(raw: str) -> pathlib.Path:
    path = pathlib.Path(raw).resolve()
    if not path.is_relative_to("/scratch"):
        raise ValueError("CNF output must remain under /scratch")
    path.mkdir(parents=True, exist_ok=True)
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-directory")
    parser.add_argument("--solve-kissat", action="store_true")
    args = parser.parse_args()
    output = scratch_directory(args.write_directory) if args.write_directory else None

    for branch, (expected_mask, expected_digest) in EXPECTED.items():
        cnf, mask = build(branch)
        verify_defect_25(branch, mask)
        payload = dimacs_bytes(cnf)
        digest = hashlib.sha256(payload).hexdigest()
        assert mask == expected_mask
        assert cnf.nv == EXPECTED_VARIABLES
        assert len(cnf.clauses) == EXPECTED_CLAUSES
        assert digest == expected_digest
        if output is not None:
            (output / f"branch-{branch}.cnf").write_bytes(payload)
        print(
            f"PASS branch={branch} variables={cnf.nv} clauses={len(cnf.clauses)} "
            f"sha256={digest}"
        )
        if args.solve_kissat:
            from pysat.solvers import Solver

            with Solver(name="kissat404", bootstrap_with=cnf.clauses) as solver:
                assert not solver.solve()
            print(f"PASS branch={branch} Kissat-4.0.4=UNSAT")


if __name__ == "__main__":
    main()
