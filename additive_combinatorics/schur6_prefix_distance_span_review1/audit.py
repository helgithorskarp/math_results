"""Independent audit of the fixed-prefix Schur distance-span theorem."""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import subprocess

SOURCE = Path(__file__).resolve().parents[1] / "schur6_prefix_distance_span"
CNF_HASH = "da79de45fb932edacfbaaa50b6528f118ca7da4d5462c6bca52375ccab7d18a9"
PROOF_HASH = "c414cc231592213f8eccad1e0149eafa9aeb7dc106e575f3d0a55daeba85df92"


def digits(value, length, maximum):
    assert isinstance(value, str) and len(value) == length
    assert set(value) <= set("123456"[:maximum])
    return value


def rows(length):
    # First-summand traversal, independent of the source's output-first audit.
    return [(x, y, x + y) for x in range(1, length + 1)
            for y in range(x, length - x + 1)]


def defects(value):
    return [(x, y, z) for x, y, z in rows(len(value))
            if value[x - 1] == value[y - 1] == value[z - 1]]


def compatible(prefix, block):
    count = 0
    bad = []
    for distance in range(1, min(len(prefix), len(block) - 1) + 1):
        label = prefix[distance - 1]
        for left in range(len(block) - distance):
            right = left + distance
            count += 1
            if block[left] == block[right] == label:
                bad.append((left, right, distance))
    return count, bad


def x(position, colour):
    return 5 * position + colour


def semantic_cnf(prefix):
    expected = Counter()
    for position in range(83):
        expected[tuple(x(position, c) for c in range(1, 6))] += 1
        for a, b in combinations(range(1, 6), 2):
            expected[tuple(sorted((-x(position, a), -x(position, b))))] += 1
    for right in range(83):
        for left in range(max(0, right - len(prefix)), right):
            colour = int(prefix[right - left - 1])
            expected[tuple(sorted((-x(left, colour), -x(right, colour))))] += 1
    assert sum(expected.values()) == 4301
    return expected


def check_cnf(path, prefix):
    raw = path.read_bytes()
    assert sha256(raw).hexdigest() == CNF_HASH
    with path.open(encoding="ascii") as stream:
        assert stream.readline().split() == ["p", "cnf", "415", "4301"]
        actual = Counter()
        for line in stream:
            values = [int(token) for token in line.split()]
            assert values and values[-1] == 0 and 0 not in values[:-1]
            clause = tuple(sorted(values[:-1]))
            assert clause and len(clause) == len(set(clause))
            assert all(1 <= abs(lit) <= 415 for lit in clause)
            actual[clause] += 1
    assert actual == semantic_cnf(prefix)


def check_proof(cnf, proof, checker):
    raw = proof.read_bytes()
    assert len(raw) == 1087155 and sha256(raw).hexdigest() == PROOF_HASH
    result = subprocess.run([str(checker), str(cnf), str(proof)],
                            check=True, capture_output=True, text=True)
    assert "s VERIFIED" in result.stdout
    assert "0 RAT lemmas in core" in result.stdout
    return result.stdout


def source_partial(data, prefix):
    values = digits(data["source_partial_uv"], 227, 5)
    places = list(range(1, 78)) + list(range(155, 305))
    assert values[:77] == prefix and len(places) == len(values)
    fixed = dict(zip(places, values))
    bad = [(x, y, z) for x, y, z in rows(304)
           if x in fixed and y in fixed and z in fixed and
           fixed[x] == fixed[y] == fixed[z]]
    assert bad == [(1, 232, 233), (3, 231, 234)]
    empty = 0
    for z in range(305, 460):
        forbidden = {fixed[x] for x in fixed if x < z and z - x in fixed
                     and fixed[x] == fixed[z - x]}
        empty += len(forbidden) == 5
    assert empty == 0
    return len(bad), empty


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--cnf", type=Path)
    p.add_argument("--proof", type=Path)
    p.add_argument("--drat-trim", type=Path)
    args = p.parse_args()
    data = json.loads((SOURCE / "data.json").read_text())
    prefix = digits(data["prefix"], 77, 5)
    block = digits(data["compatible_block"], 82, 5)
    assert not defects(prefix)
    assert len(rows(77)) == 1482
    pairs, bad = compatible(prefix, block)
    assert pairs == 3311 and not bad
    full = digits(data["attaining_word"], 237, 6)
    assert full == prefix + "6" * 78 + block
    assert {i for i, c in enumerate(full, 1) if c == "6"} == set(range(78, 156))
    assert len(rows(237)) == 14042
    assert sum(x == y for x, y, _ in rows(237)) == 118
    assert not defects(full)
    control = data["positive_control"]
    alternate = digits(control["prefix"], 77, 5)
    long_block = digits(control["compatible_block"], 155, 5)
    assert not defects(alternate)
    count, bad = compatible(alternate, long_block)
    assert count == 8932 and not bad
    assert not defects(alternate + "6" * 78 + long_block)
    assert source_partial(data, prefix) == (2, 0)
    altered = list(block)
    altered[0] = altered[1] = prefix[0]
    assert compatible(prefix, altered)[1]
    if args.cnf:
        check_cnf(args.cnf, prefix)
    else:
        assert sum(semantic_cnf(prefix).values()) == 4301
    if args.proof or args.drat_trim:
        assert args.cnf and args.proof and args.drat_trim
        check_proof(args.cnf, args.proof, args.drat_trim)
    print("PASS prefix=77 span_witness=82 full_word=237 "
          "full_rows=14042 doublings=118 alternate_span_at_least=155 "
          "cnf_clauses=4301 proof_checked=" + str(bool(args.proof)).lower())


if __name__ == "__main__":
    main()
