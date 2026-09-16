#!/usr/bin/env python3
"""Sensitivity and negative controls for the independent triple-P48 review."""

import argparse
import itertools
import json
from pathlib import Path

import independent_check as review


HERE = Path(__file__).resolve().parent


def component_size(order, edges, start):
    graph = review.adjacency(order, edges)
    seen = {start}
    stack = [start]
    while stack:
        for other in graph[stack.pop()]:
            if other not in seen:
                seen.add(other)
                stack.append(other)
    return len(seen)


def run():
    graph = review.reconstruct()
    order = len(graph["roles"])
    word, _ = review.fresh_four_colouring(order, graph["edges"])

    # Every edge of the selected seven-vertex spindle matters: deleting it
    # admits exactly twelve labelled three-colourings.
    deletion_counts = []
    for removed in graph["moser_edges"]:
        remaining = set(graph["moser_edges"]) - {removed}
        deletion_counts.append(sum(
            all(candidate[left] != candidate[right] for left, right in remaining)
            for candidate in itertools.product(range(3), repeat=7)
        ))
    review.need(deletion_counts == [12] * 11, "Moser edge-deletion sensitivity")

    # A single Gram coefficient change destroys the unit calibration.
    scale, gram = review.gram_matrix()
    perturbed = [[tuple(value) for value in row] for row in gram]
    value = list(perturbed[4][4])
    value[0] += 1
    perturbed[4][4] = tuple(value)
    review.need(review.quadratic((0, 0, 0, 0, 1, 0), perturbed)
                != (scale, 0, 0, 0), "Gram perturbation was invisible")

    # A forced monochromatic edge is rejected directly.
    bad_word = list(word)
    left, right = graph["edges"][0]
    bad_word[right] = bad_word[left]
    try:
        review.validate_word("".join(bad_word), order, graph["edges"])
    except review.ReviewFailure:
        pass
    else:
        raise review.ReviewFailure("monochromatic-word control was not rejected")

    # The displayed two-edge and two-vertex cuts disconnect, whereas each
    # single incident edge does not (there are no bridges).
    vertex = 0
    neighbours = sorted(review.adjacency(order, graph["edges"])[vertex])
    incident = [tuple(sorted((vertex, other))) for other in neighbours]
    review.need(len(review.reached_vertices(order, graph["edges"], neighbours)) == 1,
                "vertex-cut sensitivity")
    review.need(len(review.reached_vertices(order, graph["edges"], deleted_edges=incident)) == 1,
                "edge-cut sensitivity")
    single_edge_component_sizes = [
        len(review.reached_vertices(order, graph["edges"], deleted_edges=[edge]))
        for edge in incident
    ]
    review.need(single_edge_component_sizes == [order, order], "single edge became a bridge")

    # Omitting the sole layer-1/layer-2 contact breaks the patch interaction
    # cycle even though the first two patches remain joined in six places.
    last_contact = next(
        edge for edge in graph["extra"]
        if ((edge[0] in graph["layer_sets"][1] and edge[1] in graph["layer_sets"][2])
            or (edge[1] in graph["layer_sets"][1] and edge[0] in graph["layer_sets"][2]))
    )
    without_last_contact = set(graph["edges"]) - {last_contact}
    review.need(component_size(order, without_last_contact, vertex) == order,
                "finite graph unexpectedly disconnected after one contact deletion")

    return {
        "status": "PASS",
        "moser_single_edge_deletion_colourings": deletion_counts,
        "gram_perturbation_detected": True,
        "monochromatic_word_detected": True,
        "two_vertex_cut_detected": True,
        "two_edge_cut_detected": True,
        "single_incident_edge_component_sizes": single_edge_component_sizes,
        "last_patch_contact_deletion_graph_connected": True,
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
