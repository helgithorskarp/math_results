#!/usr/bin/env python3
"""Separate set-based reconstruction. Imports neither producer nor kernel nor solver."""
import argparse
from collections import Counter
import hashlib
from itertools import combinations, product
import json
from pathlib import Path

SEED_SHA = "9f4bd3853e985697f7fc496c0544f9d800235c2ece4a25cb718a2c3181559916"
SEED = Path(__file__).resolve().parent.parent / "ramsey_r55_k5_neutral_component/EXIT_GRAPH.json"


def check(ok, message):
    if not ok:
        raise ValueError(message)


def sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def read_graph(doc):
    check(set(doc) == {"n", "red_edges"}, "graph fields")
    n, raw = doc["n"], doc["red_edges"]
    check(type(n) is int and n >= 3 and type(raw) is list, "graph format")
    for edge in raw:
        check(type(edge) is list and len(edge) == 2 and all(type(v) is int for v in edge)
              and 0 <= edge[0] < edge[1] < n, "edge endpoints")
    red = {tuple(e) for e in raw}
    check(len(red) == len(raw) and raw == sorted(raw), "edge order / duplication")
    sig = {v: frozenset(i for i in range(3) if (i, v) in red) for v in range(3, n)}
    check(all(0 < len(s) < 3 for s in sig.values()), "proper nonempty signatures")
    return n, red, sig


def monos(n, edges, vertices, size, color):
    answer = []
    for subset in combinations(sorted(vertices), size):
        if all(((u, v) in edges) == color for u, v in combinations(subset, 2)):
            answer.append(list(subset))
    return answer


def preflight(doc):
    n, edges, sig = read_graph(doc)
    rows = []
    for root in range(3):
        for color in (True, False):
            vertices = [v for v in range(n) if v != root and
                        (tuple(sorted((root, v))) in edges) == color]
            rows.append({"root": root, "color": "red" if color else "blue",
                         "same_k4": monos(n, edges, vertices, 4, color),
                         "opposite_k5": monos(n, edges, vertices, 5, not color)})
    single = [v for v in sig if len(sig[v]) == 1]
    pair = [v for v in sig if len(sig[v]) == 2]
    extra = {"red_singleton_k5": monos(n, edges, single, 5, True),
             "blue_pair_k5": monos(n, edges, pair, 5, False)}
    return {"passes": not any(r["same_k4"] or r["opposite_k5"] for r in rows)
            and not any(extra.values()), "roots": rows, **extra}


def reconstruct(doc):
    """Enumerate permissive-color cliques using sets, not producer's five-set scan."""
    n, edges, sig = read_graph(doc)
    roots = frozenset(range(3))
    free = [e for e in combinations(range(3, n), 2)
            if sig[e[0]].isdisjoint(sig[e[1]]) and sig[e[0]] | sig[e[1]] == roots]
    positions = {e: j for j, e in enumerate(free)}
    rows = []
    for color in (True, False):
        adj = [set() for _ in range(n)]
        for u, v in combinations(range(n), 2):
            if (u, v) in positions or ((u, v) in edges) == color:
                adj[u].add(v)
                adj[v].add(u)

        def visit(prefix, candidates):
            if len(prefix) == 5:
                rows.append({"color": "red" if color else "blue", "vertices": list(prefix),
                             "variables": sorted(positions[e] for e in combinations(prefix, 2)
                                                 if e in positions)})
                return
            for v in sorted(candidates):
                visit(prefix + (v,), {w for w in candidates & adj[v] if w > v})

        visit((), set(range(n)))
    rows.sort(key=lambda r: (r["vertices"], r["color"] == "blue"))
    return {"variables": [list(e) for e in free], "clauses": rows}


def verify_kernel(doc, claimed):
    check(reconstruct(doc) == claimed, "complete residual formula mismatch")


def verify_signature(census):
    cases = {}
    truth_tables = 0
    for ordered in product(range(1, 7), repeat=5):
        sig = [frozenset(i for i in range(3) if x & (1 << i)) for x in ordered]
        free = [(u, v) for u, v in combinations(range(5), 2)
                if not any((i in sig[u]) == (i in sig[v]) for i in range(3))]
        face = any(all((i in s) == color for s in sig) for i in range(3)
                   for color in (True, False))
        colors = []
        if not free and not face:
            for color in (True, False):
                mixed = any(all((i in sig[v]) == color for v in four)
                            for i in range(3) for four in combinations(range(5), 4))
                if not mixed:
                    colors.append("red" if color else "blue")
                    check(all(len(s) == (1 if color else 2) for s in sig), "two-stratum theorem")
        key = tuple(sorted(ordered))
        item = (len(free), face, colors)
        if key in cases:
            check(cases[key] == item, "permutation consistency")
        cases[key] = item
    widths = Counter(x[0] for x in cases.values())
    gaps = [{"signatures": list(s), "colors_not_forbidden_by_mixed_k5": row[2]}
            for s, row in sorted(cases.items()) if row[0] == 0 and not row[1]]
    check(census == {"multisets": len(cases),
                     "width_histogram": {str(w): c for w, c in sorted(widths.items())},
                     "fully_visible_nonface_patterns": gaps}, "signature census")
    # Literal truth tables of each possible nonempty residual clause width, both colors.
    for width in widths:
        for color in (True, False):
            for values in product((False, True), repeat=width):
                mono = all(v == color for v in values)
                clause = any(v != color for v in values)
                check(clause == (not mono), "residual truth table")
                truth_tables += 1
    check(set(widths) == {0, 1, 2, 3, 4, 6}, "residual width support")
    return {"ordered_patterns": 6 ** 5, "multisets": len(cases),
            "residual_truth_tables": truth_tables}


def verify_margin(left, right, cert):
    a, b = len(left), len(right)
    if any(v < 0 or v > b for v in left) or any(v < 0 or v > a for v in right):
        check(cert == {"feasible": False, "reason": "out_of_range"}, "margin bounds")
        return
    if sum(left) != sum(right):
        check(cert == {"feasible": False, "reason": "total_mismatch"}, "margin totals")
        return
    edges = [tuple(e) for e in cert["edges"]]
    check(len(set(edges)) == len(edges) and all(0 <= i < a and 0 <= j < b for i, j in edges),
          "margin witness edges")
    ld = [sum(i == u for i, j in edges) for u in range(a)]
    rd = [sum(j == v for i, j in edges) for v in range(b)]
    check(all(x <= y for x, y in zip(ld, left)) and all(x <= y for x, y in zip(rd, right)),
          "partial flow capacity")
    sink = a + b + 1
    raw = cert["reachable"]
    reached = set(raw)
    check(raw == sorted(reached) and 0 in reached and sink not in reached and
          all(type(v) is int and 0 <= v <= sink for v in reached), "cut partition")
    cut = sum(x for i, x in enumerate(left) if i + 1 not in reached)
    cut += sum(1 for i in range(a) for j in range(b)
               if i + 1 in reached and a + 1 + j not in reached)
    cut += sum(x for j, x in enumerate(right) if a + 1 + j in reached)
    check(len(edges) == cert["flow"] == cert["cut_capacity"] == cut, "flow / cut equality")
    check(cert["required"] == sum(left), "required flow")
    check(cert["feasible"] == (ld == left and rd == right), "margin feasibility")
    if not cert["feasible"]:
        check(cut < sum(left), "strict infeasibility cut")


def verify_interface(doc, target, interface):
    n, red, sig = read_graph(doc)
    free = {tuple(e) for e in reconstruct(doc)["variables"]}
    fixed = red - free
    fixed_degrees = [sum(v in e for e in fixed) for v in range(n)]
    check(all(target[e] == fixed_degrees[e] for e in range(3)), "root degree interface")
    margins = [target[v] - fixed_degrees[v] for v in range(n)]
    check(interface["margins"] == margins, "residual degree margins")
    check(len(interface["blocks"]) == 3, "degree block count")
    for mask, block in zip((1, 2, 3), interface["blocks"]):
        s = frozenset(i for i in range(3) if mask & (1 << i))
        left = [v for v in sig if sig[v] == s]
        right = [v for v in sig if sig[v] == frozenset(range(3)) - s]
        lm, rm = [margins[v] for v in left], [margins[v] for v in right]
        check((block["left"], block["right"], block["left_margins"], block["right_margins"])
              == (left, right, lm, rm), "degree block reconstruction")
        verify_margin(lm, rm, block["certificate"])
    check(interface["degree_feasible"] == all(b["certificate"]["feasible"] for b in interface["blocks"]),
          "degree interface status")


def full_completions(fixture, ker, expected):
    n, red, _ = read_graph(fixture["graph"])
    free = [tuple(e) for e in ker["variables"]]
    fixed = red - set(free)
    check(len(free) == 12 and n == 15, "bounded enumeration contract")
    all_fives = [tuple(combinations(five, 2)) for five in combinations(range(n), 5)]
    accepted, degree, joint = [], [], []
    for assignment in range(4096):
        graph = fixed | {e for j, e in enumerate(free) if assignment & (1 << j)}
        # Every literal five-set is visited until an actual obstruction is found.
        sat = not any(all(e in graph for e in pairs) or all(e not in graph for e in pairs)
                      for pairs in all_fives)
        formula_sat = all(any(bool(assignment & (1 << j)) != (r["color"] == "red")
                              for j in r["variables"]) for r in ker["clauses"])
        check(sat == formula_sat, "completion-to-graph equivalence")
        d = [sum(v in e for e in graph) for v in range(n)]
        degree_ok = d == fixture["target_degrees"]
        # Independently compare original degree checks with the three margin equations.
        fixed_d = [sum(v in e for e in fixed) for v in range(n)]
        free_d = [sum(v in e for e in graph - fixed) for v in range(n)]
        margin_ok = all(free_d[v] == fixture["target_degrees"][v] - fixed_d[v] for v in range(n))
        check(degree_ok == margin_ok, "degree factor interface")
        if sat:
            accepted.append(assignment)
        if degree_ok:
            degree.append(assignment)
        if sat and degree_ok:
            joint.append(assignment)
    result = {"assignments": 4096, "ramsey_completions": len(accepted),
              "ramsey_assignment_sha256": sha(accepted), "degree_completions": degree,
              "joint_completions": joint, "first_accepted": accepted[0],
              "first_rejected": next(m for m in range(4096) if m not in set(accepted))}
    check(result == expected, "completion census / assignment entries")
    return result


def seed_audit(claimed):
    raw = SEED.read_bytes()
    check(hashlib.sha256(raw).hexdigest() == SEED_SHA, "seed SHA256")
    words = [int(x, 16) for x in json.loads(raw)["red_adjacency_hex"]]
    check(len(words) == 43 and all(0 <= x < 1 << 43 and not (x >> v & 1)
                                 for v, x in enumerate(words)), "seed bit bounds")
    check(all(bool(words[u] >> v & 1) == bool(words[v] >> u & 1)
              for u, v in combinations(range(43), 2)), "seed symmetry")
    doc = {"n": 43, "red_edges": [[u, v] for u, v in combinations(range(43), 2) if words[u] >> v & 1]}
    _, edges, sig = read_graph(doc)
    ker = reconstruct(doc)
    empty = [r for r in ker["clauses"] if not r["variables"]]
    outside = [r for r in empty if min(r["vertices"]) >= 3 and
               not any(all((i in sig[v]) == color for v in r["vertices"])
                       for i in range(3) for color in (True, False))]
    p = preflight(doc)
    expected = {"seed_sha256": SEED_SHA, "n": 43, "red_edges": len(edges),
                "cell_sizes": [sum(sum(1 << i for i in s) == mask for s in sig.values()) for mask in range(8)],
                "free_edges": len(ker["variables"]), "visible_central_edges": 780 - len(ker["variables"]),
                "preflight_passes": p["passes"],
                "root_failures": [{"root": r["root"], "color": r["color"],
                                   "same_k4": len(r["same_k4"]), "opposite_k5": len(r["opposite_k5"])} for r in p["roots"]],
                "red_singleton_k5": p["red_singleton_k5"], "blue_pair_k5": p["blue_pair_k5"],
                "residual_occurrences": len(ker["clauses"]),
                "residual_width_histogram": {str(w): c for w, c in sorted(Counter(len(r["variables"]) for r in ker["clauses"]).items())},
                "residual_sha256": sha(ker), "immutable_k5": empty,
                "outside_all_root_neighborhoods": outside,
                "degree_interface": claimed["degree_interface"]}
    check(claimed == expected, "full seed audit reconstruction")
    verify_interface(doc, [w.bit_count() for w in words], claimed["degree_interface"])
    for r in outside:
        check(all(len(sig[v]) == (1 if r["color"] == "red" else 2) for v in r["vertices"]),
              "seed two-stratum classification")
    return {"full_residual_occurrences": len(ker["clauses"]), "immutable": len(empty),
            "outside_neighborhoods": dict(Counter(r["color"] for r in outside)),
            "residual_sha256": sha(ker)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    docs = {name: json.loads((args.source / (name + ".json")).read_text()) for name in
            ("fixtures", "small_kernel", "report", "margin_certificates", "seed_audit")}
    fixtures, report = docs["fixtures"], docs["report"]
    for name, color in (("red_singleton_necessity", True), ("blue_pair_necessity", False)):
        doc = fixtures[name]
        n, red, sig = read_graph(doc)
        check(n == 8 and list(map(len, sig.values())) == [1 if color else 2] * 5, "necessity fixture")
        p = preflight(doc)
        check(p == report["necessity_preflights"][name], "necessity preflight entries")
        check(not any(r["same_k4"] or r["opposite_k5"] for r in p["roots"]), "necessity six neighborhoods")
        check(monos(n, red, range(n), 5, color) == [[3, 4, 5, 6, 7]] and
              not monos(n, red, range(n), 5, not color), "unique necessity obstruction")
        check(p["red_singleton_k5"] == ([[3, 4, 5, 6, 7]] if color else []) and
              p["blue_pair_k5"] == ([] if color else [[3, 4, 5, 6, 7]]), "necessity two checks")
    pos = fixtures["positive"]
    q = {x * x % 17 for x in range(1, 17)}
    edges = {(u, v) for u, v in combinations(range(17), 2) if (v - u) % 17 in q}
    check(not monos(17, edges, range(17), 4, True) and not monos(17, edges, range(17), 4, False),
          "literal Paley17 K4 check, no imported theorem")
    keep = [0, 1, 2] + [v for v in range(3, 17) if 0 < sum((i, v) in edges for i in range(3)) < 3]
    check(pos["original_labels"] == keep and pos["toggled_visible_edge"] == [3, 4], "fixture provenance")
    mapped = {(i, j) for i, j in combinations(range(len(keep)), 2) if (keep[i], keep[j]) in edges}
    mapped.symmetric_difference_update({(3, 4)})
    check(pos["graph"] == {"n": 15, "red_edges": [list(e) for e in sorted(mapped)]}, "fixture edges")
    check(pos["target_degrees"] == [sum(v in e for e in mapped) for v in range(15)], "fixture degrees")
    check(preflight(pos["graph"]) == report["positive_preflight"] and report["positive_preflight"]["passes"],
          "positive preflight")
    verify_kernel(pos["graph"], docs["small_kernel"])
    verify_interface(pos["graph"], pos["target_degrees"], report["positive_degree_interface"])
    check(len(docs["margin_certificates"]) == 81, "complete 2x2 margin domain")
    for margins, row in zip(product(range(3), repeat=4), docs["margin_certificates"]):
        check(row["left"] + row["right"] == list(margins), "margin enumeration order")
        verify_margin(row["left"], row["right"], row["certificate"])
        feasible = any([sum(mask >> (2 * i + j) & 1 for j in range(2)) for i in range(2)] == row["left"]
                       and [sum(mask >> (2 * i + j) & 1 for i in range(2)) for j in range(2)] == row["right"]
                       for mask in range(16))
        check(feasible == row["certificate"]["feasible"], "all 16 literal bipartite graphs")
    result = {"status": "VERIFIED", "signature_checks": verify_signature(report["signature_census"]),
              "margin_cases": 81, "necessity_fixtures": 2,
              "completion_census": full_completions(pos, docs["small_kernel"], report["completion_census"]),
              "seed": seed_audit(docs["seed_audit"])}
    args.report.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
