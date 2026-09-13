#!/usr/bin/env python3
"""Semantic negative controls for the independent separated-triple audit."""

from itertools import combinations, product
import json
from pathlib import Path

import independent_audit as audit


HERE = Path(__file__).resolve().parent


def main():
    proper, _ = audit.circle_audit()

    # The sqrt(3) intersection chord is one C6 edge, so its two endpoints
    # cannot both receive the same leaf-palette colour.
    if any(word[0] == word[1] for word in proper):
        raise AssertionError("false equal-colour sqrt(3) endpoint claim accepted")

    # A deliberately wrong central prescription (same colour on adjacent
    # vertices) cannot be extended by either proper C6 word.
    if any(word[0] == 0 and word[1] == 0 for word in proper):
        raise AssertionError("wrong central prescription accepted")

    # Reconstruct the spindle and confirm every edge is essential to its
    # three-colour obstruction.  This detects an omitted strict unit edge.
    zero = audit.complex_number()
    u = audit.complex_number(1)
    v = (audit.rational(audit.Q(1, 2)),
         (audit.Q(0), audit.Q(1, 2), audit.Q(0), audit.Q(0)))
    rho = (audit.rational(audit.Q(5, 6)),
           (audit.Q(0), audit.Q(0), audit.Q(1, 6), audit.Q(0)))
    uv = audit.complex_add(u, v)
    vertices = (zero, u, v, uv, audit.complex_multiply(rho, u),
                audit.complex_multiply(rho, v), audit.complex_multiply(rho, uv))
    edges = tuple(pair for pair in combinations(range(7), 2)
                  if audit.squared_distance(vertices[pair[0]], vertices[pair[1]]) == audit.ONE)
    edge_deletions_three_colourable = 0
    for omitted in edges:
        remaining = set(edges) - {omitted}
        if any(all(word[i] != word[j] for i, j in remaining)
               for word in product(range(3), repeat=7)):
            edge_deletions_three_colourable += 1
    if edge_deletions_three_colourable != 11:
        raise AssertionError(edge_deletions_three_colourable)

    result = {
        "status": "PASS",
        "false_equal_colour_sqrt3_claim_rejected": True,
        "wrong_adjacent_central_prescription_rejected": True,
        "sharpness_edge_deletions_three_colourable": edge_deletions_three_colourable,
        "distance_three_cross_leaf_edge_retained": audit.boundary_audit()["distance_three_cross_leaf_edge_witness"],
    }
    if result != json.loads((HERE / "EXPECTED_CONTROLS.json").read_text()):
        raise AssertionError("expected controls mismatch")
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
