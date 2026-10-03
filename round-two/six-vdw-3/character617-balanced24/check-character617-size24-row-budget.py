"""Independent literal cost-list and individual-factor row-count checker.

No Euler criterion, producer masks, cheapest-adjacent shortcut or grouped
binomial row coefficients are used. Entire C is reconstructed literally.
"""
import argparse
import collections
import hashlib
import itertools
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
    need(a == 1, "nonzero field inverse")
    return u % 617


def individual_product(scores):
    low = min(scores)
    # A five-row monomial has reduced degree total-5*low. All reduced
    # costs are nonnegative, so discarding degrees above100-5*low is sound.
    budget = 100-5*low
    if budget < 0:
        return []
    dp = [collections.Counter() for j in range(6)]
    dp[0][0] = 1
    for score in scores:
        cost = score-low
        for j in range(5, 0, -1):
            for total, count in tuple(dp[j-1].items()):
                if total+cost <= budget:
                    dp[j][total+cost] += count
    return sorted([[s+5*low, c] for s, c in dp[5].items()])


ap = argparse.ArgumentParser()
ap.add_argument("--input", type=Path, required=True)
ap.add_argument("--domain", type=Path, required=True)
ap.add_argument("--output", type=Path, required=True)
args = ap.parse_args()
need(not args.output.exists(), "preserve independent output")
data = json.loads(args.input.read_text())
domain = json.loads(args.domain.read_text())
need(data["schema"] == "private-character617-size24-row-budget-v1"
     and data["part_sizes"] == [10, 14] and data["missing_budget"] == 20
     and data["scaled_budget"] == 100 and data["additional_rows"] == 5
     and data["domain_cores"] == 3400, "actual relaxation premises")
need(data["records_sha256"] == hashlib.sha256(canon(data["records"])).hexdigest(),
     "entire untrusted range record digest")
need(domain["status"] == "COMPLETE_PRIVATE_ROW_CAPACITY_AUTHOR_CHECKED"
     and domain["checked_five_sets"] == 76735,
     "independently complete capacity precursor")
cores = []
for item in domain["records"]:
    if len(item["C"]) < 6:
        continue
    for size, count, total in item["selected_column_counts"]:
        need(count > 0 and total > 0, "positive exact physical column coefficient")
        for b0 in itertools.combinations(item["C"], size):
            cores.append((item["A0"], list(b0), item["C"]))
cores.sort(key=lambda r: (r[0], r[1]))
need(len(cores) == 3400 and 0 <= data["start"] < data["stop"] <= 3400,
     "whole independently enumerated core family")
need(len(data["records"]) == data["stop"]-data["start"], "entire declared core range")
squares = sorted({q*q % 617 for q in range(1, 617)})
nonsquares = sorted(set(range(1, 617))-set(squares))
tset = set(nonsquares)
v = set()
for step in range(1, 617):
    points = {(1+j*step) % 617 for j in range(1, 7)}
    if points <= tset:
        v.update(points)
ratios = v | {inverse(t) for t in v}
neighbors = {q: {t for t in nonsquares if t*inverse(q) % 617 in ratios}
             for q in squares}
records, cache = [], {}
for actual, (a0, b0, common) in zip(data["records"], cores[data["start"]:data["stop"]]):
    key = tuple(a0)
    if key not in cache:
        whole_common = set.intersection(*(neighbors[q] for q in a0))
        need(sorted(whole_common) == common, "literal entire common neighborhood")
        outside = sorted(tset-whole_common)
        d0 = {t: sum(t not in neighbors[q] for q in a0) for t in outside}
        # Each physical outside column contributes exactly its full cost.
        cache[key] = {q: sorted(d0[t]+5*(t not in neighbors[q]) for t in outside)
                      for q in squares if q not in a0}
    costs = cache[key]
    k = 14-len(b0)
    scores = [[q, 5*sum(t not in neighbors[q] for t in b0)+sum(costs[q][:k])]
              for q in squares if q not in a0]
    coeff = individual_product([h for q, h in scores])
    expected = {"A0": a0, "B0": b0, "C": common, "scores": scores,
                "weighted_lower": sum(sorted(h for q, h in scores)[:5]),
                "row_coefficients": coeff,
                "row_choices": sum(n for cost, n in coeff)}
    need(actual == expected, "every actual row score and exact five-row coefficient")
    records.append(expected)
result = {"schema": data["schema"], "agent": "six-vdw-3", "role": "researcher",
          "part_sizes": [10, 14], "missing_budget": 20, "scaled_budget": 100,
          "additional_rows": 5, "start": data["start"], "stop": data["stop"],
          "domain_cores": 3400, "records": records,
          "records_sha256": hashlib.sha256(canon(records)).hexdigest(),
          "row_choices": sum(r["row_choices"] for r in records),
          "surviving_cores": sum(r["row_choices"] > 0 for r in records),
          "status": "COMPLETE_PRIVATE_ROW_BUDGET_RANGE"}
need(result == data, "entire producer/checker mathematical transcript")
args.output.write_text(json.dumps(result, sort_keys=True)+"\n")
print(json.dumps({k: v for k, v in result.items() if k != "records"}))
