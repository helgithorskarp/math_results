#!/usr/bin/env python3
"""Read every emitted P82 four-eleven query using Python integers."""
import argparse
import json
from pathlib import Path
import struct
from checks import SOURCE,sidon,rows,mask,same

def audit(work):
    weights=list(map(int,(SOURCE/'weights.txt').read_text().split()))
    def cap(k):return 3776423 if k==9 else 444444*k if k<9 else 4000000
    def weight(m):return sum(w for x,w in enumerate(weights)if m>>x&1)
    records=options=maximum=bytes_read=0
    paths=sorted(work.glob('sweep4_0_*.bin'))
    assert paths
    for path in paths:
        same(path,path.with_name(path.name.replace('sweep4_0_','sweep4_1_')))
        data=path.read_bytes();offset=0;bytes_read+=len(data)
        def word():
            nonlocal offset
            assert offset+8<=len(data)
            z=struct.unpack_from('<Q',data,offset)[0];offset+=8;return z
        def readmask():return word()+(word()<<64)
        while offset<len(data):
            domain=readmask();count=word();assert 2<=count<=4
            profile=[word()for _ in range(count)];upper=word();n=word()
            assert profile in [[10,10,10,8],[10,10,8],[10,8],[10,10,9,9],[10,9,9],[9,9]]
            assert 0<domain<1<<82 and domain.bit_count()==sum(profile)and 0<upper<=cap(profile[0])and n>0
            k=profile[0];multiplicity=profile.count(k);others=sum(cap(t)for t in profile if t!=k)
            lower=max(0,(weight(domain)-others+multiplicity-1)//multiplicity)
            previous=-1
            for _ in range(n):
                a=readmask();assert previous<a and a&domain==a and a.bit_count()==k
                points=[x for x in range(82)if a>>x&1]
                assert sidon(points)and lower<=sum(weights[x]for x in points)<=upper
                previous=a
            records+=1;options+=n;maximum=max(maximum,n)
        assert offset==len(data)
    expected=json.loads((SOURCE/'expected.json').read_text())['4']
    assert bytes_read==expected['trace_bytes_per_method']and options==expected['totals']['options']
    calls=2*expected['packings']+options
    assert calls==expected['totals']['calls']and records<=expected['totals']['queries']<=calls<2**64
    return dict(verified=True,nonempty_query_records=records,options=options,largest_option_list=maximum,bytes=bytes_read,integer_call_bound=calls,all_candidates_checked_by_pair_sums=True)

def main():
    if not __debug__:raise SystemExit('Do not use -O/PYTHONOPTIMIZE.')
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--work',type=Path,required=True);a=p.parse_args();result=audit(a.work.resolve())
    (a.work/'trace_audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
