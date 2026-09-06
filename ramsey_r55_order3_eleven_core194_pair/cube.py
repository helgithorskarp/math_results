#!/usr/bin/env python3
"""Complete empty-pair color split with Core194's zero-common-fixed bound."""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import shutil

ROOT=Path(__file__).resolve().parent
PREVIOUS=ROOT.parent/'ramsey_r55_order3_eleven_core194_multiplicity'
PARENT=ROOT.parent/'ramsey_r55_order3_eleven_cycle_obstruction'
WORD='100110110110110100'
PAIRS=list(combinations(range(4),2))
BASE=dict(bytes=24968424,sha256='214cbdad727ec3f48e97e62246134b341719277981119bd6b89baa5475b2dbb4')


def require(ok,why):
    if not ok:raise ValueError(why)


def info(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while chunk:=f.read(1<<20):h.update(chunk)
    return dict(bytes=path.stat().st_size,sha256=h.hexdigest())


def premise():
    for name,pin in [('result.json','864276e0fca83db96ce2629f7320310ee2f7e2ffe3e5cd3ab0e60aa7dc930a1e'),
                     ('verification.json','6110551fe9bcd1e7b3015e784f1dd405c00fdfc55b8979f0456a0f6391049038'),
                     ('boundary.json','b1b3b5f6eb3cc924d8831715656b299d4b805d02367f468c20e6711c2fc96bd3')]:
        require(info(PREVIOUS/name)['sha256']==pin,'pinned '+name)
    r=json.loads((PREVIOUS/'result.json').read_text());v=json.loads((PREVIOUS/'verification.json').read_text())
    require(r['complete'] and v['verified'] and r['open']==v['open']==['multiple'],'only multiple branch remains')
    expected=['one_01','one_02','one_03','one_12','one_13','one_23']
    require(r['excluded']==v['excluded']==expected,'complete one-empty closure')
    for k in expected:
        a=next(c for c in r['cases'] if c['id']==k);b=next(c for c in v['cases'] if c['id']==k)
        require(a['replay']['verified'] and b['replay']['verified'] and a['formula']==b['formula'],'two full preceding proof replays')
    a=next(c for c in r['cases'] if c['id']=='multiple');b=next(c for c in v['cases'] if c['id']=='multiple')
    require(a['formula']==b['formula']==BASE,'entire multiple base identity')
    return a


def core_red(a,b):
    i,s=divmod(a,3);j,t=divmod(b,3)
    return i==j or WORD[3*PAIRS.index((i,j))+(t-s)%3]=='1'


def certificate():
    rows=[]
    for mask in range(16):
        if mask.bit_count()>=3:
            neighbors=[a for a in range(12) if mask&(1<<(a//3))]
            q=next(c for c in combinations(neighbors,4) if all(core_red(a,b) for a,b in combinations(c,2)))
            rows.append(dict(mask=mask,color='red',vertices=list(q)+[14]))
        else:
            neighbors=[a for a in range(12) if not mask&(1<<(a//3))]
            edge=next((a,b) for a,b in combinations(neighbors,2) if not core_red(a,b))
            rows.append(dict(mask=mask,color='blue',vertices=list(edge)+[12,13,14]))
    return dict(index=194,bits=WORD,empty_pair=[12,13],third_fixed=14,forbidden_common_blue_signatures=rows)


def write_local(work):
    work.mkdir(parents=True,exist_ok=True)
    (work/'certificate.json').write_text(json.dumps(certificate(),indent=2,sort_keys=True)+'\n')
    core=[(a,b) for a,b in combinations(range(12),2) if core_red(a,b)]
    for name,n,edge in [('blue_pair14.edges',14,[]),('red_pair15.edges',15,[(12,13)])]:
        (work/name).write_text(str(n)+'\n'+''.join(f'{a} {b}\n' for a,b in core+edge))


def cases():
    premise()
    return [dict(id='blue',index=194,pair_red=False),dict(id='red',index=194,pair_red=True)]


def clauses(case):
    require(case in cases(),'exact pair-color case')
    if case['pair_red']:return [(166,)]
    return [(-166,)]+[(167+k,175+k) for k in range(8)]


def make(base,output,case):
    require(info(base)==BASE,'complete multiple base identity');tail=clauses(case)
    with base.open('rb') as f,output.open('wb') as g:
        require(f.readline()==b'p cnf 34320 617936\n','multiple base header')
        g.write(f'p cnf 34320 {617936+len(tail)}\n'.encode());shutil.copyfileobj(f,g)
        for row in tail:g.write((' '.join(map(str,row))+' 0\n').encode())
    return info(output)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args();write_local(a.work)
