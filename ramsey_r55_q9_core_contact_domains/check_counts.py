"""Entrywise census audit, complement certificates, and exact global accounting."""
from decimal import Decimal,localcontext
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path
import argparse,hashlib,json,struct
from inputs import HERE,catalogue,need,parents,sha

def ratio(x):return dict(numerator=x.numerator,denominator=x.denominator)
def decimal(x):
    with localcontext() as c:c.prec=40;return str(Decimal(x.numerator)/Decimal(x.denominator))
def audit(cache,rows_path,columns_path,tables):
    words=catalogue(cache);rows=[list(map(int,s.split())) for s in Path(rows_path).read_text().splitlines()]
    columns=[list(map(int,s.split())) for s in Path(columns_path).read_text().splitlines()]
    need(len(rows)==len(columns)==362,'complete census count')
    raw=Path(tables).read_bytes();need(len(raw)==23912272,'table length');width=8257
    for i,row in enumerate(rows):
        need(len(row)==5 and row[0]==i and columns[i]==row[:3],'row/column census disagreement')
        _,plain,joint,dest,packed=row
        need(0<joint<=plain<=15**7 and 0<=dest<362 and 0<=packed<1<<21,'count/certificate range')
        p=[(packed>>(3*k))&7 for k in range(7)];need(sorted(p)==list(range(7)),'complement permutation')
        edges={edge:(words[i]>>k)&1 for k,edge in enumerate(combinations(range(7),2))}
        w=sum((1-edges[tuple(sorted((p[u],p[v])))])<<k for k,(u,v) in enumerate(combinations(range(7),2)))
        need(w==words[dest],'complement edge mismatch')
        for j,total in enumerate((plain,joint)):
            prefix=struct.unpack_from('<8257I',raw,(2*i+j)*width*4)
            need(prefix[0]==0 and prefix[-1]==total and all(a<=b for a,b in zip(prefix,prefix[1:])),'prefix partition')
    parents() # includes the pinned h4035 expectation and h3887 registry source
    old=json.loads((HERE.parent/'ramsey_r55_packing_augmentation'/'EXPECTED.json').read_text())
    new=before=0;q9before=q9after=0;classes=[];minimum=Fraction(1);maximum=Fraction(0)
    for c in old['classes']:
        q,r,mult=c['q'],c['r'],c['core_count'];a,b=r-1,q-r
        matrix=comb(1998+a-1,a)*comb(1931+b-1,b)*37823**(comb(a,2)+comb(b,2))*35714**(a*b)
        stars=15**(q*(43-4*q));need(c['per_task']==matrix*stars,'parent matrix/cardinality')
        old_local=c['retained_per_task'];old_class=mult*old_local;before+=old_class
        if q==9:
            need(mult==362 and old_local==matrix*(50151*15**3)**r*(15**7)**b,'q9 parent contact count')
            contacts=[row[2]**r*rows[row[3]][1]**b for row in rows]
            local=[matrix*t for t in contacts];new_class=sum(local)
            fractions=[Fraction(t,old_local) for t in local]
            minimum=min(minimum,min(fractions));maximum=max(maximum,max(fractions))
            q9before+=old_class;q9after+=new_class
            need(all(0<t<old_local for t in local),'strict q9 reduction')
            classes.append(dict(q=q,r=r,core_count=mult,before=old_class,after=new_class,
                retained_fraction=ratio(Fraction(new_class,old_class)),minimum=ratio(min(fractions)),maximum=ratio(max(fractions))))
        else:
            new_class=old_class
            classes.append(dict(q=q,r=r,core_count=mult,before=old_class,after=new_class))
        new+=new_class
    need(before==old['new_carrier'],'global parent census')
    need(Fraction(before-new,before)>Fraction(853,1000),'stated global percentage')
    need(Fraction(q9before-q9after,q9before)>Fraction(8835,10000),'stated q9 percentage')
    need(maximum<Fraction(4076,10000),'stated worst-task percentage')
    # h4029 and h4001 were already accounted for in this inherited upper envelope.
    prior_upper=Fraction(**old['new_composite_upper']);new_upper=prior_upper-q9before+q9after
    need(new_upper>0 and new_upper<=new,'composite upper')
    return dict(status='CERTIFIED_Q9_CONTACT_CARRIER_COUNTS',gate='PASS' if 2*new<=before else 'FAIL',
        family='h4035 full bare carrier with joint q9 block/core contact domains',
        tasks=2189178,affected_tasks=1810,remaining_whole_tasks=2188660,new_task_decisions=0,
        q10_children_inspected=0,solver_calls=0,target_found=False,
        plain_range=[min(r[1] for r in rows),max(r[1] for r in rows)],
        joint_range=[min(r[2] for r in rows),max(r[2] for r in rows)],
        before=before,after=new,removed_fraction=ratio(Fraction(before-new,before)),
        removed_decimal=decimal(Fraction(before-new,before)),
        q9_before=q9before,q9_after=q9after,q9_removed_fraction=ratio(Fraction(q9before-q9after,q9before)),
        q9_removed_decimal=decimal(Fraction(q9before-q9after,q9before)),
        minimum_task_retained=ratio(minimum),maximum_task_retained=ratio(maximum),
        maximum_task_retained_decimal=decimal(maximum),
        inherited_composite_before=ratio(prior_upper),inherited_composite_after=ratio(new_upper),
        inherited_composite_removed_decimal=decimal((prior_upper-new_upper)/prior_upper),
        classes=classes,census_records=362,independent_counts=724,complement_edge_checks=362*21,
        prefix_boundaries=362*2*width,
        counts_sha256=sha(Path(rows_path).read_bytes()),columns_sha256=sha(Path(columns_path).read_bytes()),
        prefix_sha256=sha(raw))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('cache');p.add_argument('rows');p.add_argument('columns');p.add_argument('tables');p.add_argument('--output');a=p.parse_args()
    result=audit(a.cache,a.rows,a.columns,a.tables);text=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if a.output:Path(a.output).write_text(text)
    else:print(text,end='')
