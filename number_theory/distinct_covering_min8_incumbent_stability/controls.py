"""Meaningful malformed/incomplete-certificate controls; standard library."""
import copy
import json
from pathlib import Path

from check import budget, compute, residual

ROOT=Path(__file__).resolve().parent


def main():
    inputs=[json.loads((ROOT/name).read_text()) for name in ('core.json','upper_cover.json','weights.json')]
    result=compute(*inputs)
    if result['exact_family_minimum_lcm']!=20160:raise ValueError('positive control failed')
    labels=[]
    for name in ('missing_core','duplicate_core','bad_upper_phase','missing_weight_case',
                 'missing_resource','covered_weight','negative_weight','wrong_demand','nonstrict_cut'):
        core,upper,weights=copy.deepcopy(inputs)
        cut=weights['cuts'][0]
        if name=='missing_core':core['congruences'].pop()
        elif name=='duplicate_core':core['congruences'][1]=core['congruences'][0]
        elif name=='bad_upper_phase':upper['congruences'][0][0]=8
        elif name=='missing_weight_case':weights['cuts'].pop(0)
        elif name=='missing_resource':cut['capacities'].pop()
        elif name=='negative_weight':cut['weights'][0][1]=-1
        elif name=='wrong_demand':cut['demand']+=1
        else:
            prefix=[row for row in core['congruences'] if row[1] not in cut['removed']]
            points=residual(prefix)
            if name=='covered_weight':
                x=next(x for x in range(5040) if x not in set(points))
                cut['weights'].append([x,1]);cut['weights'].sort()
            else:
                free=[m for m in range(8,cut['period']+1)
                      if cut['period']%m==0 and m not in {m for a,m in prefix}]
                cut['weights']=[[x,1] for x in points]
                cut['demand'],cut['capacities']=budget(cut['period'],free,points,[1]*len(points))
                if cut['demand']>sum(c for m,c in cut['capacities']):raise ValueError('nonstrict fixture is strict')
        try:compute(core,upper,weights)
        except ValueError:labels.append(name)
        else:raise ValueError('corrupted certificate accepted: '+name)
    print(json.dumps({'status':'CONTROLS_PASSED','positive_full_certificate':True,'rejected':labels}))


if __name__=='__main__':main()
