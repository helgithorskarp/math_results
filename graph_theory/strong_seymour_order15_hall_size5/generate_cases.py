#!/usr/bin/env python3
"""Generate the nine exact size-five Hall-witness SAT cases.

Generated CNFs must be written below /scratch.  The source imports the
audited all-vertex no-strong encoding and adds only the structural branch,
ordinary-root coverage, proved D-degree flags, and harmless symmetries.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path


S = range(5)
S_PAIRS = [(first, second) for first in S for second in S if first < second]
S_PERMUTATIONS = list(itertools.permutations(S))
STRICT_TYPES = [2, 4, 8, 10, 12, 40, 41, 76]

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
BASE_PATH = REPOSITORY_ROOT / "strong_seymour_order15" / "generate_cnf.py"
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


def adjacency(bits: int) -> list[list[bool]]:
    graph = [[False] * 5 for _ in S]
    for shift, (first, second) in enumerate(S_PAIRS):
        graph[first][second] = bool(bits & (1 << shift))
        graph[second][first] = not graph[first][second]
    return graph


def encode_tournament(
    graph: list[list[bool]], permutation: tuple[int, ...]
) -> int:
    return sum(
        int(graph[permutation[first]][permutation[second]]) << shift
        for shift, (first, second) in enumerate(S_PAIRS)
    )


def enumerate_strict_types() -> list[int]:
    representatives = []
    for bits in range(1 << len(S_PAIRS)):
        graph = adjacency(bits)
        if min(sum(graph[vertex]) for vertex in S) < 1:
            continue
        if bits == min(
            encode_tournament(graph, permutation)
            for permutation in S_PERMUTATIONS
        ):
            representatives.append(bits)
    assert representatives == STRICT_TYPES
    return representatives


def add_common(base, cnf, pool) -> None:
    # At the normalized root, S=1..5, C=6..7, R=8..11, D=12..14.
    # Since S sends no arc to D, ordinaryness of the root forces every
    # d in D to be reached from C.
    for head in range(12, 15):
        cnf.append([base.arc(pool, 6, head), base.arc(pool, 7, head)])

    # Each d in D dominates x and all of S.  If d had degree six, it would
    # reach C through x and R through S, giving six second out-neighbors.
    # The inherited frontier excludes such an ordinary degree-six vertex.
    for vertex in range(12, 15):
        cnf.append([pool.id(("degree-at-least-seven", vertex))])

    # C, R, and D remain independently relabelable in every branch.
    cnf.append([base.arc(pool, 6, 7)])
    cnf.append([base.arc(pool, 8, 9)])
    cnf.append([base.arc(pool, 12, 13)])


def local_literals(base, pool, vertex: int) -> list[int]:
    """The eight literals counted by p(vertex)+q(vertex)."""
    return [
        *[
            base.arc(pool, vertex, other)
            for other in range(1, 6)
            if other != vertex
        ],
        *[base.arc(pool, vertex, head) for head in range(8, 12)],
    ]


def build_tight(base):
    cnf, pool = base.build(root_degree=7, root_hall_size=5, mode="all")
    add_common(base, cnf, pool)
    cnf.extend(
        base.CardEnc.equals(
            local_literals(base, pool, 1),
            bound=4,
            vpool=pool,
            encoding=base.EncType.seqcounter,
        ).clauses
    )
    # Vertex 1 is the normalized tight vertex; the remaining four members of
    # S can still be relabeled independently.
    cnf.append([base.arc(pool, 2, 3)])
    return cnf, pool


def build_strict(base, bits: int):
    cnf, pool = base.build(root_degree=7, root_hall_size=5, mode="all")
    add_common(base, cnf, pool)
    graph = adjacency(bits)
    for shift, (first, second) in enumerate(S_PAIRS):
        literal = base.arc(pool, first + 1, second + 1)
        cnf.append([literal if bits & (1 << shift) else -literal])
    for vertex in range(1, 6):
        cnf.extend(
            base.CardEnc.atleast(
                local_literals(base, pool, vertex),
                bound=5,
                vpool=pool,
                encoding=base.EncType.seqcounter,
            ).clauses
        )
    return cnf, pool, sorted(sum(graph[vertex]) for vertex in S)


def write_case(path: Path, cnf, pool, **metadata) -> dict:
    cnf.to_file(path)
    return {
        **metadata,
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
    strict_types = enumerate_strict_types()

    cnf, pool = build_tight(base)
    records = [
        write_case(
            args.output / "s5-tight.cnf",
            cnf,
            pool,
            case="tight",
            branch="tight",
        )
    ]
    for index, bits in enumerate(strict_types):
        cnf, pool, scores = build_strict(base, bits)
        records.append(
            write_case(
                args.output / f"s5-strict-type-{index:02d}.cnf",
                cnf,
                pool,
                case=f"strict-{index:02d}",
                branch="strict",
                score_sequence=scores,
                tournament_bits=bits,
            )
        )
    print(
        json.dumps(
            {
                "base_generator_sha256": base_sha256,
                "cases": records,
                "status": "GENERATED",
                "strict_tournament_types": strict_types,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
