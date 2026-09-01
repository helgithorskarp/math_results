#!/usr/bin/env python3
"""Regenerate and hash the cleaned D>=27 CNFs for branches 100--105."""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

from pysat.card import CardEnc, EncType


SOURCE_ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE_ROOT / "q7_ld29_family_reduction"))

from local_graphs import local_graph_assumptions, local_graph_representatives  # noqa: E402
from search_q7_ld29 import (  # noqa: E402
    add_nonisolated_variables,
    add_pair_indicators,
    add_singleton_variables,
    build as base_build,
    dimacs_bytes,
)


EXPECTED = {
    100: (6015, "aca52d0151fe1c517a336d2dd9a53a2ba5b3585b8539e6068ac647eb2e1fa113"),
    101: (6142, "c1caefd18c0496a55c19540168dc823388e11d167348c0f86616901940e7921e"),
    102: (6655, "54baf336bf5be635c4a8cf7c0de47753c538b7f49982f40c6c90b9d8c5b7efd5"),
    103: (7103, "957a1e8df8027d53570844d4de962aad74638792a7d480b7eb5786850d584169"),
    104: (7166, "985792613b77973a4b195cf26f2b20f6c0b6231d34c009ee10093ae004cc690a"),
    105: (8157, "b04bc5d1f2fb792db707bb4a8feeaefe0dabb50b2c469b44aa08661d219fa451"),
}
EXPECTED_VARIABLES = 10432
EXPECTED_CLAUSES = 183619


def build(branch: int):
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
            bound=7,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend(
        CardEnc.atleast(
            lits=singleton,
            bound=51,
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
            bound=9,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )

    mask = local_graph_representatives()[branch]
    cnf.extend([[literal] for literal in local_graph_assumptions(mask)])

    # The predecessor's distance-two separation clauses contain their two
    # endpoint literals twice.  Removing repeated occurrences is a
    # clause-by-clause Boolean identity and makes DRAT-trim warning-free.
    cnf.clauses[:] = [list(dict.fromkeys(clause)) for clause in cnf.clauses]
    return cnf, mask


def scratch_directory(raw: str) -> pathlib.Path:
    path = pathlib.Path(raw).resolve()
    if not path.is_relative_to("/scratch"):
        raise ValueError("CNF output must remain under /scratch")
    path.mkdir(parents=True, exist_ok=True)
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-directory")
    args = parser.parse_args()
    output = scratch_directory(args.write_directory) if args.write_directory else None

    for branch, (expected_mask, expected_digest) in EXPECTED.items():
        cnf, mask = build(branch)
        payload = dimacs_bytes(cnf)
        digest = hashlib.sha256(payload).hexdigest()
        assert mask == expected_mask
        assert mask.bit_count() == 11
        assert cnf.nv == EXPECTED_VARIABLES
        assert len(cnf.clauses) == EXPECTED_CLAUSES
        assert digest == expected_digest
        if output is not None:
            (output / f"branch-{branch}.cnf").write_bytes(payload)
        print(
            f"PASS branch={branch} mask={mask} variables={cnf.nv} "
            f"clauses={len(cnf.clauses)} sha256={digest}"
        )


if __name__ == "__main__":
    main()
