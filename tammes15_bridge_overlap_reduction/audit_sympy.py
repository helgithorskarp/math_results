#!/usr/bin/env python3
"""Separate SymPy arithmetic audit of the complete overlap certificate.

The finite graph catalog, graph canonicalization and compact proof seeds
are shared with the stdlib checker. All coordinates, scalar residuals,
root counts, Gram placements and signs are rederived in Q(t)/ANP here.
This is not independent enumeration, formalization or mathematical review.
"""
from pathlib import Path
from family import catalog
from check import decagon
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import comb
import json
import sympy as s
from sympy.polys.fields import field
from sympy.polys.polyclasses import ANP

def need(q,msg):
    if not q:raise ValueError(msg)

K,t=field('t',s.QQ);one,zero=K.one,K.zero
H=[[one if i==j else t for j in range(3)] for i in range(3)]
HI=[[((1/(1-t)) if i==j else zero)-t/((1-t)*(1+2*t)) for j in range(3)] for i in range(3)]
DH=(1-t)**2*(1+2*t);r=2*t/(1+t)

def dot(x,y):return (1-t)*sum((a*b for a,b in zip(x,y)),zero)+t*sum(x,zero)*sum(y,zero)
def cross(x,y):return [x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0]]
def matvec(m,x):return [sum((a*b for a,b in zip(row,x)),zero) for row in m]
def reflect(a,i,j,old):return [r*(x+y)-z for x,y,z in zip(a[i],a[j],a[old])]
def neighbors(edges,n):return {i:{j for u,v in edges for j in ((v,) if u==i else (u,) if v==i else ())} for i in range(n)}
def coefficients(p):
    return [Fraction(int(q.numerator),int(q.denominator)) for i in range(p.degree()+1) for q in (p.get((i,),0),)] if p else []
def polynomial(p,x):return s.Poly(sum(s.Rational(q.numerator,q.denominator)*x**i for i,q in enumerate(coefficients(p))),x,domain=s.QQ)
def p_sign(p):
    cs=coefficients(p)
    if not cs:return 0
    n=len(cs)-1;lo,step=Fraction(1,2),Fraction(1,10)
    affine=[sum(cs[j]*comb(j,k)*lo**(j-k)*step**k for j in range(k,n+1)) for k in range(n+1)]
    b=[sum(affine[k]*Fraction(comb(i,k),comb(n,k)) for k in range(i+1)) for i in range(n+1)]
    if all(v>=0 for v in b) and any(v>0 for v in b):return 1
    if all(v<=0 for v in b) and any(v<0 for v in b):return -1
    return 0

def sign(r):return p_sign(r.numer)*p_sign(r.denom)

class Algebra:
    def __init__(self,p,lo,hi):
        self.mod=list(reversed(p));self.lo,self.hi=lo,hi
        self.zero=ANP([],self.mod,s.QQ);self.one=ANP([1],self.mod,s.QQ);self.t=ANP([1,0],self.mod,s.QQ)
    def number(self,q):
        q=Fraction(q);return ANP([s.QQ(q.numerator,q.denominator)],self.mod,s.QQ)
    def from_rat(self,q):
        def convert(p):return ANP([s.QQ(v.numerator,v.denominator) for v in reversed(coefficients(p))],self.mod,s.QQ)
        return convert(q.numer)/convert(q.denom)
    def interval(self,p):
        lo=hi=Fraction(0)
        for q in p.to_list():
            v=Fraction(int(q.numerator),int(q.denominator))
            ends=(lo*self.lo,lo*self.hi,hi*self.lo,hi*self.hi)
            lo,hi=min(ends)+v,max(ends)+v
        return lo,hi
    def sign(self,p):
        if p==self.zero:return 0
        lo,hi=self.interval(p)
        if lo>0:return 1
        if hi<0:return -1
        raise ValueError('independent interval sign unresolved')
    def dot(self,x,y):return (self.one-self.t)*sum((a*b for a,b in zip(x,y)),self.zero)+self.t*sum(x,self.zero)*sum(y,self.zero)
    def det(self,m):return m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])-m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])+m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0])
    def solve(self,m,b):
        d=self.det(m)
        if d==self.zero:return None
        return tuple(self.det([[b[i] if j==k else m[i][j] for j in range(3)] for i in range(3)])/d for k in range(3))


B={8:[one,zero,zero],9:[zero,one,zero],10:[zero,zero,one],11:[-one,r,r],12:[r,r,-one]}
KAPPA=t*(9*t*t-2*t-3)/(1+t)**2
F=(-1,-3,2,6,-1,13)
ROOT_LO=Fraction('0.59260590292507377809642492233275')
ROOT_HI=Fraction('0.59260590292507377809642492233276')

def coordinates(record):
    a={v:[one if i==k else zero for i in range(3)] for k,v in enumerate(record['anchors'])}
    for v,i,j,old in record['steps']:a[v]=reflect(a,i,j,old)
    need(all(dot(q,q)==one for q in a.values()),'separate A unit norms')
    need(all(dot(a[i],a[j])==t for i,j in record['edges']),'separate A contacts')
    return a

def placement(a,u,v,orientation):
    normal=matvec(HI,cross(u,v));bcross=cross(B[11],B[12]);points=dict(a)
    for j,vector in B.items():
        b1,b2=dot(vector,B[11]),dot(vector,B[12]);l=DH*sum((x*y for x,y in zip(vector,bcross)),zero)/(1-KAPPA*KAPPA)
        points[j]=[((b1-KAPPA*b2)*x+(b2-KAPPA*b1)*y)/(1-KAPPA*KAPPA)+orientation*l*z for x,y,z in zip(u,v,normal)]
    return points

def open_roots(poly,lo=s.Rational(1,2),hi=s.Rational(3,5)):
    for endpoint in (lo,hi):
        while poly.degree()>0 and poly.eval(endpoint)==0:
            poly=poly.exquo(s.Poly(poly.gens[0]-endpoint,poly.gens[0],domain=s.QQ))
    return int(poly.count_roots(lo,hi)) if poly.degree()>0 else 0

def field_seed(entry):
    p=entry['polynomial'];x=s.Symbol('x');poly=s.Poly.from_list(list(reversed(p)),x,domain=s.QQ)
    lo,hi=(Fraction(*q) for q in entry['bracket'])
    need(open_roots(poly)==1 and open_roots(poly,s.Rational(lo.numerator,lo.denominator),s.Rational(hi.numerator,hi.denominator))==1,'separate seed root counts')
    need(poly.eval(s.Rational(lo.numerator,lo.denominator))*poly.eval(s.Rational(hi.numerator,hi.denominator))<0,'separate seed endpoint signs')
    return Algebra(p,lo,hi),poly


def audit(data):
    zero_reject={tuple(q[:3]):q[3] for q in data['zero_rejections']};zero_alias={tuple(q[:3]):q[3] for q in data['zero_aliases']}
    root_reject={tuple(q[:3]):q[3] for q in data['root_rejections']};disjoint={tuple(q) for q in data['disjoint_branches']}
    active={(p,c):i for p,c,i in data['active']};fields=[field_seed(q) for q in data['roots']]
    used_zr=set();used_za=set();used_rr=set();used_db=set();used_active=set();aliases=[]
    counts=[0,0,0,0];x=s.Symbol('x')
    need(dot(B[11],B[12])==KAPPA,'separate B ear Gram')
    for p,record in enumerate(catalog()):
        a=coordinates(record);forced={}
        for i,j,old in record['candidates']:
            w=dot(a[i],a[j]);forced[(i,j,old)]=[2*t/(1+w)*(xx+yy)-z for xx,yy,z in zip(a[i],a[j],a[old])]
        for c,(left,right) in enumerate(record['gluings']):
            u,v=forced[left],forced[right];R=dot(u,v)-KAPPA
            if not R:
                counts[1]+=1
                for orientation in (-1,1):
                    key=(p,c,orientation);points=placement(a,u,v,orientation)
                    need(all(dot(q,q)==one for q in points.values()),'separate continuous frame norms')
                    if key in zero_reject:
                        i,j=zero_reject[key];g=dot(points[i],points[j]);need(sign(g-t)==1,'separate uniform collision')
                        if i<8 and j in (8,9,10):need(sign(1-g)==1,'separate uniform noncoincidence')
                        used_zr.add(key);continue
                    need(key in zero_alias,'separate zero branch omitted');pairs=zero_alias[key];mapping={i:i for i in range(13)}
                    for i,j in pairs:need(points[i]==points[j],'separate alias identity');mapping[j]=i
                    triangle=tuple(sorted(mapping[j] for j in (8,9,10)))
                    prescribed_triangles={tuple(sorted(record['anchors']))}|{tuple(sorted((vv,i,j))) for vv,i,j,old in record['steps']}
                    need(triangle in prescribed_triangles,'separate shared prescribed triangle')
                    quotient={mapping[j]:points[j] for j in points};need(len(quotient)==10,'separate quotient cardinality');edges=[]
                    for i,j in combinations(sorted(quotient),2):
                        g=dot(quotient[i],quotient[j]);need(sign(1-g)==1,'separate quotient distinctness')
                        need(not (t-g) or sign(t-g)==1,'separate quotient packing')
                        if not t-g:edges.append((i,j))
                    order,canonical,_=decagon(edges,sorted(quotient))
                    aliases.append({'key':list(key),'anchor_aliases':pairs,'shared_B_anchor_triangle':list(triangle),'packing_points':10,'contacts':len(edges),'boundary_order':order,'canonical_decagon_mask':canonical});used_za.add(key)
                continue
            poly=polynomial(R.numer,x);n=open_roots(poly)
            if not n:counts[0]+=1;need((p,c) not in active,'separate spurious root assignment');continue
            need(n==1 and (p,c) in active,'separate complete root partition');used_active.add((p,c))
            index=active[(p,c)];f,factor=fields[index];need(poly.rem(factor).is_zero,'separate scalar factor')
            if tuple(data['roots'][index]['polynomial'])==F:counts[3]+=1;continue
            if f.lo>ROOT_HI:counts[2]+=1;continue
            need(f.hi<ROOT_LO,'separate strict-incumbent root comparison')
            for orientation in (-1,1):
                key=(p,c,orientation);points={j:tuple(f.from_rat(q) for q in vector) for j,vector in placement(a,u,v,orientation).items()}
                need(all(f.dot(q,q)==f.one for q in points.values()),'separate root frame norms')
                if key in root_reject:
                    i,j=root_reject[key];g=f.dot(points[i],points[j]);need(f.sign(g-f.t)==1,'separate root collision')
                    if i<8 and j in (8,9,10):need(f.sign(f.one-g)==1,'separate root noncoincidence')
                    used_rr.add(key)
                else:
                    need(key in disjoint,'separate root branch omitted')
                    need(all(f.sign(f.t-f.dot(points[i],points[j]))>=0 for i,j in combinations(range(13),2)),'separate disjoint packing');used_db.add(key)
    need(counts==[322,7,2,1],'separate355 scalar partition')
    need(used_zr==set(zero_reject) and used_za==set(zero_alias) and used_rr==set(root_reject) and used_db==disjoint and used_active==set(active),'separate no unused row')
    return aliases,counts


def audit_exception(entry):
    a={0:[one,zero,zero],6:[zero,one,zero],7:[zero,zero,one]}
    for vv,i,j,old in ((5,0,6,7),(4,0,5,6),(1,0,4,5),(3,1,4,0),(2,1,3,4)):a[vv]=reflect(a,i,j,old)
    w=dot(a[2],a[7]);center=[t/(1+w)*(x+y) for x,y in zip(a[2],a[7])];normal=matvec(HI,cross(a[2],a[7]))
    delta=DH*(1+w-2*t*t)/((1+w)**2*(1-w));v=reflect(a,5,6,0)
    alpha=dot(center,v)-KAPPA;beta=dot(normal,v);R=alpha*alpha-delta*beta*beta
    need(sign(alpha)==-1 and sign(beta)==sign(delta)==1,'separate exception unsquared signs')
    seed={'polynomial':entry['root_polynomial'],'bracket':entry['root_bracket']};f,poly=field_seed(seed);x=poly.gens[0]
    need(polynomial(R.numer,x)==poly*s.Poly((x-1)**2,x),'separate degree15 identity')
    lo,hi=f.lo,f.hi
    def val(q):return Fraction(poly.eval(s.Rational(q.numerator,q.denominator)))
    sl=val(lo)
    for _ in range(160):
        mid=(lo+hi)/2;sm=val(mid);need(sm!=0,'separate exception midpoint')
        if sm*sl>0:lo,sl=mid,sm
        else:hi=mid
    f=Algebra(entry['root_polynomial'],lo,hi);u=[c-alpha/beta*n for c,n in zip(center,normal)]
    branches=[]
    for orientation in (-1,1):
        points={j:tuple(f.from_rat(q) for q in vector) for j,vector in placement(a,u,v,orientation).items()}
        need(all(f.dot(q,q)==f.one for q in points.values()),'separate exceptional frame norms')
        need(all(f.sign(f.one-f.dot(points[i],points[j]))==1 for i,j in combinations(range(13),2)),'separate exception actual distinctness')
        branches.append({'orientation':orientation,'strictly_distinct_pairs':78,'A_B_cross_pairs':40})
    return {'root_degree':15,'branches':branches,'A_B_coincidences':0,'local_scope':'With only B ears outside A, any packing realization is forced to have all13 original positions distinct; prior saturation theorem then applies.'}

if __name__=='__main__':
    data=json.loads(Path(__file__).with_name('certificate.json').read_text());aliases,counts=audit(data)
    print(json.dumps({'status':'SEPARATE_SYMPY_ARITHMETIC_AUDIT','scalar_partition':counts,'continuous_shared_triangle_branches':aliases,'exception':audit_exception(data['exception_root']),'trust':'Finite graph catalog, graph canonicalization and proof seeds shared; coordinates, root counts, frames and signs separately rederived. Not independent mathematical review.'},indent=2,sort_keys=True))
