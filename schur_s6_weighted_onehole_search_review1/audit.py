"""Independent weighted-CNF, partial-word, and full-word Schur-six audit."""

import argparse
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "schur_s6_weighted_onehole_search"
PLAIN = ROOT / "schur_s6_unrestricted_fullword_search"
N, K = 537, 6
PLAIN_HASH = "fd6503a79cfeb53c614fe436669f192e81416b6e7292069938cf607f41b070e2"
WEIGHTED_HASH = "59065da7bf54c6f9468a4b578bc0214830d5d5c6af8de44e80dbc004594ddc10"


def read_word(path):
    raw = path.read_bytes()
    assert raw.endswith(b"\n") and raw.count(b"\n") == 1
    value = raw[:-1].decode("ascii")
    assert len(value) == N and set(value) <= set("123456?")
    return value


def triples():
    # First-summand traversal differs from the source's output-first check.
    return [(a, b, a + b) for a in range(1, N + 1)
            for b in range(a, N - a + 1)]


def defects(value, rows):
    return [(a, b, z) for a, b, z in rows
            if value[a - 1] != "?" and
            value[a - 1] == value[b - 1] == value[z - 1]]


def x(v, c):
    return (v - 1) * K + c


def audit_cnf(partial, witness_log):
    with tempfile.TemporaryDirectory(prefix="schur-weighted-review-") as tmp:
        plain = Path(tmp) / "plain.cnf"
        weighted = Path(tmp) / "weighted.cnf"
        subprocess.run([sys.executable, "-B", str(PLAIN / "encode.py"),
                        "--mode", "plain", str(plain)], cwd=PLAIN,
                       check=True, capture_output=True)
        subprocess.run([sys.executable, "-B", str(SOURCE / "weighted_encode.py"),
                        str(weighted)], cwd=SOURCE,
                       check=True, capture_output=True)
        assert sha256(plain.read_bytes()).hexdigest() == PLAIN_HASH
        assert sha256(weighted.read_bytes()).hexdigest() == WEIGHTED_HASH
        with plain.open(encoding="ascii") as p, weighted.open(encoding="ascii") as w:
            assert p.readline().split() == ["p", "cnf", "3222", "441145"]
            assert w.readline().split() == ["p", "cnf", "3222", "441682"]
            original = 0
            for line in p:
                assert line == w.readline()
                original += 1
            assert original == 441145
            for v in range(1, N + 1):
                assert w.readline() == " ".join(str(x(v, c)) for c in range(1, K + 1)) + " 0\n"
            assert w.readline() == ""

        # Make all unselected Boolean literals false, including all at the hole.
        true = {x(v, int(c)) for v, c in enumerate(partial, 1) if c != "?"}
        assert len(true) == N - 1
        failed = []
        with weighted.open(encoding="ascii") as stream:
            next(stream)
            for line in stream:
                literals = [int(t) for t in line.split()]
                assert literals[-1] == 0
                if not any(t in true if t > 0 else -t not in true
                           for t in literals[:-1]):
                    failed.append(tuple(literals[:-1]))
        hole_clause = tuple(x(35, c) for c in range(1, K + 1))
        assert failed == [hole_clause, hole_clause]
        if witness_log:
            signed = [int(token) for line in witness_log.read_text().splitlines()
                      if line.startswith("v ") for token in line.split()[1:]
                      if token != "0"]
            assert len(signed) == K * N
            assert {abs(lit) for lit in signed} == set(range(1, K * N + 1))
            assert {lit for lit in signed if lit > 0} == true
    return len(failed)


def distance(value, old):
    assert len(old) == N and set(old) == set("123456")
    return min(sum(c != "?" and c != relabel[int(old[i]) - 1]
                   for i, c in enumerate(value))
               for relabel in permutations("123456"))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--witness-log", type=Path)
    args = p.parse_args()
    rows = triples()
    assert len(rows) == 72092 and sum(a == b for a, b, _ in rows) == 268
    partial = read_word(SOURCE / "partial35.txt")
    assert partial[0] == "1"
    assert [v for v, c in enumerate(partial, 1) if c == "?"] == [35]
    assert not defects(partial, rows)
    fills = {c: len(defects(partial.replace("?", c), rows))
             for c in "123456"}
    assert fills == {"1": 31, "2": 47, "3": 41,
                     "4": 43, "5": 51, "6": 41}
    assert read_word(SOURCE / "completed31.txt") == partial.replace("?", "1")
    three = read_word(SOURCE / "best3.txt")
    two = read_word(SOURCE / "best2.txt")
    assert set(three) == set(two) == set("123456")
    assert defects(three, rows) == [(1, 1, 2), (1, 2, 3), (1, 55, 56)]
    assert defects(two, rows) == [(1, 1, 2), (1, 2, 3)]
    assert sha256((two + "\n").encode()).hexdigest() == \
        "ba8f2f4946290d192882c107391145196a4733e0a8074671331143d28ee74e69"
    prior = read_word(ROOT / "schur_s6_distant_two_defect_search" / "best2.txt")
    assert distance(two, prior) == 398
    previous = json.loads((ROOT / "schur_s6_multi_alignment_recombination" /
                           "sources.json").read_text())
    distances = {name: distance(two, row["word"])
                 for name, row in previous.items()}
    assert distances == {"W": 422, "190": 430, "359": 416,
                         "best3": 426, "347": 432}
    failed = audit_cnf(partial, args.witness_log)
    print("PASS triples=72092 doublings=268 weighted_clauses=441682 "
          f"hole=35 weighted_unsatisfied={failed} completion_best=31 "
          "best2_defects=[(1,1,2),(1,2,3)] prior_distance=398 "
          f"old_distances={distances}")


if __name__ == "__main__":
    main()
