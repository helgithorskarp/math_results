"""Fresh literal q18 coordinates and actual-entry repair accounting; stdlib only."""
from fractions import Fraction as F
from itertools import combinations
from collections import Counter
import hashlib,json


def need(ok,message):
    if not ok:raise ValueError(message)


def integer(x,label):need(type(x) is int,label);return x


def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()


def literal():
    members=[0]
    for size in (1,2,3):
        for points in combinations(range(21),size):
            A=sum(1<<i for i in points)
            if size==3 and ((A&7).bit_count()<2 or (A&7==6 and A&(((1<<9)-1)<<3))):continue
            members.append(A)
    D=sorted(members);need(len(D)==278 and len(set(D))==278,'complete carrier')
    need(all(A^(1<<i) in D for A in D for i in range(21) if A>>i&1),'all downset deletions')
    stars=[sum(A>>i&1 for A in D) for i in range(21)]
    need(stars==[58,49,49]+[23]*9+[24]*9,'all original stars')
    return D,stars


def typ(A):return A&7,((A>>3)&511).bit_count(),((A>>12)&511).bit_count()


def build(D,table,den):
    proper=D[1:];n=len(proper);a=proper.index(1);star=[i for i,A in enumerate(proper) if A&1];rest=[i for i,A in enumerate(proper) if not A&1]
    C=[[0]*n for _ in proper];used=set()
    for i,A in enumerate(proper):
        for j,B in enumerate(proper):
            if i==j:C[i][j]=57*den
            elif A&B:C[i][j]=-den
            elif a not in (i,j):
                k=tuple(sorted((typ(A),typ(B))));need(k in table,'whole orbit coverage');used.add(k);C[i][j]=table[k]
    need(used==set(table),'no unused coefficient')
    for i in rest:C[i][a]=C[a][i]=-sum(C[i][j] for j in star if j!=a)
    need(all(sum(C[i][j] for j in star)==0 for i in range(n)),'every actual star row')
    need(all(C[i][j]==C[j][i] for i in range(n) for j in range(n)),'full C symmetry')
    U=[[278*den*(i==j)-den-C[i][j] for j in range(n)] for i in range(n)]
    rows=[sum(row) for row in C];L=[[0]*278 for _ in D];L[0][0]=den+sum(rows)
    for i in range(n):
        L[0][i+1]=L[i+1][0]=den-rows[i]
        for j in range(n):L[i+1][j+1]=den+C[i][j]
    need(all(sum(row)==278*den for row in L),'all original L row sums')
    # Entire upper endpoint including empty; use literal incidence lift row sums.
    ur=[sum(row) for row in U]
    for i in range(278):
        for j in range(278):
            lifted=sum(ur) if i==j==0 else -ur[(j or i)-1] if not i or not j else U[i-1][j-1]
            need(278*den*(i==j)-L[i][j]==lifted,'entire original upper lift')
    M=[[L[i][j]-58*den*(i==j) for j in range(278)] for i in range(278)]
    need(all(sum(row)==220*den for row in M),'every original M row')
    need(all(not A&B or M[i][j]==0 for i,A in enumerate(D) for j,B in enumerate(D)),'all support including diagonals')
    need(all(M[i][j]==M[j][i] for i in range(278) for j in range(278)),'entire M symmetry')
    h=[278*(A&1!=0)-58 for A in D]
    need(sum(h)==0 and all(sum(v*x for v,x in zip(row,h))==0 for row in L),'whole centered star actual kernel')
    return C,U,L,M


def add(d,i,j,v):
    d[i,j]=d.get((i,j),0)+v
    if not d[i,j]:del d[i,j]


def outerlift(R):
    """Literal columns e_A-e_empty; no hard-coded empty-completion rule."""
    out={}
    for (i,j),v in R.items():
        for k,u in ((i+1,1),(0,-1)):
            for l,w in ((j+1,1),(0,-1)):add(out,k,l,v*u*w)
    return out


def repairs(D):
    proper=D[1:];n=len(proper);a=proper.index(1);B=[[0]*278 for _ in D];proper_envelope=[[0]*n for _ in proper];nn=0;trades=0;ks=[0]*n;nn_degree=[0]*n;star_degree=[0]*n;count=0;slots=[]
    for i,A in enumerate(proper):
        for j in range(i):
            G=proper[j]
            if A&G or a in (i,j):continue
            count+=1;slots.append((i,j));R={(i,j):1,(j,i):1}
            if (A&1)!=(G&1):
                trades+=1;r=i if not A&1 else j;s=j if r==i else i;ks[r]+=1;star_degree[s]+=1
                R[r,a]=R[a,r]=-1
                expected={(r+1,s+1):1,(s+1,r+1):1,(r+1,a+1):-1,(a+1,r+1):-1,(0,s+1):-1,(s+1,0):-1,(0,a+1):1,(a+1,0):1}
            else:
                need(not A&1 and not G&1,'only NN unit edges');nn+=1;nn_degree[i]+=1;nn_degree[j]+=1
                expected={(i+1,j+1):1,(j+1,i+1):1,(0,i+1):-1,(i+1,0):-1,(0,j+1):-1,(j+1,0):-1,(0,0):2}
            actual=outerlift(R);need(actual==expected,'each literal generator completion')
            need(all(sum(v for (r,c),v in actual.items() if r==row)==0 for row in {q for pair in actual for q in pair}),'every supported generator row sum')
            need(all(not D[i]&D[j] for (i,j) in actual),'every generator support')
            for (r,c),v in R.items():proper_envelope[r][c]+=abs(v)
            for (r,c),v in actual.items():B[r][c]+=abs(v)
    need(count==29802 and nn==19522 and trades==10280 and sum(ks)==10280,'complete independent coordinate census')
    need(len(set(slots))==count,'injective nonanchor coefficient decoder')
    # Each independent coefficient appears in its unique nonanchor proper entry.
    # Rh=0 uniquely recovers the219 nonstar anchor positions.
    for i,A in enumerate(proper):
        for j,G in enumerate(proper):
            expected=ks[j] if i==a else ks[i] if j==a else int(i!=j and not A&G)
            need(proper_envelope[i][j]==expected,'entire proper interval envelope')
    for i,A in enumerate(D):
        for j,G in enumerate(D):
            if i and j:expected=proper_envelope[i-1][j-1]
            elif not i and not j:expected=2*nn
            else:
                k=(i or j)-1;expected=trades if k==a else star_degree[k] if proper[k]&1 else nn_degree[k]
            need(B[i][j]==expected,'every original entry budget including loop')
    S=sum(v*v for row in proper_envelope for v in row)
    need(S==2*(count+sum(k*k for k in ks))==1060012 and S<1030**2,'exact Frobenius squared box budget')
    return B,dict(coordinates=count,nn_edges=nn,anchored_trades=trades,anchor_conditions=219,maximum_anchor_count=max(ks),sum_anchor_counts=sum(ks),sum_anchor_squares=sum(k*k for k in ks),anchor_count_census=sorted(Counter(ks[i] for i,A in enumerate(proper) if not A&1).items()),frobenius_squared_budget=S,proper_interval_envelope_sha256=hashlib.sha256(canon(proper_envelope)).hexdigest(),actual_entry_budgets_sha256=hashlib.sha256(canon(B)).hexdigest())
