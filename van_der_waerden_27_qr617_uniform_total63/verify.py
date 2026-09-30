#!/usr/bin/env python3
"""Replay the complete asymmetric root covers and the separate uniform63 corollary."""
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
spec = importlib.util.spec_from_file_location("qr617_uniform63_unchanged_tree_checker", TREE_PATH)
tree = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tree)
core = tree.core
D, COLORS = tree.D, tree.COLORS
FORMAT, TRACE_FORMAT = tree.FORMAT, tree.TRACE_FORMAT
require, replay, verify_tree = tree.require, tree.replay, tree.verify_tree
BUDGETS = [[30, 32], [32, 30]]
NUMERIC_PREMISES = [
    "bafkreibznuuclypj37y3zawaphzeh5dgnvduhwqlt5runpxa7dl55b6izy",
    "bafkreihgdtm5j53hqnupmkdhptjvlzeashiqgukum6p63ksj7l4ozqft4q",
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
    return [(e, root, B.copy()) for e in (0, 1) for B in BUDGETS
            for root in roots_for(e)]


def filename(e, root, B):
    return f"tree-{e}-{root}-{B[0]}-{B[1]}.json"


def required_names():
    return sorted(filename(*case) for case in cases())


def verify_box(bundle, e, B):
    require(B in BUDGETS, "Unsupported asymmetric box")
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
    # The two numerical lemmas are explicit external premises. These new
    # branch checks neither assume their bounds nor rerun their proofs.
    require([sum(COLORS[x] == c for x in D) for c in (0, 1)] == [1848, 1848],
            "Wrong original class sizes")
    pairs = [[a, b] for a in range(30, 33) for b in range(30, 63-a)]
    require(pairs == [[30, 30], [30, 31], [30, 32], [31, 30], [31, 31], [32, 30]],
            "Incomplete low-total integer domain")
    coverage = []
    for a, b in pairs:
        if a <= 30 and b <= 32:
            reason = "new_asymmetric30_32"
        elif a <= 31 and b <= 31:
            reason = "cited_both_endpoint_balanced31_31"
        elif a <= 32 and b <= 30:
            reason = "new_asymmetric32_30"
        else:
            raise ValueError("Uncovered low-total pair")
        coverage.append({"pair": [a, b], "excluded_by": reason})
    require(2*1848-63 == 3633, "Incorrect complement arithmetic")
    boundary = [[a, 63-a] for a in range(30, 34)]
    upper = sorted([[1848-a, 1848-b] for a, b in boundary])
    return {"premise_graph_refs": NUMERIC_PREMISES,
            "numerical_premises_reproved_by_this_command": False,
            "uniform_class_bounds_given_cited_profile": [30, 1818],
            "total_bounds_both_endpoints": [63, 3633],
            "low_total_integer_pair_coverage": coverage,
            "complement_map": "(e,a,b)->(1-e,1848-a,1848-b)",
            "remaining_total63_pairs": boundary,
            "remaining_total3633_pairs": upper,
            "boundary_feasibility_or_attained_minimum_asserted": False}


def verify_suite(bundle):
    core.check_domain()
    require(set(bundle) == set(required_names()), "Incomplete four-box root coverage")
    boxes, all_results = [], []
    for e in (0, 1):
        for B in BUDGETS:
            names = [filename(e, root, B) for root in roots_for(e)]
            results = verify_box({name: bundle[name] for name in names}, e, B)
            boxes.append({"endpoint": e, "excluded_original_budget": B.copy(),
                          "roots": roots_for(e), "root_results": results})
            all_results.extend(results)
    return {"verified": True,
            "independent_lemma": "Both ORIGINAL asymmetric boxes30/32 and32/30 are excluded at both actual endpoints",
            "root_cases_checked": len(all_results),
            "nodes_checked": sum(r["nodes"] for r in all_results),
            "splits_checked": sum(r["splits"] for r in all_results),
            "leaves_checked": sum(len(r["leaves"]) for r in all_results),
            "original_class_sizes": [1848, 1848], "exceptional_prefix_positions_free": 7,
            "actual_periodicity_or_symmetry_assumed": False,
            "earlier_numerical_bounds_used_by_new_branch_replay": False,
            "conditional_uniform63_corollary": arithmetic_bridge(),
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
