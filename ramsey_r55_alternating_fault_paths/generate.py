#!/usr/bin/env python3
"""Emit the alternating-C_(n-1)-normalized physical Ramsey CNF."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Iterator, Sequence


RED = 1
BLUE = 0


def fixed_color(n: int, pair: tuple[int, int]) -> int | None:
    """Color of the standard alternating cycle on 0..n-2, else None."""
    u, v = pair
    cycle_order = n - 1
    if v == u + 1 and v < cycle_order:
        return RED if u % 2 == 0 else BLUE
    if u == 0 and v == cycle_order - 1:
        # The closing edge has cycle-position cycle_order-1, which is odd.
        return BLUE
    else:
        return None


def variables(n: int) -> dict[tuple[int, int], int]:
    return {
        pair: index
        for index, pair in enumerate(
            (p for p in combinations(range(n), 2) if fixed_color(n, p) is None), 1
        )
    }


def clauses(
    n: int, variable: dict[tuple[int, int], int]
) -> Iterator[tuple[int, ...]]:
    """Use positive literals for red and negative literals for blue."""
    for five in combinations(range(n), 5):
        pairs = tuple(combinations(five, 2))
        colors = tuple(fixed_color(n, pair) for pair in pairs)
        free = tuple(variable[pair] for pair, color in zip(pairs, colors) if color is None)

        # A fixed blue edge already satisfies the no-red-K5 clause.  Fixed red
        # literals are false in that clause and are simply omitted.
        if BLUE not in colors:
            yield tuple(-index for index in free)

        # The color-reversed statement for the no-blue-K5 clause.
        if RED not in colors:
            yield free


def clause_line(clause: Sequence[int]) -> bytes:
    return (" ".join(map(str, clause)) + " 0\n").encode("ascii")


def summarize(n: int) -> dict[str, object]:
    if n < 7 or n % 2 == 0:
        raise ValueError("n must be odd and at least seven")
    variable = variables(n)
    state_hist: Counter[tuple[int, int]] = Counter()
    for five in combinations(range(n), 5):
        colors = [fixed_color(n, pair) for pair in combinations(five, 2)]
        state_hist[(colors.count(RED), colors.count(BLUE))] += 1

    clause_count = sum(1 for _ in clauses(n, variable))
    width_hist: Counter[int] = Counter()
    clause_digest = hashlib.sha256()
    header = f"p cnf {len(variable)} {clause_count}\n".encode("ascii")
    dimacs_digest = hashlib.sha256(header)
    dimacs_bytes = len(header)
    for clause in clauses(n, variable):
        width_hist[len(clause)] += 1
        line = clause_line(clause)
        clause_digest.update(line)
        dimacs_digest.update(line)
        dimacs_bytes += len(line)

    five_sets = math.comb(n, 5)
    return {
        "n": n,
        "physical_edges": math.comb(n, 2),
        "fixed_cycle_edges": n - 1,
        "fixed_red_edges": (n - 1) // 2,
        "fixed_blue_edges": (n - 1) // 2,
        "variables": len(variable),
        "five_sets": five_sets,
        "fixed_edge_color_histogram": {
            f"red_{red}_blue_{blue}": count
            for (red, blue), count in sorted(state_hist.items())
        },
        "clauses": clause_count,
        "unfixed_clauses": 2 * five_sets,
        "removed_satisfied_clauses": 2 * five_sets - clause_count,
        "clause_width_histogram": {
            str(width): width_hist[width] for width in sorted(width_hist)
        },
        "clause_stream_sha256": clause_digest.hexdigest(),
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
