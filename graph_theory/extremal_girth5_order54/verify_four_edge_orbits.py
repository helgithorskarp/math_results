"""Independent group-generator orbit traversal and labeled-family count."""
from itertools import combinations
import hashlib,json,time
from four_edge_orbits import reps
SPECS=((2,2,2,2),(3,2,2),(4,2),(3,3),(5,))
def audit(fid,n6,n7):
    paths=[];offset=0
    for size in SPECS[fid]:
        paths.append(tuple(range(offset,offset+size)));offset+=size
    paths += [(v,) for v in range(offset,12)]
    edges={frozenset((u,v)) for P in paths for u,v in zip(P,P[1:])}
    N=[set() for _ in range(12)]
    for e in edges:
        u,v=tuple(e);N[u].add(v);N[v].add(u)
    masks=[sum(1<<v for v in B) for B in combinations(range(12),4)
           if all(v not in N[u] and not N[u]&N[v] for u,v in combinations(B,2))]
    ids={x:i for i,x in enumerate(masks)};size=len(masks)
    higher=[sum(1<<j for j in range(i+1,size) if (masks[i]&masks[j]).bit_count()<=1) for i in range(size)]
    def count_cliques(available,left):
        if left==0:return 1
        if left==1:return available.bit_count()
        total=0
        while available:
            bit=available&-available;available-=bit;i=bit.bit_length()-1
            total+=count_cliques(available&higher[i],left-1)
        return total
    total=count_cliques((1<<size)-1,n6+n7)
    if n7:
        if (n6,n7)!=(1,1):raise ValueError('Only needed mixed role case')
        total*=2
    generators=[]
    for P in paths:
        if len(P)>1:
            p=list(range(12))
            for u,v in zip(P,P[::-1]):p[u]=v
            generators.append(p)
    for length in sorted(set(map(len,paths))):
        same=[P for P in paths if len(P)==length]
        for P,Q in zip(same,same[1:]):
            p=list(range(12))
            for u,v in zip(P,Q):p[u],p[v]=v,u
            generators.append(p)
    maps=[]
    for p in generators:
        if {frozenset(p[t] for t in e) for e in edges}!=edges:raise ValueError('Invalid automorphism')
        maps.append([ids[sum(1<<p[t] for t in range(12) if B>>t&1)] for B in masks])
    minima=set();records=[];summed=0
    for number,Qs in enumerate(reps(fid,n6,n7)):
        f=tuple(ids[sum(1<<v for v in Q)] for Q in Qs)
        require=all((masks[a]&masks[b]).bit_count()<=1 for a,b in combinations(f,2))
        if not require or len(set(f))!=n6+n7:raise ValueError('Invalid family')
        seed=tuple(sorted(f[:n6]))+tuple(sorted(f[n6:]));orbit={seed};todo=[seed]
        while todo:
            f=todo.pop()
            for p in maps:
                z=tuple(sorted(p[i] for i in f[:n6]))+tuple(sorted(p[i] for i in f[n6:]))
                if z not in orbit:orbit.add(z);todo.append(z)
        canonical=min(orbit)
        if canonical in minima:raise ValueError('Overlapping orbit representatives')
        minima.add(canonical);summed+=len(orbit)
        records.append([number,len(orbit),hashlib.sha256(json.dumps(sorted(orbit),separators=(',',':')).encode()).hexdigest()])
    if summed!=total:raise ValueError(('Incomplete cover',fid,n6,n7,summed,total))
    return dict(fid=fid,n6=n6,n7=n7,four_sets=size,labeled_families=total,orbit_count=len(records),records=records)
