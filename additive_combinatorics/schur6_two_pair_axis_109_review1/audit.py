"""Independent audit of the two-pair axis classification modulo 109.

Rebuilds the progression cover and the three CNFs by signed half-residue
arithmetic. Imports no reviewed module or solver. S(4)=44 is external.
"""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import subprocess

SOURCE = Path(__file__).resolve().parents[1] / "schur6_two_pair_axis_109"
P = 109
EXCLUDED = (4, 28, 37)


def half(residue):
    residue %= P
    return min(residue, P - residue)


def modular_word_check(word):
    assert len(word) == P - 1 and all(type(c) is int and 0 <= c < 6 for c in word)
    assert word == word[::-1]
    rows = doublings = 0
    for x in range(1, P):
        for y in range(1, P):
            z = (x + y) % P
            if z == 0:
                continue
            rows += 1
            doublings += x == y
            assert not (word[x - 1] == word[y - 1] == word[z - 1])
    return rows, doublings


def progression_check(data):
    calculated = {}
    for d in range(2, 55):
        forbidden = {1, P - 1, d, P - d}
        possible = [u for u in range(1, P)
                    if all((u * j) % P not in forbidden for j in range(1, 46))]
        calculated[d] = possible
    covered = {d for d, candidates in calculated.items() if candidates}
    residual = sorted(set(range(2, 55)) - covered)
    assert len(covered) == 45
    assert residual == [2, 4, 27, 28, 35, 37, 53, 54]
    assert residual == data["remaining_ratios"]
    supplied = {int(d): u for d, u in data["progression_cover"].items()}
    assert set(supplied) == covered
    for d, u in supplied.items():
        assert u in calculated[d]
        values = [(u * j) % P for j in range(1, 46)]
        assert len(set(values)) == 45 and 0 not in values
    orbits = {tuple(sorted({d, half(pow(d, -1, P))})) for d in residual}
    assert orbits == {(2, 54), (4, 27), (28, 35), (37, 53)}
    assert sorted(map(list, orbits)) == data["remaining_orbits"]
    assert data["admissible_ratios"] == [2, 54]
    assert {half(54 * pow(2, -1, P))} == {27}
    return len(covered), len(orbits)


def semantic_clauses(d):
    free = [q for q in range(1, 55) if q not in (1, d)]
    assert len(free) == 52
    free_set = set(free)
    variable = {(q, c): 4 * j + c + 1
                for j, q in enumerate(free) for c in range(4)}
    clauses = set()
    for q in free:
        row = [variable[q, c] for c in range(4)]
        clauses.add(tuple(row))
        for c, e in combinations(range(4), 2):
            clauses.add(tuple(sorted((-variable[q, c], -variable[q, e]))))

    # Every nonzero residue has a signed representative in the positive half.
    # A monochromatic residual-colour triple can use only free half-points.
    for a in free:
        for b in free:
            for sa, sb in product((-1, 1), repeat=2):
                target = (sa * a + sb * b) % P
                if target == 0:
                    continue
                c = half(target)
                if c not in free_set:
                    continue
                for colour in range(4):
                    clause = {-variable[a, colour], -variable[b, colour],
                              -variable[c, colour]}
                    clauses.add(tuple(sorted(clause)))

    # The four free labels can be renamed in order of first occurrence.
    for j, q in enumerate(free):
        for colour in range(1, 4):
            clause = [-variable[q, colour]]
            clause.extend(variable[old, colour - 1] for old in free[:j])
            clauses.add(tuple(sorted(clause)))
    return clauses


def check_cnf(path, record):
    assert sha256(path.read_bytes()).hexdigest() == record["cnf_sha256"]
    assert path.stat().st_size == record["cnf_bytes"]
    with path.open(encoding="ascii") as stream:
        assert stream.readline().split() == ["p", "cnf", "208", "4056"]
        clauses = []
        for line in stream:
            values = list(map(int, line.split()))
            assert values and values[-1] == 0 and 0 not in values[:-1]
            clause = tuple(sorted(values[:-1]))
            assert clause and len(clause) == len(set(clause))
            assert all(1 <= abs(v) <= 208 for v in clause)
            clauses.append(clause)
    assert len(clauses) == len(set(clauses)) == 4056
    expected = semantic_clauses(record["ratio"])
    assert len(expected) == 4056 and set(clauses) == expected


def check_proof(cnf, proof, checker):
    result = subprocess.run([str(checker), str(cnf), str(proof)],
                            capture_output=True, text=True, check=True)
    assert "s VERIFIED" in result.stdout.splitlines()
    return sha256(proof.read_bytes()).hexdigest(), proof.stat().st_size


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf-dir", type=Path)
    parser.add_argument("--proof-dir", type=Path)
    parser.add_argument("--drat-trim", type=Path)
    args = parser.parse_args()
    if args.proof_dir or args.drat_trim:
        assert args.cnf_dir and args.proof_dir and args.drat_trim
    data = json.loads((SOURCE / "data.json").read_text())
    assert data["modulus"] == P
    assert data["external_schur_number"] == {"colours": 4, "largest_endpoint": 44}
    covered, orbits = progression_check(data)
    word = data["axis_word"]
    rows, doublings = modular_word_check(word)
    assert rows == 11556 and doublings == 108
    assert Counter(word) == Counter(dict(enumerate([2, 2, 20, 22, 26, 36])))
    assert {q for q, c in enumerate(word, 1) if c == 0} == {1, 108}
    assert {q for q, c in enumerate(word, 1) if c == 1} == {2, 107}
    assert [entry["ratio"] for entry in data["exclusions"]] == list(EXCLUDED)
    checked = 0
    for record in data["exclusions"]:
        if args.cnf_dir:
            cnf = args.cnf_dir / f"ratio{record['ratio']}.cnf"
            check_cnf(cnf, record)
            checked += 1
            if args.proof_dir:
                proof = args.proof_dir / f"ratio{record['ratio']}.drat"
                digest, size = check_proof(cnf, proof, args.drat_trim)
                assert digest == record["proof_sha256"] and size == record["proof_bytes"]
    print(f"PASS progression_cover={covered} residual_orbits={orbits} "
          f"witness_rows={rows} doublings={doublings} cnfs_checked={checked} "
          f"proofs_checked={checked if args.proof_dir else 0}")


if __name__ == "__main__":
    main()
