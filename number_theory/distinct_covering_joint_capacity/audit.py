"""Alternate CRT box decoding and phase-intersection capacity audit.

The primary check uses literal residue tests, progression slices, and set
unions. This audit reconstructs weights by CRT, uses phase histograms and
the compatible-intersection formula, and compares every pair-phase event.
Both implementations are by six-covering-2; this is not external review.
"""
from hashlib import sha256
from itertools import combinations,product
import json
from math import gcd,lcm
from pathlib import Path
import random
from time import monotonic


def prime_periods(n):
    result=[];p=2
    while p*p<=n:
        P=1
        while n%p==0: n//=p;P*=p
        if P>1: result.append(P)
        p+=1
    if n>1: result.append(n)
    return result


def histogram(weights,m):
    result=[0]*m
    for x,w in enumerate(weights): result[x%m]+=w
    return result


def phase_events(weights,m,n):
    ell=lcm(m,n);g=gcd(m,n);inverse=pow(m//g,-1,n//g)
    left=histogram(weights,m);right=histogram(weights,n);meet=histogram(weights,ell)
    for a in range(m):
        for b in range(n):
            overlap=0
            if (b-a)%g==0:
                phase=(a+m*(((b-a)//g*inverse)%(n//g)))%ell
                overlap=meet[phase]
            yield [m,n,a,b,left[a]+right[b]-overlap]


def controls():
    rng=random.Random(82910080);cases=0;phases=0
    for L in (6,8,12,18,24,30,36,40,72):
        moduli=[m for m in range(1,L+1) if L%m==0]
        for repeat in range(4):
            weights=[rng.randrange(8) for x in range(L)]
            for m,n in combinations(moduli,2):
                sets=[set(range(a,L,m)) for a in range(m)]
                other=[set(range(b,L,n)) for b in range(n)]
                for _,_,a,b,value in phase_events(weights,m,n):
                    if value!=sum(weights[x] for x in sets[a]|other[b]):
                        raise ValueError('Compatible/incompatible intersection control fails')
                    phases+=1
                cases+=1
    return cases,phases


def audit():
    root=Path(__file__).resolve().parent
    encoded=(root/'certificate.json').read_bytes();payload=json.loads(encoded)
    expected=json.loads((root/'expected.json').read_text());L=payload['L']
    if sha256(encoded).hexdigest()!=expected['certificate_sha256']: raise ValueError('Certificate bytes')
    periods=prime_periods(L);coefficients=[L//P*pow(L//P,-1,P) for P in periods]
    weights=[0]*L;seen=set()
    for box in payload['boxes']:
        axes=[[r for r in range(P) if mask>>r&1] for P,mask in zip(periods,box[:-1])]
        for coordinates in product(*axes):
            x=sum(c*a for c,a in zip(coefficients,coordinates))%L
            if x in seen: raise ValueError('CRT overlap')
            seen.add(x);weights[x]=box[-1]
    for m,a in payload['anchors']:
        if any(weights[x] for x in range(a,L,m)): raise ValueError('Covered positive weight')
    assigned={m for m,a in payload['anchors']}
    available=[m for m in range(8,L+1) if L%m==0 and m not in assigned]
    paired={m for pair in payload['pairs'] for m in pair}
    single={m:max(histogram(weights,m)) for m in available}
    capacities=[];events=[]
    for m,n in payload['pairs']:
        group=list(phase_events(weights,m,n));events.extend(group)
        capacities.append([m,n,max(event[-1] for event in group)])
    demand=sum(weights);individual=sum(single.values())
    joint=sum(v for m,v in single.items() if m not in paired)+sum(v for m,n,v in capacities)
    digest=sha256(json.dumps(events,separators=(',',':')).encode('ascii')).hexdigest()
    actual={'demand':demand,'individual_capacity':individual,'joint_capacity':joint,
            'pair_capacities':capacities,'literal_phase_pairs':len(events),'phase_events_sha256':digest,
            'positive_weight_points':len(seen),'positive_boxes':len(payload['boxes'])}
    if any(expected[k]!=v for k,v in actual.items()) or demand<=joint:
        raise ValueError('Alternate capacities or phase events differ')
    cases,phases=controls()
    return {'AUDIT':'COMPLETE EXACT NONEXTENSION','phase_events_sha256':digest,
            'small_pair_cases':cases,'small_phase_pairs':phases}


if __name__=='__main__':
    start=monotonic();result=audit();print(json.dumps({**result,'seconds':monotonic()-start},indent=2))
