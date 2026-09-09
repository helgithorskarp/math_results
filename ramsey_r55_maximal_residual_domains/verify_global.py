"""Independent factorization using contact power sums and explicit pair factors."""
from fractions import Fraction
from pathlib import Path
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent
def require(ok,why):
    if not ok:raise ValueError(why)
def multiset(k,length):
    value=1
    for j in range(1,length+1):
        value,remainder=divmod(value*(k+j-1),j);require(not remainder,'binomial recurrence')
    return value
def verify(census,data,claim_path):
    census,data=Path(census),Path(data);claim=json.loads(Path(claim_path).read_text())
    for pin in json.loads((HERE/'DEPENDENCIES.json').read_text()):
        root=HERE.parent/pin['directory'];raw=(root/'MANIFEST.json').read_bytes()
        require(hashlib.sha256(raw).hexdigest()==pin['manifest_sha256'],'parent identity')
        for name,digest in json.loads(raw).items():require(hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,'parent file '+name)
    expected=json.loads((HERE.parent/'ramsey_r55_three_block_entropy/EXPECTED.json').read_text())['global_bound']
    contact_rows=[list(map(int,l.split())) for l in (HERE.parent/'ramsey_r55_q9_core_contact_domains/COUNTS.tsv').read_text().splitlines()]
    covers={};moments={};records=0
    for pin in json.loads((HERE/'INPUTS.json').read_text()):
        n=pin['order'];raw=(data/pin['file']).read_bytes();require(hashlib.sha256(raw).hexdigest()==pin['sha256'],'core catalogue')
        graphs=raw.decode().splitlines();lines=(census/str(n)/'COUNTS.tsv').read_text().splitlines()
        require(len(graphs)==len(lines)==pin['count'],'all core records');values=[]
        for i,(line,g) in enumerate(zip(lines,graphs)):
            fields=line.split();require(int(fields[0])==i and fields[1]==g,'labelled input identity');v=int(fields[3]);require(0<=v<=15**n,'cover range');values.append(v)
        covers[n]=values;moments[n]=[sum(v**b for v in values) for b in range(6)];records+=len(values)
    require(len(claim['classes'])==18 and {(x['q'],x['r']) for x in claim['classes']}=={(q,r) for q in range(7,11) for r in range(5,q+1)},'complete task classes')
    total=Fraction();improved=0;task_ids=0
    for row in claim['classes']:
        q,r=row['q'],row['r'];n=43-4*q;b=q-r
        factor=multiset(1998,r-1)*multiset(1931,b)
        for left in range(1,q):
            for right in range(left+1,q):factor*=37823 if (left<r)==(right<r) else 35714
        if q==9:
            # Independently reconstruct contact products core by core.
            local=0;old_contact=0;strict=0
            for i,(_index,plain,joint,opposite,_perm) in enumerate(contact_rows):
                require(i==_index and 0<joint<=plain<=15**7,'inherited red contacts')
                old_blue=contact_rows[opposite][1];blue=min(old_blue,covers[7][i]);term=1;old_term=1
                for block in range(q):term*=joint if block<r else blue;old_term*=joint if block<r else old_blue
                local+=term;old_contact+=old_term;strict+=term<old_term
            local*=factor;old_contact*=factor
        else:
            red=2433780807*15**3 if q==8 else 15**n
            local=factor*red**r*moments[n][b]
            old_contact=factor*red**r*(15**n)**b*len(covers[n])
            strict=sum(v<15**n for v in covers[n]) if b else 0
        prior=next(x for x in expected['classes'] if (x['q'],x['r'])==(q,r))
        beta=Fraction(**prior['probability_upper']);upper=beta*local;old_upper=beta*old_contact
        require(old_contact==prior['before']==row['contact_parent_sum'],'complete old factorization')
        require(local==row['contact_bound_sum'] and upper==Fraction(**row['after_upper']),'new factorization')
        require(old_upper==Fraction(**prior['after_upper'])==Fraction(**row['before_upper']),'baseline upper')
        require(Fraction(**row['ratio_to_previous_upper'])==upper/old_upper and row['strictly_improved_tasks']==strict,'class consequence')
        require(row['core_count']==len(covers[n]),'class multiplicity');total+=upper;improved+=strict;task_ids+=len(covers[n])
    before=Fraction(**expected['after_upper']);ratio=total/before
    require(total==Fraction(**claim['after_upper']) and before==Fraction(**claim['before_upper']),'global weighted sum')
    require(ratio==Fraction(**claim['ratio_to_previous_upper']),'global ratio')
    require(abs(ratio-Fraction(claim['ratio_to_previous_upper_decimal']))<Fraction(1,10**39),'ratio display')
    require(1-total/expected['before']==Fraction(**claim['h4059_removed_lower']),'h4059 lower bound')
    require(claim['gate']==('PASS' if 2*total<=before else 'FAIL'),'declared gate')
    require(claim['strictly_improved_task_bounds']==improved and claim['task_ids']==task_ids==2189178,'task consequence')
    require(claim['new_task_decisions']==0 and not claim['target_found'] and claim['q10_child_inputs_inspected']==0,'scope')
    return dict(status='INDEPENDENT_COMPLETE_RESIDUAL_BOUND_VERIFIED',cores=records,classes=18,task_ids=task_ids,strictly_improved_task_bounds=improved,gate=claim['gate'])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('census');p.add_argument('data');p.add_argument('claim');a=p.parse_args();print(json.dumps(verify(a.census,a.data,a.claim),sort_keys=True))
