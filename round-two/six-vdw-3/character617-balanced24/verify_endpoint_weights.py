"""Exact local weighted endpoint audit, with two different finite mechanisms.

Seven occupied-group truth bits check every possible larger hit set. An
independent literal traversal checks every five/six-subset of the33 actual
field endpoints, including all non-hitting subsets. No generator imports.
"""
import argparse
import collections
import itertools
import json
import math
from pathlib import Path


def need(ok, why):
    if not ok:
        raise ValueError(why)


def inverse(x):
    a, b, u, v = 617, x, 0, 1
    while b:
        t = a // b
        a, b, u, v = b, a-t*b, v, u-t*v
    need(a == 1, "literal nonzero inverse")
    return u % 617


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
need(not args.output.exists(), "Preserve existing mathematical output")
need(all(617 % d for d in range(2, math.isqrt(617)+1)), "Prime field617")
squares = {q*q % 617 for q in range(1, 617)}
nonsquares = set(range(1, 617))-squares
actual = {}
for step in range(1, 617):
    points = {(1+j*step) % 617 for j in range(1, 7)}
    if points <= nonsquares:
        actual[step] = points
steps = [285, 314, 362, 381, 409, 570]
need(sorted(actual) == steps, "Every physical nonsquare endpoint progression")
supports = [actual[s] for s in steps]
shared = supports[0] & supports[5]
left = supports[0]-shared
right = supports[5]-shared
groups = [shared, left, right, *supports[1:5]]
need([len(g) for g in groups] == [3, 3, 3, 6, 6, 6, 6], "Seven physical group sizes")
need(all(not a & b for a, b in itertools.combinations(groups, 2)), "Whole disjoint group partition")
vertices = sorted(set().union(*supports))
need(len(vertices) == 33 and set().union(*groups) == set(vertices), "Every endpoint exactly once")
bad = left | right
good = set(vertices)-bad
inverses = {inverse(t) for t in vertices}
need(not set(vertices) & inverses, "No reciprocal endpoint arcs")
need(len(good | {inverse(t) for t in good}) == 54 and
     len(bad | {inverse(t) for t in bad}) == 12, "Entire symmetric weighted ratio graph")

# Independent group-occupancy proof of the universal weighted inequality.
# For an occupied type, its polynomial counts every nonempty physical subset.
coefficient = {5: collections.Counter(), 6: collections.Counter()}
allowed = []
for pattern in range(128):
    present = [(pattern >> i) & 1 for i in range(7)]
    hits = (present[0] or present[1]) and (present[0] or present[2]) and all(present[3:])
    if not hits:
        continue
    minimum_weight = sum((1 if i in (1, 2) else 2)*p for i, p in enumerate(present))
    need(minimum_weight >= 10 and sum(present) >= 5, "All occupied-group lower bounds")
    allowed.append([pattern, minimum_weight, sum(present)])
    poly = {(0, 0): 1}
    for i, (group, occupied) in enumerate(zip(groups, present)):
        choices = range(1, min(len(group), 6)+1) if occupied else (0,)
        fresh = collections.Counter()
        for (degree, bad_degree), count in poly.items():
            for take in choices:
                if degree+take <= 6:
                    fresh[degree+take, bad_degree+(take if i in (1, 2) else 0)] += count*math.comb(len(group), take)
        poly = fresh
    for (degree, bad_degree), count in poly.items():
        if degree in coefficient:
            coefficient[degree][bad_degree] += count
need(len(allowed) == 5, "All five admissible occupied-group patterns")

# Literal point masks, independently traversing ALL physical sets, not the
# producer's occupied-group patterns or its binomial coefficient polynomial.
position = {t: i for i, t in enumerate(vertices)}
bits = [1 << i for i in range(33)]
support_masks = [sum(1 << position[t] for t in points) for points in supports]
bad_mask = sum(1 << position[t] for t in bad)
literal, visited = {}, {}
for degree in (5, 6):
    counts = collections.Counter()
    number = 0
    for chosen in itertools.combinations(bits, degree):
        number += 1
        mask = sum(chosen)
        if all(mask & demand for demand in support_masks):
            bad_degree = (mask & bad_mask).bit_count()
            need(2*degree-bad_degree >= 10, "Every actual hit-set weight")
            counts[bad_degree] += 1
    need(number == math.comb(33, degree), "Complete literal physical subset coverage")
    need(counts == coefficient[degree], "Entire group/literal coefficient census")
    literal[degree], visited[degree] = counts, number
need(literal[5] == {0: 3888} and literal[6] == {0: 42768, 1: 23328, 2: 11664},
     "Exact five/six local neighbor classifications")
result = {"agent": "six-vdw-3", "role": "researcher", "prime": 617,
          "steps": steps, "supports": [sorted(x) for x in supports],
          "good_ratios": sorted(good), "bad_ratios": sorted(bad),
          "good_symmetric_ratio_count": 54, "bad_symmetric_ratio_count": 12,
          "all_group_occupancy_cases": 128, "admissible_occupancy_records": allowed,
          "all_larger_hit_sets_weight_at_least": 10,
          "literal_subset_trials": [[k, visited[k]] for k in (5, 6)],
          "literal_subset_trials_total": sum(visited.values()),
          "hit_set_bad_count_histograms": [[k, sorted(literal[k].items())] for k in (5, 6)],
          "status": "EXACT_WEIGHTED_ENDPOINT_INEQUALITY_AND_LOCAL_CLASSIFICATION"}
args.output.write_text(json.dumps(result, sort_keys=True, indent=2)+"\n")
print(json.dumps(result, sort_keys=True))
