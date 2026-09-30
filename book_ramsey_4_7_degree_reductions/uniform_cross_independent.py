#!/usr/bin/env python3
"""Independent binary-recursion and literal-page check for uniform_cross.md.

Imports no generator/matrix code. Every B graph of maximum degree three
is generated once, without restricting its edge count. Every retained
graph is tested by integer page intersections. Author implementation
independence is not independent peer review or proof formalization.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json


PAIRS = [(i, j) for i in range(7) for j in range(i+1, 7)]
ALL = (1 << 22)-1


def check(ok, message):
    if not ok:
        raise ValueError(message)


def domain():
    degrees = [0]*7

    def walk(pos, mask):
        if pos == len(PAIRS):
            yield mask
            return
        yield from walk(pos+1, mask)
        x, y = PAIRS[pos]
        if degrees[x] < 3 and degrees[y] < 3:
            degrees[x] += 1
            degrees[y] += 1
            yield from walk(pos+1, mask | (1 << pos))
            degrees[x] -= 1
            degrees[y] -= 1

    return list(walk(0, 0))


def digest(masks):
    h = sha256()
    for mask in sorted(masks):
        h.update(f"{mask};".encode())
    return h.hexdigest()


def build(q):
    qsets = [((1 << i) | (1 << j)) for i, j in q]
    aset = [((1 << i) | (1 << j)) for i, j in PAIRS if (i, j) not in q]
    red = [0]*22

    def edge(i, j):
        red[i] |= 1 << j
        red[j] |= 1 << i

    for b in range(7):
        edge(0, 15+b)
    for a in range(14):
        for c in range(a+1, 14):
            if not (aset[a] & aset[c]):
                edge(1+a, 1+c)
        for b in range(7):
            if not (aset[a] & qsets[b]):
                edge(1+a, 15+b)
    return red


def column_domain(q):
    edges = [edge for edge in PAIRS if edge not in q]
    index = {edge: j for j, edge in enumerate(edges)}
    triangle = next((a, b, c) for a, b, c in combinations(range(7), 3)
                    if all(tuple(sorted(edge)) in index for edge in ((a, b), (a, c), (b, c))))
    a, b, c = triangle
    retained = []
    for chosen in combinations(range(14), 6):
        mask = sum(1 << j for j in chosen)

        def value(i, j):
            return (mask >> index[tuple(sorted((i, j)))]) & 1

        potentials = [None]*7
        potentials[a] = value(a, b)+value(a, c)-value(b, c)
        potentials[b] = 2*value(a, b)-potentials[a]
        potentials[c] = 2*value(a, c)-potentials[a]
        for _ in range(7):
            for j, (x, y) in enumerate(edges):
                bit = (mask >> j) & 1
                if potentials[x] is None and potentials[y] is not None:
                    potentials[x] = 2*bit-potentials[y]
                if potentials[y] is None and potentials[x] is not None:
                    potentials[y] = 2*bit-potentials[x]
        check(all(x is not None for x in potentials), "Disconnected incidence graph")
        if all(potentials[x]+potentials[y] == 2*((mask >> j) & 1)
               for j, (x, y) in enumerate(edges)):
            check(sum(potentials) == 3 and sorted(potentials) == [-1, -1, 1, 1, 1, 1, 1],
                  "Unexpected binary edge potential")
            retained.append(mask)
    check(len(retained) == 7, "Complete incidence-image column domain")
    return sorted(retained)


def analyze(name, q, masks, by_edges, reference):
    base = build(q)
    columns = sorted(sum(((base[1+a] >> (15+b)) & 1) << a for a in range(14)) for b in range(7))
    check(column_domain(q) == columns == reference["control"]["column_masks"],
          "Independent binary column domain differs")
    blue_base = [ALL ^ base[i] ^ (1 << i) for i in range(22)]
    for x in range(1, 15):
        check((blue_base[0] & blue_base[x]).bit_count() == 6, "Root-A saturation")
        for y in range(x+1, 15):
            color = base if (base[x] >> y) & 1 else blue_base
            cap = 3 if color is base else 6
            check((color[x] & color[y]).bit_count() == cap, "A-A saturation")
    records, survivor_counts, histograms = [], Counter(), [Counter() for _ in range(11)]
    literal_spines_checked = 0
    hsets = [((1 << x) | (1 << y)) for x, y in PAIRS if (x, y) not in q]
    qsets = [((1 << x) | (1 << y)) for x, y in q]
    for mask in masks:
        red = base.copy()
        for j, (b, c) in enumerate(PAIRS):
            if (mask >> j) & 1:
                red[15+b] |= 1 << (15+c)
                red[15+c] |= 1 << (15+b)
        blue = [ALL ^ red[i] ^ (1 << i) for i in range(22)]
        check(all((red[0] & red[15+b]).bit_count() <= 3 for b in range(7)),
              "Binary recursion admits a root book")
        valid_B = True
        for b, c in PAIRS:
            x, y = 15+b, 15+c
            color = red if (red[x] >> y) & 1 else blue
            cap = 3 if color is red else 6
            if (color[x] & color[y]).bit_count() > cap:
                valid_B = False
                break
        if not valid_B:
            continue
        target = mask.bit_count()
        survivor_counts[target] += 1
        bad, red_count, blue_count = [], 0, 0
        for a in range(14):
            for b in range(7):
                x, y = 1+a, 15+b
                color = red if (red[x] >> y) & 1 else blue
                cap = 3 if color is red else 6
                common = color[x] & color[y]
                literal_spines_checked += 1
                if common.bit_count() > cap:
                    red_count += color is red
                    blue_count += color is blue
                    pages = [i for i in range(22) if (common >> i) & 1][:cap+1]
                    check(len(pages) == cap+1 and x not in pages and y not in pages, "Literal book")
                    bad.append(([x, y], pages))
        check(bool(bad), "Valid template survived; inspect full witness")
        core_triple = None
        for t in combinations(range(7), 3):
            labels = list(range(1, 15))+[15+b for b in t]
            pairs = hsets+[qsets[b] for b in t]
            if all(bool((red[labels[i]] >> labels[j]) & 1) == (not bool(pairs[i] & pairs[j]))
                   for i, j in combinations(range(17), 2)):
                core_triple = list(t)
                break
        check(core_triple is not None, "Induced KG17 certificate is missing")
        histograms[target][(red_count, blue_count)] += 1
        spine, pages = bad[0]
        records.append([mask, red_count, blue_count, spine, pages, core_triple])
    records.sort(key=lambda r: r[0])
    check(records == reference["book_records"], "Whole literal survivor/book records differ")
    for target in range(11):
        r = reference["by_B_edges"][target]
        check(r["red_B_edges"] == target and len(by_edges[target]) == r["root_spines_pass"]
              and digest(by_edges[target]) == r["root_domain_sha256"], "Whole per-size root domain differs")
        check(survivor_counts[target] == r["B_spines_pass"]
              and [list(key)+[value] for key, value in sorted(histograms[target].items())]
              == r["cross_violation_histogram"], "Per-size literal survivor diagnostics differ")
    check(digest(masks) == reference["whole_root_domain_sha256"], "Whole recursive root domain differs")
    check(len(records) == (8 if name == "C7" else 180), "Complete B survivor count")
    return {"name": name, "root_valid_B_graphs": len(masks), "B_spine_survivors": len(records),
            "binary_column_domain": len(columns), "valid_completions": 0,
            "literal_cross_spines_checked": literal_spines_checked,
            "whole_domain_sha256": digest(masks), "records_agree_entrywise": True}


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    expected = json.loads((root / "uniform_cross_expected.json").read_text())
    masks = domain()
    check(len(masks) == len(set(masks)) == 236926, "Full binary recursion domain")
    by_edges = [[mask for mask in masks if mask.bit_count() == e] for e in range(11)]
    check(sum(map(len, by_edges)) == len(masks), "Every root-permitted edge count included")
    cases = [("C7", sorted({tuple(sorted((i, (i+1) % 7))) for i in range(7)})),
             ("C3+C4", [(0, 1), (0, 2), (1, 2), (3, 4), (3, 6), (4, 5), (5, 6)])]
    result = [analyze(name, q, masks, by_edges, expected["templates"][i])
              for i, (name, q) in enumerate(cases)]
    print(json.dumps({"agent": "six-books-1", "role": "researcher",
                      "status": "independent implementation, author check", "templates": result},
                     sort_keys=True, separators=(",", ":")))
