"""Reviewer5 literal incidence/matrix audit reused from8152, expanded domain.
No author imports or fixtures; exact all-entry checks.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from exact import need, matvec, rank

def mask(points):
    return sum(1 << x for x in points)


def digest(value):
    return sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def rotate(A,j,v):
    return sum(1 << ((i+j)%v) for i in range(v) if A >> i & 1)


def parameters(v,lam):
    need(type(v) is int and type(lam) is int and v>=5 and 2<=lam<=v-2,'invalid design parameters')
    need(lam*(v-1)%2==0 and lam*v*(v-1)%6==0,'nonintegral design parameters')
    m,b,r=v*(v-1)//2,lam*v*(v-1)//6,lam*(v-1)//2
    return m,b,r,v+r,1+v+m+b


def weights(v,lam):
    _,_,r,s,_=parameters(v,lam)
    c=F(3*v*v-3*(lam+3)*v+11*lam,3*(v-2)*(v-3))
    d=F(v*v-v-4,(v-4)*(v-3))
    if (v,lam)==(5,3): t=F(6)
    elif (v,lam)==(6,2): t=F(2)
    else: t=F((v-1)*(lam*(v-3)-6),lam*(v*v-10*v+27)-6)
    return {'a':-F(lam,3),'c':c,'d':d,'t':t,
            'w':s-(v-3)*c-(r-2*lam)*d,'h':s-(v-4)*d-(r-3*lam)*t}


def incidence(v,lam,blocks):
    m,b,r,s,N=parameters(v,lam)
    U=set(blocks)
    need(len(blocks)==len(U)==b,'missing or repeated triple')
    need(all(type(A) is int and 0<A<1<<v and A.bit_count()==3 for A in U),'invalid triple')
    pairs=[mask(c) for c in combinations(range(v),2)]
    triples=sorted(U)
    completing={p:tuple(x for x in range(v) if not p >> x & 1 and p|(1<<x) in U) for p in pairs}
    need(all(len(xs)==lam for xs in completing.values()),'wrong literal pair multiplicity')
    need(all(sum(A >> x & 1 for A in U)==r for x in range(v)),'wrong replication')
    P=[[int(p >> x & 1) for p in pairs] for x in range(v)]
    C=[[int(x in completing[p]) for p in pairs] for x in range(v)]
    B=[[int(A >> x & 1) for A in triples] for x in range(v)]
    R=[[int(p&A==p) for A in triples] for p in pairs]
    H=[[0 if A >> x & 1 else sum(int(p|(1<<x) in U) for p in pairs if p&A==p)
        for A in triples] for x in range(v)]
    u=lam*(lam-1)//2
    dot=lambda a,b:sum(x*y for x,y in zip(a,b))
    Z=[[dot(C[x],C[y])-(r-u)*(x==y)-u for y in range(v)] for x in range(v)]
    checks=0
    for x in range(v):
        need(Z[x][x]==0 and sum(Z[x])==0,'wrong completion defect normalization')
        for y in range(v):
            for lhs,rhs in [(dot(P[x],P[y]),(v-2)*(x==y)+1),
                            (dot(B[x],B[y]),(r-lam)*(x==y)+lam),
                            (dot(P[x],C[y]),lam*(x!=y)),
                            (dot(B[x],H[y]),3*u*(x!=y)+Z[x][y]),
                            (dot(H[x],B[y]),3*u*(x!=y)+Z[x][y])]:
                need(lhs==rhs,'incidence Gram mismatch');checks+=1
        for j,A in enumerate(triples):
            need(sum(P[x][i]*R[i][j] for i in range(m))==2*B[x][j],'PR identity')
            need(sum(C[x][i]*R[i][j] for i in range(m))==B[x][j]+H[x][j],'CR identity')
            checks+=2
        for i,p in enumerate(pairs):
            need(sum(R[i][j]*B[x][j] for j in range(b))==lam*P[x][i]+C[x][i],'RB transpose identity')
            checks+=1
    # Independent complement identity, entry by entry, not just Gram hashes.
    other=v-2-lam
    Cp=[[1-P[x][i]-C[x][i] for i in range(m)] for x in range(v)]
    rp,up=F(other*(v-1),2),F(other*(other-1),2)
    need(all(a in (0,1) for row in Cp for a in row),'complement completion not binary')
    need(all(dot(Cp[x],Cp[y])-(rp-up)*(x==y)-up==Z[x][y]
             for x in range(v) for y in range(v)),'Z not invariant under triple complement')
    for x in range(v):
        for j,A in enumerate(triples):
            need(H[x][j]==3*(1-B[x][j])-sum(Cp[x][i]*R[i][j] for i in range(m)),
                 'complement form of H')
    return pairs,triples,P,C,B,R,H,Z,{'incidence_scalar_checks':checks,
             'Z_values':sorted({x for row in Z for x in row}),
             'outside_completion_multiplicities':sorted({x for row in H for x in row}),
             'complement_multiplicity':other,'complement_Z_entry_checks':v*v,
             'complement_H_entry_checks':v*b}


def matrices(v,lam,blocks):
    pairs,triples,P,C,B,R,H,Z,info=incidence(v,lam,blocks)
    m,b,r,s,N=parameters(v,lam)
    V=sorted({0}|{1<<i for i in range(v)}|set(pairs)|set(triples))
    need(len(V)==N,'wrong vertex domain')
    w=weights(v,lam);U=set(triples);index={A:j for j,A in enumerate(triples)}
    k=(v-2)*(v-3)//2
    Q,E=[],[]
    for a in V:
        qr,er=[],[]
        for bb in V:
            if a&bb:
                value,change=F(s if a==bb else 0),F(0)
            elif a==bb==0:
                value,change=F(1),F(m*k)
            elif not a or not bb:
                value=F(1)
                size=(a|bb).bit_count()
                change=F(-(v-1)*k if size==1 else k if size==2 else 0)
            else:
                x,y=sorted((a,bb),key=lambda z:z.bit_count())
                sizes=(x.bit_count(),y.bit_count())
                if sizes==(1,1):
                    value=w['a']+w['t']*Z[x.bit_length()-1][y.bit_length()-1]
                elif sizes==(1,2):
                    value=w['w']-w['d']*int(x|y in U)
                elif sizes==(1,3):
                    value=w['h']-w['t']*H[x.bit_length()-1][index[y]]
                else:
                    value=w[{(2,2):'c',(2,3):'d',(3,3):'t'}[sizes]]
                change=F({(1,1):2*k,(1,2):-(v-3),(2,2):1}.get(sizes,0))
            qr.append(value);er.append(change)
        Q.append(qr);E.append(er)
    eta=F(1,8*v*v)
    Qm=[[x+eta*y for x,y in zip(row,e)] for row,e in zip(Q,E)]
    for i,A in enumerate(V):
        need(sum(Q[i])==sum(Qm[i])==N and sum(E[i])==0,'literal row condition')
        for j,BB in enumerate(V):
            need(Q[i][j]==Q[j][i] and Qm[i][j]==Qm[j][i],'literal symmetry')
            if A&BB:
                need(Q[i][j]==Qm[i][j]==s*(i==j),'literal support condition')
    stars=[[F(bool(A >> x & 1)) for A in V] for x in range(v)]
    # Exact support sums equal multiplication by the binary star vector.
    # Avoid multiplying and adding its many zero coordinates.
    for x in range(v):
        support=[j for j,A in enumerate(V) if A>>x&1]
        need(len(support)==s and all(sum(row[j] for j in support)==s for row in Q)
             and all(sum(row[j] for j in support)==0 for row in E),
             'literal star condition')
    centered=[[x-F(s,N) for x in star] for star in stars]
    empty=[F(A==0)-F(1,N) for A in V]
    need(rank(centered)==v and rank(centered+[empty])==v+1,'literal forced Gram rank')
    need(not any(matvec(Q,empty)) and any(matvec(Qm,empty)),'empty direction not repaired')
    need(max(sum(abs(x) for x in row) for row in E)==4*m*k,'literal trade norm')
    # Check every entry of the pair/triple principal factor K independently.
    for i,A in enumerate(V):
        if A.bit_count()<2:
            continue
        for j,BB in enumerate(V):
            if BB.bit_count()<2:
                continue
            z=(A&BB).bit_count()
            ka,kb=A.bit_count(),BB.bit_count()
            if ka==kb==2:
                value=(s+w['c'])*(i==j)-w['c']*z+w['c']-1
            elif ka==kb==3:
                value=(s-w['t'])*(i==j)+w['t']*(z*(z-1)//2)-w['t']*z+w['t']-1
            else:
                value=w['d']*(z==2)-w['d']*z+w['d']-1
            need(value==Q[i][j]-1,'literal K principal block')
    return V,Q,Qm,E,{'v':v,'lambda':lam,'N':N,'s':s,'eta':str(eta),
                       'weights':{key:str(x) for key,x in w.items()},**info}


def matrix_hash(Q,V):
    order=sorted(range(len(V)),key=lambda i:(V[i].bit_count(),V[i]))
    return sha256(json.dumps([[str(Q[i][j]) for j in order] for i in order],separators=(',',':')).encode()).hexdigest()


def buffer(Q,gap):
    N=len(Q)
    return [[N*(i==j)-Q[i][j]-gap*((i==j)-F(1,N)) for j in range(N)] for i in range(N)]
