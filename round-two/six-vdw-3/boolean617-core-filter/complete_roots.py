#!/usr/bin/env python3
"""Find literal unit-demand APs forcing a monochromatic actual vertical AP.

A missing certificate is explicitly an incomplete mechanism, never infeasibility.
All original roots remain arbitrary at every integer occurrence.
"""
import argparse
import json
from pathlib import Path

P=617
N=3704


def complete(start,stop):
    char=[None]+[int(pow(z,308,P)!=1) for z in range(1,P)]
    rows=[]
    for t in range(start,stop):
        if t in (1,2):
            continue
        roots={1,2,t}
        for projected_root in (1,2,t):
            choices=[]
            for column in (1,2):
                if column == projected_root:
                    continue
                original=char[(column-projected_root)%P]
                demands=[]
                failed=[]
                for point in range(column,N+1,P):
                    found=None
                    for slot in range(7):
                        if found is not None:
                            break
                        for d in range(1,618):
                            a=point-slot*d
                            if a<1 or a+6*d>N:
                                continue
                            support=[a+k*d for k in range(7) if k!=slot]
                            if any(n%P in roots for n in support):
                                continue
                            colors=[char[(n-projected_root)%P] for n in support]
                            if all(v==1-original for v in colors):
                                found=[point,a,d,slot]
                                break
                    if found is None:
                        failed.append(point)
                    else:
                        demands.append(found)
                choices.append({'column':column,'forced_color':original,'unit_demands':demands,'missing_points':failed})
                if not failed:
                    break
            closed=next((choice for choice in choices if not choice['missing_points']),None)
            rows.append({'t':t,'projected_root':projected_root,
                         'status':'LITERAL_UNIT_VERTICAL_CONTRADICTION' if closed else 'UNIT_MECHANISM_INCOMPLETE_NO_EXCLUSION',
                         'certificate':closed,'attempted_columns':choices if closed is None else None})
    return {'schema':'boolean617-actual-interval-unit-v1','agent':'six-vdw-3','role':'researcher',
            'prime':P,'interval':N,'third_root_range':[start,stop],'cases':rows,
            'scope':'Projection regular color, roots1,2,t individually free at every occurrence; no extra edited columns.'}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--start',type=int,required=True);parser.add_argument('--stop',type=int,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if not 0<=args.start<args.stop<=P:
        raise ValueError('invalid half-open third-root range')
    result=complete(args.start,args.stop)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    failed=[(r['t'],r['projected_root']) for r in result['cases'] if r['certificate'] is None]
    print(json.dumps({'range':result['third_root_range'],'cases':len(result['cases']),
                      'literal_contradictions':len(result['cases'])-len(failed),
                      'unit_mechanism_incomplete':failed}))


if __name__=='__main__':
    main()
