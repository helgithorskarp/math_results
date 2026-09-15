#!/usr/bin/env python3
"""Small exhaustive and semantic controls for the independent checker."""

import json
from itertools import combinations, product

import verify as review


def brute_colourable(vertices, edges, pins):
    for word in product(range(4), repeat=vertices):
        if any(word[vertex] != colour for vertex, colour in pins.items()):
            continue
        if all(word[first] != word[second] for first, second in edges):
            return True
    return False


def main():
    # Check the generic multiquadratic engine against the independently
    # expanded norm on a complete small coefficient box.
    norm_checks = 0
    for a, b, c, d in product(range(-2, 3), repeat=4):
        squared = review.squared_distance(review.flat_point((a, b, c, d)),
                                           review.flat_point((0, 0, 0, 0)))
        expected = [0] * 8
        expected[0] = a * a + 33 * b * b + 3 * c * c + 11 * d * d
        expected[5] = 2 * (a * b + c * d)
        review.need(squared == tuple(expected), "expanded norm control")
        norm_checks += 1

    # Multiplication-table associativity on all basis triples catches mask or
    # repeated-radical reduction errors without using target coordinates.
    basis = [tuple(int(i == j) for i in range(8)) for j in range(8)]
    associativity_checks = 0
    for first, second, third in product(basis, repeat=3):
        review.need(review.multiply(review.multiply(first, second), third)
                    == review.multiply(first, review.multiply(second, third)),
                    "basis associativity")
        associativity_checks += 1

    # Compare DSATUR with literal brute force on every labelled graph of order
    # five under three materially different pin regimes.
    pairs = list(combinations(range(5), 2))
    pin_regimes = ({}, {0: 0, 1: 0}, {0: 0, 1: 1, 2: 2, 3: 3})
    solver_checks = 0
    for mask in range(1 << len(pairs)):
        edges = [edge for bit, edge in enumerate(pairs) if mask & (1 << bit)]
        for pins in pin_regimes:
            word, _ = review.colour_dsat(5, edges, pins)
            expected = brute_colourable(5, edges, pins)
            review.need((word is not None) == expected, "small solver control")
            if word is not None:
                review.need(review.proper(word, 5, edges), "small witness")
            solver_checks += 1

    cycle = [(vertex, (vertex + 1) % 5) for vertex in range(5)]
    cycle_adj = review.adjacency(5, cycle)
    components, cuts = review.cut_vertices_after(cycle_adj, ())
    review.need(components == 1 and not cuts, "cycle articulation control")
    components, _ = review.cut_vertices_after(cycle_adj, (0, 2))
    review.need(components == 2, "cycle pair-cut control")

    target_certificate = json.loads(
        (review.TARGET / "certificate.json").read_text())
    target_word = target_certificate["proper4"]
    source = review.golomb()
    b214 = review.read_b214()
    full, _ = review.merge_blocks(source,
                                  review.shift_b214(b214, False),
                                  review.shift_b214(b214, True))
    points = [full[index] for index in target_certificate["source_ids"]]
    edges = review.exact_edges(points)
    first, second = edges[0]
    corrupted = list(target_word)
    corrupted[second] = corrupted[first]
    review.need(not review.proper("".join(corrupted), 241, edges),
                "monochromatic edge accepted")
    deletion = target_certificate["deletion_words"]["10"]
    review.need(not review.proper(deletion.replace("-", "0"), 241, edges, 10),
                "missing deletion marker accepted")

    print(json.dumps({
        "status": "CONTROLS_PASSED",
        "expanded_norm_checks": norm_checks,
        "basis_associativity_checks": associativity_checks,
        "small_graph_solver_checks": solver_checks,
        "cycle_cut_controls": 2,
        "semantic_corruptions_rejected": 2,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
