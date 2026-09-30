#!/usr/bin/env python3
"""Optional SymPy1.14 independent exact arithmetic audit and certificate regeneration.

Imports no local research kernel and reads no certificate, expected output,
coordinate fixture, scratch file or network. The displayed root bracket,
origin tetrahedron and norm bound are proof seeds, each verified here.
"""
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
A_EDGES={(0,1),(0,4),(0,5),(0,6),(0,7),(1,2),(1,3),(1,4),(2,3),(3,4),(4,5),(5,6),(6,7)}
B_EDGES={(0,1),(0,2),(0,3),(0,4),(1,2),(2,3),(3,4)}

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

def generate():
    a={0:[one,zero,zero],6:[zero,one,zero],7:[zero,zero,one]}
    for v,i,j,old in ((5,0,6,7),(4,0,5,6),(1,0,4,5),(3,1,4,0),(2,1,3,4)):
        a[v]=reflect(a,i,j,old)
    b={0:[one,zero,zero],3:[zero,one,zero],4:[zero,zero,one]}
    b[2]=reflect(b,0,3,4);b[1]=reflect(b,0,2,3)
    need(all(dot(p,p)==one for p in (*a.values(),*b.values())),'independent patch norms')
    need(all(dot(a[i],a[j])==t for i,j in A_EDGES) and all(dot(b[i],b[j])==t for i,j in B_EDGES),'independent patch contacts')
    nb=neighbors(A_EDGES,8);E=(2,7);k=dot(b[1],b[4]);w=dot(a[2],a[7])
    c=[t/(1+w)*(x+y) for x,y in zip(a[2],a[7])];n=matvec(HI,cross(a[2],a[7]))
    D=DH*(1+w-2*t*t)/((1+w)**2*(1-w));need(sign(D)==1,'independent lens real')
    entries=[];active=[]
    for i,j in combinations(range(8),2):
        old=nb[i]&nb[j];extra=Counter(E+(i,j))
        if len(old)!=1 or any(len(nb[z])+extra[z]>5 for z in range(8)):continue
        old=next(iter(old));wij=dot(a[i],a[j])
        v=[2*t/(1+wij)*(x+y)-z for x,y,z in zip(a[i],a[j],a[old])]
        alpha=dot(c,v)-k;beta=dot(n,v);R=alpha*alpha-D*beta*beta
        entry=(i,j,old,v,alpha,beta,R);entries.append(entry)
        if not sign(R):active.append((len(entries)-1,entry))
    need(len(entries)==10 and len(active)==1 and active[0][0]==8,'independent complete ten-template partition')
    i,j,old,v,alpha,beta,R=active[0][1]
    need((i,j,old)==(5,6,0) and sign(alpha)==-1 and sign(beta)==1,'independent radical choice')
    x=s.Symbol('x');residual=polynomial(R.numer,x)
    factors=[f for f,multiplicity in s.factor_list(residual)[1] if f.count_roots(s.Rational(1,2),s.Rational(3,5))]
    need(len(factors)==1 and factors[0].degree()==15,'independent degree15 root factor')
    ppoly=factors[0].primitive()[1];p=[int(q) for q in reversed(ppoly.all_coeffs())]
    if p[-1]<0:p=[-q for q in p];ppoly=-ppoly
    lo,hi=Fraction(2196767,3802339),Fraction(535329,926590)
    need(ppoly.count_roots(s.Rational(1,2),s.Rational(3,5))==ppoly.count_roots(s.Rational(lo.numerator,lo.denominator),s.Rational(hi.numerator,hi.denominator))==1,'independent whole/root-bracket counts')
    def evaluate(q):return Fraction(ppoly.eval(s.Rational(q.numerator,q.denominator)))
    sl,sh=evaluate(lo),evaluate(hi);need(sl*sh<0,'independent root endpoint signs')
    for _ in range(160):
        mid=(lo+hi)/2;sm=evaluate(mid);need(sm!=0,'independent nonrational midpoint')
        if sm*sl>0:lo,sl=mid,sm
        else:hi,sh=mid,sm
    f=Algebra(p,lo,hi)
    u=[cc-alpha/beta*nn for cc,nn in zip(c,n)]
    U,V=[tuple(f.from_rat(q) for q in vector) for vector in (u,v)]
    kk=f.from_rat(k);need(f.dot(U,U)==f.dot(V,V)==f.one and f.dot(U,V)==kk,'independent physical ear Gram')
    normal=tuple(f.from_rat(q) for q in matvec(HI,cross(u,v)))
    bcross=cross(b[1],b[4]);branches={}
    for orientation in (-1,1):
        points={i:tuple(f.from_rat(q) for q in vector) for i,vector in a.items()}
        for j,vector in b.items():
            b1,b2=f.from_rat(dot(vector,b[1])),f.from_rat(dot(vector,b[4]))
            l=f.from_rat(DH*sum((x*y for x,y in zip(vector,bcross)),zero)/(1-k*k))
            points[j+8]=tuple(((b1-kk*b2)*uu+(b2-kk*b1)*vv)/(f.one-kk*kk)+orientation*l*nn for uu,vv,nn in zip(U,V,normal))
        need(all(f.dot(q,q)==f.one for q in points.values()),'independent full frame norms')
        branches[orientation]=points
    edges=A_EDGES|{(i+8,j+8) for i,j in B_EDGES}|{(2,9),(7,9),(5,12),(6,12)}
    need(all(f.dot(branches[sg][i],branches[sg][j])==f.t for sg in (-1,1) for i,j in edges),'independent24 contact identities')
    collision={sg:[(i,j) for i,j in combinations(range(13),2) if f.sign(f.dot(points[i],points[j])-f.t)>0] for sg,points in branches.items()}
    need(not collision[-1] and collision[1] and collision[1][0]==(0,11),'independent both-orientation packing classification')
    points=branches[-1];tetra=[0,1,4,8];chosen=[points[i] for i in tetra]
    weights=[(-1)**i*f.det([chosen[j] for j in range(4) if j!=i]) for i in range(4)]
    total=sum(weights,f.zero);weights=[q/total for q in weights]
    need(all(f.sign(q)>0 for q in weights) and sum(weights,f.zero)==f.one,'independent positive origin tetrahedron')
    need(all(sum((w*v[k] for w,v in zip(weights,chosen)),f.zero)==f.zero for k in range(3)),'independent origin relation')
    rows=[[(f.one-f.t)*p[i]+f.t*sum(p,f.zero) for i in range(3)] for p in (points[k] for k in range(13))]
    counts=[0,0,0];vertices=set();bound=f.number(Fraction(199,200))
    for triple in combinations(range(13),3):
        q=f.solve([rows[i] for i in triple],[f.t]*3)
        if q is None:counts[0]+=1;continue
        if any(f.sign(f.dot(points[i],q)-f.t)>0 for i in range(13)):counts[1]+=1;continue
        need(f.sign(f.dot(q,q)-bound)<0,'independent strict norm bound')
        counts[2]+=1;vertices.add(q)
    need(counts==[0,262,24] and len(vertices)==21,'independent complete286 vertex cover')
    for v,w in combinations(vertices,2):
        need(any(f.sign(x-y)!=0 for x,y in zip(v,w)),'independent actual vertex distinctness')
    return {'version':1,'root_polynomial':p,'root_bracket':[[2196767,3802339],[535329,926590]],'origin_tetrahedron':tetra,'rejected_orientation':1,'collision_pair':list(collision[1][0]),'norm_squared_bound':[199,200]}

if __name__=='__main__':print(json.dumps(generate(),indent=2,sort_keys=True))
