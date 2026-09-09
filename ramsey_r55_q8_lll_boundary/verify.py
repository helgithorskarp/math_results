#!/usr/bin/env python3
"""Independent physical five-set audit of produce.py's compact evidence.

Imports no producer code. Reconstructs the matrix domain directly from all
physical five-sets in two K4s, then reconstructs every witnessed bad event
from vertex subsets in the physical 43-vertex labeling.
"""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def audit(result, stream, domain_bytes):
    forbidden = []
    for five in combinations(range(8), 5):
        cross = 0
        for u,v in combinations(five,2):
            if u < 4 <= v:
                cross |= 1 << (4*u+v-4)
        require(cross != 0, 'a five-set cannot lie in one four-block')
        forbidden.append(cross)
    require(len(set(forbidden))==56, 'physical forbidden patterns')
    domain = [m for m in range(65536)
              if not any(m & f == f for f in forbidden)]
    # Blue fives are impossible in a union of two red cliques by pigeonhole.
    require(len(domain)==result['allowed_matrices']==37823, 'domain cardinality')
    rebuilt_domain=b''.join(m.to_bytes(2,'little') for m in domain)
    require(rebuilt_domain==domain_bytes,'entry-by-entry complete domain comparison')
    digest=hashlib.sha256(rebuilt_domain).hexdigest()
    require(digest==result['domain_sha256'], 'complete domain equality')
    identity=sum(1 << (5*i) for i in range(4))
    require(0 in domain and identity in domain and (65535 ^ identity) in domain,
            'known allowed controls')
    require(65535 not in domain and 15 not in domain, 'known forbidden controls')

    # Audit each labeled rectangle, not just the first rows/columns. These
    # exact marginal tables also certify nonconstant variable dependence.
    counts={}
    dimensions=Counter()
    for a in range(1,4):
        for b in range(1,4):
            if a+b>4:
                continue
            for rows in combinations(range(4),a):
                for cols in combinations(range(4),b):
                    mask=sum(1 << (4*i+j) for i in rows for j in cols)
                    count=sum(m & mask==mask for m in domain)
                    require(0<count<len(domain), 'nonconstant rectangle event')
                    require(count==result['rectangle_counts'][f'{a},{b}'],
                            'labeled rectangle marginal')
                    counts[mask]=count
                    dimensions[a,b]+=1

    events={}
    type_counts=Counter()
    for third in (3,4):
        vertices=list(range(4,12))+list(range(4*third,4*third+4))
        for five in combinations(vertices,5):
            blocks={v//4 for v in five}
            if blocks!={1,2,third}:
                continue
            masks={}
            for u,v in combinations(five,2):
                if u//4 != v//4:
                    key=(u//4,v//4)
                    masks[key]=masks.get(key,0) | (1 << (4*(u%4)+v%4))
            require(set(masks)=={(1,2),(1,third),(2,third)}, 'physical variable support')
            probability=Fraction(1)
            for mask in masks.values():
                probability *= Fraction(counts[mask],len(domain))
            require(five not in events,'distinct physical events')
            events[five]=probability
            type_counts[tuple(sum(v//4==k for v in five) for k in (1,2,third))]+=1
    require(len(events)==result['event_count']==1248,'physical event count')
    for row in result['event_types']:
        sizes=tuple(row['sizes'])
        require(type_counts[sizes]==2*row['per_triple_count'],'type multiplicity')
        matching=[p for v,p in events.items()
                  if tuple(sum(x//4==k for x in v) for k in sorted({x//4 for x in v}))==sizes]
        require(all(p==Fraction(row['probability']) for p in matching),'per-event probability')
    rebuilt=''.join(','.join(map(str,v))+'\t'+str(events[v])+'\n'
                    for v in sorted(events)).encode()
    require(rebuilt==stream, 'entry-by-entry event and probability comparison')
    require(hashlib.sha256(rebuilt).hexdigest()==result['events_sha256'],'event digest')
    total=sum(events.values(),Fraction())
    require(total==Fraction(result['clique_probability_sum']), 'clique mass')
    require(total-1==Fraction(result['clique_sum_minus_one']), 'exact excess')
    require((total>1)==result['initial_sum_greater_than_one_test_fired'],
            'honest initial gate outcome')
    minimum=min(events.values())
    require(minimum==Fraction(result['minimum_event_probability']),'minimum probability')
    weight_test=2*len(events)*minimum
    require(weight_test==Fraction(result['twice_clique_size_times_minimum']),
            'direct weight bound arithmetic')
    require(weight_test>1 and result['direct_weight_contradiction'],
            'asymmetric weight contradiction')
    require(result['status']=='FAILED_ASYMMETRIC_LLL_WEIGHTS_ON_SAME_EVENT_CLIQUE',
            'claim status')
    for key in ('new_original_task_exclusions','new_good43','resampling_steps',
                'target_solver_calls','core_catalog_records_read'):
        require(result[key]==0,'no physical task outcome or target execution')
    return dict(status='VERIFIED_LLL_CERTIFICATE_FAILURE',
                matrices_examined=65536, physical_forbidden_patterns=56,
                labeled_rectangle_marginals=sum(dimensions.values()),
                physical_events_checked=len(events),
                clique_probability_sum=str(total),
                initial_sum_gate_fired=total>1,
                twice_clique_size_times_minimum=str(weight_test),
                independent_reviewer_verdict=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run',type=Path)
    parser.add_argument('--expected',type=Path)
    args=parser.parse_args()
    result=json.loads((args.run/'RESULT.json').read_text())
    if args.expected:
        require(result==json.loads(args.expected.read_text()),'published compact result equality')
    print(json.dumps(audit(result,(args.run/'events.tsv').read_bytes(),
                           (args.run/'domain.bin').read_bytes()),indent=2,sort_keys=True))
