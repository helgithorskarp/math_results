#!/usr/bin/env python3
"""Reject malformed endpoint0 proofs and compare six full parent states."""
import argparse
import copy
import json
from pathlib import Path
import verify as v


def controls(directory):
    B = v.BUDGET.copy()
    roots = [root for _,root,_ in v.cases()]
    names = [v.filename(*case) for case in v.cases()]
    bundle = {name:json.loads((directory/name).read_text()) for name in names}
    outer = v.verify_suite
    outer(bundle)
    rejections = []


    def reject(label, action):
        try:
            action()
        except ValueError as error:
            rejections.append({"name":label, "reason":str(error)})
            return
        raise ValueError("Malformed endpoint0 proof accepted: " + label)


    for name in names:
        missing = bundle.copy()
        missing.pop(name)
        reject("missing_root_"+name, lambda data=missing: outer(data))
    key = names[0]
    for label, field, value in [
            ("wrong_endpoint", "endpoint", 1),
            ("Boolean_endpoint", "endpoint", False),
            ("unsupported_square_cap", "budget", [32,31]),
            ("unsupported_nonsquare_cap", "budget", [31,32]),
            ("wrong_root", "root", 3421)]:
        bad = bundle.copy()
        bad[key] = copy.deepcopy(bad[key])
        bad[key][field] = value
        reject(label, lambda data=bad: outer(data))
    extra = bundle.copy()
    extra["tree-1-3421-31-31.json"] = bundle[key]
    reject("unsupported_endpoint_cover", lambda: outer(extra))


    def mutate(label, change):
        data = copy.deepcopy(bundle[key])
        change(data)
        reject(label, lambda: v.verify_tree(data))


    split = bundle[key]["node"]["split"]
    v.require(split["ap"] == [1,285] and
              [x["assumption"] for x in split["children"]] == [286,571,856,1141,1426,1711],
              "Unexpected audited first root split")
    mutate("missing_petal_child", lambda d: d["node"]["split"]["children"].pop())
    mutate("duplicate_petal_child", lambda d: d["node"]["split"]["children"][1].__setitem__(
           "assumption", d["node"]["split"]["children"][0]["assumption"]))
    mutate("child_outside_required_petal", lambda d: d["node"]["split"]["children"][0].__setitem__("assumption",1))
    mutate("Boolean_child_assumption", lambda d: d["node"]["split"]["children"][0].__setitem__("assumption",True))
    mutate("nonmandatory_split", lambda d: d["node"]["split"].__setitem__("ap",[0,1]))
    mutate("wrong_child_cap", lambda d: d["node"]["split"]["children"][0]["node"]["trace"].__setitem__("budget",[32,31]))
    mutate("extra_child_hypothesis", lambda d: d["node"]["split"]["children"][0]["node"]["trace"].__setitem__("initial_forced",[1,286,2]))
    mutate("extra_tree_hypothesis", lambda d: d.__setitem__("initial_forced",[1,2]))
    mutate("supplied_child_U", lambda d: d["node"]["split"]["children"][0]["node"]["trace"].__setitem__("allowed_positions",[]))
    mutate("supplied_child_T", lambda d: d["node"]["split"]["children"][0]["node"]["trace"].__setitem__("forced_positions",[]))
    mutate("false_child_terminal", lambda d: d["node"]["split"]["children"][0]["node"]["trace"].__setitem__("contradiction",{"reason":"too_many_forced"}))
    mutate("incomplete_child_terminal", lambda d: d["node"]["split"]["children"][0]["node"]["trace"].__setitem__("status","INCOMPLETE_TIME_LIMIT"))
    reject("intersecting_packing", lambda: v.core.check_packing([{1,2},{2,3}],2))
    reject("empty_packing", lambda: v.core.check_packing([set()],1))

    # Different strict-singleton and generic-tree entry points must agree on
    # the final full states of all six primitive parents. The root1 parent
    # is STALLED, so only partial correctness is claimed for that direct trace.
    regressions = 0
    for root, name in zip(roots, names):
        trace = bundle[name]["node"]["trace"]
        strict = v.core.verify_branch(trace,complete=False,include_state=True)
        direct = {"format":v.FORMAT,"endpoint":0,"root":root,"budget":B,
                  "node":{"trace":trace}}
        checked = v.verify_tree(direct,complete=False,include_state=True)
        leaf = checked["leaves"][0]
        v.require(strict["allowed_positions"] == leaf["allowed_positions"] and
                  strict["forced_positions"] == leaf["forced_positions"] and
                  strict["step_counts"] == leaf["counts"], "Strict/generic parent states differ")
        if root != 1:
            v.core.verify_branch(trace)
        else:
            v.require(not leaf["closed"] and trace["status"] == "STALLED",
                      "Root1 parent was incorrectly treated as closed")
        regressions += 1

    return {"agent":"six-vdw-2","role":"researcher",
            "input_cases":len(bundle),"primitive_regressions":regressions,
            "controls_rejected":len(rejections),"rejections":rejections}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory",type=Path)
    parser.add_argument("--output",type=Path)
    args = parser.parse_args()
    result = controls(args.directory)
    if args.output:
        args.output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:value for k,value in result.items() if k != "rejections"},sort_keys=True))


if __name__ == "__main__":
    main()
