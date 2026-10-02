"""Emit the compact fixtures/certificates; stdout only, no frozen-file writes."""

import json

from model import (crt, divisors, eraser_graph, matching_certificate,
                   signature, weighted_cover)


def certificate():
    cofactor = 105
    points = [x for x in range(cofactor)
              if (x % 3, x % 5, x % 7) in [(0, 1, 0), (0, 0, 1), (1, 0, 0)]]
    resources = [1, 3, 5, 7]
    graph = eraser_graph(cofactor, [points, points], resources, 2)
    fractional = []
    for power in [8, 16]:
        prefixes = sorted(r + 4 * j for r in [1, 2] for j in range(power // 4))
        for d in resources:
            fractional.append({
                "modulus": power * d,
                "phases": [[crt(u, power, 0, d), 1, len(prefixes)]
                           for u in prefixes],
            })
    sat_fibers = [[2, 2 + g] if g < 315 else [2]
                  for g in [3, 15, 21, 63, 105, 315]]
    sat_resources = divisors(315)
    sat_graph = eraser_graph(315, sat_fibers, sat_resources, 2)
    sat_match = matching_certificate(sat_graph, sat_resources)
    phases = []
    for left, d in sat_match["matching"]:
        parent, child = divmod(left, 2)
        prefix = (parent + 1) + 16 * child
        phases.append([32 * d, crt(prefix, 32, sat_fibers[parent][0] % d, d)])
    return {
        "schema": 1,
        "agent": "six-covering-3",
        "role": "researcher",
        "toy": {
            "ambient_period": 1680,
            "parent_power": 4,
            "parent_prefixes": [1, 2],
            "cofactor": cofactor,
            "points": points,
            "resources_per_layer": resources,
            "prime": 2,
            "graph": graph,
            "matching_certificate": matching_certificate(graph, resources),
            "weighted_cover": weighted_cover(cofactor, [points, points], resources, 2),
            "two_layer_threshold": 4,
            "fractional_phases": fractional,
            "point_coverage": [9, 8],
            "integer_completion": False,
        },
        "period10080": {
            "ambient_period": 10080,
            "base_period": 2520,
            "cofactor": 315,
            "prefix": [[8, 0], [9, 0], [10, 1], [14, 1], [12, 10]],
            "unused_base_count": 36,
            "unused_tail_count": 24,
            "base_holes": 1398,
            "physical_holes": 5592,
            "base_fiber_sizes": [0, 192, 175, 192, 280, 192, 175, 192],
            "cofactor_resources": sat_resources,
            "subset_minimum_eraser_labels": {"5": 2, "6": 4, "7": 7},
            "max_nonempty_signature_one_fibers": 4,
            "stage_scope": "After every remaining base resource has its phase chosen; all 16d and32d free.",
        },
        "saturated_terminal_control": {
            "ambient_period": 10080,
            "parent_power": 16,
            "parent_prefixes": [1, 2, 3, 4, 5, 6],
            "cofactor": 315,
            "fibers": sat_fibers,
            "signatures": [signature(315, v) for v in sat_fibers],
            "graph": sat_graph,
            "matching_certificate": sat_match,
            "completion_phases": sorted(phases),
            "scope": "Conditional residual only; no reachability from the five-class prefix claimed.",
        },
    }


if __name__ == "__main__":
    print(json.dumps(certificate(), indent=2, sort_keys=True))
