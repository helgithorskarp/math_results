#!/usr/bin/env python3
"""SymPy producer for the factor-clean residual bridge certificate."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import platform
import time

import sympy as sp

import inputs


t = sp.symbols("t")


def polynomial(values):
    return sp.Poly(sum(sp.Rational(value) * t**i for i, value in enumerate(values)),
                   t, domain=sp.QQ)


def primitive_integers(poly):
    _, integral = sp.Poly(poly, t, domain=sp.QQ).clear_denoms(convert=True)
    _, integral = integral.primitive()
    if integral.LC() < 0:
        integral = -integral
    return [int(integral.nth(i)) for i in range(integral.degree() + 1)]


def factor_value(factor, xvalue, yvalue, modulus):
    expression = sum(sp.Rational(coefficient) * xvalue.as_expr()**i * yvalue.as_expr()**j
                     for (i, j), coefficient in factor.items())
    return sp.rem(sp.Poly(expression, t, domain=sp.QQ), modulus)


def sha256_json(value):
    return hashlib.sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def minimum_covers(good_sets, word_count):
    universe = set(range(len(good_sets)))
    coverage = [{index for index, good in enumerate(good_sets) if word in good}
                for word in range(word_count)]
    for size in range(1, word_count + 1):
        covers = [list(choice) for choice in combinations(range(word_count), size)
                  if set().union(*(coverage[word] for word in choice)) == universe]
        if covers:
            return size, covers
    raise ValueError("no finite word cover")


def produce():
    state = inputs.load()
    stream = hashlib.sha256()
    rows = []
    good_sets = []
    edge_sets = set()
    for survivor in state["survivors"]:
        modulus = polynomial(survivor["polynomial"]).monic()
        relation_a = polynomial(survivor["relation_a"])
        relation_b = polynomial(survivor["relation_b"])
        inverse = sp.invert(relation_a, modulus)
        yvalue = sp.rem(-relation_b * inverse, modulus)
        xvalue = sp.rem(sp.Poly(t, t, domain=sp.QQ) - survivor["shear"] * yvalue,
                            modulus)
        nonunits = []
        zero_factors = []
        for factor_id in state["allowed"]:
            value = factor_value(state["factors"][factor_id], xvalue, yvalue, modulus)
            common = sp.gcd(modulus, value).monic()
            if common.degree() > 0:
                nonunits.append(factor_id)
            if value.is_zero:
                zero_factors.append(factor_id)
            stream.update((json.dumps(
                [survivor["pair_index"], factor_id, primitive_integers(common)],
                separators=(",", ":")) + "\n").encode())
        inputs.need(nonunits == survivor["factor_pair"], "factor-clean producer result")
        inputs.need(zero_factors == survivor["factor_pair"], "defining factors vanish")
        proper = [index for index, bad in enumerate(state["bad_sets"])
                  if bad.isdisjoint(nonunits)]
        good_sets.append(set(proper))
        edges = inputs.graph_edges(state["base"], state["inventory"], nonunits)
        edge_key = tuple(map(tuple, edges))
        inputs.need(edge_key not in edge_sets, "distinct labelled producer graphs")
        edge_sets.add(edge_key)
        degrees = Counter()
        for left, right in edges:
            degrees[left] += 1
            degrees[right] += 1
        rows.append({
            "pair_index": survivor["pair_index"],
            "factor_pair": survivor["factor_pair"],
            "field_degree": modulus.degree(),
            "real_embeddings": len(survivor["real_intervals"]),
            "nonunit_factor_ids": nonunits,
            "zero_factor_ids": zero_factors,
            "proper_h4085_word_indices": proper,
            "unit_edge_count": len(edges),
            "unit_edge_sha256": sha256_json(edges),
            "degree_histogram": {
                str(key): value for key, value in sorted(Counter(degrees.values()).items())},
        })
    size, covers = minimum_covers(good_sets, len(state["words"]))
    canonical = covers[0]
    assignment = [{"pair_index": row["pair_index"],
                   "word_index": next(word for word in canonical if word in good)}
                  for row, good in zip(rows, good_sets)]
    return {
        "schema": "hn-three-wheel-factor-clean-bridge-v1",
        "dependencies": state["dependencies"],
        "factor_domain_size": len(state["allowed"]),
        "factor_gcd_checks": len(rows) * len(state["allowed"]),
        "factor_gcd_stream_sha256": stream.hexdigest(),
        "rows": rows,
        "minimum_component_uniform_word_cover_size": size,
        "minimum_component_uniform_word_covers": covers,
        "canonical_cover": canonical,
        "canonical_assignment": assignment,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    start = time.monotonic()
    certificate = produce()
    encoded = (json.dumps(certificate, separators=(",", ":"), sort_keys=True) + "\n").encode()
    args.output.write_bytes(encoded)
    print(json.dumps({
        "python": platform.python_version(),
        "sympy": sp.__version__,
        "certificate_bytes": len(encoded),
        "certificate_sha256": hashlib.sha256(encoded).hexdigest(),
        "factor_gcd_checks": certificate["factor_gcd_checks"],
        "elapsed_seconds": time.monotonic() - start,
    }, indent=2, sort_keys=True))
