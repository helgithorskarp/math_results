"""Independent original-set affine table and orbit sums.

The mathematical table is credited to9145 and own9303/source77e859b.
No target9434 executable, EXPECTED, RESULTS or orbit decoder is imported.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb
from linear import need,digest,mv,psd

def table(q,kap):
    need((type(q)is int or isinstance(q,F))and(type(kap)is int or isinstance(kap,F)),'exact table input')
    need(q>=4,'table domain')
    q=F(q);kap=F(kap);hh=kap/(3*q+5);s=3*q+4
    o,p,a,b,c,d,e=(0,1),(0,2),(1,0),(1,1),(2,0),(2,1),(3,0);Q={}
    def put(x,y,z):Q[tuple(sorted((x,y)))]=z
    g1=1+6/q;g2=g1-6*hh*(q+1)/(q*(q-1))
    put(o,o,(kap+g1-1+2*q-s)/(q-1))
    put(o,p,q*(q-3)/((q-1)*(q-2)))
    put(p,p,(kap+g2-1+2*q/(q-1)-s+q*(q-1)/2)/((q-2)*(q-3)/2))
    for x,aa,bb,gg in [(o,1-1/q,1+1/q,g1),(p,1+2*hh/(q*(q-1)),1+2*(hh+(q-1)**2/q)/((q-1)*(q-2)),g2)]:
        for y in [a,c]:put(x,y,aa)
        for y in [b,d]:put(x,y,bb)
        put(x,e,gg)
    rr=3+2/q
    for x,y in [(a,a),(a,b),(b,b)]:put(x,y,F(0))
    put(a,c,F(2));put(a,d,rr);put(b,c,rr);put(b,d,(s-rr)/(q-1))
    need(len(Q)==20,'complete prior affine disjoint table');return Q

def family(q,k):
    need(type(q)is int and 4<=q<=23 and type(k)is int and 0<=k<=q,'bounded new literal generator')
    Z=sum(1<<j for j in range(3,3+k));sets=[0]
    for r in [1,2,3]:
        for choices in combinations(range(q+3),r):
            A=sum(1<<j for j in choices)
            if r==3 and ((A&7).bit_count()<2 or (A&7==6 and A&Z)):continue
            sets.append(A)
    sets.sort();N=(q*q+13*q+16)//2-k
    need(len(sets)==len(set(sets))==N and sets[0]==0,'complete family cardinality')
    def admitted(A):return A.bit_count()<=2 or (A.bit_count()==3 and (A&7).bit_count()>=2 and not(A&7==6 and A&Z))
    if q<=8:need(sets==[A for A in range(1<<(q+3))if admitted(A)],'separate bounded binary membership census')
    present=set(sets)
    for A in sets:
        for bit in range(q+3):
            if A>>bit&1:need(A^(1<<bit)in present,'original downward closure')
    sizes=[sum(bool(A&(1<<j))for A in sets)for j in range(q+3)]
    expected=[3*q+4,3*q+4-k,3*q+4-k]+[q+5]*k+[q+6]*(q-k)
    need(sizes==expected,'entire original star census')
    return sets,Z

def repair(A,B):
    x,y=sorted((A,B))
    if (x,y)in [(1,2),(1,4)]:return F(1)
    if (x,y)in [(2,5),(3,4)]:return F(-1)
    return F(0)

def matrices(q,k):
    S,Z=family(q,k);non=S[1:];N=len(S);Q0=table(q,0);Q1=table(q,1)
    types=[((A&7).bit_count(),(A&~7).bit_count())for A in non]
    pair0={key:v-1 for key,v in Q0.items()};pairD={key:Q1[key]-v for key,v in Q0.items()}
    C=[];D=[];R=[]
    for i,A in enumerate(non):
        cr=[];dr=[];rr=[]
        for j,B in enumerate(non):
            if i==j:z=F(3*q+3);delta=F(0)
            elif A&B:z=F(-1);delta=F(0)
            else:key=tuple(sorted((types[i],types[j])));z=pair0[key];delta=pairD[key]
            cr.append(z);dr.append(delta);rr.append(repair(A,B))
        C.append(cr);D.append(dr);R.append(rr)
    U=[[F(N*(i==j)-1)-z for j,z in enumerate(row)]for i,row in enumerate(C)]
    return S,Z,C,D,R,U

def mix(A,B,t):return [[x+t*y for x,y in zip(row,rr)]for row,rr in zip(A,B)]
def quad(A,v):return sum(x*y for x,y in zip(v,mv(A,v)))
def pair(A,u,v):return sum(x*y for x,y in zip(u,mv(A,v)))
def orbit_data(S,Z,q,k):
    keys=[(A&7,(A&Z).bit_count(),(A&~(Z|7)).bit_count())for A in S[1:]]
    ordered=sorted(set(keys));groups=[[i for i,key in enumerate(keys)if key==wanted]for wanted in ordered]
    weights=[len(g)for g in groups]
    need(all(w==comb(k,key[1])*comb(q-k,key[2])for key,w in zip(ordered,weights)),'original binomial orbit census')
    need(sum(weights)==len(S)-1,'orbit exhaustiveness')
    return ordered,groups,weights
def orbit_form(A,groups):
    return [[sum(A[i][j]for i in x for j in y)for y in groups]for x in groups]
def representative_form(A,groups):
    # Separate arithmetic path; invariance proved by point permutations.
    return [[len(x)*sum(A[x[0]][j]for j in y)for y in groups]for x in groups]

def parameters(q,k):
    q=F(q);k=F(k);N=(q*q+13*q+16)/2-k;s=3*q+4;h=1/(3*q+5)
    alpha=q*(q+1)/2+3*(q+1)*h;gap=N-s;g=N-2*s;rr=3+2/q;ww=(s-rr)/(q-1)
    e=N-1-k*(s-k);a0=(2*k+1)*q+k-2*k/q;T=q*gap;S=alpha-2*k*h;B=T*S-2*a0*q*h
    az=(k-1)*(ww-1);aw=1+k*(ww-1);d=g+rr
    Q0=e-(k*az*az+(q-k)*aw*aw)/gap-4*q*(1-k)**2/d
    D4=S-2*h*(a0/gap+4*q*(1-k)/d);c4=h*h*(q/gap+4*q/d)
    return locals()
