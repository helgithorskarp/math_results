"""Literal controls for the extended maximum-row dense-complement cap.

One complement of the retained nondecomposable threefold13 design.
The default checks all equations, four principal forms and the exact
upper transfer. Optional --full-schur checks the two full lower forms
and centered upper buffer; it avoids the slow repaired upper elimination.
No enumeration.
Universal scope rests on DENSE_ROW_CAP.md. six-downset-2, researcher.
"""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path
import sys
from dense_row_lambda import cap_bound,cap_gap,comparison_rows,centered_certificate,fixtures,maximal_certificate,parameters
from dense_row_identities import run as identities
from content_psd import content_psd_rank
from uniform_lambda_small import design_data,weights
from verify import check_definition,exact_psd_rank,matrix_hash,rejects
from verify_three9 import buffered_upper,gram_rank
from verify_uniform_lambda_small import incidence_check
from verify_dense_lambda import complement_check


def transfer_check(Qc,Qm,eta,delta,v):
    """Literal identity plus strict norm gap, conditional on centered PSD.

    For symmetric E killing constants, ||E||<=max absolute row sum.
    Thus (delta/2)K-eta E >= (delta/2-eta bound)K >0 on 1-perp.
    This is an ordinary norm certificate, not repaired Schur elimination.
    """
    N=len(Qc);m=v*(v-1)//2;k=(v-2)*(v-3)//2
    E=[[(Qm[i][j]-Qc[i][j])/eta for j in range(N)]for i in range(N)]
    assert all(sum(row)==0 for row in E)
    bound=max(sum(abs(z)for z in row)for row in E);assert bound<=4*m*k
    margin=delta/2-eta*bound;assert margin>0
    C=buffered_upper(Qc,delta);M=buffered_upper(Qm,delta/2)
    for i in range(N):
        for j in range(N):
            K=F(i==j)-F(1,N)
            assert M[i][j]==C[i][j]+delta*K/2-eta*E[i][j]
    return {'exact_full_entry_transfer_identity':True,'trade_annihilates_constants':True,
        'maximum_absolute_trade_row_sum':str(bound),'allowed_bound_4mk':str(4*m*k),
        'strict_transfer_margin':str(margin),'requires_centered_upper_PSD':True,
        'interpretation':'Ordinary symmetric operator-norm proof; not repaired upper Schur elimination.'}


def run(full_schur=False):
    out={'agent':'six-downset-2','role':'researcher','identities':identities(),'inputs':[]}
    principal_forms=0
    for name,v,lam,blocks,generation in fixtures():
        D,s,Qc=centered_certificate(v,lam,blocks)
        _,_,Qm,eta=maximal_certificate(v,lam,blocks,(D,s,Qc))
        check_definition(D,s,Qc,psd=False);check_definition(D,s,Qm,psd=False)
        N=len(D);delta=cap_gap(v,lam);q=v-2-lam
        forms={'centered':Qc,'maximal':Qm,
            'centered_buffer':buffered_upper(Qc,delta),
            'maximal_buffer':buffered_upper(Qm,delta/2)}
        expected={'centered':N-v-1,'maximal':N-v,'centered_buffer':N-1,'maximal_buffer':N-1}
        for key,matrix in forms.items():
            if full_schur and key!='maximal_buffer':
                stats={};rank=content_psd_rank(matrix,stats);assert rank==expected[key]
                print('validated',name,key,'N',N,'rank',rank,file=sys.stderr,flush=True)
            point_indices=[i for i,A in enumerate(D)if A.bit_count()<=1]
            principal=[[matrix[i][j]for j in point_indices]for i in point_indices]
            assert exact_psd_rank(principal)==v+1;principal_forms+=1
        stars=[[F(bool(A>>x&1))-F(s,N)for A in D]for x in range(v)]
        empty=[F(i==0)-F(1,N)for i in range(N)]
        assert gram_rank(stars)==v and gram_rank(stars+[empty])==v+1
        info=incidence_check(v,lam,blocks);comp=complement_check(v,lam,blocks)
        transfer=transfer_check(Qc,Qm,eta,delta,v)
        out['inputs'].append({'name':name,'v':v,'lambda':lam,'q':q,'N':N,'s':s,
            'generation':generation,'blocks':blocks,'weights':{key:str(z)for key,z in weights(v,lam).items()},
            'predicted_ranks_from_written_proof':expected,
            'default_direct_full_Schur_forms':0,'optional_direct_full_Schur_forms':['centered','maximal','centered_buffer'],
            'repaired_upper_Schur_omitted':True,'eta':str(eta),'comparison_rows':[str(z)for z in comparison_rows(v,lam)],
            'B':str(cap_bound(v,lam)),'delta':str(delta),'maximal_buffer_gap':str(delta/2),
            'twice_half_gap_margin':str(delta-F(v*(v-1)*(v-2)*(v-3),4*v*v)),
            'half_gap_margin':str((delta-F(v*(v-1)*(v-2)*(v-3),4*v*v))/2),
            'Q00':str(Qm[0][0]),'hashes':{key:matrix_hash(matrix)for key,matrix in forms.items()},
            'principal_Fraction_forms':4,'upper_transfer':transfer,**info,**comp})
    rejects(lambda:parameters(12,7))  # q3 violates 2v>=5q+10.
    rejects(lambda:parameters(10,8))  # Separate order floor.
    rejects(lambda:centered_certificate(v,lam,blocks[:-1]))
    rejects(lambda:centered_certificate(v,lam,blocks+[blocks[0]]))
    rejects(lambda:maximal_certificate(v,lam,blocks,(D,s,Qc),eta=F(1,v*v)))
    rejects(lambda:maximal_certificate(v,lam,blocks,(D,s,Qc),eta=F(0)))
    damaged=[row[:]for row in Qc];_,_,codegrees,outside=design_data(v,lam,blocks)
    # This input has Z_l=0, so erasing the correction would change nothing.
    # Corrupt one completion codegree symmetrically instead.
    point_indices=[i for i,A in enumerate(D)if A.bit_count()==1]
    i,j=point_indices[:2];damaged[i][j]+=weights(v,lam)['t'];damaged[j][i]=damaged[i][j]
    rejects(lambda:check_definition(D,s,damaged,psd=False))
    clamped=[row[:]for row in Qc];changed=0
    for i,a in enumerate(D):
        if a.bit_count()==1:
            for j,b in enumerate(D):
                if b.bit_count()==3 and not a&b:
                    f=outside[b].get(a.bit_length()-1,0)
                    if f>1:clamped[i][j]=clamped[j][i]=Qc[i][j]+weights(v,lam)['t']*(f-1);changed+=1
    assert changed>0
    rejects(lambda:check_definition(D,s,clamped,psd=False))
    rejects(lambda:content_psd_rank(buffered_upper(Qc,N)))
    rejects(lambda:content_psd_rank([[F(0),F(1)],[F(1),F(0)]]))
    out['rejection_controls']=10;out['default_direct_full_Schur_forms']=0
    out['independent_principal_Fraction_forms']=principal_forms
    assert principal_forms==4 and len(out['inputs'])==1
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--write-expected',action='store_true')
    p.add_argument('--full-schur',action='store_true',help='Also eliminate the three optional full forms; upper repair uses the norm transfer.')
    args=p.parse_args();assert not(args.check and args.write_expected);out=run(args.full_schur)
    expected=Path(__file__).with_name('dense_row_expected.json')
    if args.check:assert out==json.loads(expected.read_text()),'expected output mismatch'
    if args.write_expected:expected.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
