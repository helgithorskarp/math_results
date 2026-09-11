#!/usr/bin/env python3
"""Reject corruptions of a small real candidate stream; no search code imported."""
from pathlib import Path
import argparse,json,struct,subprocess

def controls(program,fixture,weights,orbit):
    good=bytes.fromhex(json.loads(fixture.read_text())['trace_hex']);w=list(map(int,weights.read_text().split()))
    assert struct.unpack_from('<4Q',good)==(1,8194,8205,2)
    domain=int.from_bytes(good[32:48],'little');r,upper,count=struct.unpack_from('<3Q',good,48)
    assert r==6 and count>=2
    first=int.from_bytes(good[72:88],'little');p=[x for x in range(82)if first>>x&1];d=[x for x in range(82)if domain>>x&1];lower=(sum(w[x]for x in d)+5)//6
    def sidon(a):
        sums=[x+y for i,x in enumerate(a)for y in a[i:]];return len(sums)==len(set(sums))
    def replace(offset,length,data):return good[:offset]+data+good[offset+length:]
    collision=None
    for x in p:
        for y in d:
            if y in p:continue
            a=sorted(set(p)-{x}|{y});value=sum(w[z]for z in a)
            if lower<=value<=upper and not sidon(a):collision=sum(1<<z for z in a);break
        if collision is not None:break
    assert collision is not None
    new_upper=sum(w[x]for x in p)-1;assert new_upper>=lower
    cases={'valid_candidate_trace':good,'candidate_out_of_range':replace(72,16,(first|(1<<82)).to_bytes(16,'little')),'candidate_wrong_size':replace(72,16,(first&(first-1)).to_bytes(16,'little')),'duplicate_candidate':replace(88,16,first.to_bytes(16,'little')),'candidate_over_upper':replace(56,8,struct.pack('<Q',new_upper)),'candidate_sum_collision':replace(72,16,collision.to_bytes(16,'little'))}
    result=[]
    for name,data in cases.items():
        p=subprocess.run(list(map(str,[program,weights,orbit,4097,4098,0,1,100000])),input=data,capture_output=True)
        assert (p.returncode==0)==(name=='valid_candidate_trace'),(name,p.stderr)
        if name=='candidate_sum_collision':assert p.stderr.strip()==b'candidate pair-sum collision'
        if name=='candidate_over_upper':assert p.stderr.strip()==b'candidate weight'
        result.append(dict(name=name,accepted=p.returncode==0,stderr=p.stderr.decode().strip()))
    return result
if __name__=='__main__':
    if not __debug__:raise SystemExit('Assertions required.')
    p=argparse.ArgumentParser();p.add_argument('--program',type=Path,required=True);p.add_argument('--fixture',type=Path,required=True);p.add_argument('--weights',type=Path,required=True);p.add_argument('--orbit',type=Path,required=True);a=p.parse_args();print(json.dumps(controls(a.program,a.fixture,a.weights,a.orbit),indent=2))
