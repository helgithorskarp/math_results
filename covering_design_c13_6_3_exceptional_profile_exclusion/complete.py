"""Enumerate all four-away-block completions of the 22 feasible types."""
from itertools import combinations
from functools import cache
import json,time,argparse

BLOCKS=tuple(sum(1<<i for i in t) for t in combinations(range(11),5))

def enumerate_covers(cols):
    edges=tuple((u,v) for u,v in combinations(range(11),2) if not cols[u]&cols[v])
    coverage=tuple(sum(1<<i for i,(u,v) in enumerate(edges) if b>>u&1 and b>>v&1) for b in BLOCKS)
    candidates=[]
    for mask in sorted(set(coverage),key=lambda x:(-x.bit_count(),x)):
        if not any(mask|c==c for c in candidates):candidates.append(mask)
    incident=tuple(tuple(c for c in candidates if c>>i&1) for i in range(len(edges)))
    all_incident=tuple(tuple(i for i,c in enumerate(coverage) if c>>e&1) for e in range(len(edges)))
    @cache
    def possible(u,k):
        if not u:return True
        if not k:return False
        if k==1:return any(u&c==u for c in candidates)
        if u.bit_count()>k*max((c&u).bit_count() for c in candidates):return False
        edge=min((i for i in range(len(edges)) if u>>i&1),key=lambda i:len(incident[i]))
        return any(possible(u&~c,k-1) for c in incident[edge])
    upper=[5-c.bit_count() for c in cols]
    lower=[max(0,3-c.bit_count()) for c in cols]
    incidence=tuple(tuple(p for p in range(11) if b>>p&1) for b in BLOCKS)
    chosen=[];degrees=[0]*11;answers=set();nodes=0
    def visit(u,k):
        nonlocal nodes
        nodes+=1
        if not k:
            if u==0 and all(lower[p]<=degrees[p]<=upper[p] for p in range(11)):
                answers.add(tuple(sorted(BLOCKS[i] for i in chosen)))
            return
        if any(degrees[p]>upper[p] or degrees[p]+k<lower[p] for p in range(11)):return
        if sum(max(0,lower[p]-degrees[p]) for p in range(11))>5*k:return
        if not possible(u,k):return
        if k==1:
            options=[i for i,c in enumerate(coverage) if c&u==u]
        elif u:
            edge=min((e for e in range(len(edges)) if u>>e&1),key=lambda e:len(all_incident[e]))
            options=all_incident[edge]
        else:
            options=range(len(BLOCKS))
        for i in options:
            if i in chosen or any(degrees[p]>=upper[p] for p in incidence[i]):continue
            chosen.append(i)
            for p in incidence[i]:degrees[p]+=1
            visit(u&~coverage[i],k-1)
            for p in incidence[i]:degrees[p]-=1
            chosen.pop()
    visit((1<<len(edges))-1,4)
    out=dict(covers=sorted(answers),nodes=nodes,oracle_states=possible.cache_info().misses)
    possible.cache_clear()
    return out
