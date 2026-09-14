#!/usr/bin/env python3
"""Exact verifier for four concurrent P147 triangular patches.

The exact point, contact-phase, coincidence, and sparse-radical arithmetic
engine is imported from the preceding P36 theorem and pinned by SHA-256.  This
program replaces explicit enumeration of every four-cycle placement by an
equivalent two-edge-path parity census.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import combinations
import hashlib
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "hadwiger_nelson_four_triangular_patches" / "verify.py"
BASE_SHA256 = "ecb0cc54aef4ab7d6edbbdb2e08be6e17de00e062e5c40413fafb26b9fd2c49a"


def require(condition, message):
    if not condition:
        raise ValueError(message)


require(BASE.is_file(), "missing pinned P36 exact-arithmetic engine")
require(hashlib.sha256(BASE.read_bytes()).hexdigest() == BASE_SHA256,
        "P36 exact-arithmetic engine has changed")
SPEC = importlib.util.spec_from_file_location("p36_exact_engine", BASE)
exact = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(exact)


def update_hash(digest, value):
    digest.update(repr(value).encode("ascii"))
    digest.update(b"\n")


def text_key(value):
    return str(tuple(value))


def insert_path(buckets, target, channel, value, middle):
    """Insert a path label; return an opposite-label middle if one exists."""
    row = buckets[target][channel]
    opposite = row.get(value ^ 1)
    if opposite is not None:
        require(opposite != middle,
                "one geometric two-edge path acquired two parity labels")
    row.setdefault(value, middle)
    return opposite


def scan(limit):
    exact.LIMIT = limit
    inventory = exact.build_inventory()
    events = inventory["events"]
    classes = sorted({exact.canonical_phase(exact.phase_from_key(key))
                      for key in events})
    identity = exact.canonical_phase(exact.rational_phase(1, 0))
    nonidentity = [key for key in classes if key != identity]
    phases = {key: exact.phase_from_key(key) for key in classes}
    require(all(key in events for key in classes),
            "canonical event representative absent from inventory")

    inventory_digest = hashlib.sha256()
    for key in sorted(events):
        update_hash(inventory_digest,
                    (key, tuple(sorted(events[key])),
                     tuple(sorted(inventory["coincidences"].get(key, ())))))

    pair_profiles = Counter()
    base_constraints = {}
    for key in nonidentity:
        constraint = exact.pair_constraints(phases[key], inventory)
        base_constraints[key] = constraint
        pair_profiles[constraint] += 1

    constraint_cache = {}

    def constraints(layer_phases):
        sign, zero = [], []
        active = rational = 0
        for left, right in combinations(range(len(layer_phases)), 2):
            delta = exact.phase_multiply(
                exact.phase_conjugate(layer_phases[left]), layer_phases[right])
            key = exact.phase_key(delta)
            if key not in constraint_cache:
                constraint_cache[key] = exact.pair_constraints(delta, inventory)
            sign_bit, zero_bit = constraint_cache[key]
            if sign_bit is not None:
                sign.append((left, right, sign_bit))
            if zero_bit is not None:
                zero.append((left, right, zero_bit))
            if key in events:
                active += 1
                rational += int(exact.is_rational_key(key))
        return tuple(sign), tuple(zero), active, rational

    triangle_count = 0
    triangle_profiles = Counter()
    bad_triangles = []
    triangle_digest = hashlib.sha256()
    one = exact.rational_phase(1, 0)
    for offset, alpha in enumerate(nonidentity):
        for beta in nonidentity[offset + 1:]:
            relative = exact.phase_key(exact.phase_multiply(
                exact.phase_conjugate(phases[alpha]), phases[beta]))
            if relative not in events:
                continue
            sign, zero, active, rational = constraints(
                (one, phases[alpha], phases[beta]))
            sign_ok = exact.solve_xor(3, sign) is not None
            zero_ok = exact.solve_xor(3, zero) is not None
            triangle_count += 1
            triangle_profiles[(active, rational, len(sign), len(zero),
                               sign_ok, zero_ok)] += 1
            update_hash(triangle_digest, (alpha, beta, sign, zero))
            if not sign_ok or not zero_ok:
                bad_triangles.append((alpha, beta, sign, zero))

    # For a normalized four-cycle 1--a--t--c--1, inconsistency in either
    # binary constraint graph is equivalent to the accumulated label on
    # 1--a--t differing from that on 1--c--t.  Thus grouping two-edge paths
    # by (t, channel) is a complete C4 obstruction test.
    buckets = defaultdict(lambda: {"sign": {}, "zero": {}})
    constrained_paths = Counter()
    all_paths = 0
    path_digest = hashlib.sha256()
    conflict_channels = set()
    conflict_samples = []
    conjugates = {key: exact.phase_conjugate(phases[key])
                  for key in nonidentity}
    for alpha in nonidentity:
        base_sign, base_zero = base_constraints[alpha]
        for step in nonidentity:
            target = exact.canonical_phase(
                exact.phase_multiply(phases[alpha], phases[step]))
            if target in (identity, alpha):
                continue
            phases.setdefault(target, exact.phase_from_key(target))
            delta = exact.phase_multiply(conjugates[alpha], phases[target])
            edge_sign, edge_zero = exact.pair_constraints(delta, inventory)
            all_paths += 1
            update_hash(path_digest,
                        (alpha, step, target, base_sign, base_zero,
                         edge_sign, edge_zero))
            for channel, left, right in (
                    ("sign", base_sign, edge_sign),
                    ("zero", base_zero, edge_zero)):
                if left is None or right is None:
                    continue
                constrained_paths[channel] += 1
                value = left ^ right
                opposite = insert_path(buckets, target, channel, value, alpha)
                if opposite is not None:
                    conflict_channels.add((target, channel))
                    if len(conflict_samples) < 10:
                        conflict_samples.append(
                            (channel, target, opposite, alpha))

    channel_buckets = {
        channel: sum(bool(row[channel]) for row in buckets.values())
        for channel in ("sign", "zero")
    }
    label_states = {
        channel: sum(len(row[channel]) for row in buckets.values())
        for channel in ("sign", "zero")
    }
    require(triangle_count > 0 and all_paths > 0, "empty obstruction census")

    report = {
        "verified": not bad_triangles and not conflict_channels,
        "arithmetic": "exact integers, Fractions, sparse squarefree radicals",
        "base_engine_sha256": BASE_SHA256,
        "norm_limit": limit,
        "patch_vertices": len(inventory["points"]),
        "patch_edges": len(inventory["seed_edges"]),
        "maximum_union_vertices": 4 * len(inventory["points"]) - 3,
        "primitive_contact_lines": len(inventory["lines"]),
        "universal_contact_pairs": len(inventory["universal"]),
        "event_phases": len(events),
        "rational_event_phases": sum(exact.is_rational_key(key)
                                      for key in events),
        "event_classes_mod_units": len(classes),
        "rational_event_classes_mod_units": sum(
            exact.is_rational_key(key) for key in classes),
        "coincidence_phases": len(inventory["coincidences"]),
        "pair_constraint_profiles": {
            text_key(key): count for key, count in sorted(pair_profiles.items(),
                                                          key=lambda row: str(row[0]))
        },
        "normalized_active_triangles": triangle_count,
        "triangle_profiles": {
            text_key(key): count for key, count in sorted(triangle_profiles.items())
        },
        "inconsistent_triangles": len(bad_triangles),
        "two_edge_products": all_paths,
        "constrained_two_edge_paths": dict(sorted(constrained_paths.items())),
        "distinct_constrained_targets": len(buckets),
        "channel_target_buckets": channel_buckets,
        "channel_label_states": label_states,
        "opposite_parity_target_channels": len(conflict_channels),
        "conflict_samples": [repr(row) for row in conflict_samples],
        "inventory_sha256": inventory_digest.hexdigest(),
        "triangle_census_sha256": triangle_digest.hexdigest(),
        "two_edge_path_census_sha256": path_digest.hexdigest(),
    }
    return report


def certify():
    report = scan(147)
    require(report["verified"], "P147 parity obstruction found")
    require(report["inconsistent_triangles"] == 0,
            "P147 inconsistent triangle found")
    require(report["opposite_parity_target_channels"] == 0,
            "P147 inconsistent four-cycle found")
    require(report["channel_label_states"] == report["channel_target_buckets"],
            "a P147 target channel carries both parity labels")
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    report = certify()
    if args.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        require(report == expected, "result differs from EXPECTED.json")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
