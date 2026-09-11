"""Complete quad-family orbits for the two five-edge high forests."""
from itertools import combinations, permutations
from functools import lru_cache
def forest(k):
    return [(0,1),(2,3),(4,5),(6,7),(8,9)] if k==0 else [(0,1),(0,2),(3,4),(5,6),(7,8)]
def independent(S,k):
    E=forest(k)
    if any(u in S and v in S for u,v in E):return False
    return not(k and 1 in S and 2 in S)
def key(Qs,k):
    colors=[sum((t in Q)<<i for i,Q in enumerate(Qs)) for t in range(12)]
    candidates=[]
    for perm in permutations(range(len(Qs))):
        c=[sum(((x>>i)&1)<<perm[i] for i in range(len(Qs))) for x in colors]
        if k==0:
            candidates.append(((),tuple(sorted(tuple(sorted((c[u],c[v]))) for u,v in forest(k))),tuple(sorted(c[10:]))))
        else:
            candidates.append(((c[0],*sorted(c[1:3])),tuple(sorted(tuple(sorted((c[u],c[v]))) for u,v in forest(k)[2:])),tuple(sorted(c[9:]))))
    return min(candidates)
@lru_cache(None)
def reps(k,r):
    blocks=[frozenset(q) for q in combinations(range(12),4) if independent(q,k)]
    levels={():()}
    for size in range(1,r+1):
        nxt={}
        for qs in levels.values():
            for q in blocks:
                if any(len(q&p)>1 for p in qs):continue
                new=tuple(sorted(qs+(q,),key=lambda x:tuple(sorted(x))))
                canonical=key(new,k)
                if canonical not in nxt:nxt[canonical]=new
        levels=nxt
    return tuple(levels[x] for x in sorted(levels))
