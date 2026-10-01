#!/usr/bin/env python3
"""Exact reference geometry for the small-quartic-bow theorem.

Points are (Xa,Xb,Ya,Yb), giving coordinates (Xa+Xb*sqrt(3))/2,
(Ya+Yb*sqrt(3))/2. Author: six-heesch-3, researcher, 2026-10-01.
"""
from collections import Counter,defaultdict
from functools import lru_cache

AXIAL=((0,0),(-1,-1),(0,-2),(1,-2),(2,-2),(2,-1),(4,-2),(5,-1),
       (4,0),(3,0),(2,2),(0,3),(0,2),(-1,2))
IDENTITY=(0,0,0,0,0,0)
def require(ok,msg):
    if not ok:raise ValueError(msg)
def qadd(p,q):return p[0]+q[0],p[1]+q[1]
def qsub(p,q):return p[0]-q[0],p[1]-q[1]
def qmul(p,q):return p[0]*q[0]+3*p[1]*q[1],p[0]*q[1]+p[1]*q[0]
def qsign(p):
    a,b=p
    if not a:return (b>0)-(b<0)
    if not b or (a>0)==(b>0):return (a>0)-(a<0)
    d=a*a-3*b*b;require(d!=0,'rational sqrt(3)')
    return ((a>0)-(a<0)) if d>0 else ((b>0)-(b<0))
def qcmp(a,b):return qsign(qsub(a,b))
def add(p,q):return tuple(x+y for x,y in zip(p,q))
def sub(p,q):return tuple(x-y for x,y in zip(p,q))
def cross(p,q):return qsub(qmul(p[:2],q[2:]),qmul(p[2:],q[:2]))
def dot(p,q):return qadd(qmul(p[:2],q[:2]),qmul(p[2:],q[2:]))
def rot30(p):
    a,b,c,d=p;n=(3*b-c,a-d,a+3*d,b+c)
    require(all(x%2==0 for x in n),'rotation module')
    return tuple(x//2 for x in n)
@lru_cache(None)
def orient(angle,flip,p):
    if flip:p=(p[0],p[1],-p[2],-p[3])
    for _ in range(angle%12):p=rot30(p)
    return p
def point(pose,p):return add(orient(pose[0],pose[1],p),pose[2:])
def compose(m,n):
    return ((m[0]+(-1 if m[1] else 1)*n[0])%12,m[1]^n[1])+add(m[2:],orient(m[0],m[1],n[2:]))
def inverse(m):
    a=(-m[0] if not m[1] else m[0])%12
    return (a,m[1])+orient(a,m[1],tuple(-x for x in m[2:]))
def twice_area(poly):
    return tuple(sum(cross(a,poly[(i+1)%len(poly)])[k] for i,a in enumerate(poly)) for k in (0,1))
def polygon():
    w=(0,0);vv=[]
    for i,(x,y) in enumerate(AXIAL):
        a,b=w;n=2*a+b;require(n%3==0,'prefix coefficient')
        vv.append((2*x+y-2*a-b,n//3,b,y-b))
        dx=AXIAL[(i+1)%14][0]-x;dy=AXIAL[(i+1)%14][1]-y
        if dx*dx+dx*dy+dy*dy==3:w=(a+dx,b+dy)
    require(w==(0,0),'long edge closure')
    return tuple(vv)
VERTICES=polygon()
DIRECTIONS=tuple(orient(i,0,(2,0,0,0)) for i in range(12))
DIR_INDEX={v:i for i,v in enumerate(DIRECTIONS)}
EDGES=tuple(sub(VERTICES[(i+1)%14],v) for i,v in enumerate(VERTICES))
require(all(dot(v,v)==(4,0) for v in EDGES),'nonunit edge')
require(all(v in DIR_INDEX for v in EDGES),'unknown direction')
EDGE_DIR=tuple(DIR_INDEX[v] for v in EDGES)
SECTORS=[]
for i,a in enumerate(EDGE_DIR):
    n=(EDGE_DIR[i-1]+6-a)%12;require(n in (3,4,6,8,9),'corner angle')
    SECTORS.append(sum(1<<((a+k)%12) for k in range(n)))
ROOT_INDEX={p:i for i,p in enumerate(VERTICES)}
GOAL=sum((4095^s)<<(12*i) for i,s in enumerate(SECTORS))
def in_triangle(p,t):return all(qsign(cross(sub(t[(i+1)%3],t[i]),sub(p,t[i])))>=0 for i in range(3))
def triangulate(poly):
    require(qsign(twice_area(poly))>0,'orientation')
    ids=list(range(len(poly)));result=[]
    while True:
        changed=False
        for k,i in enumerate(ids):
            if qsign(cross(sub(poly[i],poly[ids[k-1]]),sub(poly[ids[(k+1)%len(ids)]],poly[i])))==0:
                ids.pop(k);changed=True;break
        if not changed:break
    while len(ids)>3:
        for k,i in enumerate(ids):
            ix=(ids[k-1],i,ids[(k+1)%len(ids)]);t=tuple(poly[j] for j in ix)
            if qsign(twice_area(t))<=0:continue
            if any(in_triangle(poly[j],t) for j in ids if j not in ix):continue
            result.append(t);ids.pop(k);break
        else:raise ValueError('ear decomposition')
    result.append(tuple(poly[j] for j in ids))
    require(tuple(sum(twice_area(t)[k] for t in result) for k in (0,1))==twice_area(poly),'triangle area')
    return tuple(result)
TRIANGLES=triangulate(VERTICES)
def bounds(poly):
    result=[]
    for axis in (0,2):
        vals=[p[axis:axis+2] for p in poly];low=high=vals[0]
        for v in vals[1:]:
            if qcmp(v,low)<0:low=v
            if qcmp(v,high)>0:high=v
        result.append((low,high))
    return tuple(result)
def bbox_overlap(a,b):return all(qcmp(a[k][1],b[k][0])>0 and qcmp(b[k][1],a[k][0])>0 for k in (0,1))
def triangle_overlap(a,b):
    for t,u in ((a,b),(b,a)):
        for i,p in enumerate(t):
            e=sub(t[(i+1)%3],p)
            if all(qsign(cross(e,sub(q,p)))<=0 for q in u):return False
    return True
def on_segment(p,a,b):
    if qsign(cross(sub(b,a),sub(p,a))):return False
    for k in (0,2):
        q=p[k:k+2];x=a[k:k+2];y=b[k:k+2]
        if qcmp(x,y)>0:x,y=y,x
        if qcmp(q,x)<0 or qcmp(q,y)>0:return False
    return True
@lru_cache(20000)
def shape(pose):
    poly=tuple(point(pose,p) for p in VERTICES);tri=[]
    for t in TRIANGLES:
        u=tuple(point(pose,p) for p in t)
        if pose[1]:u=(u[0],u[2],u[1])
        tri.append(u)
    return poly,tuple(tri),bounds(poly)
def geometry(m,n):
    p,tp,bp=shape(m);q,tq,bq=shape(n)
    if bbox_overlap(bp,bq) and any(triangle_overlap(a,b) for a in tp for b in tq):return None
    pset=set(p);qset=set(q)
    for a in pset-qset:
        if any(on_segment(a,b,q[(j+1)%14]) for j,b in enumerate(q)):return None
    for a in qset-pset:
        if any(on_segment(a,b,p[(j+1)%14]) for j,b in enumerate(p)):return None
    edges={tuple(sorted((a,p[(i+1)%14]))):(i,a,p[(i+1)%14]) for i,a in enumerate(p)}
    relations=[]
    for j,a in enumerate(q):
        b=q[(j+1)%14];key=tuple(sorted((a,b)))
        if key not in edges:continue
        i,x,y=edges[key];reverse=int(x==b)
        require((-1)**m[1]==(-1)**(reverse+1+n[1]),'contact normals')
        relations.append((i,j,reverse))
    return tuple(sorted(relations))
def star_image(bits,a,f):return sum(1<<((a+k if not f else a-k-1)%12) for k in range(12) if bits&(1<<k))
def coverage(pose):
    covered=0
    for j,p in enumerate(shape(pose)[0]):
        if p not in ROOT_INDEX:continue
        i=ROOT_INDEX[p];s=star_image(SECTORS[j],pose[0],pose[1])
        require(not s&SECTORS[i],'overlapping angles')
        covered|=s<<(12*i)
    require(covered&~GOAL==0,'coverage outside goal')
    return covered
