#!/usr/bin/env python3
"""Complete formula reconstruction by exhaustive small truth tables."""
import argparse
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
from physical import decode, rows, require, check_physical


def tables():
    table = {}
    for k in (4, 5):
        pairs = list(combinations(range(k), 2))
        table[k] = {}
        for base in range(1 << len(pairs)):
            options = []
            for spin in range(1 << k):
                colors = {(base >> i & 1) ^ (spin >> u & 1) ^ (spin >> v & 1)
                          for i, (u, v) in enumerate(pairs)}
                if len(colors) == 1:
                    options.append((spin, colors.pop()))
            table[k][base] = options
    return table


def expected(graph):
    n = len(graph)
    truth = tables()
    result = set()
    for vertices in combinations(range(n+1), 5):
        core = [v for v in vertices if v < n]
        base = sum(graph[u][v] << i for i, (u, v) in enumerate(combinations(core, 2)))
        for spin, color in truth[len(core)][base]:
            if core[0] == 0 and spin & 1:
                continue
            assignment = {v: spin >> i & 1 for i, v in enumerate(core) if v}
            if n in vertices:
                assignment.update({n+v: color for v in core})
            clause = frozenset(-v if bit else v for v, bit in assignment.items())
            require(clause not in result, "Duplicate reconstructed clause")
            result.add(clause)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("catalog", type=Path)
    parser.add_argument("parent", type=int)
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    graph = decode(args.catalog.read_text().splitlines()[args.parent])
    supplied = rows(args.cnf, 2*len(graph)-1)
    rebuilt = expected(graph)
    require(supplied == rebuilt, "Complete formula differs")
    report = {"status": "EXACT_FULL_FAMILY_CNF", "parent": args.parent,
              "clauses": len(supplied), "physical": check_physical(graph, supplied),
              "cnf_sha256": sha256(args.cnf.read_bytes()).hexdigest()}
    text = json.dumps(report, indent=2)+"\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
