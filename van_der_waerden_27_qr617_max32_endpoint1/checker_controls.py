#!/usr/bin/env python3
"""Check direct-proof compatibility and reject wrong coverage or hypotheses."""
import argparse
import copy
import json
from pathlib import Path
import verify as v


def controls(directory):
    bundle = {name: json.loads((directory / name).read_text()) for name in v.required_names()}
    regressions = 0
    for e, root, B in v.cases():
        data = bundle[v.filename(e, root, B)]
        v.require((data.get("endpoint"), data.get("root"), data.get("budget")) == (e, root, B),
                  "Wrong control input hypotheses")
        v.require(set(data["node"]) == {"trace"}, "This control requires a direct singleton trace")
        strict = v.core.verify_branch(data["node"]["trace"], complete=False, include_state=True)
        v.core.verify_branch(data["node"]["trace"])
        checked = v.verify_tree(data, include_state=True)
        leaf = checked["leaves"][0]
        v.require(checked["closed"] and
                  leaf["allowed_positions"] == strict["allowed_positions"] and
                  leaf["forced_positions"] == strict["forced_positions"] and
                  leaf["counts"] == strict["step_counts"], "Strict/tree singleton checking disagrees")
        regressions += 1

    rejected = []
    def reject(label, action):
        try:
            action()
        except ValueError as error:
            rejected.append({"name": label, "reason": str(error)})
            return
        raise ValueError("Malformed proof accepted: " + label)

    for name in v.required_names():
        missing = bundle.copy()
        missing.pop(name)
        reject("missing_root_" + name, lambda b=missing: v.verify_suite(b))
    key = v.required_names()[0]
    for label, field, value in [
        ("wrong_endpoint", "endpoint", 0),
        ("Boolean_endpoint", "endpoint", True),
        ("unsupported_larger_cap", "budget", [32, 31]),
        ("unsupported_other_class_cap", "budget", [31, 32]),
        ("wrong_root", "root", 1)]:
        bad = bundle.copy()
        bad[key] = copy.deepcopy(bad[key])
        bad[key][field] = value
        reject(label, lambda b=bad: v.verify_suite(b))
    extra = bundle.copy()
    extra["tree-0-1-31-31.json"] = bundle[key]
    reject("unsupported_endpoint_cover", lambda: v.verify_suite(extra))

    def mutate(label, change):
        bad = copy.deepcopy(bundle[key])
        change(bad)
        reject(label, lambda: v.verify_tree(bad))

    mutate("changed_trace_budget", lambda d: d["node"]["trace"].__setitem__("budget", [32, 31]))
    mutate("extra_trace_hypothesis", lambda d: d["node"]["trace"].__setitem__("initial_forced", [1, 3421]))
    mutate("extra_tree_hypothesis", lambda d: d.__setitem__("initial_forced", [1, 3421]))
    mutate("supplied_U", lambda d: d["node"]["trace"].__setitem__("allowed_positions", []))
    mutate("supplied_T", lambda d: d["node"]["trace"].__setitem__("forced_positions", []))
    mutate("false_terminal", lambda d: d["node"]["trace"].__setitem__("contradiction", {"reason": "too_many_forced"}))
    mutate("unproved_partial_terminal", lambda d: d["node"]["trace"].__setitem__("status", "INCOMPLETE_TIME_LIMIT"))
    mutate("constant_AP", lambda d: d["node"]["trace"]["records"].__setitem__(0, ["t", 1, 1, 0]))
    mutate("Boolean_AP", lambda d: d["node"]["trace"]["records"].__setitem__(0, ["t", 1, False, 1]))
    mutate("AP_hits_pole", lambda d: d["node"]["trace"]["records"].__setitem__(0, ["t", 1, 0, 1]))
    mutate("forbid_forced_root", lambda d: d["node"]["trace"]["records"].__setitem__(0, ["f", 3421, [[3421, 47]]]))
    reject("intersecting_packing", lambda: v.core.check_packing([{1, 2}, {2, 3}], 2))
    reject("empty_packing", lambda: v.core.check_packing([set()], 1))
    return {"agent": "six-vdw-2", "role": "researcher", "primitive_regressions": regressions,
            "input_cases": len(bundle), "controls_rejected": len(rejected), "rejections": rejected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = controls(args.directory)
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: value for k, value in result.items() if k != "rejections"}, sort_keys=True))


if __name__ == "__main__":
    main()
