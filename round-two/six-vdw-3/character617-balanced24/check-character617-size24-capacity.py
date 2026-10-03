"""Literal five-row checker and independent full column-factor coefficient DP.

The producer's singleton replacement/remaining-hole maximum is NOT used to
compute positive-case maxima here. All31 missing-pattern types participate in
the exact finite product, including every singleton and every available column.
"""
import argparse
import collections
import hashlib
import json
import math
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def inverse(x):
    a, b, u, v = 617, x, 0, 1
    while b:
        k = a//b
        a, b, u, v = b, a-k*b, v, u-k*v
    need(a == 1, "literal inverse")
    return u % 617


def product_counts(patterns, cap=(2,2,2,2,2)):
    zero = (0,)*len(cap)
    dp = {(zero,0):1}
    for pattern, number in sorted(patterns.items()):
        sites = tuple(i for i in range(len(cap)) if (pattern >> i)&1)
        need(sites and number > 0, "actual noncommon columns")
        other = collections.defaultdict(int)
        for (used,size), count in dp.items():
            maximum = min(number, *(cap[i]-used[i] for i in sites))
            for take in range(maximum+1):
                new = tuple(used[i]+(take if i in sites else 0) for i in range(len(cap)))
                other[new,size+take] += count*math.comb(number,take)
        dp = dict(other)
    counts = collections.Counter()
    for (used,size), number in dp.items():
        counts[size] += number
    return counts


ap = argparse.ArgumentParser()
ap.add_argument("--input", type=Path, required=True)
ap.add_argument("--domain", type=Path, required=True)
ap.add_argument("--output", type=Path, required=True)
ap.add_argument("--start", type=int, required=True)
ap.add_argument("--stop", type=int, required=True)
args = ap.parse_args()
need(not args.output.exists(), "preserve independent output")
data = json.loads(args.input.read_text())
domain = json.loads(args.domain.read_text())
need(data["schema"] == "private-character617-size24-rowcapacity-v1" and data["part_sizes"] == [10,14]
     and data["missing_budget"] == 20 and data["first_five_maximum_missing_per_row"] == 2,
     "exact size24 row-capacity premises")
need(domain["five_records_sha256"] == hashlib.sha256(canon(domain["five_records"])).hexdigest() == "91e05116779017c8c5ed60a23094a1cc3cfc15a8193aa5c010151916253d4f4b", "whole separately proved domain")
need(len(data["records"]) == len(domain["five_records"]) == 76735, "every five-row record")
need(data["records_sha256"] == hashlib.sha256(canon(data["records"])).hexdigest(), "whole repaired-hash evidence")
need(0 <= args.start < args.stop <= 76735, "declared complete range")
sq = sorted({q*q % 617 for q in range(1,617)})
ns = sorted(set(range(1,617))-set(sq))
nsset = set(ns)
v = set()
for step in range(1,617):
    points = {(1+j*step)%617 for j in range(1,7)}
    if points <= nsset:
        v.update(points)
ratios = v | {inverse(t) for t in v}
neighbors = {q:{t for t in ns if t*inverse(q)%617 in ratios} for q in sq}
records, histogram = [], collections.Counter()
remaining = cores = labeled_column_packs = 0
for actual, row in zip(data["records"][args.start:args.stop], domain["five_records"][args.start:args.stop]):
    a0, common = row["A0"], row["C"]
    need(actual["A0"] == a0 and actual["C"] == common, "every row binds to independent tuple domain")
    literal_common = {t for t in ns if all(t in neighbors[q] for q in a0)}
    need(sorted(literal_common) == common, "full literal common neighborhood")
    singleton = []
    for i in range(5):
        part = nsset.copy()
        for j,q in enumerate(a0):
            if j != i:
                part.intersection_update(neighbors[q])
        singleton.append(len(part-literal_common))
    base = sum(min(2,n) for n in singleton)
    upper = (10+base)//2
    expected = {"A0":a0, "C":common, "singleton_counts":singleton, "singleton_capacity":base,
                "outside_cardinality_upper":upper, "exact_outside_maximum":None, "surviving_core_sizes":[]}
    pack_counts = []
    if upper >= 14-len(common):
        patterns = collections.Counter()
        for t in ns:
            if t not in literal_common:
                pattern = sum(1<<i for i,q in enumerate(a0) if t not in neighbors[q])
                patterns[pattern] += 1
        counts = product_counts(patterns)
        expected["exact_outside_maximum"] = max(counts)
        expected["surviving_core_sizes"] = [s for s in range(4,len(common)+1) if counts[14-s]]
        pack_counts = [[s, counts[14-s], math.comb(len(common),s)*counts[14-s]] for s in expected["surviving_core_sizes"]]
    need(actual == expected, "full row-capacity maximum and every core size")
    histogram[len(common),base,bool(expected["surviving_core_sizes"])] += 1
    if expected["surviving_core_sizes"]:
        remaining += 1
        cores += sum(math.comb(len(common),s) for s in expected["surviving_core_sizes"])
        labeled_column_packs += sum(n for s,c,n in pack_counts)
        records.append({"A0":a0, "C":common, "selected_column_counts":pack_counts})
result = {"agent":"six-vdw-3", "role":"researcher", "start":args.start, "stop":args.stop,
          "checked_five_sets":args.stop-args.start, "remaining_five_sets":remaining,
          "remaining_labeled_cores":cores, "labeled_fourteen_column_packs":labeled_column_packs,
          "histogram":[[c,b,s,n] for (c,b,s),n in sorted(histogram.items())], "records":records,
          "records_sha256":hashlib.sha256(canon(records)).hexdigest(),
          "status":"COMPLETE_PRIVATE_ROW_CAPACITY_RANGE_CHECKED"}
args.output.write_text(json.dumps(result,sort_keys=True)+"\n")
print(json.dumps({k:v for k,v in result.items() if k not in ("histogram","records")}))
