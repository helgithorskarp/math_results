#!/usr/bin/env python3
"""Solver-free check: physical Paley K5 clauses plus a small ASCII DRAT proof.

This checker imports neither the formula generator nor the formula auditor.
It uses direct graph evaluation for the input clauses and plain repeated
unit propagation for RUP/RAT, retaining a multiset of frozensets. It is not a
formally verified checker.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import time


def require(condition, message):
    if not condition:
        raise ValueError(message)


def clause(line):
    values = list(map(int, line.split()))
    require(values and values[-1] == 0 and 0 not in values[:-1], "Bad clause terminator")
    values.pop()
    require(len(set(values)) == len(values), "Repeated literal")
    require(not any(-x in values for x in values), "Tautological input/proof clause")
    return values


def physical_core(path):
    lines = path.read_text().splitlines()
    header = lines[0].split()
    require(len(header) == 4 and header[:2] == ["p", "cnf"], "Bad header")
    require(40 <= int(header[2]) <= 123, "Unexpected header variable range")
    require(int(header[3]) == len(lines) - 1, "Bad core clause count")
    result = set()
    colors = Counter()
    widths = Counter()
    for line in lines[1:]:
        row = clause(line)
        require(len(row) in (4, 5), "Not a physical core K5 clause")
        require(all(1 <= abs(x) <= 40 for x in row), "Non-core variable")
        assignment = {abs(x): int(x < 0) for x in row}
        if len(row) == 4:
            assignment[0] = 0
        require(len(assignment) == 5, "Not five physical vertices")
        physical = {int(pow((u - v) % 41, 20, 41) == 1) ^ assignment[u] ^ assignment[v]
                    for u, v in combinations(sorted(assignment), 2)}
        require(len(physical) == 1, "Clause does not forbid an actual monochromatic K5")
        colors[str(physical.pop())] += 1
        widths[str(len(row))] += 1
        frozen = frozenset(row)
        require(frozen not in result, "Duplicate core clause")
        result.add(frozen)
    return result, {"core_clauses": len(result), "core_widths": dict(sorted(widths.items())),
                    "core_colors": dict(sorted(colors.items())),
                    "core_variables": sorted({abs(x) for row in result for x in row})}


def rup(database, candidate):
    """Is a contradiction obtained from F plus the negations of candidate?"""
    if any(-x in candidate for x in candidate):
        return True  # A tautology is implied by every formula.
    true = {-x for x in candidate}
    changed = True
    while changed:
        changed = False
        for row in database:
            if row & true:
                continue
            remaining = [x for x in row if -x not in true]
            if not remaining:
                return True
            if len(remaining) == 1:
                true.add(remaining[0])
                changed = True
    return False


def verify_proof(database, path):
    database = Counter(database)
    statistics = Counter()
    empty = False
    for number, line in enumerate(path.read_text().splitlines(), 1):
        require(not empty, "Proof continues after the empty clause")
        deleted = line.startswith("d ")
        row = clause(line[2:] if deleted else line)
        frozen = frozenset(row)
        if deleted:
            statistics["deletions"] += 1
            if frozen not in database:
                statistics["absent_deletions"] += 1
            elif database[frozen] == 1:
                del database[frozen]
            else:
                database[frozen] -= 1
            continue
        statistics["additions"] += 1
        if rup(database, frozen):
            statistics["rup_additions"] += 1
        else:
            require(row, f"Empty clause fails RUP at line {number}")
            pivot = row[0]
            for other in database:
                if -pivot not in other:
                    continue
                resolvent = frozen | (other - {-pivot})
                require(rup(database, resolvent), f"RAT failed at line {number}, pivot {pivot}")
                statistics["rat_resolvents"] += 1
            statistics["rat_additions"] += 1
        database[frozen] += 1
        empty = not row
    require(empty, "No derived empty clause")
    return dict(sorted(statistics.items()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("core", type=Path)
    parser.add_argument("proof", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    database, report = physical_core(args.core)
    report["proof"] = verify_proof(database, args.proof)
    report.update({"status": "VERIFIED_PALEY41_SWITCH_CLASS_EXCLUSION",
                   "core_sha256": sha256(args.core.read_bytes()).hexdigest(),
                   "proof_sha256": sha256(args.proof.read_bytes()).hexdigest()})
    text = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")
    print(json.dumps({"certificate_verification_seconds": time.monotonic() - start}))


if __name__ == "__main__":
    main()
