#!/usr/bin/env python3
"""Build the fixed template and a 24-variable consequence of Ramsey(5,5)."""
import argparse
import itertools as it
import json
from pathlib import Path

MODULES = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12],
           [13, 14, 15], [16, 17, 18]]
PAIRS = list(it.combinations(range(43), 2))
EDGE_ID = {p: i + 1 for i, p in enumerate(PAIRS)}


def template():
    fixed = {(0, v): 1 for v in range(1, 19)}
    for i, j in it.combinations(range(5), 2):
        color = int((j - i) in (1, 4))
        for u, v in it.product(MODULES[i], MODULES[j]):
            fixed[u, v] = color
    free = sorted(p for m in MODULES for p in it.combinations(m, 2))
    return fixed, free


def build():
    fixed, free = template()
    local_id = {p: i + 1 for i, p in enumerate(free)}
    sources = {}
    for color, size in ((1, 4), (0, 5)):
        for subset in it.combinations(range(1, 19), size):
            pairs = list(it.combinations(subset, 2))
            if any(p in fixed and fixed[p] != color for p in pairs):
                continue
            clause = tuple((1 - 2 * color) * local_id[p]
                           for p in pairs if p not in fixed)
            if clause not in sources:
                vertices = [0, *subset] if color else list(subset)
                sources[clause] = {"color": color, "vertices": vertices}
    clauses = list(sources)
    payload = {"n": 43, "modules": MODULES, "root": 0,
               "fixed": [[*p, c] for p, c in sorted(fixed.items())],
               "local_pairs": free,
               "premises": [{"local_clause": c, **sources[c]} for c in clauses]}
    cnf = f"p cnf {len(free)} {len(clauses)}\n"
    cnf += "".join(" ".join(map(str, (*c, 0))) + "\n" for c in clauses)
    return payload, cnf


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    payload, cnf = build()
    (args.out / "input.cnf").write_text(cnf)
    (args.out / "TEMPLATE.json").write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps({"variables": len(payload["local_pairs"]),
                      "clauses": len(payload["premises"]),
                      "fixed": len(payload["fixed"]),
                      "fixed_red": sum(e[2] for e in payload["fixed"]),
                      "clause_lengths": sorted(set(len(p["local_clause"])
                                                   for p in payload["premises"]))}))


if __name__ == "__main__":
    main()
