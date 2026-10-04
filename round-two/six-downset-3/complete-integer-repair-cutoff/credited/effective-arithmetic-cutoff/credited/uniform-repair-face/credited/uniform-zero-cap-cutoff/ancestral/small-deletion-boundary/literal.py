"""Standalone affine table and literal domain for the finite duals.

Standard library only. The two coefficients of every table entry are
expanded directly from the credited table, independently of its evaluator.
No author matrix, sector decoder, elimination routine, or search is imported.
"""
from fractions import Fraction as F
from itertools import combinations


def require(ok, message):
    if not ok:
        raise ValueError(message)


def table(q):
    require(type(q) is int and q >= 4, 'literal integer q>=4 required')
    q = F(q); s = 3*q+4; h = 1/(3*q+5)
    o,p,a,b,c,d,e = (0,1),(0,2),(1,0),(1,1),(2,0),(2,1),(3,0)
    out = {}
    def put(x,y,base,slope=F(0)):
        out[tuple(sorted((x,y)))] = (F(base),F(slope))
    put(o,o,(6/q-q-4)/(q-1),1/(q-1))
    put(o,p,q*(q-3)/((q-1)*(q-2)))
    den=(q-2)*(q-3)/2
    put(p,p,(6/q+2*q/(q-1)-s+q*(q-1)/2)/den,
        (1-6*h*(q+1)/(q*(q-1)))/den)
    for leaf,alpha,beta,gamma in (
        (o,(1-1/q,0),(1+1/q,0),(1+6/q,0)),
        (p,(1,2*h/(q*(q-1))),
         (1+2*(q-1)/(q*(q-2)),2*h/((q-1)*(q-2))),
         (1+6/q,-6*h*(q+1)/(q*(q-1))))):
        for core,value in ((a,alpha),(c,alpha),(b,beta),(d,beta),(e,gamma)):
            put(leaf,core,*value)
    rr=3+2/q; ww=(s-rr)/(q-1)
    for x,y,value in ((a,a,0),(a,b,0),(b,b,0),(a,c,2),(a,d,rr),(b,c,rr),(b,d,ww)):
        put(x,y,value)
    return out


def member(q,k,A):
    require(type(A) is int and 0 <= A and A.bit_length() <= q+3, 'invalid original bitmask')
    size=A.bit_count(); core=(A&7).bit_count(); outside=A>>3
    return (size<=2 or size==3 and core>=2) and not (
        A&7==6 and outside.bit_count()==1 and outside.bit_length()<=k)


def domain(q,k,scan=False):
    require(type(q) is int and type(k) is int and 4<=q<=11 and k in (2,3),
            'finite q4..11,k2/3 guard')
    if scan:
        return [A for A in range(1<<(q+3)) if member(q,k,A)]
    return [0]+sorted(sum(1<<i for i in pts)
        for size in (1,2,3) for pts in combinations(range(q+3),size)
        if member(q,k,sum(1<<i for i in pts)))


def typ(A):
    return (A&7).bit_count(),(A>>3).bit_count()


def core_data(q,k,scan=False):
    X=domain(q,k,scan); N=len(X); n=N-1; s=3*q+4
    require(N==(q*q+13*q+16)//2-k and N<=137,'original dimension and guard')
    w=table(q); C0=[]; delta=[]
    for A in X[1:]:
        row=[];der=[]
        for B in X[1:]:
            if A==B: x,d=F(s-1),F(0)
            elif A&B: x,d=F(-1),F(0)
            else:
                x,d=w[tuple(sorted((typ(A),typ(B))))];x-=1
            row.append(x);der.append(d)
        C0.append(row);delta.append(der)
    R=[[F(0)]*n for _ in range(n)]; ix={A:i for i,A in enumerate(X[1:])}
    for A,B,value in ((1,2,1),(1,4,1),(2,5,-1),(4,3,-1)):
        i,j=ix[A],ix[B]; R[i][j]=R[j][i]=F(value)
    U0=[[F(N*int(i==j)-1)-C0[i][j] for j in range(n)] for i in range(n)]
    return X,N,s,C0,delta,R,U0


def quadratic(w,A):
    return sum(w[i]*A[i][j]*w[j] for i in range(len(w)) for j in range(len(w)))


def action(A,w):
    return [sum(x*y for x,y in zip(row,w)) for row in A]
