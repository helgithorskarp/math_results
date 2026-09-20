#!/usr/bin/env python3
"""Generate the rigid size-three Hall branch at order 15.

The full no-strong-tournament encoding is imported from the earlier
``strong_seymour_order15`` artifact.  This wrapper adds only consequences of
the written reduction for an ordinary degree-seven root whose minimal Hall
witness has size three.

Every generated file must live below /scratch; proof traces are evidence, not
repository source.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BASE_PATH = ROOT / "strong_seymour_order15" / "generate_cnf.py"


def load_base():
    spec = importlib.util.spec_from_file_location("strong_seymour_base", BASE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {BASE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_output(path: Path | None) -> None:
    if path is not None and (
        not path.is_absolute() or path.parts[:2] != ("/", "scratch")
    ):
        raise SystemExit("every output must be an absolute path below /scratch")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--map", type=Path)
    args = parser.parse_args()
    validate_output(args.output)
    validate_output(args.map)

    base = load_base()
    cnf, pool = base.build(root_degree=7, root_hall_size=3, mode="all")

    # Root 0 has A={1,...,7}, B={8,...,14}, minimal witness
    # S={1,2,3}, and Gamma(S)={8,9}.  Since the selected root is ordinary,
    # every member of B has a predecessor in A.  For D={10,...,14}, only
    # C={4,...,7} can be such a predecessor.
    for head in range(10, 15):
        cnf.append([base.arc(pool, tail, head) for tail in range(4, 8)])

    # The local reduction shows that the only residue not already forcing an
    # ordinary degree-six vertex is a directed triangle S with S -> Gamma(S).
    cnf.append([base.arc(pool, 1, 2)])
    cnf.append([base.arc(pool, 2, 3)])
    cnf.append([base.arc(pool, 3, 1)])
    for tail in range(1, 4):
        for head in range(8, 10):
            cnf.append([base.arc(pool, tail, head)])

    # Relabeling inside each remaining root region preserves every preceding
    # clause, so fix one representative arc in C, Gamma(S), and D.
    cnf.append([base.arc(pool, 4, 5)])
    cnf.append([base.arc(pool, 8, 9)])
    cnf.append([base.arc(pool, 10, 11)])

    cnf.to_file(args.output)
    if args.map is not None:
        args.map.write_text(
            json.dumps(
                {str(variable): list(name) for name, variable in pool.obj2id.items()},
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )

    print(
        json.dumps(
            {
                "base_generator_sha256": sha256(BASE_PATH),
                "case": "d7-s3-rigid",
                "clauses": len(cnf.clauses),
                "cnf_sha256": sha256(args.output),
                "variables": pool.top,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
