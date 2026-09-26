#!/usr/bin/env python3
"""Independent exact stress audit for the rational-frontier producer.

This script does not import the submitted producer or its expected output.
It implements the published merge/expand/round construction with separate
data structures and exact Fraction arithmetic, then exercises a deterministic
family of contractions, rotations, merge patterns, and weight-simplex faces.
The finite stress run is implementation evidence, not the universal proof.
"""

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
from math import comb
from pathlib import Path
import argparse
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def vsub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def norm_squared(a):
    return sum(x*x for x in a)


def nearest_integer(x):
    """A deterministic nearest integer, with half-grid ties rounded upward."""
    n = x.numerator // x.denominator
    return n if x-Q(n) < Q(1, 2) else n+1


def compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for first in range(total+1):
        for rest in compositions(total-first, parts-1):
            yield (first,)+rest


def validate_input(k, source, target, weights):
    require(isinstance(k, int) and k >= 1, "invalid k")
    require(len(source) == len(target) == len(weights), "label mismatch")
    require(1 <= len(source) <= k**6, "atom budget")
    require(source[0] == target[0] == (Q(0), Q(0), Q(0)), "anchor")
    require(all(len(p) == 3 for p in source+target), "dimension")
    require(all(norm_squared(p) <= 4*k*k for p in source+target), "radius")
    require(all(w >= 0 for w in weights) and sum(weights) == 1, "weights")
    for i, j in combinations(range(len(source)), 2):
        require(norm_squared(vsub(target[i], target[j])) <=
                norm_squared(vsub(source[i], source[j])), "not a contraction")


def independent_producer(k, source, target, weights):
    source = [tuple(map(Q, p)) for p in source]
    target = [tuple(map(Q, p)) for p in target]
    weights = list(map(Q, weights))
    validate_input(k, source, target, weights)

    coordinate_denominator = 256*k**3
    weight_denominator = 4*k**7
    merge_radius = Q(1, 4*k)
    expansion = 1+Q(1, 8*k*k)

    representatives = [0]
    for label in range(1, len(source)):
        separated = all(norm_squared(vsub(source[label], source[r])) >
                        merge_radius**2 for r in representatives)
        if separated:
            representatives.append(label)

    assignment = []
    for label in range(len(source)):
        choices = [slot for slot, r in enumerate(representatives)
                   if norm_squared(vsub(source[label], source[r])) <=
                   merge_radius**2]
        require(choices, "greedy cover failure")
        assignment.append(choices[0])

    merged_weights = [Q(0) for _ in representatives]
    for label, slot in enumerate(assignment):
        merged_weights[slot] += weights[label]
        r = representatives[slot]
        require(norm_squared(vsub(target[label], target[r])) <=
                merge_radius**2, "image merge bound")

    source_integer = []
    target_integer = []
    for r in representatives:
        source_integer.append(tuple(nearest_integer(
            coordinate_denominator*expansion*x) for x in source[r]))
        target_integer.append(tuple(nearest_integer(
            coordinate_denominator*y) for y in target[r]))

    weight_integer = [(weight_denominator*w).numerator //
                      (weight_denominator*w).denominator
                      for w in merged_weights]
    missing = weight_denominator-sum(weight_integer)
    remainders = [weight_denominator*w-n for w, n in
                  zip(merged_weights, weight_integer)]
    order = sorted(range(len(representatives)),
                   key=lambda i: (-remainders[i], i))
    require(0 <= missing < len(representatives), "remainder allocation")
    for i in order[:missing]:
        weight_integer[i] += 1

    # Independently recheck every output-contract inequality.
    radius_limit = (3*k*coordinate_denominator)**2
    require(all(norm_squared(p) <= radius_limit
                for p in source_integer+target_integer), "output radius")
    require(source_integer[0] == target_integer[0] == (0, 0, 0),
            "rounded anchor")
    require(sum(weight_integer) == weight_denominator and
            all(isinstance(n, int) and n >= 0 for n in weight_integer),
            "integer weights")

    losses = []
    expected_loss = Q(0)
    for i, j in combinations(range(len(representatives)), 2):
        loss = (norm_squared(vsub(source_integer[i], source_integer[j]))-
                norm_squared(vsub(target_integer[i], target_integer[j])))
        require(loss >= 256*k*k, "integer contraction margin")
        losses.append(loss)
        expected_loss += Q(2*weight_integer[i]*weight_integer[j]*loss,
                           weight_denominator**2*coordinate_denominator**2)

    positive_weights = sum(n > 0 for n in weight_integer)
    if positive_weights >= 2:
        require(expected_loss >= Q(1, 2048*k**18), "pair-loss floor")
    else:
        require(expected_loss == 0, "point-law loss")

    weight_error = sum(abs(w-Q(n, weight_denominator))
                       for w, n in zip(merged_weights, weight_integer))
    require(weight_error <= Q(len(representatives), weight_denominator)
            <= Q(1, 4*k), "weight approximation")

    # Recheck the proof-level bounds rather than estimating a hinge integral.
    require(2*merge_radius+2*k*(expansion-1)+Q(2, coordinate_denominator)
            == Q(3, 4*k)+Q(1, 128*k**3), "geometric budget identity")
    require(Q(5, 8*k)+Q(1, 256*k**3) <= Q(161, 256*k),
            "hinge-transfer envelope")

    return {
        "source_integer": source_integer,
        "target_integer": target_integer,
        "weight_integer": weight_integer,
        "representatives": representatives,
        "assignment": assignment,
        "weight_error": str(weight_error),
        "minimum_margin": min(losses) if losses else None,
        "expected_loss": str(expected_loss),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    k = 2
    values = tuple(Q(a, 16) for a in (-5, -3, -1, 1, 3, 5))
    scales = (Q(0), Q(1, 3), Q(1))
    rotations = ((Q(1), Q(0)), (Q(3, 5), Q(4, 5)))
    weight_vectors = tuple(tuple(Q(n, 4) for n in ns)
                           for ns in compositions(4, 4))

    stream = sha256()
    cases = 0
    merged_cases = 0
    zero_weight_cases = 0
    point_output_cases = 0
    minimum_margin = None
    maximum_weight_error = Q(0)
    for chosen in combinations(values, 3):
        source = [(Q(0), Q(0), Q(0))]+[(x, Q(0), Q(0)) for x in chosen]
        for scale in scales:
            for cosine, sine in rotations:
                target = [(scale*cosine*x, scale*sine*x, Q(0))
                          for x, _, _ in source]
                for weights in weight_vectors:
                    out = independent_producer(k, source, target, weights)
                    cases += 1
                    merged_cases += len(out["representatives"]) < len(source)
                    zero_weight_cases += any(w == 0 for w in weights)
                    point_output_cases += sum(n > 0 for n in out["weight_integer"]) == 1
                    maximum_weight_error = max(maximum_weight_error,
                                               Q(out["weight_error"]))
                    if out["minimum_margin"] is not None:
                        minimum_margin = (out["minimum_margin"] if minimum_margin is None
                                          else min(minimum_margin, out["minimum_margin"]))
                    stream.update((json.dumps(out, sort_keys=True,
                                              separators=(",", ":"))+"\n").encode())

    # Duplicate-source and near-collision controls outside the regular grid.
    rotation = lambda x: (Q(3, 5)*x, Q(4, 5)*x, Q(0))
    specials = [
        ([(0, 0, 0), (0, 0, 0), (Q(1, 4096), 0, 0), (Q(1, 4), 0, 0)],
         [(0, 0, 0), (0, 0, 0), rotation(Q(1, 4096)), rotation(Q(1, 4))],
         (Q(0), Q(1, 7), Q(2, 7), Q(4, 7))),
        ([(0, 0, 0), (Q(1, 8), 0, 0), (Q(1, 8), 0, 0)],
         [(0, 0, 0), (0, 0, 0), (0, 0, 0)],
         (Q(1, 3), Q(1, 3), Q(1, 3))),
        ([(0, 0, 0), (Q(1, 2), 0, 0), (0, Q(1, 2), 0),
          (0, 0, Q(1, 2))],
         [(0, 0, 0), (Q(1, 4), 0, 0), (0, Q(1, 4), 0),
          (0, 0, Q(1, 4))],
         (Q(1, 4), Q(1, 4), Q(1, 4), Q(1, 4))),
    ]
    for source, target, weights in specials:
        out = independent_producer(k, source, target, weights)
        cases += 1
        merged_cases += len(out["representatives"]) < len(source)
        zero_weight_cases += any(w == 0 for w in weights)
        point_output_cases += sum(n > 0 for n in out["weight_integer"]) == 1
        maximum_weight_error = max(maximum_weight_error, Q(out["weight_error"]))
        if out["minimum_margin"] is not None:
            minimum_margin = min(minimum_margin, out["minimum_margin"])
        stream.update((json.dumps(out, sort_keys=True,
                                  separators=(",", ":"))+"\n").encode())

    budget_checks = 0
    for t in range(1, 65):
        require(Q(14, 3*t)+Q(161, 256*t) == Q(4067, 768*t)
                < Q(16, 3*t), "global error composition")
        require((1536*t**4+1)**6*(4*t**7+1) <= 2**69*t**31,
                "configuration-count base")
        require(Q(2, (4*t**7)**2*256*t**4) == Q(1, 2048*t**18),
                "pair-loss constant")
        budget_checks += 3

    coefficient_checks = 0
    for degree in range(33):
        for j in range(degree+1):
            exact_norm = (2*(degree+1)*comb(degree, j)*sum(
                (Q(comb(degree-j, ell), (j+ell+1)*(j+ell+2))
                 for ell in range(degree-j+1)), Q(0)))
            require(exact_norm <= (degree+1)*3**degree,
                    "moment amplification")
            coefficient_checks += 1

    result = {
        "status": "INDEPENDENT_RATIONAL_FRONTIER_STRESS_PASS",
        "imports_submitted_code_or_expected_output": False,
        "stress_cases": cases,
        "cases_with_source_merging": merged_cases,
        "cases_with_zero_input_weights": zero_weight_cases,
        "point_law_outputs": point_output_cases,
        "minimum_integer_pair_margin": minimum_margin,
        "maximum_weight_l1_error": str(maximum_weight_error),
        "budget_identity_checks": budget_checks,
        "coefficient_norm_checks": coefficient_checks,
        "output_stream_sha256": stream.hexdigest(),
    }
    encoded = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.check:
        expected = Path(__file__).with_name("EXPECTED.json").read_text()
        require(encoded == expected, "review expected-output mismatch")
    print(encoded, end="")


if __name__ == "__main__":
    main()
