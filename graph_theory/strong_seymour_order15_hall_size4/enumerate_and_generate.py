#!/usr/bin/env python3
"""Classify size-four Hall signatures and generate their exact SAT cases.

All generated CNFs must be written below /scratch.  The source imports the
audited all-vertex encoding from the earlier ``strong_seymour_order15``
contribution and adds only the proved local signature and normalization
clauses.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path


S = range(4)
R = range(3)
S_PAIRS = [(first, second) for first in S for second in S if first < second]
S_PERMUTATIONS = list(itertools.permutations(S))
R_PERMUTATIONS = list(itertools.permutations(R))
EXPECTED_REPRESENTATIVES = [
    "000000111111111111",
    "000010111111111111",
    "001000111111011011",
    "001000111111011101",
    "001000111111011111",
    "001000111111111011",
    "001000111111111111",
    "001001111111001111",
    "001001111111011111",
    "001001111111111111",
]

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


def tournament(bits: int) -> list[list[bool]]:
    adjacency = [[False] * 4 for _ in S]
    for shift, (first, second) in enumerate(S_PAIRS):
        if bits & (1 << shift):
            adjacency[first][second] = True
        else:
            adjacency[second][first] = True
    return adjacency


def links(bits: int) -> list[list[bool]]:
    return [
        [bool(bits & (1 << (3 * tail + head))) for head in R]
        for tail in S
    ]


def forced_extra_seconds(
    adjacency: list[list[bool]], link: list[list[bool]], vertex: int
) -> set[tuple[str, int]]:
    """Return second in-neighbors forced using only S, R, and R -> x."""
    extras: set[tuple[str, int]] = set()
    direct_s = [other for other in S if adjacency[vertex][other]]
    direct_r = [head for head in R if link[vertex][head]]
    if direct_r:
        extras.add(("root", 0))
    for other in S:
        if adjacency[vertex][other]:
            continue
        if any(adjacency[midpoint][other] for midpoint in direct_s) or any(
            not link[other][head] for head in direct_r
        ):
            extras.add(("S", other))
    for head in R:
        if link[vertex][head]:
            continue
        if any(link[midpoint][head] for midpoint in direct_s):
            extras.add(("R", head))
    return extras


def encode(
    adjacency: list[list[bool]],
    link: list[list[bool]],
    s_permutation: tuple[int, ...],
    r_permutation: tuple[int, ...],
) -> str:
    bits = [
        int(adjacency[s_permutation[first]][s_permutation[second]])
        for first, second in S_PAIRS
    ]
    bits.extend(
        int(link[s_permutation[tail]][r_permutation[head]])
        for tail in S
        for head in R
    )
    return "".join(str(bit) for bit in bits)


def canonical(
    adjacency: list[list[bool]], link: list[list[bool]]
) -> str:
    return min(
        encode(adjacency, link, s_permutation, r_permutation)
        for s_permutation in S_PERMUTATIONS
        for r_permutation in R_PERMUTATIONS
    )


def enumerate_signatures() -> tuple[dict[str, int], collections.Counter[str]]:
    feasible = 0
    forced_ordinary = 0
    orbits: collections.Counter[str] = collections.Counter()
    for tournament_bits in range(1 << len(S_PAIRS)):
        adjacency = tournament(tournament_bits)
        internal_outdegrees = [sum(adjacency[vertex]) for vertex in S]
        for link_bits in range(1 << 12):
            link = links(link_bits)
            if any(sum(link[tail][head] for tail in S) < 2 for head in R):
                continue
            hall_outdegrees = [sum(link[vertex]) for vertex in S]
            if any(
                internal_outdegrees[vertex] + hall_outdegrees[vertex] < 3
                for vertex in S
            ):
                continue
            feasible += 1

            ordinary = any(
                internal_outdegrees[vertex] + hall_outdegrees[vertex] == 3
                and len(forced_extra_seconds(adjacency, link, vertex)) >= 2
                for vertex in S
            )
            if ordinary:
                forced_ordinary += 1
                continue
            orbits[canonical(adjacency, link)] += 1

    counts = {
        "all_patterns": (1 << len(S_PAIRS)) * (1 << 12),
        "degree_feasible": feasible,
        "forced_ordinary": forced_ordinary,
        "orbit_count": len(orbits),
        "surviving_labeled": sum(orbits.values()),
    }
    assert counts == {
        "all_patterns": 262144,
        "degree_feasible": 22368,
        "forced_ordinary": 21896,
        "orbit_count": 10,
        "surviving_labeled": 472,
    }
    assert sorted(orbits) == EXPECTED_REPRESENTATIVES
    assert collections.Counter(orbits.values()) == {8: 2, 24: 4, 72: 3, 144: 1}
    return counts, orbits


def add_signature(
    base, cnf, pool, representative: str
) -> None:
    bits = [int(value) for value in representative]
    shift = 0
    for first, second in S_PAIRS:
        literal = base.arc(pool, first + 1, second + 1)
        cnf.append([literal if bits[shift] else -literal])
        shift += 1
    for tail in S:
        for head in R:
            literal = base.arc(pool, tail + 1, head + 8)
            cnf.append([literal if bits[shift] else -literal])
            shift += 1
    assert shift == len(bits)


def generate_cases(output: Path, orbits: collections.Counter[str]) -> list[dict]:
    base = load_base()
    output.mkdir(parents=True, exist_ok=True)
    records = []
    for index, representative in enumerate(sorted(orbits)):
        cnf, pool = base.build(root_degree=7, root_hall_size=4, mode="all")

        # The selected root is ordinary.  Since S has no arcs to D, each
        # d in D={11,...,14} must be reached from C={5,6,7}.
        for head in range(11, 15):
            cnf.append([base.arc(pool, tail, head) for tail in range(5, 8)])
        add_signature(base, cnf, pool, representative)

        # C and D remain independently relabelable after fixing S and R.
        cnf.append([base.arc(pool, 5, 6)])
        cnf.append([base.arc(pool, 11, 12)])

        path = output / f"s4-orbit-{index:02d}.cnf"
        cnf.to_file(path)
        records.append(
            {
                "case": index,
                "clauses": len(cnf.clauses),
                "cnf_bytes": path.stat().st_size,
                "cnf_sha256": sha256(path),
                "orbit_size": orbits[representative],
                "representative": representative,
                "variables": pool.top,
            }
        )
    return records


def validate_output(path: Path) -> None:
    if not path.is_absolute() or path.parts[:2] != ("/", "scratch"):
        raise SystemExit("the output directory must be an absolute path below /scratch")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    validate_output(args.output)

    base_sha256 = sha256(BASE_PATH)
    assert base_sha256 == EXPECTED_BASE_SHA256
    counts, orbits = enumerate_signatures()
    report = {
        "base_generator_sha256": base_sha256,
        "cases": generate_cases(args.output, orbits),
        "classification": counts,
        "status": "GENERATED",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
