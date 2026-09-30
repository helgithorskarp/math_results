#!/usr/bin/env python3
"""Exhaust the parity-slack-four defect templates, using integer Bareiss."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
import json
from math import isqrt
from pathlib import Path
import random

N = 22
TARGETS = ((6, 14, 2), (8, 8, 6), (10, 2, 10))


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def determinant(matrix):
    """Fraction-free elimination; all divisions and row signs are checked."""
    a = [row[:] for row in matrix]
    n, previous, sign = len(a), 1, 1
    require(n > 0 and all(len(row) == n for row in a), "nonsquare matrix")
    for k in range(n - 1):
        pivot_row = next((i for i in range(k, n) if a[i][k]), None)
        if pivot_row is None:
            return 0
        if pivot_row != k:
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = pivot * a[i][j] - a[i][k] * a[k][j]
                require(numerator % previous == 0, "inexact Bareiss division")
                a[i][j] = numerator // previous
        for i in range(k + 1, n):
            a[i][k] = 0
        previous = pivot
    return sign * a[-1][-1]


def forced_matrix(degree, defect):
    y = [10 - d for d in degree]
    return [[25 * (i == j) + 24 - 4 * (y[i] + y[j])
             + 4 * (y[i] ** 2 - 2 * y[i]) * (i == j) - 4 * defect[i][j]
             for j in range(N)] for i in range(N)]


def template_census(histogram):
    a, b, c = histogram
    degree = [8] * a + [9] * b + [10] * c
    require(len(degree) == N and 3 * a + b == 32 and b % 2 == 0,
            "wrong first-slack histogram")
    records = []
    for center_count in (1, 2):
        for classes in combinations_with_replacement((8, 9, 10), center_count):
            # A single center has excess four, or both centers have excess two.
            row_degrees = [(4 if center_count == 1 else 2) + (d % 2) for d in classes]
            weights = range(1) if center_count == 1 else range(min(row_degrees) + 1)
            for weight in weights:
                available = {d: [i for i, value in enumerate(degree) if value == d]
                             for d in (8, 9, 10)}
                if any(classes.count(d) > len(available[d]) for d in (8, 9, 10)):
                    continue
                centers = [available[d].pop(0) for d in classes]
                if sum(value - weight for value in row_degrees) > len(available[9]):
                    continue
                defect = [[0] * N for _ in range(N)]
                if weight:
                    i, j = centers
                    defect[i][j] = defect[j][i] = weight
                for i, value in zip(centers, row_degrees):
                    for _ in range(value - weight):
                        leaf = available[9].pop(0)
                        defect[i][leaf] = defect[leaf][i] = 1
                require(len(available[9]) % 2 == 0, "odd matching remainder")
                for k in range(0, len(available[9]), 2):
                    i, j = available[9][k:k + 2]
                    defect[i][j] = defect[j][i] = 1
                excess = [sum(defect[i]) - degree[i] % 2 for i in range(N)]
                require(sum(excess) == 4 and all(x >= 0 and x % 2 == 0 for x in excess),
                        "wrong incident parity or slack")
                require([i for i, x in enumerate(excess) if x] == sorted(centers),
                        "wrong abnormal vertices")
                matrix = forced_matrix(degree, defect)
                value = determinant(matrix)
                require(value > 0, "unexpected nonpositive determinant")
                root = isqrt(value)
                require(root * root < value < (root + 1) ** 2, "integer-square survivor")
                records.append({
                    "center_classes": list(classes), "center_row_degrees": row_degrees,
                    "center_edge_weight": weight,
                    "defect_edges": [[i, j, defect[i][j]] for i, j in combinations(range(N), 2)
                                     if defect[i][j]],
                    "det_H": value, "floor_sqrt_det": root,
                    "forced_matrix_sha256": sha256(encode(matrix)).hexdigest()})
    require(len(records) == (9 if b == 2 else 22), "unexpected template count")
    return {"degree_histogram": list(histogram), "red_edges": sum(degree) // 2,
            "total_spine_defect": b // 2 + 2, "template_count": len(records), "records": records}


def histogram_audit():
    first_slack, remaining = [], []
    for a in range(N + 1):
        for b in range(N + 1 - a):
            c = N - a - b
            if b % 2 == 0 and 3 * a + b == 32:
                first_slack.append([a, b, c])
    require(first_slack == [list(h) for h in TARGETS], "incomplete histogram domain")
    for edges in (97, 98, 99):
        cases = [[a, b, N - a - b] for a in range(N + 1) for b in range(N + 1 - a)
                 if 8 * a + 9 * b + 10 * (N - a - b) == 2 * edges and 3 * a + b <= 31]
        remaining.append({"red_edges": edges, "necessary_histograms": cases})
    return {"first_slack_histograms": first_slack, "remaining_low_edge_histograms": remaining}


def controls():
    counts, digest = Counter(), sha256()
    for seed in range(24):
        rng = random.Random(324000 + seed)
        red = [[0] * N for _ in range(N)]
        for i, j in combinations(range(N), 2):
            red[i][j] = red[j][i] = int(rng.randrange(100) < 24 + 2 * seed)
        degree = list(map(sum, red))
        red_square = [[sum(red[i][k] * red[k][j] for k in range(N))
                       for j in range(N)] for i in range(N)]
        defect = [[0] * N for _ in range(N)]
        page_sum = 0
        for i, j in combinations(range(N), 2):
            pages = red_square[i][j] if red[i][j] else 20 - degree[i] - degree[j] + red_square[i][j]
            defect[i][j] = defect[j][i] = (3 if red[i][j] else 6) - pages
            page_sum += pages
        matrix = forced_matrix(degree, defect)
        K = [[2 * red[i][j] + (2 * degree[i] - 17) * (i == j)
              for j in range(N)] for i in range(N)]
        square = [[sum(K[i][k] * K[k][j] for k in range(N))
                   for j in range(N)] for i in range(N)]
        require(matrix == square, "universal square identity")
        total = sum(defect[i][j] for i, j in combinations(range(N), 2))
        require(2 * total == 132 - 3 * sum((d - 10) ** 2 for d in degree), "total defect identity")
        require(page_sum % 3 == 0 and page_sum // 3 == 1540 - sum(d * (21 - d) for d in degree) // 2,
                "monochromatic triangle identity")
        require(all(sum(defect[i]) % 2 == degree[i] % 2 for i in range(N)), "incident parity")
        digest.update(encode([seed, degree, total, matrix]) + b"\n")
        counts.update(graphs=1, spines=231, matrix_entries=484, incident_parities=22)
    return {"counts": dict(sorted(counts.items())), "sha256": digest.hexdigest()}


def result():
    require(determinant([[0, 1], [2, 3]]) == -2 and determinant([[1, 2], [2, 4]]) == 0,
            "determinant sign/singular control")
    return {"agent": "six-books-1", "role": "researcher",
            "claim": "No parity-slack-four defect on degrees8..10; 3n8+n9<=31 after prior equality exclusion",
            "template_results": [template_census(h) for h in TARGETS],
            "histogram_audit": histogram_audit(), "controls": controls()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-expected", type=Path)
    args = parser.parse_args()
    output = result()
    if args.write_expected:
        args.write_expected.write_text(json.dumps(output, indent=2) + "\n")
    else:
        expected = json.loads(Path(__file__).with_name("first_slack_expected.json").read_text())
        require(encode(output) == encode(expected), "expected output mismatch")
    print(json.dumps({"complete": True, "templates": [r["template_count"] for r in output["template_results"]],
                      "square_survivors": 0, "controls": output["controls"]}))


if __name__ == "__main__":
    main()
