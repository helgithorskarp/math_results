#!/usr/bin/env python3
"""Small-radius and adversarial controls for the review path census."""

from collections import defaultdict
import json

import independent_check as check


def main():
    check.negative_controls()
    exact = check.review
    exact.LIMIT = 36
    inventory = exact.build_inventory()
    events = inventory["events"]
    classes = sorted({exact.canonical_phase(exact.phase_from_key(key))
                      for key in events})
    identity = exact.canonical_phase(exact.IDENTITY)
    nonidentity = [key for key in classes if key != identity]
    phases = {key: exact.phase_from_key(key) for key in classes}

    def requirements(key):
        return exact.pair_requirements(exact.phase_from_key(key), inventory)

    triangles = 0
    bad_triangles = 0
    for offset, alpha in enumerate(nonidentity):
        for beta in nonidentity[offset + 1:]:
            relative = exact.phase_key(exact.phase_product(
                exact.phase_conjugate(phases[alpha]), phases[beta]))
            if relative not in events:
                continue
            rows = ((0, 1, requirements(alpha)),
                    (0, 2, requirements(beta)),
                    (1, 2, requirements(relative)))
            for channel in (0, 1):
                equations = check.channel_equations(rows, channel)
                bad_triangles += int(
                    exact.propagate_parity(3, equations) is None)
            triangles += 1

    labels = defaultdict(set)
    products = 0
    for middle in nonidentity:
        left = requirements(middle)
        inverse = exact.phase_conjugate(phases[middle])
        for step in nonidentity:
            target = exact.canonical_phase(
                exact.phase_product(phases[middle], phases[step]))
            if target in (identity, middle):
                continue
            phases.setdefault(target, exact.phase_from_key(target))
            delta = exact.phase_key(exact.phase_product(inverse, phases[target]))
            check.need(delta in events, "P36 canonicalization lost an event edge")
            right = requirements(delta)
            products += 1
            for channel in (0, 1):
                if left[channel] is not None and right[channel] is not None:
                    labels[(target, channel)].add(left[channel] ^ right[channel])

    conflicts = sum(len(values) > 1 for values in labels.values())
    check.need((len(inventory["points"]), len(inventory["seed_edges"])) ==
               (127, 342), "P36 patch census changed")
    check.need((len(events), len(classes)) == (594, 99),
               "P36 event census changed")
    check.need((triangles, bad_triangles) == (186, 0),
               "P36 triangle comparison failed")
    check.need((products, conflicts) == (9506, 0),
               "P36 endpoint-label comparison failed")

    # Directly corrupt one nonempty bucket and demand detection.
    key = next(iter(labels))
    original = next(iter(labels[key]))
    labels[key].add(original ^ 1)
    check.need(any(len(values) > 1 for values in labels.values()),
               "corrupted P36 endpoint bucket was accepted")

    print(json.dumps({
        "verified": True,
        "p36_patch_vertices": len(inventory["points"]),
        "p36_patch_edges": len(inventory["seed_edges"]),
        "p36_event_phases": len(events),
        "p36_event_classes_mod_units": len(classes),
        "p36_active_triangles": triangles,
        "p36_inconsistent_triangle_channels": bad_triangles,
        "p36_two_edge_products": products,
        "p36_opposite_parity_target_channels_before_corruption": conflicts,
        "synthetic_bucket_corruption_detected": True,
        "explicit_p36_four_cycle_reference": 8100,
        "explicit_reference_checker_sha256": check.DEPENDENCY_SHA256,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
