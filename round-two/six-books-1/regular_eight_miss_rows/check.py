"""Exact controls for the analytic eight-point miss-row reduction.

Actual author six-books-1, researcher. Standard library, integer arithmetic.
These controls are not a host census or a proof of a Ramsey endpoint.
"""
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def mask(points):
    return sum(1 << i for i in points)


def adj(n, edges):
    p = [[0] * n for _ in range(n)]
    for i, j in edges:
        need(i != j and 0 <= i < n and 0 <= j < n, "bad edge")
        p[i][j] = p[j][i] = 1
    return p


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def gram(sets):
    return [[sum(i in s and j in s for s in sets) for j in range(10)]
            for i in range(10)]


def s0_matrix(p):
    h = list(map(sum, p))
    pp = matmul(p, p)
    return [[4 * (i == j) + h[i] + h[j] - 2 - 3 * p[i][j] - pp[i][j]
             for j in range(10)] for i in range(10)]


def k_matrix(p):
    pp = matmul(p, p)
    return [[4 * (i == j) + 3 - 3 * p[i][j] - pp[i][j]
             for j in range(10)] for i in range(10)]


def triple_controls():
    t5 = [set(t) for t in combinations(range(5), 3)]
    bad5 = sum(all(len(a & b) <= 1 for a, b in combinations(t, 2))
               for t in product(t5, repeat=3))
    need(bad5 == 0, "three triples fit a five-set")
    t6 = [set(t) for t in combinations(range(6), 3)]
    pairs6 = [(a, b) for a, b in product(t6, repeat=2) if len(a & b) <= 1]
    need(all(len(set(range(6)) - (a | b)) <= 1 for a, b in pairs6),
         "two triples leave two points")
    triples6 = [t for t in combinations(t6, 3)
                if all(len(a & b) <= 1 for a, b in combinations(t, 2))]
    need(all(len(set.union(*t)) >= 6 for t in triples6), "three triples miss a point")
    systems = [t for t in combinations(t6, 4)
               if all(len(a & b) <= 1 for a, b in combinations(t, 2))]
    need(len(systems) == 30, "four-triple system count")
    profiles = []
    for t in systems:
        need(all(sum(i in s for s in t) == 2 for i in range(6)), "outside cut degrees")
        need(all(len(a & b) == 1 for a, b in combinations(t, 2)), "cut pair relation")
        for order in permutations(t):
            profiles.append(sum(mask(s) << (6 * i) for i, s in enumerate(order)))
    profiles.sort()
    need(len(profiles) == len(set(profiles)) == 720, "labeled cut profiles")
    return {"five_point_ordered_triples": 1000, "feasible_five_point_triples": bad5,
            "six_point_pair_records": len(pairs6), "six_point_triple_records": len(triples6),
            "four_triple_systems": len(systems), "labeled_profiles": profiles}


def packing_controls():
    universe = set(range(8))
    fours = [set(t) for t in combinations(range(8), 4)]
    fives = [set(t) for t in combinations(range(8), 5)]
    sixes = [set(t) for t in combinations(range(8), 6)]
    repeated_trials = 0
    for c in fours:
        d = universe - c
        for k, rows in ((5, fives), (6, sixes)):
            for q in rows:
                repeated_trials += 1
                need(not (len(q & c) <= k - 4 and len(q & d) <= k - 4),
                     "repeated four-row containment")
    nested = [(u, w) for u, w in product(fives, repeat=2) if len(u & w) <= 2]
    for u, w in nested:
        need(u | w == universe, "nested five-row covering")
        need(not any(len(c & u) <= 1 and len(c & w) <= 1 for c in fours),
             "nested four/five/five packing")
    return {"repeated_containment_trials": repeated_trials,
            "nested_five_pairs": len(nested), "nested_four_trials": len(nested) * len(fours)}


def bipartite_codes():
    triples = list(combinations(range(5), 3))
    codes = []
    for rows in product(triples, repeat=5):
        if all(sum(j in row for row in rows) == 3 for j in range(5)):
            codes.append(sum(mask(row) << (5 * i) for i, row in enumerate(rows)))
    codes.sort()
    need(len(codes) == 2040, "cubic bipartite count")
    return codes


def bipartite_graph(code):
    return adj(10, [(i, j + 5) for i in range(5) for j in range(5)
                    if code >> (5 * i + j) & 1])


FOURS = sorted((mask(t), list(combinations(t, 2)), set(t))
               for t in combinations(range(10), 4))
FIVES = sorted((mask(t), list(combinations(t, 2)), set(t))
               for t in combinations(range(10), 5))


def residual(s0, rows):
    return [[s0[i][j] - sum(i in s and j in s for s in rows) for j in range(10)]
            for i in range(10)]


def bipartite_controls(codes):
    i_set, w = set(range(5)), {5, 6}
    z = set(range(10)) - w
    q = i_set | {5}
    records = []
    for code in codes:
        p = bipartite_graph(code)
        s0 = s0_matrix(p)
        cap = residual(s0, [z, q])
        negative = any(x < 0 for row in cap for x in row)
        words = []
        if not negative:
            for word, pairs, points in FOURS:
                if all(cap[a][b] >= 1 for a, b in pairs):
                    need(len(points & i_set) <= 1, "one-W six-row word lemma")
                    words.append(word)
        # A five-row wholly in Z: enumerate every possible second five-row.
        base = residual(s0, [z, i_set])
        five_hist = Counter()
        if all(x >= 0 for row in base for x in row):
            for _, pairs, points in FIVES:
                if all(base[a][b] >= 1 for a, b in pairs):
                    s = len(points & i_set)
                    need(s <= 2, "five-row overlap bound")
                    five_hist[s] += 1
        w_cap = s0[5][6]
        need(w_cap <= 3, "W pair cap")
        need(all(15 - s > 8 + w_cap for s in five_hist), "five-row incidence contradiction")
        records.append([code, negative, words, [[s, n] for s, n in sorted(five_hist.items())], w_cap])
    return {"records_sha256": digest(records), "pair_capacity_entries": len(codes) * 100,
            "negative_six_row_controls": sum(row[1] for row in records),
            "nonnegative_six_row_controls": sum(not row[1] for row in records),
            "admissible_four_word_counts": {str(k): v for k, v in sorted(Counter(len(row[2]) for row in records).items())},
            "second_five_row_records": sum(sum(n for _, n in row[3]) for row in records)}


def petersen_control():
    labels = list(combinations(range(5), 2))
    p = adj(10, [(i, j) for i, j in combinations(range(10), 2)
                 if set(labels[i]).isdisjoint(labels[j])])
    need(matmul(p, p) == [[2 * (i == j) + 1 - p[i][j] for j in range(10)]
                         for i in range(10)], "Petersen relation")
    independent = [sorted(s) for _, pairs, s in FOURS if all(not p[a][b] for a, b in pairs)]
    need(len(independent) == 5, "five independent four-sets")
    i_set = set(independent[0])
    o_set = set(range(10)) - i_set
    s0 = s0_matrix(p)
    records = []
    for w0 in combinations(sorted(o_set), 2):
        w = set(w0)
        z, q = set(range(10)) - w, i_set | w
        cap = residual(s0, [z, q])
        need(all(x >= 0 for row in cap for x in row), "Petersen large-row capacity")
        words = []
        for word, pairs, s in FOURS:
            if all(cap[a][b] >= 1 for a, b in pairs):
                count = len(s & i_set)
                need(count in (0, 1, 4), "two-W six-row word lemma")
                if count == 1:
                    need(all(not p[a][b] for a, b in pairs), "one-I row independence")
                words.append(word)
        records.append({"W": sorted(w), "red_W": bool(p[w0[0]][w0[1]]), "four_words": words})
    return p, independent, {"P": p, "I": sorted(i_set), "word_records": records}


def realize(degrees):
    d = degrees[:]
    edges = []
    while any(d):
        order = sorted(range(len(d)), key=lambda i: (-d[i], i))
        i, count = order[0], d[order[0]]
        targets = order[1:count + 1]
        need(len(targets) == count and all(d[j] > 0 for j in targets), "degree realization")
        d[i] = 0
        for j in targets:
            edges.append((i, j))
            d[j] -= 1
    g = adj(len(d), edges)
    need(list(map(sum, g)) == degrees, "realization degrees")
    return g


def pages(g, a, b):
    if g[a][b]:
        return [i for i in range(len(g)) if g[a][i] and g[b][i]]
    return [i for i in range(len(g)) if i not in (a, b) and not g[a][i] and not g[b][i]]


def contraction_control(p_plus, independent):
    x, y = next((i, j) for i, j in combinations(range(10), 2) if p_plus[i][j])
    p = [row[:] for row in p_plus]
    p[x][y] = p[y][x] = 0
    e = adj(10, [(x, y)])
    pe, ep = matmul(p, e), matmul(e, p)
    f = [[2 * e[i][j] + pe[i][j] + ep[i][j] for j in range(10)] for i in range(10)]
    sets = [set(range(10)) - {x, y}] + [set(s) for s in independent for _ in range(2)]
    s0, mg = s0_matrix(p), gram(sets)
    need(s0 == [[mg[i][j] + f[i][j] for j in range(10)] for i in range(10)], "contracted Gram")
    need(gram(sets[1:]) == k_matrix(p_plus), "K(P+E) contraction")
    h = list(map(sum, p))
    for i in range(10):
        t = sum(len(s) - 4 for s in sets if i in s)
        need(sum(f[i]) == 3 * h[i] + sum(h) - 24 - sum(h[j] for j in range(10) if p[i][j]) - t,
             "general defect margin")
    neighbors = list(range(1, 9))
    tail = realize([4 - (i in neighbors) for i in range(1, 11)])
    edges = [(0, i + 1) for i in range(10)]
    edges += [(i + 1, j + 1) for i, j in combinations(range(10), 2) if p[i][j]]
    edges += [(i + 1, b + 11) for b, s in enumerate(sets) for i in range(10) if i not in s]
    edges += [(11, b + 11) for b in neighbors]
    edges += [(i + 12, j + 12) for i, j in combinations(range(10), 2) if tail[i][j]]
    g = adj(22, edges)
    need(list(map(sum, g)) == [10] * 22, "literal contracted control regularity")
    for i, j in combinations(range(10), 2):
        need((3 if p[i][j] else 6) - len(pages(g, i + 1, j + 1)) == f[i][j], "literal local defect")
    c, d = next((c, d) for c, d in combinations(neighbors, 2) if sets[c] == sets[d])
    c, d = c + 11, d + 11
    actual_pages = pages(g, c, d)
    need(len(actual_pages) > (3 if g[c][d] else 6), "missing literal forbidden book")
    return {"low_pair": [x, y], "P": p, "F": f, "K": k_matrix(p_plus),
            "miss_sets": [sorted(s) for s in sets],
            "graph_rows": ["".join(map(str, row)) for row in g],
            "repeated_pair": [c, d], "spine_color": "red" if g[c][d] else "blue",
            "literal_pages": actual_pages}


def baseline():
    raw = (HERE / "baseline21.rows").read_bytes()
    rows = raw.decode().splitlines()
    n = len(rows)
    need(n == 21 and all(len(r) == n and set(r) <= {"0", "1"} for r in rows), "baseline format")
    g = [list(map(int, r)) for r in rows]
    need(all(g[i][i] == 0 and g[i][j] == g[j][i] for i in range(n) for j in range(n)), "baseline simple")
    maxima = [max(len(pages(g, i, j)) for i, j in combinations(range(n), 2) if g[i][j] == color)
              for color in (1, 0)]
    degrees = list(map(sum, g))
    need(sum(degrees) == 186 and maxima == [3, 6], "known witness mismatch")
    return {"order": n, "red_edges": sum(degrees) // 2,
            "degrees": {str(k): v for k, v in sorted(Counter(degrees).items())},
            "page_maxima": maxima, "rows_sha256": hashlib.sha256(raw).hexdigest()}


def build():
    codes = bipartite_codes()
    p, independent, p_record = petersen_control()
    return {"baseline": baseline(), "triple_controls": triple_controls(),
            "packing_controls": packing_controls(), "bipartite_codes": codes,
            "bipartite_controls": bipartite_controls(codes), "petersen_control": p_record,
            "contraction_control": contraction_control(p, independent)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="regenerate compact expected controls")
    args = parser.parse_args()
    record = build()
    path = HERE / "expected.json"
    if args.write:
        path.write_text(json.dumps(record, sort_keys=True, indent=2) + "\n")
    else:
        need(record == json.loads(path.read_text()), "expected control mismatch")
    print(json.dumps({"status": "PASS", "bipartite_matrices": len(record["bipartite_codes"]),
                      "labeled_triple_profiles": len(record["triple_controls"]["labeled_profiles"]),
                      "expected_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
