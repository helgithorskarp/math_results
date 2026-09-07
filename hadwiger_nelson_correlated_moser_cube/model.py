"""Exact integer coefficient contact census for M+uM+u^2M."""
from collections import defaultdict
from functools import reduce
from itertools import combinations, product
from math import gcd

M=[(0,0,0,0),(36,0,0,0),(18,0,18,0),(54,0,18,0),
   (30,0,0,2),(15,-3,15,1),(45,-3,15,3)]
Z=(0,0)
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def scale(a,n):return (n*a[0],n*a[1])
def mul(a,b):return (a[0]*b[0]+33*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def conjprod(a,b):
    x,y=a[:2],a[2:];v,w=b[:2],b[2:]
    return (add(mul(x,v),scale(mul(y,w),3)),sub(mul(y,v),mul(x,w)))
def norm(a):return conjprod(a,a)[0]
def canonical(p):
    p=list(p)
    while p and p[-1]==Z:p.pop()
    if not p:return ()
    a,b=p[-1];q=[mul(c,(a,-b))for c in p]
    g=reduce(gcd,(abs(v)for c in q for v in c))
    if q[-1][0]<0:g=-g
    return tuple((c[0]//g,c[1]//g)for c in q)
def contact(a,b,c,target):
    k=sub(add(add(norm(a),norm(b)),norm(c)),(1296*target,0))
    bx,by=conjprod(b,a);cx,cy=conjprod(c,b);hx,hy=add(bx,cx),add(by,cy)
    jx,jy=conjprod(c,a)
    return canonical([add(add(k,scale(hx,2)),scale(jx,2)),
        add(scale(hy,-12),scale(jy,-24)),add(scale(k,6),scale(jx,-36)),
        add(scale(hy,-36),scale(jy,72)),add(add(scale(k,9),scale(hx,-18)),scale(jx,18))])
def generate():
    addresses=list(product(range(7),repeat=3));delta={(i,j):tuple(a-b for a,b in zip(M[i],M[j]))for i in range(7)for j in range(7)}
    polys=defaultdict(list);zeros=defaultdict(list);generic=[];constant=0
    for v,w in combinations(range(343),2):
        a,b,c=(delta[i,j]for i,j in zip(addresses[v],addresses[w]))
        p=contact(a,b,c,1)
        if not p:generic.append([v,w])
        elif len(p)>1:polys[p].append([v,w])
        else:constant+=1
        q=contact(a,b,c,0)
        if len(q)>1:zeros[q].append([v,w])
    out={'M':M,'addresses':addresses,'generic_edges':generic,'constant_nonunit_pairs':constant,
         'contacts':[{'poly':p,'pairs':polys[p]}for p in sorted(polys)],
         'collision_norms':[{'poly':p,'pairs':zeros[p]}for p in sorted(zeros)]}
    return out
