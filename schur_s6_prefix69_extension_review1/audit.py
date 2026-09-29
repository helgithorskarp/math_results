"""Independent output-first audit of a fixed Schur-six prefix threshold."""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "schur_s6_prefix69_extension"
CNF_HASH = "b454847f2307822f31a2054b461096f1addc85bf3a48179caed4f8a5b6bb1dc2"
PROOF_HASH = "70406c65d476271ab08ba944cc313fee1a7f45818d7cba284b52c298309a3efa"


def triples(n):
    # Output-first traversal, unlike the reviewed encoder's first-summand loop.
    for z in range(2, n + 1):
        for x in range(1, z // 2 + 1):
            yield x, z - x, z


def variable(position, colour):
    return 6 * (position - 1) + colour


def literal_word_check(prefix, word):
    assert len(prefix) == 69 and set(prefix) == set("123456")
    assert len(word) == 338 and set(word) == set("123456")
    assert word[:69] == prefix
    prior = (ROOT / "schur_s6_nonlocal_doubling_search/best4.txt").read_text().strip()
    assert len(prior) == 537 and prior[:69] == prefix
    rows = doublings = 0
    for x, y, z in triples(len(word)):
        rows += 1
        doublings += x == y
        assert not (word[x - 1] == word[y - 1] == word[z - 1]), (x, y, z)
    assert rows == 28561 and doublings == 169
    return rows, doublings


def semantic_cnf(prefix):
    n = 339
    expected = Counter()
    for v in range(1, n + 1):
        expected[tuple(variable(v, c) for c in range(1, 7))] += 1
        for c, d in combinations(range(1, 7), 2):
            expected[tuple(sorted((-variable(v, c), -variable(v, d))))] += 1
    rows = doublings = 0
    for x, y, z in triples(n):
        rows += 1
        doublings += x == y
        for c in range(1, 7):
            expected[tuple(sorted({-variable(x, c), -variable(y, c),
                                   -variable(z, c)}))] += 1
    for v, digit in enumerate(prefix, 1):
        expected[(variable(v, int(digit)),)] += 1
    assert rows == 28730 and doublings == 169
    assert sum(expected.values()) == len(expected) == 177873
    return expected


def check_cnf(path, prefix):
    assert sha256(path.read_bytes()).hexdigest() == CNF_HASH
    with path.open(encoding="ascii") as stream:
        assert stream.readline().split() == ["p", "cnf", "2034", "177873"]
        actual = Counter()
        for line in stream:
            values = [int(token) for token in line.split()]
            assert values and values[-1] == 0 and 0 not in values[:-1]
            clause = tuple(sorted(values[:-1]))
            assert clause and len(clause) == len(set(clause))
            assert all(1 <= abs(lit) <= 2034 for lit in clause)
            actual[clause] += 1
    assert actual == semantic_cnf(prefix)


def check_proof(cnf, proof, checker):
    assert sha256(proof.read_bytes()).hexdigest() == PROOF_HASH
    assert proof.stat().st_size == 16811935
    result = subprocess.run([str(checker), str(cnf), str(proof)],
                            capture_output=True, text=True, check=True)
    assert "s VERIFIED" in result.stdout.splitlines()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf", type=Path)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--drat-trim", type=Path)
    args = parser.parse_args()
    if args.proof or args.drat_trim:
        assert args.cnf and args.proof and args.drat_trim
    prefix = (SOURCE / "prefix69.txt").read_text().strip()
    word = (SOURCE / "witness338.txt").read_text().strip()
    rows, doublings = literal_word_check(prefix, word)
    if args.cnf:
        check_cnf(args.cnf, prefix)
    else:
        semantic_cnf(prefix)
    if args.proof:
        check_proof(args.cnf, args.proof, args.drat_trim)
    print(f"PASS prefix=69 witness=338 witness_rows={rows} doublings={doublings} "
          f"cnf_clauses=177873 proof_checked={str(bool(args.proof)).lower()}")


if __name__ == "__main__":
    main()
