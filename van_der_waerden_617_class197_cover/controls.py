"""Negative controls for coverage, actual APs, screens and exact inequalities."""
from copy import deepcopy
import json
from pathlib import Path
import verify
import verify_leaf

HERE = Path(__file__).parent


def leaves(node):
    if "leaf" in node:
        return [node["leaf"]]
    return leaves(node["unchanged"])+leaves(node["edited"])


def main():
    cases = {s: json.loads((HERE / f"certificates/phase-{s}.json").read_text())
             for s in (184, 201, 205, 269)}
    outcomes = []

    def reject(name, phase, mutate, message):
        candidate = deepcopy(cases[phase])
        mutate(candidate)
        try:
            verify.check(candidate, HERE / f"base/certificates/phase-{phase}.json", HERE / "base/verify.py")
        except ValueError as exc:
            if message not in str(exc):
                raise AssertionError(f"{name}: unexpected rejection {exc}") from exc
            outcomes.append({"control": name, "result": "REJECTED", "reason": str(exc)})
        else:
            raise AssertionError(f"{name}: invalid proof accepted")

    reject("missing edited branch", 201, lambda x: x["tree"].pop("edited"), "Exactly two children")
    reject("missing unchanged branch", 201, lambda x: x["tree"].pop("unchanged"), "Exactly two children")
    reject("arbitrary inherited assumption", 201,
           lambda x: x["tree"].update({"forced": [2065]}), "Exactly two children")
    reject("repeated split", 184,
           lambda x: x["tree"]["edited"].update({"split": 2548}), "New eligible split")
    reject("boolean split", 201, lambda x: x["tree"].update({"split": True}), "New eligible split")
    reject("ineligible split", 201, lambda x: x["tree"].update({"split": -1}), "New eligible split")
    reject("unsupported root budget", 201, lambda x: x.update({"class_cap": 195}), "Tree frontier")
    reject("boolean root budget", 201, lambda x: x.update({"class_cap": True}), "Tree frontier")
    reject("wrong root phase", 201, lambda x: x.update({"phase": 205}), "Tree base phase")
    reject("wrong base bytes", 201, lambda x: x.update({"base_certificate_sha256": "0"*64}), "Tree base bytes")
    reject("wrong leaf phase", 201, lambda x: leaves(x["tree"])[0].update({"phase": 205}), "Leaf phase/base")
    reject("unsupported leaf budget", 201,
           lambda x: leaves(x["tree"])[0].update({"class_cap": 197}), "Frontier")
    reject("extra leaf state", 201,
           lambda x: leaves(x["tree"])[0].update({"forbidden": [2065]}), "Schema")
    reject("zero denominator", 269,
           lambda x: leaves(x["tree"])[0].update({"denominator": 0}), "Frontier")
    reject("zero AP step", 269,
           lambda x: leaves(x["tree"])[0]["color0_APs"][0].__setitem__(1, 0), "Actual AP integers")
    reject("out of range AP", 269,
           lambda x: leaves(x["tree"])[0]["color0_APs"][0].__setitem__(0, -1), "Actual crossing coordinates")
    reject("boolean AP weight", 269,
           lambda x: leaves(x["tree"])[0]["color0_APs"][0].__setitem__(2, True), "AP entry")
    reject("negative AP weight", 269,
           lambda x: leaves(x["tree"])[0]["color0_APs"][0].__setitem__(2, -1), "Positive unique AP")
    reject("duplicate AP", 269,
           lambda x: leaves(x["tree"])[0]["color0_APs"].append(leaves(x["tree"])[0]["color0_APs"][0]),
           "Positive unique AP")
    reject("unrepaired point overload", 269,
           lambda x: leaves(x["tree"])[0]["color0_APs"][0].__setitem__(2, 100_000_000), "Exact point capacity")
    reject("no cover-two strengthening", 269,
           lambda x: leaves(x["tree"])[0].update({"color0_cover2": []}), "No strict exact")
    reject("duplicate triple AP", 269,
           lambda x: leaves(x["tree"])[0]["color0_cover2"][0][0].__setitem__(1,
                       leaves(x["tree"])[0]["color0_cover2"][0][0][0]), "Three distinct unique APs")
    reject("negative triple weight", 269,
           lambda x: leaves(x["tree"])[0]["color0_cover2"][0].__setitem__(1, -1), "Positive triple weight")
    reject("duplicate cut", 269,
           lambda x: leaves(x["tree"])[0]["color0_cover2"].append(leaves(x["tree"])[0]["color0_cover2"][0]),
           "Three distinct unique APs")

    # Locate three actual base APs sharing one eligible point. They cannot
    # support a valid two-hit assertion. This exercises the hypothesis of
    # the combinatorial cut rather than a syntactic malformed-row test.
    phase = 269
    base = json.loads((HERE / f"base/certificates/phase-{phase}.json").read_text())
    old = verify.module(HERE / "base/verify.py", "control_old_base")
    old.check_case(base)
    load = [0]*3704
    for a, d, w in base["color0_APs"]:
        for j in range(7):
            load[a+j*d] += w
    delta = 196*base["denominator"]-sum(w for a, d, w in base["color0_APs"])
    incidence = {}
    for a, d, w in base["color0_APs"]:
        for j in range(7):
            x = a+j*d
            if base["denominator"]-load[x] <= delta:
                incidence.setdefault(x, []).append([a, d])
    point = next(x for x, aps in sorted(incidence.items()) if len(aps) >= 3)
    common_triple = incidence[point][:3]
    reject("cover-two common intersection", 269,
           lambda x: leaves(x["tree"])[0]["color0_cover2"][0].__setitem__(0, common_triple),
           "Nonempty petals and empty common intersection")
    reject("surcharge at ineligible position", 269,
           lambda x: leaves(x["tree"])[0].update({"color0_surcharges": [[-1, 1]]}),
           "Eligible unique positive surcharge")
    reject("negative surcharge", 269,
           lambda x: leaves(x["tree"])[0].update({"color0_surcharges": [[point, -1]]}), "Eligible unique")
    reject("surcharge penalty erases strict gap", 269,
           lambda x: leaves(x["tree"])[0].update({"color0_surcharges": [[point, 1_000_000_000]]}),
           "No strict exact")

    # An unchanged-child proof is valid only under its inherited condition.
    # It must be reported as conditional and cannot replace a complete tree.
    branch = cases[201]["tree"]["unchanged"]["leaf"]
    result = verify_leaf.check(branch, HERE / "base/certificates/phase-201.json",
                               HERE / "base/verify.py", forbidden={2065})
    if result["status"] != "VERIFIED_EXACT_CONDITIONAL_BRANCH_EXCLUSION":
        raise AssertionError("Conditional proof mislabeled")
    reject("isolated child substituted for full coverage", 201,
           lambda x: x.update({"tree": {"leaf": deepcopy(branch)}}), "Exact point capacity")
    print(json.dumps({"agent": "six-vdw-3", "role": "researcher", "negative_controls": len(outcomes),
                      "all_rejected": True, "conditional_child_scope_checked": True,
                      "outcomes": outcomes}))


if __name__ == "__main__":
    main()
