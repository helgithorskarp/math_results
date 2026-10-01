"""Validated curve differentiation and mean-value enclosures.
Actual author six-tammes-2, researcher; no floating input.
"""
from pathlib import Path
import sys
from math import isqrt,comb
from dependency import e
I,Q,S=e.I,e.Q,e.S
class D:
    radius=Q(0)
    def __init__(self,v=0,d=0,c=None):
        self.v,self.d=I.cv(v),I.cv(d)
        self.c=self.v if c is None else I.cv(c)
        if D.radius:
            bound=max(abs(self.d.l),abs(self.d.h))
            error=I.raw(-bound,bound)*I(D.radius)
            self.v=intersect(self.v,self.c+error)
    @staticmethod
    def cv(x):return x if isinstance(x,D) else D(x)
    def __add__(self,x):
        x=D.cv(x);return D(self.v+x.v,self.d+x.d,self.c+x.c)
    __radd__=__add__
    def __neg__(self):return D(-self.v,-self.d,-self.c)
    def __sub__(self,x):return self+-D.cv(x)
    def __rsub__(self,x):return D.cv(x)+-self
    def __mul__(self,x):
        x=D.cv(x);return D(self.v*x.v,self.d*x.v+self.v*x.d,self.c*x.c)
    __rmul__=__mul__
    def __truediv__(self,x):
        x=D.cv(x);return D(self.v/x.v,(self.d*x.v-self.v*x.d)/(x.v*x.v),self.c/x.c)
    def __rtruediv__(self,x):return D.cv(x)/self
    def __pow__(self,n):
        e.require(type(n)is int and n>=0,'nonnegative power');r=D(1)
        for _ in range(n):r=r*self
        return r
    def sqrt(self):
        if self.v.l<=0:raise ArithmeticError('strict square-root argument unresolved')
        l=isqrt(self.v.l*S);h=isqrt(self.v.h*S)
        if h*h<self.v.h*S:h+=1
        v=I.raw(l,h)
        cl=isqrt(self.c.l*S);ch=isqrt(self.c.h*S)
        if ch*ch<self.c.h*S:ch+=1
        return D(v,self.d/(2*v),I.raw(cl,ch))
def mv(A,x):return [sum((a*b for a,b in zip(row,x)),D()) for row in A]
def dot(a,b,H):return sum((a[i]*H[i][j]*b[j] for i in range(3) for j in range(3)),D())
def cross(a,b):return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]
def det(A):
    return A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1])-A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0])+A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0])
def solve(A,z):
    de=det(A)
    return [det([[z[i] if j==a else A[i][j] for j in range(3)] for i in range(3)])/de for a in range(3)]
def refine_unit_derivative(point,others,products,H):
    # Differentiate norm=1 and the two exact prescribed products.  The
    # three independent normals determine the same derivative uniquely.
    hv=[[z.v for z in row] for row in H];hd=[[z.d for z in row] for row in H]
    value=[z.v for z in point]
    A=[e.mv(hv,[z.v for z in vector]) for vector in (point,*others)]
    rhs=[-e.dot(value,value,hd)/2]
    for vector,product in zip(others,products):
        rhs.append(product.d-e.dot([z.d for z in vector],value,hv)
                   -e.dot([z.v for z in vector],value,hd))
    derivative=e.solve(A,rhs)
    return [D(z.v,intersect(z.d,d),z.c) for z,d in zip(point,derivative)]
def refined_solve(A,z):
    x=solve(A,z)
    rhs=[r.d-sum((a.d*b.v for a,b in zip(row,x)),I()) for row,r in zip(A,z)]
    derivative=e.solve([[a.v for a in row] for row in A],rhs)
    return [D(a.v,intersect(a.d,d),a.c) for a,d in zip(x,derivative)]
def build(t,q):
    H=[[D(1) if i==j else t for j in range(3)] for i in range(3)]
    HI=[[(1/(1-t) if i==j else 0)-t/((1-t)*(1+2*t)) for j in range(3)] for i in range(3)]
    de=(1-t)**2*(1+2*t);r=2*t/(1+t)
    k=t*(9*t*t-2*t-3)/(1+t)**2;gamma=k/(1+k)
    mu=(t-1)*(t+1)*(2*t+1)*(3*t-1)/(9*t**3-t*t-t+1)
    B={i:[D(1 if j==s else 0) for j in range(3)] for s,i in enumerate((1,2,4))}
    for n,i,j,o in ((8,2,4,1),(10,1,2,4),(12,1,10,2),(13,2,8,4)):
        B[n]=[r*(a+b)-c for a,b,c in zip(B[i],B[j],B[o])]
    d=mv(HI,cross(B[8],B[2]));x=1/q;L=1+de*x*x
    alpha=(de*x*x-1)/L;beta=2*de*x/L
    U=[t*a+alpha*(b-t*a)+beta*c for a,b,c in zip(B[8],B[2],d)]
    # The selected original V has positive orientation at t=117/200.
    # Its two-product Gram determinant stays positive on the covered domain,
    # so continuity identifies this same square-root branch everywhere.
    s=dot(U,B[10],H)
    gram=1-s*s-k*k-t*t+2*s*k*t
    radical=(de*gram).sqrt()
    normal=mv(HI,cross(U,B[10]))
    V=[((k-s*t)*u+(t-s*k)*v+radical*n)/(1-s*s)
       for u,v,n in zip(U,B[10],normal)]
    V=refine_unit_derivative(V,(U,B[10]),(k,t),H)
    W=[gamma*(u+v)-mu*c for u,v,c in zip(U,V,mv(HI,cross(U,V)))]
    W=refine_unit_derivative(W,(U,V),(k,k),H)
    P=dict(B);den=(2*r-1)*(r+1)
    for label,coeffs in ((0,(r,r,1-r)),(5,(1-r,r,r)),(11,(r,1-r,r))):
        P[label]=[sum((a*v[i] for a,v in zip(coeffs,(U,W,V))),D())/den for i in range(3)]
    P.update({6:U,7:W,9:V})
    return P,H
def bivariate(table,left,right,a,b):
    # Two successive exact power-to-Bernstein transforms bound the rectangle.
    degree=max(len(row) for row in table)-1
    tr=[]
    for row in table:
        row=tuple(row)+(0,)*(degree+1-len(row))
        tr.append(e.bernstein(row,left,right))
    coeffs=[]
    for j in range(degree+1):coeffs.extend(e.bernstein([row[j] for row in tr],a,b))
    return I(min(coeffs),max(coeffs))
TABLE=e.data['-1']['factors'][0]['table']
AT=[[j*c for j,c in enumerate(row) if j] for row in TABLE]
AQ=[[i*c for c in row] for i,row in enumerate(TABLE) if i]
def tangent(left,right,a,b):
    return -bivariate(AT,left,right,a,b)/bivariate(AQ,left,right,a,b)
def diagonal_table(table,mid,qcenter,slope):
    # Exact substitution t=mid+h, q=qcenter+slope*h+z.  Rows index z.
    maxh=max(i+len(row)-1 for i,row in enumerate(table))
    result=[[Q(0)]*(maxh+1) for _ in table]
    tpower=[[Q(comb(j,k))*mid**(j-k) for k in range(j+1)]
            for j in range(max(len(row) for row in table))]
    qpower=[[Q(comb(j,k))*qcenter**(j-k)*slope**k for k in range(j+1)]
            for j in range(len(table))]
    for i,row in enumerate(table):
        for j,value in enumerate(row):
            if not value:continue
            for z in range(i+1):
                coefficient=value*comb(i,z)
                for th,tc in enumerate(tpower[j]):
                    for qh,qc in enumerate(qpower[i-z]):
                        result[z][th+qh]+=coefficient*tc*qc
    return result
def tangent_refined(left,right,a,b,mid_a,mid_b):
    result=tangent(left,right,a,b)
    mid=(left+right)/2;radius=(right-left)/2
    center_tangent=tangent(mid,mid,mid_a,mid_b)
    slope=Q(round(Q(center_tangent.l+center_tangent.h,2*S)*10**6),10**6)
    qcenter=(mid_a+mid_b)/2
    at=diagonal_table(AT,mid,qcenter,slope)
    aq=diagonal_table(AQ,mid,qcenter,slope)
    for _ in range(2):
        error=(mid_b-mid_a)/2+radius*max(abs(x-slope) for x in result.fractions())
        narrower=-bivariate(at,-radius,radius,-error,error)/bivariate(aq,-radius,radius,-error,error)
        result=intersect(result,narrower)
    return result
def extension(P,H):
    X=[refined_solve([mv(H,P[i]) for i in tri],[H[0][1]]*3) for tri in ((0,4,6),(0,4,7),(1,4,7))]
    n=[X[0][j]+X[1][j]+Q(4,5)*X[2][j] for j in range(3)]
    rows={i:mv(H,p) for i,p in P.items()};rows['cut']=mv(H,n)
    return n,rows
def mean_value(center,derivative,radius):
    bound=max(abs(derivative.l),abs(derivative.h))
    error=I.raw(-bound,bound)*I(radius)
    return center+error
def intersect(a,b):
    lo,hi=max(a.l,b.l),min(a.h,b.h)
    e.require(lo<=hi,'valid interval intersection')
    return I.raw(lo,hi)
def recondition(value,center,radius):
    # Both enclosures contain the same differentiable curve value.  Retain
    # the independently enclosed derivative after narrowing only the value.
    return D(intersect(value.v,mean_value(center.v,value.d,radius)),value.d,value.c)
def enclosed_model(left,right,a,b,mid_a,mid_b):
    mid=(left+right)/2;radius=(right-left)/2
    D.radius=radius
    qp=tangent_refined(left,right,a,b,mid_a,mid_b)
    P,H=build(D(I(left,right),1,I(mid)),D(I(a,b),qp,I(mid_a,mid_b)))
    P0,H0=build(D(I(mid)),D(I(mid_a,mid_b)))
    P={i:[recondition(w,z,radius) for w,z in zip(p,P0[i])] for i,p in P.items()}
    n,_=extension(P,H)
    n0,rows0=extension(P0,H0)
    n=[recondition(w,z,radius) for z,w in zip(n0,n)]
    nn=recondition(dot(n,n,H),dot(n0,n0,H0),radius)
    length=nn.sqrt();length0=dot(n0,n0,H0).sqrt()
    rows={i:mv(H,p) for i,p in P.items()};rows['cut']=mv(H,n)
    rows0={i:mv(H0,p) for i,p in P0.items()};rows0['cut']=mv(H0,n0)
    rows={i:[recondition(w,z,radius) for z,w in zip(rows0[i],row)] for i,row in rows.items()}
    return {'P':P,'n':n,'rows':rows,'H':H,'P0':P0,'n0':n0,
            'rows0':rows0,'H0':H0,'qprime':qp,'radius':radius,'nn':nn,
            't':D(I(left,right),1,I(mid)),'t0':D(I(mid)),
            'length':length,'length0':length0}
def enclosed(left,right,a,b,mid_a,mid_b):
    model=enclosed_model(left,right,a,b,mid_a,mid_b)
    P,n,rows,H,qp=(model[k] for k in ('P','n','rows','H','qprime'))
    pack={i:[w.v for w in p] for i,p in P.items()}
    normal=[w.v for w in n]
    normals={i:[w.v for w in row] for i,row in rows.items()}
    return pack,normal,normals,[[I(1) if i==j else I(left,right) for j in range(3)] for i in range(3)],qp
