#!/usr/bin/env python3
"""Exact signed-column certificates excluding e(B)=6 at 106 edges.

See degree106_columns.md for the general identity and arbitrary-graph
bridge. Uses the earlier complete necessary-state generator.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path

from degree106_check import PAIRS, capacity, require, signed_rows, state

FORMS = (
    ("P7", {(i, i + 1) for i in range(6)}, 2),
    ("P3+C4", {(0, 1), (1, 2), (3, 4), (4, 5), (5, 6), (3, 6)}, 1),
    ("P2+C5", {(0, 1), (2, 3), (3, 4), (4, 5), (5, 6), (2, 6)}, 0),
)


def fingerprint(records):
    return sha256(json.dumps(sorted(records), separators=(",", ":")).encode()).hexdigest()


def adjacency(n, edges):
    out = [[0] * n for _ in range(n)]
    for x, y in edges:
        out[x][y] = out[y][x] = 1
    return out


def multiply(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def transpose(a):
    return list(map(list, zip(*a)))


def algebra_controls():
    ps = [adjacency(14, [(i, j) for i, j in combinations(range(14), 2)
                         if (j - i) % 14 in (1, 2, 3, 11, 12, 13)]),
          adjacency(14, [(i, j) for i, j in combinations(range(14), 2) if i // 7 == j // 7]),
          adjacency(14, [(i, j) for i, j in combinations(range(14), 2)
                         if i // 7 != j // 7 and i % 7 != j % 7])]
    ls = [adjacency(7, edges) for _, edges, _ in FORMS]
    ls += [adjacency(7, []), adjacency(7, PAIRS)]
    base = [{i % 7, (i + 1) % 7, (i + 3) % 7} for i in range(14)]
    counts, stream = Counter(), []
    for pi, p in enumerate(ps):
        require(list(map(sum, p)) == [6] * 14, "control blue regularity")
        for li, l in enumerate(ls):
            h = list(map(sum, l))
            e = sum(h) // 2
            for t in range(4):
                sigma = [int(b in {(pi + li + j) % 7 for j in range(t)}) for b in range(7)]
                for variant in range(4):
                    rows = [row.copy() for row in base]
                    used, restore = set(), []
                    if variant in (1, 2):
                        for i in range(variant):
                            b = min(rows[i])
                            rows[i].remove(b)
                            used.add(i)
                            restore.append(b)
                    elif variant == 3:
                        used.add(0)
                        restore = sorted(rows[0])[:2]
                        rows[0].difference_update(restore)
                    for b in restore + [b for b in range(7) if sigma[b]]:
                        i = next(i for i in range(14) if i not in used and b not in rows[i])
                        rows[i].add(b)
                        used.add(i)
                    m = [[int(b in row) for b in range(7)] for row in rows]
                    require([sum(row[b] for row in m) for b in range(7)] == [6 + v for v in sigma],
                            "control column sizes")
                    k = list(map(sum, m))
                    r = [v - 3 for v in k]
                    require(sum(r) == t and min(k) >= 1 and max(k) <= 4, "control row profile")
                    w = [sum(row[b] * sigma[b] for b in range(7)) for row in m]
                    eta = [sum(p[i][j] * r[j] for j in range(14)) - w[i] + r[i]
                           for i in range(14)]
                    pm, ml = multiply(p, m), multiply(m, l)
                    s = multiply(transpose(m), m)
                    u = [sum(m[i][b] * r[i] for i in range(14)) for b in range(7)]
                    v = [sum(m[i][b] * r[i] ** 2 for i in range(14)) for b in range(7)]
                    n = sum(x * x for x in r)
                    d = [sum(s[b][z] * sigma[z] for z in range(7))
                         - sum(l[b][z] * u[z] for z in range(7))
                         - (h[b] + sigma[b]) * u[b] - v[b] + t * h[b] + n - 3 * t
                         for b in range(7)]
                    red = [0] * 22

                    def edge(x, y):
                        red[x] |= 1 << y
                        red[y] |= 1 << x

                    for b in range(7):
                        edge(0, 15 + b)
                    for i, j in combinations(range(14), 2):
                        if not p[i][j]:
                            edge(1 + i, 1 + j)
                    for i in range(14):
                        for b in rows[i]:
                            edge(1 + i, 15 + b)
                    for b, z in PAIRS:
                        if l[b][z]:
                            edge(15 + b, 15 + z)
                    blue = [((1 << 22) - 1) ^ red[i] ^ (1 << i) for i in range(22)]
                    defects = [[0] * 7 for _ in range(14)]
                    for i in range(14):
                        for b in range(7):
                            graph, cap = (red, 3) if m[i][b] else (blue, 6)
                            actual = cap - (graph[1 + i] & graph[15 + b]).bit_count()
                            formula = pm[i][b] - ml[i][b] + h[b] + k[i] - 6
                            formula += m[i][b] * (4 - k[i] - h[b] - sigma[b])
                            require(actual == formula, "literal general cross-spine identity")
                            defects[i][b] = actual
                            counts["literal_cross_spines"] += 1
                        total = 2 * e - 21 + 10 * k[i] - k[i] ** 2
                        total -= 2 * sum(h[b] for b in rows[i])
                        require(sum(defects[i]) == total + eta[i], "general row-budget residual")
                        counts["row_budget_residuals"] += 1
                    for b in range(7):
                        actual = sum(r[i] * defects[i][b] for i in range(14))
                        correction = sum(m[i][b] * eta[i] for i in range(14))
                        require(actual == d[b] + correction, "signed-column residual identity")
                        counts["signed_column_residuals"] += 1
                        counts["nonzero_column_residuals"] += int(correction != 0)
                        stream.append([pi, li, t, variant, b, actual, d[b], correction])
                    counts["graphs"] += 1
                    counts["size_one_controls"] += int(1 in k)
    require(counts["nonzero_column_residuals"] > 0, "residual control is vacuous")
    return {"counts": dict(sorted(counts.items())), "stream_sha256": fingerprint(stream),
            "interpretation": "algebra controls; no book validity or saturation assumed"}


def check_form(name, edges, bound, old_expected):
    h, _ = capacity(edges, [0] * 7)
    counts, by_a, margins = Counter(), Counter(), Counter()
    raw, records, certificates = [], [], []
    for ones in combinations(range(7), 2):
        sigma = [int(b in ones) for b in range(7)]
        weight = sum(h[b] for b in ones)
        for a in range(bound + 1):
            budget = 6 - weight - a
            for defect in combinations_with_replacement(range(21), budget):
                status, data = state(edges, sigma, a, defect)
                counts[status] += 1
                raw.append([list(ones), a, list(defect), status])
                if data is None:
                    continue
                s, u, q = data
                for ts, hs, _ in signed_rows(h, sigma, a, s, u, q):
                    record = [list(ones), a, list(defect), [list(t) for t in ts], [list(z) for z in hs]]
                    v = [sum(b in row for row in ts + hs) for b in range(7)]
                    d = [sum(s[b][z] * sigma[z] for z in range(7))
                         - sum(u[z] for z in range(7) if (min(b, z), max(b, z)) in edges)
                         - (h[b] + sigma[b]) * u[b] - v[b] + 2 * h[b] + 2 * a - 4
                         for b in range(7)]
                    negative_budget = sum(7 - 2 * sum(h[b] for b in row) for row in ts)
                    forced = sum(max(0, -x) for x in d)
                    require(forced > negative_budget, "signed-column necessary budget survived")
                    records.append(record)
                    certificates.append([record, d, negative_budget, forced])
                    margins[forced - negative_budget] += 1
                    by_a[a] += 1
    require(fingerprint(records) == old_expected["signed_sha256"], "previous complete signed domain differs")
    return {"name": name, "raw_states": len(raw), "state_counts": dict(sorted(counts.items())),
            "states_sha256": fingerprint(raw), "signed_configurations": len(records),
            "configurations_by_a": dict(sorted(by_a.items())), "signed_sha256": fingerprint(records),
            "strict_margin_histogram": dict(sorted(margins.items())),
            "certificates_sha256": fingerprint(certificates), "survivors": 0}, {
                "name": name, "configurations": sorted(records), "certificates": sorted(certificates)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=Path, help="optional private complete entry stream")
    args = parser.parse_args()
    old = json.loads(Path(__file__).with_name("degree106_expected.json").read_text())
    out, records = [], []
    for name, edges, bound in FORMS:
        previous = next(v for v in old["forms"] if v["name"] == name)
        result, entries = check_form(name, edges, bound, previous)
        out.append(result)
        records.append(entries)
    result = {"agent": "six-books-1", "role": "researcher",
              "claim": "only (e(B),t)=(7,1) or (8,0) at a degree-seven 106-edge root",
              "forms": out, "algebra_controls": algebra_controls()}
    expected = Path(__file__).with_name("degree106_columns_expected.json")
    require(json.loads(json.dumps(result)) == json.loads(expected.read_text()), "compact expected output differs")
    if args.records:
        args.records.write_text(json.dumps(records, separators=(",", ":")) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
