#!/usr/bin/env python3
"""Regenerate and hash cleaned local-collision CNFs for branches 83--96."""

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
    83: (1023, "752930d0052e755230c08abcbfcfe42738fc431200a344d89b618d52dd4132d3"),
    84: (1791, "7f943b89342dcddad4a95a150c7a2bf8bfbf353ff6250cf287a9dca8b5ca8885"),
    85: (1919, "bc17d469ed940c8505b0036de40a9f5ca1286c2bf7e13c45de0d21ff64093621"),
    86: (2015, "68439ebdc0fad1ec9bc679d97712039154b321ae8ef9c92aea2a72d085b79a3c"),
    87: (2046, "4c4811e22fb9efaa6feeec11d527378aee48a096c88de8089209a1eac7365dce"),
    88: (4061, "841d1b78387c1c8ed113a60c6dce30978773c1d461b35671084241036b4bb695"),
    89: (5879, "91a65e9aea9e0ff8f4d55ccf5a9f037d4095c2c5a6d8447153ba8275f097a392"),
    90: (5951, "475476f0704a2598b26eb44d062f44e185940c677580971e8d2ee2551de275a1"),
    91: (6007, "b3e87d09cab27bd4ccca1b682ecb5159c3f2b654a2f98853a244a799f3a6691b"),
    92: (6011, "bc73dded850505fbac488d086b5bd01516a99b20d4ccb51710b7b6fdca62e5ff"),
    93: (6014, "0f6bf0edf4529168968fa6bb18447fd0da6da75083ce7fc1b40a16354a5c99d5"),
    94: (6654, "03a2f4116cee54b7741b2e20cecc08dbb6fa873217be0de4f084fb91b75210be"),
    95: (7071, "846625701f72bfb910c1e306f266515e303287e32f1f0b1109c13071e2be8af7"),
    96: (7101, "41df9c0b6a874a2494dc1e43086baff6980cf773bb2ec84865a98e9b0a99916c"),
}
EXPECTED_VARIABLES = 10432
EXPECTED_CLAUSES = 183619


def build(branch: int):
    defect_bound = 26 if branch == 89 else 25
    edge_bound = 12 if branch == 89 else 13
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
        assert mask.bit_count() == 10
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
