"""Private first-five row-capacity reduction for the size24 10/14 split.

An optimal column packing fills all available singleton-missing columns (up to
capacity two at each of the five rows). Replacing an incident larger missing
pattern by an unused singleton preserves cardinality and frees other capacity.
Remaining columns form a five-vertex hypergraph packing in residual capacities.
This is only a necessary prefix cut, with no full-support feasibility assertion.
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


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(",", ":")).encode()


ap = argparse.ArgumentParser()
ap.add_argument("--input", type=Path, required=True)
ap.add_argument("--output", type=Path, required=True)
args = ap.parse_args()
need(not args.output.exists(), "preserve previous pilot")
data = json.loads(args.input.read_text())
need(data["five_records_sha256"] == "91e05116779017c8c5ed60a23094a1cc3cfc15a8193aa5c010151916253d4f4b", "new whole independently checked domain")
sq = [q for q in range(1, 617) if pow(q, 308, 617) == 1]
ns = [t for t in range(1, 617) if pow(t, 308, 617) == 616]
supports = [[(1+j*d) % 617 for j in range(1, 7)] for d in range(1, 617)
            if all(pow((1+j*d)%617, 308, 617) == 616 for j in range(1, 7))]
v = {t for s in supports for t in s}
ratios = v | {pow(t, 615, 617) for t in v}
neighbors = {q: sum(1 << (q*d % 617) for d in ratios) for q in sq}
universe = sum(1 << t for t in ns)
records = []
hist = collections.Counter()
remaining, core_cases = 0, 0
for row in data["five_records"]:
    a0, common = row["A0"], row["C"]
    masks = [neighbors[q] for q in a0]
    cm = universe
    for m in masks:
        cm &= m
    need(cm.bit_count() == len(common), "whole common size")
    singleton = []
    for i in range(5):
        m = universe
        for j, nb in enumerate(masks):
            if j != i:
                m &= nb
        singleton.append((m & ~cm).bit_count())
    base = sum(min(n, 2) for n in singleton)
    upper = (10+base)//2
    required = 14-len(common)
    result = {"A0": a0, "C": common, "singleton_counts": singleton,
              "singleton_capacity": base, "outside_cardinality_upper": upper,
              "exact_outside_maximum": None, "surviving_core_sizes": []}
    if upper >= required:
        holes = tuple(2-min(n, 2) for n in singleton)
        patterns = []
        for pattern in range(1, 32):
            if pattern.bit_count() < 2 or any((pattern >> i)&1 and not holes[i] for i in range(5)):
                continue
            m = universe
            for i in range(5):
                m &= (~masks[i]) if (pattern >> i)&1 else masks[i]
            number = m.bit_count()
            if number:
                patterns.append((pattern, number))
        dp = {(0,0,0,0,0): 0}
        for pattern, number in patterns:
            other = dict(dp)
            sites = [i for i in range(5) if (pattern >> i)&1]
            for used, packed in dp.items():
                for take in range(1, min(number, *(holes[i]-used[i] for i in sites))+1):
                    new = tuple(used[i] + take*((pattern >> i)&1) for i in range(5))
                    other[new] = max(other.get(new, -1), packed+take)
            dp = other
        exact = base+max(dp.values())
        result["exact_outside_maximum"] = exact
        result["surviving_core_sizes"] = list(range(max(4, 14-exact), len(common)+1))
        if result["surviving_core_sizes"]:
            remaining += 1
            core_cases += sum(math.comb(len(common), s) for s in result["surviving_core_sizes"])
    hist[len(common), base, bool(result["surviving_core_sizes"])] += 1
    records.append(result)
output = {"schema": "private-character617-size24-rowcapacity-v1", "agent": "six-vdw-3", "role": "researcher",
          "part_sizes": [10,14], "missing_budget": 20, "first_five_maximum_missing_per_row": 2,
          "domain_five_sets": len(records), "remaining_five_sets": remaining, "remaining_labeled_cores": core_cases,
          "histogram": [[c,b,s,n] for (c,b,s),n in sorted(hist.items())],
          "records_sha256": hashlib.sha256(canonical(records)).hexdigest(), "records": records,
          "status": "COMPLETE_PRIVATE_CAPACITY_PILOT_REQUIRES_INDEPENDENT_CHECK"}
args.output.write_text(json.dumps(output, sort_keys=True)+"\n")
print(json.dumps({k:v for k,v in output.items() if k not in ("records", "histogram")}))
print(json.dumps({"remaining_by_common_size": sorted(collections.Counter(len(r["C"]) for r in records if r["surviving_core_sizes"]).items())}))
