"""Output-first audit of the four-parent Schur-six palette exclusion."""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "schur_s6_four_parent_palette"
PARENTS = (
    ("parent_a.txt", "schur_s6_distant_two_defect_search/best2.txt", "8b6d6ae59d806f53b633c1ec4c6c9989c7f521a5924295ea4c2dc8868ebabdd2"),
    ("parent_b.txt", "schur_s6_nonlocal_doubling_search/best4.txt", "46693293b8bd8e7ebf6fe9ffeeee1c4a26cdc16d1c33c65c7193d0699e855083"),
    ("parent_c.txt", "additive_combinatorics/schur6_support_exchange_traps/traded.txt", "27d47e8c601847189df814f4256b7bc0cb7e8ee63df652340841fa5a7e784c30"),
    ("parent_d.txt", "schur_s6_weighted_onehole_search/best2.txt", "ba8f2f4946290d192882c107391145196a4733e0a8074671331143d28ee74e69"),
)
# The old label at each new label 1,...,6; A is the identity.
OLD_AT_NEW = ((1, 2, 3, 4, 5, 6), (1, 6, 5, 2, 3, 4),
              (1, 3, 2, 6, 5, 4), (5, 2, 1, 4, 6, 3))
EXPECTED_DEFECTS = (
    {(3, 3, 6), (3, 6, 9)},
    {(2, 281, 283), (4, 146, 150), (4, 260, 264), (4, 391, 395)},
    set(),
    {(1, 1, 2), (1, 2, 3)},
)
CNF_HASH = "d6f554606c9d980baff5435f27d54908db38cf180d1374042fe8a3d8adbe24c6"
PROOF_HASH = "a48c10a38cc513c17104c5b34d9260c5b36fe74bd8bb766e5bc30a7c00cb7cff"


def triples():
    """Enumerate every unordered x+y=z with output first, including x=y."""
    for z in range(2, 538):
        for x in range(1, z // 2 + 1):
            yield x, z - x, z


def load_palettes():
    words = []
    for name, origin, expected_hash in PARENTS:
        raw = (SOURCE / name).read_bytes()
        assert sha256(raw).hexdigest() == expected_hash
        assert raw == (ROOT / origin).read_bytes()
        word = raw.decode("ascii").strip()
        assert len(word) == 537 and set(word) <= set("0123456")
        words.append(word)
    rows = list(triples())
    assert len(rows) == 72092 and sum(x == y for x, y, _ in rows) == 268
    for index, word in enumerate(words):
        defects = {(x, y, z) for x, y, z in rows
                   if word[x-1] != "0" and word[x-1] == word[y-1] == word[z-1]}
        holes = {i for i, colour in enumerate(word, 1) if colour == "0"}
        assert defects == EXPECTED_DEFECTS[index]
        assert holes == ({161} if index == 2 else set())
    palettes = [()]
    for i in range(537):
        allowed = set()
        for word, permutation in zip(words, OLD_AT_NEW):
            if word[i] != "0":
                allowed.add(permutation.index(int(word[i])) + 1)
        palettes.append(tuple(sorted(allowed)))
    assert Counter(map(len, palettes[1:])) == {1: 10, 2: 97, 3: 320, 4: 110}
    assert [i for i in range(1, 538) if len(palettes[i]) == 1] == [
        104, 284, 296, 304, 343, 361, 408, 428, 512, 516]
    return palettes, rows


def check_prior_incomparability(palettes):
    """Compare domain sizes with the earlier certified six-alignment family."""
    base = ROOT / "schur_s6_multi_alignment_recombination"
    words = json.loads((base / "sources.json").read_text())
    case = json.loads((base / "cases.json").read_text())["two_347_alignments"]
    sizes = {}
    for position in (17, 104):
        old = {int(perm[int(words[name]["word"][position - 1]) - 1])
               for name, perm in case}
        sizes[position] = (len(palettes[position]), len(old))
    assert sizes == {17: (2, 1), 104: (1, 2)}
    return sizes


def semantic_clauses(palettes, rows):
    number = {(i, colour): j for j, (i, colour) in enumerate(
        ((i, colour) for i in range(1, 538) for colour in palettes[i]), 1)}
    assert len(number) == 1604
    expected = Counter()
    for i in range(1, 538):
        expected[tuple(number[i, c] for c in palettes[i])] += 1
        for c, d in combinations(palettes[i], 2):
            expected[tuple(sorted((-number[i, c], -number[i, d])))] += 1
    for x, y, z in rows:
        for c in set(palettes[x]) & set(palettes[y]) & set(palettes[z]):
            expected[tuple(sorted({-number[x, c], -number[y, c], -number[z, c]}))] += 1
    assert sum(expected.values()) == len(expected) == 53932
    return expected


def check_cnf(path, expected):
    assert sha256(path.read_bytes()).hexdigest() == CNF_HASH
    with path.open(encoding="ascii") as stream:
        assert stream.readline().split() == ["p", "cnf", "1604", "53932"]
        actual = Counter()
        for line in stream:
            row = [int(token) for token in line.split()]
            assert row and row[-1] == 0 and 0 not in row[:-1]
            clause = tuple(sorted(row[:-1]))
            assert clause and len(clause) == len(set(clause))
            assert all(1 <= abs(lit) <= 1604 for lit in clause)
            actual[clause] += 1
    assert actual == expected


def check_proof(cnf, proof, checker):
    assert proof.stat().st_size == 10169326
    assert sha256(proof.read_bytes()).hexdigest() == PROOF_HASH
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
    palettes, rows = load_palettes()
    sizes = check_prior_incomparability(palettes)
    expected = semantic_clauses(palettes, rows)
    if args.cnf:
        check_cnf(args.cnf, expected)
    if args.proof:
        check_proof(args.cnf, args.proof, args.drat_trim)
    print("PASS parents=4 triples=72092 doublings=268 variables=1604 "
          "clauses=53932 palette_sizes=10,97,320,110 "
          f"prior_sizes_17_104={sizes[17]},{sizes[104]} "
          f"proof_checked={str(bool(args.proof)).lower()}")


if __name__ == "__main__":
    main()
