#!/usr/bin/env python3
"""Check the24 new joint-budget branches; the60-edit corollary cites prior class29."""
import argparse
import hashlib
import importlib.util
import json
import time
from pathlib import Path

CORE_PATH = Path(__file__).resolve().parent.parent / "van_der_waerden_27_qr617_mixed_edit_region/verify.py"
spec = importlib.util.spec_from_file_location("qr617_joint_checker_core", CORE_PATH)
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)
verify_branch = core.verify_branch
check_packing = core.check_packing
require = core.require
COLORS, D = core.COLORS, core.D
LAST = core.LAST
ENDPOINT_APS = {0: [1, 617], 1: [3421, 47]}
BOXES = {0: [(29, 30), (30, 29)], 1: [(29, 30), (30, 29)]}
CLASS29_GRAPH_REF = "bafkreigdc2r7hp4snvr5h3sqwtzth6bcx7ocbtcpzabiodifflmb36ewrq"


def required_names():
    return [f"branch-{e}-{root}-{a}-{b}.json"
            for e, pair in ENDPOINT_APS.items()
            for a, b in BOXES[e] for root in sorted(core.endpoint_points(pair, e))]


def arithmetic_bridge():
    """Finite boundary check; PROOF.md supplies the all-counts written argument."""
    for total in range(60):
        for a in range(total + 1):
            b = total - a
            if min(a, b) < 29:
                continue
            require(any(a <= x and b <= y for x, y in BOXES[0]),
                    "Uncovered total<=59 given the cited class29 premise")
    pairs = [[a, 60 - a] for a in range(61) if a >= 29 and 60 - a >= 29]
    require(pairs == [[29, 31], [30, 30], [31, 29]], "Wrong next total60 frontier")
    require(all(all(not (a <= x and b <= y) for x, y in BOXES[0]) for a, b in pairs),
            "Reported frontier lies in an excluded box")
    require(2 * 1848 - 60 == 3636 and 1848 - 29 == 1819,
            "Incorrect complement arithmetic")
    return pairs


def verify_suite(bundle):
    core.check_domain()
    require(isinstance(bundle, dict) and set(bundle) == set(required_names()),
            "Missing, duplicated or unexpected root/cap coverage")
    results = []
    for e, pair in ENDPOINT_APS.items():
        roots = sorted(core.endpoint_points(pair, e))
        require(len(roots) == 6, "Endpoint root cover has wrong size")
        for a, b in BOXES[e]:
            for root in roots:
                name = f"branch-{e}-{root}-{a}-{b}.json"
                data = bundle[name]
                require(isinstance(data, dict) and data.get("endpoint") == e and
                        data.get("root") == root and data.get("budget") == [a, b],
                        "Wrong quantified root/cap case")
                results.append(verify_branch(data))
    pairs = arithmetic_bridge()
    return {"verified": True,
            "verified_claim": "The four displayed joint-budget boxes are excluded",
            "branches_checked": len(results),
            "excluded_boxes_by_endpoint": {str(e): [list(B) for B in BOXES[e]] for e in (0, 1)},
            "original_class_sizes": [1848, 1848],
            "exceptional_prefix_positions_free": 7,
            "both_endpoint_values_covered": True,
            "earlier_numerical_bounds_used_by_new_branch_replay": False,
            "corollary_given_cited_uniform_class29_premise": {
                "premise_graph_ref": CLASS29_GRAPH_REF,
                "premise_reproved_by_this_command": False,
                "total_edit_bounds": [60, 3636], "each_original_class_edit_bounds": [29, 1819],
                "remaining_total60_pairs_by_endpoint": {"0": pairs, "1": pairs}},
            "branch_results": results}


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
        require(result == expected.get("verification"), "Checking differs from expected results")
    return {"certificates": manifest, "verification": result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--expected", type=Path)
    parser.add_argument("--write-expected", type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    expected = json.loads(args.expected.read_text()) if args.expected else None
    result = verify_directory(args.directory, expected)
    if args.write_expected:
        args.write_expected.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: value for k, value in result["verification"].items()
                      if k != "branch_results"}, sort_keys=True))
    print(json.dumps({"checking_seconds": round(time.monotonic() - start, 3)}, sort_keys=True))


if __name__ == "__main__":
    main()
