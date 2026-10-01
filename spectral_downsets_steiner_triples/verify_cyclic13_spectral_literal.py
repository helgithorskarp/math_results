"""Three noncyclic final matrices after2/3/4 overlapping legal Pasch moves.

All definition, six-block, constant, incidence, complement, point-Gram and
full repair-transfer equations;42 point/comparison Fraction PSD forms and
12 supplementary principal forms. Full lower/upper PSD and ranks follow
the written proofs, with zero whole-slack dense eliminations. Author-side
checks, not an independent reviewer verdict. six-downset-2, researcher.
"""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path
from cyclic13_spectral import certificates,fixtures,initial_point_certificate,comparison_data
from pasch_defect import switch_update,point_defect,perturbation_certificate
from defect_gram import compact_scalars
from uniform_lambda_small import weights,design_data
from verify import check_definition,exact_psd_rank,matrix_hash,rejects
from verify_three9 import buffered_upper,gram_rank
from verify_uniform_lambda_small import incidence_check
from verify_dense_lambda import complement_check
from verify_dense_row_lambda import transfer_check
from verify_defect_gram_literal import block_check,point_gram_check
from verify_cyclic13_spectral import tuple_defect


def run():
    v=13;kappa=F(50,3);out={'agent':'six-downset-2','role':'researcher','inputs':[]}
    principal_forms=0;small_forms=0
    expected=[(F(160,3),F(255,26),(15,44,34)),
              (F(68),F(177,26),(16,51,34)),
              (F(254,3),F(17,13),(18,59,34))]
    for (lam,gamma0,bound,mask,initial,moves),(gamma,required_half,crosses)in zip(fixtures(),expected):
        D,s,Qc,Qm,eta,blocks,Z,data,updates=certificates(v,lam,initial,moves,gamma0,bound)
        assert data['gamma']==gamma and data['B']==bound and data['delta']==len(D)-bound
        assert data['half_gap_margin']==required_half and tuple(data['crosses'])==crosses
        assert not data['row_criterion_sufficient']
        assert Z==tuple_defect(lam,blocks)
        check_definition(D,s,Qc,psd=False);check_definition(D,s,Qm,psd=False)
        K=[[F(x==y)-F(1,v)for y in range(v)]for x in range(v)]
        initialZ=tuple_defect(lam,initial)
        initial_form=[[gamma0*K[x][y]-initialZ[x][y]for y in range(v)]for x in range(v)]
        assert exact_psd_rank(initial_form)==12;small_forms+=1
        current=initial;seen={tuple(current)};step_forms=[];supports=[]
        for i,(groups,reverse)in enumerate(moves):
            current,nextZ,Delta,info=switch_update(v,lam,current,groups,reverse)
            assert nextZ==tuple_defect(lam,current) and Delta==updates[i][0]
            assert tuple(current)not in seen;seen.add(tuple(current))
            supports.append({x for pair in groups for x in pair})
            ranks={};hashes={}
            for sign in (-1,1):
                form=[[kappa*K[x][y]+sign*Delta[x][y]for y in range(v)]for x in range(v)]
                key='kappa_K_'+str(sign)+'_Delta';ranks[key]=exact_psd_rank(form);hashes[key]=matrix_hash(form)
            form=[[(gamma0+(i+1)*kappa)*K[x][y]-nextZ[x][y]for y in range(v)]for x in range(v)]
            ranks['accumulated_gamma_K_minus_Z']=exact_psd_rank(form)
            hashes['accumulated_gamma_K_minus_Z']=matrix_hash(form)
            assert set(ranks.values())=={12};small_forms+=3
            step_forms.append({'step':i+1,**info,'small_Fraction_PSD_ranks':ranks,'small_matrix_sha256':hashes})
        assert current==blocks and set(blocks)!=set(initial)and len(seen)==len(moves)+1
        overlap=[len(supports[i]&supports[i+1])for i in range(len(supports)-1)]
        assert min(overlap)>0 and len({tuple(sorted(row))for row in Z})==13
        assert exact_psd_rank(data['comparison'])==3;small_forms+=1
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
            'N':N,'s':s,'initial_mean_point_gamma':gamma0,'moves':step_forms,
            'initial_point_Fraction_PSD_rank':12,'initial_point_matrix_sha256':matrix_hash(initial_form),
            'mean_point_gamma':str(gamma),'B':str(bound),'delta':str(delta),
            'actual_final_absolute_row':max(sum(map(abs,row))for row in Z),
            'final_point_row_signature_types':13,'no_thirteen_cycle_automorphism':True,
            'consecutive_support_intersection_sizes':overlap,'unique_path_states':len(seen),
            'eta':str(eta),'Q00':str(Qm[0][0]),'scalar_cap':compact_scalars(data),
            'row_bound':str(data['row_bound']),'old_row_criterion_sufficient':False,
            'comparison_Fraction_PSD_rank':3,'comparison_matrix_sha256':matrix_hash(data['comparison']),
            'predicted_ranks_from_written_proofs':predicted,'principal_Fraction_forms':4,
            'hashes':{key:matrix_hash(matrix)for key,matrix in forms.items()},
            'structural_upper':structure,'point_Gram':point,'upper_transfer':transfer,
            **incidence_check(v,lam,blocks),**complement_check(v,lam,blocks)})
    controls=[]
    def reject(name,call):rejects(call);controls.append(name)
    reject('missing_block',lambda:initial_point_certificate(v,lam,initial[:-1],gamma0))
    reject('repeated_block',lambda:initial_point_certificate(v,lam,initial+[initial[0]],gamma0))
    reject('insufficient_initial_mean_point_bound',lambda:initial_point_certificate(v,lam,initial,gamma0-1))
    reject('nonlegal_orientation',lambda:switch_update(v,lam,initial,moves[0][0],not moves[0][1]))
    reject('repeated_support_point',lambda:switch_update(v,lam,initial,((0,1),(2,3),(4,0))))
    reject('support_outside_groundset',lambda:switch_update(v,lam,initial,((0,1),(2,3),(4,13))))
    reject('negative_defect_bound',lambda:comparison_data(v,lam,-1,bound))
    reject('insufficient_Pasch_norm_budget',lambda:perturbation_certificate(v,16))
    reject('zero_eta',lambda:certificates(v,lam,initial,moves,gamma0,bound,eta=0))
    reject('oversized_eta',lambda:certificates(v,lam,initial,moves,gamma0,bound,eta=F(1,676)))
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
    reject('false_zero_joint_cap',lambda:comparison_data(v,lam,gamma,0))
    reject('indefinite_zero_diagonal',lambda:exact_psd_rank([[F(0),F(1)],[F(1),F(0)]]))
    out.update(rejection_controls=controls,direct_full_Schur_forms=0,
        independent_principal_Fraction_forms=principal_forms,complete_small_Fraction_PSD_forms=small_forms,
        additional_layer_constant_PSD_forms=3,all_real_eta_interval='0 < eta <= 1/1352 by the ordinary norm transfer proof')
    assert len(out['inputs'])==3 and principal_forms==12 and small_forms==42 and len(controls)==16
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--write-expected',action='store_true')
    args=p.parse_args();assert not(args.check and args.write_expected);out=run()
    expected=Path(__file__).with_name('cyclic13_spectral_literal_expected.json')
    if args.check:assert out==json.loads(expected.read_text()),'Expected output mismatch'
    if args.write_expected:expected.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
