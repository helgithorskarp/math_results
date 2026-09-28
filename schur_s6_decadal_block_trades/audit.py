"""Independent all-clause audit of one decadal block-permutation CNF."""

import argparse
import hashlib
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 537
SEED_SHA256 = "58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3"


def check(path, offset):
    assert 1 <= offset <= 10
    source = (HERE / "seed537.txt").read_bytes()
    assert hashlib.sha256(source).hexdigest() == SEED_SHA256
    old = [0] + [int(d) for d in source.decode("ascii").strip()]
    assert len(old) == N + 1 and set(old[1:]) == set(range(1, 7))

    # This arithmetic block lookup is independent of the encoder's interval
    # construction. The first interval ends at offset, the rest have width 10.
    def block(v):
        return 0 if v <= offset else 1 + (v - offset - 1) // 10

    rows = sorted({(block(v), old[v]) for v in range(1, N + 1)})
    index = {row: i for i, row in enumerate(rows)}

    def variable(row, colour):
        return 6 * index[row] + colour

    expected = Counter()
    for row in rows:
        expected[tuple(variable(row, c) for c in range(1, 7))] += 1
        for c in range(1, 7):
            for d in range(c + 1, 7):
                expected[(-variable(row, c), -variable(row, d))] += 1

    for b in range(max(row[0] for row in rows) + 1):
        palette = [row for row in rows if row[0] == b]
        for i, first in enumerate(palette):
            for second in palette[i + 1:]:
                for c in range(1, 7):
                    expected[(-variable(first, c), -variable(second, c))] += 1

    for row in rows:
        if row[0] == 0:
            expected[(variable(row, row[1]),)] += 1

    supports = set()
    defects = []
    triples = 0
    for x in range(1, N + 1):
        for y in range(x, N + 1 - x):
            z = x + y
            triples += 1
            if old[x] == old[y] == old[z]:
                defects.append((x, y, z))
            supports.add(tuple(sorted({(block(x), old[x]),
                                       (block(y), old[y]),
                                       (block(z), old[z])})))
    assert triples == 72092 and defects == [(12, 12, 24), (12, 24, 36)]
    assert all(len(support) > 1 for support in supports)
    for support in supports:
        for c in range(1, 7):
            expected[tuple(-variable(row, c) for row in support)] += 1

    actual = Counter()
    with Path(path).open(encoding="ascii") as stream:
        header = stream.readline().strip().split()
        assert len(header) == 4 and header[:2] == ["p", "cnf"]
        assert int(header[2]) == 6 * len(rows)
        for line in stream:
            literals = tuple(map(int, line.split()))
            assert literals and literals[-1] == 0
            clause = literals[:-1]
            assert all(1 <= abs(lit) <= 6 * len(rows) for lit in clause)
            actual[clause] += 1
        assert int(header[3]) == sum(actual.values())

    assert actual == expected, ("missing", sum((expected - actual).values()),
                                "extra", sum((actual - expected).values()))
    print(f"PASS offset={offset} blocks={1 + block(N)} rows={len(rows)} "
          f"supports={len(supports)} clauses={sum(actual.values())} "
          "seed_defects=2 all_clauses_audited=yes")
    return {"offset": offset, "blocks": 1 + block(N), "rows": len(rows),
            "supports": len(supports), "variables": 6 * len(rows),
            "clauses": sum(actual.values())}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("offset", type=int)
    parser.add_argument("cnf", type=Path)
    args = parser.parse_args()
    check(args.cnf, args.offset)
