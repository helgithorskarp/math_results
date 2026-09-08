#!/usr/bin/env python3
"""Exact fixed-core extension CNFs; no symmetry or degree restrictions."""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("case", choices=["G1", "G2"])
    parser.add_argument("--inputs", type=Path, default=Path(__file__).with_name("INPUTS.json"))
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    core = json.loads(args.inputs.read_text())["graphs"][args.case]
    k, n = len(core), 18
    for i, row in enumerate(core):
        if len(row) != len(set(row)) or i in row or any(j < 0 or j >= k or i not in core[j] for j in row):
            raise ValueError("Invalid simple undirected core")
    pairs = list(it.combinations(range(n), 2))
    fixed = {e: int(e[1] in core[e[0]]) for e in pairs if e[1] < k}
    free = [e for e in pairs if e not in fixed]
    variables = {e: i + 1 for i, e in enumerate(free)}
    clauses = set()
    counts = {}

    def add(kind, literals):
        counts[kind] = counts.get(kind, 0) + 1
        clause = []
        for edge, positive in literals:
            if edge in fixed:
                if fixed[edge] == positive:
                    return
            else:
                v = variables[edge]
                clause.append(v if positive else -v)
        clauses.add(tuple(sorted(clause)))

    for vertices in it.combinations(range(n), 4):
        add("K4", [(e, False) for e in it.combinations(vertices, 2)])
    path_patterns = sorted({tuple(sorted(tuple(sorted((p[i], p[i + 1]))) for i in range(4)))
                            for p in it.permutations(range(5))})
    if len(path_patterns) != 60:
        raise RuntimeError("Incorrect path pattern count")
    local_pairs = list(it.combinations(range(5), 2))
    pattern_signs = [[e not in path for e in local_pairs] for path in path_patterns]
    for vertices in it.combinations(range(n), 5):
        edges = list(it.combinations(vertices, 2))
        add("I5", [(e, True) for e in edges])
        for signs in pattern_signs:
            add("P5", list(zip(edges, signs)))
    ordered = sorted(clauses, key=lambda c: (len(c), c))
    args.out.mkdir(parents=True, exist_ok=True)
    cnf = f"p cnf {len(free)} {len(ordered)}\n" + "".join(" ".join(map(str, c)) + " 0\n" for c in ordered)
    (args.out / f"{args.case}.cnf").write_text(cnf)
    metadata = {"case": args.case, "order": n, "core_order": k,
                "free_pairs": free, "variables": len(free), "clauses": len(ordered),
                "empty_clause": [] in [list(c) for c in ordered], "raw_constraints": counts,
                "cnf_sha256": hashlib.sha256(cnf.encode()).hexdigest(),
                "inputs_sha256": hashlib.sha256(args.inputs.read_bytes()).hexdigest()}
    (args.out / f"{args.case}.build.json").write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: value for key, value in metadata.items() if key != "free_pairs"}, sort_keys=True))


if __name__ == "__main__":
    main()
