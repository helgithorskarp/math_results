#!/usr/bin/env python3
"""Independent complete dense cap certificates; no author imports or CAS."""
import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
import sys
from exact import need,matvec,psd_rank,controls
from literal import mask,rotate,digest,parameters,weights,incidence,matrices,matrix_hash
from lower import certify
from scalar import run as scalar_run

def cyclic_missing(n,target,extra_step=None):
    """Bounded first-witness orbit construction in decreasing canonical order.

    Fixed n=11/13 prime makes every triple orbit full. No isomorphism census
    or nonexistence assertion is made if construction fails or hits its cap.
    """
    need(n in (11,13),'unsupported prime witness order')
    reps=sorted({min(rotate(mask(c),j,n) for j in range(n)) for c in combinations(range(n),3)},reverse=True)
    vectors=[]
    for A in reps:
        pts=[x for x in range(n) if A>>x&1]
        counts=Counter(min((x-y)%n,(y-x)%n) for x,y in combinations(pts,2))
        vectors.append([counts[i] for i in range(1,(n+1)//2)])
        need(len({rotate(A,j,n) for j in range(n)})==n,'short triple orbit')
    slots=sum(target)//3;nodes=0
    def choose(start,picks,deficit):
        nonlocal nodes
        nodes+=1;need(nodes<=10000,'witness construction operational cap')
        if len(picks)==slots:return picks if not any(deficit) else None
        for i in range(start,len(reps)):
            if all(a<=b for a,b in zip(vectors[i],deficit)):
                ans=choose(i+1,picks+[i],[b-a for a,b in zip(vectors[i],deficit)])
                if ans is not None:return ans
        return None
    picks=choose(0,[],list(target));need(picks is not None,'bounded construction produced no witness')
    U={rotate(reps[i],j,n) for i in picks for j in range(n)}
    if extra_step is not None:U.update(mask((n,i,(i+extra_step)%n)) for i in range(n))
    return U,{'modulus':n,'reverse_canonical_seeds':[reps[i] for i in picks],
      'difference_targets':list(target),'extra_cycle_step':extra_step,'search_nodes':nodes}

def fixtures():
    yield 12,10,set(),{'kind':'complete triple layer'}
    missing,g=cyclic_missing(13,[1]*6)
    yield 13,10,missing,g
    missing,g=cyclic_missing(11,[2,1,2,2,2],extra_step=2)
    yield 12,8,missing,g

def upper(V,Q,Qm,E,v,l):
    q=v-2-l;need(q>=0 and v>=12 and v>=4*(q+1),'dense domain')
    m,b,r,s,N=parameters(v,l);w=weights(v,l);c,d,t=w['c'],w['d'],w['t']
    need(0<c<F(4,3) and 0<d<2 and 1<t<2 and abs(d-w['w'])<1 and abs(3*t-w['h'])<2,'dense weight signs')
    layers=[[i for i,A in enumerate(V) if A.bit_count()==j] for j in range(4)]
    pairs=[V[i] for i in layers[2]];T=[V[i] for i in layers[3]]
    missing={mask(a) for a in combinations(range(v),3)}-set(T)
    P=[[int(A>>x&1) for A in pairs] for x in range(v)]
    Cq=[[int(not(A>>x&1) and A|(1<<x) in missing) for A in pairs] for x in range(v)]
    Bp=[[int(A>>x&1) for A in T] for x in range(v)]
    R=[[int(A&C==A) for C in T] for A in pairs]
    Rq=[[int(A&C==A) for C in sorted(missing)] for A in pairs]
    need(all(sum(row)==q for row in Rq),'missing pair degrees')
    need(all(sum(row)==q*(v-1)//2 for row in Cq) and all(sum(Cq[x][i] for x in range(v))==q for i in range(m)),'missing completion normalization')
    Z=[[sum(a*b for a,b in zip(Cq[x],Cq[y]))-F(q*(v-q),2)*(x==y)-F(q*(q-1),2) for y in range(v)] for x in range(v)]
    need(all(Z[x][x]==0 and sum(Z[x])==0 for x in range(v)),'missing defect normalization')
    PtP=[[sum(P[x][i]*P[x][j] for x in range(v)) for j in range(m)] for i in range(m)]
    for i in range(m):
        for j in range(m):
            need(sum(a*b for a,b in zip(R[i],R[j]))+sum(a*b for a,b in zip(Rq[i],Rq[j]))==(v-4)*(i==j)+PtP[i][j],'complete pair Gram')
    Pi=[[F(i==j)-F(PtP[i][j],v-2)+F(2,(v-2)*(v-1)) for j in range(m)] for i in range(m)]
    need(all(sum(row)==0 for row in Pi),'projector row sums')
    need(all(sum(Pi[i][j]*P[x][j] for j in range(m))==0 for i in range(m) for x in range(v)),'projector kills P')
    # Literal identities for every full upper block, including all J terms.
    for x,ii in enumerate(layers[1]):
        for y,jj in enumerate(layers[1]):need(Q[ii][jj]==(s+F(l,3))*(x==y)-F(l,3)+t*Z[x][y],'full point block')
        for i,jj in enumerate(layers[2]):need(Q[ii][jj]==(d-w['w'])*P[x][i]+d*Cq[x][i]+w['w']-d,'full point/pair block')
        for i,jj in enumerate(layers[3]):need(Q[ii][jj]==(w['h']-3*t)*(1-Bp[x][i])+t*sum(Cq[x][j]*R[j][i] for j in range(m)),'full point/triple block')
    for i,ii in enumerate(layers[2]):
        for j,jj in enumerate(layers[3]):need(Q[ii][jj]==d*(R[i][j]-(pairs[i]&T[j]).bit_count()+1),'full pair/triple block')
    old=F(s)+F(v*v,2)+(q*q+2*q+F(3,2))*v-10
    new=F(s)+F(v*v,4)+(q*q+2*q+4)*v-16
    need(old-new==F((v-4)*(v-6),4)>0,'new cap improvement')
    need(F(v+6,4)**2>2*v-6 and F(v-4,2)>1,'new direct operator norm comparisons')
    crossnew=F((v-4)*(v+6),4)
    rowcap=max(F(s)+(q*q+F(3,2)*q+F(13,6))*v,F(s)+F(v*v,4)+(2*q+4)*v-16)
    need(rowcap<=new and rowcap<old,'row maximum cap')
    output={}
    for name,bound,cross in [('original',old,F(v*(v-4),2)),('improved',new,crossnew),('row_maximum',rowcap,crossnew)]:
        G=[[s+F(v,3)+q*(q-1)*v,F(v,3)+F(q*v,2),(F(3,2)+2*q)*v],
          [F(v,3)+F(q*v,2),s+F(4,3),cross],[(F(3,2)+2*q)*v,cross,s+2*(v-5)]]
        M=[[bound*(i==j)-G[i][j] for j in range(3)] for i in range(3)]
        margins=[bound-sum(row) for row in G]
        need(all(z>=0 for z in margins) and margins[1]>0 and G[0][1]>0 and G[1][2]>0 and psd_rank(M)==3,'full three-layer strict comparison')
        delta=N-bound;loss=F(m*(v-2)*(v-3),4*v*v)
        need(delta/2>loss and bound>F(l*(v+7),6)+1,'constant cap or real-interval buffer')
        constant_ranks={}
        for form,A,gap in [('centered_buffered_upper',Q,delta),('repaired_buffered_upper',Qm,delta/2)]:
            C=[[N*len(I)*(i==j)-sum(A[x][y] for x in I for y in J)-gap*(len(I)*(i==j)-F(len(I)*len(J),N)) for j,J in enumerate(layers)] for i,I in enumerate(layers)]
            need(psd_rank(C)==3 and not any(matvec(C,[1]*4)),'full four-layer upper constant restriction')
            constant_ranks[form]=3
        output[name]={'cap':str(bound),'delta':str(delta),'repaired_buffer':str(delta/2),
          'repair_loss_at_max_eta':str(loss),'strict_repair_margin_above_half_gap':str(delta/2-loss),
          'comparison_matrix':[[str(a) for a in row] for row in G],
          'row_margins':list(map(str,margins)),'comparison_rank':3,'constant_restriction_ranks':constant_ranks,
          'upper_ranks':{'centered_buffered_upper':N-1,'repaired_buffered_upper':N-1}}
    return {'certificate':'Complete constant/mean-zero incidence comparison; not whole dense elimination',
      'q':q,'missing_blocks':sorted(missing),'Z_values':list(map(str,sorted({a for row in Z for a in row}))),
      'pair_Gram_entries_checked':m*m,'projector_entries_constructed':m*m,
      'projector_annihilation_checks':m*v,'constant_and_mean_zero_completeness':'written universal proof',
      'caps':output}

def finite(v,l,missing,generation):
    allT={mask(c) for c in combinations(range(v),3)};U=allT-missing
    V,Q,Qm,E,info=matrices(v,l,sorted(U))
    lower=certify(V,Q,Qm,E,v,l,weights(v,l));caps=upper(V,Q,Qm,E,v,l)
    ranks=lower['lower_ranks'].copy()
    for name,z in caps['caps'].items():
        for k,rr in z['upper_ranks'].items():ranks[name+'_'+k]=rr
    info.update(generation=generation,blocks=sorted(U),lower_certificate=lower,
      upper_certificate=caps,complete_structural_PSD_ranks=ranks,
      centered_sha256=matrix_hash(Q,V),repaired_sha256=matrix_hash(Qm,V))
    print('validated independent dense input',v,l,'q',v-l-2,'N',len(V),'ranks',ranks,file=sys.stderr,flush=True)
    return info

def run():
    scalar=scalar_run();control=controls();rows=[finite(v,l,missing,g) for v,l,missing,g in fixtures()]
    rejected=[]
    for v,l in ((11,8),(12,6),(13,7)):
        try:
            q=v-2-l;need(type(v) is int and type(l) is int and v>=12 and q>=0 and v>=4*(q+1),'dense domain')
        except ValueError:rejected.append([v,l])
        else:raise ValueError('outside dense domain accepted')
    return {'agent':'six-reviewer-5','role':'independent mathematical reviewer','trust':'CPython exact stdlib Fraction; complete written mode proof; no author imports',
      'scalar':scalar,'engine_controls':control,'finite_inputs':rows,'out_of_domain_controls':rejected,
      'complete_structural_PSD_forms':sum(len(x['complete_structural_PSD_ranks']) for x in rows),
      'whole_dense_PSD_forms':0}

if __name__=='__main__':
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--write',type=Path);g.add_argument('--check',type=Path);a=p.parse_args();x=run()
    if a.write:a.write.write_text(json.dumps(x,indent=2)+'\n')
    else:need(x==json.loads(a.check.read_text()),'independent expected mismatch')
    print(json.dumps({'status':'passed','complete_structural_PSD_forms':x['complete_structural_PSD_forms'],'whole_dense_PSD_forms':0,'canonical_sha256':digest(x)}))
