#!/usr/bin/env python3
"""Certificate and external-DRAT checks for the good43 edge window 392..511."""

import argparse
import collections
import hashlib
import itertools
import json
import subprocess
import tempfile
from pathlib import Path

import networkx as nx

import closure_t5_127
import ct_t5_open
import sat_endpoint_t5


ROOT = Path(__file__).resolve().parent
CATALOG_SHA256 = "83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0"


def load(name):
    return json.loads((ROOT / name).read_text())


def check_global_join():
    rows = []
    for z in range(1, 9):
        minimum_square_sum = None
        for cuts in itertools.combinations(range(1, 8), z - 1):
            endpoints = (0,) + cuts + (8,)
            parts = tuple(endpoints[i + 1] - endpoints[i]
                          for i in range(z))
            square_sum = sum(value * value for value in parts)
            if minimum_square_sum is None or square_sum < minimum_square_sum:
                minimum_square_sum = square_sum
        lower = 8 * (19 - z) + minimum_square_sum
        upper_if_four = 2 * (43 - z) + 24
        rows.append({"z": z, "minimum_square_sum": minimum_square_sum,
                     "lower_S": lower, "upper_if_h_at_most_4": upper_if_four,
                     "gap": lower - upper_if_four})
    if min(row["gap"] for row in rows) != 2:
        raise ValueError("global incidence gap")
    return rows


def check_physical_records(catalog_rows, physical):
    graph_cache = {}
    for item in physical["survivors"]:
        for key in ("left_catalog_index", "right_catalog_index"):
            index = item[key]
            if index not in graph_cache:
                graph_cache[index] = nx.from_graph6_bytes(catalog_rows[index])
        left = graph_cache[item["left_catalog_index"]]
        right = graph_cache[item["right_catalog_index"]]
        if left.number_of_edges() < 127 or right.number_of_edges() < 127:
            raise ValueError("nondense residual")
        common = tuple(item["left_common"])
        images = tuple(item["right_common_images"])
        if set(common) != set(left.neighbors(item["left_root"])):
            raise ValueError("left root/common")
        if set(images) != set(right.neighbors(item["right_root"])):
            raise ValueError("right root/common")
        mapping = dict(zip(common, images))
        for a, b in itertools.combinations(common, 2):
            if left.has_edge(a, b) != right.has_edge(mapping[a], mapping[b]):
                raise ValueError("nonisomorphic recorded common graph")
        common_graph = left.subgraph(common)
        internal = tuple(common_graph.degree(vertex) for vertex in common)
        base = tuple(24 - left.degree(vertex) - right.degree(mapping[vertex])
                     + common_graph.degree(vertex) for vertex in common)
        if list(base) != item["base"]:
            raise ValueError("base mismatch")
        delta = tuple(item["delta_witness"])
        if sum(delta) > 5:
            raise ValueError("deficit total")
        t_size = len(common) - 5
        if any(not 0 <= base[i] - delta[i] <= t_size
               for i in range(len(common))):
            raise ValueError("C-to-T capacity")
        position = {vertex: index for index, vertex in enumerate(common)}
        for a, b in common_graph.edges():
            cap = (13 - len(set(left[a]) & set(left[b]))
                   - len(set(right[mapping[a]]) & set(right[mapping[b]])))
            i, j = position[a], position[b]
            minimum_intersection = max(
                0, base[i] - delta[i] + base[j] - delta[j] - t_size)
            if minimum_intersection > cap:
                raise ValueError("edge intersection cap")
    return graph_cache


def check_closure(catalog_rows, physical, closure, graph_cache):
    if closure["tested_residuals"] != len(physical["survivors"]):
        raise ValueError("closure join")
    statuses = collections.Counter()
    for index, expected in enumerate(closure["results"]):
        if expected["residual_index"] != index:
            raise ValueError("closure index")
        item = physical["survivors"][index]
        for key in ("left_catalog_index", "right_catalog_index"):
            graph_index = item[key]
            if graph_index not in graph_cache:
                graph_cache[graph_index] = nx.from_graph6_bytes(
                    catalog_rows[graph_index])
        fixed, active_order = closure_t5_127.fixed_gluing(item, graph_cache)
        actual = closure_t5_127.close(fixed, active_order)
        actual = json.loads(json.dumps(actual))
        for key in ("status", "forced_edges", "conflict", "trace"):
            if actual.get(key) != expected.get(key):
                raise ValueError(f"closure mismatch {index} {key}")
        statuses[actual["status"]] += 1
    if statuses != {"CONTRADICTION": 298, "OPEN": 32}:
        raise ValueError("closure status totals")
    return [index for index, result in enumerate(closure["results"])
            if result["status"] == "OPEN"]


def check_ct(physical, ct, open_indices, graph_cache):
    if [item["residual_index"] for item in ct["results"]] != open_indices:
        raise ValueError("CT/open join")
    branch_keys = []
    for result in ct["results"]:
        index = result["residual_index"]
        item = physical["survivors"][index]
        base, caps, deltas_raw = ct_t5_open.constraints(item, graph_cache)
        deltas = {tuple(map(int, row)) for row in deltas_raw}
        witnesses = result["ct_witnesses"]
        if {tuple(entry["delta"]) for entry in witnesses} != deltas:
            raise ValueError("incomplete delta join")
        for delta_index, entry in enumerate(witnesses):
            delta = tuple(entry["delta"])
            masks = tuple(entry["row_masks"])
            row_degrees = tuple(base[i] - delta[i] for i in range(len(base)))
            if any(mask.bit_count() != row_degrees[i]
                   for i, mask in enumerate(masks)):
                raise ValueError("CT row degree")
            for (i, j), cap in caps.items():
                if (masks[i] & masks[j]).bit_count() > cap:
                    raise ValueError("CT witness cap")
            branch_keys.append((index, delta_index))
    if len(branch_keys) != 52:
        raise ValueError("endpoint branch count")
    return branch_keys


def check_branch_proofs(catalog, physical_path, ct_path, branch_keys,
                        proofs, drat_trim):
    actual_keys = [(record["metadata"]["residual_index"],
                    record["metadata"]["delta_index"])
                   for record in proofs["records"]]
    if actual_keys != branch_keys:
        raise ValueError("proof branch join")
    core_histogram = collections.Counter()
    with tempfile.TemporaryDirectory(prefix="r55-edge-window-verify-") as raw_tmp:
        tmp = Path(raw_tmp)
        for branch_index, (key, record) in enumerate(zip(branch_keys,
                                                          proofs["records"])):
            clauses, metadata = sat_endpoint_t5.build(
                catalog, physical_path, ct_path, key[0], key[1])
            metadata = json.loads(json.dumps(metadata))
            if metadata != record["metadata"] or record["status"] != "UNSAT_VERIFIED":
                raise ValueError("endpoint metadata")
            clause_set = {tuple(sorted(clause)) for clause in clauses}
            core_clauses = record["core_clauses"]
            if any(tuple(sorted(clause)) not in clause_set
                   for clause in core_clauses):
                raise ValueError("core not contained in endpoint formula")
            core = tmp / "core.cnf"
            proof = tmp / "proof.drat"
            with core.open("w") as stream:
                stream.write(f"p cnf {record['core_variables']} {len(core_clauses)}\n")
                for clause in core_clauses:
                    stream.write(" ".join(map(str, clause)) + " 0\n")
            proof.write_text("\n".join(record["trimmed_drat"]) + "\n")
            checked = subprocess.run([drat_trim, str(core), str(proof)],
                                     capture_output=True, text=True, timeout=60)
            if checked.returncode != 0 or "s VERIFIED" not in checked.stdout + checked.stderr:
                raise ValueError(f"DRAT branch {branch_index}")
            core_histogram[len(core_clauses)] += 1
    return dict(sorted(core_histogram.items()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--drat-trim", required=True)
    args = parser.parse_args()
    raw = args.catalog.read_bytes()
    if hashlib.sha256(raw).hexdigest() != CATALOG_SHA256:
        raise ValueError("catalog SHA256")
    catalog_rows = raw.splitlines()
    if len(catalog_rows) != 352366:
        raise ValueError("catalog count")
    coarse = load("COARSE.json")
    physical = load("PHYSICAL.json")
    closure = load("CLOSURE.json")
    ct = load("CT.json")
    proofs = load("BRANCH_PROOFS.json")
    if (coarse["status"] != "COMPLETE_COARSE_SCAN" or
            coarse["retained_graphs"] != 4428 or
            coarse["stats"]["surviving_profile_pairs"] != 201):
        raise ValueError("coarse certificate")
    if (physical["status"] != "COMPLETE_PHYSICAL_BUDGET_CLASSIFICATION" or
            len(physical["survivors"]) != 330):
        raise ValueError("physical certificate")
    global_rows = check_global_join()
    graph_cache = check_physical_records(catalog_rows, physical)
    open_indices = check_closure(catalog_rows, physical, closure, graph_cache)
    branch_keys = check_ct(physical, ct, open_indices, graph_cache)
    core_histogram = check_branch_proofs(
        str(args.catalog), str(ROOT / "PHYSICAL.json"), str(ROOT / "CT.json"),
        branch_keys, proofs, args.drat_trim)
    output = {
        "status": "VERIFIED_EDGE_WINDOW_392_511",
        "catalog_records": len(catalog_rows),
        "dense_graphs": coarse["retained_graphs"],
        "coarse_profile_pairs": coarse["stats"]["profile_pairs"],
        "coarse_survivors": coarse["stats"]["surviving_profile_pairs"],
        "physical_isomorphisms": physical["stats"]["isomorphisms"],
        "physical_residuals": len(physical["survivors"]),
        "closure_contradictions": 298,
        "closure_open": len(open_indices),
        "endpoint_branches": len(branch_keys),
        "endpoint_unsat_verified": len(branch_keys),
        "minimum_global_incidence_gap": min(row["gap"] for row in global_rows),
        "core_clause_histogram": core_histogram,
    }
    output = json.loads(json.dumps(output))
    if output != load("EXPECTED_OUTPUT.json"):
        raise ValueError("unexpected final summary")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
