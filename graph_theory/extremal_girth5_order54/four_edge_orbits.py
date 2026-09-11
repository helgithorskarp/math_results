"""Complete colored quad-family orbits on four-edge path forests."""
from itertools import combinations,permutations,product
from functools import lru_cache
FORESTS=((2,2,2,2),(3,2,2),(4,2),(3,3),(5,))
@lru_cache(None)
def components(fid):
    paths=[];v=0
    for n in FORESTS[fid]:
        paths.append(tuple(range(v,v+n)));v+=n
    return tuple(paths)+tuple((t,) for t in range(v,12))
@lru_cache(None)
def forest(fid):
    return tuple((u,v) for P in components(fid) for u,v in zip(P,P[1:]))
@lru_cache(None)
def forbidden(fid):
    E=forest(fid);N=[set() for _ in range(12)]
    for u,v in E:N[u].add(v);N[v].add(u)
    return frozenset((u,v) for u,v in combinations(range(12),2) if v in N[u] or N[u]&N[v])
def independent(B,fid):
    return not any(u in B and v in B for u,v in forbidden(fid))
@lru_cache(None)
def role_permutations(degrees):
    groups=[[i for i,d in enumerate(degrees) if d==a] for a in sorted(set(degrees))]
    out=[]
    for ps in product(*(list(permutations(g)) for g in groups)):
        p=list(range(len(degrees)))
        for g,q in zip(groups,ps):
            for i,j in zip(g,q):p[i]=j
        out.append(tuple(p))
    return tuple(out)
def key(Qs,fid,degrees):
    colors=[sum((t in Q)<<i for i,Q in enumerate(Qs)) for t in range(12)]
    keys=[]
    for p in role_permutations(degrees):
        c=[sum(((x>>i)&1)<<p[i] for i in range(len(Qs))) for x in colors]
        keys.append(tuple(sorted((len(P),min(tuple(c[t] for t in P),tuple(c[t] for t in P[::-1]))) for P in components(fid))))
    return min(keys)
@lru_cache(None)
def reps(fid,n6,n7=0):
    blocks=[frozenset(B) for B in combinations(range(12),4) if independent(B,fid)]
    if not n6 and not n7:return ((),)
    if n7:previous=reps(fid,n6,n7-1)
    else:previous=reps(fid,n6-1,0)
    degrees=(6,)*n6+(7,)*n7;out={}
    for Qs in previous:
        for Q in blocks:
            if any(len(Q&A)>1 for A in Qs):continue
            new=Qs+(Q,)
            new=tuple(sorted(new[:n6],key=lambda A:tuple(sorted(A))))+tuple(sorted(new[n6:],key=lambda A:tuple(sorted(A))))
            code=key(new,fid,degrees)
            if code not in out:out[code]=new
    return tuple(out[x] for x in sorted(out))
