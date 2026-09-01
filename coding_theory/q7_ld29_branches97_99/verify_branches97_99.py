#!/usr/bin/env python3
"""Regenerate and hash defect-18 CNFs for local branches 97--99."""

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
    97: (
        2047,
        "2f5dc4218d46c49fff6fc90839d9366aacd0297ce39236b0dc54ed20f327082f",
    ),
    98: (
        4063,
        "dca0244b77491d58e833a4b6a949f8a23717c6bd32044eab45f0a8f9fb9790fc",
    ),
    99: (
        5887,
        "30fd463e8dc5097774ab489660376a406cd8e4f5710caf25752bd363c305bd72",
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
        assert mask.bit_count() == 11

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
