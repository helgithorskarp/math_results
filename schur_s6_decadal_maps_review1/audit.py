"""Decode every CNF clause for the noninjective decadal Schur map family."""

import argparse
import hashlib
from pathlib import Path

N = 537
SEED_SHA256 = "58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3"
CNF_SHA256 = "fb1b8382355c35a0df6d22ed53e8812da3c5ae9bf2f3910733c3e3c649a9bae4"
ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "schur_s6_decadal_maps/seed537.txt"
EARLIER_SEED = ROOT / "schur_s6_decadal_block_trades/seed537.txt"


def block(v):
    return (v - 1) // 10


def decode(literal):
    assert literal != 0 and abs(literal) <= 1578
    index = abs(literal) - 1
    return index // 6, index % 6 + 1


def audit(path):
    seed = SEED.read_bytes()
    assert hashlib.sha256(seed).hexdigest() == SEED_SHA256
    assert seed == EARLIER_SEED.read_bytes()
    digits = seed.decode("ascii").strip()
    assert len(digits) == N and set(digits) == set("123456")
    word = [0] + [int(c) for c in digits]
    rows = sorted({(block(v), word[v]) for v in range(1, N + 1)})
    row_id = {row: i for i, row in enumerate(rows)}
    assert len(rows) == 263 and len({b for b, _ in rows}) == 54
    root = row_id[(block(1), word[1])]
    assert word[1] == 2 and root == 1

    supports = set()
    defects = []
    triples = doubling = 0
    for x in range(1, N // 2 + 1):
        for y in range(x, N - x + 1):
            z = x + y
            triples += 1
            doubling += (x == y)
            if word[x] == word[y] == word[z]:
                defects.append((x, y, z))
            support = frozenset(row_id[(block(v), word[v])] for v in (x, y, z))
            assert len(support) >= 2
            supports.add(support)
    assert triples == 72092 and doubling == 268
    assert defects == [(12, 12, 24), (12, 24, 36)]
    assert len(supports) == 52754

    digest = hashlib.sha256()
    seen = set()
    onehot = set()
    at_most = set()
    triple_clauses = set()
    units = set()
    with path.open("rb") as stream:
        header = stream.readline()
        digest.update(header)
        assert header == b"p cnf 1578 320733\n"
        for line in stream:
            digest.update(line)
            data = [int(token) for token in line.split()]
            assert data and data[-1] == 0 and 0 not in data[:-1]
            clause = tuple(sorted(data[:-1]))
            assert len(clause) == len(set(clause)) and clause not in seen
            seen.add(clause)
            entries = [decode(lit) for lit in clause]

            if all(lit > 0 for lit in clause):
                if len(clause) == 6:
                    assert len({row for row, _ in entries}) == 1
                    assert {c for _, c in entries} == set(range(1, 7))
                    onehot.add(entries[0][0])
                else:
                    assert len(clause) == 1 and entries[0] == (root, 2)
                    units.add(clause[0])
                continue

            assert all(lit < 0 for lit in clause)
            if len(clause) == 2 and entries[0][0] == entries[1][0]:
                (row, c), (_, d) = entries
                assert c != d
                at_most.add((row, min(c, d), max(c, d)))
                continue
            assert len(clause) in (2, 3)
            assert len({c for _, c in entries}) == 1
            support = frozenset(row for row, _ in entries)
            assert len(support) == len(entries) and support in supports
            triple_clauses.add((support, entries[0][1]))

    assert digest.hexdigest() == CNF_SHA256
    assert onehot == set(range(263))
    assert len(at_most) == 15 * 263
    assert len(triple_clauses) == 6 * len(supports)
    assert units == {6 * root + 2}
    assert len(seen) == 263 + 15 * 263 + 6 * 52754 + 1 == 320733
    print("PASS rows=263 supports=52754 clauses=320733 triples=72092 "
          "doubling=268 seed_defects=2 exact_semantics=yes "
          "noninjective_maps=yes one_global_unit=yes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    audit(parser.parse_args().cnf)
