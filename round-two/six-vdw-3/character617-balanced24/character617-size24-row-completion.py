"""Enumerate every allocated five-row choice and its relaxed column minimum.

The bit-sliced producer minimizes over all k columns outside the entire C;
first-five capacity/order constraints are intentionally relaxed at this stage.
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


def choices(scores):
    ordered = sorted((h, q) for q, h in scores)
    costs = [h for h, q in ordered]

    def walk(start, selected, total):
        left = 5-len(selected)
        if not left:
            yield sorted(selected)
            return
        if start+left > len(ordered) or total+sum(costs[start:start+left]) > 100:
            return
        for pos in range(start, len(ordered)-left+1):
            if total+sum(costs[pos:pos+left]) > 100:
                break
            h, q = ordered[pos]
            yield from walk(pos+1, selected+[q], total+h)

    yield from walk(0, [], 0)


def increment(planes, word):
    for i in range(4):
        planes[i], word = planes[i] ^ word, planes[i] & word
    need(word == 0, "four planes exactly suffice for ten rows")


ap = argparse.ArgumentParser()
ap.add_argument("--domain", type=Path, required=True)
ap.add_argument("--selection", type=Path, required=True)
ap.add_argument("--output", type=Path, required=True)
args = ap.parse_args()
need(not args.output.exists(), "preserve completed output")
domain = json.loads(args.domain.read_text())
need(domain["records_sha256"] == hashlib.sha256(canon(domain["records"])).hexdigest()
     == "3ef4aded675b0c98bba22df7ae280b5623b2429a8906bedc26cbf2afa8d87ddd",
     "whole separately checked allocated row domain")
indices = json.loads(args.selection.read_text())
need(len(indices) == len(set(indices)) and all(type(i) is int and 0 <= i < 3400 for i in indices),
     "explicit distinct mathematical core indices")
squares = [q for q in range(1, 617) if pow(q, 308, 617) == 1]
nonsquares = [t for t in range(1, 617) if pow(t, 308, 617) == 616]
universe = sum(1 << t for t in nonsquares)
v = {p for d in range(1, 617)
     if all(pow((1+j*d) % 617, 308, 617) == 616 for j in range(1, 7))
     for p in [(1+j*d) % 617 for j in range(1, 7)]}
ratios = v | {pow(t, 615, 617) for t in v}
masks = {q: sum(1 << (q*d % 617) for d in ratios) for q in squares}
records = []
for index in indices:
    core = domain["records"][index]
    a0, b0, common = core["A0"], core["B0"], core["C"]
    outside = universe ^ sum(1 << t for t in common)
    bm = sum(1 << t for t in b0)
    k = 14-len(b0)
    base = [0]*4
    for q in a0:
        increment(base, outside & ~masks[q])
    answers, histogram = [], collections.Counter()
    for added in choices(core["scores"]):
        planes = base.copy()
        for q in added:
            increment(planes, outside & ~masks[q])
        need(not (outside & ~(planes[0] | planes[1] | planes[2] | planes[3])),
             "outside columns are genuinely noncommon")
        remaining, minimum = k, sum(len(b0)-(masks[q] & bm).bit_count() for q in added)
        for cost in range(1, 11):
            mask = outside
            for j in range(4):
                mask &= planes[j] if (cost >> j) & 1 else ~planes[j]
            take = min(remaining, mask.bit_count())
            remaining -= take
            minimum += cost*take
            if not remaining:
                break
        need(remaining == 0, "entire relaxed outside column domain")
        answers.append(added+[minimum])
        histogram[minimum] += 1
    answers.sort()
    need(len(answers) == core["row_choices"], "every independently counted actual five-row choice")
    records.append({"core_index": index, "A0": a0, "B0": b0, "C": common,
                    "row_choices": len(answers), "answers": answers,
                    "conditional_minimum": min(histogram) if histogram else None,
                    "missing_histogram": sorted(histogram.items()),
                    "remaining_row_choices": sum(n for m, n in histogram.items() if m <= 20)})
result = {"schema": "private-character617-size24-row-completion-v1",
          "agent": "six-vdw-3", "role": "researcher", "part_sizes": [10, 14],
          "missing_budget": 20, "scaled_row_budget": 100, "additional_rows": 5,
          "selected_core_indices": indices, "records": records,
          "records_sha256": hashlib.sha256(canon(records)).hexdigest(),
          "row_choices": sum(r["row_choices"] for r in records),
          "remaining_row_choices": sum(r["remaining_row_choices"] for r in records),
          "status": "COMPLETE_PRIVATE_RELAXED_ROW_COMPLETION_BATCH"}
args.output.write_text(json.dumps(result, sort_keys=True)+"\n")
print(json.dumps({k: v for k, v in result.items() if k not in ("records", "selected_core_indices")}))
