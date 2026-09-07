#!/usr/bin/env python3
"""Stdlib audit by real Cartesian algebra and rational linear systems.

No producer, numerical geometry, FLINT, NumPy, or SAT imports.
"""
import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations
import json
from math import lcm
from pathlib import Path

ZERO=(F(0),)*8
ONE=(F(1),)+ZERO[1:]
SQUARES=(3,11,247)

def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def minus(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(a,t):return tuple(x*t for x in a)

def product(a,b):
    out=[F(0)]*8
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:
                    coefficient=1
                    for k,square in enumerate(SQUARES):
                        if i&j&(1<<k):coefficient*=square
                    out[i^j]+=x*y*coefficient
    return tuple(out)

def inverse(a):
    """Solve multiplication-by-a as an8-dimensional rational linear system."""
    matrix=[[F(0)]*9 for _ in range(8)]
    for j in range(8):
        basis=tuple(F(int(k==j)) for k in range(8))
        column=product(a,basis)
        for i in range(8):matrix[i][j]=column[i]
    matrix[0][8]=F(1)
    for col in range(8):
        pivot=next((i for i in range(col,8) if matrix[i][col]),None)
        if pivot is None:raise ValueError('singular real field element')
        matrix[col],matrix[pivot]=matrix[pivot],matrix[col]
        divisor=matrix[col][col];matrix[col]=[x/divisor for x in matrix[col]]
        for i in range(8):
            if i!=col and matrix[i][col]:
                t=matrix[i][col];matrix[i]=[x-t*y for x,y in zip(matrix[i],matrix[col])]
    z=tuple(matrix[i][8] for i in range(8))
    if product(a,z)!=ONE:raise ValueError('inverse identity failed')
    return z

def padd(p,q):return plus(p[0],q[0]),plus(p[1],q[1])
def psub(p,q):return minus(p[0],q[0]),minus(p[1],q[1])
def pn(p):return plus(product(p[0],p[0]),product(p[1],p[1]))

def encode(p):
    x,y=p
    if any(x[i] for i in (1,2,4,7)) or any(y[i] for i in (0,3,5,6)):
        raise ValueError('outside source CM subspace')
    raw=(x[0],y[1],y[2],-x[3],y[4],-x[5],-x[6],-y[7])
    den=lcm(*(v.denominator for v in raw))
    return tuple(int(v*den) for v in raw),den

def norm_coefficients(z):
    a,b,c,d,e,f,g,h=z
    return (a*a+3*b*b+11*c*c+33*d*d+247*e*e+741*f*f+2717*g*g+8151*h*h,
            2*(-a*d+247*f*g+b*c-247*e*h),
            2*(-a*f+11*d*g+b*e-11*c*h),
            2*(-a*g+3*d*f+c*e-3*b*h))

def squared_difference(p,q):
    a,ad=p;b,bd=q
    delta=tuple(x*bd-y*ad for x,y in zip(a,b))
    return norm_coefficients(delta),(ad*bd)**2

def seed(raw):
    if len(raw)!=40 or any(len(v)!=4 or any(type(x)!=int for x in v) for v in raw):
        raise ValueError('bad source rows')
    base=[]
    for a,b,c,d in raw:
        x=(F(c,36),F(0),F(0),F(d,36),F(0),F(0),F(0),F(0))
        y=(F(0),F(-a,36),F(-b,36),F(0),F(0),F(0),F(0),F(0))
        base.append((x,y))
    cosine=F(119,128);sine=(F(0),F(0),F(0),F(0),F(3,128),F(0),F(0),F(0))
    if plus(scale(ONE,cosine*cosine),product(sine,sine))!=ONE:
        raise ValueError('bad source rotation')
    out=list(base)
    for x,y in base[1:]:out.append((minus(scale(x,cosine),product(sine,y)),plus(product(sine,x),scale(y,cosine))))
    if len(set(out))!=79:raise ValueError('source points coincide')
    return out

def center(a,b,c):
    ux,uy=psub(b,a);vx,vy=psub(c,a)
    determinant=minus(product(ux,vy),product(uy,vx))
    invdet=inverse(determinant)
    r1=scale(pn((ux,uy)),F(1,2));r2=scale(pn((vx,vy)),F(1,2))
    dx=product(minus(product(r1,vy),product(uy,r2)),invdet)
    dy=product(minus(product(ux,r2),product(r1,vx)),invdet)
    z=padd(a,(dx,dy))
    if any(pn(psub(z,v))!=ONE for v in (a,b,c)):raise ValueError('circumradius is not one')
    return z

def append_center(pts,triple):
    if type(triple)!=list or len(triple)!=3 or any(type(i)!=int or i<0 or i>=len(pts) for i in triple):
        raise ValueError('bad triple indices')
    if len(set(triple))!=3:raise ValueError('repeated triple vertex')
    z=center(*(pts[i] for i in triple))
    if z in set(pts):raise ValueError('coincident appended point')
    return z

def word_check(word,n,edges):
    if type(word)!=str or len(word)!=n or set(word)-set('0123'):raise ValueError('malformed colour word')
    if any(word[a]==word[b] for a,b in edges):raise ValueError('monochromatic unit edge')

def rejected(fn):
    try:fn()
    except ValueError:return 1
    raise ValueError('invalid certificate accepted')

def verify(raw,cert,producer=None):
    required={'format':1,'source':'EI2018-G79','trajectory_cap':1,'vertex_cap':508,
              'query_conflict_cap':100000,'trajectory_conflict_cap':500000,'status':'SAT'}
    if any(cert.get(k)!=v for k,v in required.items()):raise ValueError('wrong pilot metadata')
    if not 79<=cert['vertices']<=508 or len(cert['tape'])!=cert['vertices']-79:
        raise ValueError('wrong tape length')
    pts=seed(raw)
    for t in cert['tape']:pts.append(append_center(pts,t))
    encoded=[encode(p) for p in pts]
    if producer is not None:
        expected=[[F(x) for x in z] for z in producer]
        actual=[[F(x,d) for x in a] for a,d in encoded]
        if actual!=expected:raise ValueError('producer coordinates disagree')
    edges=[];aux=[];checks=0
    for j in range(len(pts)):
        earlier=0
        for i in range(j):
            n,d=squared_difference(encoded[i],encoded[j]);checks+=1
            if n==(d,0,0,0):edges.append((i,j));earlier+=1
            if j<79 and 3*n[0]==11*d and not any(n[1:]):aux.append((i,j))
        if j>=79 and earlier<3:raise ValueError('lost three-contact construction')
    seed_edges=[e for e in edges if e[1]<79]
    if len(seed_edges)!=165 or len(aux)!=118:raise ValueError('wrong source edge counts')
    if len(edges)!=cert['edges']:raise ValueError('wrong strict edge count')
    word_check(cert['colouring'],len(pts),edges)
    if cert['queries']!=len(pts)-78:raise ValueError('wrong SAT prefix count')
    controls=0;word=list(cert['colouring']);a,b=edges[0];word[b]=word[a]
    controls+=rejected(lambda:word_check(''.join(word),len(pts),edges))
    controls+=rejected(lambda:word_check(cert['colouring'][:-1],len(pts),edges))
    controls+=rejected(lambda:word_check('4'+cert['colouring'][1:],len(pts),edges))
    controls+=rejected(lambda:append_center(pts,[0,0,1]))
    controls+=rejected(lambda:append_center(pts,[0,1,len(pts)]))
    # Real z=(-16-sqrt33)/17 has rational norm coefficient1 but is not unit.
    if norm_coefficients((-16,0,0,1,0,0,0,0))!=(289,32,0,0):raise ValueError('nonrational norm control failed')
    return {'verified':True,'vertices':len(pts),'edges':len(edges),'all_pair_norm_checks':checks,
            'exact_circumcenters':len(cert['tape']),'verified_four_colourings':1,
            'certified_induced_prefixes':cert['queries'],'seed_vertices':79,'seed_unit_edges':165,
            'seed_auxiliary_pairs':118,'auxiliary_edges_used_in_unit_graph':0,
            'monochromatic_auxiliary_pairs_in_saved_word':sum(cert['colouring'][a]==cert['colouring'][b] for a,b in aux),
            'rejected_corruptions':controls,'colouring_sha256':hashlib.sha256(cert['colouring'].encode()).hexdigest(),
            'coordinate_sha256':hashlib.sha256(json.dumps([[[str(c) for c in a],str(d)] for a,d in encoded],separators=(',',':')).encode()).hexdigest(),
            'edge_sha256':hashlib.sha256(json.dumps(edges,separators=(',',':')).encode()).hexdigest(),
            'chromatic_upper_bound':4,'non_four_colourable_signal':False,'whole_family_classified':False,'record_improvement':False}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--certificate',type=Path,required=True)
    p.add_argument('--seed',type=Path,default=Path(__file__).with_name('seed40.json'))
    p.add_argument('--producer-points',type=Path)
    args=p.parse_args();raw=args.certificate.read_bytes();sr=args.seed.read_bytes()
    producer=json.loads(args.producer_points.read_text()) if args.producer_points else None
    out=verify(json.loads(sr),json.loads(raw),producer)
    out.update({'certificate_sha256':hashlib.sha256(raw).hexdigest(),'source40_sha256':hashlib.sha256(sr).hexdigest()})
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
