"""Inherited AP controls plus rejection controls for the new profile cover."""
import argparse
import copy
import itertools
import json
from pathlib import Path

import generate
import verify


def rejected(name, action, results):
    try:
        action()
    except ValueError as error:
        results.append({"name": name, "rejected": True, "reason": str(error)})
        return
    raise AssertionError(f"Invalid certificate accepted: {name}")


def oracle_controls():
    # Four abstract vertices and up to three hyperedges, including empty and
    # repeated edges. The oracle enumerates hitting sets, not disjoint packings.
    # A failed greedy search is deliberately left without any conclusion.
    cases = certificates = 0
    for size in (1, 2, 3):
        for masks in itertools.combinations_with_replacement(range(16), size):
            edges = [(mask, index, 1) for index, mask in enumerate(masks)]
            for count in range(1, 6):
                cases += 1
                witness = generate.select_witness(edges, count)
                if witness is None:
                    continue
                certificates += 1
                petals = [{x for x in range(4) if masks[index] & (1 << x)}
                          for index, d in witness]
                if not any(not petal for petal in petals):
                    verify.check_packing(petals, count)
                feasible = any(h.bit_count() < count and all(h & mask for mask in masks)
                               for h in range(16))
                if feasible:
                    raise AssertionError("Greedy certificate contradicted by a brute-force hitting set")
    return {"abstract_hypergraph_budget_cases": cases,
            "packing_certificates_checked_against_hitting_sets": certificates}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    bundle = {name: json.loads((args.directory / name).read_text())
              for name in verify.required_names()}
    verify.verify_suite(bundle)
    proof = bundle["branch-0-1-29-30.json"]
    index = next(i for i, row in enumerate(proof["records"])
                 if row[0] == "m" and any(row[1] not in {a + j * d for j in range(7)}
                                          for a, d in row[2]))
    partial = copy.deepcopy(proof)
    partial.update(status="STALLED", contradiction={})
    partial["records"] = copy.deepcopy(proof["records"][:index + 1])
    verify.verify_branch(partial, complete=False)
    results = []

    def mutation(name, change):
        bad = copy.deepcopy(partial)
        change(bad)
        rejected(name, lambda: verify.verify_branch(bad, complete=False), results)

    mutation("earlier_format_with_mixed_tag", lambda d: d.update(format="qr617-weighted-conditional-color-budget-v1"))
    mutation("mixed_target_already_forced", lambda d: d["records"][-1].__setitem__(1, d["root"]))
    mutation("missing_mixed_APs", lambda d: d["records"][-1].__setitem__(2, []))
    mutation("insufficient_mixed_packing", lambda d: d["records"][-1][2].pop())
    mutation("intersecting_mixed_petals", lambda d: d["records"][-1][2].__setitem__(1, d["records"][-1][2][0]))
    mutation("constant_AP", lambda d: d["records"][-1][2][0].__setitem__(1, 0))
    mutation("prefix_AP_hits_pole", lambda d: d["records"][-1][2].__setitem__(0, [0, 1]))
    mutation("prefix_AP_outside_interval", lambda d: d["records"][-1][2].__setitem__(0, [3700, 1]))
    mutation("legacy_tag_requires_target_in_every_AP", lambda d: d["records"][-1].__setitem__(0, "f"))
    mutation("extra_covering_hypothesis", lambda d: d.update(initial_forced=[d["root"], d["records"][-1][1]]))
    mutation("unknown_status", lambda d: d.update(status="UNKNOWN"))
    mutation("noninteger_budget", lambda d: d["budget"].__setitem__(0, 29.0))
    mutation("wrong_endpoint_for_cover_clause", lambda d: d["records"][-1][2].__setitem__(0, verify.ENDPOINT_APS[1]))
    if verify.COLORS[partial["records"][-1][1]] == partial["endpoint"]:
        mutation("mixed_endpoint_petal_wrong_original_class",
                 lambda d: d["records"][-1][2].__setitem__(0, verify.ENDPOINT_APS[0]))

    state_before = copy.deepcopy(partial)
    state_before["records"].pop()
    state = verify.verify_branch(state_before, complete=False, include_state=True)
    forced = set(state["forced_positions"])
    v = partial["records"][-1][1]
    unproved = None
    for diff in range(1, 20):
        for j in range(7):
            start = v - j * diff
            if start < 0 or start + 6 * diff > verify.LAST:
                continue
            points = {start + k * diff for k in range(7)}
            if points <= verify.D and any(x != v and verify.COLORS[x] == verify.COLORS[v]
                                         and x not in forced for x in points):
                unproved = [start, diff]
                break
        if unproved is not None:
            break
    if unproved is None:
        raise AssertionError("Could not build an unproved antecedent control")
    mutation("mixed_prefix_antecedent_unproved", lambda d: d["records"][-1][2].__setitem__(0, unproved))
    complete_bad = copy.deepcopy(proof)
    complete_bad["contradiction"] = {"reason": "too_many_forced"}
    rejected("false_terminal_cardinality", lambda: verify.verify_branch(complete_bad), results)
    missing = bundle.copy()
    missing.pop(next(iter(missing)))
    rejected("missing_covering_root", lambda: verify.verify_suite(missing), results)
    bad_box = copy.deepcopy(bundle)
    name = next(iter(bad_box))
    bad_box[name]["budget"][0] += 1
    rejected("wrong_budget_box_for_coverage", lambda: verify.verify_suite(bad_box), results)
    no_corner = {name: data for name, data in bundle.items()
                 if not (data["endpoint"] == 0 and data["budget"] == [29, 30])}
    rejected("missing_entire_endpoint0_joint_box", lambda: verify.verify_suite(no_corner), results)
    extra = bundle.copy()
    extra["branch-0-1-29-29.json"] = copy.deepcopy(proof)
    rejected("extra_unproved_joint_budget_case", lambda: verify.verify_suite(extra), results)
    narrower = bundle.copy()
    name = "branch-1-3421-29-30.json"
    narrower[name] = copy.deepcopy(bundle[name])
    narrower[name]["budget"] = [29, 29]
    rejected("earlier_narrower_budget_cannot_cover_new_box", lambda: verify.verify_suite(narrower), results)
    wrong_endpoint = bundle.copy()
    name = "branch-1-3421-30-29.json"
    wrong_endpoint[name] = copy.deepcopy(bundle[name])
    wrong_endpoint[name]["endpoint"] = 0
    rejected("endpoint_transfer_unsupported", lambda: verify.verify_suite(wrong_endpoint), results)
    packing = copy.deepcopy(bundle["branch-0-1235-30-29.json"])
    packing["contradiction"]["aps"][1] = packing["contradiction"]["aps"][0]
    rejected("intersecting_terminal_required_packing", lambda: verify.verify_branch(packing), results)
    no_endpoint1_box = {name: data for name, data in bundle.items()
                        if not (data["endpoint"] == 1 and data["budget"] == [30, 29])}
    rejected("missing_entire_endpoint1_joint_box", lambda: verify.verify_suite(no_endpoint1_box), results)
    summary = {"agent": "six-vdw-2", "role": "researcher", "valid_suite_accepted": True,
               "controls": results, **oracle_controls()}
    if args.output:
        args.output.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
