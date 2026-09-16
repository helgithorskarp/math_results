#!/usr/bin/env python3
"""Negative and sensitivity controls for the independent quartic review."""

import argparse
import json
from pathlib import Path

import independent_check as review


HERE = Path(__file__).resolve().parent


def components(order, edges, deleted_vertices=(), deleted_edges=()):
    deleted_vertices = set(deleted_vertices)
    deleted_edges = {tuple(sorted(edge)) for edge in deleted_edges}
    graph = [[] for _ in range(order)]
    for left, right in edges:
        if left in deleted_vertices or right in deleted_vertices:
            continue
        if tuple(sorted((left, right))) in deleted_edges:
            continue
        graph[left].append(right)
        graph[right].append(left)
    unseen = set(range(order)) - deleted_vertices
    sizes = []
    while unseen:
        start = min(unseen)
        seen = {start}
        stack = [start]
        while stack:
            for other in graph[stack.pop()]:
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
        sizes.append(len(seen))
        unseen -= seen
    return sorted(sizes)


def must_reject(function, message):
    try:
        function()
    except review.ReviewFailure:
        return
    raise review.ReviewFailure("control was accepted: " + message)


def run():
    built = review.construct()
    order = len(built["points"])
    word, _, _ = review.fresh_three_colouring(order, built["edges"])

    must_reject(lambda: review.validate_sieve(157, 13), "bad finite-field root")
    must_reject(lambda: review.validate_sieve(8, 0), "noninvertible denominator")

    bad_word = list(word)
    left, right = built["edges"][0]
    bad_word[right] = bad_word[left]
    must_reject(lambda: review.validate_word("".join(bad_word), order, built["edges"]),
                "monochromatic review word")

    bad_source = list(built["source"])
    changed = list(bad_source[0])
    changed[0] += 1
    bad_source[0] = tuple(changed)
    bad_edges, _, _ = review.complete_edges(bad_source)
    review.need(len(bad_edges) != 198 or review.digest([review.encode_point(point) for point in bad_source])
                != "5cf77673a80f4c571fb405c8ace8cf7dde1b84c4e9d62718c9bb7083018aa0d9",
                "source-coordinate perturbation was invisible")

    threshold_counts = {
        str(threshold): sum(count >= threshold for count in built["contacts"].values())
        for threshold in (3, 4, 5, 6)
    }
    review.need(threshold_counts == {"3": 132, "4": 32, "5": 10, "6": 0},
                "threshold sensitivity")

    omitted = sorted(built["points"][:-1])
    review.need(review.digest([review.encode_point(point) for point in omitted])
                != "19001684386ee2397e2e8d062c195ee4efdc9b42b9df3748aeed74f6cf6187ac",
                "selected-point omission was invisible")

    source_vertex_components = components(74, built["source_edges"], [35, 38])
    source_edge_components = components(74, built["source_edges"], deleted_edges=[(0, 10), (10, 24), (10, 48)])
    completion_vertex_components = components(order, built["edges"], [96, 97, 100])
    completion_edge_components = components(order, built["edges"], deleted_edges=[(95, 96), (95, 97), (95, 100)])
    review.need(source_vertex_components == [8, 64], "source two-vertex cut")
    review.need(source_edge_components == [1, 73], "source three-edge cut")
    review.need(completion_vertex_components == [1, 202], "completion three-vertex cut")
    review.need(completion_edge_components == [1, 205], "completion three-edge cut")

    triangle = (11, 39, 79)
    edge_set = set(built["edges"])
    review.need(all(tuple(sorted(edge)) in edge_set for edge in ((11, 39), (11, 79), (39, 79))),
                "source triangle sensitivity")

    return {
        "status": "PASS",
        "bad_sieves_rejected": 2,
        "monochromatic_word_rejected": True,
        "source_coordinate_perturbation_detected": True,
        "threshold_selected_counts": threshold_counts,
        "selected_point_omission_detected": True,
        "source_two_vertex_cut_components": source_vertex_components,
        "source_three_edge_cut_components": source_edge_components,
        "completion_three_vertex_cut_components": completion_vertex_components,
        "completion_three_edge_cut_components": completion_edge_components,
        "source_triangle_retained": len(triangle) == 3,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    arguments = parser.parse_args()
    result = run()
    if arguments.check_expected:
        expected = json.loads((HERE / "CONTROLS_EXPECTED.json").read_text())
        review.need(result == expected, "controls differ from CONTROLS_EXPECTED.json")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
