#!/usr/bin/env python3
"""Verify and build the full-family certificate splits for Q7 LD29 branches 70--71."""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import pathlib
import sys


SOURCE_ROOT = pathlib.Path(__file__).resolve().parents[1]
KERNEL_PATH = SOURCE_ROOT / "q7_ld29_branch69_split" / "verify_branch69_split.py"
EXPECTED_KERNEL_SHA256 = "22f8450808d6a3b337bb93c9837841b6eaf966f1abd8ebf908975a0da2304fb0"
assert hashlib.sha256(KERNEL_PATH.read_bytes()).hexdigest() == EXPECTED_KERNEL_SHA256
sys.path.insert(0, str(KERNEL_PATH.parent))

import verify_branch69_split as shared  # noqa: E402


core = shared.core
BRANCHES = (70, 71)
EXPECTED_MASKS = {70: 1887, 71: 1915}
EXPECTED_LOCAL_DATA = {
    70: ((2, 2, 3, 3, 3, 5), 4, 12, 45, 26, 3),
    71: ((2, 2, 2, 4, 4, 4), 4, 12, 45, 26, 3),
}
EXPECTED_D24_SURVIVORS = (
    (5, (1, 1, 5, 5), 1, 0),
    (5, (2, 5, 5), 0, 0),
)
EXPECTED_CASES = {
    70: (
        (22, 111), (22, 113), (22, 123), (22, 125),
        (26, 111), (26, 113), (26, 119), (26, 125),
        (42, 95), (42, 113), (42, 119), (42, 125),
        (63, 70), (70, 113), (70, 123), (70, 125),
    ),
    71: (
        (14, 113), (14, 119), (14, 123), (14, 125),
        (28, 111), (28, 113), (28, 119), (28, 123),
        (42, 95), (42, 113), (42, 119), (42, 125),
        (63, 70), (70, 113), (70, 123), (70, 125),
    ),
}


def load_manifest() -> dict[str, dict[str, str]]:
    path = pathlib.Path(__file__).with_name("certificate_manifest.tsv")
    with path.open(newline="") as handle:
        rows = tuple(csv.DictReader(handle, delimiter="\t"))
    result = {row["formula"]: row for row in rows}
    expected_names = {
        *(f"branch{branch}-d25" for branch in BRANCHES),
        *(
            f"branch{branch}-exception-f{first}-g{second}"
            for branch in BRANCHES
            for first, second in EXPECTED_CASES[branch]
        ),
    }
    assert len(rows) == len(result) == 34
    assert set(result) == expected_names
    return result


MANIFEST = load_manifest()


def exceptional_cases(mask: int) -> tuple[tuple[int, int], ...]:
    return tuple(
        (first, second)
        for first, second in itertools.combinations(range(128), 2)
        if core.center_cost(first, mask) is not None
        and core.center_cost(second, mask) is not None
        and core.center_cost(first, mask) + core.center_cost(second, mask) <= 1
        and core.hamming_distance(first, second) >= 5
    )


def verify_branch(branch: int, mask: int) -> tuple[tuple[int, int], ...]:
    assert mask == EXPECTED_MASKS[branch]
    assert mask.bit_count() == 9
    assert core.local_data(mask) == EXPECTED_LOCAL_DATA[branch]
    assert core.raw_states(mask, 23) == ()
    survivors = tuple(
        filter(core.survives_defect_six_occupancy, core.raw_states(mask, 24))
    )
    assert survivors == EXPECTED_D24_SURVIVORS
    cases = exceptional_cases(mask)
    assert cases == EXPECTED_CASES[branch]
    assert all(
        core.center_cost(first, mask) + core.center_cost(second, mask) == 1
        for first, second in cases
    )
    print(
        f"PASS branch={branch} mask={mask} local_data={core.local_data(mask)} "
        f"exceptional_cases={len(cases)}"
    )
    return cases


def check(cnf, name: str, output: pathlib.Path | None, solve_kissat: bool) -> None:
    core.check_formula(cnf, MANIFEST[name]["cnf_sha256"], name, output)
    if solve_kissat:
        core.solve_kissat(cnf, name)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-directory")
    parser.add_argument("--solve-kissat", action="store_true")
    args = parser.parse_args()
    output = core.scratch_directory(args.write_directory) if args.write_directory else None

    for branch in BRANCHES:
        core.BRANCH = branch
        strong, mask = core.build_with_defect_bound(25)
        assert len(strong.clauses) == core.EXPECTED_BASE_CLAUSES
        cases = verify_branch(branch, mask)
        check(strong, f"branch{branch}-d25", output, args.solve_kissat)

        base, second_mask = core.build_with_defect_bound(24)
        assert second_mask == mask
        assert len(base.clauses) == core.EXPECTED_BASE_CLAUSES
        for first, second in cases:
            cnf = base.copy()
            core.add_center_case(cnf, first, second)
            name = f"branch{branch}-exception-f{first}-g{second}"
            check(cnf, name, output, args.solve_kissat)


if __name__ == "__main__":
    main()
