"""Exact triangular-grid geometry adapted from six-reviewer-1.

Only generic centroid, D6, star, mesh and footprint definitions are reused
from ../heesch_polyiamond_deficit_review1/check.py, SHA256
9c96aa23e9bcc4d84d8cc222523d7db515887b09219c770838cd4b7073402eef.
No T214-specific statement, bound or review verdict transfers to T211.
"""
from collections import defaultdict
from functools import lru_cache
from itertools import combinations

IDENTITY = (1, 0, 0, 1, 0, 0)
DIR = ((1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1), (1, -1))

def require(ok, message):
    if not ok:
        raise ValueError(message)

def norm(v):
    x, y = v
    return x*x+x*y+y*y

def vertices(f):
    sx, sy = f
    r = sx % 3
    require(r == sy % 3 and r in (1, 2), ('invalid face', f))
    x, y = (sx-r)//3, (sy-r)//3
    if r == 1:
        return ((x, y), (x+1, y), (x, y+1))
    return ((x+1, y+1), (x, y+1), (x+1, y))

def triangle(vs):
    require(len(set(vs)) == 3 and all(norm((u[0]-v[0],u[1]-v[1])) == 1
            for u, v in combinations(vs, 2)), ('non-unit triangle', vs))
    f = (sum(v[0] for v in vs), sum(v[1] for v in vs))
    require(set(vertices(f)) == set(vs), 'face decoder mismatch')
    return f

def point(p, v):
    a,b,c,d,x,y = p
    return (a*v[0]+b*v[1]+x, c*v[0]+d*v[1]+y)

def face(p, f):
    a,b,c,d,x,y = p
    return (a*f[0]+b*f[1]+3*x, c*f[0]+d*f[1]+3*y)

def compose(p, q):
    a,b,c,d,x,y = p; e,f,g,h,u,v = q
    return (a*e+b*g,a*f+b*h,c*e+d*g,c*f+d*h,a*u+b*v+x,c*u+d*v+y)

def inverse(p):
    a,b,c,d,x,y = p; z = a*d-b*c
    require(abs(z) == 1, 'nonunimodular pose')
    q = (d//z,-b//z,-c//z,a//z,0,0)
    u,v = point(q, (-x,-y))
    out = q[:4]+(u,v)
    require(compose(p,out) == compose(out,p) == IDENTITY, 'inverse mismatch')
    return out

def matrices():
    unit = [(x,y) for x in range(-1,2) for y in range(-1,2) if norm((x,y)) == 1]
    out = sorted((a,b,c,d) for a,c in unit for b,d in unit
                 if 2*a*b+a*d+b*c+2*c*d == 1)
    require(len(out) == 12, 'Gram isometry census')
    return out

@lru_cache(maxsize=None)
def star(v):
    x,y = v
    return tuple(triangle((v,(x+DIR[j][0],y+DIR[j][1]),
                          (x+DIR[(j+1)%6][0],y+DIR[(j+1)%6][1]))) for j in range(6))

def mesh(fs):
    edges = defaultdict(list); vs = set()
    for f in fs:
        tri = vertices(f); vs.update(tri)
        for e in combinations(tri,2):
            edges[tuple(sorted(e))].append(f)
    require(all(len(rows) in (1,2) for rows in edges.values()), 'nonmanifold edge')
    boundary = defaultdict(set); adjacent = defaultdict(set)
    for e, rows in edges.items():
        if len(rows) == 1:
            u,v = e; boundary[u].add(v); boundary[v].add(u)
        else:
            u,v = rows; adjacent[u].add(v); adjacent[v].add(u)
    seen = set(); todo = [next(iter(fs))]
    while todo:
        f = todo.pop()
        if f not in seen:
            seen.add(f); todo.extend(adjacent[f]-seen)
    require(seen == fs, 'not edge connected')
    for v in vs:
        link = [f in fs for f in star(v)]
        transitions = sum(link[j] != link[(j+1)%6] for j in range(6))
        require(transitions in (0,2), ('pinched vertex',v))
    require(boundary and all(len(row)==2 for row in boundary.values()), 'boundary degree')
    seen = set(); todo = [next(iter(boundary))]
    while todo:
        v = todo.pop()
        if v not in seen:
            seen.add(v); todo.extend(boundary[v]-seen)
    require(seen == set(boundary), 'multiple boundary components')
    chi = len(vs)-len(edges)+len(fs)
    require(chi == 1, 'Euler characteristic not one')
    return {'faces':len(fs),'vertices':len(vs),'edges':len(edges),'chi':chi,
            'boundary_vertices':len(boundary)},vs

class Geometry:
    def __init__(self, fs):
        self.fs = fs
        self.vs = {v for f in fs for v in vertices(f)}
        self.ms = matrices()

    @lru_cache(maxsize=4000)
    def footprint(self, p):
        return frozenset(face(p, f) for f in self.fs)

    def union(self, fixed):
        occupied = set()
        for p in fixed:
            foot = self.footprint(p)
            require(not occupied & foot, 'overlapping fixed copies')
            occupied.update(foot)
        return occupied
