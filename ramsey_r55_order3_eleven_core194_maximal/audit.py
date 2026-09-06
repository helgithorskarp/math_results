#!/usr/bin/env python3
"""Independent physical-orbit, clique, transformation and complete-CNF checker."""
from functools import lru_cache
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parent
BITS='100110110110110100'
SEED=ROOT.parent/'ramsey_r55_order3_eleven_neighborhood24/c194.edges'


def need(ok,message):
    if not ok:raise ValueError(message)


def read_seed():
    raw=SEED.read_bytes()
    need(hashlib.sha256(raw).hexdigest()=='41d4c7939f74d60ff1716787923afca5349829cc90fd5c79be95f8c1e82b1178','literal seed identity')
    lines=raw.decode().splitlines();n,m=map(int,lines[0].split());red=set()
    for row in lines[1:]:
        a,b=map(int,row.split());need(0<=a<b<n and (a,b) not in red,'distinct seed edge');red.add((a,b))
    need(n==24 and len(red)==m==156,'seed counts');return red


def action(v):return 3*(v//3)+(v%3+1)%3 if v<33 else v


@lru_cache(None)
def physical(n):
    red=read_seed();left=set(combinations(range(n),2));edges={};orbits=[]
    while left:
        p=min(left);orbit={p};q=tuple(sorted(map(action,p)))
        while q!=p:orbit.add(q);q=tuple(sorted(map(action,q)))
        left-=orbit;a,b=p
        if n==24 and a//3==b//3:constant=a<12
        elif n==43 and b<24:constant=p in red
        elif n==43 and 33 in p:constant=next(v for v in p if v!=33)>=24
        elif n==43 and b<33 and a//3==b//3:constant=False
        else:orbits.append(orbit);continue
        for q in orbit:edges[q]=constant
    for i,orbit in enumerate(sorted(orbits,key=min),1):
        for q in orbit:edges[q]=i
    need(len(edges)==n*(n-1)//2,'complete physical pairs')
    return edges


def clique_rows(n,edges,order,color):
    allowed=[0]*n
    for (a,b),v in edges.items():
        if type(v)is int or v==color:allowed[a]|=1<<b;allowed[b]|=1<<a
    rows=set();count=0
    def visit(chosen,candidates):
        nonlocal count
        if len(chosen)==order:
            count+=1;rows.add(tuple(sorted({(-edges[e] if color else edges[e]) for e in combinations(chosen,2) if type(edges[e])is int})));return
        if candidates.bit_count()<order-len(chosen):return
        while candidates:
            bit=candidates&-candidates;candidates-=bit;v=bit.bit_length()-1
            visit(chosen+[v],candidates&allowed[v])
    visit([], (1<<n)-1)
    return rows,count


def graph_word(word):
    need(type(word)is str and len(word)==21 and all(c in '0123456789abcdef' for c in word),'84-bit word')
    w=int(word,16);return {e for e,v in physical(24).items() if (v if type(v)is bool else bool(w>>(v-1)&1))}


def graph_check(red):
    for size,color in ((5,True),(4,False)):
        need(not any(all((e in red)==color for e in combinations(vs,2)) for vs in combinations(range(24),size)),'literal forbidden clique')
    for e in combinations(range(24),2):
        need((e in red)==(tuple(sorted(map(action,e))) in red),'literal C3 invariance')
        if e[0]//3==e[1]//3:need((e in red)==(e[0]<12),'internal colors')
    word=''.join('1' if (3*i,3*j+d) in red else '0' for i,j in combinations(range(4),2) for d in range(3))
    need(word==BITS,'literal core194')
    degrees=[sum(tuple(sorted((v,u))) in red for u in range(24) if u!=v) for v in range(24)]
    return dict(red_edges=len(red),degrees=degrees,red_K5=0,blue_K4=0)


def contacts(red):return [tuple(int(tuple(sorted((3*i,3*j+d))) in red) for i in range(4) for d in range(3)) for j in range(4,8)]


def shifted(w,s):return tuple(w[3*i+(d+s)%3] for i in range(4) for d in range(3))


def check_representatives(data):
    need(set(data)=={'red_stabilizer','representatives'} and data['red_stabilizer']==24,'representative schema')
    reps=data['representatives'];need(len(reps)==4 and [r['word'] for r in reps]==sorted(set(r['word'] for r in reps)),'four distinct ordered representatives')
    seed=read_seed();graphs=[]
    for r in reps:
        need(set(r)=={'word','pullback_permutation'},'representative fields');p=r['pullback_permutation']
        need(len(p)==24 and all(type(v)is int for v in p) and sorted(p)==list(range(24)),'permutation')
        need(all((v<12)==(p[v]<12) and p[action(v)]==action(p[v]) for v in range(24)),'color parts and action commute')
        red=graph_word(r['word']);need(all((e in red)==(tuple(sorted((p[e[0]],p[e[1]]))) in seed) for e in combinations(range(24),2)),'literal pullback equality')
        result=graph_check(red);need(result['degrees']==[13]*24,'derived regularity')
        c=contacts(red);need(c==sorted(c) and len(set(c))==4,'distinct ordered contact columns')
        need(all(len({shifted(w,s) for s in range(3)})==3 and w==min(shifted(w,s) for s in range(3)) for w in c),'unique minimal phases')
        graphs.append(red)
    # The blue-cycle group fixes the red core pointwise. Physical pullbacks
    # enumerate disjoint free orbits of the four canonical representatives.
    words=set();orbit_sizes=[]
    for red in graphs:
        orbit=set()
        for p in permutations(range(4,8)):
            for shifts in product(range(3),repeat=4):
                f=list(range(12))+[3*p[j]+(d+shifts[j])%3 for j in range(4) for d in range(3)]
                w=sum(int(tuple(sorted((f[3*i],f[3*j+d]))) in red)<<(v-1) for (i,j,d),v in (( (i,j,d),physical(24)[3*i,3*j+d]) for i,j in combinations(range(8),2) for d in range(3)))
                orbit.add(w)
        need(len(orbit)==1944 and not words&orbit,'four free disjoint blue orbits');orbit_sizes.append(len(orbit));words|=orbit
    encoded=''.join(f'{w:021x}\n' for w in sorted(words)).encode()
    return dict(canonical_representatives=4,blue_group_orbit_sizes=orbit_sizes,labeled_local_graphs=len(words),
        words_sha256=hashlib.sha256(encoded).hexdigest(),all_red_degrees=13,seed=graph_check(seed))


def normalization():
    edges=physical(24);cols=[[edges[3*i,3*j+d] for i in range(4) for d in range(3)] for j in range(4,8)]
    phases=[]
    for variables in cols:
        for w in product((0,1),repeat=12):
            if any(shifted(w,s)<w for s in (1,2)):
                phases.append(tuple(-v if b else v for v,b in zip(variables,w)))
    ordering=[];top=84
    for left,right in zip(cols,cols[1:]):
        previous=None
        for k,(x,y) in enumerate(zip(left,right)):
            # A first differing pair must be 0,1. q means the prefix is equal.
            ordering.append(tuple(([-previous] if previous else [])+[-x,y]))
            if k==11:continue
            top+=1;q=top
            if previous:ordering.append((-q,previous))
            ordering.extend([(-q,-x,y),(-q,x,-y),tuple(([-previous] if previous else [])+[-x,-y,q]),tuple(([-previous] if previous else [])+[x,y,q])])
            previous=q
    return phases,ordering,top


def expected(kind,reps):
    n=24 if kind=='classification' else 43;need(kind in ('classification','extension'),'formula role');edges=physical(n)
    rows=set()
    for order,color in (((4,False),(5,True)) if n==24 else ((5,False),(5,True))):rows|=clique_rows(n,edges,order,color)[0]
    output=sorted(rows);top=max(v for v in edges.values() if type(v)is int)
    if n==24:
        core=[edges[3*i,3*j+d] for i,j in combinations(range(4),2) for d in range(3)]
        output.extend((v if b=='1' else -v,) for v,b in zip(core,BITS))
        phase,order,top=normalization();output.extend(phase);output.extend(order)
        output.extend(tuple(-(i+1) if int(r['word'],16)>>i&1 else i+1 for i in range(84)) for r in reps['representatives'])
    return top,output


def check_formula(path,kind,reps):
    top,rows=expected(kind,reps)
    with path.open() as f:
        need(f.readline()==f'p cnf {top} {len(rows)}\n','complete header')
        for row in rows:need(f.readline()==' '.join(map(str,row))+' 0\n','exact independent clause sequence')
        need(not f.read(),'exact EOF')
    return dict(variables=top,clauses=len(rows),primary_variables=84 if kind=='classification' else 216,all_pairs=len(physical(24 if kind=='classification' else 43)))
