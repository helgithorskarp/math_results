"""Definition-level positive corona reader, using exact unit-cell geometry.

Adapted from six-heesch-2/strip-t5/exact.py (source a5052d63996131ca4eaceb22c1293a6fd4f9a056).
The positive checker uses no SAT, search certificate, contact domain or grid-lock
assumption. Explicit grid copies are admissible Euclidean copies directly.
"""
from tilings import affine, require

DIRS = ((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))


def isometry(g):
    require(len(g)==6 and all(type(v) is int for v in g), 'Invalid motion')
    a,b,c,d,u,v = g
    # Preservation of x^2+xy+y^2 is Euclidean isometry in axial coordinates.
    return (a*a+a*c+c*c == b*b+b*d+d*d == 1
            and 2*a*b+a*d+b*c+2*c*d == 1)


def halo(cells):
    cells=set(cells)
    return {(x+a,y+b) for x,y in cells for a,b in DIRS}-cells


def component(cells, first):
    cells=set(cells)
    require(first in cells, 'Missing component seed')
    reached={first}
    todo=[first]
    while todo:
        x,y=todo.pop()
        for a,b in DIRS:
            q=(x+a,y+b)
            if q in cells and q not in reached:
                reached.add(q)
                todo.append(q)
    return reached


def holes(cells):
    cells=set(cells)
    require(bool(cells), 'Empty region')
    lx,hx=min(x for x,y in cells)-1,max(x for x,y in cells)+1
    ly,hy=min(y for x,y in cells)-1,max(y for x,y in cells)+1
    empty={(x,y) for x in range(lx,hx+1) for y in range(ly,hy+1)}-cells
    return empty-component(empty,(lx,ly))


def coronas(tile, placements):
    tile=tuple(map(tuple,tile))
    require(len(set(tile))==len(tile) and component(tile,min(tile))==set(tile)
            and not holes(tile), 'The prototype is not a polyhex disc')
    occupied=set()
    copies=[]
    levels=[]
    for row in placements:
        level,g=row['level'],tuple(row['pose'])
        require(type(level) is int and level>=0 and isometry(g), 'Invalid corona copy')
        t=affine(tile,g)
        require(occupied.isdisjoint(t), 'Overlapping whole copies')
        occupied.update(t)
        copies.append(t)
        levels.append(level)
    require(levels.count(0)==1 and copies[levels.index(0)]==tile, 'Wrong central copy')
    previous=set()
    stats=[]
    for k in range(max(levels)+1):
        layer=[t for t,l in zip(copies,levels) if l==k]
        require(bool(layer), 'Missing corona')
        region=previous.union(*(set(t) for t in layer))
        require(component(region,min(region))==region and not holes(region), 'A prefix is not a disc')
        if k:
            require(halo(previous)<=region, 'Incomplete corona')
            old=[t for t,l in zip(copies,levels) if l==k-1]
            require(all(any(not halo(t).isdisjoint(u) for u in old) for t in layer),
                    'An added copy does not touch the previous corona')
        stats.append({'level':k,'copies':len(layer),'cumulative_cells':len(region),'hole_cells':0})
        previous=region
    return stats
