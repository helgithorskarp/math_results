#!/usr/bin/env python3
"""Group orbit-closed clique cuts and reconstruct a vertex witness for each."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

sys.path.insert(0, str(Path(__file__).parent))
from search import cut_orbit  # noqa: E402


def find_witness(n: int, distances: set[int], target: int) -> list[int] | None:
    clauses = [[1]]
    for u in range(n):
        for v in range(u + 1, n):
            delta = abs(u - v)
            if min(delta, n - delta) not in distances:
                clauses.append([-(u + 1), -(v + 1)])
    card = CardEnc.atleast(lits=list(range(1, n + 1)), bound=target,
                           top_id=n, encoding=EncType.seqcounter)
    clauses.extend(card.clauses)
    with Solver(name="cadical195", bootstrap_with=clauses) as solver:
        if not solver.solve():
            return None
        vertices = [lit - 1 for lit in solver.get_model() if 1 <= lit <= n]
    return vertices[:target]


def pair_distances(n: int, vertices: list[int]) -> set[int]:
    result = set()
    for i, u in enumerate(vertices):
        for v in vertices[i + 1:]:
            delta = abs(u - v)
            result.add(min(delta, n - delta))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--existing", type=Path,
                        help="reuse already reconstructed orbit records")
    args = parser.parse_args()

    data = json.loads(args.checkpoint.read_text())
    n = data["n"]
    target = data["k"]
    all_cuts = sorted({tuple(cut) for cut in data["cuts"]})
    cut_keys = set(all_cuts)
    initial = len(all_cuts)
    covered: set[tuple[int, ...]] = set()
    records = []
    if args.existing:
        old = json.loads(args.existing.read_text())
        if old["n"] != n or old["target"] != target:
            raise ValueError("existing witness parameters do not match")
        records = old["orbit_representatives"]
        for record in records:
            for image in cut_orbit(n, record["cut"]):
                key = tuple(image)
                if key in cut_keys:
                    covered.add(key)
    started = time.monotonic()
    for representative in all_cuts:
        if representative in covered:
            continue
        if args.limit is not None and len(records) >= args.limit:
            break
        orbit = cut_orbit(n, list(representative))
        for image in orbit:
            key = tuple(image)
            if key in cut_keys:
                covered.add(key)
        clique = find_witness(n, set(representative), target)
        if clique is None:
            raise RuntimeError("cut has no target-clique witness")
        observed = pair_distances(n, clique)
        if not observed <= set(representative):
            raise AssertionError("reconstructed witness does not validate cut")
        records.append({
            "cut": list(representative),
            "vertices": clique,
            "orbit_size": len(orbit),
        })
        if len(records) % 1000 == 0:
            print(f"orbits={len(records)} remaining={initial - len(covered)} "
                  f"elapsed={time.monotonic() - started:.1f}s", flush=True)

    output = {
        "n": n,
        "target": target,
        "input_cut_count": initial,
        "remaining_cut_count": initial - len(covered),
        "orbit_representatives": records,
    }
    args.output.write_text(json.dumps(output, separators=(",", ":")) + "\n")
    print(json.dumps({k: v for k, v in output.items()
                      if k != "orbit_representatives"}))
    return 0 if len(covered) == initial else 2


if __name__ == "__main__":
    raise SystemExit(main())
