#!/usr/bin/env python3
"""Independent truth-pattern audit of a fixed-core extension formula."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def is_path(word, pairs):
    adjacency = [set() for _ in range(5)]
    for bit, (u, v) in enumerate(pairs):
        if word >> bit & 1:
            adjacency[u].add(v)
            adjacency[v].add(u)
    if sorted(map(len, adjacency)) != [1, 1, 2, 2, 2]:
        return False
    reached, pending = {0}, [0]
    while pending:
        for v in adjacency[pending.pop()]:
            if v not in reached:
                reached.add(v)
                pending.append(v)
    return len(reached) == 5


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("case", choices=["G1", "G2"])
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--inputs", type=Path, default=Path(__file__).with_name("INPUTS.json"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    rows = json.loads(args.inputs.read_text())["graphs"][args.case]
    size = len(rows)
    if any(len(set(row)) != len(row) or i in row or any(v < 0 or v >= size or i not in rows[v] for v in row)
           for i, row in enumerate(rows)):
        raise ValueError("Invalid core")
    edge_number, next_variable = {}, 1
    for u in range(18):
        for v in range(u + 1, 18):
            if v >= size:
                edge_number[u, v] = next_variable
                next_variable += 1

    lines = args.cnf.read_text().splitlines()
    header = lines.pop(0).split()
    if header[:2] != ["p", "cnf"] or int(header[2]) != next_variable - 1:
        raise ValueError("Wrong DIMACS header")
    observed = []
    for line in lines:
        values = list(map(int, line.split()))
        if not values or values[-1] != 0 or 0 in values[:-1]:
            raise ValueError("Malformed clause")
        clause = values[:-1]
        if len(set(clause)) != len(clause) or any(-v in clause or not 1 <= abs(v) < next_variable for v in clause):
            raise ValueError("Noncanonical clause")
        observed.append(tuple(sorted(clause)))
    if len(observed) != int(header[3]) or len(set(observed)) != len(observed):
        raise ValueError("Wrong clause count or duplicate")

    small_pairs = list(itertools.combinations(range(5), 2))
    path_words = [word for word in range(1024) if is_path(word, small_pairs)]
    if len(path_words) != 60:
        raise ValueError("Path classifier count mismatch")
    expected, core_obstructions = set(), {"K4": 0, "I5": 0, "P5": 0}
    for order in (4, 5):
        for vertices in itertools.combinations(range(18), order):
            edges = list(itertools.combinations(vertices, 2))
            words = [(63, "K4")] if order == 4 else [(0, "I5")] + [(w, "P5") for w in path_words]
            for word, kind in words:
                clause = []
                for bit, edge in enumerate(edges):
                    desired = word >> bit & 1
                    if edge in edge_number:
                        variable = edge_number[edge]
                        clause.append(-variable if desired else variable)
                    elif int(edge[1] in rows[edge[0]]) != desired:
                        break
                else:
                    expected.add(tuple(sorted(clause)))
                    if not clause:
                        core_obstructions[kind] += 1
    actual = set(observed)
    if actual != expected:
        raise ValueError(f"Formula differs: extra={len(actual-expected)}, missing={len(expected-actual)}")
    result = {"case": args.case, "audit": "PASS", "variables": next_variable - 1,
              "clauses": len(expected), "core_obstructions": core_obstructions,
              "path_words": len(path_words), "cnf_sha256": hashlib.sha256(args.cnf.read_bytes()).hexdigest(),
              "inputs_sha256": hashlib.sha256(args.inputs.read_bytes()).hexdigest()}
    args.out.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
