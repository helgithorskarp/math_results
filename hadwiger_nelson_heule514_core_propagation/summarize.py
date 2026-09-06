#!/usr/bin/env python3
"""Canonical surviving-core frontier and profiles from the fully checked stream.

Run after verify.py. This only groups already-verified records; it is not an
additional colouring or core solver.
"""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import struct


def summarize(work,verification):
    report=json.loads(verification.read_text());raw=(work/'cores.bin').read_bytes()
    if sha256(raw).hexdigest()!=report['core_records_sha256']:raise ValueError('verified core stream digest')
    meta=json.loads((work/'inputs.json').read_text());large=set(meta['large'])
    cores=set();profiles={};order_hist=Counter()
    for index,(tag,encoded) in enumerate(struct.iter_unpack('<h65s',raw)):
        if tag>=0:continue
        mask=int.from_bytes(encoded,'little')
        missing=tuple(v for v in range(514) if not mask & (1<<v))
        if missing in cores:raise ValueError('unexpected duplicate surviving core')
        cores.add(missing);order=514-len(missing);order_hist[order]+=1
        key=(order,len(set(missing)&large),sum(1<<(v-510) for v in missing if v>=510))
        cell=profiles.setdefault(key,dict(count=0,first_input_row=index,representative_core_omissions=list(missing)))
        cell['count']+=1
    if len(cores)!=report['survivors']:raise ValueError('complete survivor quotient')
    stream=''.join(','.join(map(str,D))+'\n' for D in sorted(cores,key=lambda D:(len(D),D))).encode('ascii')
    (work/'core_omissions.txt').write_bytes(stream)
    output=dict(distinct_surviving_cores=len(cores),duplicate_core_records=0,
                cores_by_order={str(k):v for k,v in sorted(order_hist.items())},
                profile_count=len(profiles),profiles=[dict(core_order=k[0],large_omissions=k[1],new_omission_mask=k[2],**v) for k,v in sorted(profiles.items())],
                core_frontier_bytes=len(stream),core_frontier_sha256=sha256(stream).hexdigest(),
                core_frontier_format='Sorted by (number of missing vertices, increasing missing-index tuple); comma-separated decimal ASCII and one LF per tuple',
                parent_core_records_sha256=report['core_records_sha256'])
    (work/'core_census.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k!='profiles'},sort_keys=True))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--verification',type=Path,required=True);a=p.parse_args();summarize(a.work,a.verification)
