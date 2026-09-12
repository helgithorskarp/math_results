"""Exact complete task ranges and size comparison, using integer arithmetic."""
from pathlib import Path
from math import comb
import json
HERE=Path(__file__).resolve().parent


def carrier():
    old=json.loads((HERE.parent/'ramsey_r55_maximal_block_order/TASKS.json').read_text())
    ranges=[];removed=[];before=after=0
    sizes={7:640,8:546356,9:362,10:4}
    for c in old['classes']:
        q,r=c['q'],c['r'];A,B=r-1,q-r
        count=comb(1998+A-1,A)*comb(1931+B-1,B)*37823**(comb(A,2)+comb(B,2))*35714**(A*B)*15**(q*(43-4*q))
        if count!=c['per_task'] or (c['core_start'],c['core_stop'])!=(0,sizes[q]):
            raise ValueError('inherited carrier count')
        before+=count*sizes[q]
        row=dict(q=q,r=r,core_start=0,core_stop=sizes[q],task_count=sizes[q],
                 first_task=c['first_task'],last_task=c['last_task'])
        if q==7 and r<7:removed.append(row)
        else:ranges.append(row);after+=count*sizes[q]
    if before!=old['P'] or not 0<after<before:raise ValueError('strict complete-carrier reduction')
    return dict(status='STRICTLY_SMALLER_GLOBALLY_COMPLETE_CARRIER',old_macros=18,new_macros=16,
                old_task_count=2189178,new_task_count=sum(r['task_count'] for r in ranges),
                removed_task_count=sum(r['task_count'] for r in removed),
                removed_ranges=removed,retained_ranges=ranges,old_bo1_labeled_carrier=before,
                new_bo1_labeled_carrier=after,removed_bo1_labeled_carrier=before-after,
                new_original_task_verdicts=0,
                scope='Exact unfiltered ordered pair/star carrier sizes; no runtime or filtered-volume claim')


if __name__=='__main__':print(json.dumps(carrier(),sort_keys=True,indent=2))
