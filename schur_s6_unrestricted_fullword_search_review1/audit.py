"""Independent semantic audit of unrestricted Schur-six CNFs and full fixtures."""

import hashlib
import itertools
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "schur_s6_unrestricted_fullword_search"
N, K = 537, 6


def x(v, c):
    return (v - 1) * K + c


def seen(v, c):
    return K * N + (v - 1) * (K - 1) + c


def rows():
    for z in range(2, N + 1):
        for a in range(1, z // 2 + 1):
            yield a, z - a, z


def expected_clauses(mode):
    clauses = set()
    add = lambda literals: clauses.add(tuple(sorted(literals)))
    if mode == "plain":
        add((x(1, 1),))
    for v in range(1, N + 1):
        add(x(v, c) for c in range(1, K + 1))
        for a, b in itertools.combinations(range(1, K + 1), 2):
            add((-x(v, a), -x(v, b)))
    for a, b, z in rows():
        support = {a, b, z}
        for c in range(1, K + 1):
            add(-x(v, c) for v in support)
    if mode == "rgs":
        for v in range(1, N + 1):
            for c in range(1, K):
                add((-x(v, c), seen(v, c)))
                if v == 1:
                    add((-seen(v, c), x(v, c)))
                else:
                    add((-seen(v - 1, c), seen(v, c)))
                    add((-seen(v, c), seen(v - 1, c), x(v, c)))
            for c in range(2, K + 1):
                add((-x(v, c),) if v == 1 else
                    (-x(v, c), seen(v - 1, c - 1)))
    return clauses


def cnf_audit(mode, path):
    result = subprocess.run([sys.executable, "-B", str(SOURCE / "encode.py"),
                             "--mode", mode, str(path)], cwd=SOURCE,
                            check=True, capture_output=True, text=True)
    expected = json.loads((SOURCE / "expected.json").read_text())[mode]["cnf"]
    assert expected["sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
    assert expected["sha256"] in result.stdout
    clauses = expected_clauses(mode)
    assert len(clauses) == expected["clauses"]
    actual = set()
    with path.open(encoding="ascii") as stream:
        assert stream.readline().split() == ["p", "cnf",
                                             str(expected["variables"]),
                                             str(expected["clauses"])]
        for line in stream:
            fields = [int(t) for t in line.split()]
            assert fields and fields[-1] == 0 and 0 not in fields[:-1]
            clause = tuple(sorted(fields[:-1]))
            assert clause and len(clause) == len(set(clause))
            assert all(1 <= abs(lit) <= expected["variables"] for lit in clause)
            assert clause not in actual
            actual.add(clause)
    assert actual == clauses
    return len(actual)


def defects(word, partial=False):
    assert len(word) == N
    bad = []
    for a, b, z in rows():
        if partial and "?" in (word[a - 1], word[b - 1], word[z - 1]):
            continue
        if word[a - 1] == word[b - 1] == word[z - 1]:
            bad.append((a, b, z))
    return bad


def fixture_audit(plain):
    partial = (SOURCE / "partial537.txt").read_text().strip()
    complete = (SOURCE / "completed11.txt").read_text().strip()
    best = (SOURCE / "best4.txt").read_text().strip()
    assert len(partial) == len(complete) == len(best) == N
    assert set(partial) <= set("123456?")
    assert set(complete) == set(best) == set("123456")
    assert [i for i, c in enumerate(partial, 1) if c == "?"] == [2, 4]
    assert not defects(partial, True)
    assert complete == partial.replace("?", "2")
    options = []
    for a, b in itertools.product("123456", repeat=2):
        word = partial[:1] + a + partial[2:3] + b + partial[4:]
        options.append((len(defects(word)), a, b))
    assert min(options) == (11, "2", "2")
    assert sum(score == 11 for score, _, _ in options) == 1
    assert len(defects(complete)) == 11
    assert defects(best) == [(1, 1, 2), (1, 2, 3), (4, 4, 8), (4, 5, 9)]
    assert hashlib.sha256((best + "\n").encode()).hexdigest() == \
        "a947b6e20966bb3d7931f82b9958facd066436c7d928fb5be6b244ed89b1e845"

    # Treat every unselected colour literal as false; only the two positive
    # at-least-one clauses at the holes should then fail.
    true = {x(v, int(c)) for v, c in enumerate(partial, 1) if c != "?"}
    unsatisfied = []
    with plain.open(encoding="ascii") as stream:
        next(stream)
        for line in stream:
            literals = [int(t) for t in line.split()[:-1]]
            if not any(t in true if t > 0 else -t not in true for t in literals):
                unsatisfied.append(tuple(literals))
    assert unsatisfied == [tuple(x(v, c) for c in range(1, K + 1)) for v in (2, 4)] or \
        set(unsatisfied) == {tuple(x(v, c) for c in range(1, K + 1)) for v in (2, 4)}

    sources = json.loads((ROOT / "schur_s6_multi_alignment_recombination/sources.json").read_text())
    distance = {}
    for name, row in sources.items():
        source = row["word"]
        assert len(source) == N
        distance[name] = min(sum(c != "?" and c != perm[int(source[i]) - 1]
                                 for i, c in enumerate(partial))
                             for perm in itertools.permutations("123456"))
    assert distance == {"W": 401, "190": 421, "359": 407,
                        "best3": 409, "347": 414}
    return distance


def symmetry_control():
    canonical = set()
    for word in itertools.product(range(1, 4), repeat=4):
        order = tuple(dict.fromkeys(word))
        relabel = {c: i + 1 for i, c in enumerate(order)}
        norm = tuple(relabel[c] for c in word)
        canonical.add(norm)
        assert norm[0] == 1
        for c in range(2, max(norm) + 1):
            assert norm.index(c - 1) < norm.index(c)
    assert len(canonical) == 14


def main():
    with tempfile.TemporaryDirectory(prefix="schur-full-review-") as temp:
        plain = Path(temp) / "plain.cnf"
        rgs = Path(temp) / "rgs.cnf"
        counts = (cnf_audit("plain", plain), cnf_audit("rgs", rgs))
        distance = fixture_audit(plain)
    symmetry_control()
    assert sum(1 for _ in rows()) == 72092
    assert sum(a == b for a, b, _ in rows()) == 268
    print(f"PASS exact_cnf_clauses={counts} triples=72092 doublings=268 "
          f"partial_holes=[2, 4] partial_unsatisfied=2 "
          f"completion_best=11 complete_best4_defects=4 distances={distance} "
          f"small_canonical=14")


if __name__ == "__main__":
    main()
