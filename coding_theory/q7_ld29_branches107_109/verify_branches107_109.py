#!/usr/bin/env python3
"""Regenerate and hash defect-18 CNFs for local branches 107--109."""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

SOURCE_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE_ROOT / "q7_ld29_defect18"))
sys.path.insert(0, str(SOURCE_ROOT / "q7_ld29_family_reduction"))

from local_graphs import local_graph_assumptions, local_graph_representatives  # noqa: E402
from search_q7_ld29 import dimacs_bytes  # noqa: E402
from search_q7_ld29_d18 import strengthened  # noqa: E402


EXPECTED = {
    107: (
        6143,
        "f41b48ef238d0682c8e30d54d6b53c1852d50ac709d8d732c5d4df9286f6e14e",
    ),
    108: (
        7167,
        "73a3d3fa288009acc5e342e3be0ffac5885f132e6467dceddf1395e028a37714",
    ),
    109: (
        8159,
        "6a736aad2eeb4e190d14414d800140bb41fc6c9b69d548c0ddfbd31712fce3e6",
    ),
}
EXPECTED_VARIABLES = 10432
EXPECTED_CLAUSES = 183619


def scratch_directory(raw: str) -> pathlib.Path:
    path = pathlib.Path(raw).resolve()
    if not path.is_relative_to("/scratch"):
        raise ValueError("CNF output must stay under /scratch")
    path.mkdir(parents=True, exist_ok=True)
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-directory")
    args = parser.parse_args()
    output = scratch_directory(args.write_directory) if args.write_directory else None

    representatives = local_graph_representatives()
    for branch, (expected_mask, expected_digest) in EXPECTED.items():
        mask = representatives[branch]
        assert mask == expected_mask
        assert mask.bit_count() == 12

        cnf = strengthened(pair_bounds=False, dynamic_pair_bound=False)
        cnf.extend([[literal] for literal in local_graph_assumptions(mask)])
        payload = dimacs_bytes(cnf)
        digest = hashlib.sha256(payload).hexdigest()

        assert cnf.nv == EXPECTED_VARIABLES
        assert len(cnf.clauses) == EXPECTED_CLAUSES
        assert digest == expected_digest

        if output is not None:
            (output / f"branch-{branch}.cnf").write_bytes(payload)

        print(
            f"PASS branch={branch} mask={mask} edges={mask.bit_count()} "
            f"variables={cnf.nv} clauses={len(cnf.clauses)} sha256={digest}"
        )


if __name__ == "__main__":
    main()
