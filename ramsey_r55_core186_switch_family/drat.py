#!/usr/bin/env python3
"""Vendored RUP/RAT kernel: Paley41 source dac1474f64f1df456bfb4653bd97beb71063f23a.
Function bodies are copied verbatim; see imports.json. Not a new DRAT algorithm.
"""
from collections import Counter


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
