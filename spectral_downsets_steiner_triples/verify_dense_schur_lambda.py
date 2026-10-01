"""Literal structural control for the dense three-layer Sylvester cap.

One complement of a retained cyclic fourfold13 input, not an enumeration.
Every centered block entry, layer-constant restriction and repair transfer
is checked exactly. Whole-matrix PSD/ranks follow from the written ordinary
bridge and reviewed parent lower theorem; no dense Schur elimination is run.
Four principal Fraction controls supplement, but do not prove, whole PSD.
Standard library only. six-downset-2, researcher.
"""
import argparse
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
from dense_schur_lambda import (cap_bound,cap_gap,comparison_data,
    centered_certificate,fixtures,maximal_certificate,parameters)
from dense_schur_identities import run as identities
from uniform_lambda_small import design_data,weights
from verify import check_definition,exact_psd_rank,matrix_hash,rejects
from verify_three9 import buffered_upper,gram_rank
from verify_uniform_lambda_small import incidence_check
from verify_dense_lambda import complement_check


def block_check(D,s,Q,v,lam,blocks):
    """All six nonempty blocks, including their constant J terms."""
    pairs,_,codegrees,_=design_data(v,lam,blocks)
    ww=weights(v,lam);c,d,t,w,h=[ww[key]for key in ('c','d','t','w','h')]
    alltriples={sum(1<<x for x in p)for p in combinations(range(v),3)}
    missing=alltriples-set(blocks);u=lam*(lam-1)//2
    layers={k:[i for i,A in enumerate(D)if A.bit_count()==k]for k in range(4)}
    assert all(Q[0][j]==Q[j][0]==1 for j in range(len(D)))
    checked={}
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
                    Cq=int(not inter and a|b in missing)
                    value=(d-w)*inter+d*Cq+w-d-1
                elif (ka,kb)==(1,3):
                    CqR=sum(int(not a&p and a|p in missing)for p in pairs if p&b==p)
                    value=(3*t-h)*inter+t*CqR+h-3*t-1
                elif (ka,kb)==(2,2):
                    value=(s+c)*int(i==j)-c*inter+c-1
                elif (ka,kb)==(2,3):
                    value=d*(int(a&b==a)-inter)+d-1
                else:
                    value=(s-t)*int(i==j)+t*F(inter*(inter-1),2)-t*inter+t-1
                assert Q[i][j]-1==value,(ka,kb,a,b)
                count+=1
        checked[str(ka)+str(kb)]=count
    # Exact regularity separates all layer constants from layerwise zero sums.
    row_sums={}
    for ka in range(4):
        row_sums[ka]=[]
        for kb in range(4):
            values={sum(Q[i][j]-1 for j in layers[kb])for i in layers[ka]}
            assert len(values)==1
            row_sums[ka].append(values.pop())
    constant_gram=[[len(layers[i])*row_sums[i][j]for j in range(1,4)]for i in range(1,4)]
    assert all(constant_gram[i][j]==constant_gram[j][i]for i in range(3)for j in range(3))
    assert exact_psd_rank(constant_gram)==1
    alpha=sum(row_sums[k][k]for k in range(4))
    assert alpha==F(lam*(v+7),6)+1 and 0<alpha<s<cap_bound(v,lam)
    return {'all_six_block_entries':checked,'empty_L_row_zero':True,
        'layer_constant_Gram_rank':1,'layer_constant_positive_eigenvalue':str(alpha),
        'layer_regular_row_sums':[[str(z)for z in row_sums[k]]for k in range(4)],
        'scope':'Every literal block entry and complete layer-constant space; ordinary operator-norm bridge supplies all remaining modes.'}


def transfer_check(Qc,Qm,eta,g,v):
    """Weak repair norm margin plus strictly positive centered upper form.

    At the largest permitted eta the norm margin is zero. Strictness comes
    from the positive-definite three-layer comparison, not from that margin.
    """
    N=len(Qc);m=v*(v-1)//2;k=(v-2)*(v-3)//2
    E=[[(Qm[i][j]-Qc[i][j])/eta for j in range(N)]for i in range(N)]
    assert all(sum(row)==0 for row in E)
    bound=max(sum(abs(z)for z in row)for row in E);assert bound<=4*m*k
    margin=g/2-eta*bound;assert margin>=0
    C=buffered_upper(Qc,g);M=buffered_upper(Qm,g/2)
    for i in range(N):
        for j in range(N):
            K=F(i==j)-F(1,N)
            assert M[i][j]==C[i][j]+g*K/2-eta*E[i][j]
    return {'exact_full_entry_transfer_identity':True,'trade_annihilates_constants':True,
        'maximum_absolute_trade_row_sum':str(bound),'allowed_bound_4mk':str(4*m*k),
        'weak_transfer_margin':str(margin),'requires_strict_centered_upper_form':True,
        'interpretation':'Ordinary norm transfer with nonnegative margin; centered comparison supplies strictness. No dense upper elimination.'}


def run():
    out={'agent':'six-downset-2','role':'researcher','identities':identities(),'inputs':[]}
    principal_forms=0
    for name,v,lam,blocks,generation in fixtures():
        D,s,Qc=centered_certificate(v,lam,blocks)
        _,_,Qm,eta=maximal_certificate(v,lam,blocks,(D,s,Qc))
        check_definition(D,s,Qc,psd=False);check_definition(D,s,Qm,psd=False)
        N=len(D);g=cap_gap(v,lam);q=v-2-lam
        G,C,minors,tau=comparison_data(v,lam)
        assert exact_psd_rank(C)==3 and all(z>0 for z in minors) and tau==N-g
        structure=block_check(D,s,Qc,v,lam,blocks)
        info=incidence_check(v,lam,blocks);comp=complement_check(v,lam,blocks)
        forms={'centered':Qc,'maximal':Qm,
            'centered_buffer':buffered_upper(Qc,g),'maximal_buffer':buffered_upper(Qm,g/2)}
        expected={'centered':N-v-1,'maximal':N-v,'centered_buffer':N-1,'maximal_buffer':N-1}
        point_indices=[i for i,A in enumerate(D)if A.bit_count()<=1]
        for matrix in forms.values():
            principal=[[matrix[i][j]for j in point_indices]for i in point_indices]
            assert exact_psd_rank(principal)==v+1;principal_forms+=1
        stars=[[F(bool(A>>x&1))-F(s,N)for A in D]for x in range(v)]
        empty=[F(i==0)-F(1,N)for i in range(N)]
        assert gram_rank(stars)==v and gram_rank(stars+[empty])==v+1
        transfer=transfer_check(Qc,Qm,eta,g,v)
        assert eta==F(1,8*v*v) and transfer['weak_transfer_margin']=='0'
        out['inputs'].append({'name':name,'v':v,'lambda':lam,'q':q,'N':N,'s':s,
            'generation':generation,'blocks':blocks,'weights':{key:str(z)for key,z in weights(v,lam).items()},
            'predicted_ranks_from_written_proof':expected,'direct_full_Schur_forms':0,
            'eta':str(eta),'comparison_matrix':[[str(z)for z in row]for row in G],
            'comparison_Sylvester_minors':[str(z)for z in minors],'comparison_Fraction_PSD_rank':3,
            'B':str(tau),'delta':str(g),'maximal_buffer_gap':str(g/2),
            'Q00':str(Qm[0][0]),'hashes':{key:matrix_hash(matrix)for key,matrix in forms.items()},
            'principal_Fraction_forms':4,'structural_upper':structure,'upper_transfer':transfer,**info,**comp})
    controls=[]
    def reject(name,call):rejects(call);controls.append(name)
    reject('excluded_q6v17',lambda:parameters(17,9))
    reject('order_floor',lambda:parameters(10,8))
    reject('missing_block',lambda:centered_certificate(v,lam,blocks[:-1]))
    reject('repeated_block',lambda:centered_certificate(v,lam,blocks+[blocks[0]]))
    reject('oversized_eta',lambda:maximal_certificate(v,lam,blocks,(D,s,Qc),eta=F(1,v*v)))
    reject('zero_eta',lambda:maximal_certificate(v,lam,blocks,(D,s,Qc),eta=F(0)))
    damaged=[row[:]for row in Qc]
    i,j=[i for i,A in enumerate(D)if A.bit_count()==1][:2]
    damaged[i][j]+=weights(v,lam)['t'];damaged[j][i]=damaged[i][j]
    reject('corrupted_completion_codegree',lambda:check_definition(D,s,damaged,psd=False))
    reject('corrupted_literal_block',lambda:block_check(D,s,damaged,v,lam,blocks))
    _,_,_,outside=design_data(v,lam,blocks);clamped=[row[:]for row in Qc];changed=0
    for i,a in enumerate(D):
        if a.bit_count()==1:
            for j,b in enumerate(D):
                if b.bit_count()==3 and not a&b:
                    f=outside[b].get(a.bit_length()-1,0)
                    if f>1:clamped[i][j]=clamped[j][i]=Qc[i][j]+weights(v,lam)['t']*(f-1);changed+=1
    assert changed>0
    reject('clamped_outside_multiplicity',lambda:check_definition(D,s,clamped,psd=False))
    _,Cbad,bad_minors,_=comparison_data(17,9)
    assert bad_minors[-1]<0
    reject('negative_q6v17_comparison',lambda:exact_psd_rank(Cbad))
    reject('indefinite_zero_diagonal',lambda:exact_psd_rank([[F(0),F(1)],[F(1),F(0)]]))
    out['excluded_q6v17_Sylvester_minors']=[str(z)for z in bad_minors]
    out['excluded_comparison_interpretation']='Failure of this sufficient comparison at +9; no H/cap/design nonexistence conclusion.'
    out['rejection_controls']=controls;out['direct_full_Schur_forms']=0
    out['independent_principal_Fraction_forms']=principal_forms
    assert principal_forms==4 and len(out['inputs'])==1 and len(controls)==11
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--write-expected',action='store_true')
    args=p.parse_args();assert not(args.check and args.write_expected);out=run()
    path=Path(__file__).with_name('dense_schur_expected.json')
    if args.check:assert out==json.loads(path.read_text()),'expected output mismatch'
    if args.write_expected:path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
