"""Independently decode every clause of the published 82-suffix Schur CNF.

Each accepted clause is classified by its mathematical meaning. The class
counts then prove completeness because duplicate clauses are rejected.
"""

import argparse
import hashlib
from collections import Counter
from pathlib import Path

N = 537
TAIL = "5464645646554125541455614546231564345643554232546465264655416354243561655116556425"
CNF_SHA256 = "3ac77a4fba2b88e9f0eb43643eed39ac96c8bd42b1753aba1ffb064562bc7c80"


def decode(literal):
    assert literal != 0 and abs(literal) <= 6 * N
    index = abs(literal) - 1
    return index // 6 + 1, index % 6 + 1


def category(clause):
    assert len(set(clause)) == len(clause)
    data = [decode(literal) for literal in clause]
    if all(literal > 0 for literal in clause):
        if len(clause) == 6:
            assert len({v for v, _ in data}) == 1
            assert {c for _, c in data} == set(range(1, 7))
            return "one_colour"
        assert len(clause) == 1
        value, colour = data[0]
        assert 456 <= value <= N and colour == int(TAIL[value - 456])
        return "suffix_unit"

    assert all(literal < 0 for literal in clause)
    if len(clause) == 2:
        (a, ca), (b, cb) = data
        if a == b:
            assert ca != cb
            return "at_most_one"
        assert ca == cb and 2 * min(a, b) == max(a, b)
        return "doubling"
    assert len(clause) == 3
    assert len({c for _, c in data}) == 1
    x, y, z = sorted(v for v, _ in data)
    assert x < y < z and x + y == z
    return "distinct_sum"


def audit(path):
    assert len(TAIL) == 82 and set(TAIL) <= set("123456")
    root = Path(__file__).resolve().parents[1]
    assert (root / "schur_s6_tail82_certificate/tail82.txt").read_text().strip() == TAIL
    digest = hashlib.sha256()
    counts = Counter()
    seen = set()
    with path.open("rb") as stream:
        header = stream.readline()
        digest.update(header)
        assert header == b"p cnf 3222 441226\n"
        for line in stream:
            digest.update(line)
            entries = [int(token) for token in line.split()]
            assert entries and entries[-1] == 0 and 0 not in entries[:-1]
            clause = tuple(sorted(entries[:-1]))
            assert clause not in seen
            seen.add(clause)
            counts[category(clause)] += 1

    doubles = N // 2
    unordered_sums = sum(z // 2 for z in range(2, N + 1))
    expected = {
        "one_colour": N,
        "at_most_one": 15 * N,
        "distinct_sum": 6 * (unordered_sums - doubles),
        "doubling": 6 * doubles,
        "suffix_unit": len(TAIL),
    }
    assert unordered_sums == 72092 and counts == expected, (counts, expected)
    assert sum(counts.values()) == 441226
    assert digest.hexdigest() == CNF_SHA256
    print("PASS clauses=441226 triples=72092 doubling=268 suffix_units=82 "
          "semantics=exact cnf_sha256=3ac77a4fba2b88e9f0eb43643eed39ac96c8bd42b1753aba1ffb064562bc7c80")


def audit_core(path):
    count = 0
    units = set()
    with path.open(encoding="ascii") as stream:
        assert stream.readline().strip() == "p cnf 3222 23020"
        for line in stream:
            if line.startswith("c"):
                continue
            literals = [int(token) for token in line.split()]
            assert literals and literals[-1] == 0
            count += 1
            if len(literals) == 2 and literals[0] > 0:
                assert literals[0] not in units
                units.add(literals[0])
    expected = {(v - 1) * 6 + int(TAIL[v - 456]) for v in range(456, N + 1)}
    assert count == 23020 and units == expected
    print("PASS core_original_clauses=23020 core_suffix_units=82 all_suffix_units_used=yes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf", type=Path)
    parser.add_argument("--core", type=Path)
    args = parser.parse_args()
    audit(args.cnf)
    if args.core:
        audit_core(args.core)
