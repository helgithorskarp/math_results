"""Reviewer-owned exact audit of the entropy cover and global rational bound."""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import argparse
import json

SCALE = 10**18


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fraction(obj):
    return Fraction(obj["numerator"], obj["denominator"])


def least_grid_root(value, exponent):
    low, high = 0, SCALE
    while low < high:
        middle = (low + high) // 2
        if Fraction(middle, SCALE) ** exponent >= value:
            high = middle
        else:
            low = middle + 1
    answer = Fraction(low, SCALE)
    require(answer**exponent >= value, "root is not an upper bound")
    require(low == 0 or Fraction(low - 1, SCALE) ** exponent < value,
            "root is not the least grid upper bound")
    return answer


def event_certificate(q, r):
    blocks = tuple(range(1, q))
    incidence = Counter()
    kinds = Counter()
    for triple in combinations(blocks, 3):
        colours = {block: int(block < r) for block in triple}
        for centre in triple:
            outside = tuple(block for block in triple if block != centre)
            if colours[outside[0]] == colours[centre] == colours[outside[1]]:
                kind = "same"
            elif colours[outside[0]] == colours[outside[1]] != colours[centre]:
                kind = "minority"
            else:
                kind = "majority"
            kinds[kind] += 1
            for edge in combinations(triple, 2):
                incidence[edge] += 1
    reads = set(incidence.values())
    require(set(incidence) == set(combinations(blocks, 2)), "coordinate omitted")
    require(len(reads) == 1, "nonuniform coordinate cover")
    return kinds, reads.pop(), sum(incidence.values())


def check(local_path, target_path, parent_path):
    local = json.loads(Path(local_path).read_text())
    target = json.loads(Path(target_path).read_text())
    parent = json.loads(Path(parent_path).read_text())["census"]
    require(local["status"] == "REVIEWER_LITERAL_MASK_SCAN_COMPLETE", "local status")
    require(local["domains"] == {"RR": 37823, "RB": 35714, "BB": 37823},
            "domain counts")
    probabilities = {}
    for name in ("same", "majority", "minority"):
        own = local["probabilities"][name]
        submitted = target["local"]["probabilities"][name]
        require((own["allowed"], own["total"], own["mask_classes"]) ==
                (submitted["allowed"], submitted["total"], submitted["mask_classes"]),
                "submitted local count mismatch: " + name)
        probabilities[name] = Fraction(own["allowed"], own["total"])

    target_global = target["global_bound"]
    parent_classes = {(row["q"], row["r"]): row for row in parent["classes"]}
    submitted_classes = {(row["q"], row["r"]): row
                         for row in target_global["classes"]}
    expected_keys = {(q, r) for q in range(7, 11) for r in range(5, q + 1)}
    require(len(target_global["classes"]) == 18, "submitted class count")
    require(set(parent_classes) == set(submitted_classes) == expected_keys,
            "18-class coverage")

    before = 0
    after = Fraction(0)
    total_events = 0
    total_occurrences = 0
    task_ids = 0
    minimum_removal = Fraction(1)
    class_summary = []
    for q, r in sorted(expected_keys):
        kinds, read, occurrences = event_certificate(q, r)
        power = Fraction(1)
        for name, count in kinds.items():
            power *= probabilities[name] ** count
        upper = least_grid_root(power, read)
        inherited = parent_classes[q, r]
        submitted = submitted_classes[q, r]
        require(submitted["read"] == read, "submitted read multiplicity")
        require(fraction(submitted["probability_upper"]) == upper,
                "submitted root upper")
        require(submitted["before"] == inherited["after"], "parent class weight")
        require(submitted["core_count"] == inherited["core_count"], "core count")
        require(fraction(submitted["after_upper"]) == inherited["after"] * upper,
                "class weighted upper")
        before += inherited["after"]
        after += inherited["after"] * upper
        task_ids += inherited["core_count"]
        total_events += sum(kinds.values())
        total_occurrences += occurrences
        minimum_removal = min(minimum_removal, 1 - upper)
        class_summary.append({"q": q, "r": r, "events": dict(kinds),
                              "read": read,
                              "upper_numerator": upper.numerator,
                              "upper_denominator": upper.denominator})

    removed = (before - after) / before
    require(before == parent["after"] == target_global["before"], "global parent count")
    require(after == fraction(target_global["after_upper"]), "global upper count")
    require(removed == fraction(target_global["removed_lower"]), "removal fraction")
    require(task_ids == target_global["task_ids"] ==
            target_global["affected_task_ids"] == 2189178, "task coverage")
    require(total_events == 2952 and total_occurrences == 8856, "event coverage totals")
    require(4 * after <= 3 * before, "declared quarter-removal gate")
    require(target_global["new_task_decisions"] == 0 and
            target_global["solver_calls"] == 0 and
            target_global["q10_child_inputs_inspected"] == 0 and
            not target_global["target_found"],
            "scope mismatch")
    return {
        "status": "REVIEWER_ENTROPY_AND_GLOBAL_BOUND_VERIFIED",
        "local_allowed": {name: local["probabilities"][name]["allowed"]
                          for name in ("same", "majority", "minority")},
        "classes": len(class_summary),
        "abstract_events": total_events,
        "coordinate_occurrences": total_occurrences,
        "task_ids": task_ids,
        "removed_lower_numerator": removed.numerator,
        "removed_lower_denominator": removed.denominator,
        "minimum_class_removal_numerator": minimum_removal.numerator,
        "minimum_class_removal_denominator": minimum_removal.denominator,
        "gate": "PASS",
        "new_task_decisions": 0,
        "target_found": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("local")
    parser.add_argument("target_expected")
    parser.add_argument("parent_expected")
    args = parser.parse_args()
    print(json.dumps(check(args.local, args.target_expected, args.parent_expected),
                     sort_keys=True, indent=2))
