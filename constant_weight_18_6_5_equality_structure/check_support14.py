#!/usr/bin/env python3
"""Exact finite local checks supporting SUPPORT14.md; no global code search."""

import argparse
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def odd_matching_check():
    pairs = list(combinations(range(3), 2))
    perfect = []
    for mask in range(1 << len(pairs)):
        edges = [p for i, p in enumerate(pairs) if mask >> i & 1]
        if all(sum(v in p for p in edges) == 1 for v in range(3)):
            perfect.append(mask)
    require(not perfect, "unexpected perfect matching on three vertices")
    weights = list(product((1, 2, 3), repeat=3))
    feasible = [w for w in weights if sum(w) <= 3]
    require(feasible == [(1, 1, 1)], "shared-anchor capacity differs")
    # Each of three S points has precisely the distinct H neighbors a,b,
    # so its incident weights are (2,3) in one order. a also has weight 1
    # to u. Every one of the eight possibilities exceeds a's capacity.
    distinct = list(product(((2, 3), (3, 2)), repeat=3))
    feasible_distinct = [w for w in distinct if 1 + sum(x[0] for x in w) <= 5]
    require(not feasible_distinct, "distinct anchors unexpectedly fit")
    return {"three_vertex_graph_masks": 8, "perfect_matchings": len(perfect),
            "shared_anchor_weight_vectors_checked": len(weights),
            "shared_anchor_possible_weights": [list(w) for w in feasible],
            "distinct_anchor_weight_vectors_checked": len(distinct),
            "distinct_anchor_capacity_solutions": len(feasible_distinct)}


def isolated_checks():
    rows = []
    for h in range(12, 17):
        s = 18 - h
        weights = list(product((2, 3), repeat=s))
        feasible = [w for w in weights if sum(w) <= 5]
        require(bool(feasible) == (h >= 16), "isolated carrier threshold differs")
        rows.append({"h": h, "s": s, "weight_vectors_checked": len(weights),
                     "weighted_degree_solutions": len(feasible)})
    return rows


def pair_checks():
    """Enumerate actual third-point sets for a weight-two S pair.

    H labels 0 and 1 are the two distinct weight-three roots. The S-pair
    has seven H leave thirds, including both roots. The pair (root 0,u)
    has nine H leave thirds plus the forced S mate. The former set must
    be disjoint from the latter except for root 0, which is not a possible
    third point of (root 0,u). This includes the forced omission at root 1.
    """
    rows = []
    for h in range(12, 17):
        universe = set(range(h))
        pair_sets = solutions = 0
        for rest in combinations(range(2, h), 5):
            pair_thirds = {0, 1, *rest}
            pair_sets += 1
            possible_root_thirds = universe - pair_thirds
            for root_thirds in combinations(sorted(possible_root_thirds), 9):
                require(0 not in root_thirds and 1 not in root_thirds,
                        "root thirds contain a root or its forced omission")
                require(set(root_thirds).isdisjoint(pair_thirds),
                        "two leaves occupy a deficit-zero pair")
                solutions += 1
        require(bool(solutions) == (h >= 16), "paired carrier threshold differs")
        rows.append({"h": h, "pair_third_sets_checked": pair_sets,
                     "compatible_root_third_sets": solutions})
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-expected", action="store_true")
    args = parser.parse_args()
    report = {"h_13_odd_matching_and_anchor_checks": odd_matching_check(),
              "isolated_point_carrier": isolated_checks(),
              "weight_two_pair_carrier": pair_checks(),
              "global_72_word_exclusion": False,
              "theorem_depends_on_computation": False}
    raw = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("ascii")
    if args.write_expected:
        (HERE / "support14_expected.json").write_bytes(raw)
    else:
        require((HERE / "support14_expected.json").read_bytes() == raw,
                "exact output differs from support14_expected.json")
    print(raw.decode("ascii"), end="")


if __name__ == "__main__":
    main()
