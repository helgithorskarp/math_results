#!/usr/bin/env python3
"""Exact four-colour complement of two reflected pairs in Z/109Z."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

MODULUS = 109
RATIOS = (4, 28, 37)


def formula(ratio):
    if ratio not in RATIOS:
        raise ValueError("expected one of the three exclusion representatives")
    p = MODULUS
    positions = [q for q in range(1, 55) if q not in (1, ratio)]
    variable = {(q, c): 4*j+c+1
                for j, q in enumerate(positions) for c in range(4)}
    clauses = []
    for q in positions:
        row = [variable[q, c] for c in range(4)]
        clauses.append(row)
        clauses.extend([[-v, -w] for v, w in itertools.combinations(row, 2)])

    forbidden = set()
    for x in range(1, p):
        for y in range(x, p):
            z = (x+y) % p
            if z == 0:
                continue
            points = tuple(min(q, p-q) for q in (x, y, z))
            if any(q in (1, ratio) for q in points):
                continue
            for c in range(4):
                forbidden.add(tuple(sorted({-variable[q, c] for q in points})))
    clauses.extend(map(list, sorted(forbidden, key=lambda row: (len(row), row))))

    # Relabel the four remaining colours by the order of first appearance.
    for j, q in enumerate(positions):
        for c in range(1, 4):
            clauses.append([-variable[q, c]] +
                           [variable[old, c-1] for old in positions[:j]])
    return len(variable), clauses


def dimacs(ratio):
    variables, clauses = formula(ratio)
    return (f"p cnf {variables} {len(clauses)}\n" +
            "".join(" ".join(map(str, row))+" 0\n" for row in clauses)).encode()


def write_formulas(output, ratios=RATIOS):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    result = []
    for ratio in ratios:
        content = dimacs(ratio)
        (output / f"ratio{ratio}.cnf").write_bytes(content)
        result.append({"ratio": ratio, "bytes": len(content),
                       "sha256": hashlib.sha256(content).hexdigest()})
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--ratios", nargs="+", type=int, choices=RATIOS, default=RATIOS)
    args = parser.parse_args()
    print(json.dumps(write_formulas(args.output, args.ratios), indent=2))
