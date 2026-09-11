#!/usr/bin/env python3
"""Exact, standard-library CNF for a k-set with no exp(G)-term zero sum.

The production instance is G=C3+C18 and k=21. No anchor is fixed.
Each fixed-total instance forbids complements of size k-exp(G).
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


class CNF:
    def __init__(self, primary_variables):
        self.nv = primary_variables
        self.clauses = []

    def new(self):
        self.nv += 1
        return self.nv

    def add(self, *literals):
        if not literals or any(not isinstance(x, int) or x == 0 for x in literals):
            raise ValueError("invalid clause")
        self.clauses.append(list(literals))

    def write(self, path):
        with Path(path).open("w") as out:
            out.write(f"p cnf {self.nv} {len(self.clauses)}\n")
            for clause in self.clauses:
                out.write(" ".join(map(str, clause)) + " 0\n")


def path_constraint(cnf, variables, weights, states, target, modulus=None):
    """Force a deterministic prefix path by forward implications.

    States are 0,...,states-1. Without modulus, overflow is forbidden.
    Auxiliary states need not be one-hot: the actual path is forced from
    its initial state, and every incorrect final state is explicitly false.
    Conversely, the actual path alone satisfies these clauses.
    """
    if len(variables) != len(weights) or not 0 <= target < states:
        raise ValueError("bad path parameters")
    q = [[cnf.new() for _ in range(states)] for _ in range(len(variables)+1)]
    for r in range(states):
        cnf.add(q[0][r] if r == 0 else -q[0][r])
    for i, (x, weight) in enumerate(zip(variables, weights)):
        for r in range(states):
            cnf.add(-q[i][r], x, q[i+1][r])
            successor = r + weight
            if modulus is not None:
                successor %= modulus
            if successor < states:
                cnf.add(-q[i][r], -x, q[i+1][successor])
            else:
                cnf.add(-q[i][r], -x)
    for r in range(states):
        cnf.add(q[-1][r] if r == target else -q[-1][r])
    return q


def build(moduli=(3,18), size=21, total=(0,0)):
    m, n = moduli
    if m < 2 or n % m or not n <= size <= m*n:
        raise ValueError("require 2 <= m | n and n <= size <= m*n")
    if len(total) != 2 or not (0 <= total[0] < m and 0 <= total[1] < n):
        raise ValueError("total outside group")
    points = list(itertools.product(range(m), range(n)))
    xs = list(range(1,len(points)+1))
    cnf = CNF(len(points))
    paths = []
    paths.append(path_constraint(cnf, xs, [1]*len(xs), size+1, size))
    for coordinate, modulus in enumerate(moduli):
        paths.append(path_constraint(cnf, xs, [p[coordinate] for p in points],
                                     modulus, total[coordinate], modulus))
    forbidden = []
    for ids in itertools.combinations(range(len(points)), size-n):
        if all(sum(points[i][c] for i in ids) % moduli[c] == total[c]
               for c in range(2)):
            clause = [-i-1 for i in ids]
            # The empty-complement boundary is relevant only to semantic controls.
            if clause:
                cnf.add(*clause)
            else:
                cnf.clauses.append([])
            forbidden.append(list(ids))
    metadata = {"moduli":list(moduli), "size":size, "total":list(total),
                "points":points, "primary_variables":len(points),
                "variables":cnf.nv, "clauses":len(cnf.clauses),
                "forbidden_complements":len(forbidden)}
    return cnf, metadata, paths, forbidden


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("a",type=int)
    parser.add_argument("b",type=int)
    parser.add_argument("output",type=Path)
    args = parser.parse_args()
    cnf, metadata, _, _ = build(total=(args.a,args.b))
    cnf.write(args.output)
    metadata["cnf_sha256"] = hashlib.sha256(args.output.read_bytes()).hexdigest()
    args.output.with_suffix(".json").write_text(json.dumps(metadata,indent=2)+"\n")
    print(json.dumps({k:v for k,v in metadata.items() if k!="points"}))


if __name__ == "__main__":
    main()
