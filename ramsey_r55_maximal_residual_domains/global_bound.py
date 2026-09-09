"""Exact upper bound on the complete h4069 family with residual restrictions."""
from collections import Counter
from decimal import Decimal,localcontext
from fractions import Fraction as F
from math import comb
from pathlib import Path
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent
def need(ok,why):
    if not ok:raise ValueError(why)
def rat(x):return dict(numerator=x.numerator,denominator=x.denominator)
def dec(x):
    with localcontext() as c:c.prec=40;return str(Decimal(x.numerator)/Decimal(x.denominator))
def run(census,data):
    census,data=Path(census),Path(data)
    receipt=json.loads((census/'CENSUS.json').read_text());need(receipt['status']=='COMPLETE_INDEPENDENT_MAXIMAL_RESIDUAL_CENSUS','complete independent census')
    counts={};stats=[]
    for pin in json.loads((HERE/'INPUTS.json').read_text()):
        n=pin['order'];lines=(data/pin['file']).read_text().splitlines();rows=(census/str(n)/'COUNTS.tsv').read_text().splitlines()
        need(len(rows)==len(lines)==pin['count'],'catalogue coverage')
        values=[]
        for index,(raw,g) in enumerate(zip(rows,lines)):
            i,word,free,cover=raw.split();need(int(i)==index and word==g,'catalogue identity/order')
            free,cover=int(free),int(cover);need(0<=cover<=15**n and 1<=free<=2**n,'cover bounds');values.append(cover)
        need(hashlib.sha256((census/str(n)/'COUNTS.tsv').read_bytes()).hexdigest()==next(x for x in receipt['catalogues'] if x['order']==n)['count_sha256'],'count receipt')
        counts[n]=values;stats.append(dict(order=n,cores=len(values),minimum=min(values),maximum=max(values),strict_star_reductions=sum(x<15**n for x in values),zero_covers=values.count(0)))
    parent=json.loads((HERE.parent/'ramsey_r55_q9_core_contact_domains/EXPECTED.json').read_text())['census']
    old=json.loads((HERE.parent/'ramsey_r55_three_block_entropy/EXPECTED.json').read_text())['global_bound']
    contacts=[list(map(int,s.split())) for s in (HERE.parent/'ramsey_r55_q9_core_contact_domains/COUNTS.tsv').read_text().splitlines()]
    need(len(contacts)==362,'contact count')
    classes=[];after=F();improved=0
    for row in old['classes']:
        q,r=row['q'],row['r'];n=43-4*q;b=q-r;a=r-1;values=counts[n];beta=F(**row['probability_upper'])
        inherited=next(x for x in parent['classes'] if (x['q'],x['r'])==(q,r));old_class=inherited['after']
        need(old_class==row['before'],'h4069 class provenance')
        if q==9:
            matrix=comb(1998+a-1,a)*comb(1931+b-1,b)*37823**(comb(a,2)+comb(b,2))*35714**(a*b)
            old_values=[matrix*x[2]**r*contacts[x[3]][1]**b for x in contacts]
            new_values=[matrix*x[2]**r*min(values[i],contacts[x[3]][1])**b for i,x in enumerate(contacts)]
        else:
            old_per,remainder=divmod(old_class,len(values));need(remainder==0,'uniform core count')
            constant,remainder=divmod(old_per,(15**n)**b);need(remainder==0,'independent blue contact coordinates')
            old_values=[old_per]*len(values);new_values=[constant*v**b for v in values]
        need(sum(old_values)==old_class and all(0<=v<=u for v,u in zip(new_values,old_values)),'class upper validity')
        count=sum(v<u for v,u in zip(new_values,old_values));improved+=count
        new=beta*sum(new_values);before=F(**row['after_upper']);need(before==beta*old_class,'old weighted bound');after+=new
        classes.append(dict(q=q,r=r,core_count=len(values),before_upper=rat(before),after_upper=rat(new),strictly_improved_tasks=count,
                            contact_bound_sum=sum(new_values),contact_parent_sum=old_class,ratio_to_previous_upper=rat(new/before)))
    before=F(**old['after_upper']);need(sum(F(**x['before_upper']) for x in classes)==before,'all classes')
    parent_count=parent['after'];need(before<=parent_count,'parent bound')
    return dict(status='COMPLETE_MAXIMAL_RESIDUAL_GLOBAL_UPPER',gate='PASS' if 2*after<=before else 'FAIL',
                baseline_quantity='h4069 upper certificate, not its unknown exact count',before_upper=rat(before),after_upper=rat(after),
                ratio_to_previous_upper=rat(after/before),ratio_to_previous_upper_decimal=dec(after/before),
                h4059_removed_lower=rat(1-after/parent_count),h4059_removed_lower_decimal=dec(1-after/parent_count),
                classes=classes,cores=stats,task_ids=2189178,strictly_improved_task_bounds=improved,
                new_task_decisions=0,target_found=False,solver_calls=0,q10_child_inputs_inspected=0,
                q9_rule='min of dependent contact-domain cardinalities, never their product')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('census');p.add_argument('data');p.add_argument('out');a=p.parse_args();result=run(a.census,a.data)
    Path(a.out).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('classes','before_upper','after_upper','ratio_to_previous_upper','h4059_removed_lower')},sort_keys=True))
