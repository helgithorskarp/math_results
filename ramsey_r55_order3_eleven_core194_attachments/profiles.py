#!/usr/bin/env python3
"""Exact degree-profile cover for a distinguished Core194 blue empty pair."""
from math import factorial
from pathlib import Path
import argparse
import json


def require(ok,why):
    if not ok:raise ValueError(why)


def multinomial(counts):
    answer=factorial(sum(counts))
    for n in counts:answer//=factorial(n)
    return answer


def contacts(counts):
    a,b,c=counts
    return [(True,True)]*a+[(True,False)]*b+[(False,True)]*c


def moving_units(counts):
    rows=[]
    for i,(u,v) in enumerate(contacts(counts),4):
        rows += [211+i if u else -(211+i),222+i if v else -(222+i)]
    return rows


def fixed_units(counts):
    rows=[]
    for k,(u,v) in enumerate(contacts(counts)):
        rows += [167+k if u else -(167+k),175+k if v else -(175+k)]
    return rows


def certificate():
    profiles=[]
    for b in range(4):
        for c in range(b,4):
            a=7-b-c
            if b==c==0:continue
            for y in range(9):
                for z in range(9-y):
                    if b==c and y>z:continue
                    x=8-y-z
                    du=3*(a+b)+x+y;dv=3*(a+c)+x+z
                    if not(18<=du<=24 and 18<=dv<=24):continue
                    counts=[a,b,c,x,y,z]
                    weight=multinomial(counts[:3])*multinomial(counts[3:])
                    if (b,y)!=(c,z):weight*=2
                    profiles.append(dict(counts=counts,red_degrees=[du,dv],labeled_assignments=weight,
                        units=moving_units(counts[:3])+fixed_units(counts[3:])))
    profiles.sort(key=lambda r:r['counts'])
    moving=[]
    for abc in sorted({tuple(r['counts'][:3]) for r in profiles}):
        rows=[r for r in profiles if tuple(r['counts'][:3])==abc]
        moving.append(dict(id='a%d_b%d_c%d'%abc,counts=list(abc),joint_profiles=len(rows),
            labeled_assignments=sum(r['labeled_assignments'] for r in rows),units=moving_units(abc)))
    require(len(profiles)==119 and len(moving)==9,'derived complete profile counts')
    return dict(types=['RR','RB','BR'],counts_order=['a','b','c','x','y','z'],
        pair=[33,34],blue_cycles=list(range(4,11)),other_fixed=list(range(35,43)),
        degree_window=[18,24],profiles=profiles,moving_cases=moving,
        all_no_BB_assignments=3**15,allowed_labeled_assignments=sum(r['labeled_assignments'] for r in profiles),
        scope='two-star degree relaxation, not full graph realizability')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    a.output.write_text(json.dumps(certificate(),indent=2,sort_keys=True)+'\n')
    print('Generated119joint profiles and9moving cases')
