#!/usr/bin/env python3
"""Exact C-to-T feasibility for neighborhood-closure-open t=5 residuals."""

import argparse
import collections
import itertools
import json
import time
from pathlib import Path

import networkx as nx
import numpy as np


def delta_table(order):
    rows = []
    for total in range(6):
        for tokens in itertools.combinations_with_replacement(range(order), total):
            row = [0] * order
            for token in tokens:
                row[token] += 1
            rows.append(row)
    return np.asarray(rows, dtype=np.int8)


def ct_feasible(order, row_degrees, caps):
    t_size = order - 5
    full = range(t_size)
    domains = [[sum(1 << bit for bit in chosen)
                for chosen in itertools.combinations(full, degree)]
               for degree in row_degrees]
    if any(not domain for domain in domains):
        return None
    constrained_degree = collections.Counter()
    for i, j in caps:
        constrained_degree[i] += 1
        constrained_degree[j] += 1
    order_rows = sorted(range(order),
                        key=lambda i: (len(domains[i]),
                                       -constrained_degree[i], i))
    # T labels are globally exchangeable; normalize one nonconstant row.
    first = next((i for i in order_rows if len(domains[i]) > 1), None)
    if first is not None:
        domains[first] = domains[first][:1]
    assigned = {}

    def visit(position):
        if position == len(order_rows):
            return tuple(assigned[i] for i in range(order))
        vertex = order_rows[position]
        for mask in domains[vertex]:
            valid = True
            for other, other_mask in assigned.items():
                cap = caps.get(tuple(sorted((vertex, other))))
                if cap is not None and (mask & other_mask).bit_count() > cap:
                    valid = False
                    break
            if valid:
                assigned[vertex] = mask
                result = visit(position + 1)
                if result is not None:
                    return result
                del assigned[vertex]
        return None

    return visit(0)


def constraints(item, graphs):
    left = graphs[item["left_catalog_index"]]
    right = graphs[item["right_catalog_index"]]
    common = tuple(item["left_common"])
    images = tuple(item["right_common_images"])
    mapping = dict(zip(common, images))
    position = {vertex: index for index, vertex in enumerate(common)}
    common_graph = left.subgraph(common)
    internal = tuple(common_graph.degree(vertex) for vertex in common)
    base = tuple(24 - left.degree(vertex) - right.degree(mapping[vertex])
                 + common_graph.degree(vertex) for vertex in common)
    caps = {}
    for a, b in common_graph.edges():
        cap = (13 - len(set(left[a]) & set(left[b]))
               - len(set(right[mapping[a]]) & set(right[mapping[b]])))
        caps[tuple(sorted((position[a], position[b])))] = cap
    profile_left = tuple(item["left_profile"])
    profile_right = tuple(item["right_profile"])
    c = len(common)
    e = common_graph.number_of_edges()
    first_need = max(0, c * (29 - c) + 2 * e
                     - profile_left[0] - profile_right[0])
    second_need = max(0, sum(value * value for value in internal)
                      + (40 - c) * e
                      - profile_left[1] - profile_right[1])
    vectors = delta_table(c)
    lower = np.asarray([max(0, value - (c - 5)) for value in base])
    upper = np.asarray([min(5, value) for value in base])
    mask = np.all(vectors >= lower, axis=1)
    mask &= np.all(vectors <= upper, axis=1)
    mask &= np.sum(vectors, axis=1) >= first_need
    mask &= vectors @ np.asarray(internal) >= second_need
    for (i, j), cap in caps.items():
        required = base[i] + base[j] - (c - 5) - cap
        mask &= vectors[:, i] + vectors[:, j] >= required
    return base, caps, vectors[np.flatnonzero(mask)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--physical", type=Path, required=True)
    parser.add_argument("--closure", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    physical = json.loads(args.physical.read_text())
    closure = json.loads(args.closure.read_text())
    open_indices = [item["residual_index"] for item in closure["results"]
                    if item["status"] == "OPEN"]
    rows = args.catalog.read_bytes().splitlines()
    used = {physical["survivors"][index][key] for index in open_indices
            for key in ("left_catalog_index", "right_catalog_index")}
    graphs = {index: nx.from_graph6_bytes(rows[index]) for index in used}
    results = []
    started = time.time()
    for residual_index in open_indices:
        item = physical["survivors"][residual_index]
        base, caps, deltas = constraints(item, graphs)
        feasible = []
        for delta_raw in deltas:
            delta = tuple(map(int, delta_raw))
            row_degrees = tuple(base[i] - delta[i] for i in range(len(base)))
            witness = ct_feasible(len(base), row_degrees, caps)
            if witness is not None:
                feasible.append({"delta": delta, "row_masks": witness})
        result = {
            "residual_index": residual_index,
            "profile_pair_index": item["profile_pair_index"],
            "budget_feasible_deltas": len(deltas),
            "ct_feasible_deltas": len(feasible),
            "ct_witnesses": feasible,
        }
        results.append(result)
        print(json.dumps({key: result[key] for key in
                          ("residual_index", "profile_pair_index",
                           "budget_feasible_deltas", "ct_feasible_deltas")},
                         sort_keys=True), flush=True)
    histogram = collections.Counter(item["ct_feasible_deltas"] for item in results)
    output = {
        "status": ("COMPLETE_ALL_OPEN_MAPS_CT_INFEASIBLE" if
                   histogram == {0: len(results)} else
                   "COMPLETE_WITH_CT_FEASIBLE_MAPS"),
        "open_maps": len(results),
        "ct_feasible_map_count": sum(
            item["ct_feasible_deltas"] > 0 for item in results),
        "ct_feasible_delta_histogram": dict(sorted(histogram.items())),
        "elapsed_seconds": time.time() - started,
        "results": results,
    }
    args.output.write_text(json.dumps(output, sort_keys=True) + "\n")
    print(json.dumps({key: output[key] for key in
                      ("status", "open_maps", "ct_feasible_map_count",
                       "ct_feasible_delta_histogram", "elapsed_seconds")},
                     sort_keys=True))


if __name__ == "__main__":
    main()
