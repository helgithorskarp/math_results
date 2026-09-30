#!/usr/bin/env python3
"""Independent literal-page checker for the two forced order22 templates.

Imports no generator code. Reconstructs incidence-image column domains by
triangle potentials, and B graphs by binary edge recursion. Author check,
not independent peer review. The written/external reduction is not formalized.
"""

from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json


def check(ok, message):
    if not ok:
        raise ValueError(message)


PAIRS = [(i, j) for i in range(7) for j in range(i+1, 7)]
ALL = (1 << 22)-1


def domain():
    degrees = [0]*7

    def walk(pos, left, mask):
        if left == 0:
            yield mask
            return
        if 21-pos < left:
            return
        yield from walk(pos+1, left, mask)
        x, y = PAIRS[pos]
        if degrees[x] < 3 and degrees[y] < 3:
            degrees[x] += 1
            degrees[y] += 1
            yield from walk(pos+1, left-1, mask | (1 << pos))
            degrees[x] -= 1
            degrees[y] -= 1

    return list(walk(0, 7, 0))


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

        potentials = [None]*7  # Twice x, determined through a triangle and graph propagation.
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
        check(all(x is not None for x in potentials), "Disconnected H")
        if all(potentials[x]+potentials[y] == 2*((mask >> j) & 1)
               for j, (x, y) in enumerate(edges)):
            check(sum(potentials) == 3 and sorted(potentials) == [-1, -1, 1, 1, 1, 1, 1],
                  "Unexpected binary potential")
            retained.append(mask)
    check(len(retained) == 7, "Complete column domain differs")
    return sorted(retained)


def analyze(name, q, masks, reference):
    base = build(q)
    columns = sorted(sum(((base[1+a] >> (15+b)) & 1) << a for a in range(14)) for b in range(7))
    check(column_domain(q) == columns == reference["control"]["column_masks"],
          "Independent incidence-image domain differs")
    blue_base = [ALL ^ base[i] ^ (1 << i) for i in range(22)]
    for x in range(1, 15):
        check((blue_base[0] & blue_base[x]).bit_count() == 6, "Root blue saturation")
        for y in range(x+1, 15):
            color = base if (base[x] >> y) & 1 else blue_base
            limit = 3 if color is base else 6
            check((color[x] & color[y]).bit_count() == limit, "A-spine saturation")
    records = []
    for mask in masks:
        red = base.copy()
        edges = []
        for j, (b, c) in enumerate(PAIRS):
            if (mask >> j) & 1:
                red[15+b] |= 1 << (15+c)
                red[15+c] |= 1 << (15+b)
                edges.append([b, c])
        blue = [ALL ^ red[i] ^ (1 << i) for i in range(22)]
        check(all((red[0] & red[15+b]).bit_count() <= 3 for b in range(7)),
              "Recursive domain admits root book")
        invalid_B = False
        for b, c in PAIRS:
            x, y = 15+b, 15+c
            color = red if (red[x] >> y) & 1 else blue
            cap = 3 if color is red else 6
            if (color[x] & color[y]).bit_count() > cap:
                invalid_B = True
                break
        if invalid_B:
            continue
        bad = []
        for a in range(14):
            for b in range(7):
                x, y = 1+a, 15+b
                color = red if (red[x] >> y) & 1 else blue
                cap = 3 if color is red else 6
                common = color[x] & color[y]
                if common.bit_count() > cap:
                    check(color is blue and common.bit_count() == 7, "Unexpected violation")
                    bad.append((x, y, [i for i in range(22) if (common >> i) & 1]))
        check(len(bad) == 14, "All surviving completions must have fourteen blue cross books")
        x, y, pages = bad[0]
        records.append({"B_edge_mask": mask, "B_edges": edges,
                        "B_degrees": [(red[15+b] & (((1 << 7)-1) << 15)).bit_count() for b in range(7)],
                        "violating_blue_cross_spines": len(bad),
                        "book": {"color": "blue", "spine": [x, y], "pages": pages}})
    records.sort(key=lambda r: r["B_edges"])
    check(records == reference["B_spine_survivors"], "Literal survivor/book records differ")
    stream = sha256()
    for mask in sorted(masks):
        stream.update(f"{mask};".encode())
    check(stream.hexdigest() == reference["root_domain_stream_sha256"], "Whole recursive domain differs")
    check(len(records) == (1 if name == "C7" else 24), "Complete B survivor count differs")
    return {"name": name, "recursive_root_valid_B_graphs": len(masks),
            "binary_potential_columns": len(columns), "B_spine_survivors": len(records),
            "valid_completions": 0, "literal_books_checked": 14*len(records),
            "whole_domain_sha256": stream.hexdigest(), "records_agree_entrywise": True}


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    expected = json.loads((root / "degree105_expected.json").read_text())
    masks = domain()
    check(len(masks) == len(set(masks)) == 66090, "Binary recursion coverage count")
    cases = [("C7", sorted({tuple(sorted((i, (i+1) % 7))) for i in range(7)})),
             ("C3+C4", [(0, 1), (0, 2), (1, 2), (3, 4), (3, 6), (4, 5), (5, 6)])]
    result = [analyze(name, q, masks, expected["templates"][i]) for i, (name, q) in enumerate(cases)]
    print(json.dumps({"agent": "six-books-1", "role": "researcher",
                      "status": "independent implementation, author check", "templates": result},
                     indent=2, sort_keys=True))
