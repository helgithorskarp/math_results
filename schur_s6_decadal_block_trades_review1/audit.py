"""Independent complete clause audit of the ten decadal Schur trade CNFs."""

import hashlib
import json
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "schur_s6_decadal_block_trades"
SEED_SHA256 = "58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3"
MANIFEST_SHA256 = "cbb25d08b20ca32d6e70ab713a4d98a15022c25187d3a3b58feecc65d7b0e489"
N = 537


def block_of(v, offset):
    if v <= offset:
        return 0
    return 1 + (v - offset - 1) // 10


def clauses_for(offset, word):
    rows = sorted({(block_of(v, offset), word[v]) for v in range(1, N + 1)})
    row_id = {row: i for i, row in enumerate(rows)}

    def lit(row, colour):
        return 6 * row + colour

    expected = Counter()
    for i, (block, old_colour) in enumerate(rows):
        expected[tuple(lit(i, c) for c in range(1, 7))] += 1
        for c in range(1, 7):
            for d in range(c + 1, 7):
                expected[tuple(sorted((-lit(i, c), -lit(i, d))))] += 1
        if block == 0:
            expected[(lit(i, old_colour),)] += 1

    by_block = {}
    for i, (block, _) in enumerate(rows):
        by_block.setdefault(block, []).append(i)
    for group in by_block.values():
        for j, i in enumerate(group):
            for k in group[j + 1:]:
                for c in range(1, 7):
                    expected[tuple(sorted((-lit(i, c), -lit(k, c))))] += 1

    supports = set()
    defects = []
    triples = doubles = 0
    for x in range(1, N // 2 + 1):
        for y in range(x, N - x + 1):
            z = x + y
            triples += 1
            doubles += (x == y)
            if word[x] == word[y] == word[z]:
                defects.append((x, y, z))
            support = frozenset(row_id[(block_of(v, offset), word[v])]
                                for v in (x, y, z))
            assert len(support) >= 2
            supports.add(support)
    assert triples == 72092 and doubles == 268
    assert defects == [(12, 12, 24), (12, 24, 36)]

    for support in supports:
        for c in range(1, 7):
            expected[tuple(sorted(-lit(i, c) for i in support))] += 1
    return rows, supports, expected


def audit_case(offset, word, reference, temp):
    cnf = temp / f"offset-{offset}.cnf"
    produced = subprocess.run([sys.executable, "-B", str(SOURCE / "encode.py"),
                               str(offset), str(cnf)], capture_output=True, text=True)
    assert produced.returncode == 0, produced.stderr
    assert hashlib.sha256(cnf.read_bytes()).hexdigest() == reference["cnf_sha256"]
    rows, supports, expected = clauses_for(offset, word)
    actual = Counter()
    with cnf.open(encoding="ascii") as stream:
        header = stream.readline().strip().split()
        assert header == ["p", "cnf", str(6 * len(rows)), str(sum(expected.values()))]
        for line in stream:
            entries = [int(s) for s in line.split()]
            assert entries and entries[-1] == 0 and 0 not in entries[:-1]
            clause = tuple(sorted(entries[:-1]))
            assert all(1 <= abs(lit) <= 6 * len(rows) for lit in clause)
            assert len(set(clause)) == len(clause)
            actual[clause] += 1
    assert actual == expected, (offset, sum((expected - actual).values()),
                                sum((actual - expected).values()))
    assert (len(rows), len(supports), sum(actual.values())) == (
        reference["rows"], reference["supports"], reference["clauses"])
    print(f"PASS offset={offset} rows={len(rows)} supports={len(supports)} "
          f"clauses={sum(actual.values())} exact_multiset=yes", flush=True)


def main():
    seed = (SOURCE / "seed537.txt").read_bytes()
    assert hashlib.sha256(seed).hexdigest() == SEED_SHA256
    digits = seed.decode("ascii").strip()
    assert len(digits) == N and set(digits) == set("123456")
    word = [0] + [int(d) for d in digits]
    manifest = (SOURCE / "expected.json").read_bytes()
    assert hashlib.sha256(manifest).hexdigest() == MANIFEST_SHA256
    reference = {row["offset"]: row for row in json.loads(manifest)}
    assert set(reference) == set(range(1, 11))
    with tempfile.TemporaryDirectory(prefix="schur-decadal-review-") as directory:
        temp = Path(directory)
        for offset in range(1, 11):
            audit_case(offset, word, reference[offset], temp)
    print("PASS offsets=10 triples=72092 doubling=268 seed_defects=2")


if __name__ == "__main__":
    main()
