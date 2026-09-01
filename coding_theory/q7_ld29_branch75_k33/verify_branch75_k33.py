#!/usr/bin/env python3
"""Verify the family split and build exact Q7 LD29 branch-75 CNFs."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import pathlib
import sys
import time


SOURCE_ROOT = pathlib.Path(__file__).resolve().parents[1]
CORE_PATH = SOURCE_ROOT / "q7_ld29_branch79_split" / "verify_branch79_split.py"
D23_PATH = SOURCE_ROOT / "q7_ld29_branches63_82" / "verify_branches63_82.py"
EXPECTED_CORE_SHA256 = "ea313ef366ad3b2da6c4e43d721aef8e96ec9bfa7dafe18c8fdade61c5fdd687"
EXPECTED_D23_SHA256 = "e2e2be7ab9fd6f5d26973507865c97eb1f20121d603eea6a082715adc796ec49"
assert hashlib.sha256(CORE_PATH.read_bytes()).hexdigest() == EXPECTED_CORE_SHA256
assert hashlib.sha256(D23_PATH.read_bytes()).hexdigest() == EXPECTED_D23_SHA256
sys.path.insert(0, str(CORE_PATH.parent))
sys.path.insert(0, str(D23_PATH.parent))

import verify_branch79_split as core  # noqa: E402
import verify_branches63_82 as d23  # noqa: E402


BRANCH = 75
EXPECTED_MASK = 4060
EXPECTED_LOCAL_DATA = ((3, 3, 3, 3, 3, 3), 0, 12, 42, 18, 3)
EXPECTED_D23_SURVIVOR = ((5, (1, 5, 5), 1, 1),)
EXPECTED_CENTERS = frozenset({15, 113, 63, 95, 111, 119, 123, 125, 126, 127})
EXPECTED_PAIR = ((15, 113),)
EXPECTED_VARIABLES = 10432
EXPECTED_STRONG_CLAUSES = 183619
EXPECTED_PAIR_CLAUSES = 183635
EXPECTED_STRONG_DIGEST = "dae5dfbd19fb3cacb48ba5782bbcff6c86f331b70ea6cee530ef3aa48907555e"
EXPECTED_PAIR_DIGEST = "c2847656e6d4774bfa7c46a740e8ce29a26f9d72875ac0dd1a6e0d168c21e262"


def configure_core() -> None:
    core.BRANCH = BRANCH
    core.EXPECTED_MASK = EXPECTED_MASK


def verify_split(mask: int) -> tuple[tuple[int, int], ...]:
    """Check the unique exceptional geometry at total family defect 23."""
    assert mask == EXPECTED_MASK
    assert mask.bit_count() == 9
    assert core.local_data(mask) == EXPECTED_LOCAL_DATA

    # In the canonical labeling the local graph is K_{3,3}, with parts
    # {0,1,2} and {3,4,5} (these are directions 1,...,6 in the cube).
    expected_edges = frozenset(itertools.product(range(3), range(3, 6)))
    assert core.selected_edges(mask) == expected_edges

    survivors = tuple(
        filter(core.survives_defect_six_occupancy, core.raw_states(mask, 23))
    )
    assert survivors == EXPECTED_D23_SURVIVOR

    # The state has two noncodeword defect-five centers and only one free
    # missing family slot.  Every center must therefore have local cost at
    # most one.  For K_{3,3}, no center has cost exactly one: the only
    # candidates are the two weight-four independent-part centers and the
    # eight words of weight at least six.
    centers = frozenset(
        center
        for center in range(128)
        if core.center_cost(center, mask) is not None
        and core.center_cost(center, mask) <= 1
    )
    assert centers == EXPECTED_CENTERS
    assert {core.center_cost(center, mask) for center in centers} == {0}

    # Two full-neighborhood noncodeword centers must be separated by at
    # least five: distances 2 or 3 lose a son slot in each family, distance
    # 4 loses at least three slots, and distance 1 is immediately
    # inconsistent.  Exactly one labeled pair survives.
    pairs = tuple(
        (first, second)
        for first, second in itertools.combinations(sorted(centers), 2)
        if core.hamming_distance(first, second) >= 5
    )
    assert pairs == EXPECTED_PAIR
    assert tuple(center.bit_count() for center in pairs[0]) == (4, 4)

    print(
        f"PASS branch={BRANCH} mask={mask} local_graph=K3,3 "
        f"local_data={core.local_data(mask)} d23_survivors={len(survivors)} "
        f"center_candidates={len(centers)} exceptional_pairs={len(pairs)}"
    )
    return pairs


def formulas():
    """Return the D>=24 formula and the sole D=23 exceptional formula."""
    configure_core()
    strong, mask = core.build_with_defect_bound(24)
    assert len(strong.clauses) == EXPECTED_STRONG_CLAUSES
    pairs = verify_split(mask)

    base, second_mask, defect_bound = d23.build(BRANCH)
    assert second_mask == mask
    assert defect_bound == 23
    first, second = pairs[0]
    core.add_center_case(base, first, second)
    assert len(base.clauses) == EXPECTED_PAIR_CLAUSES
    return (
        ("branch75-d24", strong, EXPECTED_STRONG_DIGEST),
        ("branch75-d23-f15-g113", base, EXPECTED_PAIR_DIGEST),
    )


def scratch_directory(raw: str) -> pathlib.Path:
    path = pathlib.Path(raw).resolve()
    if not path.is_relative_to("/scratch"):
        raise ValueError("CNF output must remain under /scratch")
    path.mkdir(parents=True, exist_ok=True)
    return path


def check_formula(cnf, expected_digest: str, name: str, output: pathlib.Path | None) -> None:
    payload = core.dimacs_bytes(cnf)
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

    started = time.monotonic()
    with Solver(name="kissat404", bootstrap_with=cnf.clauses) as solver:
        assert not solver.solve()
    print(f"PASS formula={name} Kissat-4.0.4=UNSAT seconds={time.monotonic()-started:.3f}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-directory")
    parser.add_argument("--solve-kissat", action="store_true")
    args = parser.parse_args()
    output = scratch_directory(args.write_directory) if args.write_directory else None

    for name, cnf, expected_digest in formulas():
        check_formula(cnf, expected_digest, name, output)
        if args.solve_kissat:
            solve_kissat(cnf, name)


if __name__ == "__main__":
    main()
