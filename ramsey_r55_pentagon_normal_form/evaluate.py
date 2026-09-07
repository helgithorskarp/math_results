#!/usr/bin/env python3
"""Evaluate all clauses, preserving multiplicity of physical five-sets."""
import argparse
import json
from pathlib import Path


def evaluate(cnf, bits):
    if len(bits) != 842 or any(c not in "01" for c in bits):
        raise ValueError("expected 842 binary values")
    values = [None] + [int(c) for c in bits]
    violated = []
    visited = 0
    with Path(cnf).open() as source:
        header = source.readline().split()
        if len(header) != 4 or header[:3] != ['p', 'cnf', '842']:
            raise ValueError("formula header")
        total = int(header[3])
        for visited, line in enumerate(source, 1):
            clause = list(map(int, line.split()))
            if not clause or clause[-1] != 0 or any(not 1 <= abs(x) <= 842 for x in clause[:-1]):
                raise ValueError("literal domain or terminator")
            if not any(values[abs(x)] == int(x > 0) for x in clause[:-1]):
                violated.append(visited)
        if visited != total:
            raise ValueError("clause count")
    return {"status": "EVALUATED_ALL_CLAUSES", "variables": 842,
            "clauses": visited, "violated_clauses": len(violated),
            "violated_rows_1_based": violated, "satisfies_formula": not violated}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('cnf', type=Path)
    parser.add_argument('bits', type=Path)
    args = parser.parse_args()
    print(json.dumps(evaluate(args.cnf, args.bits.read_text().strip()), sort_keys=True))
