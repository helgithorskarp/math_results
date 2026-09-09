#!/usr/bin/env python3
"""Produce the mode-specific free-action interface for the A5 pair frontier."""

import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PENCIL = load(
    "five_orbit_pencil_producer",
    ROOT / "hadwiger_nelson_radix_five_active_pencil" / "produce.py",
)
REFLECTION = ROOT / "hadwiger_nelson_radix_reflection_axes"
sys.path.insert(0, str(REFLECTION))
FREE = load("five_orbit_reflection_accounting", REFLECTION / "free_action.py")

ACTION_ORDER = ("1", "R", "R^2", "C", "RC", "R^2C")
MODES = (
    "exact_five_compatible",
    "parallel_signatures_require_at_least_six",
    "unrealized_pencil_type_requires_at_least_six",
)


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def file_digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def output_map(counter):
    return {str(key): value for key, value in sorted(counter.items())}


def summarize(rows):
    histogram = Counter()
    bidegree_sums = Counter()
    orbit_sums = Counter()
    total_degree = bidegree = rotation_free = orbit_allowance = 0
    for _, _, mask, sharp_bound, allowance in rows:
        stabilizer = mask.bit_count()
        rotation_stabilizer = (mask & 7).bit_count()
        histogram[stabilizer] += 1
        bidegree_sums[stabilizer] += sharp_bound
        orbit_sums[stabilizer] += allowance
        total_degree += 2 * sharp_bound
        bidegree += sharp_bound
        rotation_free += sharp_bound // rotation_stabilizer
        orbit_allowance += allowance
    return {
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


def make_rows(pairs, factors, group):
    degrees = [max(i + j for i, j, _ in factor) for factor in factors]
    rows = []
    for pair in pairs:
        a, b = pair
        key = (a, b)
        if not (0 <= a < b < len(factors)):
            raise ValueError("invalid canonical pair")
        images = [tuple(sorted((action[a], action[b]))) for action in group]
        if min(images) != key:
            raise ValueError("pair is not a global D3 representative")
        mask = sum(1 << index for index, image in enumerate(images) if image == key)
        stabilizer = mask.bit_count()
        if stabilizer * len(set(images)) != 6:
            raise ValueError("orbit-stabilizer failure")
        sharp_bound = 2 * (degrees[a] // 2) * (degrees[b] // 2)
        if sharp_bound * 2 != degrees[a] * degrees[b]:
            raise ValueError("unexpected norm-curve bidegree")
        rows.append([a, b, mask, sharp_bound, sharp_bound // stabilizer])
    return rows


def compute(export_interface=None):
    with tempfile.TemporaryDirectory(prefix="hn-five-orbit-produce-") as directory:
        pencil_path = Path(directory) / "pencil-interface.json"
        pencil_certificate = PENCIL.make_certificate(pencil_path)
        pencil = json.loads(pencil_path.read_text())

    factors, group = FREE.curve_group()
    if len(group) != len(ACTION_ORDER):
        raise ValueError("named D3 action order")
    if digest(factors) != pencil["curve_inventory_sha256"]:
        raise ValueError("curve inventory alignment")

    rows_by_mode = {
        mode: make_rows(pencil["pair_representatives"][mode], factors, group)
        for mode in MODES
    }
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

    mode_summaries = {mode: summarize(rows_by_mode[mode]) for mode in MODES}
    all_pairs = sorted(
        [row[:2] for rows in rows_by_mode.values() for row in rows]
    )
    all_rows = [row for rows in rows_by_mode.values() for row in rows]
    combined = summarize(all_rows)
    imported = json.loads((REFLECTION / "FRONTIER_EFFECT.json").read_text())
    if digest(all_pairs) != imported["remaining_pairs_sha256"]:
        raise ValueError("h4167 retained-pair digest")
    if combined["pair_systems"] != imported["global_pair_systems"]:
        raise ValueError("global pair count")
    if combined["nonfour_D3_orbit_allowance"] != imported["remaining_nonfour_D3_orbit_allowance"]:
        raise ValueError("global free-action allowance")
    if combined["product_surface_intersection_allowance"] != imported["bidegree_allowance"]:
        raise ValueError("global product-surface allowance")

    exact = mode_summaries["exact_five_compatible"]
    at_least_six = summarize(
        rows_by_mode["parallel_signatures_require_at_least_six"]
        + rows_by_mode["unrealized_pencil_type_requires_at_least_six"]
    )
    return {
        "schema": "hn-radix-five-active-orbits-v1",
        "sources": {
            "five_active_pencil_certificate_sha256": file_digest(
                ROOT / "hadwiger_nelson_radix_five_active_pencil" / "certificate.json"
            ),
            "reflection_axis_frontier_effect_sha256": file_digest(
                REFLECTION / "FRONTIER_EFFECT.json"
            ),
            "reflection_axis_certificate_sha256": file_digest(
                REFLECTION / "certificate.json"
            ),
            "curve_inventory_sha256": digest(factors),
            "retained_pair_inventory_sha256": digest(all_pairs),
        },
        "mode_summaries": mode_summaries,
        "exact_five_frontier": exact,
        "at_least_six_frontier": at_least_six,
        "global_reconciliation": combined,
        "explicit_interface": {
            "bytes": len(encoded.encode()),
            "canonical_json_sha256": digest(interface),
            "file_sha256": hashlib.sha256(encoded.encode()).hexdigest(),
            "row_count": len(all_rows),
            "action_order": ACTION_ORDER,
        },
        "all_exact_five_pairs_have_h4171_constraint_avoiding_extension": pencil_certificate[
            "pair_frontier"
        ]["all_exact_five_pairs_have_constraint_avoiding_extension"],
        "global_representatives_not_chamber_restricted": True,
        "whole_pair_systems_removed": 0,
        "six_active_gate_closed": False,
        "record_improvement": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--export-interface", type=Path)
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError(args.out)
    certificate = compute(args.export_interface)
    raw = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    args.out.write_text(raw)
    print(
        json.dumps(
            {
                "path": str(args.out),
                "bytes": len(raw.encode()),
                "sha256": hashlib.sha256(raw.encode()).hexdigest(),
                "exact_five_pair_systems": certificate["exact_five_frontier"]["pair_systems"],
                "exact_five_nonfour_D3_orbit_allowance": certificate["exact_five_frontier"][
                    "nonfour_D3_orbit_allowance"
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
