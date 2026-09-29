"""Optional floating discovery of the stored exact integer certificates.

Solver success is insufficient: every returned certificate is checked by
check.py. A timeout or failed reconstruction raises and proves nothing.
Verified discovery environment: NumPy 2.4.6, SciPy 1.17.1, CPython 3.11.2.
"""
import argparse
import json
from pathlib import Path
import warnings
from orbits import boxes_from_weights, divisors, quotient_rows
from check import FIRST, SECOND, SECOND_PHASE, PREFIX, L, PERIODS, normalize42, normalize45, exact_check


def find_certificate(anchors,time_limit=5):
    import numpy as np
    from scipy.sparse import coo_matrix
    from scipy.optimize import linprog
    remaining=[m for m in divisors(L) if m>=8 and m not in dict(anchors)]
    orbits,rows=quotient_rows(L,anchors,remaining)
    n=len(orbits)
    offsets={m:n+i for i,m in enumerate(remaining)}
    rr=[]; cc=[]; vv=[]
    for i,(m,key,coefficients) in enumerate(rows):
        for j,value in coefficients.items(): rr.append(i); cc.append(j); vv.append(value)
        rr.append(i); cc.append(offsets[m]); vv.append(-1)
    shape=(len(rows),n+len(remaining))
    matrix=coo_matrix((vv,(rr,cc)),shape=shape).tocsr()
    equality=coo_matrix(([len(o) for o in orbits],([0]*n,list(range(n)))),shape=(1,shape[1])).tocsr()
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore',message='Unrecognized options detected')
        result=linprog(np.r_[np.zeros(n),np.ones(len(remaining))],A_ub=matrix,b_ub=np.zeros(len(rows)),
                       A_eq=equality,b_eq=[1],bounds=(0,None),method='highs',
                       options={'time_limit':time_limit,'threads':1})
    if result.x is None:
        raise RuntimeError(f'Inconclusive solver result: {result.status}: {result.message}')
    for scale in (1000,10000,100000,1000000,10000000):
        weights={x:int(round(t*scale)) for orbit,t in zip(orbits,result.x[:n]) if round(t*scale)>0 for x in orbit}
        vector=[weights.get(x,0) for x in range(L)]
        try: exact_check(anchors,vector)
        except ValueError: continue
        return boxes_from_weights(L,anchors,weights)
    raise RuntimeError('No exact strict certificate was reconstructed; no exclusion is inferred.')


def generate():
    first={}; second={}; pool=[]; ids={}
    def add(anchors):
        boxes=find_certificate(anchors)
        key=json.dumps(boxes,separators=(',',':'))
        if key not in ids: ids[key]=len(pool); pool.append(boxes)
        return ids[key]
    first_phases=sorted({normalize42(a)[0] for a in range(FIRST)})
    second_phases=sorted({normalize45(a)[0] for a in range(SECOND)})
    for a in first_phases:
        if a!=SECOND_PHASE:
            first[str(a)]=add(PREFIX+[(FIRST,a)])
            print(f'certified 42 phase {a}',flush=True)
    for a in second_phases:
        second[str(a)]=add(PREFIX+[(FIRST,SECOND_PHASE),(SECOND,a)])
        print(f'certified 45 phase {a}',flush=True)
    return {'schema':1,'agent':'six-covering-2','role':'researcher','L':L,'minimum':8,
            'prime_power_axes':PERIODS,'prefix':PREFIX,'first':first,'second':second,'boxes':pool}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',type=Path,required=True)
    args=parser.parse_args()
    args.write.write_text(json.dumps(generate(),separators=(',',':'))+'\n')
