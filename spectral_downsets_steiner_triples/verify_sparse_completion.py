"""Complete literal structural controls for a direct-completion sparse cap.

One cyclic simple2-(21,3,4) input, not an exhaustive design cohort.
Every block and constant mode is checked; complete ordinary norm/Sylvester
interpretation supplies the whole upper form. The reviewed parent supplies
whole lower PSD/ranks. No full512-by-512 dense Schur elimination is run.
Four principal Fraction forms supplement the complete structural certificate.
six-downset-2, researcher. Standard library; assertions enabled.
"""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path
from sparse_completion_lambda import (cap_bound,cap_gap,comparison_data,
    centered_certificate,fixtures,maximal_certificate,parameters)
from sparse_completion_identities import run as identities
from uniform_lambda_small import design_data,weights
from verify import check_definition,exact_psd_rank,matrix_hash,rejects
from verify_three9 import buffered_upper,gram_rank
from verify_uniform_lambda_small import incidence_check
from verify_dense_lambda import complement_check
from verify_dense_row_lambda import transfer_check


def block_check(D,s,Q,v,lam,blocks):
    """Direct-completion incidence, including all six rectangular J terms."""
    _,completing,codegrees,H=design_data(v,lam,blocks)
    ww=weights(v,lam);c,d,t,w,h=[ww[key]for key in ('c','d','t','w','h')]
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
                    Cl=int(a in completing[b])
                    value=-w*inter-d*Cl+w-1
                elif (ka,kb)==(1,3):
                    outside=H[b].get(a.bit_length()-1,0)
                    value=-h*inter-t*outside+h-1
                elif (ka,kb)==(2,2):value=(s+c)*int(i==j)-c*inter+c-1
                elif (ka,kb)==(2,3):value=d*(int(a&b==a)-inter)+d-1
                else:value=(s-t)*int(i==j)+t*F(inter*(inter-1),2)-t*inter+t-1
                assert Q[i][j]-1==value,(ka,kb,a,b)
                count+=1
        checked[str(ka)+str(kb)]=count
    row_sums={}
    for ka in range(4):
        row_sums[ka]=[]
        for kb in range(4):
            values={sum(Q[i][j]-1 for j in layers[kb])for i in layers[ka]}
            assert len(values)==1;row_sums[ka].append(values.pop())
    constant_gram=[[len(layers[i])*row_sums[i][j]for j in range(1,4)]for i in range(1,4)]
    assert all(constant_gram[i][j]==constant_gram[j][i]for i in range(3)for j in range(3))
    assert exact_psd_rank(constant_gram)==1
    alpha=sum(row_sums[k][k]for k in range(4))
    assert alpha==F(lam*(v+7),6)+1 and 0<alpha<s<cap_bound(v,lam)
    return {'all_six_block_entries':checked,'empty_L_row_zero':True,
        'layer_constant_Gram_rank':1,'layer_constant_positive_eigenvalue':str(alpha),
        'layer_regular_row_sums':[[str(z)for z in row_sums[k]]for k in range(4)],
        'scope':'Every literal block and complete constant space; direct-completion norm bounds exhaust all other modes in the ordinary proof.'}


def run():
    out={'agent':'six-downset-2','role':'researcher','identities':identities(),'inputs':[]}
    principal_forms=0
    for name,v,lam,blocks,generation in fixtures():
        D,s,Qc=centered_certificate(v,lam,blocks)
        _,_,Qm,eta=maximal_certificate(v,lam,blocks,(D,s,Qc))
        check_definition(D,s,Qc,psd=False);check_definition(D,s,Qm,psd=False)
        N=len(D);delta=cap_gap(v,lam);g=F((v-1)*(v-2)*(v-3),4*v)
        G,rows=comparison_data(v,lam);B=max(rows)
        C=[[F(B if i==j else 0)-G[i][j]for j in range(3)]for i in range(3)]
        assert exact_psd_rank(C)==3 and delta>g>0
        structure=block_check(D,s,Qc,v,lam,blocks)
        info=incidence_check(v,lam,blocks);comp=complement_check(v,lam,blocks)
        forms={'centered':Qc,'maximal':Qm,
            'centered_buffer':buffered_upper(Qc,delta),'maximal_buffer':buffered_upper(Qm,delta/2)}
        predicted={'centered':N-v-1,'maximal':N-v,'centered_buffer':N-1,'maximal_buffer':N-1}
        point_indices=[i for i,A in enumerate(D)if A.bit_count()<=1]
        for matrix in forms.values():
            principal=[[matrix[i][j]for j in point_indices]for i in point_indices]
            assert exact_psd_rank(principal)==v+1;principal_forms+=1
        stars=[[F(bool(A>>x&1))-F(s,N)for A in D]for x in range(v)]
        empty=[F(i==0)-F(1,N)for i in range(N)]
        assert gram_rank(stars)==v and gram_rank(stars+[empty])==v+1
        transfer=transfer_check(Qc,Qm,eta,delta,v)
        assert eta==F(1,8*v*v) and transfer['strict_transfer_margin']==str((delta-g)/2)
        out['inputs'].append({'name':name,'v':v,'lambda':lam,'N':N,'s':s,'q':v-2-lam,
            'blocks':blocks,'generation':generation,'weights':{key:str(z)for key,z in weights(v,lam).items()},
            'predicted_ranks_from_written_proof':predicted,'direct_full_Schur_forms':0,
            'eta':str(eta),'comparison_matrix':[[str(z)for z in row]for row in G],
            'comparison_rows':[str(z)for z in rows],'comparison_Fraction_PSD_rank':3,
            'B':str(B),'delta':str(delta),'g':str(g),'maximal_buffer_gap':str(delta/2),
            'Q00':str(Qm[0][0]),'hashes':{key:matrix_hash(matrix)for key,matrix in forms.items()},
            'principal_Fraction_forms':4,'structural_upper':structure,'upper_transfer':transfer,**info,**comp})
    controls=[]
    def reject(name,call):rejects(call);controls.append(name)
    reject('outside_v3lambda8',lambda:parameters(19,4))
    reject('outside_order_floor',lambda:parameters(12,2))
    reject('missing_block',lambda:centered_certificate(v,lam,blocks[:-1]))
    reject('repeated_block',lambda:centered_certificate(v,lam,blocks+[blocks[0]]))
    reject('oversized_eta',lambda:maximal_certificate(v,lam,blocks,(D,s,Qc),eta=F(1,4*v*v)))
    reject('zero_eta',lambda:maximal_certificate(v,lam,blocks,(D,s,Qc),eta=F(0)))
    damaged=[row[:]for row in Qc]
    i,j=[i for i,A in enumerate(D)if A.bit_count()==1][:2]
    damaged[i][j]+=weights(v,lam)['t'];damaged[j][i]=damaged[i][j]
    reject('corrupted_completion_codegree',lambda:check_definition(D,s,damaged,psd=False))
    reject('corrupted_direct_block',lambda:block_check(D,s,damaged,v,lam,blocks))
    _,_,_,outside=design_data(v,lam,blocks);clamped=[row[:]for row in Qc];changed=0
    for i,a in enumerate(D):
        if a.bit_count()==1:
            for j,b in enumerate(D):
                if b.bit_count()==3 and not a&b:
                    f=outside[b].get(a.bit_length()-1,0)
                    if f>1:clamped[i][j]=clamped[j][i]=Qc[i][j]+weights(v,lam)['t']*(f-1);changed+=1
    assert changed>0
    reject('clamped_outside_multiplicity',lambda:check_definition(D,s,clamped,psd=False))
    reject('false_zero_comparison_cap',lambda:exact_psd_rank([[-z for z in row]for row in G]))
    reject('indefinite_zero_diagonal',lambda:exact_psd_rank([[F(0),F(1)],[F(1),F(0)]]))
    out['rejection_controls']=controls;out['direct_full_Schur_forms']=0
    out['independent_principal_Fraction_forms']=principal_forms
    assert principal_forms==4 and len(out['inputs'])==1 and len(controls)==11
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--write-expected',action='store_true')
    args=p.parse_args();assert not(args.check and args.write_expected);out=run()
    path=Path(__file__).with_name('sparse_completion_expected.json')
    if args.check:assert out==json.loads(path.read_text()),'expected output mismatch'
    if args.write_expected:path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
