#!/usr/bin/env python3
"""Cold complete-record verification and a separate nodal Bernstein identity route."""
from pathlib import Path
from fractions import Fraction as Q
from math import comb
import json
import check

def evaluate(p,x):
    out=Q(0)
    for v in reversed(p):out=out*x+Q(v)
    return out

def verify_list(h,coeff,band):
    n=len(h)-1
    check.need(len(coeff)==n+1,'entire coefficient list')
    check.need(all(v>0 for v in coeff) or all(v<0 for v in coeff),'strict sign including endpoint coefficients')
    # Difference has degree <=n. Equality at n+1 DISTINCT exact nodes proves identity.
    a,b=band
    for i in range(n+1):
        t=Q(i,n) if n else Q(0)
        rhs=sum(coeff[k]*comb(n,k)*t**k*(1-t)**(n-k) for k in range(n+1))
        check.need(evaluate(h,a+(b-a)*t)==rhs,'whole polynomial identity at complete nodal set')

def run():
    expected=json.loads((Path(__file__).parent/'EXPECTED.json').read_text())
    actual=check.run();check.need(check.canonical(actual)==check.canonical(expected),'whole canonical fresh record equals included record')
    nodes=0
    for row in expected['witnesses'].values():
        h=tuple(Q(v) for v in row['h'])
        for name,band in (('bernstein_original',check.J),('bernstein_wider',check.WIDE)):
            verify_list(h,tuple(Q(v) for v in row[name]),band);nodes+=len(h)
    row=next(iter(expected['witnesses'].values()));h=tuple(Q(v) for v in row['h']);damaged=[Q(v) for v in row['bernstein_wider']];damaged[0]+=1
    caught=False
    try:verify_list(h,damaged,check.WIDE)
    except ValueError:caught=True
    check.need(caught,'damaged otherwise-signed coefficient must reject')
    return dict(agent='six-reviewer-2',role='independent mathematical reviewer',whole_expected_equal=True,complete_nodal_identities=76,distinct_exact_nodes=nodes,damaged_coefficient_rejected=True)

if __name__=='__main__':print(json.dumps(run(),sort_keys=True,separators=(',',':')))
