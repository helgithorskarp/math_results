"""Exact construction and general colour-domain search (producer only)."""
from fractions import Fraction as F
from itertools import combinations
from math import gcd

RAD=(1,3,5,7,15,21,35,105)
def real(r=1,c=0):return tuple(F(c) if d==r else F(0) for d in RAD)
ZERO=real();ONE=real(1,1)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(a,k):return tuple(k*x for x in a)
def mul(a,b):
    out=[F(0)]*8
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:
                    d=gcd(RAD[i],RAD[j])
                    out[RAD.index(RAD[i]*RAD[j]//(d*d))]+=x*y*d
    return tuple(out)
def padd(a,b):return add(a[0],b[0]),add(a[1],b[1])
def pscale(a,k):return scale(a[0],k),scale(a[1],k)
def sub(a,b):return padd(a,pscale(b,-1))
def norm(a):return add(mul(a[0],a[0]),mul(a[1],a[1]))
def iroot3(a):return scale(mul(real(3,1),a[1]),-1),mul(real(3,1),a[0])
def cell():
    p=[(real(1,F(-1,2)),ZERO),(real(1,F(1,2)),ZERO),
       (real(1,F(3,4)),real(15,F(1,4))),
       (ZERO,add(real(15,F(1,4)),real(7,F(1,4)))),
       (real(1,F(-3,4)),real(15,F(1,4)))]
    for a,b in ((2,3),(4,0)):
        for s in (1,-1):
            p.append(pscale(padd(padd(p[a],p[b]),pscale(iroot3(sub(p[b],p[a])),s)),F(1,2)))
    return p
def construction():
    p=cell()
    return p+[pscale(x,-1) for x in p if pscale(x,-1) not in p]
def edges(p):
    return [(i,j) for i,j in combinations(range(len(p)),2) if norm(sub(p[i],p[j]))==ONE]
def patterns(n):
    def grow(w):
        if len(w)==n:yield w;return
        for c in range(min(3,max(w,default=-1)+1)+1):yield from grow(w+(c,))
    return grow(())
def solve(n,e,pins=(),colours=4):
    adj=[set() for _ in range(n)]
    for a,b in e:adj[a].add(b);adj[b].add(a)
    domains=[(1<<colours)-1]*n
    for v,c in pins:domains[v]&=1<<c
    def visit(dom):
        if 0 in dom:return None
        queue=[v for v,d in enumerate(dom) if d&(d-1)==0];done=set()
        while queue:
            v=queue.pop()
            if v in done:continue
            done.add(v)
            for u in sorted(adj[v]):
                d=dom[u]&~dom[v]
                if d!=dom[u]:
                    if not d:return None
                    dom[u]=d
                    if d&(d-1)==0:queue.append(u)
        pending=[v for v,d in enumerate(dom) if d&(d-1)]
        if not pending:return ''.join(str(d.bit_length()-1) for d in dom)
        v=min(pending,key=lambda v:(dom[v].bit_count(),-len(adj[v]),v))
        for c in range(colours):
            if dom[v]&(1<<c):
                child=dom.copy();child[v]=1<<c
                ans=visit(child)
                if ans is not None:return ans
        return None
    return visit(domains)
