"""Exact convex/polygon geometry, shared with the author's earlier readers.
All input coordinates are integers. Positive affine scaling interprets
(x,y) as physical (x,sqrt(3)*y)/4 without changing incidences.
This is shared geometry, not an independent implementation or review.
Author: six-heesch-3, researcher.
"""
from collections import defaultdict
from functools import lru_cache
from itertools import combinations
from math import gcd

def require(condition,message):
    if not condition:
        raise ValueError(message)

def sub(a,b):
    return a[0]-b[0],a[1]-b[1]

def cross(a,b):
    return a[0]*b[1]-a[1]*b[0]

def turn(a,b,c):
    return cross(sub(b,a),sub(c,a))

def twice_area(p):
    return sum(cross(a,p[(i+1)%len(p)]) for i,a in enumerate(p))

def ccw(p):
    return tuple(p) if twice_area(p)>0 else tuple(reversed(p))

def box(p):
    return min(x for x,y in p),max(x for x,y in p),min(y for x,y in p),max(y for x,y in p)

def boxes_meet(a,b,closed=True):
    if closed:
        return a[0]<=b[1] and b[0]<=a[1] and a[2]<=b[3] and b[2]<=a[3]
    return a[0]<b[1] and b[0]<a[1] and a[2]<b[3] and b[2]<a[3]

def convex_intersection(a,b,closed):
    for p,q in ((a,b),(b,a)):
        for i,v in enumerate(p):
            values=[turn(v,p[(i+1)%len(p)],w) for w in q]
            if (max(values)<0 if closed else max(values)<=0):
                return False
    return True

def on_segment(p,a,b):
    return turn(a,b,p)==0 and min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1])

def segments_meet(a,b,c,d):
    if not boxes_meet(box((a,b)),box((c,d))):
        return False
    u,v,w,z=turn(a,b,c),turn(a,b,d),turn(c,d,a),turn(c,d,b)
    if (u>0 and v<0 or u<0 and v>0) and (w>0 and z<0 or w<0 and z>0):
        return True
    return (u==0 and on_segment(c,a,b) or v==0 and on_segment(d,a,b)
            or w==0 and on_segment(a,c,d) or z==0 and on_segment(b,c,d))

@lru_cache(None)
def atoms(m):
    require(isinstance(m,int) and m>=1,'bad strip length')
    result=[]
    for j in range(m):
        x=8*j
        result.append(ccw(((x,0),(x+2,2),(x+6,2),(x+8,0),(x+6,-2),(x+2,-2))))
        result.append(ccw(((x+2,2),(x+4,4),(x+6,2))))
        if j<m-1:
            result.append(ccw(((x+6,2),(x+8,0),(x+10,2))))
    result.append(ccw(((8*m-2,2),(8*m,0),(8*m,2))))
    for p in result:
        require(twice_area(p)>0,'degenerate atom')
        require(all(turn(p[i],p[(i+1)%len(p)],p[(i+2)%len(p)])>0 for i in range(len(p))),
                'nonconvex atom')
    require(sum(twice_area(p) for p in result)==4*(16*m-1),'prototype area mismatch')
    for a,b in combinations(result,2):
        require(not convex_intersection(a,b,False),'prototype atom interiors overlap')
    return tuple(result)

def boundary(polygons):
    """Split/cancel oriented supports exactly, then certify one simple CCW cycle."""
    lines=defaultdict(lambda:defaultdict(int))
    vertices=defaultdict(dict)
    for p in polygons:
        require(twice_area(p)>0,'boundary input is not CCW')
        for i,a in enumerate(p):
            b=p[(i+1)%len(p)];dx,dy=sub(b,a);g=gcd(abs(dx),abs(dy))
            require(g>0,'zero atom edge')
            u,v=dx//g,dy//g
            if u<0 or u==0 and v<0:
                u,v=-u,-v
            key=(u,v,u*a[1]-v*a[0])
            t=u*a[0]+v*a[1];s=u*b[0]+v*b[1]
            vertices[key][t]=a;vertices[key][s]=b
            lo,hi=sorted((t,s));sign=1 if s>t else -1
            lines[key][lo]+=sign;lines[key][hi]-=sign
    edges=[]
    for key,events in lines.items():
        ts=sorted(events);count=0
        for t,s in zip(ts,ts[1:]):
            count+=events[t]
            require(abs(count)<=1,'overlapping oriented boundary support')
            if count:
                a,b=vertices[key][t],vertices[key][s]
                edges.append((a,b) if count>0 else (b,a))
        require(count+events[ts[-1]]==0,'open support event sum')
    succ=defaultdict(list);pred=defaultdict(list)
    for a,b in edges:
        succ[a].append(b);pred[b].append(a)
    require(edges and set(succ)==set(pred),'open union boundary')
    require(all(len(succ[p])==len(pred[p])==1 for p in succ),'pinched union boundary')
    start=p=min(succ);cycle=[];seen=set()
    while p not in seen:
        seen.add(p);cycle.append(p);p=succ[p][0]
    require(p==start and len(cycle)==len(edges),'union has more than one boundary component')
    ordered=tuple((a,cycle[(i+1)%len(cycle)]) for i,a in enumerate(cycle))
    for i,j in combinations(range(len(ordered)),2):
        if (i-j)%len(ordered) in (1,len(ordered)-1):
            continue
        require(not segments_meet(*ordered[i],*ordered[j]),'union boundary self-intersects')
    require(twice_area(cycle)==sum(twice_area(p) for p in polygons),'union boundary area mismatch')
    return tuple(cycle),ordered
