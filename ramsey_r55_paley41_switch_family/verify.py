#!/usr/bin/env python3
"""Independent physical truth-table reconstruction; imports no producer code."""
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


def tables():
    result = {}
    trials = 0
    for k in (3, 4, 5):
        pairs = tuple(combinations(range(k), 2))
        table = {}
        for base in range(1 << len(pairs)):
            valid = []
            for spin in range(1 << k):
                colors = {(base >> bit & 1) ^ (spin >> u & 1) ^ (spin >> v & 1)
                          for bit, (u, v) in enumerate(pairs)}
                trials += 1
                if len(colors) == 1:
                    valid.append((colors.pop(), spin))
            table[base] = valid
        result[k] = table
    return result, trials


def parse(path):
    clauses = []
    with path.open() as stream:
        words = next(stream).split()
        require(len(words) == 4 and words[:3] == ["p", "cnf", "123"],
                "Bad DIMACS header")
        expected = int(words[3])
        for line in stream:
            row = tuple(map(int, line.split()))
            require(len(row) >= 2 and row[-1] == 0 and 0 not in row[:-1],
                    "Bad clause terminator")
            clause = row[:-1]
            require(all(1 <= abs(x) <= 123 for x in clause), "Variable outside family")
            require(len({abs(x) for x in clause}) == len(clause), "Repeated variable")
            require(list(map(abs, clause)) == sorted(map(abs, clause)), "Noncanonical order")
            clauses.append(clause)
    require(len(clauses) == expected, "DIMACS clause-count mismatch")
    require(len(set(clauses)) == expected, "Repeated clause")
    return set(clauses)


def check(path):
    supplied = parse(path)
    table, trials = tables()
    # Independent Paley convention: Euler's criterion, not residue enumeration.
    matrix = [[int(u != v and pow((u - v) % 41, 20, 41) == 1)
               for v in range(41)] for u in range(41)]
    require(all(matrix[u][v] == matrix[v][u] for u in range(41) for v in range(41)),
            "Nonsymmetric Paley graph")
    require(all(sum(row) == 20 for row in matrix), "Unexpected Paley degree")
    external = {}
    index = 41
    for u in range(43):
        for v in range(u + 1, 43):
            if u >= 41 or v >= 41:
                external[u, v] = index
                index += 1
    require(index == 124, "Wrong external-edge count")
    regenerated = set()
    family_subsets = Counter()
    for vertices in combinations(range(43), 5):
        core = tuple(v for v in vertices if v < 41)
        k = len(core)
        family_subsets[str(k)] += 1
        base = sum(matrix[u][v] << bit for bit, (u, v) in enumerate(combinations(core, 2)))
        for color, spin in table[k][base]:
            if core[0] == 0 and spin & 1:
                continue
            assignment = {vertex: spin >> j & 1 for j, vertex in enumerate(core) if vertex}
            for u, v in combinations(vertices, 2):
                if v >= 41:
                    assignment[external[u, v]] = color
            clause = tuple(-v if bit else v for v, bit in sorted(assignment.items()))
            require(clause not in regenerated, "Independent reconstruction duplicate")
            regenerated.add(clause)
    require(supplied == regenerated,
            f"Formula mismatch: {len(supplied-regenerated)} extra, {len(regenerated-supplied)} missing")
    return {"status": "VERIFIED_EXACT_FULL_FAMILY_CNF", "clauses": len(supplied),
            "truth_table_cases": trials, "physical_five_subsets": sum(family_subsets.values()),
            "five_subsets_by_core_size": dict(sorted(family_subsets.items())),
            "cnf_sha256": sha256(path.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    report = check(args.cnf)
    text = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")
    print(json.dumps({"verification_seconds": time.monotonic() - start}))


if __name__ == "__main__":
    main()
