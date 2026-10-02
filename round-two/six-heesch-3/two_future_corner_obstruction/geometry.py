#!/usr/bin/env python3
"""Integer lower-certificate reader for the mixed-grid strip family.

This module does NOT read an SVG and does NOT prove an upper bound or
an arbitrary-motion grid locking theorem. Every point is interpreted as
(x,sqrt(3)*y)/4. Positive affine rescaling reduces all incidence and
interior tests to integer cross products in (x,y). Poses are actual
Euclidean congruences:60-degree rotations and optional y reflection.
Author: six-heesch-3, researcher.
"""
from collections import Counter,defaultdict
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json
from math import gcd
from pathlib import Path
import resource
import time

HERE=Path(__file__).resolve().parent

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

def rotate(angle,p):
    require(angle in range(0,12,2),'reader accepts only60-degree rotations')
    x,y=p
    for unused in range(angle//2):
        xx,yy=x-3*y,x+y
        require(xx%2==0 and yy%2==0,'rotation leaves integer module')
        x,y=xx//2,yy//2
    return x,y

def point(pose,p):
    a,f,tx,ty=pose
    require(f in (0,1),'invalid reflection')
    x,y=rotate(a,(p[0],-p[1] if f else p[1]))
    return x+tx,y+ty

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

@lru_cache(2048)
def shape(m,pose):
    aa=tuple(ccw(tuple(point(pose,p) for p in poly)) for poly in atoms(m))
    return aa,tuple(box(p) for p in aa),box(tuple(v for p in aa for v in p))

def pair(m,p,q,stats=None):
    """Return (interiors_overlap,closed_sets_touch) without restricting T contacts."""
    a,ab,abox=shape(m,p);b,bb,bbox=shape(m,q)
    if not boxes_meet(abox,bbox):
        return False,False
    touch=False
    for pa,ba in zip(a,ab):
        for pb,bc in zip(b,bb):
            if not boxes_meet(ba,bc):
                continue
            if stats is not None:
                stats['atom_pair_tests']+=1
            if boxes_meet(ba,bc,False) and convex_intersection(pa,pb,False):
                return True,True
            if not touch and convex_intersection(pa,pb,True):
                touch=True
    return False,touch

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

def check(data):
    start=time.monotonic()
    m=data['tile_hexagons'];copies=data['copies']
    require(copies,'empty witness')
    poses=[tuple(r['pose']) for r in copies];levels=[r['level'] for r in copies]
    require(all(len(p)==4 and all(isinstance(x,int) for x in p) for p in poses),'noninteger pose')
    require(len(set(poses))==len(poses),'duplicate pose')
    require(all(isinstance(i,int) and i>=0 for i in levels),'invalid corona level')
    require(levels.count(0)==1 and poses[levels.index(0)]==(0,0,0,0),'root is not normalized')
    h=max(levels)
    require(sorted(set(levels))==list(range(h+1)),'missing corona level')
    counts=[levels.count(i) for i in range(h+1)]
    if 'level_counts' in data:
        require(counts==data['level_counts'],'declared counts disagree')
    boundary(atoms(m))
    contacts=[set() for p in poses];stats=Counter()
    for i,j in combinations(range(len(poses)),2):
        overlap,touch=pair(m,poses[i],poses[j],stats)
        require(not overlap,f'copy interiors overlap: {i},{j}')
        if touch:
            contacts[i].add(j);contacts[j].add(i)
    for i,level in enumerate(levels):
        if level:
            require(any(levels[j]==level-1 for j in contacts[i]),f'copy {i} misses preceding corona')
    prefixes=[];previous=None
    for level in range(h+1):
        ids=[i for i,l in enumerate(levels) if l<=level]
        aa=tuple(p for i in ids for p in shape(m,poses[i])[0])
        cycle,edges=boundary(aa)
        if previous is not None:
            require(not any(segments_meet(*a,*b) for a in previous for b in edges),
                    f'prefix {level-1} is not strictly inside prefix {level}')
        previous=edges
        prefixes.append({'corona':level,'copies':len(ids),'boundary_segments':len(edges),
                         'twice_area_integer':twice_area(cycle),'is_simple_disc':True,
                         'previous_strictly_interior':None if not level else True})
    return {'agent':'six-heesch-3','role':'researcher','status':'exact construction-side certificate only',
            'tile_hexagons':m,'verified_coronas':h,'copies':len(poses),'level_counts':counts,
            'prefixes':prefixes,'closed_contact_pairs':sum(map(len,contacts))//2,
            'atom_pair_tests':stats['atom_pair_tests'],'elapsed_seconds':time.monotonic()-start,
            'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'upper_bound_claimed':False,'all_motion_grid_locking_claimed':False}
