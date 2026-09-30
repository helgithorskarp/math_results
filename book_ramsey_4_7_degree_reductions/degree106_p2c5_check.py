#!/usr/bin/env python3
"""Exclude the P2+C5 branch, using compact complete necessary states.

The arbitrary-graph bridge and the three counting contradictions are in
degree106_p2c5.md. No full incidence matrix or graph is enumerated.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
import json
from pathlib import Path

from degree106_check import PAIRS, capacity, require, signed_rows, state

EDGES = {(0, 1), (2, 3), (3, 4), (4, 5), (5, 6), (2, 6)}
LEAVES = {0, 1}
CYCLE = {2, 3, 4, 5, 6}


def fingerprint(records):
    return sha256(json.dumps(sorted(records), separators=(",", ":")).encode()).hexdigest()


def adjacency(n, edges):
    out = [[0] * n for _ in range(n)]
    for a, b in edges:
        out[a][b] = out[b][a] = 1
    return out


def product(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def algebra_controls():
    """Check literal pages and the marked identity including its residual.

    These controls usually violate book caps and saturation. Neither their
    feasibility nor a classification of regular graphs is used in the proof.
    """
    ps = [adjacency(14, [(i, j) for i, j in combinations(range(14), 2)
                         if (j - i) % 14 in (1, 2, 3, 11, 12, 13)]),
          adjacency(14, [(i, j) for i, j in combinations(range(14), 2)
                         if i // 7 == j // 7]),
          adjacency(14, [(i, j) for i, j in combinations(range(14), 2)
                         if i // 7 != j // 7 and i % 7 != j % 7])]
    base = [{i % 7, (i + 1) % 7, (i + 3) % 7} for i in range(14)]
    require(all(sum(b in row for row in base) == 6 for b in range(7)), "control columns")
    l = adjacency(7, EDGES)
    h = list(map(sum, l))
    counts = Counter()
    diagnostics = []
    for graph_index, p in enumerate(ps):
        require(list(map(sum, p)) == [6] * 14, "control blue degrees")
        p2 = product(p, p)
        for marks in combinations(range(7), 2):
            for variant in range(2):
                missing = [[i for i, row in enumerate(base) if b not in row] for b in marks]
                i = missing[0][variant]
                j = next(a for a in missing[1][variant:] + missing[1][:variant] if a != i)
                rows = [row.copy() for row in base]
                rows[i].add(marks[0])
                rows[j].add(marks[1])
                m = [[int(b in row) for b in range(7)] for row in rows]
                k = list(map(sum, m))
                r = [v - 3 for v in k]
                w = [sum(row[b] for b in marks) for row in m]
                pr = [sum(p[a][z] * r[z] for z in range(14)) for a in range(14)]
                residual = [pr[a] - w[a] + r[a] for a in range(14)]
                pm, ml = product(p, m), product(m, l)
                red = [set() for _ in range(22)]

                def edge(a, b):
                    red[a].add(b)
                    red[b].add(a)

                for b in range(7):
                    edge(0, 15 + b)
                for a, z in combinations(range(14), 2):
                    if not p[a][z]:
                        edge(1 + a, 1 + z)
                for a in range(14):
                    for b in rows[a]:
                        edge(1 + a, 15 + b)
                for b, z in EDGES:
                    edge(15 + b, 15 + z)
                blue = [set(range(22)) - n - {a} for a, n in enumerate(red)]
                p_h = p[i][j]
                c = len(rows[i] & rows[j])
                gram_residual = c - 3 + p2[i][j] - 3 * p_h
                for a in (i, j):
                    defects = []
                    for b in range(7):
                        graph, bound = (red, 3) if m[a][b] else (blue, 6)
                        literal = bound - len(graph[1 + a] & graph[15 + b])
                        formula = pm[a][b] - ml[a][b] + h[b] - 2
                        formula -= m[a][b] * (h[b] + int(b in marks))
                        require(literal == formula, "literal cross-spine identity")
                        defects.append(literal)
                        counts["literal_cross_spines"] += 1
                    row_budget = 15 - 2 * sum(h[b] for b in rows[a])
                    require(sum(defects) == row_budget + residual[a], "row-budget residual")
                    simplified = 4 + 3 * p_h - c + sum(h[b] for b in marks)
                    simplified -= sum(h[b] for b in rows[a] & set(marks))
                    simplified -= sum(ml[a][b] for b in marks)
                    correction = gram_residual + residual[a]
                    correction -= sum(p[a][z] * residual[z] for z in range(14))
                    literal = sum(defects[b] for b in marks)
                    require(literal == simplified + correction, "marked-defect residual identity")
                    counts["marked_residual_identities"] += 1
                    counts["row_budget_identities"] += 1
                    counts["nonzero_residual_controls"] += int(correction != 0)
                    diagnostics.append([graph_index, list(marks), variant, a, literal,
                                        simplified, correction])
                counts["graphs"] += 1
    require(counts["nonzero_residual_controls"] > 0, "residual test is vacuous")
    return {"counts": dict(sorted(counts.items())), "stream_sha256": fingerprint(diagnostics),
            "interpretation": "algebra controls, not Ramsey witnesses"}


def counting_certificate(ones, hs, p, c, s):
    """Verify the hypotheses and numeric margins of the written cases."""
    w = set(ones)
    a, b = map(set, hs)
    if w == LEAVES:
        require(p == 0 and c == 3 and (a & b) <= CYCLE, "leaf-marked shape")
        require(len(a & LEAVES) == len(b & LEAVES) == 1 and
                a & LEAVES != b & LEAVES and a & CYCLE == b & CYCLE,
                "leaf-marked exceptional rows")
        require(s[0][1] == 0, "marked leaf columns must be disjoint")
        t = a & CYCLE
        require(all(s[x][y] == 2 for x, y in combinations(sorted(t), 2)), "triple pair capacities")
        induced_edges = sum(x in t and y in t for x, y in EDGES)
        demand = 6 + 2 * induced_edges
        require(demand > 6, "three C5 vertices are independent")
        return ["leaves", 6, demand]
    require(w <= CYCLE and LEAVES <= a and LEAVES <= b, "cycle-marked shape")
    require(s[0][1] == 2, "leaf pair capacity must be filled")
    adjacent = tuple(ones) in EDGES
    if adjacent:
        require(p == 0 and c == 2 and (a & CYCLE).isdisjoint(b & CYCLE),
                "adjacent cycle-marked shape")
    else:
        require(p == 1 and c == 4 and a == b == LEAVES | w,
                "nonadjacent cycle-marked shape")
    unmarked = CYCLE - w
    require(all(s[x][y] <= 2 for x, y in combinations(sorted(unmarked), 2)), "unmarked capacity")
    # Four cycle-only rows; across the two H vertices there are <=2p
    # blue incidences to those rows. Pr=w-r makes this their mark count.
    available = 2 * len(tuple(combinations(unmarked, 2)))
    forced = 4 * 3 - 2 * (2 * p)
    require(forced > available, "unmarked pair-budget contradiction")
    return ["adjacent_cycle" if adjacent else "nonadjacent_cycle", available, forced]


def reduction():
    h, _ = capacity(EDGES, [0] * 7)
    scalar_counts, filter_counts, shape_counts = Counter(), Counter(), Counter()
    raw, signed, survivors, certificates = [], [], [], []
    for ones in combinations(range(7), 2):
        sigma = [int(b in ones) for b in range(7)]
        weight = sum(h[b] for b in ones)
        for defect in combinations_with_replacement(range(21), 6 - weight):
            status, data = state(EDGES, sigma, 0, defect)
            scalar_counts[status] += 1
            raw.append([list(ones), list(defect), status])
            if data is None:
                continue
            s, u, q = data
            require(q == 0, "a=0 has negative incidence")
            for ts, hs, _ in signed_rows(h, sigma, 0, s, u, q):
                require(not ts, "a=0 has a negative row")
                record = [list(ones), 0, list(defect), [], [list(row) for row in hs]]
                signed.append(record)
                marked = [sum(sigma[b] for b in row) for row in hs]
                if marked[0] != marked[1] or marked[0] not in (1, 2):
                    filter_counts["positive_sigma_equation"] += 1
                    continue
                p = marked[0] - 1
                c = len(set(hs[0]) & set(hs[1]))
                if not 0 <= 3 + 3 * p - c <= 6 - p:
                    filter_counts["positive_pair_codegree"] += 1
                    continue
                valid = True
                for row in hs:
                    total = 15 - 2 * sum(h[b] for b in row)
                    marked_defect = 4 + 3 * p - c + weight
                    marked_defect -= sum(h[b] for b in row if sigma[b])
                    marked_defect -= sum(sigma[z] for b in row for z in range(7)
                                         if (min(b, z), max(b, z)) in EDGES)
                    valid &= 0 <= marked_defect <= total
                if not valid:
                    filter_counts["marked_cross_defects"] += 1
                    continue
                filter_counts["survive"] += 1
                survivors.append(record)
                certificate = counting_certificate(ones, hs, p, c, s)
                shape_counts[certificate[0]] += 1
                certificates.append([record, certificate])
    require(len(raw) == 30646 and len(signed) == 1180, "finite domain differs")
    require(fingerprint(signed) == "a1cd55a47f99be2d982e8402e29ac10e5f8b9f135c899c654f0e45348d1243f6",
            "published exceptional-row domain differs")
    require(filter_counts == Counter(positive_sigma_equation=190,
                                    marked_cross_defects=950, survive=40), "filter counts differ")
    require(shape_counts == Counter(leaves=10, adjacent_cycle=20, nonadjacent_cycle=10),
            "survivor shapes differ")
    return {"raw_states": len(raw), "scalar_counts": dict(sorted(scalar_counts.items())),
            "raw_states_sha256": fingerprint(raw), "signed_configurations": len(signed),
            "signed_sha256": fingerprint(signed), "filter_counts": dict(sorted(filter_counts.items())),
            "shapes": dict(sorted(shape_counts.items())), "survivors_sha256": fingerprint(survivors),
            "counting_certificates_sha256": fingerprint(certificates),
            "excluded_configurations": len(survivors)}, {
                "signed": sorted(signed), "survivors": sorted(survivors),
                "certificates": sorted(certificates)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", type=Path, help="optional private complete entry stream")
    args = parser.parse_args()
    result, records = reduction()
    output = {"agent": "six-books-1", "role": "researcher",
              "claim": "P2+C5 excluded only for a degree-seven root in the 106-edge e6/t2 branch",
              "reduction": result, "algebra_controls": algebra_controls()}
    expected = Path(__file__).with_name("degree106_p2c5_expected.json")
    require(output == json.loads(expected.read_text()), "compact expected output differs")
    if args.records:
        args.records.write_text(json.dumps(records, separators=(",", ":")) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
