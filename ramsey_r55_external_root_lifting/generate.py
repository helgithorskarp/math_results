#!/usr/bin/env python3
"""Optional numerical discovery; output is checked with exact integer arithmetic."""
import argparse
from fractions import Fraction
from math import gcd,lcm
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog,milp,Bounds,LinearConstraint
import model


def primal(rows):
    A=np.array([a for a,b in rows]);b=np.array([b for a,b in rows]);n=A.shape[1]
    r=milp(np.zeros(n),integrality=np.ones(n),bounds=Bounds(0,np.inf),
           constraints=LinearConstraint(A,-np.inf,b),options={'time_limit':5})
    if not r.success:raise ValueError('No exact-primal candidate: '+r.message)
    z=[round(v) for v in r.x]
    if not all(sum(a*v for a,v in zip(row,z))<=bound for row,bound in rows):
        raise ValueError('Rounded primal rejected')
    return z


def dual(rows):
    A=np.array([a for a,b in rows]);b=np.array([b for a,b in rows])
    r=linprog(b,A_eq=np.concatenate((A.T,np.ones((1,len(rows))))),
              b_eq=[0]*A.shape[1]+[1],bounds=(0,None),method='highs')
    if not r.success or r.fun>=-1e-7:raise ValueError('No negative dual candidate')
    fractions=[Fraction(float(v)).limit_denominator(1000000) for v in r.x]
    den=lcm(*(v.denominator for v in fractions));nums=[int(v*den) for v in fractions]
    factor=gcd(*nums);nums=[v//factor for v in nums]
    if any(v<0 for v in nums):raise ValueError('Negative dual multiplier')
    if any(sum(v*row[i] for v,(row,b) in zip(nums,rows)) for i in range(A.shape[1])):
        raise ValueError('Nonzero exact dual coefficient')
    rhs=sum(v*b for v,(row,b) in zip(nums,rows))
    if rhs>=0:raise ValueError('Nonnegative dual bound')
    return {'multipliers':[[i,v] for i,v in enumerate(nums) if v],'rhs':rhs}


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();records=[]
    for mask in (3,7):
        for y in model.vectors(mask):
            orb=model.orbit(mask,y)
            if min(orb)!=(mask,y):continue
            failed=None;record={'mask':mask,'y':y,'orbit_size':len(orb)}
            for stage in range(3):
                rows=model.system(mask,y,stage)
                A=np.array([a for a,b in rows]);b=np.array([b for a,b in rows])
                result=linprog(np.zeros(A.shape[1]),A_ub=A,b_ub=b,bounds=(None,None),method='highs')
                if not result.success:
                    # Solver infeasibility by itself is never an output claim.
                    record['dual']=dual(rows);failed=stage;break
            record['first_failed_stage']=failed
            stage=2 if failed is None else failed-1
            if stage>=0:record['primal']=primal(model.system(mask,y,stage))
            records.append(record)
    args.output.write_text(json.dumps(records,indent=2,sort_keys=True)+'\n')
    print(f'Discovered {len(records)} orbit certificates; run verify.py before relying on them')


if __name__=='__main__':main()
