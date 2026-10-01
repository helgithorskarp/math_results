"""Exact full-matrix controls for the dense-complement cap.

Three literal input designs, not an enumeration. Eight full integer
Schur checks on q0/q2 verify lower and buffered upper forms. The q1
input checks definition/incidence and four principal Fraction forms;
its full repaired check exceeded a bounded preliminary batch and is
explicitly omitted. Universal scope rests
on DENSE_COMPLEMENT_CAP.md, not these inputs.
CPython3.11+ stdlib, assertions enabled. six-downset-2, researcher.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
import sys
from certificates import mask
from dense_lambda import cap_bound,cap_gap,centered_certificate,fixtures,maximal_certificate,parameters
from dense_lambda_identities import run as identities
from content_psd import content_psd_rank
from uniform_lambda_small import design_data,weights
from verify import check_definition,exact_psd_rank,matrix_hash,rejects
from verify_three9 import buffered_upper,gram_rank
from verify_uniform_lambda_small import incidence_check
from verify_content_psd import run as backend_controls


def complement_check(v,lam,blocks):
    pairs,Tl,code_l,Hl=design_data(v,lam,blocks);q=v-2-lam
    missing=sorted({mask(p) for p in combinations(range(v),3)}-set(blocks))
    assert len(missing)==q*v*(v-1)//6
    Tq={p:[] for p in pairs};Rq_gram=Counter();Rl_gram=Counter()
    for family,target,gram in ((blocks,Tl,Rl_gram),(missing,Tq,Rq_gram)):
        for A in family:
            contained=[mask(p) for p in combinations([x for x in range(v) if A>>x&1],2)]
            assert len(contained)==3
            for p in contained:
                if family is missing:target[p].append(A^p)
                for p2 in contained:gram[p,p2]+=1
    code_q=Counter()
    for p in pairs:
        assert len(Tq[p])==q and set(Tl[p]).isdisjoint(Tq[p])
        assert set(Tl[p])|set(Tq[p])=={1<<x for x in range(v) if not p>>x&1}
        code_q.update(x|y for x,y in combinations(Tq[p],2))
    for x,y in combinations(range(v),2):
        p=(1<<x)|(1<<y)
        assert code_l[p]-lam*(lam-1)//2==code_q[p]-q*(q-1)//2
    for A in blocks:
        contained=[p for p in pairs if p&A==p]
        for x in range(v):
            count=sum(int(1<<x in Tq[p]) for p in contained)
            assert count==3*int(not A>>x&1)-Hl[A].get(x,0)
    for p in pairs:
        for p2 in pairs:
            assert Rl_gram[p,p2]+Rq_gram[p,p2]==(v-4)*int(p==p2)+(p&p2).bit_count()
    return {'complement_degree':q,'complement_blocks':len(missing),
        'completion_partition':True,'Z_complement_identity':True,
        'outside_cross_identity':True,'complete_pair_Gram_identity':True}


def run():
    out={'agent':'six-downset-2','role':'researcher','identities':identities(),'backend_controls':backend_controls(),'inputs':[]}
    full_forms=principal_forms=0
    for name,v,lam,blocks,generation in fixtures():
        D,s,Qc=centered_certificate(v,lam,blocks)
        _,_,Qm,eta=maximal_certificate(v,lam,blocks,(D,s,Qc))
        check_definition(D,s,Qc,psd=False);check_definition(D,s,Qm,psd=False)
        N=len(D);delta=cap_gap(v,lam);q=v-2-lam
        forms={'centered':Qc,'maximal':Qm,
            'centered_buffer':buffered_upper(Qc,delta),
            'maximal_buffer':buffered_upper(Qm,delta/2)}
        expected={'centered':N-v-1,'maximal':N-v,'centered_buffer':N-1,'maximal_buffer':N-1}
        ranks={};elimination={}
        for key,matrix in forms.items():
            if q!=1:
                stats={};rank=content_psd_rank(matrix,stats);assert rank==expected[key];ranks[key]=rank;elimination[key]=stats;full_forms+=1
                print('validated',name,key,'N',N,'rank',rank,file=sys.stderr,flush=True)
            # Independent small principal checks supplement the reused full
            # fraction-free backend. They do not certify full PSD alone.
            point_indices=[i for i,A in enumerate(D) if A.bit_count()<=1]
            principal=[[matrix[i][j] for j in point_indices] for i in point_indices]
            assert exact_psd_rank(principal)==v+1;principal_forms+=1
        stars=[[F(bool(A>>x&1))-F(s,N) for A in D] for x in range(v)]
        empty=[F(i==0)-F(1,N) for i in range(N)]
        assert gram_rank(stars)==v and gram_rank(stars+[empty])==v+1
        info=incidence_check(v,lam,blocks);comp=complement_check(v,lam,blocks)
        out['inputs'].append({'name':name,'v':v,'lambda':lam,'q':q,'N':N,'s':s,
            'generation':generation,'blocks':blocks,'weights':{k:str(z) for k,z in weights(v,lam).items()},
            'full_matrix_ranks_checked':ranks,'predicted_ranks_from_written_proof':expected,
            'full_matrix_omitted':q==1,'eta':str(eta),'B':str(cap_bound(v,lam)),'delta':str(delta),
            'maximal_buffer_gap':str(delta/2),'norm_gap_comparison':str(delta-F(v*(v-1)*(v-2)*(v-3),8*v*v)),
            'Q00':str(Qm[0][0]),'hashes':{key:matrix_hash(matrix) for key,matrix in forms.items()},
            'principal_Fraction_forms':4,'elimination':elimination,**info,**comp})
    rejects(lambda:parameters(12,7))  # q3 outside the proved upper range.
    rejects(lambda:parameters(10,8))  # The separate order floor.
    rejects(lambda:centered_certificate(v,lam,blocks[:-1]))
    rejects(lambda:centered_certificate(v,lam,blocks+[blocks[0]]))
    rejects(lambda:maximal_certificate(v,lam,blocks,(D,s,Qc),eta=F(1,v*v)))
    rejects(lambda:maximal_certificate(v,lam,blocks,(D,s,Qc),eta=F(0)))
    damaged=[row[:] for row in Qc];_,_,codegrees,outside=design_data(v,lam,blocks);u=lam*(lam-1)//2
    for i,a in enumerate(D):
        if a.bit_count()==1:
            for j,b in enumerate(D):
                if b.bit_count()==1 and a!=b:damaged[i][j]-=weights(v,lam)['t']*(codegrees[a|b]-u)
    rejects(lambda:check_definition(D,s,damaged,psd=False))
    clamped=[row[:] for row in Qc];changed=0
    for i,a in enumerate(D):
        if a.bit_count()==1:
            for j,b in enumerate(D):
                if b.bit_count()==3 and not a&b:
                    f=outside[b].get(a.bit_length()-1,0)
                    if f>1:clamped[i][j]=clamped[j][i]=Qc[i][j]+weights(v,lam)['t']*(f-1);changed+=1
    assert changed>0
    rejects(lambda:check_definition(D,s,clamped,psd=False))
    # On the constant complement this false buffer is -L, hence non-PSD.
    rejects(lambda:content_psd_rank(buffered_upper(Qc,N)))
    rejects(lambda:content_psd_rank([[F(0),F(1)],[F(1),F(0)]]))
    out['rejection_controls']=10;out['full_integer_PSD_forms']=full_forms
    out['independent_principal_Fraction_forms']=principal_forms
    assert full_forms==8 and principal_forms==12 and len(out['inputs'])==3
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--write-expected',action='store_true')
    args=p.parse_args();assert not(args.check and args.write_expected)
    out=run();expected=Path(__file__).with_name('dense_lambda_expected.json')
    if args.check:assert out==json.loads(expected.read_text()),'expected output mismatch'
    if args.write_expected:expected.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
