#!/usr/bin/env python3
"""Four-case determinant certificate for the last 97-edge degree histogram.

Written incidence arguments in degree97.md supply the coverage bridge.
This self-contained program checks its finite components and exact matrices.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
import json
from math import isqrt
from pathlib import Path
import random

N = 22
D = [8] * 4 + [9] * 18
PAIRS4 = list(combinations(range(4), 2))
PAIRS22 = list(combinations(range(N), 2))


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def det(A):
    a = [row[:] for row in A]
    previous, sign = 1, 1
    require(a and all(len(row) == len(a) for row in a), "nonsquare matrix")
    for k in range(len(a) - 1):
        row = next((i for i in range(k, len(a)) if a[i][k]), None)
        if row is None:
            return 0
        if row != k:
            a[row], a[k] = a[k], a[row]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, len(a)):
            for j in range(k + 1, len(a)):
                value = pivot * a[i][j] - a[i][k] * a[k][j]
                require(value % previous == 0, "inexact Bareiss division")
                a[i][j] = value // previous
        for i in range(k + 1, len(a)):
            a[i][k] = 0
        previous = pivot
    return sign * a[-1][-1]


def small_bridge_checks():
    graph_records = []
    for mask in range(64):
        edges = [pair for slot, pair in enumerate(PAIRS4) if mask >> slot & 1]
        h = [sum(i in pair for pair in edges) for i in range(4)]
        if min(h) >= 2:
            graph_records.append([mask, h, len(edges)])
    require(Counter(r[2] for r in graph_records) == {4: 3, 5: 6, 6: 1}, "four-vertex coverage")
    subsets = [tuple(i for i in range(4) if mask >> i & 1) for mask in range(1, 16)]
    c4 = [s for s in subsets if not ({0, 2} <= set(s) or {1, 3} <= set(s))]
    kh = [s for s in subsets if not {0, 1} <= set(s)]
    require(len(c4) == 8 and all(len(s) <= 2 for s in c4), "C4 subset coverage")
    require(len(kh) == 11 and all(len(set(s) & {0, 1}) * len(set(s) & {2, 3}) <= len(s) - 1
                                for s in kh), "K4-e mixed-pair inequality")
    exceptional = []
    columns = [(s,) for s in subsets if len(s) == 3]
    columns += list(combinations_with_replacement([s for s in subsets if len(s) == 2], 2))
    for family in columns:
        family = tuple(sorted(family))
        local = [[0 if i == j else 1 - sum(i in s and j in s for s in family)
                  for j in range(4)] for i in range(4)]
        allowed = all(x >= 0 for row in local for x in row) and all(sum(row) <= 2 for row in local)
        if allowed:
            require(len(family) == 2 and not set(family[0]) & set(family[1]), "nondisjoint survivor")
            require(list(map(sum, local)) == [2] * 4, "surviving defect not full row two")
        exceptional.append({"columns": [list(s) for s in family], "local_F": local, "allowed": allowed})
    exceptional.sort(key=lambda r: (len(r["columns"]), r["columns"]))
    require(len(exceptional) == 25 and sum(r["allowed"] for r in exceptional) == 3, "K4 pattern coverage")
    return {"four_vertex_graphs": graph_records, "C4_allowed_subsets": [list(s) for s in c4],
            "K4_minus_edge_allowed_subsets": [list(s) for s in kh],
            "K4_exceptional_patterns": exceptional,
            "C4_required_and_actual_cross_edges": [30, 24],
            "K4_minus_edge_required_and_available_mixed_pairs": [8, 4]}


def forced(degrees, F):
    y = [10 - d for d in degrees]
    return [[25 * (i == j) + 24 - 4 * (y[i] + y[j])
             + 4 * (y[i] ** 2 - 2 * y[i]) * (i == j) - 4 * F[i][j]
             for j in range(N)] for i in range(N)]


def four_cases():
    records = []
    for w in range(4):
        F = [[0] * N for _ in range(N)]
        for i, j in ((0, 2), (0, 3), (1, 2), (1, 3)):
            F[i][j] = F[j][i] = 1
        F[4][5] = F[5][4] = w
        available = list(range(6, N))
        for center in (4, 5):
            for _ in range(3 - w):
                leaf = available.pop(0)
                F[center][leaf] = F[leaf][center] = 1
        for i, j in zip(available[::2], available[1::2]):
            F[i][j] = F[j][i] = 1
        require(list(map(sum, F)) == [2] * 4 + [3] * 2 + [1] * 16, "wrong defect row sums")
        require(sum(F[i][j] for i, j in PAIRS22) == 15, "wrong total defect")
        H = forced(D, F)
        value = det(H)
        require(value > 0, "nonpositive determinant")
        root = isqrt(value)
        require(root * root < value < (root + 1) ** 2, "square determinant")
        modulus = 13 if w == 0 else 23
        require(all(modulus % p for p in range(2, isqrt(modulus) + 1)), "nonprime modulus")
        residue = value % modulus
        require(residue not in {x * x % modulus for x in range(modulus)}, "quadratic residue determinant")
        records.append({"center_weight": w, "leaves_per_center": 3 - w,
                        "F": F, "H": H, "det_H": value, "floor_sqrt_det": root,
                        "nonsquare_modulus": modulus, "det_residue": residue})
    return records


def signed_controls():
    remaining = D[:]
    red = [set() for _ in D]
    while max(remaining):
        i = max(range(N), key=lambda j: (remaining[j], -j))
        count, remaining[i] = remaining[i], 0
        candidates = sorted((j for j in range(N) if remaining[j]), key=lambda j: (-remaining[j], j))
        require(len(candidates) >= count, "Havel-Hakimi control failed")
        for j in candidates[:count]:
            red[i].add(j)
            red[j].add(i)
            remaining[j] -= 1
    require(list(map(len, red)) == D, "control has wrong degrees")
    records = []
    for seed in range(24):
        rng = random.Random(971200 + seed)
        for _ in range(100):
            edges = [(i, j) for i in range(N) for j in sorted(red[i]) if i < j]
            (a, b), (c, d) = rng.sample(edges, 2)
            if len({a, b, c, d}) != 4 or c in red[a] or d in red[b]:
                continue
            for i, j in ((a, b), (c, d)):
                red[i].remove(j)
                red[j].remove(i)
            for i, j in ((a, c), (b, d)):
                red[i].add(j)
                red[j].add(i)
        require(list(map(len, red)) == D, "switch changes degrees")
        blue = [set(range(N)) - red[i] - {i} for i in range(N)]
        F = [[0] * N for _ in range(N)]
        for i, j in PAIRS22:
            f = 3 - len(red[i] & red[j]) if j in red[i] else 6 - len(blue[i] & blue[j])
            F[i][j] = F[j][i] = f
        incident = list(map(sum, F))
        for i in range(N):
            require(incident[i] == 194 - 294 + 38 * D[i] - D[i] ** 2 - 2 * sum(D[j] for j in red[i]),
                    "literal row identity control")
            q = incident[i] - D[i] % 2
            require(q % 2 == 0 and 2 * len(red[i] & set(range(4))) == 2 * (10 - D[i]) + q,
                    "D8 neighbor identity control")
        H = forced(D, F)
        K = [[2 * int(j in red[i]) + (2 * D[i] - 17) * (i == j) for j in range(N)] for i in range(N)]
        require([[sum(K[i][k] * K[k][j] for k in range(N)) for j in range(N)] for i in range(N)] == H,
                "integer square identity control")
        require(sum(incident) == 30, "signed total defect")
        mask = sum(1 << slot for slot, (i, j) in enumerate(PAIRS22) if j in red[i])
        records.append({"red_mask": mask, "incident_defect": incident, "F_H_sha256": sha256(encode([F, H])).hexdigest()})
    return records


def baseline():
    rows = Path(__file__).with_name("baseline21.rows").read_text().split()
    require(len(rows) == 21 and all(len(row) == 21 and set(row) <= {"0", "1"} for row in rows), "malformed baseline")
    red = [{j for j, c in enumerate(row) if c == "1"} for row in rows]
    require(all(i not in red[i] and (j in red[i]) == (i in red[j]) for i in range(21) for j in range(21)), "baseline symmetry")
    blue = [set(range(21)) - red[i] - {i} for i in range(21)]
    maxima = [max(len(A[i] & A[j]) for i, j in combinations(range(21), 2) if j in A[i]) for A in (red, blue)]
    histogram = Counter(map(len, red))
    require(histogram == {8: 4, 9: 16, 10: 1} and maxima == [3, 6], "known baseline differs")
    return {"red_edges": sum(map(len, red)) // 2, "degree_histogram": [4, 16, 1], "max_pages": maxima}


def result():
    require(det([[0, 1], [2, 3]]) == -2 and det([[1, 2], [2, 4]]) == 0, "determinant controls")
    return {"agent": "six-books-1", "role": "researcher", "degree_histogram": [4, 18, 0],
            "red_edges": 97, "total_defect": 15, "incident_parity_surplus": 12,
            "small_bridge_checks": small_bridge_checks(), "cases": four_cases(),
            "signed_controls": signed_controls(), "known_baseline21": baseline()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-expected", type=Path)
    args = parser.parse_args()
    actual = result()
    if args.write_expected:
        args.write_expected.write_text(json.dumps(actual, separators=(",", ":")) + "\n")
    else:
        expected = json.loads(Path(__file__).with_name("degree97_expected.json").read_text())
        require(encode(actual) == encode(expected), "expected certificate differs")
    print(json.dumps({"complete": True, "four_vertex_graphs": 10, "K4_column_patterns": 25,
                      "forced_matrices": 4, "positive_nonsquare_determinants": 4,
                      "modular_certificates": [[r["nonsquare_modulus"], r["det_residue"]] for r in actual["cases"]],
                      "signed_controls": 24, "incident_identity_checks": 528,
                      "square_identity_entries": 11616}))


if __name__ == "__main__":
    main()
