#!/usr/bin/env python3
"""Produce the exact factor-action and orbit-representative certificate."""
from collections import Counter
from pathlib import Path
import argparse
import json
import sys

import sympy as sp

import verify as V


x, y = sp.symbols("x y")


def sympy_polynomial(polynomial):
    return sum(coefficient * x**i * y**j for (i, j), coefficient in polynomial.items())


def factor_ids(polynomial, lookup):
    expression = sympy_polynomial(polynomial)
    result = []
    for factor, exponent in sp.factor_list(expression, x, y)[1]:
        poly = sp.Poly(factor, x, y, domain=sp.QQ)
        encoded = {(i, j): int(coefficient) for (i, j), coefficient in poly.terms()}
        # Clear any rational denominator before canonical lookup.
        denominator, primitive = poly.clear_denoms(convert=True)
        encoded = {(i, j): int(coefficient) for (i, j), coefficient in primitive.terms()}
        target = lookup[V.canonical(encoded)]
        result.append((target, exponent))
    return result


def produce():
    source, factors, active, source_rows, cover = V.source_state()
    alignment = V.alignment_ids(factors)
    domain_ids = sorted(active - alignment)
    position = {factor_id: i for i, factor_id in enumerate(domain_ids)}
    safe = alignment | (set(range(len(factors))) - active)
    lookup = {V.canonical(factor): i for i, factor in enumerate(factors)}
    generator_names = ("swap", "conjugate", "rotate_x", "transpose_01")
    generators = {}
    permutations = []
    bad_sets = [set(row["bad"]) - alignment for row in source_rows]
    for name in generator_names:
        identities = []
        targets = []
        for factor_id in domain_ids:
            decomposition = factor_ids(V.transform(factors[factor_id], name), lookup)
            nonsafe = [(target, exponent) for target, exponent in decomposition if target not in safe]
            V.need(len(nonsafe) == 1 and nonsafe[0][1] == 1, name + " image factor")
            target = nonsafe[0][0]
            V.need(target in position, name + " image domain")
            extras = [[other, exponent] for other, exponent in decomposition if other in safe]
            identities.append({"target": target, "extras": extras})
            targets.append(position[target])
        permutation = tuple(targets)
        V.need(len(set(permutation)) == len(domain_ids), name + " permutation")
        permutations.append(permutation)
        word_map = []
        for bad in bad_sets:
            image = {domain_ids[permutation[position[factor_id]]] for factor_id in bad}
            matches = [i for i, target in enumerate(bad_sets) if target == image]
            V.need(len(matches) == 1, name + " word action")
            word_map.append(matches[0])
        generators[name] = {"identities": identities, "word_map": word_map}

    group = V.group_closure(permutations)
    temporary = {"factors": factors, "pair_orbit_representatives": []}
    primary = cover["primary_index"]
    protecting = {
        factor_id: min(
            (i for i, row in enumerate(source_rows) if factor_id not in row["bad"]),
            key=lambda i: (source_rows[i]["bad_degree_sum"], i),
        )
        for factor_id in sorted(source_rows[primary]["bad"])
    }
    selected = {
        tuple(sorted((position[factor_id], position[other])))
        for factor_id, word in protecting.items()
        for other in source_rows[word]["bad"]
        if factor_id in position and other in position
    }
    orbit_by_key = {}
    for pair in selected:
        orbit = {
            tuple(sorted((permutation[pair[0]], permutation[pair[1]])))
            for permutation in group
        }
        orbit_by_key.setdefault(min(orbit), orbit)
    bidegrees = [(max(i for i, _ in factors[f]), max(j for _, j in factors[f])) for f in domain_ids]
    total_degrees = [max(i + j for i, j in factors[f]) for f in domain_ids]

    def costs(pair):
        ax, ay = bidegrees[pair[0]]
        bx, by = bidegrees[pair[1]]
        return ax * by + ay * bx, total_degrees[pair[0]] * total_degrees[pair[1]], pair

    representatives = []
    for orbit in orbit_by_key.values():
        pair = min(orbit, key=costs)
        representatives.append(sorted((domain_ids[pair[0]], domain_ids[pair[1]])))
    representatives.sort()

    collision_representatives = [
        {"squared_norms": [1, 3, 3], "radicand": 33,
         "x_coefficients": ["-1/2", "1/6"], "y_coefficients": ["-1/2", "-1/6"]},
        {"squared_norms": [1, 4, 4], "radicand": 5,
         "x_coefficients": ["0", "1/3"], "y_coefficients": ["0", "-1/3"]},
        {"squared_norms": [3, 3, 4], "radicand": 6,
         "x_coefficients": ["0", "1/3"], "y_coefficients": ["1", "-2/3"]},
        {"squared_norms": [3, 4, 4], "radicand": 13,
         "x_coefficients": ["2/3", "1/3"], "y_coefficients": ["2/3", "-1/3"]},
    ]
    alignment_collision_types = [
        {"squared_norms": [1, 1, 1], "solutions": [["1", "-1"], ["-1", "1"]]},
        {"squared_norms": [1, 1, 3], "solutions": [["1/3", "inf"], ["-1/3", "1"]]},
        {"squared_norms": [1, 1, 4], "solutions": [["0", "inf"]]},
        {"squared_norms": [1, 3, 4], "solutions": [["1/3", "-1"], ["-1", "1"]]},
        {"squared_norms": [3, 3, 3], "solutions": [["1", "-1"], ["-1", "1"]]},
        {"squared_norms": [4, 4, 4], "solutions": [["1", "-1"], ["-1", "1"]]},
    ]
    certificate = {
        "schema": "hn-three-wheel-symmetry-frontier-v1",
        "source_certificate_sha256": V.SOURCE_CERTIFICATE_SHA256,
        "alignment_factor_ids": sorted(alignment),
        "nonalignment_factor_ids": domain_ids,
        "generators": generators,
        "pair_orbit_representatives": representatives,
        "alignment_collision_types": alignment_collision_types,
        "collision_orbit_representatives": collision_representatives,
    }
    return certificate


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    encoded = (json.dumps(produce(), separators=(",", ":"), sort_keys=True) + "\n").encode()
    (args.out / "certificate.json").write_bytes(encoded)
    print(json.dumps({"bytes": len(encoded), "certificate": str(args.out / "certificate.json")}, indent=2))
