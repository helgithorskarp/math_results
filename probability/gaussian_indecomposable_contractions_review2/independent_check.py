#!/usr/bin/env python3
"""Independent exact checks for the indecomposable-contraction review.

This checker imports no code or data from the reviewed packet.  It works
directly with dictionaries of labelled squared distances, certifies why the
binary reflection parametrisation is complete, enumerates the full distance
intervals of four fixtures, and checks the coefficient identities used for
the all-depth regular-simplex flap argument.
"""

import argparse
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def vec_sub(x, y):
    return tuple(a - b for a, b in zip(x, y))


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def cross(x, y):
    return (
        x[1] * y[2] - x[2] * y[1],
        x[2] * y[0] - x[0] * y[2],
        x[0] * y[1] - x[1] * y[0],
    )


def sqdist(x, y):
    z = vec_sub(x, y)
    return dot(z, z)


def distance_table(points):
    return {(i, j): sqdist(points[i], points[j])
            for i, j in combinations(range(len(points)), 2)}


def between(lower, middle, upper):
    return all(lower[pair] <= middle[pair] <= upper[pair] for pair in upper)


def leq(lower, upper):
    return all(lower[pair] <= upper[pair] for pair in upper)


def fixtures():
    core = ((0, 0, 0), (-1, 0, 0), (0, -1, 0), (0, 0, -1))
    yield (
        "two_independent_caps",
        core + ((1, -1, -1), (-1, 1, -1)),
        core + ((-1, -1, -1), (-1, -1, -1)),
    )

    source = (
        (0, 0, 0), (-1, -1, 0), (-1, 0, 1), (0, -1, 1),
        (1, -2, 5), (-2, -5, -1), (-5, 1, 2),
    )
    normals = ((1, 1, 1), (1, -1, -1), (-1, 1, -1))
    target = source[:4] + tuple(
        tuple(Fraction(x) - Fraction(8, 3) * n for x, n in zip(source[4 + i], normals[i]))
        for i in range(3)
    )
    yield "three_cyclic_caps", source, target

    simplex = tuple(v for v in product((-1, 1), repeat=3) if v[0] * v[1] * v[2] == 1)
    labels = tuple((i, j) for i in range(4) for j in range(4) if i != j)
    for depth in (1, 2):
        source = simplex + tuple(
            tuple(simplex[j][k] - depth * simplex[i][k] for k in range(3))
            for i, j in labels
        )
        target = simplex + tuple(
            tuple(simplex[j][k] + depth * simplex[i][k] for k in range(3))
            for i, j in labels
        )
        yield f"classical_flaps_depth_{depth}", source, target


def certify_binary_completeness(source, target):
    """Each moving point is the two-point intersection of three anchor spheres."""
    require(source[:4] == target[:4], "the first four labels must be fixed")
    root = source[:4]
    require(dot(cross(vec_sub(root[1], root[0]), vec_sub(root[2], root[0])),
                vec_sub(root[3], root[0])) != 0, "root tetrahedron is degenerate")

    anchor_sets = []
    for label in range(4, len(source)):
        anchors = tuple(
            i for i in range(4)
            if sqdist(source[label], root[i]) == sqdist(target[label], root[i])
        )
        require(len(anchors) == 3, "moving label does not have exactly three anchors")
        a, b, c = (root[i] for i in anchors)
        require(dot(cross(vec_sub(b, a), vec_sub(c, a)),
                    cross(vec_sub(b, a), vec_sub(c, a))) != 0,
                "anchor triple is collinear")
        require(source[label] != target[label], "reflection alternatives coincide")
        # Three non-collinear sphere equations cut out an affine line normal
        # to the anchor plane; a sphere intersects that line in at most two
        # points.  The two displayed endpoints realize both points.
        anchor_sets.append(anchors)
    return anchor_sets


def interval_fixture(name, source, target):
    anchor_sets = certify_binary_completeness(source, target)
    upper = distance_table(source)
    lower = distance_table(target)
    require(all(lower[p] <= upper[p] for p in upper), "endpoint is not a contraction")

    states = {}
    for bits in product((0, 1), repeat=len(source) - 4):
        points = source[:4] + tuple(
            (source, target)[bit][label]
            for label, bit in zip(range(4, len(source)), bits)
        )
        distances = distance_table(points)
        if between(lower, distances, upper):
            tag = "".join(str(bit) for bit in bits)
            states[tag] = distances

    require(len({tuple(table.items()) for table in states.values()}) == len(states),
            "distinct root-fixed placements have duplicate distance matrices")
    top = "0" * (len(source) - 4)
    bottom = "1" * (len(source) - 4)
    require(top in states and bottom in states, "an endpoint is absent")

    covers = []
    for high, high_table in states.items():
        for low, low_table in states.items():
            if high == low or not leq(low_table, high_table):
                continue
            intervenes = any(
                mid not in (high, low)
                and all(low_table[p] <= mid_table[p] <= high_table[p] for p in high_table)
                for mid, mid_table in states.items()
            )
            if not intervenes:
                covers.append((high, low))
    covers.sort()

    chains = []

    def extend(path):
        if path[-1] == bottom:
            chains.append(path)
            return
        for high, low in covers:
            if high == path[-1]:
                extend(path + [low])

    extend([top])
    require(chains, "no saturated endpoint chain")
    return {
        "name": name,
        "labels": len(source),
        "binary_candidates": 2 ** (len(source) - 4),
        "anchor_sets": [list(a) for a in anchor_sets],
        "interval_states": sorted(states),
        "cover_edges": [list(edge) for edge in covers],
        "saturated_chains": chains,
        "input_distinct": len(set(source)),
        "output_distinct": len(set(target)),
    }


def simplex_gram(i, j):
    return 3 if i == j else -1


def gram_difference(a, b, c, d):
    """(v_a-v_b).(v_c-v_d) for the four simplex vectors."""
    return simplex_gram(a, c) - simplex_gram(a, d) - simplex_gram(b, c) + simplex_gram(b, d)


def check_all_depth_flap_identities():
    flap_labels = tuple((i, j) for i in range(4) for j in range(4) if i != j)
    core_cases = 0
    for i, j in flap_labels:
        for k in range(4):
            coefficient = 4 * (simplex_gram(i, j) - simplex_gram(i, k))
            require(coefficient == (-16 if k == i else 0), "core/flap coefficient identity")
            core_cases += 1

    flap_pair_cases = 0
    for (i, j), (k, ell) in combinations(flap_labels, 2):
        coefficient = 4 * gram_difference(j, ell, i, k)
        expected = -16 * (int(j == k) + int(ell == i))
        require(coefficient == expected, "flap/flap coefficient identity")
        require(coefficient <= 0, "flap endpoint expansion has the wrong sign")
        flap_pair_cases += 1

    same_flap_pairs = sum(1 for (i, _), (k, _) in combinations(flap_labels, 2) if i == k)
    common_tip_cross_pairs = sum(
        1 for (i, j), (k, ell) in combinations(flap_labels, 2)
        if i != k and j == ell and j not in (i, k)
    )
    require(same_flap_pairs == 12, "same-flap synchronizing pairs")
    require(common_tip_cross_pairs == 12, "cross-flap synchronizing pairs")
    return {
        "core_flap_coefficient_cases": core_cases,
        "flap_pair_coefficient_cases": flap_pair_cases,
        "same_flap_pairs_forcing_one_sign_per_flap": same_flap_pairs,
        "common_tip_pairs_forcing_all_flap_signs_equal": common_tip_cross_pairs,
        "mixed_same_flap_extra_squared_distance_coefficient": 12,
        "opposite_cross_flap_squared_distance_coefficient": 4,
        "endpoint_cross_flap_squared_distance_coefficient": 8,
    }


def compute():
    records = [interval_fixture(*fixture) for fixture in fixtures()]
    require([len(record["interval_states"]) for record in records] == [4, 2, 2, 2],
            "unexpected interval sizes")
    require([len(record["saturated_chains"]) for record in records] == [2, 1, 1, 1],
            "unexpected chain counts")
    return {
        "scope": (
            "Definition-level exact fixture intervals and all-depth flap identities only; "
            "Brehm extension and the universal reduction remain written-proof obligations."
        ),
        "flap_identities": check_all_depth_flap_identities(),
        "fixtures": records,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true", help="print the recomputed JSON")
    args = parser.parse_args()
    rendered = json.dumps(compute(), indent=2, sort_keys=True) + "\n"
    if args.emit:
        print(rendered, end="")
        return
    expected = (HERE / "EXPECTED.json").read_text()
    require(rendered == expected, "EXPECTED.json does not match recomputation")
    print("PASS: independent interval counts 4,2,2,2 and saturated chains 2,1,1,1")
    print("PASS: exact all-depth simplex-flap coefficient and synchronization identities")


if __name__ == "__main__":
    main()
