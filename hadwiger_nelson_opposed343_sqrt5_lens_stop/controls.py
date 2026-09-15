#!/usr/bin/env python3
"""Independent arithmetic, graph, and corruption controls for the lens stop."""

from __future__ import annotations

from itertools import combinations
import copy
import json

import verify as V


PRIMES = (3, 5, 11)


def mask_radicand(mask):
    result = 1
    for bit, prime in enumerate(PRIMES):
        if mask >> bit & 1:
            result *= prime
    return result


def multiply_by_masks(a, b):
    """Alternative multiplication via bit masks, not gcd/radicand lookup."""
    out = [0] * 8
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i ^ j] += x * y * mask_radicand(i & j)
    return tuple(out)


def squared_distance_by_masks(p, q):
    dx = tuple(x - y for x, y in zip(p[0], q[0]))
    dy = tuple(x - y for x, y in zip(p[1], q[1]))
    return tuple(x + y for x, y in zip(multiply_by_masks(dx, dx),
                                      multiply_by_masks(dy, dy)))


def expect_failure(call):
    try:
        call()
    except ValueError:
        return
    raise ValueError("corrupted control was accepted")


def run():
    # Exhaust the multiplication table with independently derived repeated
    # radical factors.
    basis_products = 0
    for i in range(8):
        for j in range(8):
            a = tuple(V.SCALE if k == i else 0 for k in range(8))
            b = tuple(V.SCALE if k == j else 0 for k in range(8))
            V.need(V.multiply_raw(a, b) == multiply_by_masks(a, b),
                   "basis multiplication disagreement")
            basis_products += 1

    geometry = V.build_geometry()
    alternative_edges = tuple(
        (a, b) for a, b in combinations(range(451), 2)
        if squared_distance_by_masks(geometry["points"][a], geometry["points"][b])
        == V.UNIT_SQUARED
    )
    V.need(alternative_edges == geometry["edges"], "alternative complete edge scan disagrees")

    # Positive certificates do not rely on the producing solver: corrupt one
    # actual edge explicitly and require direct rejection.
    source = json.loads((V.SOURCE / "certificate.json").read_text())
    certificate = json.loads((V.HERE / "certificate.json").read_text())
    V.verify_positive_certificate(certificate, geometry, source["surviving_patterns"])
    corrupted = copy.deepcopy(certificate)
    pattern = source["surviving_patterns"][0]
    word = list(corrupted["words"][pattern])
    a, b = next(edge for edge in geometry["edges"] if edge[0] >= 10 and edge[1] >= 10)
    word[b] = word[a]
    corrupted["words"][pattern] = "".join(word)
    expect_failure(lambda: V.verify_positive_certificate(
        corrupted, geometry, source["surviving_patterns"]))

    # Definition-level graph cut controls.
    V.need(V.separation_counts(3, ((0, 1), (1, 2))) == (1, 2), "path cut control")
    V.need(V.separation_counts(3, ((0, 1), (1, 2), (0, 2))) == (0, 0),
           "triangle cut control")
    expect_failure(lambda: V.divide_exact((1,) + (0,) * 7, 2))

    # The field extension is substantive: every new point has a nonzero
    # coefficient in a basis term containing sqrt(5).
    outside = sum(any(point[axis][mask] for axis in (0, 1) for mask in (2, 3, 6, 7))
                  for point in geometry["points"][343:])
    V.need(outside == 108, "outside-field control")

    return {
        "verified": True,
        "basis_products_checked": basis_products,
        "alternative_point_pairs_scanned": 451 * 450 // 2,
        "alternative_edges_recovered": len(alternative_edges),
        "positive_certificate_accepted_before_corruption": True,
        "improper_word_corruption_rejected": True,
        "nonintegral_division_rejected": True,
        "path_and_triangle_cut_controls": True,
        "outside_source_field_points": outside,
        "normal_assertions_not_required": True,
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
