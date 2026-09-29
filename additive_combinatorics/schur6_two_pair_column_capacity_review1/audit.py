"""Independent output-first literal audit of the normalized 109-column CNF."""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import subprocess

P = 109
SUPPORT = frozenset(range(0, 108, 2))
FREE = tuple(x for x in range(P) if x not in SUPPORT)
FREE_INDEX = {x: j for j, x in enumerate(FREE)}
CNF_HASH = "ed370a49ae6f766d1c3d728d0ecbdac14d275d3d4b607c155b6339067557f061"
PROOF_HASH = "0cfb50c37a7969ff795de82a2708288012924fa64232146dbb4f351ca7106579"


def axis(residue, colour):
    """Return a Boolean constant or the DIMACS variable for E(residue)=colour."""
    q = min(residue % P, (-residue) % P)
    assert 1 <= q <= 54
    if q <= 2:
        return colour == q - 1
    if colour <= 1:
        return False
    return 4 * (q - 3) + colour - 1


def column(position, colour):
    """Return a Boolean constant or the DIMACS variable for V(position)=colour."""
    if position in SUPPORT:
        return colour == 0
    if colour <= 1:
        return False
    return 208 + 4 * FREE_INDEX[position] + colour - 1


def add_forbidden(clauses, values):
    if any(value is False for value in values):
        return
    row = tuple(sorted({-value for value in values if value is not True}))
    assert row, "fixed colours make the model immediately impossible"
    clauses.add(row)


def semantic_clauses():
    clauses = set()
    for q in range(3, 55):
        row = tuple(axis(q, c) for c in range(2, 6))
        clauses.add(row)
        for pair in combinations(row, 2):
            add_forbidden(clauses, pair)
    for position in FREE:
        row = tuple(column(position, c) for c in range(2, 6))
        clauses.add(row)
        for pair in combinations(row, 2):
            add_forbidden(clauses, pair)

    # Output-first axis traversal differs from both the encoder and its audit.
    axis_rows = doublings = 0
    for z in range(1, P):
        for x in range(1, P):
            y = (z - x) % P
            if y == 0 or x > y:
                continue
            axis_rows += 1
            doublings += x == y
            for colour in range(6):
                add_forbidden(clauses, (axis(x, colour), axis(y, colour),
                                        axis(z, colour)))
    for x, y in combinations(range(P), 2):
        for colour in range(6):
            add_forbidden(clauses, (column(x, colour), column(y, colour),
                                    axis(y - x, colour)))

    # Order only colours that occur on the positive axis. Any used subset
    # can be relabelled as an initial segment, while V is relabelled with it.
    for q in range(3, 55):
        for colour in range(3, 6):
            row = [-axis(q, colour)]
            row.extend(axis(earlier, colour - 1) for earlier in range(3, q))
            clauses.add(tuple(sorted(row)))
    assert axis_rows == 5832 and doublings == 108
    assert len(FREE) == 55 and len(clauses) == 10161
    return clauses, axis_rows, doublings


def check_cycle_normalization():
    assert len(SUPPORT) == 54
    assert all((x + 1) % P not in SUPPORT for x in SUPPORT)
    rotations = {tuple(sorted((x + shift) % P for x in SUPPORT))
                 for shift in range(P)}
    assert len(rotations) == P
    for member in rotations:
        gaps = [(member[(j + 1) % 54] - member[j]) % P
                for j in range(54)]
        assert Counter(gaps) == {2: 53, 3: 1}


def check_cnf(path, expected):
    raw = path.read_bytes()
    assert len(raw) == 170880 and sha256(raw).hexdigest() == CNF_HASH
    lines = raw.decode("ascii").splitlines()
    assert lines[0].split() == ["p", "cnf", "428", "10161"]
    actual = Counter()
    for line in lines[1:]:
        values = [int(token) for token in line.split()]
        assert values and values[-1] == 0 and 0 not in values[:-1]
        row = tuple(sorted(values[:-1]))
        assert row and len(row) == len(set(row))
        assert all(1 <= abs(literal) <= 428 for literal in row)
        actual[row] += 1
    assert len(actual) == sum(actual.values()) == len(expected)
    assert set(actual) == expected


def check_proof(cnf, proof, checker):
    assert proof.stat().st_size == 91233941
    assert sha256(proof.read_bytes()).hexdigest() == PROOF_HASH
    result = subprocess.run([str(checker), str(cnf), str(proof), "-I", "-U"],
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
    check_cycle_normalization()
    expected, axis_rows, doublings = semantic_clauses()
    if args.cnf:
        check_cnf(args.cnf, expected)
    if args.proof:
        check_proof(args.cnf, args.proof, args.drat_trim)
    print(f"PASS axis_rows={axis_rows} doublings={doublings} "
          f"column_pairs=5886 clauses={len(expected)} "
          f"proof_checked={str(bool(args.proof)).lower()}")


if __name__ == "__main__":
    main()
