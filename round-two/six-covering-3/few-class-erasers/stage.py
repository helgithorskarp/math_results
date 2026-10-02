"""Necessary cheap-erasure cuts AFTER precisely all36 free base phases."""

import argparse
import json
from pathlib import Path

from model import divisors, parent_cut, signature

PREFIX = ((8, 0), (9, 0), (10, 1), (14, 1), (12, 10))
BASE = [n for n in range(8, 2521) if 2520 % n == 0 and n not in {m for m, _ in PREFIX}]


def evaluate(phases):
    if not isinstance(phases, list) or any(not isinstance(row, list) or len(row) != 2 for row in phases):
        raise ValueError("expected [modulus, phase] pairs")
    if any(type(n) is not int or type(a) is not int or n < 1 or not 0 <= a < n for n, a in phases):
        raise ValueError("invalid original modulus or phase")
    if sorted(n for n, a in phases) != BASE:
        raise ValueError("choose exactly one phase at each of the36 free base labels")
    chosen = list(PREFIX) + phases
    holes = [[] for _ in range(8)]
    for x in range(2520):
        if all(x % n != a for n, a in chosen):
            holes[x % 8].append(x % 315)
    prefixes = [r for r, v in enumerate(holes) if v]
    fibers = [sorted(holes[r]) for r in prefixes]
    return {"agent": "six-covering-3", "role": "researcher", "base_phases": 36,
            "prefixes": prefixes, "holes": fibers,
            "signatures": [signature(315, v) for v in fibers],
            "single_cost_cut": parent_cut(315, fibers, divisors(315), q=2),
            "pair_cost_cut": parent_cut(315, fibers, divisors(315), q=3),
            "scope": "Only this fully specified base assignment. A passing cut gives no tail witness."}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("base_phases", type=Path)
    args = ap.parse_args()
    print(json.dumps(evaluate(json.loads(args.base_phases.read_text())), sort_keys=True))
