"""Exact rational entropy certificate for every complete h4059 carrier class."""
from decimal import Decimal,localcontext
from fractions import Fraction as F
from math import comb
from pathlib import Path
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent
SCALE=10**18

def need(ok,why):
    if not ok:raise ValueError(why)
def rat(x):return dict(numerator=x.numerator,denominator=x.denominator)
def decimal(x):
    with localcontext() as c:c.prec=40;return str(Decimal(x.numerator)/Decimal(x.denominator))
def parent():
    pins=json.loads((HERE/'DEPENDENCIES.json').read_text());need(len(pins)==2,'two parents')
    for pin in pins:
        root=HERE.parent/pin['directory'];raw=(root/pin['manifest']).read_bytes()
        need(hashlib.sha256(raw).hexdigest()==pin['sha256'],'parent manifest')
        entries=(dict((name,digest) for digest,name in (line.split('  ',1) for line in raw.decode().splitlines())) if pin['manifest']=='SHA256SUMS' else json.loads(raw))
        for name,digest in entries.items():need(hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,'parent file '+name)
    return json.loads((HERE.parent/'ramsey_r55_q9_core_contact_domains'/'EXPECTED.json').read_text())['census']

def root_upper(p,k):
    need(F(0)<p<=1 and type(k) is int and k>0,'root input');low,high=0,SCALE
    numerator=p.numerator*SCALE**k;denominator=p.denominator
    while low<high:
        middle=(low+high)//2
        if middle**k*denominator>=numerator:high=middle
        else:low=middle+1
    need(low**k*denominator>=numerator,'root upper inequality')
    need(low==0 or (low-1)**k*denominator<numerator,'minimal grid root')
    return F(low,SCALE)
def calculate(local):
    local=json.loads(Path(local).read_text());need(local['status']=='COMPLETE_CENTRED_TRIPLE_CENSUS','complete primitive count')
    probability={k:F(v['allowed'],v['total']) for k,v in local['probabilities'].items()}
    old=parent();before=old['after'];classes=[];after=F(0)
    for row in old['classes']:
        q,r=row['q'],row['r'];a,b=r-1,q-r;m=q-1
        same=comb(a,3)+comb(b,3);mixed=comb(m,3)-same;k=3*(m-2)
        need(3*comb(m,3)*3==comb(m,2)*k,'exact projection cover')
        power=probability['same']**(3*same)*probability['majority']**(2*mixed)*probability['minority']**mixed
        upper=root_upper(power,k);need(upper<1,'strict class reduction')
        weight=row['after'];after+=weight*upper
        classes.append(dict(q=q,r=r,core_count=row['core_count'],matrix_coordinates=comb(m,2),same_triples=same,mixed_triples=mixed,events=3*comb(m,3),read=k,probability_upper=rat(upper),before=weight,after_upper=rat(weight*upper)))
    need(sum(x['before'] for x in classes)==before,'complete class sum')
    removed=(before-after)/before
    return dict(status='CERTIFIED_THREE_BLOCK_GLOBAL_CARRIER_BOUND',gate='PASS' if 4*after<=3*before else 'FAIL',
        parent='h4059 complete bare carrier',before=before,after_upper=rat(after),removed_lower=rat(removed),
        removed_lower_decimal=decimal(removed),minimum_class_removal_lower_decimal=decimal(min(1-F(**x['probability_upper']) for x in classes)),
        classes=classes,root_scale=SCALE,task_ids=2189178,affected_task_ids=2189178,remaining_whole_tasks=2188660,
        new_task_decisions=0,solver_calls=0,q10_child_inputs_inspected=0,target_found=False)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('local');p.add_argument('--out');a=p.parse_args();x=calculate(a.local);s=json.dumps(x,indent=2,sort_keys=True)+'\n'
    if a.out:Path(a.out).write_text(s)
    else:print(s,end='')
