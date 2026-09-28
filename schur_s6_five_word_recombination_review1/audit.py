"""Independent word-provenance and semantic CNF audit for five-word recombination."""

import hashlib
import json
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "schur_s6_five_word_recombination"
NAMES = ("W", "190", "359", "best3", "347")


def load_words():
    sources = json.loads((SOURCE / "sources.json").read_text(encoding="ascii"))
    assert tuple(sources) == NAMES
    fixtures = {
        str(row["multiplier"]): row
        for row in json.loads((ROOT / "schur_s6_537_doubling_traps/fixtures.json").read_text())
    }
    assert sources["W"]["word"] == (ROOT / "schur_s6_all_decadal_maps/seed537.txt").read_text().strip()
    assert sources["best3"]["word"] == (ROOT / "schur_s6_nonlocal_doubling_search/best3.txt").read_text().strip()
    for name in ("190", "347", "359"):
        assert sources[name]["word"] == fixtures[name]["colors"]
        assert sources[name]["expected_bad"] == [fixtures[name]["expected_bad_triple"]]

    aligned = []
    bad_counts = {}
    for name, row in sources.items():
        word, perm = row["word"], row["permutation"]
        assert len(word) == 537 and set(word) == set("123456")
        assert len(perm) == 6 and set(perm) == set("123456")
        bad = []
        for x in range(1, 269):
            for y in range(x, 538 - x):
                z = x + y
                if word[x - 1] == word[y - 1] == word[z - 1]:
                    bad.append([x, y, z])
        assert bad == row["expected_bad"], (name, bad)
        bad_counts[name] = len(bad)
        aligned.append([int(perm[int(d) - 1]) for d in word])
    assert bad_counts == {"W": 2, "190": 1, "359": 1, "best3": 3, "347": 1}
    return aligned, bad_counts


def audit():
    aligned, bad_counts = load_words()
    domains = [()] + [tuple(sorted({word[v - 1] for word in aligned}))
                      for v in range(1, 538)]
    histogram = [sum(len(domains[v]) == k for v in range(1, 538))
                 for k in range(1, 7)]
    assert histogram == [2, 112, 285, 134, 4, 0]
    forced = [v for v in range(1, 538) if len(domains[v]) == 1]
    variable = {(v, c): i + 1 for i, (v, c) in enumerate(
        (v, c) for v in range(1, 538) for c in domains[v]
    )}
    reverse = {i: pair for pair, i in variable.items()}
    assert len(variable) == 1637

    forbidden = set()
    triples = doubling = constrained = schur_clauses = 0
    for z in range(2, 538):
        for x in range(1, z // 2 + 1):
            y = z - x
            triples += 1
            doubling += x == y
            positions = frozenset((x, y, z))
            common = set.intersection(*(set(domains[v]) for v in positions))
            constrained += bool(common)
            schur_clauses += len(common)
            for c in common:
                forbidden.add((positions, c))
    assert (triples, doubling, constrained, schur_clauses) == (72092, 268, 45807, 58292)
    assert len(forbidden) == schur_clauses

    expected = json.loads((SOURCE / "expected.json").read_text())
    assert expected["sources_sha256"] == hashlib.sha256((SOURCE / "sources.json").read_bytes()).hexdigest()
    assert expected["variables"] == len(variable)
    assert expected["domain_histogram"] == histogram
    with tempfile.TemporaryDirectory(prefix="schur-five-review-") as tmp:
        cnf = Path(tmp) / "case.cnf"
        subprocess.run([sys.executable, "-B", str(SOURCE / "encode.py"),
                        "--cnf", str(cnf)], check=True, capture_output=True, text=True)
        raw = cnf.read_bytes()
        assert len(raw) == expected["cnf_bytes"]
        assert hashlib.sha256(raw).hexdigest() == expected["cnf_sha256"]

        at_least = set()
        at_most = set()
        schur = set()
        clauses = set()
        with cnf.open(encoding="ascii") as stream:
            assert stream.readline().split() == ["p", "cnf", "1637", "60640"]
            for line in stream:
                items = list(map(int, line.split()))
                assert items and items[-1] == 0 and 0 not in items[:-1]
                literals = tuple(sorted(items[:-1]))
                assert len(literals) == len(set(literals)) and literals not in clauses
                clauses.add(literals)
                assert all(1 <= abs(lit) <= len(variable) for lit in literals)
                if all(lit > 0 for lit in literals):
                    decoded = [reverse[lit] for lit in literals]
                    positions = {v for v, _ in decoded}
                    assert len(positions) == 1
                    v = positions.pop()
                    assert {c for _, c in decoded} == set(domains[v])
                    at_least.add(v)
                else:
                    assert all(lit < 0 for lit in literals)
                    decoded = [reverse[-lit] for lit in literals]
                    positions = frozenset(v for v, _ in decoded)
                    if len(positions) == 1:
                        assert len(decoded) == 2
                        v = next(iter(positions))
                        colours = frozenset(c for _, c in decoded)
                        assert len(colours) == 2 and colours <= set(domains[v])
                        at_most.add((v, colours))
                    else:
                        assert len(positions) == len(decoded) and len(positions) in (2, 3)
                        colours = {c for _, c in decoded}
                        assert len(colours) == 1
                        pair = (positions, next(iter(colours)))
                        assert pair in forbidden
                        schur.add(pair)
    assert len(clauses) == expected["clauses"] == 60640
    assert at_least == set(range(1, 538))
    assert at_most == {
        (v, frozenset((a, b))) for v in range(1, 538)
        for i, a in enumerate(domains[v]) for b in domains[v][i + 1:]
    }
    assert schur == forbidden
    print(f"PASS words=5 original_bad={bad_counts} forced_positions={forced} "
          f"domains={histogram} triples={triples} doubling={doubling} "
          f"constrained={constrained} variables={len(variable)} "
          f"clauses={len(clauses)} exact_semantics=yes", flush=True)


if __name__ == "__main__":
    audit()
