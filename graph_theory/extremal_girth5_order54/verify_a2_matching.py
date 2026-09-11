#!/usr/bin/env python3
"""Finite controls for the human A2 five-matching exclusion.

Python 3.11+, standard library. These controls do not replace the written
graph-to-set argument or replay the imported A2 classification certificates.
"""
import hashlib
import json
from collections import Counter
from itertools import combinations, combinations_with_replacement
from math import comb


def require(condition, message):
    if not condition:
        raise ValueError(message)


def family_digest(families):
    h = hashlib.sha256()
    for family in families:
        h.update((",".join(map(str, family)) + "\n").encode())
    return h.hexdigest()


def triple_families():
    """Compare bitset clique enumeration with direct subset enumeration."""
    triples = list(combinations(range(8), 3))
    masks = [sum(1 << x for x in t) for t in triples]
    compatible = [
        sum(1 << j for j in range(i + 1, 56)
            if (masks[i] & masks[j]).bit_count() <= 1)
        for i in range(56)
    ]
    families = [[] for _ in range(6)]

    def visit(family, available):
        families[len(family)].append(tuple(family))
        if len(family) == 5:
            return
        while available:
            bit = available & -available
            available -= bit
            i = bit.bit_length() - 1
            visit(family + [i], available & compatible[i])

    visit([], (1 << 56) - 1)
    sets = list(map(frozenset, triples))
    rows = []
    for k in range(6):
        # A separate representation and algorithm checks every k-subset
        # of the 56 triples. No symmetry quotient is taken in either run.
        direct = [
            f for f in combinations(range(56), k)
            if all(len(sets[i] & sets[j]) <= 1 for i, j in combinations(f, 2))
        ]
        require(direct == families[k], "entrywise family mismatch")
        histogram = Counter()
        for f in direct:
            disjoint = sum(not (sets[i] & sets[j]) for i, j in combinations(f, 2))
            histogram[disjoint] += 1
            union = set().union(*(sets[i] for i in f))
            intersections = comb(k, 2) - disjoint
            require(len(union) >= 3*k - intersections, "union inequality")
            require(disjoint <= 3, "three-pair packing bound")
        rows.append({
            "triples": k, "families": len(direct),
            "disjoint_pair_histogram": dict(sorted(histogram.items())),
            "sha256": family_digest(direct)
        })
    require([r["families"] for r in rows] == [1, 56, 1120, 10080, 42840, 84000],
            "full labeled family counts")
    # A sharpness control: the bound 3 is attained for this abstract set
    # problem. It is not a graph or a realization of the order-54 profile.
    example = [(0, 6, 7), (1, 3, 7), (1, 4, 5), (2, 3, 5), (2, 4, 6)]
    f = list(map(frozenset, example))
    require(all(len(a & b) <= 1 for a, b in combinations(f, 2)), "example linearity")
    require(sum(not(a & b) for a, b in combinations(f, 2)) == 3, "example sharpness")
    return {"rows": rows, "sharp_abstract_example": example}


def high_incidence_bound():
    """All labeled four-sets in a fixed high five-edge matching."""
    high_edges = [(i, i+1) for i in range(0, 10, 2)]
    # R={0,2}: nonsinks have five six-neighbors; matched sinks four;
    # the two isolated high vertices have three.
    six_degrees = [5, 4, 5, 4, 4, 4, 4, 4, 4, 4, 3, 3]
    records = []
    for q in combinations(range(12), 4):
        if any(u in q and v in q for u, v in high_edges):
            continue
        incident = sum(six_degrees[t] for t in q)
        require(incident >= 14, "quad six-incidence bound")
        for delta in (0, 1):
            # The unique c=2 six-vertex either meets q once or avoids it.
            outside = 14 - (incident - 4 - delta)
            require(outside <= 5, "at most five outside triples")
            records.append((q, delta, outside))
    return {
        "independent_four_sets": len(records)//2,
        "c2_intersection_cases": len(records),
        "minimum_six_incidence": min(sum(six_degrees[t] for t in q) for q, _, _ in records),
        "maximum_outside_triples": max(x for _, _, x in records)
    }


def local_and_partition_checks():
    negative = []
    local_count = 0
    for d, cs in ((6, (2, 3, 4)), (7, (1, 2))):
        for c in cs:
            for a in range(d-c+1):
                b = d-a-c
                eps = b + 2*c - (8 if d == 6 else 7)
                local_count += 1
                if (c-3)*eps < 0:
                    negative.append((d, c, eps))
    require(sorted(set(negative)) == [(7, 1, 1), (7, 2, 1), (7, 2, 2)],
            "negative contribution types")
    formats = {}
    for c, eps in ((1, 1), (2, 1), (2, 2)):
        possibilities = []
        for sizes in combinations_with_replacement(range(1, 5), 4-eps):
            if sizes.count(4) > 1 or sum(sizes) < 12-c:
                continue
            possibilities.append(sizes)
        formats[f"c{c}_epsilon{eps}"] = possibilities
    require(formats == {"c1_epsilon1": [], "c2_epsilon1": [(3, 3, 4)],
                        "c2_epsilon2": []}, "unique-quad far formats")

    # In the residual m=4 profile, suppose the two quads are disjoint.
    # Fix one as points 8..11, the second as 0..3. A bad vertex using
    # only the first would partition 0..7 into blocks of sizes 2,3,3,
    # each intersecting the second quad in at most one point.
    other_quad = set(range(4))
    candidate_partitions = 0
    valid_partitions = 0
    for own in combinations(range(8), 2):
        rest = set(range(8)) - set(own)
        for first in combinations(sorted(rest), 3):
            second = tuple(sorted(rest - set(first)))
            if first > second:
                continue
            candidate_partitions += 1
            blocks = [set(own), set(first), set(second)]
            if all(len(block & other_quad) <= 1 for block in blocks):
                valid_partitions += 1
    require(candidate_partitions == 280 and valid_partitions == 0,
            "disjoint-quad partition obstruction")
    # In m=5 the epsilon sum is 6 and its c-weighted sum is 10.
    # In m=4 they are 6 and 8. Every other contribution is nonnegative
    # after the imported b1=b22=0 result for m=4.
    require(3*6-10 == 8 and 3*6-8 == 10, "bad-vertex lower bounds")
    require(8 > 3 and 10 > 9, "closing contradictions")
    return {
        "local_types": local_count,
        "negative_types": sorted(set(negative)),
        "m5_far_formats": formats,
        "m4_disjoint_quad_partitions_checked": candidate_partitions,
        "m4_disjoint_quad_partitions_surviving": valid_partitions,
        "m5_bad_lower": 8, "m5_bad_upper": 3,
        "m4_disjoint_quads_bad_lower": 10,
        "m4_disjoint_quads_bad_upper": 9
    }


def main():
    result = {
        "claim": "No z12,A2,m5 graph; in remaining m4 the two four-sets intersect once",
        "status": "human closing proof with finite controls; imports A2 classification",
        "high_incidence": high_incidence_bound(),
        "local_checks": local_and_partition_checks(),
        "triple_packing": triple_families()
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
