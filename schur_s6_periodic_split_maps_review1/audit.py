"""Independent semantic audit of the periodic split-map Schur CNFs."""

import bisect
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "schur_s6_periodic_split_maps"
SEED_HASH = "58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3"


def cuts_for(period, phase, offset):
    cuts = [offset]
    start = offset + 1
    j = 0
    while start <= 537:
        stop = min(537, start + 9)
        if j % period == phase and stop >= start + 5:
            cuts.append(start + 4)
        cuts.append(stop)
        start = stop + 1
        j += 1
    assert cuts == sorted(set(cuts)) and cuts[-1] == 537
    original = list(range(offset, 538, 10))
    if original[-1] != 537:
        original.append(537)
    assert set(original) < set(cuts)  # Strictly refines its old decadal grid.
    return cuts


def audit_one(key, reference, word):
    period = reference["period"]
    phase = reference.get("phase", 0)
    offset = reference["offset"]
    parts = tuple(map(int, key.split("-")))
    assert parts == ((period, offset) if phase == 0 else (period, phase, offset))
    cuts = cuts_for(period, phase, offset)
    shared_old_colour_splits = 0
    start = offset + 1
    j = 0
    while start <= 537:
        stop = min(537, start + 9)
        if j % period == phase and stop >= start + 5:
            left = {word[v] for v in range(start, start + 5)}
            right = {word[v] for v in range(start + 5, stop + 1)}
            shared_old_colour_splits += bool(left & right)
        start = stop + 1
        j += 1
    # Assigning different images to a shared old colour on the two halves
    # gives a word unavailable to the unsplit decadal map family.
    assert shared_old_colour_splits > 0

    def block(v):
        return bisect.bisect_left(cuts, v)

    rows = sorted({(block(v), word[v]) for v in range(1, 538)})
    row_id = {row: i for i, row in enumerate(rows)}
    assert len(rows) == reference["rows"]
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
    assert (triples, doubling) == (72092, 268)
    assert defects == [(12, 12, 24), (12, 24, 36)]
    assert len(supports) == reference["supports"]

    with tempfile.TemporaryDirectory(prefix=f"schur-split-review-{key}-") as tmp:
        cnf = Path(tmp) / "case.cnf"
        subprocess.run(
            [sys.executable, "-B", str(SOURCE / "encode.py"),
             str(period), str(offset), str(cnf), "--phase", str(phase)],
            check=True, capture_output=True, text=True,
        )
        assert cnf.stat().st_size == reference["cnf_bytes"]
        assert hashlib.sha256(cnf.read_bytes()).hexdigest() == reference["cnf_sha256"]

        nrows = len(rows)
        variables = 6 * nrows
        expected_clauses = 16 * nrows + 1 + 5 * (nrows - 1) + 6 * len(supports)
        assert (variables, expected_clauses) == (reference["variables"],
                                                 reference["clauses"])

        def decode(literal):
            assert literal and abs(literal) <= variables
            value = abs(literal) - 1
            return value // 6, value % 6 + 1

        onehot = set()
        at_most = set()
        growth = set()
        forbidden = set()
        units = set()
        seen = set()
        with cnf.open(encoding="ascii") as stream:
            assert stream.readline() == f"p cnf {variables} {expected_clauses}\n"
            for line in stream:
                values = list(map(int, line.split()))
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
                        units.add(1)
                elif positive:
                    assert len(negative) == 1
                    row, colour = decode(negative[0])
                    assert row >= 1 and 2 <= colour <= 6
                    assert {decode(lit) for lit in positive} == {
                        (prior, colour - 1) for prior in range(row)
                    }
                    growth.add((row, colour))
                elif len(clause) == 2 and entries[0][0] == entries[1][0]:
                    (row, first), (_, second) = entries
                    at_most.add((row, min(first, second), max(first, second)))
                else:
                    assert len(clause) in (2, 3)
                    assert len({colour for _, colour in entries}) == 1
                    support = frozenset(row for row, _ in entries)
                    assert len(support) == len(entries) and support in supports
                    forbidden.add((support, entries[0][1]))

        assert len(seen) == expected_clauses
        assert onehot == set(range(nrows)) and units == {1}
        assert at_most == {
            (row, first, second) for row in range(nrows)
            for first in range(1, 7) for second in range(first + 1, 7)
        }
        assert growth == {
            (row, colour) for row in range(1, nrows) for colour in range(2, 7)
        }
        assert forbidden == {
            (support, colour) for support in supports for colour in range(1, 7)
        }
    print(f"PASS case={key} rows={nrows} supports={len(supports)} "
          f"clauses={expected_clauses} shared_splits={shared_old_colour_splits} "
          "exact_semantics=yes", flush=True)


def main():
    raw = (SOURCE / "seed537.txt").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SEED_HASH
    digits = raw.decode("ascii").strip()
    assert len(digits) == 537 and set(digits) == set("123456")
    word = [0] + [int(c) for c in digits]
    manifest = json.loads((SOURCE / "expected.json").read_text())
    cases = manifest["cases"]
    assert len(cases) == 17
    assert {case["offset"] for case in cases.values()} == set(range(1, 11))
    for key in sorted(cases):
        audit_one(key, cases[key], word)
    print("PASS all_17_cases exact_semantics=yes", flush=True)


if __name__ == "__main__":
    main()
