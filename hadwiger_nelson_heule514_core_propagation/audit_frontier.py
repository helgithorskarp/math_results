#!/usr/bin/env python3
"""Independent bijection audit of canonical core tuples and the 77 profiles."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import struct


def audit(work,verification):
    report=json.loads(verification.read_text());raw=(work/'cores.bin').read_bytes()
    if sha256(raw).hexdigest()!=report['core_records_sha256']:raise ValueError('checked core stream digest')
    remaining={encoded for tag,encoded in struct.iter_unpack('<h65s',raw) if tag==-1}
    if len(remaining)!=report['survivors']:raise ValueError('distinct surviving native cores')
    large=set(json.loads((work/'inputs.json').read_text())['large'])
    census=json.loads((work/'core_census.json').read_text());data=(work/'core_omissions.txt').read_bytes()
    if sha256(data).hexdigest()!=census['core_frontier_sha256']:raise ValueError('core frontier digest')
    counts=Counter();orders=Counter();previous=None;rows=0
    def profile(D):return (514-len(D),len(set(D)&large),sum(1<<(v-510) for v in D if v>=510))
    for line in data.decode('ascii').splitlines():
        D=tuple(map(int,line.split(',')));key=(len(D),D)
        if len(D) not in(6,7) or tuple(sorted(set(D)))!=D or not all(0<=v<514 for v in D):raise ValueError('core omission tuple')
        if previous is not None and previous>=key:raise ValueError('canonical core frontier order')
        retained=((1<<514)-1)-sum(1<<v for v in D)
        encoded=retained.to_bytes(65,'little')
        if encoded not in remaining:raise ValueError('unexpected or duplicate core')
        remaining.remove(encoded);counts[profile(D)]+=1;orders[514-len(D)]+=1;rows+=1;previous=key
    if remaining or rows!=report['survivors']:raise ValueError('complete core bijection')
    expected={(r['core_order'],r['large_omissions'],r['new_omission_mask']):r['count'] for r in census['profiles']}
    if dict(counts)!=expected or len(counts)!=census['profile_count']:raise ValueError('all core profile counts')
    for r in census['profiles']:
        D=tuple(r['representative_core_omissions']);tag,encoded=struct.unpack_from('<h65s',raw,67*r['first_input_row'])
        if tag!=-1 or ((1<<514)-1)-sum(1<<v for v in D)!=int.from_bytes(encoded,'little'):raise ValueError('representative native row')
        if profile(D)!=(r['core_order'],r['large_omissions'],r['new_omission_mask']):raise ValueError('representative profile')
    return dict(status='EXACT CANONICAL CORE BIJECTION AND PROFILE PARTITION VERIFIED',
                core_tuples=rows,profiles=len(counts),representatives_checked=len(counts),
                core_orders={str(k):v for k,v in sorted(orders.items())},
                core_frontier_sha256=sha256(data).hexdigest(),new_solver_queries=0)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--verification',type=Path,required=True);p.add_argument('--report',type=Path);a=p.parse_args()
    result=audit(a.work,a.verification)
    if a.report:a.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
