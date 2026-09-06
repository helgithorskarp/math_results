#!/usr/bin/env python3
"""Propagate five local saturated-neighborhood obstructions to full extensions."""
from itertools import combinations
from pathlib import Path
import hashlib
import json
import shutil

ROOT=Path(__file__).resolve().parent
PREVIOUS=ROOT.parent/'ramsey_r55_order3_eleven_neighborhood24'
FULL_PREVIOUS=ROOT.parent/'ramsey_r55_order3_eleven_blue_bound_propagation'
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
        while b:=f.read(1<<20):h.update(b)
    return dict(bytes=path.stat().st_size,sha256=h.hexdigest())


def cases():
    for name,pin in PINS.items():require(info(PREVIOUS/name)['sha256']==pin,'pinned local '+name)
    require(info(FULL_PREVIOUS/'boundary.json')['sha256']=='999e0c36bbf87c466b816a262d91ca0ff37c86017c0f61c0f0e82378f51294ac','whole-core starting boundary')
    require(info(BASE_SOURCE/'result.json')['sha256']=='536397d3b24e5d14a5144108be91933e72c85248dc5b4d0ab6231b16f37fcf44','unrestricted bases')
    old=json.loads((PREVIOUS/'result.json').read_text());verified=json.loads((PREVIOUS/'verification.json').read_text())
    boundary=json.loads((PREVIOUS/'boundary.json').read_text());bases=json.loads((BASE_SOURCE/'result.json').read_text())
    require(old['complete'] and verified['verified'] and not old['target_graph'],'complete imported local verdict')
    selected=[r for r in old['cases'] if r['status']=='local_excluded']
    reviewed=[r for r in verified['cases'] if r['status']=='local_excluded']
    require([r['index'] for r in selected]==[r['index'] for r in reviewed]==old['local_excluded']==boundary['local_excluded'],'exact local exclusion cover')
    base_map={r['index']:r for r in bases['cases'] if r['status']=='open'};rows=[]
    for r,v in zip(selected,reviewed):
        base=base_map[r['index']]
        require(r['replay']['verified'] and v['replay']['verified'] and r['solver_code']==20,'two imported full DRAT replays')
        require(all(r[k]==v[k]==base[k] for k in ('index','bits','labeled','omitted')),'same literal red core')
        require(r['index'] in boundary['remaining_full_cores'],'currently unresolved full core')
        require(base['formula']['sha256']!=r['formula']['sha256'],'full base, not local24 formula')
        require(len(base['omitted'])==2,'all five have two complementary anchors')
        rows.append({k:base[k] for k in ('index','bits','labeled','omitted','formula')})
    require([r['index'] for r in rows]==[124,155,159,168,180] and sum(c['labeled'] for c in rows)==2268,'complete five-case totals')
    return rows


def clauses():
    rows=list(combinations(range(215,222),4))
    require(len(rows)==35 and len(set(rows))==35,'all positive four-subsets')
    return rows


def make(base,output,case):
    require(info(base)==case['formula'],'unrestricted complete base identity')
    with base.open('rb') as f,output.open('wb') as g:
        require(f.readline()==b'p cnf 34300 617482\n','full base header')
        g.write(b'p cnf 34300 617517\n');shutil.copyfileobj(f,g)
        for row in clauses():g.write((' '.join(map(str,row))+' 0\n').encode())
    return info(output)
