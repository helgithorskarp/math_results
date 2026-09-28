"""Independent semantic audit of the six-alignment Schur CNF."""

import hashlib
import json
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "schur_s6_multi_alignment_recombination"
N = 537


def read_inputs():
    words = json.loads((SOURCE / "sources.json").read_text())
    cases = json.loads((SOURCE / "cases.json").read_text())
    previous = json.loads((ROOT / "schur_s6_five_word_recombination/sources.json").read_text())
    fixtures = {str(f["multiplier"]): f["colors"] for f in json.loads(
        (ROOT / "schur_s6_537_doubling_traps/fixtures.json").read_text())}
    assert set(words) == {"W", "190", "359", "best3", "347"}
    for name, row in words.items():
        word = row["word"]
        assert len(word) == N and set(word) == set("123456")
        assert word == previous[name]["word"]
        if name in fixtures:
            assert word == fixtures[name]
        if name == "best3":
            assert word == (ROOT / "schur_s6_nonlocal_doubling_search/best3.txt").read_text().strip()
        if name == "W":
            assert word == (ROOT / "schur_s6_all_decadal_maps/seed537.txt").read_text().strip()
        bad = [[x, z - x, z] for z in range(2, N + 1)
               for x in range(1, z // 2 + 1)
               if word[x - 1] == word[z - x - 1] == word[z - 1]]
        assert bad == row["expected_bad"], (name, bad)
    assert cases["two_347_alignments"][:5] == [
        [name, previous[name]["permutation"]]
        for name in ("W", "190", "359", "best3", "347")]
    assert cases["two_347_alignments"][5] == ["347", "524163"]
    return words, cases


def make_domains(words, alignment):
    columns = []
    for name, permutation in alignment:
        assert sorted(permutation) == list("123456")
        columns.append([int(permutation[int(d) - 1]) for d in words[name]["word"]])
    return [frozenset()] + [frozenset(col[v - 1] for col in columns)
                            for v in range(1, N + 1)]


def main():
    words, cases = read_inputs()
    alignment = cases["two_347_alignments"]
    old = make_domains(words, alignment[:5])
    domains = make_domains(words, alignment)
    assert all(old[v] <= domains[v] for v in range(1, N + 1))
    assert sum(len(domains[v]) - len(old[v]) for v in range(1, N + 1)) == 81
    histogram = [sum(len(domains[v]) == k for v in range(1, N + 1))
                 for k in range(1, 7)]
    assert histogram == [2, 91, 258, 170, 16, 0]
    assert [v for v in range(1, N + 1) if len(domains[v]) == 1] == [17, 62]

    pairs = [(v, c) for v in range(1, N + 1) for c in sorted(domains[v])]
    variable = {pair: i for i, pair in enumerate(pairs, 1)}
    reverse = {i: pair for pair, i in variable.items()}
    assert len(variable) == 1718
    forbidden = set()
    triples = doubling = constrained = 0
    for z in range(2, N + 1):
        for x in range(1, z // 2 + 1):
            y = z - x
            triples += 1
            doubling += x == y
            support = frozenset((x, y, z))
            shared = set.intersection(*(set(domains[v]) for v in support))
            constrained += bool(shared)
            forbidden.update((support, c) for c in shared)
    assert (triples, doubling, constrained, len(forbidden)) == (72092, 268, 49824, 68650)

    expected = json.loads((SOURCE / "expected.json").read_text())
    facts = expected["cases"]["two_347_alignments"]
    assert hashlib.sha256((SOURCE / "sources.json").read_bytes()).hexdigest() == expected["sources_sha256"]
    assert hashlib.sha256((SOURCE / "cases.json").read_bytes()).hexdigest() == expected["cases_sha256"]
    with tempfile.TemporaryDirectory(prefix="schur-six-review-") as tmp:
        cnf = Path(tmp) / "case.cnf"
        subprocess.run([sys.executable, "-B", str(SOURCE / "encode.py"),
                        "--case", "two_347_alignments", "--cnf", str(cnf)],
                       check=True, capture_output=True, text=True)
        raw = cnf.read_bytes()
        assert len(raw) == facts["cnf_bytes"]
        assert hashlib.sha256(raw).hexdigest() == facts["cnf_sha256"]
        seen = Counter()
        at_least = set()
        at_most = set()
        schur = set()
        with cnf.open(encoding="ascii") as stream:
            assert stream.readline().split() == ["p", "cnf", "1718", "71232"]
            for line in stream:
                ints = list(map(int, line.split()))
                assert ints and ints[-1] == 0 and 0 not in ints[:-1]
                lits = tuple(sorted(ints[:-1]))
                assert lits and len(lits) == len(set(lits))
                assert all(1 <= abs(lit) <= len(pairs) for lit in lits)
                seen[lits] += 1
                assert seen[lits] == 1
                if all(lit > 0 for lit in lits):
                    decoded = [reverse[lit] for lit in lits]
                    positions = {v for v, _ in decoded}
                    assert len(positions) == 1
                    v = positions.pop()
                    assert {c for _, c in decoded} == domains[v]
                    at_least.add(v)
                else:
                    assert all(lit < 0 for lit in lits)
                    decoded = [reverse[-lit] for lit in lits]
                    positions = frozenset(v for v, _ in decoded)
                    if len(positions) == 1:
                        assert len(decoded) == 2
                        v = next(iter(positions))
                        colours = frozenset(c for _, c in decoded)
                        assert len(colours) == 2 and colours <= domains[v]
                        at_most.add((v, colours))
                    else:
                        assert len(positions) == len(decoded) and len(positions) in (2, 3)
                        colours = {c for _, c in decoded}
                        assert len(colours) == 1
                        item = (positions, next(iter(colours)))
                        assert item in forbidden
                        schur.add(item)
    assert len(seen) == facts["clauses"] == 71232
    assert at_least == set(range(1, N + 1))
    assert at_most == {(v, frozenset((a, b)))
                       for v in range(1, N + 1)
                       for a in domains[v] for b in domains[v] if a < b}
    assert schur == forbidden
    print(f"PASS words=5 alignments=6 added_choices=81 forced=[17, 62] "
          f"histogram={histogram} triples={triples} doubling={doubling} "
          f"constrained={constrained} variables={len(variable)} "
          f"clauses={len(seen)} exact_semantics=yes")


if __name__ == "__main__":
    main()
