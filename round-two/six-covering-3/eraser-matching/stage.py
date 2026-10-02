"""Apply the necessary two-layer cut AFTER all36 free base phases are chosen.

Input is a JSON list of [modulus, phase] pairs for precisely those36 labels.
No search, phase fixing, or root nonexistence inference is performed here.
"""

import argparse
import json
from pathlib import Path

from model import divisors, eraser_graph, matching_certificate, signature, weighted_cover

PREFIX = [[8, 0], [9, 0], [10, 1], [14, 1], [12, 10]]
BASE_RESOURCES = [n for n in range(8, 2521) if 2520 % n == 0 and n not in {n for n, a in PREFIX}]


def evaluate(phases):
    if not isinstance(phases, list) or any(not isinstance(row, list) or len(row) != 2 for row in phases):
        raise ValueError("expected a list of36 [modulus, phase] pairs")
    if sorted(n for n, a in phases) != BASE_RESOURCES:
        raise ValueError("must choose each of the36 original unused base moduli exactly once")
    if any(type(n) is not int or type(a) is not int or not 0 <= a < n for n, a in phases):
        raise ValueError("phase outside its original modulus")
    all_phases = PREFIX + phases
    fibers = [[] for _ in range(8)]
    for x in range(2520):
        if not any(x % n == a for n, a in all_phases):
            fibers[x % 8].append(x % 315)
    prefixes = [r for r, v in enumerate(fibers) if v]
    nonempty = [sorted(fibers[r]) for r in prefixes]
    resources = divisors(315)
    graph = eraser_graph(315, nonempty, resources, 2)
    cover = weighted_cover(315, nonempty, resources, 2)
    threshold = 4 * len(graph) - 3 * len(resources)
    return {"agent": "six-covering-3", "role": "researcher", "base_phases": 36,
            "prefixes": prefixes, "holes": nonempty,
            "signatures": [signature(315, v) for v in nonempty],
            "matching_certificate": matching_certificate(graph, resources),
            "weighted_cover": cover, "two_layer_threshold": threshold,
            "excluded_by_two_layer_cut": cover["value"] < threshold,
            "scope": "Only this fully specified base assignment; passing is inconclusive."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("base_phases", type=Path)
    args = parser.parse_args()
    print(json.dumps(evaluate(json.loads(args.base_phases.read_text())), sort_keys=True))
