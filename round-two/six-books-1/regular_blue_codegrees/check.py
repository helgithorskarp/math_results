"""Exact arithmetic controls for the written regular blue-codegree proof.

Actual author: six-books-1, researcher. CPython 3.11.2, standard library.
This is not a host-graph enumeration or a certificate of Ramsey exactness.
"""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def adjacency(n, edges):
    p = [[0] * n for _ in range(n)]
    for i, j in edges:
        need(0 <= i < n and 0 <= j < n and i != j, "bad edge")
        p[i][j] = p[j][i] = 1
    return p


def product(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def gram(rows):
    return product(list(map(list, zip(*rows))), rows)


def k_matrix(p):
    pp = product(p, p)
    return [[4 * int(i == j) + 3 - 3 * p[i][j] - pp[i][j]
             for j in range(10)] for i in range(10)]


def independent_fours(p):
    return [list(s) for s in combinations(range(10), 4)
            if all(not p[i][j] for i, j in combinations(s, 2))]


def quadratic(a, q):
    return sum(q[i] * a[i][j] * q[j]
               for i in range(len(q)) for j in range(len(q)))


def negative_form(k):
    # Small literal forms are controls only, not an enumeration premise.
    for size in range(1, 5):
        for plus in combinations(range(10), size):
            rest = [i for i in range(10) if i not in plus]
            for minus in combinations(rest, size):
                q = [int(i in plus) - int(i in minus) for i in range(10)]
                value = quadratic(k, q)
                if value < 0:
                    return {"vector": q, "value": value}
    raise ValueError("no small negative control found")


def realize_degrees(degrees):
    # A deterministic Havel--Hakimi construction for explicit controls.
    residual = list(degrees)
    edges = []
    while any(residual):
        order = sorted(range(len(residual)), key=lambda i: (-residual[i], i))
        i = order[0]
        d = residual[i]
        targets = order[1:d + 1]
        need(len(targets) == d and all(residual[j] > 0 for j in targets),
             "nongraphical control degree sequence")
        residual[i] = 0
        for j in targets:
            edges.append((i, j))
            residual[j] -= 1
    p = adjacency(len(degrees), edges)
    need(list(map(sum, p)) == degrees, "degree realization failed")
    return p


def decode_rows(rows):
    n = len(rows)
    need(all(len(row) == n and set(row) <= {"0", "1"} for row in rows),
         "bad adjacency rows")
    g = [list(map(int, row)) for row in rows]
    need(all(g[i][i] == 0 and g[i][j] == g[j][i]
             for i in range(n) for j in range(n)), "bad simple graph")
    return g


def page_sets(g, i, j):
    n = len(g)
    if g[i][j]:
        return [k for k in range(n) if g[i][k] and g[j][k]]
    return [k for k in range(n) if k not in (i, j)
            and not g[i][k] and not g[j][k]]


def baseline_record():
    raw = (HERE / "baseline21.rows").read_bytes()
    g = decode_rows(raw.decode().splitlines())
    n = len(g)
    degree = list(map(sum, g))
    maxima = [0, 0]
    for i, j in combinations(range(n), 2):
        color = 0 if g[i][j] else 1
        maxima[color] = max(maxima[color], len(page_sets(g, i, j)))
    need(n == 21 and sum(degree) == 186 and maxima == [3, 6],
         "primary baseline mismatch")
    return {"order": n, "red_edges": sum(degree) // 2,
            "degrees": {str(k): v for k, v in sorted(Counter(degree).items())},
            "red_blue_page_maxima": maxima,
            "rows_sha256": hashlib.sha256(raw).hexdigest()}


def rooted_control(p, fours, size):
    expanded = [s for s in fours for _ in range(2)]
    a = 0
    if size == 10:
        sets = [list(range(10))] + expanded
    else:
        r = next(s for s in fours if a not in s)
        remaining = list(expanded)
        remaining.remove(r)
        sets = [[i for i in range(10) if i != a], sorted([a] + r)] + remaining
    m = [[int(i in s) for i in range(10)] for s in sets]
    need(list(map(sum, zip(*m))) == [5] * 10, "miss column counts")
    d = list(map(sum, m))
    # b is adjacent to all other rows for size10; for size9 it misses
    # only the five-point row. The remaining degree sequence is realized.
    neighbors_b = list(range(1, 11)) if size == 10 else list(range(2, 11))
    tail_degrees = [d[i] - int(i in neighbors_b) for i in range(1, 11)]
    tail = realize_degrees(tail_degrees)
    edges = [(0, i + 1) for i in range(10)]
    edges += [(i + 1, j + 1) for i, j in combinations(range(10), 2) if p[i][j]]
    edges += [(i + 1, b + 11) for b in range(11) for i in range(10) if not m[b][i]]
    edges += [(11, b + 11) for b in neighbors_b]
    edges += [(i + 12, j + 12) for i, j in combinations(range(10), 2) if tail[i][j]]
    g = adjacency(22, edges)
    need(list(map(sum, g)) == [10] * 22, "control not ten-regular")
    s0 = [[x + 1 for x in row] for row in k_matrix(p)]
    actual_s = gram(m)
    f = [[s0[i][j] - actual_s[i][j] for j in range(10)] for i in range(10)]
    need(all(x >= 0 for row in f for x in row), "control local defect negative")
    for i in range(10):
        for j in range(i):
            ii, jj = i + 1, j + 1
            literal = (3 if g[ii][jj] else 6) - len(page_sets(g, ii, jj))
            need(literal == f[i][j], "literal local defect mismatch")
    extra = [sum((len(z) - 4) for z in sets if i in z) for i in range(10)]
    need(list(map(sum, f)) == [6 - x for x in extra], "margin identity")
    if size == 10:
        need(not any(x for row in f for x in row), "size10 defect nonzero")
        need(gram(m[1:]) == k_matrix(p), "size10 Gram identity")
    else:
        r = [m[1][i] - int(i == a) for i in range(10)]
        left = [[m[0][i] * m[0][j] + m[1][i] * m[1][j] + f[i][j]
                 for j in range(10)] for i in range(10)]
        need(left == [[1 + r[i] * r[j] for j in range(10)] for i in range(10)],
             "size9 star identity")
        need(gram(m[2:] + [r]) == k_matrix(p), "size9 Gram conversion")
    repeated = next((c, d_) for c, d_ in combinations(neighbors_b, 2)
                    if len(sets[c]) == 4 and sets[c] == sets[d_])
    c, d_ = [x + 11 for x in repeated]
    pages = page_sets(g, c, d_)
    need(len(pages) > (3 if g[c][d_] else 6), "repeated row not forbidden")
    return {"large_row_size": size, "graph_rows": ["".join(map(str, row)) for row in g],
            "miss_sets": sets, "defect_matrix": f,
            "repeated_pair": [c, d_], "spine_color": "red" if g[c][d_] else "blue",
            "literal_pages": pages}


def build():
    labels = list(combinations(range(5), 2))
    p = adjacency(10, [(i, j) for i, j in combinations(range(10), 2)
                       if set(labels[i]).isdisjoint(labels[j])])
    pp = product(p, p)
    need(list(map(sum, p)) == [3] * 10, "Petersen control degrees")
    need(pp == [[2 * int(i == j) + 1 - p[i][j] for j in range(10)]
                for i in range(10)], "Petersen relation")
    fours = independent_fours(p)
    need(len(fours) == 5 and Counter(i for s in fours for i in s) == Counter({i: 2 for i in range(10)}),
         "independent four-set count")
    need(k_matrix(p) == [[2 * int(i == j) + 2 - 2 * p[i][j] for j in range(10)]
                         for i in range(10)], "K identity")
    prism = adjacency(10, [(i, (i + 1) % 5) for i in range(5)]
                      + [(i + 5, (i + 1) % 5 + 5) for i in range(5)]
                      + [(i, i + 5) for i in range(5)])
    mobius = adjacency(10, [(i, (i + 1) % 10) for i in range(10)]
                       + [(i, i + 5) for i in range(5)])
    negative = []
    for name, control in (("pentagonal_prism", prism), ("mobius_ladder10", mobius)):
        need(list(map(sum, control)) == [3] * 10, "negative control not cubic")
        need(sum(product(product(control, control), control)[i][i] for i in range(10)) == 0,
             "negative control not triangle-free")
        negative.append({"name": name, "graph_rows": ["".join(map(str, row)) for row in control],
                         **negative_form(k_matrix(control))})
    return {"baseline": baseline_record(), "P": p, "K": k_matrix(p),
            "independent_four_sets": fours,
            "controls": [rooted_control(p, fours, size) for size in (10, 9)],
            "negative_forms": negative}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="explicitly regenerate compact expected data")
    args = parser.parse_args()
    record = build()
    serialized = json.dumps(record, sort_keys=True, indent=2) + "\n"
    if args.write:
        (HERE / "expected.json").write_text(serialized)
    else:
        need((HERE / "expected.json").read_text() == serialized, "expected data mismatch")
    print(json.dumps({"status": "PASS", "baseline_edges": 93,
                      "independent_four_sets": len(record["independent_four_sets"]),
                      "rooted_controls": len(record["controls"]),
                      "negative_forms": len(record["negative_forms"]),
                      "expected_sha256": hashlib.sha256(serialized.encode()).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
