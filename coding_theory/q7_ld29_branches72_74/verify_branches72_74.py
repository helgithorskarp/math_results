#!/usr/bin/env python3
"""Verify the defect bound and exact Q7 LD29 formulas for branches 72--74."""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys
import time


SOURCE_ROOT = pathlib.Path(__file__).resolve().parents[1]
CORE_PATH = SOURCE_ROOT / "q7_ld29_branch79_split" / "verify_branch79_split.py"
EXPECTED_CORE_SHA256 = "ea313ef366ad3b2da6c4e43d721aef8e96ec9bfa7dafe18c8fdade61c5fdd687"
assert hashlib.sha256(CORE_PATH.read_bytes()).hexdigest() == EXPECTED_CORE_SHA256
sys.path.insert(0, str(CORE_PATH.parent))

import verify_branch79_split as core  # noqa: E402


BRANCHES = (72, 73, 74)
EXPECTED_MASKS = {72: 1917, 73: 2013, 74: 2014}
EXPECTED_LOCAL_DATA = {
    72: ((2, 2, 3, 3, 4, 4), 3, 12, 44, 24, 3),
    73: ((2, 2, 3, 3, 4, 4), 3, 12, 44, 24, 3),
    74: ((2, 3, 3, 3, 3, 4), 2, 12, 43, 22, 3),
}
EXPECTED_D23_STATES = {
    72: ((5, (5, 6), 0, 1),),
    73: ((5, (5, 6), 0, 1),),
    74: ((5, (5, 6), 1, 1),),
}
EXPECTED_DIGESTS = {
    72: "c6d5047b8dc7b79227bda5801bbd485af32db416851b8841695e0d1ec987de78",
    73: "a9fe582da3b94771a7517e69949ca4e3edcee87ca1bc1a81a67ccd011cbb58ec",
    74: "c54ae62e5223fc3b00c5b0946f08580f84abf1856a32f7419664699e7c50f512",
}
EXPECTED_VARIABLES = 10432
EXPECTED_CLAUSES = 183619


def verify_defect_bound(branch: int, mask: int) -> None:
    """Check the complete branch-local capacity proof of D >= 24."""
    assert mask == EXPECTED_MASKS[branch]
    assert mask.bit_count() == 9
    assert core.local_data(mask) == EXPECTED_LOCAL_DATA[branch]

    # The graph contribution establishing the universal bound supplies
    # D >= 18.  Pure capacity excludes D=18,...,22 in these branches.
    assert all(core.raw_states(mask, defect) == () for defect in range(18, 23))

    # At D=23 exactly one capacity row remains.  It contains a defect-six
    # father.  Such a family has I(f)=N[f]; with s free missing slots it
    # places at least 8-s codewords in families, exceeding budget one.
    states = core.raw_states(mask, 23)
    assert states == EXPECTED_D23_STATES[branch]
    assert not any(core.survives_defect_six_occupancy(state) for state in states)
    couples, extra, slack, budget = states[0]
    assert couples == 5 and extra == (5, 6) and budget == 1
    assert 8 - slack > budget

    print(
        f"PASS branch={branch} mask={mask} local_data={core.local_data(mask)} "
        f"d18_to_d22_states=0 d23_state={states[0]} implies_D_at_least=24"
    )


def scratch_directory(raw: str) -> pathlib.Path:
    path = pathlib.Path(raw).resolve()
    if not path.is_relative_to("/scratch"):
        raise ValueError("CNF output must remain under /scratch")
    path.mkdir(parents=True, exist_ok=True)
    return path


def solve_kissat(cnf, branch: int) -> None:
    from pysat.solvers import Solver

    started = time.monotonic()
    with Solver(name="kissat404", bootstrap_with=cnf.clauses) as solver:
        assert not solver.solve()
    print(f"PASS branch={branch} Kissat-4.0.4=UNSAT seconds={time.monotonic()-started:.3f}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-directory")
    parser.add_argument("--solve-kissat", action="store_true")
    args = parser.parse_args()
    output = scratch_directory(args.write_directory) if args.write_directory else None

    for branch in BRANCHES:
        core.BRANCH = branch
        cnf, mask = core.build_with_defect_bound(24)
        verify_defect_bound(branch, mask)
        payload = core.dimacs_bytes(cnf)
        digest = hashlib.sha256(payload).hexdigest()
        assert cnf.nv == EXPECTED_VARIABLES
        assert len(cnf.clauses) == EXPECTED_CLAUSES
        assert digest == EXPECTED_DIGESTS[branch]
        if output is not None:
            (output / f"branch{branch}-d24.cnf").write_bytes(payload)
        print(
            f"PASS formula=branch{branch}-d24 variables={cnf.nv} "
            f"clauses={len(cnf.clauses)} sha256={digest}"
        )
        if args.solve_kissat:
            solve_kissat(cnf, branch)


if __name__ == "__main__":
    main()
