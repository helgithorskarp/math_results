"""Canonical-log affine phase-power profiles and actual AP certificates."""
import argparse
import csv
import json
from pathlib import Path

REPS=[8,10,12,16,20,34,72]


def full(mask):return [((mask>>(s%10))&1)^(s//10) for s in range(20)]


def produce():
    logarithm={};r=1
    for i in range(30):
        if r in logarithm:raise ValueError('field root not primitive')
        logarithm[r]=i;r=3*r%31
    if r!=1 or set(logarithm)!=set(range(1,31)):raise ValueError('complete primitive field coordinates')
    units=[u for u in range(20) if len({u*s%20 for s in range(20)})==20]
    CRT={(r,s):next(x for x in range(620) if x%31==r and x%20==s) for r in range(31) for s in range(20)}
    records=[];attempts=0;eligible=bad=positive=0
    for mask in REPS:
        b=full(mask)
        for u in units:
            for t in range(20):
                perm=[(u*s+t)%20 for s in range(20)];powers=[list(range(20))]
                for _ in range(30):powers.append([perm[s] for s in powers[-1]])
                mismatch=next((s for s in range(20) if b[powers[30][s]]!=b[s]),None)
                closed=int(mismatch is None)
                eligible+=closed
                word=[None if x%31==0 else b[powers[logarithm[x%31]][x%20]] for x in range(620)]
                witness=None
                # For closed profiles this is complete; otherwise it is a witness search only.
                for a in range(1,31):
                    if any((a+j)%31==0 for j in range(7)):continue
                    for s in range(20):
                        if witness is not None:break
                        start=CRT[a,s]
                        for h in range(20):
                            d=CRT[1,h];terms=[word[(start+j*d)%620] for j in range(7)];attempts+=1
                            if len(set(terms))==1:
                                if d>310:start=(start+6*d)%620;d=620-d
                                witness=[start,d,terms[0]];break
                    if witness is not None:break
                if witness is None:
                    positive+=1;records.append([mask,u,t,closed,'CORE',-1,-1,-1])
                else:
                    bad+=1;records.append([mask,u,t,closed,'BAD_AP',*witness])
    return records,{'author':'six-vdw-1','role':'researcher','status':'ALL_CANONICAL_PHASE_POWER_PROFILES_HAVE_ACTUAL_BAD_APS' if not positive else 'UNTRUSTED_REGULAR_CORE_PROPOSALS',
                    'normalized_base_generator_inputs':1120,'closure_eligible':eligible,'explicit_bad_APs':bad,'partial_core_proposals':positive,
                    'witness_search_APs_per_profile_max':9600,'complete_normalization_only_for_closed_transport':True,'normalized_AP_attempts':attempts,
                    'scope':'All canonical-log affine phase-power parameters at primitive root3 only; not arbitrary regular620 cores or W(2,7).'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output',type=Path);a=p.parse_args()
    if a.output.exists():raise ValueError('preserve canonical phase-power catalogue')
    records,result=produce()
    with a.output.open('w',newline='') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['row','u','t','closed','status','a','d','color']);w.writerows(records)
    print(json.dumps(result,sort_keys=True),flush=True)
