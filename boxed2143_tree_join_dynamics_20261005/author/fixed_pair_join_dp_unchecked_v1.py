#!/usr/bin/env python3
"""Exact rank-shuffle count for two fixed words via the checked tree quotient."""
from collections import defaultdict
from itertools import permutations
import json
from pathlib import Path
import platform
import resource
from time import perf_counter

from kernel import validate_permutation
from tree_dynamics import (clear_caches, insert_maximum_shape, shape_legal_gaps)


class StateCapExceeded(RuntimeError):
    pass


def rank_insertion_gaps(p):
    positions=[0]*(len(p)+1)
    for j,x in enumerate(p):
        positions[x]=j
    return tuple(sum(positions[y]<positions[x] for y in range(1,x))
                 for x in range(1,len(p)+1))


def count_join(alpha,beta,state_cap=50000):
    alpha=validate_permutation(alpha)
    beta=validate_permutation(beta)
    if len(alpha)!=len(beta):
        raise ValueError('balanced join words must have equal lengths')
    m=len(alpha)
    gaps_a=rank_insertion_gaps(alpha)
    gaps_b=rank_insertion_gaps(beta)
    current={(0,()):1}
    rows=[]
    processed=0
    maximum=1
    for total in range(2*m):
        children=defaultdict(int)
        for (i,tree),weight in current.items():
            j=total-i
            legal=set(shape_legal_gaps(tree))
            if i<m and gaps_a[i] in legal:
                children[(i+1,insert_maximum_shape(tree,gaps_a[i]))]+=weight
                processed+=1
            if j<m and i+gaps_b[j] in legal:
                children[(i,insert_maximum_shape(tree,i+gaps_b[j]))]+=weight
                processed+=1
        if len(children)>state_cap:
            clear_caches()
            raise StateCapExceeded('state cap reached; no complete count')
        current=dict(children)
        maximum=max(maximum,len(current))
        rows.append({'ranks_inserted':total+1,'states':len(current)})
        clear_caches()
    result=sum(weight for (i,tree),weight in current.items()
               if i==m and m in shape_legal_gaps(tree))
    clear_caches()
    return {'alpha':alpha,'beta':beta,'m':m,'valid_rank_partitions':result,
            'states_per_level':rows,'peak_level_states':maximum,
            'legal_transitions':processed,'state_cap':state_cap}


def canonical_231(height):
    if height==0:
        return ()
    small=canonical_231(height-1)
    d=len(small)
    return small+(2*d+1,)+tuple(x+d for x in small)


def difficult_pair(height):
    if height==1:
        return (1,),(1,)
    small=canonical_231(height-1)
    d=len(small)
    m=2*d+1
    alpha=tuple(x+d for x in small)+(m,)+small
    left_values=(1,)+tuple(range(d+2,2*d+1))
    beta=tuple(left_values[x-1] for x in small)+(m,)+tuple(x+1 for x in small)
    return alpha,beta


def main():
    root=Path(__file__).resolve().parent
    start=perf_counter()
    literal=json.loads((root/'balanced_join_reference.json').read_text())
    controls=0
    for row in literal['rows']:
        for expected in row['pair_counts']:
            actual=count_join(expected['alpha'],expected['beta'])
            if actual['valid_rank_partitions']!=expected['valid_rank_partitions']:
                raise RuntimeError('Definition baseline mismatch')
            controls+=1
    native=json.loads((root/'balanced_join_cpp_h3.json').read_text())
    tokens=(root/'balanced_fiber_h3.txt').read_text().split()
    m,count=map(int,tokens[:2])
    fiber=[tuple(map(int,tokens[2+k*m:2+(k+1)*m])) for k in range(count)]
    tested_pairs=set()
    selections=[(0,0),(0,count-1),(count-1,0),(count-1,count-1)]
    selections.append((fiber.index(tuple(native['first_minimizing_alpha'])),
                       fiber.index(tuple(native['first_minimizing_beta']))))
    for ai,bi in selections:
        if (ai,bi) in tested_pairs:
            continue
        tested_pairs.add((ai,bi))
        actual=count_join(fiber[ai],fiber[bi])
        if actual['valid_rank_partitions']!=native['pair_counts_in_input_order'][ai*count+bi]:
            raise RuntimeError('Native literal m7 pair baseline mismatch')
        controls+=1
    family=[]
    for height in range(1,6):
        alpha,beta=difficult_pair(height)
        try:
            row=count_join(alpha,beta)
        except StateCapExceeded:
            family.append({'height':height,'m':len(alpha),'status':'state cap; no count certified'})
            break
        row['height']=height
        row['candidate_bound']=1<<((len(alpha)-1)//2)
        row['candidate_bound_passes']=row['valid_rank_partitions']>=row['candidate_bound']
        family.append(row)
        print(json.dumps({k:v for k,v in row.items() if k!='states_per_level'}),flush=True)
        if not row['candidate_bound_passes']:
            break
    result={'actor':'literature-researcher-3','status':'exact fixed-pair finite counts; uniform quotient counting argument and new certificate awaiting review',
            'full_growth_target_solved':False,'literal_baseline_pairs_compared':controls,
            'scope':'all m1,3 pairs; four m7 corners and first minimizing pair; explicit P_h,Q_h until first bound failure or state cap',
            'family':family,'python':platform.python_version(),'seconds':perf_counter()-start,
            'peak_rss_kib_linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'processes':1,'native_threads':1}
    (root/'fixed_pair_join_counts.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='family'},indent=2))


if __name__=='__main__':
    main()
