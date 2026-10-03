"""Complete, ranged uniform row-budget coefficients for the remaining cores.

Graph-only necessary relaxation. The outside columns range over the complement
of the ENTIRE common neighborhood. Neither rows nor physical columns are
identified under additional symmetries.
"""
import argparse
import collections
import hashlib
import itertools
import json
import math
from pathlib import Path


def need(ok, why):
    if not ok:
        raise ValueError(why)


def canon(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":")).encode()


def coefficients(scores):
    """Grouped binomial product, coefficient z^5 and x-degree at most100."""
    smallest = sorted(scores)
    if sum(smallest[:5]) > 100:
        return []
    groups = collections.Counter(scores)
    dp = {(0, 0): 1}
    for cost, number in sorted(groups.items()):
        nd = collections.defaultdict(int)
        for (size, total), count in dp.items():
            for take in range(min(number, 5-size, (100-total)//cost)+1):
                nd[size+take, total+take*cost] += count*math.comb(number, take)
        dp = dict(nd)
    return sorted([[s, c] for (n, s), c in dp.items() if n == 5])


ap = argparse.ArgumentParser()
ap.add_argument("--domain", type=Path, required=True)
ap.add_argument("--output", type=Path, required=True)
ap.add_argument("--start", type=int, required=True)
ap.add_argument("--stop", type=int, required=True)
args = ap.parse_args()
need(not args.output.exists(), "preserve any completed output")
domain = json.loads(args.domain.read_text())
need(domain["records_sha256"] == hashlib.sha256(canon(domain["records"])).hexdigest()
     == "709c375afac0a4fb76946d5590df22bd23b26eb2334049b01f121f4b31e6b768",
     "complete checked capacity domain")
cores = []
for r in domain["records"]:
    if len(r["C"]) < 6:
        continue
    for s in r["surviving_core_sizes"]:
        for b0 in itertools.combinations(r["C"], s):
            cores.append((r["A0"], list(b0), r["C"]))
cores.sort(key=lambda r: (r[0], r[1]))
need(len(cores) == 3400 and 0 <= args.start < args.stop <= 3400,
     "every remaining core and declared disjoint range")
squares = [q for q in range(1, 617) if pow(q, 308, 617) == 1]
nonsquares = [t for t in range(1, 617) if pow(t, 308, 617) == 616]
v = {p for d in range(1, 617)
     if all(pow((1+j*d) % 617, 308, 617) == 616 for j in range(1, 7))
     for p in [(1+j*d) % 617 for j in range(1, 7)]}
ratios = v | {pow(t, 615, 617) for t in v}
masks = {q: sum(1 << (q*d % 617) for d in ratios) for q in squares}
records = []
cache = {}
for a0, b0, common in cores[args.start:args.stop]:
    key = tuple(a0)
    if key not in cache:
        buckets = collections.defaultdict(int)
        for t in nonsquares:
            if t not in common:
                d0 = sum(not masks[q] & (1 << t) for q in a0)
                buckets[d0] |= 1 << t
        cache[key] = buckets
    buckets = cache[key]
    k = 14-len(b0)
    bm = sum(1 << t for t in b0)
    scores = []
    for q in squares:
        if q in a0:
            continue
        # All adjacent costs are <=5, all nonadjacent costs are >=6.
        # There are at least66-|C|>=58 adjacent outside columns, and k<=9.
        left, outside = k, 0
        for cost, mask in sorted(buckets.items()):
            take = min(left, (mask & masks[q]).bit_count())
            left -= take
            outside += cost*take
            if not left:
                break
        need(left == 0, "exact cheapest outside columns all adjacent")
        g = len(b0)-(masks[q] & bm).bit_count()
        scores.append([q, 5*g+outside])
    coeff = coefficients([h for q, h in scores])
    records.append({"A0": a0, "B0": b0, "C": common, "scores": scores,
                    "weighted_lower": sum(sorted(h for q, h in scores)[:5]),
                    "row_coefficients": coeff,
                    "row_choices": sum(n for cost, n in coeff)})
result = {"schema": "private-character617-size24-row-budget-v1",
          "agent": "six-vdw-3", "role": "researcher", "part_sizes": [10, 14],
          "missing_budget": 20, "scaled_budget": 100, "additional_rows": 5,
          "start": args.start, "stop": args.stop, "domain_cores": 3400,
          "records": records, "records_sha256": hashlib.sha256(canon(records)).hexdigest(),
          "row_choices": sum(r["row_choices"] for r in records),
          "surviving_cores": sum(r["row_choices"] > 0 for r in records),
          "status": "COMPLETE_PRIVATE_ROW_BUDGET_RANGE"}
args.output.write_text(json.dumps(result, sort_keys=True)+"\n")
print(json.dumps({k: v for k, v in result.items() if k != "records"}))
