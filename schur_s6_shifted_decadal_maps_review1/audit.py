"""Decode and audit every clause of a shifted noninjective Schur map CNF."""

import argparse
import bisect
import hashlib
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SEED = HERE / "schur_s6_shifted_decadal_maps/seed537.txt"
EARLIER_SEED = HERE / "schur_s6_decadal_maps/seed537.txt"
SEED_SHA256 = "58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3"
CASES = {
    1: (55, 268, 53162, 323261,
        "d9574c00603e4b263813267fa006b5c492d1f7e50668610860f1f94316bf9036"),
    9: (54, 264, 52382, 318517,
        "aeec936688e6a4e5260c1a3c33a14b2718b8c8e6da6deebe12a4e9e2c29eec80"),
}


def audit(offset, cnf):
    blocks_expected, rows_expected, supports_expected, clauses_expected, cnf_hash = CASES[offset]
    raw = SEED.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SEED_SHA256
    assert raw == EARLIER_SEED.read_bytes()
    digits = raw.decode("ascii").strip()
    assert len(digits) == 537 and set(digits) == set("123456")
    word = [0] + [int(digit) for digit in digits]

    # Locate a position by explicit cut points, without the encoder's block formula.
    cuts = list(range(offset, 538, 10))
    if cuts[-1] != 537:
        cuts.append(537)
    assert len(cuts) == blocks_expected and cuts[-1] == 537

    def block(v):
        assert 1 <= v <= 537
        return bisect.bisect_left(cuts, v)

    rows = sorted({(block(v), word[v]) for v in range(1, 538)})
    row_id = {row: i for i, row in enumerate(rows)}
    assert len(rows) == rows_expected
    root = row_id[(block(1), word[1])]
    assert word[1] == 2

    supports = set()
    defects = []
    triples = doubling = 0
    for x in range(1, 269):
        for y in range(x, 538 - x):
            z = x + y
            triples += 1
            doubling += x == y
            if word[x] == word[y] == word[z]:
                defects.append((x, y, z))
            support = frozenset(row_id[(block(v), word[v])] for v in (x, y, z))
            assert len(support) >= 2
            supports.add(support)
    assert triples == 72092 and doubling == 268
    assert defects == [(12, 12, 24), (12, 24, 36)]
    assert len(supports) == supports_expected

    max_var = 6 * rows_expected

    def decode(literal):
        assert literal and abs(literal) <= max_var
        index = abs(literal) - 1
        return index // 6, index % 6 + 1

    seen = set()
    onehot = set()
    at_most = set()
    forbidden = set()
    units = set()
    digest = hashlib.sha256()
    with Path(cnf).open("rb") as stream:
        header = stream.readline()
        digest.update(header)
        assert header == f"p cnf {max_var} {clauses_expected}\n".encode()
        for line in stream:
            digest.update(line)
            values = [int(token) for token in line.split()]
            assert values and values[-1] == 0 and 0 not in values[:-1]
            clause = tuple(sorted(values[:-1]))
            assert len(clause) == len(set(clause)) and clause not in seen
            seen.add(clause)
            entries = [decode(literal) for literal in clause]
            if all(literal > 0 for literal in clause):
                if len(clause) == 6:
                    assert len({row for row, _ in entries}) == 1
                    assert {colour for _, colour in entries} == set(range(1, 7))
                    onehot.add(entries[0][0])
                else:
                    assert len(clause) == 1 and entries[0] == (root, 2)
                    units.add(clause[0])
                continue

            assert all(literal < 0 for literal in clause)
            if len(clause) == 2 and entries[0][0] == entries[1][0]:
                (row, colour), (_, other) = entries
                assert colour != other
                at_most.add((row, min(colour, other), max(colour, other)))
                continue
            assert len(clause) in (2, 3)
            assert len({colour for _, colour in entries}) == 1
            support = frozenset(row for row, _ in entries)
            assert len(support) == len(entries) and support in supports
            forbidden.add((support, entries[0][1]))

    assert digest.hexdigest() == cnf_hash
    assert onehot == set(range(rows_expected))
    assert len(at_most) == 15 * rows_expected
    assert units == {6 * root + 2}
    assert len(forbidden) == 6 * supports_expected
    assert len(seen) == 16 * rows_expected + 1 + 6 * supports_expected == clauses_expected
    print(f"PASS offset={offset} rows={rows_expected} supports={supports_expected} "
          f"clauses={clauses_expected} triples={triples} doubling={doubling} "
          "seed_defects=2 exact_semantics=yes noninjective_maps=yes one_global_unit=yes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("offset", type=int, choices=sorted(CASES))
    parser.add_argument("cnf", type=Path)
    args = parser.parse_args()
    audit(args.offset, args.cnf)
