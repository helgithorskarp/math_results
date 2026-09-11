"""Independent orbit coverage by explicit generator traversal."""
from itertools import combinations
from collections import Counter
import json,hashlib,time
from a0_quad_orbits import reps
def audit(k,r):
    edges=[(0,1),(2,3),(4,5),(6,7),(8,9)] if k==0 else [(0,1),(0,2),(3,4),(5,6),(7,8)]
    nbr=[set() for _ in range(12)]
    for u,v in edges:nbr[u].add(v);nbr[v].add(u)
    masks=[sum(1<<t for t in B) for B in combinations(range(12),4) if all(v not in nbr[u] and not nbr[u]&nbr[v] for u,v in combinations(B,2))]
    ids={b:i for i,b in enumerate(masks)};n=len(masks)
    compatible=[set(j for j in range(i+1,n) if (masks[i]&masks[j]).bit_count()<=1) for i in range(n)]
    if r==2:allfamilies={(i,j) for i in range(n) for j in compatible[i]}
    elif r==3:allfamilies={(i,j,l) for i in range(n) for j in compatible[i] for l in compatible[i]&compatible[j]}
    else:raise ValueError(r)
    total=len(allfamilies)
    swaps=[]
    if k==0:
        swaps += [[(a,b)] for a,b in edges]
        swaps += [[(2*i,2*i+2),(2*i+1,2*i+3)] for i in range(4)]
        swaps += [[(10,11)]]
    else:
        swaps += [[(1,2)]]
        swaps += [[e] for e in edges[2:]]
        swaps += [[(3+2*i,5+2*i),(4+2*i,6+2*i)] for i in range(2)]
        swaps += [[(9,10)],[(10,11)]]
    maps=[]
    E={frozenset(e) for e in edges}
    for ss in swaps:
        p=list(range(12))
        for a,b in ss:p[a],p[b]=p[b],p[a]
        if {frozenset((p[a],p[b])) for a,b in edges}!=E:raise ValueError('Not automorphism')
        maps.append([ids[sum(1<<p[t] for t in range(12) if B>>t&1)] for B in masks])
    records=[]
    for number,Qs in enumerate(reps(k,r)):
        seed=tuple(sorted(ids[sum(1<<t for t in Q)] for Q in Qs))
        if seed not in allfamilies:raise ValueError('Duplicate or missing representative')
        allfamilies.remove(seed);orbit={seed};todo=[seed]
        while todo:
            f=todo.pop()
            for p in maps:
                new=tuple(sorted(p[i] for i in f))
                if new in orbit:continue
                if new not in allfamilies:raise ValueError('Orbit overlap or invalid image')
                allfamilies.remove(new);orbit.add(new);todo.append(new)
        raw=json.dumps(sorted(orbit),separators=(',',':')).encode()
        records.append(dict(orbit=number,size=len(orbit),member_sha256=hashlib.sha256(raw).hexdigest()))
    if allfamilies:raise ValueError('Incomplete orbit cover')
    return dict(k=k,quads=r,quad_count=n,labeled_families=total,orbit_count=len(records),records=records)
