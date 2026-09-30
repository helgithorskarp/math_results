#!/usr/bin/env python3
"""Check inherited states, complete36-case coverage and corrupted proofs.

Adapted from the cited class29 controls; no numerical premise is tested here.
"""
import argparse
import copy
import itertools
import json
from pathlib import Path
import verify as v


def empty_trace(root, budget, endpoint=0):
    return {"format": v.TRACE_FORMAT, "endpoint": endpoint, "root": root,
            "budget": budget.copy(), "status": "STALLED", "records": [],
            "contradiction": {}}


def controls(directory):
    bundle = {name: json.loads((directory / name).read_text()) for name in v.required_names()}
    checked = v.verify_suite(bundle)
    regressions = 0
    for data in bundle.values():
        trace = data["node"]["trace"]
        old = v.core.verify_branch(trace, complete=False, include_state=True)
        U, T, counts = v.replay(trace, data["endpoint"], data["root"], data["budget"], v.D,
                              {data["root"]}, False)
        v.require(sorted(U) == old["allowed_positions"] and
                  sorted(T) == old["forced_positions"] and counts == old["step_counts"],
                  "Primitive replay disagrees with original single-root checker")
        regressions += 1

    # Definition-level oracle: splitting is a cover, with no exclusivity premise.
    oracle_states = oracle_models = 0
    for Umask, Tmask, Pmask in itertools.product(range(16), range(16), range(1, 16)):
        U = {x for x in range(4) if Umask >> x & 1}
        T = {x for x in range(4) if Tmask >> x & 1}
        P = {x for x in range(4) if Pmask >> x & 1}
        if not T <= U or not P <= U - T:
            continue
        oracle_states += 1
        for Smask in range(16):
            S = {x for x in range(4) if Smask >> x & 1}
            if not T <= S <= U:
                continue
            oracle_models += 1
            v.require(bool(P & S) == any(T | {w} <= S for w in P),
                      "Disjunctive cover disagrees with Boolean oracle")

    root, ap, budget = 1852, [1617, 47], [1848, 0]
    petal = v.core.mandatory_clause(ap, 0, {root})
    positive = {"format": v.FORMAT, "endpoint": 0, "root": root, "budget": budget,
                "node": {"trace": empty_trace(root, budget),
                         "split": {"ap": ap, "children": []}}}
    for w in sorted(petal):
        trace = empty_trace(root, budget)
        trace.update(status="EXCLUDED", contradiction={"reason": "too_many_forced"})
        positive["node"]["split"]["children"].append(
            {"assumption": w, "node": {"trace": trace}})
    synthetic = v.verify_tree(positive)
    v.require(synthetic["closed"] and len(synthetic["leaves"]) == 6,
              "Positive complete six-way control failed")

    rejected = []
    def reject(label, action):
        try:
            action()
        except ValueError as error:
            rejected.append({"name": label, "reason": str(error)})
            return
        raise ValueError("Malformed certificate accepted: " + label)

    def mutate(label, change, base=positive, complete=True):
        data = copy.deepcopy(base)
        change(data)
        reject(label, lambda: v.verify_tree(data, complete=complete))

    reject("child_trace_alone_has_no_global_cover",
           lambda: v.core.verify_branch(positive["node"]["split"]["children"][0]["node"]["trace"]))
    mutate("missing_child", lambda d: d["node"]["split"]["children"].pop())
    mutate("duplicate_child", lambda d: d["node"]["split"]["children"][1].__setitem__(
           "assumption", d["node"]["split"]["children"][0]["assumption"]))
    mutate("nonpetal_child", lambda d: d["node"]["split"]["children"][0].__setitem__("assumption", root))
    mutate("changed_child_budget", lambda d: d["node"]["split"]["children"][0]["node"]["trace"].__setitem__("budget", [1848, 1]))
    mutate("extra_child_hypothesis", lambda d: d["node"]["split"]["children"][0]["node"]["trace"].__setitem__("initial_forced", [root, 999]))
    mutate("supplied_U", lambda d: d["node"]["split"]["children"][0]["node"]["trace"].__setitem__("allowed_positions", []))
    mutate("supplied_T", lambda d: d["node"]["split"]["children"][0]["node"]["trace"].__setitem__("forced_positions", []))
    mutate("changed_child_root", lambda d: d["node"]["split"]["children"][0]["node"]["trace"].__setitem__("root", 1))
    mutate("constant_AP", lambda d: d["node"]["split"].__setitem__("ap", [1617, 0]))
    mutate("Boolean_AP", lambda d: d["node"]["split"].__setitem__("ap", [False, 1]))
    mutate("AP_hits_pole", lambda d: d["node"]["split"].__setitem__("ap", [0, 1]))
    mutate("satisfied_AP", lambda d: d["node"]["split"].__setitem__("ap", [1, 617]))
    mutate("root_outside_cover", lambda d: d.__setitem__("root", 2))
    mutate("extra_tree_hypothesis", lambda d: d.__setitem__("initial_forced", [root, 1664]))
    mutate("open_child_cannot_close_parent", lambda d: d["node"]["split"]["children"][0]["node"].__setitem__("trace", empty_trace(root, budget)))
    mutate("false_terminal", lambda d: d["node"]["split"]["children"][0]["node"]["trace"].__setitem__("contradiction", {"reason": "empty_required", "ap": ap}))
    mutate("forbid_inherited_root", lambda d: d["node"]["split"]["children"][0]["node"]["trace"].__setitem__("records", [["f", root, [ap]]]))

    partial = copy.deepcopy(bundle["tree-0-1-30-30.json"])
    for child in partial["node"]["split"]["children"]:
        child["node"]["trace"] = empty_trace(1, [30, 30])
    state = v.verify_tree(partial, complete=False, include_state=True)
    v.require(not state["closed"] and [x["path"] for x in state["leaves"]] ==
              [[315], [629], [943], [1257], [1571]] and
              all(x["allowed"] == 3403 and x["forced"] == 2 for x in state["leaves"]),
              "Valid five-way partial tree has wrong inherited state")
    mutate("unverified_shrinking_of_parent_petal",
           lambda d: d["node"]["trace"].__setitem__("records", []), base=partial, complete=False)
    mutate("partial_tree_blocks_exclusion", lambda d: None, base=partial)
    missing = bundle.copy()
    missing.pop("tree-0-1852-30-30.json")
    reject("missing_endpoint_root", lambda: v.verify_suite(missing))
    wrong = bundle.copy()
    wrong["tree-0-1-30-30.json"] = copy.deepcopy(wrong["tree-0-1-30-30.json"])
    wrong["tree-0-1-30-30.json"]["budget"] = [29, 30]
    reject("changed_quantified_budget", lambda: v.verify_suite(wrong))
    for e, B in [(0,[29,31]),(0,[30,30]),(0,[31,29]),
                 (1,[29,31]),(1,[30,30]),(1,[31,29])]:
        missing_box = {name:data for name,data in bundle.items()
                       if not (data["endpoint"] == e and data["budget"] == B)}
        reject("missing_entire_box_" + str(e) + "_" + str(B),
               lambda b=missing_box: v.verify_suite(b))
    extra = bundle.copy()
    extra["tree-0-1-29-32.json"] = bundle["tree-0-1-29-31.json"]
    reject("extra_unproved_box", lambda: v.verify_suite(extra))
    bad_endpoint = bundle.copy()
    bad_endpoint["tree-0-1-30-30.json"] = copy.deepcopy(bundle["tree-0-1-30-30.json"])
    bad_endpoint["tree-0-1-30-30.json"]["endpoint"] = 1
    reject("unsupported_endpoint_transfer", lambda: v.verify_suite(bad_endpoint))
    reject("intersecting_packing", lambda: v.core.check_packing([{1, 2}, {2, 3}], 2))
    reject("empty_packing", lambda: v.core.check_packing([set()], 1))
    return {"agent": "six-vdw-2", "role": "researcher", "checked_trees": checked["branches_checked"],
            "checked_terminal_leaves": checked["leaves_checked"], "primitive_regressions": regressions,
            "oracle_states": oracle_states, "oracle_models": oracle_models,
            "valid_six_way_tree": True, "valid_partial_five_way_tree": True,
            "controls_rejected": len(rejected), "rejections": rejected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = controls(args.directory)
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "rejections"}, sort_keys=True))


if __name__ == "__main__":
    main()
