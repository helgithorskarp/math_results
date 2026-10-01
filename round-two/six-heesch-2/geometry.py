"""Unmarked polyhexes in exact axial coordinates, with arbitrary-size integers."""
DIRS = ((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))

def normalize(cells):
    a,b=min(cells)
    return tuple(sorted((x-a,y-b) for x,y in cells))

def matrices():
    out=[]
    for reflect in (False,True):
        m=(1,1,0,-1) if reflect else (1,0,0,1)
        for _ in range(6):
            out.append(m)
            a,b,c,d=m;m=(-c,-d,a+c,b+d)
    return tuple(out)

def affine(cells,g):
    a,b,c,d,u,v=g
    return tuple(sorted((a*x+b*y+u,c*x+d*y+v) for x,y in cells))

def inverse(g):
    a,b,c,d,u,v=g;det=a*d-b*c
    assert det in (-1,1)
    aa,bb,cc,dd=d*det,-b*det,-c*det,a*det
    return (aa,bb,cc,dd,-aa*u-bb*v,-cc*u-dd*v)

def orientations(cells):
    return tuple(sorted({normalize(affine(cells,m+(0,0))) for m in matrices()}))

def canonical(cells):
    return min(orientations(cells))

def pose(cells,target):
    target=tuple(sorted(target))
    for m in matrices():
        raw=affine(cells,m+(0,0))
        u,v=min(raw);x,y=min(target)
        g=m+(x-u,y-v)
        if affine(cells,g)==target:return g
    raise ValueError('Footprints are not congruent polyhexes')

def halo(cells):
    s=set(cells)
    return {(x+a,y+b) for x,y in s for a,b in DIRS}-s

def contacts(cells):
    s=set(cells);h=halo(s);out=set()
    for o in orientations(cells):
        for u,v in {(x-a,y-b) for x,y in h for a,b in o}:
            t=tuple((x+u,y+v) for x,y in o)
            if s.isdisjoint(t):out.add(t)
    return tuple(sorted(out))

def connected(cells):
    unseen=set(cells);stack=[unseen.pop()]
    while stack:
        x,y=stack.pop()
        for a,b in DIRS:
            q=(x+a,y+b)
            if q in unseen:unseen.remove(q);stack.append(q)
    return not unseen

def holes(cells):
    s=set(cells)
    lx=min(x for x,y in s)-1;hx=max(x for x,y in s)+1
    ly=min(y for x,y in s)-1;hy=max(y for x,y in s)+1
    unseen={(x,y) for x in range(lx,hx+1) for y in range(ly,hy+1)}-s
    stack=[(lx,ly)];unseen.remove(stack[0])
    while stack:
        x,y=stack.pop()
        for a,b in DIRS:
            q=(x+a,y+b)
            if q in unseen:unseen.remove(q);stack.append(q)
    return unseen
