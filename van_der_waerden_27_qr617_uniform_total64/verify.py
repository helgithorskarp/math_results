"""Definition-level full-root and corruption-control audit partitions."""
import argparse
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
PROVENANCE = json.loads((HERE / "provenance.json").read_text())
for dependency in PROVENANCE["computational_dependencies"]:
    for name, digest in dependency["files"].items():
        if hashlib.sha256((BASE / dependency["directory"] / name).read_bytes()).hexdigest() != digest:
            raise ValueError("Changed computational dependency")
spec = importlib.util.spec_from_file_location("uniform64_unchanged_tree_checker",
    BASE / "van_der_waerden_27_qr617_class29_disjunction/verify.py")
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
core, D, COLORS = v.core, v.D, v.COLORS
FORMAT, TRACE_FORMAT = v.FORMAT, v.TRACE_FORMAT
require, verify_tree = v.require, v.verify_tree
ROOTS = [1, 618, 1235, 1852, 2469, 3086]
BUDGETS = [[30, 33], [31, 32], [32, 31], [33, 30]]
CHILDREN = [286, 571, 856, 1141, 1426, 1711]
B = None
DIRECTORY = None
BOX = None
EXPECTED = json.loads((HERE / "expected.json").read_text())


def filename(root):
    return filename_for(root, B)


def check_root(root, data, include_state=False):
    v.require(type(data.get("endpoint")) is int and type(data.get("root")) is int and
              (data.get("endpoint"), data.get("root"), data.get("budget")) == (0, root, B),
              "Wrong quantified endpoint0/root/requested original-class box")
    return v.verify_tree(data, include_state=include_state)


def check_suite(bundle):
    v.require(set(bundle) == {filename(r) for r in ROOTS}, "Missing or unexpected mandatory root")
    v.require(ROOTS == sorted(v.core.endpoint_points([1, 617], 0)), "Wrong complete anchor cover")
    results = [check_root(r, bundle[filename(r)]) for r in ROOTS]
    v.require(all(x["closed"] for x in results), "Open mandatory root")
    totals = {k: sum(x["step_totals"][k] for x in results) for k in results[0]["step_totals"]}
    return {"endpoint": 0, "budget": B, "whole_box_excluded": True,
            "roots": ROOTS, "roots_checked": len(results),
            "nodes": sum(x["nodes"] for x in results),
            "splits": sum(x["splits"] for x in results),
            "leaves": sum(len(x["leaves"]) for x in results),
            "step_totals": totals, "root_results": results}


def load(root):
    v.require(root in ROOTS, "Root outside complete anchor cover")
    path = DIRECTORY / filename(root)
    raw = path.read_bytes()
    row = next(x for x in BOX["certificates"] if x["root"] == root)
    v.require(len(raw) == row["bytes"] and hashlib.sha256(raw).hexdigest() == row["sha256"],
              "Frozen proof bytes changed")
    return json.loads(raw), {"root": root, "file": path.name, "bytes": len(raw),
                            "sha256": row["sha256"]}


def root_partition(root):
    data, manifest = load(root)
    full = check_root(root, data, include_state=True)
    result = copy.deepcopy(full)
    for leaf in result["leaves"]:
        leaf.pop("allowed_positions")
        leaf.pop("forced_positions")
    parent = {**data, "node": {"trace": data["node"]["trace"]}}
    generic = v.verify_tree(parent, complete=False, include_state=True)["leaves"][0]
    strict = v.core.verify_branch(parent["node"]["trace"], complete=False, include_state=True)
    v.require(generic["allowed_positions"] == strict["allowed_positions"] and
              generic["forced_positions"] == strict["forced_positions"] and
              generic["counts"] == strict["step_counts"], "Strict/generic full parent states differ")
    if root == 1:
        v.require(not generic["closed"] and parent["node"]["trace"]["status"] == "STALLED",
                  "Stalled parent alone counted as exclusion")
        K = sorted(v.core.mandatory_clause([1, 285], 0, set(generic["forced_positions"])) &
                   set(generic["allowed_positions"]))
        v.require(K == [286, 571, 856, 1141, 1426, 1711], "Wrong full root1 child cover")
        v.require((full["nodes"], full["splits"], len(full["leaves"])) == (7, 1, 6), "Wrong complete root1 topology")
    else:
        v.core.verify_branch(parent["node"]["trace"])
        v.require((full["nodes"], full["splits"], len(full["leaves"])) == (1, 0, 1), "Wrong direct root topology")
    parent_result = {"root": root, "allowed": generic["allowed"], "forced": generic["forced"],
                     "counts": generic["counts"], "strict_generic_full_state_equal": True}
    index = ROOTS.index(root)
    v.require(result == BOX["verification"]["root_results"][index], "Full root output differs from expected")
    v.require(parent_result == BOX["parent_states"][index], "Full parent regression differs from expected")
    return {"root_result": result, "certificate": manifest, "parent_state": parent_result}


def reject_controls(root, mutations):
    base, _ = load(root)
    rejected = []
    for name, mutate in mutations:
        data = copy.deepcopy(base)
        mutate(data)
        try:
            check_root(root, data)
        except ValueError as error:
            rejected.append({"root": root, "name": name, "reason": str(error)})
        else:
            raise ValueError("Accepted corruption " + name)
    return rejected


def root_controls(root):
    data, _ = load(root)
    terminal = check_root(root, data, include_state=True)["leaves"][0]
    v.require(all(sum(v.COLORS[x] == side for x in terminal["forced_positions"]) <= B[side]
                  for side in (0, 1)), "False terminal control is not false")
    wrong = ROOTS[(ROOTS.index(root) + 1) % len(ROOTS)]

    def trace(d):
        return (d["node"]["split"]["children"][0]["node"]["trace"] if root == 1 else d["node"]["trace"])

    return reject_controls(root, [
        ("Boolean_endpoint", lambda d: d.update(endpoint=False)),
        ("wrong_endpoint", lambda d: d.update(endpoint=1)),
        ("wrong_root", lambda d: d.update(root=wrong)),
        ("swapped_original_budget", lambda d: d.update(budget=list(reversed(B)))),
        ("enlarged_original_budget", lambda d: d.update(budget=[B[0]+1, B[1]])),
        ("extra_initial_hypothesis", lambda d: d.update(initial_forced=[wrong])),
        ("supplied_parent_state", lambda d: d["node"]["trace"].update(allowed_positions=[root])),
        ("false_terminal", lambda d: trace(d).update(contradiction={"reason": "too_many_forced"})),
        ("incomplete_terminal", lambda d: trace(d).update(status="STALLED", contradiction={})),
    ])


def split_controls():
    split = lambda d: d["node"]["split"]
    child = lambda d: split(d)["children"][0]["node"]["trace"]
    return reject_controls(1, [
        ("missing_child", lambda d: split(d)["children"].pop()),
        ("duplicate_child", lambda d: split(d)["children"].__setitem__(1, copy.deepcopy(split(d)["children"][0]))),
        ("Boolean_child", lambda d: split(d)["children"][0].update(assumption=True)),
        ("child_outside_full_petal", lambda d: split(d)["children"][0].update(assumption=618)),
        ("nonmandatory_split", lambda d: split(d).update(ap=[2, 1])),
        ("wrong_child_budget", lambda d: child(d).update(budget=[B[0], B[1]+1])),
        ("wrong_child_root", lambda d: child(d).update(root=618)),
        ("extra_child_hypothesis", lambda d: child(d).update(initial_forced=[1, 286, 618])),
        ("supplied_child_state", lambda d: child(d).update(allowed_positions=[])),
    ])


def coverage_controls():
    v.require(ROOTS == sorted(v.core.endpoint_points([1, 617], 0)), "Wrong complete anchor roots")
    bundle = {filename(root): load(root)[0] for root in ROOTS}
    rejected = []
    for root in ROOTS:
        omitted = dict(bundle)
        omitted.pop(filename(root))
        try:
            check_suite(omitted)
        except ValueError as error:
            rejected.append({"root": root, "name": "missing_mandatory_root", "reason": str(error)})
        else:
            raise ValueError("Accepted omitted root")
    unexpected = {**bundle, "unexpected-root.json": bundle[filename(1)]}
    try:
        check_suite(unexpected)
    except ValueError as error:
        rejected.append({"name": "unexpected_root", "reason": str(error)})
    else:
        raise ValueError("Accepted unexpected root")
    return rejected


def arithmetic_bridge():
    core.check_domain()
    v.require([sum(COLORS[x] == side for x in D) for side in (0, 1)] == [1848, 1848],
              "Wrong original class sizes")
    v.require(ROOTS == sorted(core.endpoint_points([1, 617], 0)), "Wrong actual anchor cover")
    for dependency in PROVENANCE["numerical_dependencies"]:
        for name, digest in dependency["files"].items():
            v.require(hashlib.sha256((BASE / dependency["directory"] / name).read_bytes()).hexdigest() == digest,
                      "Changed separately cited numerical source")
    pairs = [[a, b] for a in range(30, 34) for b in range(30, 34) if a+b <= 63]
    v.require(len(pairs) == 10, "Incomplete exact low-total integer domain")
    coverage = []
    for a, b in pairs:
        eligible = [C for C in BUDGETS if a <= C[0] and b <= C[1]]
        v.require(eligible, "Uncovered pair below64")
        coverage.append({"pair": [a, b], "excluded_by_original_box": eligible[0]})
    omissions = []
    for omitted in BUDGETS:
        remaining = [C for C in BUDGETS if C != omitted]
        v.require(not any(omitted[0] <= C[0] and omitted[1] <= C[1] for C in remaining),
                  "Omitted-box control does not expose a missing boundary")
        omissions.append({"omitted_box": omitted, "uncovered_total63_pair": omitted})
    for reference_color in (0, 1):
        for actual_color in (0, 1):
            edited = int(actual_color != reference_color)
            complemented = int((1-actual_color) != reference_color)
            v.require(complemented == 1-edited, "Incorrect pointwise complement identity")
    at64 = [[a, 64-a] for a in range(30, 35)]
    v.require(2*1848-64 == 3632 and
              all(not any(a <= C[0] and b <= C[1] for C in BUDGETS) for a, b in at64),
              "Incorrect complement or boundary scope")
    return {"class_floor30_dependency": PROVENANCE["numerical_dependencies"][0]["graph_reference"],
            "endpoint1_lower64_combination_dependency": PROVENANCE["numerical_dependencies"][1]["graph_reference"],
            "old_numeric_proof_corpora_replayed": False, "pinned_numeric_source_hashes_checked": True,
            "new_endpoint0_total_lower_bound": 64, "new_endpoint1_total_upper_bound": 3632,
            "combined_total_bounds_both_endpoints": [64, 3632],
            "combined_class_bounds_both_endpoints": [30, 1818],
            "low_total_pairs": coverage, "omitted_box_controls": omissions,
            "complement_map": "(e,a,b)->(1-e,1848-a,1848-b)",
            "remaining_total64_pairs_both_endpoints": at64,
            "remaining_total3632_pairs_both_endpoints": sorted([[1848-a,1848-b] for a,b in at64]),
            "boundary_feasibility_asserted": False}


def main():
    global B, DIRECTORY, BOX
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("directory", type=Path)
    p.add_argument("--budget", type=int, nargs=2)
    p.add_argument("--task", choices=["root", "controls", "split", "coverage", "arithmetic"], required=True)
    p.add_argument("--root", type=int)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    v.require(not args.output.exists(), "Saved partition exists; no automatic retry")
    DIRECTORY, B = args.directory, args.budget
    if args.task == "arithmetic":
        v.require(B is None and args.root is None, "Wrong arithmetic quantifiers")
        names = {filename_for(root, C) for C in BUDGETS for root in ROOTS}
        v.require({path.name for path in DIRECTORY.glob("tree-*.json")} == names,
                  "Incomplete or extra four-box file coverage")
        result = arithmetic_bridge()
    else:
        v.require(B in BUDGETS, "Wrong original-class caps")
        BOX = next(row for row in EXPECTED["boxes"] if row["budget"] == B)
        v.require(BOX["roots"] == ROOTS, "Wrong complete expected anchor cover")
        v.require(args.root in ROOTS if args.task in ("root", "controls") else args.root is None,
                  "Wrong partition root")
        if args.task == "root":
            result = root_partition(args.root)
        elif args.task == "controls":
            result = {"rejected": root_controls(args.root)}
        elif args.task == "split":
            result = {"rejected": split_controls()}
        else:
            result = {"rejected": coverage_controls()}
    payload = {"agent": "six-vdw-2", "role": "researcher", "endpoint": 0,
               "budget": B, "task": args.task, "root": args.root, "result": result}
    args.output.write_text(json.dumps(payload, indent=2)+"\n")
    print(json.dumps({"budget": B, "task": args.task, "root": args.root,
                      "optimized_flag": sys.flags.optimize, "status": "PARTITION_CHECKED"}), flush=True)


def filename_for(root, budget):
    return f"tree-0-{root}-{budget[0]}-{budget[1]}.json"


if __name__ == "__main__":
    main()
