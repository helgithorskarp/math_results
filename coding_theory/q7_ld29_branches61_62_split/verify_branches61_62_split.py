#!/usr/bin/env python3
"""Verify the D>=24 full-family splits for Q7 LD29 branches 61 and 62."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import pathlib
import sys

from pysat.card import CardEnc, EncType


SOURCE_ROOT = pathlib.Path(__file__).resolve().parents[1]
LADDER_PATH = SOURCE_ROOT / "q7_ld29_branches0_62_bounds" / "verify_lower_frontier_bounds.py"
SPLIT_PATH = SOURCE_ROOT / "q7_ld29_branch79_split" / "verify_branch79_split.py"
EXPECTED_LADDER_SHA256 = "acde98fb29c8673d57ceddc47b36e5b46a62a0cfa13ed542886e96fbaf0c4852"
EXPECTED_SPLIT_SHA256 = "ea313ef366ad3b2da6c4e43d721aef8e96ec9bfa7dafe18c8fdade61c5fdd687"
assert hashlib.sha256(LADDER_PATH.read_bytes()).hexdigest() == EXPECTED_LADDER_SHA256
assert hashlib.sha256(SPLIT_PATH.read_bytes()).hexdigest() == EXPECTED_SPLIT_SHA256
sys.path.insert(0, str(SOURCE_ROOT / "q7_ld29_family_reduction"))
sys.path.insert(0, str(SOURCE_ROOT / "q7_ld29_branch79_split"))

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


MASKS = {61: 5941, 62: 5948}
EXPECTED_STATES = (
    (5, (1, 1, 1, 5, 5), 1, 1),
    (5, (1, 2, 5, 5), 0, 1),
    (5, (3, 5, 5), 0, 1),
)
EXPECTED_CASES = {
    61: ((70, 125), (70, 123), (70, 63), (56, 119), (56, 111), (56, 95)),
    62: ((50, 125), (50, 111), (50, 95), (56, 119), (56, 111), (56, 95)),
}
EXPECTED_DIGESTS = {
    61: {
        (70, 125): "f4e6e3063025e380c1d8e4bdb8b4011a7e654de593939893a82dad0d3df984b4",
        (70, 123): "a58f7e922b0e69805aeeb3b6160592a2c5388e9b9f8cdac787b6efc944e87214",
        (70, 63): "6e0e1af9fac6bcd2ef0911609a6f4ca10455980ca763a625b899383bc619f62e",
        (56, 119): "2bac9b66ec4c38169bcf8a6cd584995b72fef5a676365ae7a2d0a00b152990db",
        (56, 111): "a7473865e1ba903ef7869c023a154cb1fdc2b8c585bfde60207d8a9a7edc4967",
        (56, 95): "df24f5951951af7d3b43b0b6f04fb03bb0d50ab02f5c6b1744fa1bedb314f781",
    },
    62: {
        (50, 125): "d1b9c55ae2aec498a52001bac3a58a8d9557e71f22a17d4183d7bac7962fd224",
        (50, 111): "7bc7711344341e7d03623b756aec50d4120663b3b483ccab30b7cb83986f30c5",
        (50, 95): "fc679ae0eb673785bbb719aab4b0822bc65b13ba1a136f985835697d98057427",
        (56, 119): "54997ab8189fa936ada28908449e21d238e1773fc342190ea0e58ce6e808aada",
        (56, 111): "49367548736f044fe39af17af681fc28b59f9ef9a391e5e97a444dcca9a77230",
        (56, 95): "576548f3b467c5e8832d55d00f2d92c6115b37c3008c216a51917c77b2fb0fe1",
    },
}
EXPECTED_VARIABLES = 10432
EXPECTED_CLAUSES = 183635


def exceptional_cases(mask: int) -> tuple[tuple[int, int], ...]:
    cases = tuple(
        (
            sum(1 << (coordinate + 1) for coordinate in triangle),
            127 ^ (1 << (omitted + 1)),
        )
        for triangle in split.triangles(mask)
        for omitted in triangle
    )
    possible = {
        tuple(sorted((first, second)))
        for first, second in itertools.combinations(range(128), 2)
        if split.center_cost(first, mask) is not None
        and split.center_cost(second, mask) is not None
        and split.center_cost(first, mask) + split.center_cost(second, mask) <= 1
        and split.hamming_distance(first, second) >= 5
    }
    assert possible == {tuple(sorted(case)) for case in cases}
    return cases


def verify_analytic_split(branch: int, mask: int) -> tuple[tuple[int, int], ...]:
    data = split.local_data(mask)
    assert data == ((2, 2, 3, 3, 3, 3), 2, 10, 36, 20, 2)
    states = tuple(
        filter(split.survives_defect_six_occupancy, split.raw_states(mask, 23))
    )
    assert states == EXPECTED_STATES

    # Both defect-five families are full in the two zero-slack states.  They
    # must have noncodeword fathers because a selected full father alone
    # needs seven family codewords, exceeding the global budget one.  Their
    # centers therefore have total local cost zero and mutual distance at
    # least five.  Exhaustion of all 128 vertices shows this is impossible.
    zero_cost = tuple(
        center for center in range(128) if split.center_cost(center, mask) == 0
    )
    assert all(center.bit_count() >= 6 for center in zero_cost)
    assert all(
        split.hamming_distance(first, second) <= 2
        for first, second in itertools.combinations(zero_cost, 2)
    )

    # The remaining state has one free missing slot.  Exhaustive center-cost
    # classification leaves exactly a triangle center and a weight-six
    # center omitting one coordinate of that triangle.
    cases = exceptional_cases(mask)
    assert cases == EXPECTED_CASES[branch]
    print(
        f"PASS analytic branch={branch} mask={mask} degrees={data[0]} "
        f"triangles={data[1]} local_defect={data[2]} capacity={data[3]} "
        f"forced_deficit={data[4]} alpha={data[5]} cases={len(cases)}"
    )
    return cases


def build_base(branch: int):
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
    representatives = local_graph_representatives()
    assert len(representatives) == 115
    mask = representatives[branch]
    assert mask == MASKS[branch]
    cnf.extend([[literal] for literal in local_graph_assumptions(mask)])
    cnf.clauses[:] = [list(dict.fromkeys(clause)) for clause in cnf.clauses]
    return cnf, mask


def add_centers(cnf, first: int, second: int) -> None:
    units = [
        -(first + 1),
        -(second + 1),
        *(neighbor + 1 for neighbor in NEIGHBORS[first]),
        *(neighbor + 1 for neighbor in NEIGHBORS[second]),
    ]
    assert len(set(units)) == 16
    cnf.extend([[literal] for literal in units])
    cnf.clauses[:] = [list(dict.fromkeys(clause)) for clause in cnf.clauses]


def scratch_directory(raw: str) -> pathlib.Path:
    path = pathlib.Path(raw).resolve()
    if not path.is_relative_to("/scratch"):
        raise ValueError("CNF output must remain under /scratch")
    path.mkdir(parents=True, exist_ok=True)
    return path


def check_formula(branch: int, first: int, second: int, cnf, output: pathlib.Path | None):
    payload = dimacs_bytes(cnf)
    digest = hashlib.sha256(payload).hexdigest()
    assert cnf.nv == EXPECTED_VARIABLES
    assert len(cnf.clauses) == EXPECTED_CLAUSES
    assert digest == EXPECTED_DIGESTS[branch][(first, second)]
    name = f"branch{branch}-d23-f{first}-g{second}"
    if output is not None:
        (output / f"{name}.cnf").write_bytes(payload)
    print(
        f"PASS formula={name} variables={cnf.nv} clauses={len(cnf.clauses)} "
        f"sha256={digest}"
    )
    return name


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

    for branch in sorted(MASKS):
        base, mask = build_base(branch)
        cases = verify_analytic_split(branch, mask)
        for first, second in cases:
            cnf = base.copy()
            add_centers(cnf, first, second)
            name = check_formula(branch, first, second, cnf, output)
            if args.solve_kissat:
                solve_kissat(cnf, name)


if __name__ == "__main__":
    main()
