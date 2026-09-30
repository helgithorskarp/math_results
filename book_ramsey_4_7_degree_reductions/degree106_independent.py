#!/usr/bin/env python3
"""Second author implementation; imports no generator code.

Literal B-spine capacities, a scalar two-column moment, positive-row
multiset tables, and rational congruence provide separate implementation
checks. This is neither external peer review nor a formal proof.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path

PAIRS = list(combinations(range(7), 2))
FORMS = [
    ("P7", [(i, i + 1) for i in range(6)]),
    ("P4+C3", [(0, 1), (1, 2), (2, 3), (4, 5), (4, 6), (5, 6)]),
    ("P3+C4", [(0, 1), (1, 2), (3, 4), (4, 5), (5, 6), (3, 6)]),
    ("P2+C5", [(0, 1), (2, 3), (3, 4), (4, 5), (5, 6), (2, 6)]),
]


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def capacities(edges, ones):
    neighbors = [{j for j in range(7) if (min(i, j), max(i, j)) in edges and i != j}
                 for i in range(7)]
    blue = [set(range(7)) - n - {i} for i, n in enumerate(neighbors)]
    col = [6 + int(i in ones) for i in range(7)]
    mat = [[0] * 7 for _ in range(7)]
    for i in range(7):
        mat[i][i] = col[i]
    for i, j in PAIRS:
        if j in neighbors[i]:
            value = 3 - 1 - len(neighbors[i] & neighbors[j])
        else:
            value = 6 - len(blue[i] & blue[j]) - (14 - col[i] - col[j])
        mat[i][j] = mat[j][i] = value
    return [len(n) for n in neighbors], col, mat


def screen(edges, ones, a, defect):
    h, col, s = capacities(edges, ones)
    for j in defect:
        b, z = PAIRS[j]
        s[b][z] -= 1
        s[z][b] -= 1
    if any(not 0 <= s[b][z] <= min(col[b], col[z]) for b, z in PAIRS):
        return "intersection_range", None
    u = [sum(row) - 3 * col[b] for b, row in enumerate(s)]
    if any(v not in range(-a, a + 3) for v in u):
        return "row_bounds", None
    z, w = ones
    delta = sum(v * v for v in u) - 4 - 8 * a - 5 * (u[z] + u[w]) + 2 * s[z][w]
    if delta not in range(0, 8 * a + 1, 4):
        return "moment", None
    q = delta // 4
    lower = [max(0, -v) for v in u]
    upper = [min(a, a + 2 - v) for v in u]
    for points, total in ((ones, q), (set(range(7)) - set(ones), 2 * a - q)):
        if not sum(lower[b] for b in points) <= total <= sum(upper[b] for b in points):
            return "signed_incidence", None
    return "survive", (h, s, u, q)


def indefinite(mat):
    """Exact symmetric congruence; returns True only on a PSD obstruction."""
    a = [[Fraction(v) for v in row] for row in mat]
    for i in range(7):
        if a[i][i] < 0:
            return True
        if a[i][i] == 0:
            if any(a[i][j] for j in range(i + 1, 7)):
                return True
            continue
        for j in range(i + 1, 7):
            for k in range(j, 7):
                a[k][j] = a[j][k] = a[j][k] - a[i][j] * a[i][k] / a[i][i]
    return False


def positive_table(h, size):
    choices = [p for p in combinations(range(7), 4) if sum(h[b] for b in p) <= 7]
    table = defaultdict(list)
    for rows in combinations_with_replacement(choices, size):
        loads = tuple(sum(b in p for p in rows) for b in range(7))
        table[loads].append(rows)
    return table


def process_form(name, edges, vectors):
    edges = set(edges)
    h, _, _ = capacities(edges, ())
    tables = {a: positive_table(h, a + 2) for a in range(3)}
    negative = [p for p in combinations(range(7), 2) if sum(h[b] for b in p) <= 3]
    counts = Counter()
    by_a = Counter()
    signed_by_a = Counter()
    vector_counts = Counter()
    stream = sha256()
    records = []
    for ones in combinations(range(7), 2):
        weight = sum(h[b] for b in ones)
        for a in range(5):
            budget = 6 - weight - a
            if budget < 0:
                continue
            for defect in combinations_with_replacement(range(21), budget):
                status, data = screen(edges, ones, a, defect)
                counts["states"] += 1
                counts[status] += 1
                stream.update(json.dumps([ones, a, defect, status],
                                         separators=(",", ":")).encode() + b"\n")
                if data is None:
                    continue
                require(a <= 2 and (name != "P2+C5" or a <= 1), "unexpected a")
                by_a[a] += 1
                _, s, u, q = data
                for ts in combinations_with_replacement(negative, a):
                    negative_loads = [sum(b in p for p in ts) for b in range(7)]
                    if sum(negative_loads[b] for b in ones) != q:
                        continue
                    loads = tuple(u[b] + negative_loads[b] for b in range(7))
                    for hs in tables[a].get(loads, ()):
                        rem = [[s[b][z] - sum(b in p and z in p for p in ts + hs)
                                for z in range(7)] for b in range(7)]
                        if any(v < 0 for row in rem for v in row):
                            continue
                        signed_by_a[a] += 1
                        records.append([list(ones), a, list(defect),
                                        [list(p) for p in ts], [list(p) for p in hs]])
                        if name == "P4+C3":
                            require(indefinite(rem), "PSD residual Gram survived")
                            scores = [sum(v[b] * rem[b][z] * v[z]
                                          for b in range(7) for z in range(7)) for v in vectors]
                            require(min(scores) < 0, "no integer negative certificate")
                            vector_counts[next(j for j, value in enumerate(scores) if value < 0)] += 1
    records.sort()
    require(name != "P3+C4" or not signed_by_a[2], "P3+C4 final bound failed")
    require(name != "P2+C5" or not signed_by_a[1] and not signed_by_a[2],
            "P2+C5 final bound failed")
    return {"name": name, "counts": dict(sorted(counts.items())),
            "necessary_states_by_a": dict(sorted(by_a.items())),
            "signed_configurations_by_a": dict(sorted(signed_by_a.items())),
            "states_sha256": stream.hexdigest(),
            "signed_sha256": sha256(json.dumps(records, separators=(",", ":")).encode()).hexdigest(),
            "negative_vectors_used": dict(sorted(vector_counts.items()))}


def prescribed_graphs(target):
    deg = [0] * 7
    possible = [[sum(b in p for p in PAIRS[j:]) for b in range(7)] for j in range(22)]

    def rec(j, chosen):
        if any(deg[b] > target[b] or deg[b] + possible[j][b] < target[b] for b in range(7)):
            return
        if j == 21:
            if deg == target:
                yield tuple(chosen)
            return
        yield from rec(j + 1, chosen)
        b, z = PAIRS[j]
        deg[b] += 1
        deg[z] += 1
        yield from rec(j + 1, chosen + [j])
        deg[b] -= 1
        deg[z] -= 1

    return sorted(rec(0, []))


def main():
    expected = json.loads(Path(__file__).with_name("degree106_expected.json").read_text())
    scalar = []
    for e in range(1, 9):
        t = 8 - e
        bounds = []
        for n0 in range(8):
            for n1 in range(8 - n0):
                for n2 in range(8 - n0 - n1):
                    n3 = 7 - n0 - n1 - n2
                    h = [0] * n0 + [1] * n1 + [2] * n2 + [3] * n3
                    if sum(h) != 2 * e:
                        continue
                    bounds.append(max(32 * e - 3 * sum(v * v for v in h) + 6 * t
                                      - 2 * sum(h[b] for b in marked) - 126
                                      for marked in combinations(range(7), t)))
        scalar.append({"e": e, "t": t, "histograms": len(bounds), "max_2U_upper": max(bounds)})
    require(scalar == expected["scalar"], "independent scalar domain differs")
    isolate_forms = [("C6", {(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (1, 6)}),
                     ("2C3", {(1, 2), (1, 3), (2, 3), (4, 5), (4, 6), (5, 6)})]
    for name, edges in isolate_forms:
        _, col, mat = capacities(edges, (0, 1))
        u = [sum(mat[b]) - 3 * col[b] for b in range(7)]
        if name == "C6":
            require(sum(v * v for v in u) == 24 and
                    4 + 8 + 5 * (u[0] + u[1]) - 2 * mat[0][1] + 4 == 20,
                    "independent isolate moment differs")
        else:
            x = [0, 1, 1, 1, -1, -1, -1]
            require(sum(x[b] * mat[b][z] * x[z] for b in range(7) for z in range(7)) == -11,
                    "independent isolate Gram differs")
    target = [1, 1, 1, 2, 2, 2, 3]
    graphs = prescribed_graphs(target)
    counts = Counter()
    stream = sha256()
    for chosen in graphs:
        counts["L"] += 1
        edges = {PAIRS[j] for j in chosen}
        for ones in combinations(range(7), 2):
            weight = sum(target[b] for b in ones)
            for a in range(2):
                budget = 3 - weight - a
                if budget < 0:
                    continue
                for defect in combinations_with_replacement(range(21), budget):
                    status, _ = screen(edges, ones, a, defect)
                    require(status != "survive", "three-leaf state survived")
                    counts["states"] += 1
                    counts[status] += 1
                    stream.update(json.dumps([chosen, ones, a, defect, status],
                                             separators=(",", ":")).encode() + b"\n")
    actual = {"counts": dict(sorted(counts.items())), "states_sha256": stream.hexdigest()}
    require(actual == expected["three_leaf"], "three-leaf entry stream differs")
    forms = [process_form(name, edges, expected["negative_vectors"]) for name, edges in FORMS]
    require(json.loads(json.dumps(forms)) == expected["forms"], "form entry streams differ")
    print(json.dumps({"agent": "six-books-1", "role": "researcher",
                      "status": "all necessary-state and signed-row streams agree",
                      "three_leaf": actual, "forms": forms}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
