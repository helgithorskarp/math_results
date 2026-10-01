#!/usr/bin/env python3
"""Exact parameter classification for three exceptional ternary columns."""
import argparse
import json
import math
from pathlib import Path

def need(condition,message):
    if not condition:raise ValueError(message)

def representatives(q):
    need(q>=7 and all(q%d for d in range(2,math.isqrt(q)+1)), 'q must be prime >=7')
    rows=[]
    for kind in ('same','mixed'):
        unseen=set(range(2,q))
        while unseen:
            lam=min(unseen)
            if kind=='same':
                inverse=pow(lam,-1,q); other_inverse=pow(1-lam,-1,q)
                orbit={lam,(1-lam)%q,inverse,other_inverse,(lam*pow(lam-1,-1,q))%q,((lam-1)*inverse)%q}
                stabilizer=6//len(orbit)
            else:
                orbit={lam,(1-lam)%q};stabilizer=2//len(orbit)
            need(orbit<=unseen,'Parameter classes intersect')
            rows.append({'kind':kind,'lambda':lam,'parameter_orbit':sorted(orbit),
                         'skeleton_stabilizer_order':stabilizer,
                         'raw_skeleton_orbit_size':6*q*(q-1)//stabilizer})
            unseen-=orbit
    return rows

def skeleton(q,kind,lam):
    need(q>=7 and all(q%d for d in range(2,math.isqrt(q)+1)), 'q must be prime >=7')
    need(kind in ('same','mixed') and 1<lam<q,'Malformed representative')
    tau=[0]*q;tau[0]=tau[1]=1;tau[lam]=1 if kind=='same' else 2
    return tau

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--q',type=int,default=103)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();rows=representatives(args.q)
    record={'agent':'six-vdw-3','role':'researcher','q':args.q,'representatives':rows,
            'representative_count':len(rows),'raw_skeleton_count':4*args.q*(args.q-1)*(args.q-2),
            'orientation_bits_per_representative':args.q,'global_complement_normalized_free_bits':args.q-1,
            'orientation_invariance_imposed':False}
    args.output.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({key:value for key,value in record.items() if key!='representatives'}))

if __name__=='__main__':main()
