#!/usr/bin/env python3
"""Coarse exhaustive scan for the density-127, deficit-five overlap lemma."""

import collections
import itertools
import json
import sys
import time

import networkx as nx


CATALOG = sys.argv[1]
OUTPUT = sys.argv[2]
THRESHOLD = 127
TOLERANCE = 5


def main():
    started = time.time()
    histogram = collections.Counter()
    buckets = collections.defaultdict(lambda: collections.Counter())
    retained = 0
    rooted = 0
    for graph_index, line in enumerate(open(CATALOG, "rb")):
        graph = nx.from_graph6_bytes(line.strip())
        edge_count = graph.number_of_edges()
        histogram[edge_count] += 1
        if edge_count < THRESHOLD:
            continue
        retained += 1
        full_degree = dict(graph.degree())
        for root in graph:
            common = tuple(graph.neighbors(root))
            common_graph = graph.subgraph(common)
            degrees = tuple(sorted(dict(common_graph.degree()).values()))
            p_value = sum(full_degree[v] for v in common)
            q_value = sum(
                full_degree[u] + full_degree[v]
                - len(set(graph[u]) & set(graph[v]))
                for u, v in common_graph.edges()
            )
            buckets[(len(common), degrees)][(p_value, q_value)] += 1
            rooted += 1

    stats = collections.Counter()
    survivors = []
    for (common_order, degrees), profile_counts in buckets.items():
        edges = sum(degrees) // 2
        first_target = common_order * (29 - common_order) + 2 * edges
        second_target = sum(x * x for x in degrees) + (40 - common_order) * edges
        profiles = sorted(profile_counts)
        for left, right in itertools.combinations_with_replacement(profiles, 2):
            stats["profile_pairs"] += 1
            first_margin = left[0] + right[0] + TOLERANCE - first_target
            if first_margin < 0:
                stats["rejected_first"] += 1
                continue
            second_margin = (left[1] + right[1]
                             + TOLERANCE * max(degrees, default=0)
                             - second_target)
            if second_margin < 0:
                stats["rejected_second"] += 1
                continue
            stats["surviving_profile_pairs"] += 1
            survivors.append({
                "common_order": common_order,
                "common_degree_sequence": degrees,
                "left": left,
                "right": right,
                "left_occurrences": profile_counts[left],
                "right_occurrences": profile_counts[right],
                "first_margin": first_margin,
                "second_margin": second_margin,
            })

    result = {
        "status": "COMPLETE_COARSE_SCAN",
        "catalog_graphs": sum(histogram.values()),
        "catalog_histogram": dict(sorted(histogram.items())),
        "threshold": THRESHOLD,
        "retained_graphs": retained,
        "rooted_occurrences": rooted,
        "bucket_count": len(buckets),
        "distinct_profiles": sum(len(x) for x in buckets.values()),
        "tolerance": TOLERANCE,
        "stats": dict(stats),
        "survivors": survivors,
        "elapsed_seconds": time.time() - started,
    }
    with open(OUTPUT, "w") as handle:
        json.dump(result, handle, sort_keys=True)
        handle.write("\n")
    print(json.dumps({key: result[key] for key in (
        "status", "catalog_graphs", "retained_graphs", "rooted_occurrences",
        "bucket_count", "distinct_profiles", "stats", "elapsed_seconds")},
                     sort_keys=True))


main()
