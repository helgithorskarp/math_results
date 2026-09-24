"""Exact set-cover decision for the missed-pair graph of a local system."""
from itertools import combinations
from functools import cache
from collections import Counter
import json,time,argparse

BLOCKS=tuple(sum(1<<i for i in t) for t in combinations(range(11),5))



def require(condition, message):
    if not condition:
        raise ValueError(message)


def solve(cols):
    edges=tuple((u,v) for u,v in combinations(range(11),2) if not cols[u]&cols[v])
    coverage={b:sum(1<<i for i,(u,v) in enumerate(edges) if b>>u&1 and b>>v&1) for b in BLOCKS}
    reverse={mask:block for block,mask in coverage.items()}
    candidates=[]
    for mask in sorted(reverse,key=lambda x:(-x.bit_count(),x)):
        if not any(mask|c==c for c in candidates):candidates.append(mask)
    incident=tuple(tuple(c for c in candidates if c>>i&1) for i in range(len(edges)))
    vertex_edges=tuple(sum(1<<i for i,(u,v) in enumerate(edges) if p in (u,v)) for p in range(11))
    @cache
    def visit(uncovered,left):
        if not uncovered:return ()
        if left==0:return None
        if left==1:
            for c in candidates:
                if c&uncovered==uncovered:return (c,)
            return None
        if uncovered.bit_count()>left*max((c&uncovered).bit_count() for c in candidates):return None
        if sum(((e&uncovered).bit_count()+3)//4 for e in vertex_edges)>left*5:return None
        pivot=min((i for i in range(len(edges)) if uncovered>>i&1),key=lambda i:len(incident[i]))
        for c in sorted(incident[pivot],key=lambda c:-(c&uncovered).bit_count()):
            rest=visit(uncovered&~c,left-1)
            if rest is not None:return (c,)+rest
        return None
    answer=visit((1<<len(edges))-1,4)
    out=dict(missed_edges=len(edges),candidates=len(candidates),states=visit.cache_info().misses)
    if answer is not None:
        blocks=[reverse[c] for c in answer]
        require(all(any(b>>u&1 and b>>v&1 for b in blocks) for u,v in edges), 'invalid local witness')
        out['witness']=blocks
    visit.cache_clear()
    return out
