"""Independent typed count compositions, no author mathematical imports.

The producer chooses support counts N at fixed degree target D. Here
choose counts of the two row kinds first, then derive both D and N.
Every degree target and pre-support multiplicity is checked separately.
"""
from collections import Counter
import itertools,json,time
from pathlib import Path
S=Path('round-two/six-code-3/scratch')

def need(c,m):
    if not c:raise ValueError(m)

def compositions(total,n):
    if n==1:yield (total,);return
    for c in range(total+1):
        for tail in compositions(total-c,n-1):yield (c,)+tail

def accepted(unit,double,threshold=5):
    size=[u+t for u,t in zip(unit,double)]
    return all((u==0 or n>=2) and (t==0 or n>=threshold) for u,t,n in zip(unit,double,size))

def main():
    start=time.monotonic();author=json.loads((S/'pass18-t4-support-producer.json').read_text())
    projected=[x for x in itertools.product(range(14),repeat=4) if sum(x)==24 and 5<=x[0]<=13 and all(1<=x[a]<=9 for a in (1,2,3))]
    statistics=[];attempts=0
    for rec in author['records']:
        U,V=rec['unit_rows'],rec['double_rows'];weights=Counter();valid={D:[] for D in projected}
        for unit in compositions(U,4):
            for double in compositions(V,4):
                attempts+=1;need(attempts<=500000 and time.monotonic()-start<20,'INCOMPLETE fixed independent typed-count guard')
                D=tuple(u+2*t for u,t in zip(unit,double))
                if D not in valid:continue
                weights[D]+=1
                if accepted(unit,double):valid[D].append([u+t for u,t in zip(unit,double)])
        expected=[dict(D4=list(D),typed_weight_allocations=weights[D],passing_support_N4=sorted(valid[D])) for D in sorted(projected)]
        need(expected==rec['rows'],'every degree target, typed multiplicity and support witness differs')
        need(not any(valid.values()),'independent typed support survivor')
        need(sum(weights.values())==rec['typed_weight_allocations'],'whole pre-support count')
        statistics.append(dict(unit_rows=U,double_rows=V,degree_targets=len(projected),typed_weight_allocations=sum(weights.values()),passing_support_allocations=0))
    need(author['degree_target_count']==len(projected),'whole target rectangle')
    need(accepted((2,2,2,2),(3,3,0,0)),'independent positive abstract partition')
    need(not accepted((2,0,0,2),(2,4,4,0)),'independent strict threshold rejection')
    need(accepted((2,0,0,2),(2,4,4,0),threshold=4),'independent weakened-threshold survivor')
    result=dict(agent='six-code-3',role='researcher',status='COMPLETE_TWO_ALGORITHM_FOCUSED_T4_SUPPORT_AGREEMENT',degree_targets=len(projected),statistics=statistics,independent_typed_compositions_checked=attempts,all_target_rows_and_pre_support_multiplicities_match=True,all_actual_T4_survivors_excluded=True,controls=dict(positive_partition=1,strict_support_rejection=1,weakened_support_positive=1),ordinary_bridges_formalized=False,external_review=False,new_unrestricted_code_bound=None,elapsed_seconds=time.monotonic()-start)
    out=S/'pass18-t4-independent-support.json';need(not out.exists(),'fresh independent output');out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
