#!/usr/bin/env python3
"""Verify and build the full-family certificate split for Q7 LD29 branch 69."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import pathlib
import sys


SOURCE_ROOT = pathlib.Path(__file__).resolve().parents[1]
CORE_PATH = SOURCE_ROOT / "q7_ld29_branch79_split" / "verify_branch79_split.py"
EXPECTED_CORE_SHA256 = "ea313ef366ad3b2da6c4e43d721aef8e96ec9bfa7dafe18c8fdade61c5fdd687"
assert hashlib.sha256(CORE_PATH.read_bytes()).hexdigest() == EXPECTED_CORE_SHA256
sys.path.insert(0, str(CORE_PATH.parent))

import verify_branch79_split as core  # noqa: E402


BRANCH = 69
EXPECTED_MASK = 1789
EXPECTED_STRONG_DIGEST = "d9cb1197b68fd318cc8f9c713b2f9ad375a28dfc10e27eccafb3f1370d9323d7"
EXPECTED_EXCEPTION_DIGESTS = {
    (22, 111): "58992a0e49a6c50d593e165a3e9bdd4dfc742aeab16919c3e2e59796c791e650",
    (22, 113): "3df9c319d8228eed8685e97c94943507ffbbc7506a70eb4dcc18b054a60224f5",
    (22, 123): "755984369a7ce700338696fb1a0cbd8933e05f12e688e07ea8504f2e3fac6b98",
    (22, 125): "c39e3443d7d8325fae5e6be891ffa7446ac17e680b6589a6b66a886fccc96158",
    (28, 111): "987dad667e32b870283471d0776b031589934db05fac9f9ec71eeac6c639dacc",
    (28, 113): "59070b70bb4274ce03b31062909a0c91944620e291b1cefe47249e1777c57df5",
    (28, 119): "860d12a615b26af325aa23ed51c9ec5f14595076b7f7ad049f95fc112590699a",
    (28, 123): "e4ba7a50e23f84792857dc2de15b8211860fa2f13a344cb658e9074d5a64fbe5",
    (38, 95): "49a102515be97753ff35b787333c548ebe6241885b2b49eb006561bc2752bc29",
    (38, 113): "18b87234e74c57811535b7fc4e59104711061c8aaa31617caeb12e77b8824a9d",
    (38, 123): "63ebcf5a1d050022fbef5cc845fcc33bec5a3801d6a3b45f365a14183526d573",
    (38, 125): "6d8d352c416f266f548f9318c0a88b06cf616973e3a20edbdcdcd751cbd6ebb8",
    (44, 95): "98a737187965efbe56feb49e88145685a5d9f9496b2ed3a05f7ca59ebaf3dae9",
    (44, 113): "a4affcd150833d3a2ab6f09c1cd4de53203037a20ffd326ef98578c94acc63ea",
    (44, 119): "0172dbfb83b9235bddab0c5360c052b5b610f0c82eb5eda3cd9a55a6a2ef0bcc",
    (44, 123): "60c466aabb802a1b07d2f2e950cffe7d1ca173696124f4a0a3a2b581f4256aa5",
}
EXPECTED_CASES = tuple(EXPECTED_EXCEPTION_DIGESTS)
EXPECTED_D24_SURVIVORS = (
    (5, (1, 1, 5, 5), 1, 0),
    (5, (2, 5, 5), 0, 0),
)


def configure_core() -> None:
    core.BRANCH = BRANCH
    core.EXPECTED_MASK = EXPECTED_MASK


def exceptional_cases(mask: int) -> tuple[tuple[int, int], ...]:
    """Enumerate all center pairs compatible with the one-slot relaxation."""
    possible = tuple(
        (first, second)
        for first, second in itertools.combinations(range(128), 2)
        if core.center_cost(first, mask) is not None
        and core.center_cost(second, mask) is not None
        and core.center_cost(first, mask) + core.center_cost(second, mask) <= 1
        and core.hamming_distance(first, second) >= 5
    )
    assert possible == EXPECTED_CASES
    assert all(
        core.center_cost(first, mask) + core.center_cost(second, mask) == 1
        for first, second in possible
    )
    return possible


def verify_split(mask: int) -> tuple[tuple[int, int], ...]:
    data = core.local_data(mask)
    assert mask == EXPECTED_MASK
    assert mask.bit_count() == 9
    assert data == ((1, 3, 3, 3, 4, 4), 4, 12, 43, 24, 3)
    assert core.raw_states(mask, 23) == ()
    survivors = tuple(
        filter(core.survives_defect_six_occupancy, core.raw_states(mask, 24))
    )
    assert survivors == EXPECTED_D24_SURVIVORS

    cases = exceptional_cases(mask)
    print(
        f"PASS branch={BRANCH} mask={mask} degrees={data[0]} triangles={data[1]} "
        f"local_defect={data[2]} capacity={data[3]} deficit={data[4]} "
        f"alpha={data[5]} exceptional_cases={len(cases)}"
    )
    return cases


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-directory")
    parser.add_argument("--solve-kissat", action="store_true")
    args = parser.parse_args()
    output = core.scratch_directory(args.write_directory) if args.write_directory else None

    configure_core()
    strong, mask = core.build_with_defect_bound(25)
    assert len(strong.clauses) == core.EXPECTED_BASE_CLAUSES
    cases = verify_split(mask)
    core.check_formula(strong, EXPECTED_STRONG_DIGEST, "branch69-d25", output)
    if args.solve_kissat:
        core.solve_kissat(strong, "branch69-d25")

    base, second_mask = core.build_with_defect_bound(24)
    assert second_mask == mask
    assert len(base.clauses) == core.EXPECTED_BASE_CLAUSES
    for first, second in cases:
        cnf = base.copy()
        core.add_center_case(cnf, first, second)
        name = f"branch69-exception-f{first}-g{second}"
        core.check_formula(cnf, EXPECTED_EXCEPTION_DIGESTS[(first, second)], name, output)
        if args.solve_kissat:
            core.solve_kissat(cnf, name)


if __name__ == "__main__":
    main()
