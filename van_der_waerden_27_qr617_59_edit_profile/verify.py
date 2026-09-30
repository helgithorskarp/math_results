#!/usr/bin/env python3
"""Exact QR617 59-edit profile checker; replay uses the published Euler/set core."""
import argparse
import hashlib
import importlib.util
import json
import time
from pathlib import Path

CORE_PATH = Path(__file__).resolve().parent.parent / "van_der_waerden_27_qr617_mixed_edit_region/verify.py"
spec = importlib.util.spec_from_file_location("qr617_profile_checker_core", CORE_PATH)
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)

# Re-export the exact AP interpretation for certificate rejection controls.
verify_branch = core.verify_branch
check_packing = core.check_packing
require = core.require
COLORS, D, LAST = core.COLORS, core.D, core.LAST
ENDPOINT_APS = {0: [1, 617], 1: [3421, 47]}
BOXES = {0: [(27, 1848), (1848, 28), (29, 29), (28, 30)],
         1: [(28, 1848), (1848, 28), (29, 29)]}


def required_names():
    return [f"branch-{e}-{root}-{a}-{b}.json"
            for e, pair in ENDPOINT_APS.items()
            for a, b in BOXES[e] for root in sorted(core.endpoint_points(pair, e))]


def lower_condition(endpoint, a, b):
    if endpoint == 0:
        return a >= 28 and b >= 29 and max(a, b) >= 30 and (a >= 29 or b >= 31)
    return a >= 29 and b >= 29 and max(a, b) >= 30


def arithmetic_bridge():
    """Check the small integer boundary; PROOF.md supplies the quantified bridge."""
    boundary = list(range(61)) + [1817, 1818, 1819, 1820, 1848]
    pairs_at_59 = {}
    for e in (0, 1):
        for a in boundary:
            for b in boundary:
                avoids_boxes = all(not (a <= x and b <= y) for x, y in BOXES[e])
                require(avoids_boxes == lower_condition(e, a, b), "Incorrect box-to-profile bridge")
        for a in range(59):
            for b in range(59 - a):
                require(any(a <= x and b <= y for x, y in BOXES[e]), "Uncovered total at most58")
        pairs_at_59[str(e)] = [[a, 59 - a] for a in range(60)
                              if lower_condition(e, a, 59 - a)]
    require(pairs_at_59 == {"0": [[28, 31], [29, 30], [30, 29]],
                           "1": [[29, 30], [30, 29]]}, "Incorrect remaining total59 frontier")
    require(2 * 1848 - 59 == 3637 and 1848 - 29 == 1819 and
            1848 - 28 == 1820 and 1848 - 30 == 1818 and 1848 - 31 == 1817,
            "Incorrect complement arithmetic")
    return pairs_at_59


def verify_suite(bundle):
    core.check_domain()
    require(set(bundle) == set(required_names()), "Missing, duplicated, or unexpected case coverage")
    results = []
    for e, pair in ENDPOINT_APS.items():
        roots = sorted(core.endpoint_points(pair, e))
        require(len(roots) == 6, "Endpoint cover has wrong size")
        for a, b in BOXES[e]:
            for root in roots:
                name = f"branch-{e}-{root}-{a}-{b}.json"
                data = bundle[name]
                require(data.get("endpoint") == e and data.get("root") == root and
                        data.get("budget") == [a, b], "Wrong quantified branch")
                results.append(verify_branch(data))
    remaining = arithmetic_bridge()
    return {"verified": True, "branches_checked": len(results),
            "original_class_sizes": [1848, 1848], "total_edit_bounds": [59, 3637],
            "minimum_changes_by_endpoint": {"0": [28, 29], "1": [29, 29]},
            "maximum_changes_by_endpoint": {"0": [1819, 1819], "1": [1820, 1819]},
            "maximum_of_edit_counts_at_least": 30, "minimum_of_edit_counts_at_most": 1818,
            "endpoint0_lower_corner": "a>=29 or b>=31",
            "endpoint1_upper_corner": "a<=1819 or b<=1817",
            "remaining_total59_pairs_by_endpoint": remaining,
            "exceptional_prefix_positions_free": 7, "both_endpoint_values_covered": True,
            "external_numerical_cut_assumptions": 0, "branch_results": results}


def verify_directory(directory, expected=None):
    bundle, manifest = {}, []
    for name in required_names():
        raw = (directory / name).read_bytes()
        bundle[name] = json.loads(raw)
        manifest.append({"file": name, "bytes": len(raw),
                         "sha256": hashlib.sha256(raw).hexdigest()})
    result = verify_suite(bundle)
    if expected is not None:
        require(manifest == expected.get("certificates"), "Bytes differ from reference manifest")
        require(result == expected.get("verification"), "Verification differs from expected results")
    return {"certificates": manifest, "verification": result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--expected", type=Path)
    parser.add_argument("--write-expected", type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    expected = json.loads(args.expected.read_text()) if args.expected else None
    checked = verify_directory(args.directory, expected)
    if args.write_expected:
        args.write_expected.write_text(json.dumps(checked, indent=2) + "\n")
    print(json.dumps({k: v for k, v in checked["verification"].items() if k != "branch_results"},
                     sort_keys=True))
    print(json.dumps({"checking_seconds": round(time.monotonic() - start, 3)}, sort_keys=True))


if __name__ == "__main__":
    main()
