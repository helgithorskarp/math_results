#!/usr/bin/env python3
"""Check exact integration of the root census with HN2's h4185 interface."""

import argparse
import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def compute(root_interface, anchor_interface):
    roots = json.loads(Path(root_interface).read_text())
    anchor = json.loads(Path(anchor_interface).read_text())
    need(digest(roots) == "8a20abdaeee5b06d4c2851945ae03cae8b56879afca5f7af59be675a88475c64", "root interface")
    need(digest(anchor) == "5496087ac2e75104443c73022ec58bdcc71bb3bafb4605c79aed487fdd3f1da3", "h4185 interface")
    effect = json.loads(
        (ROOT / "hadwiger_nelson_radix_first_step_anchor" / "FRONTIER_EFFECT.json").read_text()
    )
    need(effect["export_interface_sha256"] == digest(anchor), "h4185 frontier binding")

    pairs = sorted(tuple(entry["pair"]) for entry in roots["entries"])
    removed = sorted(tuple(row[:2]) for row in anchor["removed"])
    pair_set = set(pairs)
    removed_set = set(removed)
    extra_rows = sorted(row for row in anchor["removed"] if tuple(row[:2]) not in pair_set)
    inside_rows = sorted(row for row in anchor["removed"] if tuple(row[:2]) in pair_set)
    anchors = sorted({entry["anchor_curve"] for entry in roots["entries"]})
    need(len(pairs) == len(pair_set) == 400, "400 distinct root-census pairs")
    need(pair_set <= removed_set and len(inside_rows) == 400, "every root pair removed by h4185")
    need(len(extra_rows) == 24, "24 additional at-least-six anchor pairs")
    need(anchors == anchor["anchor_curves"], "identical six anchor curves")
    need(sum(row[4] for row in inside_rows) == 2904, "root-stratum prior allowance")
    need(sum(row[4] for row in extra_rows) == 108, "additional h4185 allowance")
    need(2330 + 574 + 108 == effect["removed_orbit_allowance"], "allowance reconciliation")

    return {
        "anchor_curves": anchors,
        "h4185": {
            "additional_at_least_six_anchor_pairs": len(extra_rows),
            "additional_at_least_six_allowance": sum(row[4] for row in extra_rows),
            "all_root_census_pairs_removed": True,
            "artifact_ref": "bafkreih7dzrfyq3uhwyiw6jkqhu7uzj2wtmre6sdax34rl34iw2syi73ty",
            "exact_five_anchor_pairs": len(inside_rows),
            "export_interface_sha256": digest(anchor),
            "post_frontier": {
                "at_least_six_allowance": effect["remaining_at_least_six_allowance"],
                "at_least_six_pairs": effect["remaining_at_least_six_pairs"],
                "exact_five_allowance": effect["remaining_exact_five_allowance"],
                "exact_five_pairs": effect["remaining_exact_five_pairs"],
                "global_allowance": effect["remaining_global_allowance"],
                "global_pairs": effect["remaining_global_pairs"],
            },
            "removed_pair_sha256": digest(removed),
            "removed_pairs": len(removed),
            "removed_pairs_outside_root_census_sha256": digest(
                sorted(tuple(row[:2]) for row in extra_rows)
            ),
            "source_commit": "c67e7e5053e320672bb9aa745c400e5d4e5402af",
        },
        "root_census": {
            "eligible_orbit_allowance_before_h4185": 574,
            "interface_sha256": digest(roots),
            "pair_allowance_before_root_census": sum(row[4] for row in inside_rows),
            "pair_sha256": digest(pairs),
            "pairs": len(pairs),
            "root_census_reduction": 2330,
            "superseded_as_live_allowance": True,
        },
        "total_h4185_removed_allowance_reconciliation": {
            "h4185_removed_allowance": effect["removed_orbit_allowance"],
            "identity": "2330+574+108=3012",
            "verified": True,
        },
        "record_improvement": False,
        "status": "H4185_ANCHOR_REMOVAL_EXACTLY_CONTAINS_ROOT_CENSUS",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--roots", type=Path, required=True)
    parser.add_argument("--anchor", type=Path, required=True)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = compute(args.roots, args.anchor)
    if args.check_expected:
        need(result == json.loads((HERE / "INTEGRATION.json").read_text()), "integration certificate")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
