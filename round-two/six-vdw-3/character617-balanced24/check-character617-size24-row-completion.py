"""Literal reversed adjacency / row-mask popcount independent minimum checker.

The exact earlier individual-factor coefficient certifies coverage, combined
with every physical row tuple's legality and uniqueness. No producer row DFS
or bit-sliced cost addition is imported.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path


def need(ok, why):
    if not ok:
        raise ValueError(why)


def canon(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":")).encode()


def inverse(x):
    a, b, u, v = 617, x, 0, 1
    while b:
        z = a//b
        a, b, u, v = b, a-z*b, v, u-z*v
    need(a == 1, "literal field inverse")
    return u % 617


ap = argparse.ArgumentParser()
ap.add_argument("--domain", type=Path, required=True)
ap.add_argument("--selection", type=Path, required=True)
ap.add_argument("--input", type=Path, required=True)
ap.add_argument("--output", type=Path, required=True)
args = ap.parse_args()
need(not args.output.exists(), "preserve independent output")
domain = json.loads(args.domain.read_text())
need(domain["records_sha256"] == hashlib.sha256(canon(domain["records"])).hexdigest()
     == "3ef4aded675b0c98bba22df7ae280b5623b2429a8906bedc26cbf2afa8d87ddd"
     and domain["status"] == "COMPLETE_PRIVATE_ROW_BUDGET_AUTHOR_CHECKED", "exact independently checked row domain")
data = json.loads(args.input.read_text())
indices = json.loads(args.selection.read_text())
need(data["schema"] == "private-character617-size24-row-completion-v1"
     and data["part_sizes"] == [10, 14] and data["missing_budget"] == 20
     and data["scaled_row_budget"] == 100 and data["additional_rows"] == 5,
     "actual conditional minimum premises")
need(data["selected_core_indices"] == indices and len(indices) == len(set(indices))
     and all(type(i) is int and 0 <= i < 3400 for i in indices)
     and len(data["records"]) == len(indices), "entire distinct selected batch")
need(data["records_sha256"] == hashlib.sha256(canon(data["records"])).hexdigest(), "untrusted whole record digest")
squares = sorted({q*q % 617 for q in range(1, 617)})
nonsquares = sorted(set(range(1, 617))-set(squares))
sset, tset = set(squares), set(nonsquares)
v = set()
for d in range(1, 617):
    support = {(1+j*d) % 617 for j in range(1, 7)}
    if support <= tset:
        v.update(support)
ratios = v | {inverse(t) for t in v}
reverse = {t: {q for q in squares if t*inverse(q) % 617 in ratios} for t in nonsquares}
reverse_masks = {t: sum(1 << q for q in reverse[t]) for t in nonsquares}
records = []
for index, actual in zip(indices, data["records"]):
    core = domain["records"][index]
    a0, b0, common = core["A0"], core["B0"], core["C"]
    need(common == [t for t in nonsquares if set(a0) <= reverse[t]], "entire literal common set")
    outside = [t for t in nonsquares if t not in common]
    k = 14-len(b0)
    weights = dict(core["scores"])
    base = sum(1 << q for q in a0)
    previous, answers, histogram = None, [], collections.Counter()
    for item in actual["answers"]:
        need(type(item) is list and len(item) == 6 and all(type(q) is int for q in item), "literal tuple and integer minimum")
        added = item[:5]
        need(added == sorted(set(added)) and len(added) == 5 and set(added) <= sset-set(a0), "five physical distinct added rows")
        need(previous is None or previous < added, "strict tuple ordering proves no repeated row choice")
        previous = added
        need(sum(weights[q] for q in added) <= 100, "within the complete allocated coefficient domain")
        rowmask = base | sum(1 << q for q in added)
        cost_counts = [0]*11
        for t in outside:
            cost_counts[10-(reverse_masks[t] & rowmask).bit_count()] += 1
        need(cost_counts[0] == 0 and sum(cost_counts) == len(outside), "every actual noncommon physical column")
        missing = sum(10-(reverse_masks[t] & rowmask).bit_count() for t in b0)
        remaining = k
        for cost, multiplicity in enumerate(cost_counts):
            take = min(remaining, multiplicity)
            missing += cost*take
            remaining -= take
        need(remaining == 0 and missing == item[5], "exact whole relaxed column minimum")
        answers.append(added+[missing])
        histogram[missing] += 1
    need(len(answers) == core["row_choices"], "legality, uniqueness and complete independently counted coefficient imply coverage")
    expected = {"core_index": index, "A0": a0, "B0": b0, "C": common,
                "row_choices": len(answers), "answers": answers,
                "conditional_minimum": min(histogram) if histogram else None,
                "missing_histogram": sorted([list(x) for x in histogram.items()]),
                "remaining_row_choices": sum(n for m, n in histogram.items() if m <= 20)}
    need(actual == expected, "whole actual row/minimum transcript")
    records.append(expected)
result = {"schema": data["schema"], "agent": "six-vdw-3", "role": "researcher",
          "part_sizes": [10, 14], "missing_budget": 20, "scaled_row_budget": 100,
          "additional_rows": 5, "selected_core_indices": indices, "records": records,
          "records_sha256": hashlib.sha256(canon(records)).hexdigest(),
          "row_choices": sum(r["row_choices"] for r in records),
          "remaining_row_choices": sum(r["remaining_row_choices"] for r in records),
          "status": "COMPLETE_PRIVATE_RELAXED_ROW_COMPLETION_BATCH"}
need(data == result, "entire independent mathematical transcript")
args.output.write_text(json.dumps(result, sort_keys=True)+"\n")
print(json.dumps({k: v for k, v in result.items() if k not in ("records", "selected_core_indices")}))
