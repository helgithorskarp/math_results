"""Independent full actual-word/cyclic-AP check for arbitrary subgroup rows."""
import argparse
import hashlib
import json
from math import gcd
from pathlib import Path


def require(ok,message):
    if not ok:raise ValueError(message)


def check_word(d,assignment,word,target=False):
    q,m,k=d['field_prime'],d['row_half'],d['AP_length'];H=d['subgroup'];fixed=d['fixed_first_coset_row']
    require(all(type(v) is int for v in [q,m,k]) and 3<=q<=31 and 1<=m<=10 and 2<=k<=7 and all(q%i for i in range(2,q)) and gcd(q,2*m)==1,'raw physical prime/CRT domains')
    require(type(H) is list and H and all(type(h) is int and 1<=h<q for h in H) and H==sorted(set(H)) and 1 in H and all(a*b%q in H for a in H for b in H),'raw declared multiplicative subgroup')
    require(d['author']=='six-vdw-1' and d['role']=='researcher' and d['model_kind']=='arbitrary_subgroup_antipodal_regular' and d['membership_clauses']==[],'chosen arbitrary-coset family')
    require(type(d['palette']) is bool and(fixed is None or(type(fixed) is int and 0<=fixed<2**m and not d['palette'])),'firstrow/palette domains')
    representatives=sorted({min(r*h%q for h in H) for r in range(1,q)})
    n,nv=2*q*m,m*len(representatives)
    require((d['period'],d['variables'],d['free_point_inputs_before_AP'])==(n,nv,nv-(m if fixed is not None else int(d['palette']))),'whole independent input dimensions')
    if target:require((q,m,k,H,fixed,d['palette'])==(31,10,7,[1,5,25],16,False),'exact production arbitrary H3 head')
    require(type(assignment) is list and len(assignment)==nv and all(type(v) is int and 0<abs(v)<=nv for v in assignment) and {abs(v) for v in assignment}==set(range(1,nv+1)),'complete unique original inputs')
    positive={v for v in assignment if v>0};rows=[sum(2**j for j in range(m) if m*g+j+1 in positive) for g in range(len(representatives))]
    require(fixed is None or rows[0]==fixed,'actual absolute firstrow')
    require(not d['palette'] or 1 not in positive,'global palette')
    colors=[]
    for x in range(n):
        if x%q==0:colors.append(None);continue
        rep=min(x%q*h%q for h in H);row=rows[representatives.index(rep)];s=x%(2*m)
        colors.append(((row//2**(s%m))%2+s//m)%2)
    require(type(word) is list and len(word)==n and all(v is None or(type(v) is int and v in [0,1]) for v in word) and word==colors,'whole raw actual-color word')
    regular=poles=0
    for a in range(n):
        for b in range(n):
            if a==b:continue
            positions=[(a+j*(b-a))%n for j in range(k)]
            if any(x%q==0 for x in positions):poles+=1;continue
            regular+=1;require(len({colors[x] for x in positions})>1,'actual regular monochromatic progression')
    return {'author':'six-vdw-1','role':'researcher','status':'COMPLETE_ACTUAL_ARBITRARY_H3_ROW16_CORE_CHECK' if target else 'COMPLETE_TINY_ACTUAL_SUBGROUP_CORE_CHECK',
            'regular_pairs':regular,'pole_touching_pairs_unchecked':poles,'arbitrary_coset_row_masks':rows,'period_partial_word':colors,
            'scope':'Regular core only; finite actual poles and3704 interval unassigned.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('model',type=Path);p.add_argument('proposal',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    require(not a.output.exists(),'preserve checked certificate')
    d=json.loads(a.model.read_text());candidate=json.loads(a.proposal.read_text())
    require(candidate['status']=='PARTIAL_SAT_PROPOSAL' and candidate['model_sha256']==hashlib.sha256(a.model.read_bytes()).hexdigest() and candidate['cnf_sha256']==hashlib.sha256(a.model.with_suffix('.cnf').read_bytes()).hexdigest(),'candidate provenance')
    result=check_word(d,candidate['assignment'],candidate['period_partial_word'],True)
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['arbitrary_coset_row_masks','period_partial_word']},sort_keys=True),flush=True)
