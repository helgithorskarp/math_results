#!/usr/bin/env python3
"""Regenerate and hash the exact defect-18 CNF for local branch 106."""

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


BRANCH = 106
EXPECTED_MASK = 4095
EXPECTED_VARIABLES = 10432
EXPECTED_CLAUSES = 183619
EXPECTED_SHA256 = "b239814a4d9e7b86cad4bf07cedd0723515c2ca7bb86930fd8fa6e36082829f3"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-cnf")
    args = parser.parse_args()

    representatives = local_graph_representatives()
    mask = representatives[BRANCH]
    assert mask == EXPECTED_MASK
    assert mask.bit_count() == 12

    cnf = strengthened(pair_bounds=False, dynamic_pair_bound=False)
    cnf.extend([[literal] for literal in local_graph_assumptions(mask)])
    payload = dimacs_bytes(cnf)
    digest = hashlib.sha256(payload).hexdigest()

    assert cnf.nv == EXPECTED_VARIABLES
    assert len(cnf.clauses) == EXPECTED_CLAUSES
    assert digest == EXPECTED_SHA256

    if args.write_cnf:
        path = pathlib.Path(args.write_cnf).resolve()
        if not path.is_relative_to("/scratch"):
            raise ValueError("CNF output must stay under /scratch")
        path.write_bytes(payload)

    print(f"PASS branch={BRANCH} mask={mask} edges={mask.bit_count()}")
    print(f"PASS variables={cnf.nv} clauses={len(cnf.clauses)}")
    print(f"PASS sha256={digest}")


if __name__ == "__main__":
    main()
