#!/usr/bin/env python3
"""Build one CNF whose models choose and four-colour one candidate repair."""
from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1] / "math_results"
SOURCE = REPO / "hadwiger_nelson_h516_k23free_edge_repair"
SOURCE_SHA256 = "7be0344d1811866429181436b2f85653fc801272a7a3efddad6125539e50cbbb"
ANCHOR = (1, 189, 192)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--encoding", choices=("sequential", "unary"), default="sequential")
    args = parser.parse_args()
    if sha256(SOURCE / "graph.json") != SOURCE_SHA256:
        raise ValueError("source graph identity")
    graph = json.loads((SOURCE / "graph.json").read_text())
    labels = graph["labels"]
    edges = [tuple(edge) for edge in graph["edges"]]
    edge_set = set(edges)
    if args.cases:
        cases = [tuple(sorted(map(int, line.split()))) for line in args.cases.read_text().splitlines() if line.strip()]
    else:
        classification = json.loads((HERE / "classification.json").read_text())
        cases = [
            tuple(row["edge"])
            for row in classification["cases"]
            if row["classification"] == "EXACTLY_FIVE_CHROMATIC_AND_NO_PLANE_UNIT_EDGE_MAP"
        ]
    if len(cases) != len(set(cases)) or not cases or not set(cases) <= edge_set:
        raise ValueError("case edges")
    if set(cases) & {tuple(sorted(pair)) for pair in combinations(ANCHOR, 2)}:
        raise ValueError("anchor deletion")
    position = {label: index for index, label in enumerate(labels)}
    gate_variables = [4 * len(labels) + i + 1 for i in range(len(cases))]
    gate = dict(zip(cases, gate_variables))
    auxiliary_variables = [] if args.encoding == "unary" else [
        4 * len(labels) + len(cases) + i + 1 for i in range(len(cases) - 1)
    ]
    selector_variables = gate_variables + auxiliary_variables

    clauses = []
    for label in labels:
        clauses.append([4 * position[label] + colour + 1 for colour in range(4)])
    for left, right in edges:
        if (left, right) in gate:
            prefix = [gate[(left, right)]]
        else:
            prefix = []
        for colour in range(4):
            clauses.append(prefix + [-4 * position[left] - colour - 1, -4 * position[right] - colour - 1])
    for colour, label in enumerate(ANCHOR):
        clauses.append([4 * position[label] + colour + 1])
    clauses.append(gate_variables)
    if args.encoding == "sequential":
        clauses.append([-gate_variables[0], auxiliary_variables[0]])
        for i in range(1, len(gate_variables) - 1):
            clauses.append([-gate_variables[i], auxiliary_variables[i]])
            clauses.append([-auxiliary_variables[i - 1], auxiliary_variables[i]])
            clauses.append([-gate_variables[i], -auxiliary_variables[i - 1]])
        clauses.append([-gate_variables[-1], -auxiliary_variables[-1]])
    else:
        clauses.extend([-a, -b] for a, b in combinations(gate.values(), 2))

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w") as f:
        f.write(f"p cnf {4 * len(labels) + len(selector_variables)} {len(clauses)}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")
    print(json.dumps({
        "variables": 4 * len(labels) + len(selector_variables),
        "clauses": len(clauses),
        "case_encoding": args.encoding,
        "repair_cases": [list(edge) for edge in cases],
        "sha256": sha256(args.out),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
