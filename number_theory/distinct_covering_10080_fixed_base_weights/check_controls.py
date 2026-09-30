"""Complete ordinary-predicate controls for the fixed-base weight checker.

Actual author six-covering-1, researcher. Optional classes and every phase
are enumerated in four tiny coprime periods with several nonuniform weights.
"""
import hashlib
import itertools
import json
from pathlib import Path
import time
from check import ordinary_audit


def main():
    start=time.monotonic(); events=hashlib.sha256(); families=[]; vectors=0
    for B,C,labels in ((4,3,[2,3,4,6]),(4,5,[2,4,5,10]),
                       (3,5,[3,5,15]),(12,5,[3,4,5,10])):
        N=B*C
        for f in ([1]*B,[z%4 for z in range(B)],
                  [2 if z%3==0 else 0 for z in range(B)]):
            count=0
            choices=[[None]+list(range(m)) for m in labels]
            for option in itertools.product(*choices):
                rows=[(a,m) for a,m in zip(option,labels) if a is not None]
                result=ordinary_audit(N,B,C,rows,f)
                F=[f[x%B] for x in range(N)]
                tails=[m for a,m in rows if m%C==0]
                cap=sum(max(sum(F[x] for x in range(N) if x%m==a)
                            for a in range(m)) for m in tails)
                R=sum(sum(f[z] for z in range(B) if z%m==a)
                      for a,m in rows if m%C)
                holes=[x for x in range(N) if all(x%m!=a for a,m in rows)]
                gap=C*sum(f)-cap
                lower=(max(0,gap-C*R)+max(f)-1)//max(f)
                if (result['tail_capacity']!=cap
                        or result['fixed_base_phase_weight_sum']!=R
                        or result['literal_fixture_holes']!=len(holes)
                        or result['minimum_physical_holes']!=lower
                        or sum(F[x] for x in holes)<max(0,gap-C*R)
                        or len(holes)<lower
                        or (not holes and C*R<gap)):
                    raise ValueError('Complete toy control differs')
                events.update(json.dumps([B,C,option,f,cap,R,len(holes),lower]).encode())
                count+=1
            families.append(dict(base_period=B,prime=C,labels=labels,weights=f,vectors=count))
            vectors+=count
    bad=[(12,4,3,[(0,2),(1,2)],[0,1,2,3]),
         (12,4,3,[(0,5)],[0,1,2,3]),
         (12,4,3,[(2,2)],[0,1,2,3]),
         (12,4,3,[(0,2)],[0,1,2,True]),
         (12,4,3,[(0,2)],[0,1,2,-1]),
         (12,4,3,[(0,2)],[0,0,0,0])]
    rejected=0
    for args in bad:
        try:ordinary_audit(*args)
        except ValueError:rejected+=1
        else:raise ValueError('Malformed control was accepted')
    obj=dict(agent='six-covering-1',role='researcher',status='COMPLETE_LITERAL_CONTROLS_PASSED',
             complete_families=len(families),phase_and_omission_vectors=vectors,
             malformed_rejections=rejected,events_sha256=events.hexdigest(),
             families=families,seconds=time.monotonic()-start,
             scope='Only checker controls; no mathematical global exclusion from toy enumeration')
    print(json.dumps({k:v for k,v in obj.items() if k!='families'}))


if __name__=='__main__':main()
