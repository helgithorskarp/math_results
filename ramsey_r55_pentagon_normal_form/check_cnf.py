#!/usr/bin/env python3
"""Independent full-five-set physical CNF auditor, importing no producer."""
import argparse
import hashlib
import itertools as it
import json
from collections import Counter
from pathlib import Path


def require(test, message):
    if not test:
        raise ValueError(message)


def layout(n=43, cycles=5, joined=True):
    require(type(n) is int and type(cycles) is int and type(joined) is bool,
            "invalid parameter types")
    offset = 2 * int(joined)
    require(cycles >= int(joined) and n >= offset + 5 * cycles, "invalid dimensions")
    fixed = [[None] * n for _ in range(n)]
    for u in range(offset, offset + 5 * cycles):
        for v in range(u + 1, offset + 5 * cycles):
            bu, ru = divmod(u - offset, 5)
            bv, rv = divmod(v - offset, 5)
            if bu == bv:
                fixed[u][v] = fixed[v][u] = int(rv - ru in (1, 4))
    if joined:
        for u in (0, 1):
            for v in range(u + 1, 7):
                fixed[u][v] = fixed[v][u] = 1
    index = [[0] * n for _ in range(n)]
    variable = 0
    for u in range(n):
        for v in range(u + 1, n):
            if fixed[u][v] is None:
                variable += 1
                index[u][v] = index[v][u] = variable
    return fixed, index, variable


def check(path, n=43, cycles=5, joined=True):
    fixed, index, nv = layout(n, cycles, joined)
    count = Counter()
    lengths = Counter()
    assignments_checked = 0
    path = Path(path)
    with path.open() as source:
        header = source.readline().split()
        require(len(header) == 4 and header[:2] == ["p", "cnf"], "invalid header")
        require(int(header[2]) == nv and int(header[3]) >= 0, "invalid dimensions")
        for color in (1, 0):
            for vertices in it.combinations(range(n), 5):
                assignments_checked += 1
                expected = []
                possible = True
                for i, j in it.combinations(vertices, 2):
                    if fixed[i][j] is not None:
                        if fixed[i][j] != color:
                            possible = False
                            break
                    else:
                        expected.append(-index[i][j] if color else index[i][j])
                if not possible:
                    continue
                actual = source.readline().split()
                require(actual, "missing physical clause")
                require(list(map(int, actual)) == expected + [0],
                        f"incorrect clause: color={color}, vertices={vertices}")
                count[color] += 1
                lengths[len(expected)] += 1
        require(sum(count.values()) == int(header[3]), "clause count mismatch")
        require(source.read() == "", "extra formula content")
    with path.open("rb") as source:
        digest = hashlib.file_digest(source, "sha256").hexdigest()
    return {"status": "VERIFIED_COMPLETE_FRAME_CNF", "n": n, "cycles": cycles,
            "joined": joined, "fixed_pairs": n * (n - 1) // 2 - nv,
            "variables": nv, "clauses": sum(count.values()),
            "red_clauses": count[1], "blue_clauses": count[0],
            "length_histogram": {str(k): v for k, v in sorted(lengths.items())},
            "bytes": path.stat().st_size, "sha256": digest,
            "physical_five_color_cases": assignments_checked}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cnf", type=Path)
    args = parser.parse_args()
    print(json.dumps(check(args.cnf), sort_keys=True))
