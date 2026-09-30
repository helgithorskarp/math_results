#!/usr/bin/env python3
"""Positive and negative controls for the exact checker and finite cover."""
import argparse
import copy
import json
from pathlib import Path
import verify


def rejected(name, action):
    try:
        action()
    except (ValueError, KeyError, TypeError, IndexError) as error:
        return {"control": name, "reason": str(error)}
    raise AssertionError(f"Corrupted proof accepted: {name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", type=Path, default=Path("build"))
    args = parser.parse_args()
    bundle = {name: json.loads((args.directory / name).read_text()) for name in verify.required_names()}
    result = verify.verify_suite(bundle)
    assert result["verified_new_box_exclusions"]
    passed = []

    # Exact fractional-packing rule: total weight3, vertex loads2, scale2.
    verify.weighted_bound([{1, 2}, {2, 3}, {1, 3}], [1, 1, 1], 2, 1)
    passed.append(rejected("weighted vertex overload",
                           lambda: verify.weighted_bound([{1}], [2], 1, 1)))
    passed.append(rejected("weighted sum must be strictly greater",
                           lambda: verify.weighted_bound([{1}, {2}], [1, 1], 1, 2)))

    weighted = next(data for data in bundle.values() if any(r[0] == "w" for r in data["records"]))
    for label, mutation in (
        ("nonpositive weighted scale", lambda row: row.__setitem__(2, 0)),
        ("nonpositive AP weight", lambda row: row[3][0].__setitem__(2, 0)),
        ("noninteger AP weight", lambda row: row[3][0].__setitem__(2, 1.5)),
        ("weighted AP touches a pole", lambda row: row[3].__setitem__(0, [0, 1, 1])),
        ("weighted AP is constant", lambda row: row[3][0].__setitem__(1, 0)),
    ):
        case = copy.deepcopy(weighted)
        mutation(next(row for row in case["records"] if row[0] == "w"))
        passed.append(rejected(label, lambda case=case: verify.verify_branch(case)))

    # Move a conditional rule whose antecedent contains a later forced point
    # to the initial state; this must fail even when all APs are well formed.
    candidate = None
    for data in bundle.values():
        for row in data["records"]:
            if row[0] != "f":
                continue
            v = row[1]
            for pair in row[2]:
                points = verify.progression(pair)
                negative = {x for x in points if verify.COLORS[x] == verify.COLORS[v]}
                if not (negative - {v} <= {data["root"]}):
                    candidate = (data, row)
                    break
            if candidate:
                break
        if candidate:
            break
    assert candidate is not None, "No activated conditional rule available for the control"
    case = copy.deepcopy(candidate[0])
    case["records"].insert(0, copy.deepcopy(candidate[1]))
    passed.append(rejected("unproved conditional antecedent", lambda: verify.verify_branch(case)))

    forcing = next(data for data in bundle.values() if any(row[0] == "t" for row in data["records"]))
    case = copy.deepcopy(forcing)
    case["records"].insert(0, next(row.copy() for row in case["records"] if row[0] == "t"))
    passed.append(rejected("premature singleton forcing", lambda: verify.verify_branch(case)))

    case = copy.deepcopy(weighted)
    case["records"].insert(0, ["budget", 0])
    passed.append(rejected("unexhausted original-color budget", lambda: verify.verify_branch(case)))

    case = copy.deepcopy(weighted)
    case["records"] = []
    passed.append(rejected("final contradiction without deductions", lambda: verify.verify_branch(case)))

    case = copy.deepcopy(weighted)
    case["initial_forced"] = [case["root"], next(x for x in verify.D if x != case["root"])]
    passed.append(rejected("additional root hypothesis", lambda: verify.verify_branch(case)))

    missing = bundle.copy()
    del missing["branch-1-3656-27-29.json"]
    passed.append(rejected("missing covering root", lambda: verify.verify_suite(missing)))
    missing = {name: data for name, data in bundle.items() if not name.startswith("branch-1-")}
    passed.append(rejected("missing endpoint color", lambda: verify.verify_suite(missing)))
    missing = {name: data for name, data in bundle.items() if not name.endswith("-29-27.json")}
    passed.append(rejected("missing budget box", lambda: verify.verify_suite(missing)))

    wrong = bundle.copy()
    name = "branch-0-1-29-27.json"
    wrong[name] = copy.deepcopy(bundle[name])
    wrong[name]["budget"] = [28, 27]
    passed.append(rejected("substituted narrower budget", lambda: verify.verify_suite(wrong)))

    wrong = bundle.copy()
    wrong[name] = copy.deepcopy(bundle[name])
    wrong[name]["root"] = 618
    passed.append(rejected("substituted root", lambda: verify.verify_suite(wrong)))

    print(json.dumps({"positive_suite_control": True, "positive_weighted_rule_control": True,
                      "rejected_controls": passed}, sort_keys=True))


if __name__ == "__main__":
    main()
