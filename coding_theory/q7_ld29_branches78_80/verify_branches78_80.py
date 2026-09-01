#!/usr/bin/env python3
"""Verify defect-25 rigidity and build exact Q7 LD29 branch 78/80 CNFs."""

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
    78: (5943, "26817751225eb282b2de0a3d9c6106b03775f519ae3be515e825b99c70f99524"),
    80: (5950, "9f3abd711640d651a95cafbe0f6f47398f62d66d83f964dfb7640feac8af6b2a"),
}
EXPECTED_SURVIVOR = (5, (1, 1, 5, 5), 0, 0)
EXPECTED_VARIABLES = 10432
EXPECTED_CLAUSES = 183619


def selected_edges(mask: int) -> frozenset[tuple[int, int]]:
    return frozenset(edge for index, edge in enumerate(EDGES) if (mask >> index) & 1)


def local_data(mask: int) -> tuple[tuple[int, ...], int, int, int, int]:
    edges = selected_edges(mask)
    degrees = [sum(vertex in edge for edge in edges) for vertex in COORDINATES]
    fathers = {vertex for vertex, degree in enumerate(degrees) if degree >= 2}
    triangles = sum(
        all(edge in edges for edge in itertools.combinations(triple, 2))
        for triple in itertools.combinations(COORDINATES, 3)
    )
    local_defect = sum(degrees[vertex] - 1 for vertex in fathers)
    local_capacity = sum(FAMILY_CAPACITY[degrees[vertex] - 1] for vertex in fathers)
    father_edges = sum(first in fathers and second in fathers for first, second in edges)
    forced_deficit = 2 * father_edges + 2 * triangles
    return tuple(sorted(degrees)), triangles, local_defect, local_capacity, forced_deficit


def independence_number(mask: int) -> int:
    edges = selected_edges(mask)
    return max(
        len(vertices)
        for size in range(7)
        for vertices in itertools.combinations(COORDINATES, size)
        if not any(edge in edges for edge in itertools.combinations(vertices, 2))
    )


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
            capacity = local_capacity + sum(FAMILY_CAPACITY[defect] for defect in extra)
            free_missing = capacity - family_vertices - forced_deficit
            if free_missing >= 0:
                states.append((couples, extra, free_missing, family_codeword_budget))
    return tuple(states)


def survives_defect_six_occupancy(
    state: tuple[int, tuple[int, ...], int, int],
) -> bool:
    _, extra, free_missing, family_codeword_budget = state
    defect_six_families = extra.count(6)
    forced_family_codewords = max(0, 8 * defect_six_families - free_missing)
    return forced_family_codewords <= family_codeword_budget


def hamming_distance(first: int, second: int) -> int:
    return (first ^ second).bit_count()


def verify_center_geometry(mask: int) -> None:
    """Exhaust the elementary weight/independence bridge for two full F7 fathers."""
    edges = selected_edges(mask)
    local_codewords = tuple((1 << (first + 1)) | (1 << (second + 1)) for first, second in edges)

    # Weight-three full fathers would be supported on local triangles and would
    # make all three corresponding son slots absent, one more than the two
    # charged by the triangle lower bound.  With zero free missing slots they
    # are impossible.  At weight four, isolation of the seven neighboring
    # codewords forbids distance two from any selected local codeword.
    candidates = tuple(
        center
        for center in range(128)
        if (
            (center.bit_count() >= 4 and center.bit_count() != 4)
            or (
                center.bit_count() == 4
                and all(hamming_distance(center, word) != 2 for word in local_codewords)
            )
        )
    )
    assert all(center.bit_count() >= 5 for center in candidates)
    assert all(
        hamming_distance(first, second) <= 4
        for first, second in itertools.combinations(candidates, 2)
    )

    assert independence_number(mask) == 2
    assert not any(
        all(edge not in edges for edge in itertools.combinations(vertices, 2))
        for vertices in itertools.combinations(COORDINATES, 3)
    )


def verify_defect_25(branch: int, mask: int) -> None:
    degrees, triangles, local_defect, local_capacity, forced_deficit = local_data(mask)
    assert mask.bit_count() == 9
    assert local_defect == 12
    assert raw_states(mask, 23) == ()
    survivors = tuple(filter(survives_defect_six_occupancy, raw_states(mask, 24)))
    assert survivors == (EXPECTED_SURVIVOR,)
    verify_center_geometry(mask)
    print(
        f"PASS branch={branch} mask={mask} degrees={degrees} triangles={triangles} "
        f"local_defect={local_defect} local_capacity={local_capacity} "
        f"forced_deficit={forced_deficit} alpha=2 D>=25"
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
