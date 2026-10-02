"""Definition-level numeric P22 cover and nested-root certificate checker.

Imports no generator, profiler, sibling checker or solver. Scalar pruning,
family and heap primitives are copied from this author's nested_verify.py;
this remains same-author algorithmic independence, not external review.
"""
import argparse
from copy import deepcopy
import hashlib
import heapq
from itertools import combinations
import json
from pathlib import Path
import resource
import time

import os
HERE=Path(__file__).resolve().parent
ROOT=Path(os.environ.get('NATIVE20_WORKDIR','scratch/native20-evidence')).resolve()
ROOT.mkdir(parents=True,exist_ok=True)
PINS={'fixture.json':'93b7cda51cc14fa8f53c0ed89c7c1c2150b8ab6b58f823fc69b41ec7035022e6',
      'generate.py':'08a37678a11392ed46907ab30b2463d841e3e068764c09e410244490f2212381',
      'NESTED.md':'3c291c8796cc7586db522d515098debf769482dc5b2d6bf8467fd8aa03322433'}
SIZES=(0,0,1,3,5,9,12,16,19,25,29,35,39,44)
FAMILIES=(("one_minimum",1,0),("one_maximum",0,1),("two_minima",2,0),
          ("two_maxima",0,2),("mixed_pair",1,1))
METRICS={}

def need(test, message):
    if not test:
        raise ValueError(message)


def count(name, amount=1):
    METRICS[name] = METRICS.get(name, 0) + amount


def digest(obj):
    return hashlib.sha256(json.dumps(obj, separators=(",", ":")).encode()).hexdigest()


def marked(value):
    return value < 0 or value > 1


def ports(row):
    return [sum(2 ** i for i, v in enumerate(row) if v < 0),
            sum(2 ** i for i, v in enumerate(row) if v > 1)]


def simulate(row, gates):
    values = list(row)
    for a, b in gates:
        if values[a] > values[b]:
            values[a], values[b] = values[b], values[a]
    return values


def template(n, low, high):
    need(low >= 0 and high >= 0 and not low & high and (low | high) < 2 ** n,
         "invalid original marker masks")
    lows = [i for i in range(n) if low >> i & 1]
    highs = [i for i in range(n) if high >> i & 1]
    free = [i for i in range(n) if not (low | high) >> i & 1]
    row = [0] * n
    for rank, i in enumerate(lows):
        row[i] = rank - len(lows)
    for rank, i in enumerate(highs):
        row[i] = rank + 2
    return row, free


def family(n, gates, low, high, level):
    initial, free = template(n, low, high)
    touches = final = None
    active = 0
    for x in range(2 ** len(free)):
        row = list(initial)
        for j, i in enumerate(free):
            row[i] = x >> j & 1
        hit_mask = 0
        for t, (a, b) in enumerate(gates):
            hit = marked(row[a]) or marked(row[b])
            if hit:
                hit_mask |= 2 ** t
            if row[a] > row[b]:
                if not hit:
                    active |= 2 ** t
                row[a], row[b] = row[b], row[a]
        if touches is None:
            touches, final = hit_mask, ports(row)
        need(touches == hit_mask and final == ports(row), "free-dependent marker route")
        count(level + "_free_assignments")
        count(level + "_gate_evaluations", len(gates))
    redundant = (2 ** len(gates) - 1) & ~(touches | active)
    return [low, high, *final, touches.bit_count(), redundant.bit_count(), redundant]


def pruning(n, gates, record):
    low, high = record[:2]
    reference, free = template(n, low, high)
    carrier = [free.index(i) if i in free else None for i in range(n)]
    word, touches = [], 0
    for t, (a, b) in enumerate(gates):
        if marked(reference[a]) or marked(reference[b]):
            touches |= 2 ** t
            need(not record[6] >> t & 1, "marked gate also deleted as free identity")
            if reference[a] > reference[b]:
                reference[a], reference[b] = reference[b], reference[a]
                carrier[a], carrier[b] = carrier[b], carrier[a]
        elif not record[6] >> t & 1:
            word.append([carrier[a], carrier[b]])
    output_free = [i for i in range(n) if not marked(reference[i])]
    rename = {carrier[i]: j for j, i in enumerate(output_free)}
    need(sorted(rename) == list(range(len(free))), "nonbijective free-carrier routing")
    result = {"outer_record": record, "marked_touch_mask": touches,
              "input_free_wires": free, "output_free_wires": output_free,
              "input_to_output_wire": [rename[i] for i in range(len(free))],
              "retained_prefix": [[rename[a], rename[b]] for a, b in word]}
    need(touches.bit_count() == record[4] and record[6].bit_count() == record[5],
         "deletion count differs")
    need(len(word) + record[4] + record[5] == len(gates), "gates not partitioned")
    for x in range(2 ** len(free)):
        full = list(template(n, low, high)[0])
        small = [0] * len(free)
        for j, i in enumerate(free):
            full[i] = small[rename[j]] = x >> j & 1
        actual = simulate(full, gates)
        need([actual[i] for i in output_free] == simulate(small, result["retained_prefix"]),
             "conditional pruning function differs")
        count("pruning_function_assignments")
    return result


def summary(records, l, h):
    records.sort()
    classes = {}
    for row in records:
        key = tuple(row[2:4])
        d, c = classes.get(key, (0, 0))
        classes[key] = max(d, row[4]), max(c, row[4] + row[5])
    envelope = [[lo, hi, d, c] for (lo, hi), (d, c) in sorted(classes.items())]
    return {"low_count": l, "high_count": h, "envelope": envelope,
            "records_sha256": digest(records),
            "summary": {"ordinary_mass": sum(2 ** row[2] for row in envelope),
                        "semantic_mass": sum(2 ** row[3] for row in envelope),
                        "maximum_deletions": max(row[4] for row in records),
                        "maximum_semantic_deletions": max(row[4] + row[5] for row in records),
                        "maximum_redundancies": max(row[5] for row in records),
                        "port_classes": len(envelope)}}


def profiles(n, gates, level="inner"):
    result = {}
    for name, l, h in FAMILIES:
        if l + h > n:
            continue
        records = []
        for lows in combinations(range(n), l):
            other = [i for i in range(n) if i not in lows]
            for highs in combinations(other, h):
                low, high = sum(2 ** i for i in lows), sum(2 ** i for i in highs)
                records.append(family(n, gates, low, high, level))
        result[name] = summary(records, l, h)
    return result


def ceil_log(mass):
    need(mass > 0, "empty dyadic mass")
    e = 0
    while 2 ** e < mass:
        e += 1
    return e


def huffman(labels):
    heap = list(labels)
    need(bool(heap), "empty route set")
    heapq.heapify(heap)
    while len(heap) > 1:
        a, b = heapq.heappop(heap), heapq.heappop(heap)
        heapq.heappush(heap, 1 + max(a, b))
    return heap[0]


def anchor_bounds(n, data):
    result = {}
    for side, column, count_name, unary in (("low", 0, "low_count", "one_minimum"),
                                          ("high", 1, "high_count", "one_maximum")):
        chosen = {name: item for name, item in data.items() if item[count_name]}
        sizes = {name: SIZES[n - item["low_count"] - item["high_count"]]
                 for name, item in chosen.items()}
        base = min(sizes.values())
        reachable = sorted(row[column].bit_length() - 1 for row in data[unary]["envelope"])
        rows = []
        for p in reachable:
            masses = {name: sum(2 ** row[3] for row in item["envelope"] if row[column] >> p & 1)
                      for name, item in chosen.items()}
            label = max(sizes[name] + ceil_log(mass) for name, mass in masses.items() if mass)
            rows.append({"port": p, "anchored_masses": masses, "label": label,
                         "units": 2 ** (label - base)})
        units = sum(row["units"] for row in rows)
        b = huffman(row["label"] for row in rows)
        need(b == base + ceil_log(units), "Huffman and dyadic formulas differ")
        result[side] = {"base": base, "normalized_mass": units, "lower_bound": b, "rows": rows}
    return result


def bound(n, gates, level="control"):
    if n < 2:
        return 0
    return max(x["lower_bound"] for x in anchor_bounds(n, profiles(n, gates, level)).values())


from functools import lru_cache
import sys
PILOT_ROOT=ROOT
@lru_cache(None)
def checked_inner(word):
    data=profiles(7,word,"inner");anchors=anchor_bounds(7,data)
    b=max(16,*(a["lower_bound"] for a in anchors.values()))
    return {"inner_records_sha256":{name:a["records_sha256"] for name,a in data.items()},
            "inner_anchor_leaves":{side:[[r["port"],r["label"]] for r in a["rows"]] for side,a in anchors.items()},
            "inner_anchor_bounds":{side:a["lower_bound"] for side,a in anchors.items()},"inner_bound":b}
def main_nested():
    start=time.monotonic();begin=int(sys.argv[1]);stop=int(sys.argv[2]);records=[]
    for name in ["nested-screen-0-20.json","nested-screen-20-765.json"]:
        records.extend(json.loads((PILOT_ROOT/name).read_text())["sufficient_records"])
    records.sort(key=lambda x:x["remaining_position"])
    need([x["remaining_position"] for x in records]==list(range(765)),"nested cover missing")
    roots=json.loads((PILOT_ROOT/"postjoint-cover.json").read_text())["roots"]
    remaining=json.loads((PILOT_ROOT/"constant-remaining-roots.json").read_text())
    need(len(roots)==23006 and len(remaining)==765,"complete root counts differ")
    need([x["root"] for x in records]==remaining,"nested root cover differs from exact constant-stage remainder")
    prefix=json.loads((PILOT_ROOT/"p20-intake.json").read_text())["cases"][1]["gates"]
    checked=upgraded=0
    for case in records[begin:stop]:
        need(case["prefix_length"]==roots[case["root"]]["prefix_length"],"nested root length differs")
        gates=prefix+roots[case["root"]]["word"];classes=set();mass=0
        for w in case["selected_domains"]:
            lo,hi=w["original"]
            need(lo.bit_count()==hi.bit_count()==3,"outer domain is not a full (3,3) clamping")
            record=family(13,gates,lo,hi,"outer")
            need(record[:2]==[lo,hi] and record[2:4]==w["current"],"outer current masks differ")
            cost=record[4]+record[5]
            if w["constant_only"]:
                need(w["outer_record"]==record and w["inner_bound"]==16 and w["nested_label"]==cost+16,"constant fallback differs")
                b=16
            else:
                pruned=pruning(13,gates,record)
                need(pruned==w["pruning"],"complete carrier/pruning fields differ")
                values=checked_inner(tuple(map(tuple,pruned["retained_prefix"])))
                need(all(w[k]==v for k,v in values.items()),"inner exact records/leaves/bounds differ")
                b=values["inner_bound"]
                need(w["prefix_cost"]==cost and w["nested_label"]==cost+b,"nested total label differs")
                upgraded+=1
            tag=tuple(record[2:4]);need(tag not in classes,"selected classes repeat");classes.add(tag)
            mass+=2**(cost+b);checked+=1
        need(mass==case["selected_mass"] and mass>2**44,"selected mass not an exclusion")
        need((mass-1).bit_length()==case["total_lower_bound"],"nested lower bound differs")
    result={"agent":"six-sorting-2","role":"researcher","status":"SELECTED_NESTED_PARTITION_ALL_NUMERIC_FIELDS_AND_PRUNING_FUNCTIONS_VERIFIED",
            "remaining_position_range":[begin,min(stop,len(records))],"verified_exclusions":len(records[begin:stop]),"selected_domain_occurrences":checked,
            "upgraded_occurrences":upgraded,"distinct_inner_prefixes":checked_inner.cache_info().currsize,"metrics":dict(METRICS),
            "seconds":time.monotonic()-start,"maximum_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "boundary":"Standalone stdlib numeric checker primitives are copied with attribution from own public p22_verify.py; no producer/sibling checker imports. Original full cubes, carriers, complete pruning functions and all five inner clamping families are replayed. The imported universal nested bound9007, S5/S6/S7 and unformalized bridges remain explicit."}
    (PILOT_ROOT/f"verify-nested-{begin}-{min(stop,len(records))}.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,sort_keys=True),flush=True)
if __name__=="__main__":main_nested()
