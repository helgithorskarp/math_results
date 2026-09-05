#!/usr/bin/env python3
"""Deterministic fixture construction and bounded exact enumeration."""
import argparse
from collections import Counter
import hashlib
from itertools import combinations, combinations_with_replacement, product
import json
from pathlib import Path
import kernel as k

SEED_SHA = "9f4bd3853e985697f7fc496c0544f9d800235c2ece4a25cb718a2c3181559916"
SEED = Path(__file__).resolve().parent.parent / "ramsey_r55_k5_neutral_component/EXIT_GRAPH.json"


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()


def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def save(path, obj):
    path.write_text(json.dumps(obj, sort_keys=True, indent=2) + "\n")


def load_seed():
    raw = SEED.read_bytes()
    k.require(hashlib.sha256(raw).hexdigest() == SEED_SHA, "seed SHA256")
    adj = [int(x, 16) for x in json.loads(raw)["red_adjacency_hex"]]
    k.require(len(adj) == 43 and k.decode(k.document(adj)) == adj, "seed graph")
    return adj


def necessity(red):
    sig = [1, 1, 1, 2, 4] if red else [3, 3, 3, 5, 6]
    adj = [0] * 8
    for u, v in combinations(range(8), 2):
        color = (True if v < 3 else bool(sig[v - 3] & (1 << u))) if u < 3 else red
        if color:
            adj[u] |= 1 << v
            adj[v] |= 1 << u
    return k.document(adj)


def positive_fixture():
    residues = {i * i % 17 for i in range(1, 17)}
    original = [sum(1 << v for v in range(17) if (v - u) % 17 in residues)
                for u in range(17)]
    keep = [0, 1, 2] + [v for v in range(3, 17) if
                       sum(1 << i for i in range(3) if original[i] >> v & 1) not in (0, 7)]
    base = [sum(1 << j for j, v in enumerate(keep) if original[u] >> v & 1) for u in keep]
    # A bounded, deterministic construction: the first eligible visible central edge.
    # The selected first pair is (3,4); no 43-vertex search is performed.
    free = set(k.free_edges(base))
    for u, v in combinations(range(3, len(base)), 2):
        if (u, v) in free:
            continue
        adj = base[:]
        adj[u] ^= 1 << v
        adj[v] ^= 1 << u
        if k.preflight(adj)["passes"] and k.compile_kernel(adj)["clauses"]:
            return {"original_labels": keep, "toggled_visible_edge": [u, v],
                    "graph": k.document(adj), "target_degrees": [a.bit_count() for a in adj]}
    raise ValueError("bounded fixture construction found no example")


def signature_census():
    widths = Counter()
    gap = []
    for sig in combinations_with_replacement(range(1, 7), 5):
        width = sum(x ^ y == 7 for x, y in combinations(sig, 2))
        widths[width] += 1
        common = any(all(bool(x & (1 << i)) == color for x in sig)
                     for i in range(3) for color in (True, False))
        if width == 0 and not common:
            allowed = ["red" if red else "blue" for red in (True, False)
                       if all(sum(bool(x & (1 << i)) == red for x in sig) < 4
                              for i in range(3))]
            gap.append({"signatures": list(sig), "colors_not_forbidden_by_mixed_k5": allowed})
    return {"multisets": 252, "width_histogram": dict(sorted(widths.items())),
            "fully_visible_nonface_patterns": gap}


def completion_census(fixture, kernel):
    adj = k.decode(fixture["graph"])
    target = fixture["target_degrees"]
    q = len(kernel["variables"])
    k.require(q == 12, "bounded fixture must have exactly twelve free edges")
    accepted, degree, joint = [], [], []
    for mask in range(1 << q):
        sat = k.satisfies(kernel, mask)
        degree_ok = [x.bit_count() for x in k.complete(adj, mask)] == target
        if sat:
            accepted.append(mask)
        if degree_ok:
            degree.append(mask)
        if sat and degree_ok:
            joint.append(mask)
    return {"assignments": 1 << q, "ramsey_completions": len(accepted),
            "ramsey_assignment_sha256": digest(accepted),
            "degree_completions": degree, "joint_completions": joint,
            "first_accepted": accepted[0], "first_rejected": next(m for m in range(1 << q)
                                                                   if m not in set(accepted))}


def seed_audit(adj):
    sig = k.signatures(adj)
    ker = k.compile_kernel(adj)
    empty = [r for r in ker["clauses"] if not r["variables"]]
    outside = []
    for r in empty:
        five = r["vertices"]
        if min(five) >= 3 and not any(
                all(bool(adj[e] >> v & 1) == color for v in five)
                for e in range(3) for color in (True, False)):
            outside.append(r)
    pre = k.preflight(adj)
    return {"seed_sha256": SEED_SHA, "n": 43, "red_edges": sum(a.bit_count() for a in adj) // 2,
            "cell_sizes": [sig[3:].count(s) for s in range(8)],
            "free_edges": len(ker["variables"]), "visible_central_edges": 780 - len(ker["variables"]),
            "preflight_passes": pre["passes"],
            "root_failures": [{"root": r["root"], "color": r["color"],
                               "same_k4": len(r["same_k4"]),
                               "opposite_k5": len(r["opposite_k5"])} for r in pre["roots"]],
            "red_singleton_k5": pre["red_singleton_k5"], "blue_pair_k5": pre["blue_pair_k5"],
            "residual_occurrences": len(ker["clauses"]),
            "residual_width_histogram": dict(sorted(Counter(len(r["variables"]) for r in ker["clauses"]).items())),
            "residual_sha256": digest(ker), "immutable_k5": empty,
            "outside_all_root_neighborhoods": outside,
            "degree_interface": k.degree_interface(adj, [a.bit_count() for a in adj])}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=False)
    fixtures = {"red_singleton_necessity": necessity(True),
                "blue_pair_necessity": necessity(False), "positive": positive_fixture()}
    pos = fixtures["positive"]
    ker = k.compile_kernel(k.decode(pos["graph"]))
    flow_cases = []
    for margins in product(range(3), repeat=4):
        flow_cases.append({"left": list(margins[:2]), "right": list(margins[2:]),
                           "certificate": k.bipartite(list(margins[:2]), list(margins[2:]))})
    report = {"signature_census": signature_census(),
              "positive_preflight": k.preflight(k.decode(pos["graph"])),
              "positive_degree_interface": k.degree_interface(k.decode(pos["graph"]), pos["target_degrees"]),
              "completion_census": completion_census(pos, ker),
              "necessity_preflights": {name: k.preflight(k.decode(fixtures[name])) for name in
                                       ("red_singleton_necessity", "blue_pair_necessity")}}
    for name, doc in (("fixtures.json", fixtures), ("small_kernel.json", ker),
                      ("report.json", report), ("margin_certificates.json", flow_cases),
                      ("seed_audit.json", seed_audit(load_seed()))):
        save(args.work / name, doc)
    print(json.dumps({"status": "COMPLETE", "completion_census": report["completion_census"]}, sort_keys=True))


if __name__ == "__main__":
    main()
