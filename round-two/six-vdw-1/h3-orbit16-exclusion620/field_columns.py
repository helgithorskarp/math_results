"""Exact necessary fixed-phase H3 field-column census, not a full core search."""
import argparse
import json
from pathlib import Path


def census():
    remaining = set(range(1,31)); cosets = []
    while remaining:
        a = min(remaining)
        orbit = sorted({a,5*a%31,25*a%31})
        if len(orbit)!=3 or not set(orbit)<=remaining:
            raise ValueError('actual multiplicative partition')
        cosets.append(orbit); remaining -= set(orbit)
    where = {r:i for i,c in enumerate(cosets) for r in c}
    aps = []
    for start in range(31):
        for step in range(1,31):
            terms = [(start+j*step)%31 for j in range(7)]
            if 0 in terms: continue
            support = sum(1<<i for i in {where[r] for r in terms})
            aps.append((start,step,support))
    supports = sorted({p[2] for p in aps})
    admissible=[]; excluded=[]
    for mask in range(1024):
        witness=next(((a,d,int(mask&s==s)) for a,d,s in aps if mask&s in [0,s]),None)
        if witness is None: admissible.append(mask)
        else: excluded.append([mask,*witness])
    return {'author':'six-vdw-1','role':'researcher','status':'COMPLETE_NECESSARY_H3_FIXED_PHASE_CENSUS',
            'field_prime':31,'AP_length':7,'H3':[1,5,25],'cosets':cosets,'all_input_masks':1024,
            'actual_regular_field_APs':len(aps),'distinct_unsigned_supports':len(supports),
            'support_size_histogram':{str(k):sum(s.bit_count()==k for s in supports) for k in range(1,8)},
            'admissible_count':len(admissible),'admissible_masks':admissible,'excluded_count':len(excluded),
            'excluded_actual_field_AP_witnesses':excluded,
            'scope':'Necessary tests for a single fixed phase of a CHOSEN H3-invariant regular620 core; not full100-input feasibility or a W bound.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output',type=Path);a=p.parse_args()
    if a.output.exists():raise ValueError('preserve exact field-column census')
    result=census();a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['admissible_masks','excluded_actual_field_AP_witnesses']},sort_keys=True),flush=True)
