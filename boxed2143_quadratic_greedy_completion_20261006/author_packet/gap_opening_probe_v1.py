#!/usr/bin/env python3
"""Exact rule validation and diagnostic overhead data; no growth theorem."""
from hashlib import sha256
from itertools import permutations
import json
import math
from pathlib import Path
import random
import resource
import statistics
import time

from kernel import insert_maximum, legal_maximum_gaps, validate_permutation
from verify_kernel import direct_occurrences


class Incomplete(RuntimeError):
    pass


def complete(p, deadline, max_points=10000, literal=False):
    p=validate_permutation(p)
    original_position={v:i for i,v in enumerate(p)}
    word=()
    identities=[]
    costs=[]
    trace=[]
    stream=sha256()
    for rank in range(1,len(p)+1):
        pos=original_position[rank]
        gap=next((i for i,v in enumerate(identities)
                  if v is not None and original_position[v]>pos),len(word))
        repairs=0
        first_distance=None
        while True:
            if time.monotonic()>deadline:
                raise Incomplete('time cap reached; no completed input reported')
            if len(word)>=max_points:
                raise Incomplete('point cap reached; no completed input reported')
            gaps=legal_maximum_gaps(word)
            if gap in gaps:
                word=insert_maximum(word,gap)
                identities.insert(gap,rank)
                if literal and direct_occurrences(word):
                    raise RuntimeError('literal source child is not avoiding')
                costs.append(repairs)
                stream.update(json.dumps([word,identities],separators=(',',':')).encode()+b'\n')
                break
            k=max(g for g in gaps if g<gap)
            distance=gap-k
            if first_distance is None:
                first_distance=distance
            word=insert_maximum(word,k)
            identities.insert(k,None)
            gap+=1
            repairs+=1
            child_gaps=legal_maximum_gaps(word)
            if k+1 not in child_gaps or k+2 not in child_gaps:
                raise RuntimeError('two-gap opening claim failed')
            new_k=max(g for g in child_gaps if g<=gap)
            if gap-new_k>distance-1 or repairs>first_distance:
                raise RuntimeError('distance/termination bound failed')
            if literal and direct_occurrences(word):
                raise RuntimeError('literal auxiliary child is not avoiding')
            if len(p)<=8:
                trace.append({'source_rank':rank,'auxiliary_gap':k,'tracked_gap':gap,
                              'distance_before':distance,'distance_after':gap-new_k})
            stream.update(json.dumps([word,identities],separators=(',',':')).encode()+b'\n')
    source_word=tuple(v for v in identities if v is not None)
    if source_word!=p:
        raise RuntimeError('source positional decoding failed')
    source_values=[v for v,t in zip(word,identities) if t is not None]
    value_rank={v:i+1 for i,v in enumerate(sorted(source_values))}
    if tuple(value_rank[v] for v in source_values)!=p:
        raise RuntimeError('source value decoding failed')
    result={'input':p,'output_length':len(word),'auxiliaries':len(word)-len(p),
            'stage_costs':costs,'trace_sha256':stream.hexdigest()}
    if len(p)<=8:
        result.update({'output':word,'source_identities':identities,'auxiliary_trace':trace})
    return result


def main():
    root=Path(__file__).resolve().parent
    output=root/'gap_opening_probe_v1.json'
    if output.exists():
        raise RuntimeError('Preserve original; replay in a fresh directory')
    start=time.monotonic()
    deadline=start+180
    result={'actor':'literature-researcher-3','full_target_solved':False,
            'status':'running diagnostic prefix; no growth claim',
            'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'plan_sha256':sha256((root/'GAP_OPENING_ENTROPY_PLAN_V1.md').read_bytes()).hexdigest(),
            'complete_small_inputs':[],'specified_families':[],'random_pilots':[],
            'time_cap_seconds':180,'max_points_per_input':10000}
    two_gap_stream=sha256();parents=children=0
    for n in range(7):
        for p in permutations(range(1,n+1)):
            if direct_occurrences(p):
                continue
            parents+=1
            for g in legal_maximum_gaps(p):
                q=insert_maximum(p,g);lg=legal_maximum_gaps(q)
                if direct_occurrences(q) or g+1 not in lg or (g<n and g+2 not in lg):
                    raise RuntimeError('complete literal two-gap domain mismatch')
                children+=1
                two_gap_stream.update(json.dumps([p,g,q,lg],separators=(',',':')).encode()+b'\n')
    result['two_gap_literal_control']={'max_parent':6,'parents':parents,
        'legal_children':children,'stream_sha256':two_gap_stream.hexdigest()}
    output.write_text(json.dumps(result,indent=2)+'\n')
    for m in range(1,7):
        counts={};worst=None;stream=sha256();total=0
        for p in permutations(range(1,m+1)):
            r=complete(p,deadline,literal=True)
            counts[r['output_length']]=counts.get(r['output_length'],0)+1
            total+=r['output_length']
            if worst is None or r['output_length']>worst['output_length']:
                worst=r
            stream.update(json.dumps(r,separators=(',',':'),sort_keys=True).encode()+b'\n')
        result['complete_small_inputs'].append({'m':m,'input_count':math.factorial(m),
             'output_length_histogram':counts,'output_length_sum':total,
             'worst_input':worst,'input_stream_sha256':stream.hexdigest()})
        output.write_text(json.dumps(result,indent=2)+'\n')
    for m in (8,16,32,64,128,256):
        q=m//2
        families={'increasing':tuple(range(1,m+1)),
                  'decreasing':tuple(range(m,0,-1)),
                  'low_descent_high_descent':tuple(range(q,0,-1))+tuple(range(m,q,-1)),
                  'adjacent_swapped_pairs':tuple(v for k in range(1,m+1,2) for v in (k+1,k)),
                  'zigzag_extrema':tuple(v for k in range(1,q+1) for v in (m-k+1,k))}
        for name,p in families.items():
            r=complete(p,deadline)
            r['family']=name
            result['specified_families'].append(r)
            output.write_text(json.dumps(result,indent=2)+'\n')
        pilots=[]
        for trial in range(12):
            seed=1000003*m+trial
            p=list(range(1,m+1));random.Random(seed).shuffle(p)
            r=complete(tuple(p),deadline);r['seed']=seed
            pilots.append(r)
        lengths=[r['output_length'] for r in pilots]
        result['random_pilots'].append({'m':m,'trials':12,'mean_length':statistics.mean(lengths),
            'median_length':statistics.median(lengths),'max_length':max(lengths),
            'completed_inputs':pilots,'uniform_distribution_claim':False})
        output.write_text(json.dumps(result,indent=2)+'\n')
    result['status']='completed same-author diagnostics; uniform cost/density unresolved'
    result['seconds']=time.monotonic()-start
    result['peak_rss_kib_linux']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'seconds':result['seconds'],
        'two_gap_literal_control':result['two_gap_literal_control'],
        'random_rows':[{k:v for k,v in r.items() if k!='completed_inputs'} for r in result['random_pilots']],
        'family_lengths':[(r['family'],len(r['input']),r['output_length']) for r in result['specified_families']]},indent=2))


if __name__=='__main__':
    main()
