#!/usr/bin/env python3
"""Literal independent square-set verification of interval unit certificates."""
import argparse
import hashlib
import json
from pathlib import Path


def demand(ok, why):
    if not ok:
        raise ValueError(why)


def verify(record):
    p,n=617,3704
    demand(record['schema']=='boolean617-actual-interval-unit-v1','schema')
    demand(record['prime']==p and record['interval']==n,'prime/interval')
    start,stop=record['third_root_range']
    demand(type(start) is int and type(stop) is int and 0<=start<stop<=p,'range')
    wanted=[(t,r) for t in range(start,stop) if t not in (1,2) for r in (1,2,t)]
    demand([(row['t'],row['projected_root']) for row in record['cases']]==wanted,'every projection/root case exactly once')
    squares={x*x%p for x in range(1,p)}
    demand(len(squares)==308 and 0 not in squares,'square set')
    points=demands=vertical_points=closed=0
    stream=hashlib.sha256()
    incomplete=[]
    for row in record['cases']:
        t,r=row['t'],row['projected_root']
        roots={1,2,t}
        cert=row['certificate']
        if cert is None:
            demand(row['status']=='UNIT_MECHANISM_INCOMPLETE_NO_EXCLUSION','incomplete status')
            incomplete.append([t,r])
            continue
        demand(row['status']=='LITERAL_UNIT_VERTICAL_CONTRADICTION','closed status')
        q=cert['column'];forced=cert['forced_color']
        demand(type(q) is int and q in (1,2) and q!=r,'target column must be nonprojected original root')
        demand(type(forced) is int and forced==int((q-r)%p not in squares),'forced original character color')
        demand(cert['missing_points']==[] and len(cert['unit_demands'])==7,'complete vertical unit cover')
        expected_points=list(range(q,n+1,p))
        demand([d[0] for d in cert['unit_demands']]==expected_points,'all actual vertical positions')
        for point,a,d,slot in cert['unit_demands']:
            demand(all(type(v) is int for v in (point,a,d,slot)),'integer witness data')
            demand(a>=1 and d>=1 and a+6*d<=n and 0<=slot<7,'ordinary interval AP')
            demand(a+slot*d==point and point%p==q,'target point identity')
            demand(len({a+j*d for j in range(7)})==7,'nonconstant AP')
            colors=[]
            for j in range(7):
                if j==slot:
                    continue
                x=a+j*d
                demand(x%p not in roots,'a unit-demand support hits an arbitrary free root')
                color=int((x-r)%p not in squares)
                colors.append(color);points+=1
            demand(colors==[1-forced]*6,'six fixed opposing colors must force the target')
            demands+=1
            stream.update(f'{t},{r},{q},{forced},{point},{a},{d},{slot}\n'.encode())
        demand(expected_points==[q+j*p for j in range(7)] and expected_points[-1]<=n,'actual nonconstant vertical AP')
        vertical_points+=7
        closed+=1
    return {'schema':'boolean617-actual-interval-unit-check-v1',
            'status':'COMPLETE_LITERAL_INTERVAL_EXCLUSION' if not incomplete else 'PARTIAL_POSITIVE_CERTIFICATES_NO_COMPLETE_EXCLUSION',
            'third_root_range':[start,stop],'projection_cases':len(wanted),'closed_cases':closed,
            'incomplete_cases':incomplete,'literal_unit_APs':demands,'fixed_support_points_checked':points,
            'vertical_AP_points_checked':vertical_points,'unit_transcript_sha256':stream.hexdigest()}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--input',type=Path,required=True);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    receipt=verify(json.loads(args.input.read_text()))
    args.output.write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(json.dumps(receipt))


if __name__=='__main__':
    main()
