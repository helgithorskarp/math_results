#!/usr/bin/env python3
"""Emit the exact Hamilton-cycle-normalized physical Ramsey(5,5;n) CNF."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from itertools import combinations
from pathlib import Path
from typing import Iterable, Iterator, Sequence


def cycle_edge(n: int, u: int, v: int) -> bool:
    return (u - v) % n in (1, n - 1)


def variables(n: int) -> dict[tuple[int, int], int]:
    return {
        pair: index
        for index, pair in enumerate(
            (p for p in combinations(range(n), 2) if not cycle_edge(n, *p)), 1
        )
    }


def clauses(n: int, variable: dict[tuple[int, int], int]) -> Iterator[tuple[int, ...]]:
    for five in combinations(range(n), 5):
        pairs = tuple(combinations(five, 2))
        free = tuple(variable[pair] for pair in pairs if pair in variable)
        # At least one free pair is blue.  Fixed cycle pairs are red.
        yield tuple(-x for x in free)
        # If there is no fixed red pair, at least one free pair must be red.
        if len(free) == 10:
            yield free


def clause_line(clause: Sequence[int]) -> bytes:
    return (" ".join(map(str, clause)) + " 0\n").encode("ascii")


def summarize(n: int) -> dict[str, object]:
    if n < 5:
        raise ValueError("n must be at least five")
    variable = variables(n)
    cycle_hist: dict[int, int] = {}
    for five in combinations(range(n), 5):
        fixed = sum(cycle_edge(n, *p) for p in combinations(five, 2))
        cycle_hist[fixed] = cycle_hist.get(fixed, 0) + 1
    clause_count = math.comb(n, 5) + cycle_hist.get(0, 0)
    width_hist: dict[int, int] = {}
    digest = hashlib.sha256()
    dimacs_digest = hashlib.sha256()
    header = f"p cnf {len(variable)} {clause_count}\n".encode("ascii")
    dimacs_digest.update(header)
    dimacs_bytes = len(header)
    observed = 0
    for clause in clauses(n, variable):
        observed += 1
        width_hist[len(clause)] = width_hist.get(len(clause), 0) + 1
        line = clause_line(clause)
        digest.update(line)
        dimacs_digest.update(line)
        dimacs_bytes += len(line)
    if observed != clause_count:
        raise AssertionError((observed, clause_count))
    return {
        "n": n,
        "physical_edges": math.comb(n, 2),
        "fixed_cycle_edges": n,
        "variables": len(variable),
        "five_sets": math.comb(n, 5),
        "cycle_edge_histogram": {str(k): cycle_hist[k] for k in sorted(cycle_hist)},
        "clauses": clause_count,
        "unfixed_clauses": 2 * math.comb(n, 5),
        "removed_satisfied_clauses": math.comb(n, 5) - cycle_hist.get(0, 0),
        "clause_width_histogram": {str(k): width_hist[k] for k in sorted(width_hist)},
        "clause_stream_sha256": digest.hexdigest(),
        "dimacs_bytes": dimacs_bytes,
        "dimacs_sha256": dimacs_digest.hexdigest(),
    }


def write_dimacs(n: int, path: Path) -> dict[str, object]:
    summary = summarize(n)
    variable = variables(n)
    with path.open("wb") as handle:
        handle.write(f"p cnf {len(variable)} {summary['clauses']}\n".encode("ascii"))
        for clause in clauses(n, variable):
            handle.write(clause_line(clause))
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=43)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()
    result = write_dimacs(args.n, args.output) if args.output else summarize(args.n)
    if args.summary or not args.output:
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
