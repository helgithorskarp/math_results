#!/usr/bin/env python3
"""Independently check a CaDiCaL SAT model and its physical good45 meaning."""

import argparse
from itertools import combinations


def read_model(path):
    status = None
    assignment = {}
    for line in open(path):
        if line.startswith("s "):
            status = line.strip()
        elif line.startswith("v "):
            for value in map(int, line.split()[1:]):
                if value:
                    assignment[abs(value)] = value > 0
    if status != "s SATISFIABLE":
        raise SystemExit(f"not a SAT model: {status}")
    return assignment


def check_cnf(path, assignment):
    variables = clauses_expected = clauses = 0
    with open(path) as handle:
        for line in handle:
            if line.startswith("c") or not line.strip():
                continue
            if line.startswith("p"):
                _, _, variables, clauses_expected = line.split()
                variables, clauses_expected = int(variables), int(clauses_expected)
                continue
            literals = list(map(int, line.split()))
            assert literals[-1] == 0
            clauses += 1
            if not any(assignment.get(abs(x), False) == (x > 0) for x in literals[:-1]):
                raise SystemExit(f"unsatisfied CNF clause {clauses}")
    if clauses != clauses_expected or len(assignment) < variables:
        raise SystemExit("incomplete model or CNF count mismatch")
    return variables, clauses


def check_physical(assignment):
    edge = [[False] * 45 for _ in range(45)]
    variable = 0
    for j in range(1, 44):
        for i in range(j):
            variable += 1
            edge[i][j] = edge[j][i] = assignment[variable]
    assert variable == 946
    for i in range(22):
        edge[i][44] = edge[44][i] = True
    for vertices in combinations(range(45), 5):
        count = sum(edge[i][j] for i, j in combinations(vertices, 2))
        if count in (0, 10):
            raise SystemExit(f"forbidden five-set {vertices}, edges={count}")
    e_h = sum(edge[i][j] for i, j in combinations(range(22), 2))
    e_q = sum(not edge[i][j] for i, j in combinations(range(22, 44), 2))
    if e_h < 110 or e_h + e_q < 220:
        raise SystemExit("cardinality target failed")
    degrees = [sum(row) for row in edge]
    return e_h, e_q, min(degrees), max(degrees)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf")
    parser.add_argument("model")
    args = parser.parse_args()
    model = read_model(args.model)
    nvars, nclauses = check_cnf(args.cnf, model)
    eh, eq, dlo, dhi = check_physical(model)
    print("SAT_MODEL_VERIFIED", "variables", nvars, "clauses", nclauses,
          "eH", eh, "eQ", eq, "paired", eh+eq,
          "degree_range", f"{dlo}..{dhi}")
