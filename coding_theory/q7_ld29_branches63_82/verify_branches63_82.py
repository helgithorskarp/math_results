#!/usr/bin/env python3
"""Regenerate cleaned local-collision CNFs for branches 63--82."""

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
    63: (511, "b7bb7daa54a9867bb412501504847553f251ea045d224edb0ef9fcb5a36b7ca7"),
    64: (767, "264afff56486ad1588bfb4d64455d08b7672611df99e601c5fc72322138425c3"),
    65: (959, "43eca752ef184f70432bb21e801c47309507a12732e095587df3250eee2958ed"),
    66: (1022, "fa6b0df7ffed68dae5012d8eb27046100e41f4b14af13fb8d87031915bcb7470"),
    67: (1759, "1120cf1dc8f9af44a10c950b953a96ea33010a8520e3bc037343e19986606c10"),
    68: (1783, "f1114e5860c93de7730218e9f96f1bb8aa293e6e79b2d1362be59b2ea902c737"),
    69: (1789, "20a141cde2ad132b8652e9344b347d2500ba111b812d860357a0920711bd2c98"),
    70: (1887, "afe48c8b28790e34fcb63da81f81dbcff39ce44ef38426a2dc31a6032b172595"),
    71: (1915, "d09825105fa927c6e87bd30755d86704a0ffba37d136843829b6f8369685c105"),
    72: (1917, "b73ccbf643dab6725c1b2647a69fadcee505abcc030998d44236819b03cf482d"),
    73: (2013, "4d82b526b105005c3ac1ae6c4d719f8a5ac47b05baf8bb7329a2350504f4c6b6"),
    74: (2014, "752b25f57c6b7dc406f077a19084df460b983cfb734f64a5e5bcbc454a0d8178"),
    75: (4060, "18872266ef26ac72755e418b096fa8765b396404c5e4c042761ede053fbeae26"),
    76: (5875, "1df2f81704ffc5df56f98286a3489786d995e0d5b0b5c035117349873b8b1a49"),
    77: (5919, "db773ef5069bc97a02bf231213ed869c0320a43e1eafc1bc462f3f298d12bf5a"),
    78: (5943, "b09525af81f08daa18daee7ca2ebb92e1cbf4eaf480c1ffc2d09e80e2372c262"),
    79: (5949, "ef570e0774d5e9ed2d5cf14789fbaa84e7e4c6604a2169ee2c1dcd6c47f5d574"),
    80: (5950, "556e3c737cdf5c22c49224830aa3fe821f3ca40f63a244845b38c0d7fffb17c3"),
    81: (6010, "59e88e82f6b924a017d3d85b7988f6c6159ce9b5bf51fe6099ca6f91f46dc0c4"),
    82: (7100, "8677b4a362cada7159fce48a355ade47c8c797fdc232b2740035e8660c9d66b5"),
}
DEFECT_24 = {64, 68, 69, 70, 71, 76, 77, 78, 79, 80, 81}
EXPECTED_VARIABLES = 10432
EXPECTED_CLAUSES = 183619


def build(branch: int):
    defect_bound = 24 if branch in DEFECT_24 else 23
    edge_bound = 15 if defect_bound == 24 else 17
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
            bound=34 - defect_bound,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    cnf.extend(
        CardEnc.atleast(
            lits=singleton,
            bound=24 + defect_bound,
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
            bound=edge_bound,
            top_id=cnf.nv,
            encoding=EncType.totalizer,
        ).clauses
    )
    mask = local_graph_representatives()[branch]
    cnf.extend([[literal] for literal in local_graph_assumptions(mask)])
    cnf.clauses[:] = [list(dict.fromkeys(clause)) for clause in cnf.clauses]
    return cnf, mask, defect_bound


def scratch_directory(raw: str) -> pathlib.Path:
    path = pathlib.Path(raw).resolve()
    if not path.is_relative_to("/scratch"):
        raise ValueError("CNF output must remain under /scratch")
    path.mkdir(parents=True, exist_ok=True)
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-directory")
    parser.add_argument("--branch", type=int, choices=sorted(EXPECTED))
    args = parser.parse_args()
    output = scratch_directory(args.write_directory) if args.write_directory else None
    branches = [args.branch] if args.branch is not None else sorted(EXPECTED)

    for branch in branches:
        cnf, mask, defect_bound = build(branch)
        payload = dimacs_bytes(cnf)
        digest = hashlib.sha256(payload).hexdigest()
        expected_mask, expected_digest = EXPECTED[branch]
        assert mask == expected_mask
        assert mask.bit_count() == 9
        assert cnf.nv == EXPECTED_VARIABLES
        assert len(cnf.clauses) == EXPECTED_CLAUSES
        assert digest == expected_digest
        if output is not None:
            (output / f"branch-{branch}.cnf").write_bytes(payload)
        print(
            f"PASS branch={branch} mask={mask} defect_bound={defect_bound} "
            f"variables={cnf.nv} clauses={len(cnf.clauses)} sha256={digest}"
        )


if __name__ == "__main__":
    main()
