"""Exact permutation bounds and complete trace generation; see proof.md."""
from math import factorial
from functools import lru_cache

def fall(n,k):
    return factorial(n)//factorial(n-k) if 0<=k<=n else 0

@lru_cache(maxsize=2000)
def coefficients(v,s,r=5,positions=None):
    N=v-s
    start=(v-s)//2
    positions=tuple(range(start,start+s)) if positions is None else tuple(positions)
    assert len(positions)==s and len(set(positions))==s
    assert all(0<=k<v for k in positions) and N>=r
    masks=range(1<<s)
    out=[]
    for k in range(v):
        left=sum(1<<i for i,p in enumerate(positions) if p<k)
        right=sum(1<<i for i,p in enumerate(positions) if p>k)
        L=k-left.bit_count();R=v-1-k-right.bit_count()
        marked=(1<<positions.index(k)) if k in positions else 0
        a1=[];a2=[];pairs=[]
        for A in masks:
            a=r-A.bit_count()
            if a<0:continue
            if marked:
                if A&marked and A&~(left|marked)==0:
                    a1.append((A,fall(L,a)*factorial(N-a)))
                if A&marked and A&~(right|marked)==0:
                    a2.append((A,fall(R,a)*factorial(N-a)))
            else:
                if a>=1 and A&~left==0:a1.append((A,fall(L,a-1)*a*factorial(N-a)))
                if a>=1 and A&~right==0:a2.append((A,fall(R,a-1)*a*factorial(N-a)))
        for A,_ in a1:
            for B,_ in a2:
                a=r-A.bit_count();b=r-B.bit_count()
                if marked:
                    if A&B!=marked or a+b>N:continue
                    c=fall(L,a)*fall(R,b)*factorial(N-a-b)
                else:
                    if A&B or a+b-1>N:continue
                    c=fall(L,a-1)*fall(R,b-1)*factorial(N-a-b+1)
                if c:pairs.append((A,B,c))
        out.append((a1,a2,pairs,marked,L,R))
    return factorial(N),out

CONFIGURATIONS = set()

def bound(v,counts,r=5,positions=None):
    s=(len(counts)-1).bit_length()
    assert len(counts)==1<<s and all(isinstance(x,int) and x>=0 for x in counts)
    assert v-s >= r
    CONFIGURATIONS.add((v,s,r,positions))
    den,cs=coefficients(v,s,r,positions)
    total=0
    for a,b,ps,marked,L,R in cs:
        x=sum(counts[A]*c for A,c in a)
        y=sum(counts[A]*c for A,c in b)
        z=sum(counts[A]*(counts[B]-(A==B))*c for A,B,c in ps)
        total+=min(x,y,z,den)
    return total,den

def profiles(v,m,s):
    # Ordered least-degree vertices; exact trace counts. Pair coverage necessary.
    lo=(v+2)//4
    if s==0:yield (m,);return
    if s==1:
        for d in range(lo,5*m//v+1):yield (m-d,d)
    if s==2:
        for a in range(lo,5*m//v+1):
            for b in range(a,(5*m-a)//(v-1)+1):
                for c in range(1,min(a,b)+1):
                    if m-a-b+c>=0:yield(m-a-b+c,a-c,b-c,c)
    if s==3:
        for a in range(lo,5*m//v+1):
            for b in range(a,(5*m-a)//(v-1)+1):
                for c in range(b,(5*m-a-b)//(v-2)+1):
                    for ab in range(1,min(a,b)+1):
                        for ac in range(1,min(a,c)+1):
                            for bc in range(1,min(b,c)+1):
                                for t in range(min(ab,ac,bc)+1):
                                    x=[0]*8
                                    x[7]=t;x[3]=ab-t;x[5]=ac-t;x[6]=bc-t
                                    x[1]=a-ab-ac+t;x[2]=b-ab-bc+t;x[4]=c-ac-bc+t;x[0]=m-sum(x)
                                    if min(x)<0:continue
                                    # Every marked vertex must cover all outside vertices.
                                    if any(sum(x[A]*(5-A.bit_count()) for A in range(8) if A>>i&1)<v-s for i in range(s)):continue
                                    yield tuple(x)

def reindex(x,order):
    y=[0]*(1<<len(order))
    for A,n in enumerate(x):
        B=sum(1<<j for j,i in enumerate(order) if A>>i&1)
        y[B]+=n
    return tuple(y)


def extends(x,d):
    n=len(x)
    y=[0]*n
    def rec(i,t):
        if i==n-1:
            if t<=x[i]:
                y[i]=t
                yield tuple(x[j]-y[j] for j in range(n))+tuple(y)
            return
        for k in range(min(t,x[i])+1):
            y[i]=k
            yield from rec(i+1,t-k)
    yield from rec(0,d)
