"""Compare the search against unpruned named-colour enumeration on small cases."""
from itertools import combinations,product
from colour_check import solve

def run():
    checked=0
    for n,with_triples,pin_cases in [
        (5,False,[[],[(0,0),(1,0)]]),
        (4,True,[[],[(0,0),(1,0)],[(0,0),(1,1)]])]:
        pairs=list(combinations(range(n),2))
        triples=list(combinations(range(n),3)) if with_triples else []
        for pins in pin_cases:
            words=[w for w in product(range(4),repeat=n)
                   if all(w[v]==c for v,c in pins)]
            valid_masks=[]
            for w in words:
                edge_mask=sum(1<<k for k,(i,j) in enumerate(pairs) if w[i]!=w[j])
                tri_mask=sum(1<<k for k,t in enumerate(triples) if len({w[v] for v in t})>1)
                valid_masks.append((edge_mask,tri_mask))
            for e in range(1<<len(pairs)):
                es=[p for k,p in enumerate(pairs) if e>>k&1]
                for h in range(1<<len(triples)):
                    ts=[t for k,t in enumerate(triples) if h>>k&1]
                    brute=any(e & ~a==0 and h & ~b==0 for a,b in valid_masks)
                    answer,_=solve(n,es,pins,ts)
                    if (answer is not None)!=brute:raise ValueError('Small exhaustive mismatch')
                    if answer is not None:
                        if (any(answer[i]==answer[j] for i,j in es) or
                            any(answer[v]!=c for v,c in pins) or
                            any(len({answer[v] for v in t})==1 for t in ts)):
                            raise ValueError('Invalid small witness')
                    checked+=1
    if checked!=5120:raise ValueError('Small control count')
    return checked
