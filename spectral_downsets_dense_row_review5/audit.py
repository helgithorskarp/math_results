#!/usr/bin/env python3
"""Independent complete dense cap certificates; no author imports or CAS."""
import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
import sys
from exact import need,matvec,psd_rank,controls,determinant3
from literal import mask,rotate,digest,parameters,weights,incidence,matrices,matrix_hash
from lower import certify
from scalar import run as scalar_run

def cyclic_missing(n,q):
    """Bounded independent first-witness search, not a census.

    Compute each orbit signature from all its actual pair incidences.
    For n=15 force the unique five-element triple orbit; all other used
    orbits are full. No prime-orbit assumption is made at composite order.
    """
    need(n in (13,15),'unsupported literal witness order')
    pairs=[mask(c) for c in combinations(range(n),2)]
    distance={A:min((x-y)%n,(y-x)%n) for A in pairs for x,y in [tuple(i for i in range(n) if A>>i&1)]}
    reps=sorted({min(rotate(mask(c),j,n) for j in range(n)) for c in combinations(range(n),3)},reverse=True)
    orbits=[];vectors=[]
    for A in reps:
        orbit={rotate(A,j,n) for j in range(n)}
        count=Counter(mask(c) for B in orbit for c in combinations([i for i in range(n) if B>>i&1],2))
        vector=[]
        for d in range(1,(n+1)//2):
            values={count[B] for B in pairs if distance[B]==d}
            need(len(values)==1,'nonuniform actual cyclic pair orbit')
            vector.append(values.pop())
        need(sum(vector)*n==3*len(orbit),'orbit signature normalization')
        orbits.append(orbit);vectors.append(vector)
    forced=[i for i,U in enumerate(orbits) if len(U)!=n]
    need((n==13 and not forced) or (n==15 and len(forced)==1 and len(orbits[forced[0]])==5),'short orbit coverage')
    target=[q]*((n-1)//2)
    for i in forced:target=[a-b for a,b in zip(target,vectors[i])]
    candidates=[i for i,U in enumerate(orbits) if len(U)==n]
    slots=sum(target)//3;need(sum(target)%3==0,'witness slot divisibility');nodes=0
    def choose(start,picks,deficit):
        nonlocal nodes
        nodes+=1;need(nodes<=10000,'witness construction operational cap')
        if len(picks)==slots:return picks if not any(deficit) else None
        for j in range(start,len(candidates)):
            i=candidates[j]
            if all(a<=b for a,b in zip(vectors[i],deficit)):
                ans=choose(j+1,picks+[i],[b-a for a,b in zip(vectors[i],deficit)])
                if ans is not None:return ans
        return None
    picks=choose(0,[],target);need(picks is not None,'bounded construction produced no witness')
    U=set().union(*(orbits[i] for i in picks+forced))
    need(all(sum(B&A==A for B in U)==q for A in pairs),'literal missing pair degrees')
    return U,{'modulus':n,'missing_multiplicity':q,'reverse_canonical_seeds':[reps[i] for i in picks],
      'forced_short_orbit_seeds':[reps[i] for i in forced],'actual_orbit_pair_signatures':[vectors[i] for i in picks+forced],
      'search_nodes':nodes,'fixed_node_guard':10000,'interpretation':'first witness only; no census or nonexistence claim'}

def fixtures():
    for v,q in ((13,3),(15,4)):
        missing,g=cyclic_missing(v,q)
        yield v,v-2-q,missing,g

def upper(V,Q,Qm,E,v,l):
    q=v-2-l;need(q>=0 and v>=12 and 2*v>=5*q+10,'dense domain')
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
    x,y=next((x,y) for x in range(v) for y in range(v) if Z[x][y])
    point_row=layers[1][x];point_star=[j for j,A in enumerate(V) if A>>y&1]
    correct_star_sum=sum(Q[point_row][j] for j in point_star)
    erased_star_sum=correct_star_sum-t*Z[x][y]
    need(correct_star_sum==s and sum(Q[point_row])-t*sum(Z[x])==N,
         'defect-erasure control normalization')
    try:need(erased_star_sum==s,'erased defect violates centered-star equation')
    except ValueError:erasure_rejected=True
    else:raise ValueError('erased nonzero completion defect accepted')
    erasure_record={'points':[x,y],'Z_entry':str(Z[x][y]),'row_sum_preserved':True,
        'correct_star_sum':str(correct_star_sum),'erased_star_sum':str(erased_star_sum),
        'rejected':erasure_rejected}
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
    a12=F(v,3)+F(q*v,2);a13=(F(3,2)+2*q)*v
    D1=F(s)+F(l,3)+t*F(q*(q-1)*v,2);D2=F(s)+F(4,3);D3=F(s)+2*(v-5)
    old23=F(v*(v-4),2);new23=F((v-4)*(v+6),4)
    need(F(v+6,4)**2>2*v-6 and old23-new23==F((v-4)*(v-6),4)>0,'direct operator comparison')
    oldG=[[D1,a12,a13],[a12,D2,old23],[a13,old23,D3]]
    newG=[[D1,a12,a13],[a12,D2,new23],[a13,new23,D3]]
    old=max(sum(row) for row in oldG);direct=max(sum(row) for row in newG)
    need(direct==max(sum(newG[0]),sum(newG[2])) and sum(newG[2])>sum(newG[1]),'exact maximal comparison rows')
    M=[[direct*(i==j)-newG[i][j] for j in range(3)] for i in range(3)]
    need(psd_rank(M)==3 and all(direct-sum(row)>=0 for row in newG) and direct-sum(newG[1])>0,'strict connected row comparison')
    determinant=determinant3(M)
    sigma2=sum(M[i][i]*M[j][j]-M[i][j]**2 for i,j in combinations(range(3),2))
    epsilon=determinant/sigma2;tracecap=direct-epsilon
    need(determinant>0 and sigma2>0 and epsilon>0 and tracecap>D1>=s and tracecap<direct<=old,'quantitative inverse-trace cap')
    need(psd_rank([[M[i][j]-epsilon*(i==j) for j in range(3)] for i in range(3)])==3,'inverse-trace lower eigenvalue bridge')
    output={}
    for name,bound,G in [('original',old,oldG),('direct_row',direct,newG),('inverse_trace',tracecap,newG)]:
        M=[[bound*(i==j)-G[i][j] for j in range(3)] for i in range(3)]
        margins=[bound-sum(row) for row in G]
        if name!='inverse_trace':need(all(z>=0 for z in margins) and margins[1]>0,'comparison row signs')
        need(psd_rank(M)==3,'complete three-layer strict upper comparison')
        delta=N-bound;loss=F(m*(v-2)*(v-3),4*v*v)
        need(delta/2>loss and bound>F(l*(v+7),6)+1,'constant cap or full real repair interval')
        constant_ranks={}
        for form,A,gap in [('centered_buffered_upper',Q,delta),('repaired_buffered_upper',Qm,delta/2)]:
            C=[[N*len(I)*(i==j)-sum(A[x][y] for x in I for y in J)-gap*(len(I)*(i==j)-F(len(I)*len(J),N)) for j,J in enumerate(layers)] for i,I in enumerate(layers)]
            need(psd_rank(C)==3 and not any(matvec(C,[1]*4)),'full four-layer upper constant restriction')
            constant_ranks[form]=3
        output[name]={'cap':str(bound),'delta':str(delta),'repaired_buffer':str(delta/2),
          'repair_loss_at_max_eta':str(loss),'actual_half_gap_margin':str(delta/2-loss),
          'doubled_half_gap_margin':str(delta-2*loss),
          'comparison_matrix':[[str(a) for a in row] for row in G],
          'row_margins':list(map(str,margins)),'comparison_rank':3,'constant_restriction_ranks':constant_ranks,
          'upper_ranks':{'centered_buffered_upper':N-1,'repaired_buffered_upper':N-1}}
    output['inverse_trace'].update(positive_row_matrix_determinant=str(determinant),
        principal_2_by_2_minor_sum=str(sigma2),epsilon=str(epsilon),pre_tightening_row_cap=str(direct))
    rounded=(tracecap.numerator+tracecap.denominator-1)//tracecap.denominator
    need(tracecap<rounded<old,'literal boundary rounded cap')
    output['inverse_trace']['rounded_corollary']={'cap':rounded,'delta':N-rounded,
        'repaired_buffer':str(F(N-rounded,2)),
        'actual_half_gap_margin':str(F(N-rounded,2)-loss),
        'interpretation':'Loewner consequence of exact trace cap; not an extra eliminated form'}
    return {'certificate':'Complete constant/mean-zero incidence comparison; not whole dense elimination',
      'q':q,'missing_blocks':sorted(missing),'Z_values':list(map(str,sorted({a for row in Z for a in row}))),
      'erased_defect_control':erasure_record,
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
    for v,l in ((11,8),(12,7),(15,8)):
        try:
            q=v-2-l;need(type(v) is int and type(l) is int and v>=12 and q>=0 and 2*v>=5*q+10,'dense domain')
        except ValueError:rejected.append([v,l])
        else:raise ValueError('outside dense domain accepted')
    return {'agent':'six-reviewer-5','role':'independent mathematical reviewer','trust':'CPython exact stdlib Fraction; complete written mode proof; no author imports',
      'scalar':scalar,'engine_controls':control,'finite_inputs':rows,'out_of_domain_controls':rejected,
      'complete_structural_PSD_forms':sum(len(x['complete_structural_PSD_ranks']) for x in rows),
      'whole_dense_PSD_forms':0}

if __name__=='__main__':
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--write',type=Path);g.add_argument('--check',type=Path);a=p.parse_args();x=run()
    if a.write:a.write.write_text(json.dumps(x,separators=(',',':'))+'\n')
    else:need(x==json.loads(a.check.read_text()),'independent expected mismatch')
    print(json.dumps({'status':'passed','complete_structural_PSD_forms':x['complete_structural_PSD_forms'],'whole_dense_PSD_forms':0,'canonical_sha256':digest(x)}))
