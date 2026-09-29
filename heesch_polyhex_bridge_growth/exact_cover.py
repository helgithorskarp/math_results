"""Exhaustive definition-level halo exact cover, independent of SAT."""
from geometry import halo, contacts, holes
VERTICES=((1,1),(2,-1),(1,-2),(-1,-1),(-2,1),(-1,2))
def euler_holes(cells):
    vertices=set();edges=set()
    for x,y in cells:
        vs=[(3*x+a,3*y+b) for a,b in VERTICES]
        vertices.update(vs)
        for j in range(6): edges.add(tuple(sorted((vs[j],vs[(j+1)%6]))))
    return 1-len(vertices)+len(edges)-len(cells)

def enumerate_exact(cells,ts,limit=None):
    h=sorted(halo(cells));allcells=sorted(set().union(*(set(t) for t in ts)))
    index={p:i for i,p in enumerate(allcells)};hindex={p:i for i,p in enumerate(h)}
    masks=[sum(1<<index[p] for p in t) for t in ts]
    covers=[sum(1<<hindex[p] for p in t if p in hindex) for t in ts]
    at=[[] for p in h]
    for i,c in enumerate(covers):
        for j in range(len(h)):
            if (c>>j)&1:at[j].append(i)
    solutions=[];hf=0;used=set();nodes=0;complete=True
    def rec(occupied,remaining,chosen):
        nonlocal nodes,hf,complete
        if limit is not None and len(solutions)>=limit:
            complete=False;return
        nodes+=1
        if not remaining:
            sol=tuple(sorted(chosen));solutions.append(sol);used.update(sol)
            region=set(cells)
            for i in sol:region.update(ts[i])
            if euler_holes(region)==0:hf+=1
            return
        best=None
        for j in range(len(h)):
            if (remaining>>j)&1:
                legal=[i for i in at[j] if not masks[i]&occupied]
                if best is None or len(legal)<len(best):best=legal
                if not legal:return
                if len(best)==1:break
        for i in best:
            rec(occupied|masks[i],remaining&~covers[i],chosen+(i,))
    rec(0,(1<<len(h))-1,())
    assert len(solutions)==len(set(solutions))
    return dict(surrounds=len(solutions),holefree=hf,nodes=nodes,viable=len(used),complete=complete),solutions
def first_decision(cells):
    ts=contacts(cells);required=sorted(halo(cells));at=[[] for p in required]
    allcells=sorted(set().union(*(set(t) for t in ts)));idx={p:i for i,p in enumerate(allcells)}
    masks=[sum(1<<idx[p] for p in t) for t in ts];hidx={p:i for i,p in enumerate(required)}
    covers=[sum(1<<hidx[p] for p in t if p in hidx) for t in ts]
    for i,t in enumerate(ts):
        for p in t:
            if p in hidx:at[hidx[p]].append(i)
    nodes=0
    def rec(occupied,rem,chosen):
        nonlocal nodes
        nodes+=1
        if not rem:return chosen
        best=None
        for j in range(len(required)):
            if (rem>>j)&1:
                legal=[i for i in at[j] if not occupied&masks[i]]
                if best is None or len(legal)<len(best):best=legal
                if not legal:return None
                if len(best)==1:break
        for i in best:
            ans=rec(occupied|masks[i],rem&~covers[i],chosen+(i,))
            if ans is not None:return ans
        return None
    sol=rec(0,(1<<len(required))-1,())
    if sol is None:return dict(status='H0',nodes=nodes,contacts=len(ts))
    patch=set(cells)
    for i in sol:patch.update(ts[i])
    return dict(status='surrounded',nodes=nodes,contacts=len(ts),holefree=not holes(patch),witness=[ts[i] for i in sol])
