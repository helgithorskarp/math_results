"""Independent local completion enumeration by four-bit point signatures."""
from collections import defaultdict
from itertools import combinations
import argparse,json,time

def enumerate_dual(columns):
    adjacency=[{q for q in range(11) if q!=p and columns[p]&columns[q]==0} for p in range(11)]
    order=sorted(range(11),key=lambda p:(-len(adjacency[p]),-columns[p].bit_count(),p))
    initial=[]
    for p in order:
        lo=max((len(adjacency[p])+3)//4,3-columns[p].bit_count(),0)
        hi=min(4,5-columns[p].bit_count())
        initial.append(tuple(m for m in range(16) if lo<=m.bit_count()<=hi))
    weights=[0]*4;histories=[0]*4;assigned={};answers=set();nodes=0
    def visit(depth,domains):
        nonlocal nodes
        nodes+=1
        if depth==11:
            if weights!=[5]*4:return
            rows=tuple(sorted(sum(1<<p for p,m in assigned.items() if m>>r&1) for r in range(4)))
            if len(set(rows))!=4:return
            answers.add(rows);return
        if any(not d for d in domains):return
        needed=[5-w for w in weights]
        if any(n<0 for n in needed):return
        if sum(min(m.bit_count() for m in d) for d in domains)>sum(needed):return
        if sum(max(m.bit_count() for m in d) for d in domains)<sum(needed):return
        for r,n in enumerate(needed):
            if sum(any(m>>r&1 for m in d) for d in domains)<n:return
            if sum(all(m>>r&1 for m in d) for d in domains)>n:return
        groups=defaultdict(list)
        for r,h in enumerate(histories):groups[h].append(r)
        canonical=[]
        for m in domains[0]:
            if any([m>>r&1 for r in g]!=sorted([m>>r&1 for r in g],reverse=True) for g in groups.values()):continue
            canonical.append(m)
        p=order[depth]
        old_hist=histories.copy()
        for m in canonical:
            for r in range(4):
                weights[r]+=m>>r&1
                histories[r]=(histories[r]<<1)|(m>>r&1)
            assigned[p]=m
            saturated=sum(1<<r for r,w in enumerate(weights) if w==5)
            future=[]
            for q,domain in zip(order[depth+1:],domains[1:]):
                future.append(tuple(v for v in domain if not v&saturated and (q not in adjacency[p] or v&m)))
            visit(depth+1,tuple(future))
            del assigned[p]
            for r in range(4):weights[r]-=m>>r&1
            histories[:]=old_hist
    visit(0,tuple(initial))
    return sorted(answers),nodes
