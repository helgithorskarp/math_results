#!/usr/bin/env python3
"""Verify the D>=24 bridge and exact Q7 LD29 branch-60 formula."""

from __future__ import annotations

import argparse
import functools
import hashlib
import itertools
import pathlib
import sys

from pysat.card import CardEnc, EncType


SOURCE_ROOT = pathlib.Path(__file__).resolve().parents[1]
LADDER_PATH = SOURCE_ROOT / "q7_ld29_branches0_62_bounds" / "verify_lower_frontier_bounds.py"
EXPECTED_LADDER_SHA256 = "acde98fb29c8673d57ceddc47b36e5b46a62a0cfa13ed542886e96fbaf0c4852"
assert hashlib.sha256(LADDER_PATH.read_bytes()).hexdigest() == EXPECTED_LADDER_SHA256
sys.path.insert(0, str(SOURCE_ROOT / "q7_ld29_family_reduction"))

from local_graphs import local_graph_assumptions, local_graph_representatives  # noqa: E402
from search_q7_ld29 import (  # noqa: E402
    add_nonisolated_variables,
    add_pair_indicators,
    add_singleton_variables,
    build as base_build,
    dimacs_bytes,
)


BRANCH = 60
EXPECTED_MASK = 5911
EXPECTED_DIGEST = "0cbef6fab7be0192154c33cdbc7105dd91392073d2dffac0148d466bdd7ee144"
EXPECTED_VARIABLES = 10432
EXPECTED_CLAUSES = 183619
COORDINATES = tuple(range(6))
EDGES = tuple(itertools.combinations(COORDINATES, 2))
FAMILY_CAPACITY = {1: 4, 2: 7, 3: 11, 4: 16, 5: 22, 6: 29}


def graph_data(mask: int):
    selected_edges = {edge for index, edge in enumerate(EDGES) if mask >> index & 1}
    degrees = tuple(
        sum(vertex in edge for edge in selected_edges) for vertex in COORDINATES
    )
    triangles = tuple(
        triple
        for triple in itertools.combinations(COORDINATES, 3)
        if all(tuple(sorted(pair)) in selected_edges for pair in itertools.combinations(triple, 2))
    )
    independence_number = max(
        len(vertices)
        for size in range(7)
        for vertices in itertools.combinations(COORDINATES, size)
        if all(
            tuple(sorted(pair)) not in selected_edges
            for pair in itertools.combinations(vertices, 2)
        )
    )
    local_defect = sum(degree - 1 for degree in degrees if degree >= 2)
    local_capacity = sum(FAMILY_CAPACITY[degree - 1] for degree in degrees if degree >= 2)
    father_edges = sum(
        degrees[first] >= 2 and degrees[second] >= 2
        for first, second in selected_edges
    )
    forced_deficit = 2 * father_edges + 2 * len(triangles)
    return (
        selected_edges,
        degrees,
        triangles,
        independence_number,
        local_defect,
        local_capacity,
        forced_deficit,
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


def surviving_d23_states(local_defect: int, local_capacity: int, forced_deficit: int):
    result = []
    total_defect = 23
    for couples in range((34 - total_defect) // 2 + 1):
        family_codeword_budget = 34 - total_defect - 2 * couples
        family_vertices = 104 - total_defect - 2 * couples
        for extra_defects in defect_partitions(total_defect - local_defect):
            total_capacity = local_capacity + sum(
                FAMILY_CAPACITY[defect] for defect in extra_defects
            )
            total_deficit = total_capacity - family_vertices
            if total_deficit < forced_deficit:
                continue
            free_missing = total_deficit - forced_deficit
            f6 = extra_defects.count(6)
            f5 = extra_defects.count(5)
            survives = False
            for codeword_f5 in range(f5 + 1):
                noncodeword_f5 = f5 - codeword_f5
                for missing_f6 in range(free_missing + 1):
                    for missing_codeword_f5 in range(free_missing - missing_f6 + 1):
                        missing_noncodeword_f5 = (
                            free_missing - missing_f6 - missing_codeword_f5
                        )
                        forced_family_codewords = max(0, 8 * f6 - missing_f6) + max(
                            0, 7 * codeword_f5 - missing_codeword_f5
                        )
                        forced_isolated = max(
                            0, 7 * noncodeword_f5 - 2 * missing_noncodeword_f5
                        )
                        if (
                            forced_family_codewords <= family_codeword_budget
                            and forced_family_codewords + forced_isolated
                            <= 29 - 2 * couples
                        ):
                            survives = True
            if survives:
                result.append(
                    (
                        couples,
                        extra_defects,
                        free_missing,
                        family_codeword_budget,
                    )
                )
    return tuple(result)


def hamming_distance(first: int, second: int) -> int:
    return (first ^ second).bit_count()


def verify_defect_24(mask: int) -> None:
    (
        selected_edges,
        degrees,
        triangles,
        independence_number,
        local_defect,
        local_capacity,
        forced_deficit,
    ) = graph_data(mask)
    assert tuple(sorted(degrees)) == (2, 2, 2, 3, 3, 4)
    assert len(triangles) == 3
    assert independence_number == 2
    assert (local_defect, local_capacity, forced_deficit) == (10, 37, 22)

    states = surviving_d23_states(local_defect, local_capacity, forced_deficit)
    assert states == ((5, (1, 1, 1, 5, 5), 0, 1),)

    # In this unique state, both defect-five families are full and their
    # fathers are noncodewords: a selected full F7 father would force seven
    # family codewords, exceeding the displayed budget one.
    selected_local_words = {
        (1 << (first + 1)) | (1 << (second + 1))
        for first, second in selected_edges
    }
    triangle_centers = {
        sum(1 << (coordinate + 1) for coordinate in triangle)
        for triangle in triangles
    }
    assert triangle_centers == {26, 56, 70}

    # A noncodeword full F7 center has all seven neighbors selected and all
    # 21 distance-two sons present.  The normalization eliminates weights at
    # most two.  A weight-three center is one of the triangles above and
    # consumes a third local missing slot where the triangle count charged
    # only two, impossible because free_missing=0.
    fixed_selected = {0, *selected_local_words}
    fixed_absent = {
        *(1 << coordinate for coordinate in range(7)),
        *((1 << 0) | (1 << coordinate) for coordinate in range(1, 7)),
        *(
            (1 << (first + 1)) | (1 << (second + 1))
            for first, second in EDGES
            if (first, second) not in selected_edges
        ),
    }
    for center in range(128):
        if center.bit_count() <= 2:
            neighbors = {center ^ (1 << coordinate) for coordinate in range(7)}
            assert center in fixed_selected or neighbors & fixed_absent
    weight_three_candidates = {
        center
        for center in range(128)
        if center.bit_count() == 3
        and center not in fixed_selected
        and not {
            center ^ (1 << coordinate) for coordinate in range(7)
        }
        & fixed_absent
    }
    assert weight_three_candidates == triangle_centers

    # Every codeword neighbor of a full noncodeword F7 center is isolated.
    # Thus a selected local word at distance two from a weight-four center is
    # impossible: their two common neighbors would be selected and adjacent
    # to that local word.  Alpha(H)=2 makes the necessary candidate set empty.
    weight_four_candidates = {
        center
        for center in range(128)
        if center.bit_count() == 4
        and all(
            hamming_distance(center, word) != 2 for word in selected_local_words
        )
    }
    assert not weight_four_candidates

    # Two full centers must be at distance at least five: distances 1--4
    # respectively violate the first center's codeword neighborhood, son
    # signature, distance-three exclusion, or the second center's full
    # neighborhood.  But two words of weights at least five in Q7 are at
    # distance at most four.
    high_weight = [vertex for vertex in range(128) if vertex.bit_count() >= 5]
    assert max(
        hamming_distance(first, second)
        for first, second in itertools.combinations(high_weight, 2)
    ) == 4
    print(
        f"PASS branch={BRANCH} mask={mask} degrees={tuple(sorted(degrees))} "
        f"triangles={len(triangles)} alpha={independence_number} "
        f"local_defect={local_defect} capacity={local_capacity} "
        f"forced_deficit={forced_deficit} unique_D23_state={states[0]} D>=24"
    )


def build_formula():
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
            bound=10,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend(
        CardEnc.atleast(
            lits=singleton,
            bound=48,
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
            bound=15,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    representatives = local_graph_representatives()
    assert len(representatives) == 115
    mask = representatives[BRANCH]
    cnf.extend([[literal] for literal in local_graph_assumptions(mask)])
    cnf.clauses[:] = [list(dict.fromkeys(clause)) for clause in cnf.clauses]
    return cnf, mask


def scratch_path(raw: str) -> pathlib.Path:
    path = pathlib.Path(raw).resolve()
    if not path.is_relative_to("/scratch"):
        raise ValueError("CNF output must remain under /scratch")
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-cnf")
    parser.add_argument("--solve-kissat", action="store_true")
    args = parser.parse_args()

    cnf, mask = build_formula()
    verify_defect_24(mask)
    payload = dimacs_bytes(cnf)
    digest = hashlib.sha256(payload).hexdigest()
    assert mask == EXPECTED_MASK
    assert mask.bit_count() == 8
    assert cnf.nv == EXPECTED_VARIABLES
    assert len(cnf.clauses) == EXPECTED_CLAUSES
    assert digest == EXPECTED_DIGEST
    if args.write_cnf:
        scratch_path(args.write_cnf).write_bytes(payload)
    if args.solve_kissat:
        from pysat.solvers import Solver

        with Solver(name="kissat404", bootstrap_with=cnf.clauses) as solver:
            assert not solver.solve()
        print("PASS Kissat 4.0.4 returned UNSAT")
    print(
        f"PASS branch={BRANCH} variables={cnf.nv} clauses={len(cnf.clauses)} "
        f"sha256={digest}"
    )


if __name__ == "__main__":
    main()
