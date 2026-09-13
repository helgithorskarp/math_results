#!/usr/bin/env python3
"""Solver-free witness audit and optional DRAT check for the pool reduction."""
from __future__ import annotations

import argparse
import itertools
import json
import subprocess
from pathlib import Path

from certlib import CNF, selector_exact_q_cnf, sha256, unpack_colours

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
PAIR = PARENT / "hadwiger_nelson_parts509_pair_closure"
BUDGET = PARENT / "hadwiger_nelson_parts509_s_replacement_budget"
INTERFACE = PARENT / "hadwiger_nelson_parts509_interface_lemma"

EXPECTED_HASHES = {
    PAIR / "ambient_w3_edges.json":
        "960d32618cf5afd013f29b3f6e2e85cb6a35e7d6b8884a6680a657f8e6c46f92",
    BUDGET / "pool_S.json":
        "fd636275fccdd84266655ba9ada22412f7d2aef66a0ad66f6ee5bd738570939e",
    INTERFACE / "interface_L.json":
        "a160340461815e57c46936fb7d0001b74881fe753d904a5ddc7fb866cfc29637",
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def dpll(clauses, assignment):
    clauses = [list(c) for c in clauses]
    assignment = dict(assignment)
    while True:
        changed = False
        for clause in clauses:
            live = [x for x in clause if abs(x) not in assignment]
            if any(assignment.get(abs(x)) == (x > 0) for x in clause):
                continue
            if not live:
                return False
            if len(live) == 1:
                literal = live[0]
                value = literal > 0
                old = assignment.get(abs(literal))
                if old is not None and old != value:
                    return False
                if old is None:
                    assignment[abs(literal)] = value
                    changed = True
        if not changed:
            break
    if all(any(assignment.get(abs(x)) == (x > 0) for x in clause)
           for clause in clauses):
        return True
    variable = next(abs(x) for clause in clauses for x in clause
                    if abs(x) not in assignment)
    return (dpll(clauses, assignment | {variable: False}) or
            dpll(clauses, assignment | {variable: True}))


def counter_controls():
    checked = 0
    for n in range(1, 6):
        for target in range(n + 1):
            exact = CNF(n)
            exact.count_exact(list(range(1, n + 1)), target)
            atmost = CNF(n)
            atmost.at_most(list(range(1, n + 1)), target)
            for bits in itertools.product((False, True), repeat=n):
                assignment = {i + 1: bits[i] for i in range(n)}
                need(dpll(exact.clauses, assignment) == (sum(bits) == target),
                     "binary exact-counter control failed")
                need(dpll(atmost.clauses, assignment) == (sum(bits) <= target),
                     "sequential at-most control failed")
                checked += 2
    return checked


def verify(certificate_path):
    for path, expected in EXPECTED_HASHES.items():
        need(sha256(path) == expected, f"source hash changed: {path.name}")
    certificate = json.loads(certificate_path.read_text())
    pool_data = json.loads((BUDGET / "pool_S.json").read_text())
    pool = sorted(pool_data["W_S"])
    q5 = sorted(pool_data["Q5"])
    need(certificate["pool"] == pool and certificate["Q5"] == q5,
         "pool data mismatch")
    need(certificate["S"] == list(range(374, 509)), "S labels changed")
    need(len(pool) == 303 and len(q5) == 168, "pool cardinality changed")
    need(set(q5) <= set(pool), "Q5 outside pool")

    interface = json.loads((INTERFACE / "interface_L.json").read_text())
    l_words = [row["witness_colouring_L"] for row in interface["classes"]]
    need(len(l_words) == 20 and all(len(w) == 374 for w in l_words),
         "interface witness shape")
    ambient = json.loads((PAIR / "ambient_w3_edges.json").read_text())
    pool_set = set(pool)
    l_set = set(range(374))
    l_edges, cross_edges, pool_edges = [], [], []
    for a, b in ambient["edges"]:
        if a in l_set and b in l_set:
            l_edges.append((a, b))
        elif a in pool_set and b in pool_set:
            pool_edges.append((a, b))
        elif a in l_set and b in pool_set:
            cross_edges.append((a, b))
        elif b in l_set and a in pool_set:
            cross_edges.append((b, a))
    for word in l_words:
        need(all(word[a] != word[b] for a, b in l_edges),
             "improper L interface witness")

    rows = certificate["killing_sets"]
    keys = set()
    edge_checks = 0
    provenance = {}
    for row in rows:
        d = tuple(row["D"])
        need(d == tuple(sorted(set(d))) and set(d) <= pool_set and d,
             "invalid killing set")
        need(d not in keys, "duplicate killing set")
        keys.add(d)
        p = row["class_index"]
        need(type(p) is int and 0 <= p < 20, "bad class index")
        selected = [v for v in pool if v not in set(d)]
        word = unpack_colours(row["colouring_U_minus_D_2bit"],
                              len(selected))
        colours = dict(zip(selected, word))
        l_word = l_words[p]
        for a, b in pool_edges:
            if a in colours and b in colours:
                edge_checks += 1
                need(colours[a] != colours[b], "pool edge is monochromatic")
        for l, u in cross_edges:
            if u in colours:
                edge_checks += 1
                need(l_word[l] != colours[u], "cross edge is monochromatic")
        source = row["provenance"]
        provenance[source] = provenance.get(source, 0) + 1
    need(provenance == certificate["killing_set_provenance_counts"],
         "provenance counts changed")

    selector_summaries = {}
    proof_manifest = json.loads((HERE / "proof_manifest.json").read_text())
    for q_count in certificate["closed_q5_counts"]:
        path = HERE / f"selector_q{q_count}.cnf"
        rebuilt = selector_exact_q_cnf(
            pool, q5, [row["D"] for row in rows], q_count,
            certificate["target_pool_order"]).dimacs()
        need(path.read_bytes() == rebuilt,
             f"q={q_count} selector CNF did not rebuild")
        selector = certificate["selectors"][str(q_count)]
        header = rebuilt.splitlines()[0].decode().split()
        need(selector["variables"] == int(header[2]) and
             selector["clauses"] == int(header[3]),
             f"q={q_count} selector dimensions changed")
        need(selector["sha256"] == sha256(path),
             f"q={q_count} selector hash changed")
        proof = proof_manifest["proofs"][str(q_count)]
        need(proof["cnf_sha256"] == selector["sha256"] and
             proof["drat_trim_status"] == "s VERIFIED" and
             proof["proof_bytes"] > 0 and len(proof["proof_sha256"]) == 64,
             f"q={q_count} proof manifest changed")
        selector_summaries[str(q_count)] = {
            "variables": selector["variables"],
            "clauses": selector["clauses"],
            "sha256": selector["sha256"],
            "proof_bytes": proof["proof_bytes"],
            "proof_sha256": proof["proof_sha256"],
        }
    controls = counter_controls()
    result = {
        "status": "VERIFIED_PARTS_POOL_Q5_AT_LEAST_SEVEN_REDUCTION",
        "pool_vertices": len(pool),
        "fixed_L_vertices": 374,
        "target_total_vertices": 508,
        "killing_sets": len(rows),
        "killing_witness_edge_checks": edge_checks,
        "selectors": selector_summaries,
        "counter_truth_table_checks": controls,
        "q5_points_required": 7,
        "scope": "fixed Parts L and the sealed S-union-Q5 level-1 pool",
    }
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    need(result == expected, "verification summary differs from EXPECTED.json")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path,
                        default=HERE / "certificate.json")
    parser.add_argument("--skip-expected", action="store_true")
    parser.add_argument("--drat-dir", type=Path)
    parser.add_argument("--drat-trim", type=Path)
    args = parser.parse_args()
    result = verify(args.certificate)
    if not args.skip_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        need(result == expected, "verification receipt differs from EXPECTED.json")
    if args.drat_dir or args.drat_trim:
        need(args.drat_dir and args.drat_trim,
             "both DRAT-directory arguments are required")
        checked = []
        for q_count in (4, 5, 6):
            cnf = HERE / f"selector_q{q_count}.cnf"
            drat = args.drat_dir / f"selector_q{q_count}.drat"
            proc = subprocess.run([str(args.drat_trim), str(cnf), str(drat)],
                                  text=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)
            need(proc.returncode == 0 and "s VERIFIED" in proc.stdout,
                 f"q={q_count} drat-trim did not verify")
            checked.append(q_count)
        result["drat_verified_q5_counts"] = checked
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"verification failed: {error}")
        raise SystemExit(1)
