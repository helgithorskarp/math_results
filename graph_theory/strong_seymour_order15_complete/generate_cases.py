#!/usr/bin/env python3
"""Generate the 19 structurally certified size-six Hall-witness cases."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path


SCORE_SEQUENCES = [
    (1, 1, 1, 3, 4, 5),
    (1, 1, 1, 4, 4, 4),
    (1, 1, 2, 2, 4, 5),
    (1, 1, 2, 3, 3, 5),
    (1, 1, 2, 3, 4, 4),
    (1, 1, 3, 3, 3, 4),
    (1, 2, 2, 2, 3, 5),
    (1, 2, 2, 2, 4, 4),
    (1, 2, 2, 3, 3, 4),
    (1, 2, 3, 3, 3, 3),
    (2, 2, 2, 2, 2, 5),
    (2, 2, 2, 2, 3, 4),
    (2, 2, 2, 3, 3, 3),
]
REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
BASE_PATH = REPOSITORY_ROOT / "strong_seymour_order15" / "generate_cnf.py"
EXPECTED_PATH = Path(__file__).with_name("EXPECTED.json")
EXPECTED_BASE_SHA256 = (
    "5dda45c3e5e9aeeb286bfa6844e911bf8d9cb47918e2cf21f0fb00e2482d0517"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load_base():
    spec = importlib.util.spec_from_file_location("strong_seymour_base", BASE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {BASE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def internal(base, pool, vertex: int) -> list[int]:
    return [
        base.arc(pool, vertex, other)
        for other in range(1, 7)
        if other != vertex
    ]


def hall(base, pool, vertex: int) -> list[int]:
    return [base.arc(pool, vertex, head) for head in range(8, 13)]


def add_common(base, cnf, pool) -> None:
    # At root 0, S=1..6, C={7}, R=8..12, and D=13..14.  Since S sends
    # no arc to D, ordinaryness of the root forces the sole c in C to reach D.
    cnf.append([base.arc(pool, 7, 13)])
    cnf.append([base.arc(pool, 7, 14)])

    # R and D are independently relabelable in every signature.
    cnf.append([base.arc(pool, 8, 9)])
    cnf.append([base.arc(pool, 13, 14)])


def equals(base, cnf, pool, literals: list[int], bound: int) -> None:
    cnf.extend(
        base.CardEnc.equals(
            literals,
            bound=bound,
            vpool=pool,
            encoding=base.EncType.seqcounter,
        ).clauses
    )


def atleast(base, cnf, pool, literals: list[int], bound: int) -> None:
    cnf.extend(
        base.CardEnc.atleast(
            literals,
            bound=bound,
            vpool=pool,
            encoding=base.EncType.seqcounter,
        ).clauses
    )


def build_tight(base, score: int):
    cnf, pool = base.build(root_degree=7, root_hall_size=6, mode="all")
    add_common(base, cnf, pool)
    equals(base, cnf, pool, internal(base, pool, 1), score)
    equals(base, cnf, pool, hall(base, pool, 1), 5 - score)

    # Vertex 1 is the chosen tight vertex.  The other five S vertices remain
    # freely relabelable, so one representative internal arc is harmless.
    cnf.append([base.arc(pool, 2, 3)])
    return cnf, pool


def build_strict(base, scores: tuple[int, ...]):
    cnf, pool = base.build(root_degree=7, root_hall_size=6, mode="all")
    add_common(base, cnf, pool)
    for vertex, score in enumerate(scores, start=1):
        equals(base, cnf, pool, internal(base, pool, vertex), score)
        atleast(base, cnf, pool, hall(base, pool, vertex), 6 - score)

    # Scores sort the vertices.  Within each equal-score block, swapping the
    # first two labels reverses their mutual arc and preserves all constraints.
    start = 0
    while start < len(scores):
        end = start + 1
        while end < len(scores) and scores[end] == scores[start]:
            end += 1
        if end - start >= 2:
            cnf.append([base.arc(pool, start + 1, start + 2)])
        start = end
    return cnf, pool


def write(path: Path, cnf, pool, case: str) -> dict[str, object]:
    cnf.to_file(path)
    return {
        "case": case,
        "clauses": len(cnf.clauses),
        "cnf_bytes": path.stat().st_size,
        "cnf_sha256": sha256(path),
        "variables": pool.top,
    }


def validate_output(path: Path) -> None:
    if not path.is_absolute() or path.parts[:2] != ("/", "scratch"):
        raise SystemExit("the output directory must be an absolute path below /scratch")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    validate_output(args.output)
    args.output.mkdir(parents=True, exist_ok=True)

    base_sha256 = sha256(BASE_PATH)
    assert base_sha256 == EXPECTED_BASE_SHA256
    base = load_base()
    records = []
    for score in range(6):
        case = f"tight-p{score}"
        cnf, pool = build_tight(base, score)
        records.append(write(args.output / f"s6-{case}.cnf", cnf, pool, case))
    for index, scores in enumerate(SCORE_SEQUENCES):
        case = f"strict-score-{index:02d}"
        cnf, pool = build_strict(base, scores)
        records.append(write(args.output / f"s6-{case}.cnf", cnf, pool, case))

    expected = json.loads(EXPECTED_PATH.read_text())
    expected_records = [
        {
            "case": case,
            "clauses": values["clauses"],
            "cnf_bytes": values["cnf_bytes"],
            "cnf_sha256": values["cnf_sha256"],
            "variables": values["variables"],
        }
        for case, values in expected["cases"].items()
    ]
    assert records == expected_records
    print(
        json.dumps(
            {
                "base_generator_sha256": base_sha256,
                "cases": records,
                "status": "GENERATED",
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
