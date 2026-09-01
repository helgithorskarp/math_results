#!/usr/bin/env python3
"""Regenerate the dynamic-pair-bound CNFs for local branches 100--102."""

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
    100: (
        6015,
        "fc6a90431f7d71b665ea97ade16472825b6e3a956c3ec27bf8f53974f0731686",
    ),
    101: (
        6142,
        "c825e0cfd82e920c91b709b8ee0e87d685335819782c0104ab007c30872bf619",
    ),
    102: (
        6655,
        "a1a410dad343156c009b64dfbc750f1836f2df14701bf7f76d323891785951e4",
    ),
}
EXPECTED_VARIABLES = 90177
EXPECTED_CLAUSES = 1215249


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

        cnf = strengthened(pair_bounds=True, dynamic_pair_bound=True)
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
