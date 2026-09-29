"""Alternative exact audit: no CRT box decoding, histograms, or solver.

The proof table is expanded by literal integer remainders. Phase transport
is an integer permutation computed by trial along a complementary period.
Every actual phase is checked with direct arithmetic-progression sums.
Stabilizer orbits are separately checked using literal tree generators.
"""
from collections import defaultdict
from hashlib import sha256
from itertools import combinations
import json
from math import prod
from pathlib import Path
import random
from time import monotonic
from check import L,PERIODS,PREFIX
from orbits import divisors,factor_levels,orbit_data,quotient_rows


def literal_decode(boxes):
    candidates=[[box for box in boxes if box[0]>>r&1] for r in range(32)]
    result=[]
    for x in range(L):
        hits=[box[-1] for box in candidates[x%32]
              if all(box[i]>>(x%P)&1 for i,P in enumerate(PERIODS[1:],1))]
        if len(hits)>1: raise ValueError('Literal overlapping boxes')
        result.append(hits[0] if hits else 0)
    return result


def transport(weights,P,a,b):
    if a==b: return weights
    step=L//P
    result=[]
    for x in range(L):
        residue=x%P
        target=b if residue==a else a if residue==b else residue
        y=next((x+k*step)%L for k in range(P) if (x+k*step)%P==target)
        result.append(weights[y])
    return result


def literal_check(anchors,weights):
    for m,a in anchors:
        if any(weights[x] for x in range(a,L,m)): raise ValueError('Covered positive-weight point')
    assigned={m for m,a in anchors}
    demand=sum(weights)
    capacity=sum(max(sum(weights[x] for x in range(a,L,m)) for a in range(m))
                 for m in range(8,L+1) if L%m==0 and m not in assigned)
    if demand<=capacity: raise ValueError('Non-strict literal certificate')
    return demand,capacity


def audit_certificate(payload):
    decoded=[literal_decode(boxes) for boxes in payload['boxes']]
    events=[]
    for phase42 in range(42):
        if phase42==29:
            for phase45 in range(45):
                r=phase45%9; root=r%3
                normalized=root if root in (1,2) else r
                representative=next(b for b in range(45) if b%9==normalized and b%5==phase45%5)
                weights=decoded[payload['second'][str(representative)]]
                if normalized!=r: weights=transport(weights,9,normalized,r)
                demand,capacity=literal_check(PREFIX+[(42,29),(45,phase45)],weights)
                events.append([[(42,29),(45,phase45)],demand,capacity])
        else:
            r=phase42%7; normalized=r if r<5 else 4
            representative=next(b for b in range(42) if b%7==normalized and b%6==phase42%6)
            weights=decoded[payload['first'][str(representative)]]
            if r!=normalized: weights=transport(weights,7,normalized,r)
            demand,capacity=literal_check(PREFIX+[(42,phase42)],weights)
            events.append([[(42,phase42)],demand,capacity])
    return sha256(json.dumps(events,separators=(',',':')).encode('ascii')).hexdigest()


def generator_orbits(period,anchors):
    """Enumerate elementary prefix-child swaps that literally fix anchors."""
    parent=list(range(period))
    def find(x):
        while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
        return x
    for p,powers in factor_levels(period):
        P=p**len(powers); step=period//P
        inverse=next(k for k in range(P) if step*k%P==1)
        for power in powers:
            for prefix in range(power):
                for a,b in combinations(range(p),2):
                    permutation=[]
                    for x in range(period):
                        r=x%P; child=r//power%p
                        target=r
                        if r%power==prefix:
                            if child==a: target+=(b-a)*power
                            elif child==b: target-=(b-a)*power
                        permutation.append((x+step*((target-r)*inverse%P))%period)
                    if any((x%m==residue)!=(y%m==residue) for m,residue in anchors
                           for x,y in enumerate(permutation)): continue
                    for x,y in enumerate(permutation):
                        rx,ry=find(x),find(y)
                        if rx!=ry: parent[rx]=ry
    groups=defaultdict(list)
    for x in range(period):
        if all(x%m!=a for m,a in anchors): groups[find(x)].append(x)
    return {frozenset(points) for points in groups.values()}


def audit_orbits_and_rows():
    rng=random.Random(81710080)
    cases=0; checked_rows=0
    inputs=[]
    for period in (8,12,18,24,36,40,72):
        for repeat in range(8):
            eligible=[m for m in divisors(period) if m>=2]
            chosen=rng.sample(eligible,min(3,len(eligible)))
            inputs.append((period,[(m,rng.randrange(m)) for m in chosen]))
    inputs.extend([(L,PREFIX[:9]),(L,PREFIX)])
    for period,anchors in inputs:
        orbits,phase_keys=orbit_data(period,anchors)
        if {frozenset(points) for points in orbits}!=generator_orbits(period,anchors):
            raise ValueError('Literal stabilizer generator orbits differ')
        remaining=[m for m in divisors(period) if m not in dict(anchors)]
        _,rows=quotient_rows(period,anchors,remaining)
        for m,key,coefficients in rows:
            # Test every actual phase, including all equivalent phases.
            for phase,phase_key in enumerate(phase_keys(m)):
                if phase_key!=key: continue
                for j,orbit in enumerate(orbits):
                    literal=sum(x%m==phase for x in orbit)
                    if literal!=coefficients.get(j,0): raise ValueError('Literal quotient coefficient differs')
                checked_rows+=1
        cases+=1
    return cases,checked_rows


if __name__=='__main__':
    start=monotonic(); root=Path(__file__).resolve().parent
    payload=json.loads((root/'certificates.json').read_text())
    expected=json.loads((root/'expected.json').read_text())
    digest=audit_certificate(payload)
    if digest!=expected['events_sha256']: raise ValueError('Literal proof events differ')
    print('ALL 86 LITERAL CERTIFICATE BRANCHES PASSED.',flush=True)
    cases,rows=audit_orbits_and_rows()
    print(f'ALTERNATE AUDIT PASSED: {cases} literal-generator orbit cases; {rows} literal quotient phase rows.',flush=True)
    print(f'Seconds: {monotonic()-start:.3f}',flush=True)
