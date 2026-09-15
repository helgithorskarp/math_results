#!/usr/bin/env python3
"""Independent arithmetic, graph-search, and corruption controls."""

import copy
import json
from itertools import combinations, product

import verify as review


PRIMES = (3, 5, 11)


def mask_factor(mask):
    result = 1
    for bit, prime in enumerate(PRIMES):
        if mask & (1 << bit):
            result *= prime
    return result


def mask_multiply(first, second):
    result = [0] * 8
    for i, a in enumerate(first):
        for j, b in enumerate(second):
            result[i ^ j] += a * b * mask_factor(i & j)
    return tuple(result)


def mask_squared_distance(first, second):
    dx = tuple(a - b for a, b in zip(review.axis_to_flat(first[0]),
                                     review.axis_to_flat(second[0]), strict=True))
    dy = tuple(a - b for a, b in zip(review.axis_to_flat(first[1]),
                                     review.axis_to_flat(second[1]), strict=True))
    xx = mask_multiply(dx, dx)
    yy = mask_multiply(dy, dy)
    return tuple(a + b for a, b in zip(xx, yy, strict=True))


def brute_colourable(vertices, edges, colours):
    return any(all(word[first] != word[second] for first, second in edges)
               for word in product(range(colours), repeat=vertices))


def expect_failure(call):
    try:
        call()
    except ValueError:
        return
    raise ValueError("semantic corruption accepted")


def main():
    basis_products = 0
    for i in range(8):
        for j in range(8):
            first = tuple(int(index == i) for index in range(8))
            second = tuple(int(index == j) for index in range(8))
            tower = review.axis_to_flat(
                review.f_mul(review.axis_from_flat(first),
                             review.axis_from_flat(second)))
            review.need(tower == mask_multiply(first, second),
                        "tower/mask multiplication disagreement")
            basis_products += 1

    geometry = review.build_geometry()
    mask_edges = tuple(
        (first, second)
        for first, second in combinations(range(451), 2)
        if mask_squared_distance(geometry["points"][first],
                                 geometry["points"][second])
        == (review.SCALE * review.SCALE,) + (0,) * 7
    )
    review.need(mask_edges == geometry["edges"], "mask edge stream")

    pairs = list(combinations(range(5), 2))
    solver_checks = 0
    for mask in range(1 << len(pairs)):
        edges = [edge for bit, edge in enumerate(pairs) if mask & (1 << bit)]
        for colours in (2, 3):
            review.need(review.k_colourable(5, edges, colours)
                        == brute_colourable(5, edges, colours),
                        "small colouring search")
            solver_checks += 1

    triangle = {(0, 1), (0, 2), (1, 2)}
    path = {(0, 1), (1, 2)}
    review.need(review.graph_isomorphic(3, triangle, triangle),
                "isomorphism reflexivity")
    review.need(not review.graph_isomorphic(3, triangle, path),
                "isomorphism false positive")
    visited, cuts = review.cut_vertices_after_pair(
        review.adjacency(3, path), -1, -1)
    review.need(visited == 3 and cuts == {1}, "path cut control")
    visited, cuts = review.cut_vertices_after_pair(
        review.adjacency(3, triangle), -1, -1)
    review.need(visited == 3 and not cuts, "triangle cut control")

    parent = json.loads((review.PARENT / "certificate.json").read_text())
    target = json.loads((review.TARGET / "certificate.json").read_text())
    review.verify_relations(geometry)
    corrupted = copy.deepcopy(target)
    pattern = parent["surviving_patterns"][0]
    word = list(corrupted["words"][pattern])
    first, second = geometry["edges"][0]
    word[second] = word[first]
    corrupted["words"][pattern] = "".join(word)

    def check_corruption():
        candidate = corrupted["words"][pattern]
        review.need(candidate[:10] == pattern
                    and review.proper(candidate, 451, geometry["edges"]),
                    "corrupted word")

    expect_failure(check_corruption)
    expect_failure(lambda: review.f_div_exact(((1, 0, 0, 0), review.E_ZERO), 2))

    print(json.dumps({
        "status": "CONTROLS_PASSED",
        "basis_products_checked": basis_products,
        "alternative_point_pairs_scanned": 451 * 450 // 2,
        "alternative_edges_recovered": len(mask_edges),
        "small_graph_colour_checks": solver_checks,
        "isomorphism_and_cut_controls": 4,
        "semantic_corruptions_rejected": 2,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
