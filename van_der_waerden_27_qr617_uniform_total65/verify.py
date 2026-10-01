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
spec = importlib.util.spec_from_file_location("uniform65_unchanged_tree_checker",
    BASE / "van_der_waerden_27_qr617_class29_disjunction/verify.py")
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
core, D, COLORS = v.core, v.D, v.COLORS
FORMAT, TRACE_FORMAT = v.FORMAT, v.TRACE_FORMAT
require, verify_tree = v.require, v.verify_tree
CASES = [[0, [33, 31]], [0, [30, 34]], [0, [34, 30]], [1, [30, 34]], [1, [31, 33]], [1, [33, 31]], [1, [34, 30]]]
E = B = DIRECTORY = BOX = None
ROOTS = CHILDREN = SPLIT_ROOT = SPLIT_AP = ANCHOR_AP = None
EXPECTED = json.loads((HERE / "expected.json").read_text())


def case_spec(endpoint, budget):
    require(type(endpoint) is int and [endpoint, budget] in CASES,
            "Wrong endpoint/original-class cap box")
    anchor = core.ENDPOINT_APS[endpoint]
    roots = sorted(core.endpoint_points(anchor, endpoint))
    expected_roots = ([1,618,1235,1852,2469,3086] if endpoint == 0 else
                      [3421,3468,3515,3562,3609,3656])
    require(roots == expected_roots, "Wrong complete actual anchor root cover")
    if endpoint == 0:
        split_root, ap, children = 1, [1,285], [286,571,856,1141,1426,1711]
    elif budget == [31,33]:
        split_root, ap, children = 3656, [2455,208], [2663,2871,3079,3287,3495]
    elif budget == [33,31]:
        split_root, ap, children = 3656, [1885,303], [2188,2491,2794,3097,3400]
    else:
        split_root, ap, children = None, None, []
    return {"endpoint": endpoint, "budget": budget, "roots": roots, "anchor": anchor,
            "split_root": split_root, "split_ap": ap, "children": children}


def select_case(endpoint, budget):
    global E, B, ROOTS, CHILDREN, SPLIT_ROOT, SPLIT_AP, ANCHOR_AP, BOX
    case = case_spec(endpoint, budget)
    E, B = endpoint, budget
    ROOTS, CHILDREN, SPLIT_ROOT = case["roots"], case["children"], case["split_root"]
    SPLIT_AP, ANCHOR_AP = case["split_ap"], case["anchor"]
    BOX = next(row for row in EXPECTED["boxes"] if (row["endpoint"], row["budget"]) == (E, B))
    require(BOX["roots"] == ROOTS, "Wrong full expected anchor cover")


def filename(root):
    return filename_for(root, B)


def check_root(root, data, include_state=False):
    v.require(type(data.get("endpoint")) is int and type(data.get("root")) is int and
              (data.get("endpoint"), data.get("root"), data.get("budget")) == (E, root, B),
              "Wrong quantified endpoint/root/requested original-class box")
    return v.verify_tree(data, include_state=include_state)


def check_suite(bundle):
    v.require(set(bundle) == {filename(r) for r in ROOTS}, "Missing or unexpected mandatory root")
    v.require(ROOTS == sorted(v.core.endpoint_points(ANCHOR_AP, E)), "Wrong complete anchor cover")
    results = [check_root(r, bundle[filename(r)]) for r in ROOTS]
    v.require(all(x["closed"] for x in results), "Open mandatory root")
    totals = {k: sum(x["step_totals"][k] for x in results) for k in results[0]["step_totals"]}
    return {"endpoint": E, "budget": B, "whole_box_excluded": True,
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
    if root == SPLIT_ROOT:
        v.require(not generic["closed"] and parent["node"]["trace"]["status"] == "STALLED",
                  "Stalled parent alone counted as exclusion")
        K = sorted(v.core.mandatory_clause(SPLIT_AP, E, set(generic["forced_positions"])) &
                   set(generic["allowed_positions"]))
        v.require(K == CHILDREN, "Wrong full split child cover")
        v.require((full["nodes"], full["splits"], len(full["leaves"])) == (len(CHILDREN)+1, 1, len(CHILDREN)), "Wrong complete split topology")
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
        return (d["node"]["split"]["children"][0]["node"]["trace"] if root == SPLIT_ROOT else d["node"]["trace"])

    return reject_controls(root, [
        ("Boolean_endpoint", lambda d: d.update(endpoint=bool(E))),
        ("wrong_endpoint", lambda d: d.update(endpoint=1-E)),
        ("wrong_root", lambda d: d.update(root=wrong)),
        ("same_total_wrong_original_caps", lambda d: d.update(budget=[B[0]-1, B[1]+1])),
        ("enlarged_original_budget", lambda d: d.update(budget=[B[0]+1, B[1]])),
        ("extra_initial_hypothesis", lambda d: d.update(initial_forced=[wrong])),
        ("supplied_parent_state", lambda d: d["node"]["trace"].update(allowed_positions=[root])),
        ("false_terminal", lambda d: trace(d).update(contradiction={"reason": "too_many_forced"})),
        ("incomplete_terminal", lambda d: trace(d).update(status="STALLED", contradiction={})),
    ])


def split_controls():
    require(SPLIT_ROOT is not None, "This quantified box has no split")
    split = lambda d: d["node"]["split"]
    child = lambda d: split(d)["children"][0]["node"]["trace"]
    return reject_controls(SPLIT_ROOT, [
        ("missing_child", lambda d: split(d)["children"].pop()),
        ("duplicate_child", lambda d: split(d)["children"].__setitem__(1, copy.deepcopy(split(d)["children"][0]))),
        ("Boolean_child", lambda d: split(d)["children"][0].update(assumption=True)),
        ("child_outside_full_petal", lambda d: split(d)["children"][0].update(assumption=ROOTS[1])),
        ("nonmandatory_split", lambda d: split(d).update(ap=[2, 1])),
        ("wrong_child_budget", lambda d: child(d).update(budget=[B[0], B[1]+1])),
        ("wrong_child_root", lambda d: child(d).update(root=ROOTS[1])),
        ("extra_child_hypothesis", lambda d: child(d).update(initial_forced=[SPLIT_ROOT, CHILDREN[0], ROOTS[1]])),
        ("supplied_child_state", lambda d: child(d).update(allowed_positions=[])),
    ])


def coverage_controls():
    v.require(ROOTS == sorted(v.core.endpoint_points(ANCHOR_AP, E)), "Wrong complete anchor roots")
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
    unexpected = {**bundle, "unexpected-root.json": bundle[filename(ROOTS[0])]}
    try:
        check_suite(unexpected)
    except ValueError as error:
        rejected.append({"name": "unexpected_root", "reason": str(error)})
    else:
        raise ValueError("Accepted unexpected root")
    return rejected


def arithmetic_bridge():
    core.check_domain()
    require([sum(COLORS[x] == side for x in D) for side in (0,1)] == [1848,1848],
            "Wrong original class sizes")
    require(EXPECTED["cases"] == CASES, "Missing or extra new endpoint/cap box")
    for dependency in PROVENANCE["numerical_dependencies"]:
        for name, digest in dependency["files"].items():
            require(hashlib.sha256((BASE/dependency["directory"]/name).read_bytes()).hexdigest() == digest,
                    "Changed separately cited numerical source")
    old, published = [json.loads((BASE/dependency["directory"]/"expected.json").read_text())
                      for dependency in PROVENANCE["numerical_dependencies"]]
    require(old["combined_class_bounds"] == published["combined_class_bounds"] == [30,1818] and
            old["combined_total_bounds"] == published["combined_total_bounds"] == [64,3632],
            "Wrong inherited numerical profile")
    prior = [[0,[32,32]],[1,[32,32]],[0,[31,33]]]
    require(published["cases"] == EXPECTED["old_published_direct_boxes"] == prior,
            "Wrong published three-box premise")
    all_cases = prior + CASES
    boundary64 = [[a,64-a] for a in range(30,35)]
    require(all(sorted([B for e,B in all_cases if e == endpoint]) == boundary64
                for endpoint in (0,1)), "Incomplete five-box total64 cover")
    for q in (0,1):
        for actual in (0,1):
            require(int((1-actual) != q) == 1-int(actual != q), "Wrong pointwise complement")
    omitted = []
    for endpoint,B in CASES:
        others = [[e,K] for e,K in all_cases if [e,K] != [endpoint,B]]
        require(not any(e == endpoint and B[0] <= K[0] and B[1] <= K[1] for e,K in others),
                "Omitted-box control fails to expose a coverage gap")
        omitted.append({"omitted":[endpoint,B],"uncovered_pair":B})
    next_pairs = [[a,65-a] for a in range(30,36)]
    require(all(not any(e == endpoint and a <= A and b <= B
                        for e,(A,B) in all_cases) for endpoint in (0,1) for a,b in next_pairs),
            "Incorrect remaining total65 boundary")
    require(len(D) == 3696 and 3696-65 == 3631 and
            EXPECTED["combined_class_bounds"] == [30,1818] and
            EXPECTED["combined_total_bounds"] == [65,3631], "Wrong combined profile")
    return {"new_direct_boxes":CASES,"previous_published_direct_boxes":prior,
            "all_direct_boxes":all_cases,"direct_numeric_proof_inputs":[],
            "original_class_sizes":[1848,1848],"inherited_class_bounds":[30,1818],
            "inherited_total_bounds":[64,3632],"combined_class_bounds":[30,1818],
            "combined_total_bounds":[65,3631],"total64_all_boundary_pairs":boundary64,
            "remaining_total64_pairs":{"0":[],"1":[]},
            "remaining_total3632_pairs":{"0":[],"1":[]},
            "next_total65_pairs_both_endpoints":next_pairs,
            "complement":"(e,a,b)->(1-e,1848-a,1848-b), no original-class swap",
            "omitted_box_controls":omitted,"old_numeric_proof_corpora_replayed":False,
            "uniform65_proved":True,"floor66_or_class31_proved":False,
            "boundary_feasibility_asserted":False,"witness_or_global_W_bound_asserted":False}


def main():
    global DIRECTORY
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("directory", type=Path)
    p.add_argument("--endpoint", type=int)
    p.add_argument("--budget", type=int, nargs=2)
    p.add_argument("--task", choices=["root","controls","split","coverage","arithmetic"], required=True)
    p.add_argument("--root", type=int)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    require(not args.output.exists(), "Saved partition exists; no automatic retry")
    DIRECTORY = args.directory
    if args.task == "arithmetic":
        require(args.endpoint is None and args.budget is None and args.root is None, "Wrong arithmetic quantifiers")
        names = {filename_for(root,C,e) for e,C in CASES for root in case_spec(e,C)["roots"]}
        require({path.name for path in DIRECTORY.glob("tree-*.json")} == names,
                "Missing or extra complete seven-box forest files")
        result = arithmetic_bridge()
    else:
        select_case(args.endpoint, args.budget)
        require(args.root in ROOTS if args.task in ("root","controls") else args.root is None,
                "Wrong partition root")
        if args.task == "root": result = root_partition(args.root)
        elif args.task == "controls": result = {"rejected":root_controls(args.root)}
        elif args.task == "split": result = {"rejected":split_controls()}
        else: result = {"rejected":coverage_controls()}
    payload = {"agent":"six-vdw-2", "role":"researcher", "endpoint":E, "budget":B,
               "task":args.task, "root":args.root, "result":result}
    args.output.write_text(json.dumps(payload,indent=2)+"\n")
    print(json.dumps({"endpoint":E,"budget":B,"task":args.task,"root":args.root,
                      "optimized_flag":sys.flags.optimize,"status":"PARTITION_CHECKED"}),flush=True)


def filename_for(root, budget, endpoint=None):
    e = E if endpoint is None else endpoint
    return f"tree-{e}-{root}-{budget[0]}-{budget[1]}.json"


if __name__ == "__main__":
    main()
