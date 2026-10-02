#!/usr/bin/env python3
"""Independent column enumeration and literal selected-spine checker."""
from collections import Counter
from copy import deepcopy
from itertools import combinations, product
from math import comb
from pathlib import Path
import hashlib
import json
import sys
import time


def canonical(value):
    return json.dumps(value, separators=(",", ":"))


def unique_object(items):
    answer = {}
    for key, value in items:
        if key in answer:
            raise ValueError("duplicate JSON field")
        answer[key] = value
    return answer


def graph(columns, sy_columns=None):
    neighbors = [set() for _ in range(16)]

    def edge(i, j):
        neighbors[i].add(j)
        neighbors[j].add(i)

    for j in (1, 2, *range(3, 11)):
        edge(0, j)
    for j in (2, 11, 12):
        edge(1, j)
    for j in range(9, 16):
        edge(2, j)
    for i, j in ((0,4), (4,3), (3,1), (1,2), (2,5), (5,0)):
        edge(i+3, j+3)
    for sx, points in ((9, (3,5)), (10, (2,4))):
        for i in points:
            edge(sx, i+3)
    for i, column in enumerate(columns):
        for t in range(3):
            if column & (1 << t):
                edge(i+3, t+13)
    for sy, points in ((11, (0,2)), (12, (0,1))):
        for t in points:
            edge(sy, t+13)
    if sy_columns is not None:
        for i, column in enumerate(sy_columns):
            for s in range(2):
                if column & (1 << s):
                    edge(i+3, s+11)
    return neighbors


def necessary(neighbors, vertices, total_degrees, outside_size):
    universe = set(vertices)
    red = {i: neighbors[i] & universe for i in vertices}
    blue = {i: universe-red[i]-{i} for i in vertices}
    missing_red = {i: total_degrees[i]-len(red[i]) for i in vertices}
    if any(q < 0 or q > outside_size for q in missing_red.values()):
        raise ValueError("outside degree is invalid")
    for ix, i in enumerate(vertices):
        for j in vertices[ix+1:]:
            if j in red[i]:
                actual_inside = len(red[i] & red[j])
                outside_minimum = max(0, missing_red[i]+missing_red[j]-outside_size)
                if actual_inside+outside_minimum > 3:
                    return False
            else:
                actual_inside = len(blue[i] & blue[j])
                outside_minimum = max(0, outside_size-missing_red[i]-missing_red[j])
                if actual_inside+outside_minimum > 6:
                    return False
    return True


def finish(domain):
    universe = set(range(22))
    fours = tuple(set(z) for z in combinations(range(16,22), 4))
    threes = tuple(set(z) for z in combinations(range(16,22), 3))
    counts = Counter(); frames = compatible = 0
    for lows, c, s0, s1, beta in domain:
        sy_columns = tuple(((s0 >> i) & 1) + 2*((s1 >> i) & 1) for i in range(6))
        neighbors = graph(c, sy_columns)
        xrows = [neighbors[t] & set(range(3,9)) for t in (14,15)]
        ownrows = [neighbors[s] & set(range(3,9)) for s in (9,10)]
        if any(all(len(row & own) >= 1 for own in ownrows) for row in xrows):
            counts["union_obstruction"] += 1
        else:
            if lows[1:3] != (0,0) or any(len(row) != 3 or not {3,4} <= row for row in xrows):
                raise ValueError("ordinary finish normal form")
            if any(sorted(len(row & own) for own in ownrows) != [0,1] for row in xrows):
                raise ValueError("ordinary own-X overlaps")
            counts["two_T_three_sets_obstruction"] += 1
        sx_count = 0
        for a, b in product(fours, repeat=2):
            sx0 = neighbors[9] | a
            sx1 = neighbors[10] | b
            if len(sx0) != 10 or len(sx1) != 10:
                raise ValueError("literal SX degree")
            common_blue = len((universe-sx0-{9}) & (universe-sx1-{10}))
            if common_blue > 6:
                continue
            sx_count += 1; frames += 1
            candidates = []
            for t in (14,15):
                rows = []
                for z in threes:
                    whole = neighbors[t] | z
                    if len(whole) != 10-lows[t-13]:
                        raise ValueError("literal T degree")
                    if len(whole & sx0) <= 3 and len(whole & sx1) <= 3:
                        rows.append(whole)
                candidates.append(rows)
            for t1, t2 in product(*candidates):
                if len((universe-t1-{14}) & (universe-t2-{15})) <= 6:
                    compatible += 1
        if sx_count != 90:
            raise ValueError("literal blue SX spine coverage")
    if compatible:
        raise ValueError("literal selected spines admit a Y completion")
    return {"union_obstruction": counts["union_obstruction"],
            "two_T_three_sets_obstruction": counts["two_T_three_sets_obstruction"],
            "labeled_SX_Y_frames": frames, "compatible_T_Y_row_pairs": compatible}


def regenerate():
    start = time.monotonic()
    vertices14 = tuple(i for i in range(16) if i not in (11,12))
    vertices16 = tuple(range(16))
    sy_choices = []
    for sy_columns in product(range(4), repeat=6):
        ranks = tuple(sum(bool(column & (1 << s)) for column in sy_columns) for s in range(2))
        if any(rank not in (3,4) for rank in ranks):
            continue
        masks = tuple(sum(int(bool(sy_columns[i] & (1 << s))) << i for i in range(6)) for s in range(2))
        sy_choices.append((sy_columns, tuple(4-rank for rank in ranks), masks))
    if len(sy_choices) != 1225:
        raise ValueError("complete SY-column domain")
    domain = []
    for columns in product((3,5,6,7), (3,5,6,7), range(1,8), range(1,8), range(1,8), range(1,8)):
        ranks = tuple(sum(bool(column & (1 << t)) for column in columns) for t in range(3))
        if ranks[0] not in (4,5) or any(rank not in (2,3) for rank in ranks[1:]):
            continue
        low_t = (5-ranks[0], 3-ranks[1], 3-ranks[2])
        c = columns+(6,6)
        neighbors = graph(c)
        degrees = (10,10,9,*([10]*8),10,10,*(10-l for l in low_t))
        if not necessary(neighbors, vertices14, degrees, 8):
            continue
        for sy_columns, low_s, masks in sy_choices:
            lows = low_t+low_s
            if sum(lows) > 3:
                continue
            beta = tuple(4-columns[i].bit_count()-sum(bool(sy_columns[i] & (1 << s)) for s in range(2))
                         if i < 2 else
                         3-columns[i].bit_count()-sum(bool(sy_columns[i] & (1 << s)) for s in range(2))
                         for i in range(6))
            if any(b < 0 or b > 2 for b in beta):
                continue
            neighbors = graph(c, sy_columns)
            degrees = (10,10,9,*([10]*8),*(10-l for l in low_s),*(10-l for l in low_t))
            if not necessary(neighbors, vertices16, degrees, 6):
                continue
            if sum(beta) != 1+sum(lows):
                raise ValueError("edge-count bridge")
            expected_q = (0,6,0,*(3+b for b in beta),4,4,2,2,2,3,3)
            if tuple(degrees[i]-len(neighbors[i]) for i in range(16)) != expected_q:
                raise ValueError("actual outside-row budgets")
            domain.append((lows,c,masks[0],masks[1],beta))
        if time.monotonic()-start > 30:
            raise RuntimeError("30-second guard: incomplete enumeration proves no exclusion")
    domain.sort()
    if any(item[0][0] != 1 for item in domain):
        raise ValueError("T0 tag refinement")
    flags = tuple(l for l in product(range(2), repeat=5) if sum(l) <= 3)
    counts = Counter(item[0] for item in domain)
    coverage = [{"low_T0_T1_T2_SY0_SY1": l, "ordinary_Y_low_count": 3-sum(l),
                 "labeled_ordinary_Y_choices": comb(6,3-sum(l)), "X_interfaces": counts[l]} for l in flags]
    ending = finish(domain)
    if time.monotonic()-start > 30:
        raise RuntimeError("30-second guard: incomplete finish proves no exclusion")
    return {"schema":1, "agent":"six-books-1", "role":"researcher",
            "scope":"specified one-nine leaf; red degrees 9^4,10^18; both SX omit T0",
            "flag_words":len(flags), "labeled_actual_low_placements":sum(x["labeled_ordinary_Y_choices"] for x in coverage),
            "tag_coverage":coverage, "X_interface_count":len(domain),
            "X_domain_sha256":hashlib.sha256(canonical(domain).encode()).hexdigest(),
            "X_domain":domain, "every_X_interface_has_T0_degree9":True, "finish":ending}


def accept(text, expected):
    value = json.loads(text, object_pairs_hook=unique_object)
    if canonical(value) != canonical(expected):
        raise ValueError("complete independently regenerated record differs")


def controls(expected):
    universe = set(range(6))
    subsets = tuple({i for i in range(6) if mask & (1 << i)} for mask in range(64))
    for a, b in product(subsets, repeat=2):
        red_min = max(0,len(a)+len(b)-6)
        blue_min = max(0,6-len(a)-len(b))
        if len(a & b) < red_min or len((universe-a) & (universe-b)) < blue_min:
            raise ValueError("colored subset minimum control")
    def damaged(change, repair_hash=False):
        value = deepcopy(expected); change(value)
        if repair_hash:
            value["X_domain_sha256"] = hashlib.sha256(canonical(value["X_domain"]).encode()).hexdigest()
        return canonical(value)
    damages = [
        damaged(lambda r: r.__setitem__("scope", "all 22-vertex hosts")),
        damaged(lambda r: r.__setitem__("labeled_actual_low_placements", 109)),
        damaged(lambda r: r["tag_coverage"].pop(0)),
        damaged(lambda r: r["tag_coverage"][0].__setitem__("ordinary_Y_low_count", 0)),
        damaged(lambda r: r["tag_coverage"][0].__setitem__("X_interfaces", 1)),
        damaged(lambda r: r["X_domain"].pop(), True),
        damaged(lambda r: r["X_domain"].append(deepcopy(r["X_domain"][0])), True),
        damaged(lambda r: r["X_domain"][0][0].__setitem__(0, 0), True),
        damaged(lambda r: r["X_domain"][0][1].__setitem__(0, 7), True),
        damaged(lambda r: r["X_domain"][0][4].__setitem__(0, 2), True),
        damaged(lambda r: r["finish"].__setitem__("union_obstruction", 111)),
        damaged(lambda r: r["finish"].__setitem__("compatible_T_Y_row_pairs", 1)),
        canonical(expected)[:-1]+',"schema":1}',
        canonical(expected)+' false',
    ]
    for text in damages:
        try:
            accept(text,expected)
        except (ValueError, json.JSONDecodeError):
            continue
        raise ValueError("a damaged certificate was accepted")
    return {"six_point_subset_pairs":4096, "rejected_damages":len(damages)}


if __name__ == "__main__":
    expected = regenerate()
    if len(sys.argv) == 2 and sys.argv[1] == "--emit":
        print(canonical(expected))
    elif len(sys.argv) == 2 and sys.argv[1] == "--self-test":
        accept(Path(__file__).with_name("EXPECTED.json").read_text(), expected)
        # Damages operate on a normal JSON value, rather than Python tuples.
        print(canonical(controls(json.loads(canonical(expected)))))
    elif len(sys.argv) == 2:
        accept(Path(sys.argv[1]).read_text(), expected)
        print(canonical({"verified":True, "X_interfaces":len(expected["X_domain"]),
                         "domain_sha256":expected["X_domain_sha256"], "finish":expected["finish"]}))
    else:
        raise SystemExit("usage: verify.py EXPECTED.json | --emit | --self-test")
