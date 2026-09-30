#!/usr/bin/env python3
"""Optional SymPy1.14 independent arithmetic and noncrossing certificate generator.

Reads no certificate, expected output, coordinates, scratch file or network.
Only the mathematical reflection, Gram and Bernstein formulas are shared.
"""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from math import comb
import json
import sympy as s
from sympy.polys.fields import field

def need(p,message):
    if not p:raise ValueError(message)

K,t=field('t',s.QQ)
one,zero=K.one,K.zero
H=[[one if i==j else t for j in range(3)] for i in range(3)]
HI=[[((1/(1-t)) if i==j else zero)-t/((1-t)*(1+2*t)) for j in range(3)] for i in range(3)]
DH=(1-t)**2*(1+2*t)

def dot(x,y):
    return sum((x[i]*H[i][j]*y[j] for i in range(3) for j in range(3)),zero)

def cross(x,y):
    return [x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0]]

def p_sign(p):
    if not p:return 0
    degree=p.degree()
    coeff=[Fraction(int(c.numerator),int(c.denominator)) for k in range(degree+1)
           for c in (p.get((k,),0),)]
    lo,step=Fraction(1,2),Fraction(1,10)
    affine=[sum(coeff[j]*comb(j,k)*lo**(j-k)*step**k for j in range(k,degree+1)) for k in range(degree+1)]
    bs=[sum(affine[k]*Fraction(comb(i,k),comb(degree,k)) for k in range(i+1)) for i in range(degree+1)]
    if all(x>=0 for x in bs) and any(x>0 for x in bs):return 1
    if all(x<=0 for x in bs) and any(x<0 for x in bs):return -1
    return 0

@lru_cache(None)
def sign(r):
    return p_sign(r.numer)*p_sign(r.denom)

def dihedral(n):
    return [tuple((shift+direction*i)%n for i in range(n)) for shift in range(n) for direction in (-1,1)]

def image(e,p):return frozenset(tuple(sorted((p[i],p[j]))) for i,j in e)
def mask(e,n):return sum(1<<k for k,p in enumerate(combinations(range(n),2)) if p in e)
def neighbors(e,n):return {i:{j for u,v in e for j in ((v,) if u==i else (u,) if v==i else ())} for i in range(n)}

def catalog(n):
    boundary=frozenset((i,i+1) for i in range(n-1))|{(0,n-1)}
    diagonals=[p for p in combinations(range(n),2) if p not in boundary]
    def crosses(p,q):
        a,b=p;c,d=q
        return a<c<b<d or c<a<d<b
    all_edges={boundary|frozenset(ds) for ds in combinations(diagonals,n-3)
               if not any(crosses(p,q) for p,q in combinations(ds,2))}
    eligible={e for e in all_edges if max(Counter(i for pair in e for i in pair).values())<=5}
    keys={}
    for e in sorted(eligible,key=lambda e:mask(e,n)):
        keys.setdefault(min(mask(image(e,p),n) for p in dihedral(n)),e)
    return list(e for _,e in sorted(keys.items()))

def coordinates(e,n):
    active=set(range(n));removed=[]
    while len(active)>3:
        nb={i:{j for j in active if i!=j and tuple(sorted((i,j))) in e} for i in active}
        v=min(i for i in active if len(nb[i])==2)
        i,j=sorted(nb[v]);old=(nb[i]&nb[j])-{v}
        need(len(old)==1,'unique old triangle')
        removed.append((v,i,j,next(iter(old))));active.remove(v)
    points={v:[one if k==h else zero for k in range(3)] for h,v in enumerate(sorted(active))}
    for v,i,j,old in reversed(removed):
        points[v]=[2*t/(1+t)*(x+y)-z for x,y,z in zip(points[i],points[j],points[old])]
    need(all(dot(x,x)==one for x in points.values()),'independent A unit norms')
    need(all(dot(points[i],points[j])==t for i,j in e),'independent A contact equations')
    return points

def frame(a,i,j):
    w=dot(a[i],a[j]);need(sign(1+w)==sign(1-w)==1,'independent pair rank')
    c=[t/(1+w)*(x+y) for x,y in zip(a[i],a[j])]
    raw=cross(a[i],a[j]);normal=[sum((x*y for x,y in zip(row,raw)),zero) for row in HI]
    delta=DH*(1+w-2*t*t)/((1+w)**2*(1-w))
    need(dot(c,normal)==zero,'independent normal')
    need(dot(c,a[i])==dot(c,a[j])==t,'independent center equations')
    need(dot(normal,a[i])==dot(normal,a[j])==zero,'independent contact nullspace')
    need(dot(normal,normal)==(1-w*w)/DH,'independent normal length')
    need(dot(c,c)+delta*dot(normal,normal)==one,'independent sphere identity')
    return c,normal,delta

def gaps(a,c,normal,delta,k):
    alpha=dot(c,a[k])-t;beta=dot(normal,a[k])
    return alpha,beta,alpha*alpha-delta*beta*beta

def generate():
    blocked=[];exceptions=[];counts=[];grams=set()
    for n in (5,6,7,8):
        reps=catalog(n);count=[0,0,0]
        for ai,e in enumerate(reps):
            a=coordinates(e,n);nb=neighbors(e,n)
            for i,j in combinations(range(n),2):
                if nb[i]&nb[j] or max(len(nb[i]),len(nb[j]))>4:continue
                w=dot(a[i],a[j]);grams.add(w)
                if sign(2*t*t-1-w)==1:
                    count[0]+=1;continue
                c,normal,delta=frame(a,i,j)
                tests={k:gaps(a,c,normal,delta,k) for k in range(n) if k not in (i,j)}
                witnesses=[k for k,(alpha,_,square) in tests.items() if sign(alpha)==sign(square)==1]
                if witnesses:
                    k=min(witnesses)
                    alpha,_,square=tests[k]
                    q4=49*t**4+44*t**3+14*t*t+4*t+1
                    q5=49*t**5-3*t**4-22*t**3+2*t*t+5*t+1
                    need(alpha==16*t**4*(1-t)*(2*t+1)/q5,'independent shared alpha')
                    need(square==16*t*t*(1-t)**2*(1+t)**2*(2*t+1)**2*(3*t+1)*(5*t*t-1)/(q4*q5),'independent shared square')
                    blocked.append([n,ai,i,j,k]);count[1]+=1;continue
                need(sign(delta)==1,'independent exceptional reality')
                need(all(sign(t-dot(a[u],a[v]))==1 for u,v in combinations(range(n),2) if (u,v) not in e),'independent exceptional A packing')
                compatible=[]
                for orientation in (-1,1):
                    if all(sign(alpha)==-1 and (not beta or sign(orientation*beta)==-1 or
                                                sign(orientation*beta)==sign(square)==1)
                           for alpha,beta,square in tests.values()):
                        compatible.append(orientation)
                need(len(compatible)==1,'independent exceptional position count')
                orientation=compatible[0]
                rejected=[k for k,(alpha,beta,square) in tests.items() if sign(alpha)==-1 and sign(-orientation*beta)==1 and sign(square)==-1]
                need(rejected,'independent opposite-position violation')
                exceptions.append({'n':n,'type':ai,'pair':[i,j],'orientation':orientation,'rejected_witness':min(rejected)})
                count[2]+=1
        counts.append(count)
    need(counts==[[0,0,0],[1,0,0],[5,1,0],[24,7,1]] and len(grams)==7,'independent complete pair counts')
    need(len(blocked)==8 and len(exceptions)==1,'independent certificate coverage')
    return {'version':1,'blocked':blocked,'exception':exceptions[0]}

if __name__=='__main__':
    print(json.dumps(generate(),indent=2,sort_keys=True))
