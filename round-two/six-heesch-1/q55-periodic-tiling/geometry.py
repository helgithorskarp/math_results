"""Exact unit-cell construction primitives, using Python integers only."""
from collections import deque
from itertools import product
FOUR=((1,0),(-1,0),(0,1),(0,-1))
NINE=tuple(product((-1,0,1),repeat=2))

def require(ok,message):
    if not ok:raise ValueError(message)

def norm(cells):
    lo=min(x for x,y in cells),min(y for x,y in cells)
    return tuple(sorted((x-lo[0],y-lo[1]) for x,y in cells))

def images(cells):
    return tuple(sorted({norm([(sx*(y if swap else x),sy*(x if swap else y)) for x,y in cells])
                         for swap in (False,True) for sx,sy in product((-1,1),repeat=2)}))

def halo(cells):
    return {(x+dx,y+dy) for x,y in cells for dx,dy in NINE}-set(cells)

def connected(cells,start):
    seen={start};todo=deque([start])
    while todo:
        x,y=todo.popleft()
        for dx,dy in FOUR:
            q=x+dx,y+dy
            if q in cells and q not in seen:seen.add(q);todo.append(q)
    return seen

def disc(cells):
    cells=set(cells)
    if not cells or connected(cells,min(cells))!=cells:return False
    for vertex in {(x+dx,y+dy) for x,y in cells for dx,dy in product((0,1),repeat=2)}:
        x,y=vertex
        qs=[(x,y),(x-1,y),(x-1,y-1),(x,y-1)]
        bits=[q in cells for q in qs]
        if sum(bits)==2 and bits[0]==bits[2]:return False
    ax,bx=min(x for x,y in cells)-1,max(x for x,y in cells)+1
    ay,by=min(y for x,y in cells)-1,max(y for x,y in cells)+1
    empty={(x,y) for x in range(ax,bx+1) for y in range(ay,by+1)}-cells
    return connected(empty,(ax,ay))==empty

def verify_lower(data):
    cells=set(map(tuple,data['cells']));require(disc(cells),'prototype is not a disc')
    shapes=images(cells);occupied=set();stats=[]
    for k,ps in enumerate(data['levels']):
        previous=set(occupied)
        for o,x,y in ps:
            fp={(a+x,b+y) for a,b in shapes[o]}
            require(not fp&occupied,'lower whole-copy overlap')
            if k:require(bool(fp&halo(previous)),'lower copy misses prior prefix')
            occupied|=fp
        if k:require(halo(previous)<=occupied,'lower incomplete collar')
        require(disc(occupied),'lower prefix is not a disc')
        stats.append(dict(level=k,copies=sum(map(len,data['levels'][:k+1])),cells=len(occupied)))
    require(len(data['levels'][0])==1 and set(cells)=={(a+data['levels'][0][0][1],b+data['levels'][0][0][2])
                                                     for a,b in shapes[data['levels'][0][0][0]]},'wrong literal lower root')
    return stats
