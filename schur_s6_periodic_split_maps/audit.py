"""Independent x-first full-clause audit of periodic-split CNFs."""

import argparse
import hashlib
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE_HASH = "58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3"


def check(period, offset, path, phase=0):
    assert period in (2, 4)
    assert 1 <= offset <= 10
    assert 0 <= phase < period
    source = (HERE / "seed537.txt").read_bytes()
    assert hashlib.sha256(source).hexdigest() == SOURCE_HASH
    digits = source.decode("ascii").strip()
    assert len(digits) == 537 and set(digits) == set("123456")
    old = [0] + list(map(int, digits))

    # Different arithmetic formula and triple traversal from encode.py.
    def block(v):
        if v <= offset:
            return 0
        t = v - offset - 1
        old_block, within_block = divmod(t, 10)
        earlier_splits = max(0, 1 + (old_block - phase - 1) // period)
        current_split = old_block % period == phase and within_block >= 5
        return 1 + old_block + earlier_splits + current_split

    rows = sorted({(block(v), old[v]) for v in range(1, 538)})
    index = {row: i for i, row in enumerate(rows)}
    var = lambda row, colour: 6 * index[row] + colour
    expected = Counter()
    for row in rows:
        expected[tuple(var(row, c) for c in range(1, 7))] += 1
        for first in range(1, 7):
            for second in range(first + 1, 7):
                expected[(-var(row, first), -var(row, second))] += 1

    expected[(var(rows[0], 1),)] += 1
    for i in range(1, len(rows)):
        for colour in range(2, 7):
            expected[tuple([-var(rows[i], colour)]
                           + [var(rows[j], colour - 1) for j in range(i)])] += 1

    supports = set()
    defects = []
    triples = 0
    for x in range(1, 538):
        for y in range(x, 538 - x):
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
        for colour in range(1, 7):
            expected[tuple(-var(row, colour) for row in support)] += 1

    actual = Counter()
    with Path(path).open(encoding="ascii") as stream:
        header = stream.readline().split()
        assert header == ["p", "cnf", str(6 * len(rows)),
                          str(sum(expected.values()))]
        for line in stream:
            literals = list(map(int, line.split()))
            assert literals and literals[-1] == 0
            clause = tuple(literals[:-1])
            assert all(1 <= abs(lit) <= 6 * len(rows) for lit in clause)
            actual[clause] += 1
    assert actual == expected, (sum((expected - actual).values()),
                                sum((actual - expected).values()))
    rgs_clauses = 1 + 5 * (len(rows) - 1)
    print(f"PASS period={period} offset={offset} phase={phase} rows={len(rows)} supports={len(supports)} "
          f"clauses={sum(actual.values())} triples={triples} doubling=268 "
          f"rgs_clauses={rgs_clauses} exact_clause_multiset=yes")
    result = {"period": period, "offset": offset, "rows": len(rows),
              "supports": len(supports), "variables": 6 * len(rows),
              "clauses": sum(actual.values()), "rgs_clauses": rgs_clauses,
              "triples": triples}
    if phase:
        result["phase"] = phase
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("period", type=int, choices=(2, 4))
    parser.add_argument("offset", type=int)
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--phase", type=int, default=0)
    args = parser.parse_args()
    check(args.period, args.offset, args.cnf, args.phase)
