#!/usr/bin/env python3
"""Independent physical-orbit and possible-clique reconstruction; no producer import."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

CORE = (1742,3477,2915,1777,3498,2908,941,1371,2294,3181,2715,1846)


def require(ok, why):
    if not ok:
        raise ValueError(why)


def rotate(v):
    return v if v >= 33 else 3*(v//3)+(v%3+1)%3


def orbits():
    remaining = set(combinations(range(43), 2))
    types = [[], [], []]
    internal = {}
    while remaining:
        start = min(remaining)
        orbit = {start}
        p = tuple(sorted(map(rotate, start)))
        while p != start:
            orbit.add(p)
            p = tuple(sorted(map(rotate, p)))
        remaining -= orbit
        a, b = start
        if b < 33 and a//3 == b//3:
            internal.update((e, a < 12) for e in orbit)
        else:
            t = 0 if b < 33 else (1 if a >= 33 else 2)
            types[t].append((start, orbit))
    types[0].sort(key=lambda row:(row[0][0]//3,row[0][1]//3,(row[0][1]-row[0][0])%3))
    types[1].sort()
    types[2].sort(key=lambda row:(row[0][1],row[0][0]//3))
    require(list(map(len, types)) == [165,45,110] and len(internal) == 33, 'physical orbit census')
    mapping = {e:k for k, (_, orbit) in enumerate(sum(types, []), 1) for e in orbit}
    require(len(mapping) == 870, 'all noninternal pairs')
    return mapping, internal


def setup(color):
    require(color in ('blue', 'red'), 'case color')
    ids, known = orbits()
    fixed = {}
    for a, b in combinations(range(12), 2):
        value = bool(CORE[a] & (1 << b))
        require(value == bool(CORE[b] & (1 << a)), 'symmetric literal core')
        if (a, b) in known:
            require(known[a,b] == value, 'red core triangles')
        else:
            x = ids[a,b]
            require(x not in fixed or fixed[x] == value, 'core is invariant')
            fixed[x] = value
    for f in (33,34):
        for a in range(12):
            fixed[ids[a,f]] = False
    fixed[ids[33,34]] = color == 'red'
    require(len(fixed) == 27, '27 exact fixed primary colors')
    known.update((e, fixed[x]) for e, x in ids.items() if x in fixed)
    return ids, known, fixed


def cliques(neighbors, size):
    def visit(chosen, available):
        if len(chosen) == size:
            yield chosen
            return
        while available.bit_count() >= size-len(chosen):
            bit = available & -available
            available ^= bit
            v = bit.bit_length()-1
            yield from visit(chosen+(v,), available & neighbors[v])
    yield from visit((), (1 << len(neighbors))-1)


def expected(color):
    ids, known, fixed = setup(color)
    result = set()
    census = {}
    for red in (False, True):
        neighbors = [0]*43
        for a,b in combinations(range(43),2):
            if (a,b) not in known or known[a,b] == red:
                neighbors[a] |= 1 << b
                neighbors[b] |= 1 << a
        count = 0
        for q in cliques(neighbors,5):
            count += 1
            variables = {ids[e] for e in combinations(q,2) if e not in known}
            result.add(tuple(sorted(-x if red else x for x in variables)))
        census['possible_red' if red else 'possible_blue'] = count
    census['distinct_ramsey_clauses'] = len(result)
    result.update((x if c else -x,) for x,c in fixed.items())
    before = len(result)
    if color == 'blue':
        result.update(tuple(sorted((ids[33,f],ids[34,f]))) for f in range(35,43))
    census.update(new_pair_consequences=len(result)-before, fixed_units=len(fixed), variables=320,clauses=len(result))
    return sorted(result), census


def parse(path):
    with Path(path).open('r') as stream:
        h = stream.readline().split()
        require(len(h)==4 and h[:3]==['p','cnf','320'], 'exact primary-only header')
        rows=[]
        for line in stream:
            values = list(map(int,line.split()))
            require(values and values[-1]==0 and all(1<=abs(x)<=320 for x in values[:-1]), 'DIMACS row')
            row=tuple(values[:-1])
            require(row==tuple(sorted(set(row))) and not any(-x in row for x in row), 'canonical non-tautological row')
            rows.append(row)
        require(len(rows)==int(h[3]) and rows==sorted(set(rows)), 'exact count, distinct order and EOF')
    return rows


def audit(path, color, wanted=None):
    rows=parse(path)
    if wanted is None:
        wanted,census=expected(color)
    else:
        wanted,census=wanted
    require(rows==wanted, 'entrywise complete literal formula')
    return dict(color=color, census=census, clause_lengths=dict(sorted(Counter(map(len,rows)).items())),
                sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest(), bytes=Path(path).stat().st_size,
                reconstruction='physical C3 pair orbits and possible-color clique recursion', exact=True)


def local_lemma():
    witnesses=[]
    for mask in range(16):
        red_edges={e for e in combinations(range(12),2) if CORE[e[0]] & (1 << e[1])}
        red_edges.update((a,14) for a in range(12) if mask & (1 << (a//3)))
        found=[]
        for q in combinations(range(15),5):
            colors={e in red_edges for e in combinations(q,2)}
            if len(colors)==1:
                c=next(iter(colors))
                if (c and 14 in q) or (not c and {12,13,14} <= set(q)):
                    found.append((c,q))
        require(found, 'every common-fixed signature has literal obstruction')
        c,q=found[0]
        witnesses.append(dict(signature=mask,color='red' if c else 'blue',vertices=q))
    return witnesses


def graph(path, full_color=None):
    lines=Path(path).read_text().splitlines()
    require(lines and len(lines[0].split())==1,'one order header')
    n=int(lines[0]);require(5<=n<=43,'graph order')
    edges=[tuple(map(int,line.split())) for line in lines[1:]]
    require(edges==sorted(set(edges)) and all(len(e)==2 and 0<=e[0]<e[1]<n for e in edges),'edge list')
    red=set(edges);count=0
    for q in combinations(range(n),5):
        count+=1
        require(len({e in red for e in combinations(q,2)})==2,'monochromatic K5')
    if full_color is not None:
        require(n==43,'target order')
        _,known,_=setup(full_color)
        require(all((e in red)==c for e,c in known.items()),'literal core/action fixed colors')
        require(all(((a,b) in red)==(tuple(sorted((rotate(a),rotate(b)))) in red) for a,b in combinations(range(n),2)), 'C3 graph action')
    return dict(order=n,red_edges=len(red),five_sets=count,ramsey=True)


if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--color', choices=('blue','red'),required=True)
    p.add_argument('--formula',type=Path,required=True)
    p.add_argument('--report',type=Path,required=True)
    args=p.parse_args()
    answer=audit(args.formula,args.color)
    args.report.write_text(json.dumps(answer,indent=2,sort_keys=True)+'\n')
    print('PASS independently reconstructed complete '+args.color+' formula')
