#!/usr/bin/env python3
"""Guard the four local neighborhood bounds by each fixed vertex's empty signature."""
from itertools import combinations
from pathlib import Path
import hashlib
import json
import shutil
ROOT=Path(__file__).resolve().parent
PREVIOUS=ROOT.parent/'ramsey_r55_order3_eleven_neighborhood24'
BOUNDARY=ROOT.parent/'ramsey_r55_order3_eleven_core194_full'
FULL_PREVIOUS=ROOT.parent/'ramsey_r55_order3_eleven_local_bound_propagation'
BASE_SOURCE=ROOT.parent/'ramsey_r55_order3_eleven_empty_propagation'
PARENT=ROOT.parent/'ramsey_r55_order3_eleven_cycle_obstruction'
PINS={'result.json':'0876627e923713f8b87aa13beb8ee59506abb495232957afa041da8b035ea0a6',
      'verification.json':'9d34be3c2dff518a99852b1d5aea45dc0396fe94aac51a657951459d13737790',
      'boundary.json':'eb3ecc31d5a4d7e6ae6d17bb3ac5f5aec079e69707fe1a463b58afcc53fd908e'}


def require(ok,why):
    if not ok:raise ValueError(why)


def info(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while chunk:=f.read(1<<20):h.update(chunk)
    return dict(bytes=path.stat().st_size,sha256=h.hexdigest())


def cases():
    for name,pin in PINS.items():require(info(PREVIOUS/name)['sha256']==pin,'pinned local '+name)
    require(info(BOUNDARY/'boundary.json')['sha256']=='c7f5159da6ec5003385aa5487a4358b03b54c829912755412df84e6399011840','current whole boundary')
    require(info(BASE_SOURCE/'result.json')['sha256']=='536397d3b24e5d14a5144108be91933e72c85248dc5b4d0ab6231b16f37fcf44','unrestricted bases')
    local=json.loads((PREVIOUS/'result.json').read_text());verified=json.loads((PREVIOUS/'verification.json').read_text())
    boundary=json.loads((BOUNDARY/'boundary.json').read_text());bases=json.loads((BASE_SOURCE/'result.json').read_text())
    require(local['complete'] and verified['verified'] and not local['target_graph'],'complete local evidence')
    require(local['local_excluded']==[r['index'] for r in verified['cases'] if r['status']=='local_excluded']==[124,155,159,168,180],'five certified local obstructions')
    selected=[i for i in local['local_excluded'] if i in boundary['remaining_full_cores']]
    require(selected==[124,155,168,180],'exact four unresolved cores')
    rows=[]
    for index in selected:
        r=next(c for c in local['cases'] if c['index']==index)
        v=next(c for c in verified['cases'] if c['index']==index)
        base=next(c for c in bases['cases'] if c['index']==index)
        require(r['status']==v['status']=='local_excluded' and r['solver_code']==20 and r['replay']['verified'] and v['replay']['verified'],'two local full DRAT replays')
        require(r['formula']==v['formula'],'same local formula in both rounds')
        require(all(r[k]==v[k]==base[k] for k in ('index','bits','labeled','omitted')),'same literal red core')
        require(base['status']=='open' and len(base['omitted'])==2,'unrestricted two-anchor base')
        require(base['formula']['sha256']!=r['formula']['sha256'],'full base not local formula')
        rows.append({k:base[k] for k in ('index','bits','labeled','omitted','formula')})
    require(sum(c['labeled'] for c in rows)==1944,'four core label total')
    return rows


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
        require(f.readline()==b'p cnf 34300 617482\n','full base header')
        g.write(b'p cnf 34300 617832\n');shutil.copyfileobj(f,g)
        for row in clauses():g.write((' '.join(map(str,row))+' 0\n').encode())
    return info(output)
