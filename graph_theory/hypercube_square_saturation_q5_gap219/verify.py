#!/usr/bin/env python3
"""Compact exact verifier for unattainability of Q5 facet deficit 218."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
PARENT = HERE.parent / "hypercube_square_saturation_q5_gap218"
TARGET = 218
EXPECTED_PROFILE_HASH = "9dc4c10874d87acd730ab6fb0741b23da45c13a4d01ba29149dcc11e8f4aefbb"


def live_capacity_maxima():
    """Maximum Q5 edges supported on exactly a prescribed set of live facets."""

    facets = tuple((coordinate, bit) for coordinate in range(5) for bit in (0, 1))
    edge_supports = []
    for direction in range(5):
        for vertex in range(32):
            if (vertex >> direction) & 1:
                continue
            edge_supports.append(frozenset(
                (coordinate, (vertex >> coordinate) & 1)
                for coordinate in range(5)
                if coordinate != direction
            ))
    result = []
    for live_count in range(1, 11):
        result.append(max(
            sum(support <= frozenset(live) for support in edge_supports)
            for live in combinations(facets, live_count)
        ))
    return result


def smaller_deficit_profiles(classes, capacities):
    """Necessary global profiles made only from positive deficits below 218."""

    survivors = set()

    def visit(start, chosen, total):
        if chosen and total == TARGET:
            positive_count = len(chosen)
            positive_edges = sum(item[1] for item in chosen)
            for equality_count in range(11 - positive_count):
                empty_count = 10 - positive_count - equality_count
                incidence = positive_edges + 17 * equality_count
                if incidence % 4:
                    continue
                global_edges = incidence // 4
                live_count = positive_count + equality_count
                if not global_edges or global_edges > capacities[live_count - 1]:
                    continue
                exceptional_neighbors = positive_count + empty_count - 1
                if any(item[2] > exceptional_neighbors for item in chosen):
                    continue
                survivors.add((chosen, equality_count, empty_count, global_edges))
            return
        if total >= TARGET or len(chosen) == 10:
            return
        for index in range(start, len(classes)):
            item = classes[index]
            if total + item[0] > TARGET:
                break
            visit(index, chosen + (item,), total + item[0])

    visit(0, (), 0)
    return tuple(sorted(survivors))


def verify():
    rows = json.loads((PARENT / "PROFILE_CLASSES.json").read_text())
    profile_hash = sha256(
        json.dumps(rows, separators=(",", ":")).encode("ascii")
    ).hexdigest()
    if len(rows) != 182 or profile_hash != EXPECTED_PROFILE_HASH:
        raise AssertionError("accepted strict-subendpoint profile certificate changed")
    if max(row[0] for row in rows) != 217:
        raise AssertionError("profile certificate is not the delta<218 table")

    capacities = live_capacity_maxima()
    if capacities != [0, 0, 0, 1, 5, 9, 16, 28, 48, 80]:
        raise AssertionError("unexpected live-facet capacity table")
    classes = tuple(sorted(tuple(row[:4]) for row in rows))
    survivors = smaller_deficit_profiles(classes, capacities)
    if survivors:
        raise AssertionError("a strict-subendpoint total-218 profile survived")

    # If one facet itself has delta=218, solve 17*S-3*E=218 with E<=24.
    endpoint_solutions = tuple(
        (edges, slack)
        for edges in range(25)
        for slack in range(25)
        if 17 * slack - 3 * edges == TARGET
    )
    if endpoint_solutions != ((1, 13), (18, 16)):
        raise AssertionError("unexpected local endpoint arithmetic")
    # A one-edge Q4 pattern has (T,P,S)=(0,0,6), excluding (1,13).
    one_edge_statistics = (1, 0, 0, 6)
    endpoint_edge_count = 18

    endpoint_live_cases = []
    for equality_count in range(10):
        incidence = endpoint_edge_count + 17 * equality_count
        if incidence % 4:
            continue
        global_edges = incidence // 4
        live_count = equality_count + 1
        endpoint_live_cases.append(
            (equality_count, 9 - equality_count, live_count,
             global_edges, capacities[live_count - 1])
        )
    expected_cases = [(2, 7, 3, 13, 0), (6, 3, 7, 30, 16)]
    if endpoint_live_cases != expected_cases:
        raise AssertionError("unexpected single-endpoint live-facet cases")
    if any(global_edges <= capacity for _, _, _, global_edges, capacity in endpoint_live_cases):
        raise AssertionError("a single-endpoint case survived its live-facet capacity")

    local_ratio = Fraction(12 * 56 + 219, 34 * 56)
    global_coefficient = local_ratio / 12
    asymptotic = Fraction(13328, 7319)
    previous = Fraction(19992, 10979)
    if local_ratio != Fraction(891, 1904) or global_coefficient != Fraction(297, 7616):
        raise AssertionError("incorrect local-to-global coefficient")
    if asymptotic - previous != Fraction(6664, 80355301):
        raise AssertionError("incorrect asymptotic improvement")
    integer_bounds = []
    for dimension in range(5, 11):
        old_value = Fraction(19992 * dimension * 2**dimension,
                             10979 * dimension + 29005)
        new_value = Fraction(13328 * dimension * 2**dimension,
                             7319 * dimension + 19337)
        ceil = lambda value: (value.numerator + value.denominator - 1) // value.denominator
        integer_bounds.append((dimension, ceil(old_value), ceil(new_value)))
    if any(old != new for _, old, new in integer_bounds[:-1]):
        raise AssertionError("integer bound improves before dimension ten")
    if integer_bounds[-1] != (10, 1475, 1476):
        raise AssertionError("incorrect first integer improvement")

    return {
        "status": "PASS",
        "accepted_profile_rows": len(rows),
        "accepted_profile_sha256": profile_hash,
        "live_capacity_maxima": capacities,
        "strict_subendpoint_total218_survivors": len(survivors),
        "local_endpoint_diophantine_solutions": endpoint_solutions,
        "one_edge_q4_statistics": one_edge_statistics,
        "single_endpoint_live_cases": endpoint_live_cases,
        "q5_deficit_lower_bound": 219,
        "q5_slack_edge_ratio": str(local_ratio),
        "global_slack_coefficient": str(global_coefficient),
        "global_bound": "13328*d*2^d/(7319*d+19337)",
        "asymptotic_constant": str(asymptotic),
        "improvement_over_gap218": str(asymptotic - previous),
        "first_improved_integer_bound": integer_bounds[-1],
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
