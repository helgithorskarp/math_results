"""Exact axial-coordinate polyhex geometry; Python arbitrary precision."""
DIRS = ((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))
def normalize(cells):
    a,b=min(cells)
    return tuple(sorted((x-a,y-b) for x,y in cells))

def halo(cells):
    s=set(cells)
    return {(x+a,y+b) for x,y in s for a,b in DIRS}-s

def orientations(cells):
    seen=set();out=[]
    for reflect in (0,1):
        pts=[(x+y,-y) if reflect else (x,y) for x,y in cells]
        for rot in range(6):
            o=normalize(pts)
            if o not in seen:
                seen.add(o);out.append(o)
            pts=[(-y,x+y) for x,y in pts]
    return out

def contacts(cells):
    s=set(cells);h=halo(s);out=set()
    for o in orientations(cells):
        for dx,dy in {(x-a,y-b) for x,y in h for a,b in o}:
            t=tuple((x+dx,y+dy) for x,y in o)
            if s.isdisjoint(t):out.add(t)
    return sorted(out)

def holes(cells):
    s=set(cells);lo_x=min(x for x,y in s)-1;hi_x=max(x for x,y in s)+1
    lo_y=min(y for x,y in s)-1;hi_y=max(y for x,y in s)+1
    unseen={(x,y) for x in range(lo_x,hi_x+1) for y in range(lo_y,hi_y+1)}-s
    q=[(lo_x,lo_y)];unseen.remove(q[0])
    while q:
        x,y=q.pop()
        for a,b in DIRS:
            p=(x+a,y+b)
            if p in unseen:unseen.remove(p);q.append(p)
    return unseen

def transform_between(cells,tile):
    for reflect in (0,1):
        M=(1,1,0,-1) if reflect else (1,0,0,1)
        for rot in range(6):
            a,b,c,d=M;raw=[(a*x+b*y,c*x+d*y) for x,y in cells]
            if normalize(raw)==normalize(tile):
                mx,my=min(raw);sx,sy=min(tile)
                return (a,b,c,d,sx-mx,sy-my)
            M=(-c,-d,a+c,b+d)
    raise ValueError('Non-congruent tile')

def transform(t,cells):
    a,b,c,d,x,y=t
    return tuple(sorted((a*u+b*v+x,c*u+d*v+y) for u,v in cells))
