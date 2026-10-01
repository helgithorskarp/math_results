"""Five-coefficient exact arithmetic at the bracketed Tammes incumbent root."""
from fractions import Fraction as Q
from itertools import permutations

F=tuple(map(Q,(-1,-3,2,6,-1,13)))
ZERO=(Q(0),)*5
ONE=(Q(1),)+ZERO[1:]
T=(Q(0),Q(1),Q(0),Q(0),Q(0))
LO=Q('0.59260590292507377809642492233275')
HI=Q('0.59260590292507377809642492233276')

def require(ok,message):
    if not ok:raise ValueError(message)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def scale(a,q):return tuple(x*q for x in a)
def scalar(q):return (Q(q),)+ZERO[1:]
def reduce(p):
    p=list(p)
    for k in range(len(p)-1,4,-1):
        c=p[k]/F[5]
        for j in range(6):p[k-5+j]-=c*F[j]
    return tuple((p+[Q(0)]*5)[:5])
def mul(a,b):
    p=[Q(0)]*9
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y:p[i+j]+=x*y
    return reduce(p)
def sum_field(values):
    s=ZERO
    for v in values:s=add(s,v)
    return s
def dot(x,y):return sum_field(mul(a,b) for a,b in zip(x,y))
def matvec(M,v):return tuple(dot(row,v) for row in M)
def det(M):
    require(len(M)==3 and all(len(row)==3 for row in M),'three by three determinant')
    s=ZERO
    for p in permutations(range(3)):
        z=ONE
        for i in range(3):z=mul(z,M[i][p[i]])
        inv=sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
        s=add(s,scale(z,(-1)**inv))
    return s
def imul(a,b):
    z=[x*y for x in a for y in b]
    return min(z),max(z)
def interval(p):
    out=(Q(0),Q(0))
    for c in reversed(p):
        x,y=imul(out,(LO,HI));out=(x+c,y+c)
    return out
def sign(p):
    if p==ZERO:return 0
    lo,hi=interval(p)
    if lo>0:return 1
    if hi<0:return -1
    raise ValueError('unresolved exact sign in fixed root bracket')
def evaluate(p,t):
    out=Q(0)
    for c in reversed(p):out=out*t+c
    return out
def inverse(p):
    require(sign(p)!=0,'nonzero divisor at the real root')
    cols=[mul(p,tuple(Q(i==j) for i in range(5))) for j in range(5)]
    A=[[cols[j][i] for j in range(5)]+[Q(i==0)] for i in range(5)]
    for i in range(5):
        pivot=next((j for j in range(i,5) if A[j][i]),None)
        require(pivot is not None,'invertible coefficient multiplication matrix')
        A[i],A[pivot]=A[pivot],A[i]
        d=A[i][i];A[i]=[x/d for x in A[i]]
        for j in range(5):
            if j!=i:
                d=A[j][i];A[j]=[x-d*y for x,y in zip(A[j],A[i])]
    out=tuple(row[-1] for row in A)
    require(mul(p,out)==ONE,'exact inverse identity')
    return out
def readpoly(p):
    require(isinstance(p,list) and len(p)==5,'five field coefficients')
    return tuple(Q(x) for x in p)
