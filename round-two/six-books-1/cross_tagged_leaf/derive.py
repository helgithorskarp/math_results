#!/usr/bin/env python3
"""Exact row producer for the specified cross-omission leaf sector."""
from collections import Counter
from itertools import combinations, product
from math import comb
from pathlib import Path
import hashlib
import json
import sys
import time

CYCLE = ((0,4),(4,3),(3,1),(1,2),(2,5),(5,0))
OWN = (40,20)
MINIMUM = (2,2,1,1,1,1)
SCOPE = "specified one-nine leaf; red degrees 9^4,10^18; cross-repeated omission"


def canonical(value):
    return json.dumps(value, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def guard(start):
    if time.monotonic()-start > 30:
        raise RuntimeError("30s phase guard: incomplete enumeration proves no exclusion")


def masks(n):
    return tuple(sorted(sum(1 << i for i in row) for row in combinations(range(6),n)))


def known16(item):
    r,lows,columns,s0,s1,beta = item
    red = [0]*16
    def edge(i,j):
        red[i] |= 1 << j
        red[j] |= 1 << i
    for z in (1,2,*range(3,11)):
        edge(0,z)
    for z in (2,11,12):
        edge(1,z)
    for z in range(9,16):
        edge(2,z)
    for i,j in CYCLE:
        edge(3+i,3+j)
    for s in range(2):
        for i in range(6):
            if OWN[s] & (1 << i):
                edge(9+s,3+i)
            if (s0,s1)[s] & (1 << i):
                edge(11+s,3+i)
    for i in range(8):
        for t in range(3):
            if columns[i] & (1 << t):
                edge(3+i,13+t)
    for s,row in enumerate((6,3)):
        for t in range(3):
            if row & (1 << t):
                edge(11+s,13+t)
    degrees = (10,10,9,*([10]*8),10-lows[3],10-lows[4],
               *(10-lows[t] for t in range(3)))
    q = (0,6,0,*(3+b for b in beta),4,4,2,2,3,2,3)
    if tuple(red[i].bit_count()+q[i] for i in range(16)) != degrees:
        raise ValueError("actual degree/core-row mismatch")
    if sum(beta) != 1+sum(lows):
        raise ValueError("ordinary-X/Y edge budget mismatch")
    limits = {}
    for i,j in combinations(range(16),2):
        cap = 3 if red[i] & (1 << j) else degrees[i]+degrees[j]-14
        limits[i,j] = cap-(red[i]&red[j]).bit_count()
    return red,degrees,q,limits


def x_domain():
    pools = {n:masks(n) for n in range(2,6)}
    flags = tuple(l for l in product(range(2),repeat=5) if sum(l) <= 3)
    domain = []
    for r in range(2):
        sx = (6,5) if r == 0 else (5,6)
        for lows in flags:
            start = time.monotonic()
            for rows in product(pools[4-lows[0]],pools[4-lows[1]],pools[3-lows[2]]):
                columns = tuple(sum(int(bool(rows[t] & (1 << i))) << t
                                    for t in range(3)) for i in range(6))+sx
                k = tuple(columns[i].bit_count()-MINIMUM[i] for i in range(6))
                if min(k) < 0:
                    continue
                if sum(k) != 3-sum(lows[:3]):
                    raise ValueError("actual T excess mismatch")
                if any((columns[i]&columns[j]).bit_count() > min(2,k[i]+k[j])
                       for i,j in CYCLE):
                    continue
                if any((sx[s]&columns[i]).bit_count() > min(2,1+k[i])
                       for s in range(2) for i in range(6) if OWN[s] & (1 << i)):
                    continue
                for sy in product(pools[4-lows[3]],pools[4-lows[4]]):
                    beta = tuple(2-k[i]-sum(int(bool(row & (1 << i))) for row in sy)
                                 for i in range(6))
                    if min(beta) < 0 or max(beta) > 2:
                        continue
                    item = (r,lows,columns,sy[0],sy[1],beta)
                    _,_,q,limit = known16(item)
                    if all(max(0,q[i]+q[j]-6) <= value for (i,j),value in limit.items()):
                        domain.append(item)
                guard(start)
            guard(start)
    domain.sort()
    return flags,domain


def endpoint_sets(frame):
    _,intersection,t0,t1,t2,s0,s1 = frame
    return (15,51 if intersection == 2 else 23,s0,s1,t0,t1,t2)


def y_domain(xs,known):
    start = time.monotonic()
    pools = {2:masks(2),3:masks(3)}
    domain = []
    for index in range(len(xs)):
        _,_,_,limit = known[index]
        def allowed(i,j,a,b):
            return (a&b).bit_count() <= limit[min(i,j),max(i,j)]
        for intersection,b in ((2,51),(3,23)):
            a = 15
            candidates = [tuple(m for m in pools[(3,2,3)[t]]
                               if allowed(9,13+t,a,m) and allowed(10,13+t,b,m))
                          for t in range(3)]
            for ts in product(*candidates):
                if any(not allowed(13+i,13+j,ts[i],ts[j])
                       for i,j in combinations(range(3),2)):
                    continue
                if ts[0] | ts[1] | ts[2] != 63:
                    continue
                sy = [tuple(m for m in pools[2]
                            if allowed(9,11+s,a,m) and allowed(10,11+s,b,m)
                            and all(allowed(11+s,13+t,m,ts[t]) for t in range(3)))
                      for s in range(2)]
                for p,q in product(*sy):
                    if allowed(11,12,p,q):
                        domain.append((index,intersection,*ts,p,q))
            guard(start)
    domain.sort()
    return domain


def row_domain(ys,known):
    start = time.monotonic()
    pools = {n:masks(n) for n in range(3,6)}
    domain = []
    for index,frame in enumerate(ys):
        _,_,q,limit = known[frame[0]]
        ep = endpoint_sets(frame)
        rows = tuple(tuple(m for m in pools[q[3+i]]
                          if all((m&ep[e]).bit_count() <= limit[3+i,9+e]
                                 for e in range(7))) for i in range(6))
        if all(rows):
            domain.append((index,rows))
        guard(start)
    return domain


def join_domain(xs,ys,rowsets,known):
    start = time.monotonic()
    domain = []
    for yi,candidates in rowsets:
        frame = ys[yi]
        item = xs[frame[0]]
        _,_,_,limit = known[frame[0]]
        ep = endpoint_sets(frame)
        high = tuple(5-sum(bool(m & (1 << j)) for m in ep[:2]) for j in range(6))
        order = sorted(range(6),key=lambda i:(len(candidates[i]),i))
        chosen = [None]*6
        columns = [0]*6
        def visit(depth):
            if depth == 6:
                if any(columns[j] not in (high[j]-1,high[j]) for j in range(6)):
                    return
                low_y = sum(int(columns[j] == high[j]-1) << j for j in range(6))
                if low_y.bit_count() != 3-sum(item[1]):
                    raise ValueError("complete ordinary-Y tag budget")
                domain.append((yi,tuple(chosen),low_y))
                return
            i = order[depth]
            for m in candidates[i]:
                if any((m&chosen[j]).bit_count() > limit[min(3+i,3+j),max(3+i,3+j)]
                       for j in order[:depth]):
                    continue
                if any(columns[j]+bool(m & (1 << j)) > high[j] for j in range(6)):
                    continue
                chosen[i] = m
                for j in range(6):
                    columns[j] += bool(m & (1 << j))
                if all(columns[j]+5-depth >= high[j]-1 for j in range(6)):
                    visit(depth+1)
                for j in range(6):
                    columns[j] -= bool(m & (1 << j))
                chosen[i] = None
        visit(0)
        guard(start)
    domain.sort()
    return domain


def witnesses(xs,ys,joins,known):
    start = time.monotonic()
    answer = []
    tags = Counter()
    for index,(yi,cross,low_y) in enumerate(joins):
        frame = ys[yi]
        item = xs[frame[0]]
        red = known[frame[0]][0][:]+[0]*6
        for i,m in enumerate((0,63,0,*cross,*endpoint_sets(frame))):
            for j in range(6):
                if m & (1 << j):
                    red[i] |= 1 << (16+j)
                    red[16+j] |= 1 << i
        found = False
        for i,j in combinations(range(22),2):
            common = red[i]&red[j]
            if red[i] & (1 << j) and common.bit_count() >= 4:
                pages = tuple(p for p in range(22) if common & (1 << p))[:4]
                answer.append((index,i,j,pages))
                found = True
                break
        if not found:
            raise ValueError("known edges have no four-page red witness")
        tags[(tuple(item[1]),low_y)] += 1
        guard(start)
    return answer,sorted((l,low_y,n) for (l,low_y),n in tags.items())


def derive():
    flags,xs = x_domain()
    known = [known16(item) for item in xs]
    ys = y_domain(xs,known)
    rows = row_domain(ys,known)
    joins = join_domain(xs,ys,rows,known)
    books,tags = witnesses(xs,ys,joins,known)
    by_tag = Counter((item[0],item[1]) for item in xs)
    coverage = [{"repeated_SX":r,"low_T0_T1_T2_SY0_SY1":l,
                 "ordinary_Y_low_count":3-sum(l),
                 "labeled_ordinary_Y_choices":comb(6,3-sum(l)),
                 "X_interfaces":by_tag[r,l]} for r in range(2) for l in flags]
    values = {"X":xs,"Y_endpoints":ys,"XY_rows":rows,"XY_joins":joins,"red_books":books}
    return {"schema":1,"agent":"six-books-1","role":"researcher","scope":SCOPE,
            "normalized_repeated_SX_choices":2,"flag_words_per_core":len(flags),
            "labeled_low_placements_per_core":sum(comb(6,3-sum(l)) for l in flags),
            "tag_coverage":coverage,"canonical_ordered_SX_pairs":((15,51),(15,23)),
            "labeled_SX_pair_orbit_sizes":(90,120),
            "counts":{name:len(value) for name,value in values.items()},
            "domain_sha256":{name:digest(value) for name,value in values.items()},
            "domains":values,"join_tag_histogram":tags,
            "unblocked_partial_joins":len(joins)-len(books),
            "internal_Y_edges_used_in_witnesses":0}


def summary(record):
    answer = {key:value for key,value in record.items() if key != "domains"}
    answer["red_book_witnesses"] = record["domains"]["red_books"]
    return answer


if __name__ == "__main__":
    result = derive()
    if len(sys.argv) == 2 and sys.argv[1] == "--summary":
        print(canonical(summary(result)))
    elif len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] == "--emit"):
        print(canonical(result))
    else:
        raise SystemExit("usage: derive.py --emit | --summary")
