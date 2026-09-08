#!/usr/bin/env python3
"""Small independent exact DPLL checker for the extracted physical cores."""
from functools import lru_cache
import json
from pathlib import Path
import sys
import time


def parse(path):
    variables = None
    clauses = []
    for line in path.read_text().splitlines():
        if not line or line.startswith("c"):
            continue
        if line.startswith("p "):
            _, typ, nv, nc = line.split()
            if typ != "cnf":
                raise ValueError("not CNF")
            variables, expected = int(nv), int(nc)
            continue
        lits = list(map(int, line.split()))
        if not lits or lits[-1] != 0:
            raise ValueError("unterminated clause")
        pos = neg = 0
        for lit in lits[:-1]:
            bit = 1 << (abs(lit) - 1)
            if lit > 0:
                pos |= bit
            else:
                neg |= bit
        if pos & neg:
            raise ValueError("tautological clause")
        clauses.append((pos, neg))
    if variables is None or len(clauses) != expected:
        raise ValueError("bad header")
    return variables, tuple(clauses)


def decide(variables, clauses):
    full = (1 << variables) - 1
    counts = {"calls": 0, "cache_hits": 0, "conflicts": 0,
              "units": 0, "branches": 0}

    @lru_cache(maxsize=None)
    def search(true, false):
        counts["calls"] += 1
        while True:
            changed = False
            all_satisfied = True
            for pos, neg in clauses:
                if pos & true or neg & false:
                    continue
                all_satisfied = False
                remaining = (pos | neg) & ~(true | false)
                if not remaining:
                    counts["conflicts"] += 1
                    return False
                if remaining & (remaining - 1) == 0:
                    counts["units"] += 1
                    if pos & remaining:
                        true |= remaining
                    else:
                        false |= remaining
                    changed = True
                    break
            if all_satisfied:
                return True
            if not changed:
                break

        scores = [0] * variables
        for pos, neg in clauses:
            if pos & true or neg & false:
                continue
            remaining = (pos | neg) & ~(true | false)
            while remaining:
                bit = remaining & -remaining
                scores[bit.bit_length() - 1] += 1
                remaining -= bit
        unassigned = full & ~(true | false)
        if not unassigned:
            raise AssertionError("unassigned state inconsistency")
        candidates = [i for i in range(variables) if unassigned >> i & 1]
        variable = max(candidates, key=lambda i: (scores[i], -i))
        bit = 1 << variable
        counts["branches"] += 1
        before = search.cache_info().hits
        if search(true | bit, false):
            counts["cache_hits"] += search.cache_info().hits - before
            return True
        if search(true, false | bit):
            counts["cache_hits"] += search.cache_info().hits - before
            return True
        counts["cache_hits"] += search.cache_info().hits - before
        return False

    sat = search(0, 0)
    counts["cached_states"] = search.cache_info().currsize
    return sat, counts


def main(paths):
    rows = []
    for path in paths:
        start = time.monotonic()
        variables, clauses = parse(path)
        sat, counts = decide(variables, clauses)
        rows.append({"path": str(path), "variables": variables,
                     "clauses": len(clauses), "satisfiable": sat,
                     "elapsed_seconds": time.monotonic() - start, **counts})
        if sat:
            raise AssertionError(f"unexpected SAT core {path}")
    print(json.dumps(rows, indent=2, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: dpll_check.py CORE.cnf ...")
    main([Path(x) for x in sys.argv[1:]])
