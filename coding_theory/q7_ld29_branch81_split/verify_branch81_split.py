#!/usr/bin/env python3
"""Verify and build the full-family certificate split for Q7 LD29 branch 81."""

from __future__ import annotations

import argparse
import pathlib
import sys


SOURCE_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE_ROOT / "q7_ld29_branch79_split"))

import verify_branch79_split as core  # noqa: E402


BRANCH = 81
EXPECTED_MASK = 6010
EXPECTED_STRONG_DIGEST = "e87f121853c895100ba83341e78cda9e171df76881b6b8c2e552ce77e2581f4c"
EXPECTED_EXCEPTION_DIGESTS = {
    (42, 125): "9086a9b408fe92d9e061023a775c63ffdde8691a89b2df5ad84f44705b307419",
    (42, 119): "3ac7583d62653c75fea155e73f5404396245e9504d270714732bd1bb49cede89",
    (42, 95): "d824636ab88236f92dc1b8a2258da45d0f50b55a66c5a568127293b2226c524a",
    (28, 123): "55e5dfdf219d45a150f61fb4a412cf932105e5269964dcda88bfd3fdfb2203f6",
    (28, 119): "7fd8a821efae7a84041896174c21be35154ddd855d642bf9ae23239c67009184",
    (28, 111): "94f8d621409f63fdaa9679bf1a64b8b67991fd40ff99fde962d23c7b4cbaed8a",
    (56, 119): "ac0555d79944e44fe18eee0eeef82102c43009b5335c5822bd134c36675b1659",
    (56, 111): "c8ccc85d927b36fa7ff3d7b574a63ac704690f8143698175dba1ff302fe35f52",
    (56, 95): "389b5d07ef8576cb05a71e73f1d46624ece2fd783ef18b43d83853d1d1ef3a2b",
}
EXPECTED_CASES = tuple(EXPECTED_EXCEPTION_DIGESTS)


def configure_core() -> None:
    core.BRANCH = BRANCH
    core.EXPECTED_MASK = EXPECTED_MASK


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-directory")
    parser.add_argument("--solve-kissat", action="store_true")
    args = parser.parse_args()
    output = core.scratch_directory(args.write_directory) if args.write_directory else None

    configure_core()
    strong, mask = core.build_with_defect_bound(25)
    assert len(strong.clauses) == core.EXPECTED_BASE_CLAUSES
    cases = core.verify_split(mask)
    assert cases == EXPECTED_CASES
    core.check_formula(strong, EXPECTED_STRONG_DIGEST, "branch81-d25", output)
    if args.solve_kissat:
        core.solve_kissat(strong, "branch81-d25")

    base, second_mask = core.build_with_defect_bound(24)
    assert second_mask == mask
    assert len(base.clauses) == core.EXPECTED_BASE_CLAUSES
    for first, second in cases:
        cnf = base.copy()
        core.add_center_case(cnf, first, second)
        name = f"branch81-exception-f{first}-g{second}"
        core.check_formula(cnf, EXPECTED_EXCEPTION_DIGESTS[(first, second)], name, output)
        if args.solve_kissat:
            core.solve_kissat(cnf, name)


if __name__ == "__main__":
    main()
