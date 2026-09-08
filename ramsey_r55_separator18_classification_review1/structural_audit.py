#!/usr/bin/env python3
"""Independent arithmetic audit for the separator-18 reduction.

This checker imports no claimant module.  It exhausts R(3,3;6), checks the
displayed degree arguments for R(3,4)<=9 and R(3,5)<=14, and enumerates every
component-size/independence profile compatible with the imported minimum
degree 18 and the independence budget four.
"""

import argparse
import itertools
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def edge_index(n):
    return {pair: i for i, pair in enumerate(itertools.combinations(range(n), 2))}


def clique(code, vertices, index):
    return all(code >> index[pair] & 1 for pair in itertools.combinations(vertices, 2))


def exhaustive_r33():
    index = edge_index(6)
    triples = list(itertools.combinations(range(6), 3))
    checked = 0
    for code in range(1 << 15):
        red = any(clique(code, q, index) for q in triples)
        blue = any(all(not (code >> index[pair] & 1)
                       for pair in itertools.combinations(q, 2)) for q in triples)
        require(red or blue, "R(3,3)<=6 counterexample")
        checked += 1
    return checked


def component_profiles():
    caps = {1: 4, 2: 13, 3: 24}
    types = [
        (size, alpha)
        for alpha in (1, 2, 3)
        for size in range(alpha, caps[alpha] + 1)
    ]
    candidates = set()
    for separator_size in range(19):
        for number_of_components in range(2, 5):
            for chosen in itertools.combinations_with_replacement(types, number_of_components):
                if sum(size for size, _ in chosen) != 43 - separator_size:
                    continue
                if sum(alpha for _, alpha in chosen) > 4:
                    continue
                if any(size + separator_size < 19 for size, _ in chosen):
                    continue
                candidates.add((separator_size, tuple(sorted(chosen))))

    rows = []
    for separator_size, chosen in sorted(candidates):
        row = {
            "separator_size": separator_size,
            "component_types": [list(item) for item in chosen],
        }
        clique_component = next(
            (size for size, alpha in chosen if alpha == 1 and size > 1), None
        )
        if clique_component is not None:
            lower = (clique_component * (19 - clique_component)
                     - (clique_component - 1) * separator_size)
            upper = {2: 13, 3: 4, 4: 0}[clique_component]
            require(lower > upper, "clique component not contradicted")
            row.update(
                reason="clique_common_neighborhood",
                a=clique_component,
                lower=lower,
                upper=upper,
            )
        elif chosen == ((13, 2), (13, 2)):
            require(separator_size == 17, "13+13 separator size")
            row["reason"] = "two_thirteen_components"
        elif chosen == ((12, 2), (13, 2)):
            require(separator_size == 18, "12+13 separator size")
            row["reason"] = "unique_twelve_attachment"
        elif chosen == ((1, 1), (24, 3)):
            require(separator_size == 18, "singleton boundary size")
            row["reason"] = "allowed_singleton_boundary"
        else:
            raise ValueError(("unclassified component profile", separator_size, chosen))
        rows.append(row)
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--claim-package", required=True, type=Path)
    args = parser.parse_args()
    certificate = json.loads((args.claim_package / "CERTIFICATE.json").read_text())

    r33_checked = exhaustive_r33()
    require(r33_checked == 32768, "R(3,3) graph count")

    # In a triangle-free graph with alpha<=3 on nine vertices, every
    # neighborhood has size<=3.  R(3,3)<=6 bounds every nonneighbor set by
    # five, so every degree is also >=3; a 3-regular graph on nine vertices
    # would have odd degree sum 27.
    require(3 * 9 % 2 == 1, "R(3,4) parity contradiction")
    # In a triangle-free graph with alpha<=4 on fourteen vertices,
    # neighborhoods have size<=4.  R(3,4)<=9 bounds a nonneighbor set by
    # eight, so degrees are >=13-8=5.
    require(13 - 8 > 4, "R(3,5) degree contradiction")

    profiles = component_profiles()
    require(profiles == certificate["component_profiles"], "component profile mismatch")
    reasons = {}
    for row in profiles:
        reasons[row["reason"]] = reasons.get(row["reason"], 0) + 1

    result = {
        "status": "INDEPENDENT_STRUCTURAL_ARITHMETIC_VERIFIED",
        "claimant_modules_imported": False,
        "R33_graphs_exhausted": r33_checked,
        "R34_upper_bound_9_degree_parity_checked": True,
        "R35_upper_bound_14_degree_contradiction_checked": True,
        "R45_upper_bound_25_imported": True,
        "minimum_degree_in_each_colour": 18,
        "component_profiles": len(profiles),
        "profile_reasons": dict(sorted(reasons.items())),
        "retained_profile": {"separator_size": 18, "component_orders": [1, 24]},
        "unresolved_before_attachment_lemma": [
            {"separator_size": 17, "component_orders": [13, 13]},
            {"separator_size": 18, "component_orders": [12, 13]},
        ],
    }
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
