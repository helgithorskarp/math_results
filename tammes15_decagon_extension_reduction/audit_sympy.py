#!/usr/bin/env python3
"""Separate QQ(t) arithmetic audit; catalog, graph canonicalization and seeds shared.

Coordinates, cofactors, Cramer solves and root/sign checks are rederived.
This is not independent graph enumeration or mathematical review.
"""
from collections import Counter
from fractions import Fraction
from functools import lru_cache,reduce
from itertools import combinations,permutations
from math import comb,gcd,lcm
from pathlib import Path
import argparse,json
import sympy as s
from sympy.polys.fields import field
from family import catalog
from polytope import canonical

def need(q,msg):
    if not q:raise ValueError(msg)
K,t=field('t',s.QQ);one,zero=K.one,K.zero
H=[[one if i==j else t for j in range(3)] for i in range(3)]
HI=[[((1/(1-t)) if i==j else zero)-t/((1-t)*(1+2*t)) for j in range(3)] for i in range(3)]
DH=(1-t)**2*(1+2*t);r=2*t/(1+t);kap=t*(9*t*t-2*t-3)/(1+t)**2
B={8:[one,zero,zero],9:[zero,one,zero],10:[zero,zero,one],11:[-one,r,r],12:[r,r,-one]}
def dot(x,y):return (1-t)*sum((a*b for a,b in zip(x,y)),zero)+t*sum(x,zero)*sum(y,zero)
def rawdot(x,y):return sum((a*b for a,b in zip(x,y)),zero)
def cross(x,y):return [x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0]]
def matvec(m,x):return [rawdot(row,x) for row in m]
def coeffs(p):return tuple(Fraction(q.numerator,q.denominator) for i in range(p.degree()+1) for q in (p.get((i,),0),)) if p else ()

@lru_cache(None)
def psign(cs):
    if not cs:return 0
    n=len(cs)-1;lo,step=Fraction(1,2),Fraction(1,10)
    affine=[sum(cs[j]*comb(j,k)*lo**(j-k)*step**k for j in range(k,n+1)) for k in range(n+1)]
    b=[sum(affine[k]*Fraction(comb(i,k),comb(n,k)) for k in range(i+1)) for i in range(n+1)]
    if all(v>=0 for v in b) and any(v>0 for v in b):return 1
    if all(v<=0 for v in b) and any(v<0 for v in b):return -1
    x=s.Symbol('x');p=s.Poly.from_list([s.Rational(v.numerator,v.denominator) for v in reversed(cs)],x,domain=s.QQ)
    for endpoint in (s.Rational(1,2),s.Rational(3,5)):
        while p.degree()>0 and p.eval(endpoint)==0:p=p.exquo(s.Poly(x-endpoint,x,domain=s.QQ))
    if p.degree()>0 and p.count_roots(s.Rational(1,2),s.Rational(3,5)):return None
    v=sum(c*Fraction(11,20)**i for i,c in enumerate(cs));return (v>0)-(v<0)
def sign(q):
    if not q:return 0
    a,b=psign(coeffs(q.numer)),psign(coeffs(q.denom))
    return a*b if a is not None and b not in (0,None) else None
def encoded(q):
    a,b=coeffs(q.numer),coeffs(q.denom);scale=lcm(*(z.denominator for z in a+b))
    aa=[int(z*scale) for z in a];bb=[int(z*scale) for z in b];g=reduce(gcd,aa+bb,0)
    if bb[-1]<0:g=-g
    return {'numerator':[z//g for z in aa],'denominator':[z//g for z in bb]}
def code(y):return tuple((tuple(z['numerator']),tuple(z['denominator'])) for z in map(encoded,y))
def det(m):
    return sum(((-1)**sum(p[i]>p[j] for i,j in combinations(range(3),2))*m[0][p[0]]*m[1][p[1]]*m[2][p[2]] for p in permutations(range(3))),zero)
def numerator(m,k):return det([[t if j==k else m[i][j] for j in range(3)] for i in range(3)])

def core(key,aliases):
    p,c,orientation=key;record=catalog()[p]
    a={v:[one if i==k else zero for i in range(3)] for k,v in enumerate(record['anchors'])}
    for v,i,j,old in record['steps']:a[v]=[r*(x+y)-z for x,y,z in zip(a[i],a[j],a[old])]
    forced=[]
    for i,j,old in record['gluings'][c]:forced.append([2*t/(1+dot(a[i],a[j]))*(x+y)-z for x,y,z in zip(a[i],a[j],a[old])])
    u,v=forced;need(dot(u,v)==kap,'separate continuous ear Gram')
    normal=matvec(HI,cross(u,v));bcross=cross(B[11],B[12]);raw=dict(a)
    for j,x in B.items():
        b1,b2=dot(x,B[11]),dot(x,B[12]);lam=DH*rawdot(x,bcross)/(1-kap*kap)
        raw[j]=[((b1-kap*b2)*xx+(b2-kap*b1)*yy)/(1-kap*kap)+orientation*lam*z for xx,yy,z in zip(u,v,normal)]
    mapping={i:i for i in range(13)}
    for i,j in aliases:need(raw[i]==raw[j],'separate alias');mapping[j]=i
    points={mapping[i]:raw[i] for i in raw};need(len(points)==10,'separate ten points')
    need(all(dot(x,x)==one for x in points.values()),'separate unit norms');edges=[]
    for i,j in combinations(sorted(points),2):
        gap=t-dot(points[i],points[j]);need(not gap or sign(gap)==1,'separate packing');need(sign(1-dot(points[i],points[j]))==1,'separate distinctness')
        if not gap:edges.append((i,j))
    mask,canonical_mapping=canonical(edges,sorted(points));return points,mask,canonical_mapping

def audit_type(entry):
    points,mask,mapping=core(entry['key'],entry['aliases']);need(mask==entry['canonical_mask'],'separate mask')
    tet=entry['origin_tetrahedron'];cof=[(-1)**j*det([points[tet[k]] for k in range(4) if k!=j]) for j in range(4)]
    need(sign(sum(cof,zero)) in (-1,1) and any(sign(x) in (-1,1) for x in cof),'separate nonzero origin sum and rank')
    weights=[x/sum(cof,zero) for x in cof];need(all(sign(x)==1 for x in weights),'separate positive origin weights')
    need(all(sum((weights[j]*points[tet[j]][k] for j in range(4)),zero)==zero for k in range(3)),'separate origin identity')
    normals={j:matvec(H,x) for j,x in points.items()};vertices={};rejected=0
    need(len(entry['cover'])==120 and {tuple(z[:3]) for z in entry['cover']}==set(combinations(sorted(points),3)),'separate complete triple cover')
    for row in entry['cover']:
        triple=row[:3];m=[normals[j] for j in triple];d=det(m);nums=[numerator(m,k) for k in range(3)];need(d!=zero,'separate nonidentical rank')
        if row[3]==1:
            need(sign(t*d-rawdot(normals[row[4]],nums))==1 and sign(t*d-rawdot(normals[row[5]],nums))==-1,'separate opposite sides');rejected+=1;continue
        need(row[3:]==[0],'separate feasible row');y=[q/d for q in nums]
        need(all(psign(coeffs(x.denom)) in (-1,1) for x in y),'separate coordinate denominators')
        need(all(sign(t-rawdot(n,y)) in (0,1) for n in normals.values()),'separate feasibility')
        need(all(rawdot(normals[j],y)==t for j in triple),'separate active constraints')
        outside=sign(dot(y,y)-1);need(outside in (-1,1),'separate norm class')
        z=vertices.setdefault(code(y),{'y':y,'outside':outside==1,'independent':[]})
        if sign(d) in (-1,1):z['independent'].append(list(triple))
    rows=list(vertices.values());need(all(z['independent'] for z in rows),'separate uniform rank')
    for a,b in combinations(rows,2):need(any(sign(x-y) in (-1,1) for x,y in zip(a['y'],b['y'])),'separate vertex distinctness')
    outside=[z for z in rows if z['outside']];need(len(outside)==4,'separate four exterior')
    result={'key':entry['key'],'canonical_mask':mask,'total_triples':120,'opposite_side_triples':rejected,'feasible_triples':120-rejected,'vertices':len(rows),'inside_vertices':len(rows)-4,'exterior_vertices':4,'origin_tetrahedron':tet,'origin_weights':[encoded(x) for x in weights],'exterior_seed_triples':[z['independent'][0] for z in outside]}
    return result,points,mapping

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--type',type=int,choices=range(4));args=parser.parse_args()
    data=json.loads(Path(__file__).with_name('certificate.json').read_text());entries=data['types'] if args.type is None else [data['types'][args.type]]
    rows=[];reps={}
    for entry in entries:
        result,points,mapping=audit_type(entry);rows.append(result);reps[result['canonical_mask']]=(points,mapping)
    if args.type is None:
        for p,c,sg,aliases in data['six_alias_cases']:
            points,mask,mapping=core((p,c,sg),aliases);need(mask in reps,'separate six-placement type cover')
            rp,rm=reps[mask];inverse={j:i for i,j in rm.items()};corr={i:inverse[j] for i,j in mapping.items()}
            need(all(dot(points[i],points[j])==dot(rp[corr[i]],rp[corr[j]]) for i,j in combinations(sorted(points),2)),'separate exact Gram isometries')
    assignments={tuple([0]*a+[1]*b+[2]*c+[3]*(5-a-b-c)) for a in range(6) for b in range(6-a) for c in range(6-a-b)}
    need(len(assignments)==56,'separate weak-composition census')
    print(json.dumps({'status':'SEPARATE_SYMPY_ARITHMETIC_AUDIT','types':rows,'cap_assignments_per_type':len(assignments),'semialgebraic_systems':4*len(assignments),'trust':'Catalog, graph canonicalization and certificate seeds shared; coordinates, cofactors, Cramer solves and signs separately rederived. Not independent mathematical review.'},indent=2,sort_keys=True))
