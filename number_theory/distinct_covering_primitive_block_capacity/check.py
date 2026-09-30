"""Literal period43200 check of one specified covering prefix."""
from hashlib import sha256
from math import gcd, lcm
from pathlib import Path
from time import monotonic
import argparse
import json

from block import exact_K, exact_J, hypothesis

HERE = Path(__file__).resolve().parent
N,Q,B,b,p = 43200,3600,1728,144,5
PLACED = ((8,0),(9,0),(10,5),(12,1),(15,11),(16,4),
          (18,3),(20,2),(24,10),(25,1))
TOP = (B,B*p,N)


def progression_maximum(values,modulus,point_bound):
    best=0
    for a in range(modulus):
        best=max(best,sum(values[a::modulus]))
        # The theoretical pointwise bound proves this is already maximal.
        if best==point_bound:
            break
    return best


def check():
    raw=(HERE/'weights.json').read_bytes()
    data=json.loads(raw)
    if data['Q']!=Q or type(data['boxes']) is not list:
        raise ValueError('Weight period/schema differs')
    vector=[0]*Q
    points=0
    for box in data['boxes']:
        if (type(box) is not list or len(box)!=4
                or any(type(v) is not int for v in box) or box[-1]<=0):
            raise ValueError('Invalid literal box')
        if any(not 0<mask<1<<axis for mask,axis in zip(box[:3],(16,9,25))):
            raise ValueError('Out-of-axis literal mask')
        hits=0
        for x in range(Q):
            if all(mask>> (x%axis)&1 for mask,axis in zip(box[:3],(16,9,25))):
                if vector[x]:
                    raise ValueError('Overlapping boxes')
                vector[x]=box[-1]
                hits+=1
        if not hits:
            raise ValueError('Empty CRT box')
        points+=hits
    if not any(vector):
        raise ValueError('Zero weight')
    if (len(PLACED)!=len({n for n,a in PLACED})
            or not any(n==8 for n,a in PLACED)
            or any(n<8 or N%n or not 0<=a<n for n,a in PLACED)):
        raise ValueError('Incorrect exactly-eight prefix')
    resources=tuple(n for n in range(8,N+1) if N%n==0 and n not in {m for m,a in PLACED})
    hypothesis(B,b,p,Q,resources)
    full=[vector[x%Q] for x in range(N)]
    if any(full[x] and any(x%n==a for n,a in PLACED) for x in range(N)):
        raise ValueError('Weight on a covered physical point')
    largest=max(full)
    caps={n:progression_maximum(full,n,(N//n)*largest) for n in resources}
    base_maxima={g:progression_maximum(vector,g,(Q//g)*largest)
                 for g in {gcd(Q,n) for n in resources}}
    for n in resources:
        if caps[n]!=(N//lcm(Q,n))*base_maxima[gcd(Q,n)]:
            raise RuntimeError('Physical capacity disagrees with exact CRT lift')
    K,witness=exact_K(B,b,p,Q,vector)
    J=exact_J(b,p,Q,vector)
    top_sum=sum(caps[n] for n in TOP)
    ordinary=sum(caps.values())
    simple=ordinary-top_sum+2*caps[B*p]+2*caps[N]
    whole_fibre=ordinary-top_sum+J
    corrected=ordinary-top_sum+K
    demand=sum(full)
    if not corrected<demand or not K<=J<=2*caps[B*p]+2*caps[N]:
        raise RuntimeError('Strict corrected inequality or comparison fails')
    return {'agent':'six-covering-3','role':'researcher',
            'scope':'one fixed-prefix exclusion; full43200 root unresolved',
            'N':N,'Q':Q,'placed':PLACED,'boxes':len(data['boxes']),
            'positive_base_points':points,'maximum_point_weight':largest,
            'actual_unused_divisors':len(resources),'base_demand':sum(vector),
            'physical_demand':demand,'ordinary_capacity':ordinary,
            'simple_fibre_capacity':simple,'whole_fibre_J_capacity':whole_fibre,
            'primitive_block_K_capacity':corrected,'K':K,'J':J,
            'K_witness':witness,'strict_gap':demand-corrected,
            'K_essential_beyond_J':whole_fibre>=demand,
            'actual_top_capacities':{n:caps[n] for n in TOP},
            'literal_actual_capacity_checks':len(caps),
            'weights_sha256':sha256(raw).hexdigest(),
            'all_actual_capacities':caps}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    start=monotonic()
    result=json.loads(json.dumps(check()))
    expected=HERE/'expected.json'
    if args.write:
        expected.write_text(json.dumps(result,indent=2)+'\n')
    elif result!=json.loads(expected.read_text()):
        raise RuntimeError('Expected exact evidence differs')
    print('Physical demand',result['physical_demand'],'ordinary',result['ordinary_capacity'],
          'J',result['whole_fibre_J_capacity'],'K',result['primitive_block_K_capacity'],
          'strict gap',result['strict_gap'])
    print('All68 actual remaining-divisor maxima and literal support checked.')
    print('The old J budget also excludes this prefix; full43200 remains unresolved.')
    print('Elapsed seconds:',monotonic()-start)


if __name__=='__main__':
    main()
