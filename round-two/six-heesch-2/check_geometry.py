"""Definition-level witness checks and a boundary-edge contact inventory."""
from geometry import DIRS,matrices,affine,orientations,connected,halo,holes

def check_group():
    ms=matrices()
    assert len(set(ms))==12
    for a,b,c,d in ms:
        assert a*d-b*c in (-1,1)
        assert {(a*x+b*y,c*x+d*y) for x,y in DIRS}==set(DIRS)
        for e,f,g,h in ms:assert (a*e+b*g,a*f+b*h,c*e+d*g,c*f+d*h) in ms

def edge_contacts(tile):
    """Align opposing unit boundary edges, rather than cells to a halo."""
    root=set(tile);out=set()
    boundary=[(p,(a,b)) for p in root for a,b in DIRS if (p[0]+a,p[1]+b) not in root]
    for o in orientations(tile):
        own=set(o)
        edges={(a,b):[p for p in o if (p[0]-a,p[1]-b) not in own] for a,b in DIRS}
        for (x,y),(a,b) in boundary:
            for u,v in edges[a,b]:
                shifted=tuple(sorted((s+x+a-u,t+y+b-v) for s,t in o))
                if root.isdisjoint(shifted):out.add(shifted)
    return out

def check_coronas(tile,placements,allow_final_holes=True):
    assert connected(tile) and not holes(tile)
    assert len(set(tile))==len(tile)
    assert all(type(x) is int and type(y) is int for x,y in tile)
    copies=[];levels=[]
    for record in placements:
        k=record['level'];g=tuple(record['pose'])
        assert type(k) is int and k>=0 and len(g)==6 and all(type(v) is int for v in g)
        assert g[:4] in matrices()
        copies.append(affine(tile,g));levels.append(k)
    assert levels.count(0)==1
    assert copies[levels.index(0)]==tuple(sorted(tile))
    occupied=set()
    for t in copies:
        assert occupied.isdisjoint(t);occupied.update(t)
    stats=[];previous=set()
    for k in range(max(levels)+1):
        layer=[t for t,l in zip(copies,levels) if l==k]
        assert layer
        region=previous.union(*(set(t) for t in layer))
        assert connected(region)
        missing=holes(region)
        if k<max(levels) or not allow_final_holes:assert not missing
        if k:
            assert halo(previous)<=region
            old=[t for t,l in zip(copies,levels) if l==k-1]
            assert all(any(set(t)&halo(u) for u in old) for t in layer)
        stats.append({'level':k,'copies':len(layer),'cumulative_cells':len(region),'hole_cells':len(missing)})
        previous=region
    return stats,copies,levels
