#!/usr/bin/env python3
"""Independent all-multiplicity H audit and complement-STS cap validation.

No author executable, fixture or polynomial implementation is imported.
All-order claims are the ordinary proofs in REVIEW.md. Full matrices are
literal rational entries on independently constructed finite designs.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys

from exact import need, matvec, rank, determinant3, psd_rank as rational_psd
from fraction_free import psd_rank
from scalar import run as scalar_run
from certificates import certify


def mask(points):
    return sum(1 << x for x in points)


def digest(value):
    return sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def rotate(A,j,v):
    return sum(1 << ((i+j)%v) for i in range(v) if A >> i & 1)


def cyclic_four():
    """Select eight of the 22 cyclic triple orbits, in reverse canonical order.

    This is a bounded witness construction, not a design classification.
    All output pair degrees are subsequently checked literally.
    """
    v=13
    reps=sorted({min(rotate(mask(c),j,v) for j in range(v)) for c in combinations(range(v),3)},reverse=True)
    vectors=[]
    for a in reps:
        points=[i for i in range(v) if a >> i & 1]
        counts=Counter(min((x-y)%v,(y-x)%v) for x,y in combinations(points,2))
        vectors.append([counts[i] for i in range(1,7)])
    nodes=0
    def choose(start,chosen,deficit):
        nonlocal nodes
        nodes+=1
        need(nodes<=100_000,'cyclic witness construction reached operational cap')
        if len(chosen)==8:
            return chosen if not any(deficit) else None
        if len(reps)-start<8-len(chosen):
            return None
        for i in range(start,len(reps)):
            if all(a<=b for a,b in zip(vectors[i],deficit)):
                result=choose(i+1,chosen+[i],[b-a for a,b in zip(vectors[i],deficit)])
                if result is not None:
                    return result
        return None
    selected=choose(0,[],[4]*6)
    need(selected is not None,'bounded cyclic construction did not produce a witness')
    seeds=[reps[i] for i in selected]
    U={rotate(a,j,v) for a in seeds for j in range(v)}
    return U,{'canonical_seeds':seeds,'witness_construction_nodes':nodes,'selection_order':'decreasing orbit representative'}


def complement_sts(v):
    need(v==13,'only the literal thirteen-point STS fixture is used')
    seeds=[mask((0,1,4)),mask((0,2,7))]
    missing={rotate(a,j,v) for a in seeds for j in range(v)}
    all_triples={mask(c) for c in combinations(range(v),3)}
    return all_triples-missing,{'missing_STS_cyclic_seeds':seeds,'missing_blocks':sorted(missing)}


def parameters(v,lam):
    need(type(v) is int and type(lam) is int and v>=13 and 2<=lam<=v-2,'invalid design parameters')
    need(lam*(v-1)%2==0 and lam*v*(v-1)%6==0,'nonintegral design parameters')
    m,b,r=v*(v-1)//2,lam*v*(v-1)//6,lam*(v-1)//2
    return m,b,r,v+r,1+v+m+b


def weights(v,lam):
    _,_,r,s,_=parameters(v,lam)
    c=F(3*v*v-3*(lam+3)*v+11*lam,3*(v-2)*(v-3))
    d=F(v*v-v-4,(v-4)*(v-3))
    t=F((v-1)*(lam*(v-3)-6),lam*(v*v-10*v+27)-6)
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
    for star in stars:
        need(matvec(Q,star)==[F(s)]*N and not any(matvec(E,star)),'literal star condition')
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


def engine_controls():
    count=accepted=0
    for values in product((-1,0,1),repeat=6):
        a,b,c,d,e,f=values;Q=[[a,d,e],[d,b,f],[e,f,c]]
        expected=min(a,b,c,a*b-d*d,a*c-e*e,b*c-f*f,determinant3(Q))>=0
        try:
            psd_rank(Q);got=True
        except ValueError:
            got=False
        need(expected==got,'fraction-free PSD/principal-minor control')
        count+=1;accepted+=got
    gram=[]
    for rows,columns in [(7,3),(13,8)]:
        V=[[F(((i+1)*(j+3)+i*j)%11-5,j+1) for j in range(columns)] for i in range(rows)]
        Q=[[sum(a*b for a,b in zip(x,y)) for y in V] for x in V]
        rr=rational_psd(Q)
        need(psd_rank(Q)==rr==rank(V),'two PSD engines disagree on rational Gram')
        gram.append({'rows':rows,'columns':columns,'rank':rr})
    rejects=0
    for Q in [[[0,1],[1,0]],[[-1]],[[1,0],[1,1]],[[1,0]],[[1,2],[2,1]]]:
        try:
            psd_rank(Q)
        except ValueError:
            rejects+=1
        else:
            raise ValueError('damaged fraction-free control accepted')
    need(psd_rank([[0,0],[0,F(1,3)]])==1,'symmetric pivot-swap control')
    return {'principal_minor_comparisons':count,'accepted':accepted,
            'rational_Gram_two_engine_comparisons':gram,'invalid_matrices_rejected':rejects}


def finite(v,lam,U,label,generation,dense_cap):
    V,Q,Qm,E,info=matrices(v,lam,sorted(U));N=len(V)
    print('literal construction checked',label,'N',N,file=sys.stderr,flush=True)
    proof=certify(V,Q,Qm,E,v,lam,weights(v,lam),dense_cap)
    ranks=proof['lower_ranks'].copy()
    if dense_cap:
        upper=proof['upper'];ranks.update(upper['upper_ranks'])
        info.update(new_centered_cap=upper['centered_cap'],new_delta=upper['delta'],repaired_upper_buffer=upper['repaired_upper_buffer'])
    info['complete_structural_PSD_certificate']=proof
    print('complete structured certificate checked',label,ranks,file=sys.stderr,flush=True)
    info.update(label=label,generation=generation,blocks=sorted(U),blocks_sha256=digest(sorted(U)),
                certified_PSD_ranks=ranks,centered_sha256=matrix_hash(Q,V),repaired_sha256=matrix_hash(Qm,V))
    return info


def run():
    scalar=scalar_run()
    controls=engine_controls()
    U,generation=cyclic_four()
    rows=[finite(13,4,U,'reverse-developed cyclic lambda4',generation,False)]
    missing,generation2=complement_sts(13)
    rows.append(finite(13,10,missing,'all triples minus cyclic STS13',generation2,True))
    rejected=0
    for v,lam,blocks in [(12,4,sorted(U)),(13,12,sorted(U)),(14,3,sorted(U)),
                         (13,4,sorted(U)[:-1]),(13,4,sorted(U)+[next(iter(U))])]:
        try:
            incidence(v,lam,blocks)
        except ValueError:
            rejected+=1
        else:
            raise ValueError('invalid design accepted')
    return {'agent':'six-reviewer-5','role':'independent mathematical reviewer',
            'arithmetic':'standard-library integers/Fraction; no author imports',
            'scalar':scalar,'PSD_controls':controls,'finite_inputs':rows,'design_controls_rejected':rejected}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--write',type=Path);group.add_argument('--check',type=Path)
    args=parser.parse_args();result=run()
    if args.write:
        args.write.write_text(json.dumps(result,indent=2)+'\n')
    else:
        need(result==json.loads(args.check.read_text()),'complete independent summary mismatch')
    print(json.dumps({'status':'passed','complete_structural_PSD_forms':sum(len(x['certified_PSD_ranks']) for x in result['finite_inputs']),
                      'identities':result['scalar']['identity_count'],
                      'positive_certificates':result['scalar']['positive_certificate_count'],
                      'canonical_sha256':digest(result)}))
