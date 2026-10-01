"""Find compact periodic witnesses; failure is not a nontiling verdict."""
from geometry import orientations
from cover import Cover

def search(tile,max_copies=2,node_limit=50000):
    n=len(tile);os=orientations(tile)
    for copies in range(1,max_copies+1):
        area=copies*n
        for w in range(1,area+1):
            if area%w:continue
            h=area//w
            for s in range(w):
                def residue(p):
                    x,y=p;cy=y%h
                    return ((x-s*((y-cy)//h))%w,cy)
                root={residue(p) for p in tile}
                if len(root)!=n:continue
                if copies==1:return {'periods':[[w,0],[s,h]],'tiles':[tile]}
                required={(x,y) for x in range(w) for y in range(h)}-root
                choices={}
                for o in os:
                    if len({residue(p) for p in o})!=n:continue
                    for dx in range(w):
                        for dy in range(h):
                            footprint=tuple((x+dx,y+dy) for x,y in o)
                            key=tuple(sorted(residue(p) for p in footprint))
                            if root.isdisjoint(key):choices.setdefault(key,footprint)
                if not choices:continue
                if copies==2:
                    key=tuple(sorted(required))
                    if key in choices:return {'periods':[[w,0],[s,h]],'tiles':[tile,choices[key]]}
                else:
                    c=Cover(required,choices,node_limit=node_limit)
                    found=c.find()
                    if found is not None:
                        return {'periods':[[w,0],[s,h]],'tiles':[tile]+[choices[c.tiles[j]] for j in found]}
    return None

def verify(tile,witness):
    from geometry import pose
    (w,z),(s,h)=witness['periods']
    assert z==0 and w>0 and h>0 and 0<=s<w
    footprints=[tuple(map(tuple,t)) for t in witness['tiles']]
    assert all(len(t)==len(tile) and pose(tile,t) for t in footprints)
    points=[p for t in footprints for p in t]
    assert len(points)==w*h
    # Direct lattice-difference membership, independent of search residues.
    for i,(x,y) in enumerate(points):
        for u,v in points[:i]:
            dx=x-u;dy=y-v
            assert dy%h or (dx-s*(dy//h))%w
    return True
