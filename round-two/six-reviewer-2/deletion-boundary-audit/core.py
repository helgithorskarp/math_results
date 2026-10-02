"""Independent original-set matrices for the credited affine table of9145.

No researcher executable is imported. Table coefficients are mathematical
inputs from the displayed9145 formula; dual vectors are credited data.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations,permutations
from pathlib import Path
import hashlib,json

ROOT=Path(__file__).resolve().parent

def need(ok,why):
    if not ok:raise ValueError(why)

def exact(v):
    need(type(v) is int or isinstance(v,F),'exact integer/rational input')
    return F(v)

def canonical(v):
    if isinstance(v,F):return str(v)
    if isinstance(v,dict):return {str(k):canonical(w) for k,w in v.items()}
    if isinstance(v,(list,tuple)):return [canonical(w) for w in v]
    return v

def digest(v):
    return hashlib.sha256(json.dumps(canonical(v),sort_keys=True,separators=(',',':')).encode()).hexdigest()

def mask(A):return sum(1 << i for i in A)

def domain(q,k,Z=None):
    need(type(q) is int and q>=4 and type(k) is int and 1<=k<=q,'domain parameters')
    W=set(range(3,q+3));Z=set(range(3,3+k)) if Z is None else set(Z)
    need(len(Z)==k and Z<=W,'deletion set')
    K={0,1,2};sets=[frozenset()]
    for r in [1,2,3]:
        for c in combinations(range(q+3),r):
            A=frozenset(c)
            if r==3 and (len(A&K)<2 or (0 not in A and 1 in A and 2 in A and A&W<=Z)):
                continue
            sets.append(A)
    sets.sort(key=mask)
    # Separate whole binary membership scan checks normalization/completeness.
    scanned=[]
    for m in range(1 << (q+3)):
        A=frozenset(i for i in range(q+3) if m >> i & 1)
        if len(A)<=2 or (len(A)==3 and len(A&K)>=2 and
                          not (0 not in A and 1 in A and 2 in A and A&W<=Z)):
            scanned.append(A)
    need(sets==scanned,'entire actual original domain')
    need(len(sets)==(q*q+13*q+16)//2-k,'domain cardinality')
    return sets

def table(q,kappa):
    q=exact(q);kap=exact(kappa)
    need(q>=4,'table q range')
    return _table(q,kap)

@lru_cache(maxsize=64)
def _table(q,kap):
    h=kap/(3*q+5);s=3*q+4
    o,p,a,b,c,d,e=(0,1),(0,2),(1,0),(1,1),(2,0),(2,1),(3,0)
    Q={}
    def put(i,j,v):Q[tuple(sorted((i,j)))]=F(v)
    g1=1+6/q;g2=g1-6*h*(q+1)/(q*(q-1))
    put(o,o,(kap+g1-1+2*q-s)/(q-1))
    put(o,p,q*(q-3)/((q-1)*(q-2)))
    put(p,p,(kap+g2-1+2*q/(q-1)-s+q*(q-1)/2)/((q-2)*(q-3)/2))
    for x,aa,bb,gg in [(o,1-1/q,1+1/q,g1),
        (p,1+2*h/(q*(q-1)),1+2*(h+(q-1)**2/q)/((q-1)*(q-2)),g2)]:
        for y in [a,c]:put(x,y,aa)
        for y in [b,d]:put(x,y,bb)
        put(x,e,gg)
    rr=3+2/q
    for i,j in [(a,a),(a,b),(b,b)]:put(i,j,0)
    put(a,c,2);put(a,d,rr);put(b,c,rr);put(b,d,(s-rr)/(q-1))
    need(len(Q)==20,'entire feasible disjoint type table')
    return Q

def primitive(q,A,B,kappa):
    if A==B:return F(3*q+3)
    if A&B:return F(-1)
    def typ(S):return len(S&{0,1,2}),len(S-set([0,1,2]))
    return table(q,kappa)[tuple(sorted((typ(A),typ(B))))]-1

def repair(A,B):
    endpoints=frozenset([A,B])
    if endpoints in [frozenset([frozenset([0]),frozenset([1])]),
                     frozenset([frozenset([0]),frozenset([2])])]:return F(1)
    if endpoints in [frozenset([frozenset([1]),frozenset([0,2])]),
                     frozenset([frozenset([2]),frozenset([0,1])])]:return F(-1)
    return F(0)

def matrices(q,k,Z=None):
    sets=domain(q,k,Z);non=sets[1:];n=len(non);N=n+1
    Q0=table(q,F(0));Q1=table(q,F(1))
    def value(A,B,Q):
        if A==B:return F(3*q+3)
        if A&B:return F(-1)
        ta=(len(A&{0,1,2}),len(A-{0,1,2}));tb=(len(B&{0,1,2}),len(B-{0,1,2}))
        return Q[tuple(sorted((ta,tb)))]-1
    C0=[[value(A,B,Q0) for B in non] for A in non]
    Delta=[[value(A,B,Q1)-C0[i][j] for j,B in enumerate(non)] for i,A in enumerate(non)]
    R=[[repair(A,B) for B in non] for A in non]
    U0=[[N*int(i==j)-1-C0[i][j] for j in range(n)] for i in range(n)]
    return sets,C0,Delta,R,U0

def affine(A,B,t):return [[a+t*b for a,b in zip(ar,br)] for ar,br in zip(A,B)]
def mv(A,v):return [sum(a*b for a,b in zip(row,v)) for row in A]
def quad(A,v):return sum(a*b for a,b in zip(v,mv(A,v)))
def projector(v):
    norm=sum(w*w for w in v);need(norm>0,'nonzero projector column')
    return [[F(i==j)-a*b/norm for j,b in enumerate(v)] for i,a in enumerate(v)]
def shift(A,delta,v=None):
    n=len(A);P=projector(v) if v is not None else [[F(i==j) for j in range(n)] for i in range(n)]
    return affine(A,P,-delta)

def psd(A):
    """Exact rational Schur congruence with largest-diagonal pivoting.

    Unlike the author's denominator-cleared fixed-order engine, the
    reference keeps Fraction entries and chooses new physical pivots.
    """
    n=len(A);need(all(len(r)==n for r in A),'square form')
    B=[[exact(v) for v in row] for row in A]
    need(all(B[i][j]==B[j][i] for i in range(n) for j in range(n)),'symmetric form')
    pivots=[];labels=list(range(n))
    while B:
        m=len(B);need(all(B[i][i]>=0 for i in range(m)),'negative Schur diagonal')
        p=max(range(m),key=lambda i:B[i][i]);d=B[p][p]
        if d==0:
            need(all(v==0 for row in B for v in row),'zero-diagonal nonzero residual')
            break
        pivots.append([labels[p],d]);ix=[i for i in range(m) if i!=p]
        ratios=[B[i][p]/d for i in ix]
        new=[[F(0)]*len(ix) for _ in ix]
        for i,ii in enumerate(ix):
            for j in range(i,len(ix)):
                value=B[ii][ix[j]]-ratios[i]*B[p][ix[j]]
                new[i][j]=new[j][i]=value
        B=new;labels=[labels[i] for i in ix]
    return {'dimension':n,'rank':len(pivots),'pivot_record_sha256':digest(pivots)}

def determinant(A):
    n=len(A);total=F(0)
    for p in permutations(range(n)):
        inversions=sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        term=F((-1)**inversions)
        for i in range(n):term*=A[i][p[i]]
        total+=term
    return total

def lift(C):
    n=len(C);N=n+1
    # Literal sparse E rows, with the actual empty coordinate retained.
    E=[[(i,F(-1)) for i in range(n)]]+[[(i,F(1))] for i in range(n)]
    EC=[[sum(v*C[k][j] for k,v in row) for j in range(n)] for row in E]
    return [[F(1)+sum(EC[i][k]*v for k,v in E[j]) for j in range(N)] for i in range(N)]

def whole_controls(q,k,kappa,t,sets,C):
    N=len(sets);s=3*q+4;non=sets[1:];L=lift(C)
    Z=set(range(3,3+k));deleted=[frozenset([1,2,x]) for x in Z]
    h=F(1,3*q+5);alpha=F(q*(q+1),2)+3*(q+1)*h
    rho=[]
    for A in non:
        a=len(A&{0,1,2});r=F(1) if a==0 else (h if a<3 else -3*(q+1)*h)
        rowR=2 if A==frozenset([0]) else (-1 if A in [frozenset([0,1]),frozenset([0,2])] else 0)
        rho.append(kappa*r-sum(primitive(q,A,B,kappa) for B in deleted)+t*rowR)
    total=kappa*(alpha-2*k*h)+k*(s-k)
    need(total==sum(rho),'closed whole empty-loop scalar')
    for i,A in enumerate(sets):
        for j,B in enumerate(sets):
            closed=(1+total if i==j==0 else (1-rho[j-1] if i==0 else
                (1-rho[i-1] if j==0 else 1+primitive(q,A,B,kappa)+t*repair(A,B))))
            need(L[i][j]==closed,'all actual whole entries versus closed row formula')
            need(not (A&B) or L[i][j]==s*int(i==j),'whole intersection support')
        need(sum(L[i])==N,'actual whole row sum')
    Sa=[F(0 in A) for A in sets];center=[a-F(s,N) for a in Sa]
    need(mv(L,center)==[0]*N,'whole centered actual a-star kernel')
    U=[[N*int(i==j)-L[i][j] for j in range(N)] for i in range(N)]
    need(mv(U,[F(1)]*N)==[0]*N,'actual constant cap kernel')
    return {'N':N,'s':s,'ordered_whole_entries':N*N,'L_sha256':digest(L),
            'upper_sha256':digest(U),'empty_L_loop':L[0][0],
            'empty_M_loop':(L[0][0]-s)/(N-s),'closed_rho_sha256':digest(rho)}
