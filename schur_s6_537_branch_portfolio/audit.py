"""Independently enumerate the exact clause multiset, including doublings."""
import argparse
from collections import Counter
from pathlib import Path

N = 537
K = 6


def variable(v, colour):
    return 6 * v - 6 + colour


def expected(branch):
    clauses = Counter()

    def add(literals):
        clauses[tuple(sorted(set(literals)))] += 1

    for colour in range(1, 7):
        if colour == 1:
            add([variable(1, colour)])
    for v in range(1, N + 1):
        add([variable(v, c) for c in range(1, 7)])
        for a in range(1, 7):
            for b in range(a + 1, 7):
                add([-variable(v, b), -variable(v, a)])
    triples = 0
    for x in range(1, N + 1):
        for y in range(x, N - x + 1):
            z = x + y
            triples += 1
            for c in range(1, 7):
                add([-variable(x, c), -variable(y, c), -variable(z, c)])
    add([variable(2, 2)])
    add([variable(N, branch)])
    assert triples == 72092 and sum(clauses.values()) == 441147
    return clauses


def check(path, branch):
    got = Counter()
    with Path(path).open(encoding="ascii") as stream:
        if stream.readline().strip() != "p cnf 3222 441147":
            raise AssertionError("wrong DIMACS header")
        for number, line in enumerate(stream, 1):
            literals = [int(t) for t in line.split()]
            if not literals or literals[-1] != 0 or 0 in literals[:-1]:
                raise AssertionError(f"bad DIMACS line {number}")
            clause = tuple(sorted(set(literals[:-1])))
            if any(abs(t) > 3222 or t == 0 or -t in clause for t in clause):
                raise AssertionError(f"invalid clause {number}")
            got[clause] += 1
    if number != 441147 or got != expected(branch):
        raise AssertionError("clause multiset mismatch")
    print(f"PASS branch={branch} vars=3222 clauses=441147 triples=72092 doubling=yes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("branch", type=int, choices=(1, 2, 3))
    parser.add_argument("cnf", type=Path)
    args = parser.parse_args()
    check(args.cnf, args.branch)
