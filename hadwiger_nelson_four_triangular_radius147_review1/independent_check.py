#!/usr/bin/env python3
"""Independent exact review of the four-concurrent-P147 theorem.

The target imports the author's P36 arithmetic engine and aggregates ordered
point pairs by primitive contact lines.  This checker instead pins and imports
the already-published clean-room P36 *review* engine.  That engine represents
surd bases by prime-support tuples and derives the roots directly from every
ordered point pair.  No target code or target-generated data is imported.

At radius 147 we independently rebuild the complete event inventory and use
parity propagation / endpoint-label sets to test all triangle and four-cycle
obstructions.  Target-compatible hashes are computed only after the objects
have been independently derived.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import importlib.util
import json
from math import isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEPENDENCY = (HERE.parent / "hadwiger_nelson_four_triangular_patches_review1"
              / "independent_check.py")
DEPENDENCY_SHA256 = (
    "9ec7fe896e1c2197da0788d00ee033dae81348172ce26e449599cd8d2798644d"
)
LIMIT = 147

# These are claims under review.  They are checked after, and are not used to
# generate, the point set, event phases, or obstruction census.
TARGET = {
    "patch_vertices": 535,
    "patch_edges": 1518,
    "maximum_union_vertices": 2137,
    "primitive_contact_lines": 4788,
    "universal_contact_pairs": 12,
    "event_phases": 6054,
    "rational_event_phases": 1338,
    "event_classes_mod_units": 1009,
    "rational_event_classes_mod_units": 223,
    "coincidence_phases": 246,
    "normalized_active_triangles": 4449,
    "two_edge_products": 1015056,
    "distinct_constrained_targets": 140656,
    "opposite_parity_target_channels": 0,
    "inventory_sha256":
        "eb56210013f2d8e777b50a164ea774c6756da01658b83c8101f3ba9af01f23da",
    "triangle_census_sha256":
        "66fe9d7754ed5cb87de728577be27d10c9d521c49aba7c8d5db829740e6ebbf4",
    "two_edge_path_census_sha256":
        "68a570b0073f76b80a6ea7e3a82a39fe4737f71fa00ee4a929020801c6bcfac0",
}


def need(condition, message):
    if not condition:
        raise AssertionError(message)


need(DEPENDENCY.is_file(), "missing clean-room P36 review engine")
need(hashlib.sha256(DEPENDENCY.read_bytes()).hexdigest() == DEPENDENCY_SHA256,
     "clean-room P36 review engine has changed")
SPEC = importlib.util.spec_from_file_location("reviewed_p36_engine", DEPENDENCY)
review = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(review)


def update_digest(digest, value):
    digest.update(repr(value).encode("ascii"))
    digest.update(b"\n")


def text_key(value):
    return str(tuple(value))


def patch(limit):
    """Build P_limit with an independently justified finite search box."""
    bound = isqrt(4 * limit // 3) + 1
    return {(a, b) for a in range(-bound, bound + 1)
            for b in range(-bound, bound + 1)
            if review.ring_norm((a, b)) <= limit}


def channel_equations(pair_rows, channel):
    result = []
    for left, right, requirements in pair_rows:
        bit = requirements[channel]
        if bit is not None:
            result.append((left, right, bit))
    return tuple(result)


def negative_controls():
    need(review.propagate_parity(
        3, ((0, 1, 0), (1, 2, 0), (0, 2, 1))) is None,
         "odd triangle was accepted")
    need(review.propagate_parity(
        4, ((0, 1, 0), (1, 2, 0), (2, 3, 0), (0, 3, 1))) is None,
         "odd square was accepted")
    need(review.propagate_parity(
        4, ((0, 1, 1), (1, 2, 0), (2, 3, 1))) is not None,
         "consistent forest was rejected")
    synthetic = defaultdict(set)
    synthetic[("target", "sign")].add(0)
    need(not any(len(values) > 1 for values in synthetic.values()),
         "one synthetic path created a conflict")
    synthetic[("target", "sign")].add(1)
    need(any(len(values) > 1 for values in synthetic.values()),
         "opposite synthetic path labels were not detected")


def certify():
    # The imported engine is independent of the target and deliberately uses
    # a loose point box plus direct ordered-pair root generation.
    review.LIMIT = LIMIT
    inventory = review.build_inventory()
    events = inventory["events"]
    phases = {}

    def phase(key):
        if key not in phases:
            phases[key] = review.phase_from_key(key)
        return phases[key]

    classes = sorted({review.canonical_phase(phase(key)) for key in events})
    identity_key = review.canonical_phase(review.IDENTITY)
    nonidentity = [key for key in classes if key != identity_key]
    need(all(key in events for key in classes),
         "a canonical event representative is absent from the raw inventory")

    requirement_cache = {}

    def requirements(key):
        if key not in requirement_cache:
            requirement_cache[key] = review.pair_requirements(phase(key), inventory)
        return requirement_cache[key]

    # Every raw phase is a separate exact pair check.  Inversion swaps the two
    # layers and therefore must preserve each XOR requirement.
    raw_pair_histogram = Counter(requirements(key) for key in events)
    inverse_mismatches = 0
    missing_inverse_phases = 0
    for key in events:
        inverse_key = review.phase_key(review.phase_conjugate(phase(key)))
        if inverse_key not in events:
            missing_inverse_phases += 1
        elif requirements(key) != requirements(inverse_key):
            inverse_mismatches += 1
    need(missing_inverse_phases == 0, "event inventory is not inversion-closed")
    need(inverse_mismatches == 0, "inverse interfaces have different XOR labels")
    need(requirements(review.phase_key(review.IDENTITY)) == (0, 0),
         "identical patches do not impose palette equality")

    canonical_pair_histogram = Counter(requirements(key) for key in nonidentity)

    triangle_count = 0
    triangle_profiles = Counter()
    bad_triangles = 0
    triangle_digest = hashlib.sha256()
    for offset, alpha_key in enumerate(nonidentity):
        for beta_key in nonidentity[offset + 1:]:
            relative = review.phase_product(
                review.phase_conjugate(phase(alpha_key)), phase(beta_key))
            relative_key = review.phase_key(relative)
            if relative_key not in events:
                continue
            pair_rows = (
                (0, 1, requirements(alpha_key)),
                (0, 2, requirements(beta_key)),
                (1, 2, requirements(relative_key)),
            )
            sign = channel_equations(pair_rows, 0)
            zero = channel_equations(pair_rows, 1)
            sign_ok = review.propagate_parity(3, sign) is not None
            zero_ok = review.propagate_parity(3, zero) is not None
            rational = sum(review.is_rational_key(key)
                           for key in (alpha_key, beta_key, relative_key))
            triangle_profiles[(3, rational, len(sign), len(zero),
                               sign_ok, zero_ok)] += 1
            triangle_count += 1
            bad_triangles += int(not sign_ok or not zero_ok)
            update_digest(triangle_digest,
                          (alpha_key, beta_key, sign, zero))

    # Generate every normalized length-two walk.  Unlike the target's mutable
    # per-target maps, collect the independently computed accumulated labels
    # into mathematical sets and inspect those sets only after enumeration.
    endpoint_labels = defaultdict(set)
    constrained_paths = Counter()
    all_paths = 0
    path_digest = hashlib.sha256()
    for middle_key in nonidentity:
        left_sign, left_zero = requirements(middle_key)
        middle_inverse = review.phase_conjugate(phase(middle_key))
        for step_key in nonidentity:
            target_key = review.canonical_phase(
                review.phase_product(phase(middle_key), phase(step_key)))
            if target_key in (identity_key, middle_key):
                continue
            actual_step_key = review.phase_key(
                review.phase_product(middle_inverse, phase(target_key)))
            need(actual_step_key in events,
                 "canonicalized length-two walk lost its second event edge")
            right_sign, right_zero = requirements(actual_step_key)
            all_paths += 1
            update_digest(path_digest,
                          (middle_key, step_key, target_key,
                           left_sign, left_zero, right_sign, right_zero))
            for channel, left, right in (
                    ("sign", left_sign, right_sign),
                    ("zero", left_zero, right_zero)):
                if left is None or right is None:
                    continue
                constrained_paths[channel] += 1
                endpoint_labels[(target_key, channel)].add(left ^ right)

    conflicts = {key: values for key, values in endpoint_labels.items()
                 if len(values) > 1}
    channel_buckets = {
        channel: sum(key[1] == channel for key in endpoint_labels)
        for channel in ("sign", "zero")
    }
    label_states = {
        channel: sum(len(values) for key, values in endpoint_labels.items()
                     if key[1] == channel)
        for channel in ("sign", "zero")
    }
    constrained_targets = {key[0] for key in endpoint_labels}
    bucket_digest = hashlib.sha256()
    for key in sorted(endpoint_labels):
        update_digest(bucket_digest, (key, tuple(sorted(endpoint_labels[key]))))

    # Independent exact bridge from the continuum P147 theorem to the
    # record-relevant translated-P36 corollary.
    p36, p37, p147, p148 = (patch(limit) for limit in (36, 37, 147, 148))
    differences = {(z[0] - anchor[0], z[1] - anchor[1])
                   for z in p36 for anchor in p36}
    difference_max_norm = max(map(review.ring_norm, differences))
    conjugated_p36 = {review.ring_conjugate(z) for z in p36}
    need(differences <= p147, "a recentered P36 patch escapes P147")
    need(conjugated_p36 == p36, "P36 is not reflection-invariant")

    report = {
        "verified": bad_triangles == 0 and not conflicts,
        "review_method": (
            "direct ordered-pair roots; prime-support surds; parity propagation; "
            "endpoint-label sets"
        ),
        "review_dependency_sha256": DEPENDENCY_SHA256,
        "norm_limit": LIMIT,
        "patch_vertices": len(inventory["points"]),
        "patch_edges": len(inventory["seed_edges"]),
        "maximum_union_vertices": 4 * len(inventory["points"]) - 3,
        "primitive_contact_lines": len(inventory["lines"]),
        "universal_contact_pairs": len(inventory["universal"]),
        "event_phases": len(events),
        "rational_event_phases": sum(review.is_rational_key(key) for key in events),
        "irrational_event_phases": sum(not review.is_rational_key(key)
                                       for key in events),
        "event_classes_mod_units": len(classes),
        "rational_event_classes_mod_units": sum(
            review.is_rational_key(key) for key in classes),
        "irrational_event_classes_mod_units": sum(
            not review.is_rational_key(key) for key in classes),
        "coincidence_phases": len(inventory["coincidences"]),
        "raw_pair_constraint_histogram": {
            text_key(key): count for key, count in sorted(
                raw_pair_histogram.items(), key=lambda row: repr(row[0]))
        },
        "canonical_nonidentity_pair_constraint_histogram": {
            text_key(key): count for key, count in sorted(
                canonical_pair_histogram.items(), key=lambda row: repr(row[0]))
        },
        "missing_inverse_phases": missing_inverse_phases,
        "inverse_constraint_mismatches": inverse_mismatches,
        "normalized_active_triangles": triangle_count,
        "triangle_profiles": {
            text_key(key): count for key, count in sorted(triangle_profiles.items())
        },
        "inconsistent_triangles": bad_triangles,
        "two_edge_products": all_paths,
        "constrained_two_edge_paths": dict(sorted(constrained_paths.items())),
        "distinct_constrained_targets": len(constrained_targets),
        "channel_target_buckets": channel_buckets,
        "channel_label_states": label_states,
        "opposite_parity_target_channels": len(conflicts),
        "p36_points": len(p36),
        "p37_points": len(p37),
        "p147_points": len(p147),
        "p148_points": len(p148),
        "p36_difference_hull_points": len(differences),
        "p36_difference_hull_maximum_norm": difference_max_norm,
        "p36_difference_hull_contained_in_p147": differences <= p147,
        "p36_reflection_invariant": conjugated_p36 == p36,
        "maximum_common_point_p36_union_vertices": 4 * len(p36) - 3,
        "inventory_sha256": inventory["inventory_sha256"],
        "triangle_census_sha256": triangle_digest.hexdigest(),
        "two_edge_path_census_sha256": path_digest.hexdigest(),
        "review_endpoint_label_buckets_sha256": bucket_digest.hexdigest(),
    }

    for field, expected in TARGET.items():
        need(report[field] == expected,
             f"target disagreement for {field}: {report[field]!r} != {expected!r}")
    need(report["canonical_nonidentity_pair_constraint_histogram"] == {
        "(0, 0)": 6,
        "(0, None)": 268,
        "(1, 0)": 8,
        "(1, None)": 234,
        "(None, 1)": 212,
        "(None, None)": 280,
    }, "canonical pair profile differs from target")
    need(report["channel_target_buckets"] ==
         report["channel_label_states"] == {"sign": 117402, "zero": 23362},
         "an endpoint/channel has opposite path parities")
    need((len(p36), len(p37), len(p147), len(p148)) == (127, 139, 535, 547),
         "radial patch cardinality boundary changed")
    need((len(differences), difference_max_norm) == (469, 144),
         "P36 translation hull changed")
    need(report["maximum_common_point_p36_union_vertices"] == 505,
         "common-point P36 vertex bound changed")
    need(report["verified"], "P147 obstruction census found a conflict")
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    negative_controls()
    report = certify()
    output = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.check_expected:
        expected = (HERE / "EXPECTED.json").read_text()
        need(output == expected, "output differs from review EXPECTED.json")
    print(output, end="")


if __name__ == "__main__":
    main()
