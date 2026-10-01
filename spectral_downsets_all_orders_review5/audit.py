#!/usr/bin/env python3
"""Independent exact all-order audit; no author code, fixtures, or CAS imports."""
import argparse
from fractions import Fraction as F
from itertools import combinations,product
from math import comb
import json
from pathlib import Path
import sys
from exact import need,matvec,psd_rank,controls
from fraction_free import psd_rank as integer_psd
from literal import mask,rotate,digest,parameters,weights,incidence,matrices,matrix_hash,buffer
from lower import certify
from scalar import run as scalar_run,cap_data

def enumerate_six():
    """Every labelled ten-block subset of all20 triples, exactly184756 inputs.

    Base16 digits encode the15 pair degrees. Each degree<=10<16, so no
    carries occur. Equality to the all2 target is equivalent to a design.
    """
    pairs=list(combinations(range(6),2));triples=list(combinations(range(6),3))
    indices={p:i for i,p in enumerate(pairs)}
    encoded=[sum(16**indices[p] for p in combinations(T,2)) for T in triples]
    target=2*sum(16**i for i in range(15));valid=[];tested=0
    for selected in combinations(range(20),10):
        tested+=1
        if sum(encoded[i] for i in selected)==target:
            U=[mask(triples[i]) for i in selected]
            pairs1,T,P,C,B,R,H,Z,_=incidence(6,2,U)
            need(not any(x for row in Z for x in row),'six-point Z')
            need(all(H[x][i]==1-B[x][i] for x in range(6) for i in range(10)),'six-point H')
            need(all(A&T for A,T in combinations(U,2)),'disjoint six-point blocks')
            valid.append(sorted(U))
    need(tested==comb(20,10)==184756 and len(valid)==12,'six-point exhaustive census')
    return valid,{'tested_subsets':tested,'valid_labelled_designs':len(valid),'all_Z_zero':True,
      'all_H_equals_J_minus_B':True,'all_disjoint_block_pairs_absent':True,'all_designs_sha256':digest(valid),'designs':valid}

def fixtures(six):
    for v in (5,6):yield v,v-2,{mask(c) for c in combinations(range(v),3)},{'construction':'complete triple layer'}
    yield 6,2,set(six[0]),{'construction':'first lexicographic exhaustive six-point witness'}
    fano={rotate(mask((0,1,3)),j,7) for j in range(7)}
    reflected={mask((-x)%7 for x in range(7) if A>>x&1) for A in fano}
    all7={mask(c) for c in combinations(range(7),3)}
    need(not(fano&reflected),'two independently mirrored STS layers overlap')
    for l,U in ((2,fano|reflected),(3,all7-fano-reflected),(4,all7-fano),(5,all7)):
        yield 7,l,U,{'construction':'cyclic difference-cover STS and its reflection','first_STS':sorted(fano),'reflected_STS':sorted(reflected)}
    missing=set()
    for x,y in product(range(3),repeat=2):
        for a,b in ((1,0),(0,1),(1,1),(1,2)):
            missing.add(mask(3*((x+k*a)%3)+(y+k*b)%3 for k in range(3)))
    need(len(missing)==12,'affine STS9 line count')
    yield 9,6,{mask(c) for c in combinations(range(9),3)}-missing,{'construction':'complement of all affine lines in F3^2','missing_STS':sorted(missing)}

def upper_certificate(V,Q,Qm,E,v,l):
    dat=cap_data(v);N=len(V);Bcap=F(dat['centered_cap']);delta=F(dat['delta'])
    layers=[[i for i,A in enumerate(V) if A.bit_count()==j] for j in range(4)]
    p=[V[i] for i in layers[2]];T=[V[i] for i in layers[3]];m=len(p);b=len(T)
    missing={mask(c) for c in combinations(range(v),3)}-set(T)
    need(len(missing)==v*(v-1)//6,'missing STS cardinality')
    P=[[int(A>>x&1) for A in p] for x in range(v)]
    R=[[int(A&C==A) for C in T] for A in p]
    Rb=[[int(A&C==A) for C in sorted(missing)] for A in p]
    need(all(sum(row)==1 for row in Rb),'missing STS pair degrees')
    Cp=[[int(not(A>>x&1) and A|(1<<x) in missing) for A in p] for x in range(v)]
    w=weights(v,l);s=parameters(v,l)[3];d,t=w['d'],w['t']
    need(all(sum(a*c for a,c in zip(Cp[x],Cp[y]))==F(v-1,2)*(x==y) for x in range(v) for y in range(v)),'missing completion Gram')
    for x,ii in enumerate(layers[1]):
        for y,jj in enumerate(layers[1]):
            need(Q[ii][jj]==(s+F(l,3))*(x==y)-F(l,3),'zero-defect point block')
        for j,jj in enumerate(layers[2]):
            need(Q[ii][jj]==(d-w['w'])*P[x][j]+d*Cp[x][j]+w['w']-d,'mean point/pair formula')
        for j,jj in enumerate(layers[3]):
            bx=int(T[j]>>x&1);cpR=sum(Cp[x][i]*R[i][j] for i in range(m))
            need(Q[ii][jj]==(w['h']-3*t)*(1-bx)+t*cpR,'mean point/triple formula')
    for i,ii in enumerate(layers[2]):
        for j,jj in enumerate(layers[3]):
            need(Q[ii][jj]==d*(R[i][j]-(p[i]&T[j]).bit_count()+1),'mean pair/triple formula')
    # Exact universal full-triple pair Gram identity minus the missing blocks.
    PtP=[[sum(P[x][i]*P[x][j] for x in range(v)) for j in range(m)] for i in range(m)]
    for i in range(m):
        for j in range(m):
            lhs=sum(R[i][k]*R[j][k] for k in range(b))
            rhs=(v-4)*(i==j)+PtP[i][j]-sum(a*c for a,c in zip(Rb[i],Rb[j]))
            need(lhs==rhs,'complement pair Gram identity')
    Pi=[[F(i==j)-F(PtP[i][j],v-2)+F(2,(v-2)*(v-1)) for j in range(m)] for i in range(m)]
    need(all(sum(row)==0 for row in Pi),'projector row sums')
    need(all(sum(Pi[i][j]*P[x][j] for j in range(m))==0 for i in range(m) for x in range(v)),'projector kills P')
    need(all(sum(Pi[i][k]*Pi[k][j] for k in range(m))==Pi[i][j] for i in range(m) for j in range(m)),'projector idempotence')
    const={}
    for label,A,gap in [('centered',Q,delta),('repaired',Qm,delta/2)]:
        G=[[N*len(I)*(i==j)-sum(A[x][y] for x in I for y in J)
            -gap*(len(I)*(i==j)-F(len(I)*len(J),N))
            for j,J in enumerate(layers)] for i,I in enumerate(layers)]
        need(psd_rank(G)==3 and not any(matvec(G,[1]*4)),'buffered full constant restriction')
        const[label]=3
    need(max(sum(abs(x) for x in row) for row in E)==4*m*(v-2)*(v-3)//2,'trade norm')
    return {**dat,'pair_Gram_entries_checked':m*m,'projector_entries_checked':m*m,
      'full_constant_buffered_upper_ranks':const,'upper_PSD_ranks':{'centered_buffered_upper':N-1,'repaired_buffered_upper':N-1}}

def finite(v,l,U,generation):
    V,Q,Qm,E,info=matrices(v,l,sorted(U));N=len(V)
    proof=certify(V,Q,Qm,E,v,l,weights(v,l));ranks=proof['lower_ranks'].copy()
    # Dense elimination is restricted to <=57 here; the118-point case has a
    # complete universal incidence/Schur and projection certificate instead.
    dense={}
    if N<=57:
        for label,A in [('centered_lower',Q),('repaired_lower',Qm)]:
            rr=integer_psd(A);need(rr==ranks[label],'whole dense lower rank');dense[label]=rr
    if (v,l) in ((7,4),(9,6)):
        upper=upper_certificate(V,Q,Qm,E,v,l);proof['upper']=upper;ranks.update(upper['upper_PSD_ranks'])
        if N<=57:
            for label,A,gap in [('centered_buffered_upper',Q,F(upper['delta'])),('repaired_buffered_upper',Qm,F(upper['repaired_buffer']))]:
                rr=integer_psd(buffer(A,gap));need(rr==N-1,'whole dense upper rank');dense[label]=rr
    # Both singular choices disappear entrywise: only Z, H and disjoint
    # triple positions can carry t. The exhaustive six-point identity check
    # establishes this for every labelled input, not just this witness.
    if (v,l) in ((5,3),(6,2)):
        p,T,P,C,B,R,H,Z,_=incidence(v,l,sorted(U))
        coefficient=3 if v==5 else 1
        need(not any(z for row in Z for z in row) and all(H[x][j]==coefficient*(1-B[x][j]) for x in range(v) for j in range(len(T))) and all(A&C for A,C in combinations(T,2)),'singular t matrix invariance')
        info['t_independent_entire_matrix']=True
    info.update(generation=generation,blocks=sorted(U),complete_structural_certificate=proof,
      certified_PSD_ranks=ranks,whole_dense_PSD_ranks=dense,centered_sha256=matrix_hash(Q,V),repaired_sha256=matrix_hash(Qm,V))
    print('validated independent input',v,l,'N',N,'ranks',ranks,file=sys.stderr,flush=True)
    return info

def run():
    scalar=scalar_run();control=controls();six,census=enumerate_six()
    rows=[finite(v,l,U,g) for v,l,U,g in fixtures(six)]
    rejects=[]
    U=set(rows[-1]['blocks'])
    for name,v,l,blocks in [('too_small',4,2,sorted(U)),('invalid_v5',5,2,sorted(U)),('invalid_v6',6,3,sorted(U)),('too_many',7,6,sorted(U)),('noninteger',7.0,2,sorted(U)),('missing',9,6,sorted(U)[:-1]),('duplicate',9,6,sorted(U)+[min(U)])]:
        try:incidence(v,l,blocks)
        except ValueError:rejects.append(name)
        else:raise ValueError('invalid design accepted:'+name)
    return {'agent':'six-reviewer-5','role':'independent mathematical reviewer',
      'trust':'CPython3 stdlib exact integers/Fraction and complete ordinary mathematical reduction; no author imports',
      'scalar':scalar,'engine_controls':control,'six_point_exhaustive_check':census,'finite_inputs':rows,
      'design_controls_rejected':rejects,'structural_PSD_forms':sum(len(x['certified_PSD_ranks']) for x in rows),
      'whole_dense_PSD_forms':sum(len(x['whole_dense_PSD_ranks']) for x in rows)}

if __name__=='__main__':
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--write',type=Path);g.add_argument('--check',type=Path);a=p.parse_args();out=run()
    if a.write:a.write.write_text(json.dumps(out,indent=2)+'\n')
    else:need(out==json.loads(a.check.read_text()),'independent expected mismatch')
    print(json.dumps({'status':'passed','structural_PSD_forms':out['structural_PSD_forms'],
      'whole_dense_PSD_forms':out['whole_dense_PSD_forms'],'canonical_sha256':digest(out)}))
