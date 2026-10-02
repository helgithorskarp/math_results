"""Original finite domains, entry matrices, and a separate empty-row formula."""
from fractions import Fraction as F
from itertools import combinations
from functools import lru_cache
import inputs
from literal import table as _table,typ,require,action,quadratic
from exact import digest,lift
table=lru_cache(maxsize=16)(_table)

KAPPA=F(1,4096)
TRADE=F(4)
LOWER_FLOOR=F(1,2**30)
CAP_FLOOR=F(1,2**20)


def member(q,k,A):
    require(type(A) is int and 0<=A<1<<(q+3),'original member bitmask')
    return (A.bit_count()<=2 or A.bit_count()==3 and (A&7).bit_count()>=2) and not (
        A&7==6 and (A>>3).bit_count()==1 and (A>>3).bit_length()<=k)


def domain(q,k=4,scan=False):
    require(type(q) is int and ((k==4 and 4<=q<=17) or (q,k)==(8,3)),
            'finite original guard k4,q4..17; q8,k3 baseline only')
    if scan:return [A for A in range(1<<(q+3)) if member(q,k,A)]
    return [0]+sorted(sum(1<<i for i in pts)
                     for size in (1,2,3) for pts in combinations(range(q+3),size)
                     if member(q,k,sum(1<<i for i in pts)))


def entry(A,B,s,w,kappa=F(0),t=F(0)):
    if A==B:return F(s-1)
    if A&B:return F(-1)
    a,b=w[tuple(sorted((typ(A),typ(B))))]
    repair={(1,2):1,(1,4):1,(2,5):-1,(3,4):-1}.get(tuple(sorted((A,B))),0)
    return a+kappa*b-1+t*repair


def original(q,kappa=F(0),t=F(0),k=4):
    require(isinstance(kappa,(int,F)) and isinstance(t,(int,F)),'exact finite parameters')
    X=domain(q,k);N=len(X);s=3*q+4
    require(N==(q*q+13*q+16)//2-k and N<=259,'original finite dimensions')
    require(X==domain(q,k,scan=True),'full membership scan agrees with combinations')
    w=table(q)
    C=[[entry(A,B,s,w,kappa,t) for B in X[1:]] for A in X[1:]]
    U=[[F(N*int(i==j)-1)-C[i][j] for j in range(N-1)] for i in range(N-1)]
    return X,N,s,C,U


def core_data(q):
    require(4<=q<=12,'bounded original duals q4..12')
    X,N,s,C,U=original(q)
    w=table(q);n=N-1
    D=[[F(0) if A==B or A&B else w[tuple(sorted((typ(A),typ(B))))][1]
        for B in X[1:]] for A in X[1:]]
    R=[[F(0)]*n for _ in range(n)];ix={A:i for i,A in enumerate(X[1:])}
    for A,B,v in ((1,2,1),(1,4,1),(2,5,-1),(4,3,-1)):
        R[ix[A]][ix[B]]=R[ix[B]][ix[A]]=F(v)
    return X,N,s,C,D,R,U


def closed_whole_entry(q,A,B,kappa=KAPPA,t=TRADE):
    """Direct scalar empty-row identity, independent of dense row summation."""
    require(13<=q<=17 and member(q,4,A) and member(q,4,B),'positive finite whole entry')
    N=(q*q+13*q+8)//2;s=3*q+4;h=F(1,3*q+5)
    alpha=F(q*(q+1),2)+3*(q+1)*h;w=table(q)
    if A==B==0:L=1+4*(s-4)+kappa*(alpha-8*h)
    elif not A or not B:
        V=A or B;core=(V&7).bit_count()
        r=F(1) if core==0 else h if core<3 else -3*(q+1)*h
        m=4 if V&6 else (V&120).bit_count()
        if m==4:deleted=F(-4)
        else:
            a,b=w[tuple(sorted((typ(V),(2,1))))]
            deleted=-m+(4-m)*(a+kappa*b-1)
        repair=2 if V==1 else -1 if V in (3,5) else 0
        L=1-(kappa*r-deleted+t*repair)
    else:L=1+entry(A,B,s,w,kappa,t)
    return L,(L-s*int(A==B))/F(N-s)


def whole(q):
    X,N,s,C,U=original(q,KAPPA,TRADE)
    L=lift(C);M=[[(L[i][j]-s*int(i==j))/F(N-s) for j in range(N)] for i in range(N)]
    require(all(L[i][j]==L[j][i] and M[i][j]==M[j][i] for i in range(N) for j in range(N)),
            'whole original symmetry')
    require(all(sum(row)==N for row in L) and all(sum(row)==1 for row in M),'every original row equation')
    require(all(M[i][j]==0 for i,A in enumerate(X) for j,B in enumerate(X) if A&B),'every intersecting support zero')
    require(all((L[i][j],M[i][j])==closed_whole_entry(q,A,B)
                for i,A in enumerate(X) for j,B in enumerate(X)),'every ordered closed whole entry')
    stars=[sum(bool(A&(1<<i)) for A in X) for i in range(q+3)]
    require(stars==[s,s-4,s-4]+[q+5]*4+[q+6]*(q-4),'complete original star census')
    a=[F(bool(A&1)) for A in X[1:]]
    require(not any(action(C,a)),'original nonempty maximum-star kernel')
    centered=[F(bool(A&1))-F(s,N) for A in X]
    require(not any(action(L,centered)) and sum(centered)==0,'whole centered maximum-star kernel')
    return X,N,s,C,U,L,M,{'q':q,'N':N,'s':s,'kappa':str(KAPPA),'t':str(TRADE),
        'whole_ordered_entries':N*N,'M_empty_empty':str(M[0][0]),
        'whole_M_digest':digest([[str(x) for x in row] for row in M]),
        'all_closed_whole_entries_match':True,'star_census':stars}
