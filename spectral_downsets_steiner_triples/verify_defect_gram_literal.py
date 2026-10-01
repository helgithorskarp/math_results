"""Full structural certificates on three worst absolute-row cyclic13 inputs.

Checks every block/constant, full point Gram identities including missing
triples, small Fraction PSD forms and exact full repair transfer. Whole
upper PSD follows the written exhaustive-mode proof; whole lower PSD/ranks
are inherited from the reviewed all-orders theorem. No dense full slack
eliminations. These three fixtures supplement the complete cohort verifier.
six-downset-2, researcher. Standard library; assertions enabled.
"""
import argparse
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
from cyclic13_gram import orbit_partition,blocks_from_mask
from defect_gram import (row_defect_data,centered_certificate,maximal_certificate,
                         scalar_data,strict_root_upper)
from uniform_lambda_small import design_data,weights
from verify import check_definition,exact_psd_rank,matrix_hash,rejects
from verify_three9 import buffered_upper,gram_rank
from verify_uniform_lambda_small import incidence_check
from verify_dense_lambda import complement_check
from verify_dense_row_lambda import transfer_check


def gram(A,T=None):
    if T is None:T=A
    return [[sum(a*b for a,b in zip(x,y))for y in T]for x in A]


def block_check(D,s,Q,v,lam,blocks,bound):
    """All six literal Q-J blocks, before discarding their J terms."""
    _,completing,codegrees,H=design_data(v,lam,blocks)
    c,d,t,w,h=[weights(v,lam)[key]for key in ('c','d','t','w','h')]
    layers={k:[i for i,A in enumerate(D)if A.bit_count()==k]for k in range(4)}
    assert all(Q[0][j]==Q[j][0]==1 for j in range(len(D)))
    checked={};u=lam*(lam-1)//2
    for ka,kb in ((1,1),(1,2),(1,3),(2,2),(2,3),(3,3)):
        count=0
        for i in layers[ka]:
            a=D[i]
            for j in layers[kb]:
                b=D[j];inter=(a&b).bit_count()
                if (ka,kb)==(1,1):
                    Z=codegrees[a|b]-u if i!=j else 0
                    value=(s+F(lam,3))*int(i==j)+t*Z-F(lam,3)-1
                elif (ka,kb)==(1,2):
                    value=-w*inter-d*int(a in completing[b])+w-1
                elif (ka,kb)==(1,3):
                    value=-h*inter-t*H[b].get(a.bit_length()-1,0)+h-1
                elif (ka,kb)==(2,2):value=(s+c)*int(i==j)-c*inter+c-1
                elif (ka,kb)==(2,3):value=d*(int(a&b==a)-inter)+d-1
                else:value=(s-t)*int(i==j)+t*F(inter*(inter-1),2)-t*inter+t-1
                assert Q[i][j]-1==value,(ka,kb,a,b)
                count+=1
        checked[str(ka)+str(kb)]=count
    rows=[]
    for ka in range(4):
        row=[]
        for kb in range(4):
            values={sum(Q[i][j]-1 for j in layers[kb])for i in layers[ka]}
            assert len(values)==1;row.append(values.pop())
        rows.append(row)
    constant_gram=[[len(layers[i])*rows[i][j]for j in range(1,4)]for i in range(1,4)]
    assert exact_psd_rank(constant_gram)==1
    alpha=sum(rows[k][k]for k in range(4))
    assert alpha==F(lam*(v+7),6)+1 and 0<alpha<s<bound
    return {'all_six_block_entries':checked,'empty_L_row_zero':True,
        'layer_constant_Gram_rank':1,'layer_constant_positive_eigenvalue':str(alpha),
        'layer_regular_row_sums':[[str(z)for z in row]for row in rows]}


def point_gram_check(v,lam,blocks,data,Z):
    pairs,completing,_,outside=design_data(v,lam,blocks)
    U=set(blocks)
    missing=[sum(1<<x for x in a)for a in combinations(range(v),3)
             if sum(1<<x for x in a)not in U]
    P=[[int(p>>x&1)for p in pairs]for x in range(v)]
    C=[[int(1<<x in completing[p])for p in pairs]for x in range(v)]
    B=[[int(a>>x&1)for a in blocks]for x in range(v)]
    H=[[outside[a].get(x,0)for a in blocks]for x in range(v)]
    R=[[int(p&a==p)for a in blocks]for p in pairs]
    Rq=[[int(p&a==p)for a in missing]for p in pairs]
    # Multiply literal completion and missing pair/triple incidence.
    FF=[[sum(C[x][j]*Rq[j][i]for j in range(len(pairs)))
         for i in range(len(missing))]for x in range(v)]
    q=v-2-lam;r=lam*(v-1)//2
    assert all(sum(row)==q*r for row in FF)
    assert all(sum(FF[x][j]for x in range(v))==3*lam for j in range(len(missing)))
    RB=gram(R,B)
    assert all(RB[j][x]==lam*P[x][j]+C[x][j]
               for j in range(len(pairs))for x in range(v))
    HB=gram(H,B);BH=gram(B,H);HH=gram(H);FFgram=gram(FF)
    u=lam*(lam-1)//2
    c,d,t,w,h=[weights(v,lam)[key]for key in ('c','d','t','w','h')]
    A12=[[w*p+d*z for p,z in zip(P[x],C[x])]for x in range(v)]
    A13=[[h*p+t*z for p,z in zip(B[x],H[x])]for x in range(v)]
    G12=gram(A12);G13=gram(A13)
    for x in range(v):
        for y in range(v):
            I=int(x==y)
            assert HB[x][y]==BH[x][y]==Z[x][y]+3*u*(1-I)
            assert HH[x][y]==data['alphaH']*I+(v-6)*Z[x][y]+data['betaH']-FFgram[x][y]
            assert G12[x][y]==data['mu12']*I+d*d*Z[x][y]+data['nu12']
            assert G13[x][y]==data['mu13']*I+data['zcoef13']*Z[x][y]+data['nu13']-t*t*FFgram[x][y]
    k12=(w*(v-1)+d*r)*(2*w+d*lam)
    k13=3*r*(h+t*(lam-1))**2
    assert all(sum(row)==k12 for row in G12)
    assert all(sum(row)==k13 for row in G13)
    assert data['mu12']+v*data['nu12']==k12
    assert data['mu13']+v*data['nu13']-t*t*3*lam*q*r==k13
    K=[[F(x==y)-F(1,v)for y in range(v)]for x in range(v)]
    forms={'point_defect':[[data['gamma']*K[x][y]-Z[x][y]for y in range(v)]for x in range(v)],
        'point_pair_Gram_upper':[[data['rho'][0]*K[x][y]-G12[x][y]+F(k12,v)
                                for y in range(v)]for x in range(v)],
        'point_triple_Gram_upper':[[data['rho'][1]*K[x][y]-G13[x][y]+F(k13,v)
                                  for y in range(v)]for x in range(v)]}
    ranks={key:exact_psd_rank(matrix)for key,matrix in forms.items()}
    assert set(ranks.values())=={v-1}
    return {'complete_point_Gram_identities':4,'all_Gram_entries_per_identity':v*v,
        'full_RB_transpose_identity_entries':len(pairs)*v,
        'missing_triples':len(missing),'missing_completion_row_sum':q*r,
        'missing_completion_column_sum':3*lam,'small_Fraction_PSD_ranks':ranks,
        'small_Fraction_matrix_hashes':{key:matrix_hash(matrix)for key,matrix in forms.items()},
        'complete_missing_Gram_sha256':matrix_hash(FFgram)}


def run():
    orbit,_=orbit_partition();out={'agent':'six-downset-2','role':'researcher','inputs':[]}
    principal_forms=0
    for lam,orbit_mask in ((4,23768),(5,40920),(6,106488)):
        v=13;blocks=blocks_from_mask(orbit_mask,orbit)
        data,Z,actual=row_defect_data(v,lam,blocks,28);assert actual==28
        D,s,Qc=centered_certificate(v,lam,blocks)
        _,_,Qm,eta=maximal_certificate(v,lam,blocks,(D,s,Qc))
        check_definition(D,s,Qc,psd=False);check_definition(D,s,Qm,psd=False)
        N=len(D);delta=data['delta'];G=data['G'];bound=data['B']
        comparison=[[F(bound if i==j else 0)-G[i][j]for j in range(3)]for i in range(3)]
        assert exact_psd_rank(comparison)==3
        structure=block_check(D,s,Qc,v,lam,blocks,bound)
        point=point_gram_check(v,lam,blocks,data,Z)
        forms={'centered':Qc,'maximal':Qm,
            'centered_buffer':buffered_upper(Qc,delta),'maximal_buffer':buffered_upper(Qm,delta/2)}
        predicted={'centered':N-v-1,'maximal':N-v,'centered_buffer':N-1,'maximal_buffer':N-1}
        indices=[i for i,A in enumerate(D)if A.bit_count()<=1]
        for matrix in forms.values():
            assert exact_psd_rank([[matrix[i][j]for j in indices]for i in indices])==v+1
            principal_forms+=1
        stars=[[F(bool(A>>x&1))-F(s,N)for A in D]for x in range(v)]
        empty=[F(i==0)-F(1,N)for i in range(N)]
        assert gram_rank(stars)==v and gram_rank(stars+[empty])==v+1
        transfer=transfer_check(Qc,Qm,eta,delta,v)
        assert eta==F(1,1352) and transfer['strict_transfer_margin']==str(data['half_gap_margin'])
        out['inputs'].append({'name':'cyclic13_lambda'+str(lam)+'_row28','v':v,'lambda':lam,
            'orbit_mask':orbit_mask,'N':N,'s':s,'blocks':blocks,'absolute_row_defect':actual,
            'predicted_ranks_from_written_proof':predicted,'direct_full_Schur_forms':0,
            'eta':str(eta),'B':str(bound),'delta':str(delta),'g':str(data['g']),
            'half_gap_margin':str(data['half_gap_margin']),'Q00':str(Qm[0][0]),
            'comparison_matrix':[[str(z)for z in row]for row in G],
            'comparison_Fraction_PSD_rank':3,'principal_Fraction_forms':4,
            'hashes':{key:matrix_hash(matrix)for key,matrix in forms.items()},
            'structural_upper':structure,'point_Gram':point,'upper_transfer':transfer,
            **incidence_check(v,lam,blocks),**complement_check(v,lam,blocks)})
    controls=[]
    def reject(name,call):rejects(call);controls.append(name)
    reject('insufficient_defect_row_bound',lambda:row_defect_data(v,lam,blocks,27))
    reject('missing_block',lambda:centered_certificate(v,lam,blocks[:-1]))
    reject('repeated_block',lambda:centered_certificate(v,lam,blocks+[blocks[0]]))
    reject('outside_order_floor',lambda:scalar_data(6,2,28))
    reject('outside_multiplicity_floor',lambda:scalar_data(13,1,28))
    reject('negative_defect_bound',lambda:scalar_data(v,lam,-1))
    reject('negative_radical',lambda:strict_root_upper(F(-1)))
    reject('oversized_eta',lambda:maximal_certificate(v,lam,blocks,(D,s,Qc),eta=F(1,676)))
    reject('zero_eta',lambda:maximal_certificate(v,lam,blocks,(D,s,Qc),eta=F(0)))
    damaged=[row[:]for row in Qc];i,j=[i for i,A in enumerate(D)if A.bit_count()==1][:2]
    damaged[i][j]+=weights(v,lam)['t'];damaged[j][i]=damaged[i][j]
    reject('corrupted_completion_codegree',lambda:check_definition(D,s,damaged,psd=False))
    reject('corrupted_literal_block',lambda:block_check(D,s,damaged,v,lam,blocks,bound))
    _,_,_,outside=design_data(v,lam,blocks);clamped=[row[:]for row in Qc];changed=0
    for i,a in enumerate(D):
        if a.bit_count()==1:
            for j,b in enumerate(D):
                if b.bit_count()==3 and not a&b:
                    f=outside[b].get(a.bit_length()-1,0)
                    if f>1:clamped[i][j]=clamped[j][i]=Qc[i][j]+weights(v,lam)['t']*(f-1);changed+=1
    assert changed>0
    reject('clamped_outside_multiplicity',lambda:check_definition(D,s,clamped,psd=False))
    broken=[row[:]for row in Z];broken[0][1]+=1
    reject('corrupted_point_Gram_identity',lambda:point_gram_check(v,lam,blocks,data,broken))
    reject('false_zero_comparison_cap',lambda:exact_psd_rank([[-z for z in row]for row in G]))
    reject('indefinite_zero_diagonal',lambda:exact_psd_rank([[F(0),F(1)],[F(1),F(0)]]))
    out['rejection_controls']=controls;out['direct_full_Schur_forms']=0
    out['independent_principal_Fraction_forms']=principal_forms
    out['complete_small_Gram_Fraction_forms']=9
    assert principal_forms==12 and len(out['inputs'])==3 and len(controls)==15
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--write-expected',action='store_true')
    args=p.parse_args();assert not(args.check and args.write_expected);out=run()
    expected=Path(__file__).with_name('defect_gram_literal_expected.json')
    if args.check:assert out==json.loads(expected.read_text()),'expected output mismatch'
    if args.write_expected:expected.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
