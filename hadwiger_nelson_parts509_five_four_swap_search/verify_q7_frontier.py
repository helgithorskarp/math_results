#!/usr/bin/env python3
"""Solver-free audit of the open q=7 construction frontier."""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from certlib import sha256, unpack_colours

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
PAIR = PARENT / "hadwiger_nelson_parts509_pair_closure"
BUDGET = PARENT / "hadwiger_nelson_parts509_s_replacement_budget"
INTERFACE = PARENT / "hadwiger_nelson_parts509_interface_lemma"

EXPECTED_HASHES = {
    HERE / "certificate.json":
        "a9e6cdc91bcd91b9db6679bab7a516edb67eaae1a688a5d80e4dbb4b0d778feb",
    PAIR / "ambient_w3_edges.json":
        "960d32618cf5afd013f29b3f6e2e85cb6a35e7d6b8884a6680a657f8e6c46f92",
    BUDGET / "pool_S.json":
        "fd636275fccdd84266655ba9ada22412f7d2aef66a0ad66f6ee5bd738570939e",
    INTERFACE / "interface_L.json":
        "a160340461815e57c46936fb7d0001b74881fe753d904a5ddc7fb866cfc29637",
}


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def mask(vertices, index):
    result = 0
    for vertex in vertices:
        result |= 1 << index[vertex]
    return result


def verify(path: Path) -> dict:
    for source, expected in EXPECTED_HASHES.items():
        need(sha256(source) == expected, f"source hash changed: {source.name}")
    base = json.loads((HERE / "certificate.json").read_text())
    data = json.loads(path.read_text())
    need(data["schema"] == "parts509-q7-frontier-v1", "schema")
    need(data["base_certificate_sha256"] == EXPECTED_HASHES[HERE / "certificate.json"],
         "base certificate link")
    pool = base["pool"]
    q5 = set(base["Q5"])
    pool_set = set(pool)
    s = set(range(374, 509))
    need(len(pool) == 303 and len(q5) == 168 and s <= pool_set,
         "pool partition")

    interface = json.loads((INTERFACE / "interface_L.json").read_text())
    l_words = [row["witness_colouring_L"] for row in interface["classes"]]
    ambient = json.loads((PAIR / "ambient_w3_edges.json").read_text())
    l_edges, cross_edges, pool_edges = [], [], []
    for a, b in ambient["edges"]:
        if a < 374 and b < 374:
            l_edges.append((a, b))
        elif a in pool_set and b in pool_set:
            pool_edges.append((a, b))
        elif a < 374 and b in pool_set:
            cross_edges.append((a, b))
        elif b < 374 and a in pool_set:
            cross_edges.append((b, a))
    need(len(l_words) == 20 and all(len(word) == 374 for word in l_words),
         "interface witness shape")
    for word in l_words:
        need(all(word[a] != word[b] for a, b in l_edges),
             "improper fixed-L witness")

    rows = data["frontier_killing_sets"]
    need(len(rows) == 50, "frontier row count")
    keys = set()
    provenance = {}
    witness_edge_checks = 0
    for row in rows:
        d = tuple(row["D"])
        need(d == tuple(sorted(set(d))) and set(d) <= pool_set and d,
             "invalid deletion set")
        need(d not in keys, "duplicate deletion set")
        keys.add(d)
        p = row["class_index"]
        need(type(p) is int and 0 <= p < 20, "interface class")
        selected = [v for v in pool if v not in set(d)]
        word = unpack_colours(row["colouring_U_minus_D_2bit"], len(selected))
        colours = dict(zip(selected, word))
        for a, b in pool_edges:
            if a in colours and b in colours:
                witness_edge_checks += 1
                need(colours[a] != colours[b], "monochromatic pool edge")
        for l, u in cross_edges:
            if u in colours:
                witness_edge_checks += 1
                need(l_words[p][l] != colours[u], "monochromatic cross edge")
        source = row["provenance"]
        provenance[source] = provenance.get(source, 0) + 1
    need(provenance == data["frontier_provenance_counts"],
         "provenance counts")

    candidate = data["candidate"]
    deleted_s = set(candidate["S_deleted"])
    added_q5 = set(candidate["Q5_added"])
    selected_set = (s - deleted_s) | added_q5
    need(len(deleted_s) == 8 and deleted_s <= s, "eight S deletions")
    need(len(added_q5) == 7 and added_q5 <= q5, "seven Q5 additions")
    need(len(selected_set) == 134, "candidate pool order")
    vertices = set(range(374)) | selected_set
    need(len(vertices) == 508, "candidate total order")

    candidate_edge_checks = 0
    candidate_patterns = []
    for entry in candidate["verified_compatible_colourings"]:
        p = entry["class_index"]
        word = unpack_colours(entry["colouring_selected_pool_2bit"], 134)
        colours = {v: l_words[p][v] for v in range(374)}
        colours.update(zip(sorted(selected_set), word))
        need(set(colours) == vertices, "candidate colour domain")
        for a, b in ambient["edges"]:
            if a in vertices and b in vertices:
                candidate_edge_checks += 1
                need(colours[a] != colours[b], "candidate colouring failed")
        candidate_patterns.append(p)
    need(candidate_patterns == [2, 3, 11, 12, 13],
         "candidate compatible-witness classes")

    base_cuts = [row["D"] for row in base["killing_sets"]]
    prior_cuts = [row["D"] for row in rows[:45]]
    new_cuts = [row["D"] for row in rows[45:]]
    need(all(selected_set & set(d) for d in base_cuts + prior_cuts),
         "candidate does not hit its input frontier")
    need(all(not (selected_set & set(d)) for d in new_cuts),
         "new cuts are not disjoint from candidate")

    index = {v: i for i, v in enumerate(pool)}
    selected_mask = mask(selected_set, index)
    all_cut_masks = [mask(d, index) for d in new_cuts + base_cuts + prior_cuts]
    s_in, s_out = sorted(s & selected_set), sorted(s - selected_set)
    q_in, q_out = sorted(q5 & selected_set), sorted(q5 - selected_set)

    def feasible(value):
        return all(value & cut for cut in all_cut_masks)

    local_counts = {}
    for rs, rq in ((1, 0), (0, 1), (2, 0), (1, 1), (0, 2)):
        tested = feasible_count = 0
        for add_s in itertools.combinations(s_out, rs):
            with_s_add = selected_mask | mask(add_s, index)
            for drop_s in itertools.combinations(s_in, rs):
                after_s = with_s_add & ~mask(drop_s, index)
                for add_q in itertools.combinations(q_out, rq):
                    with_q_add = after_s | mask(add_q, index)
                    for drop_q in itertools.combinations(q_in, rq):
                        value = with_q_add & ~mask(drop_q, index)
                        tested += 1
                        feasible_count += bool(feasible(value))
        local_counts[f"S{rs}_Q{rq}"] = {
            "tested": tested, "cut_feasible": feasible_count}
    expected_local = {
        "S1_Q0": {"tested": 1016, "cut_feasible": 0},
        "S0_Q1": {"tested": 1127, "cut_feasible": 0},
        "S2_Q0": {"tested": 224028, "cut_feasible": 0},
        "S1_Q1": {"tested": 1145032, "cut_feasible": 0},
        "S0_Q2": {"tested": 270480, "cut_feasible": 0},
    }
    need(local_counts == expected_local, "local exchange audit changed")

    return {
        "status": "VERIFIED_OPEN_Q7_FRONTIER",
        "candidate_vertices": len(vertices),
        "candidate_q5_points": len(added_q5),
        "proper_candidate_colourings": len(candidate_patterns),
        "candidate_colouring_edge_checks": candidate_edge_checks,
        "frontier_killing_sets": len(rows),
        "frontier_witness_edge_checks": witness_edge_checks,
        "input_cuts_hit": len(base_cuts) + len(prior_cuts),
        "new_disjoint_cuts": len(new_cuts),
        "balanced_exchange_selectors_tested":
            sum(row["tested"] for row in local_counts.values()),
        "balanced_exchange_cut_feasible": 0,
        "scope": data["scope"],
        "conclusion": "colourable selector; q=7 remains open",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path,
                        default=HERE / "q7_frontier_certificate.json")
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.certificate), indent=2, sort_keys=True))
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"verification failed: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
