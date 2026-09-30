"""Exact two-cell separation obstruction from a normalized monomial bound.

The five variables represent t,u,v,U,V, all normalized to [-1,1].
The chord formula requires p=R(u,v)R(U,V)-2[(1+t)|z-Z|^2+
2t(u-U)(v-V)]<=0 for a separated pair. If its constant coefficient
exceeds the sum of absolute values of all other coefficients, p>0
uniformly, so the two cells are incompatible.
"""
from fractions import Fraction as Q
from itertools import product

N=5;ZERO=(0,)*N
def constant(v):return {} if not v else {ZERO:Q(v)}
def add(p,q):
    result=p.copy()
    for k,v in q.items():result[k]=result.get(k,Q(0))+v
    return {k:v for k,v in result.items() if v}
def scale(p,v):return {k:c*v for k,c in p.items() if c*v}
def sub(p,q):return add(p,scale(q,-1))
def mul(p,q):
    result={}
    for a,c in p.items():
        for b,d in q.items():
            k=tuple(x+y for x,y in zip(a,b));result[k]=result.get(k,Q(0))+c*d
    return {k:v for k,v in result.items() if v}
def variable(i,center,half):
    exponent=list(ZERO);exponent[i]=1
    return add(constant(center),{tuple(exponent):half})
def polynomial(left,right,lo,hi):
    if not Q(1,2)<lo<=hi<Q(3,5):raise ValueError('parameter domain')
    t=variable(0,(lo+hi)/2,(hi-lo)/2);uv=[];Rs=[]
    g0=sub(constant(1),mul(t,t));g1=sub(t,mul(t,t))
    for k,cell in enumerate((left,right)):
        if len(cell)!=3 or any(type(x) is not int for x in cell):raise ValueError('cell integers')
        d,i,j=cell
        if not 0<=d<=12 or not 0<=i<2**d or not 0<=j<2**d:raise ValueError('cell bounds')
        h=Q(8,2**d)
        u=variable(1+2*k,-4+h*(Q(i)+Q(1,2)),h/2)
        v=variable(2+2*k,-4+h*(Q(j)+Q(1,2)),h/2);uv.append((u,v))
        Rs.append(add(constant(1),add(mul(g0,add(mul(u,u),mul(v,v))),scale(mul(g1,mul(u,v)),2))))
    du=sub(uv[0][0],uv[1][0]);dv=sub(uv[0][1],uv[1][1])
    distance=add(mul(add(constant(1),t),add(mul(du,du),mul(dv,dv))),scale(mul(t,mul(du,dv)),2))
    return sub(mul(Rs[0],Rs[1]),scale(distance,2))
def lower_bound(left,right,lo,hi):
    p=polynomial(left,right,lo,hi)
    return p.get(ZERO,Q(0))-sum(abs(v) for k,v in p.items() if k!=ZERO)

