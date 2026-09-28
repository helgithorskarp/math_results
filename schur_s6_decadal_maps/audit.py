"""Independently compare every emitted clause with the block-map semantics."""

import argparse
import hashlib
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 537
SOURCE_HASH = "58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3"


def check(path):
    source = (HERE / "seed537.txt").read_bytes()
    assert hashlib.sha256(source).hexdigest() == SOURCE_HASH
    old = [0] + [int(digit) for digit in source.decode("ascii").strip()]
    assert len(old) == N + 1 and set(old[1:]) == set(range(1, 7))

    def block(v):
        return (v - 1) // 10

    rows = sorted({(block(v), old[v]) for v in range(1, N + 1)})
    index = {row: i for i, row in enumerate(rows)}

    def var(row, colour):
        return 6 * index[row] + colour

    expected = Counter()
    for row in rows:
        expected[tuple(var(row, c) for c in range(1, 7))] += 1
        for first in range(1, 7):
            for second in range(first + 1, 7):
                expected[(-var(row, first), -var(row, second))] += 1

    assert old[1] == 2
    expected[(var((block(1), old[1]), old[1]),)] += 1

    supports = set()
    bad = []
    triples = 0
    for x in range(1, N + 1):
        for y in range(x, N + 1 - x):
            z = x + y
            triples += 1
            if old[x] == old[y] == old[z]:
                bad.append((x, y, z))
            supports.add(tuple(sorted({(block(x), old[x]),
                                       (block(y), old[y]),
                                       (block(z), old[z])})))
    assert triples == 72092 and bad == [(12, 12, 24), (12, 24, 36)]
    assert len(supports) == 52754 and all(len(edge) > 1 for edge in supports)
    for edge in supports:
        for colour in range(1, 7):
            expected[tuple(-var(row, colour) for row in edge)] += 1

    actual = Counter()
    with Path(path).open(encoding="ascii") as stream:
        header = stream.readline().split()
        assert header == ["p", "cnf", "1578", "320733"]
        for line in stream:
            literals = tuple(map(int, line.split()))
            assert literals and literals[-1] == 0
            clause = literals[:-1]
            assert all(1 <= abs(lit) <= 1578 for lit in clause)
            actual[clause] += 1
    assert sum(actual.values()) == 320733
    assert actual == expected, ("missing", sum((expected - actual).values()),
                                "extra", sum((actual - expected).values()))
    print("PASS rows=263 supports=52754 clauses=320733 triples=72092 "
          "doubling=268 seed_defects=2 all_clauses_audited=yes")
    return {"blocks": 54, "rows": len(rows), "supports": len(supports),
            "variables": 6 * len(rows), "clauses": sum(actual.values()),
            "triples": triples}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    args = parser.parse_args()
    check(args.cnf)
