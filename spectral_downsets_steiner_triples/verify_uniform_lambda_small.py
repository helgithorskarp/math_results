"""Full exact controls for the all-order simple triple-design H theorem.

Eleven literal designs, never an enumeration. All lower forms use exact
integer Schur; selected small forms also use independent Fraction Schur.
The universal real interval rests on UNIFORM_LAMBDA_ALL_ORDERS.md.
CPython3.11+ stdlib, assertions enabled. six-downset-2, researcher.
"""
import argparse
import json
import sys
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
from integer_psd import integer_psd_rank
from lambda_small_identities import run as identities
from uniform_lambda_small import cap_bound,centered_certificate,design_data,fixtures,maximal_certificate,parameters,weights
from verify import check_definition,exact_psd_rank,matrix_hash,rejects
from verify_three9 import gram_rank


def incidence_check(v,lam,blocks):
    # Literal incidence verification retained from verify_uniform_lambda.py;
    # this version validates the expanded input domain without monkeypatches.
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
        contained=[p for p in pairs if p&A==p];assert len(contained)==3
        for x in range(v):
            assert sum(int(p>>x&1) for p in contained)==2*int(A>>x&1)
            assert sum(int((1<<x) in completing[p]) for p in contained)==int(A>>x&1)+outside[A].get(x,0)
    for p in pairs:
        containing=[A for A in blocks if A&p==p];assert len(containing)==lam
        for x in range(v):
            assert sum(int(A>>x&1) for A in containing)==lam*int(p>>x&1)+int((1<<x) in completing[p])
    return {'incidence_identities':10,'Z_values':sorted({a for row in Z for a in row}),
            'outside_multiplicities':sorted({a for row in H for a in row})}


def run():
    out={'agent':'six-downset-2','role':'researcher','identities':identities(),'inputs':[]}
    integer_forms=rational_forms=0
    for name,v,lam,blocks,generation in fixtures():
        D,s,Qc=centered_certificate(v,lam,blocks)
        _,_,Qm,eta=maximal_certificate(v,lam,blocks,(D,s,Qc))
        check_definition(D,s,Qc,psd=False);check_definition(D,s,Qm,psd=False)
        forms={'centered':Qc} if v==4 else {'centered':Qc,'maximal':Qm}
        expected={'centered':7} if v==4 else {'centered':len(D)-v-1,'maximal':len(D)-v}
        if v==4:
            upper=[[F(len(D) if i==j else 0)-Qc[i][j] for j in range(len(D))] for i in range(len(D))]
            forms['upper']=upper;expected['upper']=len(D)-1
            assert Qm==Qc and eta==0
            # The known unique slack kills additional maximum-family vectors.
            alltriples={a for a in D if a.bit_count()==3}
            for x in range(4):
                family=alltriples|{a for a in D if a.bit_count()==2 and a>>x&1}
                assert len(family)==7 and all(a&b for a,b in combinations(family,2))
                for row in Qc:assert sum(row[D.index(a)] for a in family)==s
                assert all(row[D.index(1<<x)]==row[D.index(15^(1<<x))] for row in Qc)
            nonstar=alltriples|{3,5,6};assert len(nonstar)==7
            assert all(a&b for a,b in combinations(nonstar,2))
            assert not set.intersection(*[{x for x in range(4) if a>>x&1} for a in nonstar])
        ranks={key:integer_psd_rank(matrix) for key,matrix in forms.items()};integer_forms+=len(forms)
        assert ranks==expected
        rational_keys=[]
        if v<=6:rational_keys=list(forms)
        elif (v,lam)==(7,5):rational_keys=['centered']
        for key in rational_keys:
            assert exact_psd_rank(forms[key])==ranks[key];rational_forms+=1
        if (v,lam)==(5,3):
            _,_,half,half_eta=maximal_certificate(v,lam,blocks,(D,s,Qc),eta=eta/2)
            check_definition(D,s,half,psd=False)
            assert integer_psd_rank(half)==len(D)-v;integer_forms+=1
            assert half_eta==F(1,400)
        stars=[[F(bool(A>>x&1))-F(s,len(D)) for A in D] for x in range(v)]
        empty=[F(j==0)-F(1,len(D)) for j in range(len(D))]
        assert gram_rank(stars)==v and gram_rank(stars+[empty])==v+1
        info=incidence_check(v,lam,blocks)
        out['inputs'].append({'name':name,'v':v,'lambda':lam,'N':len(D),'s':s,
            'blocks':blocks,'generation':generation,
            'weights':{k:str(z) for k,z in weights(v,lam).items()} if v>=5 else None,
            'ranks':ranks,'eta':str(eta),'Q00':str(Qm[0][0]),
            'centered_sha256':matrix_hash(Qc),'maximal_sha256':matrix_hash(Qm),
            'independent_rational_forms':rational_keys,'upper_cap_claim':cap_bound(v,lam) is not None,**info})
        print('validated',name,'N',len(D),'ranks',ranks,file=sys.stderr,flush=True)
    # Entrywise/hash regression on one retained older-domain lambda4 input.
    from uniform_lambda import fixtures as old_fixtures,centered_certificate as old_centered,maximal_certificate as old_maximal
    name0,v0,l0,blocks0,_=next(row for row in old_fixtures() if row[2]==4)
    old=old_centered(v0,l0,blocks0);old_m=old_maximal(v0,l0,blocks0,old)
    new=centered_certificate(v0,l0,blocks0);new_m=maximal_certificate(v0,l0,blocks0,new)
    assert old==new and old_m==new_m
    parent=json.loads(Path(__file__).with_name('uniform_lambda_expected.json').read_text())
    record=next(row for row in parent['inputs'] if row['name']==name0)
    assert matrix_hash(new[2])==record['centered_sha256'] and matrix_hash(new_m[2])==record['maximal_sha256']
    out['retained_regression']={'name':name0,'v':v0,'lambda':l0,'N':len(new[0]),
        'entrywise_both':True,'centered_sha256':record['centered_sha256'],'maximal_sha256':record['maximal_sha256']}
    assert cap_bound(9,2)==60 and cap_bound(13,2)==F(364,5)
    assert cap_bound(13,3)==F(325,2) and cap_bound(96,4)==3072
    assert all(cap_bound(vv,ll) is None for vv,ll in ((5,3),(6,2),(6,4),(7,2),(7,3),(7,4),(7,5),(9,3),(12,4)))
    controls=[
        ('too_small',lambda:parameters(3,2)),('invalid_v5',lambda:parameters(5,2)),
        ('invalid_v6',lambda:parameters(6,3)),('too_many_blocks',lambda:parameters(7,6)),
        ('degree_one',lambda:parameters(7,1)),('noninteger',lambda:parameters(7.0,2)),
        ('singular_v4_weights',lambda:weights(4,2)),
        ('missing_block',lambda:centered_certificate(v,lam,blocks[:-1])),
        ('repeated_block',lambda:centered_certificate(v,lam,blocks+[blocks[0]])),
        ('oversized_eta',lambda:maximal_certificate(v,lam,blocks,(D,s,Qc),eta=F(1,v*v))),
        ('zero_eta',lambda:maximal_certificate(v,lam,blocks,(D,s,Qc),eta=F(0))),
        ('indefinite_zero_diagonal',lambda:integer_psd_rank([[F(0),F(1)],[F(1),F(0)]]))]
    damaged=[row[:] for row in Qc];_,_,codegrees,outside=design_data(v,lam,blocks)
    u=lam*(lam-1)//2
    for i,a in enumerate(D):
        if a.bit_count()==1:
            for j,b in enumerate(D):
                if b.bit_count()==1 and a!=b:
                    damaged[i][j]-=weights(v,lam)['t']*(codegrees[a|b]-u)
    controls.append(('removed_codegree',lambda:check_definition(D,s,damaged,psd=False)))
    clamped=[row[:] for row in Qc];changed=0
    for i,a in enumerate(D):
        if a.bit_count()==1:
            for j,b in enumerate(D):
                if b.bit_count()==3 and not a&b:
                    f=outside[b].get(a.bit_length()-1,0)
                    if f>1:
                        clamped[i][j]=clamped[j][i]=Qc[i][j]+weights(v,lam)['t']*(f-1);changed+=1
    assert changed>0
    controls.append(('clamped_completion',lambda:check_definition(D,s,clamped,psd=False)))
    for _,call in controls:rejects(call)
    out['rejection_controls']=[name for name,_ in controls]
    out['full_integer_PSD_forms']=integer_forms;out['independent_Fraction_PSD_forms']=rational_forms
    assert integer_forms==23 and rational_forms==9 and len(out['inputs'])==11
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--write-expected',action='store_true')
    args=p.parse_args();assert not(args.check and args.write_expected)
    out=run();expected=Path(__file__).with_name('uniform_lambda_small_expected.json')
    if args.check:assert out==json.loads(expected.read_text()),'expected output mismatch'
    if args.write_expected:expected.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
