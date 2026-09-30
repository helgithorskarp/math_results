#!/usr/bin/env python3
"""Check all48 root/cap trees; label the class29 numerical premise explicitly."""
import argparse, hashlib, importlib.util, json, time
from pathlib import Path

TREE_PATH = Path(__file__).resolve().parent.parent / "van_der_waerden_27_qr617_class29_disjunction/verify.py"
spec = importlib.util.spec_from_file_location("qr617_62_unchanged_tree_checker", TREE_PATH)
tree = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tree)
core = tree.core
D, COLORS = tree.D, tree.COLORS
FORMAT, TRACE_FORMAT = tree.FORMAT, tree.TRACE_FORMAT
require, replay, verify_tree = tree.require, tree.replay, tree.verify_tree
BOXES = {e: [[29, 32], [30, 31], [31, 30], [32, 29]] for e in (0, 1)}
CLASS29 = "bafkreigdc2r7hp4snvr5h3sqwtzth6bcx7ocbtcpzabiodifflmb36ewrq"


def cases():
    return [(e, root, B) for e in (0, 1) for B in BOXES[e]
            for root in sorted(core.endpoint_points(core.ENDPOINT_APS[e], e))]


def filename(e, root, B):
    return f"tree-{e}-{root}-{B[0]}-{B[1]}.json"


def required_names():
    return sorted(filename(*case) for case in cases())


def arithmetic_bridge():
    # A boundary regression; PROOF.md gives the full quantified argument.
    for a in range(29, 34):
        for b in range(29, 34):
            if a + b <= 61:
                require(any(a <= A and b <= B for A, B in BOXES[0]),
                        "Uncovered low-total pair")
    pairs = [[a, 62-a] for a in range(29, 34)]
    require(pairs == [[29, 33], [30, 32], [31, 31], [32, 30], [33, 29]], "Wrong boundary pairs")
    require(3696 - 62 == 3634 and 1848 - 29 == 1819 and 1848 - 31 == 1817,
            "Incorrect complement arithmetic")
    return pairs


def verify_suite(bundle):
    core.check_domain()
    require(set(bundle) == set(required_names()), "Missing, extra or unexpected root/cap coverage")
    results = []
    for e, root, B in cases():
        data = bundle[filename(e, root, B)]
        require((data.get("endpoint"), data.get("root"), data.get("budget")) == (e, root, B),
                "Wrong quantified endpoint/root/cap case")
        result = verify_tree(data)
        require(result["closed"], "An open tree cannot prove a box exclusion")
        results.append(result)
    pairs = arithmetic_bridge()
    return {"verified": True, "verified_claim": "Both endpoints exclude the four displayed joint-budget boxes",
            "branches_checked": len(results), "nodes_checked": sum(r["nodes"] for r in results),
            "splits_checked": sum(r["splits"] for r in results),
            "leaves_checked": sum(len(r["leaves"]) for r in results),
            "excluded_boxes_by_endpoint": {str(e): BOXES[e] for e in (0, 1)}, "both_endpoint_values_covered": True,
            "original_class_sizes": [1848, 1848], "exceptional_prefix_positions_free": 7,
            "earlier_numerical_bounds_used_by_new_branch_replay": False,
            "direct_independent_consequence": {"max_of_original_class_edit_counts_at_least": 31,
                                              "min_of_original_class_edit_counts_at_most": 1817},
            "corollary_given_cited_uniform_class29_premise": {
                "premise_graph_ref": CLASS29, "premise_reproved_by_this_command": False,
                "each_original_class_edit_bounds": [29, 1819], "total_edit_bounds": [62, 3634],
                "remaining_total62_pairs_by_endpoint": {str(e): pairs for e in (0, 1)}},
            "step_totals": {key: sum(r["step_totals"][key] for r in results)
                            for key in ("forbidden", "forced", "packing", "empty", "mixed", "budget")},
            "branch_results": results}


def verify_directory(directory, expected=None):
    bundle, manifest = {}, []
    found = {p.name for p in directory.glob("tree-*.json")}
    require(found == set(required_names()), "Directory lacks exact root/cap file coverage")
    for name in required_names():
        raw = (directory / name).read_bytes()
        bundle[name] = json.loads(raw)
        manifest.append({"file": name, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
    result = verify_suite(bundle)
    if expected is not None:
        require(manifest == expected.get("certificates"), "Certificate bytes differ from expected manifest")
        require(result == expected.get("verification"), "Checking results differ from expected data")
    return manifest, result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--expected", type=Path)
    parser.add_argument("--write-expected", type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    expected = json.loads(args.expected.read_text()) if args.expected else None
    manifest, result = verify_directory(args.directory, expected)
    if args.write_expected:
        args.write_expected.write_text(json.dumps({"certificates": manifest, "verification": result}, indent=2) + "\n")
    print(json.dumps({k: value for k, value in result.items() if k != "branch_results"}, sort_keys=True))
    print(json.dumps({"checking_seconds": round(time.monotonic()-start, 3)}))


if __name__ == "__main__":
    main()
