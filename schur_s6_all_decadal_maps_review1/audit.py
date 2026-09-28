"""Independently decode every clause of an all-offset Schur map CNF."""

import argparse
import bisect
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "schur_s6_all_decadal_maps/seed537.txt"
EARLIER_SEED = ROOT / "schur_s6_decadal_maps/seed537.txt"
SEED_SHA256 = "58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3"
# offset: (rows, supports, clauses, DIMACS SHA-256)
CASES = {
    1: (268, 53162, 324596, "da229a73fb90049e9b9199925bb96bef7b0380563458243e47cacbcef9928672"),
    2: (268, 52967, 323426, "8a3ee0924937ee5892e0f188a8e4d26d9f714bf0dfa6a9dd909270f06718e39b"),
    3: (265, 52252, 319073, "4be244d9c91015b0644269ae31a42264f4456f3367a9a401d84f536e70e3ec73"),
    4: (267, 52378, 319871, "648e7315dea3455d920e5f35fd3f1e05e57c1e04da0c0bc5b74a2c4169a7134d"),
    5: (270, 52662, 321638, "29b0072651171336ab603154e454fd03a65e3c3ce4cda5e119d13edaeaaee562"),
    6: (270, 53169, 324680, "d99c8e3df1efa9385b1fb47ff80bcad95e0e8ed2218cac3401af1cd83a4367f1"),
    7: (271, 53088, 324215, "a1347df154079bce5c50ba129acb9092a991bf0ed4401b7fc237df4c4473ea70"),
    8: (266, 52570, 321002, "3de8922c9b636e3b9d5b35864cddb58df53f9a3b632ca7118de696d93627dec5"),
    9: (264, 52382, 319832, "e76ee3f15e0a95ff0eec74f743e1aeb863bd30089580eb8b23eb15c7a82cb723"),
    10: (263, 52754, 322043, "7f4d0779ed524010ee3478bca9b9e2f86437a1357b2229074d1f1772146f72c2"),
}


def audit(offset, cnf):
    rows_expected, supports_expected, clauses_expected, cnf_hash = CASES[offset]
    raw = SEED.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SEED_SHA256
    assert raw == EARLIER_SEED.read_bytes()
    digits = raw.decode("ascii").strip()
    assert len(digits) == 537 and set(digits) == set("123456")
    word = [0] + [int(c) for c in digits]

    # Explicit cuts avoid either arithmetic block formula in the source.
    cuts = list(range(offset, 538, 10))
    if cuts[-1] != 537:
        cuts.append(537)

    def block(v):
        return bisect.bisect_left(cuts, v)

    rows = sorted({(block(v), word[v]) for v in range(1, 538)})
    row_id = {row: i for i, row in enumerate(rows)}
    assert len(rows) == rows_expected and word[1] == 2

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

    variables = 6 * rows_expected
    rgs_expected = 1 + 5 * (rows_expected - 1)
    assert clauses_expected == 16 * rows_expected + rgs_expected + 6 * supports_expected

    def decode(literal):
        assert literal and abs(literal) <= variables
        index = abs(literal) - 1
        return index // 6, index % 6 + 1

    seen = set()
    onehot = set()
    at_most = set()
    restricted_growth = set()
    forbidden = set()
    root_units = set()
    digest = hashlib.sha256()
    with Path(cnf).open("rb") as stream:
        header = stream.readline()
        digest.update(header)
        assert header == f"p cnf {variables} {clauses_expected}\n".encode()
        for line in stream:
            digest.update(line)
            values = [int(token) for token in line.split()]
            assert values and values[-1] == 0 and 0 not in values[:-1]
            clause = tuple(sorted(values[:-1]))
            assert len(clause) == len(set(clause)) and clause not in seen
            seen.add(clause)
            positive = [lit for lit in clause if lit > 0]
            negative = [lit for lit in clause if lit < 0]
            entries = [decode(lit) for lit in clause]

            if not negative:
                if len(clause) == 6:
                    assert len({row for row, _ in entries}) == 1
                    assert {colour for _, colour in entries} == set(range(1, 7))
                    onehot.add(entries[0][0])
                else:
                    assert clause == (1,)
                    root_units.add(1)
                continue

            if positive:
                assert len(negative) == 1
                row, colour = decode(negative[0])
                assert row >= 1 and colour >= 2
                assert len(positive) == row
                assert {decode(lit) for lit in positive} == {
                    (earlier, colour - 1) for earlier in range(row)
                }
                restricted_growth.add((row, colour))
                continue

            assert all(lit < 0 for lit in clause)
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
    assert root_units == {1}
    assert restricted_growth == {
        (row, colour) for row in range(1, rows_expected) for colour in range(2, 7)
    }
    assert len(forbidden) == 6 * supports_expected
    assert len(seen) == clauses_expected
    print(f"PASS offset={offset} rows={rows_expected} supports={supports_expected} "
          f"clauses={clauses_expected} triples={triples} doubling={doubling} "
          f"rgs_clauses={rgs_expected} seed_defects=2 exact_semantics=yes "
          "noninjective_maps=yes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("offset", type=int, choices=sorted(CASES))
    parser.add_argument("cnf", type=Path)
    args = parser.parse_args()
    audit(args.offset, args.cnf)
