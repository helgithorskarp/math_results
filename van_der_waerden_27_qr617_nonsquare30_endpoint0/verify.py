#!/usr/bin/env python3
"""Replay six endpoint-zero trees for the original-class cap (1848,29)."""
import argparse
import hashlib
import importlib.util
import json
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DEPENDENCIES = {
    "van_der_waerden_27_qr617_mixed_edit_region/generate.py":
        "f822a963f9bb6e490dcbd7fbe635dcba87889337b32c0efe8e5fdf3d28607653",
    "van_der_waerden_27_qr617_mixed_edit_region/verify.py":
        "38ba46f4f22d01ab7df79f1bb20ad7ab190230cf90a29ff1ab3b678e97e2eb33",
    "van_der_waerden_27_qr617_class29_disjunction/verify.py":
        "579763d952c364963692638d125e9ff71c6ed9add1f3e4999462bac2e8e7c0af",
}
for relative, digest in DEPENDENCIES.items():
    if hashlib.sha256((BASE / relative).read_bytes()).hexdigest() != digest:
        raise ValueError("Changed computational dependency: " + relative)

TREE_PATH = BASE / "van_der_waerden_27_qr617_class29_disjunction/verify.py"
spec = importlib.util.spec_from_file_location("qr617_nonsquare30_unchanged_tree_checker", TREE_PATH)
tree = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tree)
core = tree.core
D, COLORS = tree.D, tree.COLORS
FORMAT, TRACE_FORMAT = tree.FORMAT, tree.TRACE_FORMAT
require, replay, verify_tree = tree.require, tree.replay, tree.verify_tree
BUDGET = [1848, 29]
SQUARE30 = "bafkreifgkgk7nhqgg37tn2uevjg7u7zkmqobvmn4nvqycqp6bsba4vzfdq"
PROFILE62 = "bafkreieu7guaiaarct57a7ohr2y32mcvgc5d4uwaj6kwodienf3o5u2i2e"


def cases():
    return [(0, root, BUDGET.copy())
            for root in sorted(core.endpoint_points(core.ENDPOINT_APS[0], 0))]


def filename(e, root, B):
    return f"tree-{e}-{root}-{B[0]}-{B[1]}.json"


def required_names():
    return sorted(filename(*case) for case in cases())


def arithmetic_bridge():
    # PROOF.md proves the complement map and cites separate square30/62
    # numerical premises. This arithmetic check does not replay those proofs.
    require(sum(COLORS[x] == 0 for x in D) == 1848 and
            sum(COLORS[x] == 1 for x in D) == 1848, "Wrong original class sizes")
    require(1848-30 == 1818 and 1848-29 == 1819 and 3696-62 == 3634,
            "Incorrect complement arithmetic")
    return {"0": [[a, 62-a] for a in range(30, 33)],
            "1": [[a, 62-a] for a in range(30, 34)]}


def verify_suite(bundle):
    core.check_domain()
    require(set(bundle) == set(required_names()),
            "Missing, extra or unexpected endpoint-zero nonsquare root coverage")
    for e, root, B in cases():
        data = bundle[filename(e, root, B)]
        require(type(data.get("endpoint")) is int and type(data.get("root")) is int and
                (data.get("endpoint"), data.get("root"), data.get("budget")) == (e, root, B),
                "Wrong quantified original-class full-width endpoint/root/cap case")
    results = []
    for case in cases():
        result = verify_tree(bundle[filename(*case)])
        require(result["closed"], "An open tree cannot prove the nonsquare30 lemma")
        results.append(result)
    return {"verified": True,
            "verified_independent_lemma": "Endpoint0 implies at least30 original-q1 edits; original-q0 edits unrestricted",
            "endpoint": 0, "excluded_budget": BUDGET.copy(),
            "required_roots": [root for _, root, _ in cases()],
            "roots_checked": len(results), "nodes_checked": sum(r["nodes"] for r in results),
            "splits_checked": sum(r["splits"] for r in results),
            "leaves_checked": sum(len(r["leaves"]) for r in results),
            "original_class_sizes": [1848, 1848], "exceptional_prefix_positions_free": 7,
            "earlier_numerical_bounds_used_by_new_branch_replay": False,
            "complement_consequence": "Endpoint1 implies at most1818 original-q1 edits",
            "uniform_both_endpoint_nonsquare30_or_total63_asserted": False,
            "conditional_corollary_given_cited_square30_and_62": {
                "premise_graph_refs": [SQUARE30, PROFILE62], "premise_reproved_by_this_command": False,
                "original_class0_bounds_both_endpoints": [30, 1818],
                "original_class1_bounds_by_endpoint": {"0": [30, 1819], "1": [29, 1818]},
                "total_edit_bounds": [62, 3634],
                "remaining_total62_pairs_by_endpoint": arithmetic_bridge(),
                "boundary_feasibility_or_attained_minimum_asserted": False},
            "step_totals": {key: sum(r["step_totals"][key] for r in results)
                            for key in ("forbidden", "forced", "packing", "empty", "mixed", "budget")},
            "root_results": results}


def verify_directory(directory, expected=None):
    bundle, manifest = {}, []
    found = {p.name for p in directory.glob("tree-*.json")}
    require(found == set(required_names()),
            "Directory lacks exact endpoint-zero nonsquare root/cap file coverage")
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
        args.write_expected.write_text(json.dumps({"certificates": manifest, "verification": result}, indent=2)+"\n")
    print(json.dumps({k: value for k, value in result.items() if k != "root_results"}, sort_keys=True))
    print(json.dumps({"checking_seconds": round(time.monotonic()-start, 3)}))


if __name__ == "__main__":
    main()
