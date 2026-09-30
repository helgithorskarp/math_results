#!/usr/bin/env python3
"""Complete exact completion check for uniform_cross.md.

The combinations generator and matrix spine capacities are checked against
literal pages on every B-spine survivor. Shared exact incidence controls are
explicit source dependencies in degree105_check.py; no previous expected
output is used. The spectral/written reduction is a separate proof bridge.
"""

from collections import Counter
from hashlib import sha256
from itertools import combinations
from math import comb
from pathlib import Path
import json
import sys

from degree105_check import (PAIRS, adjacency, baseline, line_control,
                             literal_graph, multiply, neighbors, require,
                             templates, transpose)


ROOT = Path(__file__).resolve().parent


def digest(masks):
    h = sha256()
    for mask in sorted(masks):
        h.update(f"{mask};".encode())
    return h.hexdigest()


def complete(name, q):
    p, m, control = line_control(q)
    s = multiply(transpose(m), m)
    pm = multiply(p, m)
    base_red, base_blue = literal_graph(p, m, adjacency(7, []))
    for a in range(14):
        require((base_blue[0] & base_blue[1+a]).bit_count() == 6,
                "Root-A blue saturation")
        for c in range(a+1, 14):
            color = base_red if not p[a][c] else base_blue
            require((color[1+a] & color[1+c]).bit_count() == (3 if color is base_red else 6),
                    "A-A saturation")
    by_edges, records, whole_domain = [], [], []
    for target in range(11):
        counts = {"red_B_edges": target, "subsets": 0, "root_spines_pass": 0,
                  "B_spines_pass": 0, "all_cross_spines_pass": 0}
        domain, histogram = [], Counter()
        for chosen in combinations(range(21), target):
            counts["subsets"] += 1
            edges = [PAIRS[j] for j in chosen]
            ln = neighbors(7, edges)
            h = [row.bit_count() for row in ln]
            if max(h) > 3:
                continue
            mask = sum(1 << j for j in chosen)
            domain.append(mask)
            counts["root_spines_pass"] += 1
            if any(s[b][c] > (2 if (ln[b] >> c) & 1 else h[b]+h[c]-1)
                   -(ln[b] & ln[c]).bit_count() for b, c in PAIRS):
                continue
            counts["B_spines_pass"] += 1
            ml = multiply(m, adjacency(7, edges))
            bad = []
            for a in range(14):
                for b in range(7):
                    d = pm[a][b]-ml[a][b]
                    delta = d-2 if m[a][b] else d+h[b]-3
                    if delta < 0:
                        bad.append((a, b, delta))
            if not bad:
                counts["all_cross_spines_pass"] += 1
                raise ValueError("A uniform-template witness survived; inspect it")
            red, blue = literal_graph(p, m, adjacency(7, edges))
            literal = []
            for i, j in combinations(range(22), 2):
                color = red if (red[i] >> j) & 1 else blue
                cap = 3 if color is red else 6
                common = color[i] & color[j]
                if common.bit_count() > cap:
                    literal.append((i, j, cap, common))
            require([(i, j) for i, j, cap, common in literal] ==
                    [(1+a, 15+b) for a, b, delta in bad], "All 231 literal spines differ")
            for (a, b, delta), (i, j, cap, common) in zip(bad, literal):
                require(common.bit_count() == cap-delta and cap == (3 if m[a][b] else 6),
                        "Matrix defect and literal pages differ")
            i, j, cap, common = literal[0]
            pages = [x for x in range(22) if (common >> x) & 1][:cap+1]
            require(len(pages) == cap+1 and i not in pages and j not in pages,
                    "Invalid explicit book")
            core_triple = next((list(t) for t in combinations(range(7), 3)
                                if all(bool((ln[b] >> c) & 1) == set(q[b]).isdisjoint(q[c])
                                       for b, c in combinations(t, 2))), None)
            require(core_triple is not None, "B-spine survivor has no canonical induced KG17 core")
            labels = list(range(1, 15))+[15+b for b in core_triple]
            point_pairs = control["H_edges"]+[q[b] for b in core_triple]
            require(all(bool((red[labels[x]] >> labels[y]) & 1) ==
                        set(point_pairs[x]).isdisjoint(point_pairs[y])
                        for x, y in combinations(range(17), 2)), "Literal induced KG17 core certificate")
            red_bad = sum(m[a][b] for a, b, delta in bad)
            blue_bad = len(bad)-red_bad
            histogram[(red_bad, blue_bad)] += 1
            # Schema: mask, red violations, blue violations, spine, pages, B core triple.
            # The mask reconstructs all B edges, so no edge dump is needed.
            records.append([mask, red_bad, blue_bad, [i, j], pages, core_triple])
        require(counts["subsets"] == comb(21, target), "Combinations coverage count")
        whole_domain.extend(domain)
        counts["root_domain_sha256"] = digest(domain)
        counts["cross_violation_histogram"] = [list(key)+[value]
                                               for key, value in sorted(histogram.items())]
        by_edges.append(counts)
    require(len(whole_domain) == len(set(whole_domain)) == 236926, "Whole root-admissible domain")
    require(sum(c["subsets"] for c in by_edges) == 1 << 20, "All root-permitted edge counts covered")
    records.sort(key=lambda r: r[0])
    require(len(records) == (8 if name == "C7" else 180), "B survivor count")
    return {"name": name, "control": control, "by_B_edges": by_edges,
            "whole_root_domain_sha256": digest(whole_domain), "book_records": records,
            "valid_completions": 0}


def run():
    return {"agent": "six-books-1", "role": "researcher",
            "claim": "Every degree-seven order22 witness has irregular cross-incidence rows",
            "scope": "All labeled B graphs; no edge-count or symmetry hypothesis",
            "proof_status": "written reduction, external spectral classification, exact completion check",
            "record_schema": ["B_edge_mask", "red_cross_violations", "blue_cross_violations", "spine", "pages", "KG17_B_triple"],
            "baseline": baseline(), "templates": [complete(name, q) for name, q in templates()]}


if __name__ == "__main__":
    result = run()
    encoded = json.dumps(result, sort_keys=True, separators=(",", ":"))
    if "--emit-only" not in sys.argv:
        require(json.loads(encoded) == json.loads((ROOT / "uniform_cross_expected.json").read_text()),
                "Expected exact diagnostics differ")
    print(encoded)
