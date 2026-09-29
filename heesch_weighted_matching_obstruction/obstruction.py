#!/usr/bin/env python3
"""Exact additive-charge classifier and conditional finite corona certificate."""

import argparse
import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path


class Incomplete(Exception):
    """A depth limit is operational, not a mathematical answer."""


def rational(value):
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise ValueError("rational inputs must be integers or fraction strings")
    return Fraction(value)


def validate(counts, pairs):
    if not isinstance(counts, dict) or not counts:
        raise ValueError("counts must be a nonempty object")
    if any(not isinstance(k, str) or not k for k in counts):
        raise ValueError("type names must be nonempty strings")
    if any(type(v) is not int or v < 0 for v in counts.values()):
        raise ValueError("port counts must be nonnegative integers")
    if not sum(counts.values()):
        raise ValueError("at least one port occurrence is required")
    if not isinstance(pairs, (list, tuple)):
        raise ValueError("pairs must be an array")
    for pair in pairs:
        if not isinstance(pair, (list, tuple)) or len(pair) != 2:
            raise ValueError("each pair must have two type names")
        if any(not isinstance(k, str) or k not in counts for k in pair):
            raise ValueError("every paired type must occur in counts")


def classify(counts, pairs):
    """Use connected-component parity, independent of the finite checker."""
    validate(counts, pairs)
    adjacency = {k: set() for k in counts}
    for x, y in pairs:
        adjacency[x].add(y)
        adjacency[y].add(x)
    colors = {}
    components = []
    for root in sorted(counts):
        if root in colors:
            continue
        colors[root] = 0
        queue = [root]
        members = []
        bipartite = True
        for x in queue:
            members.append(x)
            for y in sorted(adjacency[x]):
                if y not in colors:
                    colors[y] = 1 - colors[x]
                    queue.append(y)
                elif colors[y] == colors[x]:
                    bipartite = False
        component = {"types": sorted(members), "bipartite": bipartite}
        if bipartite:
            sides = [sorted(x for x in members if colors[x] == c) for c in (0, 1)]
            totals = [sum(counts[x] for x in side) for side in sides]
            if totals[0] < totals[1]:
                sides.reverse()
                totals.reverse()
            component.update(positive_types=sides[0], negative_types=sides[1],
                             positive_count=totals[0], negative_count=totals[1])
        components.append(component)
    imbalanced = [c for c in components if c["bipartite"]
                  and c["positive_count"] > c["negative_count"]]
    if not imbalanced:
        return {"status": "no_additive_charge", "components": components}
    zero_supply = [c for c in imbalanced if c["negative_count"] == 0]
    best = zero_supply[0] if zero_supply else max(
        imbalanced, key=lambda c: Fraction(c["positive_count"], c["negative_count"]))
    weights = {x: 0 for x in counts}
    for x in best["positive_types"]:
        weights[x] = 1
    for x in best["negative_types"]:
        weights[x] = -1
    return {"status": "additive_charge", "components": components,
            "positive_count": best["positive_count"],
            "negative_count": best["negative_count"],
            "optimal_ratio": "infinity" if zero_supply else str(Fraction(
                best["positive_count"], best["negative_count"])),
            "weights": weights}


def first_failure(p, q, geometry_ratio, max_depth):
    if type(p) is not int or type(q) is not int or not p > q >= 0:
        raise ValueError("the recurrence requires integer p > q >= 0")
    if type(max_depth) is not int or max_depth < 1:
        raise ValueError("max_depth must be positive")
    if geometry_ratio <= 0:
        raise ValueError("geometry ratio must be positive")
    coefficient = Fraction(22, 7) * geometry_ratio
    if coefficient < 1:
        raise ValueError("supplied geometry bounds exclude even one tile")
    if q == 0:
        return {"excluded_depth": 1, "heesch_upper_bound": 0,
                "reason": "a required type has no matching supply"}
    lower = 1
    for depth in range(1, max_depth + 1):
        lower = (p * lower + q - 1) // q
        capacity = int(coefficient * (depth + 1) ** 2)
        if lower > capacity:
            return {"excluded_depth": depth, "heesch_upper_bound": depth - 1,
                    "tile_count_lower": lower, "packing_capacity_upper": capacity}
    raise Incomplete(f"no depth certificate reached through depth {max_depth}")


def closed_certificate(p, q, geometry_ratio):
    if type(p) is not int or type(q) is not int or not p > q > 0:
        raise ValueError("the closed certificate requires integer p > q > 0")
    if geometry_ratio <= 0:
        raise ValueError("geometry ratio must be positive")
    coefficient = Fraction(22, 7) * geometry_ratio
    block_length = (q + (p - q) - 1) // (p - q)
    exact_capacity = coefficient * (block_length + 1) ** 2
    capacity = -(-exact_capacity.numerator // exact_capacity.denominator)
    s = max(8, capacity.bit_length())
    depth = 2 * block_length * s
    return {"block_length": block_length, "block_capacity_constant": capacity,
            "binary_exponent": s, "excluded_depth": depth,
            "heesch_upper_bound": depth - 1}


def solve(model, max_depth=10000):
    if not isinstance(model, dict):
        raise ValueError("model must be an object")
    result = classify(model["counts"], model["pairs"])
    area = rational(model["area_lower"])
    diameter_squared = rational(model["diameter_squared_upper"])
    if area <= 0 or diameter_squared <= 0:
        raise ValueError("geometry bounds must be positive")
    if Fraction(22, 7) * diameter_squared / area < 1:
        raise ValueError("supplied geometry bounds exclude even one tile")
    result["geometry_ratio_upper"] = str(diameter_squared / area)
    if result["status"] == "additive_charge":
        p, q = result["positive_count"], result["negative_count"]
        if q:
            result["closed_certificate"] = closed_certificate(
                p, q, diameter_squared / area)
        try:
            result["depth_certificate"] = first_failure(
                p, q, diameter_squared / area, max_depth)
            result["refinement_status"] = "complete"
        except Incomplete as error:
            result["refinement_status"] = "incomplete"
            result["refinement_reason"] = str(error)
    return result


EXAMPLES = {
    "marked_hexagon_counts": {
        "counts": {"nick": 3, "bump": 2, "flat": 1},
        "pairs": [["nick", "bump"], ["flat", "flat"]],
        "area_lower": "5/2", "diameter_squared_upper": 4},
    "balanced_total_two_colors": {
        "counts": {"a_plus": 3, "a_minus": 2, "b_plus": 2, "b_minus": 3},
        "pairs": [["a_plus", "a_minus"], ["b_plus", "b_minus"]],
        "area_lower": 1, "diameter_squared_upper": 2},
    "odd_cycle": {
        "counts": {"a": 3, "b": 2, "c": 1},
        "pairs": [["a", "b"], ["b", "c"], ["c", "a"]],
        "area_lower": 1, "diameter_squared_upper": 2},
    "balanced_component": {
        "counts": {"a": 2, "b": 2}, "pairs": [["a", "b"]],
        "area_lower": 1, "diameter_squared_upper": 2},
    "missing_supply": {
        "counts": {"a": 1, "b": 0}, "pairs": [["a", "b"]],
        "area_lower": 1, "diameter_squared_upper": 2},
}


def direct_optimum(counts, pairs):
    """Independent small-instance check: enumerate weights, no graph parity."""
    labels = sorted(counts)
    optimum = None
    for values in itertools.product(range(-2, 3), repeat=len(labels)):
        weights = dict(zip(labels, values))
        if any(weights[x] + weights[y] for x, y in pairs):
            continue
        positive = sum(counts[x] * max(weights[x], 0) for x in labels)
        negative = sum(counts[x] * max(-weights[x], 0) for x in labels)
        if positive <= negative:
            continue
        if not negative:
            return "infinity"
        ratio = Fraction(positive, negative)
        if optimum is None or ratio > optimum:
            optimum = ratio
    return None if optimum is None else str(optimum)


def self_check():
    tested = 0
    for order in range(1, 4):
        labels = [str(i) for i in range(order)]
        possible_pairs = list(itertools.combinations_with_replacement(labels, 2))
        for bits in range(1 << len(possible_pairs)):
            pairs = [pair for i, pair in enumerate(possible_pairs) if bits >> i & 1]
            for values in itertools.product(range(3), repeat=order):
                if not sum(values):
                    continue
                counts = dict(zip(labels, values))
                result = classify(counts, pairs)
                actual = result.get("optimal_ratio")
                reference = direct_optimum(counts, pairs)
                if actual != reference:
                    raise AssertionError((counts, pairs, actual, reference))
                tested += 1
    assert tested == 1732
    assert first_failure(3, 2, Fraction(8, 5), 100) == {
        "excluded_depth": 18, "heesch_upper_bound": 17,
        "tile_count_lower": 2397, "packing_capacity_upper": 1815}
    # Fraction recurrence checks use its definition, rather than ceiling division.
    for p in range(2, 12):
        for q in range(1, p):
            lower = 1
            for _ in range(20):
                exact = Fraction(p * lower, q)
                candidate = (p * lower + q - 1) // q
                assert candidate - 1 < exact <= candidate
                lower = candidate
            # Direct rational powers check the closed formula on small instances.
            for geometry in (Fraction(1), Fraction(8, 5), Fraction(12)):
                certificate = closed_certificate(p, q, geometry)
                depth = certificate["excluded_depth"]
                assert Fraction(p, q) ** depth > Fraction(22, 7) * geometry * (depth + 1) ** 2
    try:
        first_failure(3, 2, Fraction(2), 1)
    except Incomplete:
        pass
    else:
        raise AssertionError("depth cutoff must report incomplete")
    limited = solve(EXAMPLES["marked_hexagon_counts"], max_depth=1)
    assert limited["refinement_status"] == "incomplete"
    assert limited["closed_certificate"]["heesch_upper_bound"] == 31
    invalid_models = [
        {"counts": {"a": -1}, "pairs": []},
        {"counts": {"a": True}, "pairs": []},
        {"counts": {"a": 0}, "pairs": []},
        {"counts": {"a": 1}, "pairs": [["a", "missing"]]},
        {"counts": {"a": 1}, "pairs": [["a"]]},
    ]
    for model in invalid_models:
        try:
            classify(model["counts"], model["pairs"])
        except ValueError:
            pass
        else:
            raise AssertionError("malformed model was accepted")
    try:
        rational(0.5)
    except ValueError:
        pass
    else:
        raise AssertionError("binary floating-point input was accepted")
    return {"status": "passed", "independent_models_checked": tested,
            "recurrence_and_rejection_checks": "passed"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["examples", "self-check", "solve"])
    parser.add_argument("model", nargs="?")
    parser.add_argument("--max-depth", type=int, default=10000)
    args = parser.parse_args()
    try:
        if args.command == "examples":
            result = {name: solve(model, args.max_depth) for name, model in EXAMPLES.items()}
        elif args.command == "self-check":
            result = self_check()
        else:
            if not args.model:
                parser.error("solve requires a model JSON file")
            result = solve(json.loads(Path(args.model).read_text()), args.max_depth)
    except Incomplete as error:
        print(json.dumps({"status": "incomplete", "reason": str(error)}, sort_keys=True))
        return 2
    except (ValueError, KeyError, TypeError, ZeroDivisionError) as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
