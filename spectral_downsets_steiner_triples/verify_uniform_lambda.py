"""Full exact validation of the uniform-lambda constructor on four inputs.

Universal scope rests on UNIFORM_LAMBDA_PROOF.md, not these fixtures.
Four centered/maximal lower pairs are checked by integer Schur; lambda4's
centered lower also uses rational Schur. Four buffered upper forms atlambda2/3
use their proved bounds. The new generic cap rangev>=24lambda is verified by
the all-parameter coefficient/norm proof, not a large dense sample.
CPython3.11+ stdlib, assertions enabled. six-downset-2, researcher.
"""
import argparse
import json
import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
from certificates import mask
from integer_psd import integer_psd_rank
from lambda_identities import run as identities
from uniform_lambda import cap_bound,cap_gap,centered_certificate,design_data,fixtures,maximal_certificate,parameters,weights
from verify import check_definition,exact_psd_rank,matrix_hash,rejects
from verify_three9 import buffered_upper,gram_rank


def incidence_check(v,lam,blocks):
    pairs,completing,codegrees,outside=design_data(v,lam,blocks)
    r=lam*(v-1)//2;u=lam*(lam-1)//2
    P=[[int(p>>x&1) for p in pairs] for x in range(v)]
    C=[[int((1<<x) in completing[p]) for p in pairs] for x in range(v)]
    B=[[int(A>>x&1) for A in blocks] for x in range(v)]
    H=[[outside[A].get(x,0) for A in blocks] for x in range(v)]
    for matrix,rs,cs in ((P,v-1,2),(C,r,lam),(B,r,3),(H,(lam-1)*r,3*(lam-1))):
        assert all(sum(row)==rs for row in matrix)
        assert all(sum(row[j] for row in matrix)==cs for j in range(len(matrix[0])))
    Z=[[0]*v for _ in range(v)]
    for x in range(v):
        for y in range(v):
            dot=lambda A,T:sum(a*b for a,b in zip(A[x],T[y]))
            assert dot(P,P)==(v-2)*int(x==y)+1
            assert dot(B,B)==(r-lam)*int(x==y)+lam
            assert dot(P,C)==dot(C,P)==lam*int(x!=y)
            Z[x][y]=dot(C,C)-(r-u)*int(x==y)-u
            assert Z[x][y]==(codegrees[(1<<x)|(1<<y)]-u if x!=y else 0)
            assert dot(B,H)==dot(H,B)==3*u*int(x!=y)+Z[x][y]
    assert all(sum(row)==0 for row in Z)
    for A in blocks:
        contained=[p for p in pairs if p&A==p]
        assert len(contained)==3
        for x in range(v):
            assert sum(int(p>>x&1) for p in contained)==2*int(A>>x&1)
            assert sum(int((1<<x) in completing[p]) for p in contained)==int(A>>x&1)+outside[A].get(x,0)
    for p in pairs:
        containing=[A for A in blocks if A&p==p]
        assert len(containing)==lam
        for x in range(v):
            assert sum(int(A>>x&1) for A in containing)==lam*int(p>>x&1)+int((1<<x) in completing[p])
    return {'incidence_identities':10,'Z_values':sorted({a for row in Z for a in row}),
            'outside_multiplicities':sorted({a for row in H for a in row})}


def run():
    out={'agent':'six-downset-2','role':'researcher','identities':identities(),'inputs':[]}
    for name,v,lam,blocks,generation in fixtures():
        D,s,Qc=centered_certificate(v,lam,blocks)
        _,_,Qm,eta=maximal_certificate(v,lam,blocks,(D,s,Qc))
        check_definition(D,s,Qc,psd=False);check_definition(D,s,Qm,psd=False)
        forms={'centered':Qc,'maximal':Qm}
        expected={'centered':len(D)-v-1,'maximal':len(D)-v}
        delta=cap_gap(v,lam)
        if delta is not None:
            forms['centered_buffer']=buffered_upper(Qc,delta)
            forms['maximal_buffer']=buffered_upper(Qm,delta/2)
            expected.update({'centered_buffer':len(D)-1,'maximal_buffer':len(D)-1})
        ranks={key:integer_psd_rank(matrix) for key,matrix in forms.items()}
        assert ranks==expected
        if lam==4:assert exact_psd_rank(Qc)==ranks['centered']
        if lam==2:
            from uniform_twofold import centered_certificate as old
            assert (D,s,Qc)==old(v,blocks)
        elif lam==3:
            from uniform_threefold import centered_certificate as old
            assert (D,s,Qc)==old(v,blocks)
        stars=[[F(bool(A>>x&1))-F(s,len(D)) for A in D] for x in range(v)]
        empty=[F(j==0)-F(1,len(D)) for j in range(len(D))]
        assert gram_rank(stars)==v and gram_rank(stars+[empty])==v+1
        info=incidence_check(v,lam,blocks)
        out['inputs'].append({'name':name,'v':v,'lambda':lam,'N':len(D),'s':s,
            'blocks':blocks,'generation':generation,'weights':{k:str(z) for k,z in weights(v,lam).items()},
            'ranks':ranks,'eta':str(eta),'Q00':str(Qm[0][0]),
            'centered_gap':str(delta) if delta is not None else None,
            'maximal_gap':str(delta/2) if delta is not None else None,
            'general_cap_range_input':v>=24*lam,
            'centered_sha256':matrix_hash(Qc),'maximal_sha256':matrix_hash(Qm),
            'rational_lower_checked':lam==4,**info})
        print('validated',name,'N',len(D),'ranks',ranks,file=sys.stderr,flush=True)
    rejects(lambda:parameters(12,4));rejects(lambda:parameters(13,12))
    rejects(lambda:parameters(14,3))
    rejects(lambda:centered_certificate(v,lam,blocks[:-1]))
    rejects(lambda:centered_certificate(v,lam,blocks+[blocks[0]]))
    rejects(lambda:maximal_certificate(v,lam,blocks,(D,s,Qc),eta=F(1,v*v)))
    damaged=[row[:] for row in Qc]
    _,_,codegrees,outside=design_data(v,lam,blocks)
    u=lam*(lam-1)//2
    for i,a in enumerate(D):
        if a.bit_count()==1:
            for j,b in enumerate(D):
                if b.bit_count()==1 and a!=b:
                    damaged[i][j]-=weights(v,lam)['t']*(codegrees[a|b]-u)
    rejects(lambda:check_definition(D,s,damaged,psd=False))
    clamped=[row[:] for row in Qc];changed=0
    for i,a in enumerate(D):
        if a.bit_count()==1:
            for j,b in enumerate(D):
                if b.bit_count()==3 and not a&b:
                    f=outside[b].get(a.bit_length()-1,0)
                    if f>1:
                        clamped[i][j]=clamped[j][i]=Qc[i][j]+weights(v,lam)['t']*(f-1)
                        changed+=1
    assert changed>0
    rejects(lambda:check_definition(D,s,clamped,psd=False))
    rejects(lambda:integer_psd_rank([[F(0),F(1)],[F(1),F(0)]]))
    out['rejection_controls']=9
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--write-expected',action='store_true')
    args=p.parse_args();assert not(args.check and args.write_expected)
    out=run();expected=Path(__file__).with_name('uniform_lambda_expected.json')
    if args.check:assert out==json.loads(expected.read_text()),'expected output mismatch'
    if args.write_expected:expected.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
