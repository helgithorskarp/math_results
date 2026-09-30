#!/usr/bin/env python3
"""Replay the four endpoint-one root covers and the separate total64 corollary."""
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
spec = importlib.util.spec_from_file_location("qr617_endpoint64_unchanged_tree_checker", TREE_PATH)
tree = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tree)
core = tree.core
D, COLORS = tree.D, tree.COLORS
FORMAT, TRACE_FORMAT = tree.FORMAT, tree.TRACE_FORMAT
require, replay, verify_tree = tree.require, tree.replay, tree.verify_tree
BUDGETS = [[30, 33], [31, 32], [32, 31], [33, 30]]
NUMERIC_PREMISES = [
    "bafkreibznuuclypj37y3zawaphzeh5dgnvduhwqlt5runpxa7dl55b6izy",
    "bafkreica4jwle5gkif5zzbowoflfreqhas5caz5hpi73fzd43s342m3ykq",
]


def roots_for(e):
    require(type(e) is int and e in (0, 1), "Invalid actual endpoint")
    ap = core.ENDPOINT_APS[e]
    terms = [ap[0] + i * ap[1] for i in range(7)]
    require(ap[1] > 0 and terms[-1] == 3703 and
            all(x in D and COLORS[x] == e for x in terms[:-1]),
            "Invalid endpoint monochromatic root cover")
    roots = sorted(core.endpoint_points(ap, e))
    require(roots == sorted(terms[:-1]) and len(roots) == 6,
            "Incomplete independently derived outer cover")
    return roots


def cases():
    return [(e, root, B.copy()) for e in (1,) for B in BUDGETS
            for root in roots_for(e)]


def filename(e, root, B):
    return f"tree-{e}-{root}-{B[0]}-{B[1]}.json"


def required_names():
    return sorted(filename(*case) for case in cases())


def verify_box(bundle, e, B):
    require(type(e) is int and e == 1 and B in BUDGETS, "Unsupported endpoint-one original-class box")
    roots = roots_for(e)
    names = [filename(e, root, B) for root in roots]
    require(set(bundle) == set(names), "Missing or extra asymmetric root")
    for root, name in zip(roots, names):
        data = bundle[name]
        require(type(data.get("endpoint")) is int and type(data.get("root")) is int and
                (data.get("endpoint"), data.get("root"), data.get("budget")) == (e, root, B),
                "Wrong quantified asymmetric endpoint/root/budget")
    results = [verify_tree(bundle[name]) for name in names]
    require(all(r["closed"] for r in results), "An open root is not a box exclusion")
    return results


def arithmetic_bridge():
    # External numerical premises are stated explicitly, never assumed by
    # the new branch replay. The floor30 alone yields endpoint-one lower64.
    require([sum(COLORS[x] == c for x in D) for c in (0, 1)] == [1848, 1848],
            "Wrong original class sizes")
    provenance = json.loads((Path(__file__).resolve().parent / "provenance.json").read_text())
    for dependency in provenance["numerical_dependencies"]:
        for name,digest in dependency["files"].items():
            require(hashlib.sha256((BASE/dependency["directory"]/name).read_bytes()).hexdigest() == digest,
                    "Changed cited numerical source: " + dependency["directory"] + "/" + name)
    pairs = [[a,b] for a in range(30,34) for b in range(30,64-a)]
    require(len(pairs) == 10, "Incomplete low-total integer domain")
    coverage = []
    for a,b in pairs:
        eligible = [B for B in BUDGETS if a <= B[0] and b <= B[1]]
        require(eligible, "Uncovered low-total pair")
        coverage.append({"pair":[a,b], "excluded_by_original_box":eligible[0].copy()})
    omissions = []
    for i,B in enumerate(BUDGETS):
        other = BUDGETS[:i]+BUDGETS[i+1:]
        require(not any(B[0] <= C[0] and B[1] <= C[1] for C in other),
                "Omitted-box control has no uncovered case")
        omissions.append({"omitted_original_box":B.copy(),"uncovered_total63_pair":B.copy()})
    require(2*1848-64 == 3632, "Incorrect complement arithmetic")
    at64 = [[a,64-a] for a in range(30,35)]
    require(all(not any(a<=B[0] and b<=B[1] for B in BUDGETS) for a,b in at64),
            "This cohort unexpectedly claims total64 exclusion")
    at63 = [[a,63-a] for a in range(30,34)]
    return {"minimal_lower64_premise_graph_refs":[NUMERIC_PREMISES[0]],
            "combined_profile_additional_premise_graph_refs":[NUMERIC_PREMISES[1]],
            "numerical_premises_reproved_by_this_command":False,
            "pinned_numerical_source_hashes_checked":True,
            "class_bounds_both_endpoints_given_cited_profile":[30,1818],
            "total_bounds_by_endpoint_given_cited_profile":{"0":[63,3632],"1":[64,3633]},
            "low_total_integer_pair_coverage":coverage,"omitted_box_controls":omissions,
            "complement_map":"(e,a,b)->(1-e,1848-a,1848-b)",
            "remaining_lower_boundary_pairs_by_endpoint":{"0":at63,"1":at64},
            "remaining_upper_boundary_pairs_by_endpoint":{
                "0":sorted([[1848-a,1848-b] for a,b in at64]),
                "1":sorted([[1848-a,1848-b] for a,b in at63])},
            "uniform_lower64_or_boundary_feasibility_asserted":False}


def verify_suite(bundle):
    core.check_domain()
    require(set(bundle) == set(required_names()), "Incomplete four-box root coverage")
    boxes, all_results = [], []
    for e in (1,):
        for B in BUDGETS:
            names = [filename(e, root, B) for root in roots_for(e)]
            results = verify_box({name: bundle[name] for name in names}, e, B)
            boxes.append({"endpoint": e, "excluded_original_budget": B.copy(),
                          "roots": roots_for(e), "root_results": results})
            all_results.extend(results)
    return {"verified": True,
            "independent_lemma": "All four ORIGINAL boxes30/33,31/32,32/31,33/30 are excluded at endpoint1",
            "root_cases_checked": len(all_results),
            "nodes_checked": sum(r["nodes"] for r in all_results),
            "splits_checked": sum(r["splits"] for r in all_results),
            "leaves_checked": sum(len(r["leaves"]) for r in all_results),
            "original_class_sizes": [1848, 1848], "exceptional_prefix_positions_free": 7,
            "actual_periodicity_or_symmetry_assumed": False,
            "earlier_numerical_bounds_used_by_new_branch_replay": False,
            "conditional_endpoint64_corollary": arithmetic_bridge(),
            "length3704_witness_or_global_W_bound_or_unrestricted_nonexistence_asserted": False,
            "step_totals": {k: sum(r["step_totals"][k] for r in all_results)
                            for k in ("forbidden", "forced", "packing", "empty", "mixed", "budget")},
            "boxes": boxes}


def verify_directory(directory, expected=None):
    found = {p.name for p in directory.glob("tree-*.json")}
    require(found == set(required_names()), "Directory lacks exact24-file case coverage")
    bundle, manifest = {}, []
    for name in required_names():
        raw = (directory / name).read_bytes()
        bundle[name] = json.loads(raw)
        manifest.append({"file": name, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
    result = verify_suite(bundle)
    if expected is not None:
        require(manifest == expected.get("certificates"), "Certificate bytes differ from expected manifest")
        require(result == expected.get("verification"), "Complete checked results differ from expected data")
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
    print(json.dumps({k: value for k, value in result.items() if k != "boxes"}, sort_keys=True))
    print(json.dumps({"checking_seconds": round(time.monotonic()-start, 3)}))


if __name__ == "__main__":
    main()
