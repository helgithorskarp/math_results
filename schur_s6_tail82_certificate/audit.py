"""Independently compare every CNF clause with the exact Schur constraints.

The audited semantics are one colour per integer, no monochromatic x+y=z
with x<=y (including x=y), and the literal suffix assignments.
"""

import argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent


def expected_clauses():
    n = 537
    tail = (HERE / "tail82.txt").read_text(encoding="ascii").strip()
    assert len(tail) == 82 and set(tail) <= set("123456")

    def lit(v, colour):
        return (v - 1) * 6 + colour

    clauses = set()
    for v in range(1, n + 1):
        clauses.add(tuple(lit(v, colour) for colour in range(1, 7)))
        for first in range(1, 7):
            for second in range(first + 1, 7):
                clauses.add((-lit(v, first), -lit(v, second)))

    triples = 0
    for x in range(1, n + 1):
        for y in range(x, n + 1 - x):
            z = x + y
            for colour in range(1, 7):
                if x == y:
                    clauses.add((-lit(x, colour), -lit(z, colour)))
                else:
                    clauses.add((-lit(x, colour), -lit(y, colour), -lit(z, colour)))
            triples += 1

    for v, digit in enumerate(tail, 456):
        clauses.add((lit(v, int(digit)),))
    assert triples == 72092 and len(clauses) == 441226
    return clauses


def check(path):
    expected = expected_clauses()
    actual = set()
    count = 0
    with Path(path).open(encoding="ascii") as stream:
        header = stream.readline().strip()
        assert header == "p cnf 3222 441226", header
        for line in stream:
            clause = tuple(map(int, line.split()))
            assert clause and clause[-1] == 0
            clause = clause[:-1]
            assert all(1 <= abs(literal) <= 3222 for literal in clause)
            assert clause not in actual, ("duplicate", clause)
            actual.add(clause)
            count += 1
    assert actual == expected, ("missing", len(expected - actual), "extra", len(actual - expected))
    assert count == 441226
    print("PASS exact_clauses=441226 triples=72092 tail_units=82 doubling_included=yes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    args = parser.parse_args()
    check(args.cnf)
