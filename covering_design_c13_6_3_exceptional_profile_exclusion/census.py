"""Complete local census by heavy supports, multigraph edges, and singletons."""
from itertools import combinations, permutations
from collections import Counter
import json, time

EDGES=tuple(combinations(range(5),2))
MASKS=tuple(sum(1<<i for i in e) for e in EDGES)
PERMS=tuple(permutations(range(5)))
ACTIONS=tuple(tuple(sum(1<<p[i] for i in range(5) if m>>i&1)
                    for m in range(32)) for p in PERMS)
EDGE_ACTIONS=tuple(tuple(MASKS.index(a[m]) for m in MASKS) for a in ACTIONS)



def require(condition, message):
    if not condition:
        raise ValueError(message)


def census():
    high=tuple(m for m in range(1,32) if m.bit_count()>=3)
    high_reps=set()
    for count in range(5):
        for h in combinations(high,count):
            if sum(m.bit_count()-1 for m in h)>9:continue
            if any((u&v).bit_count()>2 for u,v in combinations(h,2)):continue
            if any(sum(m>>i&1 for m in h)>4 for i in range(5)):continue
            high_reps.add(min(tuple(sorted(a[m] for m in h)) for a in ACTIONS))
    records=[]
    labelled_by_high=[]
    for h in sorted(high_reps):
        stabilizers=[a for a,b in zip(EDGE_ACTIONS,ACTIONS)
                     if tuple(sorted(b[m] for m in h))==h]
        degrees=[sum(m>>i&1 for m in h) for i in range(5)]
        pair_base=[sum(m&e==e for m in h) for e in MASKS]
        remain=9-sum(m.bit_count()-1 for m in h)
        labelled=0
        keys=set()
        def visit(index,left,counts):
            nonlocal labelled
            if sum(4-d for d in degrees)<2*left:return
            if index==10:
                if left:return
                labelled+=1
                key=min(tuple(counts[a[i]] for i in range(10)) for a in stabilizers)
                keys.add(key)
                return
            u,v=EDGES[index]
            for n in range(min(left,4-degrees[u],4-degrees[v],3-pair_base[index])+1):
                degrees[u]+=n;degrees[v]+=n
                visit(index+1,left-n,counts+[n])
                degrees[u]-=n;degrees[v]-=n
        visit(0,remain,[])
        labelled_by_high.append([h,labelled,len(keys)])
        for key in sorted(keys):
            d=[sum(m>>i&1 for m in h)+sum(n for n,e in zip(key,EDGES) if i in e)
               for i in range(5)]
            cols=tuple(sorted(list(h)+[m for m,n in zip(MASKS,key) for _ in range(n)]+
                              [1<<i for i in range(5) for _ in range(4-d[i])]))
            rows=tuple(sum(1<<j for j,m in enumerate(cols) if m>>i&1) for i in range(5))
            require(len(cols)==11 and all(r.bit_count()==4 for r in rows), 'invalid incidence dimensions')
            require(all((u&v).bit_count()<=2 for u,v in combinations(cols,2)), 'column pair multiplicity')
            overlap=max((u&v).bit_count() for u,v in combinations(rows,2))
            require(overlap<=3, 'repeated through rows')
            records.append(dict(high=list(h),edges=list(key),columns=list(cols),rows=list(rows),overlap=overlap))
    return records,labelled_by_high
