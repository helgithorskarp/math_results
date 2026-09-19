#!/usr/bin/env python3
"""Exact supplementary audit for PROOF.md and CASE_TABLE.md.

Python 3.11 standard library. No assertions are disabled by python -O.
No recognition or enumeration of homology spheres is claimed.
"""
from itertools import combinations, permutations, product
from math import comb
from pathlib import Path
import json


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def edges(n, mask):
    return {e for i, e in enumerate(combinations(range(n), 2)) if mask >> i & 1}


def code(n, es):
    return sum(1 << i for i, e in enumerate(combinations(range(n), 2)) if e in es)


def adjacency(n, es):
    return [{w for w in range(n) if tuple(sorted((v, w))) in es} for v in range(n)]


def count_edges(es, vertices):
    return sum(e in es for e in combinations(sorted(vertices), 2))


def alpha(es, vertices):
    vertices = sorted(vertices)
    return max(k for k in range(len(vertices)+1)
               if any(not count_edges(es, I) for I in combinations(vertices, k)))


def canonical(n, es, degrees):
    return min(code(n, {tuple(sorted((p[u], p[v]))) for u, v in es})
               for p in permutations(range(n))
               if all(degrees[i] == degrees[p[i]] for i in range(n)))


def graphs_from_shapes(n):
    # Independently organized coverage: shapes classified by edge count,
    # with complements supplying the four-, five-, and six-edge cases.
    shapes = {0: [0], 1: [0], 2: [0, 1], 3: [0, 1, 3, 7],
              4: [0, 1, 3, 12, 7, 11, 13, 15, 30, 31, 63]}[n]
    result = set()
    for mask in shapes:
        es = edges(n, mask)
        for p in permutations(range(n)):
            result.add(code(n, {tuple(sorted((p[u], p[v]))) for u, v in es}))
    require(result == set(range(1 << comb(n, 2))), "small-graph shape coverage")
    return result


def numerical_profiles():
    result = []
    checked = 0
    for n4 in range(9):
        for n5 in range(9-n4):
            for n6 in range(9-n4-n5):
                n7 = 8-n4-n5-n6
                checked += 1
                counts = [10, n4, n5, n6, n7]
                total_degree = sum(d*n for d, n in zip(range(3, 8), counts))
                if total_degree % 2:
                    continue
                moment = 846+sum(d*(3*d-37)*n for d, n in zip(range(3, 8), counts))//2
                if moment < 0:
                    continue
                a = 39-total_degree//2
                degrees = sum(([d]*counts[d-3] for d in range(5, 8)), [])
                require(len(degrees) <= 4, "at most four high-degree vertices")
                b0 = (moment-4*a)//3
                require(b0 == -2-n5-n6 < 0, "negative gamma3 at the frontier")
                result.append({"counts": counts, "R_degrees": degrees,
                               "a": a, "T_max": moment//3, "b_at_T0": b0})
    require(checked == comb(11, 3), "weak-composition coverage")
    require(len(result) == 18, "eighteen numerical profiles")
    return sorted(result, key=lambda p: p["R_degrees"])


def case_table():
    rows = []
    surviving = []
    all_labeled = after_first_filters = 0
    for p in numerical_profiles():
        ds = p["R_degrees"]
        n = len(ds)
        nq = p["counts"][1]
        representatives = []
        for mask in sorted(graphs_from_shapes(n)):
            all_labeled += 1
            es = edges(n, mask)
            adj = adjacency(n, es)
            tau = [count_edges(es, adj[v]) for v in range(n)]
            k = [p["a"]+8+d*(d-11)//2
                 +sum(ds[w]-4 for w in adj[v])-tau[v] for v, d in enumerate(ds)]
            if any(x < 0 for x in k) or sum(tau)//3 > p["T_max"]:
                continue
            after_first_filters += 1
            D = [k[v]-ds[v]+len(adj[v]) for v in range(n)]
            # Check an expanded, separately derived expression for D.
            expanded = [p["a"]+8+d*(d-13)//2
                        +sum(ds[w]-3 for w in adj[v])-tau[v]
                        for v, d in enumerate(ds)]
            require(D == expanded, "two expressions for D")
            certificates = [(D[v]+nq, [v]) for v in range(n)]
            certificates += [(D[u]+D[v]+nq, [u, v]) for u, v in sorted(es)]
            value, S = min(certificates, default=(0, []))
            if mask == canonical(n, es, ds):
                representatives.append({"mask": mask, "k": k, "D": D,
                                        "witness": S if value < 0 else None,
                                        "bound": value})
                if value >= 0:
                    surviving.append([ds, mask])
        rows.append({**p, "representatives": representatives})
    require(surviving == [[[], 0], [[5, 5], 0], [[5, 5], 1],
                          [[5, 5, 5, 5], 7], [[5, 5, 5, 5], 30], [[6], 0]],
            "complete surviving high-degree subgraphs")
    return {"rows": rows, "survivors": surviving,
            "labeled_graphs_examined": all_labeled,
            "labeled_graphs_after_first_filters": after_first_filters}


def audit_independence_bound():
    # Check the pointwise combinatorial inequality used in (3), on every
    # graph of order <=5 and every pair of subsets S,B. This is not a
    # replacement for the all-orders proof in PROOF.md.
    tested = 0
    for n in range(1, 6):
        subsets = [set(v for v in range(n) if mask >> v & 1) for mask in range(1 << n)]
        for mask in range(1 << comb(n, 2)):
            es = edges(n, mask)
            adj = adjacency(n, es)
            independence = [alpha(es, S) for S in subsets]
            for B in subsets:
                term = {v: 1-len(adj[v] & B) for v in B}
                for S, bound in zip(subsets, independence):
                    score = sum(term[v] for v in B & S)
                    require(score <= bound, "independence-number summand bound")
                    tested += 1
    return tested


def link_models():
    cycle6 = {tuple(sorted((v, (v+1) % 6))) for v in range(6)}
    first = (set(combinations(range(6), 2))-cycle6) | {(6, 7), (8, 9), (10, 11)}
    primal = {tuple(sorted((v, (v+1) % 5))) for v in range(5)}
    primal |= {(v, s) for v in range(5) for s in (5, 6)}
    adj = adjacency(7, primal)
    common = adj[0] & adj[5]
    primal.remove((0, 5))
    primal |= {(v, 7) for v in common | {0, 5}}
    second = (set(combinations(range(8), 2))-primal) | {(8, 9), (10, 11)}
    return first, second


def pair_ok(es, adj, noncubic):
    C = set(range(len(adj)))-set(noncubic)
    return all((u, v) in es or len(adj[u] & adj[v]) <= 1
               for u, v in combinations(sorted(C), 2))


def audit_links():
    result = []
    for name, es in zip(["I", "II"], link_models()):
        adj = adjacency(12, es)
        f = [sum(not count_edges(es, face) for face in combinations(range(12), k))
             for k in range(7)]
        require(f == [1, 12, 54, 116, 120, 48, 0], "explicit classified link faces")
        two = [S for S in combinations(range(12), 2) if pair_ok(es, adj, S)]
        three_independent = [S for S in combinations(range(12), 3)
                             if pair_ok(es, adj, S) and not count_edges(es, S)]
        require(not three_independent, "adjacent quintic case")
        if name == "I":
            require(not two, "nonadjacent quintic case, type I")
        else:
            require(len(two) == 4, "type II opposite-pair transversals")
            for S in two:
                require(count_edges(es, S) == 1 and all(len(adj[v]) == 3 for v in S),
                        "the two noncubic vertices occupy adjacent core positions")
                for quintic, quartic in [S, tuple(reversed(S))]:
                    neighbor_sum = sum(4 if v == quartic else 3 for v in adj[quintic])
                    neighbor_sum += 4*(5-len(adj[quintic]))
                    require(7+8+5*(5-19)//2+neighbor_sum == -2,
                            "forced negative quintic link")
        # Four-quintic C4 case: noncubic vertices have internal degree <=2.
        degree3 = [v for v in range(12) if len(adj[v]) == 3]
        obstruction = [(u, v) for u, v in combinations(degree3, 2)
                       if (u, v) not in es and len(adj[u] & adj[v]) >= 2]
        require(bool(obstruction), "all-cubic degree-three core obstruction")
        result.append({"type": name, "face_vector_with_empty": f[:-1],
                       "two_noncubic_pair_feasible": len(two),
                       "three_independent_noncubic_feasible": len(three_independent),
                       "degree_three_pair_obstructions": obstruction})
    return result


def audit_attachments():
    two_count = 0
    for cr, cs in product(range(2), repeat=2):
        for A in combinations(range(6), 4-cr):
            for B in combinations(range(6), 4-cs):
                triangles = len(set(A) & set(B))
                if cr+triangles <= 1 and cs+triangles <= 1:
                    require(cr == cs == 1 and not triangles, "two adjacent quintics")
                    two_count += 1
    four_count = 0
    cyc = [(0, 1), (1, 2), (2, 3), (0, 3)]
    for cs in product(range(2), repeat=4):
        for sets in product(*(list(combinations(range(4), 3-c)) for c in cs)):
            overlaps = {(u, v): len(set(sets[u]) & set(sets[v])) for u, v in cyc}
            if any(cs[v]+sum(t for e, t in overlaps.items() if v in e) > 1
                   for v in range(4)):
                continue
            require(cs == (1, 1, 1, 1), "four quintics each have one cubic neighbor")
            require(sets[0] == sets[2] and sets[1] == sets[3], "opposite neighborhoods")
            require(not any(overlaps.values()), "no high-vertex triangles")
            four_count += 1
    # Eleven-vertex gamma1=1 link: C5 + 3K2, obtained from suspensions.
    es = {tuple(sorted((v, (v+1) % 5))) for v in range(5)}
    es |= {(5, 6), (7, 8), (9, 10)}
    adj = adjacency(11, es)
    eligible_w = [w for w in range(11) if 1-len(adj[w]) >= 0]
    for w in eligible_w:
        attachment_sizes = [(4 if v == w else 3)-len(adj[v]) for v in range(11)]
        require(attachment_sizes.count(1) == 5 and min(attachment_sizes) >= 1,
                "six facet ridges have only five singleton completions")
    require((two_count, four_count, len(eligible_w)) == (20, 6, 6), "attachment coverage")
    return {"two_quintic_partitions": two_count, "four_quintic_partitions": four_count,
            "sextic_link_quartic_positions": len(eligible_w), "ridge_completions": 5,
            "ridge_completions_needed": 6}


def render_table(audit):
    lines = ["# Complete finite case table", "",
             "Vertices of R are labeled 0,...,r-1 in the displayed nondecreasing degree order.",
             "A mask has bit i for the i-th pair in lexicographic order: for r=4,",
             "the pairs are 01,02,03,12,13,23. Representatives minimize the mask",
             "under permutations preserving the degree labels. k and D are from (2).", "",
             "The table lists every representative with k>=0 and with the triangle",
             "count allowed by (5). A witness S is a singleton or an edge, and its",
             "displayed bound is sum(D_v:v in S)+n_4<0. A dash means it survives (4).", "",
             "For each row there are at most 64 graphs. The eleven uncolored shapes",
             "on four vertices have masks 0,1,3,12,7,11,13,15,30,31,63: edge counts",
             "0,1,2,3 supply 1,1,2,3 shapes, and complements supply counts 4,5,6.",
             "Permuting these shapes and checking degree colors gives an alternative",
             "complete enumeration; verify.py compares the full labeled sets.", "",
             "| Degrees on R | n_4 | a | T max | Mask | k | D | S | Bound |",
             "|---|---:|---:|---:|---:|---|---|---|---:|"]
    for row in audit["rows"]:
        for rep in row["representatives"]:
            val = rep["bound"] if rep["witness"] is not None else "—"
            S = rep["witness"] if rep["witness"] is not None else "—"
            lines.append(f'| {row["R_degrees"]} | {row["counts"][1]} | {row["a"]} | '
                         f'{row["T_max"]} | {rep["mask"]} | {rep["k"]} | {rep["D"]} | {S} | {val} |')
    lines += ["", "The six surviving representatives are the empty R, one sextic vertex,",
              "two quintic vertices with or without their edge, and four quintic vertices",
              "forming the star (mask 7) or the 4-cycle (mask 30). PROOF.md excludes",
              "the five representatives having nonempty R by structural arguments.", ""]
    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-table", action="store_true",
                        help="regenerate the deterministic Markdown table")
    args = parser.parse_args()
    finite = case_table()
    table = render_table(finite)
    table_path = Path(__file__).with_name("CASE_TABLE.md")
    if args.write_table:
        table_path.write_text(table)
    else:
        require(table_path.read_text() == table, "published case table matches every entry")
    out = {"status": "PASS", "finite_table": finite,
           "pointwise_independence_checks": audit_independence_bound(),
           "link_audit": audit_links(), "attachment_audit": audit_attachments(),
           "scope": "Exact finite/table checks; published topology and human bridges remain explicit."}
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
