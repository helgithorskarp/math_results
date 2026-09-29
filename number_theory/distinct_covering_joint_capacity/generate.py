"""Optional one-thread LP discovery; every emitted integer vector is checked.

Requires the sibling residual-weight-duals orbit helper and SciPy/NumPy.
The published proof uses check.py and certificate.json, without a solver.
Degenerate optima can produce different valid weight vectors.
"""
import argparse
from collections import Counter
import json
from math import gcd,lcm
from pathlib import Path
import sys
import warnings
from check import L,PREFIX,PAIRS,PERIODS,verify
from audit import phase_events
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'distinct_covering_residual_weight_duals'))
from orbits import orbit_data,boxes_from_weights


def generate():
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    orbits,_=orbit_data(L,PREFIX);width=len(orbits)
    available=[m for m in range(8,L+1) if L%m==0 and m not in {n for n,a in PREFIX}]
    paired={m for pair in PAIRS for m in pair}
    groups=list(PAIRS)+[(m,) for m in available if m not in paired]
    needed=set(available)|{lcm(m,n) for m,n in PAIRS}
    populations={m:[Counter() for a in range(m)] for m in needed}
    for j,orbit in enumerate(orbits):
        for x in orbit:
            for m in needed: populations[m][x%m][j]+=1
    rr=[];cc=[];vv=[];row=0
    for i,group in enumerate(groups):
        vectors=set()
        if len(group)==1:
            vectors={tuple(sorted(counts.items())) for counts in populations[group[0]] if counts}
        else:
            m,n=group;g=gcd(m,n);ell=lcm(m,n);inverse=pow(m//g,-1,n//g)
            for a in range(m):
                for b in range(n):
                    counts=populations[m][a]+populations[n][b]
                    if (b-a)%g==0:
                        phase=(a+m*((b-a)//g*inverse%(n//g)))%ell
                        counts.subtract(populations[ell][phase])
                    if any(v<0 for v in counts.values()): raise ValueError('Negative union coefficient')
                    vector=tuple(sorted((j,v) for j,v in counts.items() if v))
                    if vector: vectors.add(vector)
        for vector in sorted(vectors):
            for j,value in vector: rr.append(row);cc.append(j);vv.append(value)
            rr.append(row);cc.append(width+i);vv.append(-1);row+=1
    matrix=coo_matrix((vv,(rr,cc)),shape=(row,width+len(groups))).tocsr()
    equality=coo_matrix(([len(O) for O in orbits],([0]*width,list(range(width)))),shape=(1,width+len(groups))).tocsr()
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore',message='Unrecognized options detected')
        result=linprog(np.r_[np.zeros(width),np.ones(len(groups))],A_ub=matrix,b_ub=np.zeros(row),
                       A_eq=equality,b_eq=[1],bounds=(0,None),method='highs',
                       options={'threads':1,'time_limit':5})
    if result.x is None or result.fun is None or result.fun>=1:
        raise RuntimeError(f'No certificate found, LP status {result.status}; no exclusion inferred')
    for scale in (1000,10000,100000,1000000,10000000):
        values=[max(0,int(round(float(t)*scale))) for t in result.x[:width]]
        weights={x:w for O,w in zip(orbits,values) if w for x in O}
        vector=[weights.get(x,0) for x in range(L)]
        single={m:max(sum(vector[a::m]) for a in range(m)) for m in available}
        # Fast CRT proposal for the joint capacities, independently checked below.
        joint=sum(v for m,v in single.items() if m not in paired)
        joint+=sum(max(event[-1] for event in phase_events(vector,m,n)) for m,n in PAIRS)
        if sum(vector)<=joint: continue
        payload={'L':L,'minimum':8,'anchors':[list(v) for v in PREFIX],'pairs':[list(v) for v in PAIRS],
                 'boxes':boxes_from_weights(L,PREFIX,weights),'demand':sum(vector),
                 'joint_capacity':joint,'individual_capacity':sum(single.values())}
        checked=verify(payload)
        print(json.dumps({'discovery_status':result.status,'floating_objective':float(result.fun),
                          'point_orbits':width,'row_count':row,'checked_gap':checked['strict_gap']}),flush=True)
        return payload
    raise RuntimeError('Integer reconstruction failed; no exclusion inferred')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();payload=generate()
    args.output.write_text(json.dumps(payload,indent=2)+'\n')
