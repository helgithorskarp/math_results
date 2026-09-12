#!/usr/bin/env python3
"""Enumerate physical mappings surviving density-127, deficit-five budgets."""

import argparse
import collections
import itertools
import json
import time
from pathlib import Path

import networkx as nx
import numpy as np


DELTA_TABLES = {}


def delta_table(order):
    if order not in DELTA_TABLES:
        rows = []
        for total in range(6):
            for tokens in itertools.combinations_with_replacement(
                    range(order), total):
                row = [0] * order
                for token in tokens:
                    row[token] += 1
                rows.append(row)
        DELTA_TABLES[order] = np.asarray(rows, dtype=np.int8)
    return DELTA_TABLES[order]


def delta_witness(base, internal_degree, t_size, first_need, second_need,
                  pair_requirements):
    lower = tuple(max(0, value - t_size) for value in base)
    upper = tuple(min(5, value) for value in base)
    if sum(lower) > 5 or any(a > b for a, b in zip(lower, upper)):
        return None
    vectors = delta_table(len(base))
    mask = np.all(vectors >= np.asarray(lower), axis=1)
    mask &= np.all(vectors <= np.asarray(upper), axis=1)
    mask &= np.sum(vectors, axis=1) >= first_need
    mask &= vectors @ np.asarray(internal_degree) >= second_need
    for i, j, required in pair_requirements:
        mask &= vectors[:, i] + vectors[:, j] >= required
        if not np.any(mask):
            return None
    indices = np.flatnonzero(mask)
    return None if not len(indices) else tuple(map(int, vectors[indices[0]]))


def classify_common_graphs(occurrences):
    """Attach exact iso-class coordinates, doing VF2 only once per occurrence."""
    groups = collections.defaultdict(list)
    for values in occurrences.values():
        for item in values:
            bucket = (len(item["common"]),
                      tuple(sorted(dict(item["common_graph"].degree()).values())),
                      item["wl"])
            groups[bucket].append(item)
    classes = []
    for values in groups.values():
        local_classes = []
        for item in values:
            placed = False
            for class_index in local_classes:
                representative = classes[class_index]["representative"]
                matcher = nx.algorithms.isomorphism.GraphMatcher(
                    item["common_graph"], representative["common_graph"])
                mapping = next(matcher.isomorphisms_iter(), None)
                if mapping is not None:
                    item["class_index"] = class_index
                    item["to_representative"] = mapping
                    placed = True
                    break
            if not placed:
                class_index = len(classes)
                item["class_index"] = class_index
                item["to_representative"] = {
                    vertex: vertex for vertex in item["common"]}
                classes.append({"representative": item, "automorphisms": None})
                local_classes.append(class_index)
    return classes


def class_automorphisms(classes, class_index):
    entry = classes[class_index]
    if entry["automorphisms"] is None:
        graph = entry["representative"]["common_graph"]
        matcher = nx.algorithms.isomorphism.GraphMatcher(graph, graph)
        entry["automorphisms"] = tuple(matcher.isomorphisms_iter())
    return entry["automorphisms"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--coarse", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    coarse = json.loads(args.coarse.read_text())
    survivor_pairs = []
    relevant_keys = set()
    for item in coarse["survivors"]:
        bucket = (item["common_order"], tuple(item["common_degree_sequence"]))
        left = tuple(item["left"])
        right = tuple(item["right"])
        survivor_pairs.append((bucket, left, right))
        relevant_keys.add((bucket, left))
        relevant_keys.add((bucket, right))

    occurrences = collections.defaultdict(list)
    retained_lines = []
    started = time.time()
    for catalog_index, line in enumerate(args.catalog.read_bytes().splitlines()):
        graph = nx.from_graph6_bytes(line)
        if graph.number_of_edges() < 127:
            continue
        dense_index = len(retained_lines)
        retained_lines.append(line.decode("ascii"))
        full_degree = dict(graph.degree())
        for root in graph:
            common = tuple(sorted(graph.neighbors(root)))
            common_graph = graph.subgraph(common).copy()
            degrees = tuple(sorted(dict(common_graph.degree()).values()))
            p_value = sum(full_degree[v] for v in common)
            q_value = sum(
                full_degree[u] + full_degree[v]
                - len(set(graph[u]) & set(graph[v]))
                for u, v in common_graph.edges()
            )
            key = ((len(common), degrees), (p_value, q_value))
            if key in relevant_keys:
                occurrences[key].append({
                    "catalog_index": catalog_index,
                    "dense_index": dense_index,
                    "root": root,
                    "graph": graph,
                    "common": common,
                    "common_graph": common_graph,
                    "wl": nx.weisfeiler_lehman_graph_hash(
                        common_graph, iterations=len(common)),
                })

    stats = collections.Counter()
    survivor_records = []
    survivor_pair_counts = collections.Counter()
    classes = classify_common_graphs(occurrences)
    print(json.dumps({"common_iso_classes": len(classes),
                      "elapsed_seconds": time.time() - started}), flush=True)
    for pair_index, (bucket, left_profile, right_profile) in enumerate(survivor_pairs):
        lefts = occurrences[(bucket, left_profile)]
        rights = occurrences[(bucket, right_profile)]
        if left_profile == right_profile:
            occurrence_pairs = itertools.combinations_with_replacement(lefts, 2)
        else:
            occurrence_pairs = itertools.product(lefts, rights)
        common_order, degrees = bucket
        edge_count = sum(degrees) // 2
        first_need = (common_order * (29 - common_order) + 2 * edge_count
                      - left_profile[0] - right_profile[0])
        second_need = (sum(value * value for value in degrees)
                       + (40 - common_order) * edge_count
                       - left_profile[1] - right_profile[1])
        for left, right in occurrence_pairs:
            stats["occurrence_pairs"] += 1
            if left["class_index"] != right["class_index"]:
                stats["nonisomorphic_occurrence_pairs"] += 1
                continue
            left_to_rep = left["to_representative"]
            right_from_rep = {value: key for key, value in
                              right["to_representative"].items()}
            pair_had_iso = False
            pair_had_budget = False
            for automorphism in class_automorphisms(
                    classes, left["class_index"]):
                mapping = {vertex: right_from_rep[automorphism[left_to_rep[vertex]]]
                           for vertex in left["common"]}
                pair_had_iso = True
                stats["isomorphisms"] += 1
                common = left["common"]
                internal = tuple(left["common_graph"].degree(v) for v in common)
                base = tuple(
                    24 - left["graph"].degree(v)
                    - right["graph"].degree(mapping[v])
                    + left["common_graph"].degree(v)
                    for v in common
                )
                position = {vertex: index for index, vertex in enumerate(common)}
                pair_requirements = []
                impossible_cap = False
                for a, b in left["common_graph"].edges():
                    cap = (13
                           - len(set(left["graph"][a]) & set(left["graph"][b]))
                           - len(set(right["graph"][mapping[a]]) &
                                 set(right["graph"][mapping[b]])))
                    if cap < 0:
                        impossible_cap = True
                        break
                    i, j = position[a], position[b]
                    required = base[i] + base[j] - (common_order - 5) - cap
                    if required > 0:
                        pair_requirements.append((i, j, required))
                if impossible_cap:
                    stats["negative_cap_rejected_isomorphisms"] += 1
                    continue
                witness = delta_witness(base, internal, common_order - 5,
                                        max(0, first_need), max(0, second_need),
                                        tuple(sorted(pair_requirements)))
                if witness is None:
                    stats["budget_rejected_isomorphisms"] += 1
                    continue
                pair_had_budget = True
                stats["budget_feasible_isomorphisms"] += 1
                survivor_pair_counts[pair_index] += 1
                survivor_records.append({
                    "profile_pair_index": pair_index,
                    "common_order": common_order,
                    "left_profile": left_profile,
                    "right_profile": right_profile,
                    "left_dense_index": left["dense_index"],
                    "left_catalog_index": left["catalog_index"],
                    "left_root": left["root"],
                    "left_common": common,
                    "right_dense_index": right["dense_index"],
                    "right_catalog_index": right["catalog_index"],
                    "right_root": right["root"],
                    "right_common_images": tuple(mapping[v] for v in common),
                    "base": base,
                    "delta_witness": witness,
                })
            if pair_had_iso:
                stats["isomorphic_occurrence_pairs"] += 1
            if pair_had_budget:
                stats["budget_feasible_occurrence_pairs"] += 1
        if pair_index % 20 == 19:
            print(json.dumps({"profile_pairs_done": pair_index + 1,
                              "stats": dict(stats),
                              "elapsed_seconds": time.time() - started}),
                  flush=True)

    output = {
        "status": "COMPLETE_PHYSICAL_BUDGET_CLASSIFICATION",
        "threshold": 127,
        "tolerance": 5,
        "catalog_graphs": coarse["catalog_graphs"],
        "retained_graphs": len(retained_lines),
        "relevant_root_occurrences": sum(len(value) for value in occurrences.values()),
        "profile_pairs": len(survivor_pairs),
        "common_iso_classes": len(classes),
        "automorphism_histogram": dict(sorted(collections.Counter(
            len(class_automorphisms(classes, index))
            for index in range(len(classes))).items())),
        "stats": dict(stats),
        "surviving_profile_pair_counts": dict(sorted(survivor_pair_counts.items())),
        "survivors": survivor_records,
        "elapsed_seconds": time.time() - started,
    }
    args.output.write_text(json.dumps(output, sort_keys=True) + "\n")
    print(json.dumps({key: output[key] for key in (
        "status", "retained_graphs", "relevant_root_occurrences",
        "profile_pairs", "stats", "elapsed_seconds")}, sort_keys=True))


if __name__ == "__main__":
    main()
