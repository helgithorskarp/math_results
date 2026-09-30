"""Exact univariate necessary-constraint and Cramer kernel over Q(sqrt(5))."""
from fractions import Fraction
import itertools
from math import comb
from q5 import Q,dot,cross,sub,scale
from model import VERTICES

ZERO=()
def poly(c):return (Q(c),) if c!=0 else ZERO
def trim(p):
    p=list(p)
    while p and p[-1]==0:p.pop()
    return tuple(p)
def padd(p,q):return trim([(p[i] if i<len(p) else Q())+(q[i] if i<len(q) else Q()) for i in range(max(len(p),len(q)))])
def pscale(c,p):return trim([c*x for x in p])
def psub(p,q):return padd(p,pscale(-1,q))
def pmul(p,q):
    if not p or not q:return ZERO
    r=[Q()]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):r[i+j]=r[i+j]+a*b
    return trim(r)
def peval(p,t):
    r=Q()
    for c in reversed(p):r=r*t+c
    return r
def pdot(a,b):
    p=ZERO
    for x,y in zip(a,b):p=padd(p,pmul(x,y))
    return p
def pdiv(p,q):
    if not q:raise ValueError('Zero polynomial divisor')
    out=[Q()]*max(0,len(p)-len(q)+1);r=p
    while len(r)>=len(q):
        k=len(r)-len(q);c=r[-1]/q[-1];out[k]=c
        r=psub(r,(Q(),)*k+pscale(c,q))
    return trim(out),r
def pgcd(p,q):
    while q:_,r=pdiv(p,q);p,q=q,r
    return pscale(1/p[-1],p) if p else ZERO
def determinant(matrix):
    n=len(matrix);r=ZERO
    for p in itertools.permutations(range(n)):
        v=poly(1)
        for i,j in enumerate(p):v=pmul(v,matrix[i][j])
        if sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))%2:v=pscale(-1,v)
        r=padd(r,v)
    return r
def bernstein(p,lo,hi):
    degree=max(0,len(p)-1);power=[Q()]*(degree+1)
    for j,c in enumerate(p):
        for i in range(j+1):power[i]=power[i]+c*comb(j,i)*qpower(lo,j-i)*qpower(hi-lo,i)
    return [sum((power[i]*Q(Fraction(comb(k,i),comb(degree,i))) for i in range(k+1)),Q()) for k in range(degree+1)]
def qpower(q,n):
    r=Q(1)
    for _ in range(n):r=r*q
    return r
def decode(v):return tuple(Q(*x) for x in v)
def encode(v):return [[str(x.a),str(x.b)] for x in v]
def solve(rows,rhs):
    n=len(rows[0]);m=[list(r)+[Q(y)] for r,y in zip(rows,rhs)];k=0;pivots=[]
    for j in range(n):
        i=next((i for i in range(k,len(m)) if m[i][j]!=0),None)
        if i is None:continue
        m[k],m[i]=m[i],m[k];v=m[k][j];m[k]=[x/v for x in m[k]]
        for i in range(len(m)):
            if i!=k:
                v=m[i][j];m[i]=[x-v*y for x,y in zip(m[i],m[k])]
        pivots.append(j);k+=1
    if k!=n or any(all(x==0 for x in r[:-1]) and r[-1]!=0 for r in m):raise ValueError('Not uniquely solvable')
    out=[Q()]*n
    for i,j in enumerate(pivots):out[j]=m[i][-1]
    return out

def family(case,parent):
    u=decode(case['direction']);N=dot(u,u);ds=[sub(v,u) for v in parent if v!=u]
    if len(ds)!=2:raise ValueError('Not a parent corner')
    rays=[decode(m)[:3] for m in case['extreme_motions']]
    a=tuple(trim((rays[1][k],rays[0][k]-rays[1][k])) for k in range(3));A2=pdot(a,a)
    rows=[];rhs=[];labels=[]
    def put(row,b,label):rows.append(tuple(row));rhs.append(b);labels.append(label)
    for x,y in sorted({tuple(c[:2]) for c in case['contacts']}):
        e=sub(VERTICES[y],VERTICES[x]);h=dot(cross(e,u),VERTICES[x]);m=scale(1/h,cross(e,u))
        for j,v in enumerate(VERTICES):
            if dot(m,v)==1:
                r=[poly(dot(scale(1/h,cross(e,d)),sub(v,VERTICES[x]))) for d in ds]
                put(r+[ZERO,ZERO,ZERO],pscale(-2,pdot(a,tuple(poly(x) for x in cross(v,m)))),['hidden',x,y,j])
    for x,y,j in case['contacts']:
        v=VERTICES[j];e=sub(VERTICES[y],VERTICES[x]);h=dot(cross(e,u),v);m=scale(1/h,cross(e,u));g=cross(v,m)
        if cross(g,u)!=(Q(),Q(),Q()):continue
        r=[pdot(a,tuple(poly(x) for x in cross(v,scale(1/h,cross(e,d))))) for d in ds]
        b=psub(A2,pmul(pdot(a,tuple(poly(x) for x in v)),pdot(a,tuple(poly(x) for x in m))))
        put(r+[poly(dot(g,u)),poly(m[0]),poly(m[2])],b,['persistent2',x,y,j])
    for j in (9,14,54):
        v=VERTICES[j]
        if dot(u,v)!=0:raise ValueError('Invalid mirror-plane fixed vertex')
        torque=pdot(a,tuple(poly(x) for x in cross(v,u)))
        r=[pscale(-dot(v,d)/N,torque) for d in ds];av=pdot(a,tuple(poly(x) for x in v))
        put(r+[ZERO,poly(v[0]),poly(v[2])],psub(pscale(dot(v,v),A2),pmul(av,av)),['radial2',j])
    for k in range(2):put([poly(-int(j==k)) for j in range(5)],ZERO,['receiver_cone',k])
    basis=[ds[0],ds[1],scale(-1,u)];matrix=list(map(list,zip(*basis)))
    r1=solve(matrix,cross(rays[1],u));r0=solve(matrix,cross(rays[0],u))
    mirror=tuple(trim((r1[k],r0[k]-r1[k])) for k in range(2))+(ZERO,ZERO,ZERO)
    tight=[i for i,(r,b) in enumerate(zip(rows,rhs)) if pdot(r,mirror)==b]
    return rows,rhs,labels,mirror,tight

def cramer(rows,ids,coordinates,target):
    n=len(ids);matrix=[[rows[i][k] for i in ids] for k in coordinates];den=determinant(matrix);nums=[]
    if not den:raise ValueError('Identically singular basis')
    for j in range(n):
        m=[list(r) for r in matrix]
        for k,c in enumerate(coordinates):m[k][j]=poly(target[c])
        nums.append(determinant(m))
    common=den
    for num in nums:common=pgcd(common,num)
    if len(common)>1:
        den,rem=pdiv(den,common)
        if rem:raise ValueError('Incorrect determinant cancellation')
        reduced=[]
        for num in nums:
            q,rem=pdiv(num,common)
            if rem:raise ValueError('Incorrect numerator cancellation')
            reduced.append(q)
        nums=reduced
    for k in range(5):
        if pdot(nums,[rows[i][k] for i in ids])!=pscale(target[k],den):raise ValueError('Full Cramer identity fails')
    return den,nums
