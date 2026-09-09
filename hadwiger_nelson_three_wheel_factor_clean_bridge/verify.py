#!/usr/bin/env python3
"""Exact standard-library verifier for the three-wheel residual bridge."""
from collections import Counter
from fractions import Fraction as Q
from functools import reduce
from itertools import combinations
from math import gcd, lcm
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

import inputs


HERE = Path(__file__).resolve().parent


# Dense univariate polynomials, constant coefficient first.
def trim(poly):
    poly = list(poly)
    while poly and poly[-1] == 0:
        poly.pop()
    return poly


def add(left, right, scale=Q(1)):
    out = [Q(0)] * max(len(left), len(right))
    for i, value in enumerate(left):
        out[i] += value
    for i, value in enumerate(right):
        out[i] += scale * value
    return trim(out)


def multiply(left, right):
    if not left or not right:
        return []
    out = [Q(0)] * (len(left) + len(right) - 1)
    for i, value in enumerate(left):
        for j, other in enumerate(right):
            out[i + j] += value * other
    return trim(out)


def scale(poly, coefficient):
    return trim([coefficient * value for value in poly])


def divide(dividend, divisor):
    inputs.need(divisor, "nonzero polynomial divisor")
    remainder = list(dividend)
    quotient = [Q(0)] * max(0, len(dividend) - len(divisor) + 1)
    while len(remainder) >= len(divisor):
        offset = len(remainder) - len(divisor)
        coefficient = remainder[-1] / divisor[-1]
        quotient[offset] += coefficient
        for i, value in enumerate(divisor):
            remainder[i + offset] -= coefficient * value
        remainder = trim(remainder)
    return trim(quotient), remainder


def monic(poly):
    inputs.need(poly, "nonzero monic polynomial")
    return scale(poly, Q(1) / poly[-1])


def polynomial_gcd(left, right):
    left, right = trim(left), trim(right)
    while right:
        _, remainder = divide(left, right)
        left, right = right, remainder
    return monic(left) if left else []


def extended_gcd(left, right):
    old_r, current_r = list(left), list(right)
    old_s, current_s = [Q(1)], []
    old_t, current_t = [], [Q(1)]
    while current_r:
        quotient, remainder = divide(old_r, current_r)
        old_r, current_r = current_r, remainder
        old_s, current_s = current_s, add(old_s, multiply(quotient, current_s), Q(-1))
        old_t, current_t = current_t, add(old_t, multiply(quotient, current_t), Q(-1))
    coefficient = Q(1) / old_r[-1]
    return scale(old_r, coefficient), scale(old_s, coefficient), scale(old_t, coefficient)


def reduce_mod(poly, modulus):
    return divide(poly, modulus)[1]


def quotient_add(left, right, modulus, coefficient=Q(1)):
    return reduce_mod(add(left, right, coefficient), modulus)


def quotient_multiply(left, right, modulus):
    return reduce_mod(multiply(left, right), modulus)


def quotient_inverse(poly, modulus):
    common, inverse, _ = extended_gcd(poly, modulus)
    inputs.need(common == [Q(1)], "invertible shape coefficient")
    answer = reduce_mod(inverse, modulus)
    inputs.need(quotient_multiply(poly, answer, modulus) == [Q(1)],
                "checked shape inverse")
    return answer


def primitive_integers(poly):
    poly = trim(poly)
    inputs.need(poly, "nonzero primitive polynomial")
    denominator = reduce(lcm, (Q(value).denominator for value in poly), 1)
    integers = [int(Q(value) * denominator) for value in poly]
    common = reduce(gcd, (abs(value) for value in integers))
    integers = [value // common for value in integers]
    if integers[-1] < 0:
        integers = [-value for value in integers]
    return integers


def quotient_value(factor, xvalue, yvalue, modulus):
    xpowers = [[Q(1)], xvalue, quotient_multiply(xvalue, xvalue, modulus)]
    ypowers = [[Q(1)], yvalue, quotient_multiply(yvalue, yvalue, modulus)]
    value = []
    for (xdegree, ydegree), coefficient in factor.items():
        term = quotient_multiply(xpowers[xdegree], ypowers[ydegree], modulus)
        value = quotient_add(value, term, modulus, Q(coefficient))
    return value


def sha256_json(value):
    return hashlib.sha256(json.dumps(value, separators=(",", ":")).encode()).hexdigest()


def minimum_covers(good_sets, word_count):
    full = (1 << len(good_sets)) - 1
    masks = []
    for word_index in range(word_count):
        mask = 0
        for component_index, good in enumerate(good_sets):
            if word_index in good:
                mask |= 1 << component_index
        masks.append(mask)
    for size in range(1, word_count + 1):
        covers = []
        for choice in combinations(range(word_count), size):
            mask = 0
            for word_index in choice:
                mask |= masks[word_index]
            if mask == full:
                covers.append(list(choice))
        if covers:
            return size, covers
    raise ValueError("finite word family has no component cover")


def compute():
    state = inputs.load()
    factor_stream = hashlib.sha256()
    rows = []
    good_sets = []
    edge_sets = set()
    degree_histogram = Counter()
    edge_counts = []

    for survivor in state["survivors"]:
        pair_index = survivor["pair_index"]
        factor_pair = survivor["factor_pair"]
        modulus = monic([Q(value) for value in survivor["polynomial"]])
        relation_a = [Q(value) for value in survivor["relation_a"]]
        relation_b = [Q(value) for value in survivor["relation_b"]]
        inverse = quotient_inverse(relation_a, modulus)
        yvalue = quotient_multiply(scale(relation_b, Q(-1)), inverse, modulus)
        xvalue = quotient_add([Q(0), Q(1)], yvalue, modulus,
                              Q(-survivor["shear"]))

        nonunits = []
        zero_factors = []
        for factor_id in state["allowed"]:
            value = quotient_value(state["factors"][factor_id], xvalue, yvalue, modulus)
            common = polynomial_gcd(modulus, value)
            if len(common) > 1:
                nonunits.append(factor_id)
            if not value:
                zero_factors.append(factor_id)
            factor_stream.update((json.dumps(
                [pair_index, factor_id, primitive_integers(common)],
                separators=(",", ":")) + "\n").encode())
        inputs.need(nonunits == factor_pair,
                    "the only nonunit event factors are the defining pair")
        inputs.need(zero_factors == factor_pair,
                    "the defining pair vanishes identically")

        proper_words = [word_index for word_index, bad in enumerate(state["bad_sets"])
                        if bad.isdisjoint(factor_pair)]
        inputs.need(all(word_index >= 13 for word_index in proper_words),
                    "all original thirteen words fail on each survivor")
        good_sets.append(set(proper_words))

        edges = inputs.graph_edges(state["base"], state["inventory"], factor_pair)
        edge_sha256 = sha256_json(edges)
        edge_key = tuple(map(tuple, edges))
        inputs.need(edge_key not in edge_sets, "distinct labelled residual graphs")
        edge_sets.add(edge_key)
        edge_counts.append(len(edges))
        degrees = Counter()
        for left, right in edges:
            degrees[left] += 1
            degrees[right] += 1
        inputs.need(len(degrees) == 343, "every graph retains all 343 labels")
        histogram = {str(key): value for key, value in sorted(Counter(degrees.values()).items())}
        degree_histogram[len(modulus) - 1] += 1
        rows.append({
            "pair_index": pair_index,
            "factor_pair": factor_pair,
            "field_degree": len(modulus) - 1,
            "real_embeddings": len(survivor["real_intervals"]),
            "nonunit_factor_ids": nonunits,
            "zero_factor_ids": zero_factors,
            "proper_h4085_word_indices": proper_words,
            "unit_edge_count": len(edges),
            "unit_edge_sha256": edge_sha256,
            "degree_histogram": histogram,
        })

    minimum_size, covers = minimum_covers(good_sets, len(state["words"]))
    canonical_cover = covers[0]
    assignment = []
    assignment_components = Counter()
    assignment_embeddings = Counter()
    for row, good in zip(rows, good_sets):
        word_index = next(word for word in canonical_cover if word in good)
        assignment.append({"pair_index": row["pair_index"], "word_index": word_index})
        assignment_components[word_index] += 1
        assignment_embeddings[word_index] += row["real_embeddings"]

    certificate = {
        "schema": "hn-three-wheel-factor-clean-bridge-v1",
        "dependencies": state["dependencies"],
        "factor_domain_size": len(state["allowed"]),
        "factor_gcd_checks": len(rows) * len(state["allowed"]),
        "factor_gcd_stream_sha256": factor_stream.hexdigest(),
        "rows": rows,
        "minimum_component_uniform_word_cover_size": minimum_size,
        "minimum_component_uniform_word_covers": covers,
        "canonical_cover": canonical_cover,
        "canonical_assignment": assignment,
    }
    result = {
        "status": "RESIDUAL_FIELDS_ARE_FACTOR_CLEAN_AND_FOUR_WORDS_CLOSE_THE_INTERFACE",
        "record_improvement": False,
        "residual_field_components": len(rows),
        "residual_real_embeddings": sum(row["real_embeddings"] for row in rows),
        "constant_labelled_unit_graphs": len(edge_sets),
        "factor_domain_size": len(state["allowed"]),
        "factor_gcd_checks": len(rows) * len(state["allowed"]),
        "factor_gcd_stream_sha256": factor_stream.hexdigest(),
        "nonunit_factors_per_component": 2,
        "field_degree_histogram": {str(key): value for key, value in sorted(degree_histogram.items())},
        "unit_edge_count_range": [min(edge_counts), max(edge_counts)],
        "h4085_colour_words": len(state["words"]),
        "original_words": 13,
        "added_words": len(state["words"]) - 13,
        "added_words_useful_on_a_residual_component": len(set().union(*good_sets)),
        "minimum_component_uniform_word_cover_size": minimum_size,
        "minimum_component_uniform_word_cover_count": len(covers),
        "minimum_component_uniform_word_covers": covers,
        "canonical_cover": canonical_cover,
        "canonical_assignment_component_counts": {
            str(key): value for key, value in sorted(assignment_components.items())},
        "canonical_assignment_embedding_counts": {
            str(key): value for key, value in sorted(assignment_embeddings.items())},
        "remaining_three_wheel_candidate_classes": 0,
        "chromatic_solver_calls": 0,
        "new_colour_word_search": False,
        "external_reviewer_acceptance_claimed": False,
    }
    return certificate, result


def check_certificate(certificate, expected):
    inputs.need(certificate == expected, "exact factor-clean bridge certificate")


def replay_viability_dependency():
    command = [sys.executable, "-B", str(inputs.VIABILITY / "verify.py"),
               "--check-expected"]
    completed = subprocess.run(command, check=True, text=True, capture_output=True)
    output = json.loads(completed.stdout)
    inputs.need(output.get("survivor_field_interface_sha256")
                == inputs.SURVIVOR_INTERFACE_SHA256,
                "full viability replay survivor interface")
    inputs.need(output.get("injective_all_thirteen_failure_field_components") == 15
                and output.get("injective_all_thirteen_failure_real_embeddings") == 48,
                "full viability replay survivor counts")


def run(certificate_path, full_dependency_replay=False):
    if full_dependency_replay:
        replay_viability_dependency()
    expected, result = compute()
    certificate_bytes = certificate_path.read_bytes()
    certificate = json.loads(certificate_bytes)
    check_certificate(certificate, expected)
    result["certificate_bytes"] = len(certificate_bytes)
    result["certificate_sha256"] = hashlib.sha256(certificate_bytes).hexdigest()
    result["full_viability_dependency_replay_performed"] = full_dependency_replay
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--check-expected", action="store_true")
    parser.add_argument("--full-dependency-replay", action="store_true")
    args = parser.parse_args()
    output = run(args.certificate, args.full_dependency_replay)
    if args.check_expected:
        expected_output = json.loads((HERE / "EXPECTED.json").read_text())
        # The expensive dependency replay is an optional precondition and does
        # not change the bridge result recorded in EXPECTED.json.
        expected_output["full_viability_dependency_replay_performed"] = args.full_dependency_replay
        inputs.need(output == expected_output, "expected verifier result")
    print(json.dumps(output, indent=2, sort_keys=True))
