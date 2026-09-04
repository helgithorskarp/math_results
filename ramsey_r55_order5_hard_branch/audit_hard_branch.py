#!/usr/bin/env python3
"""Exact audit and machine-readable marked cases for the analytic theorem.

No solver or full 43-vertex construction search. All graph counting uses
literal adjacency and subsets; no teammate graph code is imported.
"""

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
from random import Random


HERE = Path(__file__).resolve().parent
U = dict(zip(range(18, 25), (85, 92, 100, 107, 114, 122, 132)))
WEIGHT = dict(zip(range(18, 25), (21, 12, 3, 0, 3, 12, 21)))
COLUMNS = {0: (0, 1, 2, 3, 5, 5, 6, 6), 1: tuple(range(8))}


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def provenance():
    files = {
        "ramsey_r55_local_extremal_deficiency/extrema.json":
            "7233dd701f47de79c65ecccb6b06ad8f79b16b92c08cfcf73bcef1ed3b4d5b10",
        "ramsey_r55_order5_f3_incidence/result.json":
            "976ac059bded965af662337aebc7c491e5c9d0c710030127f3ee0436408fcb52",
    }
    for name, digest in files.items():
        require(sha256((HERE.parent/name).read_bytes()).hexdigest() == digest, name)
    data = json.loads((HERE.parent/"ramsey_r55_order5_f3_incidence/result.json").read_text())
    require({row["h"]: tuple(row["columns"]) for row in data["representatives"]} == COLUMNS,
            "incidence representatives")


def rotate(vertex):
    if vertex < 3:
        return vertex
    cycle, phase = divmod(vertex-3, 5)
    return 3+5*cycle+(phase+1) % 5


def orbit_spectrum(sets):
    remaining = set(sets)
    spectrum = Counter()
    while remaining:
        start = min(remaining)
        orbit, current = set(), start
        while current not in orbit:
            orbit.add(current)
            current = tuple(sorted(map(rotate, current)))
        require(current == start, "orbit closure")
        remaining.difference_update(orbit)
        spectrum[len(orbit)] += 1
    return spectrum


def arithmetic():
    # Outside degrees 20..22, even one moving cycle exceeds the weight budget.
    require(all(5*WEIGHT[d] > 39 for d in (18, 19, 23, 24)), "moving degree range")
    hist = Counter()
    profiles = set()
    for degrees in product((20, 21, 22), repeat=8):
        weight = 3+5*sum(WEIGHT[d] for d in degrees)
        if weight > 39:
            continue
        hist["weight"] += 1
        degree_sum = 62+5*sum(degrees)
        if degree_sum % 2:
            continue
        hist["parity"] += 1
        if weight == 3:
            m = degree_sum // 2
            z_pair_sum = comb(22, 2)-m+20*21
            congruence_cap = 5*((U[20]-7)//5)+5*((U[22]-7)//5)
            require(z_pair_sum == 200 > congruence_cap == 195, "one-defect contradiction")
            hist["one_defect_rejected"] += 1
            continue
        require(weight == 33 and (43-weight)//2 == 5, "five-unit budget")
        z_pairs = [(r,b) for r in range(0,U[20]-6,5) for b in range(0,U[22]-6,5)
                   if (U[20]-7-r)+(U[22]-7-b) <= 5]
        require(z_pairs == [(90,105)], z_pairs)
        total_red = 200+90+5*sum(U[d]-7 for d in degrees)
        total_blue = 200+105+5*sum(U[42-d]-7 for d in degrees)
        if total_red % 3 or total_blue % 3:
            hist["triangle_rejected"] += 1
            continue
        hist["survives"] += 1
        full = tuple(int(d == 20)+2*int(d == 21)+5*degrees.count(d) for d in range(18,25))
        profiles.add((full,degree_sum//2,total_red//3,total_blue//3))
    require(hist == Counter(weight=129,parity=113,one_defect_rejected=1,
                            triangle_rejected=56,survives=56), hist)
    require(profiles == {((0,0,6,32,5,0,0),451,1430,1435)}, profiles)
    return hist


def swap_xy(mask):
    return (mask & 4)+((mask & 1) << 1)+((mask & 2) >> 1)


def marked_cases():
    cases = []
    labeled = Counter()
    for h, columns in COLUMNS.items():
        masks = set()
        for low in range(8):
            for high in range(8):
                if low == high:
                    continue
                # Weighted-neighbor identities at x,y,z, respectively.
                sums = [5*(int(bool(columns[high] & (1<<f)))-int(bool(columns[low] & (1<<f))))
                        for f in range(3)]
                if sums != [0,0,-5]:
                    continue
                labeled[h] += 1
                a,b = columns[low],columns[high]
                masks.add(min((a,b),(swap_xy(a),swap_xy(b))))
        require(labeled[h] == 4, labeled)
        for a,b in sorted(masks):
            if a & b & 3 == 3:
                require((h,a,b) == (1,7,3), "unexpected common-red-pair exclusion")
                continue
            low,high = columns.index(a),columns.index(b)
            degrees = [21]*8
            degrees[low],degrees[high] = 20,22
            cases.append({
                "h": h, "columns": list(columns), "low_cycle": low, "high_cycle": high,
                "cycle_red_degrees": degrees,
                "row_sum_targets": [d-2-mask.bit_count() for d,mask in zip(degrees,columns)],
                "low_high_red_cross_degree": 3,
                "normal_difference_targets": [[i,int(bool(mask & 4))] for i,mask in enumerate(columns)
                                              if i not in (low,high)],
                "fixed_cut_targets": {"R_x":15-h,"R_y":15-h,"B_x":16,"B_y":16,"R_z":14,"B_z":17},
            })
    require([(r["h"],r["low_cycle"],r["high_cycle"]) for r in cases] == [(0,4,1),(1,4,0),(1,5,1)], cases)
    require([k for k in range(6) if k-3 == 0 and 2-k == -1] == [3], "special cross degree")
    return cases


def adjacency(columns, steps, words):
    n = 3+5*len(columns)
    answer = [[False]*n for _ in range(n)]
    for a,b in combinations(range(n),2):
        if b < 3:
            red = (a,b) == (0,1)
        elif a < 3:
            red = bool(columns[(b-3)//5] & (1<<a))
        else:
            ca,pa = divmod(a-3,5)
            cb,pb = divmod(b-3,5)
            if ca == cb:
                red = min(abs(pa-pb),5-abs(pa-pb)) == steps[ca]
            else:
                red = bool(words[ca,cb] & (1<<((pb-pa) % 5)))
        answer[a][b] = answer[b][a] = red
    return answer


def homogeneous_fives(adj):
    return [vertices for vertices in combinations(range(len(adj)),5)
            if sum(adj[a][b] for a,b in combinations(vertices,2)) in (0,10)]


def pair_audit(cases):
    rows = []
    tested = valid = 0
    for h,a,b in ((0,5,1),(1,4,0),(1,5,1),(1,7,3)):
        for s,t in product((1,2),repeat=2):
            good = []
            for word in range(32):
                if word.bit_count() != 3:
                    continue
                adj = adjacency((a,b),(s,t),{(0,1):word})
                tested += 1
                bad = homogeneous_fives(adj)
                if not bad:
                    good.append(word)
                    valid += 1
                if (a,b) == (7,3):
                    require(any(set((0,1)) <= set(five) and
                                all(adj[u][v] for u,v in combinations(five,2)) for five in bad),
                            "explicit red K5 through fixed xy")
            expected = 0 if (a,b)==(7,3) else (5 if (a,b)==(5,1) and s==t else 10)
            require(len(good) == expected, (h,a,b,s,t,good))
            rows.append([h,a,b,s,t,good])
    require((tested,valid) == (160,100), (tested,valid))
    for case in cases:
        a,b = case["columns"][case["low_cycle"]],case["columns"][case["high_cycle"]]
        case["special_pair_word_domains"] = [[s,t,words] for h,aa,bb,s,t,words in rows
                                              if (h,aa,bb)==(case["h"],a,b)]
    return rows


def formula_audit():
    rng = Random(550543)
    checked = 0
    for h,columns in COLUMNS.items():
        for sample in range(20):
            steps = [rng.choice((1,2)) for _ in range(8)]
            words = {p:(0 if sample==0 else 31 if sample==1 else rng.randrange(32))
                     for p in combinations(range(8),2)}
            adj = adjacency(columns,steps,words)
            k = {p:word.bit_count() for p,word in words.items()}
            for i in range(8):
                predicted = 2+columns[i].bit_count()+sum(value for pair,value in k.items() if i in pair)
                require(all(sum(adj[3+5*i+t]) == predicted for t in range(5)), "cycle degree formula")
            for fixed in range(3):
                red_set = [i for i,mask in enumerate(columns) if mask & (1<<fixed)]
                blue_set = [i for i in range(8) if i not in red_set]
                red_cross = sum(k[a,b] for a,b in combinations(red_set,2))
                blue_cross = sum(5-k[a,b] for a,b in combinations(blue_set,2))
                expected_red = 5*(4+red_cross+(1+h if fixed<2 else 0))
                expected_blue = 5*(4+blue_cross+(2 if fixed<2 else 4))
                neighbors = [v for v in range(43) if adj[fixed][v]]
                nonneighbors = [v for v in range(43) if v!=fixed and not adj[fixed][v]]
                actual_red = sum(adj[a][b] for a,b in combinations(neighbors,2))
                actual_blue = sum(not adj[a][b] for a,b in combinations(nonneighbors,2))
                require((actual_red,actual_blue)==(expected_red,expected_blue), "fixed local edge formula")
            checked += 1
    require(checked == 40, "fixture count")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit the reproducible marked-case handoff")
    args = parser.parse_args()
    provenance()
    for fixed in range(3):
        pairs = combinations([v for v in range(43) if v != fixed],2)
        require(orbit_spectrum(pairs) == Counter({5:172,1:1}), "fixed pair orbits")
    require(orbit_spectrum(combinations(range(43),3)) == Counter({5:2468,1:1}), "triangle orbits")
    arithmetic()
    cases = marked_cases()
    pair_audit(cases)
    formula_audit()
    document = {"format":"r55-order5-hard-branch-v1", "scope":"necessary constraints, not global feasibility",
                "red_degree_counts_18_to_24":[0,0,6,32,5,0,0], "red_edges":451,
                "weight":33, "excess":5, "red_blue_triangles":[1430,1435],
                "z_local_counts":[90,105], "other_vertices_local_deficiency":7,
                "exact_anchor_count":32, "total_cross_degree_sum":70, "cases":cases}
    encoded = json.dumps(document,indent=2,sort_keys=True)+"\n"
    if args.json:
        print(encoded,end="")
        return
    print("PASS pinned extrema and teammate incidence manifests")
    print("PASS fixed-vertex pair orbits: 1 singleton + 172 five-orbits, at each fixed vertex")
    print("PASS triangle orbits: 1 singleton + 2468 five-orbits; fixed triangle mixed")
    print("PASS labeled degree tests: 6561 -> 129 weight -> 113 parity -> 56 surviving assignments")
    print("PASS rejections: one one-defect assignment and 56 triangle-incidence assignments")
    print("PASS unique global profile: 20^6,21^32,22^5; m=451 W=33 excess=5")
    print("PASS z local pair=90,105; all other local deficiencies=7; exact anchors=32")
    print("PASS triangle totals red=1430 blue=1435")
    print("PASS exceptional placements: 4+4 labeled, 1+3 marked classes, 3 retained after xy-K5 obstruction")
    print("PASS exceptional cross degree=3; six ordinary-cycle difference constraints per case")
    print("PASS local pair audit: 160 colorings, 1287 five-sets each, 100 valid restricted colorings")
    print("PASS degree and fixed-local formulas on 40 arbitrary invariant fixtures (not target witnesses)")
    print("SCOPE three marked hard-branch cases remain unresolved; no full construction search")
    print("cases_sha256="+sha256(encoded.encode("ascii")).hexdigest())


if __name__ == "__main__":
    main()
