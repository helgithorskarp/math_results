#!/usr/bin/env python3
"""Guard the derived Core194 bound by each fixed vertex's empty signature."""
from itertools import combinations
from pathlib import Path
import hashlib
import json
import shutil
ROOT=Path(__file__).resolve().parent
PREVIOUS=ROOT.parent/'ramsey_r55_order3_eleven_core194_maximal'
FULL_PREVIOUS=ROOT.parent/'ramsey_r55_order3_eleven_local_bound_propagation'
BASE_SOURCE=ROOT.parent/'ramsey_r55_order3_eleven_empty_propagation'
PARENT=ROOT.parent/'ramsey_r55_order3_eleven_cycle_obstruction'
PINS={'result.json':'f3bedff36c6adc13ca6da2939f92a14063c0eeb8d92086cd1e58f1b8b816dfeb',
      'verification.json':'577657fd087cd0069036a9d10f3c766864b3fbb41f220c7cf02f2314d7c9bd5e',
      'boundary.json':'82e98aabaec56602126eec754028269dd8bcb2cf467bd9299d076c1deea030bf'}


def require(ok,why):
    if not ok:raise ValueError(why)


def info(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while chunk:=f.read(1<<20):h.update(chunk)
    return dict(bytes=path.stat().st_size,sha256=h.hexdigest())


def cases():
    for name,pin in PINS.items():require(info(PREVIOUS/name)['sha256']==pin,'pinned maximal-branch '+name)
    require(info(FULL_PREVIOUS/'boundary.json')['sha256']=='9195e8c27426bd7829814c5e085fdd03fa623753faa6153a9654219576bfedd4','prior whole boundary')
    require(info(BASE_SOURCE/'result.json')['sha256']=='536397d3b24e5d14a5144108be91933e72c85248dc5b4d0ab6231b16f37fcf44','unrestricted bases')
    old=json.loads((PREVIOUS/'result.json').read_text());verified=json.loads((PREVIOUS/'verification.json').read_text())
    boundary=json.loads((PREVIOUS/'boundary.json').read_text());bases=json.loads((BASE_SOURCE/'result.json').read_text())
    require(old['complete'] and old['maximal_branch_excluded'] and verified['maximal_branch_excluded'] and not old['target_graph'],'complete branch verdict')
    require([r['kind'] for r in old['cases']]==[r['kind'] for r in verified['cases']]==['classification','extension'],'both parts of transferred refutation')
    for r,v in zip(old['cases'],verified['cases']):
        require(r['status']=='excluded' and r['solver_code']==20 and r['replay']['verified'] and v['replay']['verified'],'two imported full replays')
        require(r['formula']==v['formula'] and r['proof']==v['proof'],'same imported inputs and traces')
    require(boundary['new_maximal_branch_exclusions']==[194] and 194 in boundary['remaining_full_cores'],'open full Core194, closed maximal branch')
    base=next(r for r in bases['cases'] if r['index']==194)
    require(base['status']=='open' and base['bits']=='100110110110110100' and base['labeled']==81 and base['omitted']==[0,1,2,3],'literal Core194 identity')
    require(base['formula']==dict(bytes=24956496,sha256='2df3017147bd8cb5ceb6f561b8014a5b808e77db14fc6d9f3d6978b53d8c6490'),'complete unrestricted base')
    return [{k:base[k] for k in ('index','bits','labeled','omitted','formula')}]


def clauses():
    rows=[]
    for f in range(10):
        start=211+11*f;guard=list(range(start,start+4))
        rows.extend(tuple(guard)+selected for selected in combinations(range(start+4,start+11),4))
    require(len(rows)==len(set(rows))==350 and all(len(r)==8 for r in rows),'all ten guarded bounds')
    return rows


def make(base,output,case):
    require(info(base)==case['formula'],'unrestricted base identity')
    with base.open('rb') as f,output.open('wb') as g:
        require(f.readline()==b'p cnf 34320 617582\n','full base header')
        g.write(b'p cnf 34320 617932\n');shutil.copyfileobj(f,g)
        for row in clauses():g.write((' '.join(map(str,row))+' 0\n').encode())
    return info(output)
