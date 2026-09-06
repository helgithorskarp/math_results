#!/usr/bin/env python3
"""Complete bitmask cover audit of the frozen surviving-core stream."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
FRONTIER_SHA='f00bfa52ad63aafb374150cff7917bd7c45716bee19cf416b350b2d0a16d1be2'


def load(p): return json.loads(p.read_text())
def save(p,x): p.write_text(json.dumps(x,indent=2)+'\n')


def run(pilot,frontier,inputs):
    all_rows=load(pilot/'certificate.json'); by_cut={}
    for row in all_rows:
        by_cut.setdefault(tuple(row['D']),row)
    keys=sorted(by_cut,key=lambda D:(len(D),D)); minimal=[]
    for D in keys:
        if not any(set(E)<=set(D) for E in minimal): minimal.append(D)
    cert=[dict(index=i,source_candidate=by_cut[D]['index'],D=list(D),colouring=by_cut[D]['colouring'])
          for i,D in enumerate(minimal)]
    masks=[sum(1<<v for v in D) for D in minimal]
    large=set(load(inputs)['large'])
    raw=frontier.read_bytes()
    if sha256(raw).hexdigest()!=FRONTIER_SHA:raise ValueError('frozen core frontier digest')
    coverage=Counter();profile=Counter();remaining=Counter();survivors=[];tags=bytearray();previous=None
    for line in raw.decode('ascii').splitlines():
        O=tuple(map(int,line.split(',')));key=(len(O),O)
        if (previous is not None and previous>=key) or tuple(sorted(set(O)))!=O:raise ValueError('canonical core order')
        previous=key; bits=sum(1<<v for v in O)
        pr=(514-len(O),len(large.intersection(O)),sum(1<<(v-510) for v in O if v>=510))
        profile[pr]+=1
        index=next((i for i,m in enumerate(masks) if bits&m==m),None)
        tags.append(255 if index is None else index)
        if index is None:
            survivors.append(line);remaining[pr]+=1
        else:coverage[index]+=1
    if sum(profile.values())!=190536:raise ValueError('input row count')
    candidate_indices=[]
    for row in load(HERE/'candidates.json'):
        O=set(row['omitted']);index=next((i for i,D in enumerate(minimal) if set(D)<=O),None)
        candidate_indices.append(index)
    survivor_raw=(''.join(line+'\n' for line in survivors)).encode('ascii')
    (pilot/'coverage.bin').write_bytes(tags);(pilot/'survivors.txt').write_bytes(survivor_raw)
    save(pilot/'positive_certificate.json',cert)
    result=dict(input_cores=190536,covered=190536-len(survivors),survivors=len(survivors),
                raw_positive_witnesses=len(all_rows),unique_positive_cuts=len(keys),minimal_positive_cuts=len(minimal),
                cut_size_histogram={str(k):v for k,v in sorted(Counter(map(len,minimal)).items())},
                first_cover_histogram={str(k):v for k,v in sorted(coverage.items())},
                candidate_cover_indices=candidate_indices,
                surviving_core_orders={str(k):v for k,v in sorted(Counter({n:sum(v for (order,l,m),v in remaining.items() if order==n) for n in [507,508]}).items())},
                profile_rows=[dict(profile=list(pr),input=profile[pr],covered=profile[pr]-remaining[pr],remaining=remaining[pr]) for pr in sorted(profile)],
                covered_profiles=sum(remaining[pr]==0 for pr in profile),remaining_profiles=sum(remaining[pr]>0 for pr in profile),
                survivor_bytes=len(survivor_raw),survivor_sha256=sha256(survivor_raw).hexdigest(),
                coverage_bytes=len(tags),coverage_sha256=sha256(tags).hexdigest(),
                input_frontier_sha256=FRONTIER_SHA,record_improvement=False,family_closed=not survivors)
    save(pilot/'coverage.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ['profile_rows','candidate_cover_indices']},sort_keys=True))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--pilot',type=Path,required=True);p.add_argument('--frontier',type=Path,required=True);p.add_argument('--inputs',type=Path,required=True);a=p.parse_args();run(a.pilot,a.frontier,a.inputs)
