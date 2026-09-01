#!/usr/bin/env python3
"""Verify the full-family split and build exact Q7 LD29 branch-79 CNFs."""

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
    NEIGHBORS,
    add_nonisolated_variables,
    add_pair_indicators,
    add_singleton_variables,
    build as base_build,
    dimacs_bytes,
)


BRANCH = 79
EXPECTED_MASK = 5949
COORDINATES = tuple(range(6))
EDGES = tuple(itertools.combinations(COORDINATES, 2))
FAMILY_CAPACITY = {1: 4, 2: 7, 3: 11, 4: 16, 5: 22, 6: 29}
EXPECTED_STRONG_DIGEST = "8602da5601d1d76a2d9b87c97eaaa873b226fdc5fee9c33a3eec48fc6263f4c7"
EXPECTED_EXCEPTION_DIGESTS = {
    (70, 125): "eaf57ddda6b7529d74ad180224437c52dc95bc21f0d7501a246683cf41712907",
    (70, 123): "7991caaaf93d46d6f8a840d61e1a6a418bf23b5edf1fc84f437397125fb716b9",
    (70, 63): "97616bacb9eb75734c18117ef298a27ff7251fd9f51a41001aa06fcda49eca17",
    (50, 125): "819299c5c3037940085e6a3b3532c58ca15d8f07c912af0b7cd561591e5acdca",
    (50, 111): "e82f5f76a760c0ddda7d4661dc6dbe1f2b25afd080c7b17d7cf157a1f3e4f66a",
    (50, 95): "be9fb55033aebb4bc3459794c7cc9ed89f4618200fffe440babbd4c1ee236c80",
    (56, 119): "0bfa2b9f9ffaaeb2f3c824d701dd5eca797a4fc0f466f4bc75ed396cbf05f29c",
    (56, 111): "b057d94ecb7f251a24407072f87fc07bfdd2710a34232f5588f34f051dbc8c51",
    (56, 95): "12011f5b20655aec332d162e6e72d4eacbc1efb02fe9f66b88bc5bc999784ba1",
}
EXPECTED_D24_SURVIVORS = (
    (5, (1, 1, 5, 5), 1, 0),
    (5, (2, 5, 5), 0, 0),
)
EXPECTED_VARIABLES = 10432
EXPECTED_BASE_CLAUSES = 183619


def selected_edges(mask: int) -> frozenset[tuple[int, int]]:
    return frozenset(edge for index, edge in enumerate(EDGES) if (mask >> index) & 1)


def triangles(mask: int) -> tuple[tuple[int, int, int], ...]:
    edges = selected_edges(mask)
    return tuple(
        triple
        for triple in itertools.combinations(COORDINATES, 3)
        if all(edge in edges for edge in itertools.combinations(triple, 2))
    )


def local_data(mask: int) -> tuple[tuple[int, ...], int, int, int, int, int]:
    edges = selected_edges(mask)
    degrees = [sum(vertex in edge for edge in edges) for vertex in COORDINATES]
    fathers = {vertex for vertex, degree in enumerate(degrees) if degree >= 2}
    local_triangles = triangles(mask)
    local_defect = sum(degrees[vertex] - 1 for vertex in fathers)
    local_capacity = sum(FAMILY_CAPACITY[degrees[vertex] - 1] for vertex in fathers)
    father_edges = sum(first in fathers and second in fathers for first, second in edges)
    forced_deficit = 2 * father_edges + 2 * len(local_triangles)
    independence = max(
        len(vertices)
        for size in range(7)
        for vertices in itertools.combinations(COORDINATES, size)
        if not any(edge in edges for edge in itertools.combinations(vertices, 2))
    )
    return (
        tuple(sorted(degrees)),
        len(local_triangles),
        local_defect,
        local_capacity,
        forced_deficit,
        independence,
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
    _, _, local_defect, local_capacity, forced_deficit, _ = local_data(mask)
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
    forced_family_codewords = max(0, 8 * extra.count(6) - free_missing)
    return forced_family_codewords <= family_codeword_budget


def hamming_distance(first: int, second: int) -> int:
    return (first ^ second).bit_count()


def center_cost(center: int, mask: int) -> int | None:
    """Lower-bound extra missing slots forced by a defect-five center."""
    weight = center.bit_count()
    edges = selected_edges(mask)
    actual_local_words = tuple((1 << (i + 1)) | (1 << (j + 1)) for i, j in edges)
    if weight <= 2:
        return None
    if weight == 3:
        if center & 1:
            return None
        support = tuple(index - 1 for index in range(1, 7) if center & (1 << index))
        return 1 if all(edge in edges for edge in itertools.combinations(support, 2)) else None
    if weight == 4:
        return sum((center & word) == word for word in actual_local_words)
    if weight == 5:
        # Alpha two ensures a selected local word is supported.  That word is
        # at distance three and forces its three predecessor son slots absent.
        assert any((center & word) == word for word in actual_local_words)
        return 3
    return 0


def exceptional_cases(mask: int) -> tuple[tuple[int, int], ...]:
    cases = tuple(
        (
            sum(1 << (coordinate + 1) for coordinate in triangle),
            127 ^ (1 << (omitted + 1)),
        )
        for triangle in triangles(mask)
        for omitted in triangle
    )
    possible = {
        tuple(sorted((first, second)))
        for first, second in itertools.combinations(range(128), 2)
        if center_cost(first, mask) is not None
        and center_cost(second, mask) is not None
        and center_cost(first, mask) + center_cost(second, mask) <= 1
        and hamming_distance(first, second) >= 5
    }
    assert possible == {tuple(sorted(case)) for case in cases}
    assert len(cases) == 9
    return cases


def verify_split(mask: int) -> tuple[tuple[int, int], ...]:
    degrees, triangle_count, local_defect, capacity, deficit, independence = local_data(mask)
    assert mask == EXPECTED_MASK
    assert mask.bit_count() == 9
    assert (degrees, triangle_count, local_defect, capacity, deficit, independence) == (
        (2, 3, 3, 3, 3, 4),
        3,
        12,
        43,
        24,
        2,
    )
    assert raw_states(mask, 23) == ()
    survivors = tuple(filter(survives_defect_six_occupancy, raw_states(mask, 24)))
    assert survivors == EXPECTED_D24_SURVIVORS

    # The zero-slack survivor has two full defect-five centers.  Alpha two
    # excludes weight four; zero slack excludes weight three and weight five,
    # leaving weights at least six, whose mutual distance is at most two.
    full_candidates = tuple(
        center for center in range(128) if center_cost(center, mask) == 0
    )
    assert all(center.bit_count() >= 6 for center in full_candidates)
    assert all(
        hamming_distance(first, second) <= 2
        for first, second in itertools.combinations(full_candidates, 2)
    )

    cases = exceptional_cases(mask)
    print(
        f"PASS branch={BRANCH} mask={mask} degrees={degrees} triangles={triangle_count} "
        f"local_defect={local_defect} capacity={capacity} deficit={deficit} "
        f"alpha={independence} exceptional_cases={len(cases)}"
    )
    return cases


def build_with_defect_bound(defect_bound: int):
    edge_bound = 13 if defect_bound == 25 else 15
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
            bound=34 - defect_bound,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend(
        CardEnc.atleast(
            lits=singleton,
            bound=24 + defect_bound,
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
            bound=edge_bound,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    mask = local_graph_representatives()[BRANCH]
    cnf.extend([[literal] for literal in local_graph_assumptions(mask)])
    cnf.clauses[:] = [list(dict.fromkeys(clause)) for clause in cnf.clauses]
    return cnf, mask


def add_center_case(cnf, first: int, second: int) -> None:
    units = [
        -(first + 1),
        -(second + 1),
        *(neighbor + 1 for neighbor in NEIGHBORS[first]),
        *(neighbor + 1 for neighbor in NEIGHBORS[second]),
    ]
    cnf.extend([[literal] for literal in units])
    cnf.clauses[:] = [list(dict.fromkeys(clause)) for clause in cnf.clauses]


def scratch_directory(raw: str) -> pathlib.Path:
    path = pathlib.Path(raw).resolve()
    if not path.is_relative_to("/scratch"):
        raise ValueError("CNF output must remain under /scratch")
    path.mkdir(parents=True, exist_ok=True)
    return path


def check_formula(cnf, expected_digest: str, name: str, output: pathlib.Path | None) -> None:
    payload = dimacs_bytes(cnf)
    digest = hashlib.sha256(payload).hexdigest()
    assert cnf.nv == EXPECTED_VARIABLES
    assert digest == expected_digest
    if output is not None:
        (output / f"{name}.cnf").write_bytes(payload)
    print(
        f"PASS formula={name} variables={cnf.nv} clauses={len(cnf.clauses)} "
        f"sha256={digest}"
    )


def solve_kissat(cnf, name: str) -> None:
    from pysat.solvers import Solver

    with Solver(name="kissat404", bootstrap_with=cnf.clauses) as solver:
        assert not solver.solve()
    print(f"PASS formula={name} Kissat-4.0.4=UNSAT")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-directory")
    parser.add_argument("--solve-kissat", action="store_true")
    args = parser.parse_args()
    output = scratch_directory(args.write_directory) if args.write_directory else None

    strong, mask = build_with_defect_bound(25)
    assert len(strong.clauses) == EXPECTED_BASE_CLAUSES
    cases = verify_split(mask)
    check_formula(strong, EXPECTED_STRONG_DIGEST, "branch79-d25", output)
    if args.solve_kissat:
        solve_kissat(strong, "branch79-d25")

    base, second_mask = build_with_defect_bound(24)
    assert second_mask == mask
    assert len(base.clauses) == EXPECTED_BASE_CLAUSES
    for first, second in cases:
        cnf = base.copy()
        add_center_case(cnf, first, second)
        name = f"branch79-exception-f{first}-g{second}"
        check_formula(cnf, EXPECTED_EXCEPTION_DIGESTS[(first, second)], name, output)
        if args.solve_kissat:
            solve_kissat(cnf, name)


if __name__ == "__main__":
    main()
