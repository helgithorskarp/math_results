"""Literal matrices and small exact PSD forms on four noncyclic outputs.

Every defining/block/Gram equation and the full repair transfer is checked.
The unbounded ordinary proofs supply full lower/upper PSD and stated ranks;
no whole slack dense elimination is run. This is an author-side checker,
not an independent reviewer verdict. six-downset-2, researcher.
"""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path
from pasch_defect import certificates,fixtures,switch_update,point_defect,chain_data
from defect_gram import scalar_data,compact_scalars
from uniform_lambda_small import weights,design_data
from verify import check_definition,exact_psd_rank,matrix_hash,rejects
from verify_three9 import buffered_upper,gram_rank
from verify_uniform_lambda_small import incidence_check
from verify_dense_lambda import complement_check
from verify_dense_row_lambda import transfer_check
from verify_defect_gram_literal import block_check,point_gram_check
from verify_pasch_neighbourhood import literal_defect


def run():
    v=13;kappa=F(50,3);out={'agent':'six-downset-2','role':'researcher','inputs':[]}
    principal_forms=0;small_forms=0
    expected=[(F(134,3),F(21152,129),F(5573,1677),(14,41,34)),
              (F(134,3),F(14212,81),F(11140,1053),(14,44,34)),
              (F(134,3),F(12039,65),F(187,10),(14,46,34)),
              (F(184,3),F(14359,65),F(111,130),(16,52,34))]
    for (lam,mask,initial,moves),(gamma,required_B,required_half,crosses)in zip(fixtures(),expected):
        D,s,Qc,Qm,eta,blocks,Z,data,updates=certificates(v,lam,initial,moves)
        assert data['gamma']==gamma and data['B']==required_B
        assert data['half_gap_margin']==required_half and tuple(data['crosses'])==crosses
        assert Z==literal_defect(v,lam,blocks)
        check_definition(D,s,Qc,psd=False);check_definition(D,s,Qm,psd=False)
        K=[[F(x==y)-F(1,v)for y in range(v)]for x in range(v)]
        current=initial;step_forms=[]
        for i,(groups,reverse)in enumerate(moves):
            current,nextZ,Delta,info=switch_update(v,lam,current,groups,reverse)
            assert nextZ==literal_defect(v,lam,current) and Delta==updates[i][0]
            ranks={};hashes={}
            for sign in (-1,1):
                form=[[kappa*K[x][y]+sign*Delta[x][y]for y in range(v)]for x in range(v)]
                key='kappa_K_'+str(sign)+'_Delta';ranks[key]=exact_psd_rank(form);hashes[key]=matrix_hash(form)
            form=[[(28+(i+1)*kappa)*K[x][y]-nextZ[x][y]for y in range(v)]for x in range(v)]
            ranks['accumulated_gamma_K_minus_Z']=exact_psd_rank(form)
            hashes['accumulated_gamma_K_minus_Z']=matrix_hash(form)
            assert set(ranks.values())=={12};small_forms+=3
            step_forms.append({'step':i+1,**info,'small_Fraction_PSD_ranks':ranks,'small_matrix_sha256':hashes})
        assert current==blocks and set(blocks)!=set(initial)
        assert len({tuple(sorted(row))for row in Z})>1
        comparison=[[F(data['B']if i==j else 0)-data['G'][i][j]for j in range(3)]for i in range(3)]
        assert exact_psd_rank(comparison)==3;small_forms+=1
        structure=block_check(D,s,Qc,v,lam,blocks,data['B'])
        point=point_gram_check(v,lam,blocks,data,Z);small_forms+=3
        N=len(D);delta=data['delta']
        forms={'centered':Qc,'maximal':Qm,
            'centered_buffer':buffered_upper(Qc,delta),'maximal_buffer':buffered_upper(Qm,delta/2)}
        predicted={'centered':N-v-1,'maximal':N-v,'centered_buffer':N-1,'maximal_buffer':N-1}
        indices=[i for i,a in enumerate(D)if a.bit_count()<=1]
        for matrix in forms.values():
            assert exact_psd_rank([[matrix[i][j]for j in indices]for i in indices])==14
            principal_forms+=1
        stars=[[F(bool(a>>x&1))-F(s,N)for a in D]for x in range(v)]
        empty=[F(i==0)-F(1,N)for i in range(N)]
        assert gram_rank(stars)==v and gram_rank(stars+[empty])==v+1
        transfer=transfer_check(Qc,Qm,eta,delta,v)
        assert eta==F(1,1352) and transfer['strict_transfer_margin']==str(required_half)
        assert transfer['maximum_absolute_trade_row_sum']=='17160' and Qm[0][0]==F(217,52)
        out['inputs'].append({'name':'lambda'+str(lam)+'_moves'+str(len(moves)),
            'v':v,'lambda':lam,'initial_orbit_mask':mask,'blocks':blocks,
            'N':N,'s':s,'moves':step_forms,'mean_point_gamma':str(gamma),
            'actual_final_absolute_row':max(sum(map(abs,row))for row in Z),
            'final_point_row_signature_types':len({tuple(sorted(row))for row in Z}),
            'no_thirteen_cycle_automorphism':True,'eta':str(eta),'Q00':str(Qm[0][0]),
            'scalar_cap':compact_scalars(data),'comparison_Fraction_PSD_rank':3,
            'predicted_ranks_from_written_proofs':predicted,'principal_Fraction_forms':4,
            'hashes':{key:matrix_hash(matrix)for key,matrix in forms.items()},
            'structural_upper':structure,'point_Gram':point,'upper_transfer':transfer,
            **incidence_check(v,lam,blocks),**complement_check(v,lam,blocks)})
    controls=[]
    def reject(name,call):rejects(call);controls.append(name)
    reject('missing_block',lambda:certificates(v,lam,initial[:-1],moves))
    reject('repeated_block',lambda:certificates(v,lam,initial+[initial[0]],moves))
    reject('insufficient_initial_row_bound',lambda:chain_data(v,lam,initial,moves,gamma0=27))
    reject('nonlegal_orientation',lambda:switch_update(v,lam,initial,moves[0][0],not moves[0][1]))
    reject('repeated_support_point',lambda:switch_update(v,lam,initial,((0,1),(2,3),(4,0))))
    reject('support_outside_groundset',lambda:switch_update(v,lam,initial,((0,1),(2,3),(4,13))))
    reject('negative_defect_bound',lambda:scalar_data(v,lam,-1))
    reject('zero_eta',lambda:certificates(v,lam,initial,moves,eta=0))
    reject('oversized_eta',lambda:certificates(v,lam,initial,moves,eta=F(1,676)))
    damaged=[row[:]for row in Qc];i,j=[i for i,a in enumerate(D)if a.bit_count()==1][:2]
    damaged[i][j]+=weights(v,lam)['t'];damaged[j][i]=damaged[i][j]
    reject('corrupted_completion_entry',lambda:check_definition(D,s,damaged,psd=False))
    reject('corrupted_literal_block',lambda:block_check(D,s,damaged,v,lam,blocks,data['B']))
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
    reject('false_zero_comparison_cap',lambda:exact_psd_rank([[-z for z in row]for row in data['G']]))
    reject('indefinite_zero_diagonal',lambda:exact_psd_rank([[F(0),F(1)],[F(1),F(0)]]))
    out.update({'rejection_controls':controls,'direct_full_Schur_forms':0,
        'independent_principal_Fraction_forms':principal_forms,
        'complete_small_Fraction_PSD_forms':small_forms,
        'all_real_eta_interval':'0 < eta <= 1/1352 by the ordinary norm transfer proof'})
    assert len(out['inputs'])==4 and principal_forms==16 and small_forms==31 and len(controls)==15
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--write-expected',action='store_true')
    args=p.parse_args();assert not(args.check and args.write_expected);out=run()
    expected=Path(__file__).with_name('pasch_stability_expected.json')
    if args.check:assert out==json.loads(expected.read_text()),'Expected output mismatch'
    if args.write_expected:expected.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
