#!/usr/bin/env python3
"""Direct forbidden-five unit closure for every physical t=5 residual map."""

import argparse
import collections
import itertools
import json
import time
from pathlib import Path

import networkx as nx


def put(fixed, pair, value):
    pair = tuple(sorted(pair))
    if pair in fixed and fixed[pair] != value:
        raise ValueError("inconsistent fixed edge " + repr(pair))
    fixed[pair] = value


def fixed_gluing(item, graphs):
    left = graphs[item["left_catalog_index"]]
    right = graphs[item["right_catalog_index"]]
    left_root = item["left_root"]
    right_root = item["right_root"]
    left_common = tuple(item["left_common"])
    right_images = tuple(item["right_common_images"])
    left_tail = tuple(sorted(set(left) - {left_root} - set(left_common)))
    right_tail = tuple(sorted(set(right) - {right_root} - set(right_images)))
    common_order = len(left_common)
    if len(left_tail) != 23 - common_order or len(right_tail) != 23 - common_order:
        raise ValueError("root partition")

    left_map = {left_root: 1}
    left_map.update({vertex: 2 + index
                     for index, vertex in enumerate(left_common)})
    left_map.update({vertex: 2 + common_order + index
                     for index, vertex in enumerate(left_tail)})
    right_tail_start = 25
    right_map = {right_root: 0}
    right_map.update({vertex: 2 + index
                      for index, vertex in enumerate(right_images)})
    right_map.update({vertex: right_tail_start + index
                      for index, vertex in enumerate(right_tail)})

    fixed = {}
    for a, b in itertools.combinations(range(24), 2):
        put(fixed, (left_map[a], left_map[b]), int(left.has_edge(a, b)))
        put(fixed, (right_map[a], right_map[b]), int(right.has_edge(a, b)))
    common = tuple(range(2, 2 + common_order))
    left_side = tuple(range(2 + common_order, 25))
    right_side = tuple(range(25, 48 - common_order))
    active_order = 48 - common_order
    for vertex in range(1, 43):
        put(fixed, (0, vertex), int(vertex in (1,) + common + left_side))
    for vertex in range(43):
        if vertex != 1:
            put(fixed, (1, vertex), int(vertex in (0,) + common + right_side))
    return fixed, active_order


def close(fixed, active_order):
    assigned = dict(fixed)
    reasons = {}
    clauses = []
    occurrences = collections.defaultdict(list)
    queue = collections.deque()
    five_sets = 0
    for chosen in itertools.combinations(range(active_order), 5):
        five_sets += 1
        pairs = tuple(itertools.combinations(chosen, 2))
        for target in (0, 1):
            if any(assigned.get(pair) == target for pair in pairs):
                continue
            unknown = tuple(pair for pair in pairs if pair not in assigned)
            if not unknown:
                return {
                    "status": "CONTRADICTION",
                    "five_sets_checked": five_sets,
                    "active_clauses": len(clauses),
                    "forced_edges": 0,
                    "conflict": {"type": "initial_monochromatic_K5",
                                 "vertices": chosen, "color": 1 - target},
                    "trace": [],
                }
            index = len(clauses)
            clauses.append({"target": target, "vertices": chosen,
                            "unknown": unknown, "remaining": len(unknown),
                            "satisfied": False})
            for pair in unknown:
                occurrences[pair].append(index)
            if len(unknown) == 1:
                queue.append((unknown[0], target, index))

    trace = []
    while queue:
        pair, value, reason = queue.popleft()
        if pair in assigned:
            if assigned[pair] != value:
                return {
                    "status": "CONTRADICTION",
                    "five_sets_checked": five_sets,
                    "active_clauses": len(clauses),
                    "forced_edges": len(trace),
                    "conflict": {"type": "opposite_forces", "edge": pair,
                                 "first_reason": reasons.get(pair),
                                 "second_reason": reason},
                    "trace": trace,
                }
            continue
        assigned[pair] = value
        reasons[pair] = reason
        trace.append({"edge": pair, "value": value, "reason": reason})
        for clause_index in occurrences[pair]:
            clause = clauses[clause_index]
            if clause["satisfied"]:
                continue
            if value == clause["target"]:
                clause["satisfied"] = True
                continue
            clause["remaining"] -= 1
            if clause["remaining"] == 0:
                return {
                    "status": "CONTRADICTION",
                    "five_sets_checked": five_sets,
                    "active_clauses": len(clauses),
                    "forced_edges": len(trace),
                    "conflict": {"type": "monochromatic_K5_after_closure",
                                 "vertices": clause["vertices"],
                                 "color": 1 - clause["target"],
                                 "clause": clause_index},
                    "trace": trace,
                }
            if clause["remaining"] == 1:
                last = next(edge for edge in clause["unknown"]
                            if edge not in assigned)
                queue.append((last, clause["target"], clause_index))
    return {"status": "OPEN", "five_sets_checked": five_sets,
            "active_clauses": len(clauses), "forced_edges": len(trace),
            "trace": trace}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--physical", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    physical = json.loads(args.physical.read_text())
    rows = args.catalog.read_bytes().splitlines()
    used = {item[key] for item in physical["survivors"]
            for key in ("left_catalog_index", "right_catalog_index")}
    graphs = {index: nx.from_graph6_bytes(rows[index]) for index in used}
    results = []
    started = time.time()
    items = physical["survivors"]
    if args.limit is not None:
        items = items[:args.limit]
    for index, item in enumerate(items):
        fixed, active_order = fixed_gluing(item, graphs)
        result = close(fixed, active_order)
        result.update({
            "residual_index": index,
            "profile_pair_index": item["profile_pair_index"],
            "left_catalog_index": item["left_catalog_index"],
            "left_root": item["left_root"],
            "right_catalog_index": item["right_catalog_index"],
            "right_root": item["right_root"],
            "right_common_images": item["right_common_images"],
            "active_order": active_order,
        })
        results.append(result)
        print(json.dumps({key: result.get(key) for key in
                          ("residual_index", "profile_pair_index", "status",
                           "forced_edges", "conflict")}, sort_keys=True),
              flush=True)
    statuses = collections.Counter(item["status"] for item in results)
    output = {
        "status": ("COMPLETE_ALL_RESIDUALS_CONTRADICT" if
                   len(results) == len(physical["survivors"]) and
                   statuses == {"CONTRADICTION": len(results)} else
                   "INCOMPLETE_OR_OPEN_RESIDUALS"),
        "physical_residuals": len(physical["survivors"]),
        "tested_residuals": len(results),
        "status_counts": dict(statuses),
        "forced_edge_histogram": dict(sorted(collections.Counter(
            item["forced_edges"] for item in results).items())),
        "elapsed_seconds": time.time() - started,
        "results": results,
    }
    args.output.write_text(json.dumps(output, sort_keys=True) + "\n")
    print(json.dumps({key: output[key] for key in
                      ("status", "physical_residuals", "tested_residuals",
                       "status_counts", "forced_edge_histogram",
                       "elapsed_seconds")}, sort_keys=True))


if __name__ == "__main__":
    main()
