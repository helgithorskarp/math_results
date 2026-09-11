#!/usr/bin/env python3
"""Replay the whole low-degree theorem and quantified spanning-link cases."""
import json
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations,permutations
from collections import Counter
from math import comb
from bounds import M,envelope_bound
from forest import star_bound

ROOT=Path(__file__).parent
DATA=json.loads((ROOT/'low_degree_certificates.json').read_text())
@lru_cache(None)
def maps(s):
    return tuple(tuple(sum(1<<p[i] for i in range(s) if A>>i&1) for A in range(1<<s)) for p in permutations(range(s)))
def canonical(x):
    return min(tuple(x[A] for A in mp) for mp in maps((len(x)-1).bit_length()))
EXTRA={tuple(z['x']):z for z in DATA if z['closed']}
BAD={tuple(z['x']) for z in DATA if not z['closed']}

def degrees(x):
    return [sum(n for A,n in enumerate(x) if A>>i&1) for i in range((len(x)-1).bit_length())]

@lru_cache(None)
def good(v,x):
    s=(len(x)-1).bit_length()
    if s==1:return star_bound(v,33,x[1])<1
    for i in range(s):
        if good(v,M.reindex(x,tuple(j for j in range(s) if i!=j))):return True
    for p in permutations(range(s)):
        if envelope_bound(v,M.reindex(x,p),max_excess=3)<1:return True
    if s==5:
        y=canonical(x)
        if y in EXTRA:
            z=EXTRA[y]
            assert z['v']==v
            return envelope_bound(v,y,tuple(z['positions']),3)<1
    return False

def admissible(v,x):
    s=(len(x)-1).bit_length();N=v-s
    if any(n and A.bit_count()>5 for A,n in enumerate(x)):return False
    for i in range(s):
        if sum(n*(5-A.bit_count()) for A,n in enumerate(x) if A>>i&1)<N:return False
        for j in range(i):
            if sum(n for A,n in enumerate(x) if A>>i&1 and A>>j&1)<1:return False
    return sum(n*comb(5-A.bit_count(),2) for A,n in enumerate(x) if A.bit_count()<=3)>=comb(N,2)

def low_case(v):
    seen=Counter();closed=Counter();survivors=set()
    def visit(x):
        s=(len(x)-1).bit_length();seen[s]+=1
        if good(v,x):closed[s]+=1;return
        if s==5:survivors.add(canonical(x));return
        ds=degrees(x)
        for d in range(ds[-1],(165-sum(ds))//(v-s)+1):
            for y in M.extends(x,d):
                if admissible(v,y):visit(y)
    for x in M.profiles(v,33,3):
        if degrees(x)[0]<=6:visit(x)
    if v==23:
        assert survivors==BAD and len(BAD)==3
        for x in survivors:
            ds=degrees(x);assert sorted(ds)==[6,7,7,7,7]
            u=ds.index(6)
            assert all(not n or not A>>u&1 or A.bit_count()<=3 for A,n in enumerate(x))
        # Any four degree-seven vertices can be chosen after the unique
        # degree-six vertex; the proof makes the ensuing covering contradiction.
        assert 22-(165-(6+22*7))==17 and 17>6*2
    else:assert not survivors
    return {'v':v,'visited':dict(seen),'closed_by_coloring':dict(closed),
            'residual_types':len(survivors),'closure':'17>12' if survivors else 'all colored'}

def pair_partitions(s):
    ps=list(combinations(range(s),2));index={p:i for i,p in enumerate(ps)}
    blocks=[]
    for size in range(2,min(5,s)+1):
        for vs in combinations(range(s),size):
            blocks.append((sum(1<<index[p] for p in combinations(vs,2)),sum(1<<i for i in vs)))
    choices=[[b for b in blocks if b[0]>>i&1] for i in range(len(ps))]
    out=[]
    def rec(rem,chosen):
        if not rem:out.append(tuple(chosen));return
        i=(rem&-rem).bit_length()-1
        for bits,A in choices[i]:
            if bits&rem==bits:rec(rem^bits,chosen+[A])
    rec((1<<len(ps))-1,[])
    return out

def trace(blocks,s,m):
    x=[0]*(1<<s)
    for A in blocks:x[A]=1
    for i in range(s):x[1<<i]=6-sum(1 for A in blocks if A>>i&1)
    x[0]=m-sum(x)
    assert min(x)>=0
    return tuple(x)

def main():
    for z in DATA:
        x=tuple(z['x']);assert x==canonical(x) and sum(x)==33
        b=envelope_bound(z['v'],x,tuple(z['positions']),3)
        assert b==F(z['bound'])
        if z['closed']:assert b<1
    forest_cases=[]
    for v,m,ds in [(19,34,range(5,9)),(20,33,[5,6]),(21,33,[5,6])]:
        b=max(star_bound(v,m,d) for d in ds);assert b<1
        forest_cases.append({'v':v,'m':m,'degrees':list(ds),'max_bound':str(b)})
    small=[]
    for v in [22,23,24,25]:small.append(low_case(v))
    linear=[]
    for z in json.loads((ROOT/'linear_certificates.json').read_text()):
        s=z['s'];m=z['m'];types={canonical(trace(b,s,m)) for b in pair_partitions(s)}
        rows={tuple(row['x']):row for row in z['rows']};assert set(rows)==types
        vals=[]
        for x,row in rows.items():
            b=envelope_bound(25,x,tuple(row['positions']),0)
            assert b==F(row['bound']) and b<1;vals.append(b)
        linear.append({'v':25,'m':m,'spanning_degree6_vertices':s,'types':len(types),'max_bound':str(max(vals))})
    assert 25*7-5*34==5>=4
    for v in range(9,19):assert 33*(comb(v//2,5)+comb((v+1)//2,5))<comb(v,5)
    from audit import audit_links,audit_forests,audit_pivots
    out={'theorem':'Every pair-covered simple 5-uniform hypergraph with at most 33 edges and minimum degree at most six is 2-colorable.',
         'additional_complete_cases':'Pair-covered 19- or 25-vertex hypergraphs with at most 34 edges are 2-colorable.',
         'global_m5_lower_bound_unchanged':33,'forest_cases':forest_cases,'low_degree_cases':small,'spanning_link_cases':linear,
         'checks':{'link_envelope_maxima':audit_links(),'tail_union_families':audit_forests(),'covering_pivot_families':audit_pivots()}}
    print(json.dumps(out,indent=2))
if __name__=='__main__':
    if not __debug__:raise RuntimeError('Run without -O; assertions are required.')
    main()
