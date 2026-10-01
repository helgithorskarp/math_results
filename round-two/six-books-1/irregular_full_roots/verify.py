#!/usr/bin/env python3
"""Independent set/matrix replay. Imports no producer or campaign code."""
from copy import deepcopy
import hashlib
from itertools import combinations, combinations_with_replacement, permutations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def need(test, message):
    if not test:
        raise ValueError(message)


def sets(words):
    n = len(words)
    need(all(type(z) is int and 0 <= z < 2**n for z in words), "bit words")
    graph = [{j for j in range(n) if words[i] & 2**j} for i in range(n)]
    need(all(i not in graph[i] for i in range(n)), "simple loops")
    need(all((j in graph[i]) == (i in graph[j]) for i in range(n) for j in range(n)),
         "simple symmetry")
    return graph


def summary(graph):
    n = len(graph)
    blue = [set(range(n)) - {i} - graph[i] for i in range(n)]
    degree = [len(row) for row in graph]
    return {"edges": sum(degree) // 2,
            "degree_histogram": [[d, degree.count(d)] for d in sorted(set(degree))],
            "red_max": max(len(graph[i] & graph[j]) for i, j in combinations(range(n), 2)
                           if j in graph[i]),
            "blue_max": max(len(blue[i] & blue[j]) for i, j in combinations(range(n), 2)
                            if j not in graph[i])}


def rooted_model(cycle):
    g = [set() for _ in range(10)]

    def edge(a, b):
        g[a].add(b)
        g[b].add(a)

    for parent in range(1, 4):
        edge(0, parent)
        edge(parent, 3 + parent)
        edge(parent, 6 + parent)
    for i in range(4, 9):
        edge(i, i + 1)
    if cycle:
        edge(4, 9)
    return g


def verify_control(record, expected_local, kind, mapping):
    need(record["local"] == expected_local, "control local model")
    p = sets(record["local"])
    words = record["miss_rows"]
    need(len(words) == 11 and all(type(z) is int and 0 <= z < 1024 for z in words),
         "miss inputs")
    z = [{i for i in range(10) if w & 2**i} for w in words]
    d = record["deficits"]
    need(len(d) == 11 and all(x in [0, 1, 2] for x in d) and sum(d) == 2, "control deficits")
    if kind == 9:
        need(sorted(d) == [0] * 9 + [1, 1], "nine control degree pattern")
    else:
        need(sorted(d) == [0] * 10 + [2], "eight control degree pattern")
    need(len(z[0]) == kind, "large-row size")
    bgraph = sets(record["outside"])
    need([len(a) for a in bgraph] == [len(z[t]) - d[t] for t in range(11)], "B degrees")
    g = [set() for _ in range(22)]

    def edge(a, b):
        g[a].add(b)
        g[b].add(a)

    for i in range(10):
        edge(0, i + 1)
        for j in p[i]:
            edge(i + 1, j + 1)
        for b in range(11):
            if i not in z[b]:
                edge(i + 1, b + 11)
    for b in range(11):
        for c in bgraph[b]:
            edge(b + 11, c + 11)
    need(g == sets(record["host"]), "literal host reconstruction")
    need([len(g[i]) for i in range(11)] == [10] * 11, "full root degrees")
    need([10 - len(g[b + 11]) for b in range(11)] == d, "literal low points")
    need(summary(g) == record["summary"] and record["summary"]["edges"] == 109, "host summary")
    blue = [set(range(22)) - {i} - g[i] for i in range(22)]
    h = [len(a) for a in p]
    f = [[0] * 10 for _ in range(10)]
    s0 = [[0] * 10 for _ in range(10)]
    gram = [[sum(i in a and j in a for a in z) for j in range(10)] for i in range(10)]
    for i in range(10):
        need(sum(i in a for a in z) == h[i] + 2, "literal column")
        for j in range(10):
            if i == j:
                s0[i][j] = h[i] + 2
            else:
                red = j in p[i]
                pages = len(g[i + 1] & g[j + 1]) if red else len(blue[i + 1] & blue[j + 1])
                f[i][j] = (3 if red else 6) - pages
                s0[i][j] = h[i] + h[j] - (5 if red else 2) - len(p[i] & p[j])
            need(gram[i][j] + f[i][j] == s0[i][j], "literal signed Gram")
        u = sum(len(a) - 4 for a in z if i in a)
        need(sum(f[i]) + u == 3 * h[i] + sum(h) - 24 - sum(h[j] for j in p[i]),
             "literal defect margin")
    need(all(x >= 0 for row in f for x in row), "A capacity nonnegative")
    full = rooted_model(True)
    # A model independent of the two-subset producer, moved by its certified map.
    q = [set() for _ in range(10)]
    for i in range(10):
        q[mapping[i]] = {mapping[j] for j in full[i]}
    kernel = [[2 * (i == j) + 2 - 2 * (j in q[i]) for j in range(10)] for i in range(10)]
    if kind == 10:
        need(all(x == 0 for row in f for x in row), "ten capacity")
        need([[gram[i][j] - 1 for j in range(10)] for i in range(10)] == kernel,
             "ten contraction")
    elif kind == 9:
        five = next(a for a in z if len(a) == 5)
        center = next(iter(set(range(10)) - z[0]))
        need(center in five, "star center in five-row")
        r = five - {center}
        for i in range(10):
            for j in range(10):
                total = int(i in z[0] and j in z[0]) + int(i in five and j in five) + f[i][j]
                need(total == 1 + int(i in r and j in r), "literal rank-one identity")
                need(kernel[i][j] == gram[i][j] - int(i in z[0] and j in z[0])
                     - int(i in five and j in five) + int(i in r and j in r), "nine contraction")
    else:
        low = [i for i in range(10) if h[i] == 2]
        need(len(low) == 2 and z[0] == set(range(10)) - set(low), "eight row cubic set")
        x, y = low
        e = [[int((i, j) in [(x, y), (y, x)]) for j in range(10)] for i in range(10)]
        pa = [[int(j in p[i]) for j in range(10)] for i in range(10)]
        for i in range(10):
            for j in range(10):
                expansion = 2 * e[i][j] + sum(pa[i][t] * e[t][j] + e[i][t] * pa[t][j]
                                                for t in range(10))
                need(f[i][j] == expansion, "eight defect expansion")
                need(gram[i][j] - int(i in z[0] and j in z[0]) == kernel[i][j], "eight contraction")
    delta = [10 - len(row) for row in g]
    adjacency = [[int(j in g[i]) for j in range(22)] for i in range(22)]
    for i in range(22):
        for j in range(22):
            a = adjacency[i][j]
            form = sum(adjacency[i][t] * adjacency[t][j] for t in range(22)) + 3 * a
            capacity = 0 if i == j else (3 - len(g[i] & g[j]) if a else 6 - len(blue[i] & blue[j]))
            corrected = 4 * (i == j) + 6 - delta[i] - delta[j] + delta[i] * (i == j)
            corrected += (delta[i] + delta[j]) * a - capacity
            need(form == corrected, "whole near-regular identity")
    s, t = record["book_spine"]
    need(t not in g[s], "control blue book spine")
    pages = sorted(blue[s] & blue[t])
    need(pages == record["book_pages"] and len(pages) >= 7, "literal blue book")
    need(record["local_identity_entries"] == 100 and record["whole_identity_entries"] == 484,
         "coverage labels")


def leaf_census():
    pairs = list(combinations(range(6), 2))
    counts = [0, 0]
    for bits in range(2**15):
        weight = bits.bit_count()
        if weight not in [5, 6]:
            continue
        g = [set() for _ in range(6)]
        for k, (a, b) in enumerate(pairs):
            if bits & 2**k:
                g[a].add(b)
                g[b].add(a)
        ds = [len(a) for a in g]
        if ds == [2] * 6:
            kind = 0
        elif ds == [1, 2, 2, 2, 2, 1]:
            kind = 1
        else:
            continue
        if any(len(g[a] & g[b]) >= 2 for a, b in pairs):
            continue
        if any(b in g[a] and g[a] & g[b] for a, b in pairs):
            continue
        counts[kind] += 1
    return {"cycle_degree_graphs": counts[0], "path_degree_graphs": counts[1]}


def verify(data, finite=True):
    need(data["schema"] == 1 and data["agent"] == "six-books-1" and data["role"] == "researcher",
         "identity labels")
    profiles = {tuple(a.count(x) for x in [0, 2, 3]) for a in product([0, 2, 3], repeat=10)
                if a.count(0) <= 1 and 26 <= sum(a) <= 30 and sum(a) % 2 == 0}
    need(profiles == {tuple(a) for a in data["profiles"]} and len(data["profiles"]) == 4,
         "profile coverage")
    patterns = [tuple(a) for a in product([2, 3], repeat=4)]
    need([tuple(a["degrees"]) for a in data["cycle_degree_checks"]] == patterns, "cycle degrees")
    for row in data["cycle_degree_checks"]:
        h = row["degrees"]
        lower = sum(d + 2 for d in h) - 11
        red = sum(h[i] + h[(i + 1) % 4] - 5 for i in range(4))
        opposite = sum(h[i] + h[i + 2] - 4 for i in range(2))
        need([row["lower"], row["upper"]] == [lower, red + opposite] and red + opposite < lower,
             "cycle strict gap")
    if finite:
        scores = {h: 10**9 for h in range(8, 13)}
        for counts in combinations_with_replacement(range(5), 11):
            h = sum(counts) - 8
            if h in scores:
                scores[h] = min(scores[h], sum(t * (t - 1) // 2 for t in counts))
        need([[h, scores[h]] for h in scores] == data["packing_minima"], "independent packing minimum")
        need(leaf_census() == data["leaf_census"] == {"cycle_degree_graphs": 60, "path_degree_graphs": 24},
             "independent leaf census")
    need(data["low_overlap_union_lower"] == [[1, 12], [2, 13]], "packing constants")
    for r in [1, 2]:
        wx = set(range(4))
        wy = [{i for i in range(11) if word & 2**i} for word in range(2**11) if word.bit_count() == 4]
        need(all(len(set(range(11)) - wx - a) < 5 for a in wy if len(wx & a) <= 2 - r),
             "common cubic column cannot fit")
    valid_path = set()
    valid_cycle = set()
    for perm in permutations(range(6)):
        matching = tuple(sorted(tuple(sorted(perm[k:k + 2])) for k in [0, 2, 4]))
        if all(abs(a - b) >= 3 for a, b in matching):
            valid_path.add(matching)
        if all(min(abs(a - b), 6 - abs(a - b)) == 3 for a, b in matching):
            valid_cycle.add(matching)
    need(len(valid_path) == len(valid_cycle) == 1, "all leaf pairings")
    need(valid_path == {tuple(tuple(a) for a in q) for q in data["path_pairings"]}, "path pairing record")
    need(valid_cycle == {tuple(tuple(a) for a in q) for q in data["cycle_pairings"]}, "cycle pairing record")
    p = sets(data["petersen"])
    deleted = sets(data["deleted_petersen"])
    x, y = data["deleted_edge"]
    need(y in p[x] and deleted == [a - ({y} if i == x else {x} if i == y else set())
                                   for i, a in enumerate(p)], "one deleted edge")
    for key, source, target in [("leaf_full_isomorphism", rooted_model(True), p),
                                ("leaf_deleted_isomorphism", rooted_model(False), deleted)]:
        mapping = data[key]
        need(sorted(mapping) == list(range(10)), "isomorphism bijection")
        need(all({mapping[j] for j in source[i]} == target[mapping[i]] for i in range(10)), "model isomorphism")
    for i in range(10):
        need(len(p[i]) == 3, "cubic model")
        for j in range(10):
            need(len(p[i] & p[j]) + int(j in p[i]) == 2 * (i == j) + 1, "Petersen matrix relation")
    independent = [sum(2**i for i in range(10) if word & 2**i) for word in range(1024)
                   if word.bit_count() == 4 and all(j not in p[i] for i in range(10) for j in range(i + 1, 10)
                                                  if word & 2**i and word & 2**j)]
    need(len(independent) == 5 and set(independent) == set(data["independent_four_sets"]), "four sets")
    names = ["ten-row-one-degree-eight", "nine-row-two-degree-nine", "edge-deleted-eight-row-degree-eight"]
    need([r["name"] for r in data["controls"]] == names, "three controls")
    for rec, local, kind in zip(data["controls"], [data["petersen"], data["petersen"], data["deleted_petersen"]], [10, 9, 8]):
        verify_control(rec, local, kind, data["leaf_full_isomorphism"])
    fixture = (HERE / "baseline21.rows").read_text().splitlines()
    baseline = [{j for j, c in enumerate(line) if c == "1"} for line in fixture]
    need(len(baseline) == 21 and summary(baseline) == data["baseline"] == {
        "edges": 93, "degree_histogram": [[8, 4], [9, 16], [10, 1]], "red_max": 3, "blue_max": 6}, "baseline")


if __name__ == "__main__":
    DATA = json.loads((HERE / "expected.json").read_text())
    verify(DATA)
    damaged = []
    x = deepcopy(DATA); x["cycle_degree_checks"][0]["upper"] += 1; damaged.append(x)
    x = deepcopy(DATA); x["controls"].pop(); damaged.append(x)
    x = deepcopy(DATA); x["controls"][2]["deficits"][0] = 1; damaged.append(x)
    x = deepcopy(DATA); x["leaf_full_isomorphism"][0] = x["leaf_full_isomorphism"][1]; damaged.append(x)
    x = deepcopy(DATA); x["controls"][0]["miss_rows"][2] ^= 1; damaged.append(x)
    x = deepcopy(DATA); x["controls"][1]["book_pages"].pop(); damaged.append(x)
    for x in damaged:
        try:
            verify(x, finite=False)
        except ValueError:
            continue
        raise ValueError("damaged control accepted")
    print(json.dumps({"status": "PASS", "rejected_forged_controls": len(damaged),
                      "literal_local_entries": 300, "literal_whole_entries": 1452,
                      "expected_sha256": hashlib.sha256((HERE / "expected.json").read_bytes()).hexdigest()}))
