#!/usr/bin/env python3
"""Independent checker for the A5 five-active free-action interface."""

import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ACTION_ORDER = ("1", "R", "R^2", "C", "RC", "R^2C")
MODES = (
    "exact_five_compatible",
    "parallel_signatures_require_at_least_six",
    "unrealized_pencil_type_requires_at_least_six",
)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PENCIL = load(
    "five_orbit_pencil_checker",
    ROOT / "hadwiger_nelson_radix_five_active_pencil" / "verify.py",
)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def file_digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def compose(left, right):
    return tuple(left[right[index]] for index in range(len(left)))


def named_curve_group():
    d3 = PENCIL.D3
    rows, events, factors, _, _, _, _, circle = d3.HN2.build()
    factor_ids = {factor: index for index, factor in enumerate(factors)}
    representatives = {}
    for row, event in zip(rows, events):
        if event:
            representatives.setdefault(factor_ids[event], row)
    need(len(representatives) == len(factors), "representative row inventory")

    def permutation(transform):
        result = []
        for curve in range(len(factors)):
            image = transform(representatives[curve])
            support = [index for index, digit in enumerate(image) if digit != (0, 0)]
            if len(support) == 1:
                need(support[0] > 0, "monomial event")
                result.append(circle)
            else:
                result.append(factor_ids[d3.G.distance_event(image)])
        return tuple(result)

    identity = tuple(range(len(factors)))
    rotation = permutation(d3.rotate_row)
    conjugation = permutation(d3.conjugate_row)
    rotation2 = compose(rotation, rotation)
    group = (
        identity,
        rotation,
        rotation2,
        conjugation,
        compose(rotation, conjugation),
        compose(rotation2, conjugation),
    )
    need(len(set(group)) == 6, "six named D3 actions")
    need(compose(rotation, rotation2) == identity, "R^3=1")
    need(compose(conjugation, conjugation) == identity, "C^2=1")
    need(compose(compose(conjugation, rotation), conjugation) == rotation2, "CRC=R^-1")
    need(all(compose(a, b) in group for a in group for b in group), "D3 closure")
    degrees = [d3.HN2.degree(factor) for factor in factors]
    need(all(degree in (2, 4, 6, 8) for degree in degrees), "curve degrees")
    return factors, degrees, group


def output_map(counter):
    return {str(key): value for key, value in sorted(counter.items())}


def rows_and_summary(pairs, degrees, group):
    rows = []
    histogram = Counter()
    bidegree_sums = Counter()
    orbit_sums = Counter()
    total_degree = bidegree = rotation_free = orbit_allowance = 0
    for pair in pairs:
        a, b = pair
        need(0 <= a < b < len(degrees), "valid canonical pair")
        images = [tuple(sorted((action[a], action[b]))) for action in group]
        need(min(images) == (a, b), "global D3 representative")
        fixed = [index for index, image in enumerate(images) if image == (a, b)]
        mask = sum(1 << index for index in fixed)
        stabilizer = len(fixed)
        rotation_stabilizer = sum(index < 3 for index in fixed)
        need(stabilizer * len(set(images)) == 6, "orbit-stabilizer")
        need(stabilizer % rotation_stabilizer == 0, "rotation subgroup")
        sharp = degrees[a] * degrees[b] // 2
        need(sharp == 2 * (degrees[a] // 2) * (degrees[b] // 2), "P1xP1 bound")
        allowance = sharp // stabilizer
        rows.append([a, b, mask, sharp, allowance])
        histogram[stabilizer] += 1
        bidegree_sums[stabilizer] += sharp
        orbit_sums[stabilizer] += allowance
        total_degree += degrees[a] * degrees[b]
        bidegree += sharp
        rotation_free += sharp // rotation_stabilizer
        orbit_allowance += allowance
    summary = {
        "pair_systems": len(rows),
        "pair_stabilizer_histogram": output_map(histogram),
        "total_degree_allowance": total_degree,
        "product_surface_intersection_allowance": bidegree,
        "rotation_free_intersection_allowance": rotation_free,
        "nonfour_D3_orbit_allowance": orbit_allowance,
        "bidegree_sums_by_stabilizer": output_map(bidegree_sums),
        "orbit_allowance_sums_by_stabilizer": output_map(orbit_sums),
        "bidegree_reduction": total_degree - bidegree,
        "rotation_fixed_point_reduction": bidegree - rotation_free,
        "reflection_fixed_point_reduction": rotation_free - orbit_allowance,
        "total_reduction": total_degree - orbit_allowance,
    }
    return rows, summary


def precheck(certificate):
    need(certificate.get("schema") == "hn-radix-five-active-orbits-v1", "schema")
    need(certificate["exact_five_frontier"] == certificate["mode_summaries"][MODES[0]], "exact-five projection")
    need(certificate["global_reconciliation"]["pair_systems"] == 131356, "global pair count")
    need(certificate["global_reconciliation"]["nonfour_D3_orbit_allowance"] == 3846704, "global allowance")
    need(certificate["exact_five_frontier"]["pair_systems"] == 128616, "exact-five pair count")
    need(certificate["exact_five_frontier"]["nonfour_D3_orbit_allowance"] == 3767184, "exact-five allowance")
    need(certificate["at_least_six_frontier"]["pair_systems"] == 2740, "six-active pair count")
    need(certificate["at_least_six_frontier"]["nonfour_D3_orbit_allowance"] == 79520, "six-active allowance")
    need(
        certificate["exact_five_frontier"]["nonfour_D3_orbit_allowance"]
        + certificate["at_least_six_frontier"]["nonfour_D3_orbit_allowance"]
        == certificate["global_reconciliation"]["nonfour_D3_orbit_allowance"],
        "mode allowance partition",
    )
    need(certificate["explicit_interface"]["action_order"] == list(ACTION_ORDER), "action order")
    need(certificate["all_exact_five_pairs_have_h4171_constraint_avoiding_extension"], "extension flag")
    need(certificate["global_representatives_not_chamber_restricted"], "chamber warning")
    need(certificate["whole_pair_systems_removed"] == 0, "pair-system scope")
    need(not certificate["six_active_gate_closed"] and not certificate["record_improvement"], "claim scope")


def compute(submitted, export_interface=None):
    with tempfile.TemporaryDirectory(prefix="hn-five-orbit-check-") as directory:
        pencil_path = Path(directory) / "pencil-interface.json"
        pencil_certificate = PENCIL.compute(pencil_path)
        pencil = json.loads(pencil_path.read_text())

    factors, degrees, group = named_curve_group()
    need(digest(factors) == pencil["curve_inventory_sha256"], "curve inventory alignment")
    rows_by_mode = {}
    summaries = {}
    for mode in MODES:
        rows, summary = rows_and_summary(pencil["pair_representatives"][mode], degrees, group)
        rows_by_mode[mode] = rows
        summaries[mode] = summary

    interface = {
        "schema": "hn-radix-five-active-orbit-interface-v1",
        "curve_inventory_sha256": digest(factors),
        "action_order": ACTION_ORDER,
        "row_format": [
            "curve_a",
            "curve_b",
            "setwise_stabilizer_mask_in_action_order",
            "P1xP1_intersection_bound_2kl",
            "nonfour_stabilizer_orbit_allowance",
        ],
        "pair_modes": rows_by_mode,
        "scope": (
            "Global h4117 pair representatives after h4139 and h4167, stratified by "
            "h4171 exact-five compatibility. Stabilizer masks use the named global D3 "
            "action and must not be combined with a chamber restriction. Allowances are "
            "upper bounds, not distinct-root counts."
        ),
    }
    encoded = json.dumps(interface, sort_keys=True, separators=(",", ":")) + "\n"
    if export_interface is not None:
        path = Path(export_interface)
        if path.exists():
            raise FileExistsError(path)
        path.write_text(encoded)

    all_pairs = sorted(row[:2] for rows in rows_by_mode.values() for row in rows)
    all_rows = [row for rows in rows_by_mode.values() for row in rows]
    _, combined = rows_and_summary(all_pairs, degrees, group)
    six_pairs = (
        pencil["pair_representatives"][MODES[1]]
        + pencil["pair_representatives"][MODES[2]]
    )
    _, at_least_six = rows_and_summary(six_pairs, degrees, group)
    need(
        submitted["sources"]["five_active_pencil_certificate_sha256"]
        == file_digest(ROOT / "hadwiger_nelson_radix_five_active_pencil" / "certificate.json"),
        "h4171 certificate digest",
    )
    reflection = ROOT / "hadwiger_nelson_radix_reflection_axes"
    need(
        submitted["sources"]["reflection_axis_frontier_effect_sha256"]
        == file_digest(reflection / "FRONTIER_EFFECT.json"),
        "h4175 frontier digest",
    )
    need(
        submitted["sources"]["reflection_axis_certificate_sha256"]
        == file_digest(reflection / "certificate.json"),
        "h4175 certificate digest",
    )
    need(submitted["sources"]["curve_inventory_sha256"] == digest(factors), "submitted curve digest")
    need(submitted["sources"]["retained_pair_inventory_sha256"] == digest(all_pairs), "submitted pair digest")
    need(submitted["mode_summaries"] == summaries, "mode summaries")
    need(submitted["exact_five_frontier"] == summaries[MODES[0]], "exact-five result")
    need(submitted["at_least_six_frontier"] == at_least_six, "six-active result")
    need(submitted["global_reconciliation"] == combined, "global reconciliation")
    need(submitted["explicit_interface"]["bytes"] == len(encoded.encode()), "interface bytes")
    need(
        submitted["explicit_interface"]["canonical_json_sha256"] == digest(interface),
        "interface canonical digest",
    )
    need(
        submitted["explicit_interface"]["file_sha256"]
        == hashlib.sha256(encoded.encode()).hexdigest(),
        "interface file digest",
    )
    need(submitted["explicit_interface"]["row_count"] == len(all_rows), "interface rows")
    need(
        submitted["all_exact_five_pairs_have_h4171_constraint_avoiding_extension"]
        == pencil_certificate["pair_frontier"]["all_exact_five_pairs_have_constraint_avoiding_extension"],
        "h4171 extension result",
    )
    precheck(submitted)
    return submitted


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--export-interface", type=Path)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    submitted = json.loads(args.certificate.read_text())
    precheck(submitted)
    actual = compute(submitted, args.export_interface)
    need(actual == submitted, "certificate mismatch")
    if args.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        projection = {
            "status": "FIVE_ACTIVE_FREE_ACTION_INTERFACE_VERIFIED",
            "exact_five_pair_systems": actual["exact_five_frontier"]["pair_systems"],
            "exact_five_nonfour_D3_orbit_allowance": actual["exact_five_frontier"]["nonfour_D3_orbit_allowance"],
            "pair_systems_requiring_at_least_six": actual["at_least_six_frontier"]["pair_systems"],
            "at_least_six_nonfour_D3_orbit_allowance": actual["at_least_six_frontier"]["nonfour_D3_orbit_allowance"],
            "global_nonfour_D3_orbit_allowance": actual["global_reconciliation"]["nonfour_D3_orbit_allowance"],
            "whole_pair_systems_removed": actual["whole_pair_systems_removed"],
            "record_improvement": actual["record_improvement"],
        }
        need(projection == expected, "expected projection")
    print(json.dumps(actual, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
